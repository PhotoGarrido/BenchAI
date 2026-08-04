"""Fábrica de modelo LLM y embedder para el spike de PsicoAI.

Modos:
  - dry_run=True  → sin claves ni red: RandomChoiceLanguageModel + embedder hash.
  - dry_run=False → NaN (endpoint OpenAI-compatible, modelo qwen3.6) con un
                    wrapper propio blindado contra los tres vicios de un modelo
                    razonador dentro de Concordia:
                      1. content=None cuando el "thinking" agota max_tokens
                         → suelo de presupuesto + reintento con presupuesto doble,
                           y nunca se devuelve None.
                      2. rastros <think>...</think> incrustados → se eliminan.
                      3. thinking activado por defecto → se pide desactivarlo vía
                         chat_template_kwargs (inofensivo si el gateway lo ignora).
"""

import hashlib
import json
import os
import re
import sys
import threading
import time

import numpy as np
import openai

import manifiesto

# Grifo global hacia NaN: medido empíricamente (14-07-2026), a partir de ~4
# llamadas simultáneas el endpoint mete en cola con castigo (429+backoff:
# 8 llamadas en paralelo → 61 s frente a ~8 s en serie). Todas las instancias
# de modelo comparten este semáforo.
_SEMAFORO = threading.BoundedSemaphore(int(os.environ.get("NAN_MAX_CONCURRENTES", "3")))
# OpenRouter no tiene ese acantilado; grifo propio y más ancho.
_SEMAFORO_OR = threading.BoundedSemaphore(int(os.environ.get("OPENROUTER_MAX_CONCURRENTES", "8")))

# Límite de TASA de NaN (04-08-2026, medido en producción): 60 solicitudes/
# minuto por api_key («Limit type: requests. Current limit: 60»). El semáforo
# limita la CONCURRENCIA pero no la tasa: crónica y prisión (pools de 3-6)
# la reventaban y morían a 429 en cadena. Ventana deslizante global con
# margen; se aplica a cada solicitud FÍSICA del proveedor nan, reintentos
# incluidos.
_NAN_RPM = int(os.environ.get("NAN_RPM", "50"))
_VENTANA_NAN: list[float] = []
_VENTANA_LOCK = threading.Lock()


def _respetar_rpm_nan():
    while True:
        with _VENTANA_LOCK:
            ahora = time.monotonic()
            while _VENTANA_NAN and ahora - _VENTANA_NAN[0] > 60:
                _VENTANA_NAN.pop(0)
            if len(_VENTANA_NAN) < _NAN_RPM:
                _VENTANA_NAN.append(ahora)
                return
            espera = 60 - (ahora - _VENTANA_NAN[0]) + 0.1
        time.sleep(max(espera, 0.1))

_SYSTEM = (
    "You always continue sentences provided by the user and you never repeat "
    "what the user already said. Respond directly and concisely, with no meta "
    "commentary and no reasoning traces."
)

# E-portador (04-08): un experimento puede añadir un bloque al mensaje de
# sistema (p. ej. una política de moderación como PORTADOR de la orden).
# Afecta a todas las solicitudes posteriores del proceso y queda registrado
# verbatim (messages + sha256) en cada línea del manifiesto — el «prompt
# exacto» sigue siéndolo. Vacío por defecto: ningún experimento existente
# cambia ni un byte.
_SYSTEM_EXTRA = ""


def fijar_system_extra(texto: str) -> None:
    global _SYSTEM_EXTRA
    _SYSTEM_EXTRA = texto or ""
class RespuestaIlegibleError(RuntimeError):
    """El modelo no produjo una elección interpretable y no hay opción
    neutra: el run debe fallar visiblemente, nunca inventar una acción."""


_THINK_RE = re.compile(r"<think>.*?(?:</think>|$)", re.S)
_LETRAS = "abcdefghijklmnopqrstuvwxyz"


def _primer_json(texto: str) -> str | None:
    """Primer objeto JSON balanceado y válido dentro de un texto con adornos."""
    ini = texto.find("{")
    while ini != -1:
        profundidad = 0
        for i in range(ini, len(texto)):
            if texto[i] == "{":
                profundidad += 1
            elif texto[i] == "}":
                profundidad -= 1
                if profundidad == 0:
                    candidato = texto[ini:i + 1]
                    try:
                        json.loads(candidato)
                        return candidato
                    except ValueError:
                        break
        ini = texto.find("{", ini + 1)
    return None


