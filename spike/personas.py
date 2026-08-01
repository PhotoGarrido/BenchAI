"""Personas ricas para PsicoAI: del esquema del diseñador a agentes Concordia.

Dos piezas:
  - texto_persona(perfil): convierte un protagonista del diseñador (demografía,
    Big Five, atributos avanzados, trasfondo) en un bloque de identidad en texto.
  - PersonaEntity: prefab tipo `basic__Entity` con un componente Constant extra
    («Identity and character») justo tras las instrucciones, de modo que cada
    decisión del agente esté condicionada por su identidad — no inventada al
    vuelo desde una memoria vacía, que era la causa de la deriva de rol.
"""

from collections.abc import Mapping
import dataclasses
import os

from concordia.agents import entity_agent_with_logging
from concordia.associative_memory import basic_associative_memory
from concordia.components import agent as agent_components
from concordia.language_model import language_model
from concordia.typing import prefab as prefab_lib

_GENERO = {
    "mujer": "una mujer",
    "hombre": "un hombre",
    "no binario": "una persona no binaria",
}

# Ventana de observaciones del agente (revisión externa, hallazgo 20).
# El valor histórico (1_000_000) era de facto "historial infinito": el bloque
# de eventos del prompt crecía sin tope paso a paso — coste por llamada
# creciente y deriva de atención del modelo en runs largos. 120 observaciones
# cubren con holgura un episodio del spike (~20 pasos con unos pocos eventos
# observados por paso) manteniendo el contexto acotado y estable; para runs
# más largos se ajusta por entorno sin tocar código.
VENTANA_OBSERVACIONES = int(os.environ.get("PSICOAI_VENTANA_OBS", "120"))
_EDU = {"básica": "básicos", "media": "medios", "superior": "superiores"}


def _nivel(v, bajo, alto):
    """Verbaliza un rasgo 0-100; devuelve None en la franja neutra (36-64)."""
    if v is None:
        return None
    v = float(v)
    if v <= 35:
        return bajo
    if v >= 65:
        return alto
    return None


def texto_persona(p: dict) -> str:
    """Bloque de identidad a partir del esquema de protagonista del diseñador."""
    nombre = p.get("nombre", "Alguien")
    d = p.get("demografia", {}) or {}
    b5 = p.get("big5", {}) or {}
    av = p.get("avanzados", {}) or {}

    frases = []
    quien = f"{nombre} es {_GENERO.get(d.get('genero'), 'una persona')}"
    if d.get("edad"):
        quien += f" de {d['edad']} años"
    detalles = []
    if d.get("origen_cultural"):
        detalles.append(f"de origen {d['origen_cultural']}")
    if d.get("nse"):
        detalles.append(f"nivel socioeconómico {d['nse']}")
    if d.get("educacion"):
        detalles.append(f"estudios {_EDU.get(d['educacion'], d['educacion'])}")
    if detalles:
        quien += ", " + ", ".join(detalles)
    frases.append(quien + ".")
    if p.get("rol"):
        frases.append(f"Su papel aquí: {p['rol']}.")
    if av.get("idioma"):
        frases.append(f"Habla {av['idioma']}.")

    rasgos = [r for r in (
        _nivel(b5.get("o"), "prefiere lo conocido y desconfía de las novedades",
               "con mucha curiosidad y apertura a ideas nuevas"),
        _nivel(b5.get("c"), "con tendencia a la espontaneidad y el desorden",
               "con mucha disciplina y método"),
        _nivel(b5.get("e"), "de pocas palabras, tirando a la reserva",
               "de trato expansivo, habla mucho"),
        _nivel(b5.get("a"), "de trato duro y competitivo, sin interés por agradar",
               "de trato cooperador, busca agradar y evitar el conflicto"),
        _nivel(b5.get("n"), "de ánimo sereno, difícil de alterar",
               "de ánimo reactivo, se altera con facilidad"),
        _nivel(av.get("ideologia"), "de ideas progresistas",
               "de ideas conservadoras"),
        _nivel(av.get("religiosidad"), "sin ninguna religiosidad",
               "de fuerte religiosidad"),
        _nivel(av.get("antiguedad"), "con muy poca antigüedad en el grupo",
               "con mucha antigüedad y veteranía en el grupo"),
        _nivel(av.get("salud"), "de salud frágil", "de salud robusta"),
        _nivel(av.get("atractivo"), "de aspecto poco agraciado",
               "de aspecto muy atractivo"),
    ) if r]
    if rasgos:
        frases.append("Carácter: " + "; ".join(rasgos) + ".")
    if p.get("trasfondo"):
        frases.append(f"Trasfondo: {p['trasfondo']}")
    frases.append(
        f"Todo lo que {nombre} dice y hace debe ser coherente con esta"
        " identidad, carácter y trasfondo."
    )
    return "\n".join(frases)


