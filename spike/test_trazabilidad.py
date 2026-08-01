"""Trazabilidad de cifras (reauditoría 31-07, G9 / P0-G).

`analizar_g2.cargar` en modo publicable (`usar_manifest=True`) toma el
directorio del release_manifest (dataset fijado por hash), NUNCA el último por
glob. Este test demuestra que un directorio DECOY más reciente
(`g2_a2_99999999_999999`) cambia el resultado en modo glob pero NO en modo
manifest — la cifra citada queda anclada a su crudo fijado.

Offline, sin red: apto para CI. Uso: python test_trazabilidad.py
"""
import json
import pathlib
import shutil

import analizar_g2
import release_manifest


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


RES = pathlib.Path(__file__).parent / "resultados"


def run():
    ok = True
    decoy = RES / "g2_a2_99999999_999999"
    try:
        # Directorio del manifest (la verdad publicable) para la fase a2.
        dir_manifest = release_manifest.dir_de("g2_a2").name

        # Creamos un decoy que el glob ordenado situaría EL ÚLTIMO.
        decoy.mkdir(exist_ok=True)
        (decoy / "registros_decoy.jsonl").write_text(
            json.dumps({"modelo": "decoy", "nivel": 5, "estado": "NIVEL",
                        "contenido": "x", "fuente": "orden", "negativa": True,
                        "rep": 1, "supervisor": "Z"}) + "\n",
            encoding="utf-8")

        # Modo glob: el decoy gana (último dir) — comportamiento peligroso que
        # el modo manifest evita.
        _regs_glob, origen_glob = analizar_g2.cargar("a2", usar_manifest=False)
        ok &= _c(origen_glob == decoy.name,
                 f"modo glob: el decoy más reciente se elige ({origen_glob})")

        # Modo manifest: el decoy se IGNORA; el origen es el dataset fijado.
        regs_man, origen_man = analizar_g2.cargar("a2", usar_manifest=True)
        ok &= _c(origen_man == dir_manifest and origen_man != decoy.name,
                 f"modo manifest: cifra anclada al dataset fijado ({origen_man}),"
                 " el decoy no la cambia")
        ok &= _c(all(r.get("modelo") != "decoy" for r in regs_man),
                 "modo manifest: ningún registro del decoy entra en el análisis")
    finally:
        if decoy.exists():
            shutil.rmtree(decoy)

    # El decoy no debe quedar en el árbol (ni afectar al manifest).
    ok &= _c(not decoy.exists(), "el decoy se limpió (no contamina el árbol)")
    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
