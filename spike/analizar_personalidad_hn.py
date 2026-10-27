"""Criterios Q1-Q7 de la pasada de formatos H/N en NaN (PERSONALIDAD.md §31.1, §32.4).

Sin llamadas a modelos. Lee resultados/personalidad_hn/<modelo>/registros.jsonl
(los 6 de NaN), construye por formato la matriz modelos × ítems con la
puntuación de §32.2 (1 = polo alto) y la compara con la línea base: las
situaciones v3 del rasgo en los mismos 6 modelos, con la elección bruta (§28).
Además, descriptivos (n = 6) y el coste de pasar cada formato a los 7 externos
con los tokens medidos aquí.

Uso (desde spike/): python analizar_personalidad_hn.py
  → resultados/personalidad_fc/HN_FORMATOS.md y hn_formatos.json
"""

import json
from collections import defaultdict

import numpy as np

import analizar_personalidad_p1 as ap1
import experimento_personalidad_hn as ehn
import manifiesto
import personalidad_hn_items as it
import propuesta_hn_coste as phc
from analizar_personalidad import B, SEMILLA
from analizar_v3 import RASGOS, SALIDA, cargar_v3, puntuar
from diagnosticar_hn_v3 import hoyt, item_resto

MODELOS = ("gemma4", "qwen3.6", "qwen3.8-flash", "glm5.3-flash", "mimo-v2.6-flash",
           "deepseek-v4-flash@2026-10-17")
NO_VALIDAS = ("INVALIDA", "REHUSA", "NIEGA_IDENTIDAD", "FUERA_RANGO", "ERROR_TECNICO")
VENTANA = (0.30, 0.70)
MIN_ESCALA = 12
CRITERIOS = {"Q2": .75, "Q3": 4.0, "Q4": .20, "Q5": .85, "Q6": 3.0, "Q7": .70}
NOMBRE_F = {"HE": "escalera de tentación", "HD": "reparto tipo dictador",
            "HM": "informe con incentivo a mentir", "HO": "sobreafirmación (exploratorio)",
            "NG": "intensidad graduada", "NS": "dos opciones serenas",
            "NC": "crítica o fracaso en dos turnos"}
RASGO_F = {f: ("H" if f[0] == "H" else "N") for f in NOMBRE_F}
#: Llamadas por modelo en los externos si el formato pasa (igual diseño que en NaN,
#: salvo HE con una réplica, como en §31.1; NS solo las seleccionadas).
FACETA_HE = {h[0]: h[1] for h in it.HE}
FACETA_NG = {n[0]: n[1] for n in it.NG}


def cargar():
    regs = {}
    for m in MODELOS:
        f = ehn.SALIDA / m / "registros.jsonl"
        if not f.exists():
            continue
        # Si un id se reintentó tras un ERROR_TECNICO, manda el último registro.
        por_id = {}
        for linea in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(linea)
            por_id[r["id"]] = r
        regs[m] = list(por_id.values())
    return regs


def q1(regs, plan_n):
    out = {}
    for m, rs in regs.items():
        por = defaultdict(int)
        for r in rs:
            if r["estado"] in NO_VALIDAS:
                por[r["formato"]] += 1
        # Lo que no llegó a registrarse también es pérdida
        hechas = defaultdict(int)
        for r in rs:
            hechas[r["formato"]] += 1
        out[m] = {f: (por[f] + plan_n[f] - hechas[f]) / plan_n[f] for f in plan_n}
    return out


def _clave_item(r):
    if r["formato"] == "NC":
        return f"{r['item']}|{r['tipo']}"
    return r["item"]


def celdas(regs, formato, filtro=None, brazo="sit_propia"):
    """{m: {item: [puntos]}} con las respuestas válidas; filtro(r) → bool."""
    out = {}
    for m, rs in regs.items():
        acc = defaultdict(list)
        for r in rs:
            if r["formato"] != formato or r["estado"] != "OK" or r.get("puntos") is None:
                continue
            if formato == "NS" and r.get("brazo") != brazo:
                continue
            if filtro is not None and not filtro(r):
                continue
            acc[_clave_item(r)].append(r["puntos"])
        out[m] = {i: float(np.mean(v)) for i, v in acc.items()}
    return out


def matriz(c, ms, items):
    return np.array([[c[m].get(i, np.nan) for i in items] for m in ms], float)


