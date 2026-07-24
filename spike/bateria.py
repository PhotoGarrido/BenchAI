"""Batería completa de PsicoAI sobre una cartera de modelos (test global).

Corre, por cada modelo, la misma suite que definió los perfiles de los 4 de
NaN — E1 Asch, E2 Milgram (+E3 vacuna), C1 crónica 42 días, C1-v2 × 3
semillas, y la trilogía de la prisión (P1, P1b, P2, P2b) — lanzando cada
experimento como subproceso (así cada uno conserva sus semáforos y su tope
de llamadas propios). Los modelos corren en paralelo, cada uno con su log.

Un sub-experimento que falle se registra y NO tumba el resto de la suite
de ese modelo.

Uso:
  python bateria.py --modelos a,b,c              # cartera completa
  python bateria.py --modelos m --rapido         # humo de la suite entera
"""

import argparse
import datetime
import json
import pathlib
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

AQUI = pathlib.Path(__file__).parent

# La suite en el orden de la batería original de NaN. Las semillas de la v2
# son las mismas de C1-v2 (15/16/17-07-2026) para comparación limpia.
SUITE = [
    ("asch", "experimento_asch.py", []),
    ("milgram", "experimento_milgram.py", []),
    ("milgram_vacuna", "experimento_milgram.py", ["--vacuna"]),
    ("cronica_v1", "experimento_cronica.py", []),
    ("cronica_v2_s715", "experimento_cronica.py", ["--v2", "--semilla", "20260715"]),
    ("cronica_v2_s716", "experimento_cronica.py", ["--v2", "--semilla", "20260716"]),
    ("cronica_v2_s717", "experimento_cronica.py", ["--v2", "--semilla", "20260717"]),
    ("prision_p1", "experimento_prision.py", []),
    ("prision_p1b", "experimento_prision.py", ["--coaching"]),
    ("prision_p2", "experimento_prision.py", ["--rebelion"]),
    ("prision_p2b", "experimento_prision.py", ["--ordenes"]),
]


def correr_suite(modelo, logdir, rapido=False):
    et = modelo.split("/")[-1][:22]
    log = logdir / (modelo.replace("/", "_") + ".log")
    resultados = []
    for nombre, script, extra in SUITE:
        cmd = [sys.executable, str(AQUI / script), "--modelo", modelo] + extra
        if rapido:
            cmd.append("--rapido")
        t0 = time.time()
        with log.open("a", encoding="utf-8") as f:
            f.write(f"\n===== {nombre} · {' '.join(cmd)} =====\n")
            f.flush()
            proc = subprocess.run(cmd, cwd=AQUI, stdout=f, stderr=f)
        dur = time.time() - t0
        estado = "OK" if proc.returncode == 0 else f"FALLO rc={proc.returncode}"
        print(f"[{et}] {nombre}: {estado} · {dur/60:.1f} min", flush=True)
        resultados.append({"experimento": nombre, "estado": estado,
                           "minutos": round(dur / 60, 1)})
    return {"modelo": modelo, "suite": resultados}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modelos", required=True,
                        help="lista separada por comas (IDs OpenRouter con /)")
    parser.add_argument("--rapido", action="store_true",
                        help="humo: cada experimento en modo piloto")
    args = parser.parse_args()

    modelos = [m.strip() for m in args.modelos.split(",") if m.strip()]
    logdir = AQUI / "resultados" / datetime.datetime.now().strftime(
        "bateria_%Y%m%d_%H%M%S")
    logdir.mkdir(parents=True, exist_ok=True)
    print(f"Batería de {len(modelos)} modelos · logs en {logdir}", flush=True)

    inicio = time.time()
    with ThreadPoolExecutor(max_workers=len(modelos)) as pool:
        estados = list(pool.map(
            lambda m: correr_suite(m, logdir, rapido=args.rapido), modelos))

    (logdir / "estado.json").write_text(
        json.dumps(estados, ensure_ascii=False, indent=2), encoding="utf-8")
    fallos = [(e["modelo"], r["experimento"]) for e in estados
              for r in e["suite"] if r["estado"] != "OK"]
    print(f"\nBatería terminada en {(time.time()-inicio)/3600:.1f} h · "
          f"fallos: {fallos if fallos else 'ninguno'}", flush=True)
    # Auditoría 24-07: una batería con fallos no debe salir con código 0
    # (el proceso padre y la CI deben poder detectarlo sin leer logs).
    if fallos:
        sys.exit(1)


if __name__ == "__main__":
    main()
