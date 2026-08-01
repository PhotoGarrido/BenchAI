"""El linter corre ANTES de gastar (reauditoría 31-07, mutante 8).

El mutante 8 (eliminar la llamada al linter previa al run en
`experimento_gfinal.main`) sobrevivía en v0.1.2: la puerta prueba el linter
por separado (`experimento_gfinal.py --linter`), pero NADA comprobaba que
`main` invoque el linter y ABORTE antes de construir el proveedor y gastar.

Aquí se fuerza un linter que falla y se comprueba que:
  · `main` termina con SystemExit citando el linter;
  · `build_model` NUNCA se invocó (no se abrió proveedor ni se gastó).

Si el mutante 8 quita la puerta previa, `build_model` sí se invoca → el
sentinel lo detecta y el test se pone ROJO.

Offline, sin red: apto para CI. Uso: python test_gfinal_linter.py
"""
import sys
import tempfile

import experimento_gfinal as gfinal
import model_factory


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


def run():
    ok = True
    llamado = {"build": 0}

    def _build_centinela(*a, **k):
        llamado["build"] += 1
        raise RuntimeError("build_model NO debía invocarse: el linter debía"
                           " abortar antes de gastar")

    orig_build = model_factory.build_model
    orig_validar = gfinal.validar_linter
    argv0 = sys.argv[:]
    try:
        # El proveedor jamás debe construirse en este test.
        model_factory.build_model = _build_centinela
        gfinal.model_factory.build_model = _build_centinela
        # Forzamos un linter que falla (independiente de que exista o no la
        # llamada previa: si el mutante la borra, nuestro False no se consulta
        # y build_model se alcanza → lo detecta el centinela).
        gfinal.validar_linter = lambda *a, **k: False
        with tempfile.TemporaryDirectory() as td:
            sys.argv = ["experimento_gfinal.py", "--fase", "A",
                        "--modelos", "x", "--out", td]
            resultado = "sin-systemexit"
            try:
                gfinal.main()
            except SystemExit as e:
                resultado = str(e)
            except RuntimeError as e:
                resultado = f"RUNTIME:{e}"
        ok &= _c(llamado["build"] == 0,
                 "build_model NO se invocó (el linter abortó antes de gastar)")
        ok &= _c("linter" in resultado.lower(),
                 f"main abortó citando el linter (salida: {resultado[:60]!r})")
    finally:
        model_factory.build_model = orig_build
        gfinal.model_factory.build_model = orig_build
        gfinal.validar_linter = orig_validar
        sys.argv = argv0

    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
