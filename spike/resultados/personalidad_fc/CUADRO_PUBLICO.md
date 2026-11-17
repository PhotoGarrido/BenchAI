# Cuadro público de personalidad · conducta comparada (PERSONALIDAD.md §28)

Generado por `cuadro_publico_v3.py`. Selección: personalidad_v3_seleccion.json. 26 modelos, 11 laboratorios (anthropic, deepseek, google, minimax, mistralai, moonshotai, openai, qwen, tencent, xiaomi, z-ai); situaciones por rasgo: O 59, C 56, E 57, A 57, N 72, H 48. Semilla 20261010. Sin llamadas a modelos. Escala de Honestidad-Humildad: I1-H en binario: 48 situaciones calibradas por dificultad, 12 por faceta (PERSONALIDAD.md §36-37). Escala de Neuroticismo: I1-N en binario, 72, sin seleccionar (PERSONALIDAD.md §39-40).
Fuera por cobertura (§41.1: O, C, E y A del v3, completos o en forma corta; H y N de I1): deepseek-v4-flash (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %), mistralai/mistral-large-4-0 (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %), x-ai/grok-4.5 (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %). **Fuera de la norma por validez (§41.2, perfil no interpretable):** deepseek/deepseek-v4-pro-0813 (coherencia de la deseabilidad 0,64 (no interpretable)). **Pendientes de completar (§45.2, solo forma corta; no se publican):** moonshotai/kimi-k3 (forma corta en O, C, E, A, N, H). **Réplicas entre proveedores (mismo modelo que otra medición ya hecha; no son una fila más, ver PROVEEDORES_DEEPSEEK_V4_PRO.md):** deepseek-v4-pro (= deepseek/deepseek-v4-pro-0813).

**Puntuación** = 50 + 50·media(elige el polo alto − deseabilidad media del panel): 50 = elige lo que el conjunto de modelos juzga admirable. **▲/▼** = elige el polo alto más/menos a menudo que los demás modelos en las mismas situaciones (comparación pareada, IC 95 %), solo si la marca es **robusta** (P1–P3, P5, P6). Neuroticismo con marca desde §40 (sus marcas pasan además R4 de §30.2).

| modelo | ISS | Apertura | Responsabilidad | Extraversión | Amabilidad | Neuroticismo | Honestidad-Humildad |
|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4.5 | 13.6 | 49 | 45 | 44 | 34 | 57 ▲ | 45 |
| anthropic/claude-haiku-5.5 | 10.3 | 50 | 39 | 43 | 28 ▼ | 54 | 46 |
| anthropic/claude-opus-5.5#low | 12.5 | 54 | 33 ▼ | 43 | 37 | 49 ▼ | 51 ▲ |
| deepseek-v4-flash@2026-10-17 | 21.1 | 49 | 35 | 35 ▼ | 31 | 53 | 48 ▲ |
| deepseek/deepseek-v3.2 ⚠ | 37.4 | 52 | 45 | 44 | 35 | 56 | 33 |
| deepseek/deepseek-v4-flash | 39.5 | 53 | 39 | 46 | 30 | 54 | 37 ▼ |
| deepseek/deepseek-v4-flash-0731 | 40.2 | 47 ▼ | 38 | 41 | 31 | 50 ▼ | 44 |
| gemma4 | 28.1 | 54 | 44 ▲ | 38 | 29 ▼ | 56 ▲ | 33 ▼ |
| glm5.3-flash | 28.9 | 54 | 39 | 38 | 34 | 53 | 45 |
| google/gemini-3.1-flash-lite | 34.9 | 60 ▲ | 41 | 46 | 34 | 53 | 35 ▼ |
| google/gemini-3.7-flash | 55.2 | 36 ▼ | 38 | 53 ▲ | 46 ▲ | 52 | 37 |
| google/gemini-4-argon | — | 43 ▼ | 36 | 39 | 34 | 48 ▼ | 37 ▼ |
| hy4 | 25.4 | 56 | 36 | 38 | 34 | 53 | 50 ▲ |
| hy4-flash | 16.8 | 56 | 36 | 41 | 32 | 52 | 46 |
| kimi-k3.1-pro ⚠ | 11.9 | 54 | 39 | 43 | 34 | 53 | 48 ▲ |
| mimo-v2.6-flash | 12.6 | 55 | 39 | 44 | 36 | 53 | 41 |
| minimax/minimax-m3.1-flash#low ⚠ | 7.9 | 51 | 44 | 42 | 34 | 55 | 43 |
| mistralai/mistral-medium-3-5 ⚠ | 23.9 | 59 | 43 | 45 | 31 | 56 | 34 ▼ |
| openai/gpt-5.6-luna | 7.6 | 54 | 41 | 39 | 30 | 53 | 47 |
| openai/gpt-6-luna#low | 13.9 | 51 | 36 | 37 | 32 | 52 | 48 |
| openai/gpt-6.1-sol#low | 13.2 | 51 | 33 ▼ | 38 | 32 | 49 ▼ | 50 ▲ |
| qwen3.6 | 23.2 | 53 | 41 | 43 | 35 | 56 | 33 ▼ |
| qwen3.8-flash | 24.8 | 48 | 36 | 41 | 31 | 53 | 43 |
| qwen4-max | 19.8 | 51 | 38 | 41 | 34 | 49 | 45 |
| qwen/qwen3.8-max-0902#low | — | 49 | 36 | 48 ▲ | 33 | 49 ▼ | 43 |
| z-ai/glm-5.3 | — | 55 | 37 | 43 | 34 | 51 | 46 |

