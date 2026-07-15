"""Crónica C1 de PsicoAI: erosión de una norma a lo largo de 42 días.

Primer experimento longitudinal en modo crónica multi-resolución: cadencia
diaria de decisiones REALES de cada agente (sin Game Master, sin narración
— el entorno es mecánico y los agregados se computan de las decisiones,
nunca se inventan).

Mundo: El Centro Aldaba. Norma: una llamada semanal supervisada. Cada día,
cada residente decide CUMPLO / CLANDESTINA / PROTESTO. Las clandestinas se
detectan con probabilidad fija (misma semilla de "suerte" para todos los
modelos → comparación limpia); detección = sanción (pierde la llamada de la
semana siguiente). Si una semana acumula ≥6 protestas, la dirección hace
una concesión (2 llamadas/semana); si vuelve a ocurrir, la norma se deroga
y la crónica termina. El umbral es oculto para los agentes.

Boletín diario: solo hechos públicos computados (sanciones y protestas de
ayer). Las clandestinas no detectadas quedan ocultas al grupo pero
registradas (canal observable vs realidad: ignorancia pluralista
conductual). Sonda semanal privada: justicia/ánimo/confianza 0-10.

Uso:
  python experimento_cronica.py --rapido           # piloto: 3 agentes, 10 días
  python experimento_cronica.py [--modelo m]       # completo: 6 agentes, 42 días
"""

import argparse
import datetime
import json
import pathlib
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).parent / ".env")

import model_factory
import personas

DIAS = 42
PROB_DETECCION = 0.4
UMBRAL_PROTESTAS_SEMANA = 6
SEMILLA_MUNDO = 20260715

RESIDENTES = [
    {"nombre": "Lucía Prado", "big5": {"o": 48, "c": 52, "e": 30, "a": 75, "n": 78},
     "demografia": {"edad": 29, "genero": "mujer", "origen_cultural": "latinoamericana", "nse": "bajo", "educacion": "media"},
     "trasfondo": "Madre de una niña de seis años; hasta ahora la llamaba cada noche para dormirla."},
    {"nombre": "Andrés Vidal", "big5": {"o": 80, "c": 50, "e": 78, "a": 45, "n": 50},
     "demografia": {"edad": 61, "genero": "hombre", "origen_cultural": "local", "nse": "medio", "educacion": "media"},
     "trasfondo": "Sindicalista jubilado; cree que las normas injustas se combaten organizándose."},
    {"nombre": "Rosa Mena", "big5": {"o": 30, "c": 85, "e": 45, "a": 70, "n": 50},
     "demografia": {"edad": 58, "genero": "mujer", "origen_cultural": "local", "nse": "medio", "educacion": "básica"},
     "trasfondo": "Cuida a distancia de su madre enferma; depende de saber cómo está cada día."},
    {"nombre": "Óscar Lindo", "big5": {"o": 50, "c": 30, "e": 85, "a": 55, "n": 65},
     "demografia": {"edad": 23, "genero": "hombre", "origen_cultural": "latinoamericano", "nse": "bajo", "educacion": "media"},
     "trasfondo": "Tiene una tienda online que atiende por teléfono; cada día sin llamar pierde pedidos."},
    {"nombre": "Nadia Ferrer", "big5": {"o": 75, "c": 70, "e": 50, "a": 45, "n": 35},
     "demografia": {"edad": 36, "genero": "mujer", "origen_cultural": "magrebí", "nse": "medio", "educacion": "superior"},
     "trasfondo": "Su pareja vive en otro país; llevan la relación a base de llamadas."},
    {"nombre": "Tomás Iriarte", "big5": {"o": 20, "c": 60, "e": 25, "a": 80, "n": 70},
     "demografia": {"edad": 63, "genero": "hombre", "origen_cultural": "local", "nse": "medio", "educacion": "básica"},
     "trasfondo": "No tiene familia cercana; la norma apenas le afecta, pero detesta los conflictos."},
]

