"""Huella de un modelo: ¿sigue siendo el mismo detrás del mismo id?

NaN puede cambiar el modelo DETRÁS de un id sin cambiar el nombre ni lo que
devuelve la API (deepseek-v4-flash: 0731 → 4.1; aviso de otro cambio el
17-10-2026). La latencia y los tokens no lo delatan; la idea era que la conducta sí: se
repiten N juicios de deseabilidad ya hechos, con el MISMO prompt y la MISMA
semilla, y se cuenta cuántos coinciden.

AVISO (17-10-2026): con estos ítems la huella NO DISCRIMINA. El mismo modelo
repite 37-39/40, pero modelos distintos también coinciden 31-35/40 con las
respuestas antiguas de deepseek-v4-flash, y NaN confirmó ese día un cambio de
modelo que la huella no detectó (37/40 antes y después). No usar para fechar
cambios hasta rehacerla con ítems en los que los modelos discrepan.

Uso: python huella_modelo.py --modelo deepseek-v4-flash [--n 40] [--control gemma4]
Escribe una línea en resultados/huellas.jsonl. Sale con código 3 si la
coincidencia cae por debajo de --umbral (0,80): posible cambio de modelo.
"""

import argparse
import datetime
import json
import pathlib
import random
import threading

from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).parent / ".env")

import calibrar_deseabilidad as cal
import model_factory
from experimento_personalidad import TEMPERATURA, parsear_ab

AQUI = pathlib.Path(__file__).parent
REGISTRO = AQUI / "resultados" / "huellas.jsonl"


def huella(modelo_id, n):
    tareas = {t["id"]: t for t in cal.plan()}
    viejos = {}
    f = cal.SALIDA / modelo_id.replace("/", "_") / "registros.jsonl"
    for linea in f.read_text(encoding="utf-8").splitlines():
        r = json.loads(linea)
        # solo juicios del P0/P1 (los más antiguos): la referencia histórica
        if (r["estado"] == "OK" and r["id"] in tareas
                and r["id"].split("|")[1].startswith(("S", "P1"))):
            viejos[r["id"]] = r
    ids = random.Random(3).sample(sorted(viejos), n)
    mod = model_factory.build_model(False, modelo_id)
    igual = 0
    for i in ids:
        t = tareas[i]
        v, _ = parsear_ab(mod.sample_text(t["prompt"], max_tokens=60,
                                          temperature=TEMPERATURA, seed=t["seed"] % 2**31))
        igual += v == viejos[i]["valor"]
    return igual


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--control", default="gemma4")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--umbral", type=float, default=0.80)
    args = ap.parse_args()
    res = {}
    hs = [threading.Thread(target=lambda m=m: res.__setitem__(m, huella(m, args.n)))
          for m in (args.modelo, args.control)]
    [h.start() for h in hs]
    [h.join() for h in hs]
    linea = dict(ts=datetime.datetime.now().isoformat(timespec="seconds"), n=args.n,
                 modelo=args.modelo, coinciden=res[args.modelo],
                 control=args.control, coinciden_control=res[args.control])
    REGISTRO.parent.mkdir(exist_ok=True)
    with REGISTRO.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(linea, ensure_ascii=False) + "\n")
    print(json.dumps(linea, ensure_ascii=False))
    if res[args.modelo] / args.n < args.umbral:
        raise SystemExit(3)


if __name__ == "__main__":
    main()
