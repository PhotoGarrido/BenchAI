"""Test estático anti-XSS (offline, sin navegador ni dependencias).

Cubre TODAS las superficies HTML del repositorio: el diseñador (`panel/`),
el visor (`viewer/`), el panel del benchmark (`benchmark/`) y el sitio
divulgativo (`web/`). Falla si
  (a) hay asignaciones .innerHTML cuyo lado derecho contenga ${ o
      concatenación con variables (se permiten literales estáticos
      puros y la cadena vacía "" para vaciar),
  (b) hay atributos inline onclick= / onerror= / oninput= en los HTML,
  (c) falta la meta Content-Security-Policy en alguno de los HTML,
  (d) el visor no declara las constantes de límites de carga
      (20 MB, 200 agentes, 50000 eventos, 10000 caracteres, lista
      blanca de tipos con constraint_violation),
  (e) `web/` escribe HTML fuera de su única puerta (`web/js/marcado.js`),
      esa puerta pierde el escapador, o los datos generados
      (`web/datos.js`) traen marcado — el canario que sostiene que la
      prosa con `<b>` de la web es siempre del código y nunca del dato.

El apartado (e) es el que hace que la web pueda escribir prosa con marcado
sin abrir un agujero: `mk` escapa TODO lo interpolado y devuelve un objeto
marcado, así que una cadena suelta no puede llegar a innerHTML ni por
descuido ni por refactor. Ver la cabecera de `web/js/marcado.js`.
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
# `web/datos.js` es dato generado, no código: entra por su propio canario.
WEB_JS = sorted(
    str(p.relative_to(RAIZ)) for p in (RAIZ / "web").rglob("*.js")
    if p.name != "datos.js"
)
JS = ["panel/app.js", "viewer/app.js"] + WEB_JS
HTML = ["panel/index.html", "viewer/index.html", "benchmark/index.html",
        "web/home.html", "web/index.html", "web/visor-embebido.html"]
# La única puerta a innerHTML de `web/`, con su nombre por escrito.
PUERTA_MARCADO = "web/js/marcado.js"

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

    # (a) innerHTML dinámico en JS y HTML. La puerta de marcado se juzga
    #     aparte, en (e): ahí el lado derecho es dinámico A PROPÓSITO y lo
    #     que hay que exigir es que venga sellado por `mk`.
    for rel in JS + HTML:
        if rel == PUERTA_MARCADO:
            continue
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

    # (e) el sitio divulgativo: una sola puerta a innerHTML, con escapador,
    #     y el canario de que el dato generado no trae marcado.
    ok &= _puerta_de_marcado()

    print("\n" + ("TODOS OK" if ok else "HAY FALLOS"))
    return ok


# Marcado dentro de los datos generados: `<b>`, `<a href=…`, `<script`…
# (`a < b` o «d < 0,5» en prosa NO son marcado y no deben dar falso positivo).
_ETIQUETA = re.compile(r"<\s*/?\s*[a-zA-Z][a-zA-Z0-9]*(?:\s[^<>]*)?>")


def _puerta_de_marcado() -> bool:
    ok = True

    # e.1 · nadie de `web/` escribe HTML salvo la puerta
    fuera = [rel for rel in WEB_JS if rel != PUERTA_MARCADO
             and ".innerHTML" in (RAIZ / rel).read_text(encoding="utf-8")]
    ok &= _c(not fuera, "web/: innerHTML solo en la puerta de marcado"
             + (f" — LO USAN TAMBIÉN: {fuera}" if fuera else ""))

    # e.2 · la puerta escapa, sella y solo escribe lo sellado
    puerta = (RAIZ / PUERTA_MARCADO).read_text(encoding="utf-8")
    for nombre, patron in [
        ("escapa & < > \" '", r'"&":\s*"&amp;".*"<":\s*"&lt;".*">":\s*"&gt;"'
                             r'.*\'"\':\s*"&quot;".*"\'":\s*"&#39;"'),
        ("aplica el escapado a lo interpolado",
         r"esMarcado\(v\)\s*\?\s*v\[MARCA\]\s*:\s*escapar\(v\)"),
        ("rechaza lo que no venga sellado",
         r"if\s*\(!esMarcado\(marcado\)\)\s*\{\s*\n\s*throw"),
        ("una sola asignación a innerHTML",
         r"\A(?:(?!\.innerHTML\s*=).)*\.innerHTML\s*=\s*marcado\[MARCA\];"
         r"(?:(?!\.innerHTML\s*=).)*\Z"),
    ]:
        ok &= _c(re.search(patron, puerta, re.S) is not None,
                 f"{PUERTA_MARCADO}: {nombre}")

    # e.3 · canario: el dato generado no trae marcado. Si algún día una cita
    #       de un informe trae `<b>`, esto salta y obliga a decidir a mano.
    datos = (RAIZ / "web/datos.js").read_text(encoding="utf-8")
    etiquetas = _ETIQUETA.findall(datos)
    ok &= _c(not etiquetas, "web/datos.js: los datos generados no traen marcado"
             + (f" — VISTAS: {sorted(set(etiquetas))[:3]}" if etiquetas else ""))
    return ok


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


# El bloque __main__ va al FINAL del fichero, DESPUÉS de la redefinición de
# run() (reauditoría 31-07): situado antes, la ejecución directa salía por
# sys.exit sin evaluar jamás la ampliación de sinks — falso verde en CI.
if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