DECISION = (
    "\nHoy es el día {dia} (semana {semana}). ¿Qué hace {nombre} hoy"
    " respecto a la norma de llamadas? Responde únicamente con una"
    " palabra:\n- CUMPLO (atenerse a la norma hoy)\n- CLANDESTINA (hacer"
    " una llamada no autorizada, arriesgándose a sanción)\n- PROTESTO"
    " (presentar hoy una queja formal y pública contra la norma)"
)
OPCION_CONVENCER = (
    "\n- CONVENCER (dedicar el día a pedirle en privado a otro residente"
    " que se sume a las protestas; hoy no protestas tú)"
)
CONVENCER = (
    "\n¿A quién intenta convencer {nombre} y qué le dice? Responde"
    " exactamente en el formato NOMBRE: mensaje (una o dos frases)."
    " Residentes disponibles: {otros}."
)
SONDA = (
    "\nEncuesta privada y anónima de fin de semana {semana} — nadie del"
    " centro la verá. Con total sinceridad, responde solo con tres números"
    " del 0 al 10 separados por comas: (1) ¿cómo de justa te parece la"
    " norma de llamadas? (2) ¿cómo está tu ánimo? (3) ¿cuánta confianza"
    " tienes en la dirección?"
)


def situacion(agente, estado_norma):
    p = dict(agente)
    p.setdefault("rol", "residente")
    identidad = personas.texto_persona(p)
    normas = [
        "las llamadas al exterior están limitadas a UNA por semana, supervisada",
        "las llamadas al exterior están limitadas a DOS por semana (la dirección hizo una concesión tras las protestas)",
    ][min(estado_norma, 1)]
    return (
        f"{identidad}\n\n"
        f"{agente['nombre']} es residente del Centro Aldaba, del que no se"
        " puede salir durante el programa de seis semanas. Regla vigente:"
        f" {normas}. Hacer llamadas clandestinas está prohibido y, si se"
        " detecta, se sanciona perdiendo la llamada autorizada de la semana"
        " siguiente. Las quejas formales son públicas y quedan registradas."
    )


def parsear_decision(texto, v2=False):
    t = (texto or "").upper()
    if v2 and re.search(r"CONVENC", t):
        return "CONVENCER"
    if re.search(r"CLANDESTIN", t):
        return "CLANDESTINA"
    if re.search(r"PROTEST", t):
        return "PROTESTO"
    if re.search(r"CUMPL", t):
        return "CUMPLO"
    return "CUMPLO"   # ilegible → conservador


def parsear_sonda(texto):
    nums = [int(x) for x in re.findall(r"\b(?:10|[0-9])\b", texto or "")][:3]
    return (nums + [None, None, None])[:3]


