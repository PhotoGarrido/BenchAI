"""Cuadro público de personalidad: conducta comparada (PERSONALIDAD.md §28).

Definición fijada en §28 ANTES de recalcular. Por modelo m, situación i:
  e_m(i) = fracción de veces que elige el polo alto en R3 (órdenes × réplicas)
  d̄(i)   = media de los juicios de deseabilidad de TODOS los modelos del panel
  comparación = 50·(e_m(i) − media de los demás e_o(i)), IC 95 % por bootstrap
                de situaciones (≡ marca de §26 con deseabilidad común: d̄ se
                cancela)
  puntuación  = 50 + 50·media_i(e_m(i) − d̄(i))   (50 = elige lo que el panel
                juzga admirable)
Marca candidata: el IC de la comparación excluye 0. Se le aplican las
comprobaciones de §26 sobre esta comparación (P4 ya es la definición):
  P1 mitades por faceta (200 particiones): tasa de signo ≥ 90 %
  P2 réplica 0 y réplica 1 · P3 orden AB y BA: se mantiene en las dos
  P5 sin cada laboratorio: se mantiene en todos los paneles
  P6 Benjamini-Hochberg sobre todas las pruebas del cuadro (modelos × 6 rasgos)
Niveles de §26 sobre esas cinco: robusta (pasa todas) · frágil (falla 1-2,
signo P1 ≥ 75 %) · no publicable (signo P1 < 75 %, falla ≥ 3, se invierte en
alguna variante, o rasgo N). Solo las robustas llevan marca y frase; E con
aviso de fiabilidad; N solo descriptivo (§23). El cuadro se rehace entero:
toda marca candidata pasa por las mismas comprobaciones, estuviera o no en el
cuadro v2.

Validez (añadida a petición, 20-10): G3 y G4 de §21 recalculados sobre la
puntuación de §28. No cambian qué rasgos llevan marca; si un rasgo con marca
queda con G4 < 0,70, o E/N con G4 ≥ 0,70, se señala como CONFLICTO para que
lo resuelva David y se muestra, aparte, un escenario NO decidido con marca en
los rasgos de G4 ≥ 0,70.

Reutiliza analizar_v3 (carga, puntuación, diferencia pareada) y
analizar_robustez_v3 (variantes, laboratorios, mitades, BH, niveles, frases),
con la semilla SEMILLA. Sin llamadas a modelos. El cuadro con la deseabilidad
propia (CUADRO_V3.md, analizar_v3.py) queda como salida secundaria.

Cómo se rehace (un solo comando, desde spike/):

    python cuadro_publico_v3.py
      → resultados/personalidad_fc/CUADRO_PUBLICO.md y cuadro_publico.json

Nada está fijado a mano: los modelos salen de los datos (los que tienen
deseabilidad y ≥ 95 % de las situaciones de la selección con dato, filtro de
cargar_v3), las situaciones de la selección (solo las que tienen dato en
todos los modelos que entran) y los laboratorios del id (laboratorio()).
- Banco v3.1 de E y N: si sus situaciones se añaden a
  personalidad_v3_seleccion.json, basta con volver a ejecutar. Si llegan en
  un fichero nuevo `personalidad_v3*_seleccion.json` (p. ej.
  personalidad_v3.1_seleccion.json), se lee también por defecto, después del
  de v3 (un id repetido toma la última definición). Para elegir los ficheros
  a mano: `python cuadro_publico_v3.py --seleccion A.json B.json`.
  Ojo: un modelo que no tenga ≥ 95 % de la selección conjunta queda fuera
  hasta que se complete.
- Modelos nuevos completados: entran solos al volver a ejecutar. Si es un
  modelo de NaN sin prefijo de organización, añadir su familia a
  FAMILIA_NAN (analizar_robustez_v3.py) para que P5 lo agrupe bien.
"""

import argparse
import json
import pathlib

import numpy as np

