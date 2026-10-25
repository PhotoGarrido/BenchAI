"""Sirve `publicacion-previa/` en local con rutas limpias, como Vercel.

La previa (`python3 web/publicar.py --previa`) lleva la versión en
preparación de PsicoBench en /psicobench-nueva. `python3 -m http.server` no
entiende las rutas limpias del sitio (`/completo`, `/psicobench`), así que
este servidor prueba `<ruta>.html` cuando `<ruta>` no existe — lo mismo que
`cleanUrls` en `web/vercel.json`. Solo para validar en local; no se publica.

    python3 web/publicar.py --previa
    python3 web/servir_previa.py            # http://127.0.0.1:8743/psicobench-nueva
"""

from __future__ import annotations

import http.server
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent / "publicacion-previa"
PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 8743


class _Manejador(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(RAIZ), **kwargs)

    def end_headers(self) -> None:
        # Validar es recargar tras cada `--previa`: sin esto Chrome reutiliza
        # la hoja vieja por caché heurística (la página no deja hacer fetch).
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def translate_path(self, path: str) -> str:
        ruta = pathlib.Path(super().translate_path(path))
        if not ruta.exists() and ruta.with_suffix(".html").exists():
            return str(ruta.with_suffix(".html"))
        return str(ruta)


def main() -> int:
    if not RAIZ.exists():
        print("[servir_previa] no hay publicacion-previa/: corre "
              "`python3 web/publicar.py --previa`")
        return 1
    print(f"[servir_previa] http://127.0.0.1:{PUERTO}/psicobench-nueva")
    http.server.ThreadingHTTPServer(("127.0.0.1", PUERTO), _Manejador).serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