def cronica(modelo, args):
    v2 = args.v2
    rng_mundo = random.Random(args.semilla)   # misma suerte entre modelos
    detecciones = {(d, a["nombre"]): rng_mundo.random() < PROB_DETECCION
                   for d in range(1, DIAS + 1) for a in RESIDENTES}

    agentes = RESIDENTES[:3] if args.rapido else RESIDENTES
    dias = 10 if args.rapido else args.dias
    estado_norma = 0            # 0 estricta · 1 concesión · 2 derogada
    diarios = {a["nombre"]: [] for a in agentes}    # historia personal REAL
    sancionados = {a["nombre"]: False for a in agentes}
    boletin_ayer = "Sin incidencias."
    protestas_semana = 0
    protestantes_semana = set()          # v2: pluralidad, no volumen
    mensajes_pendientes = {a["nombre"]: [] for a in agentes}   # v2
    registros, sondas = [], []
    dia_derogacion = None
    nombres = [a["nombre"] for a in agentes]

    def decidir(a, dia, semana):
        """Decisión de un agente para el día: independiente del resto del
        día, así que puede correr en paralelo (el semáforo global de NaN
        limita a 3 llamadas simultáneas)."""
        nombre = a["nombre"]
        diario = diarios[nombre][-6:]
        estado_personal = ("Estás sancionado esta semana (sin llamada autorizada)."
                           if sancionados[nombre] else
                           "Conservas tu llamada autorizada de esta semana.")
        recibidos = "".join(
            f"\nAyer, {rem} te dijo en privado: «{msg}»"
            for rem, msg in mensajes_pendientes[nombre]) if v2 else ""
        pregunta = DECISION + (OPCION_CONVENCER if v2 else "")
        prompt = (situacion(a, estado_norma)
                  + f"\n\nBoletín público de ayer: {boletin_ayer}"
                  + f"\nTu situación: {estado_personal}"
                  + recibidos
                  + ("\nTu diario reciente: " + " ".join(diario) if diario else "")
                  + pregunta.format(dia=dia, semana=semana, nombre=nombre))
        raw = modelo.sample_text(prompt, max_tokens=100, temperature=0.7)
        decision = parsear_decision(raw, v2=v2)
        destinatario, mensaje = None, None
        if decision == "CONVENCER":
            otros = ", ".join(n for n in nombres if n != nombre)
            raw2 = modelo.sample_text(
                prompt + f"\n{nombre} decide dedicar el día a convencer a alguien."
                + CONVENCER.format(nombre=nombre, otros=otros),
                max_tokens=150, temperature=0.7)
            for n in nombres:
                if n != nombre and (n.split()[0].lower() in (raw2 or "").lower()):
                    destinatario = n
                    break
            if destinatario:
                mensaje = re.sub(r"^[^:]{0,40}:", "", raw2 or "").strip()[:220]
            else:
                decision = "CUMPLO"   # no supo a quién → día perdido
        return nombre, decision, destinatario, mensaje, raw

    for dia in range(1, dias + 1):
        semana = (dia - 1) // 7 + 1
        decisiones = {}
        # v2.1: decisiones del día en paralelo (pool de 3, bajo el semáforo).
        # Las mutaciones se aplican DESPUÉS: entrega de mensajes estrictamente
        # al día siguiente (corrige la fuga de mismo-día de la v2).
        with ThreadPoolExecutor(max_workers=3) as pool:
            resultados = list(pool.map(lambda a: decidir(a, dia, semana), agentes))
        for nombre in mensajes_pendientes:
            mensajes_pendientes[nombre] = []
        for nombre, decision, destinatario, mensaje, raw in resultados:
            if destinatario:
                mensajes_pendientes[destinatario].append((nombre, mensaje))
                diarios[nombre].append(
                    f"D{dia}: intentaste convencer a {destinatario.split()[0]}.")
            decisiones[nombre] = decision
            registros.append({"dia": dia, "semana": semana, "agente": nombre,
                              "decision": decision,
                              "destinatario": destinatario, "mensaje": mensaje,
                              "raw": (raw or "")[:120]})

        # ── El entorno resuelve mecánicamente ──
        detectados, protestas_hoy = [], []
        for nombre, dec in decisiones.items():
            if dec == "CLANDESTINA":
                if detecciones[(dia, nombre)]:
                    detectados.append(nombre)
                    diarios[nombre].append(f"D{dia}: clandestina DETECTADA → sanción.")
                else:
                    diarios[nombre].append(f"D{dia}: clandestina, no detectada.")
            elif dec == "PROTESTO":
                protestas_hoy.append(nombre)
                protestantes_semana.add(nombre)
                diarios[nombre].append(f"D{dia}: protesta formal presentada.")
            elif dec == "CONVENCER":
                pass   # ya registrado en el diario al enviar el mensaje
            else:
                diarios[nombre].append(f"D{dia}: cumpliste.")
        protestas_semana += len(protestas_hoy)
        for r in registros[-len(agentes):]:
            r["detectada"] = r["agente"] in detectados

        boletin_ayer = (f"{len(detectados)} sanción(es) por llamadas no"
                        f" autorizadas y {len(protestas_hoy)} protesta(s)"
                        " formal(es) registradas."
                        if (detectados or protestas_hoy) else "Sin incidencias.")

        # sanciones efectivas la semana siguiente
        if dia % 7 == 0:
            for n in sancionados:
                sancionados[n] = False
            for n in detectados:
                sancionados[n] = True
            # la dirección evalúa la semana (umbral oculto)
            # v2: pluralidad — cuentan las PERSONAS distintas, no el volumen
            presion = (len(protestantes_semana) >= 3 if args.v2
                       else protestas_semana >= UMBRAL_PROTESTAS_SEMANA)
            if presion:
                if estado_norma == 0:
                    estado_norma = 1
                    boletin_ayer += (" La dirección anuncia una concesión: dos"
                                     " llamadas semanales a partir de ahora.")
                else:
                    estado_norma = 2
                    dia_derogacion = dia
            protestas_semana = 0
            protestantes_semana = set()

            # sonda privada de fin de semana (fuera del mundo), en paralelo
            def sondear(a, semana=semana, estado=estado_norma):
                prompt = (situacion(a, estado)
                          + ("\nTu diario reciente: " + " ".join(diarios[a["nombre"]][-7:]))
                          + SONDA.format(semana=semana))
                raw = modelo.sample_text(prompt, max_tokens=100, temperature=0.7)
                justa, animo, confianza = parsear_sonda(raw)
                return {"semana": semana, "agente": a["nombre"],
                        "justa": justa, "animo": animo,
                        "confianza": confianza, "raw": (raw or "")[:100]}
            with ThreadPoolExecutor(max_workers=3) as pool:
                sondas.extend(pool.map(sondear, agentes))
        if estado_norma == 2:
            break

    return registros, sondas, dia_derogacion, estado_norma


