"""κ humana sobre G2 — la validación que el run G-final no pudo dar.

La κ del 27-07 sobre el G-final salió 0,32 porque su sonda estaba contaminada
por la consigna de formato (E4 del registro). Las interpretaciones de G2 son
paráfrasis genuinas (0/1.680 en formato-acción), así que la validación del
juez se hace aquí: muestra estratificada de 80 (40 actos abusivos de A2+C,
20 no abusivos de A2-prisión, 20 del dominio laboral C), juez versionado de
A4, hoja CIEGA nueva. La κ se calcula fusionando las 12 sondas de instrucción
NEUTRA de la ronda anterior (gfinal_juez), que David ya codificó a ciegas y
son el estrato de especificidad.

Salidas en resultados/g2_juez/: hoja_ciega.md · clave_privada.json ·
(tras el humano) kappa.json.

Uso: python juez_g2.py            # muestrea + juez + hoja
     python juez_g2.py --kappa hoja_rellena.json
"""

import argparse
import hashlib
import json
import pathlib
import random

from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).parent / ".env")

from a4_validacion import JUEZ_MODELO, JUEZ_PARAMS, JUEZ_PROMPT, RUBRICA
from juez_gfinal import juzgar, kappa

RES = pathlib.Path(__file__).parent / "resultados"
SEED = 20260727
NEUTROS = RES / "gfinal_juez"   # clave y hoja rellena de la ronda anterior


def _id(r):
    clave = (f"g2|{r['modelo']}|{r.get('fase')}|{r.get('contenido')}|"
             f"{r.get('fuente')}|{r.get('negativa')}|{r.get('rep')}|"
             f"{r['dia']}|{r['supervisor']}")
    return hashlib.sha1(clave.encode()).hexdigest()[:12]


def cargar(pref):
    d = sorted(RES.glob(f"g2_{pref}_2*"))[-1]
    regs = [json.loads(l) for f in sorted(d.glob("registros_*.jsonl"))
            for l in f.open(encoding="utf-8")]
    return [r for r in regs if r.get("interpretacion")], d.name


def muestrear(rng):
    a2, org_a2 = cargar("a2")
    c, org_c = cargar("c")
    for r in a2:
        r["_dominio"] = "prision"
    for r in c:
        r["_dominio"] = "laboral"
    todos = a2 + c
    abus = [r for r in todos if (r["nivel"] or 0) >= 3]
    noab_p = [r for r in a2 if r["nivel"] is not None and r["nivel"] < 3]
    lab = [r for r in c if r["nivel"] is not None]
    m = (rng.sample(abus, 40) + rng.sample(noab_p, 20) + rng.sample(lab, 20))
    vistos, unicos = set(), []
    for r in m:
        i = _id(r)
        if i not in vistos:
            vistos.add(i)
            unicos.append(dict(r, _id=i))
    rng.shuffle(unicos)
    return unicos, (org_a2, org_c)


def cargar_neutros():
    """Las 12 sondas neutras de la ronda G-final: veredicto del juez de la
    clave + etiqueta humana de la hoja rellena (codificada a ciegas el 27-07)."""
    clave = json.loads((NEUTROS / "clave_privada.json").read_text())
    hoja = {h["id"]: h["humano"] for h in json.loads(
        (NEUTROS / "hoja_rellena.json").read_text())}
    return [{"id": r["id"], "estrato": "neutro", "juez": r["juez"],
             "humano": hoja.get(r["id"]), "nivel": r["nivel"]}
            for r in clave["registros"] if r["estrato"] == "neutro"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kappa", default=None)
    args = ap.parse_args()
    outdir = RES / "g2_juez"
    outdir.mkdir(exist_ok=True)

    if args.kappa:
        clave = json.loads((outdir / "clave_privada.json").read_text())
        hoja = {h["id"]: h["humano"] for h in json.loads(
            pathlib.Path(args.kappa).read_text())}
        filas = [{"estrato": r["estrato"], "nivel": r["nivel"],
                  "juez": r["juez"], "humano": hoja.get(r["id"])}
                 for r in clave["registros"]] + cargar_neutros()
        j = [f["juez"] for f in filas]
        h = [f["humano"] for f in filas]
        k = kappa(j, h)
        pares = [(x, y) for x, y in zip(j, h)
                 if x is not None and y is not None]
        acuerdo = sum(x == y for x, y in pares) / len(pares)
        por_estrato = {}
        for est in ("abusiva", "no_abusiva", "laboral", "neutro"):
            fs = [f for f in filas if f["estrato"] == est
                  and f["humano"] is not None and f["juez"] is not None]
            if fs:
                por_estrato[est] = {
                    "n": len(fs),
                    "acuerdo": round(sum(f["juez"] == f["humano"]
                                         for f in fs) / len(fs), 3),
                    "juez_si": sum(f["juez"] for f in fs),
                    "humano_si": sum(f["humano"] for f in fs)}
        salida = {"kappa": k, "acuerdo": round(acuerdo, 3), "n": len(pares),
                  "incluye_neutros_ronda_gfinal": True,
                  "por_estrato": por_estrato}
        (outdir / "kappa.json").write_text(
            json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(salida, ensure_ascii=False, indent=2))
        return

    rng = random.Random(SEED)
    muestra, origenes = muestrear(rng)
    veredictos = juzgar(muestra)

    hoja = ["# Hoja de etiquetado a ciegas — κ sobre G2",
            "", f"Rúbrica: {RUBRICA}", "",
            "Misma rúbrica y manual que la ronda anterior"
            " (manual_codificacion.md). No abras clave_privada.json.", ""]
    clave = []
    for r, v in zip(muestra, veredictos):
        estrato = ("laboral" if r["_dominio"] == "laboral"
                   and (r["nivel"] or 0) < 3 else
                   "abusiva" if (r["nivel"] or 0) >= 3 else "no_abusiva")
        hoja += [f"## {r['_id']}", "", r["interpretacion"].strip(), "",
                 "**Respuesta: [ ] SÍ · [ ] NO**", ""]
        clave.append({"id": r["_id"], "modelo": r["modelo"],
                      "fase": r.get("fase"), "dominio": r["_dominio"],
                      "contenido": r.get("contenido"),
                      "fuente": r.get("fuente"), "nivel": r["nivel"],
                      "estrato": estrato, "juez": v,
                      "interpretacion": r["interpretacion"]})
    (outdir / "hoja_ciega.md").write_text("\n".join(hoja), encoding="utf-8")
    (outdir / "clave_privada.json").write_text(json.dumps(
        {"origenes": origenes, "seed": SEED, "rubrica": RUBRICA,
         "juez": {"modelo": JUEZ_MODELO, "params": JUEZ_PARAMS,
                  "prompt": JUEZ_PROMPT},
         "registros": clave}, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = [c for c in clave if c["juez"] is not None]
    for est in ("abusiva", "no_abusiva", "laboral"):
        fs = [c for c in ok if c["estrato"] == est]
        if fs:
            print(f"juez SÍ · {est:10}: {sum(c['juez'] for c in fs)}/{len(fs)}")
    print(f"Hoja ciega ({len(clave)} ítems nuevos; los 12 neutros se fusionan"
          f" en la κ): {outdir/'hoja_ciega.md'}")


if __name__ == "__main__":
    main()
