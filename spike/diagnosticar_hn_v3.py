"""Diagnóstico de H y N con la conducta comparada de §28 (PERSONALIDAD.md §30).

Solo datos ya medidos (banco v3, 13 modelos), sin llamadas a modelos. Todo se
calcula sobre la elección bruta e_m(i) (fracción de veces que elige el polo
alto), que es lo que compara §28; entre modelos da lo mismo que e − d̄ porque
d̄ es común. O, C, E y A se incluyen como referencia.

Por rasgo, en la escala del cuadro (×50):
  - componentes de varianza (ANOVA de dos vías modelos × situaciones, sin
    réplica): sd real entre modelos y ruido por situación; alfa de Hoyt;
  - G4 tal como se publica (mitades pares/impares) y su distribución en 2.000
    particiones aleatorias equilibradas por faceta;
  - techo/suelo de la elección bruta;
  - correlación ítem-resto entre modelos;
  - por faceta: señal, alfa, correlación con el resto del rasgo y carga cruzada;
  - matriz de correlación entre facetas (subdimensiones);
  - por qué cambia G4 al pasar de la puntuación ajustada (e − d_m) a la
    comparada (e): G4 de e, de e − d_m y de d_m solo, y correlación entre la
    elección media y la deseabilidad media de cada modelo.

Uso (desde spike/): python diagnosticar_hn_v3.py
  → resultados/personalidad_fc/DIAGNOSTICO_HN.md y diagnostico_hn.json
"""

import json

import numpy as np

from analizar_discriminacion import _id
from analizar_personalidad import SEMILLA
from analizar_v3 import RASGOS, SALIDA, cargar_v3, g4_consistencia, puntuar
from cuadro_personalidad import NOMBRE

N_PART = 2000


def matriz(a, ms, items):
    """Modelos × situaciones."""
    return np.array([[a[m][i] for i in items] for m in ms], float)


def hoyt(X):
    """(sd entre modelos, ruido por situación, alfa de Hoyt) en la escala del cuadro."""
    n_m, n_i = X.shape
    gm = X.mean()
    ms_m = n_i * ((X.mean(1) - gm) ** 2).sum() / (n_m - 1)
    res = X - X.mean(1, keepdims=True) - X.mean(0, keepdims=True) + gm
    ms_r = (res ** 2).sum() / ((n_m - 1) * (n_i - 1))
    sd_m = 50 * np.sqrt(max(0.0, (ms_m - ms_r) / n_i))
    return float(sd_m), float(50 * np.sqrt(ms_r)), float(1 - ms_r / ms_m) if ms_m else None


def sb(h1, h2):
    r = np.corrcoef(h1, h2)[0, 1]
    return float(2 * r / (1 + r)) if np.isfinite(r) and r > -1 else float("nan")


def particiones_faceta(items, faceta_de, rng, n=N_PART):
    por_f = {}
    for i in items:
        por_f.setdefault(faceta_de[i], []).append(i)
    out = []
    for _ in range(n):
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


def sb_particiones(X, idx, partes):
    vals = []
    for h1, h2 in partes:
        vals.append(sb(X[:, [idx[i] for i in h1]].mean(1), X[:, [idx[i] for i in h2]].mean(1)))
    v = np.array(vals)
    v = v[np.isfinite(v)]
    return {"mediana": float(np.median(v)), "p05": float(np.percentile(v, 5)),
            "p95": float(np.percentile(v, 95)), "frac_ge_070": float((v >= .70).mean())}


def item_resto(X):
    out = []
    for j in range(X.shape[1]):
        resto = np.delete(X, j, axis=1).mean(1)
        x = X[:, j]
        out.append(float(np.corrcoef(x, resto)[0, 1]) if x.std() and resto.std() else float("nan"))
    return np.array(out)


