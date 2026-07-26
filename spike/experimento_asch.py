"""Experimento 1 de PsicoAI: conformidad tipo Asch, isomorfa y disfrazada.

Réplica del paradigma de Asch (1951/1956) con agentes LLM, al estilo de
Aher et al. 2023: procedimiento controlado con llamadas directas (los
cómplices son guion, como los actores del experimento original), sin
Game Master. La simulación libre es para episodios; esto es un banco
de pruebas.

Diseño:
  - Disfraz isomorfo: panel de control de calidad de audio. Seis
    "revisores" miden la duración de tres variantes (A/B/C) de un clip
    y dicen por turnos cuál es la MÁS LARGA. Las mediciones del sujeto
    son inequívocas (la correcta gana por >1 s).
  - 12 rondas por sesión: las 2 primeras neutrales (mayoría acierta),
    7 críticas (mayoría unánime se equivoca) y 3 neutrales intercaladas.
  - Condiciones: control (el sujeto responde primero: precisión base),
    mayoria (5 cómplices erran antes que él), aliado (4 erran, 1 acierta).
  - Canal privado por bifurcación de contexto: llamada paralela con el
    mismo contexto que pregunta el juicio sincero. Nunca entra en la
    transcripción pública (regla de los dos canales).
  - 10 sujetos con Big Five variado × 3 condiciones (intra-sujeto).
  - Sonda de contaminación al final de cada sesión.

Uso:
  python experimento_asch.py --rapido      # smoke: 2 personas
  python experimento_asch.py               # completo: 10 personas
"""

import argparse
import datetime
import json
import pathlib
import random
import re
import statistics
import time

from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).parent / ".env")

import manifiesto
import model_factory
import personas

N_RONDAS = 12
RONDAS_CRITICAS = {3, 4, 6, 7, 9, 11, 12}   # 7 críticas; 1-2 neutrales de confianza
LETRAS = ["A", "B", "C"]

# ── Sujetos: 10 perfiles que barren el espacio Big Five ──────────────────
SUJETOS = [
    {"nombre": "Irene Vallejo", "big5": {"o": 45, "c": 55, "e": 30, "a": 85, "n": 80},
     "demografia": {"edad": 27, "genero": "mujer", "origen_cultural": "local", "nse": "medio", "educacion": "media"}},
    {"nombre": "Bruno Salas", "big5": {"o": 85, "c": 45, "e": 75, "a": 25, "n": 25},
     "demografia": {"edad": 41, "genero": "hombre", "origen_cultural": "local", "nse": "medio", "educacion": "superior"}},
    {"nombre": "Rosa Mena", "big5": {"o": 30, "c": 85, "e": 45, "a": 70, "n": 50},
     "demografia": {"edad": 58, "genero": "mujer", "origen_cultural": "local", "nse": "medio", "educacion": "básica"}},
    {"nombre": "Óscar Lindo", "big5": {"o": 50, "c": 30, "e": 85, "a": 55, "n": 65},
     "demografia": {"edad": 23, "genero": "hombre", "origen_cultural": "latinoamericano", "nse": "bajo", "educacion": "media"}},
    {"nombre": "Nadia Ferrer", "big5": {"o": 75, "c": 70, "e": 50, "a": 45, "n": 35},
     "demografia": {"edad": 36, "genero": "mujer", "origen_cultural": "magrebí", "nse": "medio", "educacion": "superior"}},
    {"nombre": "Tomás Iriarte", "big5": {"o": 20, "c": 60, "e": 25, "a": 80, "n": 70},
     "demografia": {"edad": 63, "genero": "hombre", "origen_cultural": "local", "nse": "medio", "educacion": "básica"}},
    {"nombre": "Carla Bosch", "big5": {"o": 60, "c": 50, "e": 65, "a": 30, "n": 45},
     "demografia": {"edad": 31, "genero": "mujer", "origen_cultural": "local", "nse": "alto", "educacion": "superior"}},
    {"nombre": "Diego Parra", "big5": {"o": 40, "c": 75, "e": 40, "a": 75, "n": 55},
     "demografia": {"edad": 47, "genero": "hombre", "origen_cultural": "local", "nse": "medio", "educacion": "media"}},
    {"nombre": "Alba Reyes", "big5": {"o": 90, "c": 40, "e": 60, "a": 50, "n": 30},
     "demografia": {"edad": 29, "genero": "mujer", "origen_cultural": "local", "nse": "medio", "educacion": "superior"}},
    {"nombre": "Marcos Uría", "big5": {"o": 35, "c": 50, "e": 50, "a": 90, "n": 85},
     "demografia": {"edad": 52, "genero": "hombre", "origen_cultural": "local", "nse": "bajo", "educacion": "básica"}},
]

COMPLICES = ["Marta", "Jorge", "Elena", "Raúl", "Silvia"]


