#!/usr/bin/env python3
"""Empaqueta una página de `web/` en un único HTML autocontenido.

El sitio son varios ficheros con rutas relativas: eso va perfecto en local y en
GitHub Pages, pero no sirve para pegarlo en un visor de una sola página ni para
mandárselo a alguien sin el repositorio detrás. Este script incrusta el CSS y el
JS y reescribe los enlaces relativos, sin tocar ni una línea del sitio original.

Lo que sale de aquí es un **artefacto de compilación**: se regenera cuando haga
falta y no se versiona.

Uso:
    python3 web/empaquetar.py                       # home.html → una página
    python3 web/empaquetar.py --pagina index.html   # el sitio denso
    python3 web/empaquetar.py --sin-envoltorio      # solo el contenido del
                                                    # <body>, para visores que
                                                    # ya ponen su propio <head>
    python3 web/empaquetar.py --enlace-detalle URL  # a dónde apuntan los
                                                    # enlaces a index.html
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent
REPO = "https://github.com/PhotoGarrido/PsicoAI/blob/main/"

# El orden importa: `datos.js` define window.PSICO y el resto lo consume.
SCRIPTS = {
    "index.html": ["datos.js", "js/graficas.js", "js/reproductor.js",
                   "js/pagina.js", "js/escena.js"],
    "home.html": ["datos.js", "js/oficina.js", "js/home.js"],
}
HOJAS = {"index.html": ["css/estilo.css"], "home.html": ["css/home.css"]}


def blindar(js: str) -> str:
    """Un `</script` dentro de una cadena cerraría el bloque incrustado."""
    return js.replace("</script", "<\\/script")


def construir(pagina: str, sin_envoltorio: bool = False,
              enlace_detalle: str | None = None) -> str:
    html = (RAIZ / pagina).read_text(encoding="utf-8")

    m = re.search(r"<title>(.*?)</title>", html, re.S)
    titulo = m.group(1).strip() if m else "PsicoAI"

    m = re.search(r"<body>(.*)</body>", html, re.S)
    if not m:
        raise SystemExit(f"[empaquetar] no encuentro el <body> de {pagina}")
    cuerpo = m.group(1)

    guiones = SCRIPTS[pagina]
    cuerpo, n = re.subn(r'\s*<script src="[^"]+"></script>', "", cuerpo)
    if n != len(guiones):
        raise SystemExit(
            f"[empaquetar] {pagina} carga {n} scripts y aquí se incrustan "
            f"{len(guiones)}. Sincroniza la tabla SCRIPTS antes de empaquetar.")

    # Los enlaces internos entre páginas del sitio: en un fichero suelto no
    # resuelven, así que van a donde diga --enlace-detalle (o se quedan).
    if enlace_detalle:
        cuerpo = re.sub(r'href="index\.html(#[\w-]+)?"',
                        lambda mm: f'href="{enlace_detalle}{mm.group(1) or ""}"', cuerpo)

    # Los enlaces al repositorio son relativos («../BENCHMARK.md»).
    cuerpo = re.sub(r'href="\.\./([^"]+)"', lambda mm: f'href="{REPO}{mm.group(1)}"', cuerpo)

    css = "\n".join((RAIZ / f).read_text(encoding="utf-8") for f in HOJAS[pagina])
    js = "\n".join(
        f"/* ── {g} ─────────────────────────────────────────── */\n"
        + blindar((RAIZ / g).read_text(encoding="utf-8"))
        for g in guiones)
    js = js.replace('`<a href="../${r}">${r}</a>`',
                    f'`<a href="{REPO}' + '${r}" target="_blank" rel="noopener">${r}</a>`')

    aviso = (
        f"<!-- Generado por web/empaquetar.py desde {pagina} — copia de una sola\n"
        "     página. Para trabajar sobre él, edita los ficheros de web/ y vuelve\n"
        "     a empaquetar; no edites este fichero. -->\n")

    if sin_envoltorio:
        return "\n".join([aviso, f"<title>{titulo}</title>",
                          f"<style>\n{css}\n</style>", cuerpo,
                          f"<script>\n{js}\n</script>"])

    return ('<!doctype html>\n<html lang="es">\n<head>\n'
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="color-scheme" content="dark">\n'
            + aviso + f"<title>{titulo}</title>\n"
            f"<style>\n{css}\n</style>\n</head>\n<body>\n"
            + cuerpo + f"\n<script>\n{js}\n</script>\n</body>\n</html>\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pagina", default="home.html", choices=sorted(SCRIPTS))
    ap.add_argument("--salida")
    ap.add_argument("--sin-envoltorio", action="store_true",
                    help="emite solo el contenido, sin <html>/<head>/<body>")
    ap.add_argument("--enlace-detalle",
                    help="URL a la que apuntan los enlaces a index.html")
    args = ap.parse_args()

    salida = pathlib.Path(args.salida or
                          RAIZ / f"psicoai-{pathlib.Path(args.pagina).stem}-una-pagina.html")
    salida.parent.mkdir(parents=True, exist_ok=True)
    texto = construir(args.pagina, args.sin_envoltorio, args.enlace_detalle)
    salida.write_text(texto, encoding="utf-8")
    print(f"[empaquetar] {salida} ({len(texto.encode('utf-8')) / 1024:.0f} kB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
