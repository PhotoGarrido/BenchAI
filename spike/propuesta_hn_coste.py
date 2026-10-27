"""Coste estimado de pasar la propuesta de H y N (PERSONALIDAD.md §31) a los 7 externos.

No mide nada ni llama a modelos: usa los tokens medios por llamada que
registró cada externo en la pasada v3 (solicitudes.jsonl de intento_v3_*) y
la tarifa de coste_run.py. Los modelos sin tarifa fijada reciben, en
proporción a sus tokens, lo que falta hasta el gasto real del v3 (≈ 5,0 $,
§23), como en analizar_v31_en.py (§25).

Cada formato lleva sus llamadas por modelo y un factor de tokens de entrada
y de salida frente a una llamada v3 (p. ej. la conversación de dos turnos
lleva ≈ 2,5× de entrada).

Uso (desde spike/): python propuesta_hn_coste.py
  → resultados/personalidad_fc/PROPUESTA_HN_COSTE.md y propuesta_hn_coste.json
"""

import json

import analizar_personalidad_p1 as ap1
import coste_run
from analizar_v3 import SALIDA

EXTERNOS = ("anthropic/claude-haiku-5.5", "anthropic/claude-opus-5.5#low",
            "google/gemini-3.7-flash", "google/gemini-4-argon", "openai/gpt-5.6-luna",
            "openai/gpt-6.1-sol#low", "deepseek/deepseek-v4-pro-0813")
GASTO_V3_REAL = 5.0
MARGEN = 1.25
SALDO = (1.2, 1.5)
#: formato: (rasgo, llamadas por modelo en los externos, factor entrada, factor salida, descripción)
FORMATOS = {
    "HE": ("H", 16 * 5 * 2, 1.2, 1.0, "escalera de tentación: 16 situaciones × 5 niveles × 2 órdenes"),
    "HD": ("H", 8 * 2, 1.0, 1.0, "reparto tipo dictador: 8 variantes × 2 réplicas"),
    "HM": ("H", 8 * 2, 1.0, 1.0, "informe con incentivo a mentir: 8 escenarios × 2 réplicas"),
    "HO": ("H", 36, 0.8, 1.0, "sobreafirmación: 36 términos (24 reales, 12 inexistentes)"),
    "NG": ("N", 36 * 2, 1.0, 1.0, "intensidad graduada: 36 situaciones × 2 réplicas"),
    "NS": ("N", 12 * 2 + 12 * 4, 1.0, 1.0, "dos opciones serenas: 12 seleccionadas × (2 deseab. + 4 R3)"),
    "NC": ("N", 12 * 2 * 2, 2.5, 1.0, "crítica o fracaso en dos turnos: 12 × 2 tipos × 2 réplicas"),
}


def tokens_v3():
    out = {}
    for m in EXTERNOS:
        e = m.replace("/", "_")
        n = tin = tout = 0
        for base in (ap1.DIR, ap1.CAL):
            for f in (base / e).glob("intento_v3_*/solicitudes.jsonl"):
                for linea in f.open(encoding="utf-8"):
                    t = json.loads(linea).get("tokens") or {}
                    n += 1
                    tin += t.get("prompt") or 0
                    tout += t.get("completion") or 0
        out[m] = (n, tin, tout)
    return out


def coste_por_llamada():
    """{modelo: (coste medio de una llamada v3, inferido?)}"""
    tok = tokens_v3()
    conocido, filas = 0.0, {}
    for m, (n, tin, tout) in tok.items():
        pin, pout = coste_run.precio(m)
        c = None if pin is None else (tin * pin + tout * pout) / 1e6
        filas[m] = [n, tin, tout, c, pin, pout]
        conocido += c or 0
    resto = max(0.0, GASTO_V3_REAL - conocido)
    desc = sum(f[1] + f[2] for f in filas.values() if f[3] is None)
    out = {}
    for m, (n, tin, tout, c, pin, pout) in filas.items():
        inferido = c is None
        if inferido:
            c = resto * (tin + tout) / desc if desc else 0.0
        # Precio efectivo por token de entrada y de salida (inferido: mismo reparto 1:5 que la mediana)
        if inferido:
            pin_e = c / (tin + 5 * tout) * 1e6 if tin + tout else 0
            pout_e = 5 * pin_e
        else:
            pin_e, pout_e = pin, pout
        out[m] = {"n_v3": n, "in_medio": tin / n if n else 0, "out_medio": tout / n if n else 0,
                  "coste_v3": c, "pin": pin_e, "pout": pout_e, "inferido": inferido}
    return out


def main():
    base = coste_por_llamada()
    tabla = {}
    for m, b in base.items():
        tabla[m] = {}
        for k, (_, n, fi, fo, _d) in FORMATOS.items():
            tabla[m][k] = n * (b["in_medio"] * fi * b["pin"] + b["out_medio"] * fo * b["pout"]) / 1e6
    tot = {k: sum(tabla[m][k] for m in tabla) for k in FORMATOS}
    L = ["# Coste estimado de la propuesta H/N en los 7 externos (PERSONALIDAD.md §31)", "",
         "Generado por `propuesta_hn_coste.py` con los tokens medios por llamada de la pasada v3"
         f" y la tarifa de `coste_run.py`; sin tarifa fijada (\\*), reparto del resto del gasto real"
         f" del v3 ({GASTO_V3_REAL} $) en proporción a los tokens. Sin llamadas a modelos.", "",
         "| formato | rasgo | llamadas por modelo | descripción |", "|---|---|---|---|"]
    for k, (t, n, fi, fo, d) in FORMATOS.items():
        L.append(f"| {k} | {t} | {n} | {d} (tokens de entrada ×{fi}) |")
    L += ["", "| modelo | tokens medios v3 entrada/salida | " + " | ".join(FORMATOS) + " | total |",
          "|---|---|" + "---|" * (len(FORMATOS) + 1)]
    for m, b in base.items():
        marca = " \\*" if b["inferido"] else ""
        L.append(f"| {m}{marca} | {b['in_medio']:.0f} / {b['out_medio']:.0f} | "
                 + " | ".join(f"{tabla[m][k]:.3f}" for k in FORMATOS) + f" | {sum(tabla[m].values()):.2f} |")
    L.append("| **total** | | " + " | ".join(f"**{tot[k]:.2f}**" for k in FORMATOS)
             + f" | **{sum(tot.values()):.2f}** |")
    h = sum(v for k, v in tot.items() if FORMATOS[k][0] == "H")
    n = sum(v for k, v in tot.items() if FORMATOS[k][0] == "N")
    L += ["", f"H completo ≈ {h:.2f} $ ({MARGEN * h:.2f} $ con margen); N completo ≈ {n:.2f} $"
          f" ({MARGEN * n:.2f} $); todo ≈ {h + n:.2f} $ ({MARGEN * (h + n):.2f} $). Saldo de OpenRouter:"
          f" ≈ {SALDO[0]}–{SALDO[1]} $."]
    (SALIDA / "PROPUESTA_HN_COSTE.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (SALIDA / "propuesta_hn_coste.json").write_text(json.dumps(
        {"formatos": {k: {"rasgo": t, "llamadas": n, "factor_in": fi, "factor_out": fo, "descripcion": d}
                      for k, (t, n, fi, fo, d) in FORMATOS.items()},
         "base_v3": base, "coste": tabla, "total_formato": tot, "total_H": h, "total_N": n,
         "margen": MARGEN}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
