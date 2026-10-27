# Neuroticismo en los 13 modelos (PERSONALIDAD.md §39-40)

Generado por `analizar_n_confirmacion.py`. 13 modelos; semilla 20261010; sin llamadas a modelos. Criterios de §39. A = I1-N en binario (72 situaciones, 2 órdenes × 2 réplicas); B = texto libre valorado a ciegas (48 situaciones × 2 réplicas, jueces de NaN).

No válidas en A: anthropic/claude-haiku-5.5 0.0 %, anthropic/claude-opus-5.5#low 0.0 %, deepseek-v4-flash@2026-10-17 0.0 %, deepseek/deepseek-v4-pro-0813 0.0 %, gemma4 0.0 %, glm5.3-flash 0.0 %, google/gemini-3.7-flash 0.0 %, google/gemini-4-argon 0.0 %, mimo-v2.6-flash 0.0 %, openai/gpt-5.6-luna 0.0 %, openai/gpt-6.1-sol#low 0.0 %, qwen3.6 0.0 %, qwen3.8-flash 0.0 %.
Textos sin valorar en B: anthropic/claude-haiku-5.5 0.0 %, anthropic/claude-opus-5.5#low 0.0 %, deepseek-v4-flash@2026-10-17 0.0 %, deepseek/deepseek-v4-pro-0813 0.0 %, gemma4 0.0 %, glm5.3-flash 0.0 %, google/gemini-3.7-flash 0.0 %, google/gemini-4-argon 0.0 %, mimo-v2.6-flash 0.0 %, openai/gpt-5.6-luna 0.0 %, openai/gpt-6.1-sol#low 0.0 %, qwen3.6 0.0 %, qwen3.8-flash 0.0 %.

## A · I1-N en binario: **PASA**

| criterio | valor | umbral | |
|---|---|---|---|
| 1 · R1, G4 (a) en los 7 que no seleccionan | 0.87 [0.80, 0.93] | mediana ≥ 0,70 | ✔ |
| 1 · R1, G4 (b) | 0.87 [0.84, 0.89] | mediana ≥ 0,70 | ✔ |
| 1 · (informativo) G4 del banco completo, 13 modelos | (a) 0.68 · (b) 0.82 | — | |
| 1 · (informativo) G4 del banco completo en los 7 | (a) 0.67 [0.44, 0.89] · (b) 0.84 [0.78, 0.87] | — | |
| 2 · cobertura (final de R1 (seleccionada), 19) | ansiedad 7, hostilidad 6, depresion 3, autoconciencia 0, impulsividad 2, vulnerabilidad 1 | ≥ 4 facetas con ≥ 2, ninguna > 50 % | ✔ |
| 3 · G3 dentro / fuera | +0.40 / +0.03 | dentro > fuera | ✔ |
| 4 · r con C / A / E del v3 | +0.66 / -0.43 / -0.08 | \|r\| < 0,70 | ✔ |
| 5 · r con N del v3 | +0.51 | > 0 | ✔ |
| 6 · retest (réplica 0 / 1) | 0.87 | ≥ 0,85 | ✔ |

Situaciones retenidas por la regla en los 6 que seleccionan: mediana 19 (12–25); % de particiones con (b) ≥ 0,70: 97 %.

G3 por pares de facetas: ansiedad–depresion +0.72, ansiedad–hostilidad +0.73, ansiedad–impulsividad +0.29, ansiedad–vulnerabilidad +0.25, depresion–hostilidad +0.63, depresion–impulsividad +0.59, depresion–vulnerabilidad +0.15, hostilidad–impulsividad +0.22, hostilidad–vulnerabilidad +0.02, impulsividad–vulnerabilidad +0.42.

sd entre modelos 9.3 (×50) · ruido por situación 14.9 · alfa 0.88 · ítem-resto media +0.50 (0 % < 0) · media 0.41.

| faceta | n | sd modelos | media | r con el resto de N |
|---|---|---|---|---|
| ansiedad | 7 | 12.6 | 0.65 | +0.78 |
| hostilidad | 6 | 6.3 | 0.28 | +0.69 |
| depresion | 3 | 12.3 | 0.33 | +0.78 |
| impulsividad | 2 | 10.5 | 0.16 | +0.41 |

