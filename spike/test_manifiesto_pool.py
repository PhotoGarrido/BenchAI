"""Registro de solicitudes físicas CON pools (reauditoría 31-07, P0.2).

La regresión demostrada por la reauditoría: `_ACTIVO` vive en un ContextVar
y los workers de ThreadPoolExecutor nacen con contexto vacío, así que las
llamadas hechas dentro de un pool no se registraban y el run terminaba
`completed` con `solicitudes=0`. Este test ejercita los SEIS entrypoints
del modo estudio (asch, milgram, crónica, prisión, g2, g-final) con un
proveedor falso que registra cada solicitud física igual que el real, y
afirma:

  1. el número de líneas de solicitudes.jsonl es EXACTAMENTE el número de
     llamadas físicas del modelo — también en los cuatro flujos con
     ThreadPoolExecutor (crónica, prisión, g2, g-final);
  2. la cabecera cierra completed con ese recuento (o failed si el flujo
     revienta);
  3. dos runs concurrentes con manifiestos distintos no se mezclan: cada
     jsonl contiene solo las solicitudes de su run.

Offline, sin claves y sin red: apto para CI.

Uso: python test_manifiesto_pool.py
"""

import argparse
import json
import pathlib
import tempfile
import threading

import manifiesto
import experimento_asch as asch
import experimento_milgram as milgram
import experimento_cronica as cronica_mod
import experimento_prision as prision
import experimento_g2 as g2
import experimento_gfinal as gfinal


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


class ModeloRegistrador:
    """Proveedor falso: registra cada solicitud FÍSICA en el manifiesto
    activo (como hace NaNLanguageModel) y responde con conducta válida para
    que el flujo pregunte también las sondas."""

    def __init__(self, marca):
        self.marca = marca
        self.n = 0
        self._lock = threading.Lock()

    def sample_text(self, prompt, **kw):
        with self._lock:
            self.n += 1
        manifiesto.registrar({"modelo": "falso", "run": self.marca,
                              "prompt_sha256": manifiesto.sha256_texto(prompt),
                              "respuesta": "x"})
        if "fuero interno" in prompt:
            return "NO, no me parece justo."
        if "REALMENTE" in prompt:
            return "Me piden mano dura con el grupo."
        return "ESTRICTO — aplico el reglamento sin margen."


def _lineas(td):
    f = pathlib.Path(td) / "solicitudes.jsonl"
    if not f.exists():
        return []
    return [json.loads(x) for x in f.open(encoding="utf-8")]


def _flujos():
    """Los seis entrypoints, por su función núcleo (la misma que usa el
    barrido con modelo falso), incluidos los que abren pools por dentro."""
    return [
        ("asch", lambda m: asch.sesion(m, asch.SUJETOS[0], "mayoria",
                                       seed=1000)),
        ("milgram", lambda m: milgram.sesion(m, milgram.SUJETOS[0],
                                             "autoridad")),
        ("cronica[pool]", lambda m: cronica_mod.cronica(
            m, argparse.Namespace(rapido=True, v2=False, dias=4,
                                  semilla=cronica_mod.SEMILLA_MUNDO))),
        ("prision[pool]", lambda m: prision.cronica(
            m, "programa", 2, prision.SUPERVISORES[:2],
            prision.INTERNOS[:2])),
        ("g2[pool]", lambda m: g2.brazo(
            m, {"fase": "a2", "contenido": "degradacion", "fuente": "orden",
                "negativa": True, "texto": g2.CONTENIDOS["degradacion"],
                "rep": 1}, dias=2)),
        ("gfinal[pool]", lambda m: gfinal.brazo(
            m, {"modulo": "A", "dominio": "prision",
                "contenido": "degradacion", "clausula": False,
                "marco": "orden", "rep": 1}, dias=2)),
    ]


def run():
    ok = True
    manifiesto.activar_instancia(None)

    # 1+2 · Conteo exacto por entrypoint, con estado final completed.
    for nombre, flujo in _flujos():
        with tempfile.TemporaryDirectory() as td:
            m = ModeloRegistrador(nombre)
            with manifiesto.RunManifest(td, {"flujo": nombre}):
                flujo(m)
            cab = json.loads(
                (pathlib.Path(td) / "manifest_run.json").read_text())
            lineas = _lineas(td)
            ok &= _c(m.n > 0 and len(lineas) == m.n
                     and cab["solicitudes"] == m.n
                     and cab["status"] == "completed",
                     f"{nombre}: {m.n} llamadas físicas = {len(lineas)}"
                     f" líneas = solicitudes en cabecera (completed)")

    # 2b · Un flujo que revienta dentro del pool cierra failed sin perder
    # las solicitudes ya hechas.
    class ModeloQueRevienta(ModeloRegistrador):
        def sample_text(self, prompt, **kw):
            super().sample_text(prompt, **kw)
            if self.n >= 3:
                raise RuntimeError("proveedor caído")
            return "ESTRICTO — aplico el reglamento sin margen."

    with tempfile.TemporaryDirectory() as td:
        m = ModeloQueRevienta("failed")
        try:
            with manifiesto.RunManifest(td, {}):
                gfinal.brazo(m, {"modulo": "A", "dominio": "prision",
                                 "contenido": "degradacion",
                                 "clausula": False, "marco": "orden",
                                 "rep": 1}, dias=2)
            ok &= _c(False, "el flujo debía propagar la excepción del worker")
        except RuntimeError:
            cab = json.loads(
                (pathlib.Path(td) / "manifest_run.json").read_text())
            ok &= _c(cab["status"] == "failed"
                     and cab["solicitudes"] == len(_lineas(td)) == m.n,
                     f"fallo en worker → failed con las {m.n} solicitudes"
                     " registradas")

    # 3 · Dos runs concurrentes (hilos distintos, manifiestos distintos,
    # pools por dentro): cero mezcla.
    resultados = {}

    def correr(marca, td):
        m = ModeloRegistrador(marca)
        with manifiesto.RunManifest(td, {"run": marca}):
            gfinal.brazo(m, {"modulo": "A", "dominio": "prision",
                             "contenido": "degradacion", "clausula": False,
                             "marco": "orden", "rep": 1}, dias=2)
        resultados[marca] = m.n

    with tempfile.TemporaryDirectory() as td1, \
            tempfile.TemporaryDirectory() as td2:
        h1 = threading.Thread(target=correr, args=("RUN-A", td1))
        h2 = threading.Thread(target=correr, args=("RUN-B", td2))
        h1.start(); h2.start(); h1.join(); h2.join()
        l1, l2 = _lineas(td1), _lineas(td2)
        ok &= _c(len(l1) == resultados["RUN-A"]
                 and len(l2) == resultados["RUN-B"]
                 and all(x["run"] == "RUN-A" for x in l1)
                 and all(x["run"] == "RUN-B" for x in l2),
                 f"dos runs concurrentes sin mezcla (A={len(l1)},"
                 f" B={len(l2)}; cada jsonl solo con su marca)")

    manifiesto.activar_instancia(None)
    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
