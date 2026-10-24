"""Bucle común de las baterías de personalidad: ejecuta tareas de una sola
llamada, en serie o con N hilos, y escribe cada registro en cuanto llega
(reanudable: quien llama filtra lo ya hecho).

Los hilos usan `manifiesto.map_paralelo`, que propaga el manifiesto activo a
cada worker (si no, las solicitudes físicas se perderían del registro). El
grifo y la tasa por proveedor siguen siendo los de model_factory, así que
`hilos` solo sirve de algo donde el proveedor admite concurrencia
(OpenRouter); en NaN se corre con 1.
"""

import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import manifiesto


def ejecutar(tareas, hacer_registro, fichero, etiqueta, hilos=1, cada=100):
    """`fichero`: ruta jsonl, o función que recibe cada registro (se llama bajo lock)."""
    lock = threading.Lock()
    hechas = [0]
    inicio = time.time()

    def uno(t):
        reg = hacer_registro(t)
        with lock:
            if callable(fichero):          # destino variable: lo decide quien llama
                fichero(reg)
            else:
                with fichero.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(reg, ensure_ascii=False) + "\n")
            hechas[0] += 1
            n = hechas[0]
        if n % cada == 0 or n == len(tareas):
            print(f"[{etiqueta}] {n}/{len(tareas)} · {time.time() - inicio:.0f}s",
                  flush=True)

    if hilos <= 1:
        for t in tareas:
            uno(t)
        return
    with ThreadPoolExecutor(max_workers=hilos) as pool:
        manifiesto.map_paralelo(pool, uno, tareas)
