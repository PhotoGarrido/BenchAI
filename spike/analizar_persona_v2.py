"""Biografías v2: hipótesis B1-B4 de PERSONALIDAD.md §14.

Por modelo y rasgo (bootstrap por ítem, B=2000, semilla fija):
  elasticidad v2   P(polo alto | bio alta) − P(polo alto | bio baja), ×100
  medio            P(polo alto | bio media), ×100
  comprobación     nivel leído 1-5 por nivel de biografía
  posición neutro  (R2 sin biografía − bio baja) / (bio alta − bio baja):
                   hacia qué polo se va el modelo cuando no se le dice nada.
Compara con la elasticidad de las biografías v1 (P1, resumen.json).

Uso: python analizar_persona_v2.py
"""

import json
import pathlib
from collections import defaultdict

import numpy as np

import analizar_personalidad_p1 as ap1
import personalidad_p1_items as p1
from analizar_personalidad import B, SEMILLA, _f, cargar

AQUI = pathlib.Path(__file__).parent
DIR = AQUI / "resultados" / "personalidad_persona_v2"
RASGOS = p1.RASGOS


def _boot_dif(a, b, rng):
    comunes = [k for k in a if k in b]
    d = np.array([a[k] - b[k] for k in comunes])
    if len(d) == 0:
        return None
    bs = d[rng.integers(0, len(d), size=(B, len(d)))].mean(axis=1)
    return (100 * d.mean(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5))


