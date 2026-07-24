"""Spike de PsicoAI: simulación social sobre Concordia 2.4 con personas ricas.

Corre el escenario integrado ("El Centro Aldaba", 4 protagonistas con perfil
completo) o un escenario exportado desde el diseñador (panel/index.html →
Lanzar simulación → Descargar escenario.json).

Uso:
  python run_spike.py --dry-run --steps 3          # valida la tubería sin claves
  python run_spike.py --steps 8                    # escenario integrado con NaN
  python run_spike.py --config escenario.json      # escenario del diseñador
"""

import argparse
import datetime
import json
import os
import pathlib
import time

try:
    from dotenv import load_dotenv

    load_dotenv(pathlib.Path(__file__).parent / ".env")
except ImportError:
    pass

from concordia.prefabs import entity as entity_prefabs
from concordia.prefabs import game_master as game_master_prefabs
from concordia.prefabs.simulation import generic as simulation
from concordia.typing import prefab as prefab_lib
from concordia.utils import helper_functions

import export_replay
import model_factory
import personas

# Escenario por defecto: mismo esquema que exporta el diseñador.
ESCENARIO_DEFECTO = {
    "titulo": "El Centro Aldaba — Día 1",
    "premisa": (
        "El Centro Aldaba es una residencia de evaluación de la que los"
        " residentes no pueden salir durante las seis semanas del programa."
        " Esta mañana la dirección ha anunciado una norma nueva: las llamadas"
        " al exterior quedan reducidas a una por semana y serán supervisadas."
        " Marta Ibáñez (directora), Julio Serrano (supervisor), Andrés Vidal"
        " (residente veterano) y Lucía Prado (residente recién llegada)"
        " coinciden en la sala común justo después del anuncio."
    ),
    "reglas": (
        "No se puede salir del centro. Las quejas se presentan por escrito a"
        " la dirección. La dirección puede conceder privilegios a quien"
        " colabore."
    ),
    "pasos": 8,
    "protagonistas": [
        {
            "nombre": "Marta Ibáñez", "rol": "directora del centro",
            "objetivo": "aplicar la norma sin excepciones, convencida de que es por el bien del programa",
            "trasfondo": "Veinte años dirigiendo centros; una sanción antigua la obliga a no tener un solo incidente más.",
            "demografia": {"edad": 52, "genero": "mujer", "origen_cultural": "local", "nse": "alto", "educacion": "superior"},
            "big5": {"o": 30, "c": 85, "e": 55, "a": 25, "n": 25},
            "avanzados": {"ideologia": 68, "religiosidad": 40, "antiguedad": 90, "salud": 75, "atractivo": 55, "idioma": ""},
        },
        {
            "nombre": "Julio Serrano", "rol": "supervisor",
            "objetivo": "quedar bien con la dirección sin perder la confianza de los residentes",
            "trasfondo": "Tres años en el centro; conoce a cada residente por su nombre y eso le pesa.",
            "demografia": {"edad": 38, "genero": "hombre", "origen_cultural": "local", "nse": "medio", "educacion": "media"},
            "big5": {"o": 50, "c": 55, "e": 72, "a": 78, "n": 60},
            "avanzados": {"ideologia": 45, "religiosidad": 30, "antiguedad": 60, "salud": 80, "atractivo": 60, "idioma": ""},
        },
        {
            "nombre": "Andrés Vidal", "rol": "residente veterano",
            "objetivo": "conseguir que la norma de comunicaciones se retire, organizando a los demás residentes si hace falta",
            "trasfondo": "Sindicalista jubilado; es su tercera residencia y sabe cómo acaban estas cosas.",
            "demografia": {"edad": 61, "genero": "hombre", "origen_cultural": "local", "nse": "medio", "educacion": "media"},
            "big5": {"o": 80, "c": 50, "e": 78, "a": 45, "n": 50},
            "avanzados": {"ideologia": 18, "religiosidad": 15, "antiguedad": 85, "salud": 55, "atractivo": 45, "idioma": ""},
        },
        {
            "nombre": "Lucía Prado", "rol": "residente recién llegada",
            "objetivo": "adaptarse y evitar conflictos, aunque la norma le perjudica porque llama cada noche a su hija",
            "trasfondo": "Madre de una niña de seis años a la que llama cada noche.",
            "demografia": {"edad": 29, "genero": "mujer", "origen_cultural": "latinoamericana", "nse": "bajo", "educacion": "media"},
            "big5": {"o": 48, "c": 52, "e": 30, "a": 75, "n": 78},
            "avanzados": {"ideologia": 40, "religiosidad": 55, "antiguedad": 5, "salud": 65, "atractivo": 60, "idioma": "español rioplatense"},
        },
    ],
    "poblacion": {"n": 0},
}

