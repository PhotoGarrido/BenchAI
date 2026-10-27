# Cuadro público de personalidad · conducta comparada (PERSONALIDAD.md §28)

Generado por `cuadro_publico_v3.py`. Selección: personalidad_v3_seleccion.json. 22 modelos, 9 laboratorios (anthropic, deepseek, google, minimax, mistralai, openai, qwen, xiaomi, z-ai); situaciones por rasgo: O 59, C 56, E 57, A 57, N 72, H 48. Semilla 20261010. Sin llamadas a modelos. Escala de Honestidad-Humildad: I1-H en binario: 48 situaciones calibradas por dificultad, 12 por faceta (PERSONALIDAD.md §36-37). Escala de Neuroticismo: I1-N en binario, 72, sin seleccionar (PERSONALIDAD.md §39-40).
Fuera por cobertura (§41.1: O, C, E y A del v3, completos o en forma corta; H y N de I1): deepseek-v4-flash (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %), mistralai/mistral-large-4-0 (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %), x-ai/grok-4.5 (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %). **Fuera de la norma por validez (§41.2, perfil no interpretable):** deepseek/deepseek-v4-pro-0813 (coherencia de la deseabilidad 0,64 (no interpretable)). **Pendientes de completar (§45.2, solo forma corta; no se publican):** moonshotai/kimi-k3 (forma corta en O, C, E, A, N, H).

**Puntuación** = 50 + 50·media(elige el polo alto − deseabilidad media del panel): 50 = elige lo que el conjunto de modelos juzga admirable. **▲/▼** = elige el polo alto más/menos a menudo que los demás modelos en las mismas situaciones (comparación pareada, IC 95 %), solo si la marca es **robusta** (P1–P3, P5, P6). Neuroticismo con marca desde §40 (sus marcas pasan además R4 de §30.2).

| modelo | ISS | Apertura | Responsabilidad | Extraversión | Amabilidad | Neuroticismo | Honestidad-Humildad |
|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4.5 | 13.6 | 49 | 44 | 44 | 34 | 57 ▲ | 45 |
| anthropic/claude-haiku-5.5 | 10.3 | 50 | 38 | 43 | 28 ▼ | 54 | 46 |
| anthropic/claude-opus-5.5#low | 12.5 | 54 | 32 ▼ | 43 | 38 | 49 ▼ | 51 ▲ |
| deepseek-v4-flash@2026-10-17 | 21.1 | 49 | 35 | 35 ▼ | 31 | 53 | 49 ▲ |
| deepseek/deepseek-v3.2 ⚠ | 37.4 | 52 | 45 | 44 | 35 | 56 | 33 |
| deepseek/deepseek-v4-flash | 39.5 | 53 | 39 | 46 | 30 | 55 | 37 |
| deepseek/deepseek-v4-flash-0731 | 40.2 | 47 ▼ | 38 | 41 | 31 | 50 ▼ | 44 |
| gemma4 | 28.1 | 54 | 44 | 38 | 29 ▼ | 56 | 34 ▼ |
| glm5.3-flash | 28.9 | 54 | 38 | 38 | 34 | 53 | 45 |
| google/gemini-3.1-flash-lite | 34.9 | 60 ▲ | 40 | 46 | 35 | 53 | 35 |
| google/gemini-3.7-flash | 55.2 | 36 ▼ | 38 | 53 ▲ | 47 ▲ | 52 | 37 |
| google/gemini-4-argon | — | 43 ▼ | 36 | 39 | 34 | 48 ▼ | 38 |
| mimo-v2.6-flash | 12.6 | 55 | 39 | 44 | 36 | 53 | 42 |
| minimax/minimax-m3.1-flash#low ⚠ | 7.9 | 51 | 43 | 42 | 34 | 55 | 43 |
| mistralai/mistral-medium-3-5 ⚠ | 23.9 | 59 ▲ | 42 | 45 | 31 | 56 | 34 |
| openai/gpt-5.6-luna | 7.6 | 54 | 40 | 39 | 31 | 53 | 47 |
| openai/gpt-6-luna#low | 13.9 | 52 | 35 | 37 | 33 | 52 | 48 |
| openai/gpt-6.1-sol#low | 13.2 | 51 | 33 ▼ | 38 | 33 | 49 ▼ | 51 ▲ |
| qwen3.6 | 23.2 | 53 | 41 | 43 | 35 | 56 | 34 ▼ |
| qwen3.8-flash | 24.8 | 48 | 36 | 41 | 32 | 53 | 44 |
| qwen/qwen3.8-max-0902#low | — | 49 | 35 | 48 ▲ | 33 | 49 ▼ | 44 |
| z-ai/glm-5.3 | — | 55 | 37 | 43 | 34 | 51 | 47 |

