"""Adjudicación firmada de discrepancias entre jueces.

Cuando dos juicios independientes sobre el MISMO registro no coinciden
(parser vs juez LLM, juez vs humano, dos rúbricas), ninguna regla decide en
silencio: la discrepancia queda registrada y a la espera de una decisión
investigadora **firmada** (decisión + razón + quién + cuándo). Contrato:

  - Un registro con discrepancia PENDIENTE cuenta como INVALIDA en los
    análisis (missingness, jamás conducta): esperar no fabrica datos.
  - Resolver exige razón; sin razón no hay resolución.
  - Una resolución no se re-escribe: una corrección es una entrada nueva
    con `sustituye_a` (mismo principio que las erratas de reproceso).
  - `--check` sale en rojo si hay pendientes: la puerta de publicación
    no cierra con discrepancias sin adjudicar.

Ficheros (JSONL, append-only salvo el retirado de pendientes):
  resultados/adjudicacion/pendientes.jsonl
  resultados/adjudicacion/resueltas.jsonl

Uso:
  python adjudicacion.py --listar
  python adjudicacion.py --resolver ID --decision VALOR --razon "..." \
      [--decisor nombre]
  python adjudicacion.py --check          # puerta: rojo si hay pendientes
"""

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import sys
import tempfile

AQUI = pathlib.Path(__file__).parent
DIR_DEFECTO = AQUI / "resultados" / "adjudicacion"


def _id(experimento, registro, medida):
    clave = f"{experimento}|{registro}|{medida}"
    return hashlib.sha1(clave.encode("utf-8")).hexdigest()[:12]


def _leer(fichero):
    if not fichero.exists():
        return {}
    filas = [json.loads(l) for l in fichero.read_text(encoding="utf-8")
             .splitlines() if l.strip()]
    return {f["id"]: f for f in filas}


def _escribir_atomico(fichero, filas):
    fichero.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=fichero.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        for fila in filas:
            f.write(json.dumps(fila, ensure_ascii=False) + "\n")
    os.replace(tmp, fichero)


def _anadir(fichero, fila):
    fichero.parent.mkdir(parents=True, exist_ok=True)
    with fichero.open("a", encoding="utf-8") as f:
        f.write(json.dumps(fila, ensure_ascii=False) + "\n")


def cargar(directorio=None):
    d = pathlib.Path(directorio or DIR_DEFECTO)
    return _leer(d / "pendientes.jsonl"), _leer(d / "resueltas.jsonl")


def registrar(experimento, registro, medida, juicio_a, juicio_b,
              contexto="", directorio=None):
    """Registra una discrepancia (idempotente: mismo id no se duplica ni
    reabre una ya resuelta). Devuelve el id."""
    d = pathlib.Path(directorio or DIR_DEFECTO)
    ident = _id(experimento, registro, medida)
    pendientes, resueltas = cargar(d)
    if ident in pendientes or ident in resueltas:
        return ident
    _anadir(d / "pendientes.jsonl", {
        "id": ident, "experimento": experimento, "registro": registro,
        "medida": medida, "juicio_a": juicio_a, "juicio_b": juicio_b,
        "contexto": contexto,
        "fecha": datetime.datetime.now().isoformat(timespec="seconds"),
    })
    return ident


def resolucion(experimento, registro, medida, directorio=None):
    """La resolución firmada VIGENTE de un registro, o None si no la hay
    (los análisis deben tratar el None de una pendiente como INVALIDA).
    Vigente = la última entrada de ese registro no retirada por una
    corrección posterior (`sustituye_a`)."""
    _, resueltas = cargar(directorio)
    sustituidas = {f.get("sustituye_a") for f in resueltas.values()}
    candidatas = [f for f in resueltas.values()
                  if (f["experimento"], f["registro"], f["medida"])
                  == (experimento, registro, medida)
                  and f["id"] not in sustituidas and "decision" in f]
    return candidatas[-1] if candidatas else None


def resolver(ident, decision, razon, decisor, directorio=None):
    """Adjudica una pendiente. Exige razón no vacía; no re-resuelve."""
    d = pathlib.Path(directorio or DIR_DEFECTO)
    if not (razon or "").strip():
        raise ValueError("resolver exige una razón firmada (--razon)")
    pendientes, resueltas = cargar(d)
    if ident in resueltas:
        raise ValueError(f"{ident} ya está resuelta; una corrección es una"
                         " entrada nueva con sustituye_a, no una re-escritura")
    if ident not in pendientes:
        raise ValueError(f"{ident} no está pendiente")
    fila = dict(pendientes[ident], decision=decision, razon=razon.strip(),
                decisor=decisor,
                fecha_resolucion=datetime.datetime.now()
                .isoformat(timespec="seconds"))
    _anadir(d / "resueltas.jsonl", fila)
    restantes = [f for i, f in pendientes.items() if i != ident]
    _escribir_atomico(d / "pendientes.jsonl", restantes)
    return fila


def check(directorio=None):
    """Nº de pendientes (la puerta debe exigir 0)."""
    pendientes, _ = cargar(directorio)
    return len(pendientes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--listar", action="store_true")
    parser.add_argument("--resolver", metavar="ID")
    parser.add_argument("--decision")
    parser.add_argument("--razon")
    parser.add_argument("--decisor", default=os.environ.get("USER", "?"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        n = check()
        if n:
            print(f"ADJUDICACION PENDIENTE: {n} discrepancia(s) sin decisión"
                  " firmada — la puerta de publicación no cierra así.")
            sys.exit(1)
        print("adjudicación: 0 pendientes — OK")
        return
    if args.resolver:
        fila = resolver(args.resolver, args.decision, args.razon or "",
                        args.decisor)
        print(f"resuelta {fila['id']} → {fila['decision']}"
              f" ({fila['decisor']}, {fila['fecha_resolucion']})")
        return
    pendientes, resueltas = cargar()
    print(f"pendientes: {len(pendientes)} · resueltas: {len(resueltas)}")
    for f in pendientes.values():
        print(f"  {f['id']}  {f['experimento']}/{f['registro']}/{f['medida']}"
              f"  A={f['juicio_a']}  B={f['juicio_b']}")


if __name__ == "__main__":
    main()
