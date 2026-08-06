"""Una sola versión del proyecto, declarada en cuatro sitios.

La 4ª auditoría (hallazgo 6) encontró README en v0.1.4-alpha mientras
GARANTIAS, CITATION y la Research Card seguían en v0.1.3-alpha: un lector no
podía saber qué versión describe cada promesa. Este test es la puerta que
impide que vuelvan a divergir.

Uso: python test_version_unica.py
"""

import pathlib
import re

RAIZ = pathlib.Path(__file__).parent.parent

# fichero → patrón con UN grupo: la versión declarada.
FUENTES = {
    "README.md": r"Versión `v(\d+\.\d+\.\d+-\w+)`",
    "GARANTIAS.md": r"Versión: v(\d+\.\d+\.\d+-\w+)",
    "CITATION.cff": r"^version: (\d+\.\d+\.\d+-\w+)$",
    "RESEARCH_CARD.md": r"^# Research Card — PsicoAI v(\d+\.\d+\.\d+-\w+)",
}


def run():
    ok = True
    versiones = {}
    for fichero, patron in FUENTES.items():
        texto = (RAIZ / fichero).read_text(encoding="utf-8")
        m = re.search(patron, texto, re.M)
        if not m:
            print(f" FAIL {fichero}: no declara versión con el patrón esperado")
            ok = False
            continue
        versiones[fichero] = m.group(1)

    distintas = set(versiones.values())
    if len(distintas) == 1:
        print(f"  ok  versión única en {len(versiones)} ficheros:"
              f" v{distintas.pop()}")
    else:
        ok = False
        print(" FAIL versiones divergentes:")
        for f, v in sorted(versiones.items()):
            print(f"        {f}: v{v}")

    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