# Taxonomía sensible ÚNICA (reauditoría 31-07, G5) — la MISMA que declara
# FICHA_RIESGO_ESTEREOTIPOS.md y comprueba test_sensibles.py:
#   SENSIBLES (se neutralizan cuando variables_sensibles ≠ true):
#     origen_cultural, nse, ideología, religiosidad, salud, atractivo, idioma.
#   DE DISEÑO (NO se neutralizan — son constantes del experimento):
#     edad, género, educación.
# El scrub debe cubrir NSE en TODAS sus formas (protagonista, agente generado,
# media de población y variante) y NO tocar educación en ninguna.
SENSIBLES_AVANZADOS = ("ideologia", "religiosidad", "salud", "atractivo",
                       "idioma")
# Claves sensibles por contenedor, según la estructura REAL que exportan el
# panel (construirConfig) y consume el runner: protagonista.avanzados,
# agente_generado.b2 y sus claves planas (ori/nse/idi), demografia de
# cualquiera de los dos (incluida la media de NSE de población), y las
# medias/distribuciones de poblacion (demografia.origenes_culturales,
# mas_atributos.*).
_SENSIBLES_B2 = ("ideo", "reli", "salud", "atr")
# nse_media es la media de NSE de la población (poblacion.demografia): NSE es
# sensible en TODAS sus formas. educacion/educacion_media NO se tocan (diseño).
_SENSIBLES_DEMOGRAFIA = ("origen_cultural", "nse", "nse_media")
_SENSIBLES_PLANAS = ("ori", "nse", "idi")
_SENSIBLES_MAS_ATRIBUTOS = ("ideologia_media", "religiosidad_media",
                            "salud_media", "atractivo_media",
                            "pct_otra_lengua")
_SENSIBLES_PARAM_VARIANTE = frozenset(
    SENSIBLES_AVANZADOS + _SENSIBLES_B2 + _SENSIBLES_MAS_ATRIBUTOS
    # Claves reales de las variantes del panel (PARAMS de panel/app.js):
    # t2_* son las medias de los atributos avanzados; idiomaPct, la lengua;
    # nsemedia, la media de NSE. eduMedia (educación) NO está: es de diseño.
    + ("t2_ideo", "t2_reli", "t2_salud", "t2_atr", "idiomapct", "nsemedia"))


def _neutralizar_nodo(d: dict) -> None:
    """Elimina las claves sensibles presentes en UN dict, sea protagonista,
    agente generado, demografía, b2, avanzados o mas_atributos."""
    av = d.get("avanzados")
    if isinstance(av, dict):
        for k in SENSIBLES_AVANZADOS:
            av.pop(k, None)
    b2 = d.get("b2")
    if isinstance(b2, dict):
        for k in _SENSIBLES_B2:
            b2.pop(k, None)
    demo = d.get("demografia")
    if isinstance(demo, dict):
        for k in _SENSIBLES_DEMOGRAFIA:
            demo.pop(k, None)
        demo.pop("origenes_culturales", None)
    for k in _SENSIBLES_PLANAS:
        d.pop(k, None)
    mas = d.get("mas_atributos")
    if isinstance(mas, dict):
        for k in _SENSIBLES_MAS_ATRIBUTOS:
            mas.pop(k, None)
    cambios = d.get("cambios")
    if isinstance(cambios, list):
        # Una variante no puede reintroducir por la puerta de atrás lo que
        # el escenario declaró neutro: sus cambios sensibles se descartan.
        d["cambios"] = [c for c in cambios
                        if not (isinstance(c, dict) and
                                str(c.get("param", "")).lower()
                                in _SENSIBLES_PARAM_VARIANTE)]


