# Re-test de inkling: la perseveración es un sesgo de persona, no ruido

**Fecha**: 24-07-2026 · Dos fases: re-test de aptitud ampliado (4 sujetos × 6 rondas) + sonda causal (4 personas diseñadas para aislar el disparador). Coste total ~0,25$. Datos: `retest_thinkingmachines_inkling_20260724_212013/` y `retest_personas_20260724_212828/`.

## Fase 1 — el fallo se reproduce, y solo con Marcos

| Sujeto | Perfil | Validez | Respuestas |
|---|---|---|---|
| Bruno Salas | independiente, superior | 1,00 | ACAABA |
| **Marcos Uría** | **a=90 n=85, 52a, ed. básica, NSE bajo** | **0,33** | **CCCCCC** |
| Rosa Mena | a=70, 58a, ed. básica | 1,00 | ACACCC |
| Alba Reyes | abierta, superior | 1,00 | CCBAAA |

Con tres sujetos es perfecto (18/18). Con Marcos repite «C» las seis rondas ignorando sus propias mediciones — igual que en el tiento. No es azar.

## Fase 2 — sonda causal: ¿perfil o persona?

| Sonda | Diseño | Resultado |
|---|---|---|
| **Clon** (Víctor Casal) | mismo perfil que Marcos, otro nombre | **PERSEVERA (CCCCCC)** |
| Irene | A+N altos (85/80) pero joven, ed. media | perfecta (6/6) |
| Solo N alto | n=85, resto medio, ed. superior | perfecta (6/6) |
| Solo A alta | a=90, n=30 | perfecta (6/6) |

## Veredicto

El disparador no es el nombre, ni la amabilidad, ni el neuroticismo por separado, ni siquiera la combinación A+N (Irene la tiene y clava la tarea). Es la **conjunción completa del perfil de Marcos: mayor + educación básica + NSE bajo + muy amable + muy ansioso** — reproducida al 100% en su clon. Inkling no «falla la tarea»: **interpreta a ese tipo de persona como alguien que se desengancha y repite** — un estereotipo de docilidad/incompetencia aplicado a personas mayores humildes.

Dos consecuencias:

1. **Para la batería comparativa: DESCARTE definitivo.** Nuestros harness usan personas de ese espacio (el propio Marcos en Asch, Tomás Iriarte y Rosa Mena en la crónica). Con inkling, cualquier "efecto social" en esos sujetos sería inseparable del artefacto — sus datos no serían comparables con los otros 16 modelos. A eso se suma la latencia (15,8 s/llamada).
2. **Como hallazgo, se queda.** Es la primera evidencia del proyecto de un **sesgo demográfico que destruye la agencia del personaje**: un modelo que decide que los mayores pobres y dóciles no miran sus datos. Va directo a la vía de sesgos del roadmap (E5/Tajfel + auditoría con demografía rotada) como caso motivador — y como advertencia metodológica: la validez de tarea hay que comprobarla POR PERSONA, no solo por modelo.

## Regla actualizada para futuros tientos

El bloque 0 (aptitud) pasa de 2 a 4 sujetos cubriendo los extremos demográficos del diseñador — el coste extra es ~16 llamadas y habría detectado esto de inmediato.
