"""Robustez EXPLORATORIA de H1 (revisión externa, hallazgo 13): los IC del
G-final están condicionados al banco de tareas (3 supervisores, 3 contenidos,
personas y marcos fijos). Este script cuantifica esa condicionalidad con
leave-one-content-out y leave-one-supervisor-out sobre los mismos fixtures.
No pre-registrado: descriptivo, sin decisión confirmatoria.

Uso: python analizar_gfinal_robustez.py   (usa el release manifest)
"""
import json
import pathlib
import random

from analizar_gfinal import boot, cargar

RES = pathlib.Path(__file__).parent / "resultados"
SEED = 20260729


def main():
    man = json.loads((pathlib.Path(__file__).parent.parent / "preprint" /
                      "release_manifest.json").read_text())
    a, _ = cargar("A", str(pathlib.Path(__file__).parent /
                           man["datasets"]["gfinal_A"]["dir"]))
    rng = random.Random(SEED)
    salida = {"seed": SEED, "nota": "exploratorio; H1 pooled por modelo"}
    for m in sorted({r["modelo"] for r in a}):
        rm = [r for r in a if r["modelo"] == m]
        filas = {}
        for cont in ("degradacion", "aislamiento", "privacion"):
            sub = [r for r in rm if r["contenido"] != cont]
            b = boot(rng, [r for r in sub if r["clausula"]],
                     [r for r in sub if not r["clausula"]])
            filas[f"sin_{cont}"] = {"dif": b.get("dif"), "ic95": b.get("ic95")}
        for sup in sorted({r["supervisor"] for r in rm}):
            sub = [r for r in rm if r["supervisor"] != sup]
            b = boot(rng, [r for r in sub if r["clausula"]],
                     [r for r in sub if not r["clausula"]])
            filas[f"sin_{sup.split()[0]}"] = {"dif": b.get("dif"),
                                              "ic95": b.get("ic95")}
        salida[m] = filas
    # Sensibilidad ADICIONAL (auditoría 31-07, P1.10): bootstrap de
    # DIFERENCIAS EMPAREJADAS por (dominio, contenido, rep, supervisor) —
    # las celdas con/sin cláusula comparten diseño aunque sean mundos
    # independientes. No sustituye al análisis pre-registrado (no pareado).
    from analizar_gfinal import cadenas
    for m in sorted({r["modelo"] for r in a}):
        rm = [r for r in a if r["modelo"] == m]
        def _props(rs):
            por = {}
            for r in rs:
                k = (r["dominio"], r["contenido"], r["rep"], r["supervisor"])
                por.setdefault(k, []).append(r)
            return {k: cadenas(v)[0][0] for k, v in por.items()
                    if cadenas(v)[0]}
        con = _props([r for r in rm if r["clausula"]])
        sin = _props([r for r in rm if not r["clausula"]])
        pares = [con[k] - sin[k] for k in con.keys() & sin.keys()]
        if pares:
            ds = sorted(sum(rng.choice(pares) for _ in pares) / len(pares)
                        for _ in range(5000))
            salida[m]["h1_emparejado"] = {
                "dif_media": round(sum(pares) / len(pares), 3),
                "ic95": [round(ds[125], 3), round(ds[4875], 3)],
                "n_pares": len(pares)}
    (RES / "gfinal_robustez.json").write_text(
        json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    for m, filas in salida.items():
        if isinstance(filas, dict) and "sin_degradacion" in filas:
            difs = [v["dif"] for k2, v in filas.items()
                    if k2 != "h1_emparejado" and v.get("dif") is not None]
            print(f"{m.split('/')[-1]:22} H1 LOCO/LOPO rango de dif:"
                  f" [{min(difs):+.2f}, {max(difs):+.2f}]")
    print(f"Guardado en {RES / 'gfinal_robustez.json'}")


if __name__ == "__main__":
    main()
