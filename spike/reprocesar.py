"""Reproceso versionado de TODOS los crudos con el parser actual.

Generaliza `reproc_prision.py` a los cinco experimentos (PLAN_MEJORA Fase
0.2). Para cada campo re-parseable (mapa único en `artefactos.py`) compara la
decisión ALMACENADA con la que produce el parser de hoy sobre el raw
almacenado, y clasifica:

  identica             mismo valor (incluye None==None)
  conducta_cambia      una conducta pasa a OTRA conducta → un resultado
                       publicado cambiaría. Es lo único que rompe --check.
  conducta_a_invalida  una conducta deja de ser legible (el parser nuevo es
                       más estricto): se reporta, no rompe — el registro sale
                       del análisis, no se convierte en otro dato.
  invalida_a_conducta  el parser nuevo lee conducta donde antes no había
                       (p. ej. typos de niveles): se reporta.
  fallback_convencer   crónica v2: el flujo degradó CONVENCER→CUMPLO por no
                       identificar destinatario (conducta real del flujo, no
                       del parser); no es un cambio.
  sin_raw              fila sin campo raw (formatos antiguos); se cuenta.

Alcance declarado: los raw históricos están truncados (120-200 chars según
experimento; g2 completos). Para respuestas de una palabra es suficiente; el
recorte se estampa en la salida.

No toca ningún .jsonl. Escribe resultados/reproceso.json (resumen) y
resultados/reproceso_detalle.jsonl (cada no-idéntica, auditable).

La puerta de CI es un golden-file: `reproceso_baseline.jsonl` (versionado)
contiene las no-idénticas CONOCIDAS y explicadas (typos de prisión de la
ERRATA, sondas de milgram corregidas por el v2.1…). `--check` falla solo si
aparecen desviaciones NUEVAS respecto al baseline — futuras ediciones del
parser obligan a re-ejecutar, revisar el diff y actualizar el baseline en un
commit consciente, nunca en silencio.

Uso:
  python reprocesar.py                       # reprocesa y escribe el informe
  python reprocesar.py --check               # puerta de CI (contra baseline)
  python reprocesar.py --actualizar-baseline # congela el detalle actual
  python reprocesar.py --tipo asch           # un solo experimento
"""

import argparse
import collections
import json
import pathlib
import sys

import artefactos
import parsers

RES = pathlib.Path(__file__).parent / "resultados"
CATS = ("identica", "conducta_cambia", "conducta_a_invalida",
        "invalida_a_conducta", "fallback_convencer", "sin_raw")


