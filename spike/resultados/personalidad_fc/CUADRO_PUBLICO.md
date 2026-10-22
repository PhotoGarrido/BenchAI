# Cuadro público de personalidad · conducta comparada (PERSONALIDAD.md §28)

Generado por `cuadro_publico_v3.py`. Selección: personalidad_v3_seleccion.json. 13 modelos, 7 laboratorios (anthropic, deepseek, google, openai, qwen, xiaomi, z-ai); situaciones por rasgo: O 59, C 56, E 57, A 57, N 19, H 48. Semilla 20261010. Sin llamadas a modelos. Escala de Honestidad-Humildad: I1-H en binario: 48 situaciones calibradas por dificultad, 12 por faceta (PERSONALIDAD.md §36-37). Escala de Neuroticismo: I1-N en binario, 19 elegidas por R1 (PERSONALIDAD.md §39-40).
Fuera por banco incompleto (< 95 %): deepseek-v4-flash (40 %), mistralai/mistral-large-4-0 (40 %), moonshotai/kimi-k3 (40 %), qwen/qwen3.8-max-0902#low (40 %), x-ai/grok-4.5 (40 %), z-ai/glm-5.3 (40 %).

**Puntuación** = 50 + 50·media(elige el polo alto − deseabilidad media del panel): 50 = elige lo que el conjunto de modelos juzga admirable. **▲/▼** = elige el polo alto más/menos a menudo que los demás modelos en las mismas situaciones (comparación pareada, IC 95 %), solo si la marca es **robusta** (P1–P3, P5, P6). Neuroticismo con marca desde §40 (sus marcas pasan además R4 de §30.2).

| modelo | ISS | Apertura | Responsabilidad | Extraversión | Amabilidad | Neuroticismo | Honestidad-Humildad |
|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 10.3 | 52 | 39 | 42 | 28 ▼ | 64 | 46 |
| anthropic/claude-opus-5.5#low | 12.5 | 55 | 33 ▼ | 42 | 38 | 43 ▼ | 51 ▲ |
| deepseek-v4-flash@2026-10-17 | 21.1 | 50 | 35 | 34 ▼ | 32 | 62 | 49 ▲ |
| deepseek/deepseek-v4-pro-0813 | — | 49 | 40 | 39 | 40 | 51 | 49 |
| gemma4 | 28.1 | 55 | 45 ▲ | 37 | 29 ▼ | 68 ▲ | 34 ▼ |
| glm5.3-flash | 28.9 | 55 | 39 | 38 | 34 | 62 | 45 |
| google/gemini-3.7-flash | 55.2 | 37 ▼ | 39 | 52 ▲ | 47 ▲ | 51 | 37 |
| google/gemini-4-argon | — | 44 ▼ | 36 | 38 | 35 | 42 ▼ | 38 ▼ |
| mimo-v2.6-flash | 12.6 | 56 | 40 | 43 | 36 | 62 | 42 |
| openai/gpt-5.6-luna | 7.6 | 55 | 41 | 39 | 31 | 59 | 47 |
| openai/gpt-6.1-sol#low | 13.2 | 52 | 34 ▼ | 38 | 33 | 45 ▼ | 51 ▲ |
| qwen3.6 | 23.2 | 55 | 41 | 42 | 35 | 74 ▲ | 34 ▼ |
| qwen3.8-flash | 24.8 | 49 | 36 | 40 | 32 | 62 | 44 |

Neuroticismo: I1-N en binario (19 elegidas por R1; ansiedad 7, hostilidad 6, depresion 3, impulsividad 2, vulnerabilidad 1); sin situaciones de autoconciencia. Pasó §39 (§40). Marcas con las cinco comprobaciones de §28 y R4 de §30.2.

## Validez con la definición de §28 (G3 y G4 de §21)

Mismos cálculos que `analizar_v3.py` (G3: r media entre facetas del mismo rasgo frente a facetas de otros rasgos; G4: Spearman-Brown de mitades pares/impares entre modelos), pero sobre la puntuación de §28 en vez de la ajustada por la deseabilidad propia.

