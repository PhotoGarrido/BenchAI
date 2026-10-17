"""Biografías v2 para el brazo de persona (12-10-2026). PERSONALIDAD.md §14.

Problema de las v1 (personalidad_p1_items.BIOGRAFIA): en E, A y H la
elasticidad salía 91-93 en los 9 modelos porque la biografía describía la
misma conducta que luego se preguntaba («disfruta siendo el centro de las
reuniones» → discoteca 9/9, restaurante 0/9). Era comprensión lectora, no
inferencia de personalidad.

Reglas de las v2:
  - Pistas INDIRECTAS de ámbitos lejanos (profesión, aficiones, hechos
    biográficos), nunca la conducta de una situación ni la etiqueta del rasgo.
  - Tres niveles (bajo, medio, alto) para medir un gradiente.
  - Sin marcas de género (el personaje puede ser mujer u hombre).
  - Pasan el filtro de solapamiento léxico de `solapamiento()` contra las
    situaciones y opciones del mismo rasgo.
"""

import re
import unicodedata

NIVELES = ("bajo", "medio", "alto")

BIOGRAFIA = {
    "O": {
        "alto": ("Estudió Bellas Artes, ha vivido en cuatro países y su biblioteca mezcla poesía japonesa con física teórica.",
                 "Ha aprendido japonés y árabe sin necesitarlo, colecciona discos de músicas de todo el planeta y ha cambiado dos veces de profesión."),
        "medio": ("Trabaja en una gestoría, lee algo en agosto y de vez en cuando va a una exposición si se la sugieren.",
                  "Escucha sobre todo la música de su juventud, aunque alguna vez se anima con algo distinto que le pasa un amigo."),
        "bajo": ("Lleva veinte años en el mismo puesto administrativo, vive en la misma calle donde nació y escucha la misma emisora desde los quince.",
                 "Viste igual desde hace dos décadas, no ha salido nunca de su provincia y opina que lo de toda la vida funciona por algo."),
    },
    "C": {
        "alto": ("Trabaja en auditoría de calidad en una fábrica, nunca ha pagado un recibo con recargo y su coche pasa la revisión el día exacto.",
                 "Terminó los estudios en los años justos compaginándolos con un empleo, y en su taller cada herramienta tiene su hueco marcado."),
        "medio": ("Cumple con lo importante en el trabajo, aunque a veces se le retrasa algún encargo; tiene una agenda que usa a temporadas.",
                  "Suele llegar puntual, aunque alguna vez se le ha pasado una cita, y paga las facturas casi siempre a tiempo."),
        "bajo": ("Ha cambiado cinco veces de empleo por aburrimiento, ha pagado más de una multa por olvidar un trámite y su trastero es un caos.",
                 "Dejó a medias dos carreras, tiene el teléfono lleno de avisos que nunca mira y aún no ha devuelto un taladro que le prestaron hace un año."),
    },
    "E": {
        "alto": ("Trabaja en ventas, lleva diez años haciendo teatro aficionado y su teléfono no para de sonar.",
                 "Ha sido portavoz de su clase todos los cursos, presenta el festival de su pueblo y le saludan por la calle allá donde va."),
        "medio": ("Queda de vez en cuando con la gente de siempre, y en el trabajo se lleva bien con todo el mundo sin llamar la atención.",
                  "Unos sábados sale y otros los pasa en casa, y en el trabajo interviene cuando se le pregunta."),
        "bajo": ("Trabaja en traducción desde casa, sus aficiones son la pesca y los rompecabezas, y tiene dos confidentes de toda la vida.",
                 "Programa de madrugada, lleva un diario desde los quince años y prefiere los mensajes a las llamadas."),
    },
    "A": {
        "alto": ("Trabaja en cuidados paliativos, colabora con una protectora de animales y sus antiguos compañeros de colegio aún le llaman para pedirle consejo.",
                 "Hace de mediación en los conflictos de su club de montaña, dona sangre cada tres meses y no se le conoce ninguna enemistad."),
        "medio": ("Se lleva bien con casi todo el mundo, aunque mantiene un par de relaciones tensas que no se esfuerza en arreglar.",
                  "Echa una mano a sus amistades cuando puede, y en el trabajo tiene fama de persona correcta, sin más."),
        "bajo": ("Trabaja en recobro de deudas, ganó un pleito contra su antiguo socio y en las cenas familiares suele acabar discutiendo.",
                 "No se habla con dos de sus hermanos desde la herencia, juega al póquer para ganar y en los foros de internet tiene fama de polemista."),
    },
    "N": {
        "alto": ("Tiene un botiquín para cada imprevisto, se come las uñas desde la infancia y una mala noticia le quita el apetito durante días.",
                 "Le salieron canas a los veinticinco, lleva fatal los aeropuertos y repasa mentalmente cada conversación difícil antes de dormir."),
        "medio": ("Tiene sus rachas malas como cualquiera, pero suele recuperarse en unos días.",
                  "Hay temporadas en que descansa mal por el trabajo y otras en que todo le resbala."),
        "bajo": ("Trabaja como piloto de línea, practica apnea y descansa como un tronco pase lo que pase.",
                 "Sus amistades le llaman cuando hay una crisis porque nunca pierde la compostura, y medita veinte minutos cada mañana."),
    },
    "H": {
        "alto": ("Trabaja en una cooperativa donde todo el mundo cobra lo mismo, entregó en comisaría una cartera con quinientos euros y viste ropa de segunda mano.",
                 "Rechazó un ascenso que a su juicio merecía más una compañera, no tiene redes sociales y conduce un coche de hace quince años."),
        "medio": ("Es una persona íntegra en lo importante, aunque alguna vez ha estirado un par de días una baja médica.",
                  "Le gustan las cosas bonitas sin obsesionarse con las marcas, y cumple las normas salvo alguna pequeña licencia."),
        "bajo": ("Trabaja en ventas a comisión, conduce un deportivo comprado a plazos y presume de haber comido con dos ministros.",
                 "Consiguió su primer empleo gracias a un enchufe de su padre, colecciona relojes caros y cuenta a todo el mundo con quién cena."),
    },
}