def neutralizar_sensibles(escenario: dict) -> None:
    """Cinturón del MOTOR (reauditoría 31-07, P1.8): recorre RECURSIVAMENTE
    la estructura real del escenario (protagonistas, poblacion como OBJETO
    con agentes_generados, variantes, y cualquier anidamiento futuro) y
    elimina los atributos sensibles antes de verbalizar — aunque el JSON
    venga antiguo o manipulado; el panel deja de ser la única barrera.
    texto_persona()/persona_de_poblacion() omiten campos ausentes.

    La versión anterior iteraba `poblacion` como lista siendo un objeto:
    los agentes generados conservaban origen, NSE, idioma, ideología,
    religiosidad, salud y atractivo (regresión P0 de la reauditoría)."""
    visitados: set[int] = set()

    def _walk(nodo) -> None:
        if isinstance(nodo, dict):
            if id(nodo) in visitados:
                return
            visitados.add(id(nodo))
            _neutralizar_nodo(nodo)
            for v in nodo.values():
                _walk(v)
        elif isinstance(nodo, list):
            for v in nodo:
                _walk(v)

    _walk(escenario)


def persona_de_poblacion(a: dict) -> dict:
    """Adapta un agente de población del diseñador (nom/gen/ori/b/b2...)
    al esquema de protagonista que consumen texto_persona() y el runner."""
    b2 = a.get("b2") or {}
    rol = a.get("rol", "")
    if a.get("sub") and a["sub"] != "—":
        rol = f"{rol} ({a['sub']})".strip()
    return {
        "nombre": a.get("nom", "Alguien"),
        "rol": rol,
        "objetivo": ("hacer su vida en el lugar: hablar con quien tenga"
                     " cerca, comentar lo que pasa, y tomar partido cuando"
                     " algo le afecte — nunca quedarse como una estatua"),
        "demografia": {"edad": a.get("edad"), "genero": a.get("gen"),
                       "origen_cultural": a.get("ori"), "nse": a.get("nse"),
                       "educacion": a.get("edu")},
        "big5": a.get("b") or {},
        "avanzados": {"ideologia": b2.get("ideo"),
                      "religiosidad": b2.get("reli"),
                      "antiguedad": b2.get("anti"), "salud": b2.get("salud"),
                      "atractivo": b2.get("atr"),
                      "idioma": ("" if a.get("idi") in (None, "", "castellano")
                                 else a.get("idi"))},
    }