def main():
    rng = np.random.default_rng(SEMILLA)
    v2 = cargar(DIR)
    p1d = cargar(ap1.DIR)
    v1 = json.loads((ap1.DIR / "resumen.json").read_text(encoding="utf-8"))["modelos"]
    res = {}
    for m, filas in v2.items():
        ok = [r for r in filas if r["estado"] == "OK"]
        g = {}
        for t in RASGOS:
            nivel = {n: {r["item"]: 1.0 if r["elige_alto"] else 0.0 for r in ok
                         if r["brazo"] == "sit_persona2" and r["rasgo"] == t and r["nivel"] == n}
                     for n in ("bajo", "medio", "alto")}
            comp = {n: [r["nivel_leido"] for r in ok if r["brazo"] == "comprobacion"
                        and r["rasgo"] == t and r["nivel"] == n] for n in ("bajo", "medio", "alto")}
            neutro = defaultdict(list)
            for r in p1d.get(m, []):
                if r["brazo"] == "sit_personaje" and r["estado"] == "OK" and r["rasgo"] == t:
                    neutro[r["item"]].append(1.0 if r["elige_alto"] else 0.0)
            mb, mm, ma = (np.mean(list(nivel[n].values())) if nivel[n] else np.nan
                          for n in ("bajo", "medio", "alto"))
            mn = np.mean([np.mean(v) for v in neutro.values()]) if neutro else np.nan
            g[t] = dict(
                elasticidad=_boot_dif(nivel["alto"], nivel["bajo"], rng),
                bajo=100 * mb, medio=100 * mm, alto=100 * ma,
                gradiente=bool(mb <= mm <= ma),
                comprobacion={n: float(np.mean(v)) if v else None for n, v in comp.items()},
                posicion_neutro=(float((mn - mb) / (ma - mb)) if ma - mb > .05 else None),
                elasticidad_v1=(v1[m]["rasgos"][t]["elasticidad_conducta"][0]
                                if m in v1 else None))
        res[m] = g
    ms = list(res)
    media = lambda t, f: float(np.nanmean([f(res[m][t]) for m in ms]))  # noqa: E731
    el = {t: media(t, lambda g: g["elasticidad"][0]) for t in RASGOS}
    el1 = {t: media(t, lambda g: g["elasticidad_v1"] if g["elasticidad_v1"] is not None
                    else np.nan) for t in RASGOS}
    comp = {t: media(t, lambda g: (g["comprobacion"]["alto"] or np.nan)
                     - (g["comprobacion"]["bajo"] or np.nan)) for t in RASGOS}
    grad = {t: bool(media(t, lambda g: g["bajo"]) <= media(t, lambda g: g["medio"])
                    <= media(t, lambda g: g["alto"])) for t in RASGOS}
    disc = {}
    for t in RASGOS:
        v = [res[m][t]["elasticidad"] for m in ms]
        semi = np.mean([(x[2] - x[1]) / 2 for x in v])
        disc[t] = float((max(x[0] for x in v) - min(x[0] for x in v)) / semi)
    crit = {
        "B1": {t: el[t] for t in ("E", "A", "H")},
        "B1_cumple": all(el[t] < 90 for t in ("E", "A", "H")),
        "B2": comp, "B2_cumple": sum(x >= 2 for x in comp.values()) >= 5,
        "B3": grad, "B3_cumple": sum(grad.values()) >= 5,
        "B4": disc, "B4_cumple": sum(x >= 2 for x in disc.values()) >= 3,
    }
    si = lambda b: "**CUMPLE**" if b else "**NO cumple**"  # noqa: E731
    L = ["# Biografías v2 (§14)", "", f"Modelos ({len(ms)}): {', '.join(ms)}.", "",
         "## Hipótesis", "",
         "- **B1** elasticidad < 90 en E, A y H (media de modelos; v1 entre paréntesis): "
         + ", ".join(f"{t} {el[t]:.0f} ({el1[t]:.0f})" for t in ("E", "A", "H"))
         + f" → {si(crit['B1_cumple'])}.",
         "- **B2** comprobación alto − bajo ≥ 2 (escala 1-5) en ≥ 5/6: "
         + ", ".join(f"{t} {comp[t]:.1f}" for t in RASGOS) + f" → {si(crit['B2_cumple'])}.",
         "- **B3** gradiente bajo ≤ medio ≤ alto en ≥ 5/6: "
         + ", ".join(f"{t} {'sí' if grad[t] else 'no'}" for t in RASGOS)
         + f" → {si(crit['B3_cumple'])}.",
         "- **B4** la elasticidad distingue modelos (cociente ≥ 2) en ≥ 3/6: "
         + ", ".join(f"{t} {disc[t]:.1f}" for t in RASGOS) + f" → {si(crit['B4_cumple'])}.",
         "", "## Elasticidad v2 por modelo (alto − bajo, pp) · v1 · posición del personaje sin biografía (0 = bio baja, 1 = bio alta)", "",
         "| modelo | " + " | ".join(RASGOS) + " |", "|---|" + "---|" * len(RASGOS)]
    for m in ms:
        L.append(f"| {m} | " + " | ".join(
            f"{res[m][t]['elasticidad'][0]:.0f} · {_f(res[m][t]['elasticidad_v1'])}"
            f" · {_f(res[m][t]['posicion_neutro'], 2)}" for t in RASGOS) + " |")
    L += ["", "## Elección del polo alto por nivel de biografía (media de modelos, %)", "",
          "| rasgo | baja | media | alta | comprobación baja / media / alta (1-5) |",
          "|---|---|---|---|---|"]
    for t in RASGOS:
        c = lambda n: np.nanmean([res[m][t]["comprobacion"][n] or np.nan for m in ms])  # noqa: E731
        L.append(f"| {t} | {media(t, lambda g: g['bajo']):.0f} | {media(t, lambda g: g['medio']):.0f}"
                 f" | {media(t, lambda g: g['alto']):.0f} | {c('bajo'):.1f} / {c('medio'):.1f}"
                 f" / {c('alto'):.1f} |")
    texto = "\n".join(L) + "\n"
    (DIR / "PERSONA_V2.md").write_text(texto, encoding="utf-8")
    (DIR / "persona_v2.json").write_text(json.dumps({"modelos": res, "criterios": crit},
                                                    ensure_ascii=False, indent=2, default=float),
                                         encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
