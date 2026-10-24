"""Selección del banco v3: 60 situaciones por rasgo equilibradas POR FACETA
(PERSONALIDAD.md §21).

Deseabilidad agregada = media de los 5 modelos de NaN activos (los únicos que
han juzgado todas las candidatas: P0, P1 y P3). Por faceta, con cuota 10 (H: 15):
  1. situaciones en ventana (30-70 % juzga deseable el polo alto), las más
     cercanas al 50 % primero;
  2. pares polo-alto-deseable / polo-bajo-deseable de la MISMA faceta, del más
     cercano a la ventana al más extremo, hasta la cuota.
Escribe personalidad_v3_seleccion.json e informa de la cobertura.

Uso: python seleccionar_v3.py
"""

import json
import pathlib
from collections import defaultdict

import numpy as np

import calibrar_deseabilidad as cal

AQUI = pathlib.Path(__file__).parent
#: Los 5 de NaN activos. deepseek-v4-flash (4.1) se retiró el 17-10-2026: NaN
#: cambió el modelo detrás del endpoint y sus juicios de ese día están en
#: cuarentena, así que no ha juzgado las candidatas P3 (desviación de §21,
#: documentada en §22, decidida sin ver datos de conducta).
NAN = ("gemma4", "qwen3.6", "qwen3.8-flash", "glm5.3-flash", "mimo-v2.6-flash")
CUOTA = {"H": 15}
VENTANA = (0.30, 0.70)


def deseabilidad_nan():
    acc = defaultdict(lambda: defaultdict(list))
    for m in NAN:
        f = cal.SALIDA / m / "registros.jsonl"
        ultimo = {}
        for linea in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(linea)
            ultimo[r["id"]] = r
        for r in ultimo.values():
            if r["estado"] == "OK":
                acc[r["item"]][m].append(1.0 if r["alto_deseable"] else 0.0)
    # solo situaciones juzgadas por los 6
    return {i: float(np.mean([np.mean(v) for v in d.values()]))
            for i, d in acc.items() if len(d) == len(NAN)}


def main():
    des = deseabilidad_nan()
    # P4 (banco v3.1, §24) se selecciona aparte: el banco v3 queda congelado.
    banco = {i[0]: i for i in cal.banco() if i[5] != "P4"}
    por_faceta = defaultdict(list)
    for iid, (_, rasgo, sit, alto, bajo, origen, faceta, ctx) in banco.items():
        if iid in des:
            por_faceta[(rasgo, faceta)].append(iid)
    sel, informe = [], []
    for (rasgo, faceta), ids in sorted(por_faceta.items()):
        cuota = CUOTA.get(rasgo, 10)
        ventana = sorted((i for i in ids if VENTANA[0] <= des[i] <= VENTANA[1]),
                         key=lambda i: abs(des[i] - .5))[:cuota]
        bajos = sorted((i for i in ids if des[i] < VENTANA[0]), key=lambda i: -des[i])
        altos = sorted((i for i in ids if des[i] > VENTANA[1]), key=lambda i: des[i])
        k = max(0, min(len(bajos), len(altos), (cuota - len(ventana)) // 2))
        elegidas = ventana + bajos[:k] + altos[:k]
        sel += elegidas
        informe.append((rasgo, faceta, len(ids), len(ventana), k, len(elegidas), cuota,
                        float(np.mean([des[i] for i in elegidas])) if elegidas else None))
    salida = []
    for iid in sel:
        _, rasgo, sit, alto, bajo, origen, faceta, ctx = banco[iid]
        salida.append(dict(id=iid, rasgo=rasgo, faceta=faceta, contexto=ctx, origen=origen,
                           situacion=sit, alto=alto, bajo=bajo,
                           p_alto_deseable_nan=round(des[iid], 3)))
    (AQUI / "personalidad_v3_seleccion.json").write_text(
        json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{'rasgo':5s} {'faceta':22s} cand  vent pares elegidas/cuota  deseab.media")
    for r, f, n, v, k, e, c, dm in informe:
        print(f"{r:5s} {f:22s} {n:4d} {v:5d} {k:5d} {e:5d}/{c:<5d} {'—' if dm is None else f'{100 * dm:.0f} %'}")
    from collections import Counter
    c = Counter(s["rasgo"] for s in salida)
    print("total", len(salida), dict(c), "· de ellas nuevas (P3):",
          sum(s["origen"] == "P3" for s in salida))


if __name__ == "__main__":
    main()
