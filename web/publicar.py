"""Arma `publicacion/`, que es EXACTAMENTE lo que se sirve en la web pública.

La regla es una lista blanca, no una exclusión: aquí solo entra lo que se
nombra abajo. El repositorio tiene crudos, informes, el preprint y las claves
de ejecución; nada de eso puede acabar publicado por descuido, así que no se
despliega la raíz del repo con exclusiones — se copia lo permitido y punto.

  python3 web/publicar.py            # escribe publicacion/
  python3 web/publicar.py --check    # falla si está desfasada (para CI)

Lo que sale:
  /                     web/home.html          la home divulgativa
  /completo             web/index.html         el sitio largo
  /benchmark            benchmark/index.html   el panel del benchmark
  /visor                viewer/index.html      el visor de replays
  … y los estáticos que esas cuatro necesitan, incluidos los episodios que
  el visor reproduce.
"""

from __future__ import annotations

import argparse
import filecmp
import pathlib
import shutil
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "publicacion"

# (origen, destino). Directorios enteros con `/` al final.
PIEZAS: list[tuple[str, str]] = [
    ("web/vercel.json", "vercel.json"),
    ("web/home.html", "index.html"),
    ("web/index.html", "completo.html"),
    ("web/visor-embebido.html", "visor-embebido.html"),
    ("web/visor-arranque.js", "visor-arranque.js"),
    ("web/datos.js", "datos.js"),
    ("web/css/", "css/"),
    ("web/js/", "js/"),
    ("benchmark/index.html", "benchmark/index.html"),
    ("benchmark/psicobench.json", "benchmark/psicobench.json"),
    ("viewer/index.html", "viewer/index.html"),
    ("viewer/app.js", "viewer/app.js"),
    # de los episodios solo sale el replay: el visor no lee nada más, y
    # las fichas y los generadores son material del repositorio
    ("episodios/*/replay.json", "episodios/"),
]

# Ni el linaje ni los manifiestos del benchmark salen: son de auditoría, se
# consultan en el repositorio.
FUERA = {".DS_Store", "linaje.json", ".vercel"}


def _copiar(destino: pathlib.Path) -> None:
    # El enlace con Vercel (`.vercel/project.json`) vive dentro del paquete y
    # se regenera CADA vez: si se borrase, el siguiente despliegue crearia un
    # proyecto nuevo en lugar de actualizar el que ya sirve el dominio.
    enlace = destino / ".vercel"
    guardado = None
    if enlace.exists():
        guardado = destino.parent / ".vercel_guardado"
        if guardado.exists():
            shutil.rmtree(guardado)
        shutil.copytree(enlace, guardado)
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True)
    if guardado is not None:
        shutil.copytree(guardado, destino / ".vercel")
        shutil.rmtree(guardado)
    for origen_rel, dest_rel in PIEZAS:
        origen = RAIZ / origen_rel.rstrip("/")
        dest = destino / dest_rel.rstrip("/")
        if "*" not in origen_rel and not origen.exists():
            raise SystemExit(f"[publicar] no encuentro {origen_rel}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        if "*" in origen_rel:
            for f in sorted(RAIZ.glob(origen_rel)):
                sub = dest / f.parent.name / f.name
                sub.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, sub)
            continue
        if origen_rel.endswith("/"):
            shutil.copytree(origen, dest,
                            ignore=shutil.ignore_patterns(*FUERA))
        else:
            shutil.copy2(origen, dest)

    _reescribir_enlaces(destino)

    # `completo.html` enlaza a la home como `home.html`; en la publicación la
    # home vive en la raíz.
    comp = destino / "completo.html"
    comp.write_text(comp.read_text(encoding="utf-8")
                    .replace('href="home.html"', 'href="/"'), encoding="utf-8")
    # y la home enlaza al sitio largo como `index.html`
    idx = destino / "index.html"
    idx.write_text(idx.read_text(encoding="utf-8")
                   .replace('href="index.html', 'href="/completo'), encoding="utf-8")


REPO_WEB = "https://github.com/PhotoGarrido/PsicoAI/blob/main/"


def _reescribir_enlaces(destino: pathlib.Path) -> None:
    """Los `../algo` del sitio apuntan al REPOSITORIO, no a la web.

    Las páginas viven en `web/` y enlazan a los ficheros del repo con rutas
    relativas: `../BENCHMARK.md`, `../preprint/preprint.md`. Servidas desde la
    raíz del dominio eso resuelve a `/BENCHMARK.md` — un 404 en cada «Fuente ·»
    del sitio largo. Aquí se reescriben una vez, al publicar:

      · lo que SÍ está en el paquete (benchmark, visor) → su ruta absoluta;
      · lo demás → su URL en GitHub, que es donde vive de verdad.

    Mientras el repositorio sea privado esos enlaces piden login: es la
    respuesta honesta —el documento existe y no es público todavía— y quedan
    correctos el día que se abra, sin tocar nada.
    """
    for f in sorted(destino.rglob("*.html")):
        t = f.read_text(encoding="utf-8")
        antes = t
        t = t.replace('href="../benchmark/index.html"', 'href="/benchmark"')
        t = t.replace('href="../benchmark/', 'href="/benchmark/')
        t = t.replace('href="../viewer/index.html"', 'href="/viewer/index.html"')
        t = t.replace('href="../', f'href="{REPO_WEB}')
        if t != antes:
            f.write_text(t, encoding="utf-8")

    # Y los que construye el guion: `REPO()` de pagina.js arma cada «Fuente ·»
    # en caliente, así que la reescritura del HTML no los alcanzaba.
    js = destino / "js" / "pagina.js"
    viejo = 'const REPO = (r) => mk`<a href="../${r}">${r}</a>`;'
    nuevo = ('const REPO = (r) => mk`<a href="' + REPO_WEB
             + '${r}" target="_blank" rel="noopener">${r}</a>`;')
    texto = js.read_text(encoding="utf-8")
    if viejo not in texto:
        raise SystemExit("[publicar] REPO() ha cambiado de forma: revisa la reescritura")
    js.write_text(texto.replace(viejo, nuevo), encoding="utf-8")


def _iguales(a: pathlib.Path, b: pathlib.Path) -> bool:
    cmp = filecmp.dircmp(a, b, ignore=[".vercel", ".DS_Store"])
    if cmp.left_only or cmp.right_only or cmp.diff_files:
        return False
    return all(_iguales(a / d, b / d) for d in cmp.common_dirs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="falla si publicacion/ no coincide con las fuentes")
    args = ap.parse_args()

    if args.check:
        if not SALIDA.exists():
            print("[publicar] publicacion/ no existe")
            return 1
        tmp = RAIZ / ".publicacion_check"
        _copiar(tmp)
        ok = _iguales(tmp, SALIDA)
        shutil.rmtree(tmp)
        print("[publicar] publicacion/ al día." if ok
              else "[publicar] DESFASADA: corre `python3 web/publicar.py`")
        return 0 if ok else 1

    _copiar(SALIDA)
    n = sum(1 for _ in SALIDA.rglob("*") if _.is_file())
    print(f"[publicar] {SALIDA.relative_to(RAIZ)}/ con {n} ficheros")
    return 0


if __name__ == "__main__":
    sys.exit(main())
