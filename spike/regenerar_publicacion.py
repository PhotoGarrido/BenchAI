"""Regenerador único de las cifras citables del preprint (reauditoría 31-07,
G9 / P0-G).

Un solo comando que, desde los datasets FIJADOS por hash en el
`release_manifest`, re-deriva las cifras publicables y las compara con lo que
el manuscrito cita. Nada se toma del «último directorio por glob»: si algo no
cuadra, sale con código ≠ 0.

  python regenerar_publicacion.py --check

Qué regenera y compara:
  1. Integridad del manifest (todos los datasets con hash intacto).
  2. Tabla de prisión §3.3 (P2 rebelión y P2b órdenes, media de los dos
     marcos, parser anclado v2.2) desde los 8 datasets NaN fijados.
  3. Efectos titulares de G2 (diferencias OBSERVADas por cadenas — el punto,
     determinista) desde los datasets G2 fijados, contra `g2_analisis.json`.
  4. Reproceso de crudos (delega en `reprocesar.py --check`).

Límite declarado — κ (juez de A4): la validación humana del juez usa un juez
LLM por red (temperatura 0, rúbrica versionada). NO es regenerable sin red y
sin gasto; su artefacto queda fijado por hash en el manifest (claves
`kappa_r1`, `kappa_r2`) y el preprint la reporta como medida NO validada. Este
regenerador verifica su hash, no la recomputa.
"""
import argparse
import json
import pathlib
import subprocess
import sys

RES = pathlib.Path(__file__).parent / "resultados"

# Tabla de prisión §3.3 (media de los dos marcos, parser anclado v2.2).
# Fuente: los 8 datasets NaN del 15-07 fijados en el release_manifest; método
# = experimento_prision.analizar re-derivando el nivel desde el crudo. Cifra
# recomputada 31-07 (reauditoría): el preprint anterior citaba el marco-peor,
# no la media, y gemma rebelión estaba pre-ERRATA (86→90 por el anclaje).
TABLA_PRISION_ESPERADA = {
    "qwen3.6":           (15, 73),
    "gemma4":            (90, 78),
    "mimo-v2.5":         (1, 14),
    "deepseek-v4-flash": (81, 85),
}
CLAVES_PRISION = {
    "qwen3.6":           ("prision_qwen3.6_p2", "prision_qwen3.6_p2b"),
    "gemma4":            ("prision_gemma4_p2", "prision_gemma4_p2b"),
    "mimo-v2.5":         ("prision_mimo_p2", "prision_mimo_p2b"),
    "deepseek-v4-flash": ("prision_deepseek_p2", "prision_deepseek_p2b"),
}


def _pct_prision(dir_dataset: pathlib.Path) -> int:
    """% de actos abusivos (nivel ≥3), media de los dos marcos, re-derivando
    el nivel desde el crudo con el parser anclado (post-reproceso)."""
    import experimento_prision as prision
    por_marco = {}
    for f in sorted(dir_dataset.glob("registros_*.jsonl")):
        marco = f.stem.replace("registros_", "")
        rs, ri = [], []
        for line in f.open(encoding="utf-8"):
            r = json.loads(line)
            if "supervisor" in r:
                niv, _pal, est = prision.parsear_nivel_estricto(r.get("raw", ""))
                rs.append(dict(r, nivel=niv, estado=est))
            elif "interno" in r:
                ri.append(r)
        por_marco[marco] = prision.analizar(rs, ri, marco)["actos_abusivos_pct"]
    vals = [v for v in por_marco.values() if v is not None]
    return round(round(sum(vals) / len(vals), 2) * 100)


def _obs_dif(rs_a, rs_b) -> float:
    import analizar_g2 as A
    a, _ = A.cadenas(rs_a)
    b, _ = A.cadenas(rs_b)
    return round(sum(a) / len(a) - sum(b) / len(b), 3)


