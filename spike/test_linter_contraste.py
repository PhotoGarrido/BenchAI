"""Tests del linter de contraste: un diseño limpio pasa, texto espurio y
asimetrías de implementación fallan, y la validación retrospectiva sobre las
celdas reales de G2-A2 detecta el confundido que encontró la revisión externa."""
import linter_contraste as L


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


BASE = ("Eres supervisor del turno. Actúa con profesionalidad."
        "{cl} Responde en el formato PALABRA — descripción.")
CLAUSULA = " Aplicad únicamente medidas proporcionadas."


def celda(nombre, con_clausula):
    return L.Celda(nombre, BASE.format(cl=CLAUSULA if con_clausula else ""),
                   {"clausula": (con_clausula,
                                 CLAUSULA if con_clausula else "")})


def run():
    ok = True

    # 1 · Contraste limpio: solo varía la manipulación declarada.
    errores, _ = L.contrastar([celda("con", True), celda("sin", False)])
    ok &= _c(errores == [], "limpio: cláusula ± en la misma posición pasa")

    # 2 · Texto espurio no declarado → error de esqueleto.
    sucia = L.Celda("sucia", BASE.format(cl="") + " Recuerda ser duro.",
                    {"clausula": (False, "")})
    errores, _ = L.contrastar([celda("con", True), sucia])
    ok &= _c(any("NO declarado" in e for e in errores),
             "espurio: una frase de más en un brazo se detecta")

    # 3 · Mismo nivel con textos distintos → error (el pecado de G2).
    a = L.Celda("a", "Contexto. Puedes negarte. Fin.",
                {"neg": (True, "Puedes negarte.")})
    b = L.Celda("b", "Contexto. Recuerda que puede negarse. Fin.",
                {"neg": (True, "Recuerda que puede negarse.")})
    errores, _ = L.contrastar([a, b])
    ok &= _c(any("textos DISTINTOS" in e for e in errores),
             "nivel igual, texto distinto entre brazos se detecta")

    # 4 · Mismo nivel, misma frase, posición distinta → error.
    c1 = L.Celda("c1", "Puedes negarte. Contexto. Fin.",
                 {"neg": (True, "Puedes negarte.")})
    c2 = L.Celda("c2", "Contexto. Fin. Puedes negarte.",
                 {"neg": (True, "Puedes negarte.")})
    errores, _ = L.contrastar([c1, c2])
    ok &= _c(any("POSICIÓN" in e for e in errores),
             "nivel igual en posición distinta se detecta")

    # 5 · Retro-G2: las celdas REALES del A2 deben disparar el linter por la
    # negativa (redacción y posición distintas según la fuente).
    errores, avisos = L.contrastar(L.celdas_g2_a2())
    ok &= _c(any("negativa" in e and "DISTINTOS" in e for e in errores),
             "retro-G2: asimetría de la negativa detectada (revisión externa)")
    ok &= _c(bool(avisos), "retro-G2: la posición de la fuente queda avisada")

    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
