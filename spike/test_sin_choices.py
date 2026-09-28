"""Un 200 sin `choices` (error del upstream incrustado por OpenRouter) es
transitorio: se espera y se repite dentro del grifo, queda registrado como
intento fallido y NO tumba el run (Space Bunny Alpha, 28/29-09-2026)."""

import types
import unittest.mock as mock

import manifiesto
import model_factory

fallos = []


def caso(nombre, ok):
    print(f"  {'OK ' if ok else 'FALLO'} {nombre}")
    if not ok:
        fallos.append(nombre)


vacia = types.SimpleNamespace(
    choices=None, id="gen-1", model_extra={"error": {"code": 502}})
buena = types.SimpleNamespace(
    choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="Azul"))],
    id="gen-2", model="m", usage=None, model_extra={})
respuestas = [vacia, vacia, buena]

m = model_factory.NaNLanguageModel("x/y", api_key="k", base_url="http://z",
                                   proveedor="openrouter")
registros = []
with mock.patch.object(m._client.chat.completions, "create",
                       side_effect=lambda **kw: respuestas.pop(0)), \
        mock.patch.object(manifiesto, "registrar", registros.append), \
        mock.patch.object(model_factory.time, "sleep", lambda s: None):
    texto = m._chat("hola", max_tokens=16, temperature=0, top_p=1, seed=0,
                    timeout=10)

caso("tras dos 200 vacíos devuelve la respuesta buena", texto == "Azul")
caso("los tres intentos físicos quedan registrados", len(registros) == 3)
caso("los vacíos se registran como error con el detalle del upstream",
     all("RespuestaSinChoices" in r.get("error", "") and "502" in r["error"]
         for r in registros[:2]))

if fallos:
    raise SystemExit(f"test_sin_choices: {len(fallos)} fallo(s): {fallos}")
print("test_sin_choices: OK")
