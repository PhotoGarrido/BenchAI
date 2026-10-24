"""Re-medición de un modelo «no interpretable» con semillas nuevas (PERSONALIDAD.md §45.3).

Repite, con los MISMOS ids, prompts, nombres, temperatura y max_tokens que la
batería de alta (alta_personalidad.py, que reutiliza los plan() de
experimento_personalidad_v3.py y experimento_personalidad_hn_finos.py), los
instrumentos que alimentan los índices de validez de §41.2:

  tramo 1  «deseabilidad»  juicio AB y BA de las 349 situaciones del cuadro
                           (229 del v3 en O, C, E y A; 48 de I1-H; 72 de I1-N)
  tramo 2  «rep0»          conducta (R3 del v3 y binario de I1) réplica 0, AB y BA
  tramo 3  «rep1»          ídem, réplica 1

Solo cambia la semilla: sha256(f"{prefijo}|{id}") en vez de la del ejecutor,
y cada registro lleva `semilla_prefijo`. Se escribe en una raíz aparte
(resultados/remedicion/<etiqueta>/, con la misma estructura de carpetas), así
que NO entra en el cuadro ni en ningún análisis: lo lee validez_personalidad
con `base=`. Los tramos se lanzan en orden y comparten el control de gasto en
el propio proceso (alta_personalidad.Vigilante): lo que no cabe en el tope
queda pendiente y se reanuda con el mismo comando.

Uso (desde spike/):
  python remedicion_validez.py --modelo deepseek/deepseek-v4-pro-0813 --proyectar
  python remedicion_validez.py --modelo deepseek/deepseek-v4-pro-0813 --tope 0.80 --hilos 8
  python remedicion_validez.py --modelo deepseek/deepseek-v4-pro-0813 --informe
"""

import argparse
import hashlib
import json
import sys

import numpy as np

import alta_personalidad as ap_
import parsers
import validez_personalidad as vp

RES = ap_.RES
PREFIJO = "R2310"   # semillas nuevas, fijadas en §45.3 antes de medir
TRAMOS = ("deseabilidad", "rep0", "rep1")


def raiz_de(modelo, etiqueta="2026-10-23"):
    return RES / "remedicion" / f"{modelo.replace('/', '_')}@{etiqueta}"


def es_deseab(t):
    return t.get("destino") == "cal" or t.get("formato") == "DS"


def tramo_de(t):
    if es_deseab(t):
        return "deseabilidad"
    return f"rep{t['rep']}"


def plan(modelo, raiz, prefijo=PREFIJO):
    """{tramo: {fase: [tareas]}} pendientes en `raiz`, con semillas nuevas."""
    p = ap_.plan(modelo, None, leer=(raiz,))
    out = {tr: {f: [] for f in ap_.FASES} for tr in TRAMOS}
    for fase, ts in p.items():
        for t in ts:
            t = dict(t, semilla_prefijo=prefijo,
                     seed=int(hashlib.sha256(f"{prefijo}|{t['id']}".encode()).hexdigest()[:8], 16))
            out[tramo_de(t)][fase].append(t)
    return out


def proyectar(modelo, raiz):
    p = plan(modelo, raiz)
    c, fuente, tok = ap_.coste_llamada(modelo, RES)
    n = {tr: sum(len(x) for x in d.values()) for tr, d in p.items()}
    return {"llamadas": n, "total": sum(n.values()), "coste_llamada": c, "fuente": fuente, "tokens": tok,
            "coste": {tr: (c or 0) * k for tr, k in n.items()},
            "coste_margen": {tr: (c or 0) * k * ap_.MARGEN for tr, k in n.items()}, "plan": p}


# ── Análisis (criterios de §45.3) ───────────────────────────────────────────
def _juicios(ds):
    j = {}
    for item, orden, estado, alto in ds:
        if estado == parsers.OK and alto is not None:
            j.setdefault(item, {})[orden] = bool(alto)
    return j


def wilson(k, n, z=1.96):
    if not n:
        return None, None
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return float(c - h), float(c + h)


