"""Prueba de discriminación (PERSONALIDAD.md §10): criterios D1-D4 y H1 con
los 9 modelos, autoinforme de elección forzada y anclado, y relación
exploratoria con el ISS de PsicoBench.

Reutiliza analizar_personalidad_p1 (reejecuta su análisis con todos los
modelos que haya) y personalidad_fc (puntuación de elección forzada).
Escribe resultados/personalidad_fc/DISCRIMINACION.md y discriminacion.json.

Uso: python analizar_discriminacion.py
"""

import json
import pathlib
from collections import defaultdict

import numpy as np

import analizar_personalidad_p1 as ap1
import personalidad_fc as fc
import personalidad_p1_items as p1
from analizar_personalidad import B, SEMILLA, _f, _ic, cargar

AQUI = pathlib.Path(__file__).parent
RASGOS = p1.RASGOS
EXTREMOS = ("openai_gpt-5.6-luna", "google_gemini-3.7-flash")


#: Prefijos de organización de OpenRouter: la carpeta «org_modelo» es el id
#: «org/modelo». Los ids de NaN no llevan organización ni guion bajo.
ORGS = ("openai", "anthropic", "google", "x-ai", "moonshotai", "deepseek", "qwen",
        "mistralai", "z-ai", "meta", "minimax")

#: Modelos medidos en personalidad con un id distinto del de su entrada del ISS
#: (PERSONALIDAD.md §47): MiniMax M3.1 Flash se midió en el ISS en fase stealth
#: como space-bunny-alpha (#low y #high, desvelado el 19-10-2026) y en
#: personalidad, ya público, con su id de OpenRouter y el mismo #low.
ISS_DE = {"minimax/minimax-m3.1-flash#low": "stealth/space-bunny-alpha#low"}


def _id(dirname):
    return dirname.replace("_", "/", 1) if "_" in dirname and "/" not in dirname \
        and dirname.split("_")[0] in ORGS else dirname


def iss_por_modelo():
    e = json.loads((AQUI.parent / "benchmark" / "psicobench.json").read_text(encoding="utf-8"))
    out = {}
    for x in e["entradas"]:
        out.setdefault(x["modelo"], x["iss"])
    for m, iss_id in ISS_DE.items():
        if iss_id in out:
            out.setdefault(m, out[iss_id])
    return out


