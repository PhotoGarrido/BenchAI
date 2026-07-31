#!/bin/bash
# La puerta de calidad completa de PsicoAI en un solo comando (clon limpio:
# crear antes spike/.venv e instalar requirements-ci). Sale 1 al primer fallo.
set -e
cd "$(dirname "$0")/spike"
PY=${PY:-.venv/bin/python}
$PY -m ruff check . --select E9,F63,F7,F82
$PY -m mypy --ignore-missing-imports --follow-imports=skip parsers.py artefactos.py manifiesto.py linter_contraste.py release_manifest.py
$PY -m pip_audit -r requirements-ci.txt
for t in test_parsers test_parsers_tipados test_manifiesto test_barrido_falso test_linter_contraste test_xss_estatico test_schemas; do
  echo "== $t =="; $PY $t.py > /dev/null || { echo "FALLO en $t"; exit 1; }
done
$PY reprocesar.py --check
$PY reprocesar.py --check-publication
$PY release_manifest.py --verificar
$PY experimento_gfinal.py --linter
$PY run_spike.py --dry-run --steps 2 > /dev/null
echo "PUERTA COMPLETA: OK"
