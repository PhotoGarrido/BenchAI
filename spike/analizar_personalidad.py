"""Análisis del piloto P0 de personalidad en tres registros.

Lee resultados/personalidad_p0/<modelo>/registros.jsonl y escribe
resumen.json y INFORME.md en la misma carpeta raíz. Sin red ni juez LLM:
todo sale de los registros parseados por reglas.

Qué calcula, por modelo y rasgo (escala 0-100, IC 95 % por bootstrap de
ítems — el ítem es la unidad de remuestreo, B=2000, semilla fija):
  R1  auto           autoinforme propio (bruto y corregido por aquiescencia)
  R2  sit_personaje  % de elecciones del polo alto, protagonista neutro
  R3  sit_propia     ídem, «¿qué harías tú?»
  Δ escaparate = R1 − R3    Δ yo/personaje = R3 − R2
  elasticidad    sit_persona(alto) − sit_persona(bajo)   [conducta]
                 auto_persona(alto) − auto_persona(bajo) [declarada]
y los indicadores de validez que deciden si el número significa algo:
  aquiescencia, sesgo de orden de escala, contradicción directo/inverso,
  sesgo de posición A/B, consistencia de polo entre órdenes, test-retest,
  confusión con deseabilidad, negación de identidad, reconocimiento.

Uso: python analizar_personalidad.py [--dir resultados/personalidad_p0]
"""

import argparse
import json
import pathlib
import re
from collections import defaultdict

import numpy as np

import personalidad_items as it

B = 2000
SEMILLA = 20261010
RE_RECONOCE = re.compile(r"personalidad|big\s*five|cinco\s+grandes|rasgos?\b|"
                         r"ocean\b|hexaco|psicom|test\s+de\s+personalidad", re.I)


def cargar(base):
    datos = {}
    for d in sorted(pathlib.Path(base).iterdir()):
        f = d / "registros.jsonl"
        if d.is_dir() and f.exists():
            filas = [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines()]
            # Reanudaciones: la última línea de cada id manda.
            ultimo = {r["id"]: r for r in filas}
            datos[d.name] = list(ultimo.values())
    return datos


def _boot_items(por_item, rng):
    """Media de medias por ítem + IC percentil remuestreando ítems."""
    medias = np.array([np.mean(v) for v in por_item.values() if v])
    if len(medias) == 0:
        return None, None, None
    idx = rng.integers(0, len(medias), size=(B, len(medias)))
    boots = medias[idx].mean(axis=1)
    return (float(medias.mean() * 100), float(np.percentile(boots, 2.5) * 100),
            float(np.percentile(boots, 97.5) * 100))


def _por_item(filas, campo="puntos"):
    d = defaultdict(list)
    for r in filas:
        if r.get(campo) is not None:
            d[r["item"]].append(float(r[campo]))
    return d


def _diferencia_items(a, b, rng):
    """Δ = media(a) − media(b) sobre los ítems presentes en ambos, IC por
    bootstrap pareado de ítems."""
    comunes = [k for k in a if k in b and a[k] and b[k]]
    if not comunes:
        return None, None, None
    d = np.array([np.mean(a[k]) - np.mean(b[k]) for k in comunes])
    idx = rng.integers(0, len(d), size=(B, len(d)))
    boots = d[idx].mean(axis=1)
    return (float(d.mean() * 100), float(np.percentile(boots, 2.5) * 100),
            float(np.percentile(boots, 97.5) * 100))


