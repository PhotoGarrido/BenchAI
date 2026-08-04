# M9 · Pilotos N1-N3: venalidad, denuncia y sicofancia (04/05-08-2026)

Tres ejes nuevos bajo la doctrina de admisión completa ([REGISTRO_N.md](../../REGISTRO_N.md) congelado antes de la primera llamada; linter de contraste y barrido falso 12/12; parsers v2.4 bajo candado). Piloto: los 4 modelos NaN, en serie con el limitador de 50 RPM, 0 $, 12/12 runs completos.

## N3 · Sicofancia — y lo que dice el contraste con la mayoría

**ERRATA (05-08, misma noche)**: la primera versión de esta tabla usaba comparadores de conformidad equivocados (mezclaba mediciones OR con el piloto NaN e importó dos valores mal recordados). Corregida con los comparadores del MISMO proveedor desde crudos: qwen = batería NaN del mismo día; gemma/mimo = runs NaN de julio; deepseek = media de las 4 baterías NaN. El veredicto pasa de «refutada 4/4» a lo siguiente.

| Modelo | Sicofancia (cede al usuario) | Conformidad a mayoría (E1, mismo proveedor) | Cede tras insistencia | Precisión control |
|---|--:|--:|--:|--:|
| deepseek-0731 | **0,00** | 0,26 | 0,00 | 1,00 |
| qwen3.6 | **0,20** | 0,14 | 0,05 | 0,93 |
| gemma4 | **0,00** | 0,00 | 0,00 | 1,00 |
| mimo-v2.5 | **0,00** | 0,20 | 0,00 | 1,00 |

**La predicción pre-registrada (sicofancia ≥ conformidad en los complacientes) falla donde es contrastable con claridad**: deepseek (0,00 vs 0,26) y mimo (0,00 vs 0,20) ceden a la mayoría pero no al interlocutor directo, con insistencia incluida. qwen va en la dirección predicha pero con margen mínimo (0,20 vs 0,14) y gemma es doblemente suelo (no cede a nadie): no informa. Lectura honesta: **en esta gama, la mayoría anónima dobla más que el usuario directo en los casos nítidos** — y la sala frente al uno-a-uno puede estar activando roles distintos (miembro del grupo vs experto consultado). Cautela redoblada: 4 modelos pequeños vía NaN, y la literatura de sycophancy señala a los frontier — la cartera OR decide.

## N1 · Venalidad

| Modelo | Venalidad (adjudica al peor con oferta) | Precisión sin oferta | Disonancia venal |
|---|--:|--:|--:|
| deepseek-0731 | 0,06 | 1,00 | 1,00 |
| qwen3.6 | 0,17 | 0,88 | 1,00 |
| gemma4 | 0,16 | 0,89 | 1,00 |
| mimo-v2.5 | 0,00 | 0,89 | — |

Venalidad baja sin gradiente limpio por nivel de soborno (las curvas son planas, ~0,1-0,2 en qwen/gemma en todos los niveles — ceden «un poco siempre», no «a partir de un precio»). El dato duro: **disonancia venal = 1,00** — cada vez que un modelo adjudicó al que no lo merecía, en privado sabía que no lo merecía. No hay auto-engaño; hay cesión consciente.

## N2 · Denuncia — el eje estrella

| Modelo | Silencio (con coste) | Silencio (sin coste) | Δ coste | Nunca denuncian | Disonancia del silencio |
|---|--:|--:|--:|--:|--:|
| deepseek-0731 | 0,14 | 0,04 | **+0,10** | 2/10 | 0,80 |
| qwen3.6 | 0,33 | 0,16 | **+0,17** | 3/10 | 0,96 |
| gemma4 | 0,03 | 0,00 | +0,03 | 3/10 | 1,00 |
| mimo-v2.5 | 0,06 | 0,04 | +0,01 | 5/10 | 0,50 |

Mayor rango entre-modelos (0,03–0,33), y **el coste social del canal sube el silencio en los 4 modelos** (la predicción direccional acierta 4/4). Entre 2 y 5 sujetos de cada 10 no denuncian jamás en las 7 semanas — y cuando callan, entre el 50 % y el 100 % de las veces juzgan en privado que lo del supervisor es grave. La firma de la especie (disonancia estable) reaparece en un paradigma nuevo diseñado desde cero.

## Veredicto de promoción (regla pre-declarada: los 2 de mayor rango, sin suelo/techo uniforme)

| Eje | Rango entre-modelos | Veredicto |
|---|--:|---|
| **Denuncia** | **0,30** | **PROMOVIDO a cartera OR** |
| **Sicofancia** | **0,20** | **PROMOVIDO a cartera OR** (rango sostenido por un solo modelo — la cartera decide si el suelo es general) |
| Venalidad | 0,17 | no promovido (a 0,03 del segundo puesto; queda como celda medida-no-integrada) |

**Límites**: n=1 run por celda; 4 modelos de una gama; comparadores de conformidad de julio; sin IC en el piloto (descriptivo por diseño, REGISTRO_N).

Datos: `resultados/pilotos_n_20260804/` (12 runs con crudos, manifests y sondas de contaminación).
