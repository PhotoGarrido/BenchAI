#!/bin/bash
# La puerta de calidad completa de PsicoAI en un solo comando (clon limpio:
# crear antes spike/.venv e instalar requirements.txt + requirements-ci.txt,
# como documenta el README). Sale 1 al primer fallo.
set -e
cd "$(dirname "$0")/spike"
PY=${PY:-.venv/bin/python}
"$PY" -m ruff check . --select E9,F63,F7,F82
"$PY" -m mypy --ignore-missing-imports --follow-imports=skip parsers.py artefactos.py manifiesto.py linter_contraste.py release_manifest.py
"$PY" -m pip_audit -r requirements-ci.txt
# Runtime: pins directos sin resolver transitivas (torch hace impracticable
# la resolución completa; exclusión documentada en THIRD_PARTY_NOTICES.md).
"$PY" -m pip_audit --no-deps -r requirements.txt
for t in test_parsers test_parsers_tipados test_parsers_contrato test_manifiesto test_manifiesto_pool test_sensibles test_barrido_falso test_linter_contraste test_schemas test_robustez_determinista test_replay_privacidad test_gfinal_linter test_trazabilidad test_adjudicacion test_vigia; do
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
"$PY" experimento_gfinal.py --linter
"$PY" run_spike.py --dry-run --steps 2 > /dev/null
echo "PUERTA COMPLETA: OK"
