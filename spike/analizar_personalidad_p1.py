"""Análisis del P1 de personalidad contra las hipótesis de PERSONALIDAD.md §8.

Las hipótesis y la puntuación ajustada se fijaron ANTES de ver los datos;
este script las implementa tal cual y añade los indicadores de validez del
P0. Lee resultados/personalidad_p1/<modelo>/registros.jsonl y la deseabilidad
por modelo de resultados/personalidad_p1_calibracion/<modelo>/registros.jsonl.
Escribe resumen.json e INFORME.md en resultados/personalidad_p1/.

Definiciones (§8):
  d_m(i)        p(polo alto juzgado deseable) del modelo m en el ítem i
                (media de sus dos juicios de calibración, órdenes AB y BA).
  ajustada      50 + 50 × media_i(elige_alto − d_m(i)); 50 = elegir lo que
                el propio modelo juzga deseable.
  contra        |elige_alto − d_m(i)| por elección: cuánto se aparta de lo
                que el modelo juzga deseable (H1 compara personaje frente a «tú»).

Uso: python analizar_personalidad_p1.py
"""

import json
import pathlib
from collections import defaultdict

import numpy as np

import personalidad_p1_items as p1
from analizar_personalidad import (B, RE_RECONOCE, SEMILLA, _boot_items,
                                   _diferencia_items, _f, _ic, cargar)

AQUI = pathlib.Path(__file__).parent
DIR = AQUI / "resultados" / "personalidad_p1"
CAL = AQUI / "resultados" / "personalidad_p1_calibracion"
RASGOS = p1.RASGOS


def deseabilidad():
    """{modelo: {item: d}} desde los registros de calibración."""
    out = {}
    for d in CAL.iterdir():
        f = d / "registros.jsonl"
        if not (d.is_dir() and f.exists()):
            continue
        acc = defaultdict(list)
        ultimo = {}
        for linea in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(linea)
            ultimo[r["id"]] = r
        for r in ultimo.values():
            if r["estado"] == "OK":
                acc[r["item"]].append(1.0 if r["alto_deseable"] else 0.0)
        out[d.name] = {k: float(np.mean(v)) for k, v in acc.items()}
    return out


def _por_item(filas, f):
    d = defaultdict(list)
    for r in filas:
        x = f(r)
        if x is not None:
            d[r["item"]].append(float(x))
    return d


