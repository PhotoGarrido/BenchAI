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
    # Reauditoría 31-07 (P1.10): la sensibilidad citada en el preprint
    # (LOCO/LOPO + bootstrap emparejado) queda fijada por hash como el resto.
    "gfinal_robustez": "resultados/gfinal_robustez.json",
    # Reauditoría 31-07 (P0-G / encargo item 1): los datasets NaN que
    # sostienen la tabla de prisión §3.3 (P2 rebelión y P2b órdenes, media de
    # los dos marcos, parser anclado v2.2) — antes fuera del manifest, la
    # cifra citada no era trazable a su crudo. Cohorte NaN 15-07, la misma que
    # el informe_trilogia y la ERRATA.
    "prision_qwen3.6_p2": "resultados/prision_default_rebelion_20260715_202117",
    "prision_qwen3.6_p2b": "resultados/prision_default_ordenes_20260715_205757",
    "prision_gemma4_p2": "resultados/prision_gemma4_rebelion_20260715_202913",
    "prision_gemma4_p2b": "resultados/prision_gemma4_ordenes_20260715_210812",
    "prision_mimo_p2": "resultados/prision_mimo-v2.5_rebelion_20260715_203720",
    "prision_mimo_p2b": "resultados/prision_mimo-v2.5_ordenes_20260715_211638",
    "prision_deepseek_p2":
        "resultados/prision_deepseek-v4-flash_rebelion_20260715_204524",
    "prision_deepseek_p2b":
        "resultados/prision_deepseek-v4-flash_ordenes_20260715_212448",
    # Perfiles de la batería de 16 modelos (§3.3 2º párrafo y §4): matriz
    # agregada post-reproceso.
    "matriz_bateria": "resultados/matriz_m2.json",
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


def dir_de(clave: str) -> pathlib.Path:
    """Ruta ABSOLUTA del dataset fijado `clave` en el manifest (modo
    publicable): los analizadores la usan en vez de `glob(...)[-1]`, para que
    un directorio decoy más reciente nunca cambie la cifra citada (G9)."""
    man = json.loads(FICHERO.read_text(encoding="utf-8"))
    entrada = man["datasets"][clave]
    rel = entrada.get("dir") or entrada.get("fichero")
    return pathlib.Path(__file__).parent / rel


def verificar(base: pathlib.Path | None = None) -> list:
    """Devuelve la lista de claves cuyo hash NO coincide (vacía = todo intacto).
    Reutilizable desde otros scripts (regenerar_publicacion, analizar_g2)."""
    base = base or pathlib.Path(__file__).parent
    man = json.loads(FICHERO.read_text(encoding="utf-8"))
    ahora = _hashes(base)
    return [k for k in man["datasets"] if man["datasets"][k] != ahora.get(k)]


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
    fallos = verificar(base)
    man = json.loads(FICHERO.read_text())
    if fallos:
        print("MANIFEST FALLA — datasets alterados o ausentes:", fallos)
        sys.exit(1)
    print(f"MANIFEST OK: {len(man['datasets'])} datasets con hash intacto.")


if __name__ == "__main__":
    main()
