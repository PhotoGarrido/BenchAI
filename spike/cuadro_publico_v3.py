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
puntuación de §28. Desde §41.3, revalidación automática: un rasgo con marca
que no pasa G4 (a) pares/impares ≥ 0,70, G4 (b) mediana de 200 particiones
por faceta ≥ 0,70 y G3 (dentro > fuera) pierde todas sus marcas en ese cuadro
(«en revisión»), sin intervención humana; con modelos de forma corta, también
se exige en la forma corta. (Sin --sin-revalidar ya no queda el CONFLICTO de
§29 para los rasgos con marca; un rasgo sin marca con G4 ≥ 0,70 se sigue
señalando.)

Alta de modelos (§41-42):
- Índices de validez por modelo (validez_personalidad.py, §41.2): posición
  (Δ AB−BA y fracción de A), no válidas, retest y coherencia de la
  deseabilidad. Un perfil «no interpretable» sale de la norma (no entra en la
  media de los demás, ni en d̄, ni en la selección de N, ni en P5, ni en BH) y
  se lista aparte sin puntuaciones; «aviso» publica con «interpretar con
  cautela».
- Forma corta (personalidad_forma_corta.json, §41.1-42): un modelo sin el
  banco completo entra si tiene ≥ 95 % de la forma corta de cada rasgo. Se
  compara en esas situaciones frente a los demás con dato; su puntuación se
  equipara (EQUIPARACION) a la escala completa con los modelos completos.
  Con todos completos, el cálculo es idéntico al de §40.
- Cobertura: del v3 solo se exigen O, C, E y A (H y N salen de I1).
- `--sin-validez` y `--sin-revalidar` reproducen el cuadro sin esas reglas,
  solo para comparar.

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
                         g4_consistencia, puntuar, signo)
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
#: Rasgos que el cuadro toma del banco v3 (H y N salen de I1, §37 y §40)
RASGOS_V3 = ("O", "C", "E", "A")
#: Forma corta congelada (§41.1-42); sin el fichero no entra ningún modelo con forma corta
FORMA_CORTA = pathlib.Path(__file__).parent / "personalidad_forma_corta.json"
COBERTURA_MIN = .95
#: Equiparación de la puntuación mostrada de un modelo con forma corta. §41.1
#: fijó solo la media («media»); §42 la cambia a lineal (media y desviación típica
#: entre los modelos completos) tras ver en la simulación del alta que la forma
#: corta estira la escala ×1,2-2,1. Cambio posterior a ver datos, declarado.
EQUIPARACION = "lineal"


def selecciones_por_defecto():
    return list(BANCOS)


def cargar_forma_corta(ruta=FORMA_CORTA):
    """{rasgo: [situaciones]} de la forma corta aprobada, o None si no hay."""
    ruta = pathlib.Path(ruta)
    if not ruta.exists():
        return None
    return {t: list(x["items"]) for t, x in json.loads(ruta.read_text(encoding="utf-8"))["rasgos"].items()}


def panel_publico(rutas, h_modo="i1", n_modo="i1", corta=None, validar=True):
    """Quién entra en el cuadro y con qué forma (§41.1) y validez por modelo (§41.2).

    Cobertura: O, C, E y A del v3, en conjunto (filtro de siempre, ≥ 95 %) o
    con la forma corta de cada rasgo (≥ 95 % de sus situaciones); H (I1-H, 48)
    y N (I1-N, 72), cada uno completo o corto. validar: los modelos con algún
    índice «no interpretable» salen de la norma.

    Devuelve {"rasgos_v3", "panel", "formas", "fuera_cobertura", "validez",
    "no_interpretables"}."""
    import analizar_h_confirmacion as ahc
    import analizar_n_confirmacion as anc
    import validez_personalidad as vp
    rasgos_v3 = RASGOS_V3 + (("H",) if h_modo == "v3" else ()) + (("N",) if n_modo == "v3" else ())
    v = cargar_v3(rutas, rasgos=rasgos_v3)
    corta = corta or {}
    i1 = {}
    if h_modo == "i1":
        i1["H"] = (ahc.ITEMS, ahc.cargar)
    if n_modo == "i1":
        i1["N"] = (anc.ITEMS_A, anc.cargar_a)
    formas, fuera = {}, {}
    for m in sorted(v["elecciones"]):
        f, motivo = {}, []
        cubre = lambda its, el: sum(i in el for i in its) / len(its) if its else 0.0  # noqa: E731
        if m not in v["ms"]:
            for t in rasgos_v3:
                if t in corta and cubre(corta[t], v["elecciones"][m]) >= COBERTURA_MIN:
                    f[t] = "corta"
            if len(f) < len(rasgos_v3):
                cob = 100 * cubre([s["id"] for s in v["sel"]], v["elecciones"][m])
                motivo.append(f"{', '.join(rasgos_v3)} del v3 {cob:.0f} %"
                              + (" (sin la forma corta completa)" if corta else ""))
        for t, (items, carga) in i1.items():
            el = carga([m])["elecciones"][m]
            if cubre(items, el) >= COBERTURA_MIN:
                continue
            if t in corta and cubre(corta[t], el) >= COBERTURA_MIN:
                f[t] = "corta"
            else:
                motivo.append(f"I1-{t} {100 * cubre(items, el):.0f} %")
        if motivo:
            fuera[m] = ", ".join(motivo)
        else:
            formas[m] = f
    validez = {m: vp.evaluar(m) for m in formas}
    no_interp = {m: x for m, x in validez.items() if validar and not x["interpretable"]}
    panel = [m for m in formas if m not in no_interp]
    return {"rasgos_v3": rasgos_v3, "panel": panel, "formas": {m: formas[m] for m in panel if formas[m]},
            "fuera_cobertura": fuera, "validez": validez, "no_interpretables": no_interp}


