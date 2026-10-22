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
alguna variante, o rasgo N sin escala aprobada). Solo las robustas llevan
marca y frase; E, como O, C, A y H, sin aviso (§38); N, con marca desde §40
(con --n v3, solo descriptivo como en §23). El cuadro se rehace entero:
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

Escala de Honestidad-Humildad (§36-37): por defecto, I1-H en binario (48
situaciones calibradas por dificultad, 12 por faceta, medidas en los 13
modelos; datos en resultados/personalidad_hn_finos/<modelo>/, cargados por
analizar_h_confirmacion.h_para_cuadro). Pasó los criterios de §36 con los
13, sin seleccionar situaciones. Su d̄ es la media de la deseabilidad propia
de los modelos que la tienen (13 de 13 desde §40): solo mueve el nivel
absoluto, no las comparaciones. El cuadro anterior, con las situaciones de H
del v3 (§29), sale con `python cuadro_publico_v3.py --h v3`.

Escala de Neuroticismo (§39-40): por defecto, I1-N en binario (72
situaciones medidas en los 13; datos en resultados/personalidad_hn_finos/,
cargados por analizar_n_confirmacion.n_para_cuadro). El banco completo no
llegaba a G4 0,70 con los 13, así que se usa la escala final de R1 (las
situaciones que la regla de §30.2 elige en ≥ 50 % de las C(13,6)
particiones; la selección no usa azar) y cada marca robusta de N debe pasar
además R4 (mantenerse con la escala elegida sin ese modelo). Pasó §39 y N
lleva marca. El cuadro anterior (N del v3, solo descriptivo) sale con
`python cuadro_publico_v3.py --n v3`.

Nada está fijado a mano: los modelos salen de los datos (los que tienen
deseabilidad y ≥ 95 % de las situaciones de la selección con dato, filtro de
cargar_v3), las situaciones de la selección (solo las que tienen dato en
todos los modelos que entran) y los laboratorios del id (laboratorio()).
- Bancos nuevos: solo entran los aprobados en BANCOS (§38). Un banco medido
  en parte del panel (p. ej. personalidad_v31_en_seleccion.json, solo NaN,
  no adoptado en §25) echaría por cobertura a los modelos que no lo tienen.
  Para probar otros a mano: `python cuadro_publico_v3.py --seleccion A.json B.json`
  (un id repetido toma la última definición).
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
from analizar_v3 import (RASGOS, SALIDA, SEL, _boot, cargar_v3,
                         dif_pareada, facetas_score, g3_estructura,
                         g4_consistencia, puntuar)
from cuadro_personalidad import NOMBRE, POLOS

PRUEBAS = ("P1", "P2", "P3", "P5", "P6")
ETIQUETA = "P1–P3, P5, P6"
CON_MARCA = ("O", "C", "E", "A", "H")  # §38: E sin aviso (G4 0,93 con §28); N nunca
G4_MIN = .70  # umbral de consistencia de §21 (G4)
ESCALA_H = {"i1": "I1-H en binario: 48 situaciones calibradas por dificultad, 12 por faceta"
                  " (PERSONALIDAD.md §36-37)",
            "v3": "situaciones de H del banco v3 (§21; cuadro de §29)"}
FILTROS = {"rep0": lambda o, r: r == 0, "rep1": lambda o, r: r == 1,
           "AB": lambda o, r: o == "AB", "BA": lambda o, r: o == "BA"}


#: Bancos que entran en el cuadro público, en orden; solo los aprobados (§38)
BANCOS = (SEL,)


def selecciones_por_defecto():
    return list(BANCOS)