from analizar_discriminacion import _id, iss_por_modelo
from analizar_personalidad import SEMILLA
from analizar_robustez_v3 import (B_FDR, Q, _ic_p, bh, clasificar, d_consenso,
                                  frase, laboratorio, marcas_variante, mitades,
                                  particiones)
from analizar_v3 import (AQUI, RASGOS, SALIDA, SEL, _boot, cargar_v3,
                         dif_pareada, facetas_score, g3_estructura,
                         g4_consistencia, puntuar)
from cuadro_personalidad import NOMBRE, POLOS

PRUEBAS = ("P1", "P2", "P3", "P5", "P6")
ETIQUETA = "P1–P3, P5, P6"
CON_MARCA = ("O", "C", "A", "H")  # §23/§28: E solo si robusta y con aviso; N nunca
AVISO_E = "Extraversión: fiabilidad baja (§23), con aviso"
G4_MIN = .70  # umbral de consistencia de §21 (G4)
FILTROS = {"rep0": lambda o, r: r == 0, "rep1": lambda o, r: r == 1,
           "AB": lambda o, r: o == "AB", "BA": lambda o, r: o == "BA"}


def selecciones_por_defecto():
    """El fichero del banco v3 y, detrás, cualquier `personalidad_v3*_seleccion.json`."""
    extra = sorted(p for p in AQUI.glob("personalidad_v3*_seleccion.json") if p != SEL)
    return [SEL] + extra


