"""Banco v3.1 de Extraversión y Neuroticismo: criterios K1-K8 (PERSONALIDAD.md §24).

Compara las candidatas P4 seleccionadas con las situaciones v3 del mismo
rasgo en los MISMOS 6 modelos de NaN (línea base). Aplica el filtro de ítem
fijado en §24 para proponer el banco v3.1 de E y N y estima el coste de
pasárselo a los 7 modelos externos del v3 con los tokens que registraron.

Uso: python analizar_v31_en.py → resultados/personalidad_fc/V31_EN.md y v31_en.json
"""

import json
import pathlib
from collections import defaultdict
from itertools import combinations

import numpy as np

import analizar_personalidad_p1 as ap1
import coste_run
from analizar_personalidad import cargar
from diagnosticar_en_v3 import icc_ck, item_resto

AQUI = pathlib.Path(__file__).parent
SALIDA = AQUI / "resultados" / "personalidad_fc"
SEL_V3 = AQUI / "personalidad_v3_seleccion.json"
SEL_P4 = AQUI / "personalidad_v31_en_seleccion.json"
NAN6 = ("gemma4", "qwen3.6", "qwen3.8-flash", "glm5.3-flash", "mimo-v2.6-flash",
        "deepseek-v4-flash@2026-10-17")
EXTERNOS = ("anthropic/claude-haiku-5.5", "anthropic/claude-opus-5.5#low",
            "google/gemini-3.7-flash", "google/gemini-4-argon", "openai/gpt-5.6-luna",
            "openai/gpt-6.1-sol#low", "deepseek/deepseek-v4-pro-0813")
#: Gasto real de la pasada v3 de los 7 externos según OpenRouter (§23).
GASTO_V3_REAL = 5.0
RASGOS = ("O", "C", "E", "A", "N", "H")
CUOTA = {"debil": 8, "reescritura": 4}
DEBILES = {("E", "asertividad"), ("E", "busqueda_de_emociones"), ("N", "ansiedad"),
           ("N", "hostilidad"), ("N", "depresion"), ("N", "autoconciencia"),
           ("N", "vulnerabilidad")}
FACETAS = {"E": ("cordialidad", "gregarismo", "asertividad", "actividad",
                 "busqueda_de_emociones", "emociones_positivas"),
           "N": ("ansiedad", "hostilidad", "depresion", "autoconciencia", "impulsividad",
                 "vulnerabilidad")}
B, SEMILLA = 2000, 20261020


def cargar_celdas(ids):
    datos = cargar(ap1.DIR)
    elec, elec_rep, inval = {}, {}, {}
    for m in NAN6:
        acc, rep = defaultdict(list), defaultdict(lambda: defaultdict(list))
        n = malas = 0
        for r in datos.get(m, []):
            if r["brazo"] != "sit_propia" or r["item"] not in ids:
                continue
            if r.get("version_bateria") == "v3.1":
                n += 1
            if r["estado"] != "OK":
                malas += r.get("version_bateria") == "v3.1"
                continue
            x = 1.0 if r["elige_alto"] else 0.0
            acc[r["item"]].append(x)
            rep[r.get("rep", 0)][r["item"]].append(x)
        elec[m], elec_rep[m] = acc, rep
        inval[m] = malas / n if n else None
    jui = {}
    for m in NAN6:
        f = ap1.CAL / m / "registros.jsonl"
        ultimo = {}
        for linea in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(linea)
            if r["item"] in ids:
                ultimo[r["id"]] = r
        acc = defaultdict(list)
        for r in ultimo.values():
            if r["estado"] == "OK":
                acc[r["item"]].append(1.0 if r["alto_deseable"] else 0.0)
        jui[m] = acc
    return elec, elec_rep, jui, inval


def _corr(x, y):
    return float(np.corrcoef(x, y)[0, 1]) if np.std(x) and np.std(y) else np.nan


