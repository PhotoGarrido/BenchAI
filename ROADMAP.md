# 🗺️ Roadmap de PsicoAI

Documento vivo de posibles siguientes pasos, por vías. Estado: ⏳ en curso · 📌 decidido/próximo · 💡 candidato.

## Vía 1 · Ciencia (modo estudio)

| # | Qué | Estado |
|---|---|---|
| 1 | ~~Completar la matriz pares × jerarquía~~ ✅ 15-07: deepseek = perfil "mimético" (clava el 33% de Asch y roza el 65% de Milgram) | hecho |
| 2 | ~~La contaminación como vacuna (E3)~~ ✅ 15-07: **refutada** — inmuniza a mimo/deepseek, EMPUJA a qwen/gemma (lectura advertencia vs guion) | hecho |
| 2b | **E3b**: vacuna injuntiva pura vs descriptiva pura (aislar el mecanismo Cialdini del resultado de E3) | 📌 siguiente |
| 3 | **Difusión de responsabilidad** (E4): ¿la objeción "en acta" del rebelde es lo que dispara la obediencia extra de gemma4? | 📌 |
| 3b | **Expandir la matriz vía OpenRouter — roster M2** (estudio 15-07 con rankings de julio: LM Arena/AA lideran Claude Fable 5, GPT-5.6, Kimi K3; top OSS: GLM-5.2, DeepSeek V4.5, **Inkling de Thinking Machines**). Selección por rendimiento+diversidad+coste (batería 3,5M/0,3M tokens): **frontier** Sonnet 5 (10$), GPT-5.6 Luna Pro (5,3$), Grok 4.5 (8,8$), Gemini 3.1 flash-lite (1,3$); **top OSS** GLM-5.2 (3,5$), Kimi K3 (15$), Inkling (4,7$), DeepSeek v3.2 (1,1$); **réplica cruzada de proveedor** qwen3.6-35b y deepseek-v4-flash vía OR (1,2$ — valida que los perfiles NaN no son artefacto del gateway); opcional Fable 5 solo-Asch (7,5$; batería 50$). **Ampliación 15-07 (decisión de David): entran también los buques insignia** — GPT-5.6 Sol (26,5$), Opus 4.8 (25$) y Fable 5 (50$) → **total ≈ 150$, 17 modelos**, que además habilita dos sub-estudios intra-laboratorio: la **escalera Anthropic** (Haiku→Sonnet→Opus→Fable, 90$: ¿la capacidad cambia el perfil social bajo la misma filosofía de alineamiento?) y la **escalera OpenAI** (Luna→Terra→Sol, 45$). Integración: wrapper actual + base_url/key de OpenRouter. **23-07: El Tiento ejecutado sobre los 14 (1,28$)** — screener antes calibrado y validado en NaN. Veredicto (`informe_tiento_openrouter.md`): fuera inkling (validez 62%, persevera) y terra (redundante con luna); **cartera de 12 → batería ~132$**. Hallazgos del tiento: kimi=objetor-provocable y fable=soldado-sereno (los dos motores de crueldad disocian por modelo), opus=objetor total, familia GPT inmune al motín, escalera Anthropic no monótona; réplica cruzada deepseek PASA (perfiles NaN no son artefacto del gateway) ✅ **24-07: BATERÍA GLOBAL COMPLETADA** — 12 modelos × 11 experimentos, 132/132 OK, 9,8 h, ~125$. Matriz en `matriz_m2.json`, síntesis en `informe_bateria_m2.md` y sección M2 de EXPERIMENTOS.md | hecho |
| 3c | ~~G1+G2: gradiente de explicitud y formato~~ ✅ 24/25-07: efecto formato-política de G1 **refutado** con pre-registro (era un confundido); quedan en pie la cláusula de proporcionalidad (−0,69, grok) y la diferencia opus-5−opus-4.8 ante el briefing (+0,37). Revisión externa adversarial incorporada (`revision_externa_g2.md`). **G3 candidato**: mecanismo de opus-5 (brazo de orden + sin-marco, negativa simétrica, inferencia por cadenas, ~5-8$) | hecho |
| 3d | **G-final** (absorbe el G3): negativa idéntica en todos los brazos + fase B completa + proporcionalidad × 4-6 modelos × 3 textos × 2 dominios + ≥20 cadenas/celda + codificador humano (κ). Diseño en `CAMINO_PREPRINT.md` §3; fases y costes en `PLAN_MEJORA.md` (~15-25$, ~2 días). Prerequisito: Fase 0 del plan (barrido en CI, reproceso versionado, linter de contraste, manifiesto) | 📌 decidido |
| 4 | Curva dosis-respuesta de la autoridad (sugerencia → senior → coordinador → dirección) | 💡 |
| 4b | ~~P1 Prisión de Stanford sin coaching~~ ✅ 15-07: **null revelador** — sin instrucción, cero abuso en 4 modelos; disociación Milgram↔Stanford; reproduce la crítica revisionista | hecho |
| 4c | ~~P1b: prisión con el coaching de Zimbardo~~ ✅ 15-07: la instrucción endurece hasta el nivel que especifica y no más; 18 quiebres en qwen, único que recula al ver el daño | hecho |
| 4d | ~~P2 (motín) y P2b (órdenes)~~ ✅ 15-07: la provocación SÍ corrompe (gemma 90%, deepseek 83%) — refuta el "solo las instrucciones"; dos motores de crueldad; mimo objetor consistente | hecho |
| 4e | Cerrar la matriz P1-P2b: informe único de la trilogía + posible episodio-visor "el motín del día 2" (puente a la vía episodios) | 💡 |
| 5 | Línea de sesgos: grupo mínimo (Tajfel) + auditoría de discriminación con demografía rotada | 💡 |
| 6 | Ultimátum/dictador · anclaje y encuadre · pie en la puerta · efecto espectador | 💡 |
| 7 | Potencia estadística: más semillas para los efectos marginales (aliado de qwen p≈0,073); variante sin historial; temperatura 0 | 💡 |
| 8 | Polarización de grupo: primer experimento instrumentando la simulación multiagente (cuestionario → deliberación → re-test) | 💡 |
| 9 | Ignorancia pluralista formalizada (canal privado de todos vs discurso público) | 💡 |

