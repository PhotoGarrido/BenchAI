# Cuadro público de personalidad · conducta comparada (PERSONALIDAD.md §28)

Generado por `cuadro_publico_v3.py`. Selección: personalidad_v3_seleccion.json. 13 modelos, 7 laboratorios (anthropic, deepseek, google, openai, qwen, xiaomi, z-ai); situaciones por rasgo: O 59, C 56, E 57, A 57, N 57, H 48. Semilla 20261010. Sin llamadas a modelos. Escala de Honestidad-Humildad: I1-H en binario: 48 situaciones calibradas por dificultad, 12 por faceta (PERSONALIDAD.md §36-37).
Fuera por banco incompleto (< 95 %): deepseek-v4-flash (40 %), mistralai/mistral-large-4-0 (40 %), moonshotai/kimi-k3 (40 %), qwen/qwen3.8-max-0902#low (40 %), x-ai/grok-4.5 (40 %), z-ai/glm-5.3 (40 %).

**Puntuación** = 50 + 50·media(elige el polo alto − deseabilidad media del panel): 50 = elige lo que el conjunto de modelos juzga admirable. **▲/▼** = elige el polo alto más/menos a menudo que los demás modelos en las mismas situaciones (comparación pareada, IC 95 %), solo si la marca es **robusta** (P1–P3, P5, P6). Extraversión con aviso de fiabilidad; Neuroticismo solo descriptivo, sin marca.

| modelo | ISS | Apertura | Responsabilidad | Extraversión † | Amabilidad | Neuroticismo ‡ | Honestidad-Humildad |
|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 10.3 | 52 | 39 | 42 | 28 ▼ | 56 | 46 |
| anthropic/claude-opus-5.5#low | 12.5 | 55 | 33 ▼ | 42 | 38 | 49 | 51 ▲ |
| deepseek-v4-flash@2026-10-17 | — | 50 | 35 | 34 ▼ | 32 | 51 | 49 ▲ |
| deepseek/deepseek-v4-pro-0813 | — | 49 | 40 | 39 | 40 | 47 | 49 |
| gemma4 | 28.1 | 55 | 45 ▲ | 37 | 29 ▼ | 54 | 34 ▼ |
| glm5.3-flash | 28.9 | 55 | 39 | 38 | 34 | 47 | 45 |
| google/gemini-3.7-flash | 55.2 | 37 ▼ | 39 | 52 ▲ | 47 ▲ | 48 | 37 |
| google/gemini-4-argon | — | 44 ▼ | 36 | 38 | 35 | 52 | 38 ▼ |
| mimo-v2.6-flash | 12.6 | 56 | 40 | 43 | 36 | 51 | 42 |
| openai/gpt-5.6-luna | 7.6 | 55 | 41 | 39 | 31 ▼ | 52 | 48 |
| openai/gpt-6.1-sol#low | 13.2 | 52 | 34 ▼ | 38 | 33 | 49 | 51 ▲ |
| qwen3.6 | 23.2 | 55 | 41 | 42 | 35 | 54 | 34 ▼ |
| qwen3.8-flash | 24.8 | 49 | 36 | 40 | 32 | 50 | 44 |

† fiabilidad baja (§23): marca solo si robusta, con aviso. ‡ solo descriptivo (§23).

## Validez con la definición de §28 (G3 y G4 de §21)

Mismos cálculos que `analizar_v3.py` (G3: r media entre facetas del mismo rasgo frente a facetas de otros rasgos; G4: Spearman-Brown de mitades pares/impares entre modelos), pero sobre la puntuación de §28 en vez de la ajustada por la deseabilidad propia.