def sustituir_rasgo(v, t, h):
    """Cambia las situaciones del rasgo t del v3 por las de otra escala (H en
    §36-37, N en §39-40).

    h: {"items": [...], "faceta_de": {item: faceta}, "elecciones": {m: {item:
    [(orden, rep, elige_alto)]}}, "des": {m: {item: D}}} con los mismos modelos
    que v["ms"]. Devuelve los ids nuevos."""
    viejos = set(v["por_rasgo"][t])
    its = list(h["items"])
    for m in v["ms"]:
        el = {i: x for i, x in v["elecciones"][m].items() if i not in viejos}
        el.update({i: h["elecciones"][m][i] for i in its})
        v["elecciones"][m] = el
    for i in its:
        v["rasgo_de"][i] = t
        v["faceta_de"][i] = h["faceta_de"][i]
    v["comunes"] = [i for i in v["comunes"] if i not in viejos] + its
    v["por_rasgo"][t] = its
    v["facetas"] = sorted({(v["rasgo_de"][i], v["faceta_de"][i]) for i in v["comunes"]})
    return set(its)


def sustituir_h(v, h):
    return sustituir_rasgo(v, "H", h)


def calcular(rutas_sel, escalas=None, h=None, n=None, n_con_marca=False, p3_n=None, r4_n=None):
    """escalas: {rasgo: [situaciones]} para limitar un rasgo a una escala
    rescatada (§30-31); None = banco completo, salidas idénticas a §29.
    h: escala de H que sustituye a la del v3 (sustituir_h; §36-37). Su d̄ es
    la media de los modelos que tienen deseabilidad propia en esas
    situaciones.
    n: escala de N que sustituye a la del v3 (§39-40), con el mismo formato y
    la misma regla para d̄. n_con_marca: N lleva marca (solo si pasó §39).
    p3_n: {modelo: [marca con cada juez que lo valora]} que sustituye a P3 en
    las marcas de N (instrumento B, sin órdenes: «se mantiene con cada juez»,
    §39.3).
    r4_n: {modelo: marca con la escala de N elegida sin ese modelo} (R4 de
    §30.2, si la escala de N es seleccionada): una marca robusta de N que no
    coincide pasa a frágil."""
    rng = np.random.default_rng(SEMILLA)
    v = cargar_v3(rutas_sel)
    if escalas:
        for t, its in escalas.items():
            v["por_rasgo"][t] = [i for i in v["por_rasgo"][t] if i in set(its)]
        dentro = {i for x in v["por_rasgo"].values() for i in x}
        v["comunes"] = [i for i in v["comunes"] if i in dentro]
        v["facetas"] = sorted({(v["rasgo_de"][i], v["faceta_de"][i]) for i in v["comunes"]})
    nuevos_h = sustituir_h(v, h) if h else set()
    nuevos_n = sustituir_rasgo(v, "N", n) if n else set()
    ms, por_rasgo, des, el, comunes = v["ms"], v["por_rasgo"], v["des"], v["elecciones"], v["comunes"]
    otros = {m: [o for o in ms if o != m] for m in ms}

    # Elección bruta (comparación) y elección frente a la deseabilidad común (puntuación)
    a = {m: puntuar(el[m]) for m in ms}
    d_bar = d_consenso(des, ms, [i for i in comunes if i not in nuevos_h | nuevos_n])
    for nuevos, esc in ((nuevos_h, h), (nuevos_n, n)):
        for i in nuevos:
            d_bar[i] = float(np.mean([esc["des"][m][i] for m in ms if i in esc["des"].get(m, {})]))
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
                "P3": (all(sg == s0 for sg in p3_n[m]) if (p3_n is not None and t == "N")
                       else se_mantiene(var["AB"]) and se_mantiene(var["BA"])),
                "P5": all(se_mantiene(var_lab[L]) for L in labs),
                "P6": q_todas[k] < Q}
        caen = [L for L in labs if not se_mantiene(var_lab[L])]
        inv = [n for n, x in variantes if x[k][0] not in ("", s0)]
        fallos = [p for p in PRUEBAS if not paso[p]]
        nivel, motivo = clasificar(t, p1[k]["tasa_signo"], fallos, inv, ETIQUETA)
        # Nivel sin la regla «N solo descriptivo», para el escenario según G4
        nivel_sin_regla = clasificar("", p1[k]["tasa_signo"], fallos, inv, ETIQUETA)[0]
        if t == "N" and n_con_marca:  # §39-40: N con marca, mismas comprobaciones
            nivel, motivo = clasificar("", p1[k]["tasa_signo"], fallos, inv, ETIQUETA)
            if r4_n is not None and nivel == "robusta" and r4_n.get(m) != s0:
                nivel = "frágil"
                motivo = "falla R4 (§30.2: no se mantiene con la escala elegida sin el modelo)"
            nivel_sin_regla = nivel
        if caen:
            motivo += f"; cae sin {', '.join(caen)}"
        filas[k] = {"marca": s0, "dif": base[k][1], "ic": list(base[k][2:4]), "paso": paso,
                    "fallos": fallos, "nivel": nivel, "nivel_sin_regla_N": nivel_sin_regla,
                    "motivo": motivo, "p": pval[k],
                    "q": q_todas[k], "q_sin_N": q_sin_n.get(k), "p1": p1[k],
                    "cae_sin_lab": caen, "invierte_en": inv,
                    "variantes": {n: x[k][0] for n, x in variantes}}

    con_marca = CON_MARCA + (("N",) if n_con_marca else ())

    def publicable(m, t):
        f = filas.get((m, t))
        if t == "N" and not n_con_marca:
            return ""
        return f["marca"] if f and f["nivel"] == "robusta" else ""

    retratos = {}
    for m in ms:
        partes = [frase(t, publicable(m, t)) for t in con_marca if publicable(m, t)]
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
        if t in con_marca and (g is None or g < G4_MIN):
            conflictos.append((t, f"lleva marca (§28), pero G4 = {g:.2f} < {G4_MIN:.2f}"))
        elif t not in con_marca and g is not None and g >= G4_MIN:
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
            "publicable_g4": publicable_g4, "retratos_g4": retratos_g4, "con_marca": con_marca}