def calcular(rutas_sel, escalas=None):
    """escalas: {rasgo: [situaciones]} para limitar un rasgo a una escala
    rescatada (§30-31); None = banco completo, salidas idénticas a §29."""
    rng = np.random.default_rng(SEMILLA)
    v = cargar_v3(rutas_sel)
    if escalas:
        for t, its in escalas.items():
            v["por_rasgo"][t] = [i for i in v["por_rasgo"][t] if i in set(its)]
        dentro = {i for x in v["por_rasgo"].values() for i in x}
        v["comunes"] = [i for i in v["comunes"] if i in dentro]
        v["facetas"] = sorted({(v["rasgo_de"][i], v["faceta_de"][i]) for i in v["comunes"]})
    ms, por_rasgo, des, el, comunes = v["ms"], v["por_rasgo"], v["des"], v["elecciones"], v["comunes"]
    otros = {m: [o for o in ms if o != m] for m in ms}

    # Elección bruta (comparación) y elección frente a la deseabilidad común (puntuación)
    a = {m: puntuar(el[m]) for m in ms}
    d_bar = d_consenso(des, ms, comunes)
    a_d = {m: puntuar({i: el[m][i] for i in comunes}, d_bar) for m in ms}
    punt = {}
    for m in ms:
        for t in RASGOS:
            p, lo, hi = _boot([a_d[m][i] for i in por_rasgo[t]], rng)
            punt[(m, t)] = (50 + 50 * p, 50 + 50 * lo, 50 + 50 * hi)
    base = marcas_variante(a, ms, por_rasgo, rng)

    # P2, P3: variantes de réplica y orden, con la elección bruta
    var = {k: marcas_variante({m: puntuar(el[m], None, f) for m in ms}, ms, por_rasgo, rng)
           for k, f in FILTROS.items()}
    # P5: sin cada laboratorio
    labs = sorted({laboratorio(m) for m in ms})
    var_lab = {L: marcas_variante(a, ms, por_rasgo, rng,
                                  lambda m, L=L: [o for o in ms if o != m and laboratorio(o) != L])
               for L in labs}
    # P6: p por bootstrap y BH sobre todas las pruebas del cuadro
    pruebas = [(m, t) for m in ms for t in RASGOS]
    pval = {k: _ic_p(dif_pareada(a, k[0], otros[k[0]], por_rasgo[k[1]]), rng, B_FDR)[3]
            for k in pruebas}
    q_todas = dict(zip(pruebas, bh([pval[k] for k in pruebas])))
    sin_n = [k for k in pruebas if k[1] != "N"]
    q_sin_n = dict(zip(sin_n, bh([pval[k] for k in sin_n])))
    # P1: mitades por faceta
    candidatas = [k for k in pruebas if base[k][0]]
    parts = {t: particiones(por_rasgo[t], v["faceta_de"], rng) for t in RASGOS}
    p1 = {}
    for (m, t) in candidatas:
        d = dict(zip(por_rasgo[t], dif_pareada(a, m, otros[m], por_rasgo[t])))
        p1[(m, t)] = mitades(d, parts[t], base[(m, t)][0], rng)

    variantes = list(var.items()) + [(f"sin {L}", var_lab[L]) for L in labs]
    filas = {}
    for k in candidatas:
        m, t = k
        s0 = base[k][0]
        se_mantiene = lambda x: x[k][0] == s0  # noqa: E731
        paso = {"P1": p1[k]["tasa_signo"] >= .90,
                "P2": se_mantiene(var["rep0"]) and se_mantiene(var["rep1"]),
                "P3": se_mantiene(var["AB"]) and se_mantiene(var["BA"]),
                "P5": all(se_mantiene(var_lab[L]) for L in labs),
                "P6": q_todas[k] < Q}
        caen = [L for L in labs if not se_mantiene(var_lab[L])]
        inv = [n for n, x in variantes if x[k][0] not in ("", s0)]
        fallos = [p for p in PRUEBAS if not paso[p]]
        nivel, motivo = clasificar(t, p1[k]["tasa_signo"], fallos, inv, ETIQUETA)
        # Nivel sin la regla «N solo descriptivo», para el escenario según G4
        nivel_sin_regla = clasificar("", p1[k]["tasa_signo"], fallos, inv, ETIQUETA)[0]
        if caen:
            motivo += f"; cae sin {', '.join(caen)}"
        filas[k] = {"marca": s0, "dif": base[k][1], "ic": list(base[k][2:4]), "paso": paso,
                    "fallos": fallos, "nivel": nivel, "nivel_sin_regla_N": nivel_sin_regla,
                    "motivo": motivo, "p": pval[k],
                    "q": q_todas[k], "q_sin_N": q_sin_n.get(k), "p1": p1[k],
                    "cae_sin_lab": caen, "invierte_en": inv,
                    "variantes": {n: x[k][0] for n, x in variantes}}

    def publicable(m, t):
        f = filas.get((m, t))
        return f["marca"] if f and f["nivel"] == "robusta" and t != "N" else ""

    retratos = {}
    for m in ms:
        partes = [frase(t, publicable(m, t)) for t in CON_MARCA if publicable(m, t)]
        if publicable(m, "E"):
            partes.append(frase("E", publicable(m, "E")) + f" *[{AVISO_E}]*")
        retratos[m] = {"frase": "; ".join(partes) if partes else "perfil próximo al de los demás modelos",
                       "fragiles": [f"{t}{filas[(m, t)]['marca']}" for t in RASGOS
                                    if (m, t) in filas and filas[(m, t)]["nivel"] == "frágil"]}
    # Validez con la definición de §28: G3 y G4 de §21 sobre e − d̄ (d̄ es común a
    # todos los modelos, así que da lo mismo que sobre la elección bruta)
    fac = facetas_score(a_d, ms, comunes, v["rasgo_de"], v["faceta_de"], v["facetas"])
    validez = {"G3": g3_estructura(fac, v["facetas"]), "G4": g4_consistencia(a_d, ms, por_rasgo)}
    conflictos = []
    for t in RASGOS:
        g = validez["G4"][t]
        if t in CON_MARCA and (g is None or g < G4_MIN):
            conflictos.append((t, f"lleva marca (§28), pero G4 = {g:.2f} < {G4_MIN:.2f}"))
        elif t == "E" and g is not None and g >= G4_MIN:
            conflictos.append((t, f"marca solo con aviso de fiabilidad (§28), pero G4 = {g:.2f} ≥ {G4_MIN:.2f}"))
        elif t == "N" and g is not None and g >= G4_MIN:
            conflictos.append((t, f"sin marca (§28), pero G4 = {g:.2f} ≥ {G4_MIN:.2f}"))
    # Escenario alternativo, NO decidido: llevan marca los rasgos con G4 ≥ umbral,
    # sin aviso, con los mismos niveles de robustez (sin la regla de N)
    con_marca_g4 = [t for t in RASGOS if (validez["G4"][t] or 0) >= G4_MIN]

    def publicable_g4(m, t):
        f = filas.get((m, t))
        return f["marca"] if f and t in con_marca_g4 and f["nivel_sin_regla_N"] == "robusta" else ""

    retratos_g4 = {m: "; ".join(frase(t, publicable_g4(m, t)) for t in con_marca_g4 if publicable_g4(m, t))
                   or "perfil próximo al de los demás modelos" for m in ms}
    return {"v": v, "ms": ms, "labs": labs, "punt": punt, "base": base, "filas": filas,
            "publicable": publicable, "retratos": retratos, "n_pruebas": len(pruebas),
            "validez": validez, "conflictos": conflictos, "con_marca_g4": con_marca_g4,
            "publicable_g4": publicable_g4, "retratos_g4": retratos_g4}