def sustituir_rasgo(v, t, h):
    """Cambia las situaciones del rasgo t del v3 por las de otra escala (H en
    §36-37, N en §39-40).

    h: {"items": [...], "faceta_de": {item: faceta}, "elecciones": {m: {item:
    [(orden, rep, elige_alto)]}}, "des": {m: {item: D}}} con los mismos modelos
    que v["ms"]. h["extra"] (opcional, §41.1): situaciones de la forma corta
    que no están en la escala; se cargan sus elecciones, pero no entran en
    el rasgo de los modelos completos. Un modelo sin dato en una situación
    (forma corta) se queda sin ella. Devuelve los ids nuevos."""
    viejos = set(v["por_rasgo"][t])
    its = list(h["items"])
    extra = [i for i in h.get("extra", ()) if i not in set(its)]
    for m in v["ms"]:
        el = {i: x for i, x in v["elecciones"][m].items() if i not in viejos}
        hm = h["elecciones"].get(m, {})
        el.update({i: hm[i] for i in its + extra if i in hm})
        v["elecciones"][m] = el
    for i in its + extra:
        v["rasgo_de"][i] = t
        v["faceta_de"][i] = h["faceta_de"][i]
    v["comunes"] = [i for i in v["comunes"] if i not in viejos] + its
    v["por_rasgo"][t] = its
    v["facetas"] = sorted({(v["rasgo_de"][i], v["faceta_de"][i]) for i in v["comunes"]})
    return set(its)


def sustituir_h(v, h):
    return sustituir_rasgo(v, "H", h)


