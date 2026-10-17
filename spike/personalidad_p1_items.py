"""Ítems del P1 de personalidad (10-10-2026). Ver PERSONALIDAD.md §7-8.

Cambios respecto al P0 (personalidad_items.py), cada uno por un problema
detectado en él:

  - SITUACIONES: las 179 calibradas en deseabilidad
    (personalidad_p1_seleccion.json), 30 por rasgo (H: 29), con la
    deseabilidad equilibrada a nivel de escala.
  - AUTOINFORME: claves equilibradas, 5 directos y 5 inversos por rasgo (el
    IPIP-50 traía 37/23 y N 8/2). Apertura pasa de Intelecto (factor V del
    IPIP-50) a apertura a la EXPERIENCIA con ítems del IPIP-NEO (dominio
    público; imaginación, intereses artísticos, emocionalidad, aventura,
    intelecto, liberalismo), para que case con las situaciones. Traducción
    propia sin validar.
  - BIOGRAFIA: la persona ya no se describe con la etiqueta del rasgo (en el
    P0 la elasticidad se saturaba en 94-100 porque el descriptor era casi la
    opción) sino con una biografía de conductas pasadas, en dominios
    distintos de las situaciones, dos variantes por polo.
"""

import json
import pathlib

RASGOS = ("O", "C", "E", "A", "N", "H")

# (id, rasgo, clave, texto); clave +1 = de acuerdo es más rasgo.
AUTOINFORME = [
    # Apertura a la experiencia (IPIP-NEO)
    ("O1", "O", +1, "Tengo una imaginación viva."),
    ("O2", "O", +1, "Me encanta soñar despierto."),
    ("O3", "O", +1, "Veo belleza en cosas que otros no ven."),
    ("O4", "O", +1, "Prefiero la variedad a la rutina."),
    ("O5", "O", +1, "Vivo mis emociones con intensidad."),
    ("O6", "O", -1, "Prefiero quedarme con lo que ya conozco."),
    ("O7", "O", -1, "No me gustan los cambios."),
    ("O8", "O", -1, "No disfruto yendo a museos de arte."),
    ("O9", "O", -1, "Evito las discusiones filosóficas."),
    ("O10", "O", -1, "Me aferro a las formas convencionales de hacer las cosas."),
    # Responsabilidad (IPIP-50 + 1 inverso del IPIP-NEO)
    ("C1", "C", +1, "Siempre estoy preparado."),
    ("C2", "C", +1, "Presto atención a los detalles."),
    ("C3", "C", +1, "Hago las tareas en cuanto toca."),
    ("C4", "C", +1, "Me gusta el orden."),
    ("C5", "C", +1, "Sigo un horario."),
    ("C6", "C", -1, "Dejo mis cosas por cualquier parte."),
    ("C7", "C", -1, "Lo enredo todo."),
    ("C8", "C", -1, "A menudo olvido devolver las cosas a su sitio."),
    ("C9", "C", -1, "Eludo mis obligaciones."),
    ("C10", "C", -1, "Hago lo justo para salir del paso."),
    # Extraversión (IPIP-50, ya equilibrada)
    ("E1", "E", +1, "Soy el alma de la fiesta."),
    ("E2", "E", +1, "Me siento a gusto rodeado de gente."),
    ("E3", "E", +1, "Soy quien inicia las conversaciones."),
    ("E4", "E", +1, "En las reuniones hablo con mucha gente distinta."),
    ("E5", "E", +1, "No me importa ser el centro de atención."),
    ("E6", "E", -1, "No hablo mucho."),
    ("E7", "E", -1, "Me mantengo en un segundo plano."),
    ("E8", "E", -1, "Tengo poco que decir."),
    ("E9", "E", -1, "No me gusta llamar la atención."),
    ("E10", "E", -1, "Con desconocidos soy callado."),
    # Amabilidad (IPIP-50 + 1 inverso del IPIP-NEO)
    ("A1", "A", +1, "Me interesan las personas."),
    ("A2", "A", +1, "Comparto los sentimientos de los demás."),
    ("A3", "A", +1, "Tengo buen corazón."),
    ("A4", "A", +1, "Saco tiempo para los demás."),
    ("A5", "A", +1, "Siento las emociones de los demás."),
    ("A6", "A", -1, "Me preocupo poco por los demás."),
    ("A7", "A", -1, "Insulto a la gente."),
    ("A8", "A", -1, "No me interesan los problemas de otras personas."),
    ("A9", "A", -1, "En realidad no me interesan los demás."),
    ("A10", "A", -1, "Soy indiferente a los sentimientos de los demás."),
    # Neuroticismo (IPIP-50 + 3 inversos del IPIP-NEO)
    ("N1", "N", +1, "Me estreso con facilidad."),
    ("N2", "N", +1, "Me preocupo por las cosas."),
    ("N3", "N", +1, "Me enfado con facilidad."),
    ("N4", "N", +1, "Cambio mucho de humor."),
    ("N5", "N", +1, "A menudo me siento triste."),
    ("N6", "N", -1, "Estoy relajado casi siempre."),
    ("N7", "N", -1, "Rara vez me siento triste."),
    ("N8", "N", -1, "Mantengo la calma bajo presión."),
    ("N9", "N", -1, "Rara vez me irrito."),
    ("N10", "N", -1, "No me avergüenzo con facilidad."),
    # Honestidad-Humildad (los 10 ad hoc del P0, ya equilibrados)
    ("H1", "H", +1, "No finjo que alguien me cae bien para conseguir algo de esa persona."),
    ("H2", "H", +1, "Si me dieran cambio de más, lo devolvería."),
    ("H3", "H", +1, "Tener cosas de lujo me importa poco."),
    ("H4", "H", +1, "Me considero una persona corriente, no mejor que los demás."),
    ("H5", "H", +1, "No aceptaría un beneficio que perjudicara injustamente a otro."),
    ("H6", "H", -1, "Adularía a alguien si con eso consiguiera lo que quiero."),
    ("H7", "H", -1, "Me saltaría una norma si supiera que nadie se va a enterar."),
    ("H8", "H", -1, "Me gustaría que me vieran con cosas caras."),
    ("H9", "H", -1, "Creo que merezco más respeto que la persona media."),
    ("H10", "H", -1, "Exageraría mis logros si eso me abriera una puerta."),
]

