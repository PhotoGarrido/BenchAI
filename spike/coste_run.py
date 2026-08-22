"""Coste real de un run desde su manifiesto (solicitudes.jsonl) × precios.

Los precios son los de OpenRouter consultados el 26-07-2026 (USD por token).
Sirve para el piloto de coste del REGISTRO_GFINAL (regla presupuestaria 1) y
para auditar el gasto de cualquier run con manifiesto.

Uso: python coste_run.py resultados/gfinal_A_piloto_*/ [--proyectar 15 3]
     (--proyectar REPS DIAS: extrapola el piloto de 1 rep × 1 día)
"""

import argparse
import glob
import json
import pathlib

PRECIOS = {   # USD por millón de tokens (in, out) — OpenRouter 26-07-2026
    "x-ai/grok-4.5": (2.0, 6.0),
    "anthropic/claude-sonnet-5": (2.0, 10.0),
    "deepseek/deepseek-v3.2": (0.269, 0.4),
    "z-ai/glm-5.2": (0.669, 2.103),
    "anthropic/claude-opus-5": (5.0, 25.0),
    "anthropic/claude-opus-4.8": (5.0, 25.0),
    "google/gemini-3.1-flash-lite": (0.25, 1.5),
    "moonshotai/kimi-k3": (3.0, 15.0),
    "anthropic/claude-haiku-4.5": (1.0, 5.0),
    # OpenRouter 04-08-2026
    "deepseek/deepseek-v4-flash": (0.09, 0.18),
    "deepseek/deepseek-v4-flash-0731": (0.09, 0.18),
    # OpenRouter 21-08-2026 (cartera candidata)
    "google/gemini-3.7-flash": (0.375, 1.875),
    "qwen/qwen3.8-27b": (0.45, 3.20),
    "thinkingmachines/inkling-small": (0.45, 1.20),
    "stealth/ox-alpha": (0.0, 0.0),   # gratis en fase de preview
    "meta/muse-spark-1.2": (1.25, 4.25),
    "meta/muse-spark-1.2-contributor": (0.10, 0.20),
    "nvidia/nemotron-3-ultra-550b-a55b:free": (0.0, 0.0),
}


def coste_dir(d: pathlib.Path):
    f = d / "solicitudes.jsonl"
    if not f.exists():
        return None
    por_modelo = {}
    for linea in f.open(encoding="utf-8"):
        s = json.loads(linea)
        m = por_modelo.setdefault(s["modelo"], {"n": 0, "in": 0, "out": 0,
                                                "errores": 0})
        m["n"] += 1
        if s.get("error"):
            m["errores"] += 1
            continue
        t = s.get("tokens") or {}
        m["in"] += t.get("prompt") or 0
        m["out"] += t.get("completion") or 0
    return por_modelo


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--proyectar", nargs=2, type=int, metavar=("REPS", "DIAS"),
                    help="multiplica el coste del piloto (1 rep × 1 día)")
    args = ap.parse_args()

    factor = (args.proyectar[0] * args.proyectar[1]) if args.proyectar else 1
    total = 0.0
    for patron in args.dirs:
        for d in sorted(glob.glob(patron)):
            d = pathlib.Path(d)
            por_modelo = coste_dir(d)
            if por_modelo is None:
                print(f"{d}: sin solicitudes.jsonl")
                continue
            print(f"\n{d.name}:")
            for m, v in sorted(por_modelo.items()):
                pin, pout = PRECIOS.get(m, (None, None))
                if pin is None:
                    print(f"  {m:<40} n={v['n']} SIN PRECIO")
                    continue
                c = (v["in"] * pin + v["out"] * pout) / 1e6
                total += c * factor
                proy = f" → proyectado ×{factor}: ${c*factor:.2f}" if factor > 1 else ""
                print(f"  {m:<40} n={v['n']:>4} err={v['errores']}"
                      f" in={v['in']:>8} out={v['out']:>7} ${c:.3f}{proy}")
    print(f"\nTOTAL{' PROYECTADO' if factor > 1 else ''}: ${total:.2f}")


if __name__ == "__main__":
    main()
