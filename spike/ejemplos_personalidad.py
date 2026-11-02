"""Situaciones de ejemplo para /personalidad/datos: qué eligió cada modelo.

    python spike/ejemplos_personalidad.py     # escribe resultados/personalidad_fc/ejemplos.json

La página de datos de personalidad enseña unas pocas situaciones reales del
test con la elección de cada modelo del cuadro, al modo de las «preguntas de
ejemplo» de otros benchmarks. No es una medida nueva ni entra en ninguna
puntuación: es la elección bruta (fracción de veces que eligió el polo alto,
sobre sus réplicas válidas) en situaciones que ya puntúan en el cuadro.

Selección determinista, fijada antes de mirar a ningún modelo concreto: por
rasgo, las DOS situaciones con más varianza entre modelos de la fracción de
polo alto (las que más separan al panel), con al menos `MIN_VALIDAS` réplicas
válidas por modelo. Los ítems ya son públicos en el repositorio
(`personalidad_v3_seleccion.json`, `personalidad_hn_finos_items.py`), así que
enseñarlos no añade contaminación nueva.
"""

from __future__ import annotations

import json
import pathlib
import statistics

import analizar_h_confirmacion as ahc
import analizar_n_confirmacion as anc
import cuadro_publico_v3 as cpv
import experimento_personalidad_hn_finos as ehn
import personalidad_hn_finos_items as hn
from experimento_personalidad import _nombre

AQUI = pathlib.Path(__file__).parent
CUADRO = AQUI / "resultados" / "personalidad_fc" / "cuadro_publico.json"
SALIDA = AQUI / "resultados" / "personalidad_fc" / "ejemplos.json"
POR_RASGO = 2
MIN_VALIDAS = 3


def _fraccion(registros):
    validas = [alto for (_, _, alto) in registros if alto is not None]
    return (sum(validas) / len(validas), len(validas)) if len(validas) >= MIN_VALIDAS else (None, len(validas))


def main() -> int:
    cuadro = json.loads(CUADRO.read_text(encoding="utf-8"))
    panel = [(m["id"], m["modelo"]) for m in cuadro["modelos"]]
    carpetas = [c for c, _ in panel]

    # O, C, E y A: el banco v3 (texto y nombre como en experimento_personalidad_v3)
    v = cpv.cargar_v3(cpv.selecciones_por_defecto(), rasgos=cpv.RASGOS_V3)
    sel = {d["id"]: d for d in v["sel"]}
    import calibrar_deseabilidad as cal  # el índice de nombres del banco v3
    idx = {i[0]: k for k, i in enumerate(cal.banco())}
    fuentes = {}
    for iid, d in sel.items():
        fuentes[iid] = dict(rasgo=d["rasgo"], faceta=d["faceta"], situacion=d["situacion"],
                            alto=d["alto"], bajo=d["bajo"], nombre=_nombre(idx[iid])[0],
                            el={c: v["elecciones"].get(c, {}).get(iid, []) for c in carpetas})
    # H y N: los ítems I1 (binario), con su propio cargador
    for t, items, cargar in (("H", ahc.ITEMS, ahc.cargar), ("N", anc.ITEMS_A, anc.cargar_a)):
        el = cargar(carpetas)["elecciones"]
        for k, x in enumerate(hn.I1):
            if x[0] in items:
                fuentes[x[0]] = dict(rasgo=t, faceta=x[2], situacion=x[3], alto=x[4], bajo=x[5],
                                     nombre=_nombre(k + ehn._DESPL["I1"])[0],
                                     el={c: el.get(c, {}).get(x[0], []) for c in carpetas})

    salida = []
    for t in ("O", "C", "E", "A", "N", "H"):
        candidatos = []
        for iid, f in fuentes.items():
            if f["rasgo"] != t:
                continue
            fr = {c: _fraccion(f["el"][c]) for c in carpetas}
            vals = [p for p, _ in fr.values() if p is not None]
            if len(vals) < len(carpetas) * 0.9:
                continue
            candidatos.append((statistics.pvariance(vals), iid, fr))
        for var, iid, fr in sorted(candidatos, key=lambda x: (-x[0], x[1]))[:POR_RASGO]:
            f = fuentes[iid]
            salida.append({
                "id": iid, "rasgo": t, "faceta": f["faceta"],
                "situacion": f["situacion"].replace("{nombre}", f["nombre"]),
                "alto": f["alto"], "bajo": f["bajo"], "varianza": round(var, 4),
                "elecciones": [{"modelo": mod, "alto": None if fr[c][0] is None else round(fr[c][0], 3),
                                "n": fr[c][1]} for c, mod in panel],
            })
    SALIDA.write_text(json.dumps({
        "generado_por": "spike/ejemplos_personalidad.py",
        "criterio": f"por rasgo, las {POR_RASGO} situaciones con más varianza entre modelos de la "
                    f"fracción de polo alto (≥ {MIN_VALIDAS} réplicas válidas por modelo)",
        "situaciones": salida}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[ejemplos] {len(salida)} situaciones → {SALIDA.relative_to(AQUI.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
