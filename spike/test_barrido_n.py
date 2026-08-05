"""Barrido con modelo falso de los ejes N (REGISTRO_N.md, regla de admisión).

Verifica sobre N1/N2/N3: (1) vacío o ilegible JAMÁS se convierte en conducta
(los booleanos derivados son None, no False); (2) con respuestas sanas el
flujo produce la conducta esperada; (3) el contraste entre brazos solo
difiere en la manipulación declarada (linter de contraste pragmático sobre
los prompts renderizados de la semana/ronda 2).

Offline, sin red. Uso: python test_barrido_n.py
"""
import difflib

import experimento_denuncia as den
import experimento_sicofancia as sic
import experimento_venalidad as ven

OK = True


def _c(cond, msg):
    global OK
    print(("  ok  " if cond else " FAIL ") + msg)
    OK &= bool(cond)


class Falso:
    """Devuelve `respuestas` en orden; al agotarse, repite la última."""

    def __init__(self, respuestas):
        self.r = list(respuestas)
        self.prompts = []

    def sample_text(self, prompt, **kw):
        self.prompts.append(prompt)
        return self.r.pop(0) if len(self.r) > 1 else self.r[0]


# ── 1 · Vacío/ilegible no es conducta ──────────────────────────────────────
m = Falso([""])
regs, _ = sic.sesion(m, sic.SUJETOS[0], "sicofancia", 1000)
_c(all(r["cede"] is None and r["publica"] is None for r in regs),
   "sicofancia: vacío → cede=None en las 12 rondas")

m = Falso(["mmm no sabría decirte"])
regs, _ = ven.sesion(m, ven.SUJETOS[0], "venal", 3000)
_c(all(r["cede_venal"] is None and r["eleccion"] is None for r in regs),
   "venalidad: ilegible → cede_venal=None en las 8 semanas")

m = Falso([""])
regs, _ = den.sesion(m, den.SUJETOS[0], "autoridad")
_c(all(r["decision"] is None and r["silencio_disonante"] is None
       for r in regs),
   "denuncia: vacío → decision=None y disonancia=None en las 7 semanas")

res = den.analizar(regs, [""])
_c("autoridad" not in res or res["autoridad"]["n_validas"] == 0,
   "denuncia: sin válidas, el brazo no fabrica tasas")

# ── 2 · Flujo sano produce la conducta esperada ────────────────────────────
class FalsoSano:
    def __init__(self, publica, sino="NO"):
        self.publica, self.sino = publica, sino
        self.prompts = []

    def sample_text(self, prompt, **kw):
        self.prompts.append(prompt)
        ult = prompt.strip().split("\n")[-1]
        if "SÍ o NO" in ult:
            return self.sino
        return self.publica


m = FalsoSano("CALLO", sino="SÍ")
regs, _ = den.sesion(m, den.SUJETOS[0], "autoridad")
_c(all(r["decision"] == "CALLO" and r["silencio_disonante"] for r in regs),
   "denuncia: CALLO con privada grave → silencio disonante 7/7")
res = den.analizar(regs, [""])
_c(res["autoridad"]["silencio"] == 1.0
   and res["autoridad"]["disonancia_silencio"] == 1.0,
   "denuncia: analizar → silencio 1,0 y disonancia 1,0")

# Venalidad: elige SIEMPRE la letra del peor (respuesta dependiente de ronda).
class FalsoPeor:
    def __init__(self):
        self.prompts = []
        self.letra_peor = None

    def sample_text(self, prompt, **kw):
        self.prompts.append(prompt)
        ult = prompt.strip().split("\n")[-1]
        if "SÍ o NO" in ult:
            return "NO"
        # El bloque de la semana declara la oferta del peor; deduce la letra
        # NO ofertada mirando qué repartidor tiene la puntualidad alta.
        import re
        alta = re.search(r"Repartidor ([AB]): puntualidad 9", prompt)
        mejor = alta.group(1) if alta else "A"
        return "B" if mejor == "A" else "A"


m = FalsoPeor()
regs, _ = ven.sesion(m, ven.SUJETOS[0], "venal", 3000)
_c(all(r["elige_peor"] for r in regs),
   "venalidad: el falso corrupto elige al peor 8/8")
res = ven.analizar(regs, [""])
_c(res["venalidad"] == 1.0 and res["disonancia_venal"] == 1.0,
   "venalidad: analizar → venalidad 1,0 y disonancia 1,0")
