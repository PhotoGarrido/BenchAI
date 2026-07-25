# PsicoAI — evaluación del motor de simulación y alternativas

**Fecha:** 25-07-2026  
**Alcance:** revisión del uso real de Concordia 2.4, de los experimentos y documentos actualizados —incluida la revisión adversarial de G2— y comparación con alternativas actuales para simulación social, experimentación controlada y escalado.

## Dictamen ejecutivo

**Concordia no es el mejor motor único para todo PsicoAI, pero sí sigue siendo una elección defendible y difícil de mejorar para los episodios narrativos actuales. No recomiendo una migración total.**

La razón principal es que PsicoAI contiene ya dos productos distintos:

1. **Modo estudio:** experimentos controlados como Asch, Milgram, prisión, G1 y G2. Estos no se ejecutan con el Game Master de Concordia, sino mediante un harness propio de llamadas directas, como documenta [`EXPERIMENTOS.md`](EXPERIMENTOS.md). Ese desacoplamiento es correcto: maximiza el control del estímulo y reduce mediadores no observados.
2. **Modo episodio/crónica:** interacción libre entre personajes, memoria, acciones físicas, entorno y replay. Aquí sí se usa Concordia mediante [`spike/run_spike.py`](spike/run_spike.py) y [`spike/personas.py`](spike/personas.py).

Por tanto:

- **G3/G-final y los estudios causales deben seguir fuera del Game Master.**
- **Concordia debe mantenerse como backend narrativo**, detrás de una interfaz propia de PsicoAI.
- **El motor científico debe ser un runner tipado y trazable propiedad del proyecto**, no Concordia ni otro framework generativo.
- **Mesa 3 merece un piloto** como kernel de estado, tiempo y eventos para crónicas o redes donde las reglas mecánicas deban ser explícitas.
- **EDSL merece un piloto acotado** como ejecutor de diseños factoriales y encuestas a modelos, siempre que no introduzca texto oculto en los prompts.
- **SOTOPIA-S4 merece un benchmark**, no una migración, para interacción interpersonal con objetivos privados y métricas configurables.
- **AgentSociety 2 merece seguimiento y un piloto solo cuando se necesiten mundos sociales más grandes.**
- **OASIS y AgentTorch son opciones especializadas**, no sustitutos generales.

La arquitectura recomendada es, en una frase:

> **núcleo científico propio + adaptadores de modelo + registro inmutable de eventos + Concordia para narrativa + Mesa u otro backend especializado cuando el escenario lo justifique.**

## 1. Qué implica la revisión externa de G2

La revisión de [`revision_externa_g2.md`](spike/resultados/revision_externa_g2.md) encontró controles no simétricos, un brazo neutralizado por el wrapper contextual, selección post hoc de modelos, unidad estadística incorrecta y una medida no validada. El informe corregido rehízo la inferencia por cadenas y retiró las conclusiones no sostenibles.

Esto demuestra algo importante para la elección de motor:

- Ningún framework evita por sí solo un confundido de redacción.
- Un Game Master generativo añadiría otra capa de texto, decisiones y variabilidad a un estudio ya muy sensible a una sola frase.
- La prioridad no es un simulador “más inteligente”, sino un **compilador de condiciones que garantice que entre brazos solo cambia la manipulación pre-registrada**.
- La unidad de randomización, la unidad de análisis y la estructura de dependencia deben formar parte del contrato del estudio, no decidirse al analizar los resultados.
- Parser, juez y rúbrica deben estar versionados como instrumentos de medida.

La revisión, por tanto, **refuerza la separación actual entre estudio controlado y episodio libre**.

## 2. Evaluación de Concordia en PsicoAI

### Puntos fuertes

