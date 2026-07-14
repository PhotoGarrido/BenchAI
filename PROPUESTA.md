# PsicoAI — Propuesta de proyecto (v2)

*Simulaciones de psicología social con agentes de IA que se pueden **ver**: cada sesión queda guardada y se reproduce en un visor tipo AI Town — incluyendo lo que los personajes piensan y no dicen. Didáctico primero; el rigor científico existe en la arquitectura pero es opcional.*

Fecha: 2026-07-13 · Estado: **F0 (spike) y prototipo del visor ya funcionando** — ver §10 para probarlo ahora mismo.

---

## 1. La idea en una frase

Cada escenario de PsicoAI es un **episodio observable**: agentes LLM con personalidad, objetivos y memoria viven una situación de presión social —una norma injusta, una mayoría que se equivoca, una autoridad que aprieta— y cualquiera puede reproducir la sesión como quien ve un capítulo, con una ventaja que ningún documental sobre humanos tendrá jamás: **se ven los pensamientos privados** (💭) además de lo que se dice en voz alta. La distancia entre ambos *es* la psicología social, hecha visible.

Principio rector tras el giro de orientación: **didáctico > académico**. El producto central es que alguien vea un episodio y entienda un fenómeno (conformidad, obediencia, coaliciones), no el paper. El aparato experimental —condiciones, N repeticiones, métricas, control de contaminación— queda en la arquitectura como **"modo estudio" opt-in** para cuando queramos afirmar algo con datos (F4, §8).

## 2. Decisión de arquitectura clave: replay, no directo

La visualización **nunca se acopla en vivo a la simulación**. El flujo es:

```
Concordia (headless)  →  log estructurado     →  exportador        →  visor web
simula y piensa          runs/<id>/log.json      replay.json           viewer/index.html
(minutos, LLM)           (dato primario)         (formato del visor)   (fluido, 60 fps)
```

Por qué replay gana a "en directo":
- **Ritmo**: un paso de simulación puede tardar 10–60 s (varias llamadas LLM); un replay se ve fluido y a la velocidad que elijas (0.5×–4×).
- **Compartible**: un episodio es un fichero `replay.json` — se manda por correo, se cuelga en una web, se abre en el visor y ya.
- **Re-visualizable**: cada mejora del visor embellece retroactivamente todas las sesiones ya guardadas.
- **Robusto**: si la simulación casca en el paso 37, los 36 anteriores están guardados igualmente.

La persistencia viene de serie (verificado ejecutándolo): `play()` en Concordia 2.4 devuelve un `SimulationLog` con entradas por paso/entidad, memorias por agente y export a JSON/HTML.

## 3. Lo ya construido

| Pieza | Fichero | Estado |
|---|---|---|
| Simulación 4 agentes ("El Centro Aldaba") | `spike/run_spike.py` | ✔ corre con NaN real: Game Master **situado** (lugares de la sala + acciones físicas + rastreo de posiciones), personas ricas y canal privado de pensamientos |
| Conexión NaN | `spike/model_factory.py` + `spike/.env` | ✔ **conectado y verificado** (14-07-2026): `qwen3.6` vía `api.nan.builders/v1`, ~1–3 s/llamada, salida limpia sin razonamiento incrustado, en personaje y en el formato de habla de Concordia |
| Persistencia de sesiones | `spike/runs/<id>/{log.json, transcripcion.html, meta.json, replay.json}` | ✔ automática en cada run |
| Exportador log → replay | `spike/export_replay.py` | ✔ probado (diálogo/acción/narrador/pasos) |
| **Visor tipo AI Town** | `viewer/index.html` | ✔ **prototipo funcional verificado en navegador** |
| **Diseñador de escenarios** | `panel/index.html` | ✔ situación + reparto (protagonistas Big Five/demografía/trasfondo + población por reglas con semilla) + variantes «¿y si…?» + previsualización determinista; exporta `escenario.json` |
| Personas ricas en la sim | `spike/personas.py` | ✔ prefab `persona__Entity`: la identidad (demografía + carácter + trasfondo) es un componente constante visible en cada decisión del agente |
| Puente diseñador → runner | `run_spike.py --config escenario.json` | ✔ validado (población en masa queda para F3) |

El visor (HTML autocontenido, sin dependencias ni build): sala 2D cenital estilo píxel dibujada por código, personajes con nombre y color, bocadillos de diálogo, **bocadillos de pensamiento ocultables** (botón 💭 — verlos u ocultarlos cambia la lectura de la escena: eso es didáctica), acciones, banda de narrador, movimiento entre puntos de la sala, timeline con scrubber, velocidades, feed lateral de eventos clicable (saltar a cualquier momento), panel "¿Qué estás viendo?", carga de cualquier `replay.json` por botón o arrastrar-y-soltar, y una **demo embebida** que muestra el aspecto de un episodio real. Atajos: espacio (play/pausa), ←/→ (evento).

## 4. Estado verificado de Concordia (13-07-2026)

