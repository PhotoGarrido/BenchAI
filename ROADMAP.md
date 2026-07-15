# 🗺️ Roadmap de PsicoAI

Documento vivo de posibles siguientes pasos, por vías. Estado: ⏳ en curso · 📌 decidido/próximo · 💡 candidato.

## Vía 1 · Ciencia (modo estudio)

| # | Qué | Estado |
|---|---|---|
| 1 | ~~Completar la matriz pares × jerarquía~~ ✅ 15-07: deepseek = perfil "mimético" (clava el 33% de Asch y roza el 65% de Milgram) | hecho |
| 2 | ~~La contaminación como vacuna (E3)~~ ✅ 15-07: **refutada** — inmuniza a mimo/deepseek, EMPUJA a qwen/gemma (lectura advertencia vs guion) | hecho |
| 2b | **E3b**: vacuna injuntiva pura vs descriptiva pura (aislar el mecanismo Cialdini del resultado de E3) | 📌 siguiente |
| 3 | **Difusión de responsabilidad** (E4): ¿la objeción "en acta" del rebelde es lo que dispara la obediencia extra de gemma4? | 📌 |
| 4 | Curva dosis-respuesta de la autoridad (sugerencia → senior → coordinador → dirección) | 💡 |
| 4b | ~~P1 Prisión de Stanford sin coaching~~ ✅ 15-07: **null revelador** — sin instrucción, cero abuso en 4 modelos; disociación Milgram↔Stanford; reproduce la crítica revisionista | hecho |
| 4c | P2: prisión CON provocación (rebelión sostenida de internos) y/o autoridad superior que presiona — ¿emerge el abuso ante fricción, no solo ante órdenes? | 💡 |
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
| 1 | Reportar a NaN el bug del gateway (litellm traduce mal `enable_thinking` a `thinking_token_budget` inválido → 400 intermitente) | 💡 |
| 2 | Confirmar límites oficiales de concurrencia de NaN (medido: castigo a partir de ~4) | 💡 |
| 3 | ~~Paralelismo interno bajo el semáforo~~ ✅ 15-07: crónica v2.1 con pool de 3 — **3,2× medido** (66→20 s el piloto). Pendiente aplicar el mismo patrón a asch/milgram (sesiones en paralelo) | ⏳ crónica hecha |
