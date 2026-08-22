"""Alta de un modelo nuevo en PsicoBench: la suite v0.4 de una tacada.

Convierte los ~7 pasos manuales del alta (batería + 2 runs N sueltos +
matriz + 3 JSON a mano + regeneración) en un comando con dos fases:

  python alta.py --modelos a,b                  # PLAN: proyecta coste y para
  python alta.py --modelos a,b --autorizado     # ejecuta la suite entera
  python alta.py --registrar resultados/bateria_X --modelos a,b
                                                # solo cableado post-run

Reglas de la casa que este guion hace cumplir (SETUP_PSICOAI, METODO §A):
- Sin --autorizado NO se hace ninguna llamada de pago: se imprime el plan
  con la proyección de coste y se sale. La autorización es del dueño.
- Jamás sobreescribe una clave existente de denuncia_runs.json /
  sicofancia_runs.json: el mapa es por alias y lo comparten las entradas
  históricas de ese alias — re-medir un modelo ya presente es una decisión
  de doctrina (BENCHMARK.md, «se miden versiones»), no un efecto lateral.
- El registro en fuentes_benchmark.json y la regeneración quedan hechos;
  la puerta final sigue siendo ./verificar.sh antes del commit.
"""

import argparse
import json
import pathlib
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent

# Referencias de volumen por modelo, medidas sobre la batería COMPLETA de
# stealth/ox-alpha (21/22-08-2026, 4.536 llamadas): el primer modelo
# RAZONADOR medido de punta a punta, que es el perfil de la cartera actual.
# La referencia anterior (deepseek-v4-flash, escueto y sin razonamiento)
# infravaloraba la salida en un 52% y sobrevaloraba la entrada un 15%.
# Aviso que la medición NO puede despejar: ox-alpha no factura sus tokens de
# pensamiento (reasoning_tokens=0); un razonador de PAGO normalmente sí, así
# que en esos la salida real puede ser bastante mayor que esta referencia.
REFERENCIA = {
    #  bloque          llamadas  tokens_in  tokens_out
    "bateria_m2":      (3614,    1_921_985, 807_538),
    "denuncia":        (300,       126_090,  54_308),
    "sicofancia_op":   (622,       251_698,  96_720),
}


def proveedor_de(modelo: str) -> str:
    """La convención de model_factory: id con «/» → OpenRouter, plano → NaN."""
    return "OpenRouter" if "/" in modelo else "NaN"


def proyectar_coste(modelos):
    """Plan imprimible: llamadas y coste estimado por modelo, con los pins
    de PRECIOS de coste_run.py. Sin precio conocido no se inventa nada."""
    import coste_run
    llamadas = sum(v[0] for v in REFERENCIA.values())
    t_in = sum(v[1] for v in REFERENCIA.values())
    t_out = sum(v[2] for v in REFERENCIA.values())
    plan, total, sin_precio = [], 0.0, []
    for m in modelos:
        pin, pout = coste_run.PRECIOS.get(m, (None, None))
        if pin is None:
            sin_precio.append(m)
            plan.append((m, llamadas, None))
        else:
            c = (t_in * pin + t_out * pout) / 1e6
            total += c
            plan.append((m, llamadas, c))
    return plan, total, sin_precio, (t_in, t_out)


def avisos_previos(modelos):
    """Lo que hoy falla en silencio: lab sin nombre y precio sin pin."""
    import coste_run
    import generar_benchmark
    avisos = []
    for m in modelos:
        pref = m.split("/")[0] if "/" in m else m
        if "/" in m and pref not in generar_benchmark.LABS:
            avisos.append(f"lab «{pref}» no está en LABS de generar_benchmark.py "
                          "(saldría como «?» en la tabla): añádelo antes de publicar")
        if m not in coste_run.PRECIOS:
            avisos.append(f"«{m}» no tiene precio en coste_run.PRECIOS: la "
                          "proyección y la auditoría de coste saldrán incompletas")
    return avisos


def _cargar(rel):
    f = AQUI / rel
    return f, json.loads(f.read_text(encoding="utf-8"))


def _runs_en_batch(batch: pathlib.Path, prefijo: str, modelo: str):
    """Runs COMPLETOS (con resumen.json) de un experimento y modelo dentro
    del batch, el más reciente al final. Mismo criterio que analisis_bateria:
    los abortados no tienen resumen y quedan fuera solos."""
    slug = modelo.replace("/", "_")
    return sorted(d for d in batch.glob(f"{prefijo}_{slug}_*")
                  if (d / "resumen.json").exists())


def registrar_mapas(batch: pathlib.Path, modelos, escribir=True):
    """Cablea denuncia_runs.json y sicofancia_runs.json con los runs del
    batch. Devuelve (altas, problemas). Nunca pisa una clave existente."""
    altas, problemas = [], []
    for rel, prefijo in (("denuncia_runs.json", "denuncia"),
                         ("sicofancia_runs.json", "sicofancia-op")):
        f, mapa = _cargar(rel)
        for m in modelos:
            candidatos = _runs_en_batch(batch, prefijo, m)
            if not candidatos:
                problemas.append(f"{rel}: sin run completo de {prefijo} para "
                                 f"«{m}» en {batch.name}")
                continue
            if m in mapa["runs"]:
                problemas.append(
                    f"{rel}: «{m}» ya está mapeado a {mapa['runs'][m]} — no lo "
                    "piso (el mapa es por alias y lo comparten las entradas "
                    "históricas). Si esto es una re-medición, decídelo a mano.")
                continue
            ruta = candidatos[-1].relative_to(AQUI).as_posix()
            mapa["runs"][m] = ruta
            altas.append(f"{rel}: {m} → {ruta}")
            if escribir:
                f.write_text(json.dumps(mapa, ensure_ascii=False, indent=1)
                             + "\n", encoding="utf-8")
    return altas, problemas


