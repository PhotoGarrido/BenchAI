"""Índices de validez por modelo del cuadro de personalidad (PERSONALIDAD.md §41.2).

Umbrales fijados en §41.2 ANTES de calcular. Inspirados en las escalas de
validez de los tests clínicos (VRIN/TRIN, «no sabe / no contesta»). Se
calculan sobre TODAS las respuestas del modelo en los instrumentos del cuadro:
R3 del v3 en las situaciones de O, C, E y A (resultados/personalidad_p1/),
binario de I1-H e I1-N (resultados/personalidad_hn_finos/, BI) y su
deseabilidad (v3: resultados/personalidad_p1_calibracion/; I1: DS). Último
registro por id; un ERROR_TECNICO pendiente no cuenta (fallo técnico, no
conducta).

  V1 posición    Δ = media por situación de e(AB) − e(BA) (en AB, «A» es el
                 polo alto) y fracción de respuestas «A»
  V2 no válidas  fracción de respuestas binarias no válidas
  V3 retest      r de Pearson entre e de la réplica 0 y de la 1 por situación
                 (cada celda promedia los dos órdenes)
  V4 coherencia  fracción de situaciones en que el juicio de deseabilidad
                 coincide en AB y en BA

Niveles: «válido», «aviso» o «no interpretable» por índice; el del modelo es
el peor. Un perfil no interpretable sale de la norma del cuadro (§41.2).

Uso (informativo, desde spike/): python validez_personalidad.py [modelo ...]
"""

import json
import pathlib
import sys
from collections import defaultdict

import numpy as np

import parsers

AQUI = pathlib.Path(__file__).parent
RES = AQUI / "resultados"
DIR_P1 = RES / "personalidad_p1"
DIR_CAL = RES / "personalidad_p1_calibracion"
DIR_HNF = RES / "personalidad_hn_finos"
SEL_V3 = AQUI / "personalidad_v3_seleccion.json"
#: Rasgos que el cuadro toma del banco v3 (H y N salen de I1, §37 y §40)
RASGOS_V3 = ("O", "C", "E", "A")
NIVELES = ("válido", "aviso", "no interpretable")
#: (aviso si pasa de…, no interpretable si pasa de…) — §41.2, fijado antes de calcular
UMBRALES = {
    "V1_delta": (.20, .30),      # |Δ|, mayor es peor
    "V1_frac_A": (.10, .15),     # |fracción de A − 0,5|, mayor es peor
    "V2_no_validas": (.05, .10),  # mayor es peor
    "V3_retest": (.60, .40),     # menor es peor
    "V4_coherencia": (.75, .65),  # menor es peor
}
NOMBRE_INDICE = {"V1_delta": "posición (Δ AB−BA)", "V1_frac_A": "posición (fracción de A)",
                 "V2_no_validas": "no válidas", "V3_retest": "retest",
                 "V4_coherencia": "coherencia de la deseabilidad"}


def _ultimos(f):
    """Último registro por id de un registros.jsonl (las reanudaciones mandan)."""
    if not f.exists():
        return []
    por_id = {}
    for linea in f.read_text(encoding="utf-8").splitlines():
        r = json.loads(linea)
        por_id[r["id"]] = r
    return list(por_id.values())


def items_v3(ruta=SEL_V3, rasgos=RASGOS_V3):
    return {s["id"] for s in json.loads(pathlib.Path(ruta).read_text(encoding="utf-8"))
            if s["rasgo"] in rasgos}


def respuestas(m, v3=None, base=RES):
    """Elecciones y juicios de deseabilidad de un modelo (nombre de carpeta).

    Devuelve (elecciones, deseab): elecciones = [(item, orden, rep, valor,
    estado, elige_alto)] de R3 del v3 (situaciones de `v3`) y del binario de
    I1-H e I1-N; deseab = [(item, orden, estado, alto_deseable)]."""
    v3 = items_v3() if v3 is None else v3
    base = pathlib.Path(base)
    el, ds = [], []
    for r in _ultimos(base / DIR_P1.name / m / "registros.jsonl"):
        if r.get("brazo") == "sit_propia" and r.get("item") in v3:
            el.append((r["item"], r.get("orden"), r.get("rep", 0), r.get("valor"), r["estado"],
                       r.get("elige_alto")))
    for r in _ultimos(base / DIR_CAL.name / m / "registros.jsonl"):
        if str(r.get("id", "")).startswith("deseabilidad|") and r.get("item") in v3:
            ds.append((r["item"], r.get("orden"), r["estado"], r.get("alto_deseable")))
    for r in _ultimos(base / DIR_HNF.name / m / "registros.jsonl"):
        if r.get("instr") != "I1" or r.get("rasgo") not in ("H", "N"):
            continue
        if r.get("formato") == "BI":
            el.append((r["item"], r["orden"], r["rep"], r.get("valor"), r["estado"], r.get("elige_alto")))
        elif r.get("formato") == "DS":
            ds.append((r["item"], r["orden"], r["estado"], r.get("alto_deseable")))
    return el, ds