def analizar_modelo(filas, des):
    rng = np.random.default_rng(SEMILLA)
    ok = lambda b, **kw: [r for r in filas if r["brazo"] == b and r["estado"] == "OK"  # noqa: E731
                          and all(r.get(k) == v for k, v in kw.items())]
    out = {"estados": defaultdict(lambda: defaultdict(int)), "rasgos": {}, "validez": {}}
    for r in filas:
        out["estados"][r["brazo"]][r["estado"]] += 1
    out["estados"] = {b: dict(v) for b, v in out["estados"].items()}

    # ── R1: claves equilibradas, así que la aquiescencia es el acuerdo medio − 3
    auto = ok("auto")
    out["validez"]["aquiescencia"] = float(np.mean([r["acuerdo"] for r in auto]) - 3)
    asc = [r["acuerdo"] for r in auto if r["orden"] == "asc"]
    desc = [r["acuerdo"] for r in auto if r["orden"] == "desc"]
    out["validez"]["sesgo_orden_escala"] = float(np.mean(asc) - np.mean(desc))
    pares = defaultdict(dict)
    for r in auto:
        pares[r["item"]].setdefault(r["orden"], []).append(r["acuerdo"])
    xs = [np.mean(v["asc"]) for v in pares.values() if "asc" in v and "desc" in v]
    ys = [np.mean(v["desc"]) for v in pares.values() if "asc" in v and "desc" in v]
    out["validez"]["r_ordenes_escala"] = float(np.corrcoef(xs, ys)[0, 1])
    rep = defaultdict(dict)
    for r in auto:
        rep[(r["item"], r["orden"])][r["rep"]] = r["acuerdo"]
    out["validez"]["retest_auto"] = float(np.mean(
        [v[0] == v[1] for v in rep.values() if 0 in v and 1 in v]))

    # ── Situaciones: posición y consistencia de polo entre órdenes
    for brazo in ("sit_personaje", "sit_propia", "sit_persona"):
        rs = ok(brazo)
        out["validez"][f"pA_{brazo}"] = float(np.mean([r["valor"] == "A" for r in rs]))
    for brazo in ("sit_personaje", "sit_propia"):
        polo = defaultdict(dict)
        for r in ok(brazo):
            polo[r["item"]][r["orden"]] = r["elige_alto"]
        out["validez"][f"polo_AB_BA_{brazo}"] = float(np.mean(
            [v["AB"] == v["BA"] for v in polo.values() if len(v) == 2]))

    con_d = lambda r: r["item"] in des  # noqa: E731
    elige = lambda r: 1.0 if r["elige_alto"] else 0.0  # noqa: E731
    ajust = lambda r: (elige(r) - des[r["item"]]) if con_d(r) else None  # noqa: E731
    contra = lambda r: abs(elige(r) - des[r["item"]]) if con_d(r) else None  # noqa: E731

    for rasgo in RASGOS:
        de = lambda filas_: [r for r in filas_ if r["rasgo"] == rasgo]  # noqa: E731
        g = {}
        g["R1"] = _boot_items(_por_item(de(auto), lambda r: r["puntos"]), rng)
        for reg, brazo in (("R2", "sit_personaje"), ("R3", "sit_propia")):
            g[f"{reg}_bruta"] = _boot_items(_por_item(de(ok(brazo)), elige), rng)
            a = _por_item(de(ok(brazo)), ajust)
            # ajustada: 50 + 50·media(elige − d); _boot_items devuelve ×100
            t = _boot_items(a, rng)
            g[f"{reg}_ajustada"] = (None if t[0] is None else
                                    tuple(50 + x / 2 for x in t))
            g[f"{reg}_contra"] = _boot_items(_por_item(de(ok(brazo)), contra), rng)
        g["delta_contra_personaje_menos_tu"] = _diferencia_items(
            _por_item(de(ok("sit_personaje")), contra),
            _por_item(de(ok("sit_propia")), contra), rng)
        g["elasticidad_conducta"] = _diferencia_items(
            _por_item(de(ok("sit_persona", nivel="alto")), elige),
            _por_item(de(ok("sit_persona", nivel="bajo")), elige), rng)
        g["elasticidad_declarada"] = _diferencia_items(
            _por_item(de(ok("auto_persona", nivel="alto")), lambda r: r["puntos"]),
            _por_item(de(ok("auto_persona", nivel="bajo")), lambda r: r["puntos"]), rng)
        g["deseabilidad_media_escala"] = float(np.mean(
            [des[s[0]] for s in p1.situaciones() if s[1] == rasgo and s[0] in des]))
        g["escaparate_R1_menos_R3aj"] = (g["R1"][0] - g["R3_ajustada"][0]
                                         if g["R1"][0] is not None and g["R3_ajustada"]
                                         else None)
        out["rasgos"][rasgo] = g

    # ── H1 por modelo, todos los rasgos juntos
    out["H1"] = _diferencia_items(_por_item(ok("sit_personaje"), contra),
                                  _por_item(ok("sit_propia"), contra), rng)
    sondas = [r for r in filas if r["brazo"] == "sonda"]
    out["reconoce"] = {reg: [bool(RE_RECONOCE.search(r["raw"])) for r in sondas
                             if r.get("registro") == reg]
                       for reg in ("auto", "sit_personaje", "sit_propia")}
    out["sondas"] = {r["item"]: r["raw"] for r in sondas}
    return out


