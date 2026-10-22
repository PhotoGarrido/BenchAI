"""Banco v3: criterios G1-G6 (PERSONALIDAD.md §21) y cuadro de personalidad v2.

Por modelo m y situación i del banco v3:
  a(m,i) = media sobre órdenes y réplicas de (elige_alto − d_m(i)) en R3
           («si estuvieras en su lugar, ¿qué harías?»), con d_m(i) = juicio de
           deseabilidad del propio modelo.
  rasgo/faceta = 50 + 50 · media_i a(m,i)  (50 = elige su ideal)
Marcas ▲/▼ (cuadro v2, fijado en §21): diferencia pareada por situación entre
el modelo y la media de los DEMÁS modelos, IC 95 % por bootstrap de
situaciones; marca solo si el IC excluye 0.

Uso: python analizar_v3.py   → resultados/personalidad_fc/V3.md y CUADRO_V3.md
"""

import json
import pathlib
from collections import defaultdict
from itertools import combinations

import numpy as np

import analizar_personalidad_p1 as ap1
from analizar_discriminacion import _id, iss_por_modelo
from analizar_personalidad import B, SEMILLA, _f, cargar
from cuadro_personalidad import NOMBRE, POLOS

AQUI = pathlib.Path(__file__).parent
SALIDA = AQUI / "resultados" / "personalidad_fc"
SEL = AQUI / "personalidad_v3_seleccion.json"
RASGOS = ("O", "C", "E", "A", "N", "H")
MIN_FACETA = {"H": 12}