| rasgo | G3 dentro / fuera | G3 | G4 | G4 ≥ 0,70 | en §28 |
|---|---|---|---|---|---|
| Apertura | +0.46 / -0.05 | ✔ | 0.94 | ✔ | con marca |
| Responsabilidad | +0.27 / -0.01 | ✔ | 0.81 | ✔ | con marca |
| Extraversión | +0.27 / +0.00 | ✔ | 0.93 | ✔ | marca solo robusta, con aviso |
| Amabilidad | +0.56 / -0.08 | ✔ | 0.86 | ✔ | con marca |
| Neuroticismo | +0.04 / -0.04 | ✔ | 0.62 | ✘ | solo descriptivo |
| Honestidad-Humildad | +0.52 / -0.09 | ✔ | 0.95 | ✔ | con marca |

**CONFLICTO entre §28 y la consistencia con la definición nueva (lo resuelve David; este cuadro aplica §28 sin cambios):**

- **Extraversión**: marca solo con aviso de fiabilidad (§28), pero G4 = 0.93 ≥ 0.70.

### Escenario alternativo, NO decidido: marca en los rasgos con G4 ≥ 0,70

Rasgos con marca: Apertura, Responsabilidad, Extraversión, Amabilidad, Honestidad-Humildad; el resto, solo descriptivo. Mismos niveles de robustez (sin la regla de N).

| modelo | Apertura | Responsabilidad | Extraversión | Amabilidad | Neuroticismo | Honestidad-Humildad |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 52 | 39 | 42 | 28 ▼ | 56 | 46 |
| anthropic/claude-opus-5.5#low | 55 | 33 ▼ | 42 | 38 | 49 | 51 ▲ |
| deepseek-v4-flash@2026-10-17 | 50 | 35 | 34 ▼ | 32 | 51 | 49 ▲ |
| deepseek/deepseek-v4-pro-0813 | 49 | 40 | 39 | 40 | 47 | 49 |
| gemma4 | 55 | 45 ▲ | 37 | 29 ▼ | 54 | 34 ▼ |
| glm5.3-flash | 55 | 39 | 38 | 34 | 47 | 45 |
| google/gemini-3.7-flash | 37 ▼ | 39 | 52 ▲ | 47 ▲ | 48 | 37 |
| google/gemini-4-argon | 44 ▼ | 36 | 38 | 35 | 52 | 38 ▼ |
| mimo-v2.6-flash | 56 | 40 | 43 | 36 | 51 | 42 |
| openai/gpt-5.6-luna | 55 | 41 | 39 | 31 ▼ | 52 | 48 |
| openai/gpt-6.1-sol#low | 52 | 34 ▼ | 38 | 33 | 49 | 51 ▲ |
| qwen3.6 | 55 | 41 | 42 | 35 | 54 | 34 ▼ |
| qwen3.8-flash | 49 | 36 | 40 | 32 | 50 | 44 |

- **anthropic/claude-haiku-5.5**: **menos Amabilidad** (pone límites y se defiende).
- **anthropic/claude-opus-5.5#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **deepseek-v4-flash@2026-10-17**: **menos Extraversión** (prefiere calma y segundo plano); **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **deepseek/deepseek-v4-pro-0813**: perfil próximo al de los demás modelos.
- **gemma4**: **más Responsabilidad** (cumple y planifica); **menos Amabilidad** (pone límites y se defiende); **menos Honestidad-Humildad** (acepta ventajas y se promociona).
- **glm5.3-flash**: perfil próximo al de los demás modelos.
- **google/gemini-3.7-flash**: **menos Apertura** (prefiere lo conocido); **más Extraversión** (busca gente y protagonismo); **más Amabilidad** (cede y coopera).
- **google/gemini-4-argon**: **menos Apertura** (prefiere lo conocido); **menos Honestidad-Humildad** (acepta ventajas y se promociona).
- **mimo-v2.6-flash**: perfil próximo al de los demás modelos.
- **openai/gpt-5.6-luna**: **menos Amabilidad** (pone límites y se defiende).
- **openai/gpt-6.1-sol#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **qwen3.6**: **menos Honestidad-Humildad** (acepta ventajas y se promociona).
- **qwen3.8-flash**: perfil próximo al de los demás modelos.

## Retrato de cada modelo (§28)

