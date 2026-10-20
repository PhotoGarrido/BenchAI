"""Robustez de las marcas ▲/▼ del cuadro v2 (PERSONALIDAD.md §26).

Criterios fijados en §26 ANTES de calcular. Solo datos ya recogidos: ninguna
llamada a modelos. Reutiliza analizar_v3 (carga, puntuación y diferencia
pareada) y parte de las marcas que escribió en v3.json.

  P1 mitades de situaciones (por faceta, 200 particiones): tasa de signo ≥ 90 %
  P2 réplica 0 / réplica 1: la marca se mantiene en las dos
  P3 orden AB / BA: la marca se mantiene en los dos
  P4 deseabilidad común (consenso = sin ajuste en la pareada): se mantiene
  P5 quitar un laboratorio cada vez: se mantiene en todos los paneles
  P6 Benjamini-Hochberg sobre las 78 pruebas: q < 0,05
Niveles: robusta (pasa todas) · frágil (falla 1-2, signo P1 ≥ 75 %) ·
no publicable (signo P1 < 75 %, falla ≥ 3, se invierte, o rasgo N).

Uso: python analizar_robustez_v3.py
     → resultados/personalidad_fc/ROBUSTEZ_V3.md y robustez_v3.json
"""

import json

import numpy as np

from analizar_discriminacion import _id, iss_por_modelo
from analizar_personalidad import SEMILLA, _spearman
from analizar_v3 import (RASGOS, SALIDA, _boot, cargar_v3, dif_pareada,
                         puntuar, signo)
from cuadro_personalidad import NOMBRE, POLOS

N_PARTICIONES = 200
B_MITAD = 1000
B_FDR = 20000
B_ISS = 2000
Q = .05
#: Familia de los modelos de NaN (sin prefijo de organización en el id).
FAMILIA_NAN = {"qwen": "qwen", "deepseek": "deepseek", "gemma": "google",
               "glm": "z-ai", "mimo": "xiaomi"}
PRUEBAS = ("P1", "P2", "P3", "P4", "P5", "P6")


def laboratorio(m):
    i = _id(m)
    if "/" in i:
        return i.split("/")[0]
    for pref, lab in FAMILIA_NAN.items():
        if i.startswith(pref):
            return lab
    return i


def _ic_p(x, rng, b):
    """Media, IC 95 % y p bilateral por bootstrap (suelo 1/b)."""
    x = np.asarray(x, float)
    bs = x[rng.integers(0, len(x), size=(b, len(x)))].mean(axis=1)
    p = 2 * min((bs <= 0).mean(), (bs >= 0).mean())
    return float(x.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), \
        float(min(1.0, max(p, 1 / b)))


