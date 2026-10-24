"""Forma corta del cuadro público de personalidad (PERSONALIDAD.md §41.1-42).

Criterios fijados en §41.1 ANTES de calcular. Sin llamadas a modelos: solo los
datos de los 13 modelos del cuadro de §40 (sin el filtro de validez de §41.2,
que se aplica después en el cuadro).

Bancos de partida (los del cuadro público): O, C, E y A del v3 (situaciones con
dato en los 13), las 48 de I1-H y la escala de I1-N que elige R1 (19, §40).

Regla para un tamaño k, sobre un conjunto S de modelos (elección bruta e):
  cuotas por faceta: mínimo 2 en cada faceta con ≥ 2 en el banco; el resto,
  proporcional al tamaño de la faceta (mayor resto; empates por nombre), sin
  pasar del tamaño de la faceta; dentro de cada faceta, las de mayor
  correlación ítem-resto en S (con la media de las demás del banco); sin
  varianza = la peor; empates por id; sin invertir.
Criterios (C(13,6) = 1.716 particiones: 6 seleccionan, 7 validan):
  C1 mediana de r(corta, completa) en los 7 ≥ 0,95
  C2 medianas de G4 (a) pares/impares y (b) 200 particiones por faceta ≥ 0,70
  k = el menor que cumple C1 y C2 y a partir del cual se cumplen para todo k mayor
Forma final = la regla con los 13 y ese k; C3 cobertura (ninguna faceta > 50 %;
  con los 13, r ≥ 0,95 y G4 ≥ 0,70) y C4 marcas (cuadro con los seis rasgos en
  forma corta: ¿se conservan robustas las marcas robustas del cuadro completo?).
Informativo (no decide): el menor k que conservaría las marcas perdidas de cada
rasgo y la simulación del alta real (un modelo con forma corta y los demás con
la completa, para cada uno de los 13).

Uso (desde spike/): python analizar_forma_corta.py [--rapido]
  → personalidad_forma_corta.json (forma congelada),
    resultados/personalidad_fc/FORMA_CORTA.md y forma_corta.json
"""

import argparse
import hashlib
import json
import pathlib
from itertools import combinations

import numpy as np

import analizar_h_confirmacion as ahc
import analizar_n_confirmacion as anc
import cuadro_publico_v3 as cp
from analizar_discriminacion import _id
from analizar_personalidad import SEMILLA
from analizar_v3 import RASGOS, SALIDA, cargar_v3, puntuar
from cuadro_personalidad import NOMBRE
from rescate_hn_v3 import N_SEL, g4_ab, item_resto, r4

AQUI = pathlib.Path(__file__).parent
UMBRAL_R = .95
UMBRAL_G4 = .70
MAX_FRAC_FACETA = .50
#: llamadas por situación: 4 elecciones (2 órdenes × 2 réplicas) + 2 de deseabilidad
LLAMADAS_SIT = 6
N_I1N_COMPLETO = 72
ORDEN = ("O", "C", "E", "A", "H", "N")


# ── Bancos ──────────────────────────────────────────────────────────────────
def bancos(rutas=None):
    """Modelos y, por rasgo, situaciones, facetas y matriz X (modelos × situaciones)."""
    rutas = rutas or cp.selecciones_por_defecto()
    v = cargar_v3(rutas, rasgos=cp.RASGOS_V3)
    ms = list(v["ms"])
    e = {m: puntuar(v["elecciones"][m]) for m in ms}
    out = {}
    for t in cp.RASGOS_V3:
        its = list(v["por_rasgo"][t])
        out[t] = {"items": its, "facetas": [v["faceta_de"][i] for i in its]}
    h = ahc.h_para_cuadro(rutas_sel=rutas, ms=ms)
    n = anc.n_para_cuadro(rutas_sel=rutas, ms=ms)
    out["H"] = {"items": list(h["items"]), "facetas": [h["faceta_de"][i] for i in h["items"]]}
    out["N"] = {"items": list(n["items"]), "facetas": [n["faceta_de"][i] for i in n["items"]]}
    eh = {m: puntuar(h["elecciones"][m]) for m in ms}
    en = {m: puntuar(n["elecciones"][m]) for m in ms}
    for t, ee in list(zip(cp.RASGOS_V3, [e] * 4)) + [("H", eh), ("N", en)]:
        out[t]["X"] = np.array([[ee[m][i] for i in out[t]["items"]] for m in ms], float)
    return {"ms": ms, "rasgos": out, "v": v, "h": h, "n": n, "e_n": en, "rutas": rutas}