def _boot_sd(X, rng):
    n = X.shape[1]
    bs = [hoyt(X[:, rng.integers(0, n, n)])[0] for _ in range(B)]
    return float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def estadisticos(X, rng, Xr0=None, Xr1=None):
    sd_items = np.nanstd(X, axis=0, ddof=1)
    sd_m, ruido, alfa = hoyt(X)
    ir = item_resto(X)
    res = {"n_items": int(X.shape[1]), "frac_sd010": float(np.mean(sd_items >= .10)),
           "sd_modelos": sd_m, "sd_ic": _boot_sd(X, rng), "ruido": ruido, "alfa": alfa,
           "item_resto": float(np.nanmean(ir)), "media": float(np.mean(X)),
           "perfil": [50 * float(x) for x in X.mean(1)]}
    if Xr0 is not None:
        a, b = Xr0.ravel(), Xr1.ravel()
        ok = np.isfinite(a) & np.isfinite(b)
        res["retest"] = float(np.corrcoef(a[ok], b[ok])[0, 1]) if ok.sum() > 2 else None
    return res


def linea_base(rng):
    v = cargar_v3()
    e = {m: puntuar(v["elecciones"][m]) for m in MODELOS}
    out = {}
    for t in ("H", "N"):
        X = np.array([[e[m][i] for i in v["por_rasgo"][t]] for m in MODELOS], float)
        out[t] = estadisticos(X, rng)
    # Perfiles v3 por rasgo (elección bruta) y deseabilidad propia de H
    perf = {t: [50 * float(np.mean([e[m][i] for i in v["por_rasgo"][t]])) for m in MODELOS]
            for t in RASGOS}
    des_h = [50 * float(np.mean([v["des"][m][i] for i in v["por_rasgo"]["H"]]))
             for m in MODELOS]
    return out, perf, des_h


def seleccion_ns(regs):
    """Ventana de deseabilidad media de los 6 (§21), con mínimo de 12 (§32.4)."""
    d = defaultdict(list)
    por_m = defaultdict(lambda: defaultdict(list))
    for m, rs in regs.items():
        for r in rs:
            if r["formato"] == "NS" and r.get("brazo") == "deseabilidad" and r["estado"] == "OK":
                d[r["item"]].append(1.0 if r["alto_deseable"] else 0.0)
                por_m[m][r["item"]].append(1.0 if r["alto_deseable"] else 0.0)
    media = {i: float(np.mean(v)) for i, v in d.items()}
    orden = sorted(media, key=lambda i: abs(media[i] - .5))
    sel = [i for i in orden if VENTANA[0] <= media[i] <= VENTANA[1]]
    for i in orden:
        if len(sel) >= MIN_ESCALA:
            break
        if i not in sel:
            sel.append(i)
    des_m = {m: {i: float(np.mean(v)) for i, v in x.items()} for m, x in por_m.items()}
    return sel, media, des_m


def q7(c, des_m, items):
    coinc = []
    for m in c:
        for i in items:
            if i in c[m] and i in des_m.get(m, {}) and des_m[m][i] != .5:
                coinc.append((c[m][i] - .5) * (des_m[m][i] - .5) > 0)
    return float(np.mean(coinc)) if coinc else None, len(coinc)


def posicion(regs):
    """Fracción de «A» por modelo en los formatos A/B (descriptivo)."""
    out = {}
    for m, rs in regs.items():
        out[m] = {}
        for f in ("HE", "NS", "NC"):
            letras = [(r["valor"] if f != "NC" else r["valor"][1]) for r in rs
                      if r["formato"] == f and r["estado"] == "OK"
                      and (f != "NS" or r.get("brazo") == "sit_propia")]
            out[m][f] = float(np.mean([x == "A" for x in letras])) if letras else None
    return out


def escalera(regs):
    """Elección honesta media por nivel (todos los modelos) y por faceta."""
    acc = defaultdict(list)
    for rs in regs.values():
        for r in rs:
            if r["formato"] == "HE" and r["estado"] == "OK":
                acc[(r["faceta"], r["nivel"])].append(r["puntos"])
                acc[("todas", r["nivel"])].append(r["puntos"])
    return {f: [float(np.mean(acc[(f, n)])) if acc[(f, n)] else None for n in range(5)]
            for f in ("todas",) + it.FACETAS_H}


