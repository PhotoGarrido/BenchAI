"""Release manifest: fija por hash los datasets exactos de cada cifra
publicable (revisión externa, hallazgo 19 — el análisis no debe seleccionar
silenciosamente «el último directorio»).

  python release_manifest.py --generar   # congela los datasets actuales
  python release_manifest.py --verificar # sale 1 si algún hash no coincide

`analizar_gfinal.py --manifest` usa este fichero para cargar EXACTAMENTE los
directorios fijados (y verifica sus hashes antes de calcular nada).
"""

import argparse
import hashlib
import json
import pathlib
import sys

RES = pathlib.Path(__file__).parent / "resultados"
FICHERO = pathlib.Path(__file__).parent.parent / "preprint" / "release_manifest.json"

# Datasets de los que salen las tablas del preprint (rutas relativas a spike/).
DATASETS = {
    "gfinal_A": "resultados/gfinal_A_20260726_201144",
    "gfinal_B": "resultados/gfinal_B_20260726_201146",
    "g2_a2": "resultados/g2_a2_20260725_194112",
    "g2_a3": "resultados/g2_a3_20260725_201904",
    "g2_b": "resultados/g2_b_20260725_203608",
    "g2_c": "resultados/g2_c_20260725_204754",
    "kappa_r1": "resultados/gfinal_juez",
    "kappa_r2": "resultados/g2_juez",
    "analisis_gfinal": "resultados/gfinal_analisis.json",
    "analisis_g2": "resultados/g2_analisis.json",
    "reproceso": "resultados/reproceso.json",
}


def _sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _hashes(base: pathlib.Path) -> dict:
    out = {}
    for clave, rel in DATASETS.items():
        p = base / rel
        if p.is_dir():
            out[clave] = {"dir": rel, "ficheros": {
                f.name: _sha(f) for f in sorted(p.glob("*.json*"))}}
        elif p.exists():
            out[clave] = {"fichero": rel, "sha256": _sha(p)}
        else:
            out[clave] = {"fichero": rel, "sha256": "AUSENTE"}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--generar", action="store_true")
    ap.add_argument("--verificar", action="store_true")
    args = ap.parse_args()
    base = pathlib.Path(__file__).parent

    if args.generar:
        import parsers
        FICHERO.parent.mkdir(exist_ok=True)
        FICHERO.write_text(json.dumps(
            {"parser_version": parsers.PARSER_VERSION,
             "datasets": _hashes(base)},
            ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Escrito {FICHERO}")
        return
    # verificar (por defecto)
    man = json.loads(FICHERO.read_text())
    ahora = _hashes(base)
    fallos = [k for k in man["datasets"] if man["datasets"][k] != ahora.get(k)]
    if fallos:
        print("MANIFEST FALLA — datasets alterados o ausentes:", fallos)
        sys.exit(1)
    print(f"MANIFEST OK: {len(man['datasets'])} datasets con hash intacto.")


if __name__ == "__main__":
    main()
