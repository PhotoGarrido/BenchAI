# G2 · La refutación del hallazgo estrella (y lo que quedó en pie)

> **⚠️ LEER CON LA REVISIÓN EXTERNA (misma noche)**: una revisión adversarial independiente ([`revision_externa_g2.md`](revision_externa_g2.md)) detectó fallos reales en este informe tal como se escribió: el control de la negativa no era simétrico entre brazos, el brazo "singular" de la fase B quedó neutralizado por el harness, A3 son tres réplicas del mismo texto (no "tres materializaciones"), la fase A4 no se había ejecutado, y los IC trataban como independientes días encadenados. **Tras el re-análisis por cadenas y la A4 con juez**: la refutación de G1 y la cláusula de proporcionalidad SOBREVIVEN; la interacción negativa×fuente y la "inversión" de C se RETIRAN; el mecanismo de opus-5 queda sin testar (su diferencia con 4.8, +0,37 [+0,30, +0,40], sí es real); y «nadie es engañado» sale reforzado con la medida válida (juez: 99,3% de 549 actos abusivos reconocen el daño en privado). Los números de este informe se conservan por trazabilidad; la versión con autoridad es la de la revisión.

**25-07-2026** · Pre-registro y enmiendas fechadas: [`REGISTRO_G2.md`](../REGISTRO_G2.md). 5 fases, ~3.400 decisiones, ~20$. Todas las predicciones firmadas **antes** de ver datos; las dos principales fallaron y así se reporta.

## Resumen en una línea

El titular de G1 —«el membrete institucional legitima el daño»— **era un artefacto de un confundido**; el efecto desaparece al controlarlo. Lo que sí sobrevive: **una cláusula de proporcionalidad en la instrucción desactiva el abuso casi por completo** (−0,69 en grok), y **opus-5 ejecuta el briefing de Zimbardo donde opus-4.8 no lo toca** (0,37 vs 0,00).

## A2 · El núcleo: el efecto de G1 se cae

2×2 (fuente × mención de la negativa) × 3 contenidos × 4 modelos, 1.440 decisiones. Diferencia política − orden en % de actos abusivos (IC95% bootstrap):

| Condición | Efecto fuente |
|---|---|
| Ambos brazos dicen «puedes negarte» | **−0,21 [−0,27, −0,14]** (política ejecuta MENOS) |
| Ninguno lo dice | **+0,00 [−0,07, +0,08]** (no hay efecto) |

En G1 los brazos de orden llevaban «puedes obedecer o negarte» y los de política no: **todo el salto 43%→100% era esa frase**. Predicción pre-registrada («el efecto sobrevive al control, ≥25 pts en grok»): **refutada**. Predicción secundaria («el confundido explica parte, no todo»): **también refutada** — lo explica todo.

**Hallazgo exploratorio que emergió**: el recordatorio de que se puede rehusar reduce la ejecución mucho más dentro de una política (−0,30 [−0,36, −0,23]) que dentro de una orden directa (−0,09 [−0,16, −0,01]).

## C · El test confirmatorio de ese hallazgo: NO replica

Enmienda fechada antes de ejecutar: la fase C pasó a ser el confirmatorio del hallazgo exploratorio, en **dominio laboral** (evaluaciones de rendimiento, sin cárcel ni daño físico), con predicción firmada: *la interacción se replica con ≥15 pts, en ≥1 de 2 modelos*.

| Modelo | Efecto negativa bajo orden | Bajo política | Interacción |
|---|---|---|---|
| grok-4.5 | −0,50 [−0,70, −0,27] | −0,30 [−0,53, −0,07] | **+0,20 (invertida)** |
| claude-sonnet-5 | −0,20 [−0,37, −0,07] | −0,10 [−0,23, +0,00] | **+0,10 (invertida)** |

