"""Tests del RunManifest (Fase 0.4 + revisión R3): cabecera con procedencia y
dependencias, solicitudes con timestamp, estado final garantizado por el
context manager (completed/failed), tolerancia a errores de serialización,
no-op sin activar, y el fallback de sample_choice sin imputación (hallazgo 4)."""
import json
import pathlib
import tempfile

import manifiesto
import model_factory


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


def run():
    ok = True
    manifiesto.activar_instancia(None)
    manifiesto.registrar({"x": 1})   # sin activar: no escribe ni revienta
    ok &= _c(True, "sin activar: no-op")

    with tempfile.TemporaryDirectory() as td:
        with manifiesto.RunManifest(td, {"modelo": "test"},
                                    hashes={"escenario": "abc"}):
            manifiesto.registrar({"modelo": "m", "prompt": "p",
                                  "respuesta": "r"})
            manifiesto.registrar({"modelo": "m", "error": "boom"})
            manifiesto.registrar({"raro": object()})   # no serializable
        cab = json.loads((pathlib.Path(td) / "manifest_run.json").read_text())
        ok &= _c(cab.get("commit") and cab.get("parser_version")
                 and cab["hashes"] == {"escenario": "abc"}
                 and "openai" in cab.get("dependencias", {}),
                 "cabecera con commit, parser, hashes y dependencias")
        ok &= _c(cab["status"] == "completed" and cab["solicitudes"] == 3
                 and cab["errores"] == 1,
                 "estado final completed con recuentos")
        lineas = [json.loads(l) for l in
                  (pathlib.Path(td) / "solicitudes.jsonl").open()]
        ok &= _c(len(lineas) == 3 and all("ts" in l for l in lineas),
                 "3 solicitudes con timestamp (incl. no-serializable)")

    with tempfile.TemporaryDirectory() as td:
        try:
            with manifiesto.RunManifest(td, {}):
                raise ValueError("bum")
        except ValueError:
            pass
        cab = json.loads((pathlib.Path(td) / "manifest_run.json").read_text())
        ok &= _c(cab["status"] == "failed"
                 and cab["exception_type"] == "ValueError",
                 "excepción → status failed con tipo registrado")

    # ── sample_choice sin imputación (hallazgo 4) ────────────────────────
    m = object.__new__(model_factory.NaNLanguageModel)
    m._model, m._proveedor = "falso", "test"
    m.sample_text = lambda *a, **k: "%% ilegible %%"
    try:
        model_factory.NaNLanguageModel.sample_choice(
            m, "q", ["golpear la puerta", "gritar", "salir"])
        ok &= _c(False, "sin opción neutra debía lanzar excepción")
    except model_factory.RespuestaIlegibleError:
        ok &= _c(True, "sample_choice sin neutra → RespuestaIlegibleError"
                       " (jamás un índice de acción real)")
    idx2, eleccion2, meta2 = model_factory.NaNLanguageModel.sample_choice(
        m, "q", ["golpear", "no hace nada", "gritar"])
    ok &= _c(idx2 == 1 and eleccion2 == "no hace nada"
             and meta2.get("choice_state") == "INVALIDA",
             "con neutra: índice y texto COHERENTES + INVALIDA registrada")
    manifiesto.activar_instancia(None)
    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