def informe(modelo, raiz):
    m = modelo.replace("/", "_")
    nuevo = vp.evaluar(m, base=raiz)
    viejo = vp.evaluar(m)
    el_n, ds_n = vp.respuestas(m, base=raiz)
    el_v, ds_v = vp.respuestas(m)
    jn, jv = _juicios(ds_n), _juicios(ds_v)
    pn = {i: d["AB"] == d["BA"] for i, d in jn.items() if "AB" in d and "BA" in d}
    pv = {i: d["AB"] == d["BA"] for i, d in jv.items() if "AB" in d and "BA" in d}
    # V4 conjunto (las dos pasadas, cada par AB/BA cuenta una vez)
    k = sum(pn.values()) + sum(pv.values())
    n = len(pn) + len(pv)
    v4_conj = k / n if n else None
    # V1 conjunto: todas las elecciones de las dos pasadas
    val_c, det_c = vp.indices(el_v + el_n, [])
    comunes = sorted(set(pn) & set(pv))
    inc_v = [i for i in comunes if not pv[i]]
    coh_v = [i for i in comunes if pv[i]]
    p_inc_si = float(np.mean([not pn[i] for i in inc_v])) if inc_v else None
    p_inc_no = float(np.mean([not pn[i] for i in coh_v])) if coh_v else None
    # Posición en los pares incoherentes: alto_deseable en AB ⇔ eligió «A»; en BA ⇔
    # eligió «B». Un par incoherente es, por tanto, la misma letra en los dos órdenes.
    def por_posicion(j):
        pos = {"A en los dos órdenes": 0, "B en los dos órdenes": 0}
        for d in j.values():
            if "AB" in d and "BA" in d and d["AB"] != d["BA"]:
                pos["A en los dos órdenes" if d["AB"] else "B en los dos órdenes"] += 1
        return pos
    # Retest entre pasadas: e por situación (media de órdenes y réplicas)
    def e_por_sit(el):
        d = {}
        for item, _o, _r, _v, estado, alto in el:
            if estado == parsers.OK:
                d.setdefault(item, []).append(float(alto))
        return {i: np.mean(x) for i, x in d.items()}
    en, ev = e_por_sit(el_n), e_por_sit(el_v)
    ci = sorted(set(en) & set(ev))
    r_pasadas = float(np.corrcoef([en[i] for i in ci], [ev[i] for i in ci])[0, 1]) if len(ci) > 2 else None
    v4n = nuevo["valores"]["V4_coherencia"]
    lo, hi = wilson(sum(pn.values()), len(pn))
    niv_conj = {"V1_delta": vp._nivel("V1_delta", val_c["V1_delta"]),
                "V1_frac_A": vp._nivel("V1_frac_A", val_c["V1_frac_A"]),
                "V4_coherencia": vp._nivel("V4_coherencia", v4_conj)}
    completo_minimo = len(pn) >= .95 * 349 and nuevo["detalle"]["n_elecciones"] >= .95 * 2 * 349
    # Sin el tramo 3 no hay retest dentro de la pasada nueva: V3 no se juzga en ella
    # (§45.3); el r entre pasadas es informativo.
    con_v3 = nuevo["detalle"]["n_situaciones_retest"] > 2
    nuevo_ok = all(n != "no interpretable" for k, n in nuevo["niveles"].items() if con_v3 or k != "V3_retest")
    conj_ok = all(x != "no interpretable" for x in niv_conj.values())
    if not completo_minimo:
        veredicto = "sin datos suficientes (faltan los tramos 1 y 2)"
    elif nuevo["niveles"]["V4_coherencia"] == "no interpretable" or \
            nuevo["niveles"]["V1_delta"] == "no interpretable" or nuevo["niveles"]["V1_frac_A"] == "no interpretable":
        veredicto = "rasgo estable: vuelve a salir no interpretable; sigue fuera de la norma"
    elif nuevo_ok and conj_ok:
        veredicto = "ruido de aquella pasada: vuelve a ser interpretable"
    else:
        veredicto = "no concluyente: la pasada nueva pasa, pero las dos juntas no; sigue fuera de la norma"
    return {"modelo": modelo, "raiz": str(raiz.relative_to(RES.parent)), "prefijo_semilla": PREFIJO,
            "pasada_original": viejo, "pasada_nueva": nuevo,
            "V4_nueva_wilson95": [lo, hi], "V4_conjunta": v4_conj, "V1_conjunto": val_c,
            "V1_conjunto_detalle": det_c, "niveles_conjuntos": niv_conj,
            "pares_deseabilidad": {"nueva": len(pn), "original": len(pv), "comunes": len(comunes)},
            "persistencia_incoherencia": {"P(incoherente nueva | incoherente original)": p_inc_si,
                                          "P(incoherente nueva | coherente original)": p_inc_no,
                                          "n_incoherentes_original": len(inc_v)},
            "incoherentes_por_posicion": {"nueva": por_posicion(jn), "original": por_posicion(jv)},
            "r_e_entre_pasadas": r_pasadas, "n_situaciones_r": len(ci),
            "completo_minimo": completo_minimo, "tramo3_retest": con_v3, "veredicto": veredicto,
            "V4_nueva": v4n}


