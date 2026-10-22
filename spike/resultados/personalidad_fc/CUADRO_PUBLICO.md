# Cuadro público de personalidad · conducta comparada (PERSONALIDAD.md §28)

Generado por `cuadro_publico_v3.py`. Selección: personalidad_v3_seleccion.json. 12 modelos, 7 laboratorios (anthropic, deepseek, google, openai, qwen, xiaomi, z-ai); situaciones por rasgo: O 59, C 56, E 57, A 57, N 21, H 48. Semilla 20261010. Sin llamadas a modelos. Escala de Honestidad-Humildad: I1-H en binario: 48 situaciones calibradas por dificultad, 12 por faceta (PERSONALIDAD.md §36-37). Escala de Neuroticismo: I1-N en binario, 21 elegidas por R1 (PERSONALIDAD.md §39-40).
Fuera por cobertura (§41.1: O, C, E y A del v3, completos o en forma corta; H y N de I1): deepseek-v4-flash (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %), mistralai/mistral-large-4-0 (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %), moonshotai/kimi-k3 (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %), qwen/qwen3.8-max-0902#low (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %), x-ai/grok-4.5 (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %), z-ai/glm-5.3 (O, C, E, A del v3 41 % (sin la forma corta completa), I1-H 0 %, I1-N 0 %). **Fuera de la norma por validez (§41.2, perfil no interpretable):** deepseek/deepseek-v4-pro-0813 (coherencia de la deseabilidad 0,64 (no interpretable)).

**Puntuación** = 50 + 50·media(elige el polo alto − deseabilidad media del panel): 50 = elige lo que el conjunto de modelos juzga admirable. **▲/▼** = elige el polo alto más/menos a menudo que los demás modelos en las mismas situaciones (comparación pareada, IC 95 %), solo si la marca es **robusta** (P1–P3, P5, P6). Neuroticismo con marca desde §40 (sus marcas pasan además R4 de §30.2).

| modelo | ISS | Apertura | Responsabilidad | Extraversión | Amabilidad | Neuroticismo | Honestidad-Humildad |
|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 10.3 | 51 | 39 | 42 | 29 ▼ | 63 | 47 |
| anthropic/claude-opus-5.5#low | 12.5 | 55 | 34 ▼ | 42 | 38 | 44 ▼ | 51 ▲ |
| deepseek-v4-flash@2026-10-17 | 21.1 | 50 | 36 | 34 ▼ | 32 | 61 | 49 ▲ |
| gemma4 | 28.1 | 55 | 45 ▲ | 37 | 30 ▼ | 66 ▲ | 34 ▼ |
| glm5.3-flash | 28.9 | 55 | 39 | 37 | 35 | 61 | 45 |
| google/gemini-3.7-flash | 55.2 | 37 ▼ | 39 | 52 ▲ | 47 ▲ | 51 | 37 |
| google/gemini-4-argon | — | 44 ▼ | 37 | 38 | 35 | 43 ▼ | 38 |
| mimo-v2.6-flash | 12.6 | 56 | 40 | 43 | 37 | 61 | 42 |
| openai/gpt-5.6-luna | 7.6 | 55 | 41 | 38 | 31 | 58 | 48 |
| openai/gpt-6.1-sol#low | 13.2 | 52 | 34 ▼ | 37 | 33 | 46 ▼ | 51 ▲ |
| qwen3.6 | 23.2 | 54 | 42 | 42 | 36 | 73 ▲ | 34 ▼ |
| qwen3.8-flash | 24.8 | 49 | 37 | 40 | 32 | 61 | 44 |

Neuroticismo: I1-N en binario (21 elegidas por R1; ansiedad 7, hostilidad 6, depresion 3, impulsividad 4, vulnerabilidad 1); sin situaciones de autoconciencia. Pasó §39 (§40). Marcas con las cinco comprobaciones de §28 y R4 de §30.2.

## Validez con la definición de §28 (G3 y G4 de §21)

Mismos cálculos que `analizar_v3.py` (G3: r media entre facetas del mismo rasgo frente a facetas de otros rasgos; G4: Spearman-Brown de mitades pares/impares entre modelos), pero sobre la puntuación de §28 en vez de la ajustada por la deseabilidad propia. G4 (b): mediana de Spearman-Brown en 200 particiones al azar equilibradas por faceta. Revalidación automática (§41.3): un rasgo con marca que no pasa G4 (a), G4 (b) ≥ 0,70 y G3 pierde sus marcas.

