"""Rescate de H y N con los datos del banco v3 (PERSONALIDAD.md §30-31).

Criterios fijados en §30.2 ANTES de calcular. Solo elección bruta (§28), sin
llamadas a modelos.

Regla de selección (sobre un conjunto S de modelos, solo con sus datos):
  fuera las situaciones con sd de e entre los modelos de S < 0,10; después,
  mientras alguna tenga correlación ítem-resto < 0,20 en S, se quita la peor
  y se recalcula, hasta un mínimo de 12. No se invierte ninguna.
R1 validación cruzada: las C(13,6) = 1.716 particiones; 6 seleccionan, 7
  validan. G4 en los 7 (a) pares/impares de §21 y (b) mediana de 200
  particiones al azar equilibradas por faceta. Pasa si la mediana sobre las
  particiones es ≥ 0,70 en (a) y en (b).
R2 cobertura: escala final = elegidas en ≥ 50 % de las particiones; ≥ 3
  facetas con ≥ 2 situaciones y ninguna faceta con más de la mitad.
R3 marcas: cuadro de §28 con la escala final; cinco comprobaciones de §28.
R4 sin reutilización: la marca se mantiene con la escala elegida sin ese
  modelo (los otros 12).
Se rescata un rasgo si cumple R1 y R2; sus marcas, si además R3 y R4.
O, C, E y A pasan por R1-R2 solo como referencia.

Uso (desde spike/): python rescate_hn_v3.py
  → resultados/personalidad_fc/RESCATE_HN.md y rescate_hn.json
"""

import json
from itertools import combinations

import numpy as np

from analizar_discriminacion import _id
from analizar_personalidad import SEMILLA
from analizar_v3 import RASGOS, SALIDA, _boot, cargar_v3, dif_pareada, puntuar, signo
from cuadro_personalidad import NOMBRE
import cuadro_publico_v3 as cp

SD_MIN = .10
IR_MIN = .20
N_MIN = 12
N_SEL = 6
N_SPLITS = 200
UMBRAL = .70
FREC_FINAL = .50
OBJETIVO = ("H", "N")


def item_resto(X):
    """Correlación de cada columna con la media de las demás (filas = modelos)."""
    k = X.shape[1]
    resto = (X.sum(1, keepdims=True) - X) / (k - 1)
    return _corr_columnas(X, resto)


def _corr_columnas(a, b):
    a = a - a.mean(0)
    b = b - b.mean(0)
    den = np.sqrt((a ** 2).sum(0) * (b ** 2).sum(0))
    with np.errstate(invalid="ignore", divide="ignore"):
        r = (a * b).sum(0) / den
    r[~np.isfinite(r)] = np.nan
    return r


def seleccionar(X):
    """Índices (columnas de X, modelos de S × situaciones) que retiene la regla de §30.2."""
    keep = [j for j in range(X.shape[1]) if X[:, j].std(ddof=1) >= SD_MIN]
    while len(keep) > N_MIN:
        ir = item_resto(X[:, keep])
        ir = np.where(np.isnan(ir), -np.inf, ir)
        k = int(np.argmin(ir))
        if ir[k] >= IR_MIN:
            break
        keep.pop(k)
    return keep


def sb(h1, h2):
    if h1.std() == 0 or h2.std() == 0:
        return np.nan
    r = np.corrcoef(h1, h2)[0, 1]
    return 2 * r / (1 + r) if r > -1 else np.nan


def mascaras(cols, facs, rng, n=N_SPLITS):
    """n particiones al azar de las columnas `cols`, equilibradas por faceta (como §26 P1)."""
    por_f = {}
    for k, c in enumerate(cols):
        por_f.setdefault(facs[c], []).append(k)
    M = np.zeros((n, len(cols)), bool)
    turno = 0
    for f in sorted(por_f):
        idx = np.array(por_f[f])
        k = len(idx) // 2
        if len(idx) % 2:
            k += turno
            turno = 1 - turno
        rangos = np.argsort(np.argsort(rng.random((n, len(idx))), axis=1), axis=1)
        M[:, idx] = rangos < k
    return M


def _sb_columnas(s1, s2):
    """Spearman-Brown columna a columna (modelos en filas)."""
    r = _corr_columnas(s1, s2)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = 2 * r / (1 + r)
    out[~np.isfinite(out) | (r <= -1)] = np.nan
    return out