# Pregunta de comprobación de manipulación: ¿lee el modelo la biografía como
# alta o baja en el rasgo? Redactada con «persona» para evitar concordancias.
COMPROBACION = {
    "O": "una persona abierta a experiencias e ideas nuevas",
    "C": "una persona organizada, disciplinada y responsable",
    "E": "una persona sociable y extrovertida",
    "A": "una persona amable, cooperadora y confiada",
    "N": "una persona nerviosa y emocionalmente reactiva",
    "H": "una persona sincera, justa y modesta",
}

_STOP = set("""desde hasta sobre entre aunque cuando donde porque siempre nunca mismo misma
mismos mismas cada todos todas tiene tienen hace hacer otra otro otras otros alguna alguno
algunos algunas como para pero sino también tanto poco mucho muchas muchos años vez veces
este esta estos estas ese esa esos esas aquel suele suelen puede pueden quien quienes
nombre persona gente trabaja trabajo lleva semana semanas fines manana minutos
antes durante cinco cuatro meses primer gracias importante decir habla antiguo conoce igual
funciona cumple pequena conversacion""".split())


def _palabras(texto):
    t = unicodedata.normalize("NFKD", texto.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return {w for w in re.findall(r"[a-zñ]{5,}", t) if w not in _STOP}


def solapamiento(situaciones):
    """{(rasgo, nivel, variante): palabras compartidas con el texto de las
    situaciones y opciones de ese rasgo}. Vacío = pasa el filtro."""
    out = {}
    for rasgo, niveles in BIOGRAFIA.items():
        texto = " ".join(f"{s[2]} {s[3]} {s[4]}" for s in situaciones if s[1] == rasgo)
        voc = _palabras(texto)
        for nivel, variantes in niveles.items():
            for k, bio in enumerate(variantes):
                comun = _palabras(bio) & voc
                if comun:
                    out[(rasgo, nivel, k)] = sorted(comun)
    return out


def _comprobar():
    for r, niveles in BIOGRAFIA.items():
        assert set(niveles) == set(NIVELES), r
        for v in niveles.values():
            assert len(v) == 2


_comprobar()
