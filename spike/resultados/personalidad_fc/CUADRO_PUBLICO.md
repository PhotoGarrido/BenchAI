# Cuadro público de personalidad · conducta comparada (PERSONALIDAD.md §28)

Generado por `cuadro_publico_v3.py`. Selección: personalidad_v3_seleccion.json. 13 modelos, 7 laboratorios (anthropic, deepseek, google, openai, qwen, xiaomi, z-ai); situaciones por rasgo: O 59, C 56, E 57, A 57, N 57, H 59. Semilla 20261010. Sin llamadas a modelos.
Fuera por banco incompleto (< 95 %): deepseek-v4-flash (40 %), mistralai/mistral-large-4-0 (40 %), moonshotai/kimi-k3 (40 %), qwen/qwen3.8-max-0902#low (40 %), x-ai/grok-4.5 (40 %), z-ai/glm-5.3 (40 %).

**Puntuación** = 50 + 50·media(elige el polo alto − deseabilidad media del panel): 50 = elige lo que el conjunto de modelos juzga admirable. **▲/▼** = elige el polo alto más/menos a menudo que los demás modelos en las mismas situaciones (comparación pareada, IC 95 %), solo si la marca es **robusta** (P1–P3, P5, P6). Extraversión con aviso de fiabilidad; Neuroticismo solo descriptivo, sin marca.

| modelo | ISS | Apertura | Responsabilidad | Extraversión † | Amabilidad | Neuroticismo ‡ | Honestidad-Humildad |
|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 10.3 | 52 | 39 | 42 | 28 ▼ | 56 | 38 |
| anthropic/claude-opus-5.5#low | 12.5 | 55 | 33 ▼ | 42 | 38 | 49 | 43 |
| deepseek-v4-flash@2026-10-17 | — | 50 | 35 | 34 ▼ | 32 | 51 | 41 |
| deepseek/deepseek-v4-pro-0813 | — | 49 | 40 | 39 | 40 | 47 | 41 |
| gemma4 | 28.1 | 55 | 45 ▲ | 37 | 29 ▼ | 54 | 37 |
| glm5.3-flash | 28.9 | 55 | 39 | 38 | 34 | 47 | 40 |
| google/gemini-3.7-flash | 55.2 | 37 ▼ | 39 | 52 ▲ | 47 ▲ | 48 | 37 |
| google/gemini-4-argon | — | 44 ▼ | 36 | 38 | 35 | 52 | 40 |
| mimo-v2.6-flash | 12.6 | 56 | 40 | 43 | 36 | 51 | 39 |
| openai/gpt-5.6-luna | 7.6 | 55 | 41 | 39 | 31 | 52 | 40 |
| openai/gpt-6.1-sol#low | 13.2 | 52 | 34 ▼ | 38 | 33 | 49 | 46 ▲ |
| qwen3.6 | 23.2 | 55 | 41 | 42 | 35 | 54 | 38 |
| qwen3.8-flash | 24.8 | 49 | 36 | 40 | 32 | 50 | 39 |

† fiabilidad baja (§23): marca solo si robusta, con aviso. ‡ solo descriptivo (§23).

## Validez con la definición de §28 (G3 y G4 de §21)

Mismos cálculos que `analizar_v3.py` (G3: r media entre facetas del mismo rasgo frente a facetas de otros rasgos; G4: Spearman-Brown de mitades pares/impares entre modelos), pero sobre la puntuación de §28 en vez de la ajustada por la deseabilidad propia.

| rasgo | G3 dentro / fuera | G3 | G4 | G4 ≥ 0,70 | en §28 |
|---|---|---|---|---|---|
| Apertura | +0.46 / -0.08 | ✔ | 0.94 | ✔ | con marca |
| Responsabilidad | +0.27 / -0.00 | ✔ | 0.81 | ✔ | con marca |
| Extraversión | +0.27 / +0.02 | ✔ | 0.93 | ✔ | marca solo robusta, con aviso |
| Amabilidad | +0.56 / -0.05 | ✔ | 0.86 | ✔ | con marca |
| Neuroticismo | +0.04 / -0.03 | ✔ | 0.62 | ✘ | solo descriptivo |
| Honestidad-Humildad | -0.07 / -0.04 | ✘ | 0.13 | ✘ | con marca |

**CONFLICTO entre §28 y la consistencia con la definición nueva (lo resuelve David; este cuadro aplica §28 sin cambios):**

- **Extraversión**: marca solo con aviso de fiabilidad (§28), pero G4 = 0.93 ≥ 0.70.
- **Honestidad-Humildad**: lleva marca (§28), pero G4 = 0.13 < 0.70.

### Escenario alternativo, NO decidido: marca en los rasgos con G4 ≥ 0,70

