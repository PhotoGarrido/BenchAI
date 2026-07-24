"""Re-ejecución de las 14 celdas de prisión con contaminación de trayectoria.

Contexto (auditoría + revisión Fable 24-07): el parser antiguo alimentó a la
simulación niveles mal clasificados (negativas→abuso, typos→NORMAL) en estas
celdas; el reproceso post-hoc no descontamina las trayectorias, así que se
repiten ENTERAS con el parser anclado ya integrado en experimento_prision.

Los runs antiguos NO se borran (queda el histórico + la errata); el análisis
prefiere automáticamente el run más reciente.

Uso: python relanzar_celdas.py
"""

import pathlib
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

AQUI = pathlib.Path(__file__).parent

# (modelo, flag) — exactamente las celdas con ≥1 registro mal-alimentado.
CELDAS = [
    ("anthropic/claude-haiku-4.5", "--coaching"),
    ("anthropic/claude-haiku-4.5", "--ordenes"),
    ("anthropic/claude-haiku-4.5", "--rebelion"),
    ("z-ai/glm-5.2", None),
    ("z-ai/glm-5.2", "--coaching"),
    ("z-ai/glm-5.2", "--ordenes"),
    ("anthropic/claude-sonnet-5", "--coaching"),
    ("anthropic/claude-fable-5", "--rebelion"),
    ("anthropic/claude-opus-4.8", "--ordenes"),
    ("qwen/qwen3.6-35b-a3b", None),
    ("qwen/qwen3.6-35b-a3b", "--ordenes"),
    ("qwen/qwen3.6-35b-a3b", "--rebelion"),
    ("gemma4", "--rebelion"),        # NaN, gratis
    ("qwen3.6", "--coaching"),       # NaN, gratis (los runs viejos: "default")
]


def correr(celda):
    modelo, flag = celda
    cmd = [sys.executable, str(AQUI / "experimento_prision.py"),
           "--modelo", modelo] + ([flag] if flag else [])
    et = f"{modelo.split('/')[-1]}{flag or ' (P1)'}"
    t0 = time.time()
    log = AQUI / "resultados" / "relanzar_celdas.log"
    with log.open("a", encoding="utf-8") as f:
        f.write(f"\n===== {et} · {' '.join(cmd)} =====\n"); f.flush()
        rc = subprocess.run(cmd, cwd=AQUI, stdout=f, stderr=f).returncode
    print(f"[{et}] {'OK' if rc == 0 else f'FALLO rc={rc}'} ·"
          f" {(time.time()-t0)/60:.1f} min", flush=True)
    return rc


def main():
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=6) as pool:
        rcs = list(pool.map(correr, CELDAS))
    fallos = sum(1 for rc in rcs if rc != 0)
    print(f"\n{len(CELDAS)-fallos}/{len(CELDAS)} celdas OK ·"
          f" {(time.time()-inicio)/60:.0f} min", flush=True)
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
