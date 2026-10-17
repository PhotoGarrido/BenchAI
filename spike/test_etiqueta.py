"""Contrato de la etiqueta de medición (`modelo@etiqueta`), sin red.

1. Se parte bien, también combinada con `#nivel`; una etiqueta inválida muere.
2. A la API se le pide el id LIMPIO.
3. Cada solicitud física registra la etiqueta (dos versiones del mismo id no
   se confunden en los crudos).
"""
import os
import types
import unittest.mock as mock

import manifiesto
import model_factory

fallos = []


def caso(nombre, ok):
    print(f"  {'OK ' if ok else 'FALLO'} {nombre}")
    if not ok:
        fallos.append(nombre)


print("1. partición")
caso("sin etiqueta", model_factory.partir_etiqueta("gemma4") == ("gemma4", None))
caso("con etiqueta", model_factory.partir_etiqueta("deepseek-v4-flash@v4.2") == ("deepseek-v4-flash", "v4.2"))
base, eff = model_factory.partir_effort("x-ai/grok@2026-10#low")
caso("combinada con #nivel", model_factory.partir_etiqueta(base) == ("x-ai/grok", "2026-10") and eff == "low")
for malo in ("@v4", "modelo@", "modelo@v 4"):
    try:
        model_factory.partir_etiqueta(malo)
        caso(f"rechaza «{malo}»", False)
    except SystemExit:
        caso(f"rechaza «{malo}»", True)

print("2-3. id limpio y registro")
eventos = []
resp = types.SimpleNamespace(
    choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="A"))],
    usage=types.SimpleNamespace(prompt_tokens=1, completion_tokens=1, total_tokens=2),
    id="r1", model="deepseek-v4-flash")
with mock.patch.dict(os.environ, {"NAN_BASE_URL": "http://x", "NAN_API_KEY": "k"}), \
        mock.patch.object(manifiesto, "registrar", eventos.append), \
        mock.patch("openai.resources.chat.completions.Completions.create",
                   return_value=resp) as crear:
    m = model_factory.build_model(False, "deepseek-v4-flash@v4.2")
    m.sample_text("hola", max_tokens=5)
caso("la API recibe el id limpio", crear.call_args.kwargs["model"] == "deepseek-v4-flash")
caso("la solicitud registra la etiqueta", eventos and eventos[-1].get("etiqueta_medicion") == "v4.2")

if fallos:
    raise SystemExit(f"{len(fallos)} fallo(s): {fallos}")
print("todo OK")
