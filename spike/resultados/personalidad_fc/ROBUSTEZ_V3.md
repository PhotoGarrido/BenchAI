# Robustez de las marcas del cuadro v2 (PERSONALIDAD.md §26)

Generado por `analizar_robustez_v3.py`. 13 modelos, 7 laboratorios (anthropic, deepseek, google, openai, qwen, xiaomi, z-ai). Semilla 20261010. Sin llamadas a modelos.

**27 marcas** en el cuadro: 6 robustas · 10 frágiles · 11 no publicables.

P1 = signo replicado en las dos mitades (≥ 90 %) · P2 = réplica 0 y 1 · P3 = orden AB y BA · P4 = deseabilidad común · P5 = todos los paneles sin un laboratorio · P6 = BH q < 0,05 (78).

| modelo | rasgo | marca | dif [IC] | P1 signo (sig. ambas) | P2 | P3 | P4 | P5 | P6 q78 (q65) | nivel | por qué |
|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | O | ▼ | -5.6 [-11.0, -0.5] | 96 % (0 %) | ✘ | ✘ | ✘ | ✘ | 0.1088 (0.0950) | **no publicable** | falla 5 (P2 P3 P4 P5 P6); cae sin qwen |
| anthropic/claude-haiku-5.5 | C | ▼ | -8.4 [-12.6, -4.2] | 100 % (55 %) | ✔ | ✔ | ✘ | ✔ | 0.0023 (0.0019) | **frágil** | falla P4 |
| anthropic/claude-haiku-5.5 | A | ▼ | -10.1 [-15.6, -4.8] | 100 % (62 %) | ✔ | ✔ | ✔ | ✔ | 0.0017 (0.0014) | **robusta** | pasa P1–P6 |
| anthropic/claude-haiku-5.5 | N | ▲ | +5.2 [+0.3, +10.0] | 96 % (0 %) | ✘ | ✘ | ✔ | ✘ | 0.1121 (—) | **no publicable** | N solo descriptivo (§23); cae sin openai |
| anthropic/claude-haiku-5.5 | H | ▼ | -15.0 [-19.5, -10.3] | 100 % (100 %) | ✔ | ✔ | ✘ | ✔ | 0.0006 (0.0005) | **frágil** | falla P4 |
| deepseek-v4-flash@2026-10-17 | H | ▲ | +6.8 [+2.0, +11.8] | 100 % (0 %) | ✔ | ✔ | ✘ | ✔ | 0.0278 (0.0232) | **frágil** | falla P4 |
| gemma4 | O | ▲ | +12.3 [+6.9, +18.0] | 100 % (91 %) | ✔ | ✔ | ✔ | ✔ | 0.0006 (0.0005) | **robusta** | pasa P1–P6 |
| gemma4 | E | ▲ | +7.8 [+3.2, +12.6] | 100 % (42 %) | ✔ | ✔ | ✘ | ✔ | 0.0050 (0.0041) | **frágil** | falla P4 |
| glm5.3-flash | H | ▼ | -4.7 [-8.8, -0.7] | 99 % (0 %) | ✔ | ✘ | ✘ | ✘ | 0.0784 (0.0688) | **no publicable** | falla 4 (P3 P4 P5 P6); cae sin deepseek, qwen |
| google/gemini-3.7-flash | O | ▼ | -4.7 [-9.2, -0.4] | 94 % (0 %) | ✘ | ✘ | ✔ | ✘ | 0.1198 (0.1083) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin qwen, xiaomi |
| google/gemini-3.7-flash | C | ▲ | +13.6 [+9.5, +17.6] | 100 % (100 %) | ✔ | ✔ | ✘ | ✔ | 0.0006 (0.0005) | **frágil** | falla P4 |
| google/gemini-3.7-flash | A | ▲ | +13.0 [+8.9, +17.0] | 100 % (100 %) | ✔ | ✔ | ✔ | ✔ | 0.0006 (0.0005) | **robusta** | pasa P1–P6 |
| google/gemini-3.7-flash | H | ▲ | +5.4 [+1.4, +9.1] | 100 % (5 %) | ✘ | ✘ | ✘ | ✘ | 0.0278 (0.0232) | **no publicable** | falla 4 (P2 P3 P4 P5); cae sin anthropic |
| google/gemini-4-argon | O | ▼ | -10.4 [-15.0, -5.4] | 100 % (82 %) | ✔ | ✔ | ✔ | ✔ | 0.0006 (0.0005) | **robusta** | pasa P1–P6 |
| google/gemini-4-argon | H | ▼ | -4.8 [-9.7, -0.1] | 95 % (0 %) | ✘ | ✘ | ✘ | ✘ | 0.1200 (0.1083) | **no publicable** | falla 5 (P2 P3 P4 P5 P6); cae sin deepseek, google, qwen, xiaomi |
| mimo-v2.6-flash | O | ▲ | +6.4 [+1.4, +10.7] | 100 % (0 %) | ✔ | ✔ | ✔ | ✔ | 0.0377 (0.0314) | **robusta** | pasa P1–P6 |
| mimo-v2.6-flash | C | ▼ | -10.1 [-15.1, -5.3] | 100 % (88 %) | ✔ | ✔ | ✘ | ✔ | 0.0006 (0.0005) | **frágil** | falla P4 |
| openai/gpt-5.6-luna | O | ▼ | -6.0 [-10.6, -1.8] | 100 % (3 %) | ✔ | ✘ | ✘ | ✔ | 0.0289 (0.0241) | **no publicable** | se invierte en consenso, sin_ajuste |
| openai/gpt-5.6-luna | E | ▼ | -4.3 [-8.1, -0.7] | 98 % (0 %) | ✘ | ✘ | ✘ | ✘ | 0.1021 (0.0894) | **no publicable** | falla 5 (P2 P3 P4 P5 P6); cae sin google |
| openai/gpt-5.6-luna | N | ▼ | -4.1 [-8.2, -0.2] | 94 % (0 %) | ✘ | ✘ | ✘ | ✘ | 0.1326 (—) | **no publicable** | N solo descriptivo (§23); cae sin anthropic, xiaomi, z-ai |
| openai/gpt-6.1-sol#low | C | ▼ | -7.0 [-11.6, -2.7] | 100 % (24 %) | ✔ | ✔ | ✔ | ✔ | 0.0102 (0.0085) | **robusta** | pasa P1–P6 |
| openai/gpt-6.1-sol#low | E | ▼ | -7.6 [-12.4, -3.1] | 100 % (43 %) | ✔ | ✔ | ✘ | ✔ | 0.0072 (0.0060) | **frágil** | falla P4 |
| openai/gpt-6.1-sol#low | A | ▼ | -5.3 [-10.2, -0.3] | 96 % (0 %) | ✘ | ✘ | ✘ | ✘ | 0.1121 (0.1019) | **no publicable** | falla 5 (P2 P3 P4 P5 P6); cae sin google |
| openai/gpt-6.1-sol#low | N | ▼ | -6.0 [-11.2, -1.1] | 98 % (0 %) | ✔ | ✘ | ✘ | ✔ | 0.0743 (—) | **no publicable** | N solo descriptivo (§23) |
| qwen3.6 | O | ▲ | +8.2 [+2.6, +13.8] | 100 % (16 %) | ✔ | ✘ | ✘ | ✔ | 0.0128 (0.0107) | **frágil** | falla P3 P4 |
| qwen3.6 | C | ▲ | +11.2 [+5.9, +16.3] | 100 % (77 %) | ✔ | ✔ | ✘ | ✔ | 0.0017 (0.0014) | **frágil** | falla P4 |
| qwen3.6 | H | ▲ | +11.9 [+6.6, +17.0] | 100 % (86 %) | ✔ | ✔ | ✘ | ✔ | 0.0006 (0.0005) | **frágil** | falla P4 |