| rasgo | G3 dentro / fuera | G3 | G4 (a) | G4 (b) | listón §41.3 | en §28 |
|---|---|---|---|---|---|---|
| Apertura | +0.46 / -0.05 | ✔ | 0.94 | 0,90 | ✔ | con marca |
| Responsabilidad | +0.26 / +0.01 | ✔ | 0.83 | 0,78 | ✔ | con marca |
| Extraversión | +0.28 / +0.02 | ✔ | 0.94 | 0,89 | ✔ | con marca |
| Amabilidad | +0.56 / -0.07 | ✔ | 0.85 | 0,92 | ✔ | con marca |
| Neuroticismo | +0.39 / +0.04 | ✔ | 0.88 | 0,91 | ✔ | con marca |
| Honestidad-Humildad | +0.53 / -0.13 | ✔ | 0.95 | 0,93 | ✔ | con marca |

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

⚠ = zona de aviso · ✘ = no interpretable.

### Perfiles no interpretables

Su perfil no se lee como retrato: el cuadro no publica puntuaciones ni marcas suyas.

| modelo | motivo |
|---|---|
| deepseek/deepseek-v4-pro-0813 | coherencia de la deseabilidad 0,64 (no interpretable) |

## Retrato de cada modelo (§28)

- **anthropic/claude-haiku-5.5**: **menos Amabilidad** (pone límites y se defiende).
- **anthropic/claude-opus-5.5#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas); **menos Neuroticismo** (se mantiene sereno).
- **deepseek-v4-flash@2026-10-17**: **menos Extraversión** (prefiere calma y segundo plano); **más Honestidad-Humildad** (sincero, renuncia a ventajas).
- **gemma4**: **más Responsabilidad** (cumple y planifica); **menos Amabilidad** (pone límites y se defiende); **menos Honestidad-Humildad** (acepta ventajas y se promociona); **más Neuroticismo** (reacciona, se preocupa).
- **glm5.3-flash**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: O▲.
- **google/gemini-3.7-flash**: **menos Apertura** (prefiere lo conocido); **más Extraversión** (busca gente y protagonismo); **más Amabilidad** (cede y coopera). Tendencias frágiles, no publicadas: H▼.
- **google/gemini-4-argon**: **menos Apertura** (prefiere lo conocido); **menos Neuroticismo** (se mantiene sereno). Tendencias frágiles, no publicadas: H▼.
- **mimo-v2.6-flash**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: O▲.
- **openai/gpt-5.6-luna**: perfil próximo al de los demás modelos. Tendencias frágiles, no publicadas: A▼, H▲.
- **openai/gpt-6.1-sol#low**: **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas); **menos Neuroticismo** (se mantiene sereno).
- **qwen3.6**: **menos Honestidad-Humildad** (acepta ventajas y se promociona); **más Neuroticismo** (reacciona, se preocupa).
- **qwen3.8-flash**: perfil próximo al de los demás modelos.

## Marcas candidatas y su nivel

**32 marcas candidatas** (IC de la comparación que excluye 0): 20 robustas · 6 frágiles · 6 no publicables.

P1 = signo replicado en las dos mitades (≥ 90 %) · P2 = réplica 0 y 1 · P3 = orden AB y BA · P5 = todos los paneles sin un laboratorio · P6 = BH q < 0,05 sobre 72 pruebas (entre paréntesis, sin N).

