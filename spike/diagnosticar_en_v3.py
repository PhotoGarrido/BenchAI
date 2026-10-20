"""Diagnóstico de Extraversión y Neuroticismo en el banco v3 (PERSONALIDAD.md §24).

Solo lee datos ya medidos: los 13 modelos con el banco v3 completo (mismo
filtro que analizar_v3.py). Ninguna llamada a modelos.

Para cada rasgo separa de dónde sale la (falta de) fiabilidad entre modelos:
  - señal: varianza real entre modelos de la puntuación del rasgo;
  - ruido: interacción modelo × situación + ruido de respuesta (4 elecciones
    por celda) + ruido del ajuste de deseabilidad (d_m(i) sale de solo 2
    juicios);
  - situaciones que funcionan al revés (correlación situación-resto < 0) o
    que cargan más en otro rasgo;
  - deseabilidad (ventana 30-70 %) y techo/suelo de la elección bruta;
  - facetas, contexto (propio/terceros) y origen (P0/P1/P3).

Uso: python diagnosticar_en_v3.py → resultados/personalidad_fc/DIAGNOSTICO_EN.md
     y diagnostico_en.json
"""

import json
import pathlib
from collections import defaultdict

import numpy as np

import analizar_personalidad_p1 as ap1
from analizar_personalidad import cargar

AQUI = pathlib.Path(__file__).parent
SALIDA = AQUI / "resultados" / "personalidad_fc"
SEL = AQUI / "personalidad_v3_seleccion.json"
RASGOS = ("O", "C", "E", "A", "N", "H")
VENTANA = (0.30, 0.70)


def celdas():
    """Por modelo e ítem: elecciones (0/1), juicios de deseabilidad y a(m,i)."""
    sel = json.loads(SEL.read_text(encoding="utf-8"))
    info = {s["id"]: s for s in sel}
    datos = cargar(ap1.DIR)
    # juicios individuales de deseabilidad (no solo la media) para el ruido
    jui = {}
    for d in ap1.CAL.iterdir():
        f = d / "registros.jsonl"
        if not (d.is_dir() and f.exists()):
            continue
        ultimo = {}
        for linea in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(linea)
            ultimo[r["id"]] = r
        acc = defaultdict(list)
        for r in ultimo.values():
            if r["estado"] == "OK":
                acc[r["item"]].append(1.0 if r["alto_deseable"] else 0.0)
        jui[d.name] = acc
    elec = {}
    for m, filas in datos.items():
        if m not in jui:
            continue
        acc = defaultdict(list)
        for r in filas:
            if r["brazo"] == "sit_propia" and r["item"] in info and r["estado"] == "OK":
                acc[r["item"]].append(1.0 if r["elige_alto"] else 0.0)
        elec[m] = acc
    # mismo filtro que analizar_v3: ≥ 95 % de las situaciones con dato
    ms = sorted(m for m in elec
                if sum(s["id"] in elec[m] and s["id"] in jui[m] for s in sel) / len(sel) >= .95)
    comunes = [s["id"] for s in sel if all(s["id"] in elec[m] and s["id"] in jui[m] for m in ms)]
    return sel, info, ms, comunes, elec, jui


def icc_ck(X):
    """Fiabilidad de la media de k ítems con modelos como sujetos (alfa de
    Cronbach = ICC(C,k)) y componentes de varianza. X: modelos × ítems."""
    n, k = X.shape
    gm = X.mean()
    ms_m = k * ((X.mean(1) - gm) ** 2).sum() / (n - 1)
    ms_i = n * ((X.mean(0) - gm) ** 2).sum() / (k - 1)
    res = X - X.mean(1, keepdims=True) - X.mean(0, keepdims=True) + gm
    ms_r = (res ** 2).sum() / ((n - 1) * (k - 1))
    return dict(alfa=float((ms_m - ms_r) / ms_m) if ms_m else None,
                var_modelo=float(max(0.0, (ms_m - ms_r) / k)), var_res=float(ms_r),
                var_item=float(max(0.0, (ms_i - ms_r) / n)))


