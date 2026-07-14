# 🧠 PsicoAI

**Laboratorio didáctico de psicología social con agentes de IA.** Personajes con personalidad (Big Five), demografía y memoria viven situaciones de presión social simuladas sobre [Concordia](https://github.com/google-deepmind/concordia) (DeepMind); cada sesión queda guardada y se reproduce en un visor tipo AI Town — **incluyendo lo que los personajes piensan y no dicen**. La distancia entre ambas cosas es la psicología social, hecha visible.

## Ver el Episodio 1 ahora (sin instalar nada)

1. Abre `viewer/index.html` en el navegador.
2. Botón **«Cargar replay.json»** → `episodios/ep01-el-centro-la-norma/replay.json`.
3. Lee la [ficha del episodio](episodios/ep01-el-centro-la-norma/ficha.md) y prueba el botón 💭: la escena con y sin pensamientos son dos historias distintas.

## Las piezas

| Carpeta | Qué es |
|---|---|
| `panel/` | **Diseñador de escenarios**: situación, protagonistas (Big Five + demografía + trasfondo), población generada por reglas con semilla, variantes «¿y si…?». Exporta `escenario.json`. |
| `spike/` | **El motor**: Concordia 2.4 + NaN (endpoint OpenAI-compatible), personas ricas, canal privado de pensamientos, GM situado con acciones físicas, escalado multi-agente. `python run_spike.py --config escenario.json` |
| `viewer/` | **Visor de replays**: sala 2D, bocadillos de diálogo/pensamiento/acción, movimiento, timeline, feed clicable. HTML autocontenido. |
| `episodios/` | **Sesiones curadas** con ficha didáctica. |
| [PROPUESTA.md](PROPUESTA.md) | El documento de diseño: arquitectura, regla de los dos canales, mediciones de coste/escala, fases. |

## Correr una simulación propia

```bash
cd spike
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # rellenar credenciales de NaN
python run_spike.py --steps 8                             # escenario integrado
python run_spike.py --config episodio_el_centro.json \
    --engine simultaneo --max-poblacion 6                 # el Episodio 1
```

## Principios

- **Replay, no directo**: la simulación es lenta y cara; el replay es un fichero que se comparte y se re-visualiza.
- **Dos canales**: los pensamientos nunca son visibles para otros agentes ni entran en los análisis por defecto — en un experimento real no habría acceso a ellos.
- **Curado ≠ guionizado**: toda la conducta es emergente; la curaduría selecciona y explica, nunca reescribe.
- **Esto es conducta de modelos de lenguaje en roles, no evidencia sobre humanos.**