| Dato | Valor verificado |
|---|---|
| Repo | `google-deepmind/concordia`, Apache 2.0, ~1.554 ⭐, último push 10-07-2026 |
| PyPI | `gdm-concordia` **2.4.0** (06-03-2026) · Python **≥ 3.12** |
| API v2 | prefabs + `prefab_lib.Config` + `Simulation(config, model, embedder).play()` → `SimulationLog` |
| LLM | `GptLanguageModel` acepta `api_base` → **NaN entra por configuración**, sin wrapper propio |
| Robustez | `RetryLanguageModel`, `CallLimitLanguageModel` (kill-switch) en el core |
| Regalos | `contrib/persona_generators/` (personalidades), `questionnaire_example.ipynb` (sondas psicométricas), ejemplos `resource_dilemma/`, `social_media/` |

Versión fijada: `gdm-concordia==2.4.0` (la API v2 cambió mucho respecto a tutoriales antiguos).

## 5. Arquitectura y repo objetivo

```
PsicoAI/
├── PROPUESTA.md
├── spike/                # F0: sim + exportador (hecho)
├── viewer/               # visor de replays (prototipo hecho)
│   └── index.html
├── src/psicoai/          # F2-F3: episodios como módulos
│   ├── models.py         # fábrica NaN
│   ├── personas.py       # sobre contrib.persona_generators
│   ├── episodios/        # un módulo por episodio (premisa+personajes+export)
│   └── estudio/          # F4: métricas, juez, análisis
├── configs/              # episodios declarativos (YAML)
└── runs/                 # sesiones guardadas (gitignored) — cada una con su replay.json
```

## 6. Fases

| Fase | Contenido | Criterio de salida |
|---|---|---|
| **F0 · Spike** ✔ | Concordia 2.4 instalada, sim 4 agentes, sesiones persistidas | hecho (falta el run real con NaN) |
| **F1 · Tubería de replay** ✔ ~90 % | Exportador + visor prototipo | Queda: pulir el mapeo con los textos de un run real (el dry-run produce eventos vacíos por diseño) |
| **F2 · Primer episodio real** ✔ | **Hecho (14-07-2026)**: `episodios/ep01-el-centro-la-norma/` — 40 pasos, 125 eventos, curado con ficha didáctica | Ver `ficha.md`: 4 fenómenos, momentos clave clicables, replay listo para el visor |
| **F3 · Catálogo de episodios** | 3–4 episodios-paradigma (§7) + capa didáctica ("qué mirar", pensamientos, fichas de fenómeno) + índice de sesiones | Cada episodio se lanza con un comando y sale un replay viewable |
| **F4 · Modo estudio + difusión** | El rigor: N seeds × condiciones, modelo juez, sondas de contaminación, gráficas; y compartir públicamente | Primer episodio con datos ("¿cuánto conforma un agente según su personalidad?") |

## 7. Catálogo inicial de episodios

Cada episodio = premisa + personajes + **un fenómeno psicológico** + "qué mirar" en pantalla.

1. **El Centro** (ya esbozado): una norma injusta en una institución cerrada — autoridad, obediencia, nacimiento de una coalición. *Qué mirar: quién calla en público y qué piensa en privado; el momento en que el primer aliado cambia la escena.*
2. **La fuerza del grupo** (conformidad, Asch disfrazado): un panel de revisores donde la mayoría se equivoca unánimemente; el sujeto emite juicio privado 💭 antes de hablar. *Qué mirar: la distancia entre el juicio privado y la respuesta pública, ronda a ronda.*
3. **El precio de obedecer** (gradiente de autoridad): una figura de autoridad pide aplicar sanciones crecientes a un tercero. *Qué mirar: dónde está el escalón en el que cada personalidad planta cara.*
4. **La sala del reparto** (dilema de recursos; hay ejemplo en Concordia): recurso común escaso. *Qué mirar: cooperación, acaparamiento, castigo social.*
5. **El rumor** (difusión/polarización; sobre el ejemplo `social_media/`): una información falsa entra en el grupo. *Qué mirar: quién la amplifica, quién la corrige, a quién creen.*

## 8. Honestidad didáctica (el rigor, comprimido)

Didáctico no significa inventado: los episodios son conducta **emergente real de los modelos**, no guiones escritos por nosotros — y eso hay que protegerlo y contarlo bien.

- **Regla de los dos canales** (decisión de David, 14-07-2026): en un experimento social real no hay acceso al pensamiento de nadie, así que la simulación separa estrictamente el **canal observable** (lo que cualquier participante habría visto u oído: dichos y hechos) del **canal privado** (monólogo interno). El canal privado (a) nunca es visible para otros agentes ni para el Game Master — vive dentro del agente por arquitectura—; (b) queda **fuera de todo análisis por defecto**: métricas y juez consumen solo conducta observable, comparable con la literatura humana; (c) se usa solo como capa didáctica en el visor (botón 💭) y, opt-in explícito, como validación (ej. en conformidad: distinguir complacencia pública de distorsión real del juicio); (d) es apagable en el origen (`--sin-pensamientos` o `"pensamientos": false` en el escenario).
- **Contaminación**: los modelos se saben de memoria los experimentos famosos; si montas "Asch" tal cual, recitan el guion. Por eso los episodios usan **disfraces isomorfos** (misma estructura causal, historia de portada nueva) incluso en modo didáctico.
- **Lo que esto es**: conducta de sistemas LLM en roles. **Lo que no es**: evidencia sobre humanos. Cada episodio lo dirá en su ficha; las cifras humanas clásicas se citan como *contexto*, no como equivalencia.
- **Seguridad**: tope duro de llamadas por run (`CallLimitLanguageModel`), y en F3 un clasificador barato por turno que etiqueta/pausa contenido problemático. Trazabilidad total: cada replay lleva detrás su log completo reproducible.
- **Modo estudio (F4)**: cuando queramos medir de verdad — N seeds × condiciones con control, modelo juez con rúbricas, distribuciones. La arquitectura ya lo soporta; simplemente no es el producto principal.

