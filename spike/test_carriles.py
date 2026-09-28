"""Contrato de los carriles de la batería (BATERIA_CARRILES), sin red.

1. Con N carriles corren TODOS los sub-experimentos pendientes, cada uno una
   vez, y estado.json conserva el orden canónico de la SUITE.
2. La tasa de NaN por clave se reparte: cada carril recibe NAN_RPM / N.
3. La reanudación sigue saltando lo ya hecho.
4. Un carril que falla no tumba a los demás.
"""

import json
import os
import pathlib
import subprocess
import tempfile
import threading
import unittest.mock as mock

import bateria

fallos = []


def caso(nombre, ok):
    print(f"  {'OK ' if ok else 'FALLO'} {nombre}")
    if not ok:
        fallos.append(nombre)


llamadas, entornos, lock = [], [], threading.Lock()


def falso_run(cmd, cwd, stdout, stderr, timeout, env):
    with lock:
        llamadas.append(cmd)
        entornos.append(env.get("NAN_RPM"))
    rc = 1 if "--ordenes" in cmd else 0
    return subprocess.CompletedProcess(cmd, rc)


with tempfile.TemporaryDirectory() as d, \
        mock.patch.dict(os.environ, {"BATERIA_CARRILES": "3",
                                     "NAN_RPM": "50"}), \
        mock.patch.object(bateria.subprocess, "run", falso_run):
    logdir = pathlib.Path(d)
    (logdir / "progreso.jsonl").write_text(
        json.dumps({"modelo": "m", "experimento": "asch"}) + "\n")
    r = bateria.correr_suite("m", logdir)
    nombres = [n for n, _, _ in bateria.SUITE]
    caso("estado en orden canónico de la SUITE",
         [x["experimento"] for x in r["suite"]] == nombres)
    caso("asch se salta por reanudación y el resto corre una vez",
         len(llamadas) == len(nombres) - 1)
    caso("cada carril recibe NAN_RPM 50 // 3 = 16",
         set(entornos) == {"16"})
    caso("el fallo de P2b no tumba al resto",
         [x["estado"] for x in r["suite"]].count("OK") == len(nombres) - 1)
    hechos = [json.loads(linea) for linea in
              (logdir / "progreso.jsonl").read_text().splitlines()]
    caso("progreso.jsonl registra los 12 OK sin líneas rotas",
         len(hechos) == len(nombres) - 1)
    caso("un log por sub-experimento con carriles",
         (logdir / "m__milgram.log").exists())

caso("sin carriles no se toca NAN_RPM",
     "NAN_RPM" not in bateria.entorno_carril(1, {}))

if fallos:
    raise SystemExit(f"test_carriles: {len(fallos)} fallo(s): {fallos}")
print("test_carriles: OK")