def build_model(dry_run: bool, model_name: str | None = None):
    """Modelo listo para Concordia. `model_name` permite enrutar por rol
    (p. ej. protagonistas con NAN_MODEL y población con NAN_MODEL_LIGERO)."""
    if dry_run:
        from concordia.language_model import no_language_model

        return no_language_model.RandomChoiceLanguageModel()

    from concordia.language_model import retry_wrapper

    model_name = model_name or os.environ.get("NAN_MODEL")
    # Enrutado por proveedor: los IDs de OpenRouter llevan "/" (org/modelo);
    # los de NaN son planos (qwen3.6, gemma4...).
    if model_name and "/" in model_name:
        base_url = os.environ.get("OPENROUTER_BASE_URL",
                                  "https://openrouter.ai/api/v1")
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise SystemExit("Falta OPENROUTER_API_KEY en spike/.env.")
        model = NaNLanguageModel(model_name, api_key=api_key,
                                 base_url=base_url, proveedor="openrouter")
    else:
        base_url = os.environ.get("NAN_BASE_URL")
        api_key = os.environ.get("NAN_API_KEY")
        if not (base_url and api_key and model_name):
            raise SystemExit(
                "Faltan NAN_BASE_URL / NAN_API_KEY / NAN_MODEL. "
                "Copia .env.example a .env y rellénalo, o usa --dry-run."
            )
        model = NaNLanguageModel(model_name, api_key=api_key, base_url=base_url)
    model = retry_wrapper.RetryLanguageModel(model, retry_tries=4)
    max_calls = int(os.environ.get("PSICOAI_MAX_CALLS", "2000"))
    return LimiteFailClosed(model, max_calls=max_calls)


from concordia.language_model import language_model  # noqa: E402
from concordia.language_model import call_limit_wrapper  # noqa: E402


class LimiteDeLlamadasError(RuntimeError):
    """El presupuesto de llamadas del run se agotó. Fail-closed: el run se
    detiene visiblemente en vez de fabricar una acción."""


class LimiteFailClosed(call_limit_wrapper.CallLimitLanguageModel):
    """Fail-closed sobre el CallLimitLanguageModel de Concordia (G4
    producción, reauditoría 31-07): al agotar el presupuesto, el wrapper de
    la librería devuelve `''` en sample_text y `(0, responses[0], {})` en
    sample_choice — es decir, la PRIMERA acción real del menú, exactamente
    la clase de imputación P0.1 que se corrigió en la clase base. Aquí, en
    su lugar, se LANZA: un límite agotado nunca elige por el modelo."""

    def sample_text(self, prompt, **kwargs):
        if self._calls >= self._max_calls:
            raise LimiteDeLlamadasError(
                f"límite de {self._max_calls} llamadas agotado (sample_text):"
                " el run se detiene en vez de devolver cadena vacía")
        return super().sample_text(prompt, **kwargs)

    def sample_choice(self, prompt, responses, *, seed: int | None = None):
        if self._calls >= self._max_calls:
            raise LimiteDeLlamadasError(
                f"límite de {self._max_calls} llamadas agotado (sample_choice):"
                " el run se detiene en vez de devolver la opción 0")
        return super().sample_choice(prompt, responses, seed=seed)


