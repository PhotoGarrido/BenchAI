"""Norma descriptiva frente a ideal: hipótesis N1-N4 de PERSONALIDAD.md §12.

Fuentes (por modelo m y situación i, media de los dos órdenes A/B):
  c2(m,i)  elige el polo alto el personaje (P1, sit_personaje)
  c3(m,i)  elige el polo alto «tú»         (P1, sit_propia)
  d(m,i)   el polo alto es el IDEAL        (calibración de deseabilidad)
  n(m,i)   el polo alto es lo que ELEGIRÍA la mayoría (calibrar_norma.py)

  ajustada_ref = 50 + 50 · media_i(c3 − ref)    con ref = d o n
Bootstrap por ítem (B=2000, semilla fija): todas las parejas modelo×ítem de
un ítem entran o salen juntas.

Uso: python analizar_norma.py
"""

import json
import pathlib
from collections import defaultdict

import numpy as np

import analizar_personalidad_p1 as ap1
import personalidad_p1_items as p1
from analizar_personalidad import B, SEMILLA, _f, cargar

AQUI = pathlib.Path(__file__).parent
NORMA = AQUI / "resultados" / "personalidad_p1_norma"
RASGOS = p1.RASGOS
RASGO_DE = {s[0]: s[1] for s in p1.situaciones()}


def _medias(registros, campo):
    acc = defaultdict(list)
    for r in registros:
        if r["estado"] == "OK" and r.get(campo) is not None:
            acc[r["item"]].append(1.0 if r[campo] else 0.0)
    return {k: float(np.mean(v)) for k, v in acc.items()}


def norma():
    out = {}
    for d in sorted(NORMA.iterdir()):
        f = d / "registros.jsonl"
        if d.is_dir() and f.exists():
            ultimo = {}
            for linea in f.read_text(encoding="utf-8").splitlines():
                r = json.loads(linea)
                ultimo[r["id"]] = r
            out[d.name] = _medias(ultimo.values(), "alto_elegido_mayoria")
    return out


