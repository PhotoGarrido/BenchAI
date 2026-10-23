# Cuadro público de personalidad · conducta comparada (PERSONALIDAD.md §28)

Generado por `cuadro_publico_v3.py`. Selección: personalidad_v3_seleccion.json. 14 modelos, 7 laboratorios (anthropic, deepseek, google, openai, qwen, xiaomi, z-ai); situaciones por rasgo: O 59, C 56, E 57, A 57, N 19, H 48. Semilla 20261010. Sin llamadas a modelos. Escala de Honestidad-Humildad: I1-H en binario: 48 situaciones calibradas por dificultad, 12 por faceta (PERSONALIDAD.md §36-37). Escala de Neuroticismo: I1-N en binario, 19 elegidas por R1 (PERSONALIDAD.md §39-40).
Fuera por cobertura (§41.1: O, C, E y A del v3, completos o en forma corta; H y N de I1): deepseek-v4-flash (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %), mistralai/mistral-large-4-0 (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %), x-ai/grok-4.5 (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %). **Fuera de la norma por validez (§41.2, perfil no interpretable):** deepseek/deepseek-v4-pro-0813 (coherencia de la deseabilidad 0,64 (no interpretable)). **Pendientes de completar (§45.2, solo forma corta; no se publican):** moonshotai/kimi-k3 (forma corta en O, C, E, A, N, H).

**Puntuación** = 50 + 50·media(elige el polo alto − deseabilidad media del panel): 50 = elige lo que el conjunto de modelos juzga admirable. **▲/▼** = elige el polo alto más/menos a menudo que los demás modelos en las mismas situaciones (comparación pareada, IC 95 %), solo si la marca es **robusta** (P1–P3, P5, P6). Neuroticismo con marca desde §40 (sus marcas pasan además R4 de §30.2).

| modelo | ISS | Apertura | Responsabilidad | Extraversión | Amabilidad | Neuroticismo | Honestidad-Humildad |
|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 10.3 | 51 | 39 | 42 | 28 ▼ | 64 | 46 |
| anthropic/claude-opus-5.5#low | 12.5 | 54 | 33 ▼ | 42 | 38 | 43 ▼ | 51 ▲ |
| deepseek-v4-flash@2026-10-17 | 21.1 | 50 | 36 | 34 ▼ | 31 | 62 | 49 ▲ |
| gemma4 | 28.1 | 55 | 45 ▲ | 37 | 29 ▼ | 68 ▲ | 34 ▼ |
| glm5.3-flash | 28.9 | 54 | 39 | 37 | 34 | 62 | 45 |
| google/gemini-3.7-flash | 55.2 | 36 ▼ | 39 | 52 ▲ | 47 ▲ | 51 | 37 |
| google/gemini-4-argon | — | 43 ▼ | 37 | 38 | 35 | 42 ▼ | 38 |
| mimo-v2.6-flash | 12.6 | 56 | 40 | 43 | 36 | 62 | 42 |
| openai/gpt-5.6-luna | 7.6 | 54 | 41 | 38 | 31 | 59 | 47 |
| openai/gpt-6.1-sol#low | 13.2 | 52 | 34 ▼ | 37 | 33 | 45 ▼ | 51 ▲ |
| qwen3.6 | 23.2 | 54 | 42 | 42 | 35 | 74 ▲ | 34 ▼ |
| qwen3.8-flash | 24.8 | 48 | 36 | 40 | 32 | 62 | 44 |
| qwen/qwen3.8-max-0902#low | — | 49 | 36 | 47 ▲ | 33 | 50 | 44 |
| z-ai/glm-5.3 | — | 55 | 38 | 42 | 34 | 54 | 47 |

Neuroticismo: I1-N en binario (19 elegidas por R1; ansiedad 7, hostilidad 6, depresion 3, impulsividad 2, vulnerabilidad 1); sin situaciones de autoconciencia. Pasó §39 (§40). Marcas con las cinco comprobaciones de §28 y R4 de §30.2.

