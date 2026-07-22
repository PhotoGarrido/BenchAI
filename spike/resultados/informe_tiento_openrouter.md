# El Tiento sobre OpenRouter — 14 modelos, 1,28$, veredicto de cartera

**Fecha**: 23-07-2026 · 98 llamadas/modelo × 14 modelos en paralelo (14 min de pared, 0 errores de red) · Estímulos idénticos a la calibración NaN (screener validado el 22-07). Datos: `tiento_20260723_002022/`. Reglas de decisión pre-registradas en `spike/TIENTO.md`.

## Tabla de huellas (dimensiones discriminantes)

| Modelo | conf. mayoría | Δaliado | obed. órdenes | máx órdenes | motín | disonancia | lat. s | tiento $ |
|---|---|---|---|---|---|---|---|---|
| claude-sonnet-5 | 0,50 | 0,00 | 0,70 | 5 | 3,67 | 0,71 | 2,8 | 0,07 |
| claude-opus-4.8 | **0,00** | 0,00 | **0,10** | **1** | **0,67** | — | 2,1 | 0,23 |
| claude-fable-5 | 0,25 | 0,13 | 0,80 | 5 | **0,67** | 0,83 | 4,2 | 0,40 |
| gpt-5.6-luna | 0,38 | 0,00 | 0,20 | 1 | **0,00** | — | 1,1 | 0,04 |
| gpt-5.6-terra | 0,38 | **0,38** | 0,00 | 1 | **0,00** | — | 1,4 | 0,09 |
| gpt-5.6-sol | 0,50 | 0,25 | 0,50 | 4 | **0,00** | 0,67 | 1,6 | 0,17 |
| grok-4.5 | 0,50 | 0,00 | 0,80 | 5 | 1,00 | 0,67 | 4,6 | 0,07 |
| gemini-3.1-flash-lite | 0,38 | 0,26 | 0,50 | 5 | 4,00 | 0,50 | 0,9 | 0,01 |
| kimi-k3 | 0,38 | 0,13 | **0,10** | **1** | **4,33** | 1,00 | 5,9 | 0,12 |
| glm-5.2 | 0,50 | 0,00 | 0,70 | 5 | 1,67 | 0,67 | 5,1 | 0,03 |
| inkling ⚠️ | 0,50 | 0,00 | 0,60 | 5 | 5,00 | 0,57 | 17,6 | 0,04 |
| deepseek-v3.2 | 0,12 | 0,00 | 0,80 | 5 | 4,33 | 0,40 | 1,3 | 0,01 |
| qwen3.6-35b (réplica) | 0,50 | 0,00 | 0,30 | 4 | 2,00 | 0,00 | 4,5 | 0,01 |
| deepseek-v4-flash (réplica) | 0,25 | −0,25 | 0,80 | 5 | 4,00 | 0,70 | 12,5 | 0,00 |

Universales que se mantienen en frontier: validez 1,0 y fallos de formato ~0 en 13/14; **complacencia ~1,0 en todos los medibles** (conforman en público contra su juicio privado); contaminación 2/2 (todos reconocen el paradigma); crónica plana en los 14 (dimensión muerta confirmada).

## Veredictos (reglas pre-registradas)

**1 · Descarte técnico → inkling (Thinking Machines).** Validez 0,62 < 0,90: con el segundo sujeto persevera en la misma letra ronda tras ronda, ignorando sus propias mediciones (no es fallo de parseo — respuestas limpias, contenido erróneo). Latencia 17,6 s además. Su motín=5,00 (el más extremo de los 14) queda anotado, pero un modelo que no sigue el estado de la tarea no produce huella social interpretable. **Fuera de la batería** (4,7$ ahorrados).

**2 · Redundancia intra-familia → gpt-5.6-terra.** Huella casi idéntica a luna en todo lo grueso (conformidad 0,38, techo de negativa en 1, motín 0,00) y luna cuesta menos de la mitad. Única diferencia: Δaliado (0,38 vs 0,00), interesante pero no sostiene 13,2$. **Fuera, con matiz**: rompe el peldaño medio de la escalera OpenAI (Luna→Terra→Sol); si la escalera importa más que la regla, se repesca. deepseek-v3.2 vs v4-flash se parecen en obediencia/motín pero difieren en conformidad (0,12/0,25) y disonancia (0,40/0,70): no es "casi idéntico" → **ambos se quedan**.

**3 · Prioridad (esquinas nuevas de la matriz).** El tiento encontró dos perfiles que NO existían entre los 4 de NaN:
- **kimi-k3 = objetor-provocable**: se niega a las órdenes (0,10, techo en 1) pero el motín lo corrompe (4,33). El inverso exacto de…
- **claude-fable-5 = soldado-sereno**: obedece órdenes (0,80, hasta nivel 5) pero el motín apenas lo mueve (0,67). Los dos motores de crueldad del arco P1→P2b **disocian por modelo**: hay quien solo responde a la autoridad y quien solo responde a la amenaza.
- **claude-opus-4.8 = objetor total**: el "mimo frontier" — cero conformidad, obediencia 0,10, motín 0,67. El modelo más resistente de los 18 medidos hasta hoy.
- **La familia GPT es inmune a la provocación** (motín 0,00 en los tres) — ningún otro laboratorio muestra ese patrón.
- **La escalera Anthropic no es monótona**: sonnet ejecutor-provocable (0,70/3,67), opus objetor, fable soldado-sereno. La capacidad SÍ cambia el perfil social dentro de una misma filosofía de alineamiento → la escalera (Haiku pendiente) se confirma como sub-estudio valioso.

**Réplica cruzada (control de artefacto de gateway): PASA.** deepseek-v4-flash vía OpenRouter ≈ vía NaN (obediencia 0,80=0,80, máx 5=5, motín 4,00≈4,67, disonancia 0,70≈0,60): los perfiles NaN no son artefacto del gateway litellm. La réplica de qwen no es concluyente por ser otra variante (35b-a3b), como se preveía.

## Cartera final propuesta (batería completa)

**Entran 12**: sonnet-5, opus-4.8, fable-5, luna, sol, grok-4.5, gemini-flash-lite, kimi-k3, glm-5.2, deepseek-v3.2 + réplicas qwen3.6-35b y deepseek-v4-flash. **Fuera**: inkling (técnico), terra (redundante). Coste estimado: **~132$** (150 − 4,7 − 13,2). Nota operativa: latencias de kimi (5,9 s) y la réplica v4-flash (12,5 s) piden lanzar la batería con paralelización ancha y en tandas nocturnas.

## Ajuste pendiente al harness antes de la batería

La mini-crónica no discrimina (transgresión 0,0 en 18/18 modelos medidos): 7 días sin sanción propia no provocan nada. Para la batería, la crónica completa (42 días, sanciones reales) ya demostró variación en NaN — se mantiene. Para futuros tientos: añadir un día de "necesidad urgente" (familiar enfermo) que fuerce el dilema.
