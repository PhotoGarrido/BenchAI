"""Tests del RunManifest (Fase 0.4 + revisión R3): cabecera con procedencia y
dependencias, solicitudes con timestamp, estado final garantizado por el
context manager (completed/failed), tolerancia a errores de serialización,
no-op sin activar, y el fallback de sample_choice sin imputación (hallazgo 4)."""
import json
import pathlib
import tempfile

import manifiesto
import model_factory


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


def run():
    ok = True
    manifiesto.activar_instancia(None)
    manifiesto.registrar({"x": 1})   # sin activar: no escribe ni revienta
    ok &= _c(True, "sin activar: no-op")

    with tempfile.TemporaryDirectory() as td:
        with manifiesto.RunManifest(td, {"modelo": "test"},
                                    hashes={"escenario": "abc"}):
            manifiesto.registrar({"modelo": "m", "prompt": "p",
                                  "respuesta": "r"})
            manifiesto.registrar({"modelo": "m", "error": "boom"})
            manifiesto.registrar({"raro": object()})   # no serializable
        cab = json.loads((pathlib.Path(td) / "manifest_run.json").read_text())
        ok &= _c(cab.get("commit") and cab.get("parser_version")
                 and cab["hashes"] == {"escenario": "abc"}
                 and "openai" in cab.get("dependencias", {}),
                 "cabecera con commit, parser, hashes y dependencias")
        ok &= _c(cab["status"] == "completed" and cab["solicitudes"] == 3
                 and cab["errores"] == 1,
                 "estado final completed con recuentos")
        lineas = [json.loads(l) for l in
                  (pathlib.Path(td) / "solicitudes.jsonl").open()]
        ok &= _c(len(lineas) == 3 and all("ts" in l for l in lineas),
                 "3 solicitudes con timestamp (incl. no-serializable)")

    with tempfile.TemporaryDirectory() as td:
        try:
            with manifiesto.RunManifest(td, {}):
                raise ValueError("bum")
        except ValueError:
            pass
        cab = json.loads((pathlib.Path(td) / "manifest_run.json").read_text())
        ok &= _c(cab["status"] == "failed"
                 and cab["exception_type"] == "ValueError",
                 "excepción → status failed con tipo registrado")

    # ── sample_choice sin imputación (hallazgo 4) ────────────────────────
    m = object.__new__(model_factory.NaNLanguageModel)
    m._model, m._proveedor = "falso", "test"
    m.sample_text = lambda *a, **k: "%% ilegible %%"
    try:
        model_factory.NaNLanguageModel.sample_choice(
            m, "q", ["golpear la puerta", "gritar", "salir"])
        ok &= _c(False, "sin opción neutra debía lanzar excepción")
    except model_factory.RespuestaIlegibleError:
        ok &= _c(True, "sample_choice sin neutra → RespuestaIlegibleError"
                       " (jamás un índice de acción real)")
    idx2, eleccion2, meta2 = model_factory.NaNLanguageModel.sample_choice(
        m, "q", ["golpear", "no hace nada", "gritar"])
    ok &= _c(idx2 == 1 and eleccion2 == "no hace nada"
             and meta2.get("choice_state") == "INVALIDA",
             "con neutra: índice y texto COHERENTES + INVALIDA registrada")

    # ── G4 producción: el objeto de build_model es fail-closed al límite ──
    # (reauditoría 31-07, P0-D): CallLimitLanguageModel de Concordia devuelve
    # la opción 0 —una acción real— al agotar el límite; LimiteFailClosed lo
    # convierte en excepción tipada. Se prueba el OBJETO que devuelve
    # build_model, no la clase base.
    import os
    _env = {k: os.environ.get(k) for k in
            ("NAN_BASE_URL", "NAN_API_KEY", "NAN_MODEL", "PSICOAI_MAX_CALLS")}
    os.environ.update({"NAN_BASE_URL": "http://x", "NAN_API_KEY": "x",
                       "NAN_MODEL": "modelo-falso", "PSICOAI_MAX_CALLS": "0"})
    try:
        prod = model_factory.build_model(dry_run=False)
        ok &= _c(isinstance(prod, model_factory.LimiteFailClosed),
                 "build_model envuelve el objeto productivo en LimiteFailClosed")
        ok &= _c(getattr(prod._model._model._client, "max_retries", None) == 0,
                 "el cliente OpenAI se crea con max_retries=0 (G3)")
        try:
            prod.sample_choice("q", ["golpear la puerta", "gritar", "salir"])
            ok &= _c(False, "límite agotado debía LANZAR, no devolver opción 0")
        except model_factory.LimiteDeLlamadasError:
            ok &= _c(True, "sample_choice al límite → LimiteDeLlamadasError"
                           " (jamás la opción 0)")
        try:
            prod.sample_text("q")
            ok &= _c(False, "sample_text al límite debía LANZAR, no ''")
        except model_factory.LimiteDeLlamadasError:
            ok &= _c(True, "sample_text al límite → LimiteDeLlamadasError")
    finally:
        for k, v in _env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        manifiesto.activar_instancia(None)

    # ── G3: reintentos FÍSICOS = líneas del manifiesto (500→500→200) ───────
    # Cada intento físico registra una línea (error o éxito); el SDK ya no
    # reintenta por dentro (max_retries=0), así que RetryLanguageModel es el
    # único que reintenta y el recuento cuadra.
    import types
    from concordia.language_model import retry_wrapper

    class _FakeCreate:
        def __init__(self):
            self.n = 0

        def __call__(self, **kw):
            self.n += 1
            if self.n <= 2:
                raise RuntimeError("500 Internal Server Error")
            usage = types.SimpleNamespace(prompt_tokens=10, completion_tokens=5,
                                          total_tokens=15)
            msg = types.SimpleNamespace(content="ESTRICTO — aplico.")
            return types.SimpleNamespace(
                id="req-xyz", model="modelo-falso", usage=usage,
                choices=[types.SimpleNamespace(message=msg)])

    nan = object.__new__(model_factory.NaNLanguageModel)
    nan._model, nan._proveedor = "modelo-falso", "test"
    nan._sem = model_factory._SEMAFORO
    fake = _FakeCreate()
    nan._client = types.SimpleNamespace(
        chat=types.SimpleNamespace(
            completions=types.SimpleNamespace(create=fake)))
    modelo_retry = retry_wrapper.RetryLanguageModel(
        nan, retry_tries=4, retry_delay=0.0, exponential_backoff=False,
        jitter=(0.0, 0.0))
    with tempfile.TemporaryDirectory() as td:
        with manifiesto.RunManifest(td, {}):
            texto = modelo_retry.sample_text("hola", max_tokens=64,
                                             temperature=0.7)
        lineas = [json.loads(l) for l in
                  (pathlib.Path(td) / "solicitudes.jsonl").open()]
        n_err = sum(1 for l in lineas if l.get("error"))
        ok &= _c(len(lineas) == 3 and n_err == 2 and fake.n == 3
                 and texto.startswith("ESTRICTO"),
                 "500→500→200: 3 intentos FÍSICOS = 3 líneas (2 error + 1 ok)")

    # ── G3: un fallo de escritura impide cerrar 'completed' ────────────────
    with tempfile.TemporaryDirectory() as td:
        (pathlib.Path(td) / "solicitudes.jsonl").mkdir()   # sabotea el append
        with manifiesto.RunManifest(td, {}):
            manifiesto.registrar({"modelo": "m", "respuesta": "r"})
        cab = json.loads((pathlib.Path(td) / "manifest_run.json").read_text())
        ok &= _c(cab["status"] == "degraded" and cab["solicitudes"] == 0
                 and cab.get("fallo_escritura") is True,
                 "fallo de append → 'degraded', contador 0 (nunca 'completed')")
        manifiesto.activar_instancia(None)

    # ── G11: SIGKILL entre escritura y replace ─────────────────────────────
    import signal
    import subprocess
    import sys as _sys
    import textwrap
    with tempfile.TemporaryDirectory() as td:
        script = textwrap.dedent(f"""
            import os, signal, pathlib, manifiesto
            def _kill_replace(src, dst):
                os.kill(os.getpid(), signal.SIGKILL)
            os.replace = _kill_replace
            manifiesto.RunManifest(pathlib.Path({td!r}), {{}})
        """)
        r = subprocess.run([_sys.executable, "-c", script],
                           cwd=str(pathlib.Path(__file__).parent),
                           capture_output=True)
        outdir = pathlib.Path(td)
        definitivo = outdir / "manifest_run.json"
        tmps = list(outdir.glob("*.tmp"))
        ok &= _c(r.returncode == -signal.SIGKILL and not definitivo.exists()
                 and len(tmps) >= 1,
                 "SIGKILL entre escritura y replace: sin manifest_run.json"
                 " definitivo, solo .tmp de nombre único (nunca .json.tmp fijo)")
        with manifiesto.RunManifest(td, {}):
            pass
        ok &= _c(not list(outdir.glob("*.tmp")) and definitivo.exists(),
                 "reabrir el outdir limpia los .tmp huérfanos (G11)")
        manifiesto.activar_instancia(None)

    manifiesto.activar_instancia(None)
    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
