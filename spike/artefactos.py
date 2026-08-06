"""Contrato unificado de artefactos del modo estudio.

Motivación (PLAN_MEJORA Fase 0.5): cada experimento nombra sus crudos a su
manera — `registros.jsonl` (asch, crónica), `sesiones.jsonl` (milgram, con los
registros ANIDADOS por sesión), `registros_<marco>.jsonl` (prisión, mezclando
filas de supervisor e interno), `registros_<modelo>.jsonl` (g2). Esa
heterogeneidad creó un punto ciego real: el detector de pilotos no miraba
`sesiones.jsonl` y un humo de milgram podía suplantar a un run completo
(barrido 25-07). Este módulo es la FUENTE ÚNICA del mapa de artefactos: quien
recorra resultados/ (reproceso, validación, agregadores futuros) debe iterar
con `iterar_registros`, no reimplementar el layout.

Cada registro se entrega normalizado como (tipo, fila, crudos), donde `crudos`
es la lista de (campo_raw, campo_decision, reparse) aplicable a esa fila:
`reparse(raw)` devuelve un `parsers.Resultado` con la lógica ACTUAL. Nota de
alcance: los campos raw históricos están truncados (120-200 chars según
experimento; en g2 completos) — suficiente para respuestas de una palabra,
y el reproceso lo declara en su salida.
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass, field
from typing import Callable

import parsers

TIPOS = ("asch", "milgram", "cronica", "prision", "g2", "gfinal",
         "denuncia", "venalidad", "sicofancia", "sicofancia-op")

# Contenedores de runs: directorios que AGRUPAN runs en vez de ser un run.
# Hasta la auditoría R4 el recorrido solo miraba el primer nivel de
# resultados/, así que todo el arco N (que vive en carteras) y las baterías
# eran invisibles al reproceso — un punto ciego del mismo tipo que el de
# `sesiones.jsonl` que motivó este módulo.
CONTENEDORES = ("cartera_", "bateria_", "eportador_")

# Espejo de experimento_denuncia.OPCIONES: este módulo no puede importar los
# harness (arrastran concordia). `test_barrido_falso` verifica que ambas
# copias coinciden.
OPCIONES_DENUNCIA = ["CALLO", "COMENTO", "DENUNCIO"]


@dataclass
class Crudo:
    """Un campo re-parseable de una fila: raw almacenado, decisión almacenada
    y parser actual con el que reprocesarlo."""
    campo_raw: str
    campo_decision: str
    reparse: Callable[[str], parsers.Resultado]
    etiqueta: str = ""


@dataclass
class Registro:
    tipo: str
    directorio: str
    fichero: str
    fila: dict
    crudos: list[Crudo] = field(default_factory=list)


def _tipo_de_dir(nombre: str) -> str | None:
    """Tipo de experimento por prefijo del directorio de resultados; None si
    el directorio no es un run del modo estudio (baterías, a4, etc.)."""
    for t in TIPOS:
        if nombre.startswith(t + "_"):
            return t
    return None


def _es_v2(nombre_dir: str) -> bool:
    return "_v2_" in nombre_dir


def _crudos_de_fila(tipo: str, fila: dict, nombre_dir: str) -> list[Crudo]:
    if tipo == "asch":
        cs = [Crudo("publica_raw", "publica",
                    lambda r: parsers.parsear_letra(r), "pública")]
        if fila.get("privada_raw") is not None:
            cs.append(Crudo("privada_raw", "privada",
                            lambda r: parsers.parsear_letra(r), "privada"))
        return cs
    if tipo == "milgram":
        return [Crudo("publica_raw", "decision",
                      lambda r: parsers.parsear_milgram(r), "decisión"),
                Crudo("privada_raw", "privada_justa",
                      lambda r: parsers.parsear_sino(r), "sonda justa")]
    if tipo == "cronica":
        v2 = _es_v2(nombre_dir)

        def _reparse_cronica(r: str, v2: bool = v2) -> parsers.Resultado:
            return parsers.parsear_cronica(r, v2=v2)
        return [Crudo("raw", "decision", _reparse_cronica, "decisión")]
    if tipo == "prision":
        if "supervisor" in fila:
            return [Crudo("raw", "nivel",
                          lambda r: parsers.parsear_nivel(r), "nivel")]
        if "interno" in fila:
            return [Crudo("raw", "respuesta",
                          lambda r: parsers.parsear_interno(r), "interno")]
        return []
    if tipo in ("g2", "gfinal"):
        return [Crudo("raw_publico", "nivel",
                      lambda r: parsers.parsear_nivel(r), "nivel"),
                Crudo("raw_justo", "cree_justo",
                      lambda r: parsers.parsear_sino(r), "sonda justa")]
    # ── Arco N (auditoría R4): los cuatro experimentos nuevos entran al
    # perímetro de reproceso. Campos verificados contra cada harness.
    if tipo == "denuncia":
        return [Crudo("publica_raw", "decision",
                      lambda r: parsers.parsear_eleccion(r, OPCIONES_DENUNCIA),
                      "decisión"),
                Crudo("privada_raw", "grave_privado",
                      lambda r: parsers.parsear_sino(r), "sonda grave")]
    if tipo == "venalidad":
        return [Crudo("publica_raw", "eleccion",
                      lambda r: parsers.parsear_letra(r, n_opciones=2),
                      "elección"),
                Crudo("privada_raw", "merece_privado",
                      lambda r: parsers.parsear_sino(r), "sonda merece")]
    if tipo == "sicofancia":
        cs = [Crudo("publica_raw", "publica",
                    lambda r: parsers.parsear_letra(r), "pública")]
        # El post solo existe si hubo insistencia; la privada solo fuera del
        # brazo de control.
        if fila.get("post_raw"):
            cs.append(Crudo("post_raw", "post_insistencia",
                            lambda r: parsers.parsear_letra(r),
                            "post-insistencia"))
        if fila.get("privada_raw"):
            cs.append(Crudo("privada_raw", "privada",
                            lambda r: parsers.parsear_letra(r), "privada"))
        return cs
    if tipo == "sicofancia-op":
        cs = [Crudo("inicial_raw", "inicial",
                    lambda r: parsers.parsear_letra(r, n_opciones=2),
                    "inicial")]
        if fila.get("final_raw"):
            cs.append(Crudo("final_raw", "final",
                            lambda r: parsers.parsear_letra(r, n_opciones=2),
                            "final"))
        if fila.get("privada_raw"):
            cs.append(Crudo("privada_raw", "privada",
                            lambda r: parsers.parsear_letra(r, n_opciones=2),
                            "privada"))
        return cs
    return []


def _filas(tipo: str, fichero: pathlib.Path):
    """Aplana el layout de cada experimento a filas homogéneas."""
    for linea in fichero.open(encoding="utf-8"):
        linea = linea.strip()
        if not linea:
            continue
        fila = json.loads(linea)
        if tipo == "milgram":
            # sesiones.jsonl: 1 línea por SESIÓN con los registros anidados.
            for r in fila.get("registros", []):
                yield r
        else:
            yield fila


def ficheros_crudos(directorio: pathlib.Path, tipo: str) -> list[pathlib.Path]:
    """Los .jsonl de conducta de un run. ÚNICO lugar donde vive el layout —
    incluye sesiones.jsonl (el punto ciego del detector de pilotos)."""
    if tipo == "milgram":
        return sorted(directorio.glob("sesiones.jsonl"))
    if tipo in ("prision", "g2", "gfinal"):
        return sorted(directorio.glob("registros_*.jsonl"))
    return sorted(directorio.glob("registros.jsonl"))


def _en_vuelo(d: pathlib.Path) -> bool:
    """¿El run sigue ejecutándose? Sus crudos están a medio escribir, así que
    incluirlo haría que el golden-file del reproceso dependiera del instante
    de la ejecución. Un run sin manifiesto (histórico, anterior a
    `RunManifest`) se considera terminado."""
    f = d / "manifest_run.json"
    if not f.is_file():
        return False
    try:
        estado = json.loads(f.read_text(encoding="utf-8")).get("status")
    except (OSError, ValueError):
        return False
    return estado == "running"


def dirs_de_runs(res: pathlib.Path):
    """Directorios de run bajo `res`: el primer nivel, y UN nivel dentro de
    los contenedores (carteras, baterías). Los runs en vuelo se omiten."""
    for d in sorted(res.iterdir()):
        if not d.is_dir():
            continue
        candidatos = ([s for s in sorted(d.iterdir()) if s.is_dir()]
                      if any(d.name.startswith(c) for c in CONTENEDORES)
                      else [d])
        for c in candidatos:
            if not _en_vuelo(c):
                yield c


def iterar_registros(res: pathlib.Path, tipos=TIPOS):
    """Recorre resultados/ y produce `Registro` normalizados de los runs del
    modo estudio. No filtra pilotos: eso lo decide el consumidor (el reproceso
    quiere TODOS los crudos; un agregador querrá solo runs completos)."""
    for d in dirs_de_runs(res):
        tipo = _tipo_de_dir(d.name)
        if tipo is None or tipo not in tipos:
            continue
        # Ruta relativa: dos carteras pueden tener runs homónimos, y para los
        # runs de primer nivel coincide con el nombre de siempre (el baseline
        # histórico no se mueve).
        etiqueta = str(d.relative_to(res))
        for f in ficheros_crudos(d, tipo):
            for fila in _filas(tipo, f):
                yield Registro(tipo, etiqueta, f.name, fila,
                               _crudos_de_fila(tipo, fila, d.name))
