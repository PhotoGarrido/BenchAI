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

TIPOS = ("asch", "milgram", "cronica", "prision", "g2", "gfinal")


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


def iterar_registros(res: pathlib.Path, tipos=TIPOS):
    """Recorre resultados/ y produce `Registro` normalizados de los runs del
    modo estudio. No filtra pilotos: eso lo decide el consumidor (el reproceso
    quiere TODOS los crudos; un agregador querrá solo runs completos)."""
    for d in sorted(res.iterdir()):
        if not d.is_dir():
            continue
        tipo = _tipo_de_dir(d.name)
        if tipo is None or tipo not in tipos:
            continue
        for f in ficheros_crudos(d, tipo):
            for fila in _filas(tipo, f):
                yield Registro(tipo, d.name, f.name, fila,
                               _crudos_de_fila(tipo, fila, d.name))
