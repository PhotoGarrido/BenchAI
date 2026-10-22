"""Batería de alta de personalidad: todo lo que le falta a un modelo para entrar
en el cuadro público, con un solo comando (PERSONALIDAD.md §41.4).

Mide lo que falte de:
  v3     R3 (2 órdenes × 2 réplicas) y deseabilidad (2 órdenes) de las
         situaciones de O, C, E y A del banco v3
         → resultados/personalidad_p1/<m>/ y personalidad_p1_calibracion/<m>/
  I1-H   binario (2 × 2) y deseabilidad (2) de las 48 situaciones de I1-H
  I1-N   ídem de las 72 de I1-N   → resultados/personalidad_hn_finos/<m>/
con los MISMOS planes, ids, semillas, prompts, nombres, temperatura, ficheros y
manifiestos que experimento_personalidad_v3.py y
experimento_personalidad_hn_finos.py (reutiliza sus plan() y registro()).
Reanudable: salta lo ya registrado salvo ERROR_TECNICO. Con --corta, solo las
situaciones de la forma corta (personalidad_forma_corta.json, §41.1-42).

Antes de lanzar proyecta el coste: llamadas pendientes × tokens medios por
llamada del propio modelo en sus manifiestos de personalidad × tarifa
(tarifas_openrouter.json, 23-10-2026; si falta, coste_run.PRECIOS; NaN = 0 $).
Sin historial, la mediana de los modelos externos, con aviso.

Control del gasto DENTRO del proceso (§41.4): el manifiesto activo es una
subclase que suma tokens × tarifa de cada solicitud física en cuanto se
registra; antes de cada llamada se exige gasto + hilos × (coste máximo por
llamada) < tope, y si no, la llamada no se lanza y queda pendiente. No hay
procesos que buscar (nada de pgrep ni de patrones con rutas). Un id de
OpenRouter no se lanza sin --tope.

Uso (desde spike/):
  python alta_personalidad.py --modelo x-ai/grok-4.5 --corta --proyectar
  python alta_personalidad.py --modelo x-ai/grok-4.5 z-ai/glm-5.3 --proyectar --informe
  python alta_personalidad.py --modelo x-ai/grok-4.5 --corta --tope 1.50 --hilos 8
  python alta_personalidad.py --modelo z-ai/glm-5.3 --seco [--tope 0.05]   (sin red)
Después: python cuadro_publico_v3.py
"""

import argparse
import datetime
import json
import os
import pathlib
import random
import statistics
import sys
import tempfile
import threading

from dotenv import load_dotenv

AQUI = pathlib.Path(__file__).parent
load_dotenv(AQUI / ".env")

import coste_run  # noqa: E402
import experimento_personalidad_hn_finos as ef  # noqa: E402
import experimento_personalidad_v3 as ev3  # noqa: E402
import manifiesto  # noqa: E402
import parsers  # noqa: E402
import personalidad_runner  # noqa: E402
from experimento_personalidad import TEMPERATURA  # noqa: E402

RES = AQUI / "resultados"
TARIFAS = AQUI / "tarifas_openrouter.json"
FORMA_CORTA = AQUI / "personalidad_forma_corta.json"
SALIDA_INFORME = RES / "personalidad_fc"
RASGOS_V3 = ("O", "C", "E", "A")
MARGEN = 1.15
FASES = ("v3", "I1-H", "I1-N")
DIRS = {"p1": "personalidad_p1", "cal": "personalidad_p1_calibracion", "hnf": "personalidad_hn_finos"}


class TopeDeGasto(RuntimeError):
    """El tope de gasto impide lanzar la llamada (queda pendiente)."""


# ── Tarifas y tokens ────────────────────────────────────────────────────────
def _base(modelo):
    return modelo.partition("#")[0].partition("@")[0]


def es_de_pago(modelo):
    return "/" in _base(modelo)


def tarifa(modelo):
    """(USD/M entrada, USD/M salida); NaN (id plano) = tarifa plana, 0."""
    if not es_de_pago(modelo):
        return 0.0, 0.0
    t = json.loads(TARIFAS.read_text(encoding="utf-8"))["usd_por_millon"]
    if _base(modelo) in t:
        return tuple(t[_base(modelo)])
    return coste_run.precio(modelo)