def coste_externos(n_situaciones):
    """Coste estimado de deseabilidad (2) + R3 (4) por situación en los 7 externos,
    con los tokens medios por llamada que registró cada uno en la pasada v3."""
    filas, conocido, desconocidos = [], 0.0, []
    for m in EXTERNOS:
        e = m.replace("/", "_")
        n = tin = tout = 0
        for base in (ap1.DIR, ap1.CAL):
            for f in (base / e).glob("intento_v3_*/solicitudes.jsonl"):
                for linea in f.open(encoding="utf-8"):
                    t = json.loads(linea).get("tokens") or {}
                    n += 1
                    tin += t.get("prompt") or 0
                    tout += t.get("completion") or 0
        pin, pout = coste_run.precio(m)
        c_v3 = None if pin is None else (tin * pin + tout * pout) / 1e6
        if c_v3 is None:
            desconocidos.append(m)
        else:
            conocido += c_v3
        filas.append(dict(modelo=m, n_v3=n, tok_in=tin, tok_out=tout, coste_v3=c_v3))
    # Los que no tienen tarifa fijada en coste_run se reparten lo que falta
    # hasta el gasto real del v3, en proporción a sus tokens.
    resto = max(0.0, GASTO_V3_REAL - conocido)
    tok_desc = sum(f["tok_in"] + f["tok_out"] for f in filas if f["modelo"] in desconocidos)
    for f in filas:
        if f["coste_v3"] is None:
            f["coste_v3"] = resto * (f["tok_in"] + f["tok_out"]) / tok_desc if tok_desc else 0
            f["inferido"] = True
        llamadas = 6 * n_situaciones
        f["llamadas_v31"] = llamadas
        f["coste_v31"] = f["coste_v3"] * llamadas / f["n_v3"] if f["n_v3"] else None
    return filas