## Validez con la definición de §28 (G3 y G4 de §21)

Mismos cálculos que `analizar_v3.py` (G3: r media entre facetas del mismo rasgo frente a facetas de otros rasgos; G4: Spearman-Brown de mitades pares/impares entre modelos), pero sobre la puntuación de §28 en vez de la ajustada por la deseabilidad propia. G4 (b): mediana de Spearman-Brown en 200 particiones al azar equilibradas por faceta. Revalidación automática (§41.3): un rasgo con marca que no pasa G4 (a), G4 (b) ≥ 0,70 y G3 pierde sus marcas.

| rasgo | G3 dentro / fuera | G3 | G4 (a) | G4 (b) | listón §41.3 | en §28 |
|---|---|---|---|---|---|---|
| Apertura | +0.44 / -0.05 | ✔ | 0.93 | 0,90 | ✔ | con marca |
| Responsabilidad | +0.19 / +0.01 | ✔ | 0.84 | 0,75 | ✔ | con marca |
| Extraversión | +0.27 / -0.00 | ✔ | 0.91 | 0,89 | ✔ | con marca |
| Amabilidad | +0.54 / -0.07 | ✔ | 0.84 | 0,91 | ✔ | con marca |
| Neuroticismo | +0.41 / +0.02 | ✔ | 0.88 | 0,90 | ✔ | con marca |
| Honestidad-Humildad | +0.53 / -0.12 | ✔ | 0.94 | 0,93 | ✔ | con marca |

Revalidación automática (§41.3): todos los rasgos con marca pasan el listón.

## Validez por modelo (§41.2)

Índices calculados sobre todas las respuestas del modelo en los instrumentos del cuadro (R3 del v3 en O, C, E y A; binario de I1-H e I1-N; deseabilidad). Umbrales fijados antes de calcular: posición (Δ AB−BA) aviso/no interpretable a partir de 0,20/0,30; posición (fracción de A) aviso/no interpretable a partir de |A − 0,5| = 0,10/|A − 0,5| = 0,15; no válidas aviso/no interpretable a partir de 5,0 %/10,0 %; retest aviso/no interpretable a partir de 0,60/0,40; coherencia de la deseabilidad aviso/no interpretable a partir de 0,75/0,65. Un perfil **no interpretable** sale de la norma: no entra en la media de los demás, ni en d̄, ni en la selección de N, ni en BH, y no lleva puntuaciones, marcas ni retrato.

| modelo | Δ AB−BA | fracción de A | no válidas | retest | coherencia deseabilidad | nivel |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | -0,04 | 0,48 | 0,0 % | 0,93 | 0,90 | **válido** |
| anthropic/claude-opus-5.5#low | -0,05 | 0,47 | 0,0 % | 0,96 | 0,92 | **válido** |
| deepseek-v4-flash@2026-10-17 | -0,09 | 0,45 | 0,0 % | 0,95 | 0,80 | **válido** |
| deepseek/deepseek-v4-pro-0813 | -0,30 ⚠ | 0,35 ⚠ | 0,0 % | 0,80 | 0,64 ✘ | **no interpretable** |
| gemma4 | -0,09 | 0,46 | 0,1 % | 0,95 | 0,83 | **válido** |
| glm5.3-flash | -0,10 | 0,45 | 0,0 % | 0,87 | 0,83 | **válido** |
| google/gemini-3.7-flash | -0,06 | 0,47 | 0,0 % | 0,90 | 0,90 | **válido** |
| google/gemini-4-argon | -0,09 | 0,46 | 1,5 % | 0,89 | 0,92 | **válido** |
| mimo-v2.6-flash | 0,00 | 0,50 | 0,0 % | 0,86 | 0,75 | **válido** |
| openai/gpt-5.6-luna | 0,02 | 0,51 | 0,0 % | 0,91 | 0,82 | **válido** |
| openai/gpt-6.1-sol#low | -0,06 | 0,47 | 0,0 % | 0,97 | 0,89 | **válido** |
| qwen3.6 | 0,00 | 0,50 | 0,0 % | 0,85 | 0,76 | **válido** |
| qwen3.8-flash | -0,11 | 0,44 | 0,0 % | 0,82 | 0,77 | **válido** |
| qwen/qwen3.8-max-0902#low | -0,10 | 0,45 | 0,0 % | 0,90 | 0,84 | **válido** |
| z-ai/glm-5.3 | 0,04 | 0,52 | 0,1 % | 0,86 | 0,83 | **válido** |