def calcular():
    rng = np.random.default_rng(SEMILLA)
    v = cargar_v3()
    ms, por_rasgo, des, el = v["ms"], v["por_rasgo"], v["des"], v["elecciones"]
    faceta_de = v["faceta_de"]
    e = {m: puntuar(el[m]) for m in ms}                       # elección bruta (§28)
    adj = {m: puntuar(el[m], des[m]) for m in ms}            # ajustada por el ideal propio
    dm = {m: {i: des[m][i] for i in v["comunes"]} for m in ms}  # deseabilidad propia
    totales = {t: matriz(e, ms, por_rasgo[t]).mean(1) for t in RASGOS}
    res = {"modelos": ms, "n_situaciones": {t: len(x) for t, x in por_rasgo.items()}, "rasgos": {}}
    for t in RASGOS:
        it = por_rasgo[t]
        idx = {i: k for k, i in enumerate(it)}
        X = matriz(e, ms, it)
        sd_m, ruido, alfa = hoyt(X)
        partes = particiones_faceta(it, faceta_de, rng)
        media_i = X.mean(0)
        sd_i = X.std(0)
        ir = item_resto(X)
        # Facetas
        facs = sorted({faceta_de[i] for i in it})
        fac = {}
        for f in facs:
            fi = [i for i in it if faceta_de[i] == f]
            Xf = X[:, [idx[i] for i in fi]]
            resto = X[:, [idx[i] for i in it if faceta_de[i] != f]].mean(1)
            sc = Xf.mean(1)
            cruz = {u: float(np.corrcoef(sc, totales[u])[0, 1]) for u in RASGOS if u != t}
            u_max = max(cruz, key=lambda u: abs(cruz[u]))
            sdf, _, af = hoyt(Xf)
            fac[f] = {"n": len(fi), "sd_modelos": sdf, "alfa": af,
                      "media_eleccion": float(Xf.mean()),
                      "r_resto_rasgo": float(np.corrcoef(sc, resto)[0, 1]),
                      "carga_cruzada": [u_max, cruz[u_max]],
                      "ir_medio": float(np.nanmean(ir[[idx[i] for i in fi]])),
                      "score": sc.tolist()}
        corr_f = {f"{f1}|{f2}": float(np.corrcoef(fac[f1]["score"], fac[f2]["score"])[0, 1])
                  for k, f1 in enumerate(facs) for f2 in facs[k + 1:]}
        # Ajustada frente a comparada
        A = matriz(adj, ms, it)
        D = matriz(dm, ms, it)
        r_ed = float(np.corrcoef(X.mean(1), D.mean(1))[0, 1])
        res["rasgos"][t] = {
            "sd_modelos": sd_m, "ruido_situacion": ruido, "alfa": alfa,
            "sd_modelos_ajustada": hoyt(A)[0], "alfa_ajustada": hoyt(A)[2],
            "sd_modelos_deseab": hoyt(D)[0], "alfa_deseab": hoyt(D)[2],
            "G4_pares_impares": None,  # se rellena abajo con g4_consistencia
            "G4_particiones": sb_particiones(X, idx, partes),
            "G4_particiones_ajustada": sb_particiones(A, idx, partes),
            "G4_particiones_deseab": sb_particiones(D, idx, partes),
            "r_eleccion_deseab_modelo": r_ed,
            "sd_eleccion_media": float(50 * X.mean(1).std(ddof=1)),
            "sd_deseab_media": float(50 * D.mean(1).std(ddof=1)),
            "techo_suelo": {"media_eleccion": float(media_i.mean()),
                            "frac_media_lt_010": float((media_i < .10).mean()),
                            "frac_media_gt_090": float((media_i > .90).mean()),
                            "frac_sd_lt_010": float((sd_i < .10).mean()),
                            "frac_sin_varianza": float((sd_i == 0).mean())},
            "item_resto": {"media": float(np.nanmean(ir)), "frac_neg": float(np.nanmean(ir < 0)),
                           "frac_ge_020": float(np.nanmean(ir >= .20)),
                           "por_item": {i: (None if np.isnan(ir[k]) else float(ir[k]))
                                        for k, i in enumerate(it)}},
            "facetas": fac, "corr_facetas": corr_f}
    g4 = {"comparada": g4_consistencia(e, ms, por_rasgo), "ajustada": g4_consistencia(adj, ms, por_rasgo),
          "deseab": g4_consistencia(dm, ms, por_rasgo)}
    for t in RASGOS:
        res["rasgos"][t]["G4_pares_impares"] = {k: g4[k][t] for k in g4}
    # Perfil por modelo en H y N (elección media, deseabilidad media), escala ×50
    res["perfil"] = {t: {_id(m): {"eleccion": 50 * float(np.mean([e[m][i] for i in por_rasgo[t]])),
                                  "deseab_propia": 50 * float(np.mean([dm[m][i] for i in por_rasgo[t]]))}
                         for m in ms} for t in ("H", "N")}
    return res


