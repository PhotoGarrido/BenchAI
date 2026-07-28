"""Validación de contratos (revisión externa, hallazgo 7): los replays de los
episodios publicados y el escenario de ejemplo deben validar contra los JSON
Schema de `schemas/`. Complementa a los validadores JS de panel/visor (que
implementan un subconjunto): aquí valida el schema completo con jsonschema."""
import json
import pathlib

import jsonschema

RAIZ = pathlib.Path(__file__).parent.parent


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


def run():
    ok = True
    schema_replay = json.loads(
        (RAIZ / "schemas" / "replay.schema.json").read_text())
    schema_escenario = json.loads(
        (RAIZ / "schemas" / "scenario.schema.json").read_text())
    jsonschema.Draft7Validator.check_schema(schema_replay)
    jsonschema.Draft7Validator.check_schema(schema_escenario)
    ok &= _c(True, "los dos schemas son draft-07 válidos")

    for f in sorted(RAIZ.glob("episodios/*/replay.json")):
        try:
            jsonschema.validate(json.loads(f.read_text()), schema_replay)
            ok &= _c(True, f"replay válido: {f.parent.name}")
        except jsonschema.ValidationError as e:
            ok &= _c(False, f"replay INVÁLIDO {f.parent.name}: "
                            f"{e.message[:100]}")

    esc = RAIZ / "spike" / "episodio_el_centro.json"
    try:
        jsonschema.validate(json.loads(esc.read_text()), schema_escenario)
        ok &= _c(True, "escenario de ejemplo válido contra scenario.schema")
    except jsonschema.ValidationError as e:
        ok &= _c(False, f"escenario INVÁLIDO: {e.message[:100]}")

    # Un replay corrupto DEBE fallar (el contrato rechaza, no tolera).
    try:
        jsonschema.validate({"agentes": "no-es-lista", "eventos": []},
                            schema_replay)
        ok &= _c(False, "un replay corrupto debería rechazarse")
    except jsonschema.ValidationError:
        ok &= _c(True, "un replay corrupto se rechaza")
    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