def tokens_historial(modelo, raiz=RES):
    """(n, entrada media, salida media) de las solicitudes sin error del modelo en
    sus manifiestos de personalidad (v1, v3, I1); None si no hay."""
    d = modelo.replace("/", "_")
    n = tin = tout = 0
    for sub in DIRS.values():
        for f in sorted((pathlib.Path(raiz) / sub / d).glob("intento_*/solicitudes.jsonl")):
            for linea in f.open(encoding="utf-8"):
                s = json.loads(linea)
                if s.get("error") or s.get("seco"):
                    continue
                t = s.get("tokens") or {}
                n += 1
                tin += t.get("prompt") or 0
                tout += t.get("completion") or 0
    return (n, tin / n, tout / n) if n else None


def tokens_panel(raiz=RES):
    """Mediana de entrada y salida por llamada de los modelos externos con historial."""
    vals = []
    base = pathlib.Path(raiz) / DIRS["p1"]
    for d in sorted(base.iterdir()) if base.exists() else []:
        if "_" in d.name and d.is_dir():
            x = tokens_historial(d.name.replace("_", "/", 1), raiz)
            if x:
                vals.append(x)
    if not vals:
        return 250.0, 250.0
    return statistics.median(v[1] for v in vals), statistics.median(v[2] for v in vals)


def coste_llamada(modelo, raiz=RES):
    """(USD por llamada, fuente de los tokens, (entrada, salida))."""
    pin, pout = tarifa(modelo)
    h = tokens_historial(modelo, raiz)
    if h:
        tin, tout, fuente = h[1], h[2], f"historial propio ({h[0]} llamadas)"
    else:
        tin, tout = tokens_panel(raiz)
        fuente = "SIN HISTORIAL: mediana del panel externo"
    if pin is None:
        return None, fuente + "; SIN TARIFA", (tin, tout)
    return (tin * pin + tout * pout) / 1e6, fuente, (tin, tout)


# ── Plan ────────────────────────────────────────────────────────────────────
def cargar_corta(ruta=FORMA_CORTA):
    d = json.loads(pathlib.Path(ruta).read_text(encoding="utf-8"))
    return {t: set(x["items"]) for t, x in d["rasgos"].items()}


def ficheros(modelo, raiz):
    d = modelo.replace("/", "_")
    raiz = pathlib.Path(raiz)
    return {"p1": raiz / DIRS["p1"] / d / "registros.jsonl",
            "cal": raiz / DIRS["cal"] / d / "registros.jsonl",
            "hnf": raiz / DIRS["hnf"] / d / "registros.jsonl"}


def plan(modelo, corta=None, leer=(RES,)):
    """{fase: [tareas pendientes]}. leer: raíces cuyos registros cuentan como hechos
    (en --seco, la real y la temporal)."""
    sel = [s for s in json.loads(ev3.SEL.read_text(encoding="utf-8")) if s["rasgo"] in RASGOS_V3]
    ids_v3 = {s["id"] for s in sel if corta is None or s["id"] in corta[s["rasgo"]]}
    hechas = {k: set() for k in DIRS}
    for raiz in leer:
        for k, f in ficheros(modelo, raiz).items():
            hechas[k] |= ev3._hechas(f)
    nada = pathlib.Path(tempfile.gettempdir()) / "alta_personalidad_no_existe.jsonl"
    v3 = [t for t in ev3.plan(nada, nada, ev3.SEL, ids=ids_v3)
          if t["id"] not in hechas["cal" if t["destino"] == "cal" else "p1"]]
    out = {"v3": v3}
    for fase, rasgo in (("I1-H", "H"), ("I1-N", "N")):
        ts = [t for t in ef.plan(parejas=None, bi_h_completo=rasgo == "H", bi_n_completo=rasgo == "N")
              if t["instr"] == "I1" and t["rasgo"] == rasgo and t["formato"] in ("BI", "DS")
              and (corta is None or t["item"] in corta[rasgo]) and t["id"] not in hechas["hnf"]]
        random.Random(f"orden-hnf-{modelo}").shuffle(ts)  # el orden del ejecutor
        out[fase] = ts
    return out


