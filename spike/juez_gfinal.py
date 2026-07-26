"""O4 · Juez de interpretaciones del G-final + hoja CIEGA para el humano.

Según REGISTRO_GFINAL.md: muestra estratificada de 80 interpretaciones —
40 de actos abusivos (nivel≥3), 20 de actos no abusivos en prisión, 20 del
dominio laboral — juzgadas por el juez versionado de A4 (gemini-flash-lite,
temp 0, misma rúbrica). Produce:

  gfinal_juez/juez_completo.json      todos los veredictos + procedencia
  gfinal_juez/hoja_ciega.md           SOLO texto + casilla, orden barajado,
                                      sin modelo/celda/nivel/veredicto — es
                                      lo único que debe abrir el codificador
                                      humano antes de etiquetar
  gfinal_juez/clave_privada.json      mapeo id→metadatos y veredicto del juez
                                      (NO abrir hasta terminar la hoja)

κ de Cohen: cuando la hoja vuelva rellena, `--kappa hoja_rellena.json`.

Uso: python juez_gfinal.py [--dir DIR_A] [--kappa FICHERO]
"""

import argparse
import hashlib
import json
import os
import pathlib
import random
import re
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).parent / ".env")

from a4_validacion import JUEZ_MODELO, JUEZ_PARAMS, JUEZ_PROMPT, RUBRICA

RES = pathlib.Path(__file__).parent / "resultados"
SEED = 20260726


def _id(r):
    clave = (f"{r['modelo']}|{r['dominio']}|{r['contenido']}|{r['clausula']}|"
             f"{r['marco']}|{r['rep']}|{r['dia']}|{r['supervisor']}")
    return hashlib.sha1(clave.encode()).hexdigest()[:12]


def cargar_a(explicito=None):
    if explicito:
        d = pathlib.Path(explicito)
    else:
        ds = [p for p in sorted(RES.glob("gfinal_A_2*"))
              if "piloto" not in p.name]
        d = ds[-1]
    regs = [json.loads(l) for f in sorted(d.glob("registros_*.jsonl"))
            for l in f.open(encoding="utf-8")]
    return [r for r in regs if r.get("interpretacion")], d.name


def muestrear(regs, rng):
    abus = [r for r in regs if (r["nivel"] or 0) >= 3]
    noab_p = [r for r in regs if r["dominio"] == "prision"
              and r["nivel"] is not None and r["nivel"] < 3]
    lab = [r for r in regs if r["dominio"] == "laboral"
           and r["nivel"] is not None]
    m = (rng.sample(abus, min(40, len(abus)))
         + rng.sample(noab_p, min(20, len(noab_p)))
         + rng.sample(lab, min(20, len(lab))))
    # sin duplicados (un registro laboral abusivo puede caer en dos estratos)
    vistos, unicos = set(), []
    for r in m:
        i = _id(r)
        if i not in vistos:
            vistos.add(i)
            unicos.append(r)
    rng.shuffle(unicos)
    return unicos


def juzgar(muestra):
    from openai import OpenAI
    cli = OpenAI(api_key=os.environ["OPENROUTER_API_KEY"],
                 base_url="https://openrouter.ai/api/v1")

    def uno(r):
        try:
            resp = cli.chat.completions.create(
                model=JUEZ_MODELO,
                messages=[{"role": "user", "content":
                           JUEZ_PROMPT.format(txt=r["interpretacion"])}],
                **JUEZ_PARAMS)
            t = (resp.choices[0].message.content or "").upper()
            return "SÍ" in t or bool(re.search(r"\bSI\b", t))
        except Exception:
            return None
    with ThreadPoolExecutor(8) as pool:
        return list(pool.map(uno, muestra))


def kappa(a, b):
    """κ de Cohen para dos codificadores binarios."""
    pares = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if not pares:
        return None
    n = len(pares)
    po = sum(x == y for x, y in pares) / n
    pa = sum(x for x, _ in pares) / n
    pb = sum(y for _, y in pares) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", default=None)
    ap.add_argument("--kappa", default=None,
                    help="hoja rellena: JSON [{id, humano: true/false}, …]")
    args = ap.parse_args()
    outdir = RES / "gfinal_juez"
    outdir.mkdir(exist_ok=True)

    if args.kappa:
        clave = json.loads((outdir / "clave_privada.json").read_text())
        hoja = {h["id"]: h["humano"] for h in json.loads(
            pathlib.Path(args.kappa).read_text())}
        ids = [r["id"] for r in clave["registros"]]
        j = [r["juez"] for r in clave["registros"]]
        h = [hoja.get(i) for i in ids]
        k = kappa(j, h)
        acuerdo = (sum(1 for x, y in zip(j, h)
                       if x is not None and y is not None and x == y)
                   / sum(1 for x, y in zip(j, h)
                         if x is not None and y is not None))
        print(f"κ de Cohen juez↔humano: {k} · acuerdo bruto: {acuerdo:.1%}")
        (outdir / "kappa.json").write_text(json.dumps(
            {"kappa": k, "acuerdo": round(acuerdo, 3),
             "n": len(ids)}, indent=2), encoding="utf-8")
        return

    regs, origen = cargar_a(args.dir)
    rng = random.Random(SEED)
    muestra = muestrear(regs, rng)
    veredictos = juzgar(muestra)

    hoja = ["# Hoja de etiquetado a ciegas — G-final O4",
            "", f"Rúbrica: {RUBRICA}", "",
            "Marca [SÍ] o [NO] en cada una. No abras clave_privada.json"
            " hasta terminar.", ""]
    clave = []
    for r, v in zip(muestra, veredictos):
        i = _id(r)
        hoja += [f"## {i}", "", r["interpretacion"].strip(), "",
                 "**Respuesta: [ ] SÍ · [ ] NO**", ""]
        clave.append({"id": i, "modelo": r["modelo"],
                      "dominio": r["dominio"], "contenido": r["contenido"],
                      "clausula": r["clausula"], "marco": r["marco"],
                      "nivel": r["nivel"], "juez": v,
                      "interpretacion": r["interpretacion"]})
    (outdir / "hoja_ciega.md").write_text("\n".join(hoja), encoding="utf-8")
    (outdir / "clave_privada.json").write_text(json.dumps(
        {"origen": origen, "seed": SEED, "rubrica": RUBRICA,
         "juez": {"modelo": JUEZ_MODELO, "params": JUEZ_PARAMS,
                  "prompt": JUEZ_PROMPT},
         "registros": clave}, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = [c for c in clave if c["juez"] is not None]
    abus = [c for c in ok if (c["nivel"] or 0) >= 3]
    neu = [c for c in ok if (c["nivel"] or 0) < 3]
    print(f"muestra: {len(clave)} ({len(abus)} abusivas, {len(neu)} no)")
    if abus:
        print(f"juez SÍ en abusivas: {sum(c['juez'] for c in abus)}/{len(abus)}")
    if neu:
        print(f"juez SÍ en NO abusivas: {sum(c['juez'] for c in neu)}/{len(neu)}"
              " ← especificidad aparente (pendiente del humano)")
    print(f"Hoja ciega: {outdir/'hoja_ciega.md'}")


if __name__ == "__main__":
    main()
