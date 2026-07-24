"""Agrega los resúmenes de la batería global (test global M2) en una matriz.

Para cada modelo de la cartera busca el run MÁS RECIENTE de cada experimento
de la suite y extrae las métricas que definen el perfil social:

  asch      conformidad pública (mayoría/aliado), complacencia, precisión
  milgram   supera_critico y ruptura en 'autoridad'; delta de la vacuna
  cronica   supervivencia de la norma (v1) y derogaciones en v2 (3 semillas)
  prision   % actos abusivos y nivel máx por variante (media de ambos marcos)

Salida: resultados/matriz_m2.json + tabla por pantalla.

Uso: python analisis_bateria.py --modelos a,b,c
"""

import argparse
import json
import pathlib

RES = pathlib.Path(__file__).parent / "resultados"


def ultimo(patron):
    """Directorio más reciente que casa con el patrón (o None)."""
    dirs = sorted(d for d in RES.glob(patron) if (d / "resumen.json").exists())
    return dirs[-1] if dirs else None


def carga(patron):
    d = ultimo(patron)
    return (json.loads((d / "resumen.json").read_text()), d.name) if d else (None, None)


def _r(x, nd=2):
    return None if x is None else round(x, nd)


def perfil(modelo):
    et = modelo.replace("/", "_")
    p = {"modelo": modelo, "runs": {}}

    j, run = carga(f"asch_{et}_2*")
    if j:
        p["runs"]["asch"] = run
        p["asch"] = {
            "precision_control": _r(j.get("precision_control")),
            "conformidad_mayoria": _r(j.get("conformidad_publica_mayoria")),
            "conformidad_aliado": _r(j.get("conformidad_publica_aliado")),
            "complacencia": _r(j.get("complacencia_entre_conformes")),
        }

    j, run = carga(f"milgram_{et}_2*")
    if j:
        p["runs"]["milgram"] = run
        aut = j.get("autoridad", {})
        p["milgram"] = {
            "supera_critico": _r(aut.get("supera_critico")),
            "ruptura_media": _r(aut.get("ruptura_media"), 1),
            "llega_al_maximo": _r(aut.get("llega_al_maximo")),
            "disonancia": _r(aut.get("disonancia_entre_aplicados")),
            "supera_critico_control": _r(j.get("control", {}).get("supera_critico")),
            "supera_critico_rebelde": _r(j.get("rebelde", {}).get("supera_critico")),
        }
    j, run = carga(f"milgram_{et}_vacuna_2*")
    if j and "milgram" in p:
        p["runs"]["vacuna"] = run
        sc = j.get("autoridad", {}).get("supera_critico")
        base = p["milgram"]["supera_critico"]
        p["milgram"]["vacuna_delta"] = (_r(sc - base)
                                        if None not in (sc, base) else None)

    j, run = carga(f"cronica_{et}_2*")
    if j:
        p["runs"]["cronica_v1"] = run
        p["cronica"] = {"v1_resultado": j.get("resultado")}
    derog = 0
    for s in ("715", "716", "717"):
        j, run = carga(f"cronica_{et}_v2_s{s}_2*")
        if j:
            p["runs"][f"v2_s{s}"] = run
            if "derogada" in (j.get("resultado") or ""):
                derog += 1
    p.setdefault("cronica", {})["v2_derogaciones_de_3"] = derog

    p["prision"] = {}
    for clave, patron in [("p1", f"prision_{et}_2*"),
                          ("p1b", f"prision_{et}_coaching_2*"),
                          ("p2", f"prision_{et}_rebelion_2*"),
                          ("p2b", f"prision_{et}_ordenes_2*")]:
        j, run = carga(patron)
        if not j:
            continue
        p["runs"][clave] = run
        marcos = j.get("marcos", {})
        abus = [m["actos_abusivos_pct"] for m in marcos.values()]
        p["prision"][clave] = {
            "abusivos_pct": _r(sum(abus) / len(abus)) if abus else None,
            "nivel_max": max((m["nivel_maximo_alcanzado"]
                              for m in marcos.values()), default=None),
            "quiebres": sum(m.get("quiebres", 0) for m in marcos.values()),
            "delta_marco_abusivos": _r(j.get("contraste_marco", {})
                                        .get("delta_abusivos")),
        }
    return p


CAMPOS = [
    ("asch conf.mayoría", lambda p: p.get("asch", {}).get("conformidad_mayoria")),
    ("asch conf.aliado", lambda p: p.get("asch", {}).get("conformidad_aliado")),
    ("asch complacencia", lambda p: p.get("asch", {}).get("complacencia")),
    ("milgram supera crítico", lambda p: p.get("milgram", {}).get("supera_critico")),
    ("milgram ruptura media", lambda p: p.get("milgram", {}).get("ruptura_media")),
    ("milgram disonancia", lambda p: p.get("milgram", {}).get("disonancia")),
    ("vacuna Δ", lambda p: p.get("milgram", {}).get("vacuna_delta")),
    ("crónica v1", lambda p: p.get("cronica", {}).get("v1_resultado")),
    ("crónica v2 derog/3", lambda p: p.get("cronica", {}).get("v2_derogaciones_de_3")),
    ("P1 abusivos", lambda p: p.get("prision", {}).get("p1", {}).get("abusivos_pct")),
    ("P1b abusivos", lambda p: p.get("prision", {}).get("p1b", {}).get("abusivos_pct")),
    ("P2 abusivos", lambda p: p.get("prision", {}).get("p2", {}).get("abusivos_pct")),
    ("P2b abusivos", lambda p: p.get("prision", {}).get("p2b", {}).get("abusivos_pct")),
    ("P2b nivel máx", lambda p: p.get("prision", {}).get("p2b", {}).get("nivel_max")),
    ("quiebres totales", lambda p: sum(v.get("quiebres", 0)
                                       for v in p.get("prision", {}).values())),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modelos", required=True)
    args = parser.parse_args()
    modelos = [m.strip() for m in args.modelos.split(",") if m.strip()]

    perfiles = [perfil(m) for m in modelos]
    (RES / "matriz_m2.json").write_text(
        json.dumps(perfiles, ensure_ascii=False, indent=2), encoding="utf-8")

    for p in perfiles:
        faltan = [k for k in ("asch", "milgram") if k not in p]
        if faltan or len(p.get("prision", {})) < 4:
            print(f"[aviso] {p['modelo']}: incompleto — {faltan},"
                  f" prision={list(p.get('prision', {}))}")
    ancho = 24
    print("\n" + " " * ancho
          + " | ".join(p["modelo"].split("/")[-1][:12].rjust(12) for p in perfiles))
    for nombre, fn in CAMPOS:
        fila = nombre.ljust(ancho)
        for p in perfiles:
            v = fn(p)
            if isinstance(v, str):
                v = v.replace("norma ", "")[:12]
            fila += " | " + str("—" if v is None else v).rjust(12)
        print(fila)
    print(f"\nGuardado en {RES / 'matriz_m2.json'}")


if __name__ == "__main__":
    main()