class NaNLanguageModel(language_model.LanguageModel):
    """Modelo de NaN (OpenAI-compatible) endurecido para Concordia."""

    def __init__(self, model_name: str, *, api_key: str, base_url: str,
                 proveedor: str = "nan"):
        from openai import OpenAI

        self._model = model_name
        self._proveedor = proveedor
        self._sem = _SEMAFORO_OR if proveedor == "openrouter" else _SEMAFORO
        # max_retries=0 (reauditoría 31-07, G3): el SDK de OpenAI reintenta
        # por dentro por defecto (2 veces) y esos intentos FÍSICOS no pasan
        # por nuestro registro — el manifiesto los perdía. Con reintentos del
        # SDK apagados, el ÚNICO que reintenta es RetryLanguageModel, y cada
        # intento físico = una línea de solicitudes.jsonl.
        self._client = OpenAI(api_key=api_key, base_url=base_url,
                              max_retries=0)

    def _chat(self, prompt, *, max_tokens, temperature, top_p, seed, timeout):
        with self._sem:
            try:
                return self._chat_sin_grifo(
                    prompt, max_tokens=max_tokens, temperature=temperature,
                    top_p=top_p, seed=seed, timeout=timeout)
            except openai.BadRequestError as e:
                # Un 400 no es transitorio: reintentarlo igual no lo cura.
                # Degradación: sin extra_body (por si este modelo lo rechaza)
                # y presupuesto corto; si aún así falla, vacío antes que morir.
                print(f"[nan] 400 en {self._model} (prompt {len(prompt)}"
                      f" chars, max_tokens {max_tokens}): {str(e)[:300]}",
                      file=sys.stderr)
                try:
                    return self._chat_sin_grifo(
                        prompt, max_tokens=min(max_tokens, 2048),
                        temperature=temperature, top_p=top_p, seed=seed,
                        timeout=timeout, con_extra=False)
                except openai.BadRequestError as e2:
                    print(f"[nan] 400 persistente en {self._model}:"
                          f" {str(e2)[:300]} — devuelvo vacío",
                          file=sys.stderr)
                    return ""

    def _chat_sin_grifo(self, prompt, *, max_tokens, temperature, top_p,
                        seed, timeout, con_extra=True):
        # Mistral (y algún otro proveedor) rechaza con 400 cualquier top_p≠1
        # cuando la temperatura es 0: "top_p must be 1 when using greedy
        # sampling". Detectado en G2-A5 (25-07), donde degradaba a respuesta
        # vacía y perdía las 90 celdas del modelo.
        if temperature == 0:
            top_p = 1.0
        if self._proveedor == "nan":
            _respetar_rpm_nan()
        # El anti-thinking vía chat_template_kwargs es específico del gateway
        # de NaN (litellm). OpenRouter pasa extra_body al proveedor upstream,
        # que puede rechazarlo: allí no se envía nada y el suelo de tokens +
        # el strip de <think> bastan (los razonadores serios separan el
        # reasoning del content).
        extra = ({"chat_template_kwargs": {"enable_thinking": False}}
                 if con_extra and self._proveedor == "nan" else None)
        # RunManifest (Fase 0.4; revisión R3.3): cada solicitud FÍSICA queda
        # registrada con los MENSAJES COMPLETOS (system incluido) — «prompt
        # exacto» ahora lo es de verdad — y el modelo pedido vs devuelto.
        sistema = _SYSTEM + _SYSTEM_EXTRA
        base_evento = {"modelo": self._model, "proveedor": self._proveedor,
                       "max_tokens": max_tokens, "temperature": temperature,
                       "top_p": top_p, "seed": seed,
                       "messages": [{"role": "system", "content": sistema},
                                    {"role": "user", "content": prompt}],
                       "system_prompt_sha256": manifiesto.sha256_texto(sistema)}
        t0 = time.monotonic()
        try:
            respuesta = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                seed=seed,
                timeout=timeout,
                extra_body=extra,
            )
        except Exception as e:
            manifiesto.registrar(dict(
                base_evento, latencia_s=round(time.monotonic() - t0, 3),
                error=f"{type(e).__name__}: {str(e)[:500]}"))
            raise
        uso = getattr(respuesta, "usage", None)
        manifiesto.registrar(dict(
            base_evento, latencia_s=round(time.monotonic() - t0, 3),
            request_id=getattr(respuesta, "id", None),
            model_returned=getattr(respuesta, "model", None),
            respuesta=respuesta.choices[0].message.content,
            tokens={"prompt": getattr(uso, "prompt_tokens", None),
                    "completion": getattr(uso, "completion_tokens", None),
                    "total": getattr(uso, "total_tokens", None)}))
        return respuesta.choices[0].message.content

    def sample_text(
        self,
        prompt: str,
        *,
        max_tokens: int = language_model.DEFAULT_MAX_TOKENS,
        terminators=language_model.DEFAULT_TERMINATORS,
        temperature: float = language_model.DEFAULT_TEMPERATURE,
        top_p: float = language_model.DEFAULT_TOP_P,
        top_k: int = language_model.DEFAULT_TOP_K,  # la API OpenAI no lo usa
        timeout: float = language_model.DEFAULT_TIMEOUT_SECONDS,
        seed: int | None = None,
    ) -> str:
        # Suelo de presupuesto: si el gateway razona pese a todo, que quede
        # sitio para el contenido (doc de NaN: reasoning ~3k tokens).
        presupuesto = max(max_tokens, 4096)
        texto = None
        for _ in range(3):
            texto = self._chat(
                prompt,
                max_tokens=presupuesto,
                temperature=temperature,
                top_p=top_p,
                seed=seed,
                timeout=timeout,
            )
            if texto:
                break
            presupuesto = min(presupuesto * 2, 8192)  # pensó y se quedó sin sitio
        texto = _THINK_RE.sub("", texto or "").strip()
        # El GM pide el próximo "action spec" como JSON; los modelos pequeños
        # a veces lo adornan ("1). {...}") o enumeran VARIOS specs alternativos
        # ("1). {...} 2). {...}"). Extraemos el primer objeto JSON válido y
        # completo (y no aplicamos terminadores, que podrían partirlo).
        if '"call_to_action"' in texto:
            spec = _primer_json(texto)
            if spec is not None:
                return spec
        for term in terminators or ():
            corte = texto.find(term)
            if corte != -1:
                texto = texto[:corte]
        return texto

    def sample_choice(self, prompt: str, responses, *, seed: int | None = None):
        """Revisión externa (hallazgo 4): jamás se imputa la opción 0. Tras 8
        intentos ilegibles se elige una opción NEUTRA — la marcada como
        no-acción si el menú la trae, o la ÚLTIMA opción del menú extendido
        con una abstención explícita — y el evento queda registrado como
        INVALIDA en el manifiesto. Un fallo del proveedor nunca se convierte
        en silencio en la primera acción disponible."""
        NO_ACTION = "no hace nada (respuesta no interpretable del modelo)"
        opciones = "\n".join(
            f"({_LETRAS[i]}) {r}" for i, r in enumerate(responses)
        )
        pregunta = (
            f"{prompt}\n\nOptions:\n{opciones}\n\n"
            "Answer with only the letter of your chosen option in parentheses, "
            "for example: (a).\nAnswer: ("
        )
        import parsers
        for intento in range(8):
            texto = self.sample_text(
                pregunta,
                max_tokens=256,
                temperature=min(0.2 * intento, 1.0),
                seed=seed,
            )
            res = parsers.parsear_choice(texto, len(responses))
            if res.ok:
                return res.valor, responses[res.valor], {}
        neutras = [i for i, r in enumerate(responses)
                   if "no hace nada" in str(r).lower()
                   or "no hacer nada" in str(r).lower()]
        if neutras:
            idx = neutras[0]
            manifiesto.registrar({
                "modelo": self._model, "proveedor": self._proveedor,
                "choice_state": "INVALIDA", "fallback_option": "NO_ACTION",
                "n_opciones": len(responses), "indice_devuelto": idx})
            print("[nan] sample_choice ilegible tras 8 intentos → opción"
                  f" neutra del menú (índice {idx}, INVALIDA)",
                  file=sys.stderr)
            # Coherencia índice/texto garantizada: texto = responses[idx].
            return idx, responses[idx], {"choice_state": "INVALIDA"}
        # Auditoría 31-07 (P0.1): sin opción neutra NO existe un índice
        # honesto — devolver cualquiera ejecutaría una acción real con un
        # texto que no le corresponde. Se aborta con excepción tipada.
        manifiesto.registrar({
            "modelo": self._model, "proveedor": self._proveedor,
            "choice_state": "INVALIDA", "fallback_option": "ABORT",
            "n_opciones": len(responses)})
        raise RespuestaIlegibleError(
            f"sample_choice: 8 intentos ilegibles y el menú de "
            f"{len(responses)} opciones no contiene una neutra")


def build_embedder(dry_run: bool):
    if not dry_run:
        try:
            from sentence_transformers import SentenceTransformer

            st_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
            return lambda text: st_model.encode(text, show_progress_bar=False)
        except ImportError:
            print(
                "[aviso] sentence-transformers no instalado; uso embedder hash. "
                "La memoria asociativa funcionará pero sin similitud semántica real."
            )
    return _hash_embedder


def _hash_embedder(text: str) -> np.ndarray:
    # Determinista por texto: suficiente para que la memoria asociativa opere.
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    rng = np.random.default_rng(int.from_bytes(digest[:8], "little"))
    return rng.standard_normal(64).astype(np.float32)