def clasificar(reg: artefactos.Registro, c: artefactos.Crudo):
    fila = reg.fila
    if c.campo_raw not in fila or fila[c.campo_raw] is None:
        return "sin_raw", None, None
    viejo = fila.get(c.campo_decision)
    nuevo = c.reparse(fila[c.campo_raw]).valor
    if reg.tipo == "cronica" and nuevo == "CONVENCER" and viejo == "CUMPLO" \
            and fila.get("destinatario") is None:
        return "fallback_convencer", viejo, nuevo
    if nuevo == viejo:
        return "identica", viejo, nuevo
    if viejo is not None and nuevo is not None:
        return "conducta_cambia", viejo, nuevo
    if viejo is not None:
        return "conducta_a_invalida", viejo, nuevo
    return "invalida_a_conducta", viejo, nuevo


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tipo", choices=list(artefactos.TIPOS) + ["todos"],
                    default="todos")
    ap.add_argument("--check", action="store_true",
                    help="puerta de REGRESIÓN: sale 1 ante desviaciones"
                         " nuevas respecto a reproceso_baseline.jsonl")
    ap.add_argument("--check-publication", action="store_true",
                    help="puerta de PUBLICACIÓN (revisión externa, hallazgo"
                         " 2): toda conducta_cambia debe tener errata_id en"
                         " reproceso_erratas.json; los datos confirmatorios"
                         " (gfinal) deben tener raw y parser_version")
    ap.add_argument("--actualizar-baseline", action="store_true",
                    help="congela el detalle actual como baseline (revisar"
                         " el diff antes de commitear)")
    ap.add_argument("--dir", default=None,
                    help="raíz de resultados alternativa (batch aislado)")
    args = ap.parse_args()

    res = pathlib.Path(args.dir) if args.dir else RES
    tipos = artefactos.TIPOS if args.tipo == "todos" else (args.tipo,)
    cuentas = collections.defaultdict(lambda: collections.Counter())
    detalle = []

    for reg in artefactos.iterar_registros(res, tipos):
        for c in reg.crudos:
            cat, viejo, nuevo = clasificar(reg, c)
            clave = f"{reg.tipo}·{c.etiqueta}"
            cuentas[clave][cat] += 1
            if cat not in ("identica", "sin_raw"):
                detalle.append({
                    "tipo": reg.tipo, "dir": reg.directorio,
                    "fichero": reg.fichero, "campo": c.etiqueta,
                    "categoria": cat, "viejo": viejo, "nuevo": nuevo,
                    "raw": str(reg.fila.get(c.campo_raw, ""))[:160]})

    ancho = max((len(k) for k in cuentas), default=10) + 2
    cab = "campo".ljust(ancho) + " | " + " | ".join(f"{c:>19}" for c in CATS)
    print(cab)
    print("-" * len(cab))
    total = collections.Counter()
    for k in sorted(cuentas):
        total.update(cuentas[k])
        print(k.ljust(ancho) + " | "
              + " | ".join(f"{cuentas[k][c]:>19}" for c in CATS))
    print("TOTAL".ljust(ancho) + " | "
          + " | ".join(f"{total[c]:>19}" for c in CATS))

    canon = sorted(json.dumps(d, ensure_ascii=False, sort_keys=True)
                   for d in detalle)
    baseline_f = res / "reproceso_baseline.jsonl"

    if args.check_publication:
        fallos = []
        # (a) toda conducta_cambia con errata_id
        err_f = res / "reproceso_erratas.json"
        con_errata = set()
        if err_f.exists():
            entradas = json.loads(err_f.read_text())["erratas"]
            for e in entradas:
                # Cada errata: campos obligatorios y bien tipados (P1.2).
                if not (e.get("errata_id") and e.get("justification")
                        and isinstance(e.get("affects_aggregate"), bool)):
                    fallos.append(f"errata malformada: {e.get('errata_id')}")
                clave = json.dumps(e["fila"], ensure_ascii=False,
                                   sort_keys=True)
                if clave in con_errata:
                    fallos.append(f"errata duplicada: {e.get('errata_id')}")
                con_errata.add(clave)
            actuales = {json.dumps(d, ensure_ascii=False, sort_keys=True)
                        for d in detalle if d["categoria"] == "conducta_cambia"}
            for clave in con_errata - actuales:
                fallos.append("errata huérfana (fila ya no existe en el"
                              " reproceso): " + clave[:80])
        for d in detalle:
            if d["categoria"] == "conducta_cambia":
                clave = json.dumps(d, ensure_ascii=False, sort_keys=True)
                if clave not in con_errata:
                    fallos.append("conducta_cambia SIN errata_id: "
                                  f"{d['tipo']}·{d['dir'][:40]}")
        # (b) datos confirmatorios (gfinal no-piloto): raw y parser_version
        for reg in artefactos.iterar_registros(res, ("gfinal",)):
            if "piloto" in reg.directorio:
                continue
            fila = reg.fila
            if not fila.get("raw_publico"):
                fallos.append(f"fila sin raw_publico en {reg.directorio}")
                break
            if not fila.get("parser_version"):
                fallos.append(f"fila sin parser_version en {reg.directorio}")
                break
        if fallos:
            print("\nCHECK-PUBLICATION FALLA:")
            for f in fallos[:10]:
                print("  · " + f)
            sys.exit(1)
        print(f"\nCHECK-PUBLICATION OK: {total['conducta_cambia']}"
              " conducta_cambia, todas con errata_id; datos confirmatorios"
              " con raw y parser_version.")
        return

    if args.actualizar_baseline:
        baseline_f.write_text("\n".join(canon) + "\n", encoding="utf-8")
        print(f"\nBaseline congelado: {baseline_f} ({len(canon)} filas)."
              " Revisa el diff y commitea con justificación.")
        return

    if args.check:
        if not baseline_f.exists():
            print("\nCHECK FALLA: no existe reproceso_baseline.jsonl."
                  " Genera y revisa uno con --actualizar-baseline.")
            sys.exit(1)
        base = collections.Counter(
            l.strip() for l in baseline_f.open(encoding="utf-8") if l.strip())
        ahora = collections.Counter(canon)
        nuevas = list((ahora - base).elements())
        desaparecidas = list((base - ahora).elements())
        if nuevas or desaparecidas:
            print(f"\nCHECK FALLA: el reproceso se desvía del baseline"
                  f" ({len(nuevas)} filas nuevas, {len(desaparecidas)}"
                  " desaparecidas). Un cambio de parser o de datos debe"
                  " revisarse y, si procede, congelarse con"
                  " --actualizar-baseline en un commit explicado.")
            for l in nuevas[:10]:
                print("  + " + l[:200])
            for l in desaparecidas[:10]:
                print("  - " + l[:200])
            sys.exit(1)
        print(f"\nCHECK OK: reproceso idéntico al baseline ({len(canon)}"
              f" no-idénticas conocidas; parser v{parsers.PARSER_VERSION};"
              f" {total['identica']} decisiones intactas).")
        return

    salida = {
        "parser_version": parsers.PARSER_VERSION,
        "nota_raws": "raws históricos truncados a 120-200 chars según"
                     " experimento; los runs g2 de 25-07 no guardaron"
                     " raw_publico/raw_justo (el código actual sí lo hace)",
        "por_campo": {k: dict(cuentas[k]) for k in sorted(cuentas)},
        "total": dict(total),
    }
    (res / "reproceso.json").write_text(
        json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    (res / "reproceso_detalle.jsonl").write_text(
        "\n".join(json.dumps(d, ensure_ascii=False) for d in detalle) + "\n",
        encoding="utf-8")
    print(f"\nEscritos {res / 'reproceso.json'} y reproceso_detalle.jsonl"
          f" ({len(detalle)} filas no idénticas)")
    if total["conducta_cambia"]:
        print(f"\n[AVISO] {total['conducta_cambia']} decisiones de conducta"
              " difieren de lo almacenado con el parser actual. Si no están"
              " ya explicadas en el baseline/ERRATA, investigar antes de"
              " publicar nada.")


if __name__ == "__main__":
    main()
