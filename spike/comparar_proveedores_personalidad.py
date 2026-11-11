"""Mismo modelo, dos proveedores: ¿cambia su personalidad medida? (11-11-2026)

DeepSeek V4 Pro 0813 se midió por OpenRouter (`deepseek/deepseek-v4-pro-0813`,
en el cuadro) y, por NaN, como `deepseek-v4-pro` (alta de noviembre: NaN
documenta que sirve la versión 0813). Decisión de David (10-11): la medición de
NaN no es una fila más del cuadro, sino una réplica entre proveedores.

Por rasgo (O, C, E, A del banco v3; H y N de I1) y por situación i:
  e(i) = fracción de elecciones del polo alto (órdenes × réplicas válidas).
Se compara NaN con OpenRouter con:
  r      correlación de Pearson de e(i) entre situaciones
  |Δ|    media de |e_NaN(i) − e_OR(i)|, en puntos porcentuales
  Δ      50·media(e_NaN − e_OR), escala de las comparaciones del cuadro, con
         IC 95 % por bootstrap de situaciones
y se sitúa frente a dos referencias medidas igual:
  retest     réplica 0 frente a réplica 1 dentro de cada medición (el ruido
             de volver a medir con el mismo proveedor)
  otros      OpenRouter frente a cada otro modelo del panel (mediana y mínimo
             de |Δ|): cuánto se separan modelos distintos
Lectura fijada antes de mirar: el cambio de proveedor es «despreciable» si en
cada rasgo |Δ| entre proveedores no supera el mayor |Δ| de retest de las dos
mediciones + 2 pp y el IC de Δ incluye 0; «pequeño» si |Δ| queda por debajo
del mínimo entre modelos distintos; si no, «relevante».

Se añaden los índices de validez de las dos mediciones (validez_personalidad,
§41.2): si las dos son «no interpretables», el perfil no se lee como
personalidad y las diferencias por rasgo solo describen la medición.

Sin llamadas a modelos. Uso (desde spike/):
    python comparar_proveedores_personalidad.py
      → resultados/personalidad_fc/PROVEEDORES_DEEPSEEK_V4_PRO.md y .json
"""

import json

import numpy as np

import analizar_h_confirmacion as ahc
import analizar_n_confirmacion as anc
import validez_personalidad as vp
from analizar_personalidad import SEMILLA
from analizar_v3 import SALIDA, cargar_v3
from cuadro_publico_v3 import RASGOS_V3

NAN = "deepseek-v4-pro"
OR = "deepseek_deepseek-v4-pro-0813"
B = 2000


def _i1(m):
    """Id con el que leen los cargadores de I1 (organización con «/»)."""
    return m.replace("_", "/", 1) if "_" in m.split("#")[0].split("@")[0] else m


def fraccion(el, filtro=None):
    out = {}
    for i, v in el.items():
        xs = [float(a) for o, r, a in v if filtro is None or filtro(o, r)]
        if xs:
            out[i] = float(np.mean(xs))
    return out