## Variantes de cada marca

Marca en cada variante (· = sin marca).

| modelo | rasgo | cuadro | rep0 | rep1 | AB | BA | consenso | sin ajuste |
|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | O | ▼ | ▼ | · | ▼ | · | · | · |
| anthropic/claude-haiku-5.5 | C | ▼ | ▼ | ▼ | ▼ | ▼ | · | · |
| anthropic/claude-haiku-5.5 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-haiku-5.5 | N | ▲ | ▲ | · | ▲ | · | ▲ | ▲ |
| anthropic/claude-haiku-5.5 | H | ▼ | ▼ | ▼ | ▼ | ▼ | · | · |
| deepseek-v4-flash@2026-10-17 | H | ▲ | ▲ | ▲ | ▲ | ▲ | · | · |
| gemma4 | O | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | E | ▲ | ▲ | ▲ | ▲ | ▲ | · | · |
| glm5.3-flash | H | ▼ | ▼ | ▼ | ▼ | · | · | · |
| google/gemini-3.7-flash | O | ▼ | · | ▼ | · | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | C | ▲ | ▲ | ▲ | ▲ | ▲ | · | · |
| google/gemini-3.7-flash | A | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | H | ▲ | ▲ | · | ▲ | · | · | · |
| google/gemini-4-argon | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | H | ▼ | · | · | · | ▼ | · | · |
| mimo-v2.6-flash | O | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| mimo-v2.6-flash | C | ▼ | ▼ | ▼ | ▼ | ▼ | · | · |
| openai/gpt-5.6-luna | O | ▼ | ▼ | ▼ | · | ▼ | ▲ | ▲ |
| openai/gpt-5.6-luna | E | ▼ | ▼ | · | · | ▼ | · | · |
| openai/gpt-5.6-luna | N | ▼ | · | ▼ | · | ▼ | · | · |
| openai/gpt-6.1-sol#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | E | ▼ | ▼ | ▼ | ▼ | ▼ | · | · |
| openai/gpt-6.1-sol#low | A | ▼ | · | ▼ | · | ▼ | · | · |
| openai/gpt-6.1-sol#low | N | ▼ | ▼ | ▼ | · | ▼ | · | · |
| qwen3.6 | O | ▲ | ▲ | ▲ | ▲ | · | · | · |
| qwen3.6 | C | ▲ | ▲ | ▲ | ▲ | ▲ | · | · |
| qwen3.6 | H | ▲ | ▲ | ▲ | ▲ | ▲ | · | · |

