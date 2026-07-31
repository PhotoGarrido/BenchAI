"""Neutralización de variables sensibles con CANARIOS (reauditoría 31-07,
P1.8 — regresión P0: el scrub recorría `poblacion` como lista siendo un
objeto y los agentes generados conservaban origen, NSE, idioma, ideología,
religiosidad, salud y atractivo).

Estrategia: canarios de texto inconfundibles en TODAS las posiciones reales
de la estructura (protagonistas, poblacion.agentes_generados, distribuciones
de poblacion, variantes, formas legacy) y afirmación doble:

  1. tras neutralizar_sensibles(), ningún canario sobrevive en el JSON
     serializado del escenario;
  2. tras verbalizar (texto_persona / persona_de_poblacion), ningún canario
     ni rasgo sensible aparece en el bloque de identidad que ve el modelo.

Además: la política del motor es DEFAULT SEGURO — run_spike neutraliza
salvo variables_sensibles=true — y se prueba contra el validador real.

Offline, sin claves y sin red: apto para CI.

Uso: python test_sensibles.py
"""

import copy
import json

import personas
import run_spike


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


CANARIOS = ("CANARIO_ORIGEN", "CANARIO_NSE", "CANARIO_IDIOMA")


def _escenario_canario():
    return {
        "version": 1,
        "variables_sensibles": False,
        "titulo": "t", "premisa": "p", "pasos": 2,
        "protagonistas": [{
            "nombre": "Marta", "rol": "directora",
            "demografia": {"edad": 50, "genero": "mujer",
                           "origen_cultural": "CANARIO_ORIGEN",
                           "nse": "CANARIO_NSE", "educacion": "superior"},
            "big5": {"o": 50, "c": 50, "e": 50, "a": 50, "n": 50},
            "avanzados": {"ideologia": 99, "religiosidad": 99, "salud": 1,
                          "atractivo": 99, "antiguedad": 80,
                          "idioma": "CANARIO_IDIOMA"},
        }],
        "poblacion": {
            "n": 1, "modo": "reglas", "semilla": "s",
            "demografia": {
                "edad": [20, 60], "pct_mujeres": 50,
                "origenes_culturales": [{"nombre": "CANARIO_ORIGEN",
                                         "pct": 100}],
            },
            "mas_atributos": {"ideologia_media": 99,
                              "religiosidad_media": 99, "salud_media": 1,
                              "atractivo_media": 99, "antiguedad_media": 50,
                              "pct_otra_lengua": 100},
            "agentes_generados": [{
                "nom": "Gael", "rol": "Residentes", "edad": 40,
                "gen": "hombre", "ori": "CANARIO_ORIGEN",
                "nse": "CANARIO_NSE", "edu": "media",
                "idi": "CANARIO_IDIOMA",
                "b": {"o": 50, "c": 50, "e": 50, "a": 50, "n": 50},
                "b2": {"ideo": 99, "reli": 99, "anti": 50, "salud": 1,
                       "atr": 99},
            }],
        },
        "variantes": [
            {"nombre": "más conservadores",
             "cambios": [{"param": "t2_ideo", "op": "sumar", "val": 25},
                         {"param": "pctMuj", "op": "fijar", "val": 80},
                         {"param": "idiomaPct", "op": "fijar", "val": 100}]},
        ],
        # Formas legacy/hostiles: lista suelta de agentes y anidamiento raro.
        "agentes": [{"nombre": "L", "ori": "CANARIO_ORIGEN",
                     "b2": {"ideo": 99}}],
        "extra": {"anidado": [{"avanzados": {"idioma": "CANARIO_IDIOMA"},
                               "demografia": {"nse": "CANARIO_NSE"}}]},
    }


RASGOS_SENSIBLES = ("ideas progresistas", "ideas conservadoras",
                    "religiosidad", "salud frágil", "salud robusta",
                    "poco agraciado", "muy atractivo", "Habla ")


def run():
    ok = True

    esc = _escenario_canario()
    personas.neutralizar_sensibles(esc)
    serializado = json.dumps(esc, ensure_ascii=False)
    for c in CANARIOS:
        ok &= _c(c not in serializado,
                 f"escenario neutralizado sin rastro de {c}")

    # Verbalización real: lo que vería el modelo.
    txt_prota = personas.texto_persona(esc["protagonistas"][0])
    gen = esc["poblacion"]["agentes_generados"][0]
    txt_pob = personas.texto_persona(personas.persona_de_poblacion(gen))
    for etiqueta, txt in (("protagonista", txt_prota), ("población", txt_pob)):
        ok &= _c(not any(c in txt for c in CANARIOS),
                 f"identidad de {etiqueta} sin canarios")
        ok &= _c(not any(r in txt for r in RASGOS_SENSIBLES),
                 f"identidad de {etiqueta} sin rasgos sensibles verbalizados")

    # Distribuciones y variantes: nada sensible puede volver por ahí.
    pob = esc["poblacion"]
    ok &= _c("origenes_culturales" not in pob.get("demografia", {}),
             "poblacion.demografia sin origenes_culturales")
    ok &= _c(not any(k in (pob.get("mas_atributos") or {})
                     for k in ("ideologia_media", "religiosidad_media",
                               "salud_media", "atractivo_media",
                               "pct_otra_lengua")),
             "poblacion.mas_atributos sin medias sensibles")
    params = [c["param"] for v in esc["variantes"] for c in v["cambios"]]
    ok &= _c("t2_ideo" not in params and "idiomaPct" not in params
             and "pctMuj" in params,
             "variantes: cambios sensibles fuera, no sensibles intactos")

    # Lo no sensible sobrevive (el scrub no arrasa el escenario).
    ok &= _c(esc["protagonistas"][0]["avanzados"].get("antiguedad") == 80
             and esc["protagonistas"][0]["demografia"].get("educacion")
             == "superior"
             and gen["b2"].get("anti") == 50 and gen.get("edu") == "media",
             "atributos no sensibles (antigüedad, educación) intactos")

    # Política del motor: DEFAULT SEGURO en el validador real.
    con_flag_false = _escenario_canario()
    run_spike.cargar_y_validar_escenario(con_flag_false, "(test)")
    ok &= _c("CANARIO" not in json.dumps(con_flag_false, ensure_ascii=False),
             "motor: variables_sensibles=false neutraliza")

    sin_flag = _escenario_canario()
    del sin_flag["variables_sensibles"]
    run_spike.cargar_y_validar_escenario(sin_flag, "(test)")
    ok &= _c("CANARIO" not in json.dumps(sin_flag, ensure_ascii=False),
             "motor: flag AUSENTE → default seguro (neutraliza)")

    con_true = _escenario_canario()
    con_true["variables_sensibles"] = True
    run_spike.cargar_y_validar_escenario(con_true, "(test)")
    ok &= _c("CANARIO_ORIGEN" in json.dumps(con_true, ensure_ascii=False),
             "motor: true explícito conserva (consentimiento consciente)")

    # El integrado pasa por la misma puerta sin neutralizarse (declara true).
    integrado = copy.deepcopy(run_spike.ESCENARIO_DEFECTO)
    run_spike.cargar_y_validar_escenario(integrado, "(integrado)")
    ok &= _c(integrado == run_spike.ESCENARIO_DEFECTO
             and integrado["protagonistas"][0]["avanzados"].get("ideologia")
             is not None,
             "ESCENARIO_DEFECTO: valida contra el schema y no se altera")

    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
