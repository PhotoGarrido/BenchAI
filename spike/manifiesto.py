"""RunManifest por solicitud (Fase 0.4; endurecido en revisión externa R3).

Dos piezas por directorio de salida:

  manifest_run.json    cabecera + ESTADO FINAL del run: commit, argv/args,
                       versiones (parser, python, dependencias clave), hashes
                       declarados, y al cerrar: status completed/failed,
                       recuento de solicitudes y errores, hora de fin.
  solicitudes.jsonl    append-only, una línea por SOLICITUD FÍSICA, con los
                       MENSAJES COMPLETOS (system + user), parámetros, seed,
                       latencia, tokens, request_id, modelo pedido y devuelto,
                       respuesta cruda o error. Sin claves ni cabeceras.

API: la clase `RunManifest` (context manager, estado final garantizado) es la
forma recomendada; las funciones de módulo `activar()`/`registrar()` se
mantienen por compatibilidad con los harness existentes y delegan en una
instancia por defecto. `registrar()` jamás tumba un experimento: captura
también errores de serialización, no solo de E/S (hallazgo 16).
"""

from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import threading


def _commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=pathlib.Path(__file__).parent,
            capture_output=True, text=True).stdout.strip() or "desconocido"
    except OSError:
        return "desconocido"


def _dependencias() -> dict:
    """Versiones de las dependencias directas relevantes (hallazgo 6)."""
    versiones = {}
    for mod in ("openai", "numpy", "concordia"):
        try:
            m = __import__(mod)
            versiones[mod] = getattr(m, "__version__", "sin __version__")
        except ImportError:
            versiones[mod] = "no instalado"
    return versiones


def sha256_texto(texto: str) -> str:
    return hashlib.sha256((texto or "").encode("utf-8")).hexdigest()


class RunManifest:
    """Manifiesto de un run con estado final garantizado.

    with RunManifest(outdir, vars(args), hashes={"escenario": h}) as m:
        ...  # las llamadas del modelo registran vía manifiesto.registrar()
    Al salir: status=completed (o failed con el tipo de excepción)."""

    def __init__(self, outdir, args: dict | None = None,
                 hashes: dict | None = None):
        self.outdir = pathlib.Path(outdir)
        self.outdir.mkdir(parents=True, exist_ok=True)
        self.fichero = self.outdir / "solicitudes.jsonl"
        self._lock = threading.Lock()
        self._n = 0
        self._errores = 0
        import parsers
        self.cabecera = {
            "commit": _commit(),
            "python": sys.version.split()[0],
            "parser_version": parsers.PARSER_VERSION,
            "dependencias": _dependencias(),
            "argv": sys.argv,
            "args": args,
            "hashes": hashes or {},
            "inicio": datetime.datetime.now().isoformat(timespec="seconds"),
            "status": "running",
        }
        self._escribir_cabecera()

    def _escribir_cabecera(self):
        try:
            tmp = self.outdir / "manifest_run.json.tmp"
            tmp.write_text(json.dumps(self.cabecera, ensure_ascii=False,
                                      indent=2, default=str),
                           encoding="utf-8")
            tmp.replace(self.outdir / "manifest_run.json")
        except OSError as e:
            print(f"[manifiesto] no pude escribir cabecera: {e}",
                  file=sys.stderr)

    def registrar(self, evento: dict) -> None:
        evento = dict(evento, ts=datetime.datetime.now()
                      .isoformat(timespec="milliseconds"))
        try:
            linea = json.dumps(evento, ensure_ascii=False, default=str)
        except (TypeError, ValueError) as e:
            linea = json.dumps({"error_serializacion": str(e)[:200],
                                "ts": evento["ts"]})
        with self._lock:
            self._n += 1
            if evento.get("error"):
                self._errores += 1
            try:
                with self.fichero.open("a", encoding="utf-8") as f:
                    f.write(linea + "\n")
            except OSError as e:
                print(f"[manifiesto] no pude registrar: {e}", file=sys.stderr)

    def cerrar(self, status: str = "completed", extra: dict | None = None):
        self.cabecera.update({
            "status": status,
            "fin": datetime.datetime.now().isoformat(timespec="seconds"),
            "solicitudes": self._n, "errores": self._errores,
            **(extra or {})})
        self._escribir_cabecera()

    def __enter__(self):
        activar_instancia(self)
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.cerrar("completed")
        else:
            self.cerrar("failed", {"exception_type": exc_type.__name__,
                                   "exception": str(exc)[:300]})
        activar_instancia(None)
        return False


# ── Compatibilidad de módulo (los harness llaman activar/registrar) ────────
_ACTIVO: RunManifest | None = None


def activar_instancia(m: RunManifest | None) -> None:
    global _ACTIVO
    _ACTIVO = m


def activar(outdir, args: dict | None = None,
            hashes: dict | None = None) -> RunManifest:
    m = RunManifest(outdir, args, hashes)
    activar_instancia(m)
    return m


def registrar(evento: dict) -> None:
    if _ACTIVO is not None:
        _ACTIVO.registrar(evento)