def g4_ab(XV, cols, facs, rng):
    """(a) pares/impares en el orden de cols, (b) mediana de N_SPLITS particiones al azar."""
    Y = XV[:, cols]
    a = sb(Y[:, 0::2].mean(1), Y[:, 1::2].mean(1))
    M = mascaras(list(range(len(cols))), [facs[c] for c in cols], rng)
    n1 = M.sum(1)
    s1 = (Y @ M.T.astype(float)) / n1
    s2 = (Y @ (~M).T.astype(float)) / (len(cols) - n1)
    vals = _sb_columnas(s1, s2)
    vals = vals[np.isfinite(vals)]
    return float(a), float(np.median(vals)) if len(vals) else np.nan


def r1_r2(X, items, facs, rng):
    n_m = X.shape[0]
    frec = np.zeros(len(items))
    ga, gb, ga0, gb0, n_sel, cob = [], [], [], [], [], []
    todas = list(range(len(items)))
    for S in combinations(range(n_m), N_SEL):
        V = [k for k in range(n_m) if k not in S]
        cols = seleccionar(X[list(S)])
        frec[cols] += 1
        n_sel.append(len(cols))
        a, b = g4_ab(X[V], cols, facs, rng)
        ga.append(a)
        gb.append(b)
        a0, b0 = g4_ab(X[V], todas, facs, rng)
        ga0.append(a0)
        gb0.append(b0)
        cf = {}
        for c in cols:
            cf[facs[c]] = cf.get(facs[c], 0) + 1
        cob.append(sum(x >= 2 for x in cf.values()))
    n_part = len(ga)
    frec /= n_part
    final = [items[j] for j in range(len(items)) if frec[j] >= FREC_FINAL]
    por_f = {}
    for j, i in enumerate(items):
        por_f.setdefault(facs[j], {"n_banco": 0, "n_final": 0})
        por_f[facs[j]]["n_banco"] += 1
        if frec[j] >= FREC_FINAL:
            por_f[facs[j]]["n_final"] += 1
    n_fin = len(final)
    fac_ok = [f for f, x in por_f.items() if x["n_final"] >= 2]
    max_frac = max(x["n_final"] for x in por_f.values()) / n_fin if n_fin else 1.0
    q = lambda x: {"mediana": float(np.nanmedian(x)), "p25": float(np.nanpercentile(x, 25)),  # noqa: E731
                   "p75": float(np.nanpercentile(x, 75)), "frac_ge": float(np.nanmean(np.array(x) >= UMBRAL))}
    r1 = {"n_particiones": n_part, "G4a": q(ga), "G4b": q(gb), "G4a_completa": q(ga0), "G4b_completa": q(gb0),
          "n_items_seleccionados": {"mediana": float(np.median(n_sel)), "min": int(min(n_sel)), "max": int(max(n_sel))},
          "frac_particiones_3_facetas": float(np.mean(np.array(cob) >= 3))}
    r1["pasa"] = r1["G4a"]["mediana"] >= UMBRAL and r1["G4b"]["mediana"] >= UMBRAL
    r2 = {"final": final, "n_final": n_fin, "por_faceta": por_f, "facetas_con_2": sorted(fac_ok),
          "faceta_max_frac": max_frac,
          "sin_situaciones": sorted(f for f, x in por_f.items() if x["n_final"] == 0),
          "con_1": sorted(f for f, x in por_f.items() if x["n_final"] == 1),
          "frecuencia": {items[j]: float(frec[j]) for j in range(len(items))}}
    r2["pasa"] = len(fac_ok) >= 3 and max_frac <= .5
    return r1, r2


def r4(e, ms, items_rasgo, m, s0, rng):
    """¿Se mantiene la marca s0 de m con la escala elegida sin m (los otros 12)?"""
    otros = [o for o in ms if o != m]
    X = np.array([[e[o][i] for i in items_rasgo] for o in otros])
    cols = seleccionar(X)
    its = [items_rasgo[c] for c in cols]
    dp, lo, hi = _boot(dif_pareada(e, m, otros, its), rng)
    return {"n_items": len(its), "dif": dp, "ic": [lo, hi], "marca": signo(lo, hi), "mantiene": signo(lo, hi) == s0}


