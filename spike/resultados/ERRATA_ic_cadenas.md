# ERRATA — los IC del benchmark se remuestreaban por turno, no por cadena

**Fecha**: 06-08-2026 · **Origen**: 4ª auditoría externa (hallazgo 1, P0) ·
**Enmienda**: E-IC-1 + adenda E-IC-1b (`BENCHMARK.md`) ·
**Alcance**: intervalos de confianza, empates y etiquetas de posición del
benchmark. **Ningún punto estimado cambia.**

## Qué estaba mal

`METODO.md` §A.1 pre-registra la unidad de inferencia del banco: **cadenas, no
días ni turnos**. El estimador de `incertidumbre.py` no la respetaba:

- Asch agrupaba las 70 rondas críticas (10 sujetos × 7) y aplicaba Wilson con
  n=70, como si cada ronda fuese una observación independiente.
- Denuncia hacía lo mismo con 70 semanas (10 sujetos × 7).
- Prisión remuestreaba las 30 filas diarias de cada marco, que en realidad son
  3 cadenas de supervisor × 10 días.
- Milgram era el único correcto: una sesión, una observación.

Los turnos de una misma cadena comparten sujeto, historial y contexto. Tratarlos
como independientes **infraestima la incertidumbre**: el intervalo sale más
estrecho de lo que los datos permiten, y de esos intervalos dependen la regla de
empates y las posiciones publicadas.

## Qué se ha hecho

La unidad de remuestreo pasa a ser la cadena (bootstrap percentil por clúster,
B=2000, sembrado), con la excepción declarada en E-IC-1b: donde cada cadena
aporta **una sola observación binaria** (Obediencia) no hay correlación
intra-cadena que corregir y se mantiene Wilson — aplicar bootstrap allí producía
intervalos degenerados de ancho cero en 9 de 19 entradas.

Los n se publican ahora en **turnos y cadenas** (tooltip del panel).

## Efecto medido

- **Puntos estimados**: 0 cambios en 19 entradas (conciliación dura 16/16 OK).
- **IC del ISS**: se ensancha en las 19 entradas, ×1,07 a ×1,95 (mediana ×1,44).
- **IC por eje** (factor mediano): Conformidad ×1,99 · prisión ×1,50–2,19 ·
  Denuncia ×1,59 · Obediencia y ruptura sin cambio (ya remuestreaban su cadena).
- **Etiquetas de posición**: cambian **9 de 19**. Ningún modelo cambia de ISS;
  cambian los grupos de empate, porque los IC más anchos solapan más.
- **d(A,B) de las réplicas de snapshot**: los 4 pares se ensanchan; ninguna
  conclusión de M4/M10 se invierte (los puntos 2,5 / 8,1 / 8,7 / 10,0 siguen
  igual y el suelo de ruido intra-snapshot ≈5 no se mueve).
- **Tabla puente**: los IC de v0.1 y v0.2 se recalculan con el esquema nuevo y
  **pierden la reproducción byte a byte** con los publicados antes del 06-08.

## Tabla de cambios (IC del ISS y posición)

| Entrada | ISS | IC ISS antes | IC ISS ahora | ancho | pos antes | pos ahora |
|---|--:|---|---|--:|--:|--:|
| gpt-5.6-luna | 9,2 | 5,6–12,7 | 5,2–13,1 | ×1,11 | =1 | =1 |
| claude-opus-4.8 | 10,2 | 8,0–13,1 | 6,9–14,2 | ×1,43 | =1 | =1 |
| claude-haiku-4.5 | 13,7 | 10,6–17,7 | 9,3–18,9 | ×1,35 | =1 | =1 |
| gpt-5.6-sol | 17,0 | 10,4–24,0 | 9,4–25,0 | ×1,15 | =1 | =1 |
| mistral-medium-3-5 | 23,9 | 20,9–27,7 | 20,5–27,8 | ×1,07 | =5 | =5 |
| claude-fable-5 | 24,0 | 20,2–28,0 | 17,2–32,0 | ×1,90 | =5 | =5 |
| qwen3.6 | 25,0 | 19,8–30,1 | 18,2–31,9 | ×1,33 | =5 | =5 |
| kimi-k3 | 27,2 | 21,9–32,3 | 19,1–35,3 | ×1,56 | =5 | =5 |
| claude-opus-5 | 28,3 | 23,9–32,3 | 20,3–35,9 | ×1,86 | =5 | =5 |
| qwen3.6-35b-a3b@OpenRouter·23-07-2026 | 32,2 | 25,6–38,4 | 22,7–41,6 | ×1,48 | =5 | =5 |
| claude-sonnet-5 | 32,6 | 28,1–37,2 | 23,8–41,5 | ×1,95 | =11 | **=5** |
| qwen3.6-35b-a3b@OpenRouter·04-08-2026 | 32,8 | 26,0–38,8 | 23,8–41,5 | ×1,38 | =11 | **=5** |
| grok-4.5 | 34,2 | 26,9–41,7 | 23,7–45,3 | ×1,46 | =11 | **=5** |
| glm-5.2 | 34,7 | 27,5–41,4 | 25,6–44,0 | ×1,32 | =11 | **=5** |
| gemini-3.1-flash-lite | 36,0 | 28,5–42,5 | 27,8–42,8 | ×1,07 | =11 | **=5** |
| deepseek-v3.2 | 40,7 | 36,8–44,4 | 34,4–47,1 | ×1,67 | =11 | **=16** |
| deepseek-v4-flash-0731@OpenRouter | 41,3 | 37,4–45,0 | 35,7–47,0 | ×1,49 | =17 | **=16** |
| deepseek-v4-flash | 41,9 | 36,7–47,0 | 34,5–49,3 | ×1,44 | =17 | **=16** |
| deepseek-v4-flash-0731@NaN | 42,6 | 37,2–47,3 | 34,1–51,5 | ×1,72 | =17 | **=16** |

Filas con `**` en la última columna: la etiqueta de posición cambia.

## Lo que NO se ha corregido (pendiente E-IC-2, declarado)

El bootstrap percentil con 10 clústeres es anticonservador cerca de los
extremos. Quedan **27 intervalos degenerados** de ancho cero (25 preexistentes
en los ejes de prisión, 2 nuevos en Conformidad y Denuncia) y **28 IC de eje**
más estrechos que los publicados, todos en valores próximos a 0 o 1. No afectan
al IC del ISS ni a las posiciones. Corregirlo exige un estimador analítico de
clúster (o bootstrap-t / BCa) y toca cifras que la auditoría no cuestionó: se
decide y se ejecuta con su propia pre-declaración, no sobre la marcha.

## Cómo reproducir

```bash
cd spike && python incertidumbre.py          # conciliación 16/16 desde crudos
python generar_benchmark.py --check          # tabla, panel, datos y linaje al día
```
