"""Contrato del vigía de denominadores del sitio (web/generar_datos.py).

Dos promesas, sin tocar los HTML reales:
1. Un stealth «sin desvelar» no cuenta como laboratorio: la portada expone
   `laboratorios` con nombre y `sinDesvelar` aparte (16-09-2026, Union
   Alpha: con 11 labs y un anónimo la web decía «12 laboratorios»).
2. El vigía exige el denominador en las TRES superficies (portada, home y
   /psicobench), no solo en dos: /psicobench nació el 13-09 sin vigía.
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

if fallos:
    raise SystemExit(f"test_denominadores: {len(fallos)} fallo(s): {fallos}")
print("test_denominadores: OK")