def calcular(rutas_sel):
    rng = np.random.default_rng(SEMILLA)
    v = cargar_v3(rutas_sel)
    ms, por_rasgo, fd = v["ms"], v["por_rasgo"], v["faceta_de"]
    e = {m: puntuar(v["elecciones"][m]) for m in ms}
    res = {"modelos": ms, "rasgos": {}}
    for t in RASGOS:
        items = por_rasgo[t]
        X = np.array([[e[m][i] for i in items] for m in ms])
        r1, r2 = r1_r2(X, items, [fd[i] for i in items], rng)
        res["rasgos"][t] = {"R1": r1, "R2": r2, "rescate": r1["pasa"] and r2["pasa"]}
    # R3 y R4 para H y N con su escala final (se calculan aunque no se rescaten, como información)
    base = cp.calcular(rutas_sel)
    for t in OBJETIVO:
        esc = {t: res["rasgos"][t]["R2"]["final"]}
        r = cp.calcular(rutas_sel, esc)
        filas = {}
        for (m, u), f in r["filas"].items():
            if u != t:
                continue
            nivel = f["nivel_sin_regla_N"] if t == "N" else f["nivel"]
            x4 = r4(e, ms, por_rasgo[t], m, f["marca"], rng) if nivel == "robusta" else None
            motivo = f["motivo"]
            if t == "N":  # sin la regla «N solo descriptivo», para ver la robustez de la escala
                motivo = (f"falla {' '.join(f['fallos'])}" if f["fallos"] else f"pasa {cp.ETIQUETA}") + (
                    f"; cae sin {', '.join(f['cae_sin_lab'])}" if f["cae_sin_lab"] else "")
            filas[_id(m)] = {"marca": f["marca"], "dif": f["dif"], "ic": f["ic"], "nivel": nivel,
                             "motivo": motivo,
                             "fallos": f["fallos"], "R4": x4,
                             "publicable": nivel == "robusta" and bool(x4 and x4["mantiene"])}
        # Comparación con la escala completa
        comp = {}
        for m in ms:
            fb = base["filas"].get((m, t))
            comp[_id(m)] = {"completa": fb["marca"] if fb else "",
                            "completa_nivel": (fb["nivel_sin_regla_N"] if t == "N" else fb["nivel"]) if fb else None,
                            "punt_completa": base["punt"][(m, t)][0], "punt_escala": r["punt"][(m, t)][0]}
        res["rasgos"][t]["R3"] = {"marcas": filas, "comparacion": comp,
                                  "G4_13_modelos_no_valida": r["validez"]["G4"][t],
                                  "G3_13_modelos_no_valida": r["validez"]["G3"][t]}
        # Las otras marcas del cuadro no deben cambiar de nivel por cambiar la escala de t
        # (cambia BH): se informa de las que cambian.
        cambios = []
        for k, f in r["filas"].items():
            if k[1] == t:
                continue
            fb = base["filas"].get(k)
            if fb is None or fb["nivel"] != f["nivel"]:
                cambios.append(f"{_id(k[0])} {k[1]}{f['marca']}: {fb['nivel'] if fb else '—'} → {f['nivel']}")
        for k, fb in base["filas"].items():
            if k[1] != t and k not in r["filas"]:
                cambios.append(f"{_id(k[0])} {k[1]}{fb['marca']}: {fb['nivel']} → sin marca candidata")
        res["rasgos"][t]["R3"]["cambios_otros_rasgos"] = cambios
    return res, v