| rasgo | G3 dentro / fuera | G3 | G4 | G4 ≥ 0,70 | en §28 |
|---|---|---|---|---|---|
| Apertura | +0.46 / -0.05 | ✔ | 0.94 | ✔ | con marca |
| Responsabilidad | +0.27 / +0.02 | ✔ | 0.81 | ✔ | con marca |
| Extraversión | +0.27 / +0.01 | ✔ | 0.93 | ✔ | con marca |
| Amabilidad | +0.56 / -0.06 | ✔ | 0.86 | ✔ | con marca |
| Neuroticismo | +0.40 / +0.02 | ✔ | 0.88 | ✔ | con marca |
| Honestidad-Humildad | +0.52 / -0.11 | ✔ | 0.95 | ✔ | con marca |

Sin conflictos: los rasgos con marca tienen G4 ≥ 0,70 y los demás, por debajo.

## Retrato de cada modelo (§28)

- **anthropic/claude-haiku-5.5**: **menos Amabilidad** (pone límites y se defiende).
- **anthropic/claude-opus-5.5#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas); **menos Neuroticismo** (se mantiene sereno).
- **deepseek-v4-flash@2026-10-17**: **menos Extraversión** (prefiere calma y segundo plano); **más Honestidad-Humildad** (sincero, renuncia a ventajas). Tendencias frágiles, no publicadas: A▼.
- **deepseek/deepseek-v4-pro-0813**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: A▲, N▼, H▲.
- **gemma4**: **más Responsabilidad** (cumple y planifica); **menos Amabilidad** (pone límites y se defiende); **menos Honestidad-Humildad** (acepta ventajas y se promociona); **más Neuroticismo** (reacciona, se preocupa).
- **glm5.3-flash**: perfil próximo al de los demás modelos.
- **google/gemini-3.7-flash**: **menos Apertura** (prefiere lo conocido); **más Extraversión** (busca gente y protagonismo); **más Amabilidad** (cede y coopera). Tendencias frágiles, no publicadas: H▼.
- **google/gemini-4-argon**: **menos Apertura** (prefiere lo conocido); **menos Honestidad-Humildad** (acepta ventajas y se promociona); **menos Neuroticismo** (se mantiene sereno).
- **mimo-v2.6-flash**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: O▲.
- **openai/gpt-5.6-luna**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: A▼, H▲.
- **openai/gpt-6.1-sol#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas); **menos Neuroticismo** (se mantiene sereno).
- **qwen3.6**: **menos Honestidad-Humildad** (acepta ventajas y se promociona); **más Neuroticismo** (reacciona, se preocupa).
- **qwen3.8-flash**: perfil próximo al de los demás modelos.

## Marcas candidatas y su nivel

**35 marcas candidatas** (IC de la comparación que excluye 0): 21 robustas · 8 frágiles · 6 no publicables.

P1 = signo replicado en las dos mitades (≥ 90 %) · P2 = réplica 0 y 1 · P3 = orden AB y BA · P5 = todos los paneles sin un laboratorio · P6 = BH q < 0,05 sobre 78 pruebas (entre paréntesis, sin N).