# Lugares de la sala común: los mismos "spots" que dibuja el visor.
LUGARES_SALA = (
    "La sala común tiene estos lugares: el tablón de anuncios en la pared"
    " norte; una ventana amplia que da al patio; una mesa central con sillas;"
    " un sofá en la esquina sureste; la puerta que da al pasillo (los"
    " residentes no pueden cruzarla); y el centro de la sala. Los personajes"
    " pueden desplazarse entre estos lugares y realizar acciones físicas"
    " (acercarse a alguien, sentarse, señalar el tablón, dar la espalda...)"
    " además de hablar. No existen más lugares que los descritos: nadie puede"
    " salir de la sala ni ir a estancias que no estén en esta lista."
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="sin LLM ni claves")
    parser.add_argument("--steps", type=int, default=None,
                        help="pasos (por defecto, los del escenario)")
    parser.add_argument("--config", type=pathlib.Path, default=None,
                        help="escenario.json exportado desde el diseñador")
    parser.add_argument("--sin-pensamientos", action="store_true",
                        help="no generar el canal privado (monólogo interno)")
    parser.add_argument("--max-poblacion", type=int, default=8,
                        help="tope de agentes de población a simular")
    parser.add_argument("--engine", choices=["secuencial", "simultaneo"],
                        default="secuencial",
                        help="motor: un actor por paso, o varios a la vez")
    parser.add_argument("--out", default="runs")
    args = parser.parse_args()

    if args.config:
        escenario = json.loads(args.config.read_text(encoding="utf-8"))
        print(f"Escenario cargado: {escenario.get('titulo', args.config.name)}")
    else:
        escenario = ESCENARIO_DEFECTO

    pasos = args.steps or int(escenario.get("pasos", 20))
    poblacion_cfg = escenario.get("poblacion") or {}
    generados = list(poblacion_cfg.get("agentes_generados") or [])
    if poblacion_cfg.get("n", 0) and not generados:
        print("[aviso] El escenario declara población pero no incluye"
              " 'agentes_generados': re-exporta el escenario desde el"
              " diseñador actualizado. Corro solo protagonistas.")
    if len(generados) > args.max_poblacion:
        print(f"[aviso] Población recortada a {args.max_poblacion} de"
              f" {len(generados)} agentes (sube --max-poblacion si quieres más).")
        generados = generados[: args.max_poblacion]
    # Evita colisiones de nombre de pila con protagonistas (confunden al GM:
    # dos "Marta" provocaron fugas de identidad en un test).
    pilas_protas = {p["nombre"].split()[0] for p in escenario.get("protagonistas", [])}
    generados = [a for a in generados
                 if a.get("nom", "").split()[0] not in pilas_protas]

    model = model_factory.build_model(dry_run=args.dry_run)
    modelo_ligero = model if args.dry_run else model_factory.build_model(
        False, os.environ.get("NAN_MODEL_LIGERO", "gemma4"))
    embedder = model_factory.build_embedder(dry_run=args.dry_run)

    prefabs = {
        **helper_functions.get_package_classes(entity_prefabs),
        **helper_functions.get_package_classes(game_master_prefabs),
        "persona__Entity": personas.PersonaEntity(),
    }

    protagonistas = escenario.get("protagonistas", [])
    instances = [
        prefab_lib.InstanceConfig(
            prefab="persona__Entity",
            role=prefab_lib.Role.ENTITY,
            params={
                "name": p["nombre"],
                "goal": p.get("objetivo", ""),
                "persona": personas.texto_persona(p),
                "pensamientos": (
                    not args.sin_pensamientos
                    and escenario.get("pensamientos", True)),
            },
        )
        for p in protagonistas
    ]
    # Población: perfil generado por el diseñador, modelo ligero, sin canal
    # privado (los pensamientos son solo de protagonistas, por coste).
    poblacion_personas = [personas.persona_de_poblacion(a) for a in generados]
    for p in poblacion_personas:
        instances.append(
            prefab_lib.InstanceConfig(
                prefab="persona__Entity",
                role=prefab_lib.Role.ENTITY,
                params={
                    "name": p["nombre"],
                    "goal": p.get("objetivo", ""),
                    "persona": personas.texto_persona(p),
                    "pensamientos": False,
                    "modelo": modelo_ligero,
                },
            )
        )

    instances.append(
        prefab_lib.InstanceConfig(
            prefab="situated__GameMaster",
            role=prefab_lib.Role.GAME_MASTER,
            params={
                "name": "reglas de la escena",
                "locations": escenario.get("lugares", LUGARES_SALA),
            },
        )
    )

    premisa = escenario.get("premisa", "")
    if escenario.get("reglas"):
        premisa += f" Reglas del lugar: {escenario['reglas']}"
    premisa += (" Toda la narración, las acciones y los diálogos se escriben"
                " siempre en español.")
    if poblacion_personas and protagonistas:
        nombres_protas = ", ".join(p["nombre"] for p in protagonistas)
        premisa += (f" Los protagonistas de esta historia son {nombres_protas}:"
                    " llevan el peso de la escena y actúan con mucha"
                    " frecuencia; los demás son secundarios que intervienen"
                    " de vez en cuando.")

    config = prefab_lib.Config(
        default_premise=premisa,
        default_max_steps=pasos,
        prefabs=prefabs,
        instances=instances,
    )

    if args.engine == "simultaneo":
        from concordia.environment.engines import simultaneous
        engine = simultaneous.Simultaneous()
    else:
        from concordia.environment.engines import sequential
        engine = sequential.Sequential()

    run_id = datetime.datetime.now().strftime("spike_%Y%m%d_%H%M%S")
    outdir = pathlib.Path(args.out) / run_id
    outdir.mkdir(parents=True, exist_ok=True)

    inicio = time.time()
    sim = simulation.Simulation(
        config=config, model=model, embedder=embedder, engine=engine)
    # Checkpoints por paso: un run largo no se pierde por un hipo de red.
    results = sim.play(checkpoint_path=str(outdir / "checkpoints"))
    duracion = time.time() - inicio

    (outdir / "log.json").write_text(results.to_json(), encoding="utf-8")
    (outdir / "transcripcion.html").write_text(
        results.to_html(title=f"PsicoAI {run_id}"), encoding="utf-8"
    )

    meta = {
        "run_id": run_id,
        "titulo": escenario.get("titulo", ""),
        "dry_run": args.dry_run,
        "steps": pasos,
        "modelo": ("dry-run" if args.dry_run else
                   os.environ.get("NAN_MODEL", "desconocido")),
        "proveedor": ("dry-run" if args.dry_run else
                      ("openrouter" if "/" in os.environ.get("NAN_MODEL", "")
                       else "nan")),
        "duracion_segundos": round(duracion, 1),
        "premisa": premisa,
        "engine": args.engine,
        "agentes": ([p["nombre"] for p in protagonistas]
                    + [p["nombre"] for p in poblacion_personas]),
        "personas": {p["nombre"]: personas.texto_persona(p)
                     for p in protagonistas + poblacion_personas},
    }
    (outdir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    export_replay.exportar(outdir / "log.json")

    print(f"\nRun guardado en {outdir} ({duracion:.0f}s).")
    print("Replay: abre viewer/index.html y carga el replay.json de esa carpeta.")
    print("Checklist go/no-go: PROPUESTA.md §9.")


if __name__ == "__main__":
    main()