def tokens(regs):
    """Tokens medios por llamada: por formato (esta pasada) y v3 (mismos modelos, NaN)."""
    sha_f = {manifiesto.sha256_texto(t["prompt"]): t["formato"] for t in ehn.plan()}
    acc = defaultdict(lambda: [0, 0, 0])
    for m in regs:
        for f in (ehn.SALIDA / m).glob("intento_*/solicitudes.jsonl"):
            for linea in f.open(encoding="utf-8"):
                s = json.loads(linea)
                tk = s.get("tokens") or {}
                fmt = sha_f.get(manifiesto.sha256_texto(s["messages"][-1]["content"]))
                if fmt is None or tk.get("prompt") is None:
                    continue
                a = acc[fmt]
                a[0] += 1
                a[1] += tk["prompt"]
                a[2] += tk.get("completion") or 0
    v3 = [0, 0, 0]
    for m in regs:
        for base in (ap1.DIR, ap1.CAL):
            for f in (base / m).glob("intento_v3_*/solicitudes.jsonl"):
                for linea in f.open(encoding="utf-8"):
                    tk = json.loads(linea).get("tokens") or {}
                    if tk.get("prompt") is None:
                        continue
                    v3[0] += 1
                    v3[1] += tk["prompt"]
                    v3[2] += tk.get("completion") or 0
    por = {f: {"n": a[0], "in": a[1] / a[0], "out": a[2] / a[0]} for f, a in acc.items() if a[0]}
    base = {"n": v3[0], "in": v3[1] / v3[0], "out": v3[2] / v3[0]} if v3[0] else None
    return por, base


def coste_externos(llamadas, tok, base):
    """{formato: coste total en los 7 externos} para `llamadas` {formato: n por modelo}."""
    cpl = phc.coste_por_llamada()
    out = {}
    for f, n in llamadas.items():
        fi = tok[f]["in"] / base["in"] if base else 1.0
        fo = tok[f]["out"] / base["out"] if base and base["out"] else 1.0
        out[f] = {"factor_in": fi, "factor_out": fo, "llamadas": n,
                  "por_modelo": {m: n * (b["in_medio"] * fi * b["pin"]
                                         + b["out_medio"] * fo * b["pout"]) / 1e6
                                 for m, b in cpl.items()}}
        out[f]["total"] = sum(out[f]["por_modelo"].values())
    return out


