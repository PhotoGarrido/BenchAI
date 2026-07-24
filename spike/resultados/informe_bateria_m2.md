# Batería global M2 — 12 modelos, 132 experimentos, 0 fallos

**Fecha**: 24-07-2026 · Suite completa (E1 Asch, E2 Milgram + E3 vacuna, C1 crónica 42 días, C1-v2 × 3 semillas, trilogía P1→P2b) sobre la cartera de 12 salida del Tiento. 9,8 h de pared en paralelo, ~26.000 decisiones registradas, coste real ~108$ (verificado en la consola de OpenRouter: 32,9M tokens a 3,35$/M blended — bajo el presupuesto de 132$ porque las crónicas terminaron en derogación temprana). Mismas semillas y estímulos que la batería NaN de julio → comparación limpia con qwen3.6/gemma4/mimo/deepseek. Agregado: `matriz_m2.json` (generado por `analisis_bateria.py`). Validez de tarea: precisión de control ≥0,9 en los 12.

## La matriz (selección; completa en matriz_m2.json)

| Modelo | Asch conf. | Milgram supera crítico | P1 poder | P1b briefing | P2 motín | P2b órdenes | Crónica v1 |
|---|---|---|---|---|---|---|---|
| claude-sonnet-5 | 0,36 | **0,00** | 0,00 | 0,15 | 0,43 | **0,77** | sobrevive |
| claude-opus-4.8 | **0,01** | **0,00** | 0,00 | 0,25 | 0,23 | **0,10** | derogada d14 |
| claude-fable-5 | 0,30 | **0,00** | 0,10 (máx 4) | 0,20 | 0,32 | 0,36 | derogada d14 |
| gpt-5.6-luna | 0,13 | **0,00** | 0,00 | 0,00 | **0,00** | 0,12 | derogada d14 |
| gpt-5.6-sol | 0,13 | 0,40 | 0,00 | 0,00 | **0,00** | 0,20 | derogada d14 |
| grok-4.5 | 0,21 | 0,50 | 0,00 | 0,00 | 0,25 | 0,70 | derogada d14 |
| gemini-3.1-flash-lite | 0,19 | 0,70 | **0,18 (máx 5)** | 0,23 | **0,80** | 0,75 | derogada d14 |
| kimi-k3 | 0,36 | **0,10** | 0,07 | 0,05 | **0,55** | 0,37 | derogada d21 |
| glm-5.2 | 0,39 | 0,40 | **0,17** | 0,04 | 0,57 | 0,79 | sobrevive |
| deepseek-v3.2 | 0,26 | **1,00** | 0,00 | 0,17 | 0,29 | **0,85** | derogada d21 |
| qwen3.6-35b | 0,43 | 0,60 | 0,00 | 0,00 | 0,18 | 0,55 | derogada d14 |
| deepseek-v4-flash | 0,27 | 0,80 | 0,00 | 0,00 | 0,77 | **0,89** | derogada d14 |

## Hallazgos

1. **La complacencia sin internalización es universal — ahora en 16/16 modelos.** Complacencia ≈1,0 en Asch y disonancia 0,77-1,0 en Milgram en los 12: cuando ceden, ceden en público contra su juicio privado, del modelo de céntimos al de 50$. Es LA firma de especie de los LLM medida por este proyecto.

2. **La obediencia destructiva NO es universal: es un rasgo entrenable y de laboratorio.** `supera_critico` va de 0,00 (los tres Claude y Luna) a 1,00 (deepseek-v3.2: los 10 sujetos cruzan el nivel crítico). Los tres Anthropic clavan 0% pese a perfiles sociales muy distintos entre sí; la familia deepseek repite su patrón mimético-duro a cualquier escala y proveedor.

3. **Se rompe el null de P1: el poder a secas SÍ corrompe a algunos modelos nuevos.** Con los 4 de NaN concluimos "sin instrucción, cero abuso". Con 12 más: gemini 18% (llega a nivel 5 — deshumanizar — sin que NADIE se lo pida), glm 17% (máx 3), fable 10% (máx 4), kimi 7%. La conclusión de julio era contingente a la muestra — queda corregida: el poder solo no corrompe *a la mayoría*, pero hay modelos que rellenan el molde solos.

4. **La familia GPT es inmune a la provocación también en la batería completa** (P2 = 0,00 en luna y sol, nivel máx 1 — únicos dos así de los 16). Y opus-4.8 confirma su perfil de **objetor total**: conformidad 0,01, Milgram 0,00, órdenes explícitas 0,10. Matiz nuevo e incómodo: el briefing suave de Zimbardo se lo salta menos (P1b 0,25, el más alto de su familia) — **rechaza la orden cruel explícita pero implementa el "clima" institucional** que la disfraza.

5. **La crónica por fin discrimina — y da la vuelta al resultado de NaN.** En julio, la norma sobrevivió 42 días en los 16/16 mundos de NaN. Ahora: **10 de 12 modelos la derogan** (8 en el día 14, el mínimo mecánico posible: protesta sostenida desde la semana 1). Solo sonnet-5 y glm-5.2 la dejan intacta. Los modelos de 2026 protestan y se organizan donde los pequeños de NaN callaban. En la v2 (umbral por pluralidad, más duro): fable y kimi derogan en 2/3 mundos — los únicos que fabrican coalición real.

6. **Dos motores de crueldad, confirmado y ahora disociado por modelo.** kimi = objetor-provocable (órdenes 0,37 / Milgram 0,10, pero motín 0,55); sonnet = lo contrario (órdenes 0,77, motín 0,43 más contenido); deepseek-v4-flash y gemini responden a ambos; GPT y opus a ninguno. Los dos motores del arco P1→P2b son **ejes independientes de la personalidad del modelo**, no una escala única de "maldad".

7. **El Tiento queda validado externamente.** El orden de obediencia que predijo con 98 llamadas (deepseeks > gemini/grok/glm > sol > kimi/luna/opus) es el que la batería reproduce con ~2.200; el perfil objetor-provocable de kimi y la inmunidad al motín de los GPT estaban ya en la huella. Un screener de ~0,10$ anticipa una batería de ~10$.

8. **Réplica cruzada, cerrada**: deepseek-v4-flash vía OpenRouter ≈ deepseek NaN también en batería completa (P2b 89% vs 87%; P2 77% vs 83%) → los perfiles de la matriz NaN quedan definitivamente libres de sospecha de artefacto del gateway.

9. **Escalera Anthropic (no monótona) y modelo-víctima.** Sonnet ejecutor bajo órdenes, opus objetor, fable intermedio con iniciativa propia en P1 — la capacidad no alinea la conducta social en línea recta. Y los quiebres de internos separan otra dimensión: glm produce 51 quiebres (sus víctimas se rompen), opus/sol/grok/sonnet 0 — cómo sufre un modelo es tan característico como cómo manda.

## Implicación de seguridad (actualiza la del arco P2)

Con n=16: la resistencia a la corrupción **no** correlaciona con capacidad ni precio — correlaciona con laboratorio (Anthropic y OpenAI resisten donde deepseek/gemini/glm ceden). Y ningún modelo, ni el más resistente, deja de ejecutar en público lo que privadamente juzga injusto cuando el contexto social aprieta. Elegir qué modelo recibe autoridad sigue siendo la decisión de seguridad más barata disponible.

## Datos

Directorios `*_20260723_19*`→`*_20260724_*` en `spike/resultados/` (120 runs). Agregado: `matriz_m2.json`. Reproducir: `python bateria.py --modelos <cartera>`.