def sha_banco(b):
    return hashlib.sha256("|".join(b["items"]).encode()).hexdigest()


# ── Regla de selección ──────────────────────────────────────────────────────
def tamanos_faceta(facs):
    nf = {}
    for f in facs:
        nf[f] = nf.get(f, 0) + 1
    return dict(sorted(nf.items()))


def k_minimo(facs):
    return 2 * sum(n >= 2 for n in tamanos_faceta(facs).values())


def cuotas(nf, k):
    """Cuotas por faceta para k (§41.1); None si k no cabe."""
    q = {f: (2 if n >= 2 else 0) for f, n in nf.items()}
    resto = k - sum(q.values())
    if resto < 0 or k > sum(nf.values()):
        return None
    total = sum(nf.values())
    objetivo = {f: resto * n / total for f, n in nf.items()}
    extra = {f: 0 for f in nf}
    for _ in range(resto):
        libres = [f for f in sorted(nf) if q[f] + extra[f] < nf[f]]
        if not libres:
            return None
        f = max(libres, key=lambda f: objetivo[f] - extra[f])  # empates: el primero por nombre
        extra[f] += 1
    return {f: q[f] + extra[f] for f in nf}


def ranking(XS, items, facs):
    """{faceta: [índices de columna ordenados por ítem-resto en S (desc), empates por id]}."""
    ir = item_resto(XS)
    ir = np.where(np.isnan(ir), -np.inf, ir)
    out = {}
    for j in sorted(range(len(items)), key=lambda j: (-ir[j], items[j])):
        out.setdefault(facs[j], []).append(j)
    return out


def elegir(rank, nf, k):
    q = cuotas(nf, k)
    if q is None:
        return None
    return sorted(j for f, n in q.items() for j in rank.get(f, [])[:n])


def _r(a, b):
    return float(np.corrcoef(a, b)[0, 1]) if np.std(a) and np.std(b) else float("nan")


# ── C1-C2: validación cruzada ───────────────────────────────────────────────
def validacion_cruzada(b, rng, ks):
    X, items, facs = b["X"], b["items"], b["facetas"]
    nf = tamanos_faceta(facs)
    n_m = X.shape[0]
    res = {k: {"r": [], "g4a": [], "g4b": []} for k in ks}
    g4_completa = []
    for S in combinations(range(n_m), N_SEL):
        V = [j for j in range(n_m) if j not in S]
        XV = X[V]
        rank = ranking(X[list(S)], items, facs)
        total = XV.mean(1)
        g4_completa.append(g4_ab(XV, list(range(len(items))), facs, rng))
        for k in ks:
            cols = elegir(rank, nf, k)
            res[k]["r"].append(_r(XV[:, cols].mean(1), total))
            a, bb = g4_ab(XV, cols, facs, rng)
            res[k]["g4a"].append(a)
            res[k]["g4b"].append(bb)
    resumen = {}
    for k in ks:
        q = {c: {"mediana": float(np.nanmedian(x)), "p25": float(np.nanpercentile(x, 25)),
                 "p75": float(np.nanpercentile(x, 75))} for c, x in res[k].items()}
        q["pasa"] = (q["r"]["mediana"] >= UMBRAL_R and q["g4a"]["mediana"] >= UMBRAL_G4
                     and q["g4b"]["mediana"] >= UMBRAL_G4)
        resumen[k] = q
    ga = np.array(g4_completa, float)
    return resumen, {"g4a": float(np.nanmedian(ga[:, 0])), "g4b": float(np.nanmedian(ga[:, 1]))}


def k_elegido(resumen):
    """El menor k que pasa y a partir del cual pasan todos los mayores (§41.1)."""
    ks = sorted(resumen)
    for k in ks:
        if all(resumen[x]["pasa"] for x in ks if x >= k):
            return k
    return None


# ── Forma final y C3 ────────────────────────────────────────────────────────
def forma_final(b, k, rng):
    X, items, facs = b["X"], b["items"], b["facetas"]
    nf = tamanos_faceta(facs)
    cols = elegir(ranking(X, items, facs), nf, k)
    its = [items[j] for j in cols]
    por_f = {f: sum(facs[j] == f for j in cols) for f in nf}
    a, bb = g4_ab(X, cols, facs, rng)
    c3 = {"por_faceta": por_f, "faceta_max_frac": max(por_f.values()) / len(cols),
          "facetas_conservadas": all(por_f[f] >= 2 for f, n in nf.items() if n >= 2),
          "r_13": _r(X[:, cols].mean(1), X.mean(1)), "g4a_13": a, "g4b_13": bb}
    c3["pasa"] = (c3["facetas_conservadas"] and c3["faceta_max_frac"] <= MAX_FRAC_FACETA
                  and c3["r_13"] >= UMBRAL_R and a >= UMBRAL_G4 and bb >= UMBRAL_G4)
    return its, c3