def escribir(r):
    R = r["rasgos"]
    f2 = lambda x: "—" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:+.2f}"  # noqa: E731
    L = ["# Diagnóstico de H y N con la conducta comparada (PERSONALIDAD.md §30)", "",
         f"Generado por `diagnosticar_hn_v3.py`. {len(r['modelos'])} modelos del banco v3; elección bruta"
         f" (§28). Semilla {SEMILLA}. Sin llamadas a modelos. Escala del cuadro (×50).", "",
         "## 1. Señal, ruido y consistencia por rasgo", "",
         "| rasgo | sd entre modelos | ruido por situación | alfa | G4 pares/impares | G4 en 2.000 particiones: mediana [p5, p95] | % particiones ≥ 0,70 |",
         "|---|---|---|---|---|---|---|"]
    for t in RASGOS:
        x = R[t]
        p = x["G4_particiones"]
        L.append(f"| {t} | {x['sd_modelos']:.1f} | {x['ruido_situacion']:.1f} | {x['alfa']:.2f} |"
                 f" {x['G4_pares_impares']['comparada']:.2f} | {p['mediana']:.2f} [{p['p05']:.2f}, {p['p95']:.2f}] |"
                 f" {100 * p['frac_ge_070']:.0f} % |")
    L += ["", "## 2. Techo, suelo e ítem-resto (elección bruta)", "",
          "| rasgo | elección media | % ítems media < 0,10 | % > 0,90 | % sd entre modelos < 0,10 | % sin varianza | r ítem-resto media | % r < 0 | % r ≥ 0,20 |",
          "|---|---|---|---|---|---|---|---|---|"]
    for t in RASGOS:
        ts, ir = R[t]["techo_suelo"], R[t]["item_resto"]
        L.append(f"| {t} | {ts['media_eleccion']:.2f} | {100 * ts['frac_media_lt_010']:.0f} | {100 * ts['frac_media_gt_090']:.0f} |"
                 f" {100 * ts['frac_sd_lt_010']:.0f} | {100 * ts['frac_sin_varianza']:.0f} | {ir['media']:+.2f} |"
                 f" {100 * ir['frac_neg']:.0f} | {100 * ir['frac_ge_020']:.0f} |")
    L += ["", "## 3. Ajustada (e − d_m) frente a comparada (e)", "",
          "La puntuación ajustada resta a la elección la deseabilidad propia d_m(i). Su varianza entre"
          " modelos es la de la elección, más la de la deseabilidad, menos dos veces su covarianza.", "",
          "| rasgo | G4 comparada (e) | G4 ajustada (e − d_m) | G4 de d_m sola | mediana particiones: e / e − d_m / d_m | sd entre modelos: e / e − d_m / d_m | r(elección media, deseab. media) |",
          "|---|---|---|---|---|---|---|"]
    for t in RASGOS:
        x = R[t]
        g = x["G4_pares_impares"]
        L.append(f"| {t} | {g['comparada']:.2f} | {g['ajustada']:.2f} | {g['deseab']:.2f} |"
                 f" {x['G4_particiones']['mediana']:.2f} / {x['G4_particiones_ajustada']['mediana']:.2f} /"
                 f" {x['G4_particiones_deseab']['mediana']:.2f} |"
                 f" {x['sd_modelos']:.1f} / {x['sd_modelos_ajustada']:.1f} / {x['sd_modelos_deseab']:.1f} |"
                 f" {x['r_eleccion_deseab_modelo']:+.2f} |")
    L += ["", "## 4. Facetas", "",
          "sd = sd real entre modelos de la faceta; r resto = correlación entre modelos de la faceta con el"
          " resto del rasgo; carga cruzada = rasgo ajeno con el que más correlaciona.", "",
          "| rasgo | faceta | n | elección media | sd | alfa | r resto del rasgo | ítem-resto medio | carga cruzada |",
          "|---|---|---|---|---|---|---|---|---|"]
    for t in RASGOS:
        for f, x in R[t]["facetas"].items():
            u, c = x["carga_cruzada"]
            L.append(f"| {t} | {f} | {x['n']} | {x['media_eleccion']:.2f} | {x['sd_modelos']:.1f} |"
                     f" {f2(x['alfa'])} | {f2(x['r_resto_rasgo'])} | {f2(x['ir_medio'])} | {u} {c:+.2f} |")
    for t in ("H", "N"):
        facs = list(R[t]["facetas"])
        L += ["", f"### Correlación entre facetas de {NOMBRE[t]} (entre modelos)", "",
              "| | " + " | ".join(f[:10] for f in facs) + " |", "|---|" + "---|" * len(facs)]
        for f1 in facs:
            fila = []
            for f2_ in facs:
                if f1 == f2_:
                    fila.append("1")
                else:
                    k = f"{f1}|{f2_}" if f"{f1}|{f2_}" in R[t]["corr_facetas"] else f"{f2_}|{f1}"
                    fila.append(f"{R[t]['corr_facetas'][k]:+.2f}")
            L.append(f"| {f1} | " + " | ".join(fila) + " |")
    L += ["", "## 5. Perfil por modelo en H y N (×50)", "",
          "| modelo | H elección | H deseab. propia | N elección | N deseab. propia |", "|---|---|---|---|---|"]
    for m in r["perfil"]["H"]:
        h, n = r["perfil"]["H"][m], r["perfil"]["N"][m]
        L.append(f"| {m} | {h['eleccion']:.1f} | {h['deseab_propia']:.1f} | {n['eleccion']:.1f} | {n['deseab_propia']:.1f} |")
    (SALIDA / "DIAGNOSTICO_HN.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    for t in RASGOS:
        for x in r["rasgos"][t]["facetas"].values():
            x.pop("score")
    (SALIDA / "diagnostico_hn.json").write_text(json.dumps(r, ensure_ascii=False, indent=2, default=float),
                                                encoding="utf-8")
    return L


if __name__ == "__main__":
    print("\n".join(escribir(calcular())))