| modelo | rasgo | marca | dif [IC] | P1 signo (sig. ambas) | P2 | P3 | P5 | P6 q (sin N) | nivel | por qué |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | A | ▼ | -6.9 [-10.6, -3.5] | 100 % (62 %) | ✔ | ✔ | ✔ | 0.0004 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | C | ▼ | -5.6 [-8.5, -2.9] | 100 % (80 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | N | ▼ | -15.2 [-21.2, -9.1] | 100 % (98 %) | ✔ | ✔ | ✔ | 0.0003 (—) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | H | ▲ | +8.2 [+4.9, +11.9] | 100 % (96 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | E | ▼ | -6.4 [-9.3, -3.8] | 100 % (94 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | A | ▼ | -3.4 [-5.6, -1.1] | 100 % (8 %) | ✔ | ✘ | ✔ | 0.0140 (0.0140) | **frágil** | falla P3 |
| deepseek-v4-flash@2026-10-17 | H | ▲ | +5.6 [+2.8, +8.4] | 100 % (72 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek/deepseek-v4-pro-0813 | A | ▲ | +5.4 [+2.7, +8.3] | 100 % (58 %) | ✔ | ✘ | ✔ | 0.0003 (0.0003) | **frágil** | falla P3 |
| deepseek/deepseek-v4-pro-0813 | N | ▼ | -7.3 [-12.7, -1.5] | 98 % (1 %) | ✔ | ✘ | ✔ | 0.0225 (—) | **frágil** | falla P3 |
| deepseek/deepseek-v4-pro-0813 | H | ▲ | +5.6 [+2.7, +8.8] | 100 % (69 %) | ✔ | ✘ | ✔ | 0.0004 (0.0004) | **frágil** | falla P3 |
| gemma4 | C | ▲ | +6.7 [+2.9, +10.7] | 100 % (57 %) | ✔ | ✔ | ✔ | 0.0047 (0.0046) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | A | ▼ | -5.7 [-8.4, -3.1] | 100 % (92 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | N | ▲ | +11.9 [+4.6, +18.8] | 100 % (19 %) | ✔ | ✔ | ✔ | 0.0089 (—) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | H | ▼ | -10.5 [-15.4, -5.2] | 100 % (91 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| glm5.3-flash | O | ▲ | +4.2 [+1.0, +7.5] | 100 % (0 %) | ✘ | ✘ | ✘ | 0.0299 (0.0311) | **no publicable** | falla 3 (P2 P3 P5); cae sin google |
| glm5.3-flash | E | ▼ | -3.1 [-5.9, -0.3] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.0907 (0.0927) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, google, xiaomi |
| google/gemini-3.7-flash | O | ▼ | -15.5 [-19.9, -11.4] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | E | ▲ | +13.1 [+7.3, +18.8] | 100 % (96 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | A | ▲ | +13.3 [+6.8, +19.7] | 100 % (84 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | H | ▼ | -7.1 [-12.5, -1.7] | 100 % (0 %) | ✔ | ✘ | ✔ | 0.0253 (0.0266) | **frágil** | falla P3 |
| google/gemini-4-argon | O | ▼ | -8.0 [-11.4, -4.7] | 100 % (98 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-4-argon | N | ▼ | -16.6 [-23.1, -10.3] | 100 % (99 %) | ✔ | ✔ | ✔ | 0.0003 (—) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-4-argon | H | ▼ | -6.2 [-10.4, -2.0] | 100 % (12 %) | ✔ | ✔ | ✔ | 0.0125 (0.0127) | **robusta** | pasa P1–P3, P5, P6 |
| mimo-v2.6-flash | O | ▲ | +5.6 [+1.5, +9.6] | 98 % (0 %) | ✔ | ✘ | ✘ | 0.0242 (0.0257) | **frágil** | falla P3 P5; cae sin google |
| mimo-v2.6-flash | E | ▲ | +3.1 [+0.1, +6.3] | 93 % (0 %) | ✘ | ✘ | ✘ | 0.0907 (0.0945) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin deepseek, openai, z-ai |
| mimo-v2.6-flash | N | ▲ | +5.5 [+0.3, +11.2] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.0907 (—) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, deepseek, google, openai |
| openai/gpt-5.6-luna | O | ▲ | +4.2 [+0.7, +7.6] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.0450 (0.0465) | **no publicable** | falla 3 (P2 P3 P5); cae sin google |
| openai/gpt-5.6-luna | A | ▼ | -4.1 [-6.4, -1.8] | 100 % (36 %) | ✘ | ✔ | ✔ | 0.0041 (0.0041) | **frágil** | falla P2 |
| openai/gpt-5.6-luna | H | ▲ | +4.2 [+1.1, +7.0] | 100 % (3 %) | ✔ | ✘ | ✘ | 0.0159 (0.0164) | **frágil** | falla P3 P5; cae sin google |
| openai/gpt-6.1-sol#low | C | ▼ | -5.1 [-8.3, -1.9] | 100 % (27 %) | ✔ | ✔ | ✔ | 0.0056 (0.0054) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-6.1-sol#low | N | ▼ | -13.0 [-21.5, -3.9] | 100 % (2 %) | ✔ | ✔ | ✔ | 0.0144 (—) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-6.1-sol#low | H | ▲ | +7.9 [+4.2, +11.8] | 100 % (94 %) | ✔ | ✔ | ✔ | 0.0004 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.6 | N | ▲ | +17.6 [+12.4, +23.0] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0003 (—) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.6 | H | ▼ | -10.5 [-14.9, -6.3] | 100 % (98 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.8-flash | A | ▼ | -2.9 [-5.3, -0.5] | 98 % (0 %) | ✘ | ✘ | ✔ | 0.0509 (0.0522) | **no publicable** | falla 3 (P2 P3 P6) |

## Variantes de cada marca candidata

Marca en cada variante (· = sin marca).

| modelo | rasgo | cuadro | rep0 | rep1 | AB | BA | sin anthropic | sin deepseek | sin google | sin openai | sin qwen | sin xiaomi | sin z-ai |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek-v4-flash@2026-10-17 | E | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | A | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v4-pro-0813 | A | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v4-pro-0813 | N | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek/deepseek-v4-pro-0813 | H | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | C | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| gemma4 | N | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| glm5.3-flash | O | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| glm5.3-flash | E | ▼ | · | ▼ | · | · | · | ▼ | · | ▼ | ▼ | · | ▼ |
| google/gemini-3.7-flash | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | E | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | A | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | H | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| mimo-v2.6-flash | O | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| mimo-v2.6-flash | E | ▲ | · | · | ▲ | · | ▲ | · | ▲ | · | ▲ | ▲ | · |
| mimo-v2.6-flash | N | ▲ | · | ▲ | ▲ | · | · | · | · | · | ▲ | ▲ | ▲ |
| openai/gpt-5.6-luna | O | ▲ | ▲ | · | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-5.6-luna | A | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-5.6-luna | H | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-6.1-sol#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen3.6 | N | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen3.6 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| qwen3.8-flash | A | ▼ | ▼ | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |

## Puntuación con IC 95 %

| modelo | O | C | E | A | N | H |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 52 [46, 57] | 39 [34, 44] | 42 [37, 47] | 28 [24, 33] | 64 [56, 73] | 46 [41, 51] |
| anthropic/claude-opus-5.5#low | 55 [51, 59] | 33 [29, 37] | 42 [38, 46] | 38 [33, 43] | 43 [35, 51] | 51 [47, 55] |
| deepseek-v4-flash@2026-10-17 | 50 [44, 56] | 35 [31, 40] | 34 [30, 39] | 32 [28, 35] | 62 [55, 70] | 49 [45, 53] |
| deepseek/deepseek-v4-pro-0813 | 49 [45, 54] | 40 [36, 45] | 39 [35, 42] | 40 [36, 44] | 51 [45, 56] | 49 [45, 52] |
| gemma4 | 55 [50, 61] | 45 [40, 50] | 37 [32, 42] | 29 [26, 33] | 68 [60, 76] | 34 [28, 40] |
| glm5.3-flash | 55 [50, 60] | 39 [34, 44] | 38 [33, 42] | 34 [30, 38] | 62 [54, 70] | 45 [40, 50] |
| google/gemini-3.7-flash | 37 [32, 42] | 39 [34, 44] | 52 [48, 57] | 47 [42, 52] | 51 [44, 59] | 37 [32, 42] |
| google/gemini-4-argon | 44 [39, 49] | 36 [32, 41] | 38 [33, 43] | 35 [31, 39] | 42 [34, 50] | 38 [32, 43] |
| mimo-v2.6-flash | 56 [51, 61] | 40 [35, 44] | 43 [39, 48] | 36 [32, 41] | 62 [57, 68] | 42 [37, 47] |
| openai/gpt-5.6-luna | 55 [50, 60] | 41 [36, 46] | 39 [34, 44] | 31 [27, 35] | 59 [53, 64] | 47 [42, 52] |
| openai/gpt-6.1-sol#low | 52 [47, 58] | 34 [29, 38] | 38 [33, 43] | 33 [29, 38] | 45 [37, 54] | 51 [46, 55] |
| qwen3.6 | 55 [49, 60] | 41 [36, 47] | 42 [37, 48] | 35 [31, 40] | 74 [68, 80] | 34 [29, 39] |
| qwen3.8-flash | 49 [43, 55] | 36 [31, 42] | 40 [36, 45] | 32 [28, 36] | 62 [56, 67] | 44 [39, 49] |