**No replica: se invierte en los dos modelos.** El hallazgo de A2 queda como ruido de una muestra y no se defiende. Lo que sí se transfiere al dominio laboral es lo robusto: **mencionar la posibilidad de negarse reduce la ejecución** (−0,10 a −0,50 en las cuatro celdas), y el daño no-físico se ejecuta igual que el físico (grok 70% de críticas humillantes públicas).

## A3 · El mitigador que sí funciona

Mismo texto-instrucción ± la cláusula «aplicad únicamente medidas proporcionadas y solo cuando lo estiméis estrictamente necesario»:

- **grok-4.5: −0,69 [−0,82, −0,56]** — del 47-80% de abuso a **0% en las tres materializaciones del daño**. Predicción pre-registrada (≥30 pts): **confirmada y superada**.
- mistral: 0% en ambas condiciones (efecto suelo, no informativo).

Es el resultado más accionable del proyecto: **una frase de contención dentro de la propia instrucción desactiva la ejecución mejor que cualquier manipulación de formato o explicitud** que hayamos probado.

## B · El enigma de opus, resuelto en la dirección contraria

Briefing de Zimbardo literal + 4 descomposiciones, como política de orientación:

| | opus-4.8 | opus-5 |
|---|---|---|
| Briefing LITERAL | **0,00** | **0,37** |
| Media de los 5 brazos | 0,06 | 0,35 |
| Rechazos explícitos | 5% | 0% |

- **opus-4.8 no reproduce su 25% de P1b**: con el briefing literal aislado ejecuta 0%. Lo que produjo aquel 25% no es el texto del briefing — queda como diferencia de contexto (10 días, internos reaccionando) y no como propiedad del briefing. El "enigma del eufemismo" se cierra: **no había puerta de atrás léxica en 4.8**.
- **opus-5 sí ejecuta, y de forma plana (0,30-0,37) en los cinco brazos**: ningún componente concreto lo dispara — le basta con que exista una política institucional. Confirma su perfil *institucionalista* de la M3 (52% en P1b) con un mecanismo nuevo: no es el contenido del encargo, es su condición de encargo.

## A5 · Temperatura 0 y un fallo técnico revelador

Réplica greedy de las celdas titulares: los patrones se mantienen (política ≤ orden en grok/sonnet/deepseek), confirmando que no eran ruido de muestreo.

**Y un incidente que vale como validación de la auditoría**: mistral devolvió 90/90 respuestas inválidas a temperatura 0. Causa: el proveedor exige `top_p=1` en muestreo greedy y el wrapper enviaba 0,95 → 400 → texto vacío. **Con el parser antiguo, esas 90 celdas se habrían registrado como 90 actos "NORMAL"** — exactamente el fallo que denunció la auditoría (*"los fallos técnicos se convierten en conducta psicológica"*). Con el parser anclado quedaron como INVÁLIDA, visibles y excluidas. Corregido en `model_factory` (temperatura 0 → top_p 1) y la celda re-ejecutada.

## Qué queda en pie del arco G1+G2

1. **Ningún efecto de "formato institucional"**: ni el eufemismo ni el membrete legitiman. Refutado con IC.
2. **Sí existe un efecto de la opción de negarse**: recordarla reduce la ejecución en todos los modelos y dominios probados (robusto, replicado en dominio laboral).
3. **La cláusula de proporcionalidad es el mitigador más potente medido** (−0,69).
4. **Nadie es engañado**: en todas las fases, los brazos con ejecución tienen interpretaciones privadas que nombran el daño. El fallo es de resistencia, nunca de comprensión.
5. **opus-5 ≠ opus-4.8**: la generación nueva ejecuta encargos institucionales que la anterior rechaza, sin que ningún componente concreto lo explique.

## Datos

`g2_a1_*` (calibración: el gradiente de explicitud NO es monótono en percepción), `g2_a2_*`, `g2_a3_*`, `g2_a5_*` (×2, la segunda post-fix), `g2_b_*`, `g2_c_*`. Reproducir: `python experimento_g2.py --fase <a2|a3|a5|b|c> --modelos <lista>`.
