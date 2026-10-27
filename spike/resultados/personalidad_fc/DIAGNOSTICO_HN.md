# Diagnóstico de H y N con la conducta comparada (PERSONALIDAD.md §30)

Generado por `diagnosticar_hn_v3.py`. 13 modelos del banco v3; elección bruta (§28). Semilla 20261010. Sin llamadas a modelos. Escala del cuadro (×50).

## 1. Señal, ruido y consistencia por rasgo

| rasgo | sd entre modelos | ruido por situación | alfa | G4 pares/impares | G4 en 2.000 particiones: mediana [p5, p95] | % particiones ≥ 0,70 |
|---|---|---|---|---|---|---|
| O | 5.2 | 14.7 | 0.88 | 0.94 | 0.90 [0.81, 0.96] | 100 % |
| C | 2.8 | 12.7 | 0.73 | 0.81 | 0.76 [0.51, 0.89] | 70 % |
| E | 4.1 | 13.4 | 0.84 | 0.93 | 0.88 [0.75, 0.95] | 98 % |
| A | 4.6 | 12.6 | 0.89 | 0.86 | 0.92 [0.81, 0.97] | 100 % |
| N | 2.0 | 14.2 | 0.53 | 0.62 | 0.62 [0.23, 0.83] | 29 % |
| H | 1.8 | 13.4 | 0.51 | 0.13 | 0.60 [0.18, 0.84] | 28 % |

## 2. Techo, suelo e ítem-resto (elección bruta)

| rasgo | elección media | % ítems media < 0,10 | % > 0,90 | % sd entre modelos < 0,10 | % sin varianza | r ítem-resto media | % r < 0 | % r ≥ 0,20 |
|---|---|---|---|---|---|---|---|---|
| O | 0.60 | 5 | 27 | 14 | 5 | +0.35 | 8 | 68 |
| C | 0.22 | 48 | 4 | 30 | 21 | +0.22 | 18 | 45 |
| E | 0.32 | 30 | 9 | 16 | 7 | +0.28 | 28 | 44 |
| A | 0.24 | 47 | 5 | 23 | 21 | +0.40 | 7 | 60 |
| N | 0.51 | 19 | 23 | 26 | 18 | +0.14 | 23 | 40 |
| H | 0.39 | 32 | 10 | 22 | 19 | +0.11 | 27 | 36 |

## 3. Ajustada (e − d_m) frente a comparada (e)

La puntuación ajustada resta a la elección la deseabilidad propia d_m(i). Su varianza entre modelos es la de la elección, más la de la deseabilidad, menos dos veces su covarianza.

| rasgo | G4 comparada (e) | G4 ajustada (e − d_m) | G4 de d_m sola | mediana particiones: e / e − d_m / d_m | sd entre modelos: e / e − d_m / d_m | r(elección media, deseab. media) |
|---|---|---|---|---|---|---|
| O | 0.94 | 0.90 | 0.84 | 0.90 / 0.86 / 0.86 | 5.2 / 5.3 / 4.7 | +0.41 |
| C | 0.81 | 0.81 | 0.69 | 0.76 / 0.88 / 0.89 | 2.8 / 5.8 / 5.8 | +0.26 |
| E | 0.93 | 0.36 | 0.48 | 0.88 / 0.66 / 0.83 | 4.1 / 2.9 / 4.4 | +0.69 |
| A | 0.86 | 0.78 | 0.71 | 0.92 / 0.81 / 0.70 | 4.6 / 4.5 / 3.2 | +0.35 |
| N | 0.62 | 0.17 | 0.51 | 0.62 / 0.37 / 0.54 | 2.0 / 1.5 / 2.3 | +0.58 |
| H | 0.13 | 0.91 | 0.85 | 0.60 / 0.90 / 0.93 | 1.8 / 6.0 / 6.9 | +0.47 |

## 4. Facetas

sd = sd real entre modelos de la faceta; r resto = correlación entre modelos de la faceta con el resto del rasgo; carga cruzada = rasgo ajeno con el que más correlaciona.