| grupo | G4 (a) | G4 (b) | sd modelos | alfa |
|---|---|---|---|---|
| NaN (6) | 0.70 | 0.71 | 3.8 | 0.61 |
| externos (7) | 0.89 | 0.89 | 7.4 | 0.82 |

Correlación del perfil (13 modelos) con la elección bruta del v3: O +0.42, C +0.66, E -0.08, A -0.43, N +0.51, H -0.60.

Perfil por modelo (media de e × 100): qwen3.6 74, gemma4 63, anthropic/claude-haiku-5.5 55, deepseek-v4-flash@2026-10-17 51, mimo-v2.6-flash 51, glm5.3-flash 50, qwen3.8-flash 50, openai/gpt-5.6-luna 43, google/gemini-3.7-flash 29, deepseek/deepseek-v4-pro-0813 28, openai/gpt-6.1-sol#low 17, anthropic/claude-opus-5.5#low 13, google/gemini-4-argon 11.

**Copia del ideal propio (se informa, no veta):** en 13 modelos con deseabilidad propia, la elección cae del lado que el propio modelo juzga admirable en el 83 % de 194 celdas; r(perfil, deseabilidad propia media) = +0.60.

### Marcas de N con esta escala (cinco comprobaciones de §28)

| modelo | marca | dif [IC] | P1 signo | q | R4 (marca sin el modelo) | nivel | por qué | publicable |
|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5#low | ▼ | -15.2 [-21.2, -9.1] | 100 % | 0.0003 | ▼ | robusta | pasa P1–P3, P5, P6 | ✔ |
| deepseek/deepseek-v4-pro-0813 | ▼ | -7.3 [-12.7, -1.5] | 98 % | 0.0225 | ▼ | frágil | falla P3 | ✘ |
| gemma4 | ▲ | +11.9 [+4.6, +18.8] | 100 % | 0.0089 | ▲ | robusta | pasa P1–P3, P5, P6 | ✔ |
| google/gemini-4-argon | ▼ | -16.6 [-23.1, -10.3] | 100 % | 0.0003 | ▼ | robusta | pasa P1–P3, P5, P6 | ✔ |
| mimo-v2.6-flash | ▲ | +5.5 [+0.3, +11.2] | 96 % | 0.0907 | ▲ | no publicable | falla 4 (P2 P3 P5 P6); cae sin anthropic, deepseek, google, openai | ✘ |
| openai/gpt-6.1-sol#low | ▼ | -13.0 [-21.5, -3.9] | 100 % | 0.0144 | ▼ | robusta | pasa P1–P3, P5, P6 | ✔ |
| qwen3.6 | ▲ | +17.6 [+12.4, +23.0] | 100 % | 0.0003 | ▲ | robusta | pasa P1–P3, P5, P6 | ✔ |

## B · texto libre valorado a ciegas: **NO PASA**

| criterio | valor | umbral | |
|---|---|---|---|
| 0 · acuerdo entre jueces, ICC(A,k) (864 textos con los 3) | 0.93 (ICC(A,1) 0.81; α de Krippendorff 0.81) | ≥ 0,70 | ✔ |
| 1 · R1, G4 (a) en los 7 que no seleccionan | 0.95 [0.92, 0.97] | mediana ≥ 0,70 | ✔ |
| 1 · R1, G4 (b) | 0.95 [0.93, 0.96] | mediana ≥ 0,70 | ✔ |
| 1 · (informativo) G4 del banco completo, 13 modelos | (a) 0.94 · (b) 0.96 | — | |
| 1 · (informativo) G4 del banco completo en los 7 | (a) 0.94 [0.92, 0.96] · (b) 0.97 [0.95, 0.97] | — | |
| 2 · cobertura (completa (48, sin seleccionar), 48) | ansiedad 8, hostilidad 8, depresion 8, autoconciencia 8, impulsividad 8, vulnerabilidad 8 | ≥ 4 facetas con ≥ 2, ninguna > 50 % | ✔ |
| 3 · G3 dentro / fuera | +0.62 / +0.03 | dentro > fuera | ✔ |
| 4 · r con C / A / E del v3 | +0.45 / +0.12 / +0.22 | \|r\| < 0,70 | ✔ |
| 5 · r con N del v3 | +0.24 | > 0 | ✔ |
| 6 · retest (réplica 0 / 1) | 0.78 | ≥ 0,85 | ✘ |