def calcular():
    rng = np.random.default_rng(SEMILLA)
    regs = cargar()
    ms = [m for m in MODELOS if m in regs]
    plan_n = defaultdict(int)
    for t in ehn.plan():
        plan_n[t["formato"]] += 1
    base, perf_v3, des_h = linea_base(rng)
    res = {"modelos": ms, "q1": q1(regs, dict(plan_n)), "base": base, "formatos": {}}
    sel_ns, des_media_ns, des_m_ns = seleccion_ns(regs)
    res["ns_seleccion"] = {"items": sel_ns, "deseab_media": des_media_ns}
    items = {"HE": [h[0] for h in it.HE], "HD": [h[0] for h in it.HD],
             "HM": [h[0] for h in it.HM], "HO": [h[0] for h in it.HO if not h[2]],
             "NG": [n[0] for n in it.NG], "NS": sel_ns,
             "NC": [f"{n['id']}|{t}" for n in it.NC for t in ("fundada", "infundada")]}
    extra = {"NS24": [n[0] for n in it.NS]}
    for f, its in list(items.items()) + [("NS24", extra["NS24"])]:
        fb = "NS" if f == "NS24" else f
        c = celdas(regs, fb)
        c0 = celdas(regs, fb, lambda r: r["rep"] == 0)
        c1 = celdas(regs, fb, lambda r: r["rep"] == 1)
        X = matriz(c, ms, its)
        st = estadisticos(X, rng, matriz(c0, ms, its), matriz(c1, ms, its))
        b = base[RASGO_F[fb]]
        st["Q1"] = all(res["q1"][m][fb] < .05 for m in ms)
        st["Q2"] = bool(st["frac_sd010"] >= CRITERIOS["Q2"] and st["frac_sd010"] > b["frac_sd010"])
        st["Q3"] = bool(st["sd_modelos"] >= CRITERIOS["Q3"] and st["sd_modelos"] > b["sd_modelos"])
        st["Q4"] = bool(st["item_resto"] >= CRITERIOS["Q4"])
        st["Q5"] = bool(st["retest"] is not None and st["retest"] >= CRITERIOS["Q5"])
        if fb == "HE":
            st["facetas"] = {}
            for fac in it.FACETAS_H:
                fi = [i for i in its if FACETA_HE[i] == fac]
                Xf = matriz(c, ms, fi)
                st["facetas"][fac] = {"sd_modelos": hoyt(Xf)[0], "sd_ic": _boot_sd(Xf, rng),
                                      "media": float(Xf.mean())}
            st["Q6"] = all(st["facetas"][fac]["sd_modelos"] >= CRITERIOS["Q6"]
                           for fac in ("equidad", "modestia"))
        if fb == "NG":
            st["facetas"] = {fac: {"sd_modelos": hoyt(matriz(c, ms, [i for i in its
                                                                       if FACETA_NG[i] == fac]))[0],
                                   "media": float(matriz(c, ms, [i for i in its
                                                                 if FACETA_NG[i] == fac]).mean())}
                             for fac in it.FACETAS_N}
        if fb == "NS":
            st["elige_deseable"], st["n_q7"] = q7(c, des_m_ns, its)
            st["Q7"] = bool(st["elige_deseable"] is not None
                            and st["elige_deseable"] <= CRITERIOS["Q7"])
        claves = ["Q1", "Q2", "Q3", "Q4", "Q5"] + (["Q6"] if fb == "HE" else []) + (
            ["Q7"] if fb == "NS" else [])
        st["pasa"] = all(st[k] for k in claves)
        st["criterios"] = claves
        # Descriptivos: correlación con la elección v3 de cada rasgo y con la deseabilidad H
        perfil = np.array(st["perfil"])
        st["r_v3"] = {t: float(np.corrcoef(perfil, perf_v3[t])[0, 1]) for t in RASGOS}
        st["r_deseab_H"] = float(np.corrcoef(perfil, des_h)[0, 1])
        res["formatos"][f] = st
    # Componentes de NC y HO (descriptivo)
    nc_mal = defaultdict(list)
    nc_rea = defaultdict(list)
    ho = defaultdict(lambda: {"reales": [], "inexistentes": []})
    hd_dado = defaultdict(list)
    hm_exceso = defaultdict(list)
    for m, rs in regs.items():
        for r in rs:
            if r["estado"] != "OK":
                continue
            if r["formato"] == "NC":
                nc_mal[m].append(r["malestar"])
                nc_rea[m].append(r["elige_reactiva"])
            elif r["formato"] == "HO":
                ho[m]["reales" if r["existe"] else "inexistentes"].append(r["valor"])
            elif r["formato"] == "HD":
                hd_dado[m].append(100 * r["dado"] / r["total"])
            elif r["formato"] == "HM":
                hm_exceso[m].append(r["exceso"])
    res["nc_componentes"] = {m: {"malestar": float(np.mean(nc_mal[m])),
                                 "reactiva": float(np.mean(nc_rea[m]))} for m in ms}
    res["ho_afirmacion"] = {m: {k: float(np.mean(v)) for k, v in ho[m].items()} for m in ms}
    res["hd_pct_dado"] = {m: float(np.mean(hd_dado[m])) for m in ms}
    res["hm_exceso"] = {m: float(np.mean(hm_exceso[m])) for m in ms}
    hs = [f for f in ("HE", "HD", "HM") if res["formatos"][f]["pasa"]] or ["HE", "HD", "HM"]
    media_h = np.mean([res["formatos"][f]["perfil"] for f in hs], axis=0)
    res["ho_r_con_H"] = {"formatos": hs, "r": float(np.corrcoef(res["formatos"]["HO"]["perfil"],
                                                                media_h)[0, 1])}
    # Matriz de correlación entre formatos (perfiles por modelo, n = 6)
    fs = list(items)
    res["corr_formatos"] = {f"{a}|{b}": float(np.corrcoef(res["formatos"][a]["perfil"],
                                                          res["formatos"][b]["perfil"])[0, 1])
                            for k, a in enumerate(fs) for b in fs[k + 1:]}
    res["posicion"] = posicion(regs)
    res["escalera"] = escalera(regs)
    tok, tok_v3 = tokens(regs)
    res["tokens"] = {"formatos": tok, "v3": tok_v3}
    llamadas = {"HE": 16 * 5 * 2, "HD": 8 * 2 * 2, "HM": 8 * 2 * 2, "HO": 36 * 2,
                "NG": 36 * 2, "NS": len(sel_ns) * (2 + 4), "NC": 24 * 2 * 2}
    if tok and tok_v3:
        res["coste"] = coste_externos({f: n for f, n in llamadas.items() if f in tok}, tok, tok_v3)
    return res


