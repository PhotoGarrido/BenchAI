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

    # TODOS los escenarios versionados del repo cumplen el contrato,
    # incluido el integrado del runner (reauditoría 31-07, P0.3).
    import run_spike
    validador = jsonschema.Draft7Validator(schema_escenario)
    escenarios = [("episodio_el_centro.json",
                   json.loads((RAIZ / "spike" /
                               "episodio_el_centro.json").read_text())),
                  ("escenario_test.json",
                   json.loads((RAIZ / "spike" /
                               "escenario_test.json").read_text())),
                  ("ESCENARIO_DEFECTO (integrado)",
                   run_spike.ESCENARIO_DEFECTO)]
    for nombre, esc in escenarios:
        errores = list(validador.iter_errors(esc))
        ok &= _c(not errores, f"escenario válido: {nombre}"
                 + (f" — {errores[0].message[:80]}" if errores else ""))

    # `version` está DEFINIDA en el schema (const 1): ausente, null, texto,
    # otro entero o lista se rechazan — antes se requería sin definirse y
    # cualquier valor pasaba (P0.3).
    base = json.loads((RAIZ / "spike" / "escenario_test.json").read_text())
    sin_version = {k: v for k, v in base.items() if k != "version"}
    ok &= _c(bool(list(validador.iter_errors(sin_version))),
             "escenario SIN version se rechaza")
    for v in (None, "1", 2, [1]):
        ok &= _c(bool(list(validador.iter_errors(dict(base, version=v)))),
                 f"version={v!r} se rechaza (solo el entero 1 es válido)")

    # Export del panel: la forma EXACTA que produce construirConfig() —
    # claves y tipos copiados de panel/app.js — valida contra el schema
    # (la reauditoría demostró que el panel exportaba escenarios que el
    # motor rechazaba por omitir version).
    export_panel = {
        "version": 1, "titulo": "t", "premisa": "p", "entorno": "sala_comun",
        "reglas": "", "pasos": 8, "agentes_total": 4,
        "variables_sensibles": False,
        "protagonistas": [{
            "nombre": "Ana", "rol": "directora", "objetivo": "o",
            "trasfondo": "",
            "demografia": {"edad": 40, "genero": "mujer",
                           "origen_cultural": "sin especificar",
                           "nse": "medio", "educacion": "media"},
            "big5": {"o": 50, "c": 50, "e": 50, "a": 50, "n": 50},
            "avanzados": {"ideologia": 50, "religiosidad": 50,
                          "antiguedad": 50, "salud": 50, "atractivo": 50,
                          "idioma": ""},
            "color": "#e4572e"}],
        "poblacion": {
            "n": 1, "modo": "reglas", "semilla": "s",
            "demografia": {"edad": [25, 60], "pct_mujeres": 50,
                           "incluir_no_binarias": False,
                           "origenes_culturales": [], "nse_media": 50,
                           "educacion_media": 50},
            "big5_media": {"o": 50, "c": 50, "e": 50, "a": 50, "n": 50},
            "variedad": 30, "cuotas_rol": [], "subgrupos": [],
            "correlaciones": {"amabilidad_extraversion": 0,
                              "apertura_responsabilidad": 0},
            "mas_atributos": {"ideologia_media": 50,
                              "religiosidad_media": 50,
                              "antiguedad_media": 50, "salud_media": 50,
                              "atractivo_media": 50, "pct_otra_lengua": 0},
            "descripcion_ia": "",
            "agentes_generados": [{
                "nom": "Gael Rey", "rol": "Residentes", "sub": "—",
                "edad": 40, "gen": "hombre", "ori": "local", "nse": "medio",
                "edu": "media", "idi": "castellano",
                "b": {"o": 50, "c": 50, "e": 50, "a": 50, "n": 50},
                "b2": {"ideo": 50, "reli": 50, "anti": 50, "salud": 50,
                       "atr": 50}}]},
        "variantes": [{"nombre": "v",
                       "cambios": [{"param": "pctMuj", "op": "fijar",
                                    "val": 80}]}],
    }
    errores = list(validador.iter_errors(export_panel))
    ok &= _c(not errores, "la forma que exporta el panel (construirConfig)"
             " valida contra el schema"
             + (f" — {errores[0].message[:80]}" if errores else ""))
    # y panel/app.js EMITE y COMPRUEBA la versión (contrato compartido).
    panel_js = (RAIZ / "panel" / "app.js").read_text(encoding="utf-8")
    ok &= _c("VERSION_ESCENARIO = 1" in panel_js
             and "version: VERSION_ESCENARIO" in panel_js
             and "cfg.version !== VERSION_ESCENARIO" in panel_js,
             "panel/app.js emite version y la valida antes de descargar")

    # Un replay corrupto DEBE fallar (el contrato rechaza, no tolera).
    try:
        jsonschema.validate({"agentes": "no-es-lista", "eventos": []},
                            schema_replay)
        ok &= _c(False, "un replay corrupto debería rechazarse")
    except jsonschema.ValidationError:
        ok &= _c(True, "un replay corrupto se rechaza")

    # Exportador (reauditoría 31-07, P1.6): un lugar inventado SIN actor
    # identificable emite constraint_violation SIN la clave agente (nunca
    # null) y el replay resultante valida contra el schema.
    import export_replay
    evs = export_replay._eventos_movimiento(
        "Alguien se dirige a la cocina sin que se sepa quién.",
        ["Marta Ibanez"], None, {"Marta Ibanez": "a0"})
    ok &= _c(len(evs) == 1 and evs[0]["tipo"] == "constraint_violation"
             and "agente" not in evs[0],
             "lugar inventado sin actor → constraint_violation sin clave"
             " agente")
    replay_borde = {
        "version": 1,
        "meta": {"titulo": "t", "descripcion": "", "fecha": "",
                 "fuente": "concordia"},
        "agentes": [{"id": "a0", "nombre": "Marta Ibanez", "rol": "",
                     "color": "#e4572e"}],
        "eventos": evs + [{"tipo": "dialogo", "atribucion": "ambigua",
                           "texto": "hola", "texto_crudo": "?? -- «hola»"}],
    }
    export_replay.validar_contra_schema(replay_borde, "borde")
    ok &= _c(True, "replay de borde (sin actor + diálogo ambiguo) valida")
    # y el exportador RECHAZA antes de escribir lo que el schema rechaza.
    try:
        export_replay.validar_contra_schema(
            {"version": 1, "meta": {"titulo": "t", "descripcion": "",
                                    "fecha": "", "fuente": "concordia"},
             "agentes": [],
             "eventos": [{"tipo": "constraint_violation", "texto": "x",
                          "agente": None}]}, "agente-null")
        ok &= _c(False, "agente:null debía rechazarse antes de escribir")
    except RuntimeError:
        ok &= _c(True, "validar_contra_schema aborta ante agente:null"
                 " (nada inválido llega al disco)")
    # El RUNNER debe rechazar un escenario corrupto ANTES de construir
    # modelos (P0.3): se ejecuta run_spike con un config inválido y sin
    # claves; si intentara abrir proveedor fallaría con otro mensaje.
    import subprocess
    import sys as _sys
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        f.write('{"version": 1, "agentes": "no-es-lista"}')
        corrupto = f.name
    r = subprocess.run([_sys.executable, "run_spike.py", "--config", corrupto,
                        "--dry-run", "--steps", "1"],
                       cwd=pathlib.Path(__file__).parent,
                       capture_output=True, text=True)
    ok &= _c(r.returncode != 0 and "Escenario inválido" in
             (r.stderr + r.stdout),
             "run_spike rechaza un escenario corrupto antes de todo")
    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