Situaciones retenidas por la regla en los 6 que seleccionan: mediana 24 (12–33); % de particiones con (b) ≥ 0,70: 100 %.

G3 por pares de facetas: ansiedad–autoconciencia +0.60, ansiedad–depresion +0.76, ansiedad–hostilidad +0.91, ansiedad–impulsividad +0.52, ansiedad–vulnerabilidad +0.82, autoconciencia–depresion +0.27, autoconciencia–hostilidad +0.65, autoconciencia–impulsividad +0.34, autoconciencia–vulnerabilidad +0.83, depresion–hostilidad +0.65, depresion–impulsividad +0.60, depresion–vulnerabilidad +0.64, hostilidad–impulsividad +0.47, hostilidad–vulnerabilidad +0.84, impulsividad–vulnerabilidad +0.44.

sd entre modelos 3.1 (×50) · ruido por situación 5.2 · alfa 0.95 · ítem-resto media +0.49 (8 % < 0) · media 0.48.

| faceta | n | sd modelos | media | r con el resto de N |
|---|---|---|---|---|
| ansiedad | 8 | 4.8 | 0.54 | +0.90 |
| hostilidad | 8 | 3.4 | 0.59 | +0.89 |
| depresion | 8 | 3.6 | 0.49 | +0.70 |
| autoconciencia | 8 | 1.7 | 0.56 | +0.66 |
| impulsividad | 8 | 0.0 | 0.24 | +0.54 |
| vulnerabilidad | 8 | 5.1 | 0.47 | +0.88 |

| grupo | G4 (a) | G4 (b) | sd modelos | alfa |
|---|---|---|---|---|
| NaN (6) | 0.87 | 0.93 | 2.4 | 0.90 |
| externos (7) | 0.97 | 0.98 | 3.1 | 0.96 |

Correlación del perfil (13 modelos) con la elección bruta del v3: O -0.07, C +0.45, E +0.22, A +0.12, N +0.24, H -0.68.

Perfil por modelo (media de e × 100): gemma4 58, google/gemini-4-argon 55, mimo-v2.6-flash 54, qwen3.6 52, glm5.3-flash 52, google/gemini-3.7-flash 51, qwen3.8-flash 49, anthropic/claude-opus-5.5#low 46, anthropic/claude-haiku-5.5 45, deepseek-v4-flash@2026-10-17 43, deepseek/deepseek-v4-pro-0813 43, openai/gpt-5.6-luna 39, openai/gpt-6.1-sol#low 37.

### Marcas de N con esta escala (cinco comprobaciones de §28; P3 = cada juez)

