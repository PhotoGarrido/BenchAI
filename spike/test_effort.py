"""Contrato del nivel de razonamiento (`modelo#nivel`), sin red.

El effort es la VARIABLE INDEPENDIENTE de las mediciones a varios niveles:
lo que se prueba aquí es que no puede mentir. Cuatro promesas:

1. El sufijo se parte bien y un nivel desconocido muere en el arranque.
2. A la API se le pide el id LIMPIO (el sufijo es identidad nuestra).
3. Cada solicitud física queda registrada CON su nivel (G3): dos runs de
   condiciones distintas no pueden confundirse en los crudos.
4. Un 400 con effort NO degrada a una llamada sin razonamiento: mata el run.
   Sin esta puerta, un run etiquetado «#high» podría haber corrido en bajo.
"""

import unittest.mock as mock

import openai

import manifiesto
import model_factory

fallos = []


def caso(nombre, ok):
    print(f"  {'OK ' if ok else 'FALLO'} {nombre}")
    if not ok:
        fallos.append(nombre)


# ── 1. partición del sufijo ─────────────────────────────────────────────────
caso("id sin sufijo pasa intacto",
     model_factory.partir_effort("x-ai/grok-4.5") == ("x-ai/grok-4.5", None))
caso("id con sufijo se parte",
     model_factory.partir_effort("stealth/ox-alpha#high")
     == ("stealth/ox-alpha", "high"))
caso("None no revienta", model_factory.partir_effort(None) == (None, None))
for malo in ("stealth/ox-alpha#altísimo", "stealth/ox-alpha#HIGH", "#high"):
    try:
        model_factory.partir_effort(malo)
        caso(f"«{malo}» rechazado en el arranque", False)
    except SystemExit:
        caso(f"«{malo}» rechazado en el arranque", True)


# ── doble de la API: captura lo que se le pide ──────────────────────────────
class _Mensaje:
    content = "42"


class _Eleccion:
    message = _Mensaje()


class RespuestaFalsa:
    id = "req-1"
    model = "stealth/ox-alpha"
    choices = [_Eleccion()]
    usage = None


class ClienteFalso:
    def __init__(self, error=None):
        self.error = error
        self.llamadas = []

    @property
    def chat(self):
        return self

    @property
    def completions(self):
        return self

    def create(self, **kw):
        self.llamadas.append(kw)
        if self.error and len(self.llamadas) == 1:
            raise self.error
        return RespuestaFalsa()


def modelo_con(effort, error=None):
    m = model_factory.NaNLanguageModel(
        "stealth/ox-alpha", api_key="k", base_url="https://ejemplo.invalid",
        proveedor="openrouter", effort=effort)
    m._client = ClienteFalso(error)
    return m


# ── 2 y 3. id limpio a la API, nivel en extra_body y en el manifiesto ───────
eventos = []
with mock.patch.object(manifiesto, "registrar", eventos.append):
    m = modelo_con("high")
    m._chat("hola", max_tokens=100, temperature=0, top_p=1, seed=1, timeout=30)
    kw = m._client.llamadas[0]
    caso("a la API se le pide el id LIMPIO, sin el sufijo",
         kw["model"] == "stealth/ox-alpha")
    caso("el nivel viaja en extra_body",
         (kw.get("extra_body") or {}).get("reasoning_effort") == "high")
    caso("el manifiesto registra el nivel de cada solicitud",
         eventos and eventos[-1].get("reasoning_effort") == "high")

    eventos.clear()
    m = modelo_con(None)
    m._chat("hola", max_tokens=100, temperature=0, top_p=1, seed=1, timeout=30)
    kw = m._client.llamadas[0]
    caso("sin effort no se envía el parámetro",
         "reasoning_effort" not in (kw.get("extra_body") or {}))
    caso("sin effort el manifiesto lo registra como None",
         eventos and eventos[-1].get("reasoning_effort") is None)

# ── 4. un 400 con effort mata el run; sin effort, degrada como antes ────────
err = openai.BadRequestError("400", response=mock.Mock(status_code=400),
                             body=None)
with mock.patch.object(manifiesto, "registrar", lambda e: None):
    try:
        modelo_con("high", error=err)._chat(
            "hola", max_tokens=100, temperature=0, top_p=1, seed=1, timeout=30)
        caso("400 con effort mata el run (no degrada en silencio)", False)
    except SystemExit as e:
        caso("400 con effort mata el run (no degrada en silencio)",
             "reasoning_effort" in str(e))

    m = modelo_con(None, error=err)
    salida = m._chat("hola", max_tokens=100, temperature=0, top_p=1, seed=1,
                     timeout=30)
    caso("400 sin effort conserva la degradación de siempre",
         salida == "42" and len(m._client.llamadas) == 2)

if fallos:
    raise SystemExit(f"test_effort: {len(fallos)} fallo(s): {fallos}")
print("test_effort: OK")
