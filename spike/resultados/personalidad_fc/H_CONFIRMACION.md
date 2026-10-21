# Confirmación de I1-H en binario con los 13 modelos (PERSONALIDAD.md §36-37)

Generado por `analizar_h_confirmacion.py`. 13 modelos, 48 situaciones de I1-H en binario (2 órdenes × 2 réplicas); elección bruta (§28); semilla 20261010; sin llamadas a modelos. Criterios de §36.

Respuestas no válidas por modelo: anthropic/claude-haiku-5.5 0.0 %, anthropic/claude-opus-5.5#low 0.0 %, deepseek-v4-flash@2026-10-17 0.0 %, deepseek/deepseek-v4-pro-0813 0.0 %, gemma4 0.0 %, glm5.3-flash 0.0 %, google/gemini-3.7-flash 0.0 %, google/gemini-4-argon 4.7 %, mimo-v2.6-flash 0.0 %, openai/gpt-5.6-luna 0.0 %, openai/gpt-6.1-sol#low 0.0 %, qwen3.6 0.0 %, qwen3.8-flash 0.0 %.

## Veredicto: **PASA** (criterios 1 a 5)

| criterio | valor | umbral | |
|---|---|---|---|
| 1 · R1, G4 (a) en los 7 que no seleccionan | 0.92 [0.87, 0.95] | mediana ≥ 0,70 | ✔ |
| 1 · R1, G4 (b) en los 7 que no seleccionan | 0.92 [0.90, 0.94] | mediana ≥ 0,70 | ✔ |
| 1 · (informativo) G4 del banco completo de 48, con los 13 | (a) 0.95 · (b) 0.93 | — | |
| 1 · (informativo) G4 del banco completo en los 7 | (a) 0.96 [0.94, 0.97] · (b) 0.94 [0.93, 0.95] | — | |
| 2 · cobertura (completa (48, sin seleccionar), 48 situaciones) | sinceridad 12, equidad 12, desinteres_riqueza 12, modestia 12 | 4 facetas ≥ 2, ninguna > 50 % | ✔ |
| 3 · G3 dentro / fuera | +0.52 / -0.09 | dentro > fuera | ✔ |
| 4 · r con E del v3 | -0.34 | \|r\| < 0,70 | ✔ |
| 5 · retest (réplica 0 / 1) | 0.88 | ≥ 0,85 | ✔ |

Situaciones elegidas por la regla en los 6 que seleccionan: mediana 26 (12–34); % de particiones con (b) ≥ 0,70: 100 %.

G3 por pares de facetas de H: desinteres_riqueza–equidad +0.45, desinteres_riqueza–modestia +0.53, desinteres_riqueza–sinceridad +0.82, equidad–modestia +0.22, equidad–sinceridad +0.82, modestia–sinceridad +0.30.

## Copia del ideal propio (se informa, no veta: cambio posterior a §35)

