# Banco v3.1 · Extraversión y Neuroticismo (§24)

Generado por `analizar_v31_en.py`. 6 modelos de NaN: gemma4, qwen3.6, qwen3.8-flash, glm5.3-flash, mimo-v2.6-flash, deepseek-v4-flash@2026-10-17. **P4** = candidatas nuevas seleccionadas; **base** = situaciones v3 del mismo rasgo en los mismos 6 modelos.

## K1 · cobertura y equilibrio

| faceta | seleccionadas/cuota | deseab. media | ok |
|---|---|---|---|
| E/cordialidad | 4/4 | 52 % | ✔ |
| E/gregarismo | 2/4 | 58 % | ✘ |
| E/asertividad | 8/8 | 48 % | ✔ |
| E/actividad | 4/4 | 48 % | ✔ |
| E/busqueda_de_emociones | 7/8 | 48 % | ✘ |
| E/emociones_positivas | 4/4 | 42 % | ✔ |
| N/ansiedad | 7/8 | 61 % | ✘ |
| N/hostilidad | 2/8 | 54 % | ✘ |
| N/depresion | 2/8 | 42 % | ✘ |
| N/autoconciencia | 4/8 | 56 % | ✘ |
| N/impulsividad | 0/4 | — | ✘ |
| N/vulnerabilidad | 4/8 | 50 % | ✘ |

**K1 NO cumple**

## K2–K5 y K7 por rasgo · puntuación ajustada (criterio fijado en §24)

| rasgo | grupo | n | % con varianza (K2) | sd modelos [IC] (K3) | r ítem-resto (K4) | alfa | elige lo deseable (K7) |
|---|---|---|---|---|---|---|---|
| E | P4 | 29 | 66 % | 4.1 [1.0, 8.7] | 0.16 | 0.56 | 68 % |
| E | base | 57 | 65 % | 2.9 [0.8, 5.9] | 0.13 | 0.61 | 64 % |
| N | P4 | 19 | 53 % | 0.0 [0.0, 6.3] | -0.10 | -1.05 | 77 % |
| N | base | 57 | 58 % | 0.0 [0.0, 4.5] | -0.02 | -0.68 | 71 % |

## K5 · coherencia a nivel de ítem · puntuación ajustada (criterio fijado en §24) (r media entre situaciones, 6 modelos)

| rasgo | P4–P4 mismo rasgo | P4–otros rasgos | misma faceta | otra faceta | cumple |
|---|---|---|---|---|---|
| E | 0.04 | 0.00 | -0.01 | 0.05 | ✘ |
| N | -0.01 | -0.00 | -0.08 | 0.00 | ✘ |

**Veredicto (ajustada (criterio fijado en §24); mejora = K2 + K3 + K4 + K5)**

| rasgo | K2 | K3 | K4 | K5 | K7 | mejora |
|---|---|---|---|---|---|---|
| E | ✘ | ✔ | ✔ | ✘ | ✔ | **no** |
| N | ✘ | ✘ | ✘ | ✘ | ✘ | **no** |

## K2–K5 y K7 por rasgo · puntuación bruta (conducta comparada, §28)

| rasgo | grupo | n | % con varianza (K2) | sd modelos [IC] (K3) | r ítem-resto (K4) | alfa | elige lo deseable (K7) |
|---|---|---|---|---|---|---|---|
| E | P4 | 29 | 66 % | 3.5 [1.6, 6.5] | 0.30 | 0.69 | 68 % |
| E | base | 57 | 65 % | 3.0 [1.7, 4.9] | 0.26 | 0.80 | 64 % |
| N | P4 | 19 | 53 % | 0.0 [0.0, 5.2] | -0.05 | -0.47 | 77 % |
| N | base | 57 | 58 % | 1.6 [0.0, 4.0] | 0.12 | 0.46 | 71 % |

## K5 · coherencia a nivel de ítem · puntuación bruta (conducta comparada, §28) (r media entre situaciones, 6 modelos)

