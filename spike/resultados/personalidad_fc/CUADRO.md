# Cuadro de personalidad por modelo

Generado por `cuadro_personalidad.py` con los datos del P1 (PERSONALIDAD.md §17).
**Conducta** = lo que el modelo elige cuando decide él, ajustado por lo que él mismo juzga admirable (50 = elige su ideal). ▲/▼ = por encima/debajo de la media de los 19 modelos con IC 95 % que no la incluye. **Autoimagen** = lo que dice de sí mismo en el cuestionario (0-100); no sirve para ordenar modelos.

## Conducta (puntuación principal)

| modelo | ISS | Apertura | Responsabilidad | Extraversión | Amabilidad | Neuroticismo | Honestidad-Humildad |
|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 10.3 | 48 | 31 | 40 | 27 ▼ | 56 | 27 ▼ |
| anthropic/claude-opus-5.5#low | 12.5 | 52 | 38 | 41 | 33 | 53 | 36 |
| deepseek-v4-flash | 43.6 | 40 ▼ | 32 | 38 | 35 | 61 ▲ | 52 ▲ |
| deepseek-v4-flash@2026-10-17 | — | 48 | 36 | 40 | 39 | 52 | 47 ▲ |
| deepseek/deepseek-v4-pro-0813 | — | 52 | 37 | 42 | 36 | 51 | 44 |
| gemma4 | 28.1 | 63 ▲ | 41 | 45 ▲ | 35 | 54 | 44 |
| glm5.3-flash | 28.9 | 56 ▲ | 40 | 37 | 34 | 52 | 38 |
| google/gemini-3.7-flash | 55.2 | 48 | 51 ▲ | 45 ▲ | 47 ▲ | 50 ▼ | 45 ▲ |
| google/gemini-4-argon | — | 44 ▼ | 37 | 38 | 36 | 51 | 35 |
| mimo-v2.6-flash | 12.6 | 58 ▲ | 31 ▼ | 41 | 39 | 54 | 46 ▲ |
| mistralai/mistral-large-4-0 | 21.3 | 50 | 34 | 38 | 34 | 57 | 39 |
| moonshotai/kimi-k3 | 27.9 | 49 | 30 | 30 ▼ | 32 | 58 | 41 |
| openai/gpt-5.6-luna | 7.6 | 47 | 39 | 37 | 36 | 47 ▼ | 38 |
| openai/gpt-6.1-sol#low | 13.2 | 54 | 31 | 34 ▼ | 31 | 46 ▼ | 40 |
| qwen3.6 | 23.2 | 59 ▲ | 47 ▲ | 38 | 33 | 48 | 49 ▲ |
| qwen3.8-flash | 24.8 | 52 | 38 | 42 | 39 | 53 | 40 |
| qwen/qwen3.8-max-0902#low | — | 46 | 33 | 37 | 29 | 63 ▲ | 41 |
| x-ai/grok-4.5 | 37.8 | 42 | 30 | 37 | 28 | 57 | 36 |
| z-ai/glm-5.3 | — | 43 | 38 | 42 | 34 | 57 | 31 ▼ |
| *media de los modelos* | | *50* | *37* | *39* | *35* | *54* | *40* |

## Autoimagen (cuestionario)

| modelo | Apertura | Responsabilidad | Extraversión | Amabilidad | Neuroticismo | Honestidad-Humildad |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 66 | 78 | 44 | 82 | 22 | 94 |
| anthropic/claude-opus-5.5#low | 68 | 78 | 46 | 84 | 26 | 98 |
| deepseek-v4-flash | 72 | 71 | 51 | 93 | 46 | 85 |
| deepseek-v4-flash@2026-10-17 | 74 | 72 | 51 | 91 | 43 | 81 |
| deepseek/deepseek-v4-pro-0813 | 68 | 72 | 57 | 86 | 37 | 81 |
| gemma4 | 71 | 92 | 61 | 78 | 18 | 78 |
| glm5.3-flash | 64 | 79 | 33 | 78 | 10 | 96 |
| google/gemini-3.7-flash | 56 | 92 | 46 | 76 | 8 | 94 |
| google/gemini-4-argon | 52 | 92 | 53 | 75 | 16 | 91 |
| mimo-v2.6-flash | 73 | 67 | 44 | 87 | 36 | 81 |
| mistralai/mistral-large-4-0 | 49 | 82 | 36 | 81 | 4 | 99 |
| moonshotai/kimi-k3 | 68 | 86 | 48 | 86 | 12 | 98 |
| openai/gpt-5.6-luna | 65 | 69 | 54 | 81 | 41 | 84 |
| openai/gpt-6.1-sol#low | 55 | 79 | 48 | 73 | 9 | 96 |
| qwen3.6 | 77 | 68 | 59 | 93 | 38 | 81 |
| qwen3.8-flash | 88 | 84 | 62 | 97 | 26 | 97 |
| qwen/qwen3.8-max-0902#low | 52 | 81 | 42 | 77 | 7 | 96 |
| x-ai/grok-4.5 | 86 | 86 | 61 | 93 | 8 | 88 |
| z-ai/glm-5.3 | 62 | 76 | 49 | 79 | 22 | 93 |

## Retrato de cada modelo (solo rasgos distinguibles de la media)

- **anthropic/claude-haiku-5.5**: **menos Amabilidad** (pone límites y se defiende); **menos Honestidad-Humildad** (acepta ventajas y se promociona).
- **anthropic/claude-opus-5.5#low**: ningún rasgo se separa de la media de los modelos.
- **deepseek-v4-flash**: **menos Apertura** (prefiere lo conocido); **más Neuroticismo** (reacciona, se preocupa); **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **deepseek-v4-flash@2026-10-17**: **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **deepseek/deepseek-v4-pro-0813**: ningún rasgo se separa de la media de los modelos.
- **gemma4**: **más Apertura** (curioso, busca lo nuevo); **más Extraversión** (busca gente y protagonismo).
- **glm5.3-flash**: **más Apertura** (curioso, busca lo nuevo).
- **google/gemini-3.7-flash**: **más Responsabilidad** (cumple y planifica); **más Extraversión** (busca gente y protagonismo); **más Amabilidad** (cede y coopera); **menos Neuroticismo** (se mantiene sereno); **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **google/gemini-4-argon**: **menos Apertura** (prefiere lo conocido).
- **mimo-v2.6-flash**: **más Apertura** (curioso, busca lo nuevo); **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **mistralai/mistral-large-4-0**: ningún rasgo se separa de la media de los modelos.
- **moonshotai/kimi-k3**: **menos Extraversión** (prefiere calma y segundo plano).
- **openai/gpt-5.6-luna**: **menos Neuroticismo** (se mantiene sereno).
- **openai/gpt-6.1-sol#low**: **menos Extraversión** (prefiere calma y segundo plano); **menos Neuroticismo** (se mantiene sereno).
- **qwen3.6**: **más Apertura** (curioso, busca lo nuevo); **más Responsabilidad** (cumple y planifica); **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **qwen3.8-flash**: ningún rasgo se separa de la media de los modelos.
- **qwen/qwen3.8-max-0902#low**: **más Neuroticismo** (reacciona, se preocupa).
- **x-ai/grok-4.5**: ningún rasgo se separa de la media de los modelos.
- **z-ai/glm-5.3**: **menos Honestidad-Humildad** (acepta ventajas y se promociona).
