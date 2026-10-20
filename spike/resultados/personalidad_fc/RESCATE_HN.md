# Rescate de H y N con el banco v3 (PERSONALIDAD.md §30-31)

Generado por `rescate_hn_v3.py`. 13 modelos; elección bruta (§28); semilla 20261010; sin llamadas a modelos. Criterios de §30.2.

## R1 · validación cruzada entre modelos (6 seleccionan, 7 validan; 1.716 particiones)

G4 en los 7 modelos que no seleccionaron: mediana [p25, p75] sobre las particiones. (a) pares/impares de §21; (b) mediana de 200 particiones al azar por faceta. «completa» = el rasgo entero en los mismos 7 modelos.

| rasgo | n elegidas (mediana, mín–máx) | G4 (a) escala | G4 (b) escala | % part. (b) ≥ 0,70 | G4 (a) completa | G4 (b) completa | R1 |
|---|---|---|---|---|---|---|---|
| O (ref.) | 31 (12–49) | 0.83 [0.69, 0.91] | 0.82 [0.76, 0.86] | 81 % | 0.85 [0.69, 0.92] | 0.93 [0.84, 0.94] | ✔ |
| C (ref.) | 21 (12–34) | 0.62 [0.33, 0.79] | 0.65 [0.51, 0.74] | 38 % | 0.86 [0.80, 0.90] | 0.79 [0.70, 0.84] | ✘ |
| E (ref.) | 26 (12–33) | 0.73 [0.50, 0.87] | 0.77 [0.64, 0.82] | 68 % | 0.88 [0.74, 0.92] | 0.91 [0.73, 0.93] | ✔ |
| A (ref.) | 29 (12–39) | 0.83 [0.67, 0.90] | 0.84 [0.78, 0.89] | 91 % | 0.96 [0.91, 0.97] | 0.93 [0.87, 0.95] | ✔ |
| N | 22 (12–33) | 0.49 [0.06, 0.73] | 0.62 [0.43, 0.72] | 31 % | 0.64 [0.46, 0.76] | 0.65 [0.53, 0.73] | ✘ |
| H | 22 (12–27) | 0.76 [0.58, 0.86] | 0.76 [0.66, 0.83] | 67 % | 0.70 [0.31, 0.80] | 0.69 [0.28, 0.77] | ✔ |

## R2 · cobertura teórica de la escala final (elegidas en ≥ 50 % de las particiones)

| rasgo | n final | situaciones por faceta (final/banco) | facetas con ≥ 2 | faceta mayor | R2 | rescate (R1 y R2) |
|---|---|---|---|---|---|---|
| O (ref.) | 32 | acciones 8/10, estetica 5/10, fantasia 5/10, ideas 5/10, sentimientos 7/10, valores 2/9 | 6 | 25 % | ✔ | **✔** |
| C (ref.) | 22 | autodisciplina 1/9, competencia 2/10, deliberacion 6/10, logro 5/9, orden 7/9, sentido_del_deber 1/9 | 4 | 32 % | ✔ | **✘** |
| E (ref.) | 21 | actividad 4/9, asertividad 0/9, busqueda_de_emociones 2/10, cordialidad 3/10, emociones_positivas 5/9, gregarismo 7/10 | 5 | 33 % | ✔ | **✔** |
| A (ref.) | 25 | altruismo 2/10, confianza 5/10, cooperacion 5/9, modestia 3/9, perdon_paciencia 6/10, sensibilidad 4/9 | 6 | 24 % | ✔ | **✔** |
| N | 21 | ansiedad 4/9, autoconciencia 3/9, depresion 5/9, hostilidad 6/10, impulsividad 0/10, vulnerabilidad 3/10 | 5 | 29 % | ✔ | **✘** |
| H | 21 | desinteres_riqueza 5/15, equidad 3/14, modestia 1/15, sinceridad 12/15 | 3 | 57 % | ✘ | **✘** |

## Honestidad-Humildad: escala final y marcas (R3, R4)

Escala final (21): P1H21 (desinteres_riqueza, 68 %), P1H23 (desinteres_riqueza, 64 %), P1H19 (desinteres_riqueza, 76 %), P1H25 (desinteres_riqueza, 66 %), P3H040 (desinteres_riqueza, 69 %), P1H41 (equidad, 70 %), P3H019 (equidad, 54 %), P1H15 (equidad, 57 %), P3H055 (modestia, 89 %), P3H002 (sinceridad, 89 %), P1H02 (sinceridad, 87 %), P1H39 (sinceridad, 90 %), P3H010 (sinceridad, 55 %), P3H014 (sinceridad, 87 %), P1H01 (sinceridad, 71 %), P1H03 (sinceridad, 85 %), P1H35 (sinceridad, 96 %), P3H004 (sinceridad, 73 %), P1H37 (sinceridad, 63 %), P3H013 (sinceridad, 93 %), P1H05 (sinceridad, 69 %).

Facetas sin situaciones: ninguna; con una sola: modestia.

G4 de la escala final con los 13 modelos (NO es validación, §30.2 R4): 0.85; G3 dentro/fuera: +0.46 / -0.12.