Consenso ≡ sin ajuste en la diferencia pareada: diferencia máxima 1.8e-15 puntos (cancelación de un d(i) común, §26).

## Marcas nuevas en alguna variante (no entran en el retrato)

- anthropic/claude-opus-5.5#low · C: consenso, sin_ajuste
- anthropic/claude-opus-5.5#low · H: BA, sin anthropic
- anthropic/claude-opus-5.5#low · O: consenso
- deepseek-v4-flash@2026-10-17 · A: consenso, sin_ajuste
- deepseek-v4-flash@2026-10-17 · E: consenso, sin_ajuste
- deepseek/deepseek-v4-pro-0813 · A: AB, BA, consenso, sin_ajuste
- deepseek/deepseek-v4-pro-0813 · C: AB, BA
- deepseek/deepseek-v4-pro-0813 · E: AB, BA
- deepseek/deepseek-v4-pro-0813 · H: AB, BA
- deepseek/deepseek-v4-pro-0813 · N: AB, BA, consenso, sin_ajuste
- deepseek/deepseek-v4-pro-0813 · O: AB, BA
- gemma4 · A: consenso, sin_ajuste
- gemma4 · C: consenso, sin_ajuste
- gemma4 · H: sin deepseek, sin qwen, sin xiaomi
- glm5.3-flash · E: consenso, sin_ajuste
- glm5.3-flash · N: consenso, sin_ajuste
- glm5.3-flash · O: consenso, sin_ajuste
- google/gemini-3.7-flash · E: consenso, sin_ajuste
- mimo-v2.6-flash · A: AB
- mimo-v2.6-flash · E: consenso, sin_ajuste
- mimo-v2.6-flash · H: AB, sin deepseek, sin qwen
- openai/gpt-5.6-luna · A: consenso, sin_ajuste
- openai/gpt-5.6-luna · H: BA, sin anthropic
- openai/gpt-6.1-sol#low · H: consenso, sin_ajuste
- qwen3.6 · A: BA
- qwen3.6 · E: BA, sin openai
- qwen3.8-flash · A: consenso, sin google, sin_ajuste
- qwen3.8-flash · H: AB, rep0, sin anthropic

## Puntuación según la fuente de la deseabilidad

Propia (cuadro) / consenso / sin ajuste. La comparación entre modelos no cambia entre consenso y sin ajuste; cambia el nivel absoluto.

