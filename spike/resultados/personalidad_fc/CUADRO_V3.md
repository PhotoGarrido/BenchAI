# Cuadro de personalidad por modelo · v2

Generado por `analizar_v3.py` (PERSONALIDAD.md §21). Marco: Big Five (NEO-PI-R) + Honestidad-Humildad (HEXACO); O 59, C 56, E 57, A 57, N 57, H 59 situaciones por rasgo, repartidas por faceta.
**Puntuación** = lo que el modelo elige cuando decide él, ajustado por lo que él mismo juzga admirable (50 = elige su ideal). **▲/▼** = por encima/debajo de los demás modelos, comparación pareada situación a situación, IC 95 %.

| modelo | ISS | Apertura | Responsabilidad | Extraversión | Amabilidad | Neuroticismo | Honestidad-Humildad |
|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 10.3 | 46 ▼ | 31 ▼ | 42 | 25 ▼ | 55 ▲ | 26 ▼ |
| anthropic/claude-opus-5.5#low | 12.5 | 50 | 38 | 41 | 33 | 52 | 36 |
| deepseek-v4-flash@2026-10-17 | — | 49 | 36 | 41 | 38 | 52 | 46 ▲ |
| deepseek/deepseek-v4-pro-0813 | — | 51 | 36 | 43 | 36 | 49 | 43 |
| gemma4 | 28.1 | 62 ▲ | 40 | 48 ▲ | 33 | 53 | 43 |
| glm5.3-flash | 28.9 | 54 | 40 | 38 | 32 | 52 | 35 ▼ |
| google/gemini-3.7-flash | 55.2 | 47 ▼ | 51 ▲ | 45 | 47 ▲ | 50 | 45 ▲ |
| google/gemini-4-argon | — | 42 ▼ | 39 | 38 | 36 | 51 | 35 ▼ |
| mimo-v2.6-flash | 12.6 | 57 ▲ | 29 ▼ | 41 | 38 | 52 | 45 |
| openai/gpt-5.6-luna | 7.6 | 46 ▼ | 39 | 36 ▼ | 36 | 47 ▼ | 36 |
| openai/gpt-6.1-sol#low | 13.2 | 53 | 32 ▼ | 33 ▼ | 30 ▼ | 45 ▼ | 39 |
| qwen3.6 | 23.2 | 59 ▲ | 49 ▲ | 37 | 32 | 48 | 51 ▲ |
| qwen3.8-flash | 24.8 | 50 | 39 | 41 | 38 | 52 | 36 |

## Retrato de cada modelo

- **anthropic/claude-haiku-5.5**: **menos Apertura** (prefiere lo conocido); **menos Responsabilidad** (prioriza descanso y flexibilidad); **menos Amabilidad** (pone límites y se defiende); **más Neuroticismo** (reacciona, se preocupa); **menos Honestidad-Humildad** (acepta ventajas y se promociona).
- **anthropic/claude-opus-5.5#low**: perfil próximo al de los demás modelos en los seis rasgos.
- **deepseek-v4-flash@2026-10-17**: **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **deepseek/deepseek-v4-pro-0813**: perfil próximo al de los demás modelos en los seis rasgos.
- **gemma4**: **más Apertura** (curioso, busca lo nuevo); **más Extraversión** (busca gente y protagonismo).
- **glm5.3-flash**: **menos Honestidad-Humildad** (acepta ventajas y se promociona).
- **google/gemini-3.7-flash**: **menos Apertura** (prefiere lo conocido); **más Responsabilidad** (cumple y planifica); **más Amabilidad** (cede y coopera); **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **google/gemini-4-argon**: **menos Apertura** (prefiere lo conocido); **menos Honestidad-Humildad** (acepta ventajas y se promociona).
- **mimo-v2.6-flash**: **más Apertura** (curioso, busca lo nuevo); **menos Responsabilidad** (prioriza descanso y flexibilidad).
- **openai/gpt-5.6-luna**: **menos Apertura** (prefiere lo conocido); **menos Extraversión** (prefiere calma y segundo plano); **menos Neuroticismo** (se mantiene sereno).
- **openai/gpt-6.1-sol#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **menos Extraversión** (prefiere calma y segundo plano); **menos Amabilidad** (pone límites y se defiende); **menos Neuroticismo** (se mantiene sereno).
- **qwen3.6**: **más Apertura** (curioso, busca lo nuevo); **más Responsabilidad** (cumple y planifica); **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **qwen3.8-flash**: perfil próximo al de los demás modelos en los seis rasgos.

## Perfil por faceta (puntuación ajustada)