def analizar_modelo(filas):
    rng = np.random.default_rng(SEMILLA)
    por = defaultdict(list)
    for r in filas:
        por[r["brazo"]].append(r)
    out = {"n_registros": len(filas), "estados": {}, "rasgos": {}, "validez": {}}
    for brazo, rs in por.items():
        c = defaultdict(int)
        for r in rs:
            c[r["estado"]] += 1
        out["estados"][brazo] = dict(c)

    auto = [r for r in por["auto"] if r["estado"] == "OK"]
    # ── Aquiescencia y orden de escala (R1) ────────────────────────────────
    # Aquiescencia EQUILIBRADA: el IPIP-50 trae 37 ítems directos y 23
    # inversos (N: 8/2), así que el acuerdo medio bruto mezcla contenido y
    # sesgo. Dentro de cada rasgo se promedian por separado directos e
    # inversos; sin sesgo, (directos + inversos)/2 = 3.
    claves_ = {i[0]: (i[1], i[2]) for i in it.AUTOINFORME}
    mitades = []
    for rasgo_ in it.RASGOS:
        dir_ = [r["acuerdo"] for r in auto if claves_[r["item"]] == (rasgo_, 1)]
        inv_ = [r["acuerdo"] for r in auto if claves_[r["item"]] == (rasgo_, -1)]
        if dir_ and inv_:
            mitades.append((np.mean(dir_) + np.mean(inv_)) / 2 - 3)
    aq = float(np.mean(mitades)) if mitades else None
    asc = [r["acuerdo"] for r in auto if r["orden"] == "asc"]
    desc = [r["acuerdo"] for r in auto if r["orden"] == "desc"]
    num_asc = [r["valor"] for r in auto if r["orden"] == "asc"]
    num_desc = [r["valor"] for r in auto if r["orden"] == "desc"]
    out["validez"]["aquiescencia"] = aq   # >0: tiende a «de acuerdo»
    out["validez"]["sesgo_orden_escala"] = (float(np.mean(asc) - np.mean(desc))
                                           if asc and desc else None)
    # Correlación entre lo que dice con la escala al derecho y al revés (por
    # ítem): si es alta, responde al contenido; si es ~0, al número.
    pares = defaultdict(dict)
    for r in auto:
        pares[r["item"]].setdefault(r["orden"], []).append(r["acuerdo"])
    xs, ys = [], []
    for v in pares.values():
        if "asc" in v and "desc" in v:
            xs.append(np.mean(v["asc"]))
            ys.append(np.mean(v["desc"]))
    out["validez"]["r_ordenes_escala"] = (float(np.corrcoef(xs, ys)[0, 1])
                                         if len(xs) > 3 and np.std(xs) and np.std(ys)
                                         else None)
    out["validez"]["numero_medio_asc_desc"] = (
        [float(np.mean(num_asc)), float(np.mean(num_desc))] if num_asc and num_desc else None)
    # Test-retest: misma condición, réplica 0 vs 1.
    rep = defaultdict(dict)
    for r in auto:
        rep[(r["item"], r["orden"])][r["rep"]] = r["acuerdo"]
    iguales = [v[0] == v[1] for v in rep.values() if 0 in v and 1 in v]
    out["validez"]["retest_auto_identico"] = float(np.mean(iguales)) if iguales else None

    # ── R1 por rasgo, bruto y corregido ────────────────────────────────────
    acuerdo_item = defaultdict(list)
    for r in auto:
        acuerdo_item[r["item"]].append(r["acuerdo"])
    claves = {i[0]: i[2] for i in it.AUTOINFORME}
    for rasgo in it.RASGOS:
        items = [i[0] for i in it.AUTOINFORME if i[1] == rasgo]
        bruto = {k: [(a if claves[k] > 0 else 6 - a) - 1 for a in acuerdo_item[k]]
                 for k in items}
        bruto = {k: [x / 4 for x in v] for k, v in bruto.items()}
        # Corrección: se resta la aquiescencia al acuerdo antes de aplicar la
        # clave (Meyer et al. 2026: el sesgo direccional domina entre modelos).
        corr = {k: [min(max((((a - aq) if claves[k] > 0 else 6 - (a - aq)) - 1) / 4, 0), 1)
                    for a in acuerdo_item[k]] for k in items} if aq is not None else {}
        pos = [np.mean(acuerdo_item[k]) for k in items if claves[k] > 0 and acuerdo_item[k]]
        neg = [np.mean(acuerdo_item[k]) for k in items if claves[k] < 0 and acuerdo_item[k]]
        out["rasgos"][rasgo] = {
            "R1_auto": _boot_items(bruto, rng),
            "R1_auto_corregido": _boot_items(corr, rng) if corr else None,
            # contradicción: de acuerdo (≥4) a la vez con directos e inversos
            "contradiccion": (float(np.mean(pos) >= 3.5 and np.mean(neg) >= 3.5)
                              if pos and neg else None),
            "acuerdo_directos_inversos": ([float(np.mean(pos)), float(np.mean(neg))]
                                          if pos and neg else None),
        }

    # ── Situaciones ───────────────────────────────────────────────────────
    def ok(brazo, **filtro):
        return [r for r in por[brazo] if r["estado"] == "OK"
                and all(r.get(k) == v for k, v in filtro.items())]

    for brazo in ("sit_personaje", "sit_propia", "deseabilidad", "sit_persona"):
        rs = ok(brazo)
        if rs:
            out["validez"][f"pA_{brazo}"] = float(np.mean([r["valor"] == "A" for r in rs]))
    # Consistencia de polo: misma situación y réplica, orden AB vs BA.
    for brazo in ("sit_personaje", "sit_propia"):
        polo = defaultdict(dict)
        for r in ok(brazo):
            polo[(r["item"], r["rep"])][r["orden"]] = r["elige_alto"]
        cons = [v["AB"] == v["BA"] for v in polo.values() if "AB" in v and "BA" in v]
        out["validez"][f"consistencia_polo_{brazo}"] = float(np.mean(cons)) if cons else None
        rep = defaultdict(dict)
        for r in ok(brazo):
            rep[(r["item"], r["orden"])][r["rep"]] = r["elige_alto"]
        ig = [v[0] == v[1] for v in rep.values() if 0 in v and 1 in v]
        out["validez"][f"retest_{brazo}"] = float(np.mean(ig)) if ig else None

    deseab = _por_item(ok("deseabilidad"))
    r2_item = _por_item(ok("sit_personaje"))
    r3_item = _por_item(ok("sit_propia"))
    for nombre, d in (("R2", r2_item), ("R3", r3_item)):
        comunes = [k for k in d if k in deseab]
        a = [np.mean(d[k]) for k in comunes]
        b = [np.mean(deseab[k]) for k in comunes]
        out["validez"][f"r_deseabilidad_{nombre}"] = (
            float(np.corrcoef(a, b)[0, 1]) if len(a) > 3 and np.std(a) and np.std(b) else None)
        # Acuerdo ítem a ítem: ¿elige lo que él mismo juzga más deseable?
        coin = [(np.mean(d[k]) >= .5) == (np.mean(deseab[k]) >= .5) for k in comunes]
        out["validez"][f"elige_lo_deseable_{nombre}"] = float(np.mean(coin)) if coin else None

    for rasgo in it.RASGOS:
        sel = lambda d: {k: v for k, v in d.items() if k.startswith("S" + rasgo)}  # noqa: E731
        alto = sel(_por_item(ok("sit_persona", nivel="alto")))
        bajo = sel(_por_item(ok("sit_persona", nivel="bajo")))
        a_alto = {k: v for k, v in _por_item(ok("auto_persona", nivel="alto")).items()
                  if k.startswith(rasgo)}
        a_bajo = {k: v for k, v in _por_item(ok("auto_persona", nivel="bajo")).items()
                  if k.startswith(rasgo)}
        r2, r3 = sel(r2_item), sel(r3_item)
        g = out["rasgos"][rasgo]
        g["R2_personaje"] = _boot_items(r2, rng)
        g["R3_propia"] = _boot_items(r3, rng)
        g["deseabilidad_polo_alto"] = _boot_items(sel(deseab), rng)
        g["delta_yo_personaje"] = _diferencia_items(r3, r2, rng)
        g["elasticidad_conducta"] = _diferencia_items(alto, bajo, rng)
        g["elasticidad_declarada"] = _diferencia_items(a_alto, a_bajo, rng)
        # ¿Dónde cae el personaje neutro entre la persona baja (0) y la alta (1)?
        ma, mb, mn = (np.mean([np.mean(v) for v in d.values()]) if d else None
                      for d in (alto, bajo, r2))
        g["posicion_neutro"] = (float((mn - mb) / (ma - mb))
                                if None not in (ma, mb, mn) and abs(ma - mb) > .05 else None)
        r1 = g["R1_auto"][0] if g["R1_auto"] else None
        g["delta_escaparate"] = (r1 - g["R3_propia"][0]
                                 if r1 is not None and g["R3_propia"][0] is not None else None)

    # ── Negación de identidad y reconocimiento ─────────────────────────────
    total = defaultdict(int)
    niega = defaultdict(int)
    for r in filas:
        total[r["brazo"]] += 1
        niega[r["brazo"]] += r["estado"] == "NIEGA_IDENTIDAD"
    out["validez"]["niega_identidad"] = {b: niega[b] / total[b] for b in total if total[b]}
    sondas = [r for r in por["sonda"]]
    out["validez"]["reconoce_personalidad"] = {
        reg: [bool(RE_RECONOCE.search(r["raw"])) for r in sondas if r.get("registro") == reg]
        for reg in ("auto", "sit_personaje", "sit_propia")}
    out["sondas"] = {r["item"]: r["raw"] for r in sondas}
    return out