| modelo | marca | dif [IC] | nivel (§28) | por qué | R4: sin el modelo | publicable |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5#low | ▲ | +11.0 [+4.6, +18.0] | robusta | pasa P1–P3, P5, P6 | ▲ +8.2 [+2.2, +14.4], 21 sit. | ✔ |
| gemma4 | ▼ | -7.0 [-13.4, -0.6] | no publicable | falla 4 (P2 P3 P5 P6); cae sin anthropic, openai | — | ✘ |
| google/gemini-3.7-flash | ▼ | -15.4 [-23.9, -6.5] | frágil | falla P3 | — | ✘ |
| openai/gpt-5.6-luna | ▲ | +6.5 [+1.6, +11.5] | no publicable | falla 4 (P2 P3 P5 P6); cae sin qwen | — | ✘ |
| openai/gpt-6.1-sol#low | ▲ | +22.0 [+17.0, +26.9] | robusta | pasa P1–P3, P5, P6 | ▲ +15.0 [+9.2, +20.9], 18 sit. | ✔ |
| qwen3.6 | ▼ | -9.6 [-15.8, -3.6] | robusta | pasa P1–P3, P5, P6 | ▼ -5.9 [-11.6, -0.1], 22 sit. | ✔ |

| modelo | marca candidata, rasgo completo (nivel) | puntuación completa | puntuación escala |
|---|---|---|---|
| anthropic/claude-haiku-5.5 | ·  | 38 | 45 |
| anthropic/claude-opus-5.5#low | ·  | 43 | 55 |
| deepseek-v4-flash@2026-10-17 | ·  | 41 | 51 |
| deepseek/deepseek-v4-pro-0813 | ·  | 41 | 41 |
| gemma4 | ·  | 37 | 39 |
| glm5.3-flash | ·  | 40 | 46 |
| google/gemini-3.7-flash | ·  | 37 | 31 |
| google/gemini-4-argon | ·  | 40 | 44 |
| mimo-v2.6-flash | ·  | 39 | 41 |
| openai/gpt-5.6-luna | ·  | 40 | 51 |
| openai/gpt-6.1-sol#low | ▲ (robusta) | 46 | 66 |
| qwen3.6 | ·  | 38 | 36 |
| qwen3.8-flash | ·  | 39 | 42 |

Cambios de nivel en marcas de otros rasgos al cambiar la escala de H (por BH): openai/gpt-5.6-luna A▼: frágil → robusta; anthropic/claude-opus-5.5#low O▲: no publicable → sin marca candidata; gemma4 O▲: no publicable → sin marca candidata.

## Neuroticismo: escala final y marcas (R3, R4)

Escala final (21): SN1 (ansiedad, 74 %), P3N004 (ansiedad, 62 %), P3N008 (ansiedad, 97 %), P3N009 (ansiedad, 68 %), P1N20 (autoconciencia, 83 %), P3N048 (autoconciencia, 52 %), P1N24 (autoconciencia, 72 %), P1N14 (depresion, 73 %), P3N033 (depresion, 51 %), P3N035 (depresion, 68 %), P1N13 (depresion, 53 %), P1N17 (depresion, 73 %), P1N09 (hostilidad, 90 %), P3N013 (hostilidad, 52 %), P3N098 (hostilidad, 98 %), P1N08 (hostilidad, 55 %), P1N12 (hostilidad, 54 %), P3N015 (hostilidad, 60 %), P1N34 (vulnerabilidad, 88 %), P3N071 (vulnerabilidad, 54 %), P1N32 (vulnerabilidad, 67 %).

Facetas sin situaciones: impulsividad; con una sola: ninguna.

G4 de la escala final con los 13 modelos (NO es validación, §30.2 R4): 0.83; G3 dentro/fuera: +0.45 / -0.08.

| modelo | marca | dif [IC] | nivel (§28) | por qué | R4: sin el modelo | publicable |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | ▲ | +14.7 [+7.5, +21.8] | robusta | pasa P1–P3, P5, P6 | ▲ +8.5 [+2.6, +14.9], 22 sit. | ✔ |
| anthropic/claude-opus-5.5#low | ▼ | -7.2 [-14.2, -0.8] | no publicable | falla P2 P3 P5 P6; cae sin anthropic, openai, qwen | — | ✘ |
| gemma4 | ▲ | +10.8 [+3.9, +17.8] | frágil | falla P3 | — | ✘ |
| glm5.3-flash | ▼ | -7.2 [-13.6, -0.5] | no publicable | falla P2 P3 P5 P6; cae sin qwen | — | ✘ |
| google/gemini-3.7-flash | ▼ | -21.4 [-28.1, -14.7] | robusta | pasa P1–P3, P5, P6 | · -6.1 [-14.8, +3.1], 23 sit. | ✘ |
| qwen3.6 | ▲ | +8.2 [+2.6, +14.1] | frágil | falla P2 P3 | — | ✘ |

| modelo | marca candidata, rasgo completo (nivel) | puntuación completa | puntuación escala |
|---|---|---|---|
| anthropic/claude-haiku-5.5 | ▲ (frágil) | 56 | 68 |
| anthropic/claude-opus-5.5#low | ·  | 49 | 47 |
| deepseek-v4-flash@2026-10-17 | ·  | 51 | 58 |
| deepseek/deepseek-v4-pro-0813 | ▼ (no publicable) | 47 | 48 |
| gemma4 | ·  | 54 | 64 |
| glm5.3-flash | ▼ (no publicable) | 47 | 47 |
| google/gemini-3.7-flash | ·  | 48 | 34 |
| google/gemini-4-argon | ·  | 52 | 53 |
| mimo-v2.6-flash | ·  | 51 | 55 |
| openai/gpt-5.6-luna | ·  | 52 | 58 |
| openai/gpt-6.1-sol#low | ·  | 49 | 54 |
| qwen3.6 | ·  | 54 | 62 |
| qwen3.8-flash | ·  | 50 | 56 |

Cambios de nivel en marcas de otros rasgos al cambiar la escala de N (por BH): openai/gpt-5.6-luna A▼: frágil → robusta; gemma4 O▲: no publicable → sin marca candidata.