def transversal(datos, des, res):
    """H1 agregado, H2, H3 y criterio de instrumento (§8)."""
    rng = np.random.default_rng(SEMILLA)
    out = {}
    # H1 agregado: Δ contra (personaje − tú) por (modelo, ítem), bootstrap por ítem
    por_item = defaultdict(list)
    for m, filas in datos.items():
        d = des.get(m, {})
        c2, c3 = defaultdict(list), defaultdict(list)
        for r in filas:
            if r["estado"] != "OK" or r["item"] not in d:
                continue
            x = abs((1.0 if r["elige_alto"] else 0.0) - d[r["item"]])
            if r["brazo"] == "sit_personaje":
                c2[r["item"]].append(x)
            elif r["brazo"] == "sit_propia":
                c3[r["item"]].append(x)
        for k in c2:
            if c3.get(k):
                por_item[k].append(np.mean(c2[k]) - np.mean(c3[k]))
    rasgo_de = {s[0]: s[1] for s in p1.situaciones()}
    out["H1_por_rasgo"] = {}
    for t in RASGOS:
        v = np.array([np.mean(x) for k, x in por_item.items() if rasgo_de.get(k) == t])
        b_ = v[rng.integers(0, len(v), size=(B, len(v)))].mean(axis=1)
        out["H1_por_rasgo"][t] = [float(v.mean() * 100), float(np.percentile(b_, 2.5) * 100),
                                  float(np.percentile(b_, 97.5) * 100)]
    # Indeterminación: el modelo se niega a predecir al personaje («no se
    # puede determinar»). Solo puede darse en R2/R3; se cuenta por registro.
    out["indeterminadas"] = {m: {b_: sum(1 for r in f if r["brazo"] == b_ and r["estado"] != "OK")
                                 for b_ in ("sit_personaje", "sit_propia", "sit_persona")}
                             for m, f in datos.items()}
    mi = np.array([np.mean(v) for v in por_item.values()])
    bs = mi[rng.integers(0, len(mi), size=(B, len(mi)))].mean(axis=1)
    todas = [x for v in por_item.values() for x in v]
    dirs = {m: res[m]["H1"][0] for m in res}
    out["H1"] = {"pp": float(np.mean(todas) * 100),
                 "ic": [float(np.percentile(bs, 2.5) * 100), float(np.percentile(bs, 97.5) * 100)],
                 "n_pares": len(todas), "n_items": len(mi),
                 "modelos_en_direccion": sum(v > 0 for v in dirs.values() if v is not None),
                 "por_modelo": dirs}
    out["H1"]["sostenida"] = bool(out["H1"]["ic"][0] > 0 and out["H1"]["modelos_en_direccion"] >= 5)
    # H2: escaparate de Apertura (R1 > R3 ajustada) en ≥5 de 6
    esc = {m: res[m]["rasgos"]["O"]["escaparate_R1_menos_R3aj"] for m in res}
    out["H2"] = {"por_modelo": esc, "positivos": sum(v > 0 for v in esc.values() if v is not None)}
    out["H2"]["sostenida"] = out["H2"]["positivos"] >= 5
    # H3: elasticidad conductual media entre modelos < 90 en ≥4 rasgos
    el = {t: float(np.mean([x for x in (res[m]["rasgos"][t]["elasticidad_conducta"][0]
                                         for m in res) if x is not None] or [np.nan]))
          for t in RASGOS}
    out["H3"] = {"media_por_rasgo": el, "rasgos_bajo_90": sum(v < 90 for v in el.values())}
    out["H3"]["sostenida"] = out["H3"]["rasgos_bajo_90"] >= 4
    # Criterio de instrumento: semiancho mediano del IC de R3 ≤ 15
    sw = [(res[m]["rasgos"][t]["R3_bruta"][2] - res[m]["rasgos"][t]["R3_bruta"][1]) / 2
          for m in res for t in RASGOS if res[m]["rasgos"][t]["R3_bruta"][0] is not None]
    out["instrumento"] = {"semiancho_mediano_R3": float(np.median(sw)),
                          "cumple": bool(np.median(sw) <= 15)}
    # ¿Distingue modelos? rango / semiancho medio del IC, por rasgo y registro
    out["discrimina"] = {}
    for t in RASGOS:
        fila = {}
        for k in ("R1", "R2_ajustada", "R3_ajustada"):
            v = [res[m]["rasgos"][t][k] for m in res
                 if res[m]["rasgos"][t][k] and res[m]["rasgos"][t][k][0] is not None]
            if len(v) < 2:
                fila[k] = None
                continue
            pts = [x[0] for x in v]
            semi = np.mean([(x[2] - x[1]) / 2 for x in v])
            fila[k] = float((max(pts) - min(pts)) / semi) if semi else None
        r1 = [res[m]["rasgos"][t]["R1"][0] for m in res]
        r3 = [(res[m]["rasgos"][t]["R3_ajustada"] or (None,))[0] for m in res]
        aq = [res[m]["validez"]["aquiescencia"] for m in res]
        completo = None not in r1 + r3
        fila["r_R1_R3aj"] = (float(np.corrcoef(r1, r3)[0, 1])
                             if completo and np.std(r1) and np.std(r3) else None)
        fila["r_aquiesc_R1"] = (float(np.corrcoef(aq, r1)[0, 1])
                                if None not in r1 and np.std(r1) else None)
        out["discrimina"][t] = fila
    out["reconoce"] = {reg: [int(sum(x for m in res for x in res[m]["reconoce"][reg])),
                             sum(len(res[m]["reconoce"][reg]) for m in res)]
                       for reg in ("auto", "sit_personaje", "sit_propia")}
    return out


