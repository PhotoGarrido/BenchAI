"""Sirve `publicacion/` en local con rutas limpias, como Vercel.

`python3 -m http.server` no entiende las rutas limpias del sitio
(`/completo`, `/psicobench`): este servidor prueba `<ruta>.html` cuando
`<ruta>` no existe, lo mismo que `cleanUrls` en `web/vercel.json`, y aplica
sus redirecciones sin condición de host (`/psicobench` → `/social`). Sirve
para pasar el smoke y las pruebas de la lámina contra el paquete exacto que
se despliega, antes de desplegarlo. Solo en local; no se publica.

    python3 web/publicar.py
    python3 web/servir.py                   # http://127.0.0.1:8743/
    node web/smoke.mjs http://127.0.0.1:8743
"""

from __future__ import annotations

import http.server
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent / "publicacion"
PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 8743


def _redirecciones() -> dict:
    v = RAIZ / "vercel.json"
    if not v.exists():
        return {}
    return {r["source"]: r["destination"]
            for r in json.loads(v.read_text(encoding="utf-8")).get("redirects", []) if "has" not in r}


class _Manejador(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(RAIZ), **kwargs)

    def do_GET(self) -> None:
        destino = _redirecciones().get(self.path.split("?")[0])
        if destino:
            self.send_response(308)
            self.send_header("Location", destino)
            self.end_headers()
            return
        super().do_GET()

    def end_headers(self) -> None:
        # Validar es recargar tras cada `publicar.py`: sin esto Chrome reutiliza
        # la hoja vieja por caché heurística (la página no deja hacer fetch).
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def translate_path(self, path: str) -> str:
        ruta = pathlib.Path(super().translate_path(path))
        if not ruta.exists() and ruta.with_suffix(".html").exists():
            return str(ruta.with_suffix(".html"))
        # una carpeta con su index.html se sirve sin barra final, como en
        # Vercel con `trailingSlash: false` (/personalidad)
        if ruta.is_dir() and (ruta / "index.html").exists():
            return str(ruta / "index.html")
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
