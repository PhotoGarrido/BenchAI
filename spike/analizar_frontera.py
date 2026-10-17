"""Tanda de frontera: criterios E1-E7 de PERSONALIDAD.md §19 («¿sirve el
instrumento?»), fijados antes de ver los resultados.

Usa todos los modelos con datos de P1 y calibración (18 tras la tanda); los
de FRONTERA son los 9 de la tanda del 16/17-10.

Uso: python analizar_frontera.py  → resultados/personalidad_fc/FRONTERA.md
"""

import json
import pathlib
from collections import defaultdict

import numpy as np

import analizar_personalidad_p1 as ap1
import personalidad_p1_items as p1
from analizar_discriminacion import _id
from analizar_personalidad import B, RE_RECONOCE, SEMILLA, _f, cargar

AQUI = pathlib.Path(__file__).parent
SALIDA = AQUI / "resultados" / "personalidad_fc"
RASGOS = p1.RASGOS
FRONTERA = ("openai_gpt-6.1-sol#low", "anthropic_claude-opus-5.5#low", "google_gemini-4-argon",
            "x-ai_grok-4.5", "moonshotai_kimi-k3", "deepseek_deepseek-v4-pro-0813",
            "qwen_qwen3.8-max-0902#low", "mistralai_mistral-large-4-0", "z-ai_glm-5.3")
V2 = AQUI / "resultados" / "personalidad_persona_v2"


def _r3_por_replica(filas, des, t, rep):
    acc = defaultdict(list)
    for r in filas:
        if (r["brazo"] == "sit_propia" and r.get("rep", 0) == rep and r["estado"] == "OK"
                and r["rasgo"] == t and r["item"] in des):
            acc[r["item"]].append((1.0 if r["elige_alto"] else 0.0) - des[r["item"]])
    return 50 + 50 * np.mean([np.mean(v) for v in acc.values()]) if acc else None


