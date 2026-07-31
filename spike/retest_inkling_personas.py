"""Sonda causal de la perseveración de inkling: ¿perfil o persona?

El re-test confirmó que inkling clava la tarea con 3 sujetos pero persevera
(CCCCCC) con Marcos Uría (a=90, n=85, 52 años, educación básica). Cuatro
sondas de 6 rondas en solitario para aislar el disparador:

  clon      mismo Big Five y demografía que Marcos, otro nombre
  irene     alta A+N ya existente (a=85 n=80) pero joven y ed. media
  alta_n    solo neuroticismo alto (n=85, a=50)
  alta_a    solo amabilidad alta (a=90, n=30)

Lectura: si falla el clon pero no el resto → la combinación A+N extrema con
esa demografía; si falla también irene → el perfil A+N basta; si no falla
nadie → era algo del texto exacto de la persona de Marcos.

Uso: python retest_inkling_personas.py --modelo thinkingmachines/inkling
"""

import argparse
import datetime
import json
import pathlib

from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).parent / ".env")

import manifiesto
import model_factory
import experimento_asch as asch
import tiento

SONDAS = [
    ("clon", {"nombre": "Víctor Casal",
              "big5": {"o": 35, "c": 50, "e": 50, "a": 90, "n": 85},
              "demografia": {"edad": 52, "genero": "hombre",
                             "origen_cultural": "local", "nse": "bajo",
                             "educacion": "básica"}}),
    ("irene", asch.SUJETOS[0]),
    ("alta_n", {"nombre": "Teresa Nublo",
                "big5": {"o": 50, "c": 50, "e": 50, "a": 50, "n": 85},
                "demografia": {"edad": 34, "genero": "mujer",
                               "origen_cultural": "local", "nse": "medio",
                               "educacion": "superior"}}),
    ("alta_a", {"nombre": "Ramón Cietes",
                "big5": {"o": 50, "c": 50, "e": 50, "a": 90, "n": 30},
                "demografia": {"edad": 45, "genero": "hombre",
                               "origen_cultural": "local", "nse": "medio",
                               "educacion": "media"}}),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modelo", required=True)
    parser.add_argument("--out", default="resultados")
    args = parser.parse_args()

    # Manifiesto por solicitud (reauditoría 31-07, inventario A): el outdir
    # nace ANTES de la primera llamada; microsegundos contra colisiones.
    outdir = pathlib.Path(args.out) / datetime.datetime.now().strftime(
        "retest_personas_%Y%m%d_%H%M%S_%f")
    outdir.mkdir(parents=True, exist_ok=True)
    manifiesto.activar(outdir, vars(args))

    modelo = tiento.Medidor(model_factory.build_model(
        dry_run=False, model_name=args.modelo))
    resumen = {"modelo": args.modelo, "sondas": {}}
    registros = []
    for clave, sujeto in SONDAS:
        regs = tiento.sesion_pares(modelo, sujeto, "control",
                                   seed=1009, total=6)  # mismos estímulos
        registros += regs
        respuestas = [r["publica"] for r in regs]
        moda = max(set(respuestas), key=respuestas.count)
        resumen["sondas"][clave] = {
            "sujeto": sujeto["nombre"],
            "validez": round(sum(r["acierto"] for r in regs) / 6, 2),
            "respuestas": respuestas,
            "persevera": respuestas.count(moda) >= 5,
        }
        print(clave, resumen["sondas"][clave], flush=True)

    with (outdir / "registros.jsonl").open("w", encoding="utf-8") as f:
        for r in registros:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (outdir / "resumen.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGuardado en {outdir}")


if __name__ == "__main__":
    try:
        main()
        manifiesto.cerrar_activo()
    except BaseException as _e:
        manifiesto.cerrar_activo("failed",
                                 {"exception_type": type(_e).__name__})
        raise
