"""Vigía de baterías: se reinicia el equipo, no la investigación.

Vigila un batch (`resultados/bateria_*/`): si el proceso de la batería
muere con trabajo pendiente, lo relanza con `--reanudar` (los modelos
salen del manifest.json del propio batch, no de la memoria de nadie) y
avisa por notificación de macOS. La decisión está separada en una función
pura (`decidir`) con test offline.

Uso:
  python vigia.py resultados/bateria_X/            # vigila hasta el final
  python vigia.py resultados/bateria_X/ --una-vez  # una pasada (cron/launchd)

No lanza baterías nuevas: solo reanuda una existente. El tope de
relanzamientos evita el bucle infinito si el fallo es sistemático.
"""

import argparse
import json
import pathlib
import subprocess
import sys
import time

AQUI = pathlib.Path(__file__).parent


def decidir(manifest, hay_proceso, segundos_sin_senal, umbral=600):
    """Qué hacer con el batch, sin efectos:
    'terminada' | 'terminada_con_fallos' | 'activa' | 'esperar' | 'reanudar'
    """
    if manifest.get("fin"):
        return "terminada" if manifest.get("completo") else \
            "terminada_con_fallos"
    if hay_proceso:
        return "activa"
    # Sin proceso y sin cierre: margen breve por si estamos en una carrera
    # de arranque; pasado el umbral, la batería está caída.
    return "esperar" if segundos_sin_senal < umbral else "reanudar"


def _senal_mas_reciente(logdir):
    """Último mtime de los artefactos vivos del batch (progreso, manifest,
    logs): la mejor evidencia barata de que algo sigue escribiendo."""
    candidatos = [logdir / "progreso.jsonl", logdir / "manifest.json",
                  *logdir.glob("*.log")]
    return max((f.stat().st_mtime for f in candidatos if f.exists()),
               default=0.0)


def _hay_proceso():
    r = subprocess.run(["pgrep", "-f", r"python[^ ]* .*bateria\.py"],
                       capture_output=True)
    return r.returncode == 0


def _notificar(mensaje):
    print(f"[vigía] {mensaje}", flush=True)
    try:
        subprocess.run(["osascript", "-e",
                        'display notification "' + mensaje.replace('"', "'")
                        + '" with title "PsicoAI · vigía"'],
                       capture_output=True, timeout=10)
    except OSError:
        pass


def _relanzar(logdir, manifest):
    cmd = [sys.executable, str(AQUI / "bateria.py"),
           "--modelos", ",".join(manifest["modelos"]),
           "--reanudar", str(logdir)]
    if manifest.get("rapido"):
        cmd.append("--rapido")
    with (logdir / "vigia.log").open("a", encoding="utf-8") as f:
        f.write(f"\n===== relanzamiento · {' '.join(cmd)} =====\n")
        f.flush()
        subprocess.Popen(cmd, cwd=AQUI, stdout=f, stderr=f,
                         start_new_session=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logdir", help="directorio del batch (bateria_*/)")
    parser.add_argument("--intervalo", type=int, default=120,
                        help="segundos entre pasadas (defecto 120)")
    parser.add_argument("--umbral", type=int, default=600,
                        help="segundos sin señal para dar la batería por"
                             " caída (defecto 600)")
    parser.add_argument("--max-relanzamientos", type=int, default=3)
    parser.add_argument("--una-vez", action="store_true",
                        help="una sola pasada (para cron/launchd)")
    args = parser.parse_args()

    logdir = pathlib.Path(args.logdir)
    if not (logdir / "manifest.json").exists():
        raise SystemExit(f"vigía: {logdir} no tiene manifest.json")

    relanzamientos = 0
    while True:
        manifest = json.loads((logdir / "manifest.json")
                              .read_text(encoding="utf-8"))
        sin_senal = time.time() - _senal_mas_reciente(logdir)
        accion = decidir(manifest, _hay_proceso(), sin_senal, args.umbral)
        if accion == "terminada":
            _notificar(f"batería {logdir.name}: terminada sin fallos")
            return
        if accion == "terminada_con_fallos":
            _notificar(f"batería {logdir.name}: terminada CON fallos "
                       f"({len(manifest.get('fallos', []))})")
            sys.exit(1)
        if accion == "reanudar":
            if relanzamientos >= args.max_relanzamientos:
                _notificar(f"batería {logdir.name}: caída y tope de "
                           f"{args.max_relanzamientos} relanzamientos "
                           "agotado — intervención manual")
                sys.exit(1)
            relanzamientos += 1
            _notificar(f"batería {logdir.name}: caída sin cierre — "
                       f"relanzando con --reanudar "
                       f"({relanzamientos}/{args.max_relanzamientos})")
            _relanzar(logdir, manifest)
        if args.una_vez:
            print(f"[vigía] pasada única: {accion}", flush=True)
            return
        time.sleep(args.intervalo)


if __name__ == "__main__":
    main()
