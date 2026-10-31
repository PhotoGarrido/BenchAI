"""Sirve `publicacion/` en local con rutas limpias, como Vercel.

`python3 -m http.server` no entiende las rutas limpias del sitio
(`/completo`, `/psicobench`): este servidor prueba `<ruta>.html` cuando
`<ruta>` no existe, lo mismo que `cleanUrls` en `web/vercel.json`. Sirve
para pasar el smoke y las pruebas de la lámina contra el paquete exacto que
se despliega, antes de desplegarlo. Solo en local; no se publica.

    python3 web/publicar.py
    python3 web/servir.py                   # http://127.0.0.1:8743/
    node web/smoke.mjs http://127.0.0.1:8743
"""

from __future__ import annotations

import http.server
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent / "publicacion"
PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 8743


class _Manejador(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(RAIZ), **kwargs)

    def end_headers(self) -> None:
        # Validar es recargar tras cada `publicar.py`: sin esto Chrome reutiliza
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
        print("[servir] no hay publicacion/: corre "
              "`python3 web/publicar.py`")
        return 1
    print(f"[servir] http://127.0.0.1:{PUERTO}/")
    http.server.ThreadingHTTPServer(("127.0.0.1", PUERTO), _Manejador).serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