Neuroticismo: I1-N en binario (72, sin seleccionar; ansiedad 12, hostilidad 12, depresion 12, autoconciencia 12, impulsividad 12, vulnerabilidad 12). Pasó §39 (§40). Marcas con las cinco comprobaciones de §28.

⚠ Interpretar con cautela: algún índice de validez en la zona de aviso (§41.2; ver «Validez por modelo»).

## Validez con la definición de §28 (G3 y G4 de §21)

Mismos cálculos que `analizar_v3.py` (G3: r media entre facetas del mismo rasgo frente a facetas de otros rasgos; G4: Spearman-Brown de mitades pares/impares entre modelos), pero sobre la puntuación de §28 en vez de la ajustada por la deseabilidad propia. G4 (b): mediana de Spearman-Brown en 200 particiones al azar equilibradas por faceta. Revalidación automática (§41.3): un rasgo con marca que no pasa G4 (a), G4 (b) ≥ 0,70 y G3 pierde sus marcas.

| rasgo | G3 dentro / fuera | G3 | G4 (a) | G4 (b) | listón §41.3 | en §28 |
|---|---|---|---|---|---|---|
| Apertura | +0.44 / -0.04 | ✔ | 0.89 | 0,89 | ✔ | con marca |
| Responsabilidad | +0.21 / +0.04 | ✔ | 0.84 | 0,82 | ✔ | con marca |
| Extraversión | +0.22 / +0.03 | ✔ | 0.92 | 0,86 | ✔ | con marca |
| Amabilidad | +0.38 / -0.01 | ✔ | 0.77 | 0,86 | ✔ | con marca |
| Neuroticismo | +0.21 / +0.05 | ✔ | 0.79 | 0,83 | ✔ | con marca |
| Honestidad-Humildad | +0.46 / -0.15 | ✔ | 0.93 | 0,91 | ✔ | con marca |

Revalidación automática (§41.3): todos los rasgos con marca pasan el listón.

## Validez por modelo (§41.2)

Índices calculados sobre todas las respuestas del modelo en los instrumentos del cuadro (R3 del v3 en O, C, E y A; binario de I1-H e I1-N; deseabilidad). Umbrales fijados antes de calcular: posición (Δ AB−BA) aviso/no interpretable a partir de 0,20/0,30; posición (fracción de A) aviso/no interpretable a partir de |A − 0,5| = 0,10/|A − 0,5| = 0,15; no válidas aviso/no interpretable a partir de 5,0 %/10,0 %; retest aviso/no interpretable a partir de 0,60/0,40; coherencia de la deseabilidad aviso/no interpretable a partir de 0,75/0,65. Un perfil **no interpretable** sale de la norma: no entra en la media de los demás, ni en d̄, ni en la selección de N, ni en BH, y no lleva puntuaciones, marcas ni retrato.