def registrar_fuente(batch: pathlib.Path, modelos, escribir=True):
    """Añade la matriz del batch a fuentes_benchmark.json si no está."""
    proveedores = {proveedor_de(m) for m in modelos}
    if len(proveedores) != 1:
        raise SystemExit("[alta] los modelos del batch mezclan proveedores "
                         f"({proveedores}): una fuente declara UN proveedor — "
                         "sepáralos en dos altas")
    matriz = batch.relative_to(AQUI).as_posix() + "/matriz_m2.json"
    f, fuentes = _cargar("fuentes_benchmark.json")
    if any(x["matriz"] == matriz for x in fuentes["fuentes"]):
        return f"fuentes_benchmark.json: {matriz} ya estaba"
    fuentes["fuentes"].append({"matriz": matriz,
                               "proveedor": proveedores.pop()})
    if escribir:
        f.write_text(json.dumps(fuentes, ensure_ascii=False, indent=1) + "\n",
                     encoding="utf-8")
    return f"fuentes_benchmark.json: + {matriz}"


def _correr(cmd):
    print(f"\n$ {' '.join(cmd)}", flush=True)
    rc = subprocess.run(cmd, cwd=AQUI).returncode
    if rc != 0:
        raise SystemExit(f"[alta] falló: {' '.join(cmd)} (rc={rc})")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modelos", required=True,
                    help="lista separada por comas (IDs OpenRouter con /)")
    ap.add_argument("--autorizado", action="store_true",
                    help="confirma el presupuesto y lanza la suite (sin esto, "
                         "solo se imprime el plan)")
    ap.add_argument("--registrar", default=None, metavar="BATCH",
                    help="salta la ejecución: cablea mapas+matriz+fuente de un "
                         "batch ya corrido")
    ap.add_argument("--reanudar", default=None, metavar="BATCH",
                    help="pasa --reanudar a bateria.py (batch a medio correr)")
    args = ap.parse_args()
    modelos = [m.strip() for m in args.modelos.split(",") if m.strip()]

    # ── fase de plan: siempre se imprime, con o sin autorización ─────────
    plan, total, sin_precio, (t_in, t_out) = proyectar_coste(modelos)
    print("PLAN DE ALTA — suite íntegra v0.4 (batería M2 + N2 + N3b)")
    print(f"  por modelo: ~{sum(v[0] for v in REFERENCIA.values())} llamadas · "
          f"~{t_in/1e6:.1f}M in / ~{t_out/1e6:.1f}M out · ~3-4 h de máquina")
    for m, n, c in plan:
        print(f"  {m:<44} {'$%.2f' % c if c is not None else 'SIN PRECIO'}")
    if total:
        print(f"  TOTAL con precio: ${total:.2f} (el out real puede ×3 en "
              "modelos verbosos)")
    for a in avisos_previos(modelos):
        print(f"  [aviso] {a}")

    if args.registrar:
        batch = (AQUI / args.registrar).resolve() if not pathlib.Path(
            args.registrar).is_absolute() else pathlib.Path(args.registrar)
        if not batch.is_dir():
            raise SystemExit(f"[alta] no existe {batch}")
    else:
        if not args.autorizado:
            print("\nSin --autorizado no se lanza nada (regla de presupuesto "
                  "de SETUP_PSICOAI). Revisa el plan y vuelve con --autorizado.")
            return
        cmd = [sys.executable, "bateria.py", "--modelos", ",".join(modelos)]
        if args.reanudar:
            cmd += ["--reanudar", args.reanudar]
        _correr(cmd)
        batches = sorted((AQUI / "resultados").glob("bateria_*"))
        batch = (AQUI / args.reanudar) if args.reanudar else batches[-1]

    # ── cableado post-run ────────────────────────────────────────────────
    altas, problemas = registrar_mapas(batch, modelos)
    for a in altas:
        print(f"  {a}")
    if problemas:
        for p in problemas:
            print(f"  [PROBLEMA] {p}")
        raise SystemExit("[alta] cableado incompleto: resuélvelo y repite con "
                         f"--registrar {batch.relative_to(AQUI).as_posix()}")
    _correr([sys.executable, "analisis_bateria.py", "--modelos",
             ",".join(modelos), "--dir", str(batch)])
    print("  " + registrar_fuente(batch, modelos))
    _correr([sys.executable, "generar_benchmark.py"])
    _correr([sys.executable, str(AQUI.parent / "web" / "generar_datos.py")])
    print("\nALTA REGISTRADA. Antes del commit: ./verificar.sh — y recuerda "
          "la entrada M-n en CHANGELOG/EXPERIMENTOS con el coste real "
          "(python coste_run.py '<batch>/*').")


if __name__ == "__main__":
    main()