def bh(ps):
    """q de Benjamini-Hochberg, mismo orden que ps."""
    ps = np.asarray(ps, float)
    n = len(ps)
    orden = np.argsort(ps)
    q = ps[orden] * n / np.arange(1, n + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(n)
    out[orden] = np.minimum(q, 1)
    return out


def marcas_variante(a, ms, por_rasgo, rng, otros_de=None):
    """{(m, t): (signo, dif, lo, hi)} con una puntuación `a` alternativa.

    Solo situaciones con dato en todos los modelos de la variante."""
    out = {}
    for m in ms:
        otros = otros_de(m) if otros_de else [o for o in ms if o != m]
        for t in RASGOS:
            items = [i for i in por_rasgo[t] if all(i in a[o] for o in [m] + otros)]
            dp, lo, hi = _boot(dif_pareada(a, m, otros, items), rng)
            out[(m, t)] = (signo(lo, hi), dp, lo, hi)
    return out


def particiones(items, faceta_de, rng):
    """N_PARTICIONES pares de mitades equilibradas por faceta."""
    por_f = {}
    for i in items:
        por_f.setdefault(faceta_de[i], []).append(i)
    out = []
    for _ in range(N_PARTICIONES):
        h1, h2, turno = [], [], 0
        for f in sorted(por_f):
            v = list(rng.permutation(por_f[f]))
            k = len(v) // 2
            if len(v) % 2:
                k += turno
                turno = 1 - turno
            h1 += v[:k]
            h2 += v[k:]
        out.append((h1, h2))
    return out


def d_consenso(des, ms, items):
    """Deseabilidad común d̄(i): media de los juicios de todos los modelos `ms`."""
    return {i: float(np.mean([des[m][i] for m in ms])) for i in items}


def mitades(d, partes, s0, rng):
    """P1 de una marca s0 con diferencias por situación d {item: dif}.

    Tasas sobre las particiones `partes`: signo de la marca en las dos mitades,
    marca significativa en las dos, y alguna mitad con signo contrario
    significativo (solo informativa, §27)."""
    s = 1 if s0 == "▲" else -1
    n_signo = n_sig = n_inv = 0
    for h1, h2 in partes:
        r1 = _ic_p([d[i] for i in h1], rng, B_MITAD)
        r2 = _ic_p([d[i] for i in h2], rng, B_MITAD)
        n_signo += s * r1[0] > 0 and s * r2[0] > 0
        n_sig += all(signo(r[1], r[2]) == s0 for r in (r1, r2))
        n_inv += any(signo(r[1], r[2]) not in ("", s0) for r in (r1, r2))
    n = len(partes)
    return {"tasa_signo": n_signo / n, "tasa_sig_ambas": n_sig / n,
            "tasa_half_invertida": n_inv / n}


def clasificar(t, tasa_signo, fallos, inv, todas):
    """(nivel, motivo) de una marca según los niveles de §26.

    fallos: comprobaciones que falla; inv: variantes en que se invierte;
    todas: etiqueta de las comprobaciones aplicadas («P1–P6»)."""
    if t == "N":
        return "no publicable", "N solo descriptivo (§23)"
    if tasa_signo < .75 or len(fallos) >= 3 or inv:
        return "no publicable", ", ".join(filter(None, [
            f"signo en mitades {100 * tasa_signo:.0f} % < 75 %" if tasa_signo < .75 else "",
            f"falla {len(fallos)} ({' '.join(fallos)})" if len(fallos) >= 3 else "",
            f"se invierte en {', '.join(inv)}" if inv else ""]))
    if not fallos:
        return "robusta", f"pasa {todas}"
    return "frágil", f"falla {' '.join(fallos)}"


def frase(t, s):
    """Frase del retrato para el rasgo t con marca s (▲/▼)."""
    return f"**{'más' if s == '▲' else 'menos'} {NOMBRE[t]}** ({POLOS[t][0] if s == '▲' else POLOS[t][1]})"


def main():
    rng = np.random.default_rng(SEMILLA)
    v = cargar_v3()
    ms, por_rasgo, des, el = v["ms"], v["por_rasgo"], v["des"], v["elecciones"]
    base = json.loads((SALIDA / "v3.json").read_text(encoding="utf-8"))
    marca0 = {(m, t): tuple(base["marca"][f"{m}|{t}"]) for m in ms for t in RASGOS}
    punt0 = {(m, t): base["puntuacion"][f"{m}|{t}"][0] for m in ms for t in RASGOS}
    marcadas = [k for k, x in marca0.items() if x[0]]
    a = {m: puntuar(el[m], des[m]) for m in ms}

    # ── Variantes (P2, P3, P4) ──────────────────────────────────────────────
    filtros = {"rep0": lambda o, r: r == 0, "rep1": lambda o, r: r == 1,
               "AB": lambda o, r: o == "AB", "BA": lambda o, r: o == "BA"}
    var = {k: marcas_variante({m: puntuar(el[m], des[m], f) for m in ms}, ms, por_rasgo, rng)
           for k, f in filtros.items()}
    comunes = v["comunes"]
    d_cons = d_consenso(des, ms, comunes)
    a_cons = {m: puntuar({i: el[m][i] for i in comunes}, d_cons) for m in ms}
    a_raw = {m: puntuar(el[m]) for m in ms}
    var["consenso"] = marcas_variante(a_cons, ms, por_rasgo, rng)
    var["sin_ajuste"] = marcas_variante(a_raw, ms, por_rasgo, rng)
    # Comprobación de la identidad anunciada en §26: consenso ≡ sin ajuste
    dif_max = max(abs(np.mean(dif_pareada(a_cons, m, [o for o in ms if o != m], por_rasgo[t]))
                      - np.mean(dif_pareada(a_raw, m, [o for o in ms if o != m], por_rasgo[t])))
                  for m in ms for t in RASGOS)
    punt_alt = {(m, t): (50 + 50 * np.mean([a_cons[m][i] for i in por_rasgo[t]]),
                         50 + 50 * np.mean([a_raw[m][i] for i in por_rasgo[t]]))
                for m in ms for t in RASGOS}

    # ── P5 · quitar un laboratorio cada vez ────────────────────────────────
    labs = sorted({laboratorio(m) for m in ms})
    var_lab = {L: marcas_variante(a, ms, por_rasgo, rng,
                                  lambda m, L=L: [o for o in ms if o != m and laboratorio(o) != L])
               for L in labs}

    # ── P6 · p por bootstrap y BH ──────────────────────────────────────────
    pruebas = [(m, t) for m in ms for t in RASGOS]
    pval = {k: _ic_p(dif_pareada(a, k[0], [o for o in ms if o != k[0]], por_rasgo[k[1]]),
                     rng, B_FDR)[3] for k in pruebas}
    q78 = dict(zip(pruebas, bh([pval[k] for k in pruebas])))
    sin_n = [k for k in pruebas if k[1] != "N"]
    q65 = dict(zip(sin_n, bh([pval[k] for k in sin_n])))

    # ── P1 · mitades por faceta ────────────────────────────────────────────
    parts = {t: particiones(por_rasgo[t], v["faceta_de"], rng) for t in RASGOS}
    p1 = {}
    for (m, t) in marcadas:
        d = dict(zip(por_rasgo[t], dif_pareada(a, m, [o for o in ms if o != m], por_rasgo[t])))
        p1[(m, t)] = mitades(d, parts[t], marca0[(m, t)][0], rng)

    # ── Niveles ────────────────────────────────────────────────────────────
    filas = {}
    for k in marcadas:
        m, t = k
        s0 = marca0[k][0]
        se_mantiene = lambda x: x[k][0] == s0  # noqa: E731
        invierte = lambda x: x[k][0] not in ("", s0)  # noqa: E731
        paso = {
            "P1": p1[k]["tasa_signo"] >= .90,
            "P2": se_mantiene(var["rep0"]) and se_mantiene(var["rep1"]),
            "P3": se_mantiene(var["AB"]) and se_mantiene(var["BA"]),
            "P4": se_mantiene(var["consenso"]),
            "P5": all(se_mantiene(var_lab[L]) for L in labs),
            "P6": q78[k] < Q,
        }
        caen = [L for L in labs if not se_mantiene(var_lab[L])]
        inv = [n for n, x in list(var.items()) + [(f"sin {L}", var_lab[L]) for L in labs] if invierte(x)]
        fallos = [p for p in PRUEBAS if not paso[p]]
        nivel, motivo = clasificar(t, p1[k]["tasa_signo"], fallos, inv, "P1–P6")
        if caen and not paso["P5"]:
            motivo += f"; cae sin {', '.join(caen)}"
        filas[k] = {"marca": s0, "dif": marca0[k][1], "ic": marca0[k][2:4], "paso": paso,
                    "fallos": fallos, "nivel": nivel, "motivo": motivo, "q78": q78[k],
                    "q65": q65.get(k), "p": pval[k], "p1": p1[k], "cae_sin_lab": caen,
                    "invierte_en": inv,
                    "variantes": {n: x[k][0] for n, x in var.items()}}

    nuevas = sorted({(n, k) for n, x in list(var.items()) + [(f"sin {L}", var_lab[L]) for L in labs]
                     for k in pruebas if x[k][0] and not marca0[k][0]}, key=lambda z: (z[1], z[0]))

    # ── ISS (descriptivo) ──────────────────────────────────────────────────
    iss = iss_por_modelo()
    con_iss = [m for m in ms if isinstance(iss.get(_id(m)), (int, float))]
    corr_iss = {}
    for t in RASGOS:
        x = np.array([punt0[(m, t)] for m in con_iss])
        y = np.array([float(iss[_id(m)]) for m in con_iss])
        rho = _spearman(x, y)
        bs = []
        for _ in range(B_ISS):
            j = rng.integers(0, len(x), len(x))
            r = _spearman(x[j], y[j])
            if r is not None and not np.isnan(r):
                bs.append(r)
        corr_iss[t] = (rho, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)))

    # ── Retratos ───────────────────────────────────────────────────────────
    retratos = {}
    for m in ms:
        rob = [(t, filas[(m, t)]["marca"]) for t in RASGOS
               if (m, t) in filas and filas[(m, t)]["nivel"] == "robusta"]
        partes = [frase(t, s) for t, s in rob if t != "E"]
        partes += [frase(t, s) + " *[Extraversión: fiabilidad baja, con aviso]*" for t, s in rob if t == "E"]
        txt = "; ".join(partes) if partes else "perfil próximo al de los demás modelos"
        tend = [f"{t}{filas[(m, t)]['marca']}" for t in RASGOS
                if (m, t) in filas and filas[(m, t)]["nivel"] == "frágil"]
        retratos[m] = {"texto": txt, "fragiles": tend, "N": punt0[(m, "N")]}

    # ── Informe ────────────────────────────────────────────────────────────
    cnt = {n: sum(f["nivel"] == n for f in filas.values()) for n in ("robusta", "frágil", "no publicable")}
    L = ["# Robustez de las marcas del cuadro v2 (PERSONALIDAD.md §26)", "",
         f"Generado por `analizar_robustez_v3.py`. {len(ms)} modelos, {len(labs)} laboratorios "
         f"({', '.join(labs)}). Semilla {SEMILLA}. Sin llamadas a modelos.", "",
         f"**{len(marcadas)} marcas** en el cuadro: {cnt['robusta']} robustas · {cnt['frágil']} frágiles"
         f" · {cnt['no publicable']} no publicables.", "",
         "P1 = signo replicado en las dos mitades (≥ 90 %) · P2 = réplica 0 y 1 · P3 = orden AB y BA ·"
         " P4 = deseabilidad común · P5 = todos los paneles sin un laboratorio · P6 = BH q < 0,05 (78).",
         "", "| modelo | rasgo | marca | dif [IC] | P1 signo (sig. ambas) | P2 | P3 | P4 | P5 | P6 q78 (q65) | nivel | por qué |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    ok = lambda b: "✔" if b else "✘"  # noqa: E731
    for k, f in filas.items():
        m, t = k
        L.append(f"| {_id(m)} | {t} | {f['marca']} | {f['dif']:+.1f} [{f['ic'][0]:+.1f}, {f['ic'][1]:+.1f}]"
                 f" | {100 * f['p1']['tasa_signo']:.0f} % ({100 * f['p1']['tasa_sig_ambas']:.0f} %)"
                 f" | {ok(f['paso']['P2'])} | {ok(f['paso']['P3'])} | {ok(f['paso']['P4'])}"
                 f" | {ok(f['paso']['P5'])} | {f['q78']:.4f}"
                 f" ({'—' if f['q65'] is None else f'{f["q65"]:.4f}'}) | **{f['nivel']}** | {f['motivo']} |")
    L += ["", "## Variantes de cada marca", "",
          "Marca en cada variante (· = sin marca).", "",
          "| modelo | rasgo | cuadro | rep0 | rep1 | AB | BA | consenso | sin ajuste |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k, f in filas.items():
        vv = f["variantes"]
        L.append(f"| {_id(k[0])} | {k[1]} | {f['marca']} | " + " | ".join(
            vv[n] or "·" for n in ("rep0", "rep1", "AB", "BA", "consenso", "sin_ajuste")) + " |")
    L += ["", f"Consenso ≡ sin ajuste en la diferencia pareada: diferencia máxima {dif_max:.1e} puntos"
          " (cancelación de un d(i) común, §26).", "",
          "## Marcas nuevas en alguna variante (no entran en el retrato)", ""]
    agrup = {}
    for n, k in nuevas:
        agrup.setdefault(k, []).append(n)
    L += [f"- {_id(k[0])} · {k[1]}: {', '.join(ns)}" for k, ns in agrup.items()] or ["- ninguna"]
    L += ["", "## Puntuación según la fuente de la deseabilidad", "",
          "Propia (cuadro) / consenso / sin ajuste. La comparación entre modelos no cambia entre"
          " consenso y sin ajuste; cambia el nivel absoluto.", "",
          "| modelo | " + " | ".join(RASGOS) + " |", "|---|" + "---|" * len(RASGOS)]
    for m in ms:
        L.append(f"| {_id(m)} | " + " | ".join(
            f"{punt0[(m, t)]:.0f}/{punt_alt[(m, t)][0]:.0f}/{punt_alt[(m, t)][1]:.0f}" for t in RASGOS) + " |")
    L += ["", "## Relación con el ISS (solo descriptiva)", "",
          f"Spearman entre la puntuación del cuadro y el ISS publicado, n = {len(con_iss)} modelos"
          f" con ISS ({', '.join(_id(m) for m in ms if m not in con_iss)} sin ISS). IC 95 % por"
          f" bootstrap de modelos ({B_ISS}). **Con n = {len(con_iss)} el IC es muy ancho; no se"
          " contrasta ninguna hipótesis.**", "",
          "| rasgo | ρ | IC 95 % |", "|---|---|---|"]
    for t, (r, lo, hi) in corr_iss.items():
        L.append(f"| {NOMBRE[t]} | {r:+.2f} | [{lo:+.2f}, {hi:+.2f}] |")
    L += ["", "## Retrato publicable propuesto", "",
          "Solo marcas robustas de O, C, A, H; E robusta con aviso; N solo descriptivo (§26).", ""]
    for m in ms:
        r = retratos[m]
        L.append(f"- **{_id(m)}**: {r['texto']}. *Neuroticismo (descriptivo): {r['N']:.0f}.*"
                 + (f" Tendencias frágiles, no publicadas: {', '.join(r['fragiles'])}." if r["fragiles"] else ""))
    (SALIDA / "ROBUSTEZ_V3.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (SALIDA / "robustez_v3.json").write_text(json.dumps({
        "semilla": SEMILLA, "laboratorios": {m: laboratorio(m) for m in ms},
        "marcas": {f"{m}|{t}": f for (m, t), f in filas.items()},
        "marcas_nuevas": [{"variante": n, "modelo": k[0], "rasgo": k[1]} for n, k in nuevas],
        "consenso_igual_sin_ajuste_max": dif_max,
        "puntuacion_alternativa": {f"{m}|{t}": {"propia": punt0[(m, t)], "consenso": punt_alt[(m, t)][0],
                                                "sin_ajuste": punt_alt[(m, t)][1]} for m in ms for t in RASGOS},
        "iss": {"n": len(con_iss), "spearman": corr_iss},
        "retratos": retratos}, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