def informe(res, tr):
    si = lambda b: "**SOSTENIDA**" if b else "**NO sostenida**"  # noqa: E731
    h1, h2, h3, ins = tr["H1"], tr["H2"], tr["H3"], tr["instrumento"]
    L = ["# P1 · Personalidad en tres registros", "",
         "Generado por `analizar_personalidad_p1.py`. Hipótesis y criterios fijados antes"
         " de correr (PERSONALIDAD.md §8). Escala 0-100; IC 95 % por bootstrap de ítems."
         " Ajustada: 50 = elegir lo que el propio modelo juzga deseable.", "",
         "## Hipótesis", "",
         f"- **H1 · «tú» elige mejor que el personaje:** Δ contra lo deseable (personaje − tú)"
         f" = {h1['pp']:+.1f} pp [IC {h1['ic'][0]:+.1f}, {h1['ic'][1]:+.1f}],"
         f" {h1['n_pares']} pares de {h1['n_items']} ítems; dirección en"
         f" {h1['modelos_en_direccion']}/6 modelos → {si(h1['sostenida'])}.",
         "  Por rasgo (agregado): " + ", ".join(f"{t} {v[0]:+.1f} [{v[1]:+.1f}, {v[2]:+.1f}]"
                                                for t, v in tr["H1_por_rasgo"].items()) + ".",
         f"- **H2 · escaparate de Apertura (R1 > R3 ajustada):** {h2['positivos']}/6 modelos"
         f" ({', '.join(f'{m} {v:+.0f}' for m, v in h2['por_modelo'].items())}) → {si(h2['sostenida'])}.",
         f"- **H3 · elasticidad sin saturar (<90):** {h3['rasgos_bajo_90']}/6 rasgos"
         f" ({', '.join(f'{t} {v:.0f}' for t, v in h3['media_por_rasgo'].items())}) → {si(h3['sostenida'])}.",
         f"- **Instrumento · semiancho mediano del IC de R3 ≤ 15:** {ins['semiancho_mediano_R3']:.1f}"
         f" → {'cumple' if ins['cumple'] else 'no cumple'}.", "",
         "## Validez por modelo", "",
         "| modelo | aquiesc. | sesgo orden escala | r órdenes | retest R1 | P(A) R2 | P(A) R3 | polo AB=BA R2 | polo AB=BA R3 | H1 por modelo (pp) |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for m, r in res.items():
        v = r["validez"]
        L.append(f"| {m} | {_f(v['aquiescencia'], 2)} | {_f(v['sesgo_orden_escala'], 2)}"
                 f" | {_f(v['r_ordenes_escala'], 2)} | {_f(v['retest_auto'], 2)}"
                 f" | {_f(v['pA_sit_personaje'], 2)} | {_f(v['pA_sit_propia'], 2)}"
                 f" | {_f(v['polo_AB_BA_sit_personaje'], 2)} | {_f(v['polo_AB_BA_sit_propia'], 2)}"
                 f" | {_ic(r['H1'])} |")
    for t in RASGOS:
        L += ["", f"## {t}", "",
              "| modelo | R1 | R2 bruta | R3 bruta | R2 ajustada | R3 ajustada | Δ contra (pers.−tú) | escaparate R1−R3aj | elast. conducta | elast. declarada | deseab. escala |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for m, r in res.items():
            g = r["rasgos"][t]
            L.append(f"| {m} | {_ic(g['R1'])} | {_ic(g['R2_bruta'])} | {_ic(g['R3_bruta'])}"
                     f" | {_ic(g['R2_ajustada'])} | {_ic(g['R3_ajustada'])}"
                     f" | {_ic(g['delta_contra_personaje_menos_tu'])}"
                     f" | {_f(g['escaparate_R1_menos_R3aj'])} | {_ic(g['elasticidad_conducta'])}"
                     f" | {_ic(g['elasticidad_declarada'])} | {100 * g['deseabilidad_media_escala']:.0f} |")
    L += ["", "## ¿Distingue modelos? (rango / semiancho del IC; <2 = no) y correlaciones entre modelos", "",
          "| rasgo | R1 | R2 aj. | R3 aj. | r(R1, R3aj) | r(aquiesc., R1) |", "|---|---|---|---|---|---|"]
    for t, f in tr["discrimina"].items():
        L.append(f"| {t} | {_f(f['R1'], 1)} | {_f(f['R2_ajustada'], 1)} | {_f(f['R3_ajustada'], 1)}"
                 f" | {_f(f['r_R1_R3aj'], 2)} | {_f(f['r_aquiesc_R1'], 2)} |")
    L += ["", "## No determinables (se niega a predecir; excluidas, nunca imputadas)", ""]
    L += [f"- {m}: " + ", ".join(f"{b} {n}" for b, n in v.items())
          for m, v in tr["indeterminadas"].items()]
    L += ["", "## Reconocimiento (la sonda nombra personalidad/rasgos)", ""]
    L += [f"- {reg}: {k}/{n}" for reg, (k, n) in tr["reconoce"].items()]
    return "\n".join(L) + "\n"


def main():
    datos = cargar(DIR)
    des = deseabilidad()
    faltan = [m for m in datos if m not in des]
    if faltan:
        raise SystemExit(f"sin calibración de deseabilidad para {faltan}")
    res = {m: analizar_modelo(f, des[m]) for m, f in datos.items()}
    tr = transversal(datos, des, res)
    (DIR / "resumen.json").write_text(json.dumps({"modelos": res, "transversal": tr},
                                                 ensure_ascii=False, indent=2, default=str),
                                      encoding="utf-8")
    texto = informe(res, tr)
    (DIR / "INFORME.md").write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