| modelo | Δ AB−BA | fracción de A | no válidas | retest | coherencia deseabilidad | nivel |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4.5 | -0,18 | 0,41 | 0,6 % | 0,97 | 0,86 | **válido** |
| anthropic/claude-haiku-5.5 | -0,04 | 0,48 | 0,0 % | 0,93 | 0,90 | **válido** |
| anthropic/claude-opus-5.5#low | -0,05 | 0,47 | 0,0 % | 0,96 | 0,92 | **válido** |
| deepseek-v4-flash@2026-10-17 | -0,09 | 0,45 | 0,0 % | 0,95 | 0,80 | **válido** |
| deepseek/deepseek-v3.2 | -0,25 ⚠ | 0,37 ⚠ | 0,0 % | 0,77 | 0,76 | **aviso** |
| deepseek/deepseek-v4-flash | -0,10 | 0,45 | 0,6 % | 0,81 | 0,86 | **válido** |
| deepseek/deepseek-v4-flash-0731 | -0,06 | 0,47 | 0,0 % | 0,87 | 0,86 | **válido** |
| deepseek/deepseek-v4-pro-0813 | -0,30 ⚠ | 0,35 ⚠ | 0,0 % | 0,80 | 0,64 ✘ | **no interpretable** |
| gemma4 | -0,09 | 0,46 | 0,1 % | 0,95 | 0,83 | **válido** |
| glm5.3-flash | -0,10 | 0,45 | 0,0 % | 0,87 | 0,83 | **válido** |
| google/gemini-3.1-flash-lite | -0,03 | 0,48 | 0,0 % | 0,96 | 0,88 | **válido** |
| google/gemini-3.7-flash | -0,06 | 0,47 | 0,0 % | 0,90 | 0,90 | **válido** |
| google/gemini-4-argon | -0,09 | 0,46 | 1,5 % | 0,89 | 0,92 | **válido** |
| mimo-v2.6-flash | 0,00 | 0,50 | 0,0 % | 0,86 | 0,75 | **válido** |
| minimax/minimax-m3.1-flash#low | -0,09 | 0,45 | 0,0 % | 0,75 | 0,73 ⚠ | **aviso** |
| mistralai/mistral-medium-3-5 | -0,21 ⚠ | 0,40 ⚠ | 0,0 % | 0,84 | 0,85 | **aviso** |
| openai/gpt-5.6-luna | 0,02 | 0,51 | 0,0 % | 0,91 | 0,82 | **válido** |
| openai/gpt-6-luna#low | 0,04 | 0,52 | 0,0 % | 0,90 | 0,83 | **válido** |
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

- **anthropic/claude-haiku-4.5**: **más Neuroticismo** (reacciona, se preocupa). Tendencias frágiles, no publicadas: C▲.
- **anthropic/claude-haiku-5.5**: **menos Amabilidad** (pone límites y se defiende).
- **anthropic/claude-opus-5.5#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas); **menos Neuroticismo** (se mantiene sereno).
- **deepseek-v4-flash@2026-10-17**: **menos Extraversión** (prefiere calma y segundo plano); **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **deepseek/deepseek-v3.2 ⚠**: *interpretar con cautela (posición (Δ AB−BA) 0,25 (aviso); posición (fracción de A) |A − 0,5| = 0,13 (aviso))*: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: C▲, H▼.
- **deepseek/deepseek-v4-flash**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: E▲, A▼, N▲, H▼.
- **deepseek/deepseek-v4-flash-0731**: **menos Apertura** (prefiere lo conocido); **menos Neuroticismo** (se mantiene sereno).
- **gemma4**: **menos Amabilidad** (pone límites y se defiende); **menos Honestidad-Humildad** (acepta ventajas y se promociona). Tendencias frágiles, no publicadas: C▲, E▼, N▲.
- **glm5.3-flash**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: E▼.
- **google/gemini-3.1-flash-lite**: **más Apertura** (curioso, busca lo nuevo). Tendencias frágiles, no publicadas: H▼.
- **google/gemini-3.7-flash**: **menos Apertura** (prefiere lo conocido); **más Extraversión** (busca gente y protagonismo); **más Amabilidad** (cede y coopera).
- **google/gemini-4-argon**: **menos Apertura** (prefiere lo conocido); **menos Neuroticismo** (se mantiene sereno).
- **mimo-v2.6-flash**: perfil próximo al de los demás modelos.
- **minimax/minimax-m3.1-flash#low ⚠**: *interpretar con cautela (coherencia de la deseabilidad 0,73 (aviso))*: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: C▲, N▲.
- **mistralai/mistral-medium-3-5 ⚠**: *interpretar con cautela (posición (Δ AB−BA) 0,21 (aviso); posición (fracción de A) |A − 0,5| = 0,10 (aviso))*: **más Apertura** (curioso, busca lo nuevo). Tendencias frágiles, no publicadas: N▲, H▼.
- **openai/gpt-5.6-luna**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: A▼, H▲.
- **openai/gpt-6-luna#low**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: E▼, H▲.
- **openai/gpt-6.1-sol#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas); **menos Neuroticismo** (se mantiene sereno). Tendencias frágiles, no publicadas: E▼.
- **qwen3.6**: **menos Honestidad-Humildad** (acepta ventajas y se promociona). Tendencias frágiles, no publicadas: N▲.
- **qwen3.8-flash**: perfil próximo al de los demás modelos.
- **qwen/qwen3.8-max-0902#low**: **más Extraversión** (busca gente y protagonismo); **menos Neuroticismo** (se mantiene sereno). Tendencias frágiles, no publicadas: C▼.
- **z-ai/glm-5.3**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: N▼, H▲.