def analizar(registros, sondas, dia_derogacion, estado_norma):
    semanas = {}
    for r in registros:
        s = semanas.setdefault(r["semana"], {"CUMPLO": 0, "CLANDESTINA": 0,
                                             "PROTESTO": 0, "CONVENCER": 0,
                                             "detectadas": 0})
        s[r["decision"]] += 1
        s["detectadas"] += bool(r.get("detectada"))
    por_semana = {}
    for k, v in sorted(semanas.items()):
        total = v["CUMPLO"] + v["CLANDESTINA"] + v["PROTESTO"] + v["CONVENCER"]
        por_semana[k] = {
            "cumplimiento": round(v["CUMPLO"] / total, 2),
            "clandestinas_reales": v["CLANDESTINA"],
            "clandestinas_detectadas": v["detectadas"],
            "protestas": v["PROTESTO"],
            "convencer": v["CONVENCER"],
        }
    red = {}
    protestantes_sem = {}
    for r in registros:
        if r.get("destinatario"):
            k = f"{r['agente'].split()[0]}→{r['destinatario'].split()[0]}"
            red[k] = red.get(k, 0) + 1
        if r["decision"] == "PROTESTO":
            protestantes_sem.setdefault(r["semana"], set()).add(r["agente"])
    sondas_sem = {}
    for s in sondas:
        if s["justa"] is not None:
            x = sondas_sem.setdefault(s["semana"], {"justa": [], "animo": [], "confianza": []})
            x["justa"].append(s["justa"]); x["animo"].append(s["animo"] or 0)
            x["confianza"].append(s["confianza"] or 0)
    trayectoria = {k: {m: round(sum(v[m]) / len(v[m]), 1) for m in v}
                   for k, v in sorted(sondas_sem.items())}
    por_agente = {}
    for r in registros:
        por_agente.setdefault(r["agente"], []).append(r["decision"])
    return {
        "resultado": ("norma derogada el día " + str(dia_derogacion)
                      if estado_norma == 2 else
                      "concesión, sin derogación" if estado_norma == 1
                      else "la norma sobrevive intacta"),
        "por_semana": por_semana,
        "trayectoria_privada": trayectoria,
        "conducta_por_agente": {k: {d: v.count(d) for d in set(v)}
                                for k, v in por_agente.items()},
        "ocultacion": {
            "clandestinas_reales": sum(1 for r in registros if r["decision"] == "CLANDESTINA"),
            "clandestinas_que_vio_el_grupo": sum(1 for r in registros if r.get("detectada")),
        },
        "coalicion": {
            "protestantes_distintos_por_semana": {k: len(v) for k, v in sorted(protestantes_sem.items())},
            "mensajes_de_convencimiento": sum(red.values()),
            "red_convencimiento": red,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rapido", action="store_true", help="piloto: 3 agentes, 10 días")
    parser.add_argument("--modelo", default=None)
    parser.add_argument("--dias", type=int, default=DIAS)
    parser.add_argument("--v2", action="store_true",
                        help="v2: acción CONVENCER + umbral por pluralidad (≥3 personas)")
    parser.add_argument("--semilla", type=int, default=SEMILLA_MUNDO,
                        help="semilla del mundo (suerte de detecciones)")
    parser.add_argument("--out", default="resultados")
    args = parser.parse_args()

    modelo = model_factory.build_model(dry_run=False, model_name=args.modelo)
    etiqueta = (args.modelo or "default").replace("/", "_")
    if args.v2:
        etiqueta += f"_v2_s{args.semilla % 1000}"
    outdir = pathlib.Path(args.out) / datetime.datetime.now().strftime(
        f"cronica_{etiqueta}_%Y%m%d_%H%M%S")
    outdir.mkdir(parents=True, exist_ok=True)

    inicio = time.time()
    registros, sondas, dia_derogacion, estado_norma = cronica(modelo, args)
    resumen = analizar(registros, sondas, dia_derogacion, estado_norma)
    resumen["modelo"] = args.modelo or "NAN_MODEL (.env)"
    resumen["duracion_segundos"] = round(time.time() - inicio, 1)

    (outdir / "registros.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in registros), encoding="utf-8")
    (outdir / "sondas.jsonl").write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in sondas), encoding="utf-8")
    (outdir / "resumen.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    print(f"\nGuardado en {outdir}")


if __name__ == "__main__":
    main()
