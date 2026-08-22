"""Coste proyectado de una batería EN VUELO, desde sus propios registros.

Por qué existe (22-08-2026): estimar el coste de un modelo con la
verbosidad de otro falla estrepitosamente. Muse Spark 1.2 genera 1.038
tokens de salida por llamada y ox-alpha 211 — cinco veces menos —, así que
su batería costaba 22 $ donde la referencia predecía 7. La proyección
honesta solo se puede hacer con los registros DEL PROPIO MODELO, y por eso
esto se mira a los pocos cientos de llamadas y no al final.

Uso:
  python proyectar_coste.py resultados/bateria_X
  python proyectar_coste.py resultados/bateria_X --tope 8   # sale 1 si se pasa
"""

import argparse
import glob
import json
import pathlib

import coste_run

#: Llamadas de una suite v0.4 completa (medido en la batería de ox-alpha).
LLAMADAS_SUITE = 4536


def acumular(batch: pathlib.Path):
    datos = {}
    for p in glob.glob(str(batch / "*" / "solicitudes.jsonl")):
        for linea in pathlib.Path(p).open(encoding="utf-8"):
            f = json.loads(linea)
            if f.get("error"):
                continue
            t = f.get("tokens") or {}
            d = datos.setdefault(f.get("modelo"),
                                 {"n": 0, "in": 0, "out": 0})
            d["n"] += 1
            d["in"] += t.get("prompt") or 0
            d["out"] += t.get("completion") or 0
    return datos


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("batch")
    ap.add_argument("--tope", type=float, default=None,
                    help="USD por modelo: sale con código 1 si alguna "
                         "proyección lo supera")
    args = ap.parse_args()

    batch = pathlib.Path(args.batch)
    if not batch.is_dir():
        raise SystemExit(f"[proyectar] no existe {batch}")
    datos = acumular(batch)
    if not datos:
        raise SystemExit(f"[proyectar] sin solicitudes en {batch}")

    print(f"{'modelo':<34} {'hechas':>7} {'out/llam':>9} {'gastado':>9} "
          f"{'PROYECTADO':>11}")
    print("-" * 74)
    pasados = []
    for m, d in sorted(datos.items()):
        pin, pout = coste_run.PRECIOS.get(m, (None, None))
        out_ll = d["out"] / d["n"]
        if pin is None:
            print(f"{m:<34} {d['n']:>7} {out_ll:>9.0f} {'SIN PRECIO':>9}"
                  f" {'—':>11}")
            continue
        gastado = (d["in"] * pin + d["out"] * pout) / 1e6
        proy = gastado * LLAMADAS_SUITE / d["n"]
        marca = ""
        if args.tope is not None and proy > args.tope:
            marca = "  <<< SOBRE EL TOPE"
            pasados.append((m, proy))
        print(f"{m:<34} {d['n']:>7} {out_ll:>9.0f} ${gastado:>8.3f} "
              f"${proy:>10.2f}{marca}")

    if d and datos:
        # La proyección es fiable a partir de unos cientos de llamadas: las
        # primeras son de Asch, el bloque de contexto más corto.
        pocas = [m for m, d in datos.items() if d["n"] < 200]
        if pocas:
            print(f"\n[aviso] con menos de 200 llamadas la proyección baila: "
                  f"{', '.join(pocas)}")
    if pasados:
        print(f"\n[TOPE] {len(pasados)} modelo(s) sobre {args.tope} $ por "
              "batería: decide si sigue o se para (las baterías son "
              "reanudables con --reanudar).")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
