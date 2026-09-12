"""Batería completa de PsicoAI sobre una cartera de modelos (test global).

Corre, por cada modelo, la suite íntegra del octógono v0.4 — E1 Asch,
E2 Milgram (+E3 vacuna), C1 crónica 42 días, C1-v2 × 3 semillas, la
trilogía de la prisión (P1, P1b, P2, P2b), N2 denuncia y N3b sicofancia
de opinión — lanzando cada experimento como subproceso (así cada uno
conserva sus semáforos y su tope de llamadas propios). Los modelos corren
en paralelo, cada uno con su log.

Un sub-experimento que falle se registra y NO tumba el resto de la suite
de ese modelo.

Uso:
  python bateria.py --modelos a,b,c              # cartera completa
  python bateria.py --modelos m --rapido         # humo de la suite entera
"""

import argparse
import datetime
import json
import os
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
    # v0.4: la batería alcanza al octógono. N2 y N3b se midieron en agosto
    # como runs sueltos cableados a mano por denuncia_runs.json y
    # sicofancia_runs.json; desde aquí un alta nueva los corre en el mismo
    # batch y alta.py hace el cableado. Las carteras históricas no se tocan.
    ("denuncia", "experimento_denuncia.py", []),
    ("sicofancia_op", "experimento_sicofancia_op.py", []),
]


def _progreso(logdir):
    """Sub-experimentos ya completados en este batch (runtime-state releíble,
    idea adoptada de HERMES/PRISMA 31-07: la continuidad no depende de la
    memoria de nadie sino de releer lo que quedó escrito)."""
    f = logdir / "progreso.jsonl"
    if not f.exists():
        return set()
    return {(j["modelo"], j["experimento"])
            for j in (json.loads(l) for l in f.open(encoding="utf-8"))}


def correr_suite(modelo, logdir, rapido=False):
    et = modelo.split("/")[-1][:22]
    log = logdir / (modelo.replace("/", "_") + ".log")
    hechos = _progreso(logdir)
    resultados = []
    for nombre, script, extra in SUITE:
        if (modelo, nombre) in hechos:
            print(f"[{et}] {nombre}: ya completado (reanudación) — se salta",
                  flush=True)
            resultados.append({"experimento": nombre, "estado": "OK",
                               "minutos": 0.0, "reanudado": True})
            continue
        # Aislamiento por batch (auditoría): cada run escribe DENTRO del
        # directorio de esta batería — un humo posterior ya no puede pisar ni
        # mezclarse con un run completo en resultados/ raíz.
        cmd = [sys.executable, str(AQUI / script), "--modelo", modelo,
               "--out", str(logdir)] + extra
        if rapido:
            cmd.append("--rapido")
        t0 = time.time()
        # Timeout por subexperimento (reauditoría): un run colgado no bloquea
        # la batería entera. Configurable por env; 0 = sin límite.
        timeout = int(os.environ.get("BATERIA_TIMEOUT_S", "5400")) or None
        with log.open("a", encoding="utf-8") as f:
            f.write(f"\n===== {nombre} · {' '.join(cmd)} =====\n")
            f.flush()
            try:
                proc = subprocess.run(cmd, cwd=AQUI, stdout=f, stderr=f,
                                      timeout=timeout)
                rc = proc.returncode
            except subprocess.TimeoutExpired:
                f.write(f"\n[TIMEOUT tras {timeout}s]\n")
                rc = 124
        dur = time.time() - t0
        estado = "OK" if rc == 0 else f"FALLO rc={rc}"
        print(f"[{et}] {nombre}: {estado} · {dur/60:.1f} min", flush=True)
        resultados.append({"experimento": nombre, "estado": estado,
                           "minutos": round(dur / 60, 1)})
        if rc == 0:
            with (logdir / "progreso.jsonl").open("a", encoding="utf-8") as f:
                f.write(json.dumps({"modelo": modelo, "experimento": nombre},
                                   ensure_ascii=False) + "\n")
    return {"modelo": modelo, "suite": resultados}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modelos", required=True,
                        help="lista separada por comas (IDs OpenRouter con /)")
    parser.add_argument("--rapido", action="store_true",
                        help="humo: cada experimento en modo piloto")
    parser.add_argument("--reanudar", default=None,
                        help="ruta de un bateria_*/ previo: salta los"
                             " sub-experimentos ya completados (progreso.jsonl)")
    args = parser.parse_args()

    modelos = [m.strip() for m in args.modelos.split(",") if m.strip()]
    if args.reanudar:
        logdir = pathlib.Path(args.reanudar)
        if not logdir.is_dir():
            raise SystemExit(f"--reanudar: no existe {logdir}")
    else:
        logdir = AQUI / "resultados" / datetime.datetime.now().strftime(
            "bateria_%Y%m%d_%H%M%S_%f")
    logdir.mkdir(parents=True, exist_ok=True)
    print(f"Batería de {len(modelos)} modelos · logs en {logdir}", flush=True)

    # Manifiesto de procedencia (auditoría): commit, argumentos, entorno.
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=AQUI,
                                capture_output=True, text=True).stdout.strip()
    except OSError:
        commit = "desconocido"
    manifiesto = {
        "batch_id": logdir.name,
        "commit": commit,
        "python": sys.version.split()[0],
        "modelos": modelos,
        "rapido": args.rapido,
        "suite": [n for n, _, _ in SUITE],
        "inicio": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    (logdir / "manifest.json").write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2), encoding="utf-8")

    inicio = time.time()
    # Tope configurable de modelos en paralelo (reauditoría): por defecto uno
    # por modelo, pero acotable para no saturar el proveedor.
    tope = int(os.environ.get("BATERIA_MAX_MODELOS", "0")) or len(modelos)
    with ThreadPoolExecutor(max_workers=min(tope, len(modelos))) as pool:
        estados = list(pool.map(
            lambda m: correr_suite(m, logdir, rapido=args.rapido), modelos))

    (logdir / "estado.json").write_text(
        json.dumps(estados, ensure_ascii=False, indent=2), encoding="utf-8")
    fallos = [(e["modelo"], r["experimento"]) for e in estados
              for r in e["suite"] if r["estado"] != "OK"]
    manifiesto["fin"] = datetime.datetime.now().isoformat(timespec="seconds")
    manifiesto["fallos"] = [list(f) for f in fallos]
    manifiesto["completo"] = not fallos
    (logdir / "manifest.json").write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nBatería terminada en {(time.time()-inicio)/3600:.1f} h · "
          f"fallos: {fallos if fallos else 'ninguno'}", flush=True)
    # Auditoría 24-07: una batería con fallos no debe salir con código 0
    # (el proceso padre y la CI deben poder detectarlo sin leer logs).
    if fallos:
        sys.exit(1)


if __name__ == "__main__":
    main()