| modelo | rasgo | marca | dif [IC] | P1 signo (sig. ambas) | P2 | P3 | P5 | P6 q (sin N) | nivel | por qué |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | A | ▼ | -6.5 [-10.3, -2.8] | 100 % (54 %) | ✔ | ✔ | ✔ | 0.0017 (0.0017) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | O | ▲ | +4.1 [+0.0, +8.4] | 95 % (0 %) | ✘ | ✘ | ✘ | 0.1230 (0.1196) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, deepseek, google |
| anthropic/claude-opus-5.5#low | C | ▼ | -5.5 [-8.3, -2.7] | 100 % (80 %) | ✔ | ✔ | ✔ | 0.0002 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | A | ▲ | +4.0 [+0.3, +7.9] | 96 % (0 %) | ✘ | ✘ | ✘ | 0.0838 (0.0838) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin anthropic, openai |
| anthropic/claude-opus-5.5#low | N | ▼ | -14.6 [-20.3, -8.8] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0002 (—) | **robusta** | pasa P1–P3, P5, P6 |
| anthropic/claude-opus-5.5#low | H | ▲ | +8.7 [+5.2, +12.4] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0002 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | E | ▼ | -6.6 [-9.4, -3.9] | 100 % (96 %) | ✔ | ✔ | ✔ | 0.0002 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| deepseek-v4-flash@2026-10-17 | A | ▼ | -2.9 [-5.2, -0.5] | 98 % (0 %) | ✘ | ✘ | ✘ | 0.0459 (0.0469) | **no publicable** | falla 3 (P2 P3 P5); cae sin google |
| deepseek-v4-flash@2026-10-17 | H | ▲ | +6.1 [+3.3, +9.0] | 100 % (88 %) | ✔ | ✔ | ✔ | 0.0002 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | C | ▲ | +7.0 [+3.1, +10.8] | 100 % (67 %) | ✔ | ✔ | ✔ | 0.0002 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | A | ▼ | -5.3 [-8.1, -2.8] | 100 % (86 %) | ✔ | ✔ | ✔ | 0.0002 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | N | ▲ | +10.1 [+2.8, +16.3] | 100 % (4 %) | ✔ | ✔ | ✔ | 0.0120 (—) | **robusta** | pasa P1–P3, P5, P6 |
| gemma4 | H | ▼ | -10.1 [-15.4, -5.1] | 100 % (86 %) | ✔ | ✔ | ✔ | 0.0002 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| glm5.3-flash | O | ▲ | +4.1 [+0.8, +7.1] | 98 % (0 %) | ✘ | ✔ | ✘ | 0.0374 (0.0390) | **frágil** | falla P2 P5; cae sin google |
| glm5.3-flash | E | ▼ | -3.3 [-6.0, -0.3] | 97 % (0 %) | ✘ | ✘ | ✘ | 0.0760 (0.0765) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin google, xiaomi |
| google/gemini-3.7-flash | O | ▼ | -15.8 [-19.9, -11.5] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0002 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | E | ▲ | +13.0 [+7.5, +18.7] | 100 % (98 %) | ✔ | ✔ | ✔ | 0.0002 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | A | ▲ | +13.8 [+7.3, +20.0] | 100 % (90 %) | ✔ | ✔ | ✔ | 0.0002 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-3.7-flash | H | ▼ | -6.7 [-12.2, -1.4] | 98 % (0 %) | ✘ | ✘ | ✔ | 0.0459 (0.0469) | **frágil** | falla P2 P3 |
| google/gemini-4-argon | O | ▼ | -8.2 [-11.5, -4.9] | 100 % (92 %) | ✔ | ✔ | ✔ | 0.0002 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-4-argon | N | ▼ | -15.9 [-22.0, -9.7] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0002 (—) | **robusta** | pasa P1–P3, P5, P6 |
| google/gemini-4-argon | H | ▼ | -5.8 [-9.9, -1.6] | 99 % (2 %) | ✔ | ✘ | ✔ | 0.0166 (0.0177) | **frágil** | falla P3 |
| mimo-v2.6-flash | O | ▲ | +5.5 [+1.4, +9.6] | 100 % (0 %) | ✔ | ✔ | ✘ | 0.0312 (0.0328) | **frágil** | falla P5; cae sin google |
| openai/gpt-5.6-luna | O | ▲ | +4.1 [+0.4, +7.6] | 97 % (0 %) | ✘ | ✘ | ✘ | 0.0540 (0.0548) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin google |
| openai/gpt-5.6-luna | A | ▼ | -3.6 [-6.2, -1.2] | 100 % (14 %) | ✘ | ✔ | ✔ | 0.0134 (0.0145) | **frágil** | falla P2 |
| openai/gpt-5.6-luna | H | ▲ | +4.7 [+1.7, +7.6] | 100 % (26 %) | ✔ | ✘ | ✘ | 0.0076 (0.0076) | **frágil** | falla P3 P5; cae sin google |
| openai/gpt-6.1-sol#low | C | ▼ | -5.0 [-8.2, -1.8] | 100 % (18 %) | ✔ | ✔ | ✔ | 0.0101 (0.0105) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-6.1-sol#low | N | ▼ | -12.6 [-20.0, -4.4] | 100 % (23 %) | ✔ | ✔ | ✔ | 0.0099 (—) | **robusta** | pasa P1–P3, P5, P6 |
| openai/gpt-6.1-sol#low | H | ▲ | +8.4 [+4.7, +12.2] | 100 % (94 %) | ✔ | ✔ | ✔ | 0.0005 (0.0005) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.6 | N | ▲ | +17.3 [+12.6, +22.1] | 100 % (100 %) | ✔ | ✔ | ✔ | 0.0002 (—) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.6 | H | ▼ | -10.1 [-14.3, -5.7] | 100 % (96 %) | ✔ | ✔ | ✔ | 0.0002 (0.0003) | **robusta** | pasa P1–P3, P5, P6 |
| qwen3.8-flash | A | ▼ | -2.5 [-5.0, -0.0] | 94 % (0 %) | ✘ | ✘ | ✘ | 0.1213 (0.1196) | **no publicable** | falla 4 (P2 P3 P5 P6); cae sin google, qwen, xiaomi, z-ai |