⚠ = zona de aviso · ✘ = no interpretable.

### Perfiles no interpretables

Su perfil no se lee como retrato: el cuadro no publica puntuaciones ni marcas suyas.

| modelo | motivo |
|---|---|
| deepseek/deepseek-v4-pro-0813 | coherencia de la deseabilidad 0,64 (no interpretable) |

## Pendientes de completar (§45.2)

Medidos solo con la forma corta en algún rasgo. Sus datos se guardan y cuentan para la forma completa, pero **no entran en el cuadro público** (ni en la norma de los demás) hasta tenerla: sin puntuaciones, marcas ni retrato. Índices de validez de §41.2, solo informativos.

| modelo | rasgos en forma corta | Δ AB−BA | fracción de A | no válidas | retest | coherencia deseabilidad | nivel |
|---|---|---|---|---|---|---|---|
| moonshotai/kimi-k3 | O, C, E, A, N, H | -0,05 | 0,47 | 0,0 % | 0,84 | 0,85 | válido |

## Retrato de cada modelo (§28)

- **anthropic/claude-haiku-5.5**: **menos Amabilidad** (pone límites y se defiende).
- **anthropic/claude-opus-5.5#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas); **menos Neuroticismo** (se mantiene sereno).
- **deepseek-v4-flash@2026-10-17**: **menos Extraversión** (prefiere calma y segundo plano); **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **gemma4**: **más Responsabilidad** (cumple y planifica); **menos Amabilidad** (pone límites y se defiende); **menos Honestidad-Humildad** (acepta ventajas y se promociona); **más Neuroticismo** (reacciona, se preocupa).
- **glm5.3-flash**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: E▼.
- **google/gemini-3.7-flash**: **menos Apertura** (prefiere lo conocido); **más Extraversión** (busca gente y protagonismo); **más Amabilidad** (cede y coopera). Tendencias frágiles, no publicadas: H▼.
- **google/gemini-4-argon**: **menos Apertura** (prefiere lo conocido); **menos Neuroticismo** (se mantiene sereno). Tendencias frágiles, no publicadas: H▼.
- **mimo-v2.6-flash**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: O▲.
- **openai/gpt-5.6-luna**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: A▼, H▲.
- **openai/gpt-6.1-sol#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas); **menos Neuroticismo** (se mantiene sereno).
- **qwen3.6**: **menos Honestidad-Humildad** (acepta ventajas y se promociona); **más Neuroticismo** (reacciona, se preocupa).
- **qwen3.8-flash**: perfil próximo al de los demás modelos.
- **qwen/qwen3.8-max-0902#low**: **más Extraversión** (busca gente y protagonismo).
- **z-ai/glm-5.3**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: O▲.

## Marcas candidatas y su nivel

**40 marcas candidatas** (IC de la comparación que excluye 0): 21 robustas · 7 frágiles · 12 no publicables.

P1 = signo replicado en las dos mitades (≥ 90 %) · P2 = réplica 0 y 1 · P3 = orden AB y BA · P5 = todos los paneles sin un laboratorio · P6 = BH q < 0,05 sobre 84 pruebas (entre paréntesis, sin N).