def _b(x):
    return "✔" if x else "✘"


def escribir(r):
    ms = r["modelos"]
    L = ["# Pasada de formatos H/N en NaN (PERSONALIDAD.md §31.1, §32)", "",
         "Generado por `analizar_personalidad_hn.py` sin llamadas a modelos. 6 modelos de NaN:"
         f" {', '.join(ms)}. Puntuación 0–1 con 1 = polo alto del rasgo; sd entre modelos en la"
         " escala del cuadro (×50). Línea base: situaciones v3 del rasgo en los mismos 6"
         " modelos, elección bruta.", "",
         "## Q1–Q7 por formato", "",
         "| formato | rasgo | ítems | Q1 pérdidas máx. | Q2 % ítems sd ≥ 0,10 | Q3 sd modelos [IC 95 %]"
         " | Q4 ítem-resto | Q5 retest | Q6/Q7 | alfa | media | pasa |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in ("H", "N"):
        b = r["base"][t]
        L.append(f"| *línea base v3* | {t} | {b['n_items']} | — | {100 * b['frac_sd010']:.0f} % |"
                 f" {b['sd_modelos']:.1f} [{b['sd_ic'][0]:.1f}; {b['sd_ic'][1]:.1f}] |"
                 f" {b['item_resto']:.2f} | — | — | {b['alfa']:.2f} | {b['media']:.2f} | — |")
    for f, s in r["formatos"].items():
        fb = "NS" if f == "NS24" else f
        q1 = max(r["q1"][m][fb] for m in ms)
        extra = "—"
        if "Q6" in s:
            fa = s["facetas"]
            extra = (f"equidad {fa['equidad']['sd_modelos']:.1f} · modestia"
                     f" {fa['modestia']['sd_modelos']:.1f} {_b(s['Q6'])}")
        if "Q7" in s:
            extra = f"elige lo deseable {100 * s['elige_deseable']:.0f} % {_b(s['Q7'])}"
        nombre = f"{f} · {NOMBRE_F[fb]}" + (" (las 24, informativo)" if f == "NS24" else "")
        ret = "—" if s.get("retest") is None else f"{s['retest']:.2f}"
        L.append(f"| {nombre} | {RASGO_F[fb]} | {s['n_items']} | {100 * q1:.1f} % {_b(s['Q1'])} |"
                 f" {100 * s['frac_sd010']:.0f} % {_b(s['Q2'])} |"
                 f" {s['sd_modelos']:.1f} [{s['sd_ic'][0]:.1f}; {s['sd_ic'][1]:.1f}] {_b(s['Q3'])} |"
                 f" {s['item_resto']:.2f} {_b(s['Q4'])} | {ret} {_b(s['Q5'])} | {extra} |"
                 f" {s['alfa']:.2f} | {s['media']:.2f} |"
                 f" {'—' if f == 'NS24' else '**sí**' if s['pasa'] else 'no'} |")
    L += ["", "Pasa a los externos si cumple Q1–Q5, y Q6 (HE) o Q7 (NS) cuando aplica (§31.1).", "",
          "## Perfil por modelo (media del formato ×50)", "",
          "| modelo | " + " | ".join(r["formatos"]) + " |", "|---|" + "---|" * len(r["formatos"])]
    for k, m in enumerate(ms):
        L.append(f"| {m} | " + " | ".join(f"{s['perfil'][k]:.1f}" for s in r["formatos"].values())
                 + " |")
    he = r["formatos"]["HE"]
    L += ["", "## HE por faceta y por nivel", "",
          "| faceta | sd modelos [IC] | elección honesta media | nivel 1 | 2 | 3 | 4 | 5 |",
          "|---|---|---|---|---|---|---|---|"]
    esc = r["escalera"]
    for fac in ("todas",) + it.FACETAS_H:
        fa = he["facetas"].get(fac)
        sd = "—" if fa is None else f"{fa['sd_modelos']:.1f} [{fa['sd_ic'][0]:.1f}; {fa['sd_ic'][1]:.1f}]"
        med = "—" if fa is None else f"{fa['media']:.2f}"
        L.append(f"| {fac} | {sd} | {med} | " + " | ".join(
            "—" if x is None else f"{x:.2f}" for x in esc[fac]) + " |")
    ng = r["formatos"]["NG"]
    L += ["", "## NG por faceta", "", "| faceta | sd modelos | media |", "|---|---|---|"]
    for fac, x in ng["facetas"].items():
        L.append(f"| {fac} | {x['sd_modelos']:.1f} | {x['media']:.2f} |")
    L += ["", "## Componentes y descriptivos por modelo", "",
          "| modelo | HD % dado | HM exceso medio | HO afirmación reales / inexistentes (0–6) |"
          " NC malestar (0–10) | NC elige reactiva | % A en HE | % A en NS | % A en NC |",
          "|---|---|---|---|---|---|---|---|---|"]
    for m in ms:
        ho = r["ho_afirmacion"][m]
        p = r["posicion"][m]
        L.append(f"| {m} | {r['hd_pct_dado'][m]:.0f} | {r['hm_exceso'][m]:+.2f} |"
                 f" {ho['reales']:.2f} / {ho['inexistentes']:.2f} |"
                 f" {r['nc_componentes'][m]['malestar']:.2f} | {100 * r['nc_componentes'][m]['reactiva']:.0f} % |"
                 f" {100 * p['HE']:.0f} % | {100 * p['NS']:.0f} % | {100 * p['NC']:.0f} % |")
    L += ["", f"HO frente a la media de {', '.join(r['ho_r_con_H']['formatos'])}: r ="
          f" {r['ho_r_con_H']['r']:+.2f} (umbral de §32.4: +0,50).", "",
          f"NS: {len(r['ns_seleccion']['items'])} situaciones evaluadas (ventana 30–70 % o las"
          f" {MIN_ESCALA} más cercanas al 50 %): {', '.join(r['ns_seleccion']['items'])}.", "",
          "## Descriptivo (n = 6): correlación del perfil de cada formato con la elección v3 por rasgo"
          " y con la deseabilidad propia de H", "",
          "| formato | " + " | ".join(RASGOS) + " | deseabilidad propia H (v3) |",
          "|---|" + "---|" * (len(RASGOS) + 1)]
    for f, s in r["formatos"].items():
        L.append(f"| {f} | " + " | ".join(f"{s['r_v3'][t]:+.2f}" for t in RASGOS)
                 + f" | {s['r_deseab_H']:+.2f} |")
    L += ["", "Correlación entre formatos (perfiles por modelo, n = 6): "
          + " · ".join(f"{k.replace('|', '–')} {v:+.2f}" for k, v in r["corr_formatos"].items()), ""]
    if r.get("coste"):
        tv = r["tokens"]["v3"]
        L += ["## Coste de pasar cada formato a los 7 externos", "",
              f"Tokens medios por llamada medidos aquí, divididos por los de las llamadas v3 de los"
              f" mismos modelos en NaN ({tv['in']:.0f} de entrada / {tv['out']:.1f} de salida), por la"
              " tarifa y los tokens v3 de cada externo (`propuesta_hn_coste.py`).", "",
              "| formato | llamadas por modelo | factor entrada / salida | coste en los 7 | pasa |",
              "|---|---|---|---|---|"]
        for f, c in r["coste"].items():
            pasa = r["formatos"][f]["pasa"]
            L.append(f"| {f} | {c['llamadas']} | {c['factor_in']:.2f} / {c['factor_out']:.2f} |"
                     f" {c['total']:.3f} $ | {'sí' if pasa else 'no'} |")
        tot = sum(c["total"] for f, c in r["coste"].items() if r["formatos"][f]["pasa"])
        L += ["", f"Formatos que pasan: ≈ {tot:.2f} $ ({phc.MARGEN * tot:.2f} $ con margen del 25 %).",
              ""]
    (SALIDA / "HN_FORMATOS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (SALIDA / "hn_formatos.json").write_text(json.dumps(r, ensure_ascii=False, indent=2),
                                             encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    escribir(calcular())