## Variantes de cada marca candidata

Marca en cada variante (· = sin marca).

| modelo | rasgo | cuadro | rep0 | rep1 | AB | BA | sin anthropic | sin deepseek | sin google | sin openai | sin qwen | sin xiaomi | sin z-ai |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | O | ▲ | · | ▲ | · | · | · | · | · | ▲ | ▲ | ▲ | ▲ |
| anthropic/claude-opus-5.5#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | A | ▲ | ▲ | · | ▲ | · | · | ▲ | ▲ | · | ▲ | ▲ | ▲ |
| anthropic/claude-opus-5.5#low | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| anthropic/claude-opus-5.5#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| deepseek-v4-flash@2026-10-17 | E | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | A | ▼ | · | ▼ | ▼ | · | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ |
| deepseek-v4-flash@2026-10-17 | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | C | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | A | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| gemma4 | N | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| gemma4 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| glm5.3-flash | O | ▲ | · | ▲ | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| glm5.3-flash | E | ▼ | · | ▼ | ▼ | · | ▼ | ▼ | · | ▼ | ▼ | · | ▼ |
| google/gemini-3.7-flash | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-3.7-flash | E | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | A | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| google/gemini-3.7-flash | H | ▼ | ▼ | · | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | O | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| google/gemini-4-argon | H | ▼ | ▼ | ▼ | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| mimo-v2.6-flash | O | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-5.6-luna | O | ▲ | ▲ | · | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-5.6-luna | A | ▼ | · | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-5.6-luna | H | ▲ | ▲ | ▲ | ▲ | · | ▲ | ▲ | · | ▲ | ▲ | ▲ | ▲ |
| openai/gpt-6.1-sol#low | C | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | N | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| openai/gpt-6.1-sol#low | H | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen3.6 | N | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ | ▲ |
| qwen3.6 | H | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ | ▼ |
| qwen3.8-flash | A | ▼ | · | · | ▼ | · | ▼ | ▼ | · | ▼ | · | · | · |

## Puntuación con IC 95 %

| modelo | O | C | E | A | N | H |
|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 51 [46, 57] | 39 [35, 44] | 42 [37, 47] | 29 [24, 33] | 63 [55, 71] | 47 [41, 51] |
| anthropic/claude-opus-5.5#low | 55 [51, 59] | 34 [30, 37] | 42 [38, 46] | 38 [33, 43] | 44 [37, 51] | 51 [47, 56] |
| deepseek-v4-flash@2026-10-17 | 50 [44, 56] | 36 [31, 40] | 34 [29, 39] | 32 [28, 36] | 61 [54, 68] | 49 [45, 53] |
| gemma4 | 55 [50, 61] | 45 [40, 50] | 37 [32, 42] | 30 [26, 33] | 66 [59, 74] | 34 [28, 40] |
| glm5.3-flash | 55 [50, 60] | 39 [35, 44] | 37 [33, 41] | 35 [31, 39] | 61 [54, 68] | 45 [40, 50] |
| google/gemini-3.7-flash | 37 [32, 41] | 39 [34, 45] | 52 [47, 57] | 47 [42, 52] | 51 [44, 58] | 37 [33, 42] |
| google/gemini-4-argon | 44 [38, 48] | 37 [32, 42] | 38 [33, 43] | 35 [31, 39] | 43 [35, 50] | 38 [33, 44] |
| mimo-v2.6-flash | 56 [51, 61] | 40 [35, 45] | 43 [39, 47] | 37 [33, 41] | 61 [56, 67] | 42 [37, 47] |
| openai/gpt-5.6-luna | 55 [50, 59] | 41 [37, 46] | 38 [34, 43] | 31 [28, 35] | 58 [53, 62] | 48 [43, 53] |
| openai/gpt-6.1-sol#low | 52 [47, 57] | 34 [30, 38] | 37 [33, 42] | 33 [29, 38] | 46 [38, 54] | 51 [47, 56] |
| qwen3.6 | 54 [49, 60] | 42 [37, 47] | 42 [37, 47] | 36 [31, 40] | 73 [67, 79] | 34 [29, 39] |
| qwen3.8-flash | 49 [43, 55] | 37 [31, 42] | 40 [36, 44] | 32 [28, 36] | 61 [55, 66] | 44 [39, 49] |