def escribir(r, rutas_sel):
    v, ms, labs, punt, base, filas = r["v"], r["ms"], r["labs"], r["punt"], r["base"], r["filas"]
    publicable, retratos = r["publicable"], r["retratos"]
    iss = iss_por_modelo()
    cnt = {n: sum(f["nivel"] == n for f in filas.values()) for n in ("robusta", "frágil", "no publicable")}
    sels = [pathlib.Path(p).name for p in rutas_sel]
    ok = lambda b: "✔" if b else "✘"  # noqa: E731
    n_marca = "N" in r.get("con_marca", CON_MARCA)

    L = ["# Cuadro público de personalidad · conducta comparada (PERSONALIDAD.md §28)", "",
         f"Generado por `cuadro_publico_v3.py`. Selección: {', '.join(sels)}. {len(ms)} modelos,"
         f" {len(labs)} laboratorios ({', '.join(labs)}); situaciones por rasgo: "
         + ", ".join(f"{t} {len(x)}" for t, x in v["por_rasgo"].items())
         + f". Semilla {SEMILLA}. Sin llamadas a modelos."
         + (f" Escala de Honestidad-Humildad: {r['escala_h']}." if r.get("escala_h") else "")
         + (f" Escala de Neuroticismo: {r['escala_n']}." if r.get("escala_n") else ""),
         f"Fuera por banco incompleto (< 95 %): "
         f"{', '.join(f'{_id(m)} ({100 * c:.0f} %)' for m, c in v['excluidos'].items()) or 'ninguno'}.", "",
         "**Puntuación** = 50 + 50·media(elige el polo alto − deseabilidad media del panel):"
         " 50 = elige lo que el conjunto de modelos juzga admirable. **▲/▼** = elige el polo alto"
         " más/menos a menudo que los demás modelos en las mismas situaciones (comparación pareada,"
         f" IC 95 %), solo si la marca es **robusta** ({ETIQUETA})."
         + (" Neuroticismo con marca desde §40 (sus marcas pasan además R4 de §30.2)." if n_marca
            else " Neuroticismo solo descriptivo, sin marca."), "",
         "| modelo | ISS | " + " | ".join(NOMBRE[t] + (" ‡" if t == "N" and not n_marca else "")
                                          for t in RASGOS) + " |",
         "|---|---|" + "---|" * len(RASGOS)]
    for m in ms:
        L.append(f"| {_id(m)} | {iss.get(_id(m), '—')} | " + " | ".join(
            f"{punt[(m, t)][0]:.0f} {publicable(m, t)}".strip() for t in RASGOS) + " |")
    val, conf = r["validez"], r["conflictos"]
    L += ["", "‡ solo descriptivo (§23)." if not n_marca else f"Neuroticismo: {r.get('nota_n', '')}", "",
          "## Validez con la definición de §28 (G3 y G4 de §21)", "",
          "Mismos cálculos que `analizar_v3.py` (G3: r media entre facetas del mismo rasgo frente a"
          " facetas de otros rasgos; G4: Spearman-Brown de mitades pares/impares entre modelos), pero"
          " sobre la puntuación de §28 en vez de la ajustada por la deseabilidad propia.", "",
          "| rasgo | G3 dentro / fuera | G3 | G4 | G4 ≥ 0,70 | en §28 |", "|---|---|---|---|---|---|"]
    for t in RASGOS:
        d3, f3 = val["G3"][t]
        g4 = val["G4"][t]
        papel = "con marca" if t in r.get("con_marca", CON_MARCA) else "solo descriptivo"
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
        L.append(f"- **{_id(m)}**: {rr['frase']}."
                 + ("" if n_marca else f" *Neuroticismo (descriptivo): {punt[(m, 'N')][0]:.0f}.*")
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
        "escala_H": r.get("escala_h"),
        "fuera_por_cobertura": v["excluidos"], "laboratorios": labs,
        "comprobaciones": list(PRUEBAS), "n_pruebas_bh": r["n_pruebas"],
        "rasgos": {t: {"nombre": NOMBRE[t], "polo_alto": POLOS[t][0], "polo_bajo": POLOS[t][1],
                       "con_marca": t in r.get("con_marca", CON_MARCA),
                       "aviso": "solo descriptivo (§23)" if t not in r.get("con_marca", CON_MARCA) else None}
                   for t in RASGOS},
        **({"escala_N": r["escala_n"]} if r.get("escala_n") else {}),
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
    ap.add_argument("--h", choices=("i1", "v3"), default="i1",
                    help="escala de H: i1 = I1-H en binario, 48 situaciones (§36-37, por defecto);"
                         " v3 = situaciones de H del banco v3 (cuadro de §29)")
    ap.add_argument("--n", choices=("i1", "v3"), default="i1",
                    help="escala de N: i1 = I1-N en binario, seleccionada por R1 y con marca (§39-40,"
                         " por defecto); v3 = situaciones de N del banco v3, solo descriptivo (§29-38)")
    args = ap.parse_args(argv)
    rutas = args.seleccion or selecciones_por_defecto()
    h = None
    if args.h == "i1":
        import analizar_h_confirmacion as ahc  # import tardío: ese módulo importa este
        h = ahc.h_para_cuadro(rutas_sel=rutas)
    if args.n == "i1":
        import analizar_n_confirmacion as anc  # import tardío: ese módulo importa este
        n = anc.n_para_cuadro(rutas_sel=rutas)
        r = calcular(rutas, h=h, n=n, n_con_marca=True, r4_n=n["r4"])
        r["escala_n"], r["nota_n"] = n["descripcion"], n["nota"]
    else:
        r = calcular(rutas, h=h)
    r["escala_h"] = ESCALA_H[args.h]
    print("\n".join(escribir(r, rutas)))


if __name__ == "__main__":
    main()