def proyectar(modelo, corta=None, leer=(RES,)):
    p = plan(modelo, corta, leer)
    c, fuente, tok = coste_llamada(modelo, RES)   # historial: siempre el de resultados/
    n = {f: len(x) for f, x in p.items()}
    tot = sum(n.values())
    return {"modelo": modelo, "forma": "corta" if corta else "completa", "llamadas": n, "total_llamadas": tot,
            "coste_llamada": c, "tokens_llamada": tok, "fuente_tokens": fuente, "tarifa": tarifa(modelo),
            "coste": None if c is None else c * tot, "coste_margen": None if c is None else c * tot * MARGEN,
            "plan": p}


# ── Vigilante de gasto en el propio proceso ─────────────────────────────────
class Vigilante:
    """Suma el gasto de cada solicitud física registrada y decide si cabe otra."""

    def __init__(self, tope, hilos, coste_previsto):
        self.tope, self.hilos = tope, max(1, hilos)
        self.gasto = 0.0
        self.solicitudes = 0
        self.max_llamada = 3 * (coste_previsto or 0.0)   # reserva hasta que haya datos
        self.bloqueadas = 0
        self._lock = threading.Lock()

    def sumar(self, evento):
        t = evento.get("tokens") or {}
        pin, pout = tarifa(str(evento.get("modelo") or ""))
        if pin is None:
            pin, pout = 0.0, 0.0
        c = ((t.get("prompt") or 0) * pin + (t.get("completion") or 0) * pout) / 1e6
        with self._lock:
            self.gasto += c
            self.solicitudes += 1
            self.max_llamada = max(self.max_llamada, c)

    def cabe(self):
        with self._lock:
            return self.tope is None or self.gasto + self.hilos * self.max_llamada < self.tope

    def permite(self):
        ok = self.cabe()
        if not ok:
            with self._lock:
                self.bloqueadas += 1
        return ok


class ManifiestoVigilado(manifiesto.RunManifest):
    """RunManifest que, además de registrar cada solicitud física, se la cuenta al
    vigilante: el gasto se conoce en el mismo proceso que lo produce."""

    def __init__(self, outdir, args, vigilante):
        super().__init__(outdir, args)
        self.vigilante = vigilante

    def registrar(self, evento):
        super().registrar(evento)
        self.vigilante.sumar(evento)


class ModeloSeco:
    """--seco: sin red. Responde «A»/«B» con la semilla de la tarea y registra en el
    manifiesto una solicitud con los tokens medios del modelo, para que el
    vigilante funcione como en una tanda real."""

    def __init__(self, modelo, tokens):
        self.modelo, self.tokens = _base(modelo), tokens

    def sample_text(self, prompt, max_tokens=60, temperature=TEMPERATURA, seed=0):
        txt = "A" if random.Random(seed).random() < .5 else "B"
        tin, tout = (int(round(x)) for x in self.tokens)
        manifiesto.registrar({"modelo": self.modelo, "proveedor": "seco", "seco": True, "respuesta": txt,
                              "tokens": {"prompt": tin, "completion": tout, "total": tin + tout}})
        return txt


def _dir_intento(base, prefijo):
    d = base / datetime.datetime.now().strftime(f"{prefijo}%Y%m%d_%H%M%S")
    k = 2
    while d.exists():   # dos fases en el mismo segundo no comparten carpeta (§40)
        d = d.with_name(d.name.split("~")[0] + f"~{k}")
        k += 1
    return d