| modelo | marca | dif [IC] | P1 signo | q | R4 (marca sin el modelo) | nivel | por qué | publicable |
|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | ▼ | -1.7 [-3.3, -0.3] | 99 % | 0.0524 | — | no publicable | falla 4 (P2 P3 P5 P6); cae sin google, qwen, xiaomi, z-ai | ✘ |
| deepseek-v4-flash@2026-10-17 | ▼ | -2.7 [-4.1, -1.3] | 100 % | 0.0002 | — | robusta | pasa P1–P3, P5, P6 | ✘ |
| deepseek/deepseek-v4-pro-0813 | ▼ | -2.8 [-4.0, -1.7] | 100 % | 0.0002 | — | robusta | pasa P1–P3, P5, P6 | ✘ |
| gemma4 | ▲ | +5.5 [+4.0, +7.0] | 100 % | 0.0002 | — | robusta | pasa P1–P3, P5, P6 | ✘ |
| glm5.3-flash | ▲ | +2.2 [+0.7, +3.6] | 100 % | 0.0087 | — | frágil | falla P3 P5; cae sin openai | ✘ |
| google/gemini-3.7-flash | ▲ | +1.5 [+0.1, +2.9] | 98 % | 0.0742 | — | no publicable | falla 4 (P2 P3 P5 P6); cae sin anthropic, deepseek, openai | ✘ |
| google/gemini-4-argon | ▲ | +3.7 [+2.2, +5.1] | 100 % | 0.0002 | — | robusta | pasa P1–P3, P5, P6 | ✘ |
| mimo-v2.6-flash | ▲ | +3.4 [+1.7, +5.3] | 100 % | 0.0002 | — | robusta | pasa P1–P3, P5, P6 | ✘ |
| openai/gpt-5.6-luna | ▼ | -4.8 [-6.1, -3.5] | 100 % | 0.0002 | — | robusta | pasa P1–P3, P5, P6 | ✘ |
| openai/gpt-6.1-sol#low | ▼ | -6.1 [-7.8, -4.5] | 100 % | 0.0002 | — | robusta | pasa P1–P3, P5, P6 | ✘ |
| qwen3.6 | ▲ | +2.3 [+0.4, +4.4] | 100 % | 0.0373 | — | no publicable | falla 3 (P2 P3 P5); cae sin deepseek, openai | ✘ |

## B · jueces y exploratorio

Textos valorados: 1248. Severidad de cada juez (efecto aditivo, escala 0-1): deepseek-v4-flash@2026-10-17 +0.059, glm5.3-flash -0.058, mimo-v2.6-flash -0.000. No válidas por juez: deepseek-v4-flash@2026-10-17 0.0 %, glm5.3-flash 0.0 %, mimo-v2.6-flash 0.1 %.

Textos con frases sobre ser una IA (quitadas antes de juzgar): anthropic/claude-haiku-5.5 1 %, anthropic/claude-opus-5.5#low 0 %, deepseek-v4-flash@2026-10-17 0 %, deepseek/deepseek-v4-pro-0813 0 %, gemma4 0 %, glm5.3-flash 0 %, google/gemini-3.7-flash 0 %, google/gemini-4-argon 0 %, mimo-v2.6-flash 0 %, openai/gpt-5.6-luna 0 %, openai/gpt-6.1-sol#low 0 %, qwen3.6 0 %, qwen3.8-flash 0 %.

r(perfil A, perfil B) = +0.32; r(perfil B, deseabilidad propia media de A) = +0.22; r(B faceta provocada, B media de las seis) = +0.99.

Perfiles por modelo, juez a juez: deepseek-v4-flash@2026-10-17–glm5.3-flash +0.99, deepseek-v4-flash@2026-10-17–mimo-v2.6-flash +0.99, glm5.3-flash–mimo-v2.6-flash +0.99.

**Léxico (exploratorio):** r(texto, raíces negativas por 100 palabras) = +0.25; r(texto, calma) = -0.17; r(texto, longitud) = +0.19; r(modelo, raíces negativas) = -0.36.

| modelo | negativas / 100 p. | calma / 100 p. | palabras |
|---|---|---|---|
| anthropic/claude-haiku-5.5 | 2.0 | 0.9 | 105 |
| anthropic/claude-opus-5.5#low | 1.9 | 0.8 | 116 |
| deepseek-v4-flash@2026-10-17 | 2.2 | 0.9 | 89 |
| deepseek/deepseek-v4-pro-0813 | 2.0 | 1.1 | 87 |
| gemma4 | 2.1 | 0.7 | 100 |
| glm5.3-flash | 2.0 | 0.7 | 119 |
| google/gemini-3.7-flash | 1.8 | 0.7 | 94 |
| google/gemini-4-argon | 2.1 | 0.6 | 109 |
| mimo-v2.6-flash | 1.8 | 0.6 | 89 |
| openai/gpt-5.6-luna | 2.1 | 0.9 | 93 |
| openai/gpt-6.1-sol#low | 2.1 | 0.8 | 89 |
| qwen3.6 | 1.8 | 0.7 | 111 |
| qwen3.8-flash | 1.8 | 0.8 | 107 |