def main():
    rng = np.random.default_rng(SEMILLA)
    v3 = json.loads(SEL_V3.read_text(encoding="utf-8"))
    p4 = json.loads(SEL_P4.read_text(encoding="utf-8"))
    info = {s["id"]: s for s in v3 + p4}
    elec, elec_rep, jui, inval = cargar_celdas(set(info))
    comunes = [i for i in info if all(i in elec[m] and i in jui[m] for m in NAN6)]
    grupo = {}   # (rasgo, "p4"|"v3") -> ids
    for i in comunes:
        grupo.setdefault((info[i]["rasgo"], "p4" if info[i]["origen"] == "P4" else "v3"),
                         []).append(i)
    mat = lambda ids, f: np.array([[f(m, i) for i in ids] for m in NAN6])  # noqa: E731
    Pf = lambda m, i: float(np.mean(elec[m][i]))  # noqa: E731
    Df = lambda m, i: float(np.mean(jui[m][i]))  # noqa: E731
    Af = lambda m, i: Pf(m, i) - Df(m, i)  # noqa: E731
    res = {"modelos": NAN6, "n": {f"{k[0]}/{k[1]}": len(v) for k, v in grupo.items()}}
    L = ["# Banco v3.1 · Extraversión y Neuroticismo (§24)", "",
         f"Generado por `analizar_v31_en.py`. 6 modelos de NaN: {', '.join(NAN6)}."
         " **P4** = candidatas nuevas seleccionadas; **base** = situaciones v3 del mismo rasgo"
         " en los mismos 6 modelos.", ""]

    # K1
    sel_fac = defaultdict(list)
    for s in p4:
        sel_fac[(s["rasgo"], s["faceta"])].append(s["p_alto_deseable_nan6"])
    k1 = {}
    for t, facs in FACETAS.items():
        for f in facs:
            v = sel_fac.get((t, f), [])
            cuota = CUOTA["debil" if (t, f) in DEBILES else "reescritura"]
            k1[f"{t}/{f}"] = dict(n=len(v), cuota=cuota,
                                  deseab=float(np.mean(v)) if v else None,
                                  ok=bool(v) and len(v) >= cuota and bool(.40 <= np.mean(v) <= .60))
    res["K1"] = {"facetas": k1, "cumple": all(x["ok"] for x in k1.values())}
    L += ["## K1 · cobertura y equilibrio", "", "| faceta | seleccionadas/cuota | deseab. media | ok |",
          "|---|---|---|---|"]
    for f, x in k1.items():
        dm = "—" if x["deseab"] is None else f"{100 * x['deseab']:.0f} %"
        L.append(f"| {f} | {x['n']}/{x['cuota']} | {dm} | {'✔' if x['ok'] else '✘'} |")
    L += ["", f"**K1 {'CUMPLE' if res['K1']['cumple'] else 'NO cumple'}**", ""]

    def bloque(valor, nombre):
        """K2-K5 y K7 con la puntuación `valor` (ajustada, §24; o bruta, §28)."""
        Lb = [f"## K2–K5 y K7 por rasgo · puntuación {nombre}", "",
              "| rasgo | grupo | n | % con varianza (K2) | sd modelos [IC] (K3) | r ítem-resto (K4) |"
              " alfa | elige lo deseable (K7) |", "|---|---|---|---|---|---|---|---|"]
        por = {}
        for t in ("E", "N"):
            for g in ("p4", "v3"):
                ids = grupo.get((t, g), [])
                if len(ids) < 3:
                    continue
                A, P, D = mat(ids, valor), mat(ids, Pf), mat(ids, Df)
                c = icc_ck(A)
                boots = []
                for _ in range(B):
                    j = rng.integers(0, len(ids), len(ids))
                    boots.append(50 * np.sqrt(icc_ck(A[:, j])["var_modelo"]))
                ir = item_resto(A)
                claro = D != .5
                por[(t, g)] = dict(n=len(ids), con_var=float(np.mean(P.std(0) >= .10)),
                                   sd=50 * float(np.sqrt(c["var_modelo"])),
                                   sd_ic=(float(np.percentile(boots, 2.5)),
                                          float(np.percentile(boots, 97.5))),
                                   ir=float(np.nanmean(ir)), alfa=c["alfa"],
                                   elige_deseable=float(np.mean((P[claro] - .5) * (D[claro] - .5) > 0)),
                                   ir_items=dict(zip(ids, map(float, ir))),
                                   sd_p=dict(zip(ids, map(float, P.std(0)))))
                x = por[(t, g)]
                Lb.append(f"| {t} | {'P4' if g == 'p4' else 'base'} | {x['n']} | {100 * x['con_var']:.0f} % |"
                          f" {x['sd']:.1f} [{x['sd_ic'][0]:.1f}, {x['sd_ic'][1]:.1f}] | {x['ir']:.2f} |"
                          f" {x['alfa']:.2f} | {100 * x['elige_deseable']:.0f} % |")
        # K5 coherencia a nivel de ítem
        k5 = {}
        for t in ("E", "N"):
            ids = grupo.get((t, "p4"), [])
            if len(ids) < 3:
                continue
            A = mat(ids, valor)
            otros = [i for u in RASGOS if u != t for i in grupo.get((u, "v3"), [])]
            Ao = mat(otros, valor)
            pares = list(combinations(range(len(ids)), 2))
            dentro = [_corr(A[:, a], A[:, b]) for a, b in pares]
            misma = [_corr(A[:, a], A[:, b]) for a, b in pares
                     if info[ids[a]]["faceta"] == info[ids[b]]["faceta"]]
            distinta = [_corr(A[:, a], A[:, b]) for a, b in pares
                        if info[ids[a]]["faceta"] != info[ids[b]]["faceta"]]
            fuera = [_corr(A[:, a], Ao[:, b]) for a in range(len(ids)) for b in range(len(otros))]
            k5[t] = dict(dentro=float(np.nanmean(dentro)), fuera=float(np.nanmean(fuera)),
                         misma_faceta=float(np.nanmean(misma)) if misma else float("nan"),
                         otra_faceta=float(np.nanmean(distinta)))
            k5[t]["cumple"] = bool(k5[t]["dentro"] > k5[t]["fuera"]
                                   and k5[t]["misma_faceta"] >= k5[t]["otra_faceta"])
        veredicto = {}
        for t in ("E", "N"):
            a, b = por.get((t, "p4")), por.get((t, "v3"))
            if not a or not b:
                continue
            umbral = 4.0 if t == "E" else 3.0
            veredicto[t] = dict(
                K2=bool(a["con_var"] >= .75 and a["con_var"] > b["con_var"]),
                K3=bool(a["sd"] >= umbral and a["sd"] > b["sd"]),
                K4=bool(a["ir"] >= .15 and a["ir"] > b["ir"]),
                K5=k5.get(t, {}).get("cumple", False),
                K7=bool(a["elige_deseable"] <= .70))
            veredicto[t]["mejora"] = all(veredicto[t][k] for k in ("K2", "K3", "K4", "K5"))
        Lb += ["", f"## K5 · coherencia a nivel de ítem · puntuación {nombre}"
               " (r media entre situaciones, 6 modelos)", "",
               "| rasgo | P4–P4 mismo rasgo | P4–otros rasgos | misma faceta | otra faceta | cumple |",
               "|---|---|---|---|---|---|"]
        for t, x in k5.items():
            Lb.append(f"| {t} | {x['dentro']:.2f} | {x['fuera']:.2f} | {x['misma_faceta']:.2f} |"
                      f" {x['otra_faceta']:.2f} | {'✔' if x['cumple'] else '✘'} |")
        Lb += ["", f"**Veredicto ({nombre}; mejora = K2 + K3 + K4 + K5)**", "",
               "| rasgo | K2 | K3 | K4 | K5 | K7 | mejora |", "|---|---|---|---|---|---|---|"]
        for t, v in veredicto.items():
            Lb.append(f"| {t} | " + " | ".join('✔' if v[k] else '✘' for k in ("K2", "K3", "K4", "K5", "K7"))
                      + f" | **{'sí' if v['mejora'] else 'no'}** |")
        return por, k5, veredicto, Lb + [""]

    # §24 fija la puntuación ajustada; §28 (decisión de David, 20-10) pasa el
    # cuadro público a conducta comparada (elección bruta = deseabilidad común).
    # Se informan las dos; la ajustada es el criterio fijado, la bruta el complemento.
    por, k5, veredicto, Lb = bloque(Af, "ajustada (criterio fijado en §24)")
    por_b, k5_b, veredicto_b, Lb2 = bloque(Pf, "bruta (conducta comparada, §28)")
    L += Lb + Lb2

    # K6 test-retest (P4)
    x0f, x1f, x0t, x1t = [], [], [], []
    for m in NAN6:
        r0, r1 = elec_rep[m].get(0, {}), elec_rep[m].get(1, {})
        for t in ("E", "N"):
            ids = [i for i in grupo.get((t, "p4"), []) if i in r0 and i in r1]
            if ids:
                x0t.append(np.mean([np.mean(r0[i]) - Df(m, i) for i in ids]))
                x1t.append(np.mean([np.mean(r1[i]) - Df(m, i) for i in ids]))
            for f in FACETAS[t]:
                fi = [i for i in ids if info[i]["faceta"] == f]
                if fi:
                    x0f.append(np.mean([np.mean(r0[i]) - Df(m, i) for i in fi]))
                    x1f.append(np.mean([np.mean(r1[i]) - Df(m, i) for i in fi]))
    k6 = dict(r_facetas=_corr(x0f, x1f), n_facetas=len(x0f), r_rasgo=_corr(x0t, x1t),
              n_rasgo=len(x0t))
    k6["cumple"] = bool(k6["r_facetas"] >= .85 and k6["r_rasgo"] >= .90)
    k8 = dict(invalidas=inval, cumple=all((v or 0) < .05 for v in inval.values()))
    limpio = lambda p: {f"{t}/{g}": {k: v for k, v in x.items()  # noqa: E731
                                      if k not in ("ir_items", "sd_p")} for (t, g), x in p.items()}
    res.update(K2_K7=limpio(por), K5=k5, veredicto=veredicto,
               bruta=dict(K2_K7=limpio(por_b), K5=k5_b, veredicto=veredicto_b),
               K6=k6, K8=k8)
    L += ["", "## K6 · test-retest (P4)", "",
          f"r = {k6['r_facetas']:.3f} sobre {k6['n_facetas']} modelo×faceta y "
          f"{k6['r_rasgo']:.3f} sobre {k6['n_rasgo']} modelo×rasgo → "
          f"**{'CUMPLE' if k6['cumple'] else 'NO cumple'}**", "",
          "## K8 · sin pérdidas (R3 v3.1)", "",
          ", ".join(f"{m} {'—' if v is None else f'{100 * v:.1f} %'}" for m, v in inval.items())
          + f" → **{'CUMPLE' if k8['cumple'] else 'NO cumple'}**", ""]

    # Propuesta v3.1 con el filtro de ítem fijado en §24, con las dos puntuaciones
    diag = json.loads((SALIDA / "diagnostico_en.json").read_text(encoding="utf-8"))["items"]

    def proponer(p, campo):
        out, filas = {}, []
        for t in ("E", "N"):
            a = p.get((t, "p4"))
            for f in FACETAS[t]:
                g1 = sorted((i for i in grupo.get((t, "p4"), []) if info[i]["faceta"] == f
                             and a["sd_p"][i] >= .10 and a["ir_items"][i] >= 0),
                            key=lambda i: -a["ir_items"][i])
                g2 = sorted((i for i, d in diag.items() if d["rasgo"] == t and d["faceta"] == f
                             and d.get(campo) is not None and d[campo] >= .10),
                            key=lambda i: -diag[i][campo])
                elegidas = (g1 + g2)[:10]
                out[f"{t}/{f}"] = dict(nuevas=[i for i in elegidas if i in g1],
                                       v3=[i for i in elegidas if i in g2])
                filas.append((t, f, len(out[f"{t}/{f}"]["nuevas"]), len(out[f"{t}/{f}"]["v3"])))
        return out, filas

    prop_a, filas_a = proponer(por, "r_propio")
    prop_b, filas_b = proponer(por_b, "r_propio_bruta")
    res["propuesta_v31"] = dict(ajustada=prop_a, bruta=prop_b)
    L += ["## Propuesta de banco v3.1 para E y N (filtro de ítem del §24)", "",
          "Hasta 10 por faceta: P4 con sd de la elección ≥ 0,10 y r ítem-resto ≥ 0 (6 de NaN),"
          " y después v3 con r ítem-resto ≥ 0,10 (13 modelos). La columna «bruta» aplica el mismo"
          " filtro con la elección bruta (§28).", "",
          "| rasgo | faceta | P4 (ajustada) | v3 (ajustada) | P4 (bruta) | v3 (bruta) |",
          "|---|---|---|---|---|---|"]
    for (t, f, n1, n2), (_, _, m1, m2) in zip(filas_a, filas_b):
        L.append(f"| {t} | {f} | {n1} | {n2} | {m1} | {m2} |")
    nuevas = sorted({i for p in (prop_a, prop_b) for x in p.values() for i in x["nuevas"]})
    n_nuevas = len(nuevas)
    res["nuevas_a_externos"] = nuevas
    L += ["", f"Situaciones P4 que habría que pasar a los externos (unión de las dos propuestas):"
          f" **{n_nuevas}**.", ""]

    # Coste
    cos = coste_externos(n_nuevas)
    res["coste"] = cos
    L += ["## Coste estimado para los 7 externos (deseabilidad ×2 + R3 ×4 por situación)", "",
          "| modelo | llamadas v3 | tokens medios entrada/salida | coste v3 | llamadas v3.1 | coste v3.1 |",
          "|---|---|---|---|---|---|"]
    for f in cos:
        L.append(f"| {f['modelo']} | {f['n_v3']} | {f['tok_in'] / max(f['n_v3'], 1):.0f}/"
                 f"{f['tok_out'] / max(f['n_v3'], 1):.0f} | {f['coste_v3']:.2f} ${' *' if f.get('inferido') else ''} |"
                 f" {f['llamadas_v31']} | {f['coste_v31']:.2f} $ |")
    total = sum(f["coste_v31"] or 0 for f in cos)
    res["coste_total"] = total
    L += ["", f"**Total ≈ {total:.2f} $** (≈ {1.25 * total:.2f} $ con un 25 % de margen)."
          " \\* tarifa no fijada en `coste_run.py`: se reparte el resto del gasto real del v3"
          f" ({GASTO_V3_REAL} $) en proporción a los tokens."]

    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "V31_EN.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (SALIDA / "v31_en.json").write_text(json.dumps(res, ensure_ascii=False, indent=1,
                                                   default=float), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
