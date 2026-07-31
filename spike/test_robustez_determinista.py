"""Determinismo entre procesos del análisis de robustez (reauditoría 31-07,
P1.10): la MISMA seed debe producir los MISMOS bytes de
resultados/gfinal_robustez.json aunque cambie PYTHONHASHSEED — la regresión
demostrada era que `con.keys() & sin.keys()` dependía del hash de proceso y
los IC del bootstrap emparejado variaban entre ejecuciones.

Ejecuta analizar_gfinal_robustez.py DOS veces en procesos separados con
PYTHONHASHSEED distinto y afirma: (1) mismos bytes entre ambas, (2) mismos
bytes que el artefacto versionado (fijado además por release_manifest).

Offline (fixtures versionados), sin claves y sin red: apto para CI.

Uso: python test_robustez_determinista.py
"""

import hashlib
import os
import pathlib
import subprocess
import sys

AQUI = pathlib.Path(__file__).parent
ARTEFACTO = AQUI / "resultados" / "gfinal_robustez.json"


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


def _sha():
    return hashlib.sha256(ARTEFACTO.read_bytes()).hexdigest()


def run():
    ok = True
    original = _sha()
    hashes = []
    for seed in ("1", "424242"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        r = subprocess.run([sys.executable, "analizar_gfinal_robustez.py"],
                           cwd=AQUI, env=env, capture_output=True, text=True)
        ok &= _c(r.returncode == 0,
                 f"PYTHONHASHSEED={seed}: el análisis termina bien")
        hashes.append(_sha())
    ok &= _c(hashes[0] == hashes[1],
             "mismos bytes entre procesos con PYTHONHASHSEED distinto")
    ok &= _c(hashes[-1] == original,
             "la regeneración reproduce el artefacto versionado byte a byte")
    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