## Marcas candidatas y su nivel

**65 marcas candidatas** (IC de la comparación que excluye 0): 24 robustas · 25 frágiles · 16 no publicables.

P1 = signo replicado en las dos mitades (≥ 90 %) · P2 = réplica 0 y 1 · P3 = orden AB y BA · P5 = todos los paneles sin un laboratorio · P6 = BH q < 0,05 sobre 132 pruebas (entre paréntesis, sin N).

| modelo | rasgo | marca | dif [IC] | P1 signo (sig. ambas) | P2 | P3 | P5 | P6 q (sin N) | nivel | por qué |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4.5 | C | ▲ | +6.0 [+2.5, +9.5] | 100 % (70 %) | ✔ | ✘ | ✔ | 0.0026 (0.0027) | **frágil** | falla P3 |
| anthropic/claude-haiku-4.5 | N | ▲ | +3.9 [+1.6, +6.5] | 100 % (48 %) | ✔ | ✔ | ✔ | 0.0019 (—) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-haiku-4.5 | H | ▲ | +3.0 [+0.1, +5.7] | 97 % (0 %) | ✘ | ✘ | ✘ | 0.0852 (0.0911) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin deepseek, google, mistralai, qwen, xiaomi |
| anthropic/claude-haiku-5.5 | A | ▼ | -5.9 [-9.5, -2.1] | 100 % (36 %) | ✔ | ✔ | ✔ | 0.0053 (0.0055) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-haiku-5.5 | H | ▲ | +4.1 [+0.2, +7.9] | 98 % (0 %) | ✔ | ✘ | ✘ | 0.0852 (0.0911) | **no publicable** | falla 3 (P3 P5 P6); cae sin deepseek, google, mistralai, qwen |
| anthropic/claude-opus-5.5#low | C | ▼ | -6.4 [-9.2, -3.7] | 100 % (95 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | A | ▲ | +4.2 [+0.5, +7.9] | 98 % (0 %) | ✘ | ✘ | ✔ | 0.0564 (0.0622) | **no publicable** | falla 3 (P2 P3 P6) |
| anthropic/claude-opus-5.5#low | N | ▼ | -4.1 [-6.8, -1.6] | 100 % (32 %) | ✔ | ✔ | ✔ | 0.0053 (—) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | H | ▲ | +9.3 [+6.0, +12.9] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | C | ▼ | -4.0 [-7.3, -0.6] | 98 % (0 %) | ✘ | ✘ | ✔ | 0.0511 (0.0556) | **no publicable** | falla 3 (P2 P3 P6) |
| deepseek-v4-flash@2026-10-17 | E | ▼ | -7.5 [-10.4, -4.8] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | A | ▼ | -2.5 [-4.5, -0.2] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.0721 (0.0783) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin google |
| deepseek-v4-flash@2026-10-17 | H | ▲ | +6.8 [+4.0, +9.7] | 100 % (98 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek/deepseek-v3.2 | C | ▲ | +6.3 [+2.7, +9.8] | 100 % (56 %) | ✔ | ✘ | ✔ | 0.0034 (0.0035) | **frágil** | falla P3 |
| deepseek/deepseek-v3.2 | N | ▲ | +2.8 [+0.3, +5.3] | 98 % (0 %) | ✘ | ✘ | ✔ | 0.0520 (—) | **no publicable** | falla 3 (P2 P3 P6) |
| deepseek/deepseek-v3.2 | H | ▼ | -9.3 [-13.3, -5.0] | 100 % (94 %) | ✔ | ✘ | ✔ | 0.0005 (0.0004) | **frágil** | falla P3 |
| deepseek/deepseek-v4-flash | E | ▲ | +3.5 [+0.9, +6.1] | 100 % (0 %) | ✘ | ✘ | ✔ | 0.0304 (0.0298) | **frágil** | falla P2 P3 |
| deepseek/deepseek-v4-flash | A | ▼ | -3.4 [-5.4, -1.0] | 100 % (2 %) | ✔ | ✘ | ✔ | 0.0229 (0.0227) | **frágil** | falla P3 |
| deepseek/deepseek-v4-flash | N | ▲ | +1.7 [+0.3, +3.2] | 97 % (0 %) | ✘ | ✘ | ✔ | 0.0387 (—) | **frágil** | falla P2 P3 |
| deepseek/deepseek-v4-flash | H | ▼ | -5.2 [-9.2, -1.2] | 100 % (0 %) | ✔ | ✘ | ✔ | 0.0281 (0.0277) | **frágil** | falla P3 |
| deepseek/deepseek-v4-flash-0731 | O | ▼ | -4.8 [-7.8, -1.6] | 100 % (36 %) | ✔ | ✔ | ✔ | 0.0038 (0.0038) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek/deepseek-v4-flash-0731 | N | ▼ | -2.7 [-4.1, -1.3] | 100 % (68 %) | ✔ | ✔ | ✔ | 0.0008 (—) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | C | ▲ | +5.6 [+1.9, +9.3] | 100 % (18 %) | ✔ | ✘ | ✔ | 0.0083 (0.0085) | **frágil** | falla P3 |
| gemma4 | E | ▼ | -4.8 [-8.5, -1.1] | 100 % (0 %) | ✘ | ✘ | ✔ | 0.0356 (0.0365) | **frágil** | falla P2 P3 |
| gemma4 | A | ▼ | -4.8 [-7.5, -2.3] | 100 % (74 %) | ✔ | ✔ | ✔ | 0.0008 (0.0007) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | N | ▲ | +2.8 [+0.3, +5.3] | 99 % (0 %) | ✘ | ✔ | ✔ | 0.0564 (—) | **frágil** | falla P2 P6 |
| gemma4 | H | ▼ | -8.8 [-13.7, -3.9] | 100 % (68 %) | ✔ | ✔ | ✔ | 0.0008 (0.0007) | **robusta** | pasa P1–P3, P5, P6 |
| glm5.3-flash | E | ▼ | -4.3 [-7.3, -1.3] | 100 % (7 %) | ✘ | ✔ | ✔ | 0.0189 (0.0190) | **frágil** | falla P2 |
| google/gemini-3.1-flash-lite | O | ▲ | +9.6 [+5.9, +13.3] | 100 % (99 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.1-flash-lite | E | ▲ | +4.0 [+0.2, +7.7] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.0991 (0.1041) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin deepseek, google, openai, z-ai |
| google/gemini-3.1-flash-lite | H | ▼ | -7.4 [-12.9, -2.5] | 100 % (18 %) | ✔ | ✘ | ✔ | 0.0124 (0.0126) | **frágil** | falla P3 |
| google/gemini-3.7-flash | O | ▼ | -16.4 [-20.6, -12.2] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | E | ▲ | +11.3 [+5.9, +16.7] | 100 % (86 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | A | ▲ | +13.6 [+7.5, +19.5] | 100 % (89 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | H | ▼ | -5.5 [-10.8, -0.1] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.0933 (0.0983) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, openai, z-ai |
| google/gemini-4-argon | O | ▼ | -9.0 [-12.4, -5.6] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-4-argon | C | ▼ | -3.0 [-5.8, -0.1] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.0913 (0.0971) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin google, minimax, mistralai |
| google/gemini-4-argon | N | ▼ | -4.9 [-7.6, -2.3] | 100 % (52 %) | ✔ | ✔ | ✔ | 0.0026 (—) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-4-argon | H | ▼ | -4.7 [-9.0, -0.2] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.0706 (0.0775) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, openai |
| mimo-v2.6-flash | O | ▲ | +4.0 [+0.0, +7.8] | 94 % (0 %) | ✘ | ✘ | ✘ | 0.1023 (0.1068) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, deepseek, google, minimax, qwen |
| minimax/minimax-m3.1-flash#low | C | ▲ | +4.9 [+1.4, +8.6] | 100 % (3 %) | ✘ | ✔ | ✔ | 0.0213 (0.0213) | **frágil** | falla P2 |
| minimax/minimax-m3.1-flash#low | N | ▲ | +2.6 [+0.5, +4.7] | 99 % (0 %) | ✘ | ✘ | ✔ | 0.0378 (—) | **frágil** | falla P2 P3 |
| mistralai/mistral-medium-3-5 | O | ▲ | +8.0 [+4.6, +11.5] | 100 % (96 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| mistralai/mistral-medium-3-5 | C | ▲ | +3.9 [+0.5, +7.6] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.0673 (0.0747) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin qwen |
| mistralai/mistral-medium-3-5 | E | ▲ | +2.6 [+0.1, +5.4] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.1076 (0.1117) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin deepseek, minimax, mistralai, openai, z-ai |
| mistralai/mistral-medium-3-5 | N | ▲ | +3.1 [+0.7, +5.7] | 100 % (0 %) | ✔ | ✘ | ✔ | 0.0343 (—) | **frágil** | falla P3 |
| mistralai/mistral-medium-3-5 | H | ▼ | -8.2 [-12.5, -4.2] | 100 % (88 %) | ✔ | ✘ | ✔ | 0.0005 (0.0004) | **frágil** | falla P3 |
| openai/gpt-5.6-luna | A | ▼ | -3.2 [-5.4, -0.9] | 100 % (2 %) | ✘ | ✘ | ✔ | 0.0218 (0.0216) | **frágil** | falla P2 P3 |
| openai/gpt-5.6-luna | H | ▲ | +5.4 [+2.8, +8.3] | 100 % (62 %) | ✔ | ✘ | ✔ | 0.0014 (0.0013) | **frágil** | falla P3 |
| openai/gpt-6-luna#low | C | ▼ | -3.6 [-6.9, -0.3] | 97 % (0 %) | ✘ | ✘ | ✘ | 0.0933 (0.0983) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin minimax |
| openai/gpt-6-luna#low | E | ▼ | -5.5 [-9.0, -2.0] | 100 % (7 %) | ✔ | ✘ | ✔ | 0.0124 (0.0126) | **frágil** | falla P3 |
| openai/gpt-6-luna#low | H | ▲ | +6.5 [+2.4, +10.4] | 100 % (29 %) | ✔ | ✘ | ✔ | 0.0068 (0.0070) | **frágil** | falla P3 |
| openai/gpt-6.1-sol#low | C | ▼ | -5.9 [-9.1, -2.8] | 100 % (55 %) | ✔ | ✔ | ✔ | 0.0023 (0.0023) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-6.1-sol#low | E | ▼ | -4.1 [-7.6, -0.6] | 100 % (0 %) | ✔ | ✘ | ✔ | 0.0680 (0.0751) | **frágil** | falla P3 P6 |
| openai/gpt-6.1-sol#low | N | ▼ | -3.6 [-6.3, -0.9] | 98 % (0 %) | ✔ | ✔ | ✔ | 0.0341 (—) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-6.1-sol#low | H | ▲ | +9.0 [+5.4, +12.7] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.6 | N | ▲ | +3.1 [+0.6, +5.9] | 98 % (0 %) | ✔ | ✘ | ✔ | 0.0456 (—) | **frágil** | falla P3 |
| qwen3.6 | H | ▼ | -8.8 [-13.1, -4.8] | 100 % (87 %) | ✔ | ✔ | ✔ | 0.0014 (0.0013) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.8-flash | O | ▼ | -3.7 [-7.5, -0.4] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.0852 (0.0911) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin mistralai, z-ai |
| qwen/qwen3.8-max-0902#low | C | ▼ | -3.3 [-6.0, -0.4] | 100 % (0 %) | ✔ | ✘ | ✔ | 0.0520 (0.0574) | **frágil** | falla P3 P6 |
| qwen/qwen3.8-max-0902#low | E | ▲ | +6.3 [+2.7, +9.9] | 100 % (69 %) | ✔ | ✔ | ✔ | 0.0019 (0.0018) | **robusta** | pasa P1–P3, P5, P6 |
| qwen/qwen3.8-max-0902#low | N | ▼ | -3.8 [-5.9, -1.9] | 100 % (90 %) | ✔ | ✔ | ✔ | 0.0005 (—) | **robusta** | pasa P1–P3, P5, P6 |
| z-ai/glm-5.3 | O | ▲ | +3.6 [+0.3, +6.8] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.0720 (0.0783) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin google, qwen |
| z-ai/glm-5.3 | N | ▼ | -2.3 [-3.7, -1.0] | 100 % (56 %) | ✘ | ✘ | ✔ | 0.0023 (—) | **frágil** | falla P2 P3 |
| z-ai/glm-5.3 | H | ▲ | +4.9 [+2.2, +7.5] | 100 % (55 %) | ✔ | ✘ | ✔ | 0.0030 (0.0031) | **frágil** | falla P3 |

## Variantes de cada marca candidata

Marca en cada variante (· = sin marca).

| modelo | rasgo | cuadro | rep0 | rep1 | AB | BA | sin anthropic | sin deepseek | sin google | sin minimax | sin mistralai | sin openai | sin qwen | sin xiaomi | sin z-ai |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4.5 | C | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| anthropic/claude-haiku-4.5 | N | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| anthropic/claude-haiku-4.5 | H | ▲ | ▲ | · | · | ▲ | ▲ | · | · | ▲ | · | ▲ | · | · | ▲ |
| anthropic/claude-haiku-5.5 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-haiku-5.5 | H | ▲ | ▲ | ▲ | ▲ | · | ▲ | · | · | ▲ | · | ▲ | · | ▲ | ▲ |
| anthropic/claude-opus-5.5#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | A | ▲ | ▲ | · | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| anthropic/claude-opus-5.5#low | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek-v4-flash@2026-10-17 | C | ▼ | ▼ | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | E | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | A | ▼ | · | ▼ | ▼ | · | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v3.2 | C | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v3.2 | N | ▲ | · | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v3.2 | H | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek/deepseek-v4-flash | E | ▲ | ▲ | · | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v4-flash | A | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek/deepseek-v4-flash | N | ▲ | ▲ | · | · | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v4-flash | H | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek/deepseek-v4-flash-0731 | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek/deepseek-v4-flash-0731 | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| gemma4 | C | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | E | ▼ | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| gemma4 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| gemma4 | N | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| glm5.3-flash | E | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.1-flash-lite | O | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.1-flash-lite | E | ▲ | · | ▲ | ▲ | · | ▲ | · | · | ▲ | ▲ | · | ▲ | ▲ | · |
| google/gemini-3.1-flash-lite | H | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | E | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | A | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | H | ▼ | ▼ | · | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | · |
| google/gemini-4-argon | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | C | ▼ | ▼ | · | ▼ | · | ▼ | ▼ | · | · | · | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | H | ▼ | ▼ | · | ▼ | · | · | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ |
| mimo-v2.6-flash | O | ▲ | · | ▲ | ▲ | · | · | · | · | · | ▲ | ▲ | · | ▲ | ▲ |
| minimax/minimax-m3.1-flash#low | C | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| minimax/minimax-m3.1-flash#low | N | ▲ | · | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| mistralai/mistral-medium-3-5 | O | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| mistralai/mistral-medium-3-5 | C | ▲ | ▲ | · | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ |
| mistralai/mistral-medium-3-5 | E | ▲ | · | ▲ | · | ▲ | ▲ | · | ▲ | · | · | · | ▲ | ▲ | · |
| mistralai/mistral-medium-3-5 | N | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| mistralai/mistral-medium-3-5 | H | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-5.6-luna | A | ▼ | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-5.6-luna | H | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-6-luna#low | C | ▼ | ▼ | · | · | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6-luna#low | E | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6-luna#low | H | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-6.1-sol#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | E | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen3.6 | N | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen3.6 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| qwen3.8-flash | O | ▼ | ▼ | · | · | ▼ | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | · |
| qwen/qwen3.8-max-0902#low | C | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| qwen/qwen3.8-max-0902#low | E | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen/qwen3.8-max-0902#low | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| z-ai/glm-5.3 | O | ▲ | ▲ | · | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | · | ▲ | ▲ |
| z-ai/glm-5.3 | N | ▼ | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| z-ai/glm-5.3 | H | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |

## Puntuación con IC 95 %

| modelo | O | C | E | A | N | H |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4.5 | 49 [44, 54] | 44 [39, 50] | 44 [39, 49] | 34 [30, 38] | 57 [54, 60] | 45 [40, 49] |
| anthropic/claude-haiku-5.5 | 50 [45, 56] | 38 [34, 43] | 43 [38, 48] | 28 [24, 32] | 54 [51, 57] | 46 [41, 51] |
| anthropic/claude-opus-5.5#low | 54 [50, 58] | 32 [28, 37] | 43 [39, 47] | 38 [33, 42] | 49 [46, 51] | 51 [46, 55] |
| deepseek-v4-flash@2026-10-17 | 49 [43, 55] | 35 [30, 40] | 35 [31, 40] | 31 [27, 35] | 53 [50, 56] | 49 [44, 53] |
| deepseek/deepseek-v3.2 | 52 [47, 57] | 45 [39, 50] | 44 [41, 48] | 35 [31, 39] | 56 [53, 59] | 33 [28, 38] |
| deepseek/deepseek-v4-flash | 53 [48, 58] | 39 [35, 43] | 46 [41, 50] | 30 [27, 34] | 55 [52, 57] | 37 [32, 43] |
| deepseek/deepseek-v4-flash-0731 | 47 [42, 52] | 38 [33, 42] | 41 [37, 46] | 31 [27, 35] | 50 [49, 52] | 44 [39, 50] |
| gemma4 | 54 [49, 59] | 44 [39, 49] | 38 [33, 43] | 29 [25, 33] | 56 [53, 59] | 34 [28, 40] |
| glm5.3-flash | 54 [49, 58] | 38 [34, 43] | 38 [34, 42] | 34 [30, 38] | 53 [51, 56] | 45 [40, 50] |
| google/gemini-3.1-flash-lite | 60 [55, 66] | 40 [34, 46] | 46 [41, 51] | 35 [31, 39] | 53 [50, 56] | 35 [29, 41] |
| google/gemini-3.7-flash | 36 [31, 41] | 38 [32, 44] | 53 [48, 58] | 47 [41, 52] | 52 [49, 56] | 37 [32, 42] |
| google/gemini-4-argon | 43 [38, 48] | 36 [31, 41] | 39 [34, 44] | 34 [30, 39] | 48 [45, 51] | 38 [32, 43] |
| mimo-v2.6-flash | 55 [50, 60] | 39 [35, 44] | 44 [39, 48] | 36 [32, 40] | 53 [51, 55] | 42 [37, 46] |
| minimax/minimax-m3.1-flash#low | 51 [45, 56] | 43 [38, 48] | 42 [37, 46] | 34 [31, 38] | 55 [53, 58] | 43 [39, 47] |
| mistralai/mistral-medium-3-5 | 59 [54, 64] | 42 [37, 48] | 45 [41, 49] | 31 [28, 35] | 56 [53, 59] | 34 [29, 40] |
| openai/gpt-5.6-luna | 54 [49, 59] | 40 [36, 45] | 39 [34, 44] | 31 [27, 34] | 53 [50, 55] | 47 [42, 52] |
| openai/gpt-6-luna#low | 52 [46, 57] | 35 [31, 39] | 37 [33, 41] | 33 [29, 37] | 52 [50, 55] | 48 [43, 54] |
| openai/gpt-6.1-sol#low | 51 [46, 56] | 33 [29, 37] | 38 [34, 43] | 33 [28, 37] | 49 [47, 52] | 51 [46, 55] |
| qwen3.6 | 53 [48, 59] | 41 [35, 46] | 43 [38, 48] | 35 [31, 39] | 56 [52, 59] | 34 [29, 38] |
| qwen3.8-flash | 48 [42, 54] | 36 [30, 41] | 41 [37, 45] | 32 [28, 35] | 53 [51, 56] | 44 [39, 48] |
| qwen/qwen3.8-max-0902#low | 49 [44, 54] | 35 [31, 40] | 48 [43, 53] | 33 [29, 37] | 49 [47, 51] | 44 [39, 48] |
| z-ai/glm-5.3 | 55 [50, 59] | 37 [32, 41] | 43 [38, 48] | 34 [30, 38] | 51 [49, 53] | 47 [43, 51] |