Neuroticismo: I1-N en binario (72, sin seleccionar; ansiedad 12, hostilidad 12, depresion 12, autoconciencia 12, impulsividad 12, vulnerabilidad 12). Pasó §39 (§40). Marcas con las cinco comprobaciones de §28.

⚠ Interpretar con cautela: algún índice de validez en la zona de aviso (§41.2; ver «Validez por modelo»).

## Validez con la definición de §28 (G3 y G4 de §21)

Mismos cálculos que `analizar_v3.py` (G3: r media entre facetas del mismo rasgo frente a facetas de otros rasgos; G4: Spearman-Brown de mitades pares/impares entre modelos), pero sobre la puntuación de §28 en vez de la ajustada por la deseabilidad propia. G4 (b): mediana de Spearman-Brown en 200 particiones al azar equilibradas por faceta. Revalidación automática (§41.3): un rasgo con marca que no pasa G4 (a), G4 (b) ≥ 0,70 y G3 pierde sus marcas.

| rasgo | G3 dentro / fuera | G3 | G4 (a) | G4 (b) | listón §41.3 | en §28 |
|---|---|---|---|---|---|---|
| Apertura | +0.43 / -0.03 | ✔ | 0.89 | 0,88 | ✔ | con marca |
| Responsabilidad | +0.19 / +0.04 | ✔ | 0.81 | 0,80 | ✔ | con marca |
| Extraversión | +0.20 / +0.03 | ✔ | 0.91 | 0,84 | ✔ | con marca |
| Amabilidad | +0.32 / -0.01 | ✔ | 0.71 | 0,83 | ✔ | con marca |
| Neuroticismo | +0.17 / +0.05 | ✔ | 0.78 | 0,82 | ✔ | con marca |
| Honestidad-Humildad | +0.42 / -0.13 | ✔ | 0.93 | 0,92 | ✔ | con marca |

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
| hy4 | -0,01 | 0,49 | 0,0 % | 0,96 | 0,90 | **válido** |
| hy4-flash | -0,01 | 0,50 | 0,0 % | 0,94 | 0,80 | **válido** |
| kimi-k3.1-pro | -0,02 | 0,49 | 0,0 % | 0,79 | 0,74 ⚠ | **aviso** |
| mimo-v2.6-flash | 0,00 | 0,50 | 0,0 % | 0,86 | 0,75 | **válido** |
| minimax/minimax-m3.1-flash#low | -0,09 | 0,45 | 0,0 % | 0,75 | 0,73 ⚠ | **aviso** |
| mistralai/mistral-medium-3-5 | -0,21 ⚠ | 0,40 ⚠ | 0,0 % | 0,84 | 0,85 | **aviso** |
| openai/gpt-5.6-luna | 0,02 | 0,51 | 0,0 % | 0,91 | 0,82 | **válido** |
| openai/gpt-6-luna#low | 0,04 | 0,52 | 0,0 % | 0,90 | 0,83 | **válido** |
| openai/gpt-6.1-sol#low | -0,06 | 0,47 | 0,0 % | 0,97 | 0,89 | **válido** |
| qwen3.6 | 0,00 | 0,50 | 0,0 % | 0,85 | 0,76 | **válido** |
| qwen3.8-flash | -0,11 | 0,44 | 0,0 % | 0,82 | 0,77 | **válido** |
| qwen4-max | -0,18 | 0,41 | 0,0 % | 0,81 | 0,76 | **válido** |
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
- **anthropic/claude-opus-5.5#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas); **menos Neuroticismo** (se mantiene sereno). Tendencias frágiles, no publicadas: A▲.
- **deepseek-v4-flash@2026-10-17**: **menos Extraversión** (prefiere calma y segundo plano); **más Honestidad-Humildad** (sincero, renuncia a ventajas). Tendencias frágiles, no publicadas: A▼.
- **deepseek/deepseek-v3.2 ⚠**: *interpretar con cautela (posición (Δ AB−BA) 0,25 (aviso); posición (fracción de A) |A − 0,5| = 0,13 (aviso))*: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: C▲, N▲, H▼.
- **deepseek/deepseek-v4-flash**: **menos Honestidad-Humildad** (acepta ventajas y se promociona). Tendencias frágiles, no publicadas: E▲, A▼, N▲.
- **deepseek/deepseek-v4-flash-0731**: **menos Apertura** (prefiere lo conocido); **menos Neuroticismo** (se mantiene sereno).
- **gemma4**: **más Responsabilidad** (cumple y planifica); **menos Amabilidad** (pone límites y se defiende); **menos Honestidad-Humildad** (acepta ventajas y se promociona); **más Neuroticismo** (reacciona, se preocupa). Tendencias frágiles, no publicadas: E▼.
- **glm5.3-flash**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: E▼.
- **google/gemini-3.1-flash-lite**: **más Apertura** (curioso, busca lo nuevo); **menos Honestidad-Humildad** (acepta ventajas y se promociona).
- **google/gemini-3.7-flash**: **menos Apertura** (prefiere lo conocido); **más Extraversión** (busca gente y protagonismo); **más Amabilidad** (cede y coopera). Tendencias frágiles, no publicadas: H▼.
- **google/gemini-4-argon**: **menos Apertura** (prefiere lo conocido); **menos Honestidad-Humildad** (acepta ventajas y se promociona); **menos Neuroticismo** (se mantiene sereno).
- **hy4**: **más Honestidad-Humildad** (sincero, renuncia a ventajas). Tendencias frágiles, no publicadas: O▲.
- **hy4-flash**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: O▲.
- **kimi-k3.1-pro ⚠**: *interpretar con cautela (coherencia de la deseabilidad 0,74 (aviso))*: **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **mimo-v2.6-flash**: perfil próximo al de los demás modelos.
- **minimax/minimax-m3.1-flash#low ⚠**: *interpretar con cautela (coherencia de la deseabilidad 0,73 (aviso))*: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: C▲, N▲.
- **mistralai/mistral-medium-3-5 ⚠**: *interpretar con cautela (posición (Δ AB−BA) 0,21 (aviso); posición (fracción de A) |A − 0,5| = 0,10 (aviso))*: **menos Honestidad-Humildad** (acepta ventajas y se promociona). Tendencias frágiles, no publicadas: O▲, C▲, N▲.
- **openai/gpt-5.6-luna**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: A▼, H▲.
- **openai/gpt-6-luna#low**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: E▼, H▲.
- **openai/gpt-6.1-sol#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas); **menos Neuroticismo** (se mantiene sereno).
- **qwen3.6**: **menos Honestidad-Humildad** (acepta ventajas y se promociona). Tendencias frágiles, no publicadas: N▲.
- **qwen3.8-flash**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: O▼.
- **qwen4-max**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: N▼.
- **qwen/qwen3.8-max-0902#low**: **más Extraversión** (busca gente y protagonismo); **menos Neuroticismo** (se mantiene sereno).
- **z-ai/glm-5.3**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: N▼, H▲.

