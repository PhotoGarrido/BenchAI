"""Tests del alta de personalidad y de los índices de validez (PERSONALIDAD.md §41).
Sin llamadas a modelos: el alta corre en seco en un directorio temporal.

Uso: python test_alta_personalidad.py
"""

import json
import pathlib
import random
import tempfile

import alta_personalidad as alta
import experimento_personalidad_hn_finos as ef
import experimento_personalidad_v3 as ev3
import validez_personalidad as vp

NUEVO = "x-ai/modelo-de-prueba-inexistente"
#: Un modelo de pago con v1 y sin alta (§45: glm-5.3, que se usaba aquí, ya está completo)
PENDIENTE = "mistralai/mistral-large-4-0"


def test_tarifas():
    assert alta.tarifa("gemma4") == (0.0, 0.0)                      # NaN: tarifa plana
    assert alta.tarifa("openai/gpt-6.1-sol#low") == (2.0, 10.0)     # #nivel no cambia la tarifa
    assert alta.tarifa("z-ai/glm-5.3@2026-10-23") == (0.70, 2.20)   # @medición tampoco
    assert alta.tarifa(NUEVO) == (None, None)
    assert alta.es_de_pago("x-ai/grok-4.5") and not alta.es_de_pago("qwen3.6")


def test_plan_mismos_ids_y_semillas():
    with tempfile.TemporaryDirectory() as d:
        p = alta.plan(NUEVO, None, leer=(pathlib.Path(d),))
        corta = alta.cargar_corta()
        pc = alta.plan(NUEVO, corta, leer=(pathlib.Path(d),))
    n = {f: len(x) for f, x in p.items()}
    sel = [s for s in json.loads(ev3.SEL.read_text(encoding="utf-8")) if s["rasgo"] in alta.RASGOS_V3]
    assert n == {"v3": 6 * len(sel), "I1-H": 6 * 48, "I1-N": 6 * 72}, n
    nc = {f: len(x) for f, x in pc.items()}
    k = {t: len(x) for t, x in corta.items()}
    assert nc == {"v3": 6 * sum(k[t] for t in alta.RASGOS_V3), "I1-H": 6 * k["H"], "I1-N": 6 * k["N"]}, nc
    # Mismos ids, semillas y prompts que los ejecutores
    nada = pathlib.Path(tempfile.gettempdir()) / "no_existe.jsonl"
    ref = {t["id"]: t for t in ev3.plan(nada, nada)}
    for t in p["v3"]:
        assert ref[t["id"]]["seed"] == t["seed"] and ref[t["id"]]["prompt"] == t["prompt"]
    ref = {t["id"]: t for t in ef.plan(parejas=None, bi_h_completo=True, bi_n_completo=True)}
    for t in p["I1-H"] + p["I1-N"]:
        assert ref[t["id"]]["seed"] == t["seed"] and ref[t["id"]]["prompt"] == t["prompt"]
    # Un modelo del cuadro no tiene nada pendiente
    assert sum(len(x) for x in alta.plan("openai/gpt-6.1-sol#low").values()) == 0


def test_vigilante():
    v = alta.Vigilante(tope=0.01, hilos=2, coste_previsto=0.001)
    assert v.permite()
    for _ in range(4):   # 4 × (1000 × 2 $/M) = 0,008 $
        v.sumar({"modelo": "x-ai/grok-4.5", "tokens": {"prompt": 1000, "completion": 0}})
    assert abs(v.gasto - 0.008) < 1e-12
    assert not v.permite() and v.bloqueadas == 1   # 0,008 + 2 × 0,003 ≥ 0,01
    assert alta.Vigilante(None, 8, 1.0).permite()   # sin tope (NaN)


def test_seco_tope_y_reanudacion():
    with tempfile.TemporaryDirectory() as d:
        args = ["--modelo", PENDIENTE, "--corta", "--seco", "--raiz", d, "--hilos", "3"]
        assert alta.main(args + ["--tope", "0.30"]) == 3          # se para por el tope
        manifs = [json.loads(f.read_text()) for f in pathlib.Path(d).glob("*/*/intento_*/manifest_run.json")]
        assert any(m["status"] == "failed" and m.get("exception_type") == "TopeDeGasto" for m in manifs)
        gasto = sum(m.get("gasto_estimado") or 0 for m in manifs if m["status"] == "failed")
        assert gasto < 0.30
        assert alta.main(args + ["--tope", "50"]) == 0             # se reanuda y termina
        pend = alta.plan(PENDIENTE, alta.cargar_corta(), leer=(alta.RES, pathlib.Path(d)))
        assert sum(len(x) for x in pend.values()) == 0
        # Los ids escritos no se repiten
        for f in pathlib.Path(d).glob("*/*/registros.jsonl"):
            ids = [json.loads(x)["id"] for x in f.read_text().splitlines()]
            assert len(ids) == len(set(ids)), f


def test_pago_sin_tope_no_lanza():
    def prohibido(*a, **k):   # si la guarda fallara, el test no debe gastar nada
        raise AssertionError("un id de OpenRouter sin --tope no debe lanzarse")
    original, alta.ejecutar = alta.ejecutar, prohibido
    try:
        alta.main(["--modelo", PENDIENTE, "--corta"])
    except SystemExit as e:
        assert "tope" in str(e)
    else:
        raise AssertionError("un id de OpenRouter sin --tope no debe lanzarse")
    finally:
        alta.ejecutar = original


