#!/usr/bin/env python3
"""Empaqueta `web/` en un único HTML autocontenido, para compartirlo.

El sitio de `web/` son seis ficheros que se cargan por rutas relativas: eso va
perfecto en local y en GitHub Pages, pero no sirve para pegarlo en un visor de
una sola página. Este script produce un fichero suelto con el CSS y el JS
incrustados y los enlaces al repositorio reescritos a URLs absolutas de GitHub,
sin tocar ni una línea del sitio original.

Lo que sale de aquí es un **artefacto de compilación**: se regenera cuando haga
falta y no se versiona.

Uso:
    python3 web/empaquetar.py                     # → web/psicoai-una-pagina.html
    python3 web/empaquetar.py --salida /tmp/x.html
    python3 web/empaquetar.py --sin-envoltorio    # solo el contenido del <body>
                                                  # (para visores que ya ponen
                                                  # su propio <head>)
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent
REPO = "https://github.com/PhotoGarrido/PsicoAI/blob/main/"

# El orden importa: `datos.js` define window.PSICO y el resto lo consume.
SCRIPTS = ["datos.js", "js/graficas.js", "js/reproductor.js",
           "js/pagina.js", "js/escena.js"]


def blindar(js: str) -> str:
    """Un `</script` dentro de una cadena cerraría el bloque incrustado."""
    return js.replace("</script", "<\\/script")


def construir(sin_envoltorio: bool = False) -> str:
    html = (RAIZ / "index.html").read_text(encoding="utf-8")

    titulo = re.search(r"<title>(.*?)</title>", html, re.S)
    titulo = titulo.group(1).strip() if titulo else "PsicoAI"

    cuerpo = re.search(r"<body>(.*)</body>", html, re.S)
    if not cuerpo:
        raise SystemExit("[empaquetar] no encuentro el <body> de index.html")
    cuerpo = cuerpo.group(1)

    # Los <script src> del final se sustituyen por el bloque incrustado.
    cuerpo, n = re.subn(r'\s*<script src="[^"]+"></script>', "", cuerpo)
    if n != len(SCRIPTS):
        raise SystemExit(
            f"[empaquetar] index.html carga {n} scripts y aquí se incrustan "
            f"{len(SCRIPTS)}. Sincroniza la lista SCRIPTS antes de empaquetar.")

    # Los enlaces al repositorio son relativos («../BENCHMARK.md»): fuera del
    # árbol de ficheros no resuelven, así que apuntan a GitHub.
    cuerpo = re.sub(r'href="\.\./([^"]+)"', lambda m: f'href="{REPO}{m.group(1)}"', cuerpo)
    cuerpo = re.sub(r'href=\\"\.\./([^\\"]+)\\"',
                    lambda m: f'href=\\"{REPO}{m.group(1)}\\"', cuerpo)

    css = (RAIZ / "css/estilo.css").read_text(encoding="utf-8")
    js = "\n".join(
        f"/* ── {s} ─────────────────────────────────────────── */\n"
        + blindar((RAIZ / s).read_text(encoding="utf-8"))
        for s in SCRIPTS)

    # Los enlaces relativos también viven dentro del JS (la función REPO()).
    js = js.replace('`<a href="../${r}">${r}</a>`',
                    f'`<a href="{REPO}' + '${r}" target="_blank" rel="noopener">${r}</a>`')

    aviso = (
        "<!-- Generado por web/empaquetar.py — copia de una sola página del\n"
        "     sitio de web/. Para trabajar sobre él, edita los ficheros de\n"
        "     web/ y vuelve a empaquetar; no edites este fichero. -->\n")

    partes = [aviso, f"<title>{titulo}</title>",
              f"<style>\n{css}\n</style>", cuerpo, f"<script>\n{js}\n</script>"]

    if sin_envoltorio:
        return "\n".join(partes)

    return ("<!doctype html>\n<html lang=\"es\">\n<head>\n"
            "<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<meta name=\"color-scheme\" content=\"dark\">\n"
            + aviso + f"<title>{titulo}</title>\n"
            f"<style>\n{css}\n</style>\n</head>\n<body>\n"
            + cuerpo + f"\n<script>\n{js}\n</script>\n</body>\n</html>\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--salida", default=str(RAIZ / "psicoai-una-pagina.html"))
    ap.add_argument("--sin-envoltorio", action="store_true",
                    help="emite solo el contenido, sin <html>/<head>/<body>")
    args = ap.parse_args()

    salida = pathlib.Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    texto = construir(args.sin_envoltorio)
    salida.write_text(texto, encoding="utf-8")
    print(f"[empaquetar] {salida} ({len(texto.encode('utf-8')) / 1024:.0f} kB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