| modelo | rasgo | marca | dif [IC] | P1 signo (sig. ambas) | P2 | P3 | P5 | P6 q (sin N) | nivel | por qué |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | A | ▼ | -6.4 [-10.1, -2.9] | 100 % (55 %) | ✔ | ✔ | ✔ | 0.0028 (0.0028) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-haiku-5.5 | N | ▲ | +7.9 [+0.7, +15.9] | 91 % (0 %) | ✔ | ✘ | ✘ | 0.0874 (—) | **no publicable** | falla 3 (P3 P5 P6); cae sin anthropic, google, openai |
| anthropic/claude-opus-5.5#low | C | ▼ | -5.2 [-8.0, -2.5] | 100 % (66 %) | ✔ | ✔ | ✔ | 0.0015 (0.0015) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | A | ▲ | +4.0 [+0.3, +8.1] | 95 % (0 %) | ✘ | ✘ | ✘ | 0.0772 (0.0799) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic |
| anthropic/claude-opus-5.5#low | N | ▼ | -14.8 [-20.8, -8.6] | 100 % (98 %) | ✔ | ✔ | ✔ | 0.0003 (—) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | H | ▲ | +8.2 [+4.6, +11.9] | 100 % (98 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | E | ▼ | -7.2 [-10.2, -4.3] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | A | ▼ | -2.9 [-5.2, -0.6] | 99 % (0 %) | ✘ | ✘ | ✘ | 0.0455 (0.0470) | **no publicable** | falla 3 (P2 P3 P5); cae sin google |
| deepseek-v4-flash@2026-10-17 | H | ▲ | +5.7 [+3.0, +8.8] | 100 % (80 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | C | ▲ | +7.1 [+3.3, +10.9] | 100 % (76 %) | ✔ | ✔ | ✔ | 0.0005 (0.0005) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | E | ▼ | -4.4 [-8.3, -0.6] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.0706 (0.0735) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin google, qwen |
| gemma4 | A | ▼ | -5.2 [-7.9, -2.5] | 100 % (78 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | N | ▲ | +12.1 [+4.7, +19.0] | 100 % (18 %) | ✔ | ✔ | ✔ | 0.0075 (—) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | H | ▼ | -10.3 [-15.2, -5.0] | 100 % (88 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| glm5.3-flash | O | ▲ | +3.8 [+0.7, +7.0] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.0475 (0.0487) | **no publicable** | falla 3 (P2 P3 P5); cae sin google |
| glm5.3-flash | E | ▼ | -3.9 [-6.8, -1.1] | 98 % (0 %) | ✘ | ✘ | ✔ | 0.0317 (0.0325) | **frágil** | falla P2 P3 |
| google/gemini-3.7-flash | O | ▼ | -15.8 [-20.2, -11.7] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | E | ▲ | +12.2 [+6.3, +18.0] | 100 % (92 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | A | ▲ | +13.7 [+7.3, +20.0] | 100 % (88 %) | ✔ | ✔ | ✔ | 0.0005 (0.0005) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | H | ▼ | -6.9 [-12.4, -1.3] | 100 % (0 %) | ✔ | ✘ | ✔ | 0.0384 (0.0390) | **frágil** | falla P3 |
| google/gemini-4-argon | O | ▼ | -8.3 [-11.9, -5.0] | 100 % (96 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-4-argon | N | ▼ | -16.2 [-22.6, -10.0] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0003 (—) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-4-argon | H | ▼ | -6.1 [-10.2, -1.9] | 98 % (10 %) | ✔ | ✘ | ✔ | 0.0131 (0.0133) | **frágil** | falla P3 |
| mimo-v2.6-flash | O | ▲ | +5.1 [+1.2, +9.2] | 98 % (0 %) | ✔ | ✘ | ✘ | 0.0423 (0.0440) | **frágil** | falla P3 P5; cae sin google |
| mimo-v2.6-flash | N | ▲ | +5.8 [+0.7, +11.4] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.0669 (—) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, openai |
| openai/gpt-5.6-luna | O | ▲ | +3.8 [+0.3, +7.1] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.0706 (0.0735) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin google |
| openai/gpt-5.6-luna | C | ▲ | +3.2 [+0.1, +6.7] | 93 % (0 %) | ✘ | ✘ | ✘ | 0.1135 (0.1190) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, deepseek, openai, xiaomi |
| openai/gpt-5.6-luna | A | ▼ | -3.6 [-5.9, -1.4] | 100 % (22 %) | ✘ | ✔ | ✔ | 0.0092 (0.0095) | **frágil** | falla P2 |
| openai/gpt-5.6-luna | H | ▲ | +4.3 [+1.4, +7.1] | 100 % (16 %) | ✔ | ✘ | ✘ | 0.0107 (0.0109) | **frágil** | falla P3 P5; cae sin google |
| openai/gpt-6.1-sol#low | C | ▼ | -4.7 [-7.7, -1.6] | 100 % (12 %) | ✔ | ✔ | ✔ | 0.0092 (0.0095) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-6.1-sol#low | E | ▼ | -3.7 [-7.2, -0.0] | 94 % (0 %) | ✘ | ✘ | ✘ | 0.1065 (0.1125) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, qwen, xiaomi |
| openai/gpt-6.1-sol#low | N | ▼ | -12.7 [-21.2, -3.3] | 100 % (2 %) | ✔ | ✔ | ✔ | 0.0236 (—) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-6.1-sol#low | H | ▲ | +8.0 [+4.2, +12.0] | 100 % (90 %) | ✔ | ✔ | ✔ | 0.0005 (0.0005) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.6 | N | ▲ | +17.8 [+12.6, +23.3] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0003 (—) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.6 | H | ▼ | -10.3 [-14.7, -6.2] | 100 % (98 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.8-flash | A | ▼ | -2.4 [-4.9, -0.0] | 94 % (0 %) | ✘ | ✘ | ✘ | 0.1226 (0.1278) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin google, qwen, xiaomi, z-ai |
| qwen/qwen3.8-max-0902#low | E | ▲ | +7.0 [+3.3, +10.6] | 100 % (86 %) | ✔ | ✔ | ✔ | 0.0003 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| qwen/qwen3.8-max-0902#low | N | ▼ | -7.7 [-14.3, -1.5] | 97 % (0 %) | ✘ | ✘ | ✘ | 0.0423 (—) | **no publicable** | falla 3 (P2 P3 P5); cae sin qwen |
| z-ai/glm-5.3 | O | ▲ | +4.7 [+1.5, +7.9] | 100 % (10 %) | ✔ | ✘ | ✘ | 0.0161 (0.0161) | **frágil** | falla P3 P5; cae sin google |
| z-ai/glm-5.3 | H | ▲ | +3.7 [+1.0, +6.4] | 100 % (1 %) | ✘ | ✘ | ✘ | 0.0232 (0.0230) | **no publicable** | falla 3 (P2 P3 P5); cae sin google, qwen |

## Variantes de cada marca candidata

Marca en cada variante (· = sin marca).

| modelo | rasgo | cuadro | rep0 | rep1 | AB | BA | sin anthropic | sin deepseek | sin google | sin openai | sin qwen | sin xiaomi | sin z-ai |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-haiku-5.5 | N | ▲ | ▲ | ▲ | · | ▲ | · | ▲ | · | · | ▲ | ▲ | ▲ |
| anthropic/claude-opus-5.5#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | A | ▲ | ▲ | · | ▲ | · | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| anthropic/claude-opus-5.5#low | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek-v4-flash@2026-10-17 | E | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | A | ▼ | · | ▼ | ▼ | · | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | C | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | E | ▼ | · | ▼ | ▼ | · | ▼ | ▼ | · | ▼ | · | ▼ | ▼ |
| gemma4 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| gemma4 | N | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| glm5.3-flash | O | ▲ | · | ▲ | · | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| glm5.3-flash | E | ▼ | · | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | E | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | A | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | H | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | H | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| mimo-v2.6-flash | O | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| mimo-v2.6-flash | N | ▲ | · | ▲ | ▲ | · | · | ▲ | ▲ | · | ▲ | ▲ | ▲ |
| openai/gpt-5.6-luna | O | ▲ | ▲ | · | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-5.6-luna | C | ▲ | · | · | ▲ | · | · | · | ▲ | · | ▲ | · | ▲ |
| openai/gpt-5.6-luna | A | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-5.6-luna | H | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-6.1-sol#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | E | ▼ | · | ▼ | ▼ | · | · | ▼ | ▼ | ▼ | · | · | ▼ |
| openai/gpt-6.1-sol#low | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen3.6 | N | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen3.6 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| qwen3.8-flash | A | ▼ | ▼ | · | ▼ | · | ▼ | ▼ | · | ▼ | · | · | · |
| qwen/qwen3.8-max-0902#low | E | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen/qwen3.8-max-0902#low | N | ▼ | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ |
| z-ai/glm-5.3 | O | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| z-ai/glm-5.3 | H | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | · | ▲ | ▲ |

## Puntuación con IC 95 %

| modelo | O | C | E | A | N | H |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 51 [45, 56] | 39 [35, 44] | 42 [37, 47] | 28 [24, 32] | 64 [56, 73] | 46 [41, 51] |
| anthropic/claude-opus-5.5#low | 54 [50, 59] | 33 [29, 37] | 42 [37, 46] | 38 [33, 42] | 43 [35, 52] | 51 [47, 55] |
| deepseek-v4-flash@2026-10-17 | 50 [44, 56] | 36 [31, 40] | 34 [29, 39] | 31 [28, 35] | 62 [55, 70] | 49 [44, 53] |
| gemma4 | 55 [49, 60] | 45 [40, 50] | 37 [31, 42] | 29 [25, 33] | 68 [61, 76] | 34 [27, 40] |
| glm5.3-flash | 54 [50, 59] | 39 [35, 44] | 37 [33, 41] | 34 [30, 38] | 62 [55, 70] | 45 [39, 50] |
| google/gemini-3.7-flash | 36 [31, 41] | 39 [34, 45] | 52 [47, 57] | 47 [41, 52] | 51 [44, 59] | 37 [32, 42] |
| google/gemini-4-argon | 43 [38, 48] | 37 [32, 42] | 38 [33, 42] | 35 [31, 39] | 42 [34, 50] | 38 [32, 43] |
| mimo-v2.6-flash | 56 [50, 61] | 40 [35, 45] | 43 [38, 47] | 36 [32, 40] | 62 [57, 68] | 42 [36, 46] |
| openai/gpt-5.6-luna | 54 [49, 59] | 41 [36, 46] | 38 [33, 43] | 31 [27, 34] | 59 [54, 64] | 47 [43, 52] |
| openai/gpt-6.1-sol#low | 52 [47, 57] | 34 [30, 38] | 37 [33, 42] | 33 [28, 37] | 45 [37, 53] | 51 [46, 55] |
| qwen3.6 | 54 [48, 59] | 42 [37, 47] | 42 [37, 47] | 35 [31, 40] | 74 [68, 80] | 34 [28, 39] |
| qwen3.8-flash | 48 [42, 54] | 36 [31, 42] | 40 [35, 44] | 32 [28, 36] | 62 [57, 67] | 44 [39, 48] |
| qwen/qwen3.8-max-0902#low | 49 [44, 54] | 36 [32, 41] | 47 [42, 53] | 33 [29, 37] | 50 [44, 56] | 44 [39, 48] |
| z-ai/glm-5.3 | 55 [50, 60] | 38 [33, 42] | 42 [37, 47] | 34 [30, 38] | 54 [48, 60] | 47 [43, 51] |