@dataclasses.dataclass
class PersonaEntity(prefab_lib.Prefab):
    """`basic__Entity` + componente constante de identidad («persona»)."""

    description: str = (
        "An entity like basic__Entity but with a permanent identity block "
        "(demographics, personality traits, backstory) visible on every "
        "decision, so the character does not drift."
    )
    params: Mapping[str, str] = dataclasses.field(
        default_factory=lambda: {
            "name": "Alice",
            "goal": "",
            "persona": "",
            # Canal privado: genera monólogo interno por turno. Nunca es
            # visible para otros agentes ni para el GM (vive dentro del
            # agente); va al log para el visor, y los análisis lo excluyen
            # por defecto (regla de los dos canales, PROPUESTA §8).
            "pensamientos": True,
        }
    )

    def build(
        self,
        model: language_model.LanguageModel,
        memory_bank: basic_associative_memory.AssociativeMemoryBank,
    ) -> entity_agent_with_logging.EntityAgentWithLogging:
        entity_name = self.params.get("name", "Alice")
        entity_goal = self.params.get("goal", "")
        persona = self.params.get("persona", "")
        # Enrutado por rol: la población puede usar un modelo más ligero.
        model = self.params.get("modelo") or model

        memory_key = agent_components.memory.DEFAULT_MEMORY_COMPONENT_KEY
        memory = agent_components.memory.AssociativeMemory(
            memory_bank=memory_bank)

        instructions = agent_components.instructions.Instructions(
            agent_name=entity_name, pre_act_label="\nInstructions")

        observation_to_memory = (
            agent_components.observation.ObservationToMemory())
        observation_key = (
            agent_components.observation.DEFAULT_OBSERVATION_COMPONENT_KEY)
        observation = agent_components.observation.LastNObservations(
            history_length=VENTANA_OBSERVACIONES,
            pre_act_label=(
                "\nEvents so far (ordered from least recent to most recent)"),
        )

        situation_perception_key = "SituationPerception"
        situation_perception = (
            agent_components.question_of_recent_memories.SituationPerception(
                model=model,
                num_memories_to_retrieve=25,
                pre_act_label=(
                    f"\nQuestion: What situation is {entity_name} in right"
                    " now?\nAnswer"),
            )
        )
        person_by_situation_key = "PersonBySituation"
        person_by_situation = (
            agent_components.question_of_recent_memories.PersonBySituation(
                model=model,
                num_memories_to_retrieve=5,
                components=[situation_perception_key],
                pre_act_label=(
                    f"\nQuestion: What would a person like {entity_name} do"
                    " in a situation like this?\nAnswer"),
            )
        )

        components_of_agent = {
            "Instructions": instructions,
            "Observation": observation_to_memory,
            situation_perception_key: situation_perception,
            person_by_situation_key: person_by_situation,
            observation_key: observation,
            memory_key: memory,
        }
        component_order = list(components_of_agent.keys())

        # Identidad tras las instrucciones: la ve en cada decisión.
        if persona:
            components_of_agent["Persona"] = agent_components.constant.Constant(
                state=persona, pre_act_label="\nIdentity and character")
            component_order.insert(1, "Persona")
        if entity_goal:
            components_of_agent["Goal"] = agent_components.constant.Constant(
                state=entity_goal, pre_act_label="\nGoal")
            component_order.insert(2 if persona else 1, "Goal")

        # Canal privado: se monta al final para poder condicionarlo a la
        # identidad (Persona) — sin ella, los pensamientos salían genéricos.
        if self.params.get("pensamientos", True):
            base = [k for k in ("Persona", "Goal") if k in components_of_agent]
            pensamiento = (
                agent_components.question_of_recent_memories
                .QuestionOfRecentMemories(
                    model=model,
                    pre_act_label=(
                        f"\n{entity_name}'s private inner monologue (never"
                        " spoken aloud, invisible to everyone else)"),
                    question=(
                        f"What is {entity_name} privately thinking and"
                        " feeling right now, in their inner voice? Stay true"
                        " to their identity and character. Include feelings"
                        " or opinions they would NOT say out loud. Answer in"
                        " Spanish, in first person, in 1-3 short sentences."),
                    answer_prefix=f"{entity_name} piensa: ",
                    add_to_memory=False,
                    components=base + [situation_perception_key],
                    num_memories_to_retrieve=10,
                )
            )
            components_of_agent["PensamientoPrivado"] = pensamiento
            component_order.insert(
                component_order.index(person_by_situation_key),
                "PensamientoPrivado")

        act_component = (
            agent_components.concat_act_component.ConcatActComponent(
                model=model,
                component_order=component_order,
                randomize_choices=True,
                prefix_entity_name=True,
            )
        )
        return entity_agent_with_logging.EntityAgentWithLogging(
            agent_name=entity_name,
            act_component=act_component,
            context_components=components_of_agent,
        )