def _respuestas(eleccion, juicio, n=60, seed=0):
    """Respuestas sintéticas: eleccion(item, orden, rep) → 'A'/'B'; juicio(item, orden) → bool."""
    el, ds = [], []
    for i in range(n):
        for orden in ("AB", "BA"):
            for rep in (0, 1):
                v = eleccion(i, orden, rep)
                el.append((f"I{i}", orden, rep, v, "OK", (v == "A") == (orden == "AB")))
            ds.append((f"I{i}", orden, "OK", juicio(i, orden)))
    return el, ds


def _nivel(el, ds):
    val, _ = vp.indices(el, ds)
    return max((vp._nivel(k, x) for k, x in val.items()), key=vp.NIVELES.index)


def test_validez():
    # Coherente: elige el polo alto en la mitad de las situaciones, siempre igual
    alto = lambda i, o: "A" if (i % 2 == 0) == (o == "AB") else "B"  # noqa: E731
    assert _nivel(*_respuestas(lambda i, o, r: alto(i, o), lambda i, o: i % 3 == 0)) == "válido"
    # Siempre «A»: posición pura
    assert _nivel(*_respuestas(lambda i, o, r: "A", lambda i, o: o == "AB")) == "no interpretable"
    # Al azar
    rnd = random.Random(1)
    assert _nivel(*_respuestas(lambda i, o, r: rnd.choice("AB"),
                               lambda i, o: rnd.random() < .5)) == "no interpretable"
    # 12 % de no válidas
    el, ds = _respuestas(lambda i, o, r: alto(i, o), lambda i, o: True)
    el = [x if k % 8 else (x[0], x[1], x[2], None, "INVALIDA", None) for k, x in enumerate(el)]
    val, _ = vp.indices(el, ds)
    assert vp._nivel("V2_no_validas", val["V2_no_validas"]) == "no interpretable"
    # Un ERROR_TECNICO no cuenta como no válida
    el, ds = _respuestas(lambda i, o, r: alto(i, o), lambda i, o: True)
    el[0] = (el[0][0], el[0][1], el[0][2], None, "ERROR_TECNICO", None)
    assert vp.indices(el, ds)[0]["V2_no_validas"] == 0


def test_revalidacion():
    """§41.3: un rasgo con señal pasa; uno de puro ruido pierde las marcas."""
    import numpy as np

    import cuadro_publico_v3 as cp
    from analizar_v3 import RASGOS, g4_consistencia
    rng = np.random.default_rng(0)
    ms = [f"m{k}" for k in range(12)]
    nivel = rng.normal(0, .15, len(ms))
    por_rasgo, faceta_de, a_d = {}, {}, {m: {} for m in ms}
    for t in RASGOS:
        its = [f"{t}{j}" for j in range(24)]
        por_rasgo[t] = its
        for j, i in enumerate(its):
            faceta_de[i] = f"f{j % 4}"
            for k, m in enumerate(ms):
                a_d[m][i] = (nivel[k] if t != "N" else 0) + rng.normal(0, .1)
    g3 = {t: (.5, 0.0) for t in RASGOS}
    rv = cp.revalidar_rasgos(a_d, ms, por_rasgo, faceta_de, {"G4": g4_consistencia(a_d, ms, por_rasgo), "G3": g3})
    assert all(rv[t]["pasa"] for t in RASGOS if t != "N"), rv
    assert not rv["N"]["pasa"] and "G4" in rv["N"]["motivo"]
    g3["O"] = (.1, .2)   # G3: dentro ≤ fuera
    rv = cp.revalidar_rasgos(a_d, ms, por_rasgo, faceta_de, {"G4": g4_consistencia(a_d, ms, por_rasgo), "G3": g3})
    assert not rv["O"]["pasa"] and "G3" in rv["O"]["motivo"]


def test_remedicion_mismos_prompts_semillas_nuevas():
    """§45.3: la re-medición repite ids y prompts del alta, con otra semilla."""
    import remedicion_validez as rv
    with tempfile.TemporaryDirectory() as d:
        base = alta.plan(NUEVO, None, leer=(pathlib.Path(d),))
        nueva = rv.plan(NUEVO, pathlib.Path(d))
    b = {t["id"]: t for ts in base.values() for t in ts}
    n = {t["id"]: t for tr in nueva.values() for ts in tr.values() for t in ts}
    assert set(b) == set(n) and len(n) == 2094
    assert all(n[i]["prompt"] == b[i]["prompt"] and n[i]["seed"] != b[i]["seed"] for i in b)
    assert all(n[i]["semilla_prefijo"] == rv.PREFIJO for i in n)
    assert {k: sum(len(x) for x in v.values()) for k, v in nueva.items()} == \
        {"deseabilidad": 698, "rep0": 698, "rep1": 698}


def test_forma_corta_no_se_publica():
    """§45.2: un modelo con solo la forma corta queda «pendiente de completar»."""
    import cuadro_publico_v3 as cp
    corta = cp.cargar_forma_corta()
    pp = cp.panel_publico(cp.selecciones_por_defecto(), corta=corta)
    for m, x in pp["pendientes"].items():
        assert m not in pp["panel"] and m not in pp["formas"] and x["rasgos_corta"]
    assert not pp["formas"]   # en el panel publicado no hay formas cortas
    pp2 = cp.panel_publico(cp.selecciones_por_defecto(), corta=corta, publicar_corta=True)
    assert not pp2["pendientes"]
    assert set(pp["pendientes"]) <= set(pp2["formas"]) | set(pp2["no_interpretables"])


if __name__ == "__main__":
    for nombre, f in list(globals().items()):
        if nombre.startswith("test_"):
            f()
            print(f"ok {nombre}")