def _nivel(clave, x):
    if x is None or not np.isfinite(x):
        return "no interpretable"
    aviso, malo = UMBRALES[clave]
    if clave in ("V3_retest", "V4_coherencia"):
        return "válido" if x >= aviso else "aviso" if x >= malo else "no interpretable"
    return "válido" if x <= aviso else "aviso" if x <= malo else "no interpretable"


def indices(el, ds):
    """{índice: valor} y detalles a partir de respuestas()."""
    tec = [x for x in el if x[4] != parsers.ERROR_TECNICO]
    ok = [x for x in tec if x[4] == parsers.OK]
    n_a = sum(x[3] == "A" for x in ok)
    por = defaultdict(lambda: defaultdict(list))   # item → (orden|rep) → [alto]
    for item, orden, rep, _v, _e, alto in ok:
        por[item][("o", orden)].append(float(alto))
        por[item][("r", rep)].append(float(alto))
    deltas = [np.mean(d[("o", "AB")]) - np.mean(d[("o", "BA")]) for d in por.values()
              if d.get(("o", "AB")) and d.get(("o", "BA"))]
    r0, r1 = [], []
    for d in por.values():
        if d.get(("r", 0)) and d.get(("r", 1)):
            r0.append(np.mean(d[("r", 0)]))
            r1.append(np.mean(d[("r", 1)]))
    r0, r1 = np.array(r0), np.array(r1)
    retest = float(np.corrcoef(r0, r1)[0, 1]) if len(r0) > 2 and r0.std() and r1.std() else 0.0
    juicio = defaultdict(dict)
    n_ds_a = n_ds = 0
    for item, orden, estado, alto in ds:
        if estado == parsers.OK and alto is not None:
            juicio[item][orden] = bool(alto)
            n_ds += 1
            # en AB, «A» = polo alto: elegir A ⇔ alto_deseable == (orden == AB)
            n_ds_a += bool(alto) == (orden == "AB")
    pares = [j for j in juicio.values() if "AB" in j and "BA" in j]
    coh = float(np.mean([j["AB"] == j["BA"] for j in pares])) if pares else None
    val = {"V1_delta": float(abs(np.mean(deltas))) if deltas else None,
           "V1_frac_A": abs(n_a / len(ok) - .5) if ok else None,
           "V2_no_validas": (len(tec) - len(ok)) / len(tec) if tec else None,
           "V3_retest": retest if len(r0) > 2 else None,
           "V4_coherencia": coh}
    det = {"delta_con_signo": float(np.mean(deltas)) if deltas else None,
           "frac_A": n_a / len(ok) if ok else None,
           "n_elecciones": len(tec), "n_validas": len(ok), "n_situaciones": len(por),
           "n_situaciones_retest": int(len(r0)), "n_deseabilidad_pares": len(pares),
           "frac_A_deseabilidad": n_ds_a / n_ds if n_ds else None}
    return val, det


def evaluar(m, v3=None, base=RES):
    """Índices, nivel por índice, nivel del modelo y motivo."""
    val, det = indices(*respuestas(m, v3, base))
    niv = {k: _nivel(k, x) for k, x in val.items()}
    peor = max(niv.values(), key=NIVELES.index)
    motivo = "; ".join(f"{NOMBRE_INDICE[k]} {_fmt(k, val[k])} ({n})" for k, n in niv.items() if n == peor) \
        if peor != "válido" else ""
    return {"valores": val, "niveles": niv, "nivel": peor, "interpretable": peor != "no interpretable",
            "motivo": motivo, "detalle": det}


def _fmt(k, x):
    if x is None:
        return "sin dato"
    if k == "V2_no_validas":
        return f"{100 * x:.1f} %".replace(".", ",")
    if k == "V1_frac_A":
        return "|A − 0,5| = " + f"{x:.2f}".replace(".", ",")
    return f"{x:.2f}".replace(".", ",")


def main(argv):
    ms = argv or sorted(d.name for d in DIR_P1.iterdir() if d.is_dir())
    for m in ms:
        e = evaluar(m)
        v = e["valores"]
        print(f"{m:38s} {e['nivel']:17s} Δ={_fmt('V1_delta', v['V1_delta'])} A={_fmt('V1_frac_A', v['V1_frac_A'])}"
              f" inv={_fmt('V2_no_validas', v['V2_no_validas'])} retest={_fmt('V3_retest', v['V3_retest'])}"
              f" coh={_fmt('V4_coherencia', v['V4_coherencia'])} · {e['detalle']['n_elecciones']} elecciones")


if __name__ == "__main__":
    main(sys.argv[1:])