Rasgos con marca: Apertura, Responsabilidad, Extraversión, Amabilidad; el resto, solo descriptivo. Mismos niveles de robustez (sin la regla de N).

| modelo | Apertura | Responsabilidad | Extraversión | Amabilidad | Neuroticismo | Honestidad-Humildad |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 52 | 39 | 42 | 28 ▼ | 56 | 38 |
| anthropic/claude-opus-5.5#low | 55 | 33 ▼ | 42 | 38 | 49 | 43 |
| deepseek-v4-flash@2026-10-17 | 50 | 35 | 34 ▼ | 32 | 51 | 41 |
| deepseek/deepseek-v4-pro-0813 | 49 | 40 | 39 | 40 | 47 | 41 |
| gemma4 | 55 | 45 ▲ | 37 | 29 ▼ | 54 | 37 |
| glm5.3-flash | 55 | 39 | 38 | 34 | 47 | 40 |
| google/gemini-3.7-flash | 37 ▼ | 39 | 52 ▲ | 47 ▲ | 48 | 37 |
| google/gemini-4-argon | 44 ▼ | 36 | 38 | 35 | 52 | 40 |
| mimo-v2.6-flash | 56 | 40 | 43 | 36 | 51 | 39 |
| openai/gpt-5.6-luna | 55 | 41 | 39 | 31 | 52 | 40 |
| openai/gpt-6.1-sol#low | 52 | 34 ▼ | 38 | 33 | 49 | 46 |
| qwen3.6 | 55 | 41 | 42 | 35 | 54 | 38 |
| qwen3.8-flash | 49 | 36 | 40 | 32 | 50 | 39 |

- **anthropic/claude-haiku-5.5**: **menos Amabilidad** (pone límites y se defiende).
- **anthropic/claude-opus-5.5#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad).
- **deepseek-v4-flash@2026-10-17**: **menos Extraversión** (prefiere calma y segundo plano).
- **deepseek/deepseek-v4-pro-0813**: perfil próximo al de los demás modelos.
- **gemma4**: **más Responsabilidad** (cumple y planifica); **menos Amabilidad** (pone límites y se defiende).
- **glm5.3-flash**: perfil próximo al de los demás modelos.
- **google/gemini-3.7-flash**: **menos Apertura** (prefiere lo conocido); **más Extraversión** (busca gente y protagonismo); **más Amabilidad** (cede y coopera).
- **google/gemini-4-argon**: **menos Apertura** (prefiere lo conocido).
- **mimo-v2.6-flash**: perfil próximo al de los demás modelos.
- **openai/gpt-5.6-luna**: perfil próximo al de los demás modelos.
- **openai/gpt-6.1-sol#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad).
- **qwen3.6**: perfil próximo al de los demás modelos.
- **qwen3.8-flash**: perfil próximo al de los demás modelos.

## Retrato de cada modelo (§28)

- **anthropic/claude-haiku-5.5**: **menos Amabilidad** (pone límites y se defiende). *Neuroticismo (descriptivo): 56.*
- **anthropic/claude-opus-5.5#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad). *Neuroticismo (descriptivo): 49.*
- **deepseek-v4-flash@2026-10-17**: **menos Extraversión** (prefiere calma y segundo plano) *[Extraversión: fiabilidad baja (§23), con aviso]*. *Neuroticismo (descriptivo): 51.* Tendencias frágiles, no publicadas: A▼.
- **deepseek/deepseek-v4-pro-0813**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 47.* Tendencias frágiles, no publicadas: A▲.
- **gemma4**: **más Responsabilidad** (cumple y planifica); **menos Amabilidad** (pone límites y se defiende). *Neuroticismo (descriptivo): 54.*
- **glm5.3-flash**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 47.* Tendencias frágiles, no publicadas: O▲.
- **google/gemini-3.7-flash**: **menos Apertura** (prefiere lo conocido); **más Amabilidad** (cede y coopera); **más Extraversión** (busca gente y protagonismo) *[Extraversión: fiabilidad baja (§23), con aviso]*. *Neuroticismo (descriptivo): 48.*
- **google/gemini-4-argon**: **menos Apertura** (prefiere lo conocido). *Neuroticismo (descriptivo): 52.*
- **mimo-v2.6-flash**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 51.* Tendencias frágiles, no publicadas: O▲.
- **openai/gpt-5.6-luna**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 52.* Tendencias frágiles, no publicadas: A▼.
- **openai/gpt-6.1-sol#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas). *Neuroticismo (descriptivo): 49.*
- **qwen3.6**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 54.*
- **qwen3.8-flash**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 50.*

## Marcas candidatas y su nivel

**25 marcas candidatas** (IC de la comparación que excluye 0): 11 robustas · 5 frágiles · 9 no publicables.

