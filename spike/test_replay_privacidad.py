"""Privacidad del replay público (reauditoría 31-07, G8 y mutante 11).

El mutante 11 (quitar el filtro de `pensamiento` en `replay_publico`)
sobrevivía en v0.1.2: `test_schemas.py` y el dry-run seguían verdes porque
NINGÚN test comprobaba que el monólogo interno estuviera AUSENTE del artefacto
público. Aquí se comprueba, con canarios distintivos:

  1. un pensamiento privado (canal privado) NUNCA aparece en el JSON público
     —ni como evento, ni en meta, ni en ningún fragmento serializado—;
  2. la construcción es por WHITELIST: un evento de tipo desconocido, o un
     campo privado colado en un evento público, no se distribuyen;
  3. el canary detecta fugas cortas y normalizadas (comillas curvas, unicode).

Si el filtro/whitelist se rompe (mutante 11), este test se pone ROJO: o bien
el canario aparece en la salida, o bien `replay_publico` aborta fail-closed
—ambos cuentan como fuga detectada—.

Offline, sin red: apto para CI. Uso: python test_replay_privacidad.py
"""
import json

import export_replay


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


CANARIO_LARGO = "PENSAMIENTO_CANARIO_7f9c2ab1 esto no debe salir jamás"
CANARIO_CORTO = "SECRETO7"
CANARIO_COMILLAS = "el “plan” secreto—2026 no se dice"


def _replay_con_pensamientos():
    return {
        "version": 1,
        "meta": {"titulo": "t", "descripcion": "premisa pública",
                 "fecha": "f", "fuente": "concordia"},
        "agentes": [{"id": "a0", "nombre": "Marta", "rol": "", "color": "#000"}],
        "eventos": [
            {"tipo": "narrador", "texto": "Empieza la escena."},
            {"tipo": "paso", "n": 1},
            {"tipo": "pensamiento", "agente": "a0", "atribucion": "exacta",
             "texto": CANARIO_LARGO, "canal": "privado"},
            {"tipo": "pensamiento", "agente": "a0", "atribucion": "exacta",
             "texto": CANARIO_CORTO, "canal": "privado"},
            {"tipo": "pensamiento", "agente": "a0", "atribucion": "exacta",
             "texto": CANARIO_COMILLAS, "canal": "privado"},
            {"tipo": "dialogo", "agente": "a0", "atribucion": "exacta",
             "texto": "Buenos días a todos."},
        ],
    }


def _presente(canario, publico):
    """El canario, normalizado, ¿aparece en el JSON público normalizado?"""
    return (export_replay._normalizar(canario)
            in export_replay._normalizar(json.dumps(publico, ensure_ascii=False)))


def run():
    ok = True

    # 1 · Un replay con pensamientos: el público no contiene NINGÚN canario.
    replay = _replay_con_pensamientos()
    fuga = False
    try:
        publico = export_replay.replay_publico(replay)
        for canario in (CANARIO_LARGO, CANARIO_CORTO, CANARIO_COMILLAS):
            if _presente(canario, publico):
                fuga = True
        # Ningún evento de tipo pensamiento sobrevive.
        if any(e.get("tipo") == "pensamiento"
               or e.get("canal") == "privado"
               for e in publico.get("eventos", [])):
            fuga = True
    except RuntimeError:
        # El canary fail-closed saltó: la fuga se detuvo (también es "detecta").
        fuga = True
        publico = None
    ok &= _c(not fuga,
             "ningún pensamiento privado (largo/corto/con comillas) llega al"
             " replay público, ni como evento ni en meta/fragmentos")

    # 2 · Whitelist: un campo privado colado en un evento público se descarta,
    # y un tipo desconocido no se distribuye.
    replay2 = {
        "version": 1,
        "meta": {"titulo": "t", "descripcion": "d", "fecha": "f",
                 "fuente": "concordia", "secreto_meta": CANARIO_CORTO},
        "agentes": [{"id": "a0", "nombre": "Marta", "rol": "", "color": "#000"}],
        "eventos": [
            {"tipo": "dialogo", "agente": "a0", "atribucion": "exacta",
             "texto": "Hola", "pensamiento_oculto": CANARIO_LARGO},
            {"tipo": "tipo_desconocido_futuro", "texto": CANARIO_CORTO,
             "payload": CANARIO_LARGO},
        ],
    }
    publico2 = export_replay.replay_publico(replay2)
    ser2 = json.dumps(publico2, ensure_ascii=False)
    ok &= _c("secreto_meta" not in ser2 and "pensamiento_oculto" not in ser2
             and "tipo_desconocido_futuro" not in ser2
             and CANARIO_LARGO not in ser2,
             "whitelist: campos privados y tipos desconocidos no se distribuyen")

    # 3 · Un replay limpio (sin pensamientos) NO aborta y conserva lo público.
    limpio = {
        "version": 1,
        "meta": {"titulo": "t", "descripcion": "d", "fecha": "f",
                 "fuente": "concordia"},
        "agentes": [{"id": "a0", "nombre": "Marta", "rol": "", "color": "#000"}],
        "eventos": [{"tipo": "narrador", "texto": "Escena pública."},
                    {"tipo": "dialogo", "agente": "a0", "atribucion": "exacta",
                     "texto": "Hola a todos."}],
    }
    pub_limpio = export_replay.replay_publico(limpio)
    ok &= _c(len(pub_limpio["eventos"]) == 2
             and any(e["tipo"] == "dialogo" for e in pub_limpio["eventos"]),
             "un replay sin pensamientos conserva narrador y diálogo públicos")

    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