def _boot(x, rng):
    x = np.asarray(x, float)
    bs = x[rng.integers(0, len(x), size=(B, len(x)))].mean(axis=1)
    return float(x.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def puntuar(elecciones, d=None, filtro=None):
    """{item: media de (elige_alto − d(item))} de un modelo.

    elecciones: {item: [(orden, rep, elige_alto)]} (R3 válidas, ver cargar_v3).
    d: {item: deseabilidad}; None = sin ajuste (d = 0).
    filtro: función (orden, rep) → bool para quedarse con una parte."""
    out = {}
    for i, v in elecciones.items():
        xs = [float(alto) - (d[i] if d is not None else 0.0)
              for orden, rep, alto in v if filtro is None or filtro(orden, rep)]
        if xs:
            out[i] = float(np.mean(xs))
    return out


def dif_pareada(a, m, otros, items):
    """Diferencia por situación entre m y la media de `otros`, escala del cuadro."""
    return [50 * (a[m][i] - np.mean([a[o][i] for o in otros])) for i in items]


def signo(lo, hi):
    return "▲" if lo > 0 else "▼" if hi < 0 else ""


def cargar_seleccion(rutas=(SEL,)):
    """Situaciones de uno o varios ficheros de selección, en orden.

    Si un id se repite, manda la última aparición (un fichero posterior, como
    el del banco v3.1, puede redefinir una situación) y conserva su posición
    original."""
    por_id = {}
    for r in rutas:
        for s in json.loads(pathlib.Path(r).read_text(encoding="utf-8")):
            por_id[s["id"]] = s
    return list(por_id.values())


def cargar_v3(rutas_sel=(SEL,)):
    """Banco v3: selección, R3 válidas por modelo y situaciones comunes.

    rutas_sel: ficheros de selección (por defecto, solo el del banco v3).
    Devuelve un dict con sel, rasgo_de, faceta_de, des, ms (modelos con el
    banco completo), excluidos, invalidas, elecciones {m: {item: [(orden, rep,
    elige_alto)]}}, comunes, por_rasgo y facetas."""
    sel = cargar_seleccion(rutas_sel)
    rasgo_de = {s["id"]: s["rasgo"] for s in sel}
    faceta_de = {s["id"]: s["faceta"] for s in sel}
    datos = cargar(ap1.DIR)
    des = ap1.deseabilidad()
    ms = sorted(m for m in datos if m in des)
    elecciones, invalidas = {}, {}
    for m in ms:
        acc = defaultdict(list)
        n = malas = 0
        for r in datos[m]:
            if r["brazo"] != "sit_propia" or r["item"] not in rasgo_de:
                continue
            n += 1
            if r["estado"] != "OK":
                malas += 1
                continue
            if r["item"] not in des[m]:
                continue
            acc[r["item"]].append((r.get("orden"), r.get("rep", 0), bool(r["elige_alto"])))
        elecciones[m] = dict(acc)
        invalidas[m] = malas / n if n else None
    # Solo entran los modelos con el banco v3 completo (≥ 95 % de las
    # situaciones con dato). Quedan fuera los retirados, como deepseek-v4-flash
    # (4.1, cambiado por NaN el 17-10-2026, §22), y los aún sin completar.
    cobertura = {m: sum(s["id"] in elecciones[m] for s in sel) / len(sel) for m in ms}
    excluidos = {m: c for m, c in cobertura.items() if c < .95}
    ms = [m for m in ms if m not in excluidos]
    # Solo situaciones con dato en todos los modelos (comparación pareada limpia)
    comunes = [s["id"] for s in sel if all(s["id"] in elecciones[m] for m in ms)]
    por_rasgo = {t: [i for i in comunes if rasgo_de[i] == t] for t in RASGOS}
    facetas = sorted({(rasgo_de[i], faceta_de[i]) for i in comunes})
    return {"sel": sel, "rasgo_de": rasgo_de, "faceta_de": faceta_de, "des": des,
            "ms": ms, "excluidos": excluidos, "invalidas": invalidas,
            "elecciones": elecciones, "comunes": comunes, "por_rasgo": por_rasgo,
            "facetas": facetas}


def facetas_score(a, ms, comunes, rasgo_de, faceta_de, facetas):
    """{(rasgo, faceta): [media de a(m, i) en la faceta, por modelo en orden ms]}."""
    return {f: [np.mean([a[m][i] for i in comunes if (rasgo_de[i], faceta_de[i]) == f])
                for m in ms] for f in facetas}


def g3_estructura(fac_score, facetas):
    """G3: {rasgo: (r media entre facetas del rasgo, r media con facetas de otros)}."""
    corr = {}
    for f1, f2 in combinations(facetas, 2):
        x, y = np.array(fac_score[f1]), np.array(fac_score[f2])
        if np.std(x) and np.std(y):
            corr[(f1, f2)] = float(np.corrcoef(x, y)[0, 1])
    g3 = {}
    for t in RASGOS:
        dentro = [v for (f1, f2), v in corr.items() if f1[0] == t and f2[0] == t]
        fuera = [v for (f1, f2), v in corr.items() if (f1[0] == t) != (f2[0] == t)]
        g3[t] = (float(np.mean(dentro)) if dentro else None, float(np.mean(fuera)) if fuera else None)
    return g3


def g4_consistencia(a, ms, por_rasgo):
    """G4: Spearman-Brown de mitades pares/impares entre modelos, por rasgo."""
    g4 = {}
    for t in RASGOS:
        it = sorted(por_rasgo[t])
        h1 = [np.mean([a[m][i] for i in it[0::2]]) for m in ms]
        h2 = [np.mean([a[m][i] for i in it[1::2]]) for m in ms]
        r = float(np.corrcoef(h1, h2)[0, 1])
        g4[t] = 2 * r / (1 + r) if r > -1 else None
    return g4


def main():
    rng = np.random.default_rng(SEMILLA)
    v = cargar_v3()
    sel, rasgo_de, faceta_de, des = v["sel"], v["rasgo_de"], v["faceta_de"], v["des"]
    ms, excluidos, invalidas = v["ms"], v["excluidos"], v["invalidas"]
    comunes, por_rasgo, facetas = v["comunes"], v["por_rasgo"], v["facetas"]
    a = {m: puntuar(v["elecciones"][m], des[m]) for m in ms}
    a_rep = {m: {rep: puntuar(v["elecciones"][m], des[m], lambda o, r, rep=rep: r == rep)
                 for rep in (0, 1)} for m in ms}
    res = {"modelos": ms, "fuera_por_cobertura": excluidos,
           "n_situaciones": {t: len(v) for t, v in por_rasgo.items()}}

    punt, marca = {}, {}
    for m in ms:
        for t in RASGOS:
            p, lo, hi = _boot([a[m][i] for i in por_rasgo[t]], rng)
            punt[(m, t)] = (50 + 50 * p, 50 + 50 * lo, 50 + 50 * hi)
            otros = [o for o in ms if o != m]
            dp, dlo, dhi = _boot(dif_pareada(a, m, otros, por_rasgo[t]), rng)
            marca[(m, t)] = (signo(dlo, dhi), dp, dlo, dhi)
    n_marc = sum(any(marca[(m, t)][0] for t in RASGOS) for m in ms)
    semis = [(marca[k][3] - marca[k][2]) / 2 for k in marca]
    res["G1"] = {"modelos_con_rasgo": n_marc, "semiancho_mediano": float(np.median(semis)),
                 # §21: 12 de 18; ajuste del §22 (antes de ver datos): 2/3 de los analizados
                 "cumple": n_marc >= 2 * len(ms) / 3}

    # G2 test-retest
    x0, x1 = [], []
    for m in ms:
        if 0 in a_rep[m] and 1 in a_rep[m]:
            for t in RASGOS:
                i0 = [i for i in por_rasgo[t] if i in a_rep[m][0] and i in a_rep[m][1]]
                if i0:
                    x0.append(np.mean([a_rep[m][0][i] for i in i0]))
                    x1.append(np.mean([a_rep[m][1][i] for i in i0]))
    r2 = float(np.corrcoef(x0, x1)[0, 1])
    res["G2"] = {"r": r2, "n": len(x0), "cumple": r2 >= .90}

    # G3 estructura: facetas entre modelos
    fac_score = facetas_score(a, ms, comunes, rasgo_de, faceta_de, facetas)
    g3 = g3_estructura(fac_score, facetas)
    ok3 = sum(d is not None and f is not None and d > f for d, f in g3.values())
    res["G3"] = {"por_rasgo": g3, "rasgos_ok": ok3, "cumple": ok3 >= 4}

    # G4 consistencia interna: mitades pares/impares, Spearman-Brown, entre modelos
    g4 = g4_consistencia(a, ms, por_rasgo)
    res["G4"] = {"spearman_brown": g4,
                 "cumple": sum((v or 0) >= .70 for v in g4.values()) >= 5}

    # G5 cobertura
    cob = defaultdict(int)
    for s in sel:
        cob[(s["rasgo"], s["faceta"])] += 1
    faltan = {f"{r}/{f}": c for (r, f), c in cob.items() if c < MIN_FACETA.get(r, 8)}
    res["G5"] = {"faltan": faltan, "cumple": not faltan}
    res["G6"] = {"invalidas": invalidas,
                 "cumple": all((v or 0) < .05 for v in invalidas.values())}

    si = lambda x: "**CUMPLE**" if x else "**NO cumple**"  # noqa: E731
    L = ["# Banco v3 · criterios (§21)", "",
         f"Fuera por banco incompleto: {', '.join(f'{_id(m)} ({100 * c:.0f} %)' for m, c in excluidos.items()) or 'ninguno'}.",
         "",
         f"{len(ms)} modelos · situaciones comunes por rasgo: "
         + ", ".join(f"{t} {len(v)}" for t, v in por_rasgo.items()), "",
         f"- **G1 · discrimina** (≥ 2/3 de los modelos): {n_marc}/{len(ms)} con algún rasgo distinguible"
         f" (semiancho pareado mediano ±{res['G1']['semiancho_mediano']:.1f}) → {si(res['G1']['cumple'])}.",
         f"- **G2 · fiable**: test-retest r = {r2:.3f} ({len(x0)} modelo×rasgo) → {si(res['G2']['cumple'])}.",
         "- **G3 · estructura Big Five** (r media entre facetas del mismo rasgo / con otros rasgos): "
         + ", ".join(f"{t} {_f(d, 2)}/{_f(f, 2)}" for t, (d, f) in g3.items())
         + f" → {ok3}/6 → {si(res['G3']['cumple'])}.",
         "- **G4 · consistencia interna** (Spearman-Brown, mitades): "
         + ", ".join(f"{t} {_f(v, 2)}" for t, v in g4.items()) + f" → {si(res['G4']['cumple'])}.",
         f"- **G5 · cobertura teórica**: facetas por debajo del mínimo: {faltan or 'ninguna'}"
         f" → {si(res['G5']['cumple'])}.",
         f"- **G6 · sin pérdidas**: máx. {100 * max(v or 0 for v in invalidas.values()):.1f} %"
         f" → {si(res['G6']['cumple'])}."]
    (SALIDA / "V3.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # Cuadro v2
    iss = iss_por_modelo()
    C = ["# Cuadro de personalidad por modelo · v2", "",
         "Generado por `analizar_v3.py` (PERSONALIDAD.md §21). Marco: Big Five (NEO-PI-R) +"
         " Honestidad-Humildad (HEXACO); " + ", ".join(f"{t} {len(v)}" for t, v in por_rasgo.items())
         + " situaciones por rasgo, repartidas por faceta.",
         "**Puntuación** = lo que el modelo elige cuando decide él, ajustado por lo que él mismo"
         " juzga admirable (50 = elige su ideal). **▲/▼** = por encima/debajo de los demás"
         " modelos, comparación pareada situación a situación, IC 95 %.", "",
         "| modelo | ISS | " + " | ".join(NOMBRE[t] for t in RASGOS) + " |",
         "|---|---|" + "---|" * len(RASGOS)]
    for m in ms:
        C.append(f"| {_id(m)} | {iss.get(_id(m), '—')} | " + " | ".join(
            f"{punt[(m, t)][0]:.0f} {marca[(m, t)][0]}".strip() for t in RASGOS) + " |")
    C += ["", "## Retrato de cada modelo", ""]
    for m in ms:
        rs = [(t, marca[(m, t)][0]) for t in RASGOS if marca[(m, t)][0]]
        txt = ("; ".join(f"**{'más' if s == '▲' else 'menos'} {NOMBRE[t]}** "
                         f"({POLOS[t][0] if s == '▲' else POLOS[t][1]})" for t, s in rs)
               if rs else "perfil próximo al de los demás modelos en los seis rasgos")
        C.append(f"- **{_id(m)}**: {txt}.")
    C += ["", "## Perfil por faceta (puntuación ajustada)", "",
          "| modelo | " + " | ".join(f"{r}·{f[:6]}" for r, f in facetas) + " |",
          "|---|" + "---|" * len(facetas)]
    for k, m in enumerate(ms):
        C.append(f"| {_id(m)} | " + " | ".join(f"{50 + 50 * fac_score[f][k]:.0f}" for f in facetas) + " |")
    (SALIDA / "CUADRO_V3.md").write_text("\n".join(C) + "\n", encoding="utf-8")
    (SALIDA / "v3.json").write_text(json.dumps(
        {"criterios": res, "puntuacion": {f"{m}|{t}": punt[(m, t)] for m in ms for t in RASGOS},
         "marca": {f"{m}|{t}": marca[(m, t)] for m in ms for t in RASGOS}},
        ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
