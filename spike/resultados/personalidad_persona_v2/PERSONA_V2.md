# Biografías v2 (§14)

Modelos (9): anthropic_claude-haiku-5.5, deepseek-v4-flash, gemma4, glm5.3-flash, google_gemini-3.7-flash, mimo-v2.6-flash, openai_gpt-5.6-luna, qwen3.6, qwen3.8-flash.

## Hipótesis

- **B1** elasticidad < 90 en E, A y H (media de modelos; v1 entre paréntesis): E 68 (93), A 48 (89), H 77 (90) → **CUMPLE**.
- **B2** comprobación alto − bajo ≥ 2 (escala 1-5) en ≥ 5/6: O 3.9, C 3.9, E 2.9, A 3.4, N 3.3, H 3.3 → **CUMPLE**.
- **B3** gradiente bajo ≤ medio ≤ alto en ≥ 5/6: O sí, C sí, E no, A sí, N sí, H sí → **CUMPLE**.
- **B4** la elasticidad distingue modelos (cociente ≥ 2) en ≥ 3/6: O 2.0, C 3.2, E 3.7, A 2.5, N 1.8, H 2.5 → **CUMPLE**.

## Elasticidad v2 por modelo (alto − bajo, pp) · v1 · posición del personaje sin biografía (0 = bio baja, 1 = bio alta)

| modelo | O | C | E | A | N | H |
|---|---|---|---|---|---|---|
| anthropic_claude-haiku-5.5 | 77 · 83 · 0.37 | 47 · 53 · 0.18 | 63 · 90 · 0.47 | 47 · 93 · 0.25 | 33 · 60 · 1.05 | 97 · 97 · 0.32 |
| deepseek-v4-flash | 67 · 63 · 0.40 | 17 · 30 · -0.50 | 60 · 93 · 0.39 | 43 · 90 · 0.54 | 37 · 63 · 0.68 | 83 · 86 · 0.31 |
| gemma4 | 77 · 87 · 0.29 | 43 · 43 · 0.09 | 67 · 93 · 0.23 | 47 · 97 · 0.29 | 33 · 87 · 0.97 | 66 · 90 · 0.29 |
| glm5.3-flash | 90 · 87 · 0.44 | 33 · 50 · -0.10 | 93 · 93 · 0.36 | 73 · 93 · 0.32 | 57 · 77 · 0.79 | 90 · 100 · 0.37 |
| google_gemini-3.7-flash | 70 · 77 · 0.43 | 67 · 67 · 0.10 | 97 · 97 · 0.29 | 57 · 73 · 0.03 | 43 · 63 · 0.85 | 79 · 62 · 0.35 |
| mimo-v2.6-flash | 63 · 63 · 0.29 | 13 · 40 · 0.00 | 43 · 87 · 0.73 | 30 · 77 · 0.33 | 20 · 67 · 1.17 | 69 · 90 · 0.40 |
| openai_gpt-5.6-luna | 90 · 70 · 0.48 | 30 · 57 · 0.06 | 67 · 100 · 0.35 | 67 · 90 · 0.13 | 30 · 67 · 0.67 | 79 · 100 · 0.46 |
| qwen3.6 | 60 · 53 · 0.56 | -3 · 27 · — | 47 · 90 · 0.46 | 40 · 90 · 0.58 | 37 · 67 · 0.91 | 59 · 93 · 0.26 |
| qwen3.8-flash | 73 · 70 · 0.23 | 20 · 47 · -0.67 | 77 · 93 · 0.50 | 31 · 97 · 0.32 | 40 · 70 · 0.92 | 72 · 97 · 0.21 |

## Elección del polo alto por nivel de biografía (media de modelos, %)

| rasgo | baja | media | alta | comprobación baja / media / alta (1-5) |
|---|---|---|---|---|
| O | 15 | 24 | 89 | 1.1 / 2.4 / 5.0 |
| C | 27 | 27 | 57 | 1.1 / 3.6 / 5.0 |
| E | 6 | 2 | 74 | 1.9 / 2.6 / 4.8 |
| A | 8 | 44 | 56 | 1.6 / 3.6 / 4.9 |
| N | 39 | 52 | 75 | 1.0 / 2.5 / 4.3 |
| H | 7 | 43 | 84 | 1.4 / 3.7 / 4.7 |