# ── C4: marcas ──────────────────────────────────────────────────────────────
def cuadro(B, cortas=None, formas=None):
    """Cuadro de §28 con los 13 (sin filtro de validez). cortas: {rasgo: [situaciones]}
    para TODOS los modelos (C4); formas: {modelo: {rasgo: "corta"}} para la
    simulación del alta (cortas = la forma corta)."""
    ms, h, n = B["ms"], B["h"], B["n"]
    kw = dict(panel=ms, rasgos_v3=cp.RASGOS_V3, n_con_marca=True)
    if formas:
        # R4 solo para quien seleccionó la escala de N (los completos en N)
        r4n = {m: s for m, s in n["r4"].items() if formas.get(m, {}).get("N") != "corta"}
        return cp.calcular(B["rutas"], h=h, n=n, r4_n=r4n, formas=formas, corta=cortas, **kw)
    if not cortas:
        return cp.calcular(B["rutas"], h=h, n=n, r4_n=n["r4"], **kw)
    rng = np.random.default_rng(SEMILLA)
    r4n = {m: r4(B["e_n"], ms, cortas["N"], m, "", rng)["marca"] for m in ms}
    return cp.calcular(B["rutas"], escalas={t: cortas[t] for t in cp.RASGOS_V3},
                       h=dict(h, items=cortas["H"]), n=dict(n, items=cortas["N"]), r4_n=r4n, **kw)


def robustas(r):
    return {k: f["marca"] for k, f in r["filas"].items() if f["nivel"] == "robusta"}


def comparar_marcas(rob_full, r_corta):
    rc = robustas(r_corta)
    perdidas = {k: s for k, s in rob_full.items() if rc.get(k) != s}
    nuevas = {k: s for k, s in rc.items() if k not in rob_full}
    detalle = {}
    for k in perdidas:
        f = r_corta["filas"].get(k)
        detalle[k] = ("sin marca candidata" if not f else
                      f"{f['nivel']} {f['marca']} ({f['motivo']})" if f["marca"] == rob_full[k]
                      else f"signo {f['marca']} ({f['nivel']})")
    return perdidas, nuevas, detalle