def ejecutar(modelo, p, raiz, vig, hilos, seco, args_manif):
    """Lanza las tres fases; devuelve {fase: (hechas, bloqueadas)}."""
    import model_factory
    total = sum(len(x) for x in p.values())
    # El límite de llamadas del harness (2.000 por defecto) no debe cortar el alta
    # completa (≈ 2.100 llamadas) y convertir lo que falte en ERROR_TECNICO
    necesarias = 2 * total + 100
    if int(os.environ.get("PSICOAI_MAX_CALLS", "2000")) < necesarias:
        os.environ["PSICOAI_MAX_CALLS"] = str(necesarias)
    tokens = coste_llamada(modelo)[2]
    llm = ModeloSeco(modelo, tokens) if seco else model_factory.build_model(dry_run=False, model_name=modelo)
    fich = ficheros(modelo, raiz)
    for f in fich.values():
        f.parent.mkdir(parents=True, exist_ok=True)
    items_sha = ef.items_sha256()
    resumen = {}
    for fase in FASES:
        tareas = p[fase]
        if not tareas:
            resumen[fase] = (0, 0)
            continue
        if not vig.cabe():   # ya en el tope: ni se abre manifiesto
            vig.bloqueadas += len(tareas)
            resumen[fase] = (0, len(tareas))
            continue
        if fase == "v3":
            outdir = _dir_intento(fich["p1"].parent, "intento_v3_")
        else:
            outdir = _dir_intento(fich["hnf"].parent, "intento_")
        m = ManifiestoVigilado(outdir, dict(args_manif, fase=fase, n_pendientes=len(tareas),
                                            version_bateria="v3" if fase == "v3" else ef.VERSION_BATERIA,
                                            items_sha256=items_sha), vig)
        manifiesto.activar_instancia(m)
        hechas = [0]
        bloqueadas_antes = vig.bloqueadas

        def hacer(t):
            if not vig.permite():
                return None   # no se lanza: queda pendiente para reanudar
            try:
                raw = llm.sample_text(t["prompt"], max_tokens=60, temperature=TEMPERATURA,
                                      seed=t["seed"] % 2**31)
            except Exception as ex:  # el fallo técnico nunca se vuelve conducta
                print(f"[alta {modelo}] error en {t['id']}: {type(ex).__name__}: {str(ex)[:120]}",
                      file=sys.stderr, flush=True)
                raw = ""
            if fase == "v3":
                return ev3.registro(t, raw, modelo, "v3")
            return ef.registro(t, raw, modelo, items_sha)

        def escribir(reg):
            if reg is None:
                return
            if fase == "v3":
                destino = fich["cal"] if reg.pop("destino") == "cal" else fich["p1"]
            else:
                destino = fich["hnf"]
            with destino.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(reg, ensure_ascii=False) + "\n")
            hechas[0] += 1

        try:
            personalidad_runner.ejecutar(tareas, hacer, escribir, f"alta {modelo}/{fase}", hilos, cada=100)
        except BaseException as e:
            m.cerrar("failed", {"exception_type": type(e).__name__})
            manifiesto.activar_instancia(None)
            raise
        bloq = vig.bloqueadas - bloqueadas_antes
        if bloq:
            m.cerrar("failed", {"exception_type": TopeDeGasto.__name__, "pendientes": bloq,
                                "gasto_estimado": round(vig.gasto, 4), "tope": vig.tope})
        else:
            m.cerrar("completed", {"gasto_estimado": round(vig.gasto, 4)})
        manifiesto.activar_instancia(None)
        resumen[fase] = (hechas[0], bloq)
    return resumen