| modelo | A·altrui | A·confia | A·cooper | A·modest | A·perdon | A·sensib | C·autodi | C·compet | C·delibe | C·logro | C·orden | C·sentid | E·activi | E·aserti | E·busque | E·cordia | E·emocio | E·gregar | H·desint | H·equida | H·modest | H·sincer | N·ansied | N·autoco | N·depres | N·hostil | N·impuls | N·vulner | O·accion | O·esteti | O·fantas | O·ideas | O·sentim | O·valore |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 10 | 36 | 36 | 19 | 25 | 26 | 29 | 21 | 28 | 28 | 49 | 31 | 24 | 57 | 52 | 36 | 69 | 18 | 30 | 14 | 18 | 41 | 36 | 53 | 60 | 59 | 51 | 72 | 36 | 55 | 54 | 30 | 44 | 58 |
| anthropic/claude-opus-5.5#low | 24 | 36 | 29 | 38 | 38 | 33 | 36 | 28 | 42 | 40 | 44 | 39 | 33 | 51 | 49 | 30 | 47 | 38 | 35 | 32 | 18 | 58 | 47 | 47 | 61 | 51 | 42 | 62 | 55 | 49 | 55 | 38 | 51 | 54 |
| deepseek-v4-flash@2026-10-17 | 34 | 42 | 38 | 46 | 36 | 32 | 39 | 28 | 40 | 35 | 47 | 31 | 47 | 49 | 44 | 32 | 40 | 35 | 47 | 34 | 38 | 64 | 49 | 46 | 50 | 56 | 54 | 58 | 34 | 45 | 59 | 35 | 66 | 53 |
| deepseek/deepseek-v4-pro-0813 | 26 | 24 | 39 | 35 | 44 | 50 | 35 | 31 | 50 | 25 | 47 | 29 | 21 | 54 | 48 | 44 | 53 | 36 | 48 | 38 | 35 | 50 | 38 | 49 | 50 | 61 | 40 | 58 | 42 | 44 | 66 | 35 | 64 | 56 |
| gemma4 | 22 | 30 | 32 | 36 | 35 | 42 | 44 | 29 | 45 | 38 | 46 | 40 | 39 | 51 | 52 | 45 | 57 | 41 | 42 | 35 | 39 | 57 | 47 | 50 | 50 | 56 | 50 | 62 | 64 | 54 | 68 | 41 | 68 | 83 |
| glm5.3-flash | 29 | 24 | 42 | 33 | 32 | 31 | 38 | 38 | 34 | 43 | 50 | 39 | 35 | 39 | 49 | 31 | 43 | 34 | 42 | 33 | 30 | 36 | 42 | 40 | 53 | 50 | 59 | 68 | 48 | 44 | 55 | 50 | 56 | 74 |
| google/gemini-3.7-flash | 40 | 50 | 50 | 44 | 50 | 46 | 51 | 52 | 46 | 49 | 57 | 50 | 39 | 42 | 48 | 35 | 46 | 58 | 46 | 41 | 42 | 49 | 47 | 53 | 50 | 52 | 50 | 49 | 52 | 48 | 51 | 34 | 46 | 50 |
| google/gemini-4-argon | 30 | 39 | 36 | 31 | 42 | 35 | 35 | 29 | 40 | 34 | 54 | 42 | 31 | 49 | 42 | 26 | 39 | 42 | 36 | 26 | 28 | 51 | 49 | 42 | 53 | 58 | 51 | 51 | 42 | 36 | 45 | 30 | 45 | 52 |
| mimo-v2.6-flash | 22 | 36 | 35 | 54 | 36 | 46 | 28 | 25 | 24 | 26 | 38 | 35 | 32 | 56 | 52 | 30 | 47 | 32 | 44 | 45 | 42 | 48 | 35 | 50 | 56 | 56 | 45 | 71 | 52 | 52 | 64 | 40 | 66 | 68 |
| openai/gpt-5.6-luna | 24 | 35 | 39 | 32 | 44 | 40 | 42 | 30 | 39 | 26 | 49 | 49 | 36 | 49 | 39 | 26 | 47 | 24 | 41 | 24 | 26 | 54 | 47 | 49 | 47 | 50 | 32 | 56 | 40 | 38 | 58 | 38 | 50 | 51 |
| openai/gpt-6.1-sol#low | 12 | 38 | 29 | 32 | 35 | 33 | 22 | 24 | 32 | 28 | 47 | 39 | 11 | 44 | 42 | 25 | 47 | 30 | 42 | 29 | 27 | 59 | 38 | 35 | 61 | 50 | 24 | 64 | 48 | 52 | 56 | 45 | 55 | 61 |
| qwen3.6 | 28 | 21 | 36 | 46 | 35 | 25 | 42 | 52 | 58 | 47 | 56 | 36 | 32 | 50 | 51 | 22 | 38 | 28 | 52 | 38 | 45 | 67 | 46 | 47 | 62 | 50 | 22 | 59 | 61 | 66 | 60 | 44 | 59 | 62 |
| qwen3.8-flash | 30 | 31 | 38 | 51 | 38 | 42 | 36 | 44 | 35 | 35 | 46 | 39 | 44 | 54 | 50 | 25 | 40 | 36 | 37 | 26 | 39 | 42 | 39 | 51 | 60 | 58 | 45 | 60 | 39 | 66 | 50 | 42 | 52 | 50 |