def _boot(por_item, rng):
    """Media de medias por ítem e IC percentil remuestreando ítems."""
    x = np.array([np.mean(v) for v in por_item.values() if v])
    bs = x[rng.integers(0, len(x), size=(B, len(x)))].mean(axis=1)
    return float(x.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def main():
    rng = np.random.default_rng(SEMILLA)
    datos = cargar(ap1.DIR)
    ideal = ap1.deseabilidad()
    nor = norma()
    ms = [m for m in datos if m in ideal and m in nor]
    c2 = {m: _medias([r for r in datos[m] if r["brazo"] == "sit_personaje"], "elige_alto")
          for m in ms}
    c3 = {m: _medias([r for r in datos[m] if r["brazo"] == "sit_propia"], "elige_alto")
          for m in ms}
    res = {"modelos": ms}

    # N1: norma descriptiva − ideal, por rasgo
    n1 = {}
    for t in RASGOS:
        por_item = defaultdict(list)
        for m in ms:
            for i, v in nor[m].items():
                if RASGO_DE.get(i) == t and i in ideal[m]:
                    por_item[i].append(v - ideal[m][i])
        n1[t] = [100 * x for x in _boot(por_item, rng)]
    pred = {"C": -1, "A": -1, "H": -1, "N": +1}
    aciertos = sum((n1[t][2] < 0) if s < 0 else (n1[t][1] > 0) for t, s in pred.items())
    res["N1"] = {"por_rasgo": n1, "aciertos": aciertos, "sostenida": aciertos >= 3}

    # Puntuaciones ajustadas por modelo y rasgo, con IC por ítem
    def ajustada(m, t, ref):
        por_item = {i: [c3[m][i] - ref[m][i]] for i in c3[m]
                    if RASGO_DE.get(i) == t and i in ref[m]}
        p, lo, hi = _boot(por_item, rng)
        return 50 + 50 * p, 50 + 50 * lo, 50 + 50 * hi

    aj = {k: {m: {t: ajustada(m, t, ref) for t in RASGOS} for m in ms}
          for k, ref in (("ideal", ideal), ("norma", nor))}
    res["ajustada"] = aj
    # N2: desviación absoluta media respecto de 50
    dev = {k: float(np.mean([abs(aj[k][m][t][0] - 50) for m in ms for t in RASGOS]))
           for k in aj}
    res["N2"] = {"desviacion_media": dev, "sostenida": dev["norma"] < dev["ideal"]}

    # N3: mecanismo. Distancias absolutas por (modelo, ítem).
    d_norma, d_ideal = defaultdict(list), defaultdict(list)
    for m in ms:
        for i in c2[m]:
            if i in c3[m] and i in nor[m] and i in ideal[m]:
                # >0 = el personaje está más cerca de la norma descriptiva que «tú»
                d_norma[i].append(abs(c3[m][i] - nor[m][i]) - abs(c2[m][i] - nor[m][i]))
                # >0 = «tú» está más cerca del ideal que el personaje
                d_ideal[i].append(abs(c2[m][i] - ideal[m][i]) - abs(c3[m][i] - ideal[m][i]))
    a = [100 * x for x in _boot(d_norma, rng)]
    b = [100 * x for x in _boot(d_ideal, rng)]
    res["N3"] = {"personaje_mas_cerca_de_norma": a, "tu_mas_cerca_del_ideal": b,
                 "sostenida": a[1] > 0 and b[1] > 0}
    # Por modelo (dirección)
    res["N3_por_modelo"] = {}
    for m in ms:
        xa = [abs(c3[m][i] - nor[m][i]) - abs(c2[m][i] - nor[m][i])
              for i in c2[m] if i in c3[m] and i in nor[m]]
        xb = [abs(c2[m][i] - ideal[m][i]) - abs(c3[m][i] - ideal[m][i])
              for i in c2[m] if i in c3[m] and i in ideal[m]]
        res["N3_por_modelo"][m] = [100 * float(np.mean(xa)), 100 * float(np.mean(xb))]

    # N4: discriminación (rango entre modelos / semiancho medio del IC)
    disc = {}
    for k in aj:
        disc[k] = {}
        for t in RASGOS:
            v = [aj[k][m][t] for m in ms]
            semi = np.mean([(x[2] - x[1]) / 2 for x in v])
            disc[k][t] = float((max(x[0] for x in v) - min(x[0] for x in v)) / semi)
    cuenta = {k: sum(x >= 2 for x in disc[k].values()) for k in disc}
    res["N4"] = {"discrimina": disc, "rasgos_ge2": cuenta,
                 "sostenida": cuenta["norma"] >= cuenta["ideal"]}

    si = lambda x: "**SOSTENIDA**" if x else "**NO sostenida**"  # noqa: E731
    pc = lambda t: f"{t[0]:+.1f} [{t[1]:+.1f}, {t[2]:+.1f}]"  # noqa: E731
    L = ["# Norma descriptiva frente a ideal (§12)", "",
         f"Modelos ({len(ms)}): {', '.join(ms)}. Hipótesis fijadas antes de medir.", "",
         "## Hipótesis", "",
         "- **N1 · la norma descriptiva va hacia lo cómodo** (pp, descriptiva − ideal; se"
         " predice < 0 en C, A, H y > 0 en N): "
         + ", ".join(f"{t} {pc(n1[t])}" for t in RASGOS)
         + f" → {aciertos}/4 → {si(res['N1']['sostenida'])}.",
         f"- **N2 · absorbe el sesgo sistemático** (|R3 ajustada − 50| medio): ideal"
         f" {dev['ideal']:.1f}, descriptiva {dev['norma']:.1f} → {si(res['N2']['sostenida'])}.",
         f"- **N3 · mecanismo**: el personaje, más cerca de la norma descriptiva que «tú»:"
         f" {pc(a)} pp; «tú», más cerca del ideal que el personaje: {pc(b)} pp →"
         f" {si(res['N3']['sostenida'])}.",
         f"- **N4 · no pierde discriminación** (rasgos con cociente ≥ 2): ideal"
         f" {cuenta['ideal']}/6, descriptiva {cuenta['norma']}/6 → {si(res['N4']['sostenida'])}.",
         "", "## N3 por modelo (pp; >0 = en la dirección predicha)", "",
         "| modelo | personaje más cerca de la norma | «tú» más cerca del ideal |",
         "|---|---|---|"]
    for m, (x, y) in res["N3_por_modelo"].items():
        L.append(f"| {m} | {x:+.1f} | {y:+.1f} |")
    L += ["", "## R3 ajustada: contra el ideal / contra la norma descriptiva", "",
          "| modelo | " + " | ".join(RASGOS) + " |", "|---|" + "---|" * len(RASGOS)]
    for m in ms:
        L.append(f"| {m} | " + " | ".join(
            f"{aj['ideal'][m][t][0]:.0f} / {aj['norma'][m][t][0]:.0f}" for t in RASGOS) + " |")
    L += ["", "## Discriminación (rango / semiancho del IC): ideal / descriptiva", "",
          "| " + " | ".join(RASGOS) + " |", "|" + "---|" * len(RASGOS),
          "| " + " | ".join(f"{_f(disc['ideal'][t], 1)} / {_f(disc['norma'][t], 1)}"
                            for t in RASGOS) + " |"]
    texto = "\n".join(L) + "\n"
    (NORMA / "NORMA.md").write_text(texto, encoding="utf-8")
    (NORMA / "norma.json").write_text(json.dumps(res, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
