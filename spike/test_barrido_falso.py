"""Barrido con modelo falso sobre los CINCO flujos del modo estudio.

La herramienta que encontró el bug que ninguna revisión vio (crónica escribía
«cumpliste» en el diario del agente ante un None) era un barrido artesanal de
sesión; este fichero lo hace permanente (PLAN_MEJORA Fase 0.1). Un modelo
falso devuelve SIEMPRE la misma respuesta — vacía, ilegible o truncada — y se
ejecutan los flujos reales de asch, milgram, crónica, prisión y g2 de punta a
punta, afirmando el invariante central del proyecto:

    un fallo técnico o una respuesta ilegible JAMÁS se convierte en conducta,
    ni en el dato (registros/resúmenes) ni DENTRO de la simulación (diarios,
    boletines, empujones, historial).

Offline, sin claves y sin red: apto para CI.

Uso: python test_barrido_falso.py
"""

import argparse
import re

import parsers as P
import experimento_asch as asch
import experimento_milgram as milgram
import experimento_cronica as cronica_mod
import experimento_prision as prision
import experimento_g2 as g2
import experimento_gfinal as gfinal
import analizar_g2

NO_CONDUCTA = (P.ERROR_TECNICO, P.INVALIDA)


class ModeloFalso:
    """Devuelve siempre la misma respuesta y captura cada prompt recibido,
    para poder afirmar también sobre lo que ENTRA en la simulación."""

    def __init__(self, respuesta=""):
        self.respuesta = respuesta
        self.prompts = []

    def sample_text(self, prompt, **kw):
        self.prompts.append(prompt)
        return self.respuesta


# Cargas del barrido: el vacío (400/timeout del proveedor), el texto de error
# (respuesta ilegible con contenido) y un truncado a mitad de palabra por
# experimento (el patrón que la revisión Opus 5 llamó «vacío desplazado»).
ILEGIBLE = "Error 429: Too Many Requests {rate_limit_exceeded}"
SUPLICA = "Quiero hablar con el director."   # difflib 0,92 con QUIEBRO (bug 6)


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


def sin_frase(prompts, frase):
    return not any(frase in p for p in prompts)


def barrido_asch(payload, nombre):
    ok = True
    m = ModeloFalso(payload)
    regs, _ = asch.sesion(m, asch.SUJETOS[0], "mayoria", seed=1000)
    ok &= _c(all(r["publica"] is None and r["privada"] is None for r in regs),
             f"asch/{nombre}: ninguna letra parseada")
    ok &= _c(not any(r["conforma_publico"] or r["conforma_privado"]
                     or r["acierto_publico"] for r in regs),
             f"asch/{nombre}: sin conformidad ni acierto inventados")
    ok &= _c(not any(re.search(r"R\d+: [ABC]\b", p) for p in m.prompts),
             f"asch/{nombre}: el historial público no inventa respuestas")
    return ok


def barrido_milgram(payload, nombre):
    ok = True
    m = ModeloFalso(payload)
    regs, ruptura, cont, err_tec = milgram.sesion(
        m, milgram.SUJETOS[0], "autoridad")
    ok &= _c(err_tec and ruptura == 0 and len(regs) == 1,
             f"milgram/{nombre}: sesión abortada, ruptura 0 no-conductual")
    r = regs[0]
    ok &= _c(r["decision"] is None and r["estado"] in NO_CONDUCTA
             and r["prods"] == 0 and not r["disonancia"],
             f"milgram/{nombre}: sin decisión, sin empujones, sin disonancia")
    ok &= _c(sin_frase(m.prompts, "se niega"),
             f"milgram/{nombre}: no se inyecta «se niega» en el prompt")
    resumen = milgram.analizar(
        [{"sujeto": "x", "condicion": "autoridad", "ruptura": ruptura,
          "registros": regs, "error_tecnico": err_tec}], [cont])
    ok &= _c(resumen["sesiones_excluidas_error_tecnico"] == 1
             and "autoridad" not in resumen,
             f"milgram/{nombre}: la sesión queda excluida del análisis")
    return ok


def barrido_cronica(payload, nombre, v2=False):
    ok = True
    m = ModeloFalso(payload)
    args = argparse.Namespace(rapido=True, v2=v2, dias=10,
                              semilla=cronica_mod.SEMILLA_MUNDO)
    registros, sondas, dia_derog, estado_norma = cronica_mod.cronica(m, args)
    ok &= _c(all(r["decision"] is None and not r["valida"]
                 and r["estado"] in NO_CONDUCTA for r in registros),
             f"cronica/{nombre}: ninguna decisión inventada")
    ok &= _c(dia_derog is None and estado_norma == 0,
             f"cronica/{nombre}: el mundo no se mueve solo")
    ok &= _c(sin_frase(m.prompts, "cumpliste"),
             f"cronica/{nombre}: el diario no escribe «cumpliste» (bug 25-07)")
    ok &= _c(all(s["justa"] is None for s in sondas),
             f"cronica/{nombre}: sondas sin números inventados")
    resumen = cronica_mod.analizar(registros, sondas, dia_derog, estado_norma)
    ok &= _c(resumen["decisiones_invalidas_excluidas"] == len(registros)
             and resumen["por_semana"] == {},
             f"cronica/{nombre}: análisis excluye todo y no revienta")
    return ok


