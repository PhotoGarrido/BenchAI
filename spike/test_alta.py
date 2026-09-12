"""Contrato offline de alta.py: el plan no gasta, el cableado no pisa.

Tres promesas, sin red y sin tocar los JSON reales:
1. Sin --autorizado el guion imprime el plan y sale SIN lanzar subprocesos.
2. registrar_mapas jamás sobreescribe una clave existente (el mapa es por
   alias y lo comparten entradas históricas) y exige run COMPLETO.
3. registrar_fuente rechaza mezclar proveedores y no duplica matrices.
"""

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest.mock as mock

import alta

AQUI = pathlib.Path(__file__).resolve().parent
fallos = []


def caso(nombre, ok):
    print(f"  {'OK ' if ok else 'FALLO'} {nombre}")
    if not ok:
        fallos.append(nombre)


# ── 1. sin --autorizado no hay subprocesos ──────────────────────────────────
with mock.patch.object(subprocess, "run",
                       side_effect=AssertionError("¡lanzó un subproceso!")):
    with mock.patch.object(sys, "argv",
                           ["alta.py", "--modelos", "x-ai/grok-4.5"]):
        try:
            alta.main()
            caso("plan sin --autorizado: imprime y sale sin lanzar nada", True)
        except AssertionError:
            caso("plan sin --autorizado: imprime y sale sin lanzar nada", False)
        except SystemExit as e:
            caso("plan sin --autorizado: sale limpio", e.code in (None, 0))

# ── proyección: con precio suma, sin precio se declara ──────────────────────
plan, total, sin_precio, _ = alta.proyectar_coste(
    ["x-ai/grok-4.5", "modelo-inventado-sin-precio"])
caso("proyección: el modelo con precio aporta un coste > 0",
     total > 0 and plan[0][2] is not None)
caso("proyección: el modelo sin precio queda declarado, no inventado",
     sin_precio == ["modelo-inventado-sin-precio"] and plan[1][2] is None)
caso("proveedor por convención de id (/ → OpenRouter)",
     alta.proveedor_de("x-ai/grok-4.5") == "OpenRouter"
     and alta.proveedor_de("qwen3.6") == "NaN")

# ── 2 y 3. cableado sobre un árbol temporal ─────────────────────────────────
with tempfile.TemporaryDirectory() as td:
    raiz = pathlib.Path(td)
    (raiz / "denuncia_runs.json").write_text(json.dumps(
        {"_doc": "", "runs": {"ya/mapeado": "resultados/viejo"}}),
        encoding="utf-8")
    (raiz / "sicofancia_runs.json").write_text(json.dumps(
        {"_doc": "", "runs": {}}), encoding="utf-8")
    (raiz / "fuentes_benchmark.json").write_text(json.dumps(
        {"_doc": "", "fuentes": [{"matriz": "resultados/bateria_vieja/"
                                  "matriz_m2.json", "proveedor": "NaN"}]}),
        encoding="utf-8")
    batch = raiz / "resultados" / "bateria_test"
    # run completo (con resumen) para el modelo nuevo; incompleto para el ya
    # mapeado; ninguno de sicofancia → problema declarado, no silencioso
    d1 = batch / "denuncia_nuevo_modelo_20260821_000000_000001"
    d1.mkdir(parents=True)
    (d1 / "resumen.json").write_text("{}", encoding="utf-8")
    d2 = batch / "denuncia_ya_mapeado_20260821_000000_000002"
    d2.mkdir()
    (d2 / "resumen.json").write_text("{}", encoding="utf-8")
    with mock.patch.object(alta, "AQUI", raiz):
        altas, problemas = alta.registrar_mapas(
            batch, ["nuevo/modelo", "ya/mapeado"])
        mapa = json.loads((raiz / "denuncia_runs.json")
                          .read_text(encoding="utf-8"))["runs"]
        caso("mapa: el modelo nuevo queda cableado al run completo",
             mapa.get("nuevo/modelo", "").endswith("000001"))
        caso("mapa: la clave existente NO se pisa",
             mapa["ya/mapeado"] == "resultados/viejo"
             and any("no lo piso" in p for p in problemas))
        caso("mapa: la ausencia de sicofancia es un problema declarado",
             any("sicofancia" in p for p in problemas))

        # fuente nueva + rechazo de proveedores mezclados + no duplicar
        (batch / "matriz_m2.json").write_text("{}", encoding="utf-8")
        msg = alta.registrar_fuente(batch, ["nuevo/modelo"])
        fuentes = json.loads((raiz / "fuentes_benchmark.json")
                             .read_text(encoding="utf-8"))["fuentes"]
        caso("fuente: la matriz del batch queda registrada con su proveedor",
             any(f["matriz"].endswith("bateria_test/matriz_m2.json")
                 and f["proveedor"] == "OpenRouter" for f in fuentes)
             and msg.startswith("fuentes_benchmark.json: +"))
        caso("fuente: repetir el registro no duplica",
             "ya estaba" in alta.registrar_fuente(batch, ["nuevo/modelo"]))
        try:
            alta.registrar_fuente(batch, ["con/barra", "sinbarra"])
            caso("fuente: proveedores mezclados se rechazan", False)
        except SystemExit:
            caso("fuente: proveedores mezclados se rechazan", True)

# ── la SUITE de la batería cubre el octógono ────────────────────────────────
import bateria
nombres = [n for n, _, _ in bateria.SUITE]
caso("bateria.SUITE incluye denuncia y sicofancia_op (suite v0.4 íntegra)",
     "denuncia" in nombres and "sicofancia_op" in nombres)

if fallos:
    raise SystemExit(f"test_alta: {len(fallos)} fallo(s): {fallos}")
print("test_alta: OK")