# ── Informe de presupuesto ──────────────────────────────────────────────────
def informe(filas, saldo):
    """PRESUPUESTO_ALTA.md y presupuesto_alta.json (§41.5)."""
    import validez_personalidad as vp
    por_modelo = {}
    for x in filas:
        por_modelo.setdefault(x["modelo"], {})[x["forma"]] = x
    val = {m: vp.evaluar(m.replace("/", "_")) for m in por_modelo}
    orden = sorted(por_modelo, key=lambda m: por_modelo[m]["corta"]["coste_margen"] or 1e9)
    f = lambda x: "—" if x is None else f"{x:.2f}".replace(".", ",")  # noqa: E731
    L = ["# Presupuesto del alta de personalidad (PERSONALIDAD.md §41.5-42)", "",
         "Generado por `alta_personalidad.py --proyectar --informe`. Llamadas que FALTAN a cada modelo"
         " (lo medido en el v1 no se repite) × tokens medios por llamada de sus manifiestos de personalidad ×"
         f" tarifa de OpenRouter del 23-10-2026 (`tarifas_openrouter.json`). Margen × {f(MARGEN)}."
         f" Saldo de OpenRouter: ≈ {f(saldo)} $. Sin llamadas a modelos.", "",
         "| modelo | tokens/llamada (ent./sal.) | USD/M ent./sal. | corta: llamadas | corta: $ (margen) |"
         " completa: llamadas | completa: $ (margen) | pronóstico de validez (v1) |",
         "|---|---|---|---|---|---|---|---|"]
    acum = {"corta": 0.0, "completa": 0.0}
    for m in orden:
        c, k = por_modelo[m]["corta"], por_modelo[m]["completa"]
        acum["corta"] += c["coste_margen"] or 0
        acum["completa"] += k["coste_margen"] or 0
        vv = val[m]
        L.append(f"| {m} | {c['tokens_llamada'][0]:.0f} / {c['tokens_llamada'][1]:.0f} |"
                 f" {f(c['tarifa'][0])} / {f(c['tarifa'][1])} | {c['total_llamadas']} |"
                 f" {f(c['coste'])} ({f(c['coste_margen'])}) | {k['total_llamadas']} |"
                 f" {f(k['coste'])} ({f(k['coste_margen'])}) | {vv['nivel']}"
                 f"{' — ' + vv['motivo'] if vv['motivo'] else ''} |")
    L += [f"| **total** | | | {sum(por_modelo[m]['corta']['total_llamadas'] for m in orden)} |"
          f" {f(sum(por_modelo[m]['corta']['coste'] or 0 for m in orden))} ({f(acum['corta'])}) |"
          f" {sum(por_modelo[m]['completa']['total_llamadas'] for m in orden)} |"
          f" {f(sum(por_modelo[m]['completa']['coste'] or 0 for m in orden))} ({f(acum['completa'])}) | |", ""]
    # Qué cabe, de menor a mayor coste, con margen, en el saldo
    caben = {}
    for forma in ("corta", "completa"):
        g, dentro = 0.0, []
        for m in sorted(por_modelo, key=lambda m: por_modelo[m][forma]["coste_margen"] or 1e9):
            cm = por_modelo[m][forma]["coste_margen"] or 0
            if g + cm <= saldo:
                g += cm
                dentro.append(m)
        caben[forma] = {"modelos": dentro, "gasto_margen": g}
        L.append(f"- **Caben con la forma {forma}** (de menor a mayor coste, con margen, en {f(saldo)} $):"
                 f" {', '.join(dentro) or 'ninguno'} → {f(g)} $.")
    L += ["", "Llamadas pendientes por fase (corta / completa):", ""]
    for m in orden:
        c, k = por_modelo[m]["corta"]["llamadas"], por_modelo[m]["completa"]["llamadas"]
        L.append(f"- {m}: " + " · ".join(f"{fase} {c[fase]}/{k[fase]}" for fase in FASES))
    SALIDA_INFORME.mkdir(parents=True, exist_ok=True)
    (SALIDA_INFORME / "PRESUPUESTO_ALTA.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (SALIDA_INFORME / "presupuesto_alta.json").write_text(json.dumps(
        {"saldo": saldo, "margen": MARGEN, "tarifas": json.loads(TARIFAS.read_text(encoding="utf-8")),
         "modelos": {m: {fo: {k: v for k, v in x.items() if k != "plan"} for fo, x in d.items()}
                     for m, d in por_modelo.items()},
         "pronostico_validez": val, "caben": caben}, ensure_ascii=False, indent=1, default=float) + "\n",
        encoding="utf-8")
    print("\n".join(L))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--modelo", nargs="+", required=True, help="id del modelo (varios solo con --proyectar)")
    ap.add_argument("--corta", action="store_true", help="solo la forma corta (§41.1-42)")
    ap.add_argument("--tope", type=float, help="USD: no se lanza ninguna llamada que pueda pasarlo")
    ap.add_argument("--proyectar", action="store_true", help="solo proyecta el coste y sale")
    ap.add_argument("--informe", action="store_true",
                    help="con --proyectar: escribe PRESUPUESTO_ALTA.md con forma corta y completa")
    ap.add_argument("--saldo", type=float, default=7.21, help="saldo de OpenRouter para el informe")
    ap.add_argument("--seco", action="store_true",
                    help="sin red: modelo falso, escribe en un directorio temporal (o --raiz)")
    ap.add_argument("--raiz", type=pathlib.Path,
                    help="raíz de resultados donde se escribe (por defecto resultados/; en --seco, un temporal)")
    ap.add_argument("--hilos", type=int, default=1, help="hilos (solo sirve en OpenRouter)")
    ap.add_argument("--parcial", action="store_true",
                    help="lanza aunque la proyección con margen supere el tope (se para al llegar)")
    ap.add_argument("--humo", type=int, default=0,
                    help="solo N tareas por fase, para comprobar el camino real (exige --raiz fuera de resultados/)")
    args = ap.parse_args(argv)
    if args.humo and (args.raiz is None or args.raiz.resolve() == RES.resolve()):
        ap.error("--humo escribe solo fuera de resultados/: pasa --raiz con un directorio temporal")
    corta = cargar_corta() if args.corta else None
    if args.proyectar:
        filas = []
        for m in args.modelo:
            formas = [None, cargar_corta()] if args.informe else [corta]
            for c in formas:
                x = proyectar(m, c)
                filas.append(x)
                print(f"{m:36s} forma {x['forma']:8s} " + " · ".join(f"{f} {n}" for f, n in x["llamadas"].items())
                      + f" = {x['total_llamadas']} llamadas · {x['fuente_tokens']} · "
                      + ("SIN TARIFA" if x["coste"] is None else
                         f"{x['coste']:.3f} $ ({x['coste_margen']:.3f} $ con margen)"))
        if args.informe:
            informe(filas, args.saldo)
        return 0
    if len(args.modelo) > 1:
        ap.error("se da de alta un modelo cada vez (varios solo con --proyectar)")
    modelo = args.modelo[0]
    raiz = args.raiz or (pathlib.Path(tempfile.mkdtemp(prefix="alta_seco_")) if args.seco else RES)
    if args.seco and raiz.resolve() == RES.resolve():
        ap.error("--seco no escribe en resultados/: sus respuestas son de un modelo falso")
    leer = (RES, raiz) if args.seco and raiz != RES else (raiz,)
    x = proyectar(modelo, corta, leer)
    if args.humo:
        x["plan"] = {f: ts[:args.humo] for f, ts in x["plan"].items()}
        x["llamadas"] = {f: len(ts) for f, ts in x["plan"].items()}
        x["total_llamadas"] = sum(x["llamadas"].values())
        if x["coste_llamada"] is not None:
            x["coste"] = x["coste_llamada"] * x["total_llamadas"]
            x["coste_margen"] = x["coste"] * MARGEN
    print(f"[alta {modelo}] forma {x['forma']}: " + " · ".join(f"{f} {n}" for f, n in x["llamadas"].items())
          + f" = {x['total_llamadas']} llamadas pendientes; {x['fuente_tokens']}; "
          + ("SIN TARIFA" if x["coste"] is None else f"proyección {x['coste']:.3f} $ ({x['coste_margen']:.3f} $"
                                                       f" con margen); tope {args.tope}"), flush=True)
    if x["total_llamadas"] == 0:
        print(f"[alta {modelo}] nada pendiente: python cuadro_publico_v3.py")
        return 0
    if es_de_pago(modelo) and not args.seco:
        if args.tope is None:
            raise SystemExit(f"[alta {modelo}] es de pago (OpenRouter): hace falta --tope en USD")
        if x["coste"] is None:
            raise SystemExit(f"[alta {modelo}] sin tarifa: añádela a tarifas_openrouter.json")
        if x["coste_margen"] > args.tope and not args.parcial:
            raise SystemExit(f"[alta {modelo}] la proyección con margen ({x['coste_margen']:.3f} $) pasa del"
                             f" tope ({args.tope} $): sube el tope o usa --parcial")
    vig = Vigilante(args.tope, args.hilos, x["coste_llamada"])
    args_manif = {"modelo": modelo, "forma": x["forma"], "tope": args.tope, "hilos": args.hilos,
                  "seco": args.seco, "origen": "alta_personalidad.py (PERSONALIDAD.md §41.4)"}
    res = ejecutar(modelo, x["plan"], raiz, vig, args.hilos, args.seco, args_manif)
    bloq = sum(b for _, b in res.values())
    print(f"[alta {modelo}] " + " · ".join(f"{f} {h} hechas" + (f", {b} sin lanzar" if b else "")
                                          for f, (h, b) in res.items())
          + f" · gasto estimado {vig.gasto:.4f} $ en {vig.solicitudes} solicitudes"
          + (f" · escrito en {raiz}" if raiz != RES else ""), flush=True)
    if bloq:
        print(f"[alta {modelo}] PARADO POR EL TOPE ({args.tope} $): {bloq} llamadas pendientes; se reanuda"
              " con el mismo comando y un tope mayor.")
        return 3
    from validez_personalidad import _ultimos
    errores = sum(r.get("estado") == parsers.ERROR_TECNICO
                  for f in ficheros(modelo, raiz).values() for r in _ultimos(f))
    if errores:
        print(f"[alta {modelo}] {errores} registros con ERROR_TECNICO: relanza el mismo comando para reintentarlos.")
    print(f"[alta {modelo}] siguiente paso: python cuadro_publico_v3.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
