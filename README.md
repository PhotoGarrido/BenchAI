# 🧠 PsicoAI

**Banco de pruebas conductual de agentes LLM sobre paradigmas clásicos de psicología social, más un simulador narrativo didáctico.** Versión `v0.1.4-alpha` (research preview).

## Qué es

Cuatro productos que conviven en este repositorio, deliberadamente separados:

1. **Banco experimental** (`spike/experimento_*.py`): 6 paradigmas isomorfos y disfrazados — Asch, Milgram (±vacuna), la prisión de Stanford (P1→P2b), erosión de normas en 42 días, y el gradiente de explicitud (G1→G2→G-final) — ejecutados con harness controlado sobre 17 modelos de 10 laboratorios.
2. **Benchmark PsicoBench** ([`BENCHMARK.md`](BENCHMARK.md) + `benchmark/`): el perfil social de cada medición (modelo@snapshot@proveedor) en 6 ejes conductuales + panel interactivo (`benchmark/index.html`); tabla y datos autogenerados desde las matrices y verificados en CI.
3. **Trabajo de investigación** (`preprint/`): borrador v0.3, pre-registros congelados con enmiendas fechadas, auditoría del reproceso y erratas.
4. **Simulador narrativo** (`spike/run_spike.py` + `panel/` + `viewer/`): personajes con personalidad y memoria sobre [Concordia](https://github.com/google-deepmind/concordia), con replay reproducible y canal de pensamiento privado. Produce los `episodios/` didácticos.

## Qué NO es

- **No es evidencia sobre humanos.** Se mide conducta de modelos concretos bajo protocolos concretos; los LLM tienden a sobreestimar los efectos humanos (Ashokkumar et al., Nature 2026). Ver `RESEARCH_CARD.md`.
- **No es un ranking de calidad de modelos.** PsicoBench ordena por un índice **descriptivo** de susceptibilidad social, condicionado a protocolo, fecha y proveedor; la unidad es la versión medida, no el nombre comercial (doctrina en `BENCHMARK.md`).
- **No es un producto**: es investigación en preview, con sus errores documentados a la vista.

## Estado del proyecto (01-08-2026)

- **Confirmatorio**: cláusula de proporcionalidad sostenida en 3/4 modelos (pre-registrada); mecanismo «institucionalista» de opus-5 refutado; efecto formato-política de G1 refutado. Tres refutaciones publicadas.
- **Réplica de snapshot (M4)**: el perfil social de deepseek-v4-flash **no sobrevive** a la actualización jul→0731 conservando el nombre — el agregado se mantiene (ISS 45,5→46,0) pero la composición se redistribuye; la vacuna de contaminación sí replica (Δ −0,5 en ambos). Ver `EXPERIMENTOS.md` §M4.
- **Validación del instrumento**: parsers v2.2 (tres revisiones adversariales + reproceso de 55.545 campos con raw — 55.470 idénticos; 5.472 sin raw, 5.400 de ellos la conducta de G2 — con doble gate en CI — ver [`preprint/auditoria_reproceso.md`](preprint/auditoria_reproceso.md)); validación humana del juez **fallida según su umbral pre-registrado** (κ 0,55 < 0,8) y reportada como tal.
- **Erratas vivas**: `spike/resultados/ERRATA_prision.md`, `reproceso_erratas.json`. Los errores y sus correcciones son parte del material.

## Resultados y preprint

- Registro canónico: [`EXPERIMENTOS.md`](EXPERIMENTOS.md) · Borrador: [`preprint/preprint.md`](preprint/preprint.md) · Método/puerta de calidad: [`METODO.md`](METODO.md).
- Qué es confirmatorio y qué exploratorio está marcado en cada informe; los IC están condicionados al banco de tareas (§7 del preprint).

## Reproducibilidad

- Cada solicitud física al proveedor queda en `solicitudes.jsonl` (mensajes completos, tokens, latencia, estado final del run).
- Los datasets de cada tabla del preprint están fijados por sha256 en [`preprint/release_manifest.json`](preprint/release_manifest.json); los análisis corren con `--manifest`.
- `cd spike && python reprocesar.py --check` re-deriva los 55.545 campos con raw desde crudos sin red (55.470 idénticos); `--check-publication` exige errata para toda reclasificación. Excepción declarada: la conducta de G2 (25-07) no conservó crudos.

## Demo narrativa (sin instalar nada)

1. Abre `viewer/index.html` → **«Cargar replay.json»** → `episodios/ep01-el-centro-la-norma/replay.json`.
2. La ficha didáctica está en la carpeta del episodio; el botón «Mostrar monólogo privado generado» enseña lo que los personajes piensan y no dicen (es contenido generado, no «privacidad»: el fichero completo lo contiene; distribuye `replay.public.json` si no quieres incluirlo).

## Instalación y uso

```bash
cd spike
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-ci.txt           # herramientas de la puerta (ruff, mypy, pip-audit…)
cp .env.example .env        # credenciales de tu gateway (jamás se versionan)
python run_spike.py --dry-run --steps 2      # humo sin red
python experimento_gfinal.py --linter        # verifica simetría de brazos
python test_barrido_falso.py                 # nada ilegible se vuelve conducta
cd .. && ./verificar.sh                      # la puerta completa, un solo comando
```

Los experimentos con API se documentan en cada `experimento_*.py`; **lee `METODO.md` antes de ejecutar nada con presupuesto**.

## Estructura

| Ruta | Qué es |
|---|---|
| `spike/experimento_*.py` | harness de los 6 paradigmas (modo estudio) |
| `spike/parsers.py` + tests | instrumento de medida versionado |
| `spike/manifiesto.py`, `reprocesar.py`, `linter_contraste.py`, `release_manifest.py` | procedencia, reproceso, simetría, fijación de datasets |
| `spike/resultados/` | crudos, informes, erratas, κ (CC BY 4.0) |
| `BENCHMARK.md`, `benchmark/` | PsicoBench: doctrina, tabla autogenerada, panel y datos (`generar_benchmark.py --check` en CI) |
| `preprint/` | manuscrito, auditoría, manifest |
| `panel/`, `viewer/`, `episodios/`, `schemas/` | simulador narrativo y sus contratos |
| `METODO.md`, `FICHA_RIESGO_ESTEREOTIPOS.md`, `RESEARCH_CARD.md` | contratos de método, riesgo y alcance |

## Limitaciones

Contaminación en techo (los modelos reconocen los paradigmas; medida y reportada), IC condicionados al banco de tareas, 9 cadenas/celda en el confirmatorio (recorte pre-registrado), material íntegramente en español, un solo codificador humano. Lista completa: preprint §7.

## Licencias y citación

Código **Apache-2.0** (`LICENSE`) · datos, replays y preprint **CC BY 4.0** (`LICENSE-DATOS.md`) · citar con `CITATION.cff` · seguridad: `SECURITY.md` · contribuir: `CONTRIBUTING.md`.