- **anthropic/claude-haiku-5.5**: **menos Amabilidad** (pone límites y se defiende). *Neuroticismo (descriptivo): 56.*
- **anthropic/claude-opus-5.5#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas). *Neuroticismo (descriptivo): 49.*
- **deepseek-v4-flash@2026-10-17**: **más Honestidad-Humildad** (sincero, renuncia a ventajas); **menos Extraversión** (prefiere calma y segundo plano) *[Extraversión: fiabilidad baja (§23), con aviso]*. *Neuroticismo (descriptivo): 51.* Tendencias frágiles, no publicadas: A▼.
- **deepseek/deepseek-v4-pro-0813**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 47.* Tendencias frágiles, no publicadas: A▲, H▲.
- **gemma4**: **más Responsabilidad** (cumple y planifica); **menos Amabilidad** (pone límites y se defiende); **menos Honestidad-Humildad** (acepta ventajas y se promociona). *Neuroticismo (descriptivo): 54.*
- **glm5.3-flash**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 47.* Tendencias frágiles, no publicadas: O▲.
- **google/gemini-3.7-flash**: **menos Apertura** (prefiere lo conocido); **más Amabilidad** (cede y coopera); **más Extraversión** (busca gente y protagonismo) *[Extraversión: fiabilidad baja (§23), con aviso]*. *Neuroticismo (descriptivo): 48.* Tendencias frágiles, no publicadas: H▼.
- **google/gemini-4-argon**: **menos Apertura** (prefiere lo conocido); **menos Honestidad-Humildad** (acepta ventajas y se promociona). *Neuroticismo (descriptivo): 52.*
- **mimo-v2.6-flash**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 51.* Tendencias frágiles, no publicadas: O▲.
- **openai/gpt-5.6-luna**: **menos Amabilidad** (pone límites y se defiende). *Neuroticismo (descriptivo): 52.* Tendencias frágiles, no publicadas: H▲.
- **openai/gpt-6.1-sol#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas). *Neuroticismo (descriptivo): 49.*
- **qwen3.6**: **menos Honestidad-Humildad** (acepta ventajas y se promociona). *Neuroticismo (descriptivo): 54.*
- **qwen3.8-flash**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 50.*

## Marcas candidatas y su nivel

**32 marcas candidatas** (IC de la comparación que excluye 0): 17 robustas · 7 frágiles · 8 no publicables.

P1 = signo replicado en las dos mitades (≥ 90 %) · P2 = réplica 0 y 1 · P3 = orden AB y BA · P5 = todos los paneles sin un laboratorio · P6 = BH q < 0,05 sobre 78 pruebas (entre paréntesis, sin N).