| rasgo | faceta | n | elección media | sd | alfa | r resto del rasgo | ítem-resto medio | carga cruzada |
|---|---|---|---|---|---|---|---|---|
| O | acciones | 10 | 0.54 | 8.3 | +0.73 | +0.77 | +0.47 | C +0.43 |
| O | estetica | 10 | 0.49 | 6.8 | +0.68 | +0.59 | +0.38 | A -0.67 |
| O | fantasia | 10 | 0.70 | 4.0 | +0.50 | +0.60 | +0.33 | E -0.32 |
| O | ideas | 10 | 0.41 | 4.7 | +0.47 | +0.37 | +0.19 | H +0.62 |
| O | sentimientos | 10 | 0.65 | 8.2 | +0.79 | +0.67 | +0.47 | E -0.77 |
| O | valores | 9 | 0.82 | 1.2 | +0.07 | +0.68 | +0.29 | A -0.54 |
| C | autodisciplina | 9 | 0.19 | 2.8 | +0.38 | +0.01 | +0.11 | E -0.52 |
| C | competencia | 10 | 0.21 | 1.2 | +0.08 | +0.33 | +0.12 | E +0.65 |
| C | deliberacion | 10 | 0.24 | 3.6 | +0.51 | +0.78 | +0.26 | H -0.52 |
| C | logro | 9 | 0.18 | 6.1 | +0.72 | +0.43 | +0.39 | H -0.59 |
| C | orden | 9 | 0.35 | 3.9 | +0.35 | +0.72 | +0.28 | H -0.74 |
| C | sentido_del_deber | 9 | 0.17 | 0.0 | -2.09 | +0.38 | +0.05 | A -0.49 |
| E | actividad | 9 | 0.18 | 6.7 | +0.75 | +0.59 | +0.44 | O -0.72 |
| E | asertividad | 9 | 0.62 | 5.5 | +0.57 | -0.14 | -0.02 | C -0.54 |
| E | busqueda_de_emociones | 10 | 0.44 | 0.0 | -0.60 | +0.15 | -0.04 | A +0.23 |
| E | cordialidad | 10 | 0.16 | 4.5 | +0.59 | +0.84 | +0.38 | A +0.69 |
| E | emociones_positivas | 9 | 0.35 | 5.2 | +0.59 | +0.73 | +0.38 | H -0.68 |
| E | gregarismo | 10 | 0.21 | 9.3 | +0.86 | +0.55 | +0.51 | A +0.84 |
| A | altruismo | 10 | 0.12 | 3.5 | +0.53 | +0.76 | +0.40 | N -0.71 |
| A | confianza | 10 | 0.17 | 6.2 | +0.66 | +0.76 | +0.48 | E +0.85 |
| A | cooperacion | 9 | 0.27 | 5.3 | +0.71 | +0.80 | +0.54 | E +0.82 |
| A | modestia | 9 | 0.35 | 4.6 | +0.47 | +0.32 | +0.18 | N -0.46 |
| A | perdon_paciencia | 10 | 0.30 | 6.9 | +0.73 | +0.87 | +0.49 | N -0.67 |
| A | sensibilidad | 9 | 0.25 | 0.0 | -0.56 | +0.71 | +0.24 | O -0.64 |
| N | ansiedad | 9 | 0.23 | 4.8 | +0.48 | +0.31 | +0.17 | C +0.64 |
| N | autoconciencia | 9 | 0.44 | 0.6 | +0.02 | +0.18 | +0.12 | H -0.35 |
| N | depresion | 9 | 0.53 | 3.9 | +0.48 | +0.22 | +0.20 | A -0.77 |
| N | hostilidad | 10 | 0.62 | 5.8 | +0.59 | +0.35 | +0.28 | A -0.68 |
| N | impulsividad | 10 | 0.35 | 5.0 | +0.54 | -0.54 | -0.22 | O -0.69 |
| N | vulnerabilidad | 10 | 0.84 | 4.8 | +0.63 | +0.17 | +0.29 | A -0.64 |
| H | desinteres_riqueza | 15 | 0.45 | 2.3 | +0.42 | +0.60 | +0.28 | C -0.63 |
| H | equidad | 14 | 0.22 | 0.0 | -1.02 | -0.43 | -0.14 | E +0.80 |
| H | modestia | 15 | 0.26 | 1.6 | +0.18 | -0.33 | -0.09 | A +0.75 |
| H | sinceridad | 15 | 0.60 | 8.5 | +0.86 | -0.17 | +0.40 | E -0.72 |

### Correlación entre facetas de Honestidad-Humildad (entre modelos)

| | desinteres | equidad | modestia | sinceridad |
|---|---|---|---|---|
| desinteres_riqueza | 1 | -0.07 | -0.11 | +0.55 |
| equidad | -0.07 | 1 | +0.20 | -0.55 |
| modestia | -0.11 | +0.20 | 1 | -0.40 |
| sinceridad | +0.55 | -0.55 | -0.40 | 1 |

### Correlación entre facetas de Neuroticismo (entre modelos)

| | ansiedad | autoconcie | depresion | hostilidad | impulsivid | vulnerabil |
|---|---|---|---|---|---|---|
| ansiedad | 1 | +0.29 | +0.16 | +0.43 | -0.11 | -0.09 |
| autoconciencia | +0.29 | 1 | -0.05 | +0.01 | +0.20 | -0.06 |
| depresion | +0.16 | -0.05 | 1 | +0.44 | -0.51 | +0.39 |
| hostilidad | +0.43 | +0.01 | +0.44 | 1 | -0.62 | +0.55 |
| impulsividad | -0.11 | +0.20 | -0.51 | -0.62 | 1 | -0.45 |
| vulnerabilidad | -0.09 | -0.06 | +0.39 | +0.55 | -0.45 | 1 |

## 5. Perfil por modelo en H y N (×50)

| modelo | H elección | H deseab. propia | N elección | N deseab. propia |
|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 17.4 | 41.5 | 30.5 | 25.0 |
| anthropic/claude-opus-5.5#low | 22.2 | 36.4 | 23.9 | 21.9 |
| deepseek-v4-flash@2026-10-17 | 20.6 | 24.6 | 25.4 | 23.2 |
| deepseek/deepseek-v4-pro-0813 | 20.1 | 27.5 | 21.3 | 21.9 |
| gemma4 | 16.5 | 23.3 | 28.3 | 25.4 |
| glm5.3-flash | 19.7 | 34.3 | 21.9 | 19.7 |
| google/gemini-3.7-flash | 16.3 | 21.6 | 22.6 | 22.4 |
| google/gemini-4-argon | 19.1 | 33.9 | 27.0 | 26.3 |
| mimo-v2.6-flash | 18.4 | 23.7 | 25.7 | 23.2 |
| openai/gpt-5.6-luna | 19.5 | 33.1 | 26.8 | 29.8 |
| openai/gpt-6.1-sol#low | 25.4 | 36.0 | 23.2 | 28.1 |
| qwen3.6 | 17.2 | 16.5 | 28.3 | 30.7 |
| qwen3.8-flash | 18.2 | 32.2 | 25.0 | 22.8 |