def main():
    rng = np.random.default_rng(SEMILLA)
    datos = cargar(ap1.DIR)
    des = ap1.deseabilidad()
    ms = sorted(m for m in datos if m in des)
    front = [m for m in FRONTERA if m in ms]
    res = {m: ap1.analizar_modelo(datos[m], des[m]) for m in ms}
    out = {"modelos": ms, "frontera": front}

    # E1: discriminación y modelos con algún rasgo distinguible
    media = {t: np.mean([res[m]["rasgos"][t]["R3_ajustada"][0] for m in ms]) for t in RASGOS}
    disc = {}
    for t in RASGOS:
        v = [res[m]["rasgos"][t]["R3_ajustada"] for m in ms]
        semi = np.mean([(x[2] - x[1]) / 2 for x in v])
        disc[t] = float((max(x[0] for x in v) - min(x[0] for x in v)) / semi)
    marcados = {m: [t for t in RASGOS if res[m]["rasgos"][t]["R3_ajustada"][1] > media[t]
                    or res[m]["rasgos"][t]["R3_ajustada"][2] < media[t]] for m in ms}
    n_marc = sum(bool(v) for v in marcados.values())
    out["E1"] = {"discrimina": disc, "rasgos_ge2": sum(x >= 2 for x in disc.values()),
                 "modelos_con_rasgo": n_marc,
                 "cumple": sum(x >= 2 for x in disc.values()) >= 5 and n_marc >= 12}

    # E2: test-retest entre réplicas (modelos con 2 réplicas)
    a, b = [], []
    for m in ms:
        for t in RASGOS:
            x, y = (_r3_por_replica(datos[m], des[m], t, k) for k in (0, 1))
            if x is not None and y is not None:
                a.append(x)
                b.append(y)
    r = float(np.corrcoef(a, b)[0, 1]) if len(a) > 3 else None
    out["E2"] = {"r": r, "n": len(a), "dif_media": float(np.mean(np.abs(np.subtract(a, b)))),
                 "cumple": r is not None and r >= 0.90}

    # E3: balance de deseabilidad por modelo nuevo (su propio juicio, por rasgo)
    sel = {s[0]: s[1] for s in p1.situaciones()}
    bal = {}
    for m in front:
        bal[m] = {t: float(np.mean([des[m][i] for i in des[m] if sel.get(i) == t]))
                  for t in RASGOS}
    ok3 = {m: sum(.25 <= v <= .75 for v in bal[m].values()) >= 5 for m in front}
    out["E3"] = {"balance": bal, "por_modelo": ok3, "cumple": all(ok3.values())}

    # E4: no válidas/negativas en R3
    malas = {m: float(np.mean([r["estado"] != "OK" for r in datos[m]
                               if r["brazo"] == "sit_propia"])) for m in ms}
    out["E4"] = {"tasa": malas, "cumple": all(v < .05 for v in malas.values())}

    # E5: reconocimiento en las sondas de R3 (frontera)
    son = [bool(RE_RECONOCE.search(r["raw"])) for m in front for r in datos[m]
           if r["brazo"] == "sonda" and r.get("registro") == "sit_propia"]
    out["E5"] = {"reconoce": [int(sum(son)), len(son)],
                 "cumple": bool(son) and sum(son) / len(son) <= 1 / 3}

    # E6: «tú» frente a personaje en frontera (bootstrap por ítem)
    por_item = defaultdict(list)
    for m in front:
        d = des[m]
        c2, c3 = defaultdict(list), defaultdict(list)
        for r_ in datos[m]:
            if r_["estado"] != "OK" or r_["item"] not in d:
                continue
            x = abs((1.0 if r_["elige_alto"] else 0.0) - d[r_["item"]])
            if r_["brazo"] == "sit_personaje":
                c2[r_["item"]].append(x)
            elif r_["brazo"] == "sit_propia":
                c3[r_["item"]].append(x)
        for k in c2:
            if c3.get(k):
                por_item[k].append(np.mean(c2[k]) - np.mean(c3[k]))
    mi = np.array([np.mean(v) for v in por_item.values()])
    bs = mi[rng.integers(0, len(mi), size=(B, len(mi)))].mean(axis=1)
    e6 = [100 * mi.mean(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5)]
    out["E6"] = {"pp": e6, "cumple": e6[1] > 0}

    # E7: elasticidad v2 en frontera
    v2 = cargar(V2)
    el = {}
    for t in ("O", "C", "E", "A", "N", "H"):
        vals = []
        for m in front:
            if m not in v2:
                continue
            nivel = {n: {r_["item"]: 1.0 if r_["elige_alto"] else 0.0 for r_ in v2[m]
                         if r_["brazo"] == "sit_persona2" and r_["estado"] == "OK"
                         and r_["rasgo"] == t and r_["nivel"] == n} for n in ("alto", "bajo")}
            comunes = [k for k in nivel["alto"] if k in nivel["bajo"]]
            if comunes:
                vals.append(100 * np.mean([nivel["alto"][k] - nivel["bajo"][k] for k in comunes]))
        el[t] = float(np.mean(vals)) if vals else None
    out["E7"] = {"elasticidad_media": el,
                 "cumple": all(el[t] is not None and el[t] < 90 for t in ("E", "A", "H"))}

    si = lambda x: "**CUMPLE**" if x else "**NO cumple**"  # noqa: E731
    L = ["# Tanda de frontera · ¿sirve el instrumento? (§19)", "",
         f"{len(ms)} modelos ({len(front)} de frontera). Criterios fijados antes de ver"
         " los resultados.", "", "## Criterios del cuadro", "",
         f"- **E1 · discrimina**: cociente ≥ 2 en {out['E1']['rasgos_ge2']}/6 rasgos ("
         + ", ".join(f"{t} {disc[t]:.1f}" for t in RASGOS)
         + f"); modelos con algún rasgo distinguible: {n_marc}/{len(ms)} → {si(out['E1']['cumple'])}.",
         f"- **E2 · fiable**: test-retest r = {_f(r, 3)} ({len(a)} modelo×rasgo), dif. media"
         f" {out['E2']['dif_media']:.1f} → {si(out['E2']['cumple'])}.",
         f"- **E3 · calibración válida en modelos nuevos**: {sum(ok3.values())}/{len(front)}"
         f" modelos con la escala equilibrada (25-75 %) en ≥ 5/6 rasgos → {si(out['E3']['cumple'])}.",
         f"- **E4 · sin pérdidas en R3** (< 5 %): máx. {100 * max(malas.values()):.1f} %"
         f" ({max(malas, key=malas.get)}) → {si(out['E4']['cumple'])}.", "",
         "## Módulos secundarios", "",
         f"- **E5 · disfraz en frontera**: reconocen el test en {out['E5']['reconoce'][0]}/"
         f"{out['E5']['reconoce'][1]} sondas de R3 → {si(out['E5']['cumple'])}.",
         f"- **E6 · «tú» frente a personaje en frontera**: {e6[0]:+.1f} pp [IC {e6[1]:+.1f},"
         f" {e6[2]:+.1f}] → {si(out['E6']['cumple'])}.",
         "- **E7 · fidelidad de persona sin saturar en frontera**: "
         + ", ".join(f"{t} {_f(v)}" for t, v in el.items()) + f" → {si(out['E7']['cumple'])}.",
         "", "## E3 · deseabilidad media de la escala según cada modelo de frontera (%)", "",
         "| modelo | " + " | ".join(RASGOS) + " |", "|---|" + "---|" * len(RASGOS)]
    for m in front:
        L.append(f"| {_id(m)} | " + " | ".join(f"{100 * bal[m][t]:.0f}" for t in RASGOS) + " |")
    L += ["", "## E4 · no válidas en R3 por modelo (%)", "",
          ", ".join(f"{_id(m)} {100 * v:.1f}" for m, v in malas.items())]
    texto = "\n".join(L) + "\n"
    (SALIDA / "FRONTERA.md").write_text(texto, encoding="utf-8")
    (SALIDA / "frontera.json").write_text(json.dumps(out, ensure_ascii=False, indent=2,
                                                     default=float), encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
