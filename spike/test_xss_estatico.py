"""Test estático anti-XSS (offline, sin navegador ni dependencias).

Hallazgos 3 y 7 de la revisión de seguridad: analiza panel/app.js,
viewer/app.js, panel/index.html y viewer/index.html y falla si
  (a) hay asignaciones .innerHTML cuyo lado derecho contenga ${ o
      concatenación con variables (se permiten literales estáticos
      puros y la cadena vacía "" para vaciar),
  (b) hay atributos inline onclick= / onerror= / oninput= en los HTML,
  (c) falta la meta Content-Security-Policy en alguno de los dos HTML,
  (d) el visor no declara las constantes de límites de carga
      (20 MB, 200 agentes, 50000 eventos, 10000 caracteres, lista
      blanca de tipos con constraint_violation).
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
JS = ["panel/app.js", "viewer/app.js"]
HTML = ["panel/index.html", "viewer/index.html"]

# Literal puro: una única cadena ("...", '...' o `...` sin ${ ni $).
_LITERAL_PURO = re.compile(
    r'^(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|`[^`$]*`)$')
# Asignación a .innerHTML (= o +=) hasta el ; de cierre.
_ASIGNA_INNERHTML = re.compile(r'\.innerHTML\s*\+?=\s*([^;]*);')
# Handlers inline prohibidos en HTML.
_HANDLER_INLINE = re.compile(r'\bon(?:click|error|input)\s*=', re.I)


def _c(cond, msg):
    print(("  ok  " if cond else " FAIL ") + msg)
    return cond


def _innerhtml_dinamicos(texto: str) -> list[str]:
    """Devuelve los lados derechos de innerHTML que no son literal estático."""
    malos = []
    for m in _ASIGNA_INNERHTML.finditer(texto):
        rhs = " ".join(m.group(1).split())
        if "${" in rhs or not _LITERAL_PURO.match(rhs):
            malos.append(rhs[:90])
    return malos


def run() -> bool:
    ok = True

    # (a) innerHTML dinámico en JS y HTML
    for rel in JS + HTML:
        texto = (RAIZ / rel).read_text(encoding="utf-8")
        malos = _innerhtml_dinamicos(texto)
        ok &= _c(not malos, f"{rel}: sin innerHTML dinámico"
                 + (f" — VISTOS: {malos[:3]}" if malos else ""))

    # (b) handlers inline en los HTML
    for rel in HTML:
        texto = (RAIZ / rel).read_text(encoding="utf-8")
        vistos = _HANDLER_INLINE.findall(texto)
        ok &= _c(not vistos, f"{rel}: sin onclick=/onerror=/oninput= inline"
                 + (f" — {len(vistos)} encontrados" if vistos else ""))

    # (c) meta CSP presente en ambos HTML
    for rel in HTML:
        texto = (RAIZ / rel).read_text(encoding="utf-8")
        tiene = re.search(r'http-equiv="Content-Security-Policy"', texto,
                          re.I) is not None
        ok &= _c(tiene, f"{rel}: meta Content-Security-Policy presente")

    # (d) constantes de límites de carga en el visor
    visor = (RAIZ / "viewer/app.js").read_text(encoding="utf-8")
    for nombre, patron in [
        ("LIMITE_TAM_FICHERO_MB = 20", r"LIMITE_TAM_FICHERO_MB\s*=\s*20\b"),
        ("LIMITE_TAM_FICHERO", r"const\s+LIMITE_TAM_FICHERO\s*="),
        ("LIMITE_AGENTES = 200", r"LIMITE_AGENTES\s*=\s*200\b"),
        ("LIMITE_EVENTOS = 50000", r"LIMITE_EVENTOS\s*=\s*50000\b"),
        ("LIMITE_CHARS_TEXTO = 10000", r"LIMITE_CHARS_TEXTO\s*=\s*10000\b"),
        ("TIPOS_EVENTO (lista blanca)", r"const\s+TIPOS_EVENTO\s*="),
        ("constraint_violation en la lista blanca",
         r'TIPOS_EVENTO\s*=\s*\[[^\]]*"constraint_violation"'),
    ]:
        ok &= _c(re.search(patron, visor, re.S) is not None,
                 f"viewer/app.js: constante {nombre}")

    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)


# ── Ampliación (auditoría 31-07): sinks adicionales y handlers on* completos.
_SINKS = re.compile(
    r"outerHTML\s*=|insertAdjacentHTML|document\.write|\beval\s*\(|"
    r"new\s+Function|javascript:", re.I)
_HANDLER_TOTAL = re.compile(r"\son[a-z]+\s*=", re.I)

_run_base = run


def run():
    ok = _run_base()
    for f in JS + HTML:
        t = (RAIZ / f).read_text(encoding="utf-8")
        ok &= _c(not _SINKS.search(t),
                 f"{f}: sin outerHTML/insertAdjacentHTML/document.write/"
                 "eval/new Function/javascript:")
    for f in HTML:
        t = (RAIZ / f).read_text(encoding="utf-8")
        ok &= _c(not _HANDLER_TOTAL.search(t),
                 f"{f}: sin NINGÚN handler inline on*=")
    print("ampliación de sinks: " + ("OK" if ok else "FALLOS"))
    return ok