P1 = signo replicado en las dos mitades (≥ 90 %) · P2 = réplica 0 y 1 · P3 = orden AB y BA · P5 = todos los paneles sin un laboratorio · P6 = BH q < 0,05 sobre 78 pruebas (entre paréntesis, sin N).

| modelo | rasgo | marca | dif [IC] | P1 signo (sig. ambas) | P2 | P3 | P5 | P6 q (sin N) | nivel | por qué |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | A | ▼ | -6.9 [-10.6, -3.3] | 100 % (64 %) | ✔ | ✔ | ✔ | 0.0026 (0.0022) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-haiku-5.5 | N | ▲ | +5.5 [+1.8, +9.7] | 99 % (15 %) | ✔ | ✘ | ✔ | 0.0162 (—) | **no publicable** | N solo descriptivo (§23) |
| anthropic/claude-opus-5.5#low | O | ▲ | +4.2 [+0.1, +8.6] | 94 % (0 %) | ✘ | ✘ | ✘ | 0.1582 (0.1498) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin deepseek, google |
| anthropic/claude-opus-5.5#low | C | ▼ | -5.6 [-8.3, -2.8] | 100 % (78 %) | ✔ | ✔ | ✔ | 0.0006 (0.0005) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | E | ▼ | -6.4 [-9.0, -3.8] | 100 % (94 %) | ✔ | ✔ | ✔ | 0.0006 (0.0005) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | A | ▼ | -3.4 [-5.7, -1.1] | 100 % (8 %) | ✔ | ✘ | ✔ | 0.0307 (0.0274) | **frágil** | falla P3 |
| deepseek/deepseek-v4-pro-0813 | A | ▲ | +5.4 [+2.5, +8.5] | 100 % (61 %) | ✔ | ✘ | ✔ | 0.0026 (0.0022) | **frágil** | falla P3 |
| deepseek/deepseek-v4-pro-0813 | N | ▼ | -4.4 [-8.4, -0.8] | 99 % (0 %) | ✘ | ✘ | ✔ | 0.0854 (—) | **no publicable** | N solo descriptivo (§23) |
| gemma4 | O | ▲ | +4.7 [+0.1, +8.8] | 94 % (0 %) | ✘ | ✘ | ✘ | 0.1582 (0.1498) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin deepseek, google, xiaomi |
| gemma4 | C | ▲ | +6.7 [+3.0, +10.5] | 100 % (62 %) | ✔ | ✔ | ✔ | 0.0031 (0.0026) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | A | ▼ | -5.7 [-8.5, -3.3] | 100 % (95 %) | ✔ | ✔ | ✔ | 0.0006 (0.0005) | **robusta** | pasa P1–P3, P5, P6 |
| glm5.3-flash | O | ▲ | +4.2 [+0.8, +7.2] | 100 % (0 %) | ✔ | ✘ | ✘ | 0.0477 (0.0422) | **frágil** | falla P3 P5; cae sin google |
| glm5.3-flash | E | ▼ | -3.1 [-5.8, -0.2] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.1287 (0.1242) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, google, qwen, xiaomi |
| glm5.3-flash | N | ▼ | -3.7 [-7.0, -0.2] | 97 % (0 %) | ✘ | ✘ | ✘ | 0.1192 (—) | **no publicable** | N solo descriptivo (§23); cae sin google |
| google/gemini-3.7-flash | O | ▼ | -15.5 [-19.8, -11.6] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0006 (0.0005) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | E | ▲ | +13.1 [+7.3, +18.7] | 100 % (98 %) | ✔ | ✔ | ✔ | 0.0006 (0.0005) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | A | ▲ | +13.3 [+7.1, +19.3] | 100 % (82 %) | ✔ | ✔ | ✔ | 0.0006 (0.0005) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-4-argon | O | ▼ | -8.0 [-11.5, -4.6] | 100 % (94 %) | ✔ | ✔ | ✔ | 0.0006 (0.0005) | **robusta** | pasa P1–P3, P5, P6 |
| mimo-v2.6-flash | O | ▲ | +5.6 [+1.7, +9.6] | 100 % (1 %) | ✔ | ✘ | ✘ | 0.0322 (0.0286) | **frágil** | falla P3 P5; cae sin google |
| mimo-v2.6-flash | E | ▲ | +3.1 [+0.2, +6.4] | 95 % (0 %) | ✘ | ✘ | ✘ | 0.1479 (0.1417) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin deepseek, openai, z-ai |
| openai/gpt-5.6-luna | O | ▲ | +4.2 [+0.9, +8.0] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.0796 (0.0701) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin google |
| openai/gpt-5.6-luna | A | ▼ | -4.1 [-6.4, -1.6] | 100 % (34 %) | ✘ | ✔ | ✔ | 0.0059 (0.0049) | **frágil** | falla P2 |
| openai/gpt-6.1-sol#low | C | ▼ | -5.1 [-8.1, -1.9] | 100 % (26 %) | ✔ | ✔ | ✔ | 0.0120 (0.0100) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-6.1-sol#low | H | ▲ | +6.7 [+2.9, +10.5] | 100 % (66 %) | ✔ | ✔ | ✔ | 0.0035 (0.0030) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.8-flash | A | ▼ | -2.9 [-5.4, -0.3] | 96 % (0 %) | ✘ | ✘ | ✔ | 0.0796 (0.0701) | **no publicable** | falla 3 (P2 P3 P6) |