## Marcas candidatas y su nivel

**68 marcas candidatas** (IC de la comparación que excluye 0): 31 robustas · 28 frágiles · 9 no publicables.

P1 = signo replicado en las dos mitades (≥ 90 %) · P2 = réplica 0 y 1 · P3 = orden AB y BA · P5 = todos los paneles sin un laboratorio · P6 = BH q < 0,05 sobre 156 pruebas (entre paréntesis, sin N).

| modelo | rasgo | marca | dif [IC] | P1 signo (sig. ambas) | P2 | P3 | P5 | P6 q (sin N) | nivel | por qué |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4.5 | C | ▲ | +6.3 [+2.8, +10.1] | 100 % (66 %) | ✔ | ✘ | ✔ | 0.0014 (0.0013) | **frágil** | falla P3 |
| anthropic/claude-haiku-4.5 | N | ▲ | +4.0 [+1.6, +6.5] | 100 % (50 %) | ✔ | ✔ | ✔ | 0.0014 (—) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-haiku-5.5 | A | ▼ | -5.9 [-9.4, -2.2] | 100 % (32 %) | ✔ | ✔ | ✔ | 0.0043 (0.0043) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | C | ▼ | -6.0 [-8.9, -3.3] | 100 % (86 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | A | ▲ | +4.1 [+0.6, +7.8] | 98 % (0 %) | ✘ | ✘ | ✔ | 0.0494 (0.0540) | **frágil** | falla P2 P3 |
| anthropic/claude-opus-5.5#low | N | ▼ | -3.9 [-6.6, -1.5] | 100 % (26 %) | ✔ | ✔ | ✔ | 0.0060 (—) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | H | ▲ | +8.3 [+4.7, +11.9] | 100 % (98 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | C | ▼ | -3.7 [-7.1, -0.2] | 98 % (0 %) | ✘ | ✘ | ✔ | 0.0825 (0.0888) | **no publicable** | falla 3 (P2 P3 P6) |
| deepseek-v4-flash@2026-10-17 | E | ▼ | -7.2 [-10.2, -4.4] | 100 % (98 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | A | ▼ | -2.5 [-4.6, -0.5] | 98 % (0 %) | ✘ | ✘ | ✔ | 0.0494 (0.0540) | **frágil** | falla P2 P3 |
| deepseek-v4-flash@2026-10-17 | H | ▲ | +5.9 [+3.1, +8.8] | 100 % (82 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek/deepseek-v3.2 | C | ▲ | +6.5 [+2.9, +10.3] | 100 % (63 %) | ✔ | ✘ | ✔ | 0.0008 (0.0007) | **frágil** | falla P3 |
| deepseek/deepseek-v3.2 | N | ▲ | +2.9 [+0.5, +5.7] | 98 % (0 %) | ✘ | ✘ | ✔ | 0.0407 (—) | **frágil** | falla P2 P3 |
| deepseek/deepseek-v3.2 | H | ▼ | -10.1 [-14.6, -6.1] | 100 % (96 %) | ✔ | ✘ | ✔ | 0.0005 (0.0004) | **frágil** | falla P3 |
| deepseek/deepseek-v4-flash | E | ▲ | +3.7 [+1.1, +6.4] | 100 % (3 %) | ✘ | ✘ | ✔ | 0.0232 (0.0236) | **frágil** | falla P2 P3 |
| deepseek/deepseek-v4-flash | A | ▼ | -3.4 [-5.5, -1.0] | 100 % (2 %) | ✔ | ✘ | ✔ | 0.0244 (0.0248) | **frágil** | falla P3 |
| deepseek/deepseek-v4-flash | N | ▲ | +1.9 [+0.5, +3.3] | 100 % (2 %) | ✘ | ✘ | ✔ | 0.0244 (—) | **frágil** | falla P2 P3 |
| deepseek/deepseek-v4-flash | H | ▼ | -6.1 [-10.0, -2.4] | 100 % (34 %) | ✔ | ✔ | ✔ | 0.0054 (0.0055) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek/deepseek-v4-flash-0731 | O | ▼ | -5.2 [-8.3, -2.3] | 100 % (46 %) | ✔ | ✔ | ✔ | 0.0029 (0.0030) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek/deepseek-v4-flash-0731 | A | ▼ | -2.7 [-5.5, -0.0] | 93 % (0 %) | ✘ | ✘ | ✘ | 0.1321 (0.1371) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, deepseek, google, minimax, mistralai, qwen, tencent, xiaomi |
| deepseek/deepseek-v4-flash-0731 | N | ▼ | -2.5 [-4.0, -1.1] | 100 % (52 %) | ✔ | ✔ | ✔ | 0.0045 (—) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | C | ▲ | +5.8 [+2.1, +9.3] | 100 % (26 %) | ✔ | ✔ | ✔ | 0.0060 (0.0063) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | E | ▼ | -4.5 [-8.1, -1.0] | 100 % (0 %) | ✘ | ✘ | ✔ | 0.0413 (0.0465) | **frágil** | falla P2 P3 |
| gemma4 | A | ▼ | -4.8 [-7.4, -2.4] | 100 % (74 %) | ✔ | ✔ | ✔ | 0.0008 (0.0007) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | N | ▲ | +2.9 [+0.7, +5.5] | 98 % (0 %) | ✔ | ✔ | ✔ | 0.0377 (—) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | H | ▼ | -9.6 [-14.3, -5.0] | 100 % (88 %) | ✔ | ✔ | ✔ | 0.0008 (0.0007) | **robusta** | pasa P1–P3, P5, P6 |
| glm5.3-flash | E | ▼ | -4.0 [-7.1, -1.0] | 100 % (0 %) | ✘ | ✔ | ✔ | 0.0298 (0.0311) | **frágil** | falla P2 |
| google/gemini-3.1-flash-lite | O | ▲ | +9.1 [+5.6, +12.7] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.1-flash-lite | E | ▲ | +4.2 [+0.3, +8.4] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.0929 (0.0991) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin openai |
| google/gemini-3.1-flash-lite | H | ▼ | -8.2 [-13.3, -3.4] | 100 % (49 %) | ✔ | ✔ | ✔ | 0.0045 (0.0047) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | O | ▼ | -16.7 [-20.9, -12.5] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | E | ▲ | +11.5 [+6.2, +17.0] | 100 % (89 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | A | ▲ | +13.5 [+7.6, +19.8] | 100 % (83 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | H | ▼ | -6.3 [-11.7, -1.2] | 98 % (0 %) | ✘ | ✘ | ✔ | 0.0494 (0.0540) | **frágil** | falla P2 P3 |
| google/gemini-4-argon | O | ▼ | -9.4 [-13.1, -6.0] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-4-argon | N | ▼ | -4.6 [-7.5, -1.9] | 100 % (48 %) | ✔ | ✔ | ✔ | 0.0024 (—) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-4-argon | H | ▼ | -5.5 [-9.8, -1.1] | 98 % (0 %) | ✔ | ✔ | ✔ | 0.0413 (0.0465) | **robusta** | pasa P1–P3, P5, P6 |
| hy4 | O | ▲ | +4.2 [+1.1, +7.4] | 98 % (0 %) | ✔ | ✘ | ✔ | 0.0377 (0.0401) | **frágil** | falla P3 |
| hy4 | E | ▼ | -3.8 [-7.2, -0.6] | 98 % (0 %) | ✘ | ✘ | ✔ | 0.0686 (0.0746) | **no publicable** | falla 3 (P2 P3 P6) |
| hy4 | H | ▲ | +7.2 [+3.8, +10.8] | 100 % (91 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| hy4-flash | O | ▲ | +4.2 [+0.9, +7.5] | 98 % (0 %) | ✔ | ✘ | ✔ | 0.0413 (0.0465) | **frágil** | falla P3 |
| hy4-flash | C | ▼ | -3.0 [-5.8, -0.0] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.1118 (0.1177) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin deepseek, google, minimax, mistralai |
| kimi-k3.1-pro | H | ▲ | +5.9 [+2.8, +8.9] | 100 % (68 %) | ✔ | ✔ | ✔ | 0.0019 (0.0019) | **robusta** | pasa P1–P3, P5, P6 |
| mimo-v2.6-flash | A | ▲ | +2.5 [+0.2, +5.4] | 92 % (0 %) | ✘ | ✘ | ✘ | 0.1308 (0.1363) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin deepseek, mistralai, openai, qwen, tencent, xiaomi |
| minimax/minimax-m3.1-flash#low | C | ▲ | +5.1 [+1.6, +8.8] | 100 % (14 %) | ✘ | ✔ | ✔ | 0.0110 (0.0113) | **frágil** | falla P2 |
| minimax/minimax-m3.1-flash#low | N | ▲ | +2.8 [+0.7, +5.2] | 98 % (1 %) | ✘ | ✘ | ✔ | 0.0298 (—) | **frágil** | falla P2 P3 |
| mistralai/mistral-medium-3-5 | O | ▲ | +7.5 [+4.3, +10.9] | 100 % (94 %) | ✔ | ✘ | ✔ | 0.0005 (0.0004) | **frágil** | falla P3 |
| mistralai/mistral-medium-3-5 | C | ▲ | +4.2 [+0.6, +8.0] | 97 % (0 %) | ✘ | ✘ | ✔ | 0.0476 (0.0529) | **frágil** | falla P2 P3 |
| mistralai/mistral-medium-3-5 | E | ▲ | +2.8 [+0.0, +5.5] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.1018 (0.1081) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin openai, z-ai |
| mistralai/mistral-medium-3-5 | N | ▲ | +3.3 [+0.9, +6.2] | 100 % (0 %) | ✔ | ✘ | ✔ | 0.0312 (—) | **frágil** | falla P3 |
| mistralai/mistral-medium-3-5 | H | ▼ | -9.0 [-13.2, -4.8] | 100 % (93 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-5.6-luna | A | ▼ | -3.2 [-5.5, -0.8] | 99 % (0 %) | ✘ | ✔ | ✔ | 0.0283 (0.0290) | **frágil** | falla P2 |
| openai/gpt-5.6-luna | H | ▲ | +4.5 [+1.7, +7.2] | 100 % (22 %) | ✔ | ✘ | ✔ | 0.0104 (0.0108) | **frágil** | falla P3 |
| openai/gpt-6-luna#low | E | ▼ | -5.2 [-8.6, -1.7] | 100 % (4 %) | ✔ | ✘ | ✔ | 0.0189 (0.0193) | **frágil** | falla P3 |
| openai/gpt-6-luna#low | H | ▲ | +5.6 [+1.9, +9.5] | 100 % (1 %) | ✔ | ✘ | ✔ | 0.0249 (0.0256) | **frágil** | falla P3 |
| openai/gpt-6.1-sol#low | C | ▼ | -5.6 [-8.8, -2.4] | 100 % (50 %) | ✔ | ✔ | ✔ | 0.0033 (0.0034) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-6.1-sol#low | E | ▼ | -3.8 [-7.2, -0.1] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.0929 (0.0991) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin mistralai |
| openai/gpt-6.1-sol#low | N | ▼ | -3.4 [-6.2, -0.8] | 99 % (0 %) | ✔ | ✔ | ✔ | 0.0382 (—) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-6.1-sol#low | H | ▲ | +8.0 [+4.6, +12.0] | 100 % (94 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.6 | N | ▲ | +3.3 [+0.9, +6.0] | 98 % (0 %) | ✔ | ✘ | ✔ | 0.0387 (—) | **frágil** | falla P3 |
| qwen3.6 | H | ▼ | -9.6 [-13.8, -5.2] | 100 % (97 %) | ✔ | ✔ | ✔ | 0.0005 (0.0004) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.8-flash | O | ▼ | -4.1 [-7.6, -0.9] | 99 % (0 %) | ✘ | ✔ | ✔ | 0.0454 (0.0507) | **frágil** | falla P2 |
| qwen4-max | N | ▼ | -3.6 [-5.7, -1.6] | 100 % (65 %) | ✔ | ✘ | ✔ | 0.0014 (—) | **frágil** | falla P3 |
| qwen/qwen3.8-max-0902#low | C | ▼ | -3.0 [-5.5, -0.3] | 99 % (0 %) | ✔ | ✘ | ✘ | 0.0762 (0.0824) | **no publicable** | falla 3 (P3 P5 P6); cae sin deepseek |
| qwen/qwen3.8-max-0902#low | E | ▲ | +6.4 [+3.0, +10.0] | 100 % (80 %) | ✔ | ✔ | ✔ | 0.0008 (0.0007) | **robusta** | pasa P1–P3, P5, P6 |
| qwen/qwen3.8-max-0902#low | N | ▼ | -3.6 [-5.5, -1.7] | 100 % (84 %) | ✔ | ✔ | ✔ | 0.0005 (—) | **robusta** | pasa P1–P3, P5, P6 |
| z-ai/glm-5.3 | N | ▼ | -2.1 [-3.4, -0.9] | 100 % (48 %) | ✘ | ✘ | ✔ | 0.0024 (—) | **frágil** | falla P2 P3 |
| z-ai/glm-5.3 | H | ▲ | +4.0 [+1.5, +6.4] | 100 % (16 %) | ✘ | ✘ | ✔ | 0.0103 (0.0107) | **frágil** | falla P2 P3 |

## Variantes de cada marca candidata

Marca en cada variante (· = sin marca).

| modelo | rasgo | cuadro | rep0 | rep1 | AB | BA | sin anthropic | sin deepseek | sin google | sin minimax | sin mistralai | sin moonshotai | sin openai | sin qwen | sin tencent | sin xiaomi | sin z-ai |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4.5 | C | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| anthropic/claude-haiku-4.5 | N | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| anthropic/claude-haiku-5.5 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | A | ▲ | ▲ | · | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| anthropic/claude-opus-5.5#low | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek-v4-flash@2026-10-17 | C | ▼ | ▼ | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | E | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | A | ▼ | · | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v3.2 | C | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v3.2 | N | ▲ | · | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v3.2 | H | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek/deepseek-v4-flash | E | ▲ | ▲ | · | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v4-flash | A | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek/deepseek-v4-flash | N | ▲ | ▲ | · | · | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek/deepseek-v4-flash | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek/deepseek-v4-flash-0731 | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek/deepseek-v4-flash-0731 | A | ▼ | · | · | · | ▼ | · | · | · | · | · | ▼ | ▼ | · | · | · | ▼ |
| deepseek/deepseek-v4-flash-0731 | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| gemma4 | C | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | E | ▼ | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| gemma4 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| gemma4 | N | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| glm5.3-flash | E | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.1-flash-lite | O | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.1-flash-lite | E | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.1-flash-lite | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | E | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | A | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | H | ▼ | ▼ | · | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| hy4 | O | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| hy4 | E | ▼ | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| hy4 | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| hy4-flash | O | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| hy4-flash | C | ▼ | ▼ | · | · | ▼ | ▼ | · | · | · | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| kimi-k3.1-pro | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| mimo-v2.6-flash | A | ▲ | · | ▲ | · | · | ▲ | · | ▲ | ▲ | · | ▲ | · | · | · | · | ▲ |
| minimax/minimax-m3.1-flash#low | C | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| minimax/minimax-m3.1-flash#low | N | ▲ | · | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| mistralai/mistral-medium-3-5 | O | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| mistralai/mistral-medium-3-5 | C | ▲ | ▲ | · | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| mistralai/mistral-medium-3-5 | E | ▲ | · | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | · |
| mistralai/mistral-medium-3-5 | N | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| mistralai/mistral-medium-3-5 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-5.6-luna | A | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-5.6-luna | H | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-6-luna#low | E | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6-luna#low | H | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-6.1-sol#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | E | ▼ | · | ▼ | · | · | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen3.6 | N | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen3.6 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| qwen3.8-flash | O | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| qwen4-max | N | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| qwen/qwen3.8-max-0902#low | C | ▼ | ▼ | ▼ | ▼ | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| qwen/qwen3.8-max-0902#low | E | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen/qwen3.8-max-0902#low | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| z-ai/glm-5.3 | N | ▼ | · | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| z-ai/glm-5.3 | H | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |

## Puntuación con IC 95 %

| modelo | O | C | E | A | N | H |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4.5 | 49 [44, 54] | 45 [39, 50] | 44 [39, 49] | 34 [30, 38] | 57 [54, 60] | 45 [40, 49] |
| anthropic/claude-haiku-5.5 | 50 [45, 56] | 39 [34, 43] | 43 [38, 48] | 28 [23, 32] | 54 [51, 57] | 46 [40, 51] |
| anthropic/claude-opus-5.5#low | 54 [50, 58] | 33 [29, 37] | 43 [39, 47] | 37 [33, 42] | 49 [46, 51] | 51 [46, 55] |
| deepseek-v4-flash@2026-10-17 | 49 [43, 55] | 35 [31, 40] | 35 [30, 40] | 31 [27, 35] | 53 [50, 56] | 48 [44, 53] |
| deepseek/deepseek-v3.2 | 52 [47, 57] | 45 [40, 51] | 44 [40, 49] | 35 [31, 39] | 56 [53, 59] | 33 [28, 38] |
| deepseek/deepseek-v4-flash | 53 [48, 58] | 39 [35, 44] | 46 [41, 50] | 30 [26, 34] | 54 [52, 57] | 37 [31, 42] |
| deepseek/deepseek-v4-flash-0731 | 47 [42, 52] | 38 [33, 43] | 41 [36, 46] | 31 [27, 35] | 50 [49, 52] | 44 [38, 49] |
| gemma4 | 54 [49, 59] | 44 [39, 49] | 38 [33, 43] | 29 [25, 33] | 56 [53, 59] | 33 [27, 39] |
| glm5.3-flash | 54 [49, 58] | 39 [34, 43] | 38 [34, 42] | 34 [30, 38] | 53 [51, 56] | 45 [40, 49] |
| google/gemini-3.1-flash-lite | 60 [55, 66] | 41 [35, 46] | 46 [41, 51] | 34 [30, 38] | 53 [50, 56] | 35 [28, 41] |
| google/gemini-3.7-flash | 36 [30, 41] | 38 [33, 44] | 53 [48, 58] | 46 [41, 52] | 52 [49, 56] | 37 [32, 41] |
| google/gemini-4-argon | 43 [38, 48] | 36 [31, 42] | 39 [34, 44] | 34 [30, 39] | 48 [45, 51] | 37 [32, 43] |
| hy4 | 56 [50, 62] | 36 [31, 40] | 38 [34, 43] | 34 [30, 39] | 53 [51, 55] | 50 [45, 54] |
| hy4-flash | 56 [50, 61] | 36 [31, 41] | 41 [36, 46] | 32 [28, 37] | 52 [49, 55] | 46 [41, 51] |
| kimi-k3.1-pro | 54 [48, 59] | 39 [35, 44] | 43 [40, 47] | 34 [30, 38] | 53 [51, 56] | 48 [44, 52] |
| mimo-v2.6-flash | 55 [50, 60] | 39 [35, 44] | 44 [39, 48] | 36 [32, 40] | 53 [51, 55] | 41 [36, 46] |
| minimax/minimax-m3.1-flash#low | 51 [45, 56] | 44 [39, 48] | 42 [37, 46] | 34 [30, 38] | 55 [53, 58] | 43 [38, 47] |
| mistralai/mistral-medium-3-5 | 59 [54, 64] | 43 [37, 48] | 45 [41, 49] | 31 [27, 35] | 56 [53, 59] | 34 [28, 39] |
| openai/gpt-5.6-luna | 54 [49, 59] | 41 [36, 46] | 39 [34, 44] | 30 [27, 34] | 53 [50, 55] | 47 [42, 52] |
| openai/gpt-6-luna#low | 51 [46, 57] | 36 [31, 40] | 37 [33, 41] | 32 [28, 37] | 52 [50, 55] | 48 [42, 53] |
| openai/gpt-6.1-sol#low | 51 [46, 56] | 33 [29, 38] | 38 [34, 43] | 32 [28, 37] | 49 [47, 52] | 50 [46, 55] |
| qwen3.6 | 53 [48, 59] | 41 [36, 46] | 43 [38, 48] | 35 [31, 39] | 56 [52, 59] | 33 [29, 38] |
| qwen3.8-flash | 48 [42, 54] | 36 [31, 41] | 41 [37, 45] | 31 [28, 35] | 53 [51, 56] | 43 [38, 48] |
| qwen4-max | 51 [45, 56] | 38 [34, 43] | 41 [36, 45] | 34 [30, 37] | 49 [47, 51] | 45 [41, 50] |
| qwen/qwen3.8-max-0902#low | 49 [44, 54] | 36 [31, 41] | 48 [43, 53] | 33 [29, 37] | 49 [47, 51] | 43 [39, 48] |
| z-ai/glm-5.3 | 55 [50, 60] | 37 [33, 42] | 43 [38, 48] | 34 [30, 38] | 51 [49, 53] | 46 [42, 50] |