def item_resto(X):
    """Correlación de cada ítem con la media del resto del rasgo, entre modelos."""
    out = []
    for j in range(X.shape[1]):
        resto = np.delete(X, j, axis=1).mean(1)
        x = X[:, j]
        out.append(float(np.corrcoef(x, resto)[0, 1]) if x.std() and resto.std() else np.nan)
    return np.array(out)


def main():
    sel, info, ms, comunes, elec, jui = celdas()
    n_m = len(ms)
    por_rasgo = {t: [i for i in comunes if info[i]["rasgo"] == t] for t in RASGOS}
    A, P, D, RUIDO_R, RUIDO_D = {}, {}, {}, {}, {}
    for t, ids in por_rasgo.items():
        A[t] = np.array([[np.mean(elec[m][i]) - np.mean(jui[m][i]) for i in ids] for m in ms])
        P[t] = np.array([[np.mean(elec[m][i]) for i in ids] for m in ms])
        D[t] = np.array([[np.mean(jui[m][i]) for i in ids] for m in ms])
        # varianza de error de la media de la celda (insesgada, Bernoulli)
        def ve(v):
            v = np.asarray(v)
            return float(v.var(ddof=1) / len(v)) if len(v) > 1 else 0.0
        RUIDO_R[t] = np.array([[ve(elec[m][i]) for i in ids] for m in ms]).mean()
        RUIDO_D[t] = np.array([[ve(jui[m][i]) for i in ids] for m in ms]).mean()
    total = {t: A[t].mean(1) for t in RASGOS}

    res = {"modelos": ms, "rasgos": {}, "facetas": {}, "items": {}}
    L = ["# Diagnóstico de Extraversión y Neuroticismo · banco v3", "",
         f"Generado por `diagnosticar_en_v3.py` (PERSONALIDAD.md §24). {n_m} modelos con el"
         " banco v3 completo; solo datos ya medidos.", "",
         "## 1. Señal frente a ruido por rasgo", "",
         "Escala del cuadro (50 + 50·a). *sd modelos* = desviación típica real entre modelos"
         " (componente de varianza del modelo). *ruido/ítem* = sd residual por situación"
         " (interacción modelo×situación + ruido de respuesta + ruido del ajuste). *alfa* ="
         " fiabilidad de la media del rasgo entre modelos con todas sus situaciones. *r ítem-resto*"
         " = media de la correlación de cada situación con el resto del rasgo, entre modelos.", "",
         "| rasgo | n | sd modelos | ruido/ítem | de él: respuesta | ajuste deseab. | interacción |"
         " alfa ajustada | alfa bruta | r ítem-resto (ajust.) | % ítems r<0 | % ítems sin varianza bruta |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in RASGOS:
        X = A[t]
        c, cb = icc_ck(X), icc_ck(P[t])
        ir = item_resto(X)
        sin_var = float(np.mean(P[t].std(0) < .10))
        inter = max(0.0, c["var_res"] - RUIDO_R[t] - RUIDO_D[t])
        res["rasgos"][t] = dict(n=X.shape[1], sd_modelos=50 * np.sqrt(c["var_modelo"]),
                                sd_res=50 * np.sqrt(c["var_res"]),
                                sd_ruido_respuesta=50 * np.sqrt(RUIDO_R[t]),
                                sd_ruido_ajuste=50 * np.sqrt(RUIDO_D[t]),
                                sd_interaccion=50 * np.sqrt(inter),
                                alfa=c["alfa"], alfa_bruta=cb["alfa"],
                                r_item_resto=float(np.nanmean(ir)),
                                prop_r_neg=float(np.mean(ir < 0)), prop_sin_var=sin_var,
                                rango_modelos=50 * float(np.ptp(X.mean(1))))
        g = res["rasgos"][t]
        L.append(f"| {t} | {g['n']} | {g['sd_modelos']:.1f} | {g['sd_res']:.1f} |"
                 f" {g['sd_ruido_respuesta']:.1f} | {g['sd_ruido_ajuste']:.1f} |"
                 f" {g['sd_interaccion']:.1f} | {g['alfa']:.2f} | {g['alfa_bruta']:.2f} |"
                 f" {g['r_item_resto']:.2f} | {100 * g['prop_r_neg']:.0f} | {100 * sin_var:.0f} |")

    # Deseabilidad
    L += ["", "## 2. Deseabilidad y techo/suelo", "",
          "*en ventana* = % de situaciones cuya deseabilidad media (13 modelos) cae en 30-70 %."
          " *en ventana por modelo* = media sobre modelos del % de situaciones en ventana según"
          " el juicio de cada uno. *elige lo deseable* = % de elecciones que coinciden con el"
          " polo que el propio modelo juzga deseable (si lo juzga con claridad).", "",
          "| rasgo | deseab. media | en ventana | en ventana por modelo | elige lo deseable |"
          " r ítem-resto en ventana | fuera de ventana |", "|---|---|---|---|---|---|---|"]
    for t in RASGOS:
        dm = D[t].mean(0)
        en_v = (dm >= VENTANA[0]) & (dm <= VENTANA[1])
        por_m = float(np.mean((D[t] >= VENTANA[0]) & (D[t] <= VENTANA[1])))
        claro = D[t] != .5
        coincide = float(np.mean((P[t][claro] - .5) * (D[t][claro] - .5) > 0))
        ir = item_resto(A[t])
        res["rasgos"][t].update(deseab_media=float(dm.mean()), prop_ventana=float(en_v.mean()),
                                prop_ventana_por_modelo=por_m, elige_deseable=coincide,
                                ir_ventana=float(np.nanmean(ir[en_v])) if en_v.any() else None,
                                ir_fuera=float(np.nanmean(ir[~en_v])) if (~en_v).any() else None)
        g = res["rasgos"][t]
        L.append(f"| {t} | {100 * g['deseab_media']:.0f} % | {100 * g['prop_ventana']:.0f} % |"
                 f" {100 * por_m:.0f} % | {100 * coincide:.0f} % |"
                 f" {g['ir_ventana'] if g['ir_ventana'] is None else round(g['ir_ventana'], 2)} |"
                 f" {g['ir_fuera'] if g['ir_fuera'] is None else round(g['ir_fuera'], 2)} |")

    # Facetas de E y N (y referencia del resto)
    L += ["", "## 3. Facetas", "",
          "*r faceta-resto* = correlación entre modelos de la puntuación de la faceta con la del"
          " resto del rasgo (sin la faceta). *alfa* = fiabilidad interna de la faceta entre"
          " modelos. *carga cruzada* = rasgo ajeno con el que más correlaciona la faceta.", "",
          "| rasgo | faceta | n | media | sd modelos | alfa | r ítem-resto | r faceta-resto | carga cruzada |",
          "|---|---|---|---|---|---|---|---|---|"]
    for t in RASGOS:
        ids = por_rasgo[t]
        facs = sorted({info[i]["faceta"] for i in ids})
        ir = item_resto(A[t])
        for f in facs:
            cols = [j for j, i in enumerate(ids) if info[i]["faceta"] == f]
            Xf = A[t][:, cols]
            resto = np.delete(A[t], cols, axis=1).mean(1)
            fs = Xf.mean(1)
            rfr = float(np.corrcoef(fs, resto)[0, 1])
            otros = {u: float(np.corrcoef(fs, total[u])[0, 1]) for u in RASGOS if u != t}
            u_max = max(otros, key=lambda u: abs(otros[u]))
            c = icc_ck(Xf) if len(cols) > 1 else {"alfa": None, "var_modelo": 0}
            res["facetas"][f"{t}/{f}"] = dict(n=len(cols), media=50 + 50 * float(fs.mean()),
                                              sd_modelos=50 * float(np.sqrt(c["var_modelo"])),
                                              alfa=c["alfa"], r_item_resto=float(np.nanmean(ir[cols])),
                                              r_faceta_resto=rfr, cruzada=(u_max, otros[u_max]),
                                              r_otros=otros)
            if t in "EN":
                g = res["facetas"][f"{t}/{f}"]
                alfa = "—" if g["alfa"] is None else f"{g['alfa']:.2f}"
                L.append(f"| {t} | {f} | {len(cols)} | {g['media']:.0f} | {g['sd_modelos']:.1f} |"
                         f" {alfa} |"
                         f" {g['r_item_resto']:.2f} | {rfr:.2f} | {u_max} {otros[u_max]:+.2f} |")

    # Contexto y origen
    L += ["", "## 4. Contexto y origen (r ítem-resto media; n)", "",
          "| rasgo | propio | terceros | P0 | P1 | P3 |", "|---|---|---|---|---|---|"]
    for t in RASGOS:
        ids = por_rasgo[t]
        ir = item_resto(A[t])
        celd = []
        for campo, val in (("contexto", "propio"), ("contexto", "terceros"),
                           ("origen", "P0"), ("origen", "P1"), ("origen", "P3")):
            k = [j for j, i in enumerate(ids) if info[i][campo] == val]
            celd.append(f"{np.nanmean(ir[k]):.2f} ({len(k)})" if k else "—")
        L.append(f"| {t} | " + " | ".join(celd) + " |")

    # Ítems de E y N
    L += ["", "## 5. Situaciones de E y N", "",
          "*r propio* = ítem-resto en su rasgo; *mejor ajeno* = rasgo ajeno con mayor"
          " correlación (total del rasgo). *p alto* = % de elecciones del polo alto (13 modelos);"
          " *sd p* = desviación típica entre modelos de la elección bruta.", "",
          "| id | faceta | ctx | deseab. | p alto | sd p | r propio | mejor ajeno |",
          "|---|---|---|---|---|---|---|---|"]
    for t in "EN":
        ids = por_rasgo[t]
        ir, ir_b = item_resto(A[t]), item_resto(P[t])
        orden = sorted(range(len(ids)), key=lambda j: (info[ids[j]]["faceta"], -np.nan_to_num(ir[j])))
        for j in orden:
            i = ids[j]
            x = A[t][:, j]
            otros = {u: float(np.corrcoef(x, total[u])[0, 1]) if x.std() else np.nan
                     for u in RASGOS if u != t}
            u_max = max(otros, key=lambda u: np.nan_to_num(otros[u]))
            res["items"][i] = dict(rasgo=t, faceta=info[i]["faceta"], contexto=info[i]["contexto"],
                                   origen=info[i]["origen"], deseab=float(D[t][:, j].mean()),
                                   p_alto=float(P[t][:, j].mean()), sd_p=float(P[t][:, j].std()),
                                   r_propio=float(ir[j]), r_propio_bruta=float(ir_b[j]),
                                   mejor_ajeno=(u_max, otros[u_max]))
            g = res["items"][i]
            L.append(f"| {i} | {g['faceta']} | {g['contexto'] or '—'} | {100 * g['deseab']:.0f} |"
                     f" {100 * g['p_alto']:.0f} | {g['sd_p']:.2f} | {g['r_propio']:.2f} |"
                     f" {u_max} {otros[u_max]:+.2f} |")

    # G4 (mitades pares/impares, Spearman-Brown) con la puntuación ajustada del
    # §21 y con la elección bruta del §28 (conducta comparada). Exploratorio.
    L += ["", "## 6. G4 con la elección bruta (§28, exploratorio)", "",
          "| rasgo | ajustada (§21) | bruta (§28) |", "|---|---|---|"]
    res["g4"] = {}
    for t in RASGOS:
        ids = sorted(por_rasgo[t])
        cols = {i: k for k, i in enumerate(por_rasgo[t])}
        sb = []
        for X in (A[t], P[t]):
            h1 = X[:, [cols[i] for i in ids[0::2]]].mean(1)
            h2 = X[:, [cols[i] for i in ids[1::2]]].mean(1)
            r = float(np.corrcoef(h1, h2)[0, 1])
            sb.append(2 * r / (1 + r))
        res["g4"][t] = dict(ajustada=sb[0], bruta=sb[1])
        L.append(f"| {t} | {sb[0]:.2f} | {sb[1]:.2f} |")

    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "DIAGNOSTICO_EN.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (SALIDA / "diagnostico_en.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    print("\n".join(L[:40]))


if __name__ == "__main__":
    main()