def escribir(res, v):
    R = res["rasgos"]
    si = lambda b: "✔" if b else "✘"  # noqa: E731
    L = ["# Rescate de H y N con el banco v3 (PERSONALIDAD.md §30-31)", "",
         f"Generado por `rescate_hn_v3.py`. {len(res['modelos'])} modelos; elección bruta (§28);"
         f" semilla {SEMILLA}; sin llamadas a modelos. Criterios de §30.2.", "",
         "## R1 · validación cruzada entre modelos (6 seleccionan, 7 validan; 1.716 particiones)", "",
         "G4 en los 7 modelos que no seleccionaron: mediana [p25, p75] sobre las particiones. (a) pares/impares"
         " de §21; (b) mediana de 200 particiones al azar por faceta. «completa» = el rasgo entero en los"
         " mismos 7 modelos.", "",
         "| rasgo | n elegidas (mediana, mín–máx) | G4 (a) escala | G4 (b) escala | % part. (b) ≥ 0,70 | G4 (a) completa | G4 (b) completa | R1 |",
         "|---|---|---|---|---|---|---|---|"]
    for t in RASGOS:
        r1 = R[t]["R1"]
        n = r1["n_items_seleccionados"]
        fx = lambda d: f"{d['mediana']:.2f} [{d['p25']:.2f}, {d['p75']:.2f}]"  # noqa: E731
        L.append(f"| {t}{'' if t in OBJETIVO else ' (ref.)'} | {n['mediana']:.0f} ({n['min']}–{n['max']}) |"
                 f" {fx(r1['G4a'])} | {fx(r1['G4b'])} | {100 * r1['G4b']['frac_ge']:.0f} % |"
                 f" {fx(r1['G4a_completa'])} | {fx(r1['G4b_completa'])} | {si(r1['pasa'])} |")
    L += ["", "## R2 · cobertura teórica de la escala final (elegidas en ≥ 50 % de las particiones)", "",
          "| rasgo | n final | situaciones por faceta (final/banco) | facetas con ≥ 2 | faceta mayor | R2 | rescate (R1 y R2) |",
          "|---|---|---|---|---|---|---|"]
    for t in RASGOS:
        r2 = R[t]["R2"]
        pf = ", ".join(f"{f} {x['n_final']}/{x['n_banco']}" for f, x in sorted(r2["por_faceta"].items()))
        L.append(f"| {t}{'' if t in OBJETIVO else ' (ref.)'} | {r2['n_final']} | {pf} | {len(r2['facetas_con_2'])} |"
                 f" {100 * r2['faceta_max_frac']:.0f} % | {si(r2['pasa'])} | **{si(R[t]['rescate'])}** |")
    for t in OBJETIVO:
        r2, r3 = R[t]["R2"], R[t]["R3"]
        L += ["", f"## {NOMBRE[t]}: escala final y marcas (R3, R4)", "",
              f"Escala final ({r2['n_final']}): " + ", ".join(
                  f"{i} ({v['faceta_de'][i]}, {100 * r2['frecuencia'][i]:.0f} %)" for i in r2["final"]) + ".", ""]
        if r2["sin_situaciones"] or r2["con_1"]:
            L.append(f"Facetas sin situaciones: {', '.join(r2['sin_situaciones']) or 'ninguna'}; con una sola:"
                     f" {', '.join(r2['con_1']) or 'ninguna'}.")
            L.append("")
        L += [f"G4 de la escala final con los 13 modelos (NO es validación, §30.2 R4): {r3['G4_13_modelos_no_valida']:.2f};"
              f" G3 dentro/fuera: {r3['G3_13_modelos_no_valida'][0]:+.2f} / {r3['G3_13_modelos_no_valida'][1]:+.2f}.", "",
              "| modelo | marca | dif [IC] | nivel (§28) | por qué | R4: sin el modelo | publicable |", "|---|---|---|---|---|---|---|"]
        for m, f in r3["marcas"].items():
            x4 = f["R4"]
            t4 = (f"{x4['marca'] or '·'} {x4['dif']:+.1f} [{x4['ic'][0]:+.1f}, {x4['ic'][1]:+.1f}], {x4['n_items']} sit."
                  if x4 else "—")
            L.append(f"| {m} | {f['marca']} | {f['dif']:+.1f} [{f['ic'][0]:+.1f}, {f['ic'][1]:+.1f}] | {f['nivel']} |"
                     f" {f['motivo']} | {t4} | {si(f['publicable'])} |")
        L += ["", "| modelo | marca candidata, rasgo completo (nivel) | puntuación completa | puntuación escala |",
              "|---|---|---|---|"]
        for m, c in r3["comparacion"].items():
            L.append(f"| {m} | {c['completa'] or '·'} {('(' + c['completa_nivel'] + ')') if c['completa_nivel'] else ''} |"
                     f" {c['punt_completa']:.0f} | {c['punt_escala']:.0f} |")
        L += ["", f"Cambios de nivel en marcas de otros rasgos al cambiar la escala de {t} (por BH):"
              f" {'; '.join(r3['cambios_otros_rasgos']) or 'ninguno'}."]
    (SALIDA / "RESCATE_HN.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (SALIDA / "rescate_hn.json").write_text(json.dumps(res, ensure_ascii=False, indent=2, default=float),
                                            encoding="utf-8")
    return L


def main():
    rutas = cp.selecciones_por_defecto()
    res, v = calcular(rutas)
    print("\n".join(escribir(res, v)))


if __name__ == "__main__":
    main()