def barrido_prision(payload, nombre):
    ok = True
    m = ModeloFalso(payload)
    rs, ri = prision.cronica(m, "programa", 2, prision.SUPERVISORES[:2],
                             prision.INTERNOS[:2])
    ok &= _c(all(r["nivel"] is None and r["estado"] in NO_CONDUCTA
                 for r in rs),
             f"prision/{nombre}: ningún nivel de dureza inventado")
    ok &= _c(all(r["cree_justo"] is None for r in rs),
             f"prision/{nombre}: la sonda justa no imputa (era «NO not in»)")
    ok &= _c(all(r["respuesta"] is None and not r["valida"] for r in ri),
             f"prision/{nombre}: ninguna respuesta de interno inventada")
    ok &= _c(sin_frase(m.prompts, "actuaste de forma")
             and sin_frase(m.prompts, "se negó"),
             f"prision/{nombre}: diarios y resumen sin conducta inventada")
    a = prision.analizar(rs, ri, "programa")
    ok &= _c(a["severidad_final"] is None and a["actos_abusivos_pct"] is None
             and a["n_validos"] == 0 and a["quiebres"] == 0,
             f"prision/{nombre}: severidad None (no 0), sin quiebres")
    return ok


def barrido_g2(payload, nombre):
    ok = True
    m = ModeloFalso(payload)
    celda = {"fase": "a2", "contenido": "degradacion", "fuente": "orden",
             "negativa": True, "texto": g2.CONTENIDOS["degradacion"], "rep": 1}
    regs = g2.brazo(m, celda, dias=2)
    ok &= _c(all(r["nivel"] is None and r["estado"] in NO_CONDUCTA
                 and r["cree_justo"] is None and not r["disonancia"]
                 for r in regs),
             f"g2/{nombre}: sin nivel, sin justo, sin disonancia")
    res = g2.resumir(regs)
    ok &= _c(all(v["abusivos_pct"] is None for v in res.values()),
             f"g2/{nombre}: resumen sin tasas inventadas")
    props, excluidos = analizar_g2.cadenas(
        [dict(r, modelo="falso") for r in regs])
    ok &= _c(props == [] and excluidos == len(regs),
             f"g2/{nombre}: cadenas excluye todo (None jamás es «no abusó»)")
    return ok


def barrido_gfinal(payload, nombre):
    ok = True
    m = ModeloFalso(payload)
    celda = {"modulo": "A", "dominio": "laboral", "contenido": "degradacion",
             "clausula": True, "marco": "orden", "rep": 1}
    regs = gfinal.brazo(m, celda, dias=2)
    ok &= _c(all(r["nivel"] is None and r["estado"] in NO_CONDUCTA
                 and r["cree_justo"] is None and not r["disonancia"]
                 for r in regs),
             f"gfinal/{nombre}: sin nivel, sin justo, sin disonancia")
    ok &= _c(sin_frase(m.prompts, "actuaste de forma"),
             f"gfinal/{nombre}: el diario no inventa conducta")
    ok &= _c(all(r["justo_estado"] == "NO_PREGUNTADA" for r in regs),
             f"gfinal/{nombre}: la sonda privada no se pregunta tras fallo")
    ok &= _c(sin_frase(m.prompts, "poco clara")
             and sin_frase(m.prompts, "Hoy has optado"),
             f"gfinal/{nombre}: sin glosas agramaticales inyectadas")
    res = gfinal.resumir(regs)
    ok &= _c(all(v["abuso_conductual"] is None and v["n_missing"] == v["n"]
                 for v in res.values()),
             f"gfinal/{nombre}: resumen excluye y reporta missingness")
    return ok


class ModeloGuion(ModeloFalso):
    """Devuelve respuestas conductuales válidas para ejercitar el flujo
    completo (el barrido de canal privado necesita que la privada se pregunte)."""

    def sample_text(self, prompt, **kw):
        self.prompts.append(prompt)
        if "fuero interno" in prompt:
            return "NO, no me parece justo — RESPUESTA-PRIVADA-CENTINELA"
        if "REALMENTE" in prompt:
            return "Me piden mano dura con el grupo."
        return "ESTRICTO — aplico el reglamento sin margen."


def barrido_canal_privado():
    """Regla de los dos canales (revisión externa, CI 'test del canal
    privado'): ni la PREGUNTA privada ni su RESPUESTA pueden aparecer en
    ningún prompt público o de interpretación posterior."""
    ok = True
    m = ModeloGuion()
    celda = {"modulo": "A", "dominio": "prision", "contenido": "degradacion",
             "clausula": False, "marco": "orden", "rep": 1}
    gfinal.brazo(m, celda, dias=3)
    publicos = [p for p in m.prompts if "fuero interno" not in p]
    ok &= _c(all("RESPUESTA-PRIVADA-CENTINELA" not in p for p in publicos),
             "canal privado: la respuesta privada jamás entra en otro prompt")
    ok &= _c(all("nadie lo sabrá" not in p for p in publicos),
             "canal privado: la pregunta privada jamás entra en otro prompt")
    ok &= _c(any("actuaste de forma estricto" in p.lower() for p in m.prompts),
             "canal público: el diario sí propaga la conducta pública")
    return ok


def run():
    ok = True
    cargas = [("vacio", ""), ("ilegible", ILEGIBLE)]
    for nombre, payload in cargas + [("truncado", "La variante más larga es la")]:
        ok &= barrido_asch(payload, nombre)
    for nombre, payload in cargas + [("truncado", "APLI")]:
        ok &= barrido_milgram(payload, nombre)
    for nombre, payload in cargas + [("truncado", "CLAND")]:
        ok &= barrido_cronica(payload, nombre)
    ok &= barrido_cronica("", "vacio+v2", v2=True)
    for nombre, payload in cargas + [("truncado", "DESHU"),
                                     ("suplica", SUPLICA)]:
        ok &= barrido_prision(payload, nombre)
    for nombre, payload in cargas + [("truncado", "DESHU")]:
        ok &= barrido_g2(payload, nombre)
    for nombre, payload in cargas + [("truncado", "DESHU")]:
        ok &= barrido_gfinal(payload, nombre)
    ok &= barrido_canal_privado()
    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
