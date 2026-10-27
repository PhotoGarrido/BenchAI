"""Tests de la huella conductual (PERSONALIDAD.md §43), sin llamadas."""

import contextlib
import io
import json
import sys

import analizar_huella as ah
import huella_modelo as hm
import manifiesto


def test_replica():
    assert hm.replica("sit_propia|P3H010|BA|0|None", 1) == "sit_propia|P3H010|BA|1|None"
    assert hm.replica("HNF:BI|F1-H03|AB|0", 1) == "HNF:BI|F1-H03|AB|1"
    assert hm.es_rep0("HNF:BI|F1-H03|AB|0") and not hm.es_rep0("sit_propia|X|AB|1|None")


def test_seleccion_reglas():
    # 3 modelos; S1 discrimina pero es inestable; S2 discrimina y es estable
    # en sus dos órdenes (solo entra uno); S3 estable sin discrepancia.
    def ids(s, o):
        return f"sit_propia|{s}|{o}|0|None", f"sit_propia|{s}|{o}|1|None"
    datos = {"a": {}, "b": {}, "c": {}}
    for s, o, letras, estable in (("S1", "AB", "AAB", False), ("S2", "AB", "ABB", True),
                                  ("S2", "BA", "ABA", True), ("S3", "AB", "AAA", True)):
        p0, p1 = ids(s, o)
        for m, x in zip("abc", letras):
            datos[m][p0] = (x, None)
            datos[m][p1] = (x if (estable or m != "a") else ("B" if x == "A" else "A"), None)
    orig = hm.registradas
    hm.registradas = lambda m: datos[m]
    try:
        cand = [ids(s, o)[0] for s, o in (("S1", "AB"), ("S2", "AB"), ("S2", "BA"), ("S3", "AB"))]
        sel = hm.seleccionar(["a", "b", "c"], cand, k=5)
    finally:
        hm.registradas = orig
    elegidas = [p for p, _ in sel]
    assert not any("S1" in p for p in elegidas), "un prompt inestable no entra"
    assert sum("S2" in p for p in elegidas) == 1, "una situación, un prompt"
    assert elegidas[-1].startswith("sit_propia|S3") and sel[-1][1] == 0.0
    assert sel[0][1] > 0.6


def test_distancia_ignora_no_validas():
    d, n, dif = hm.distancia({"x": "A", "y": "B"}, {"x": "B", "y": "B", "z": "A"}, ["x", "y", "z"])
    assert (n, dif) == (2, 1) and d == 0.5
    assert hm.distancia({}, {"x": "A"}, ["x"])[0] is None


def test_seleccion_congelada_coincide_con_los_prompts():
    sel = hm.cargar_seleccion()
    todos = hm.prompts()
    for c in ("oficial", "retro"):
        assert len(sel[c]) == sel["k"] == 48
        assert len({d["id"].split("|")[1] for d in sel[c]}) == 48
        for d in sel[c]:
            assert manifiesto.sha256_texto(todos[d["id"]]["prompt"]) == d["prompt_sha256"], d["id"]
    assert all(d["fuente"] == "v3" for d in sel["retro"])


def test_estadistica():
    assert ah.auc([0.0, 0.02], [0.3, 0.5]) == 1.0
    assert ah.umbral([0.0, 0.1], [0.3, 0.5]) == 0.2
    assert ah.umbral([0.0] * 19 + [0.4], [0.3, 0.5]) == 0.3        # se solapan
    assert abs(ah.cola_binomial(48, 0.0, 0.1)) < 1e-12
    assert 0.0 < ah.wilson_sup(0, 100) < 0.04


def test_externo_no_llama_sin_permiso():
    argv = sys.argv
    sys.argv = ["huella_modelo.py", "--modelo", "openai/gpt-5.6-luna"]
    try:
        hm.main()
    except SystemExit as e:
        assert "proyectar" in str(e)
    else:
        raise AssertionError("debía negarse a llamar a OpenRouter")
    finally:
        sys.argv = argv


def test_proyectar_no_llama():
    argv = sys.argv
    sys.argv = ["huella_modelo.py", "--modelo", "openai/gpt-5.6-luna", "--proyectar"]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            hm.main()
    finally:
        sys.argv = argv
    p = json.loads(buf.getvalue())
    assert p["llamadas"] == 48 and p["tokens_in"] > 0


if __name__ == "__main__":
    for nombre, f in list(globals().items()):
        if nombre.startswith("test_"):
            f()
            print(f"{nombre}: OK")