def comparar(a, b, items, rng=None):
    items = [i for i in items if i in a and i in b]
    x = np.array([a[i] for i in items])
    y = np.array([b[i] for i in items])
    d = x - y
    res = {"n": len(items), "r": float(np.corrcoef(x, y)[0, 1]) if len(items) > 2 else None,
           "abs_pp": float(100 * np.mean(np.abs(d))), "delta": float(50 * d.mean())}
    if rng is not None:
        bs = d[rng.integers(0, len(d), size=(B, len(d)))].mean(axis=1) * 50
        res["ic"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    return res


def cargar_rasgos():
    """{rasgo: (items, {modelo: elecciones})} para O, C, E, A (v3), H y N (I1)."""
    v = cargar_v3(rasgos=RASGOS_V3)
    ms = v["ms"]
    out = {t: (v["por_rasgo"][t], {m: v["elecciones"][m] for m in ms}) for t in RASGOS_V3}
    h = ahc.cargar([_i1(m) for m in ms])
    out["H"] = (ahc.ITEMS, {m: h["elecciones"][_i1(m)] for m in ms})
    n = anc.cargar_a([_i1(m) for m in ms])
    out["N"] = (anc.ITEMS_A, {m: n["elecciones"][_i1(m)] for m in ms})
    return out, ms


def calcular():
    rng = np.random.default_rng(SEMILLA)
    datos, ms = cargar_rasgos()
    otros = [m for m in ms if m not in (NAN, OR)]
    res = {}
    for t, (items, el) in datos.items():
        e = {m: fraccion(el[m]) for m in (NAN, OR, *otros) if el[m]}
        entre = comparar(e[NAN], e[OR], items, rng)
        retest = {m: comparar(fraccion(el[m], lambda o, r: r == 0),
                              fraccion(el[m], lambda o, r: r == 1), items)
                  for m in (NAN, OR)}
        vs = {o: comparar(e[OR], e[o], items) for o in otros if o in e}
        absd = sorted(x["abs_pp"] for x in vs.values())
        tope_retest = max(x["abs_pp"] for x in retest.values())
        if entre["abs_pp"] <= tope_retest + 2 and entre["ic"][0] <= 0 <= entre["ic"][1]:
            lectura = "despreciable"
        elif entre["abs_pp"] < absd[0]:
            lectura = "pequeño"
        else:
            lectura = "relevante"
        res[t] = {"proveedores": entre, "retest": retest,
                  "otros_mediana_abs_pp": float(np.median(absd)),
                  "otros_min_abs_pp": absd[0],
                  "otros_min_modelo": min(vs, key=lambda o: vs[o]["abs_pp"]),
                  "otros_mediana_r": float(np.median([x["r"] for x in vs.values()])),
                  "lectura": lectura}
    validez = {m: {k: vp.evaluar(m)[k] for k in ("nivel", "motivo", "valores")} for m in (NAN, OR)}
    return {"nan": NAN, "openrouter": OR, "panel_referencia": len(otros), "rasgos": res,
            "validez": validez}


def _f(x, d=2):
    return "—" if x is None else f"{x:.{d}f}".replace(".", ",")


def _validez(v):
    filas = "\n".join(
        f"| `{m}` | {_f(x['valores']['V1_delta'])} | {_f(x['valores']['V1_frac_A'])} | "
        f"{_f(x['valores']['V3_retest'])} | {_f(x['valores']['V4_coherencia'])} | {x['nivel']} |"
        for m, x in v.items())
    return f"""
## Validez (§41.2)

| Medición | Posición Δ AB−BA | \\|A − 0,5\\| | Retest | Coherencia de la deseabilidad | Nivel |
|---|---|---|---|---|---|
{filas}
"""


def escribir(r):
    filas = []
    for t, x in r["rasgos"].items():
        p, rt = x["proveedores"], x["retest"]
        filas.append(
            f"| {t} | {p['n']} | {_f(p['r'])} | {_f(p['abs_pp'], 1)} | "
            f"{_f(p['delta'], 1)} [{_f(p['ic'][0], 1)}; {_f(p['ic'][1], 1)}] | "
            f"{_f(rt[NAN]['abs_pp'], 1)} / {_f(rt[OR]['abs_pp'], 1)} | "
            f"{_f(x['otros_min_abs_pp'], 1)} ({x['otros_min_modelo']}) · {_f(x['otros_mediana_abs_pp'], 1)} | "
            f"{x['lectura']} |")
    md = f"""# DeepSeek V4 Pro 0813: NaN frente a OpenRouter

Mismo modelo, dos proveedores: `{NAN}` (NaN, que documenta la versión 0813) y
`deepseek/deepseek-v4-pro-0813` (OpenRouter, en el cuadro). La medición de
NaN no entra en el cuadro: se usa solo como réplica entre proveedores. Generado
por `comparar_proveedores_personalidad.py`; método y lectura en su cabecera.

Referencia: {r['panel_referencia']} modelos más del panel. |Δ| en puntos
porcentuales de elección del polo alto; Δ en la escala de las comparaciones
del cuadro (NaN − OpenRouter).

| Rasgo | Situaciones | r | \\|Δ\\| pp | Δ [IC 95 %] | Retest \\|Δ\\| NaN / OR | Otros modelos: mín. · mediana \\|Δ\\| | Lectura |
|---|---|---|---|---|---|---|---|
""" + "\n".join(filas) + "\n" + _validez(r["validez"])
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "PROVEEDORES_DEEPSEEK_V4_PRO.md").write_text(md, encoding="utf-8")
    (SALIDA / "proveedores_deepseek_v4_pro.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print(md)


if __name__ == "__main__":
    escribir(calcular())