| modelo | O | C | E | A | N | H |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 46/52/80 | 31/39/62 | 42/42/68 | 25/28/56 | 55/56/80 | 26/38/67 |
| anthropic/claude-opus-5.5#low | 50/55/84 | 38/33/56 | 41/42/68 | 33/38/65 | 52/49/74 | 36/43/72 |
| deepseek-v4-flash@2026-10-17 | 49/50/79 | 36/35/58 | 41/34/60 | 38/32/59 | 52/51/75 | 46/41/71 |
| deepseek/deepseek-v4-pro-0813 | 51/49/78 | 36/40/63 | 43/39/64 | 36/40/67 | 49/47/71 | 43/41/70 |
| gemma4 | 62/55/84 | 40/45/67 | 48/37/63 | 33/29/57 | 53/54/78 | 43/37/67 |
| glm5.3-flash | 54/55/84 | 40/39/62 | 38/38/63 | 32/34/62 | 52/47/72 | 35/40/70 |
| google/gemini-3.7-flash | 47/37/65 | 51/39/62 | 45/52/78 | 47/47/74 | 50/48/73 | 45/37/66 |
| google/gemini-4-argon | 42/44/72 | 39/36/59 | 38/38/64 | 36/35/62 | 51/52/77 | 35/40/69 |
| mimo-v2.6-flash | 57/56/85 | 29/40/62 | 41/43/69 | 38/36/64 | 52/51/76 | 45/39/68 |
| openai/gpt-5.6-luna | 46/55/84 | 39/41/64 | 36/39/64 | 36/31/58 | 47/52/77 | 36/40/69 |
| openai/gpt-6.1-sol#low | 53/52/81 | 32/34/56 | 33/38/64 | 30/33/61 | 45/49/73 | 39/46/75 |
| qwen3.6 | 59/55/83 | 49/41/64 | 37/42/68 | 32/35/63 | 48/54/78 | 51/38/67 |
| qwen3.8-flash | 50/49/78 | 39/36/59 | 41/40/66 | 38/32/59 | 52/50/75 | 36/39/68 |

## Relación con el ISS (solo descriptiva)

Spearman entre la puntuación del cuadro y el ISS publicado, n = 10 modelos con ISS (deepseek-v4-flash@2026-10-17, deepseek/deepseek-v4-pro-0813, google/gemini-4-argon sin ISS). IC 95 % por bootstrap de modelos (2000). **Con n = 10 el IC es muy ancho; no se contrasta ninguna hipótesis.**

| rasgo | ρ | IC 95 % |
|---|---|---|
| Apertura | +0.42 | [-0.37, +0.96] |
| Responsabilidad | +0.73 | [+0.19, +0.95] |
| Extraversión | +0.39 | [-0.27, +0.87] |
| Amabilidad | +0.25 | [-0.50, +0.87] |
| Neuroticismo | +0.05 | [-0.61, +0.75] |
| Honestidad-Humildad | +0.26 | [-0.42, +0.84] |

## Retrato publicable propuesto

Solo marcas robustas de O, C, A, H; E robusta con aviso; N solo descriptivo (§26).

- **anthropic/claude-haiku-5.5**: **menos Amabilidad** (pone límites y se defiende). *Neuroticismo (descriptivo): 55.* Tendencias frágiles, no publicadas: C▼, H▼.
- **anthropic/claude-opus-5.5#low**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 52.*
- **deepseek-v4-flash@2026-10-17**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 52.* Tendencias frágiles, no publicadas: H▲.
- **deepseek/deepseek-v4-pro-0813**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 49.*
- **gemma4**: **más Apertura** (curioso, busca lo nuevo). *Neuroticismo (descriptivo): 53.* Tendencias frágiles, no publicadas: E▲.
- **glm5.3-flash**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 52.*
- **google/gemini-3.7-flash**: **más Amabilidad** (cede y coopera). *Neuroticismo (descriptivo): 50.* Tendencias frágiles, no publicadas: C▲.
- **google/gemini-4-argon**: **menos Apertura** (prefiere lo conocido). *Neuroticismo (descriptivo): 51.*
- **mimo-v2.6-flash**: **más Apertura** (curioso, busca lo nuevo). *Neuroticismo (descriptivo): 52.* Tendencias frágiles, no publicadas: C▼.
- **openai/gpt-5.6-luna**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 47.*
- **openai/gpt-6.1-sol#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad). *Neuroticismo (descriptivo): 45.* Tendencias frágiles, no publicadas: E▼.
- **qwen3.6**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 48.* Tendencias frágiles, no publicadas: O▲, C▲, H▲.
- **qwen3.8-flash**: perfil próximo al de los demás modelos. *Neuroticismo (descriptivo): 52.*
