"""RunManifest por solicitud (PLAN_MEJORA Fase 0.4).

Procedencia mínima de un run del modo estudio, en dos piezas por directorio
de salida:

  manifest_run.json    cabecera: commit, argv/args, versión de parser y de
                       Python, fecha de inicio.
  solicitudes.jsonl    append-only, una línea por SOLICITUD FÍSICA al
                       proveedor (los reintentos del wrapper aparecen como
                       líneas separadas): prompt exacto, modelo, proveedor,
                       parámetros, semilla, latencia, tokens (usage), id de
                       la respuesta, respuesta cruda o error.

El gancho vive en `model_factory.NaNLanguageModel` — registra si un
experimento llamó antes a `activar(outdir)`; si no, no escribe nada (los
tests offline y el dry-run no generan ficheros).

«Reproducible» significa record/replay: con solicitudes.jsonl un análisis
puede reconstruirse sin red y una discrepancia puede auditarse solicitud a
solicitud (INFORME_EVALUACION_MOTORES, principio 3).
"""

from __future__ import annotations

import datetime
import json
import pathlib
import subprocess
import sys
import threading

_LOCK = threading.Lock()
_FICHERO: pathlib.Path | None = None


def activar(outdir, args: dict | None = None) -> None:
    """Activa el registro para este proceso y escribe la cabecera."""
    global _FICHERO
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    _FICHERO = outdir / "solicitudes.jsonl"
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=pathlib.Path(__file__).parent,
            capture_output=True, text=True).stdout.strip() or "desconocido"
    except OSError:
        commit = "desconocido"
    import parsers
    cabecera = {
        "commit": commit,
        "python": sys.version.split()[0],
        "parser_version": parsers.PARSER_VERSION,
        "argv": sys.argv,
        "args": args,
        "inicio": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    (outdir / "manifest_run.json").write_text(
        json.dumps(cabecera, ensure_ascii=False, indent=2), encoding="utf-8")


def registrar(evento: dict) -> None:
    """Añade una solicitud física al manifiesto (no-op si no está activado).
    Nunca debe tumbar un experimento: los errores de registro se avisan."""
    if _FICHERO is None:
        return
    evento = dict(evento,
                  ts=datetime.datetime.now().isoformat(timespec="milliseconds"))
    try:
        linea = json.dumps(evento, ensure_ascii=False)
        with _LOCK, _FICHERO.open("a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except OSError as e:
        print(f"[manifiesto] no pude registrar: {e}", file=sys.stderr)
