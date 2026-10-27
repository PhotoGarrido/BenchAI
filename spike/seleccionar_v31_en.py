"""Selección de las candidatas P4 de Extraversión y Neuroticismo (banco v3.1,
PERSONALIDAD.md §24). Regla fijada antes de medir, la misma del v3 (§21):

Deseabilidad agregada = media de los 6 modelos de NaN (los 5 activos más
deepseek-v4-flash@2026-10-17); solo entran situaciones juzgadas por los 6.
Por faceta, con cuota 8 en las 7 facetas débiles (14 candidatas) y 4 en las
5 de reescritura (8 candidatas):
  1. situaciones en ventana (30-70 % juzga deseable el polo alto), las más
     cercanas al 50 % primero;
  2. pares polo-alto-deseable / polo-bajo-deseable de la MISMA faceta, del más
     cercano a la ventana al más extremo, hasta la cuota.
Solo usa juicios de deseabilidad, nunca conducta. Escribe
personalidad_v31_en_seleccion.json.

Uso: python seleccionar_v31_en.py
"""

import json
import pathlib
from collections import Counter, defaultdict

import numpy as np

import calibrar_deseabilidad as cal

AQUI = pathlib.Path(__file__).parent
NAN6 = ("gemma4", "qwen3.6", "qwen3.8-flash", "glm5.3-flash", "mimo-v2.6-flash",
        "deepseek-v4-flash@2026-10-17")
DEBILES = {("E", "asertividad"), ("E", "busqueda_de_emociones"), ("N", "ansiedad"),
           ("N", "hostilidad"), ("N", "depresion"), ("N", "autoconciencia"),
           ("N", "vulnerabilidad")}
CUOTA_DEBIL, CUOTA_REESCRITURA = 8, 4
VENTANA = (0.30, 0.70)
SALIDA = AQUI / "personalidad_v31_en_seleccion.json"


def deseabilidad_nan6(ids):
    acc = defaultdict(dict)
    for m in NAN6:
        f = cal.SALIDA / m / "registros.jsonl"
        if not f.exists():
            continue
        ultimo = {}
        for linea in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(linea)
            if r["item"] in ids:
                ultimo[r["id"]] = r
        por = defaultdict(list)
        for r in ultimo.values():
            if r["estado"] == "OK":
                por[r["item"]].append(1.0 if r["alto_deseable"] else 0.0)
        for i, v in por.items():
            acc[i][m] = float(np.mean(v))
    return {i: (float(np.mean(list(d.values()))), d) for i, d in acc.items()
            if len(d) == len(NAN6)}


def main():
    banco = {i[0]: i for i in cal.banco() if i[5] == "P4"}
    des = deseabilidad_nan6(set(banco))
    faltan = sorted(set(banco) - set(des))
    por_faceta = defaultdict(list)
    for iid, (_, rasgo, *_r, faceta, _ctx) in banco.items():
        if iid in des:
            por_faceta[(rasgo, faceta)].append(iid)
    sel, informe = [], []
    for clave, ids in sorted(por_faceta.items()):
        cuota = CUOTA_DEBIL if clave in DEBILES else CUOTA_REESCRITURA
        p = {i: des[i][0] for i in ids}
        ventana = sorted((i for i in ids if VENTANA[0] <= p[i] <= VENTANA[1]),
                         key=lambda i: (abs(p[i] - .5), i))[:cuota]
        bajos = sorted((i for i in ids if p[i] < VENTANA[0]), key=lambda i: (-p[i], i))
        altos = sorted((i for i in ids if p[i] > VENTANA[1]), key=lambda i: (p[i], i))
        k = max(0, min(len(bajos), len(altos), (cuota - len(ventana)) // 2))
        elegidas = ventana + bajos[:k] + altos[:k]
        sel += elegidas
        informe.append((*clave, len(ids), len(ventana), k, len(elegidas), cuota,
                        float(np.mean([p[i] for i in elegidas])) if elegidas else None))
    salida = []
    for iid in sel:
        _, rasgo, sit, alto, bajo, origen, faceta, ctx = banco[iid]
        salida.append(dict(id=iid, rasgo=rasgo, faceta=faceta, contexto=ctx, origen=origen,
                           situacion=sit, alto=alto, bajo=bajo,
                           p_alto_deseable_nan6=round(des[iid][0], 3),
                           p_alto_deseable_por_modelo={m: round(v, 3)
                                                       for m, v in des[iid][1].items()}))
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    if faltan:
        print(f"[aviso] {len(faltan)} candidatas sin juicio de los 6 modelos: {faltan[:10]}")
    print(f"{'rasgo':5s} {'faceta':22s} cand  vent pares elegidas/cuota  deseab.media")
    for r, f, n, v, k, e, c, dm in informe:
        print(f"{r:5s} {f:22s} {n:4d} {v:5d} {k:5d} {e:5d}/{c:<5d}"
              f" {'—' if dm is None else f'{100 * dm:.0f} %'}")
    print("total", len(salida), dict(Counter(s["rasgo"] for s in salida)))


if __name__ == "__main__":
    main()
