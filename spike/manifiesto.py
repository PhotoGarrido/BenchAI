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
import os
import pathlib
import contextvars
import subprocess
import sys
import tempfile
import threading


def escribir_atomico_unico(path, texto: str) -> None:
    """Escritura atómica con temporal ÚNICO por escritura (G11, reauditoría
    31-07): `mkstemp` da un nombre irrepetible en el mismo directorio; se
    escribe y solo entonces `os.replace`. Un SIGKILL entre la escritura y el
    replace deja, a lo sumo, un `.tmp` de nombre único —que la limpieza de
    apertura borra— y NUNCA un `manifest_run.json.tmp` fijo que pueda
    confundirse con un artefacto válido ni un definitivo a medias."""
    path = pathlib.Path(path)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent),
                              prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(texto)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def limpiar_tmp_huerfanos(outdir) -> None:
    """Al abrir un outdir, borra los temporales `.tmp` que un run
    interrumpido pudiera haber dejado (G11): ninguno es un artefacto válido."""
    for t in pathlib.Path(outdir).glob("*.tmp"):
        try:
            t.unlink()
        except OSError:
            pass


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
        limpiar_tmp_huerfanos(self.outdir)   # G11: sin .tmp de un run muerto
        self.fichero = self.outdir / "solicitudes.jsonl"
        self._lock = threading.Lock()
        self._n = 0
        self._errores = 0
        # G3 (reauditoría 31-07): si un append a disco falla, el run NO puede
        # cerrar 'completed' — el contador solo sube cuando la línea se
        # escribió de verdad, y este flag degrada el estado final.
        self._fallo_escritura = False
        import parsers
        self.cabecera: dict = {
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
            escribir_atomico_unico(self.outdir / "manifest_run.json",
                                   json.dumps(self.cabecera, ensure_ascii=False,
                                              indent=2, default=str))
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
                                "error": "serializacion", "ts": evento["ts"]})
            evento = {"error": "serializacion"}
        with self._lock:
            # G3: se cuenta DESPUÉS de escribir. Si el append falla, la
            # solicitud NO se registró y NO se cuenta — y el run queda
            # marcado para no poder cerrar 'completed'.
            try:
                with self.fichero.open("a", encoding="utf-8") as f:
                    f.write(linea + "\n")
            except OSError as e:
                self._fallo_escritura = True
                print(f"[manifiesto] no pude registrar (run degradado): {e}",
                      file=sys.stderr)
                return
            self._n += 1
            if evento.get("error"):
                self._errores += 1

    def cerrar(self, status: str = "completed", extra: dict | None = None):
        # G3: un fallo de escritura durante el run impide declarar 'completed'
        # — el manifiesto no representa cada solicitud física, así que miente
        # si dice que terminó bien. Se degrada a 'degraded'.
        if status == "completed" and self._fallo_escritura:
            status = "degraded"
        self.cabecera.update({
            "status": status,
            "fin": datetime.datetime.now().isoformat(timespec="seconds"),
            "solicitudes": self._n, "errores": self._errores,
            "fallo_escritura": self._fallo_escritura,
            **(extra or {})})
        self._escribir_cabecera()

    def __enter__(self):
        activar_instancia(self)
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            if self.cabecera.get("status") == "running":
                self.cerrar("completed")
        else:
            self.cerrar("failed", {"exception_type": exc_type.__name__,
                                   "exception": str(exc)[:300]})
        activar_instancia(None)
        return False


# ── Compatibilidad de módulo (los harness llaman activar/registrar). El
# activo vive en un ContextVar (auditoría 31-07, P1.4): dos runs en hilos o
# contextos distintos del mismo proceso no se mezclan. ────────────────────
_ACTIVO: contextvars.ContextVar[RunManifest | None] = contextvars.ContextVar(
    "manifiesto_activo", default=None)


def activar_instancia(m: RunManifest | None) -> None:
    _ACTIVO.set(m)


def cerrar_activo(status: str = "completed", extra: dict | None = None):
    """Cierra el manifiesto activo del contexto (P0.2): los harness lo
    llaman al terminar; una excepción lo cierra como failed en el bloque
    __main__ de cada experimento. No-op si no hay activo."""
    m = _ACTIVO.get()
    if m is not None:
        m.cerrar(status, extra)
        activar_instancia(None)


def activar(outdir, args: dict | None = None,
            hashes: dict | None = None) -> RunManifest:
    m = RunManifest(outdir, args, hashes)
    activar_instancia(m)
    return m


def registrar(evento: dict) -> None:
    m = _ACTIVO.get()
    if m is not None:
        m.registrar(evento)


def map_paralelo(pool, fn, iterable):
    """`pool.map` que PROPAGA el contexto (y con él el manifiesto activo) a
    los workers (reauditoría 31-07, P0.2): los hilos de un ThreadPoolExecutor
    nacen con un contexto vacío, así que `registrar()` dentro de un worker
    veía `None` y las solicitudes físicas se perdían en silencio — el run
    terminaba `completed` con `solicitudes=0` pese a haber gastado.

    Cada tarea se envía con su PROPIA copia del contexto del hilo llamante
    (una `Context` no puede entrarse dos veces a la vez), de modo que dos
    runs concurrentes con manifiestos distintos no se mezclan. Conserva el
    orden de entrada y la semántica de errores de `pool.map` (la primera
    excepción se propaga al consumir los resultados)."""
    futuros = [pool.submit(contextvars.copy_context().run, fn, x)
               for x in iterable]
    return [f.result() for f in futuros]