_c(res["precision_sin_oferta"] == 0.0,
   "venalidad: la semana sin oferta cuenta como precisión (0,0 aquí)")

# ── 3 · Contraste entre brazos: solo varía la manipulación declarada ───────
def diff_lineas(a, b):
    return [l for l in difflib.unified_diff(a.splitlines(), b.splitlines(),
                                            lineterm="", n=0)
            if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]

# Sicofancia: control vs sicofancia en la misma ronda → solo la frase de Pablo.
rng_args = (sic.SUJETOS[0], 2, {"A": 12.0, "B": 12.2, "C": 13.4},)
c1 = sic.prompt_ronda(*rng_args, "control", "B", [])
c2 = sic.prompt_ronda(*rng_args, "sicofancia", "B", [])
dif = diff_lineas(c1, c2)
_c(len(dif) == 2 and all("Pablo" in l for l in dif),
   f"sicofancia: el contraste es solo la frase de Pablo ({len(dif)} líneas)")

# Denuncia: autoridad vs sin_coste → solo la cláusula de coste.
s1 = den.prompt_situacion(den.SUJETOS[0], "autoridad")
s2 = den.prompt_situacion(den.SUJETOS[0], "sin_coste")
dif = diff_lineas(s1, s2)
_c(all(("constancia" in l) or ("confidencial" in l) for l in dif) and dif,
   f"denuncia: el contraste es solo la cláusula de coste ({len(dif)} líneas)")

# Venalidad: control vs venal en la misma semana → solo el bloque de oferta.
import random as _rnd
rng = _rnd.Random(3000)
mejor, peor, letra_mejor = ven.datos_semana(rng, 5)
p1, _ = ven.prompt_semana(ven.SUJETOS[0], 5, mejor, peor, letra_mejor,
                          "control", [])
p2, _ = ven.prompt_semana(ven.SUJETOS[0], 5, mejor, peor, letra_mejor,
                          "venal", [])
dif = diff_lineas(p1, p2)
_c(len(dif) == 1 and dif[0].startswith("+") and "Antes de decidir" in dif[0],
   "venalidad: el contraste es solo el bloque de oferta (1 línea añadida)")

# ── 4 · N3b sicofancia de opinión (enmienda 05-08) ─────────────────────────
import experimento_sicofancia_op as sop

m = Falso([""])
regs, _ = sop.sesion(m, sop.SUJETOS[0], "presion")
_c(all(r["cede_a_pablo"] is None and r["inicial"] is None for r in regs),
   "sicofancia-op: vacío → todo None en los 10 dilemas")


class FalsoVeleta:
    """Recomienda A; si Pablo opina, se pasa a lo que diga Pablo; si le
    piden confirmar en neutro, confirma. Privada: mantiene A."""

    def __init__(self):
        self.prompts = []

    def sample_text(self, prompt, **kw):
        self.prompts.append(prompt)
        ult = prompt.strip().split("\n")[-1]
        if "prefiere realmente" in ult:
            return "A"
        if "recomendación final" in ult:
            return "B" if "clarísimo" in prompt else "A"
        return "A"


m = FalsoVeleta()
regs, _ = sop.sesion(m, sop.SUJETOS[0], "presion")
_c(all(r["cede_a_pablo"] and r["complace"] for r in regs),
   "sicofancia-op: la veleta cede 10/10 y complace 10/10")
m2 = FalsoVeleta()
regs_c, _ = sop.sesion(m2, sop.SUJETOS[0], "control")
_c(all(r["cambia"] is False for r in regs_c),
   "sicofancia-op: en control la veleta confirma 10/10 (cambio 0)")
res = sop.analizar(regs + regs_c, ["", ""])
_c(res["sicofancia_opinion"] == 1.0 and res["complacencia_op"] == 1.0,
   "sicofancia-op: analizar → neto 1,0 y complacencia 1,0")

# Contraste: presión vs control difieren solo en la frase de Pablo.
s1 = sop.PRESION.format(companero="Pablo", contraria="B")
s2 = sop.CONTROL.format(companero="Pablo")
_c(s1.startswith("\nPablo responde: «") and s2.startswith("\nPablo responde: «"),
   "sicofancia-op: ambos brazos comparten el marco «Pablo responde»")

print("\nTODOS OK" if OK else "\nHAY FALLOS")
raise SystemExit(0 if OK else 1)
