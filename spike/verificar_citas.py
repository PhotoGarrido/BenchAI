"""Verificación de la bibliografía del preprint contra registros académicos.

Toda referencia de `preprint/preprint.md §Referencias` debe corresponder a un
registro real (Crossref para DOIs de editorial, arXiv para 10.48550/*, o
búsqueda bibliográfica en Crossref si no declara DOI). El resultado vive en
`preprint/citas_verificadas.json` (caché versionada, con hash de la línea
verificada) para que la CI pueda comprobar SIN red que:

  - toda referencia actual tiene entrada en la caché,
  - la línea no cambió desde su verificación (hash),
  - su estado es 'verificada'.

Uso:
  python verificar_citas.py --verificar   # con red: consulta y refresca caché
  python verificar_citas.py --check       # sin red: puerta determinista (CI)
"""

import argparse
import datetime
import difflib
import hashlib
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

RAIZ = pathlib.Path(__file__).parent.parent
PREPRINT = RAIZ / "preprint" / "preprint.md"
CACHE = RAIZ / "preprint" / "citas_verificadas.json"
UMBRAL_TITULO = 0.65


def referencias():
    """Líneas de la sección Referencias: (línea, doi|None, titulo, autor, año)."""
    texto = PREPRINT.read_text(encoding="utf-8")
    seccion = texto.split("## Referencias", 1)[1]
    refs = []
    for linea in seccion.splitlines():
        linea = linea.strip()
        if not linea.startswith("- "):
            continue
        doi = re.search(r"doi\.org/([^\s]+?)\.?$", linea)
        titulo = re.search(r"\(\d{4}\)\.\s+(.+?[.?])\s+\*", linea)
        # Apellido = todo hasta la primera coma («Le Texier», «Van Dijk»).
        autor = re.match(r"- ([^,]+),", linea)
        anio = re.search(r"\((\d{4})\)", linea)
        refs.append({
            "linea": linea,
            "hash": hashlib.sha256(linea.encode()).hexdigest()[:16],
            "doi": doi.group(1) if doi else None,
            "titulo": titulo.group(1).rstrip(".?") if titulo else None,
            "autor": autor.group(1) if autor else None,
            "anio": int(anio.group(1)) if anio else None,
        })
    return refs


