"""Exporta un SimulationLog de Concordia al formato replay.json del visor.

El visor (viewer/index.html) es agnóstico de Concordia: solo entiende un
formato plano de eventos (narrador, dialogo, accion, pensamiento, paso).
Este módulo hace el mapeo. La convención de habla de Concordia es
`Nombre -- "texto"`; lo que no encaje como diálogo o acción de un agente
se atribuye al narrador.

Uso standalone:  python export_replay.py runs/<id>/log.json
Uso integrado:   run_spike.py lo llama tras cada sesión.
"""

import json
import os
import pathlib
import re
import sys

# Paleta fija: color estable por orden de aparición del agente.
COLORES = ["#e4572e", "#4d9de0", "#3bb273", "#b86fc6", "#f2a65a", "#e26d8f"]

_DIALOGO_RE = re.compile(r'^\s*(?P<nombre>[^\-"\n]{2,60}?)\s+--\s+["“](?P<texto>.+?)["”]\s*$', re.S)
_EVENT_PREFIX_RE = re.compile(r"^Step \d+ .*? --- ", re.S)

# Movimiento narrado → spot del visor. Verbo de desplazamiento seguido (a poca
# distancia) de un lugar conocido de la sala.
_MOV_RE = re.compile(
    r"(?:se acerca|se dirige|se encamina|camina|anda|va|avanza|vuelve|regresa"
    r"|se aparta|se retira|se coloca|se sienta|se planta|se levanta y va"
    r"|cruza|se mueve|se sitúa)"
    r"[^.;]{0,50}?"
    r"\b(tabl[oó]n|ventana|mesa|sof[aá]|puerta|centro|habitaci[oó]n|pasillo|cocina|salir de la sala)",
    re.I,
)
_SPOT = {
    "tablon": "tablon", "tablón": "tablon", "ventana": "ventana",
    "mesa": "mesa_s", "sofa": "sofa", "sofá": "sofa",
    "puerta": "puerta", "centro": "centro",
    # Lugares que el GM inventa fuera de la sala → visualmente, la puerta.
    "habitación": "puerta", "habitacion": "puerta", "pasillo": "puerta",
    "cocina": "puerta", "salir de la sala": "puerta",
}
# Hallazgo 21: el mapeo anterior era silencioso. Cuando el lugar narrado no
# existe en la sala, además del movimiento a la puerta se emite un evento
# constraint_violation auditable (rule=unknown_location, texto crudo).
_LUGARES_DESCONOCIDOS = {"habitación", "habitacion", "pasillo", "cocina",
                         "salir de la sala"}


_MOV_PERSONA_RE = re.compile(
    r"(?:se acerca|se aproxima|se dirige|camina|avanza|se planta|se coloca)"
    r"[^.;]{0,45}?\b(?:a|hacia|junto a|frente a|al lado de)\s+"
    r"([A-ZÁÉÍÓÚÑ][\wáéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][\wáéíóúñ]+)?)",
    re.I,
)


def _quien_actua(texto: str, nombres: list[str], agente: str | None, pos: int):
    if agente:
        return agente
    previos = [(texto.rfind(n, 0, pos), n) for n in nombres]
    previos = [(i, n) for i, n in previos if i != -1]
    return max(previos)[1] if previos else None


def _detectar_movimiento(texto: str, nombres: list[str], agente: str | None):
    """Detecta desplazamientos narrados.

    Devuelve (nombre_agente | None, destino | None, info) donde destino es
    {"spot": ...} para lugares de la sala o {"haciaAgente": nombre} al
    acercarse a alguien, e info trae la trazabilidad: "atribucion" ("exacta"
    si el actor venía dado por el evento, "regex" si se infirió del texto;
    hallazgo 22) y "raw_location" cuando el GM narró un lugar que no existe
    en la sala (hallazgo 21). Devuelve None si no hay movimiento.
    """
    m = _MOV_RE.search(texto)
    if m:
        lugar = m.group(1).lower()
        quien = _quien_actua(texto, nombres, agente, m.start())
        info = {"atribucion": "exacta" if agente else "regex"}
        if lugar in _LUGARES_DESCONOCIDOS:
            info["raw_location"] = m.group(1)
        if quien or "raw_location" in info:
            return quien, ({"spot": _SPOT[lugar]} if quien else None), info
    m = _MOV_PERSONA_RE.search(texto)
    if m:
        candidato = m.group(1)
        objetivos = [n for n in nombres
                     if n.startswith(candidato) or candidato in n]
        quien = _quien_actua(texto, nombres, agente, m.start())
        # Hallazgo 22: si el candidato casa con varios nombres, NO se adivina
        # el objetivo — mejor ningún movimiento que uno inventado.
        if len(objetivos) == 1 and quien and objetivos[0] != quien:
            return quien, {"haciaAgente": objetivos[0]}, {
                "atribucion": "exacta" if agente else "regex"}
    return None


