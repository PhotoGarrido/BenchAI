# Prueba de discriminación (§10)

Modelos: anthropic_claude-haiku-5.5, deepseek-v4-flash, gemma4, glm5.3-flash, google_gemini-3.7-flash, mimo-v2.6-flash, openai_gpt-5.6-luna, qwen3.6, qwen3.8-flash. Criterios fijados antes de ver los datos de los 3 modelos nuevos.

## Criterios

- **D1** R3 ajustada discrimina (cociente ≥ 2) en ≥ 3 rasgos: O 2.1, C 2.6, E 1.6, A 2.2, N 2.1, H 2.5 → **CUMPLE**.
- **D2** Luna vs Gemini 3.7 Flash (Gemini − Luna, R3 ajustada) separa ≥ 2 rasgos: O 3 [-6–12], C 8 [1–15], E 2 [-8–12], A 8 [-2–16], N 2 [-4–8], H 5 [-4–15] → **NO cumple**.
- **D3** |r(aquiescencia, elección forzada)| < 0,5 en C y N: C -0.29, N 0.84 (Likert: -0.80, 0.84) → **NO cumple**.
- **D4** elección forzada converge con R3 ajustada mejor que el Likert en ≥ 4 rasgos: 2/6 → **NO cumple**.
- **H1** con 9 modelos: +5.5 pp [IC +3.6, +7.4], dirección en 9/9 → **CUMPLE**.

## Por rasgo (correlaciones entre modelos)

| rasgo | r(aq, FC) | r(aq, Likert) | r(FC, R3aj) | r(Likert, R3aj) | r(anclado, R3aj) | discrimina FC | discrimina R3aj | r(ISS, R3aj) | r(ISS, FC) | r(ISS, Likert) |
|---|---|---|---|---|---|---|---|---|---|---|
| O | 0.63 | 0.47 | 0.10 | 0.11 | 0.22 | 2.1 | 2.1 | -0.00 | 0.11 | -0.28 |
| C | -0.29 | -0.80 | 0.21 | 0.27 | 0.33 | 1.5 | 2.6 | 0.46 | 0.36 | 0.52 |
| E | 0.41 | 0.16 | 0.10 | 0.59 | 0.75 | 2.1 | 1.6 | 0.14 | -0.26 | -0.03 |
| A | 0.72 | 0.73 | 0.13 | 0.25 | 0.39 | 1.4 | 2.2 | 0.37 | 0.02 | -0.10 |
| N | 0.84 | 0.84 | 0.25 | 0.14 | 0.03 | 2.3 | 2.1 | -0.13 | -0.13 | -0.37 |
| H | 0.19 | -0.46 | -0.45 | -0.59 | -0.62 | 2.1 | 2.5 | 0.50 | -0.48 | 0.23 |

## Perfiles por modelo

| modelo | ISS | O Likert / FC / R3aj | C Likert / FC / R3aj | E Likert / FC / R3aj | A Likert / FC / R3aj | N Likert / FC / R3aj | H Likert / FC / R3aj |
|---|---|---|---|---|---|---|---|
| anthropic_claude-haiku-5.5 | 10.3 | 66 / 45 / 44 | 78 / 35 / 30 | 44 / 32 / 34 | 82 / 44 / 28 | 22 / 38 / 63 | 94 / 67 / 33 |
| deepseek-v4-flash | 43.6 | 72 / 80 / 39 | 71 / 48 / 32 | 51 / 22 / 39 | 93 / 65 / 34 | 46 / 68 / 62 | 85 / 52 / 51 |
| gemma4 | 28.1 | 71 / 78 / 57 | 92 / 50 / 36 | 61 / 20 / 43 | 78 / 44 / 32 | 18 / 32 / 58 | 78 / 39 / 43 |
| glm5.3-flash | 28.9 | 64 / 55 / 52 | 79 / 25 / 38 | 33 / 25 / 34 | 78 / 60 / 29 | 10 / 38 / 56 | 96 / 68 / 37 |
| google_gemini-3.7-flash | 55.2 | 56 / 55 / 48 | 92 / 45 / 48 | 46 / 20 / 38 | 76 / 42 / 43 | 8 / 28 / 52 | 94 / 55 / 47 |
| mimo-v2.6-flash | 12.6 | 73 / 72 / 46 | 67 / 22 / 32 | 44 / 32 / 40 | 87 / 58 / 39 | 36 / 50 / 59 | 81 / 75 / 42 |
| openai_gpt-5.6-luna | 7.6 | 65 / 65 / 44 | 69 / 48 / 40 | 54 / 18 / 36 | 81 / 48 / 36 | 41 / 48 / 50 | 84 / 65 / 41 |
| qwen3.6 | 23.2 | 77 / 72 / 55 | 68 / 32 / 45 | 59 / 50 / 34 | 93 / 68 / 39 | 38 / 58 / 55 | 81 / 50 / 51 |
| qwen3.8-flash | 24.8 | 88 / 70 / 48 | 84 / 38 / 38 | 62 / 45 / 47 | 97 / 65 / 38 | 26 / 58 / 58 | 97 / 55 / 34 |