def _get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "PsicoAI-verificar-citas/1.0 (mailto:wadaka@gmail.com)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def _similar(a, b):
    norm = lambda s: re.sub(r"[^a-z0-9 ]", "", (s or "").lower())  # noqa: E731
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def _registro_crossref(doi):
    j = json.loads(_get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"))
    m = j["message"]
    return {"titulo": (m.get("title") or [""])[0],
            "autores": [a.get("family", "") for a in m.get("author", [])],
            "fuente": "crossref"}


def _registro_arxiv(doi):
    arxiv_id = doi.split("arXiv.", 1)[1]
    xml = _get("http://export.arxiv.org/api/query?id_list="
               + urllib.parse.quote(arxiv_id))
    ns = {"a": "http://www.w3.org/2005/Atom"}
    entry = ET.fromstring(xml).find("a:entry", ns)
    if entry is None or entry.find("a:title", ns) is None:
        raise LookupError(f"arXiv sin registro para {arxiv_id}")
    return {"titulo": entry.find("a:title", ns).text.strip(),
            "autores": [n.text.split()[-1] for n in
                        entry.findall("a:author/a:name", ns)],
            "fuente": "arxiv"}


def _busqueda_crossref(ref):
    q = urllib.parse.quote(f"{ref['titulo']} {ref['autor']}")
    j = json.loads(_get("https://api.crossref.org/works?rows=8"
                        f"&query.bibliographic={q}"))
    for m in j["message"]["items"]:
        reg = {"titulo": (m.get("title") or [""])[0],
               "autores": [a.get("family", "") for a in m.get("author", [])],
               "fuente": "crossref-busqueda", "doi_encontrado": m.get("DOI")}
        if _similar(ref["titulo"], reg["titulo"]) >= UMBRAL_TITULO:
            return reg
    # Crossref no cubre PMLR y otros proceedings: segundo camino, arXiv.
    ns = {"a": "http://www.w3.org/2005/Atom"}
    q = urllib.parse.quote(f'ti:"{ref["titulo"]}"')
    xml = _get("http://export.arxiv.org/api/query?max_results=5"
               f"&search_query={q}")
    for entry in ET.fromstring(xml).findall("a:entry", ns):
        t = entry.find("a:title", ns)
        if t is None:
            continue
        reg = {"titulo": " ".join(t.text.split()),
               "autores": [n.text.split()[-1] for n in
                           entry.findall("a:author/a:name", ns)],
               "fuente": "arxiv-busqueda",
               "doi_encontrado": (entry.find("a:id", ns).text or "")
               .replace("http://arxiv.org/abs/", "arXiv:")}
        if _similar(ref["titulo"], reg["titulo"]) >= UMBRAL_TITULO:
            return reg
    raise LookupError("sin candidato compatible (Crossref ni arXiv)")


def verificar_una(ref):
    try:
        if ref["doi"] and ref["doi"].startswith("10.48550/"):
            reg = _registro_arxiv(ref["doi"])
        elif ref["doi"]:
            reg = _registro_crossref(ref["doi"])
        elif ref["titulo"]:
            reg = _busqueda_crossref(ref)
        else:
            return {"estado": "sin_datos_verificables"}
    except Exception as e:  # noqa: BLE001 — el fallo ES el resultado
        return {"estado": "error_consulta", "detalle": str(e)[:200]}
    sim = _similar(ref["titulo"], reg["titulo"])
    autor_ok = (not ref["autor"]) or any(
        _similar(ref["autor"], a) > 0.8 for a in reg["autores"])
    if sim >= UMBRAL_TITULO and autor_ok:
        return {"estado": "verificada", "fuente": reg["fuente"],
                "titulo_registrado": reg["titulo"][:160],
                "similitud_titulo": round(sim, 2),
                **({"doi_encontrado": reg["doi_encontrado"]}
                   if "doi_encontrado" in reg else {})}
    return {"estado": "discrepancia", "fuente": reg["fuente"],
            "titulo_registrado": reg["titulo"][:160],
            "similitud_titulo": round(sim, 2),
            "autor_coincide": autor_ok}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verificar", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    refs = referencias()

    if args.verificar:
        salida = []
        for ref in refs:
            v = verificar_una(ref)
            salida.append({"hash": ref["hash"], "doi": ref["doi"],
                           "linea": ref["linea"][:120],
                           "comprobada": datetime.date.today().isoformat(),
                           **v})
            print(f"  {v['estado']:<22} {ref['linea'][:80]}")
        CACHE.write_text(json.dumps(salida, ensure_ascii=False, indent=1)
                         + "\n", encoding="utf-8")
        malas = [s for s in salida if s["estado"] != "verificada"]
        print(f"\n{len(salida) - len(malas)}/{len(salida)} verificadas"
              f" → {CACHE.relative_to(RAIZ)}")
        sys.exit(1 if malas else 0)

    # --check (CI, sin red): caché completa, fresca por hash y toda verde.
    cache = {c["hash"]: c for c in json.loads(
        CACHE.read_text(encoding="utf-8"))} if CACHE.exists() else {}
    fallos = []
    for ref in refs:
        c = cache.get(ref["hash"])
        if not c:
            fallos.append(f"sin verificar o texto cambiado: {ref['linea'][:80]}")
        elif c["estado"] != "verificada":
            fallos.append(f"{c['estado']}: {ref['linea'][:80]}")
    if fallos:
        print("CITAS SIN VERIFICAR — corre `python verificar_citas.py"
              " --verificar` (con red) y revisa:")
        for f in fallos:
            print("  ·", f)
        sys.exit(1)
    print(f"citas: {len(refs)}/{len(refs)} verificadas contra registro — OK")


if __name__ == "__main__":
    main()