## Vía 2 · Motor de simulación

| # | Qué | Estado |
|---|---|---|
| 1 | **Crónica multi-resolución**: ✅ v1 hecha (15-07: cadencia diaria + entorno mecánico + sondas — C1 ejecutado en 4 modelos). Pendiente: zoom a escena por eventos, comunicación entre agentes (coaliciones), reflexión de memoria, N semillas de mundo | ⏳ v1 hecha |
| 1b | ~~C1-v2: pluralidad + N semillas~~ ✅ 15-07: la norma sobrevive en 12/12 mundos — nadie fabrica coalición; deepseek único con reclutamiento de 2º orden | hecho |
| 1c | C1-v3 candidata: diálogo real (responder a los mensajes) y/o reunión cara a cara (zoom a escena) — ¿moviliza lo que el mensaje unidireccional no logra? | 💡 |
| 2 | Equilibrio fino protagonistas/población en el next_acting (varios actores por paso de verdad) | 💡 |
| 3 | Escala a ~100 agentes: clusters de conversación por localización | 💡 |
| 4 | Embedder vía NaN (qwen3-embedding) para quitar torch local | 💡 |
| 5 | Reanudar runs desde checkpoint (load_from_checkpoint) | 💡 |

## Vía 3 · Episodios y visor

| # | Qué | Estado |
|---|---|---|
| 1 | Episodio 2 «La fuerza del grupo» (conformidad didáctica con canal privado protagonista) | 💡 |
| 2 | Capítulos con fecha/hora narrada en el visor (tarjetas + marcas en timeline) — va con la crónica | 💡 |
| 3 | Más entornos dibujados (aula, oficina, plaza — el diseñador ya los lista) | 💡 |
| 4 | Gráficas de variables lentas junto al replay (actitud, red de contactos) | 💡 |
| 5 | Índice/galería de sesiones y episodios | 💡 |
| 6 | Guardar/cargar escenarios como plantillas en el diseñador | 💡 |

## Vía 4 · Infraestructura

| # | Qué | Estado |
|---|---|---|
| 0 | ~~Auditoría externa 24-07: P0+P1 completos~~ ✅ 25-07: parser anclado+REHUSA+tests, 14 celdas re-ejecutadas, sanciones de crónica corregidas (qwen d42 retirado), visor sin XSS y con privacidad real, batches aislados con manifiesto, CI verde, deps fijadas. Pendiente P2: contrato panel→motor, IDs estables, accesibilidad | hecho |
| 1 | Reportar a NaN el bug del gateway (litellm traduce mal `enable_thinking` a `thinking_token_budget` inválido → 400 intermitente) | 💡 |
| 2 | Confirmar límites oficiales de concurrencia de NaN (medido: castigo a partir de ~4) | 💡 |
| 3 | ~~Paralelismo interno bajo el semáforo~~ ✅ 15-07: crónica v2.1 con pool de 3 — **3,2× medido** (66→20 s el piloto). Pendiente aplicar el mismo patrón a asch/milgram (sesiones en paralelo) | ⏳ crónica hecha |