## 9. Formato `replay.json` (contrato del visor)

```jsonc
{
  "version": 1,
  "meta": {"titulo": "...", "descripcion": "qué estás viendo", "fecha": "...", "fuente": "concordia|demo"},
  "agentes": [{"id": "marta", "nombre": "Marta Ibáñez", "rol": "Directora", "color": "#e4572e", "spot": "tablon"}],
  "eventos": [
    {"tipo": "narrador",    "texto": "..."},
    {"tipo": "paso",        "n": 1},
    {"tipo": "dialogo",     "agente": "marta", "texto": "...", "hacia": "andres"},
    {"tipo": "pensamiento", "agente": "lucia", "texto": "..."},
    {"tipo": "accion",      "agente": "andres", "texto": "..."},
    {"tipo": "movimiento",  "agente": "andres", "spot": "ventana"}
  ]
}
```

Spots disponibles en la sala actual: `tablon, ventana, mesa_o, mesa_e, mesa_s, sofa, puerta, centro`. El visor tolera tipos desconocidos (van solo al feed), así el formato puede crecer sin romper replays viejos. Los eventos `pensamiento` llevan `"canal": "privado"` y son la única parte del replay que procede del canal no observable (regla de los dos canales, §8): los análisis los ignoran salvo bandera explícita.

## 10. Cómo probarlo ahora mismo

**Visor con demo** (sin instalar nada): abrir `viewer/index.html` en el navegador — carga sola una demo de "El Centro Aldaba" con 44 eventos. (En esta sesión quedó además servido en `http://localhost:8123`.)

**Tubería completa** (NaN ya configurado en `spike/.env`, gitignored):
```bash
cd spike
source .venv/bin/activate            # venv ya creado e instalado (incl. sentence-transformers)
python run_spike.py --steps 20       # simula con qwen3.6 y guarda runs/<id>/ con replay.json
# abrir viewer/index.html → «Cargar replay.json» → runs/<id>/replay.json
```

## 11. Costes y escala (medidos el 14-07-2026)

**Latencia por paso** (medida, escenario de 4 agentes): GM conversacional ~25 s/paso; GM situado ~86–89 s/paso (3,4×, porque rastrea posiciones y estado del mundo). Elección por episodio.

**Modelos de NaN** (medidos con prompt de roleplay): `qwen3.6` (calidad, ~2–8 s, requiere el wrapper anti-razonamiento), `gemma4` (**0,9 s** y buen español en personaje — el modelo de población), `mimo-v2.5` (~6 s), `deepseek-v4-flash` (~11 s). También `qwen3-embedding` (posible sustituto futuro del embedder local).

**Concurrencia de NaN** (medida): a partir de ~4 llamadas simultáneas el endpoint penaliza con cola/429: 8 llamadas en paralelo tardaron 61,6 s frente a ~8 s en serie. Por eso el wrapper impone un **semáforo global de 3 llamadas concurrentes** (`NAN_MAX_CONCURRENTES`). Conclusión de diseño: la simultaneidad es *lógica* (motor `simultaneous` de Concordia, varios agentes actúan por paso) pero el grifo hacia NaN se mantiene estrecho.

**Enrutado por rol**: protagonistas con `NAN_MODEL` (qwen3.6, con canal privado), población con `NAN_MODEL_LIGERO` (gemma4, sin pensamientos). La población generada por el diseñador viaja dentro de `escenario.json` (`agentes_generados`, determinista por semilla) y el runner la simula hasta `--max-poblacion`.

En modo didáctico (pocas sesiones curadas) cualquier API valdría; en modo estudio (decenas de runs por episodio) la tarifa plana de NaN es la diferencia entre iterar libremente y mirar el contador.

## 12. Qué necesito de ti

1. ~~Credenciales NaN~~ **Hecho** (14-07-2026): `qwen3.6` conectado y validado, con wrapper endurecido contra el modo razonamiento (suelo de tokens, reintentos, limpieza de `<think>`). Queda por conocer el límite de concurrencia/rate de NaN para paralelizar sesiones.
2. **Feedback del visor**: ¿es este el look? (sala píxel, bocadillos, pensamientos en lavanda). Es el momento barato de pedir cambios: paleta, sprites, tamaño de sala, más muebles/salas por episodio.
3. **Confirmar el orden del catálogo** (§7): propongo El Centro → La fuerza del grupo. 
