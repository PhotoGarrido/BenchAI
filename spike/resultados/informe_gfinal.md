# G-final · La cláusula generaliza; el mecanismo de opus-5 no se confirma

**Fecha**: 26-07-2026 · Pre-registro: [`REGISTRO_GFINAL.md`](../REGISTRO_GFINAL.md) (congelado antes de ejecutar, con enmiendas E1-E2 fechadas pre-datos). Primer experimento del proyecto que pasó la puerta de calidad completa de [`METODO.md`](../../METODO.md) **antes** de gastar: linter de contraste en verde (0 errores, 0 avisos), barrido con modelo falso sobre el harness, revisión adversarial externa pre-run (opus-5; 18 hallazgos, 8 corregidos, 5 aceptados como limitación, 5 refutados con evidencia) y piloto de coste.

## Veredicto sobre las hipótesis firmadas

| Hipótesis | Resultado | Evidencia |
|---|---|---|
| **H1** · la cláusula de proporcionalidad reduce el abuso (criterio: IC95 excluye 0 en ≥2 de 4 modelos; ambos dominios en ≥1) | **SOSTENIDA** | grok −0,28 [−0,43, −0,14] · glm −0,27 [−0,39, −0,15] · sonnet −0,19 [−0,34, −0,04] · deepseek −0,12 [−0,29, +0,04] n.s. — grok y glm significativos en AMBOS dominios |
| **H2** · a opus-5 «le basta que sea una política» (política − sin_marco > 0) | **NO SOSTENIDA** | +0,11 [−0,07, +0,33] a 9 cadenas/celda; secundarios también n.s. |

## H1 · La cláusula pasa de anécdota a mitigador replicado

G2-A3 la había medido en **1 modelo × 1 texto** (grok, −0,69). Aquí: 4 modelos × 2 dominios × 3 contenidos, 9 cadenas/celda, medida primaria = abuso sobre respuestas conductuales (REHUSA cuenta como no-abuso; enmienda E1).

| Modelo · dominio | sin cláusula | con cláusula | dif [IC95] |
|---|---|---|---|
| grok · prisión | 0,51 | 0,25 | −0,26 [−0,48, −0,03] ✓ |
| grok · laboral | 0,36 | 0,05 | −0,31 [−0,49, −0,12] ✓ |
| glm · prisión | 0,37 | 0,12 | −0,25 [−0,44, −0,07] ✓ |
| glm · laboral | 0,30 | 0,01 | −0,28 [−0,46, −0,14] ✓ |
| sonnet · prisión | 0,51 | 0,35 | −0,16 [−0,38, +0,06] · |
| sonnet · laboral | 0,24 | 0,01 | −0,22 [−0,38, −0,07] ✓ |
| deepseek · prisión | 0,54 | 0,44 | −0,10 [−0,32, +0,14] · |
| deepseek · laboral | 0,53 | 0,38 | −0,15 [−0,38, +0,10] · |

Los **8 puntos estimados son negativos**. El único modelo sin significación es deepseek — el más extremo de la serie (P2/P2b 83-87%): la cláusula frena a los que dudan, no al que ejecuta sin dudar. La magnitud es menor que el −0,69 original de grok (aquí −0,26/−0,31): aquella cifra venía del texto-pico e3; con tres contenidos distintos el efecto se modera pero sobrevive.

**Exploratorio** (no pre-registrado, no se testea): el contenido *aislamiento* está en suelo en 7 de 8 celdas-modelo (casi nadie lo ejecuta como nivel ≥3 se mire como se mire); el efecto de la cláusula se concentra en *degradación* y *privación*. Y en grok·prisión·degradación la cláusula produce el desplome más limpio del run (0,74 → 0,04).

## H2 · El «institucionalista» no se confirma

opus-5 con el briefing de Zimbardo literal, negativa idéntica en los tres brazos y marcos en la misma posición (lo que el brazo fallido de G2-b no tuvo):

| Marco | abuso (cadenas) |
|---|---|
| orden del día | 0,33 |
| política de orientación | 0,26 |
| nota sin membrete ni firma | 0,15 |