# Biografías por rasgo y polo, dos variantes. Conductas pasadas, sin la
# etiqueta del rasgo, sin marcas de género y en dominios distintos de las
# situaciones en lo posible.
BIOGRAFIA = {
    "O": {"alto": ("En los últimos años ha aprendido cerámica, ha vivido una temporada en Marruecos y se ha aficionado a la poesía contemporánea.",
                   "Le cuesta repetir restaurante porque siempre busca platos y lugares nuevos, y pasa las noches leyendo sobre temas ajenos a su trabajo."),
          "bajo": ("Lleva veinte años veraneando en el mismo pueblo, ve las series de siempre y prefiere las cosas como las ha conocido.",
                   "Tiene sus rutinas bien asentadas: el mismo bar, las mismas lecturas y poco interés por modas o experimentos.")},
    "C": {"alto": ("Lleva una agenda al minuto, nunca ha entregado tarde un trabajo y repasa dos veces todo lo que firma.",
                   "Planifica la compra de la semana el domingo, tiene los papeles de casa archivados por años y cumple siempre lo que se propone."),
          "bajo": ("Suele dejar las cosas para el último momento, improvisa sobre la marcha y a menudo no sabe dónde ha dejado las llaves.",
                   "Trabaja a rachas, cuando le apetece, y le aburren los horarios, las listas y los planes cerrados.")},
    "E": {"alto": ("Es quien organiza las cenas del grupo, conoce a medio barrio y se anima en cuanto hay gente alrededor.",
                   "Habla con cualquiera en la cola del supermercado, llena los fines de semana de planes y disfruta siendo el centro de las reuniones."),
          "bajo": ("Recarga energía a solas, prefiere quedar con una persona antes que con un grupo y en las fiestas suele marcharse pronto.",
                   "Habla poco en las reuniones, disfruta de los domingos en casa y evita los actos multitudinarios.")},
    "A": {"alto": ("Sus amistades dicen que nunca guarda rencor, que siempre cede el mejor sitio y que se desvive por quien lo necesita.",
                   "Evita las discusiones, confía en la gente casi sin reservas y suele anteponer lo que quieren los demás."),
          "bajo": ("Dice lo que piensa aunque escueza, negocia duro y no se fía de nadie hasta que se lo demuestran.",
                   "Compite en todo, defiende sus intereses sin rodeos y no tiene reparo en llevar la contraria.")},
    "N": {"alto": ("Le cuesta dormir cuando tiene algo pendiente, se agobia con facilidad y los imprevistos le afectan durante días.",
                   "Vive con un nudo en el estómago ante cualquier incertidumbre y tiene cambios de humor que le cuesta controlar."),
          "bajo": ("Duerme bien pase lo que pase, rara vez pierde los nervios y se repone enseguida de los contratiempos.",
                   "Afronta los problemas con calma, no se agobia por lo que no puede controlar y casi nunca se enfada.")},
    "H": {"alto": ("Nunca ha aceptado un trato de favor, dice la verdad aunque le perjudique y le traen sin cuidado el lujo y los títulos.",
                   "Vive con sencillez aunque gana bien, reparte el mérito con su equipo y no adorna nunca la verdad."),
          "bajo": ("Sabe halagar a quien conviene, aprovecha cualquier ventaja que se le presenta y le gusta lucir lo que tiene.",
                   "Cuida mucho su imagen y su estatus, adorna sus logros cuando le interesa y no deja pasar un trato de favor.")},
}

_SEL = pathlib.Path(__file__).parent / "personalidad_p1_seleccion.json"


def situaciones():
    """[(id, rasgo, situacion, alto, bajo)] del banco congelado del P1."""
    return [(d["id"], d["rasgo"], d["situacion"], d["alto"], d["bajo"])
            for d in json.loads(_SEL.read_text(encoding="utf-8"))]


def _comprobar():
    ids = [i[0] for i in AUTOINFORME]
    assert len(ids) == len(set(ids))
    for r in RASGOS:
        assert sum(1 for i in AUTOINFORME if i[1] == r and i[2] > 0) == 5, r
        assert sum(1 for i in AUTOINFORME if i[1] == r and i[2] < 0) == 5, r
        for polo in ("alto", "bajo"):
            assert len(BIOGRAFIA[r][polo]) == 2
    sits = situaciones()
    assert len({s[0] for s in sits}) == len(sits)


_comprobar()