def calcular(rutas_sel, escalas=None, h=None, n=None, n_con_marca=False, p3_n=None, r4_n=None,
             panel=None, formas=None, corta=None, revalidar=False, rasgos_v3=None):
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
    coincide pasa a frágil. Los modelos que no están en r4_n (forma corta de
    N: no seleccionaron la escala) no pasan R4.

    §41 (todo opcional; sin estos argumentos, el cálculo es el de §40):
    panel: modelos que entran (cobertura y validez ya decididas, panel_publico).
    formas: {modelo: {rasgo: "corta"}} de los modelos con forma corta (§41.1).
    corta: {rasgo: [situaciones de la forma corta]}.
    revalidar: un rasgo con marca que no pasa G4 (a), G4 (b) ≥ 0,70 o G3
    pierde sus marcas (§41.3).
    rasgos_v3: rasgos que se cargan del banco v3 (cobertura incluida)."""
    rng = np.random.default_rng(SEMILLA)
    v = cargar_v3(rutas_sel) if rasgos_v3 is None else cargar_v3(rutas_sel, rasgos=rasgos_v3)
    formas = formas or {}
    corta = corta or {}
    forma = lambda m, t: formas.get(m, {}).get(t, "completa")  # noqa: E731
    if panel is not None:
        # §41: el panel lo decide panel_publico (cobertura por forma y validez). Las
        # situaciones comunes se recalculan con los modelos completos del panel.
        ms_p = sorted(panel)
        completos_v3 = [m for m in ms_p if all(forma(m, t) == "completa" for t in v["por_rasgo"]
                                               if v["por_rasgo"][t])]
        v["ms"] = ms_p
        v["comunes"] = [s["id"] for s in v["sel"]
                        if all(s["id"] in v["elecciones"][m] for m in completos_v3)]
        v["por_rasgo"] = {t: [i for i in v["comunes"] if v["rasgo_de"][i] == t] for t in RASGOS}
        v["facetas"] = sorted({(v["rasgo_de"][i], v["faceta_de"][i]) for i in v["comunes"]})
        v["excluidos"] = {m: c for m, c in v["excluidos"].items() if m not in panel}
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
    hay_cortos = any(forma(m, t) == "corta" for m in ms for t in RASGOS)
    completos = [m for m in ms if all(forma(m, t) == "completa" for t in RASGOS)]

    def items_de(m, t, x=None):
        """Situaciones con las que se compara y puntúa m en t (§41.1)."""
        if forma(m, t) == "completa":
            return por_rasgo[t]
        x = el if x is None else x
        return [i for i in corta.get(t, ()) if i in x[m]]

    def dif(x, m, otros_m, t):
        """Diferencia pareada de m en t frente a la media de otros_m con dato.
        Los otros completos en t deben tener todos dato (regla de siempre de
        marcas_variante); los cortos cuentan donde tienen dato. Sin modelos
        cortos es exactamente dif_pareada sobre las situaciones con dato en
        todos."""
        oc = [o for o in otros_m if forma(o, t) == "completa"]
        ok = [o for o in otros_m if forma(o, t) != "completa"]
        its, ds = [], []
        for i in items_de(m, t, x):
            if i not in x[m] or not all(i in x[o] for o in oc):
                continue
            vals = [x[o][i] for o in oc] + [x[o][i] for o in ok if i in x[o]]
            if vals:
                its.append(i)
                ds.append(50 * (x[m][i] - np.mean(vals)))
        return its, ds

    def marcas(x, otros_de=None):
        """marcas_variante con dif (§41.1); idéntica sin modelos cortos."""
        if not hay_cortos:
            return marcas_variante(x, ms, por_rasgo, rng, otros_de)
        out = {}
        for m in ms:
            otros_m = otros_de(m) if otros_de else [o for o in ms if o != m]
            for t in RASGOS:
                dp, lo, hi = _boot(dif(x, m, otros_m, t)[1], rng)
                out[(m, t)] = (signo(lo, hi), dp, lo, hi)
        return out

    # Elección bruta (comparación) y elección frente a la deseabilidad común (puntuación)
    a = {m: puntuar(el[m]) for m in ms}
    # Situaciones cortas que no están en el banco común (p. ej. una situación corta de
    # N que la reselección de la escala dejó fuera): cuentan para los modelos cortos
    cortos_t = [t for t in RASGOS if any(forma(m, t) == "corta" for m in ms)]
    extra = sorted({i for t in cortos_t for i in corta.get(t, ())} - set(comunes))
    v3_viejos = [i for i in comunes if i not in nuevos_h | nuevos_n]
    if hay_cortos:
        d_bar = {i: float(np.mean([des[m][i] for m in ms if i in des.get(m, {})]))
                 for i in v3_viejos + [i for i in extra if i in v["rasgo_de"]]}
    else:
        d_bar = d_consenso(des, ms, v3_viejos)
    for nuevos, esc in ((nuevos_h, h), (nuevos_n, n)):
        if not esc:
            continue
        for i in sorted(nuevos) + [i for i in extra if i in esc.get("faceta_de", {})]:
            vals = [esc["des"][m][i] for m in ms if i in esc["des"].get(m, {})]
            if vals:
                d_bar[i] = float(np.mean(vals))
    a_d = {m: puntuar({i: el[m][i] for i in list(comunes) + extra if i in el[m] and i in d_bar},
                      d_bar) for m in ms}
    # Equiparación de la forma corta con los modelos completos (§41.1 y §42): lineal
    # por defecto (media y desviación típica entre modelos), o solo la media
    equip = {}
    for t in cortos_t:
        cc = [i for i in corta.get(t, ()) if all(i in a_d[o] for o in completos)]
        if not (cc and completos):
            equip[t] = {"media_completa": 0.0, "media_corta": 0.0, "razon_sd": 1.0}
            continue
        sf = np.array([np.mean([a_d[o][i] for i in por_rasgo[t]]) for o in completos])
        sc = np.array([np.mean([a_d[o][i] for i in cc]) for o in completos])
        razon = float(sf.std() / sc.std()) if EQUIPARACION == "lineal" and sc.std() > 0 else 1.0
        equip[t] = {"media_completa": float(sf.mean()), "media_corta": float(sc.mean()), "razon_sd": razon}

    def equiparar(t, x):
        e = equip[t]
        return e["media_completa"] + (x - e["media_corta"]) * e["razon_sd"]

    punt = {}
    for m in ms:
        for t in RASGOS:
            p, lo, hi = _boot([a_d[m][i] for i in items_de(m, t, a_d)], rng)
            if forma(m, t) == "corta":
                p, lo, hi = equiparar(t, p), equiparar(t, lo), equiparar(t, hi)
            punt[(m, t)] = (50 + 50 * p, 50 + 50 * lo, 50 + 50 * hi)
    base = marcas(a)

    # P2, P3: variantes de réplica y orden, con la elección bruta
    var = {k: marcas({m: puntuar(el[m], None, f) for m in ms}) for k, f in FILTROS.items()}
    # P5: sin cada laboratorio
    labs = sorted({laboratorio(m) for m in ms})
    var_lab = {L: marcas(a, lambda m, L=L: [o for o in ms if o != m and laboratorio(o) != L])
               for L in labs}
    # P6: p por bootstrap y BH sobre todas las pruebas del cuadro
    pruebas = [(m, t) for m in ms for t in RASGOS]
    pval = {k: _ic_p(dif(a, k[0], otros[k[0]], k[1])[1] if hay_cortos
                     else dif_pareada(a, k[0], otros[k[0]], por_rasgo[k[1]]), rng, B_FDR)[3]
            for k in pruebas}
    q_todas = dict(zip(pruebas, bh([pval[k] for k in pruebas])))
    sin_n = [k for k in pruebas if k[1] != "N"]
    q_sin_n = dict(zip(sin_n, bh([pval[k] for k in sin_n])))
    # P1: mitades por faceta
    candidatas = [k for k in pruebas if base[k][0]]
    parts = {t: particiones(por_rasgo[t], v["faceta_de"], rng) for t in RASGOS}
    p1 = {}
    for (m, t) in candidatas:
        if forma(m, t) == "corta":
            its, ds = dif(a, m, otros[m], t)
            p1[(m, t)] = mitades(dict(zip(its, ds)), particiones(its, v["faceta_de"], rng),
                                 base[(m, t)][0], rng)
            continue
        d = dict(zip(por_rasgo[t], dif_pareada(a, m, otros[m], por_rasgo[t]))) if not hay_cortos \
            else dict(zip(*dif(a, m, otros[m], t)))
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
            if r4_n is not None and nivel == "robusta" and m in r4_n and r4_n[m] != s0:
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

    # Validez con la definición de §28: G3 y G4 de §21 sobre e − d̄ (d̄ es común a
    # todos los modelos, así que da lo mismo que sobre la elección bruta). Con
    # modelos de forma corta, sobre los completos (la matriz debe estar llena).
    fac = facetas_score(a_d, completos, comunes, v["rasgo_de"], v["faceta_de"], v["facetas"])
    validez = {"G3": g3_estructura(fac, v["facetas"]), "G4": g4_consistencia(a_d, completos, por_rasgo)}
    revalidacion = revalidar_rasgos(a_d, completos, por_rasgo, v["faceta_de"], validez) if revalidar else None
    revalidacion_corta = None
    if revalidar and hay_cortos:
        # §41.3: con modelos cortos en el panel, también en la forma corta con todos
        pc = {t: [i for i in corta.get(t, por_rasgo[t]) if all(i in a_d[m] for m in ms)] for t in RASGOS}
        com_c = [i for t in RASGOS for i in pc[t]]
        fac_c = sorted({(v["rasgo_de"][i], v["faceta_de"][i]) for i in com_c})
        val_c = {"G3": g3_estructura(facetas_score(a_d, ms, com_c, v["rasgo_de"], v["faceta_de"], fac_c), fac_c),
                 "G4": g4_consistencia(a_d, ms, pc)}
        revalidacion_corta = revalidar_rasgos(a_d, ms, pc, v["faceta_de"], val_c)
    suspendidos = {}
    for rv, cual in ((revalidacion, "banco completo"), (revalidacion_corta, "forma corta")):
        for t, x in (rv or {}).items():
            if t in con_marca and not x["pasa"]:
                suspendidos.setdefault(t, []).append(f"{cual}: {x['motivo']}")

    def publicable(m, t):
        f = filas.get((m, t))
        if t == "N" and not n_con_marca:
            return ""
        if t in suspendidos:  # §41.3: rasgo en revisión, sin marcas
            return ""
        return f["marca"] if f and f["nivel"] == "robusta" else ""

    retratos = {}
    for m in ms:
        partes = [frase(t, publicable(m, t)) for t in con_marca if publicable(m, t)]
        retratos[m] = {"frase": "; ".join(partes) if partes else "perfil próximo al de los demás modelos",
                       "fragiles": [f"{t}{filas[(m, t)]['marca']}" for t in RASGOS
                                    if (m, t) in filas and filas[(m, t)]["nivel"] == "frágil"]}
    conflictos = []
    for t in RASGOS:
        g = validez["G4"][t]
        if revalidar and t in con_marca:
            continue  # §41.3: un rasgo con marca bajo el listón ya no es conflicto: se suspende
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
            "publicable_g4": publicable_g4, "retratos_g4": retratos_g4, "con_marca": con_marca,
            "revalidacion": revalidacion, "revalidacion_corta": revalidacion_corta,
            "suspendidos": suspendidos, "formas": {m: dict(formas.get(m, {})) for m in ms},
            "equiparacion": equip, "a_d": a_d, "a": a}


def revalidar_rasgos(a_d, ms, por_rasgo, faceta_de, validez):
    """§41.3: G4 (a) pares/impares (el del cuadro), G4 (b) mediana de 200
    particiones al azar equilibradas por faceta y G3, por rasgo. Generador
    propio con SEMILLA, para no mover el bootstrap del cuadro."""
    from rescate_hn_v3 import g4_ab  # import tardío: ese módulo importa este
    rng = np.random.default_rng(SEMILLA)
    out = {}
    for t in RASGOS:
        its = list(por_rasgo[t])
        X = np.array([[a_d[m][i] for i in its] for m in ms], float)
        g4a = validez["G4"][t]
        g4b = g4_ab(X, list(range(len(its))), [faceta_de[i] for i in its], rng)[1] if len(its) >= 4 else None
        d3, f3 = validez["G3"][t]
        fallos = []
        if g4a is None or not g4a >= G4_MIN:
            fallos.append(f"G4 (a) = {_f2(g4a)} < 0,70")
        if g4b is None or not g4b >= G4_MIN:
            fallos.append(f"G4 (b) = {_f2(g4b)} < 0,70")
        if d3 is None or f3 is None or not d3 > f3:
            fallos.append(f"G3 dentro {_f2(d3)} ≤ fuera {_f2(f3)}")
        out[t] = {"G4a": g4a, "G4b": g4b, "G3_dentro": d3, "G3_fuera": f3, "n_items": len(its),
                  "pasa": not fallos, "motivo": "; ".join(fallos)}
    return out


def _f2(x):
    return "—" if x is None or not np.isfinite(x) else f"{x:.2f}".replace(".", ",")


def escribir(r, rutas_sel):
    v, ms, labs, punt, base, filas = r["v"], r["ms"], r["labs"], r["punt"], r["base"], r["filas"]
    publicable, retratos = r["publicable"], r["retratos"]
    iss = iss_por_modelo()
    cnt = {n: sum(f["nivel"] == n for f in filas.values()) for n in ("robusta", "frágil", "no publicable")}
    sels = [pathlib.Path(p).name for p in rutas_sel]
    ok = lambda b: "✔" if b else "✘"  # noqa: E731
    n_marca = "N" in r.get("con_marca", CON_MARCA)
    pp = r.get("panel_publico")
    susp = r.get("suspendidos") or {}
    formas = r.get("formas") or {}
    val_m = (pp or {}).get("validez", {})
    no_int = (pp or {}).get("no_interpretables", {})

    def etiqueta(m):
        """Nombre del modelo con su forma (§41.1) y el aviso de validez (§41.2)."""
        cortos = [t for t in RASGOS if formas.get(m, {}).get(t) == "corta"]
        aviso = val_m.get(m, {}).get("nivel") == "aviso"
        return _id(m) + (f" (forma corta: {', '.join(cortos)})" if cortos else "") + (" ⚠" if aviso else "")

    if pp:
        fuera_txt = (f"Fuera por cobertura (§41.1: O, C, E y A del v3, completos o en forma corta;"
                     f" H y N de I1): {', '.join(f'{_id(m)} ({x})' for m, x in pp['fuera_cobertura'].items()) or 'ninguno'}.")
        if no_int:
            fuera_txt += (" **Fuera de la norma por validez (§41.2, perfil no interpretable):** "
                          + ", ".join(f"{_id(m)} ({x['motivo']})" for m, x in no_int.items()) + ".")
    else:
        fuera_txt = (f"Fuera por banco incompleto (< 95 %): "
                     f"{', '.join(f'{_id(m)} ({100 * c:.0f} %)' for m, c in v['excluidos'].items()) or 'ninguno'}.")
    L = ["# Cuadro público de personalidad · conducta comparada (PERSONALIDAD.md §28)", "",
         f"Generado por `cuadro_publico_v3.py`. Selección: {', '.join(sels)}. {len(ms)} modelos,"
         f" {len(labs)} laboratorios ({', '.join(labs)}); situaciones por rasgo: "
         + ", ".join(f"{t} {len(x)}" for t, x in v["por_rasgo"].items())
         + f". Semilla {SEMILLA}. Sin llamadas a modelos."
         + (f" Escala de Honestidad-Humildad: {r['escala_h']}." if r.get("escala_h") else "")
         + (f" Escala de Neuroticismo: {r['escala_n']}." if r.get("escala_n") else ""),
         fuera_txt, "",
         "**Puntuación** = 50 + 50·media(elige el polo alto − deseabilidad media del panel):"
         " 50 = elige lo que el conjunto de modelos juzga admirable. **▲/▼** = elige el polo alto"
         " más/menos a menudo que los demás modelos en las mismas situaciones (comparación pareada,"
         f" IC 95 %), solo si la marca es **robusta** ({ETIQUETA})."
         + (" Neuroticismo con marca desde §40 (sus marcas pasan además R4 de §30.2)." if n_marca
            else " Neuroticismo solo descriptivo, sin marca."), "",
         "| modelo | ISS | " + " | ".join(NOMBRE[t] + (" ‡" if t == "N" and not n_marca else "")
                                          + (" (en revisión)" if t in susp else "")
                                          for t in RASGOS) + " |",
         "|---|---|" + "---|" * len(RASGOS)]
    for m in ms:
        L.append(f"| {etiqueta(m)} | {iss.get(_id(m), '—')} | " + " | ".join(
            f"{punt[(m, t)][0]:.0f} {publicable(m, t)}".strip() for t in RASGOS) + " |")
    val, conf = r["validez"], r["conflictos"]
    L += ["", "‡ solo descriptivo (§23)." if not n_marca else f"Neuroticismo: {r.get('nota_n', '')}"]
    if any(formas.get(m) for m in ms):
        L += ["", f"Forma corta (§41.1, §42): puntuación en sus situaciones con equiparación {EQUIPARACION}"
              " a la escala completa con los modelos completos ("
              + ", ".join(f"{t}: desplazamiento {50 * (e['media_completa'] - e['media_corta']):+.1f},"
                          f" razón de sd {e['razon_sd']:.2f}".replace(".", ",")
                          for t, e in r.get("equiparacion", {}).items())
              + "); la marca compara frente a los demás modelos en esas mismas situaciones."]
    if val_m and any(x["nivel"] == "aviso" for m, x in val_m.items() if m in ms):
        L += ["", "⚠ Interpretar con cautela: algún índice de validez en la zona de aviso (§41.2; ver"
              " «Validez por modelo»)."]
    rv = r.get("revalidacion")
    L += ["", "## Validez con la definición de §28 (G3 y G4 de §21)", "",
          "Mismos cálculos que `analizar_v3.py` (G3: r media entre facetas del mismo rasgo frente a"
          " facetas de otros rasgos; G4: Spearman-Brown de mitades pares/impares entre modelos), pero"
          " sobre la puntuación de §28 en vez de la ajustada por la deseabilidad propia."
          + (" G4 (b): mediana de Spearman-Brown en 200 particiones al azar equilibradas por faceta."
             " Revalidación automática (§41.3): un rasgo con marca que no pasa G4 (a), G4 (b) ≥ 0,70 y"
             " G3 pierde sus marcas." if rv else ""), ""]
    if rv:
        L += ["| rasgo | G3 dentro / fuera | G3 | G4 (a) | G4 (b) | listón §41.3 | en §28 |",
              "|---|---|---|---|---|---|---|"]
    else:
        L += ["| rasgo | G3 dentro / fuera | G3 | G4 | G4 ≥ 0,70 | en §28 |", "|---|---|---|---|---|---|"]
    for t in RASGOS:
        d3, f3 = val["G3"][t]
        g4 = val["G4"][t]
        papel = "con marca" if t in r.get("con_marca", CON_MARCA) else "solo descriptivo"
        if t in susp:
            papel = "**en revisión: sin marcas**"
        if rv:
            L.append(f"| {NOMBRE[t]} | {d3:+.2f} / {f3:+.2f} | {ok(d3 > f3)} | {g4:.2f} | {_f2(rv[t]['G4b'])}"
                     f" | {ok(rv[t]['pasa'])} | {papel} |")
        else:
            L.append(f"| {NOMBRE[t]} | {d3:+.2f} / {f3:+.2f} | {ok(d3 > f3)} | {g4:.2f} | {ok(g4 >= G4_MIN)} | {papel} |")
    L += [""]
    rvc = r.get("revalidacion_corta")
    if rvc:
        L += ["En la forma corta, con todos los modelos del panel (§41.3):", "",
              "| rasgo | situaciones | G3 dentro / fuera | G4 (a) | G4 (b) | listón |", "|---|---|---|---|---|---|"]
        for t in RASGOS:
            x = rvc[t]
            L.append(f"| {NOMBRE[t]} | {x['n_items']} | {_f2(x['G3_dentro'])} / {_f2(x['G3_fuera'])} |"
                     f" {_f2(x['G4a'])} | {_f2(x['G4b'])} | {ok(x['pasa'])} |")
        L += [""]
    if rv is not None:
        if susp:
            L += ["**Rasgos en revisión (§41.3), sin marcas hasta que una sección lo corrija:**", ""]
            L += [f"- **{NOMBRE[t]}**: {'; '.join(x)}." for t, x in susp.items()] + [""]
        else:
            L += ["Revalidación automática (§41.3): todos los rasgos con marca pasan el listón.", ""]
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
    elif rv is None:
        L += ["Sin conflictos: los rasgos con marca tienen G4 ≥ 0,70 y los demás, por debajo.", ""]
    if val_m:
        from validez_personalidad import NOMBRE_INDICE, UMBRALES, _fmt
        L += ["## Validez por modelo (§41.2)", "",
              "Índices calculados sobre todas las respuestas del modelo en los instrumentos del cuadro (R3"
              " del v3 en O, C, E y A; binario de I1-H e I1-N; deseabilidad). Umbrales fijados antes de"
              " calcular: " + "; ".join(f"{NOMBRE_INDICE[k]} aviso/no interpretable a partir de "
                                        f"{_fmt(k, a)}/{_fmt(k, b)}" for k, (a, b) in UMBRALES.items())
              + ". Un perfil **no interpretable** sale de la norma: no entra en la media de los demás, ni"
              " en d̄, ni en la selección de N, ni en BH, y no lleva puntuaciones, marcas ni retrato.", "",
              "| modelo | Δ AB−BA | fracción de A | no válidas | retest | coherencia deseabilidad | nivel |",
              "|---|---|---|---|---|---|---|"]
        for m, x in val_m.items():
            vv, dd = x["valores"], x["detalle"]
            celda = lambda k, s: f"{s}{' ⚠' if x['niveles'][k] == 'aviso' else ' ✘' if x['niveles'][k] == 'no interpretable' else ''}"  # noqa: E731
            L.append(f"| {_id(m)} | {celda('V1_delta', _f2(dd['delta_con_signo']))}"
                     f" | {celda('V1_frac_A', _f2(dd['frac_A']))}"
                     f" | {celda('V2_no_validas', _fmt('V2_no_validas', vv['V2_no_validas']))}"
                     f" | {celda('V3_retest', _f2(vv['V3_retest']))}"
                     f" | {celda('V4_coherencia', _f2(vv['V4_coherencia']))} | **{x['nivel']}** |")
        L += ["", "⚠ = zona de aviso · ✘ = no interpretable.", ""]
        if no_int:
            L += ["### Perfiles no interpretables", "",
                  "Su perfil no se lee como retrato: el cuadro no publica puntuaciones ni marcas suyas.", "",
                  "| modelo | motivo |", "|---|---|"]
            L += [f"| {_id(m)} | {x['motivo']} |" for m, x in no_int.items()] + [""]
    L += ["## Retrato de cada modelo (§28)", ""]
    for m in ms:
        rr = retratos[m]
        aviso = val_m.get(m, {}).get("nivel") == "aviso"
        L.append(f"- **{etiqueta(m)}**: "
                 + (f"*interpretar con cautela ({val_m[m]['motivo']})*: " if aviso else "")
                 + f"{rr['frase']}."
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
        extra_m = {}
        if pp:
            vm = val_m.get(m, {})
            extra_m = {"forma": {t: formas.get(m, {}).get(t, "completa") for t in RASGOS},
                       "interpretable": True, "validez": vm.get("nivel"),
                       "aviso_validez": vm.get("motivo") if vm.get("nivel") == "aviso" else None}
        modelos.append({"id": m, "modelo": _id(m), "laboratorio": laboratorio(m),
                        "iss": iss.get(_id(m)), "rasgos": rasgos,
                        "frase": retratos[m]["frase"].replace("**", ""),
                        "frase_md": retratos[m]["frase"], "fragiles": retratos[m]["fragiles"], **extra_m})
    extra = {}
    if pp:
        extra = {"validez_modelos": {"criterio": "PERSONALIDAD.md §41.2", "modelos": val_m},
                 "no_interpretables": [{"id": m, "modelo": _id(m), "interpretable": False,
                                        "motivo": x["motivo"], "valores": x["valores"]}
                                       for m, x in no_int.items()],
                 "fuera_por_cobertura_41": pp["fuera_cobertura"],
                 "revalidacion": {"criterio": "PERSONALIDAD.md §41.3", "banco_completo": r.get("revalidacion"),
                                  "forma_corta": r.get("revalidacion_corta"), "en_revision": susp},
                 "forma_corta": {"fichero": FORMA_CORTA.name if r.get("forma_corta") else None,
                                 "equiparacion": r.get("equiparacion")}}
    (SALIDA / "cuadro_publico.json").write_text(json.dumps({
        "definicion": "PERSONALIDAD.md §28: conducta comparada",
        "generado_por": "spike/cuadro_publico_v3.py", "semilla": SEMILLA, "seleccion": sels,
        "n_situaciones": {t: len(x) for t, x in v["por_rasgo"].items()},
        "escala_H": r.get("escala_h"),
        "fuera_por_cobertura": v["excluidos"], "laboratorios": labs,
        "comprobaciones": list(PRUEBAS), "n_pruebas_bh": r["n_pruebas"],
        "rasgos": {t: {"nombre": NOMBRE[t], "polo_alto": POLOS[t][0], "polo_bajo": POLOS[t][1],
                       "con_marca": t in r.get("con_marca", CON_MARCA),
                       "aviso": "solo descriptivo (§23)" if t not in r.get("con_marca", CON_MARCA) else None,
                       **({"en_revision": t in susp} if pp else {})}
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
        "marcas_candidatas": {f"{m}|{t}": f for (m, t), f in filas.items()}, **extra},
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
    ap.add_argument("--sin-validez", action="store_true",
                    help="no aplica los índices de validez por modelo (§41.2): todos los que pasan la"
                         " cobertura entran en la norma (solo para comparar con el cuadro de §40)")
    ap.add_argument("--sin-revalidar", action="store_true",
                    help="no suspende las marcas de un rasgo bajo el listón de G4/G3 (§41.3);"
                         " solo para comparar")
    args = ap.parse_args(argv)
    rutas = args.seleccion or selecciones_por_defecto()
    corta = cargar_forma_corta()
    pp = panel_publico(rutas, args.h, args.n, corta, validar=not args.sin_validez)
    panel, formas = pp["panel"], pp["formas"]
    h = None
    if args.h == "i1":
        import analizar_h_confirmacion as ahc  # import tardío: ese módulo importa este
        h = ahc.h_para_cuadro(rutas_sel=rutas, ms=panel)
    comun = dict(panel=panel, formas=formas, corta=corta, revalidar=not args.sin_revalidar,
                 rasgos_v3=pp["rasgos_v3"])
    if args.n == "i1":
        import analizar_n_confirmacion as anc  # import tardío: ese módulo importa este
        # La escala de N la seleccionan los modelos con las 72 (§40-41.1)
        completos_n = [m for m in panel if formas.get(m, {}).get("N") != "corta"]
        n = anc.n_para_cuadro(rutas_sel=rutas, ms=completos_n, ms_datos=panel)
        if corta and any(f.get("N") == "corta" for f in formas.values()):
            n["extra"] = [i for i in corta.get("N", ()) if i not in n["items"]]
        r = calcular(rutas, h=h, n=n, n_con_marca=True, r4_n=n["r4"], **comun)
        r["escala_n"], r["nota_n"] = n["descripcion"], n["nota"]
    else:
        r = calcular(rutas, h=h, **comun)
    r["escala_h"] = ESCALA_H[args.h]
    r["panel_publico"] = pp
    r["forma_corta"] = corta
    print("\n".join(escribir(r, rutas)))


if __name__ == "__main__":
    main()