def _eventos_movimiento(texto_evento, nombres, actor, id_por_nombre):
    """Eventos derivados del movimiento narrado, listos para el replay:
    constraint_violation si el GM inventó un lugar + movimiento del visor."""
    det = _detectar_movimiento(texto_evento, nombres, actor)
    if det is None:
        return []
    quien, destino, info = det
    out = []
    if "raw_location" in info:
        out.append({
            "tipo": "constraint_violation",
            "rule": "unknown_location",
            "raw_location": info["raw_location"],
            "agente": id_por_nombre.get(quien),
        })
    if quien in id_por_nombre and destino:
        if "haciaAgente" in destino:
            destino = dict(destino,
                           haciaAgente=id_por_nombre.get(destino["haciaAgente"]))
            if not destino["haciaAgente"]:
                return out
        out.append({"tipo": "movimiento", "agente": id_por_nombre[quien],
                    "atribucion": info["atribucion"], **destino})
    return out


def _resolver_ref(store: dict, v):
    """Resuelve un valor del log que puede ser texto directo o {"_ref": hash}."""
    if isinstance(v, dict) and "_ref" in v:
        return store.get(v["_ref"], "")
    return v if isinstance(v, str) else ""


def _pensamiento_de(entry: dict, store: dict) -> str | None:
    """Extrae el monólogo interno (canal privado) de una entrada de acción."""
    dd = entry.get("deduplicated_data") or {}
    if isinstance(dd.get("value"), dict):  # a veces viene anidado en {key, value}
        dd = dd["value"]
    comp = dd.get("PensamientoPrivado") or {}
    texto = _resolver_ref(store, comp.get("State")).strip()
    if not texto:
        return None
    nombre = entry.get("entity_name", "")
    texto = re.sub(r"^\s*" + re.escape(nombre) + r"\s+piensa:\s*", "", texto)
    return texto.strip() or None


def _limpiar_evento(summary: str) -> str:
    texto = _EVENT_PREFIX_RE.sub("", summary or "").strip()
    texto = re.sub(r"^Event:\s*", "", texto).strip()
    return texto


def _clasificar(texto: str, nombres: list[str]) -> dict | None:
    """Convierte el texto de un evento resuelto en un evento de replay.

    Hallazgo 22: la atribución de actor es EXPLÍCITA en cada evento
    atribuido: "exacta" (el hablante coincide con un nombre conocido o el
    texto empieza por él), "regex" (el nombre se extrajo por patrón, con
    texto extra alrededor) o "ambigua" (cero o varios candidatos): entonces
    NO se adivina — agente None y el texto crudo se conserva.
    """
    if not texto:
        return None
    m = _DIALOGO_RE.match(texto)
    if m:
        hablante = m.group("nombre").strip()
        candidatos = [n for n in nombres if n in hablante]
        if len(candidatos) == 1:
            return {"tipo": "dialogo", "agente": candidatos[0],
                    "atribucion": ("exacta" if hablante == candidatos[0]
                                   else "regex"),
                    "texto": m.group("texto").strip()}
        # Varios nombres casan (o ninguno conocido): no se adivina.
        return {"tipo": "dialogo", "agente": None, "atribucion": "ambigua",
                "texto": m.group("texto").strip(), "texto_crudo": texto}
    candidatos = [n for n in nombres if texto.startswith(n)]
    if candidatos:
        # Con startswith todos los candidatos son prefijos entre sí: el más
        # largo es el más específico, no una adivinanza.
        n = max(candidatos, key=len)
        resto = texto[len(n):].strip(" \t,;:") or texto
        return {"tipo": "accion", "agente": n, "atribucion": "exacta",
                "texto": resto}
    return {"tipo": "narrador", "texto": texto}