def _f(x, nd=0):
    return "—" if x is None else f"{x:.{nd}f}"


def _ic(t):
    if not t or t[0] is None:
        return "—"
    return f"{t[0]:.0f} [{t[1]:.0f}–{t[2]:.0f}]"


def informe(res):
    L = ["# Piloto P0 · Personalidad en tres registros", "",
         "Generado por `analizar_personalidad.py`. Escala 0-100; IC 95 % por"
         " bootstrap de ítems. R1 = autoinforme, R2 = personaje, R3 = «¿qué"
         " harías tú?».", ""]
    L += ["## Validez por modelo", "",
          "| modelo | aquiesc. | sesgo orden escala | r órdenes | retest R1 | P(A) R2 | polo AB=BA R2 | polo AB=BA R3 | r deseab. R2 | elige lo deseable R3 | niega id. R1 |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for m, r in res.items():
        v = r["validez"]
        L.append(f"| {m} | {_f(v.get('aquiescencia'), 2)} | {_f(v.get('sesgo_orden_escala'), 2)}"
                 f" | {_f(v.get('r_ordenes_escala'), 2)} | {_f(v.get('retest_auto_identico'), 2)}"
                 f" | {_f(v.get('pA_sit_personaje'), 2)} | {_f(v.get('consistencia_polo_sit_personaje'), 2)}"
                 f" | {_f(v.get('consistencia_polo_sit_propia'), 2)} | {_f(v.get('r_deseabilidad_R2'), 2)}"
                 f" | {_f(v.get('elige_lo_deseable_R3'), 2)} | {_f(v.get('niega_identidad', {}).get('auto'), 2)} |")
    for rasgo in it.RASGOS:
        L += ["", f"## {it.NOMBRES_RASGO[rasgo]} ({rasgo})", "",
              "| modelo | R1 auto | R1 corregido | R2 personaje | R3 propia | Δ escaparate (R1−R3) | Δ yo−personaje | elasticidad conducta | elasticidad declarada | deseab. polo alto |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for m, r in res.items():
            g = r["rasgos"][rasgo]
            L.append(f"| {m} | {_ic(g['R1_auto'])} | {_ic(g['R1_auto_corregido'])}"
                     f" | {_ic(g['R2_personaje'])} | {_ic(g['R3_propia'])}"
                     f" | {_f(g['delta_escaparate'])} | {_ic(g['delta_yo_personaje'])}"
                     f" | {_ic(g['elasticidad_conducta'])} | {_ic(g['elasticidad_declarada'])}"
                     f" | {_ic(g['deseabilidad_polo_alto'])} |")
    L += ["", "## Sondas de reconocimiento", ""]
    for m, r in res.items():
        for k, txt in sorted(r["sondas"].items()):
            L.append(f"- **{m}** · {k}: {txt.strip()[:200]}")
    return "\n".join(L) + "\n"


def _spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3 or np.std(a) == 0 or np.std(b) == 0:
        return None
    ra = np.argsort(np.argsort(a))
    rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def transversal(datos, res):
    """Lo que solo se ve mirando todos los modelos a la vez."""
    out = {"items": {}, "perfil": {}, "entre_modelos": {}, "contra_deseable": {}}
    modelos = list(datos)
    # ── Ítems: ¿discrimina la situación entre modelos? ─────────────────────
    medias = defaultdict(lambda: defaultdict(dict))   # item → brazo → modelo
    for m, filas in datos.items():
        for brazo in ("sit_personaje", "sit_propia", "deseabilidad"):
            for item, v in _por_item([r for r in filas if r["brazo"] == brazo
                                      and r["estado"] == "OK"]).items():
                medias[item][brazo][m] = float(np.mean(v))
    for item, b in sorted(medias.items()):
        r3 = list(b["sit_propia"].values())
        r2 = list(b["sit_personaje"].values())
        de = list(b["deseabilidad"].values())
        out["items"][item] = {
            "R2": float(np.mean(r2)) if r2 else None,
            "R3": float(np.mean(r3)) if r3 else None,
            "deseab": float(np.mean(de)) if de else None,
            # varianza entre modelos de la media del ítem (0 = todos igual)
            "sd_modelos_R3": float(np.std(r3)) if len(r3) > 1 else None,
            "sd_modelos_R2": float(np.std(r2)) if len(r2) > 1 else None,
        }
    # ── Elige contra lo que él mismo juzga deseable ────────────────────────
    # Solo ítems donde el propio modelo juzga claro qué es lo deseable (sus
    # dos órdenes coinciden). Elegir lo otro es la señal de rasgo que la
    # deseabilidad no explica.
    for m, filas in datos.items():
        des = _por_item([r for r in filas if r["brazo"] == "deseabilidad"
                         and r["estado"] == "OK"])
        claro = {k: np.mean(v) >= .5 for k, v in des.items()
                 if np.mean(v) in (0.0, 1.0)}
        fila = {}
        for brazo in ("sit_personaje", "sit_propia"):
            sel = [r for r in filas if r["brazo"] == brazo and r["estado"] == "OK"
                   and r["item"] in claro]
            fila[brazo] = {"n": len(sel), "contra": (float(np.mean(
                [r["elige_alto"] != claro[r["item"]] for r in sel])) if sel else None)}
            for rasgo in it.RASGOS:
                s = [r for r in sel if r["rasgo"] == rasgo]
                fila[f"{brazo}_{rasgo}"] = (float(np.mean(
                    [r["elige_alto"] != claro[r["item"]] for r in s])) if s else None)
        fila["items_claros"] = len(claro)
        out["contra_deseable"][m] = fila
    # Agregado: Δ = contra-deseable(R2) − contra-deseable(R3) por (modelo,
    # ítem), IC por bootstrap de ítems (todas las parejas de un ítem salen o
    # entran juntas). >0: el personaje elige contra lo deseable más que «tú».
    por_item = defaultdict(list)
    for m, filas in datos.items():
        des = _por_item([r for r in filas if r["brazo"] == "deseabilidad"
                         and r["estado"] == "OK"])
        claro = {k: np.mean(v) >= .5 for k, v in des.items() if np.mean(v) in (0.0, 1.0)}
        d2, d3 = defaultdict(list), defaultdict(list)
        for r in filas:
            if r["estado"] == "OK" and r["item"] in claro:
                x = r["elige_alto"] != claro[r["item"]]
                if r["brazo"] == "sit_personaje":
                    d2[r["item"]].append(x)
                elif r["brazo"] == "sit_propia":
                    d3[r["item"]].append(x)
        for k in claro:
            if d2[k] and d3[k]:
                por_item[k].append(np.mean(d2[k]) - np.mean(d3[k]))
    if por_item:
        rng = np.random.default_rng(SEMILLA)
        mi = np.array([np.mean(v) for v in por_item.values()])
        bs = mi[rng.integers(0, len(mi), size=(B, len(mi)))].mean(axis=1)
        todas = [x for v in por_item.values() for x in v]
        out["delta_yo_personaje_agregado"] = {
            "pp": float(np.mean(todas) * 100),
            "ic": [float(np.percentile(bs, 2.5) * 100), float(np.percentile(bs, 97.5) * 100)],
            "n_pares": len(todas), "n_items": len(mi),
            "frac_pares_pos": float(np.mean([x > 0 for x in todas])),
            "frac_pares_neg": float(np.mean([x < 0 for x in todas]))}
    # Reconocimiento por registro, todos los modelos juntos.
    out["reconoce"] = {}
    for reg in ("auto", "sit_personaje", "sit_propia"):
        v = [x for m in modelos for x in res[m]["validez"]["reconoce_personalidad"][reg]]
        out["reconoce"][reg] = [int(sum(v)), len(v)]
    # ── Forma del perfil: ¿R1 ordena los rasgos como R3? ───────────────────
    for m, r in res.items():
        g = r["rasgos"]
        v = {k: [g[t][k][0] if g[t][k] and g[t][k][0] is not None else np.nan
                 for t in it.RASGOS] for k in ("R1_auto_corregido", "R2_personaje",
                                               "R3_propia")}
        ok = lambda a, b: [i for i in range(len(a)) if not (np.isnan(a[i]) or np.isnan(b[i]))]  # noqa: E731
        par = lambda a, b: _spearman([a[i] for i in ok(a, b)], [b[i] for i in ok(a, b)])  # noqa: E731
        out["perfil"][m] = {"rho_R1_R3": par(v["R1_auto_corregido"], v["R3_propia"]),
                            "rho_R2_R3": par(v["R2_personaje"], v["R3_propia"]),
                            "rho_R1_R2": par(v["R1_auto_corregido"], v["R2_personaje"])}
    # ── Entre modelos, por rasgo ───────────────────────────────────────────
    aq = [res[m]["validez"]["aquiescencia"] for m in modelos]
    for t in it.RASGOS:
        fila = {}
        for k in ("R1_auto", "R1_auto_corregido", "R2_personaje", "R3_propia"):
            vals = [res[m]["rasgos"][t][k] for m in modelos]
            vals = [x for x in vals if x and x[0] is not None]
            if len(vals) > 1:
                puntos = [x[0] for x in vals]
                semi = np.mean([(x[2] - x[1]) / 2 for x in vals])
                # rango entre modelos / semiancho medio del IC: <2 = los
                # modelos no se distinguen en este rasgo y registro
                fila[k] = {"rango": float(max(puntos) - min(puntos)),
                           "semiancho_ic": float(semi),
                           "discrimina": float((max(puntos) - min(puntos)) / semi)
                           if semi else None}
        r1 = [res[m]["rasgos"][t]["R1_auto"][0] for m in modelos]
        r3 = [res[m]["rasgos"][t]["R3_propia"][0] for m in modelos]
        fila["r_aquiescencia_R1"] = (float(np.corrcoef(aq, r1)[0, 1])
                                     if None not in aq + r1 and np.std(r1) else None)
        fila["r_R1_R3_modelos"] = (float(np.corrcoef(r1, r3)[0, 1])
                                   if None not in r1 + r3 and np.std(r1) and np.std(r3)
                                   else None)
        out["entre_modelos"][t] = fila
    return out


def informe_transversal(tr):
    L = ["", "## Transversal: lo que solo se ve con todos los modelos", "",
         "### Forma del perfil (ρ de Spearman sobre los 6 rasgos)", "",
         "| modelo | ρ R1–R3 | ρ R2–R3 | ρ R1–R2 |", "|---|---|---|---|"]
    for m, p in tr["perfil"].items():
        L.append(f"| {m} | {_f(p['rho_R1_R3'], 2)} | {_f(p['rho_R2_R3'], 2)}"
                 f" | {_f(p['rho_R1_R2'], 2)} |")
    L += ["", "### ¿Distingue modelos cada rasgo y registro? (rango / semiancho del IC; <2 = no)",
          "", "| rasgo | R1 | R1 corr. | R2 | R3 | r(aquiesc., R1) | r(R1, R3) |",
          "|---|---|---|---|---|---|---|"]
    for t, f in tr["entre_modelos"].items():
        d = lambda k: _f(f.get(k, {}).get("discrimina"), 1) if f.get(k) else "—"  # noqa: E731
        L.append(f"| {t} | {d('R1_auto')} | {d('R1_auto_corregido')} | {d('R2_personaje')}"
                 f" | {d('R3_propia')} | {_f(f['r_aquiescencia_R1'], 2)}"
                 f" | {_f(f['r_R1_R3_modelos'], 2)} |")
    L += ["", "### Elige contra lo que él mismo juzga deseable (% de elecciones)", "",
          "| modelo | ítems claros | R2 | R3 | " + " | ".join(f"R3·{t}" for t in it.RASGOS) + " |",
          "|---|---|---|---|" + "---|" * len(it.RASGOS)]
    for m, c in tr["contra_deseable"].items():
        pc = lambda x: "—" if x is None else f"{100 * x:.0f}"  # noqa: E731
        L.append(f"| {m} | {c['items_claros']} | {pc(c['sit_personaje']['contra'])}"
                 f" | {pc(c['sit_propia']['contra'])} | "
                 + " | ".join(pc(c.get(f"sit_propia_{t}")) for t in it.RASGOS) + " |")
    ag = tr.get("delta_yo_personaje_agregado")
    if ag:
        L += ["", "### Yo frente a personaje, agregado", "",
              f"Contra lo deseable (personaje − tú): **{ag['pp']:+.1f} pp**"
              f" [IC 95 % {ag['ic'][0]:+.1f}, {ag['ic'][1]:+.1f}], {ag['n_pares']} pares"
              f" modelo×ítem de {ag['n_items']} ítems; {100 * ag['frac_pares_pos']:.0f} %"
              f" de pares > 0 y {100 * ag['frac_pares_neg']:.0f} % < 0."]
    L += ["", "### Reconocimiento (la sonda nombra personalidad/rasgos)", ""]
    L += [f"- {reg}: {k}/{n}" for reg, (k, n) in tr["reconoce"].items()]
    L += ["", "### Ítems sin varianza entre modelos (sd de la media del ítem en R3 = 0)", ""]
    planos = [(k, v) for k, v in tr["items"].items() if v["sd_modelos_R3"] == 0]
    L.append(f"{len(planos)} de {len(tr['items'])}: " + ", ".join(
        f"{k} ({100 * v['R3']:.0f})" for k, v in planos))
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", default="resultados/personalidad_p0")
    args = ap.parse_args()
    datos = cargar(args.dir)
    res = {m: analizar_modelo(f) for m, f in datos.items()}
    tr = transversal(datos, res)
    base = pathlib.Path(args.dir)
    (base / "resumen.json").write_text(json.dumps(
        {"modelos": res, "transversal": tr}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    texto = informe(res) + informe_transversal(tr)
    (base / "INFORME.md").write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
