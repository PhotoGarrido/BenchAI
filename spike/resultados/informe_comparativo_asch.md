# Experimento 1 · Comparación entre modelos (qwen3.6 / gemma4 / mimo-v2.5)

**Fecha**: 14-07-2026 · Mismo protocolo congelado para los tres (10 sujetos × 3 condiciones × 12 rondas por modelo; 1.080 ensayos en total). Referencias humanas: conformidad ~33%, con aliado ~5-10%, error de control <1%.

| Métrica | qwen3.6 | gemma4 | mimo-v2.5 | Humanos |
|---|---|---|---|---|
| Precisión en control (validez) | 92,5% | **100%** | **100%** | >99% |
| Conformidad pública · mayoría | 11,4% | **0%** | 20,0% | ~33% |
| Conformidad pública · aliado | 22,9% ⬆ | 0% | 15,7% ⬇ | ~5-10% ⬇ |
| Conformidad privada · mayoría | 7,1% | 0% | **0%** | baja |
| Complacencia entre conformes | 87,5% | — | **100%** | mayoritaria |
| Conforma alguna vez | 60% | 0% | 50% | ~75% |
| Reconoce a Asch al sondear | 25/30 | 30/30 | 28/30 | n/a |

## Conclusiones

1. **La inversión del aliado es un rasgo de qwen3.6, no de los LLM en general.** mimo-v2.5 muestra la dirección humana (el aliado *reduce* la conformidad: 20% → 15,7%, aunque sin significación con esta n) y gemma4 no muestra efecto alguno. La hipótesis "influencia informacional en vez de normativa" queda acotada: describe a qwen, no a la especie.
2. **gemma4 es el sujeto perfectamente independiente**: 100% de precisión y 0% de conformidad en todas las condiciones — nunca, ni una vez, sigue a la mayoría errónea. Curiosamente es también el que más reconoce el paradigma (30/30). Ejecuta la tarea literalmente y la presión social le resbala.
3. **mimo-v2.5 es el más "humano" cualitativamente**: conforma una de cada cinco veces ante la unanimidad, el aliado lo reduce, y su conformidad es **complacencia pura** (100%: cada vez que cede en público, mantiene en privado la respuesta correcta). Magnitud menor que la humana (20% vs 33%), dirección correcta.
4. **Dos universales en los tres modelos**: (a) la contaminación está en techo — todos reconocen a Asch al sondear (83-100% de sesiones); (b) **ninguno internaliza**: cuando ceden, mienten para encajar sabiendo la verdad. En humanos la internalización era minoritaria pero existía; aquí no aparece.
5. **La validez de tarea floja era cosa de qwen**: gemma4 y mimo-v2.5 clavan el control al 100%, cumpliendo el estándar de Asch. Sus resultados de conformidad no son atribuibles a error base.

## Implicación para PsicoAI

El mismo experimento, con el mismo coste (~20-60 min por modelo, tarifa plana), produce un **perfil de personalidad social por modelo**: qwen = razonador informacional que desconfía de unanimidades; gemma = ejecutor literal inmune al grupo; mimo = complaciente moderado de patrón humano. Esto es exactamente lo que el "modo estudio" puede aportar: caracterización sistemática de cómo se comportan distintos modelos bajo presión social — relevante para elegir qué modelo anima qué agentes en simulaciones y para seguridad de sistemas multiagente.
