#!/bin/bash
# La puerta de calidad completa de PsicoAI en un solo comando (clon limpio:
# crear antes spike/.venv e instalar requirements.txt + requirements-ci.txt,
# como documenta el README). Sale 1 al primer fallo.
set -e
cd "$(dirname "$0")/spike"
PY=${PY:-.venv/bin/python}
# F,W completos (auditoría R4, P2): antes solo se miraban los
# fatales E9/F63/F7/F82, así que imports muertos y f-strings sin
# placeholder pasaban. E501/E402/E741 quedan fuera a propósito
# (longitud de línea, load_dotenv antes de imports, nombres cortos).
# Sintaxis de los workflows de CI (06-08): un `name:` con dos puntos sin
# comillas dejo la CI en rojo de arranque durante una ronda entera sin que la
# puerta local se enterase — la puerta no vigilaba su propia infraestructura.
# Sin dependencias nuevas: el parser YAML del propio Python si esta, y si no,
# se avisa y se sigue (la CI real lo valida de todas formas).
"$PY" - <<'EOF' || { echo "FALLO: workflow de CI con YAML invalido"; exit 1; }
import pathlib, sys
try:
    import yaml
except ImportError:
    print("[aviso] PyYAML no instalado; salto la validacion de workflows")
    sys.exit(0)
for f in sorted(pathlib.Path("../.github/workflows").glob("*.yml")):
    try:
        yaml.safe_load(f.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        print(f"{f}: {e}")
        sys.exit(1)
    print(f"  {f.name}: YAML valido")
EOF

"$PY" -m ruff check . --select E9,F,W
"$PY" -m mypy --ignore-missing-imports --follow-imports=skip parsers.py artefactos.py manifiesto.py linter_contraste.py release_manifest.py incertidumbre.py generar_benchmark.py
"$PY" -m pip_audit -r requirements-ci.txt
# Runtime: pins directos sin resolver transitivas (torch hace impracticable
# la resolución completa; exclusión documentada en THIRD_PARTY_NOTICES.md).
"$PY" -m pip_audit --no-deps -r requirements.txt
for t in test_parsers test_parsers_tipados test_parsers_contrato test_manifiesto test_manifiesto_pool test_sensibles test_barrido_falso test_linter_contraste test_schemas test_robustez_determinista test_replay_privacidad test_gfinal_linter test_trazabilidad test_adjudicacion test_vigia test_version_unica; do
  echo "== $t =="; "$PY" "$t.py" > /dev/null || { echo "FALLO en $t"; exit 1; }
done
# El test XSS debe ejecutar TAMBIÉN la ampliación de sinks (reauditoría
# 31-07: era código muerto tras sys.exit y daba falso verde).
echo "== test_xss_estatico =="
XSS_LOG=$(mktemp)
"$PY" test_xss_estatico.py > "$XSS_LOG"
grep -q "ampliación de sinks: OK" "$XSS_LOG" || { echo "FALLO: la ampliación de sinks no se ejecutó"; exit 1; }
rm -f "$XSS_LOG"
"$PY" reprocesar.py --check
"$PY" reprocesar.py --check-publication
"$PY" release_manifest.py --verificar
"$PY" regenerar_publicacion.py --check
"$PY" generar_benchmark.py --check
"$PY" adjudicacion.py --check
"$PY" verificar_citas.py --check
"$PY" verificar_afirmaciones.py --check
"$PY" experimento_gfinal.py --linter
"$PY" run_spike.py --dry-run --steps 2 > /dev/null
# Sitio divulgativo: sus cifras se re-derivan de las fuentes canónicas y cada
# dato citado en prosa se verifica literal contra su informe. Si una fuente
# cambia y la web se queda con un número huérfano, esto lo tumba.
"$PY" ../web/generar_datos.py --check
echo "PUERTA COMPLETA: OK"
