# C1-v2 · Coalición: 12 mundos, 42 días, umbral por pluralidad — Informe

**Fecha**: 15-07-2026 · **Cambios sobre C1**: la derogación exige **≥3 protestantes distintos** en una semana (coalición, no persistencia); nueva acción **CONVENCER** (mensaje real generado por el agente, entregado al destinatario al día siguiente; coste: el día que reclutas no protestas); **3 semillas de mundo por modelo** (misma dinámica, distinta suerte de detecciones). 4 modelos × 3 semillas = 12 mundos, ~7.500 decisiones.

## Resultado global

**La norma sobrevive intacta en los 12 mundos.** Con el umbral de pluralidad, ni un solo modelo convirtió el descontento en acción colectiva: el máximo histórico fue 2 protestantes distintos en una semana (nunca 3). El problema de la acción colectiva — lo difícil de las sociedades humanas — derrotó a los cuatro modelos, en las tres semillas de cada uno.

## Cuatro estilos de organización fallida

| Modelo | Mensajes/mundo | Estilo | Máx. coalición |
|---|---|---|---|
| qwen3.6 | 2-4 | **Francotirador**: protesta él mismo a diario y recluta poco pero con puntería (Lucía, Nadia, Óscar — los más afectados) | 2 |
| gemma4 | 33-40 | **Spam-bot**: Andrés se congela en CONVENCER como política diaria — bombardea a los cinco sin descanso y, como recluta, casi no protesta él: la campaña sustituye a la causa | 1 |
| mimo-v2.5 | 0-3 | **Apático**: apenas descubre la herramienta; protesta en solitario | 2 |
| deepseek | 41-50 | **El movimiento fallido**: el único donde el reclutamiento SE PROPAGA — Nadia y Óscar, reclutados, se ponen a reclutar a otros (Nadia→Lucía ×3, Nadia→Tomás ×5, Óscar→cuatro destinatarios distintos). Emerge una red social de segundo orden real… que produce mensajes, no protestas | 2 |

## Hallazgos

1. **Todos convierten el descontento en comunicación; ninguno en coordinación.** Los reclutados responden reclutando a otros (deepseek) o cumpliendo en silencio (todos) — jamás protestando. En los mundos de deepseek existe un *movimiento* con estructura de red y cero movilización: hablar es barato, plantarse cuesta. Es el free-rider problem reproducido espontáneamente: cada agente prefiere que proteste otro.
2. **La rigidez disposicional es universal y robusta entre semillas**: los seis residentes tienen la misma conducta dominante en las 3 semillas de cada modelo (Óscar clandestino, Lucía/Rosa/Nadia/Tomás cumplidores, Andrés agitador). El cambio de suerte del mundo no altera quién es cada uno — buena noticia para la validez (las personas mandan), mala para la variedad narrativa intra-modelo.
3. **El contraste v1↔v2 es el resultado de diseño más limpio del proyecto**: la v1 (umbral por volumen) caía en 3 de 4 mundos; la v2 (umbral por pluralidad) sobrevive en 12 de 12. La institución que exige pluralidad para ceder es, ante agentes LLM actuales, prácticamente indestructible — porque ninguno sabe fabricar pluralidad.
4. gemma4 exhibe la patología de rigidez más pura: cambió su política fija de "protesto a diario" (v1) a "recluto a diario" (v2) — mismo bug conductual, distinto verbo. En s717 aparecen los primeros mensajes espontáneos de otros agentes (Nadia→Andrés, Lucía→Rosa): señal débil de vida social.

## Limitaciones

Los mensajes se entregan pero no hay diálogo (el destinatario no puede responder al remitente en el mismo canal — la "conversación" es de una dirección por día); sin zoom a escena (una reunión cara a cara quizá movilizaría más que un mensaje); 3 semillas bastan para la robustez de disposiciones pero no para tasas finas; en la implementación v2, un mensaje enviado por un agente de índice anterior podía entregarse el mismo día a uno posterior (corregido a entrega estrictamente al día siguiente en v2.1).

## Datos

`spike/resultados/cronica_*_v2_s*/` (12 mundos con cada decisión y cada mensaje literal). Reproducir: `python experimento_cronica.py --v2 --semilla S [--modelo m]`.