# ── Coste ───────────────────────────────────────────────────────────────────
def llamadas(n_sit):
    return {t: LLAMADAS_SIT * n for t, n in n_sit.items()}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--rapido", action="store_true",
                    help="sin la búsqueda informativa del k que conserva las marcas ni la simulación")
    args = ap.parse_args(argv)
    B = bancos()
    ms = B["ms"]
    res = {"modelos": ms, "rasgos": {}}
    cortas = {}
    for t in ORDEN:
        b = B["rasgos"][t]
        rng = np.random.default_rng(SEMILLA)
        k0, n_full = k_minimo(b["facetas"]), len(b["items"])
        ks = list(range(k0, n_full))
        resumen, ref = validacion_cruzada(b, rng, ks)
        k = k_elegido(resumen)
        x = {"n_banco": n_full, "facetas_banco": tamanos_faceta(b["facetas"]), "k_min_posible": k0,
             "k": k, "cv": {str(kk): q for kk, q in resumen.items()}, "g4_completa_cv": ref,
             "sha256_banco": sha_banco(b)}
        if k is not None:
            its, c3 = forma_final(b, k, np.random.default_rng(SEMILLA))
            x.update(items=its, C3=c3)
            cortas[t] = its
        else:
            x.update(items=list(b["items"]), C3=None)
            cortas[t] = list(b["items"])
        res["rasgos"][t] = x
        print(f"{t}: banco {n_full}, k = {k}", flush=True)

    # C4: cuadro completo frente a cuadro con los seis rasgos en forma corta
    r_full = cuadro(B)
    rob = robustas(r_full)
    r_c = cuadro(B, cortas)
    perdidas, nuevas, detalle = comparar_marcas(rob, r_c)
    res["C4"] = {"robustas_completo": {f"{m}|{t}": s for (m, t), s in rob.items()},
                 "perdidas": {f"{m}|{t}": detalle[(m, t)] for (m, t) in perdidas},
                 "nuevas": {f"{m}|{t}": s for (m, t), s in nuevas.items()},
                 "conservadas": len(rob) - len(perdidas), "total": len(rob)}
    print(f"C4: {len(rob) - len(perdidas)}/{len(rob)} robustas conservadas", flush=True)

    # Informativo: menor k que conservaría las marcas perdidas de cada rasgo
    if not args.rapido:
        info = {}
        for t in ORDEN:
            obj = {k: s for k, s in perdidas.items() if k[1] == t}
            if not obj or res["rasgos"][t]["k"] is None:
                continue
            b = B["rasgos"][t]
            hallado = None
            for k in range(res["rasgos"][t]["k"] + 1, len(b["items"])):
                its, _ = forma_final(b, k, np.random.default_rng(SEMILLA))
                rr = robustas(cuadro(B, dict(cortas, **{t: its})))
                if all(rr.get(kk) == s for kk, s in rob.items() if kk[1] == t):
                    hallado = k
                    break
            info[t] = {"marcas": [f"{m}|{t}" for (m, _), _s in obj.items()], "k_que_conserva": hallado}
            print(f"  {t}: k que conserva = {hallado}", flush=True)
        res["k_que_conserva"] = info
        # Simulación del alta real: un modelo con forma corta, los demás con la completa
        sim = {}
        for m in ms:
            rs = cuadro(B, cortas, formas={m: {t: "corta" for t in RASGOS}})
            rm = {t: f["marca"] for (mm, t), f in rs["filas"].items() if mm == m and f["nivel"] == "robusta"}
            rf = {t: s for (mm, t), s in rob.items() if mm == m}
            sim[m] = {"completo": rf, "corto": rm,
                      "conservadas": sum(rm.get(t) == s for t, s in rf.items()),
                      "punt_completo": {t: r_full["punt"][(m, t)][0] for t in RASGOS},
                      "punt_corto": {t: rs["punt"][(m, t)][0] for t in RASGOS},
                      "otros_cambian": sorted(f"{_id(mm)}|{t}" for (mm, t), s in robustas(rs).items()
                                              if mm != m and rob.get((mm, t)) != s)
                      + sorted(f"{_id(mm)}|{t} (perdida)" for (mm, t), s in rob.items()
                               if mm != m and robustas(rs).get((mm, t)) != s)}
            print(f"  simulación {_id(m)}: {sim[m]['conservadas']}/{len(rf)}", flush=True)
        res["simulacion_alta"] = sim

    # Ahorro en llamadas por modelo nuevo
    n_full = {t: len(B["rasgos"][t]["items"]) for t in ORDEN}
    n_full_med = dict(n_full, N=N_I1N_COMPLETO)  # la forma completa mide las 72 de I1-N (§41.1)
    n_corta = {t: len(cortas[t]) for t in ORDEN}
    lf, lc = llamadas(n_full_med), llamadas(n_corta)
    res["llamadas"] = {"completa": lf, "corta": lc, "total_completa": sum(lf.values()),
                       "total_corta": sum(lc.values()),
                       "ahorro": 1 - sum(lc.values()) / sum(lf.values())}
    escribir(res, B)