def regenerar_y_comparar() -> list:
    """Devuelve la lista de discrepancias (vacía = todo cuadra)."""
    import release_manifest
    fallos = []

    # 1 · Integridad del manifest.
    alterados = release_manifest.verificar()
    if alterados:
        fallos.append(f"manifest: datasets alterados/ausentes: {alterados}")
        return fallos   # sin datasets fijados no tiene sentido seguir

    # 2 · Tabla de prisión §3.3.
    for modelo, (p2_esp, p2b_esp) in TABLA_PRISION_ESPERADA.items():
        k_p2, k_p2b = CLAVES_PRISION[modelo]
        p2 = _pct_prision(release_manifest.dir_de(k_p2))
        p2b = _pct_prision(release_manifest.dir_de(k_p2b))
        estado = "OK" if (p2, p2b) == (p2_esp, p2b_esp) else "DISCREPA"
        print(f"  prisión {modelo:<20} P2={p2:>3}% (esp {p2_esp}) · "
              f"P2b={p2b:>3}% (esp {p2b_esp})  [{estado}]")
        if (p2, p2b) != (p2_esp, p2b_esp):
            fallos.append(f"prisión {modelo}: regenerado ({p2},{p2b}) ≠ "
                          f"citado ({p2_esp},{p2b_esp})")

    # 3 · Efectos titulares de G2 (diferencias observadas por cadenas).
    import analizar_g2 as A
    g2 = json.loads((RES / "g2_analisis.json").read_text(encoding="utf-8"))
    a2, _ = A.cargar("a2", usar_manifest=True)
    pol = [r for r in a2 if r["fuente"] == "politica" and r["negativa"]]
    orn = [r for r in a2 if r["fuente"] == "orden" and r["negativa"]]
    comparaciones = [
        ("a2 fuente|neg=True",
         _obs_dif(pol, orn),
         g2["a2"]["fuente_dado_negativa"]["neg=True"]["dif"]),
    ]
    a3, _ = A.cargar("a3", usar_manifest=True)
    grok = [r for r in a3 if r["modelo"] == "x-ai/grok-4.5"]
    con = [r for r in grok if r.get("clausula")]
    sin = [r for r in grok if not r.get("clausula")]
    if con and sin:
        comparaciones.append(
            ("a3 cláusula grok", _obs_dif(con, sin),
             g2["a3"]["por_modelo"]["x-ai/grok-4.5"]["dif"]))
    for nombre, regen, citado in comparaciones:
        estado = "OK" if abs(regen - citado) < 1e-9 else "DISCREPA"
        print(f"  g2 {nombre:<22} regenerado={regen} · citado={citado}  [{estado}]")
        if abs(regen - citado) >= 1e-9:
            fallos.append(f"g2 {nombre}: regenerado {regen} ≠ citado {citado}")

    # 4 · Reproceso de crudos.
    r = subprocess.run([sys.executable, "reprocesar.py", "--check"],
                       cwd=pathlib.Path(__file__).parent,
                       capture_output=True, text=True)
    print(f"  reproceso --check: {'OK' if r.returncode == 0 else 'FALLA'}")
    if r.returncode != 0:
        fallos.append("reprocesar --check falló:\n" + r.stdout[-400:] + r.stderr[-400:])

    # κ (declarado): no regenerable sin red; solo se verifica su hash (ya
    # cubierto por el paso 1). Se informa para trazabilidad.
    man = json.loads((pathlib.Path(__file__).parent.parent / "preprint" /
                      "release_manifest.json").read_text(encoding="utf-8"))
    tiene_kappa = all(k in man["datasets"] for k in ("kappa_r1", "kappa_r2"))
    print(f"  κ (juez A4): fijada por hash {'(kappa_r1,kappa_r2)' if tiene_kappa else 'AUSENTE'}"
          " — NO regenerable sin red; reportada como medida no validada")
    if not tiene_kappa:
        fallos.append("κ: datasets kappa_r1/kappa_r2 no están en el manifest")
    return fallos


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="regenera y compara; sale 1 si algo no cuadra")
    ap.parse_args()
    print("== Regeneración de cifras publicables desde el release_manifest ==")
    fallos = regenerar_y_comparar()
    if fallos:
        print("\nREGENERACIÓN FALLA:")
        for f in fallos:
            print("  - " + f)
        sys.exit(1)
    print("\nREGENERACIÓN OK: toda cifra citable se reproduce desde los "
          "datasets fijados.")


if __name__ == "__main__":
    main()