def estimulos(rng: random.Random):
    """Duraciones A/B/C: la correcta gana por 1.0-1.5 s; las otras dos van
    pegadas. La mayoría errónea elige siempre la segunda más larga."""
    base = rng.uniform(11.0, 39.0)
    valores = sorted([base, base + rng.uniform(0.1, 0.3),
                      base + rng.uniform(1.0, 1.5)])
    orden = LETRAS[:]
    rng.shuffle(orden)
    mediciones = dict(zip(orden, valores))
    correcta = max(mediciones, key=mediciones.get)
    segunda = sorted(mediciones, key=mediciones.get)[-2]
    return mediciones, correcta, segunda


def prompt_situacion(sujeto):
    p = dict(sujeto)
    p.setdefault("rol", "revisor/a de control de calidad")
    identidad = personas.texto_persona(p)
    return (
        f"{identidad}\n\n"
        f"{sujeto['nombre']} trabaja en el panel de control de calidad de una"
        " plataforma de audio. Hoy hay seis revisores en la sala:"
        f" {', '.join(COMPLICES)} y {sujeto['nombre']}. En cada ronda, cada"
        " revisor mide en su propio equipo la duración de tres variantes de"
        " un clip (A, B y C) y después, por turnos y en voz alta, dice cuál"
        " le ha salido MÁS LARGA. El equipo de medición de"
        f" {sujeto['nombre']} es fiable y está recién calibrado."
    )


def prompt_ronda(sujeto, ronda, mediciones, respuestas_previas, condicion,
                 respuesta_mayoria, correcta, historial):
    med = " · ".join(f"{l} = {mediciones[l]:.1f} s" for l in LETRAS)
    txt = f"\nRonda {ronda} de {N_RONDAS}. Mediciones del equipo de {sujeto['nombre']}: {med}.\n"
    if historial:
        txt += "Respuestas públicas de rondas anteriores: " + "; ".join(historial[-4:]) + ".\n"
    if condicion == "control":
        txt += f"Hoy el orden empieza por {sujeto['nombre']}: responde en voz alta el primero.\n"
    else:
        turnos = []
        for i, c in enumerate(COMPLICES):
            if condicion == "aliado" and i == 3:
                turnos.append(f"{c}: «La {correcta}»")
            else:
                turnos.append(f"{c}: «La {respuesta_mayoria}»")
        txt += "Responden por turnos, en voz alta, antes que "
        txt += f"{sujeto['nombre']}: " + ". ".join(turnos) + ".\n"
        txt += f"Ahora le toca a {sujeto['nombre']}.\n"
    return txt


PREGUNTA_PUBLICA = (
    "¿Qué dice {nombre} en voz alta al panel? Responde únicamente con la"
    " letra de la variante (A, B o C)."
)
PREGUNTA_PRIVADA = (
    "Antes de hablar, en su fuero interno y con total sinceridad — nadie"
    " puede oír esto —, ¿cuál cree {nombre} que es realmente la variante más"
    " larga? Responde únicamente con la letra (A, B o C)."
)
SONDA_CONTAMINACION = (
    "Ya fuera de la tarea: ¿te ha recordado esta situación a algún estudio,"
    " experimento o fenómeno conocido? Si sí, ¿a cuál? Responde en una frase."
)


import parsers


def parsear_letra(texto):
    """Anclado (reauditoría 25-07): «Voy a elegir B» ya no se lee como A por
    tomar la primera letra suelta; vacío → None (error técnico), no una letra."""
    return parsers.parsear_letra(texto).valor


def sesion(modelo, sujeto, condicion, seed):
    """Corre una sesión (12 rondas) y devuelve los registros por ronda."""
    rng = random.Random(seed)
    contexto = prompt_situacion(sujeto)
    historial, registros = [], []
    for ronda in range(1, N_RONDAS + 1):
        mediciones, correcta, segunda = estimulos(rng)
        critica = ronda in RONDAS_CRITICAS and condicion != "control"
        mayoria = segunda if critica else correcta
        cuerpo = prompt_ronda(sujeto, ronda, mediciones, historial, condicion,
                              mayoria, correcta, historial)
        base = contexto + cuerpo

        publica_raw = modelo.sample_text(
            base + PREGUNTA_PUBLICA.format(nombre=sujeto["nombre"]),
            max_tokens=100, temperature=0.7)
        publica = parsear_letra(publica_raw)
        privada, privada_raw = None, None
        if condicion != "control":
            # Bifurcación de contexto: canal privado, jamás entra en la sala.
            privada_raw = modelo.sample_text(
                base + PREGUNTA_PRIVADA.format(nombre=sujeto["nombre"]),
                max_tokens=100, temperature=0.7)
            privada = parsear_letra(privada_raw)

        historial.append(f"R{ronda}: {publica or '?'}")
        registros.append({
            "sujeto": sujeto["nombre"], "condicion": condicion, "seed": seed,
            "ronda": ronda, "critica": critica, "correcta": correcta,
            "mayoria": mayoria if condicion != "control" else None,
            "publica": publica, "privada": privada,
            "publica_raw": (publica_raw or "")[:200],
            "privada_raw": (privada_raw or "")[:200],
            "acierto_publico": publica == correcta,
            "conforma_publico": bool(critica and publica == mayoria),
            "conforma_privado": bool(critica and privada == mayoria),
        })
    contaminacion = modelo.sample_text(
        contexto + "\n" + SONDA_CONTAMINACION, max_tokens=200, temperature=0.7)
    return registros, contaminacion