def escribir(res, B):
    forma = {"criterio": "PERSONALIDAD.md §41.1 (fijado antes de calcular); resultados en §42",
             "generado_por": "spike/analizar_forma_corta.py", "semilla": SEMILLA,
             "modelos": [_id(m) for m in res["modelos"]],
             "rasgos": {t: {"k": x["k"], "items": x["items"], "n_banco": x["n_banco"],
                            "sha256_banco": x["sha256_banco"],
                            "C1_r_mediana": x["cv"][str(x["k"])]["r"]["mediana"] if x["k"] else None,
                            "C2_g4a_mediana": x["cv"][str(x["k"])]["g4a"]["mediana"] if x["k"] else None,
                            "C2_g4b_mediana": x["cv"][str(x["k"])]["g4b"]["mediana"] if x["k"] else None,
                            "C3": x["C3"]}
                        for t, x in res["rasgos"].items()},
             "C4": res["C4"], "llamadas": res["llamadas"]}
    (AQUI / "personalidad_forma_corta.json").write_text(
        json.dumps(forma, ensure_ascii=False, indent=1, default=float) + "\n", encoding="utf-8")
    (SALIDA / "forma_corta.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1, default=float) + "\n", encoding="utf-8")
    f2 = lambda x: "—" if x is None or not np.isfinite(x) else f"{x:.2f}".replace(".", ",")  # noqa: E731
    ok = lambda b: "✔" if b else "✘"  # noqa: E731
    L = ["# Forma corta del cuadro público (PERSONALIDAD.md §41.1-42)", "",
         f"Generado por `analizar_forma_corta.py`, semilla {SEMILLA}, sin llamadas a modelos. "
         f"{len(res['modelos'])} modelos; C(13,6) = 1.716 particiones (6 seleccionan, 7 validan).", "",
         "| rasgo | banco | k mín. | k elegido | C1 r (mediana) | C2 G4 (a) | C2 G4 (b) | G4 banco completo (a/b) |"
         " C3 cobertura | C3 r / G4 con los 13 |", "|---|---|---|---|---|---|---|---|---|---|"]
    for t, x in res["rasgos"].items():
        k = x["k"]
        cv = x["cv"].get(str(k), {}) if k else {}
        c3 = x["C3"] or {}
        L.append(f"| {NOMBRE[t]} | {x['n_banco']} | {x['k_min_posible']} | **{k or '—'}** |"
                 f" {f2(cv.get('r', {}).get('mediana'))} | {f2(cv.get('g4a', {}).get('mediana'))} |"
                 f" {f2(cv.get('g4b', {}).get('mediana'))} | {f2(x['g4_completa_cv']['g4a'])} /"
                 f" {f2(x['g4_completa_cv']['g4b'])} |"
                 f" {', '.join(f'{f[:6]} {n}' for f, n in c3.get('por_faceta', {}).items())}"
                 f" (máx {100 * c3.get('faceta_max_frac', 0):.0f} %) {ok(c3.get('pasa'))} |"
                 f" {f2(c3.get('r_13'))} / {f2(c3.get('g4a_13'))} · {f2(c3.get('g4b_13'))} |")
    L += ["", "## Curva por k (medianas sobre las particiones)", ""]
    for t, x in res["rasgos"].items():
        L.append(f"- **{NOMBRE[t]}**: " + " · ".join(
            f"{kk}: r {f2(q['r']['mediana'])}, G4 {f2(q['g4a']['mediana'])}/{f2(q['g4b']['mediana'])}"
            f"{'' if q['pasa'] else ' ✘'}" for kk, q in x["cv"].items()))
    c4 = res["C4"]
    L += ["", "## C4 · marcas robustas con los seis rasgos en forma corta", "",
          f"Se conservan **{c4['conservadas']} de {c4['total']}** marcas robustas del cuadro completo.", ""]
    if c4["perdidas"]:
        L += ["| modelo | rasgo | en la forma corta |", "|---|---|---|"]
        for k, d in c4["perdidas"].items():
            m, t = k.split("|")
            L.append(f"| {_id(m)} | {t} | {d} |")
    if c4["nuevas"]:
        L += ["", "Robustas nuevas en la forma corta (no estaban en el completo): "
              + ", ".join(f"{_id(k.split('|')[0])} {k.split('|')[1]}{s}" for k, s in c4["nuevas"].items()) + "."]
    if res.get("k_que_conserva"):
        L += ["", "Informativo: menor k que conservaría las marcas perdidas de cada rasgo (otros rasgos en"
              " su mínimo): " + "; ".join(f"{t}: {x['k_que_conserva'] or 'ninguno por debajo del banco completo'}"
                                          for t, x in res["k_que_conserva"].items()) + "."]
    if res.get("simulacion_alta"):
        L += ["", "## Simulación del alta (informativa): un modelo con forma corta, los demás completos", "",
              "| modelo | marcas robustas (completo) | con forma corta | conservadas | otras marcas que cambian |",
              "|---|---|---|---|---|"]
        for m, x in res["simulacion_alta"].items():
            L.append(f"| {_id(m)} | {' '.join(t + s for t, s in x['completo'].items()) or '—'} |"
                     f" {' '.join(t + s for t, s in x['corto'].items()) or '—'} | {x['conservadas']}/{len(x['completo'])}"
                     f" | {', '.join(x['otros_cambian']) or '—'} |")
    ll = res["llamadas"]
    L += ["", "## Llamadas por modelo nuevo", "",
          "| | " + " | ".join(ORDEN) + " | total |", "|---|" + "---|" * (len(ORDEN) + 1),
          "| completa | " + " | ".join(str(ll["completa"][t]) for t in ORDEN) + f" | {ll['total_completa']} |",
          "| corta | " + " | ".join(str(ll["corta"][t]) for t in ORDEN) + f" | {ll['total_corta']} |",
          "", f"Ahorro: **{100 * ll['ahorro']:.0f} %** de las llamadas.", "",
          "## Situaciones de la forma corta", ""]
    for t, x in res["rasgos"].items():
        L.append(f"- **{NOMBRE[t]}** ({len(x['items'])}): {', '.join(x['items'])}")
    (SALIDA / "FORMA_CORTA.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