def _r(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = ~(np.isnan(x) | np.isnan(y))
    if ok.sum() < 3 or np.std(x[ok]) == 0 or np.std(y[ok]) == 0:
        return None
    return float(np.corrcoef(x[ok], y[ok])[0, 1])


def fc_scores():
    """{modelo: {rasgo: (punto, lo, hi)}}, IC por bootstrap de parejas."""
    rng = np.random.default_rng(SEMILLA)
    out = {}
    for m, filas in fc._leer("fc").items():
        por_par = defaultdict(list)
        for r in filas:
            por_par[r["par"]].append(r)
        pares = list(por_par)
        g = {}
        for t in RASGOS:
            # aportación media por pareja a este rasgo (None si no participa)
            v = {}
            for p in pares:
                a = fc.puntuar(por_par[p]).get(t)
                if a:
                    v[p] = np.mean(a)
            x = np.array(list(v.values()))
            bs = x[rng.integers(0, len(x), size=(B, len(x)))].mean(axis=1)
            g[t] = (50 + 50 * x.mean(), 50 + 50 * np.percentile(bs, 2.5),
                    50 + 50 * np.percentile(bs, 97.5))
        out[m] = g
    return out


def anclado(filas):
    """R1 anclado: posición del «yo» entre la persona baja (0) y alta (1)
    que el propio modelo puntúa, por ítem; media por rasgo ×100."""
    rasgo = {i[0]: i[1] for i in p1.AUTOINFORME}
    yo, pa = defaultdict(list), defaultdict(dict)
    for r in filas:
        if r["estado"] != "OK":
            continue
        if r["brazo"] == "auto":
            yo[r["item"]].append(r["puntos"])
        elif r["brazo"] == "auto_persona":
            pa[r["item"]][r["nivel"]] = r["puntos"]
    acc = defaultdict(list)
    for i, v in pa.items():
        if v.get("alto") is not None and v.get("bajo") is not None \
                and v["alto"] > v["bajo"] and yo[i]:
            acc[rasgo[i]].append((np.mean(yo[i]) - v["bajo"]) / (v["alto"] - v["bajo"]))
    return {t: (100 * float(np.mean(acc[t])) if acc[t] else None) for t in RASGOS}


def d2_extremos(datos, des):
    """Diferencia pareada por ítem en R3 ajustada entre los dos extremos."""
    rng = np.random.default_rng(SEMILLA)
    a, b = EXTREMOS
    if a not in datos or b not in datos:
        return None
    item_aj = {}
    for m in EXTREMOS:
        acc = defaultdict(list)
        for r in datos[m]:
            if r["brazo"] == "sit_propia" and r["estado"] == "OK" and r["item"] in des[m]:
                acc[r["item"]].append((1.0 if r["elige_alto"] else 0.0) - des[m][r["item"]])
        item_aj[m] = {k: np.mean(v) for k, v in acc.items()}
    rasgo_de = {s[0]: s[1] for s in p1.situaciones()}
    out = {}
    for t in RASGOS:
        d = np.array([item_aj[b][k] - item_aj[a][k] for k in item_aj[a]
                      if k in item_aj[b] and rasgo_de[k] == t])
        bs = d[rng.integers(0, len(d), size=(B, len(d)))].mean(axis=1)
        # en escala ajustada (50 + 50·x): la diferencia es 50·Δ
        out[t] = (50 * d.mean(), 50 * np.percentile(bs, 2.5), 50 * np.percentile(bs, 97.5))
    return out


def main():
    datos = cargar(ap1.DIR)
    des = ap1.deseabilidad()
    faltan = [m for m in datos if m not in des]
    if faltan:
        raise SystemExit(f"sin calibración de deseabilidad para {faltan}")
    res = {m: ap1.analizar_modelo(f, des[m]) for m, f in datos.items()}
    tr = ap1.transversal(datos, des, res)
    fcs = fc_scores()
    anc = {m: anclado(f) for m, f in datos.items()}
    iss = iss_por_modelo()
    ms = [m for m in res if m in fcs]
    aq = [res[m]["validez"]["aquiescencia"] for m in ms]
    v = lambda m, t, k: res[m]["rasgos"][t][k][0] if res[m]["rasgos"][t][k] else np.nan  # noqa: E731

    crit = {}
    disc = tr["discrimina"]
    crit["D1"] = {t: disc[t]["R3_ajustada"] for t in RASGOS}
    crit["D1_cumple"] = sum((x or 0) >= 2 for x in crit["D1"].values()) >= 3
    d2 = d2_extremos(datos, des)
    crit["D2"] = d2
    crit["D2_cumple"] = bool(d2) and sum(lo > 0 or hi < 0 for _, lo, hi in d2.values()) >= 2
    fila = {}
    for t in RASGOS:
        f = [fcs[m][t][0] for m in ms]
        r3 = [v(m, t, "R3_ajustada") for m in ms]
        r1 = [v(m, t, "R1") for m in ms]
        semi = np.mean([(fcs[m][t][2] - fcs[m][t][1]) / 2 for m in ms])
        fila[t] = dict(
            r_aq_FC=_r(aq, f), r_aq_R1=_r(aq, r1),
            r_FC_R3aj=_r(f, r3), r_R1_R3aj=_r(r1, r3),
            r_anc_R3aj=_r([anc[m][t] if anc[m][t] is not None else np.nan for m in ms], r3),
            discrimina_FC=float((max(f) - min(f)) / semi) if semi else None,
            r_ISS_R3aj=_r([iss.get(_id(m), np.nan) for m in ms], r3),
            r_ISS_FC=_r([iss.get(_id(m), np.nan) for m in ms], f),
            r_ISS_R1=_r([iss.get(_id(m), np.nan) for m in ms], r1))
    crit["por_rasgo"] = fila
    crit["D3_cumple"] = all(abs(fila[t]["r_aq_FC"] or 0) < 0.5 for t in ("C", "N"))
    crit["D4_mejora"] = sum((fila[t]["r_FC_R3aj"] or -9) > (fila[t]["r_R1_R3aj"] or -9)
                            for t in RASGOS)
    crit["D4_cumple"] = crit["D4_mejora"] >= 4
    crit["H1"] = tr["H1"]

    si = lambda b: "**CUMPLE**" if b else "**NO cumple**"  # noqa: E731
    L = ["# Prueba de discriminación (§10)", "",
         f"Modelos: {', '.join(ms)}. Criterios fijados antes de ver los datos de los"
         " 3 modelos nuevos.", "", "## Criterios", "",
         "- **D1** R3 ajustada discrimina (cociente ≥ 2) en ≥ 3 rasgos: "
         + ", ".join(f"{t} {_f(x, 1)}" for t, x in crit["D1"].items())
         + f" → {si(crit['D1_cumple'])}."]
    if d2:
        L.append("- **D2** Luna vs Gemini 3.7 Flash (Gemini − Luna, R3 ajustada) separa ≥ 2 rasgos: "
                 + ", ".join(f"{t} {_ic(x)}" for t, x in d2.items()) + f" → {si(crit['D2_cumple'])}.")
    L += [f"- **D3** |r(aquiescencia, elección forzada)| < 0,5 en C y N: C {_f(fila['C']['r_aq_FC'], 2)},"
          f" N {_f(fila['N']['r_aq_FC'], 2)} (Likert: {_f(fila['C']['r_aq_R1'], 2)},"
          f" {_f(fila['N']['r_aq_R1'], 2)}) → {si(crit['D3_cumple'])}.",
          f"- **D4** elección forzada converge con R3 ajustada mejor que el Likert en ≥ 4 rasgos:"
          f" {crit['D4_mejora']}/6 → {si(crit['D4_cumple'])}.",
          f"- **H1** con {len(ms)} modelos: {tr['H1']['pp']:+.1f} pp [IC {tr['H1']['ic'][0]:+.1f},"
          f" {tr['H1']['ic'][1]:+.1f}], dirección en {tr['H1']['modelos_en_direccion']}/{len(ms)}"
          f" → {si(tr['H1']['ic'][0] > 0)}.", "",
          "## Por rasgo (correlaciones entre modelos)", "",
          "| rasgo | r(aq, FC) | r(aq, Likert) | r(FC, R3aj) | r(Likert, R3aj) | r(anclado, R3aj) | discrimina FC | discrimina R3aj | r(ISS, R3aj) | r(ISS, FC) | r(ISS, Likert) |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for t, f in fila.items():
        L.append(f"| {t} | {_f(f['r_aq_FC'], 2)} | {_f(f['r_aq_R1'], 2)} | {_f(f['r_FC_R3aj'], 2)}"
                 f" | {_f(f['r_R1_R3aj'], 2)} | {_f(f['r_anc_R3aj'], 2)} | {_f(f['discrimina_FC'], 1)}"
                 f" | {_f(disc[t]['R3_ajustada'], 1)} | {_f(f['r_ISS_R3aj'], 2)} | {_f(f['r_ISS_FC'], 2)}"
                 f" | {_f(f['r_ISS_R1'], 2)} |")
    L += ["", "## Perfiles por modelo", "",
          "| modelo | ISS | " + " | ".join(f"{t} Likert / FC / R3aj" for t in RASGOS) + " |",
          "|---|---|" + "---|" * len(RASGOS)]
    for m in ms:
        L.append(f"| {m} | {_f(iss.get(_id(m)), 1)} | " + " | ".join(
            f"{v(m, t, 'R1'):.0f} / {fcs[m][t][0]:.0f} / {v(m, t, 'R3_ajustada'):.0f}"
            for t in RASGOS) + " |")
    texto = "\n".join(L) + "\n"
    out = fc.BASE / "DISCRIMINACION.md"
    out.write_text(texto, encoding="utf-8")
    (fc.BASE / "discriminacion.json").write_text(json.dumps(
        {"criterios": crit, "fc": fcs, "anclado": anc}, ensure_ascii=False, indent=2,
        default=float), encoding="utf-8")
    # El informe del P1 también se regenera con los 9 modelos.
    (ap1.DIR / "INFORME.md").write_text(ap1.informe(res, tr), encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