## Variantes de cada marca candidata

Marca en cada variante (· = sin marca).

| modelo | rasgo | cuadro | rep0 | rep1 | AB | BA | sin anthropic | sin deepseek | sin google | sin openai | sin qwen | sin xiaomi | sin z-ai |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-haiku-5.5 | N | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| anthropic/claude-opus-5.5#low | O | ▲ | · | · | ▲ | · | ▲ | · | · | ▲ | ▲ | ▲ | ▲ |
| anthropic/claude-opus-5.5#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | E | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | A | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek/deepseek-v4-pro-0813 | A | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v4-pro-0813 | N | ▼ | ▼ | · | ▼ | ▲ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| gemma4 | O | ▲ | · | ▲ | · | · | ▲ | · | · | ▲ | ▲ | · | ▲ |
| gemma4 | C | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| glm5.3-flash | O | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| glm5.3-flash | E | ▼ | · | ▼ | · | · | · | ▼ | · | ▼ | · | · | ▼ |
| glm5.3-flash | N | ▼ | ▼ | · | · | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | E | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | A | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-4-argon | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| mimo-v2.6-flash | O | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| mimo-v2.6-flash | E | ▲ | · | · | ▲ | · | ▲ | · | ▲ | · | ▲ | ▲ | · |
| openai/gpt-5.6-luna | O | ▲ | ▲ | · | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-5.6-luna | A | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen3.8-flash | A | ▼ | ▼ | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |

## Puntuación con IC 95 %

| modelo | O | C | E | A | N | H |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 52 [46, 57] | 39 [34, 44] | 42 [37, 47] | 28 [24, 33] | 56 [51, 61] | 38 [34, 42] |
| anthropic/claude-opus-5.5#low | 55 [51, 60] | 33 [29, 37] | 42 [38, 47] | 38 [33, 43] | 49 [45, 55] | 43 [38, 48] |
| deepseek-v4-flash@2026-10-17 | 50 [45, 56] | 35 [31, 40] | 34 [30, 39] | 32 [28, 36] | 51 [46, 56] | 41 [36, 46] |
| deepseek/deepseek-v4-pro-0813 | 49 [45, 54] | 40 [36, 45] | 39 [35, 43] | 40 [36, 43] | 47 [43, 50] | 41 [37, 45] |
| gemma4 | 55 [50, 61] | 45 [39, 50] | 37 [32, 42] | 29 [26, 33] | 54 [49, 59] | 37 [32, 41] |
| glm5.3-flash | 55 [50, 60] | 39 [35, 43] | 38 [33, 42] | 34 [31, 38] | 47 [43, 52] | 40 [36, 44] |
| google/gemini-3.7-flash | 37 [32, 42] | 39 [34, 44] | 52 [48, 57] | 47 [42, 52] | 48 [43, 53] | 37 [33, 41] |
| google/gemini-4-argon | 44 [39, 49] | 36 [32, 41] | 38 [34, 43] | 35 [31, 39] | 52 [48, 56] | 40 [35, 44] |
| mimo-v2.6-flash | 56 [51, 62] | 40 [35, 44] | 43 [39, 48] | 36 [32, 41] | 51 [46, 56] | 39 [34, 43] |
| openai/gpt-5.6-luna | 55 [50, 60] | 41 [36, 46] | 39 [34, 43] | 31 [27, 35] | 52 [47, 57] | 40 [35, 45] |
| openai/gpt-6.1-sol#low | 52 [48, 57] | 34 [29, 38] | 38 [33, 43] | 33 [29, 38] | 49 [44, 53] | 46 [41, 51] |
| qwen3.6 | 55 [49, 60] | 41 [36, 47] | 42 [37, 47] | 35 [31, 39] | 54 [49, 59] | 38 [33, 42] |
| qwen3.8-flash | 49 [43, 55] | 36 [31, 41] | 40 [36, 44] | 32 [28, 36] | 50 [45, 55] | 39 [34, 43] |