def escribir(r, rutas_sel):
    v, ms, labs, punt, base, filas = r["v"], r["ms"], r["labs"], r["punt"], r["base"], r["filas"]
    publicable, retratos = r["publicable"], r["retratos"]
    iss = iss_por_modelo()
    cnt = {n: sum(f["nivel"] == n for f in filas.values()) for n in ("robusta", "frágil", "no publicable")}
    sels = [pathlib.Path(p).name for p in rutas_sel]
    ok = lambda b: "✔" if b else "✘"  # noqa: E731

    L = ["# Cuadro público de personalidad · conducta comparada (PERSONALIDAD.md §28)", "",
         f"Generado por `cuadro_publico_v3.py`. Selección: {', '.join(sels)}. {len(ms)} modelos,"
         f" {len(labs)} laboratorios ({', '.join(labs)}); situaciones por rasgo: "
         + ", ".join(f"{t} {len(x)}" for t, x in v["por_rasgo"].items())
         + f". Semilla {SEMILLA}. Sin llamadas a modelos.",
         f"Fuera por banco incompleto (< 95 %): "
         f"{', '.join(f'{_id(m)} ({100 * c:.0f} %)' for m, c in v['excluidos'].items()) or 'ninguno'}.", "",
         "**Puntuación** = 50 + 50·media(elige el polo alto − deseabilidad media del panel):"
         " 50 = elige lo que el conjunto de modelos juzga admirable. **▲/▼** = elige el polo alto"
         " más/menos a menudo que los demás modelos en las mismas situaciones (comparación pareada,"
         f" IC 95 %), solo si la marca es **robusta** ({ETIQUETA}). Extraversión con aviso de"
         " fiabilidad; Neuroticismo solo descriptivo, sin marca.", "",
         "| modelo | ISS | " + " | ".join(NOMBRE[t] + (" †" if t == "E" else " ‡" if t == "N" else "")
                                          for t in RASGOS) + " |",
         "|---|---|" + "---|" * len(RASGOS)]
    for m in ms:
        L.append(f"| {_id(m)} | {iss.get(_id(m), '—')} | " + " | ".join(
            f"{punt[(m, t)][0]:.0f} {publicable(m, t)}".strip() for t in RASGOS) + " |")
    val, conf = r["validez"], r["conflictos"]
    L += ["", "† fiabilidad baja (§23): marca solo si robusta, con aviso. ‡ solo descriptivo (§23).", "",
          "## Validez con la definición de §28 (G3 y G4 de §21)", "",
          "Mismos cálculos que `analizar_v3.py` (G3: r media entre facetas del mismo rasgo frente a"
          " facetas de otros rasgos; G4: Spearman-Brown de mitades pares/impares entre modelos), pero"
          " sobre la puntuación de §28 en vez de la ajustada por la deseabilidad propia.", "",
          "| rasgo | G3 dentro / fuera | G3 | G4 | G4 ≥ 0,70 | en §28 |", "|---|---|---|---|---|---|"]
    for t in RASGOS:
        d3, f3 = val["G3"][t]
        g4 = val["G4"][t]
        papel = "con marca" if t in CON_MARCA else "marca solo robusta, con aviso" if t == "E" else "solo descriptivo"
        L.append(f"| {NOMBRE[t]} | {d3:+.2f} / {f3:+.2f} | {ok(d3 > f3)} | {g4:.2f} | {ok(g4 >= G4_MIN)} | {papel} |")
    L += [""]
    if conf:
        L += ["**CONFLICTO entre §28 y la consistencia con la definición nueva (lo resuelve David;"
              " este cuadro aplica §28 sin cambios):**", ""]
        L += [f"- **{NOMBRE[t]}**: {x}." for t, x in conf]
        L += ["", "### Escenario alternativo, NO decidido: marca en los rasgos con G4 ≥ 0,70", "",
              f"Rasgos con marca: {', '.join(NOMBRE[t] for t in r['con_marca_g4'])}; el resto, solo"
              " descriptivo. Mismos niveles de robustez (sin la regla de N).", "",
              "| modelo | " + " | ".join(NOMBRE[t] for t in RASGOS) + " |", "|---|" + "---|" * len(RASGOS)]
        for m in ms:
            L.append(f"| {_id(m)} | " + " | ".join(
                f"{punt[(m, t)][0]:.0f} {r['publicable_g4'](m, t)}".strip() for t in RASGOS) + " |")
        L += [""] + [f"- **{_id(m)}**: {r['retratos_g4'][m]}." for m in ms] + [""]
    else:
        L += ["Sin conflictos: los rasgos con marca tienen G4 ≥ 0,70 y los demás, por debajo.", ""]
    L += ["## Retrato de cada modelo (§28)", ""]
    for m in ms:
        rr = retratos[m]
        L.append(f"- **{_id(m)}**: {rr['frase']}. *Neuroticismo (descriptivo): {punt[(m, 'N')][0]:.0f}.*"
                 + (f" Tendencias frágiles, no publicadas: {', '.join(rr['fragiles'])}." if rr["fragiles"] else ""))
    L += ["", "## Marcas candidatas y su nivel", "",
          f"**{len(filas)} marcas candidatas** (IC de la comparación que excluye 0): {cnt['robusta']} robustas"
          f" · {cnt['frágil']} frágiles · {cnt['no publicable']} no publicables.", "",
          "P1 = signo replicado en las dos mitades (≥ 90 %) · P2 = réplica 0 y 1 · P3 = orden AB y BA ·"
          f" P5 = todos los paneles sin un laboratorio · P6 = BH q < 0,05 sobre {r['n_pruebas']} pruebas"
          " (entre paréntesis, sin N).", "",
          "| modelo | rasgo | marca | dif [IC] | P1 signo (sig. ambas) | P2 | P3 | P5 | P6 q (sin N) | nivel | por qué |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for (m, t), f in filas.items():
        L.append(f"| {_id(m)} | {t} | {f['marca']} | {f['dif']:+.1f} [{f['ic'][0]:+.1f}, {f['ic'][1]:+.1f}]"
                 f" | {100 * f['p1']['tasa_signo']:.0f} % ({100 * f['p1']['tasa_sig_ambas']:.0f} %)"
                 f" | {ok(f['paso']['P2'])} | {ok(f['paso']['P3'])} | {ok(f['paso']['P5'])}"
                 f" | {f['q']:.4f} ({'—' if f['q_sin_N'] is None else f'{f["q_sin_N"]:.4f}'})"
                 f" | **{f['nivel']}** | {f['motivo']} |")
    L += ["", "## Variantes de cada marca candidata", "", "Marca en cada variante (· = sin marca).", "",
          "| modelo | rasgo | cuadro | rep0 | rep1 | AB | BA | " + " | ".join(f"sin {x}" for x in labs) + " |",
          "|---|---|---|---|---|---|---|" + "---|" * len(labs)]
    for (m, t), f in filas.items():
        vv = f["variantes"]
        L.append(f"| {_id(m)} | {t} | {f['marca']} | " + " | ".join(
            vv[n] or "·" for n in ["rep0", "rep1", "AB", "BA"] + [f"sin {x}" for x in labs]) + " |")
    L += ["", "## Puntuación con IC 95 %", "", "| modelo | " + " | ".join(RASGOS) + " |",
          "|---|" + "---|" * len(RASGOS)]
    for m in ms:
        L.append(f"| {_id(m)} | " + " | ".join(
            f"{punt[(m, t)][0]:.0f} [{punt[(m, t)][1]:.0f}, {punt[(m, t)][2]:.0f}]" for t in RASGOS) + " |")
    (SALIDA / "CUADRO_PUBLICO.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    modelos = []
    for m in ms:
        rasgos = {}
        for t in RASGOS:
            f = filas.get((m, t))
            rasgos[t] = {"puntuacion": punt[(m, t)][0], "ic": list(punt[(m, t)][1:]),
                         "comparacion": {"dif": base[(m, t)][1], "ic": list(base[(m, t)][2:4])},
                         "marca": publicable(m, t),
                         "candidata": f["marca"] if f else "",
                         "nivel": f["nivel"] if f else None,
                         "motivo": f["motivo"] if f else None,
                         "q": f["q"] if f else None}
        modelos.append({"id": m, "modelo": _id(m), "laboratorio": laboratorio(m),
                        "iss": iss.get(_id(m)), "rasgos": rasgos,
                        "frase": retratos[m]["frase"].replace("**", ""),
                        "frase_md": retratos[m]["frase"], "fragiles": retratos[m]["fragiles"]})
    (SALIDA / "cuadro_publico.json").write_text(json.dumps({
        "definicion": "PERSONALIDAD.md §28: conducta comparada",
        "generado_por": "spike/cuadro_publico_v3.py", "semilla": SEMILLA, "seleccion": sels,
        "n_situaciones": {t: len(x) for t, x in v["por_rasgo"].items()},
        "fuera_por_cobertura": v["excluidos"], "laboratorios": labs,
        "comprobaciones": list(PRUEBAS), "n_pruebas_bh": r["n_pruebas"],
        "rasgos": {t: {"nombre": NOMBRE[t], "polo_alto": POLOS[t][0], "polo_bajo": POLOS[t][1],
                       "con_marca": t != "N",
                       "aviso": AVISO_E if t == "E" else "solo descriptivo (§23)" if t == "N" else None}
                   for t in RASGOS},
        "recuento": cnt, "modelos": modelos,
        "validez_s28": {"G3": {t: {"dentro": d, "fuera": f} for t, (d, f) in r["validez"]["G3"].items()},
                        "G4": r["validez"]["G4"], "umbral_G4": G4_MIN,
                        "conflictos": [{"rasgo": t, "detalle": x} for t, x in r["conflictos"]],
                        "escenario_g4_no_decidido": {
                            "rasgos_con_marca": r["con_marca_g4"],
                            "marcas": {m: {t: r["publicable_g4"](m, t) for t in RASGOS} for m in ms},
                            "frases": {m: r["retratos_g4"][m].replace("**", "") for m in ms}}},
        "marcas_candidatas": {f"{m}|{t}": f for (m, t), f in filas.items()}},
        ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    return L


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seleccion", nargs="+", type=pathlib.Path,
                    help="ficheros de selección (por defecto: v3 + personalidad_v3*_seleccion.json)")
    args = ap.parse_args(argv)
    rutas = args.seleccion or selecciones_por_defecto()
    print("\n".join(escribir(calcular(rutas), rutas)))


if __name__ == "__main__":
    main()
