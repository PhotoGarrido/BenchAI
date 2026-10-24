"""Tests de la pasada de formatos H/N (PERSONALIDAD.md §32): parsers, plan y
puntuación. Sin llamadas a modelos.

Uso: python test_personalidad_hn.py
"""

import experimento_personalidad_hn as e
import parsers
import personalidad_hn_items as it

OK = parsers.OK


def test_entero():
    assert e.parsear_entero("50", 0, 100) == (50, OK)
    assert e.parsear_entero("50 €", 0, 100) == (50, OK)
    assert e.parsear_entero("Le daría 30 euros.", 0, 100) == (30, OK)
    assert e.parsear_entero("1.000", 0, 1000) == (1000, OK)
    assert e.parsear_entero("500,0", 0, 1000) == (500, OK)
    assert e.parsear_entero("2,5", 0, 6)[1] == "FUERA_RANGO"
    assert e.parsear_entero("7", 1, 6)[1] == "FUERA_RANGO"
    assert e.parsear_entero("", 0, 6)[1] == parsers.ERROR_TECNICO
    assert e.parsear_entero("No puedo responder a eso.", 0, 6)[1] in (
        parsers.REHUSA, parsers.INVALIDA)
    assert e.parsear_entero("Como IA, no tengo preferencias", 0, 6)[1] == "NIEGA_IDENTIDAD"


def test_dos():
    assert e.parsear_dos("6, 4") == ((6, 4), OK)
    assert e.parsear_dos("6,4") == ((6, 4), OK)
    assert e.parsear_dos("7 y 8") == ((7, 8), OK)
    assert e.parsear_dos("1. 6\n2. 3") == ((6, 3), OK)
    assert e.parsear_dos("1) 8 2) 9") == ((8, 9), OK)
    assert e.parsear_dos("Me afectaría un 5 y le daría vueltas un 7") == ((5, 7), OK)
    assert e.parsear_dos("11, 3")[1] == "FUERA_RANGO"
    assert e.parsear_dos("5")[1] != OK
    assert e.parsear_dos("")[1] == parsers.ERROR_TECNICO


def test_num_letra():
    assert e.parsear_num_letra("7, B") == ((7, "B"), OK)
    assert e.parsear_num_letra("3 A") == ((3, "A"), OK)
    assert e.parsear_num_letra("B, 4") == ((4, "B"), OK)
    assert e.parsear_num_letra("Malestar: 6. Opción: A") == ((6, "A"), OK)
    assert e.parsear_num_letra("1. 7\n2. B") == ((7, "B"), OK)
    assert e.parsear_num_letra("12, A")[1] == "FUERA_RANGO"
    assert e.parsear_num_letra("A")[1] != OK


def test_plan_y_puntos():
    ts = e.plan()
    assert len(ts) == 768
    por = {f: sum(t["formato"] == f for t in ts) for f in e.FORMATOS}
    assert por == {"HE": 320, "HD": 32, "HM": 32, "HO": 72, "NG": 72, "NS": 144, "NC": 96}
    assert all("{" not in t["prompt"] for t in ts), "hueco sin rellenar"
    # Mismo estímulo en los dos órdenes, salvo las opciones
    he = {t["id"]: t for t in ts if t["formato"] == "HE"}
    a, b = he["HE|HE-EQ1|0|AB|0"], he["HE|HE-EQ1|0|BA|0"]
    assert a["prompt"].split("A:")[0] == b["prompt"].split("A:")[0]
    # Polo alto: en AB, la A es la honesta
    assert e.puntuar(a, "A")["puntos"] == 1.0 and e.puntuar(b, "A")["puntos"] == 0.0
    hd = next(t for t in ts if t["formato"] == "HD" and t["orden"] == "quedarse"
              and t["total"] == 100)
    assert e.puntuar(hd, "70")["dado"] == 30 and abs(e.puntuar(hd, "70")["puntos"] - .6) < 1e-9
    assert e.puntuar(hd, "20")["puntos"] == 1.0          # dar más de la mitad = equidad máxima
    hm = next(t for t in ts if t["item"] == "HM1")
    assert e.puntuar(hm, "2")["puntos"] == 1.0 and e.puntuar(hm, "6")["puntos"] == 0.0
    nc = next(t for t in ts if t["formato"] == "NC" and t["orden"] == "BA")
    r = e.puntuar(nc, "8, B")      # en BA la B es la reactiva
    assert r["elige_reactiva"] and abs(r["puntos"] - .9) < 1e-9
    # Los fallos técnicos no puntúan
    for t in (a, hd, hm, nc):
        assert e.puntuar(t, "")["puntos"] is None
        assert e.puntuar(t, "")["estado"] == parsers.ERROR_TECNICO


def test_escalera_monotona():
    for iid, *_, niveles in it.HE:
        v = [x for x, _ in niveles]
        assert v == sorted(v) and len(set(v)) == 5, iid


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            f()
    print("test_personalidad_hn: OK")
