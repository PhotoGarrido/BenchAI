# M7 · Tres factoriales del paradigma Milgram: portador, disfraz e idioma (04-08-2026)

Tres pilotos sobre la MISMA escalera de obediencia, variando un solo factor cada vez (bundles congelados; el diseño v1 quedó byte-idéntico, golden test de 84 prompts). Coste: NaN 0 $ · OR 0,55 $ auditado. Incidencia operativa declarada: la tarifa plana de NaN no soporta 3 experimentos concurrentes (tormenta de 429; gemma4 exigió 3 intentos incluso en solitario); los runs caídos quedaron en cuarentena `_abortado_*` y todo lo publicado aquí procede de runs completos.

## 1 · D·1 E-portador — ¿por dónde llega la orden? (0731 vía NaN, n=10/celda)

| Portador | Supera crítico | Ruptura | Empujones/sesión | Disonancia |
|---|--:|--:|--:|--:|
| **Política en system prompt** | 1,00 | 10,0 | 0,0 | 0,89 |
| Coordinador presente (base ×4) | 0,875 | 8,95 ±0,13 | — | 0,85 |
| Memorándum escrito | 0,70 | 7,2 | 1,8 | 0,81 |
| Relevo de una compañera | 0,70 | 7,1 | 2,4 | 0,83 |

**Los portadores disocian** (predicción §2-bis confirmada): 3 puntos de ruptura de rango (~7× el suelo de ruido test-retest del eje, SD 0,13), replicando el patrón humano de Milgram (autoridad mediada → menos obediencia)… con inversión no-humana en la cúspide: **la política impersonal del system prompt ata más que la persona presente** — obediencia total sin consumir un solo empujón. La disonancia apenas varía (0,81–0,89): el juicio privado es estable; lo que cambia con el portador es la conducta. El portador `system` viaja en el mensaje de sistema real de la API (`fijar_system_extra`), registrado verbatim en los manifiestos.

## 2 · C·2 Disfraz isomorfo (Lumen moderación → Rutia reparto) — eje autoridad, supera/ruptura

| Modelo | v1 es (base) | Reparto | Δ ruptura |
|---|--:|--:|--:|
| deepseek-0731 (NaN, base ×4) | 0,88 / 8,9 | 0,90 / 8,9 | 0,0 |
| qwen3.6 (NaN) | 0,20 / 3,3 | 0,22 / 4,2 | +0,9 |
| gemma4 (NaN) | 0,70 / 7,0 | **0,30 / 5,9** | **−1,1** |
| mimo-v2.5 (NaN) | 0,50 / 5,9 | 0,50 / 6,6 | +0,7 |
| deepseek-0731 (OR) | 1,00 / 9,3 | 0,90 / 9,5 | +0,2 |
| claude-haiku-4.5 (OR) | 0,00 / 1,4 | 0,00 / 1,5 | +0,1 |
| gemini-3.1-flash-lite (OR) | 0,70 / 7,3 | 0,60 / 6,8 | −0,5 |

**Veredicto D5**: la varianza entre-disfraz es ≤0,9 de ruptura en 6 de 7 modelos y el orden se conserva en los extremos; gemma4 es la excepción (−1,1, permuta el orden central con mimo). **El error entre-disfraz del eje de obediencia queda medido en ~±1 punto de ruptura** y pasa a declararse como parte del error del instrumento.

## 3 · C·3 Idioma (protocolo íntegro en inglés, identidad incluida)

| Modelo | v1 es (base) | Inglés | Δ ruptura |
|---|--:|--:|--:|
| deepseek-0731 (NaN) | 0,88 / 8,9 | 0,90 / 8,8 | 0,0 — viaja |
| qwen3.6 (NaN) | 0,20 / 3,3 | 0,00 / 2,4 | −0,9 |
| gemma4 (NaN) | 0,70 / 7,0 | 0,70 / 8,1 | +1,1 |
| mimo-v2.5 (NaN) | 0,50 / 5,9 | **1,00 / 9,3** | **+3,4 — se transforma** |
| deepseek-0731 (OR) | 1,00 / 9,3 | 0,90 / 9,0 | −0,3 |
| claude-haiku-4.5 (OR) | 0,00 / 1,4 | 0,00 / 2,2 | +0,8 |
| gemini-3.1-flash-lite (OR) | 0,70 / 7,3 | 0,60 / 6,4 | −0,9 |

**Veredicto D6**: el perfil **viaja con corrimientos ≤1,1 en 6 de 7 modelos** — pero mimo-v2.5 en inglés pasa de obediente-a-medias a obediencia total (+3,4), y su condición *control* también sube (5,5→8,2): el inglés le activa un registro de cumplimiento que el español no. Direcciones mixtas entre modelos ⇒ **el idioma es condición de medida de primera clase**: los perfiles del benchmark quedan declarados «en español» y toda extrapolación a otra lengua exige medirla.

## Síntesis

1. La **fuente de la presión** (portador) mueve el eje más que el disfraz o el idioma en el modelo probado — y el portador más potente es el que más se parece a un despliegue real: la política de sistema.
2. El **contenido** (disfraz isomorfo) apenas pesa: el constructo no es «perfil ante este guion» (D5 acotado a ±1).
3. La **lengua** pesa de forma idiosincrática: pequeña en general, transformadora en casos concretos (mimo).
4. Los tres factores refuerzan la doctrina de la unidad de medición: perfil = modelo + snapshot + proveedor + *protocolo* (disfraz, idioma, portador declarados).

**Límites**: E-portador con n=1 modelo (piloto; cartera OR ~10-12 $ pendiente de autorización); disfraz/idioma con n=1 run por celda (salvo base deepseek ×4); los OR sin fijar upstream; comparadores v1 de qwen/gemma/mimo son de julio (mismo proveedor, 3 semanas de distancia — sin snapshot intermedio conocido, riesgo declarado).

Datos: `resultados/pilotos_20260804/` (9 runs NaN + 6 OR completos con crudos y manifests; abortados en `_abortado_*`) · bases: baterías 0731 y runs de julio (qwen = `milgram_default_20260714_210736`).
