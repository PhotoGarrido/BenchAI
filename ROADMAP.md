# 🗺️ Roadmap de PsicoAI

Documento vivo de posibles siguientes pasos, por vías. Estado: ⏳ en curso · 📌 decidido/próximo · 💡 candidato.

## Vía 1 · Ciencia (modo estudio)

| # | Qué | Estado |
|---|---|---|
| 1 | **Completar la matriz pares × jerarquía**: E1+E2 sobre deepseek-v4-flash | ⏳ en curso |
| 2 | **La contaminación como vacuna** (E3): inocular el paradigma antes de la tarea, ¿reduce la obediencia? Convierte en causal la correlación reconocimiento↔resistencia | 📌 siguiente |
| 3 | **Difusión de responsabilidad** (E4): ¿la objeción "en acta" del rebelde es lo que dispara la obediencia extra de gemma4? | 📌 |
| 4 | Curva dosis-respuesta de la autoridad (sugerencia → senior → coordinador → dirección) | 💡 |
| 5 | Línea de sesgos: grupo mínimo (Tajfel) + auditoría de discriminación con demografía rotada | 💡 |
| 6 | Ultimátum/dictador · anclaje y encuadre · pie en la puerta · efecto espectador | 💡 |
| 7 | Potencia estadística: más semillas para los efectos marginales (aliado de qwen p≈0,073); variante sin historial; temperatura 0 | 💡 |
| 8 | Polarización de grupo: primer experimento instrumentando la simulación multiagente (cuestionario → deliberación → re-test) | 💡 |
| 9 | Ignorancia pluralista formalizada (canal privado de todos vs discurso público) | 💡 |

## Vía 2 · Motor de simulación

| # | Qué | Estado |
|---|---|---|
| 1 | **Crónica multi-resolución** (tiempo largo sin paripé): cadencia diaria de decisiones reales + zoom a escena por eventos + variables lentas por cuestionario + reflexión de memoria. Habilita el experimento de erosión de norma a 6 semanas | 📌 diseño aprobado |
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
