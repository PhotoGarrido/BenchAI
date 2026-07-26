"""Test del RunManifest (Fase 0.4): cabecera con procedencia, solicitudes
append-only con timestamp, y no-op absoluto si nadie llamó a activar()."""
import json
import pathlib
import tempfile

import manifiesto


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


def run():
    ok = True
    manifiesto._FICHERO = None
    manifiesto.registrar({"x": 1})   # sin activar: no escribe ni revienta
    ok &= _c(manifiesto._FICHERO is None, "sin activar: no-op")

    with tempfile.TemporaryDirectory() as td:
        manifiesto.activar(td, {"modelo": "test"})
        manifiesto.registrar({"modelo": "m", "prompt": "p", "respuesta": "r"})
        manifiesto.registrar({"modelo": "m", "prompt": "p", "error": "boom"})
        cab = json.loads((pathlib.Path(td) / "manifest_run.json").read_text())
        ok &= _c(cab.get("commit") and cab.get("parser_version")
                 and cab.get("args") == {"modelo": "test"},
                 "cabecera con commit, parser_version y args")
        lineas = [json.loads(l) for l in
                  (pathlib.Path(td) / "solicitudes.jsonl").open()]
        ok &= _c(len(lineas) == 2 and all("ts" in l for l in lineas),
                 "2 solicitudes físicas con timestamp")
        ok &= _c(lineas[1].get("error") == "boom",
                 "los errores también quedan registrados")
    manifiesto._FICHERO = None
    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
