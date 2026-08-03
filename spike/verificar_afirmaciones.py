"""CPR — Claim Provenance Rate del manuscrito.

Las afirmaciones del preprint llevan anclas de evidencia inline (comentarios
HTML, invisibles al render): `<!-- ev: pos:FRAGMENTO -->` apunta a una
posición epistémica de POSICIONES.md, `<!-- ev: doc:RUTA[#FRAGMENTO] -->` a
un documento del repo (y, si lleva fragmento, a texto que debe aparecer en
él), `<!-- ev: manifest:CLAVE -->` a un dataset fijado por sha256.

Este verificador resuelve cada ancla SIN red y reporta el CPR (anclas que
resuelven / anclas totales). `--check` exige CPR = 1,0 y un mínimo de anclas
(candado contra borrar anotaciones): una afirmación cuya evidencia no
resuelve no se publica.
"""

import argparse
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).parent.parent
PREPRINT = RAIZ / "preprint" / "preprint.md"
MINIMO_ANCLAS = 10

RE_ANCLA = re.compile(r"<!--\s*ev:\s*(pos|doc|manifest):([^>]+?)\s*-->")


def _claves(objeto):
    if isinstance(objeto, dict):
        for k, v in objeto.items():
            yield k
            yield from _claves(v)
    elif isinstance(objeto, list):
        for v in objeto:
            yield from _claves(v)


def resolver(tipo, valor):
    """None si resuelve; texto del fallo si no."""
    if tipo == "pos":
        texto = (RAIZ / "POSICIONES.md").read_text(encoding="utf-8")
        return None if valor in texto else f"'{valor}' no está en POSICIONES.md"
    if tipo == "doc":
        ruta, _, frag = valor.partition("#")
        f = RAIZ / ruta
        if not f.exists():
            return f"no existe {ruta}"
        if frag and frag not in f.read_text(encoding="utf-8", errors="replace"):
            return f"'{frag}' no aparece en {ruta}"
        return None
    if tipo == "manifest":
        manifest = json.loads((RAIZ / "preprint" / "release_manifest.json")
                              .read_text(encoding="utf-8"))
        return (None if valor in set(_claves(manifest))
                else f"clave '{valor}' ausente del release manifest")
    return f"tipo de ancla desconocido: {tipo}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    anclas = RE_ANCLA.findall(PREPRINT.read_text(encoding="utf-8"))
    fallos = []
    for tipo, valor in anclas:
        problema = resolver(tipo, valor.strip())
        if problema:
            fallos.append(f"ev:{tipo}:{valor.strip()} — {problema}")
    cpr = (len(anclas) - len(fallos)) / len(anclas) if anclas else 0.0
    print(f"CPR: {len(anclas) - len(fallos)}/{len(anclas)} anclas resuelven"
          f" ({cpr:.1%})")
    for f in fallos:
        print("  ·", f)
    if args.check and (fallos or len(anclas) < MINIMO_ANCLAS):
        if len(anclas) < MINIMO_ANCLAS:
            print(f"ANCLAS INSUFICIENTES: {len(anclas)} < {MINIMO_ANCLAS}")
        sys.exit(1)


if __name__ == "__main__":
    main()
