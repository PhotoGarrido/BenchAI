"""Contrato del timeout por llamada y del backoff de 429, sin red.

Un pool stealth en cola (Union Alpha, 16-09-2026: 27-229 s por llamada)
reventaba los 60 s que Concordia pone por defecto, y cada expiración se
repetía cuatro veces contra la misma cola. Tres promesas:

1. `PSICOAI_TIMEOUT_S` manda sobre el timeout que pase el experimento; sin
   la variable, el valor pasado queda intacto; un valor ilegible o ≤ 0 muere
   en el arranque.
2. Un 429 de OpenRouter espera dentro del grifo y se repite (antes solo NaN
   lo hacía; el 429 subía al RetryLanguageModel, que se rinde en un minuto).
3. Un 429 persistente acaba subiendo, no se queda esperando para siempre.
"""

import os
import unittest.mock as mock

import openai

import manifiesto
import model_factory

fallos = []


def caso(nombre, ok):
    print(f"  {'OK ' if ok else 'FALLO'} {nombre}")
    if not ok:
        fallos.append(nombre)


class _Mensaje:
    content = "42"


class _Eleccion:
    message = _Mensaje()


class RespuestaFalsa:
    id = "req-1"
    model = "stealth/union-alpha"
    choices = [_Eleccion()]
    usage = None


class ClienteFalso:
    """Falla las `fallos_iniciales` primeras llamadas con `error`."""

    def __init__(self, error=None, fallos_iniciales=1):
        self.error = error
        self.fallos_iniciales = fallos_iniciales
        self.llamadas = []

    @property
    def chat(self):
        return self

    @property
    def completions(self):
        return self

    def create(self, **kw):
        self.llamadas.append(kw)
        if self.error and len(self.llamadas) <= self.fallos_iniciales:
            raise self.error
        return RespuestaFalsa()


def modelo(proveedor="openrouter", error=None, fallos_iniciales=1):
    m = model_factory.NaNLanguageModel(
        "stealth/union-alpha", api_key="k", base_url="https://ejemplo.invalid",
        proveedor=proveedor)
    m._client = ClienteFalso(error, fallos_iniciales)
    return m


def chat(m, timeout=30):
    return m._chat("hola", max_tokens=100, temperature=0, top_p=1, seed=1,
                   timeout=timeout)


# ── 1. timeout por entorno ──────────────────────────────────────────────────
with mock.patch.object(manifiesto, "registrar", lambda e: None):
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop("PSICOAI_TIMEOUT_S", None)
        m = modelo()
        chat(m, timeout=30)
        caso("sin PSICOAI_TIMEOUT_S el timeout pasado llega intacto a la API",
             m._client.llamadas[0]["timeout"] == 30)
        caso("timeout_efectivo sin variable devuelve lo que recibe",
             model_factory.timeout_efectivo(45) == 45)

    with mock.patch.dict(os.environ, {"PSICOAI_TIMEOUT_S": "600"}):
        m = modelo()
        chat(m, timeout=30)
        caso("con PSICOAI_TIMEOUT_S=600 la API recibe 600 aunque el "
             "experimento pida 30",
             m._client.llamadas[0]["timeout"] == 600.0)

    for malo in ("abc", "0", "-5"):
        with mock.patch.dict(os.environ, {"PSICOAI_TIMEOUT_S": malo}):
            try:
                model_factory.timeout_efectivo(30)
                caso(f"PSICOAI_TIMEOUT_S={malo!r} rechazado en el arranque",
                     False)
            except SystemExit:
                caso(f"PSICOAI_TIMEOUT_S={malo!r} rechazado en el arranque",
                     True)

# ── 2. 429 de OpenRouter: espera dentro del grifo y repite ──────────────────
err429 = openai.RateLimitError("429", response=mock.Mock(status_code=429),
                               body=None)
esperas = []
with mock.patch.object(manifiesto, "registrar", lambda e: None), \
        mock.patch.object(model_factory.time, "sleep", esperas.append), \
        mock.patch.dict(os.environ, {}, clear=False):
    os.environ.pop("PSICOAI_TIMEOUT_S", None)
    m = modelo("openrouter", error=err429, fallos_iniciales=1)
    salida = chat(m)
    caso("429 en OpenRouter: espera y repite dentro del grifo",
         salida == "42" and len(m._client.llamadas) == 2
         and esperas == [model_factory.NaNLanguageModel._ESPERAS_429[0]])

    esperas.clear()
    m = modelo("nan", error=err429, fallos_iniciales=2)
    salida = chat(m)
    caso("429 en NaN conserva la escalera de esperas (5 s, 10 s)",
         salida == "42" and len(m._client.llamadas) == 3
         and esperas == list(model_factory.NaNLanguageModel._ESPERAS_429[:2]))

    # ── 3. un 429 persistente acaba subiendo ────────────────────────────────
    esperas.clear()
    n_esperas = len(model_factory.NaNLanguageModel._ESPERAS_429)
    m = modelo("openrouter", error=err429, fallos_iniciales=10_000)
    try:
        chat(m)
        caso("429 persistente sube tras agotar las esperas", False)
    except openai.RateLimitError:
        caso("429 persistente sube tras agotar las esperas",
             len(m._client.llamadas) == n_esperas + 1
             and len(esperas) == n_esperas)

if fallos:
    raise SystemExit(f"test_timeout: {len(fallos)} fallo(s): {fallos}")
print("test_timeout: OK")
