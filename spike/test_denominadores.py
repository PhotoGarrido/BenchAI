"""Contrato del vigía de denominadores del sitio (web/generar_datos.py).

Tres promesas, sin tocar los HTML reales:
1. Un stealth «sin desvelar» no cuenta como laboratorio: la portada expone
   `laboratorios` con nombre y `sinDesvelar` aparte (16-09-2026, Union
   Alpha: con 11 labs y un anónimo la web decía «12 laboratorios»).
2. El vigía exige el denominador en las TRES superficies (portada, home y
   /psicobench), no solo en dos: /psicobench nació el 13-09 sin vigía.
3. Los umbrales de distinción del ISS se derivan de los IC (y la portada
   los pinta desde los datos): hasta el 23-09-2026 vivían a mano.
"""

import importlib.util
import pathlib
import unittest.mock as mock

RAIZ = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "generar_datos", RAIZ / "web" / "generar_datos.py")
gd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gd)

fallos = []


def caso(nombre, ok):
    print(f"  {'OK ' if ok else 'FALLO'} {nombre}")
    if not ok:
        fallos.append(nombre)


def entrada(lab):
    return {"lab": lab, "ejes": {"obed": 0.5, "conf": 0.2, "denu": 0.1},
            "disonancia": 0.3, "reconocimiento": 0.9}


# 6 laboratorios con nombre + 1 stealth anónimo = 7 mediciones
entradas = [entrada(l) for l in ("A", "B", "C", "D", "E", "F")]
entradas.append(entrada(gd.SIN_DESVELAR))
bench = {"entradas": entradas}

# ── 1. conteo de laboratorios ───────────────────────────────────────────────
portada = gd.bloque_portada(bench)
caso("«sin desvelar» no cuenta como laboratorio",
     portada["laboratorios"] == 6 and gd.SIN_DESVELAR not in portada["labs"])
caso("el stealth se cuenta aparte en sinDesvelar",
     portada["sinDesvelar"] == 1 and portada["mediciones"] == 7)
caso("sin stealth, sinDesvelar es 0",
     gd.bloque_portada({"entradas": entradas[:6]})["sinDesvelar"] == 0)

# ── 2. el vigía cubre las tres superficies ──────────────────────────────────
pedidas = []
with mock.patch.object(gd, "exigir",
                       lambda rel, aguja, motivo: pedidas.append((rel, aguja))):
    gd.vigilar_denominadores(bench)
ficheros = {rel for rel, _ in pedidas}
caso("vigila portada, home y /psicobench",
     {"web/index.html", "web/home.html", "web/psicobench.html"} <= ficheros)
caso("en /psicobench exige «7 mediciones de 6 laboratorios» (sin el anónimo)",
     ("web/psicobench.html", "7 mediciones de 6 laboratorios") in pedidas)
caso("en la portada exige «7 mediciones, 6 laboratorios»",
     ("web/index.html", "7 mediciones, 6 laboratorios") in pedidas)
caso("en home exige «De seis laboratorios»",
     ("web/home.html", "De seis laboratorios") in pedidas)

caso("exige que la ficha de umbrales se pinte desde los datos",
     ("web/index.html", 'data-cifra="benchmark.distincion.bajo"') in pedidas)

# 3. Los umbrales de distinción se derivan (23-09-2026: la prosa decía 10,3
#    sobre 19 mediciones cuando con 32 era 9,5).
spec_gb = importlib.util.spec_from_file_location(
    "generar_benchmark", RAIZ / "spike" / "generar_benchmark.py")
gb = importlib.util.module_from_spec(spec_gb)
spec_gb.loader.exec_module(gb)


def m(iss, lo, hi, pos=1):
    return {"iss": iss, "iss_ic": [lo, hi], "posicion": pos}


d = gb.distincion([m(10, 5, 15), m(20, 16, 24), m(22, 14, 30),
                   m(40, 35, 45), m(99, 0, 100, pos=None)])
caso("umbral bajo = menor separación con IC disjuntos (10→20: 10,0)",
     d["bajo"] == 10.0)
caso("umbral alto = mayor separación que aún solapa (10→22: 12,0)",
     d["alto"] == 12.0)
caso("las entradas n/c (sin posición) no cuentan: 4 → 6 pares",
     d["pares"] == 6 and d["solapan"] == 2)

if fallos:
    raise SystemExit(f"test_denominadores: {len(fallos)} fallo(s): {fallos}")
print("test_denominadores: OK")
