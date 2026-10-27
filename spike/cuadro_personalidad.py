"""Cuadro de personalidad por modelo (PERSONALIDAD.md §17).

Puntuación principal = conducta propia (R3: «si estuvieras en su lugar, ¿qué
harías?») ajustada por lo que el propio modelo juzga admirable (§8):
50 = elige exactamente lo que él mismo considera ideal; más de 50 = más rasgo
del que su ideal predice. Es la medida que distingue modelos (5 de 6 rasgos
con 9 modelos, §11) y la única que no depende de cómo usa una escala.

Lectura entre modelos: para cada rasgo se compara cada modelo con la media de
los modelos medidos; «▲/▼» solo si su IC 95 % (bootstrap por ítem) no
incluye esa media. Sin marca = no distinguible de la media.

Al lado, la AUTOIMAGEN (autoinforme Likert, 0-100): lo que el modelo dice de
sí mismo. No se usa para ordenar modelos (§9.3, §11).

Uso: python cuadro_personalidad.py   → resultados/personalidad_fc/CUADRO.md
"""

import json
import pathlib

import numpy as np

import analizar_personalidad_p1 as ap1
import personalidad_p1_items as p1
from analizar_discriminacion import _id, iss_por_modelo
from analizar_personalidad import cargar

AQUI = pathlib.Path(__file__).parent
SALIDA = AQUI / "resultados" / "personalidad_fc"
RASGOS = p1.RASGOS
NOMBRE = {"O": "Apertura", "C": "Responsabilidad", "E": "Extraversión",
          "A": "Amabilidad", "N": "Neuroticismo", "H": "Honestidad-Humildad"}
POLOS = {"O": ("curioso, busca lo nuevo", "prefiere lo conocido"),
         "C": ("cumple y planifica", "prioriza descanso y flexibilidad"),
         "E": ("busca gente y protagonismo", "prefiere calma y segundo plano"),
         "A": ("cede y coopera", "pone límites y se defiende"),
         "N": ("reacciona, se preocupa", "se mantiene sereno"),
         "H": ("sincero, renuncia a ventajas", "acepta ventajas y se promociona")}


def main():
    datos = cargar(ap1.DIR)
    des = ap1.deseabilidad()
    res = {m: ap1.analizar_modelo(f, des[m]) for m, f in datos.items() if m in des}
    ms = sorted(res)
    iss = iss_por_modelo()
    media = {t: float(np.mean([res[m]["rasgos"][t]["R3_ajustada"][0] for m in ms]))
             for t in RASGOS}
    marca = {}
    for m in ms:
        for t in RASGOS:
            p, lo, hi = res[m]["rasgos"][t]["R3_ajustada"]
            marca[(m, t)] = "▲" if lo > media[t] else "▼" if hi < media[t] else ""
    L = ["# Cuadro de personalidad por modelo", "",
         "Generado por `cuadro_personalidad.py` con los datos del P1 (PERSONALIDAD.md §17).",
         "**Conducta** = lo que el modelo elige cuando decide él, ajustado por lo que él mismo"
         " juzga admirable (50 = elige su ideal). ▲/▼ = por encima/debajo de la media de los"
         f" {len(ms)} modelos con IC 95 % que no la incluye. **Autoimagen** = lo que dice de sí"
         " mismo en el cuestionario (0-100); no sirve para ordenar modelos.", "",
         "## Conducta (puntuación principal)", "",
         "| modelo | ISS | " + " | ".join(NOMBRE[t] for t in RASGOS) + " |",
         "|---|---|" + "---|" * len(RASGOS)]
    for m in ms:
        L.append(f"| {_id(m)} | {iss.get(_id(m), '—')} | " + " | ".join(
            f"{res[m]['rasgos'][t]['R3_ajustada'][0]:.0f} {marca[(m, t)]}".strip()
            for t in RASGOS) + " |")
    L.append("| *media de los modelos* | | " + " | ".join(f"*{media[t]:.0f}*" for t in RASGOS) + " |")
    L += ["", "## Autoimagen (cuestionario)", "",
          "| modelo | " + " | ".join(NOMBRE[t] for t in RASGOS) + " |",
          "|---|" + "---|" * len(RASGOS)]
    for m in ms:
        L.append(f"| {_id(m)} | " + " | ".join(
            f"{res[m]['rasgos'][t]['R1'][0]:.0f}" for t in RASGOS) + " |")
    L += ["", "## Retrato de cada modelo (solo rasgos distinguibles de la media)", ""]
    for m in ms:
        rasgos = [(t, marca[(m, t)]) for t in RASGOS if marca[(m, t)]]
        if rasgos:
            txt = "; ".join(f"**{'más' if s == '▲' else 'menos'} {NOMBRE[t]}** "
                            f"({POLOS[t][0] if s == '▲' else POLOS[t][1]})" for t, s in rasgos)
        else:
            txt = "ningún rasgo se separa de la media de los modelos"
        L.append(f"- **{_id(m)}**: {txt}.")
    texto = "\n".join(L) + "\n"
    (SALIDA / "CUADRO.md").write_text(texto, encoding="utf-8")
    (SALIDA / "cuadro.json").write_text(json.dumps(
        {m: {t: {"conducta": res[m]["rasgos"][t]["R3_ajustada"],
                 "autoimagen": res[m]["rasgos"][t]["R1"], "marca": marca[(m, t)]}
             for t in RASGOS} for m in ms}, ensure_ascii=False, indent=2, default=float),
        encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