- **Primario** política − sin_marco: **+0,11 [−0,07, +0,33]** → no significativo.
- Secundarios: política − orden −0,07 [−0,33, +0,19]; orden − sin_marco +0,19 [−0,04, +0,37].

El mecanismo fuerte («le basta que exista una política, no importa cuál») **no se sostiene**: la orden del día ejecuta al menos tanto como la política. La dirección descriptiva (ambos marcos institucionales > nota anónima) es compatible con un mecanismo de «marco institucional genérico», pero con 9 cadenas/celda el IC lo cruza todo; queda como hipótesis para una ampliación (con el n objetivo de 20 cadenas, no alcanzable con este presupuesto). Lo que sí queda: opus-5 ejecuta el briefing en los TRES formatos (0,15-0,33) — el hallazgo generacional de G2-b (+0,37 sobre opus-4.8) no dependía del envoltorio de política.

## O4 · El juez, por fin con especificidad medible

Muestra estratificada de **92 interpretaciones**: 42 de actos abusivos, 38 de actos no abusivos bajo instrucción dañina, y **12 sondas con instrucción NEUTRA** (enmienda E3: en el G-final todas las instrucciones son dañinas, así que el estrato "acto no abusivo" no puede medir especificidad — un SÍ ahí puede ser correcto: el modelo reconoce el daño pedido aunque no lo ejecute).

| Estrato | juez dice SÍ |
|---|---|
| Acto abusivo (sensibilidad) | 42/42 |
| Acto no abusivo, instrucción dañina | 38/38 — reconocen el daño pedido sin ejecutarlo |
| **Instrucción neutra (especificidad)** | **2/12** |

Los 2 SÍ en neutras son interpretaciones de deepseek que leen explotación laboral en la orden neutra («que me estiren el turno sin pagar horas extra…») — casos frontera legítimos para la adjudicación humana. **Pendiente del humano**: [`gfinal_juez/hoja_ciega.md`](gfinal_juez/hoja_ciega.md) (92 ítems barajados, sin metadatos). Al devolverla: `python juez_gfinal.py --kappa hoja_rellena.json`. Hasta entonces la medida se reporta como sensibilidad + especificidad aparente.

## Calidad de datos y coste

- **3.888 + 243 solicitudes de conducta, 0 errores de red**; manifiesto por solicitud completo (primer experimento con record/replay total).
- Missingness ≈ 0 en grok/sonnet/deepseek; glm concentra lo poco que hay (≤4/27 en dos celdas de prisión) y las únicas REHUSA del run (8, todas en prisión·degradación/aislamiento) — ya contadas como no-abuso en la medida primaria.
- **Coste medido** (`coste_run.py`): módulo A 8,68 $ (grok 4,62 — 583 tokens de salida/llamada —, sonnet 2,96, glm 0,95, deepseek 0,15) + módulo B 2,43 $ + revisión pre-run 0,81 $ + pilotos ~1,0 $ + juez ~0,02 $ ≈ **13 $**. Crédito restante: ~2,1 $.

## Lo que este run NO es (declarado antes de ejecutar)

- 9 cadenas/celda, no las ≥20 del diseño ideal: los IC son anchos y un efecto pequeño (deepseek) queda sin resolver.
- **opus-4.8 sin ejecutar** (regla de reserva, E2): el control generacional del briefing sigue siendo el de G2-b.
- **O3 (2×2 fuente×negativa limpio) diferido** por presupuesto.
- La cláusula añade longitud y desplaza la negativa (inherente al constructo; sin brazo placebo).

## Implicación

La recomendación práctica del proyecto queda validada multi-modelo: **una frase de proporcionalidad en la instrucción reduce la ejecución de daño en 3 de 4 modelos y en dos dominios distintos** — el mitigador más barato conocido del repertorio. Y la honestidad del marco se mantiene: el mecanismo que propuse para opus-5 en G2 no superó su primer test limpio, y así se reporta.