def build_replay(log_dict: dict, meta: dict) -> dict:
    entries = log_dict.get("entries", [])
    nombres = meta.get("agentes") or sorted(
        {e.get("entity_name") for e in entries if e.get("entry_type") == "entity"}
    )

    agentes = [
        {
            "id": f"a{i}",
            "nombre": nombre,
            "rol": "",
            "color": COLORES[i % len(COLORES)],
        }
        for i, nombre in enumerate(nombres)
    ]
    id_por_nombre = {a["nombre"]: a["id"] for a in agentes}

    store = log_dict.get("content_store", {})
    eventos: list[dict] = [{"tipo": "narrador", "texto": meta.get("premisa", "")}]
    paso_actual = None
    for e in sorted(entries, key=lambda x: (x.get("step", 0))):
        if e.get("component_name") != "entity_action":
            continue
        paso = e.get("step")
        if paso != paso_actual:
            paso_actual = paso
            eventos.append({"tipo": "paso", "n": paso})
        # Canal privado: el pensamiento precede a la conducta observable.
        pensamiento = _pensamiento_de(e, store)
        if pensamiento and e.get("entity_name") in id_por_nombre:
            eventos.append({
                "tipo": "pensamiento",
                "agente": id_por_nombre[e["entity_name"]],
                "atribucion": "exacta",  # viene del entity_name del log
                "texto": pensamiento,
                "canal": "privado",
                "_paso": paso,
            })
        texto_evento = _limpiar_evento(e.get("summary", ""))
        ev = _clasificar(texto_evento, nombres)
        if ev is None:
            continue
        # Movimiento físico narrado → evento estructurado antes de la acción,
        # para que el visor desplace al personaje y luego muestre el bocadillo
        # (más constraint_violation si el lugar no existe, hallazgo 21).
        actor = ev.get("agente") if ev.get("agente") in nombres else None
        eventos.extend(
            _eventos_movimiento(texto_evento, nombres, actor, id_por_nombre))
        if ev.get("agente") is not None:
            ev["agente"] = id_por_nombre[ev["agente"]]
        eventos.append(ev)

    # Fallback (motor simultáneo): sus summaries vienen vacíos ("Step N gm") y
    # los eventos resueltos viven en game_master_memories como
    # "[observation] [event] Event: ...". Si el bucle principal no produjo
    # conducta observable, reconstruimos desde ahí.
    hay_conducta = any(e["tipo"] in ("dialogo", "accion") for e in eventos)
    if not hay_conducta:
        gm_eventos = []
        for m in log_dict.get("game_master_memories") or []:
            if not isinstance(m, str) or "[putative_event]" in m:
                continue
            texto = re.sub(r"^\[observation\]\s*", "", m)
            if not texto.startswith("[event]"):
                continue
            texto = re.sub(r"^\[event\]\s*(Event:\s*)?", "", texto).strip()
            if texto and not meta.get("premisa", "").startswith(texto[:60]):
                gm_eventos.append(texto)
        pensamientos_por_paso = {}
        for e in eventos:
            if e["tipo"] == "pensamiento":
                pensamientos_por_paso.setdefault(e.get("_paso", 0), []).append(e)
        eventos = [{"tipo": "narrador", "texto": meta.get("premisa", "")}]
        for i, texto in enumerate(gm_eventos, start=1):
            eventos.append({"tipo": "paso", "n": i})
            for p in pensamientos_por_paso.get(i, []):
                eventos.append(p)
            ev = _clasificar(texto, nombres)
            if ev is None:
                continue
            actor = ev.get("agente") if ev.get("agente") in nombres else None
            eventos.extend(
                _eventos_movimiento(texto, nombres, actor, id_por_nombre))
            if ev.get("agente") is not None:
                ev["agente"] = id_por_nombre[ev["agente"]]
            eventos.append(ev)
    # limpia la marca interna de paso de los pensamientos
    for e in eventos:
        e.pop("_paso", None)

    return {
        "version": 1,
        "meta": {
            "titulo": meta.get("run_id", "Sesión PsicoAI"),
            "descripcion": meta.get("premisa", ""),
            "fecha": meta.get("run_id", ""),
            "fuente": "concordia",
        },
        "agentes": agentes,
        "eventos": eventos,
    }


def escribir_atomico(path: pathlib.Path, texto: str) -> None:
    """Escritura atómica: X.tmp + os.replace → nunca queda un X a medias.

    Un run interrumpido se distingue por el status del manifest_run.json
    (running/failed), no por un JSON truncado."""
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(texto, encoding="utf-8")
    os.replace(tmp, path)


def replay_publico(replay: dict) -> dict:
    """Copia publicable del replay: los eventos del canal privado (tipo
    "pensamiento", canal "privado" — el monólogo interno de los agentes) se
    ELIMINAN físicamente del JSON, no se ocultan (hallazgo 23)."""
    publico = dict(replay)
    publico["eventos"] = [
        e for e in replay.get("eventos", [])
        if e.get("tipo") != "pensamiento" and e.get("canal") != "privado"]
    return publico


def exportar(log_path: pathlib.Path) -> pathlib.Path:
    log_dict = json.loads(log_path.read_text(encoding="utf-8"))
    meta_path = log_path.parent / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    replay = build_replay(log_dict, meta)
    texto_full = json.dumps(replay, ensure_ascii=False, indent=2)
    texto_public = json.dumps(replay_publico(replay), ensure_ascii=False,
                              indent=2)
    # Hallazgo 23: el par full/public es el contrato nuevo. replay.json se
    # mantiene como alias byte a byte del full porque es el nombre que carga
    # el visor actual (viewer/index.html) — no se rompe nada.
    for nombre, texto in (("replay.full.json", texto_full),
                          ("replay.public.json", texto_public),
                          ("replay.json", texto_full)):
        escribir_atomico(log_path.parent / nombre, texto)
    return log_path.parent / "replay.json"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("uso: python export_replay.py runs/<id>/log.json")
    destino = exportar(pathlib.Path(sys.argv[1]))
    print(f"Replay exportado: {destino}")
