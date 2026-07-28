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
    (RES / "gfinal_robustez.json").write_text(
        json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    for m, filas in salida.items():
        if isinstance(filas, dict) and "sin_degradacion" in filas:
            difs = [v["dif"] for v in filas.values() if v["dif"] is not None]
            print(f"{m.split('/')[-1]:22} H1 LOCO/LOPO rango de dif:"
                  f" [{min(difs):+.2f}, {max(difs):+.2f}]")
    print(f"Guardado en {RES / 'gfinal_robustez.json'}")


if __name__ == "__main__":
    main()