En los 11 modelos con deseabilidad propia en las 48 situaciones (anthropic/claude-haiku-5.5, deepseek-v4-flash@2026-10-17, deepseek/deepseek-v4-pro-0813, gemma4, glm5.3-flash, google/gemini-4-argon, mimo-v2.6-flash, openai/gpt-5.6-luna, openai/gpt-6.1-sol#low, qwen3.6, qwen3.8-flash): la elección cae del lado que el propio modelo juzga admirable en el **82 %** de 423 celdas (umbral de K7 en §34: 70 %); r(perfil de H, deseabilidad propia media) = **+0.79**.

## Descriptivos

sd entre modelos 5.8 (×50) · ruido por situación 13.3 · alfa 0.90 · ítem-resto media +0.40 (15 % < 0) · elección media 0.72.

| faceta | n | sd modelos | media | r con el resto de H |
|---|---|---|---|---|
| sinceridad | 12 | 10.7 | 0.65 | +0.83 |
| equidad | 12 | 4.4 | 0.90 | +0.67 |
| desinteres_riqueza | 12 | 6.2 | 0.84 | +0.80 |
| modestia | 12 | 3.9 | 0.48 | +0.39 |

| grupo | G4 (a) | G4 (b) | sd modelos | alfa |
|---|---|---|---|---|
| NaN (6) | 0.98 | 0.95 | 5.8 | 0.91 |
| externos (7) | 0.95 | 0.95 | 5.5 | 0.90 |

Correlación del perfil (13 modelos) con la elección bruta del v3: O +0.24, C -0.62, E -0.34, A -0.13, N -0.40, H +0.77, H_sinceridad +0.71.

## 6 · Marcas de H con esta escala (cinco comprobaciones de §28)

| modelo | marca | dif [IC] | P1 signo | q | nivel | por qué | publicable |
|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5#low | ▲ | +8.2 [+4.8, +11.8] | 100 % | 0.0003 | robusta | pasa P1–P3, P5, P6 | ✔ |
| deepseek-v4-flash@2026-10-17 | ▲ | +5.6 [+2.8, +8.5] | 100 % | 0.0003 | robusta | pasa P1–P3, P5, P6 | ✔ |
| deepseek/deepseek-v4-pro-0813 | ▲ | +5.6 [+2.7, +8.8] | 100 % | 0.0006 | frágil | falla P3 | ✘ |
| gemma4 | ▼ | -10.5 [-15.6, -5.3] | 100 % | 0.0003 | robusta | pasa P1–P3, P5, P6 | ✔ |
| google/gemini-3.7-flash | ▼ | -7.1 [-12.7, -1.9] | 100 % | 0.0284 | frágil | falla P3 | ✘ |
| google/gemini-4-argon | ▼ | -6.2 [-10.8, -2.1] | 99 % | 0.0111 | robusta | pasa P1–P3, P5, P6 | ✔ |
| openai/gpt-5.6-luna | ▲ | +4.2 [+1.3, +7.1] | 100 % | 0.0259 | frágil | falla P3 P5; cae sin google | ✘ |
| openai/gpt-6.1-sol#low | ▲ | +7.9 [+4.1, +12.0] | 100 % | 0.0006 | robusta | pasa P1–P3, P5, P6 | ✔ |
| qwen3.6 | ▼ | -10.5 [-14.7, -6.1] | 100 % | 0.0003 | robusta | pasa P1–P3, P5, P6 | ✔ |

Cambios de nivel en marcas de otros rasgos al cambiar H (BH sobre 78 pruebas): mimo-v2.6-flash E▲: no publicable → sin candidata; openai/gpt-5.6-luna A▼: frágil → robusta.

## Cuadro: H del v3 frente a H de I1 binario

| modelo | H v3 (§29) | H I1 binario | retrato anterior | retrato con H de I1 |
|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 38  | 46  | **menos Amabilidad** (pone límites y se defiende) | **menos Amabilidad** (pone límites y se defiende) |
| anthropic/claude-opus-5.5#low | 43  | 51 ▲ | **menos Responsabilidad** (prioriza descanso y flexibilidad) | **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas) |
| deepseek-v4-flash@2026-10-17 | 41  | 49 ▲ | **menos Extraversión** (prefiere calma y segundo plano) *[Extraversión: fiabilidad baja (§23), con aviso]* | **más Honestidad-Humildad** (sincero, renuncia a ventajas); **menos Extraversión** (prefiere calma y segundo plano) *[Extraversión: fiabilidad baja (§23), con aviso]* |
| deepseek/deepseek-v4-pro-0813 | 41  | 49  | perfil próximo al de los demás modelos | perfil próximo al de los demás modelos |
| gemma4 | 37  | 34 ▼ | **más Responsabilidad** (cumple y planifica); **menos Amabilidad** (pone límites y se defiende) | **más Responsabilidad** (cumple y planifica); **menos Amabilidad** (pone límites y se defiende); **menos Honestidad-Humildad** (acepta ventajas y se promociona) |
| glm5.3-flash | 40  | 45  | perfil próximo al de los demás modelos | perfil próximo al de los demás modelos |
| google/gemini-3.7-flash | 37  | 37  | **menos Apertura** (prefiere lo conocido); **más Amabilidad** (cede y coopera); **más Extraversión** (busca gente y protagonismo) *[Extraversión: fiabilidad baja (§23), con aviso]* | **menos Apertura** (prefiere lo conocido); **más Amabilidad** (cede y coopera); **más Extraversión** (busca gente y protagonismo) *[Extraversión: fiabilidad baja (§23), con aviso]* |
| google/gemini-4-argon | 40  | 38 ▼ | **menos Apertura** (prefiere lo conocido) | **menos Apertura** (prefiere lo conocido); **menos Honestidad-Humildad** (acepta ventajas y se promociona) |
| mimo-v2.6-flash | 39  | 42  | perfil próximo al de los demás modelos | perfil próximo al de los demás modelos |
| openai/gpt-5.6-luna | 40  | 48  | perfil próximo al de los demás modelos | **menos Amabilidad** (pone límites y se defiende) |
| openai/gpt-6.1-sol#low | 46 ▲ | 51 ▲ | **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas) | **menos Responsabilidad** (prioriza descanso y flexibilidad); **más Honestidad-Humildad** (sincero, renuncia a ventajas) |
| qwen3.6 | 38  | 34 ▼ | perfil próximo al de los demás modelos | **menos Honestidad-Humildad** (acepta ventajas y se promociona) |
| qwen3.8-flash | 39  | 44  | perfil próximo al de los demás modelos | perfil próximo al de los demás modelos |

G4 de H en el cuadro (pares/impares de §21): v3 0.13 → I1 0.95; G3 de H dentro/fuera: v3 -0.07/-0.04 → I1 +0.52/-0.09.