def main(argv=None):
    a = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    a.add_argument("--modelo", required=True)
    a.add_argument("--etiqueta", default="2026-10-23")
    a.add_argument("--tope", type=float)
    a.add_argument("--hilos", type=int, default=1)
    a.add_argument("--proyectar", action="store_true")
    a.add_argument("--informe", action="store_true", help="índices y veredicto de §45.3 (sin llamadas)")
    a.add_argument("--tramos", default=",".join(TRAMOS))
    args = a.parse_args(argv)
    raiz = raiz_de(args.modelo, args.etiqueta)
    if args.informe:
        x = informe(args.modelo, raiz)
        raiz.mkdir(parents=True, exist_ok=True)
        sal = raiz / "informe_remedicion.json"
        sal.write_text(json.dumps(x, ensure_ascii=False, indent=1, default=float) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in x.items() if k not in ("pasada_original", "pasada_nueva")},
                         ensure_ascii=False, indent=1, default=float))
        for cual in ("pasada_original", "pasada_nueva"):
            print(cual, x[cual]["nivel"], {k: round(v, 3) if v is not None else None
                                           for k, v in x[cual]["valores"].items()},
                  "Δ con signo", round(x[cual]["detalle"]["delta_con_signo"] or 0, 3),
                  "A", round(x[cual]["detalle"]["frac_A"] or 0, 3))
        return 0
    x = proyectar(args.modelo, raiz)
    print(f"[remedición {args.modelo}] {x['fuente']} · {x['coste_llamada']:.6f} $/llamada · "
          + " · ".join(f"{tr} {x['llamadas'][tr]} ({x['coste'][tr]:.3f} $; {x['coste_margen'][tr]:.3f} con margen)"
                       for tr in TRAMOS) + f" · total {x['total']}", flush=True)
    if args.proyectar or x["total"] == 0:
        return 0
    if ap_.es_de_pago(args.modelo) and args.tope is None:
        raise SystemExit("de pago: hace falta --tope")
    vig = ap_.Vigilante(args.tope, args.hilos, x["coste_llamada"])
    args_manif = {"modelo": args.modelo, "forma": "remedicion", "tope": args.tope, "hilos": args.hilos,
                  "seco": False, "prefijo_semilla": PREFIJO,
                  "origen": "remedicion_validez.py (PERSONALIDAD.md §45.3)"}
    bloq = 0
    for tr in args.tramos.split(","):
        res = ap_.ejecutar(args.modelo, x["plan"][tr], raiz, vig, args.hilos, False, dict(args_manif, tramo=tr))
        b = sum(bb for _, bb in res.values())
        bloq += b
        print(f"[remedición {args.modelo}] tramo {tr}: " + " · ".join(f"{f} {h}" for f, (h, _) in res.items())
              + (f" · {b} sin lanzar" if b else "") + f" · gasto estimado {vig.gasto:.4f} $", flush=True)
    return 3 if bloq else 0


if __name__ == "__main__":
    sys.exit(main())