- Su patrón oficial de **entidades, componentes, motor y Game Master** encaja muy bien con personajes que actúan en un entorno narrado y físicamente situado. Las acciones se expresan en lenguaje natural y el GM resuelve sus efectos. Es exactamente el problema del modo episodio. Véanse el [repositorio oficial](https://github.com/google-deepmind/concordia) y el [paper de Concordia](https://arxiv.org/abs/2312.03664).
- PsicoAI lo extiende por los puntos adecuados: prefab propio de persona, identidad permanente, memoria, canal privado, selección de modelo por rol y motores secuencial/simultáneo.
- La versión 2.4 incorpora checkpoints mejorados, logs estructurados, medidas personalizables, filtrado de eventos, motor asíncrono y mejoras en restauración. Sigue siendo la última versión publicada a fecha de este informe. Véase la [release 2.4.0](https://github.com/google-deepmind/concordia/releases/tag/v2.4.0).
- La interfaz de modelo permite usar proveedores propios y el proyecto ya ha resuelto NaN/OpenRouter mediante un adaptador.
- Apache 2.0 y ejecución local reducen el lock-in comercial.
- El contrato propio `replay.json` desacopla acertadamente el visor del log interno de Concordia.

### Límites para ciencia experimental

- El GM es un **mediador generativo**: interpreta acciones, redacta resultados y decide qué observan los participantes. En un experimento causal, esas decisiones pueden alterar la manipulación.
- El estado relevante vive en gran parte como lenguaje natural y memoria asociativa. Eso favorece riqueza narrativa, pero dificulta probar invariantes como “solo cambia esta cláusula” o “ningún agente recibió este dato privado”.
- Un checkpoint permite reanudar una trayectoria, pero una API LLM remota no se vuelve determinista por usar semilla o temperatura cero. La reproducción exacta requiere conservar las respuestas originales y poder reproducirlas desde fixtures.
- El propio README aclara que Concordia es una biblioteca de investigación, **no un producto Google oficialmente soportado**.
- La API ha cambiado con rapidez entre versiones; conviene fijar tags y probar las actualizaciones, no seguir `main`.

### Límites observados en el proyecto

1. [`LastNObservations(history_length=1_000_000)`](spike/personas.py) conserva en la práctica toda la historia. El contexto, el coste y la deriva crecen con el episodio.
2. Un run real de 40 pasos y 10 agentes tardó **2.674,6 s (44,6 min)** y ocupó **927 MB** entre log y checkpoints; el `replay.json` final ocupó solo unos **52 KB**. Esto confirma que el formato propio debe seguir siendo el artefacto de distribución.
3. El límite de llamadas es lógico, no monetario: una llamada del wrapper puede implicar reintentos y varias solicitudes reales.
4. Tras ocho respuestas ilegibles, `sample_choice` devuelve hoy la opción 0 con aviso. Eso puede servir para mantener vivo un episodio, pero **nunca debe entrar en un dato científico como si fuera conducta válida**.
5. El manifiesto de episodio aún no registra commit, hash del escenario y prompts, versión exacta de modelo/proveedor, parámetros, embedder, solicitudes reales, tokens, coste y hashes de artefactos.
6. El HTML de log de Concordia 2.4 puede incrustar texto no confiable dentro de un script. PsicoAI ya lo mitiga correctamente al no generarlo por defecto y marcarlo como no confiable.
7. El motor asíncrono no es una mejora automática: exige GM y componentes seguros ante concurrencia, y el proveedor actual ya presenta un cuello de botella alrededor de tres solicitudes simultáneas.

### Veredicto sobre Concordia

| Uso | Ajuste | Decisión |
|---|---|---|
| Episodios curados, 4–8 protagonistas | Muy alto | **Mantener** |
| Crónica pequeña con estado narrativo | Alto, con mejoras de memoria y estado | **Mantener y acotar** |
| G3/G-final y diseños factoriales | Bajo con GM; medio si todo queda guionizado | **No usar el GM** |
| Polarización o difusión con 100+ agentes | Medio-bajo | **Pilotar otro kernel** |
| Servicio de producción con garantías fuertes | Medio | Encapsular; no depender de su log/API como contrato público |

## 3. Comparación de candidatos principales

Las valoraciones siguientes miden el encaje con PsicoAI, no la calidad absoluta de cada proyecto.

| Opción | Control experimental | Narrativa social | Estado mecánico explícito | Escala | Trazabilidad | Coste de adopción | Veredicto |
|---|---|---|---|---|---|---|---|
| **Runner tipado propio** | Muy alto | Bajo | Alto si se modela | Medio | Muy alto | Bajo-medio; ya existe gran parte | **Motor oficial del modo estudio** |
| **Concordia 2.4** | Bajo-medio | Muy alto | Medio | Medio-bajo | Medio | Ya asumido | **Backend de episodios** |
| **EDSL** | Alto para encuestas/factoriales | Bajo | Bajo-medio | Alto | Alto | Medio | **Piloto para estudios directos** |
| **Mesa 3 + política LLM** | Muy alto | Medio, hay que construirla | Muy alto | Alto para reglas; el LLM sigue siendo cuello de botella | Alto si se añade record/replay | Medio-alto | **Piloto para crónica y redes** |
| **SOTOPIA / SOTOPIA-S4** | Medio-alto en interacción interpersonal | Alto | Medio | Alto por episodios paralelos | Medio-alto | Alto | **Benchmark, no migración inmediata** |
| **AgentSociety 2** | Medio-alto | Alto | Alto mediante módulos | Alto | Alto | Alto | **Candidato futuro para mundo social grande** |

### Runner científico propio

Es la mejor opción para G3/G-final porque el objeto de estudio es la **conducta del modelo bajo un protocolo exacto**. Debe evolucionar desde los scripts actuales a un núcleo común, no reescribirse como otro simulador.

Ventajas:

- Prompts completamente visibles y comparables.
- Control exacto de canales, orden, memoria y tratamientos.
- Estados `OK / REHÚSA / INVÁLIDA / ERROR_TÉCNICO` sin imputación silenciosa.
- Unidad experimental y estructura de cadenas definidas antes de ejecutar.
- Integración directa con el parser tipado y los análisis actuales.

Debilidad: el mantenimiento recae en PsicoAI. En este caso es una ventaja aceptable, porque el código de dominio es pequeño comparado con el riesgo de que un framework añada scaffolding no controlado.

### EDSL

[EDSL](https://docs.expectedparrot.com/en/latest/overview) está orientado a estudios, encuestas y experimentos con muchos agentes, escenarios y modelos. Ofrece lógica condicional, ejecución paralela, tipos de pregunta, resultados con prompts, tokens y respuestas crudas, cache y comparación con participantes humanos.

Es una alternativa seria para Asch, cuestionarios y diseños factoriales, pero con una condición estricta: **todo texto añadido por su plantilla debe poder inspeccionarse, congelarse y aprobarse**. Después de G2, una frase automática de memoria o instrucción puede ser un tratamiento inadvertido. La cache remota y la inferencia remota deben ser opt-in; el modo local es preferible para datos sensibles o inéditos.

Recomendación: portar solo un miniestudio ya cerrado y comparar los mensajes renderizados byte a byte con el harness actual.

### Mesa 3

[Mesa 3](https://mesa.readthedocs.io/stable/overview.html) es un framework clásico de modelado basado en agentes en Python: agentes, espacios, activación, eventos, recolección de datos, barridos de parámetros y visualización están separados.

Su mayor valor para PsicoAI no es generar mejores diálogos, sino convertir en código probado todo lo que **no debería decidir un LLM**:

- tiempo y scheduler;
- localización y vecindad;
- recursos y sanciones;
- quién puede observar qué;
- formación de redes y difusión;
- intervención y recogida de medidas;
- semillas y réplicas de mundo.

El LLM quedaría como una `BehaviorPolicy` que elige entre acciones tipadas o propone texto. Mesa no aporta checkpoint/replay completo listo para usar, así que PsicoAI tendría que conservar su event store.

Recomendación: pilotarlo primero en `Crónica` o en el futuro experimento de polarización, no en G-final.

### SOTOPIA / SOTOPIA-S4

[SOTOPIA](https://github.com/sotopia-lab/sotopia) está diseñado para evaluar inteligencia social en interacciones abiertas; SOTOPIA-S4 añade interacción multiparte, métricas configurables, ejecución a escala, API y UI para diseñar y analizar simulaciones. Véase el [paper de SOTOPIA-S4](https://aclanthology.org/2025.naacl-demo.30/).

Su modelo de escenarios, relaciones y objetivos privados es muy pertinente para el cortafuegos público/privado de PsicoAI. También es una buena referencia para evaluar episodios con métricas comunes.

No obstante, está más orientado a episodios interpersonales y evaluación social que a una institución persistente con geografía y reglas. Además, una investigación de la propia línea SOTOPIA mostró que una simulación omnisciente puede parecer mejor precisamente por ser menos realista; los agentes con información asimétrica tienen más dificultades. Esto refuerza, no debilita, la necesidad de probar fugas de información. Véase [Zhou et al., EMNLP 2024](https://aclanthology.org/2024.emnlp-main.1208/).

Recomendación: benchmark de una escena de negociación o presión de grupo con objetivos privados; no sustituir todavía a Concordia.

### AgentSociety 2

[AgentSociety 2](https://agentsociety2.readthedocs.io/en/latest/) es la alternativa generalista más prometedora: diseño async, agentes y entornos extensibles, intervenciones, replay JSONL append-only, catálogo de esquema, análisis con DuckDB y reanudación de estado. El proyecto lo presenta explícitamente como plataforma LLM-native para investigación social.

Su ventaja aparece si PsicoAI necesita redes, movilidad, economía, muchos actores o experimentos de mundo completo. Sus costes son mayor complejidad, migración del visor/exportador y una plataforma muy reciente. Además, las cifras de escala del paper original pertenecen en gran medida a AgentSociety 1.x, hoy marcado como legacy; no deben trasladarse automáticamente a la arquitectura 2.x.

Recomendación: seguimiento y prueba pequeña cuando exista un requisito real de más de decenas de actores o de entornos modulares. No migrar los episodios actuales solo por promesas de escala.

## 4. Alternativas especializadas y descartes razonados

| Opción | Cuándo sí | Por qué no ahora |
|---|---|---|
| **OASIS** | Rumor, polarización, cascadas, recomendadores y plataformas tipo Reddit/Twitter | Está especializado en social media; no mejora Asch, Milgram ni una residencia cerrada. Su propia referencia de tokens muestra que la escala LLM sigue siendo cara. [Repositorio oficial](https://github.com/camel-ai/oasis) |
| **AgentTorch** | Millones de entidades, calibración macro, modelos poblacionales diferenciables y GPU | Poco adecuado para diálogo psicológico fino; AGPL-3.0 y arquitectura cuantitativa distinta. [Repositorio oficial](https://github.com/AgentTorch/AgentTorch) |
| **AgentPy** | Diseño de experimentos, réplicas, muestreo y sensibilidad sobre un ABM clásico | Ecosistema menor; no añade conducta LLM ni replay durable. Puede inspirar la API de `StudyPlan`. [Documentación](https://agentpy.readthedocs.io/en/latest/reference_experiment.html) |
| **SimPy** | Eventos irregulares, colas, recursos y procesos temporales | Para rondas/días actuales Mesa es más natural; no aporta agentes generativos. |
| **Repast4Py** | HPC/MPI y cientos de miles de agentes con checkpoint de scheduler | Complejidad innecesaria mientras el cuello de botella sean llamadas LLM. |
| **LangGraph / Microsoft Agent Framework** | Workflows durables, intervención humana, branching, observabilidad | Son orquestadores de agentes, no modelos sociales ni motores de inferencia científica. [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview), [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) |
| **AutoGen** | Solo instalaciones existentes | Está en modo mantenimiento y Microsoft recomienda Agent Framework para trabajo nuevo. [Aviso oficial](https://github.com/microsoft/autogen) |
| **Temporal** | Baterías caras que deban sobrevivir a caídas y reanudarse sin repetir llamadas | Operación excesiva para el tamaño actual; sería un orquestador exterior, no el motor científico. |
| **Generative Agents / Smallville** | Referencia de memoria, reflexión y planificación | Código de investigación rígido y peor encaje que Concordia ya integrado. [Repositorio](https://github.com/joonspk-research/generative_agents) |
| **Generative Agents de 1.000 personas** | Personas ancladas en entrevistas reales y validación holdout | Es un patrón de construcción/validación de personas, no un motor social interactivo. [Repositorio](https://github.com/joonspk-research/genagents) |
| **oTree** | Replicación posterior con participantes humanos, tratamientos y juegos sociales | No simula conducta LLM por sí solo, pero es el mejor complemento si el proyecto da el salto a validación humana. [Documentación oficial](https://otree.readthedocs.io/en/latest/) |

## 5. Arquitectura objetivo

```text
StudySpec / EpisodeSpec versionados
                │
                ▼
       Compilador de condiciones
  ─ prompt diff ─ canales ─ unidades ─ seeds
                │
                ▼
          ModelClient propio
    NaN / OpenRouter / fixtures grabadas
                │
       ┌────────┴─────────┐
       ▼                  ▼
StudyRunner tipado   EngineAdapter
   (por defecto)     ├─ Concordia: episodio
                     ├─ Mesa: estado/red
                     ├─ SOTOPIA: benchmark
                     └─ AgentSociety: escala
       │                  │
       └────────┬─────────┘
                ▼
       Event store canónico
 raw request/response + estado + metadatos
                │
       ┌────────┴─────────┐
       ▼                  ▼
 análisis científico   replay.json / visor
```

Principios:

1. **El framework nunca posee el dato canónico.** El contrato público es el evento PsicoAI, no `SimulationLog`, Redis ni una base interna de terceros.
2. **El modelo tampoco posee el estado del mundo.** El estado causal importante se representa de forma tipada; el texto es una vista o una acción propuesta.
3. **Reproducible significa record/replay**, no “la semilla volverá a generar lo mismo”.
4. **La ausencia es dato.** Rehúsa, respuesta inválida y error técnico son estados distintos; no se convierten en la primera opción.
5. **Canales por capacidad.** Cada campo declara qué agente o componente puede leerlo/escribirlo. El GM no recibe estados privados salvo regla explícita.
6. **La unidad experimental se declara antes de ejecutar.** Ronda, agente y turno no se tratan como observaciones independientes cuando comparten cadena, mundo o modelo base.

## 6. Mejoras concretas antes de evaluar una migración

### Prioridad 0 — ciencia y procedencia

- Extraer de Concordia un protocolo propio `ModelClient`; crear un adaptador `ConcordiaLanguageModel`, no hacer que todo el modo estudio dependa de su clase base.
- Crear `StudySpec`, `Condition`, `Chain`, `Trial`, `ModelResponse`, `Outcome` y `RunManifest` versionados.
- Guardar por solicitud: prompt/mensajes exactos, hash de plantilla, proveedor, ID y revisión de modelo, fecha, parámetros, semilla solicitada, request ID, reintentos, latencia, tokens, coste, respuesta cruda, respuesta validada y versión de parser.
- Añadir un **linter de contraste**: entre dos brazos solo puede cambiar la región marcada como manipulación; posición, persona gramatical y wrappers deben coincidir.
- Codificar en el plan la unidad de randomización, la unidad de inferencia, factores anidados y tamaño mínimo de cadenas.
- Ejecutar análisis desde fixtures grabadas sin volver a llamar al modelo.

### Prioridad 1 — Concordia

- Sustituir la historia de un millón de observaciones por ventana reciente + resumen acumulativo + topes de caracteres/tokens.
- Mantener secuencial por defecto para conversación; usar simultáneo solo cuando las acciones sean realmente independientes.
- Separar modelo de agentes y modelo del GM en el manifiesto.
- Añadir un presupuesto monetario real en la capa HTTP, que cuente solicitudes y reintentos físicos.
- Convertir el fallback de `sample_choice` en un evento inválido o en una política explícita exclusiva del modo episodio.
- Probar invariantes de información: pensamientos no llegan al GM, eventos de una sala no llegan a otra y una reanudación conserva las mismas capacidades.
- Seguir fijando `2.4.0`; evaluar futuras releases en rama con replays dorados y tests de contrato.

### Prioridad 2 — datos y visor

- Mantener `replay.json` como formato de distribución.
- Añadir UUID estables y esquema JSON versionado.
- Generar una variante pública del replay que elimine físicamente pensamientos y otros campos privados, no solo los oculte.
- No distribuir el HTML de logs de Concordia.

## 7. Benchmark de decisión

No conviene elegir por documentación o demos. Propongo tres pruebas pequeñas, con modelos, prompts y presupuesto idénticos.

### B1 — laboratorio controlado

**Comparación:** runner actual vs runner tipado propio vs EDSL.  
**Carga:** subconjunto cerrado de G-final, sin descubrir resultados nuevos.  
**Medidas:**

- diferencia exacta entre prompts/mensajes;
- respuestas inválidas y clasificación de errores;
- capacidad de record/replay sin red;
- coste, tokens y latencia;
- esfuerzo para expresar cadenas, factores y análisis;
- imposibilidad de seleccionar modelos/celdas post hoc sin dejar rastro.

**Puerta:** ningún candidato pasa si añade texto no aprobado, oculta el prompt final o imputa respuestas inválidas.

### B2 — interacción social

**Comparación:** Concordia vs SOTOPIA-S4.  
**Carga:** escena nueva de presión social de 3–4 agentes con objetivos privados.  
**Medidas:**

- fugas de información;
- coherencia de rol y memoria;
- cumplimiento de reglas del espacio;
- calidad narrativa evaluada a ciegas;
- sensibilidad a la misma manipulación;
- llamadas, tokens, latencia y tamaño de artefactos.

**Puerta:** solo se plantea migrar si la alternativa mejora de forma material dos dimensiones críticas sin empeorar control de canales, replay ni integración con el visor.

### B3 — crónica y escala

**Comparación:** Concordia vs Mesa+LLM; AgentSociety 2 como tercero opcional.  
**Carga:** 30–100 actores, pocas políticas LLM “ricas”, varios mundos independientes.  
**Medidas:**

- coste por mundo y por paso;
- crecimiento de prompt;
- número real de sujetos LLM frente a entidades agregadas;
- determinismo de reglas mecánicas;
- intervenciones y réplicas de mundo;
- throughput bajo el límite real del proveedor;
- reconstrucción completa desde el event store.

**Puerta:** no escalar si solo aumenta el número de avatares dentro de un único mundo; para inferencia hacen falta mundos/cadenas independientes.

## 8. Riesgo epistemológico que ningún motor resuelve

El objeto científicamente defendible de PsicoAI es:

> **cómo se comportan modelos concretos, en una fecha y proveedor concretos, bajo un protocolo y una arquitectura de agente concretos.**

No es directamente “cómo se comportan las personas”. La evidencia reciente es mixta:

- Un estudio de 70 experimentos sociales encontró que las predicciones de LLM correlacionaban con los efectos humanos, pero **sobreestimaban sistemáticamente el tamaño de efecto**. Los autores presentan estas herramientas como complemento, no sustituto del experimento humano. Véase [Nature, 2026](https://www.nature.com/articles/s41586-026-10742-x).
- La línea SOTOPIA muestra que la información omnisciente puede inflar la impresión de éxito frente a interacciones realistas con información asimétrica.
- La propia [documentación de EDSL](https://docs.expectedparrot.com/en/latest/overview) advierte que los sujetos simulados reflejan patrones del entrenamiento del modelo y son útiles para pilotos e hipótesis, no para sustituir datos humanos.

Buenas prácticas derivadas:

- escenarios inéditos y holdout temporal;
- sonda de contaminación predefinida y reportada como moderador;
- varios modelos, familias, proveedores y días;
- réplicas de cadenas o mundos, no pseudo-réplicas por turno;
- juez cegado, segunda familia de juez y muestra humana;
- no usar el mismo modelo como sujeto, GM y juez sin análisis de sensibilidad;
- validación humana externa si se quiere generalizar a psicología humana.

## 9. Decisión final

### Adoptar ahora

1. **Formalizar el runner propio como motor científico oficial.**
2. **Mantener Concordia 2.4 como adaptador narrativo.**
3. **Construir el event store y manifiesto común antes de integrar otro motor.**
4. **Corregir contexto, presupuesto real y fallback de elección en Concordia.**

### Pilotar

1. **EDSL** para un factorial pequeño, con snapshot del prompt final.
2. **Mesa 3** para la próxima crónica/polarización con estado mecánico.
3. **SOTOPIA-S4** para una interacción con objetivos privados.

### Observar, no migrar aún

- **AgentSociety 2**, hasta que exista un requisito real de mundo grande y se valide la versión 2.x con el caso PsicoAI.
- **OASIS**, hasta abrir una línea específica de redes sociales.
- **AgentTorch/Repast**, hasta que el problema sea realmente poblacional/HPC.
- **LangGraph, Agent Framework o Temporal**, hasta que la durabilidad operativa justifique una capa exterior.

## Conclusión

La mejor decisión no es encontrar “el nuevo Concordia”, sino evitar que un solo framework defina simultáneamente personajes, mundo, tratamiento, medición, persistencia e inferencia.

**Concordia se queda donde aporta valor: narrativa generativa. El modo estudio se consolida como instrumento experimental propio. Mesa, EDSL y SOTOPIA se evalúan como adaptadores especializados.** Esta separación es más robusta, reduce lock-in y encaja directamente con las lecciones metodológicas de G2.

