"""Reproceso de las sondas de justicia de Milgram con el parser actual.

Auditoría del reproceso (revisión externa 27-07, hallazgo 1): 8 sondas
privadas de milgram cambian de valor con el parser v2.1+ («SÍ. …» leídas como
False por el parser antiguo; eco de consigna). Afectan a la disonancia
agregada de gemini-flash-lite y glm-5.2(vacuna). Este script re-deriva el
resumen de CUALQUIER run de milgram desde crudos con el parser actual y lo
escribe como resumen_v2.json (el agregador lo prefiere); los .jsonl
originales no se tocan. Errata: ERR-2026-002/003 en reproceso_erratas.json.

Uso: python reproc_milgram.py
"""
import copy
import json
import pathlib

import parsers
import experimento_milgram as M

RES = pathlib.Path(__file__).parent / "resultados"


def escribir_resumen_v2(d: pathlib.Path) -> bool:
    f = d / "sesiones.jsonl"
    if not f.exists():
        return False
    ses = [json.loads(l) for l in f.open(encoding="utf-8")]
    cambiadas = 0
    for s in ses:
        for r in s["registros"]:
            nuevo = parsers.parsear_sino(r.get("privada_raw", "")).valor
            if nuevo != r.get("privada_justa"):
                cambiadas += 1
            r["privada_justa"] = nuevo
            r["disonancia"] = bool(r.get("decision") == "APLICO"
                                   and nuevo is False)
    resumen = M.analizar(copy.deepcopy(ses), ["" for _ in ses])
    resumen.update({"reprocesado": True,
                    "parser_version": parsers.PARSER_VERSION,
                    "sondas_reclasificadas": cambiadas})
    (d / "resumen_v2.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    return cambiadas > 0


def main():
    tocados = []
    for d in sorted(RES.iterdir()):
        if d.is_dir() and d.name.startswith("milgram"):
            if escribir_resumen_v2(d):
                tocados.append(d.name)
    print(f"resumen_v2.json con sondas reclasificadas en: {tocados}")


if __name__ == "__main__":
    main()