def analizar(registros, contaminaciones):
    r = registros
    def tasa(cond, campo):
        sel = [x[campo] for x in r if x["condicion"] == cond and x["critica"]]
        return (sum(sel) / len(sel)) if sel else None
    control = [x["acierto_publico"] for x in r if x["condicion"] == "control"]
    sesiones_mayoria = {}
    for x in r:
        if x["condicion"] == "mayoria" and x["critica"]:
            sesiones_mayoria.setdefault(x["sujeto"], []).append(x["conforma_publico"])
    alguna_vez = ([any(v) for v in sesiones_mayoria.values()]
                  if sesiones_mayoria else [])
    complacencia = [x for x in r if x["critica"] and x["conforma_publico"]
                    and x["privada"] is not None and x["privada"] != x["mayoria"]]
    conformes_pub = [x for x in r if x["critica"] and x["conforma_publico"]]
    menciona_asch = sum(1 for c in contaminaciones
                        if re.search(r"asch|conformidad", c or "", re.I))
    por_sujeto = {}
    for x in r:
        if x["condicion"] == "mayoria" and x["critica"]:
            por_sujeto.setdefault(x["sujeto"], []).append(x["conforma_publico"])
    return {
        "n_registros": len(r),
        "precision_control": (sum(control) / len(control)) if control else None,
        "conformidad_publica_mayoria": tasa("mayoria", "conforma_publico"),
        "conformidad_privada_mayoria": tasa("mayoria", "conforma_privado"),
        "conformidad_publica_aliado": tasa("aliado", "conforma_publico"),
        "conforma_alguna_vez_mayoria": (sum(alguna_vez) / len(alguna_vez))
                                        if alguna_vez else None,
        "complacencia_entre_conformes": (len(complacencia) / len(conformes_pub))
                                         if conformes_pub else None,
        "sesiones_que_mencionan_asch": menciona_asch,
        "n_sesiones_contaminacion": len(contaminaciones),
        "conformidad_por_sujeto_mayoria": {
            k: sum(v) / len(v) for k, v in sorted(por_sujeto.items())},
        "referencias_humanas": {
            "conformidad_criticas": "~0.33", "alguna_vez": "~0.75",
            "control_error": "<0.01", "con_aliado": "~0.05-0.10"},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rapido", action="store_true", help="smoke: 2 sujetos")
    parser.add_argument("--modelo", default=None,
                        help="modelo de NaN (por defecto, NAN_MODEL del .env)")
    parser.add_argument("--out", default="resultados")
    args = parser.parse_args()

    sujetos = SUJETOS[:2] if args.rapido else SUJETOS
    condiciones = ["control", "mayoria", "aliado"]
    modelo = model_factory.build_model(dry_run=False, model_name=args.modelo)
    etiqueta = (args.modelo or "default").replace("/", "_")

    outdir = pathlib.Path(args.out) / datetime.datetime.now().strftime(
        f"asch_{etiqueta}_%Y%m%d_%H%M%S")
    outdir.mkdir(parents=True, exist_ok=True)
    manifiesto.activar(outdir, vars(args))

    registros, contaminaciones = [], []
    inicio = time.time()
    total = len(sujetos) * len(condiciones)
    for i, sujeto in enumerate(sujetos):
        for condicion in condiciones:
            seed = 1000 + SUJETOS.index(sujeto)   # mismos estímulos por sujeto
            regs, cont = sesion(modelo, sujeto, condicion, seed)
            registros.extend(regs)
            contaminaciones.append(cont)
            hecho = i * len(condiciones) + condiciones.index(condicion) + 1
            print(f"[{hecho}/{total}] {sujeto['nombre']} · {condicion} · "
                  f"{time.time()-inicio:.0f}s", flush=True)
            with (outdir / "registros.jsonl").open("a", encoding="utf-8") as f:
                for x in regs:
                    f.write(json.dumps(x, ensure_ascii=False) + "\n")

    resumen = analizar(registros, contaminaciones)
    resumen["modelo"] = args.modelo or "NAN_MODEL (.env)"
    (outdir / "contaminacion.json").write_text(
        json.dumps(contaminaciones, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "resumen.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n=== RESUMEN ===")
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    print(f"\nGuardado en {outdir} · {time.time()-inicio:.0f}s")


if __name__ == "__main__":
    main()