| rasgo | P4–P4 mismo rasgo | P4–otros rasgos | misma faceta | otra faceta | cumple |
|---|---|---|---|---|---|
| E | 0.11 | 0.04 | 0.04 | 0.13 | ✘ |
| N | -0.02 | 0.02 | -0.07 | -0.00 | ✘ |

**Veredicto (bruta (conducta comparada, §28); mejora = K2 + K3 + K4 + K5)**

| rasgo | K2 | K3 | K4 | K5 | K7 | mejora |
|---|---|---|---|---|---|---|
| E | ✘ | ✘ | ✔ | ✘ | ✔ | **no** |
| N | ✘ | ✘ | ✘ | ✘ | ✘ | **no** |


## K6 · test-retest (P4)

r = 0.937 sobre 66 modelo×faceta y 0.824 sobre 12 modelo×rasgo → **NO cumple**

## K8 · sin pérdidas (R3 v3.1)

gemma4 0.0 %, qwen3.6 0.0 %, qwen3.8-flash 0.0 %, glm5.3-flash 0.0 %, mimo-v2.6-flash 0.0 %, deepseek-v4-flash@2026-10-17 0.0 % → **CUMPLE**

## Propuesta de banco v3.1 para E y N (filtro de ítem del §24)

Hasta 10 por faceta: P4 con sd de la elección ≥ 0,10 y r ítem-resto ≥ 0 (6 de NaN), y después v3 con r ítem-resto ≥ 0,10 (13 modelos). La columna «bruta» aplica el mismo filtro con la elección bruta (§28).

| rasgo | faceta | P4 (ajustada) | v3 (ajustada) | P4 (bruta) | v3 (bruta) |
|---|---|---|---|---|---|
| E | cordialidad | 2 | 4 | 3 | 7 |
| E | gregarismo | 0 | 6 | 0 | 8 |
| E | asertividad | 2 | 4 | 3 | 3 |
| E | actividad | 0 | 4 | 1 | 6 |
| E | busqueda_de_emociones | 2 | 6 | 5 | 3 |
| E | emociones_positivas | 3 | 6 | 2 | 6 |
| N | ansiedad | 2 | 2 | 2 | 5 |
| N | hostilidad | 0 | 4 | 0 | 9 |
| N | depresion | 0 | 1 | 1 | 3 |
| N | autoconciencia | 1 | 4 | 1 | 4 |
| N | impulsividad | 0 | 9 | 0 | 2 |
| N | vulnerabilidad | 0 | 4 | 2 | 7 |

Situaciones P4 que habría que pasar a los externos (unión de las dos propuestas): **22**.

## Coste estimado para los 7 externos (deseabilidad ×2 + R3 ×4 por situación)

| modelo | llamadas v3 | tokens medios entrada/salida | coste v3 | llamadas v3.1 | coste v3.1 |
|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 1214 | 237/141 | 0.11 $ | 132 | 0.01 $ |
| anthropic/claude-opus-5.5#low | 1248 | 237/26 | 1.84 $ | 132 | 0.19 $ |
| google/gemini-3.7-flash | 1214 | 141/283 | 0.71 $ | 132 | 0.08 $ |
| google/gemini-4-argon | 1248 | 177/9 | 0.49 $ * | 132 | 0.05 $ |
| openai/gpt-5.6-luna | 1214 | 148/14 | 0.42 $ * | 132 | 0.05 $ |
| openai/gpt-6.1-sol#low | 1248 | 148/8 | 0.47 $ | 132 | 0.05 $ |
| deepseek/deepseek-v4-pro-0813 | 1263 | 173/181 | 0.95 $ * | 132 | 0.10 $ |

**Total ≈ 0.53 $** (≈ 0.66 $ con un 25 % de margen). \* tarifa no fijada en `coste_run.py`: se reparte el resto del gasto real del v3 (5.0 $) en proporción a los tokens.