| modelo | rasgo | marca | dif [IC] | P1 signo (sig. ambas) | P2 | P3 | P5 | P6 q (sin N) | nivel | por qué |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | A | ▼ | -6.9 [-10.5, -3.4] | 100 % (65 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-haiku-5.5 | N | ▲ | +5.5 [+1.7, +9.6] | 100 % (10 %) | ✔ | ✘ | ✔ | 0.0134 (—) | **no publicable** | N solo descriptivo (§23) |
| anthropic/claude-opus-5.5#low | O | ▲ | +4.2 [+0.0, +8.5] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.1368 (0.1247) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, deepseek, google |
| anthropic/claude-opus-5.5#low | C | ▼ | -5.6 [-8.4, -2.8] | 100 % (74 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | H | ▲ | +8.2 [+4.8, +11.8] | 100 % (96 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | E | ▼ | -6.4 [-9.2, -3.8] | 100 % (93 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | A | ▼ | -3.4 [-5.6, -1.1] | 100 % (10 %) | ✔ | ✘ | ✔ | 0.0125 (0.0104) | **frágil** | falla P3 |
| deepseek-v4-flash@2026-10-17 | H | ▲ | +5.6 [+2.8, +8.5] | 100 % (78 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek/deepseek-v4-pro-0813 | A | ▲ | +5.4 [+2.4, +8.4] | 100 % (55 %) | ✔ | ✘ | ✔ | 0.0016 (0.0013) | **frágil** | falla P3 |
| deepseek/deepseek-v4-pro-0813 | N | ▼ | -4.4 [-8.2, -0.7] | 99 % (0 %) | ✘ | ✘ | ✔ | 0.0699 (—) | **no publicable** | N solo descriptivo (§23) |
| deepseek/deepseek-v4-pro-0813 | H | ▲ | +5.6 [+2.7, +8.8] | 100 % (72 %) | ✔ | ✘ | ✔ | 0.0006 (0.0005) | **frágil** | falla P3 |
| gemma4 | O | ▲ | +4.7 [+0.3, +9.4] | 95 % (0 %) | ✘ | ✘ | ✘ | 0.1224 (0.1125) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin deepseek, google |
| gemma4 | C | ▲ | +6.7 [+3.0, +10.6] | 100 % (55 %) | ✔ | ✔ | ✔ | 0.0029 (0.0024) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | A | ▼ | -5.7 [-8.4, -3.3] | 100 % (96 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | H | ▼ | -10.5 [-15.6, -5.3] | 100 % (92 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| glm5.3-flash | O | ▲ | +4.2 [+1.0, +7.7] | 100 % (0 %) | ✔ | ✘ | ✘ | 0.0283 (0.0246) | **frágil** | falla P3 P5; cae sin google |
| glm5.3-flash | E | ▼ | -3.1 [-5.9, -0.1] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.0868 (0.0804) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, google |
| glm5.3-flash | N | ▼ | -3.7 [-7.1, -0.3] | 97 % (0 %) | ✘ | ✘ | ✘ | 0.0855 (—) | **no publicable** | N solo descriptivo (§23); cae sin google |
| google/gemini-3.7-flash | O | ▼ | -15.5 [-19.4, -11.3] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | E | ▲ | +13.1 [+7.3, +18.7] | 100 % (97 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | A | ▲ | +13.3 [+7.0, +19.0] | 100 % (84 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | H | ▼ | -7.1 [-12.7, -1.9] | 100 % (0 %) | ✔ | ✘ | ✔ | 0.0284 (0.0246) | **frágil** | falla P3 |
| google/gemini-4-argon | O | ▼ | -8.0 [-11.4, -4.6] | 100 % (93 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-4-argon | H | ▼ | -6.2 [-10.8, -2.1] | 99 % (12 %) | ✔ | ✔ | ✔ | 0.0111 (0.0092) | **robusta** | pasa P1–P3, P5, P6 |
| mimo-v2.6-flash | O | ▲ | +5.6 [+1.6, +9.5] | 98 % (0 %) | ✔ | ✘ | ✘ | 0.0278 (0.0242) | **frágil** | falla P3 P5; cae sin google |
| openai/gpt-5.6-luna | O | ▲ | +4.2 [+0.7, +7.9] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.0600 (0.0520) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin google |
| openai/gpt-5.6-luna | A | ▼ | -4.1 [-6.5, -1.6] | 100 % (36 %) | ✔ | ✔ | ✔ | 0.0041 (0.0034) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-5.6-luna | H | ▲ | +4.2 [+1.3, +7.1] | 100 % (6 %) | ✔ | ✘ | ✘ | 0.0259 (0.0226) | **frágil** | falla P3 P5; cae sin google |
| openai/gpt-6.1-sol#low | C | ▼ | -5.1 [-8.1, -2.1] | 100 % (22 %) | ✔ | ✔ | ✔ | 0.0082 (0.0069) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-6.1-sol#low | H | ▲ | +7.9 [+4.1, +12.0] | 100 % (92 %) | ✔ | ✔ | ✔ | 0.0006 (0.0005) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.6 | H | ▼ | -10.5 [-14.7, -6.1] | 100 % (98 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.8-flash | A | ▼ | -2.9 [-5.3, -0.4] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.0612 (0.0530) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin google |

## Variantes de cada marca candidata

Marca en cada variante (· = sin marca).

| modelo | rasgo | cuadro | rep0 | rep1 | AB | BA | sin anthropic | sin deepseek | sin google | sin openai | sin qwen | sin xiaomi | sin z-ai |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-haiku-5.5 | N | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| anthropic/claude-opus-5.5#low | O | ▲ | · | · | ▲ | · | · | · | · | ▲ | ▲ | ▲ | ▲ |
| anthropic/claude-opus-5.5#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek-v4-flash@2026-10-17 | E | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | A | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v4-pro-0813 | A | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v4-pro-0813 | N | ▼ | ▼ | · | ▼ | ▲ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek/deepseek-v4-pro-0813 | H | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | O | ▲ | · | ▲ | · | · | ▲ | · | · | ▲ | ▲ | ▲ | ▲ |
| gemma4 | C | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| gemma4 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| glm5.3-flash | O | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| glm5.3-flash | E | ▼ | · | ▼ | · | · | · | ▼ | · | ▼ | ▼ | ▼ | ▼ |
| glm5.3-flash | N | ▼ | ▼ | · | · | · | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | E | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | A | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | H | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| mimo-v2.6-flash | O | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-5.6-luna | O | ▲ | ▲ | · | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-5.6-luna | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-5.6-luna | H | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-6.1-sol#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen3.6 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| qwen3.8-flash | A | ▼ | ▼ | · | ▼ | · | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ |

## Puntuación con IC 95 %

| modelo | O | C | E | A | N | H |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 52 [46, 57] | 39 [34, 44] | 42 [37, 47] | 28 [24, 33] | 56 [51, 61] | 46 [41, 51] |
| anthropic/claude-opus-5.5#low | 55 [51, 59] | 33 [29, 37] | 42 [38, 46] | 38 [33, 43] | 49 [44, 54] | 51 [46, 55] |
| deepseek-v4-flash@2026-10-17 | 50 [45, 56] | 35 [31, 40] | 34 [30, 39] | 32 [28, 36] | 51 [45, 56] | 49 [44, 53] |
| deepseek/deepseek-v4-pro-0813 | 49 [45, 54] | 40 [36, 45] | 39 [35, 42] | 40 [36, 44] | 47 [43, 50] | 49 [46, 52] |
| gemma4 | 55 [50, 61] | 45 [40, 50] | 37 [32, 43] | 29 [26, 33] | 54 [48, 59] | 34 [28, 40] |
| glm5.3-flash | 55 [50, 60] | 39 [34, 43] | 38 [34, 42] | 34 [31, 39] | 47 [43, 52] | 45 [40, 50] |
| google/gemini-3.7-flash | 37 [32, 42] | 39 [34, 44] | 52 [47, 57] | 47 [42, 52] | 48 [43, 53] | 37 [32, 42] |
| google/gemini-4-argon | 44 [39, 49] | 36 [32, 42] | 38 [34, 43] | 35 [30, 40] | 52 [48, 57] | 38 [33, 43] |
| mimo-v2.6-flash | 56 [51, 61] | 40 [35, 44] | 43 [39, 48] | 36 [32, 41] | 51 [46, 56] | 42 [37, 47] |
| openai/gpt-5.6-luna | 55 [50, 60] | 41 [36, 46] | 39 [34, 44] | 31 [27, 35] | 52 [47, 57] | 48 [43, 52] |
| openai/gpt-6.1-sol#low | 52 [47, 57] | 34 [30, 38] | 38 [33, 42] | 33 [29, 38] | 49 [44, 53] | 51 [46, 55] |
| qwen3.6 | 55 [49, 60] | 41 [36, 47] | 42 [37, 48] | 35 [31, 40] | 54 [49, 59] | 34 [29, 39] |
| qwen3.8-flash | 49 [43, 55] | 36 [31, 42] | 40 [36, 44] | 32 [28, 36] | 50 [46, 55] | 44 [39, 49] |
