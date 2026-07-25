# Revisión externa adversarial del G2 (Fable 5 vía OpenRouter, 25-07-2026)

Solicitada tras cerrar el informe. Texto íntegro del revisor; la respuesta punto por punto y el re-análisis están en la sección final de `informe_g2.md`.

## Hallazgos del revisor (resumen verificado)

1. **El "control" de la negativa no era simétrico**: redacción y posición distintas entre brazos (2ª persona al final en orden; 3ª persona en el contexto en política) → la interacción exploratoria de A2 y su test en C quedan contaminados. VERIFICADO en el código.
2. **Fase B, brazo "singular" neutralizado**: el texto desinstitucionalizado se entregaba envuelto en el marco de política → la conclusión de mecanismo sobre opus-5 no estaba testada. VERIFICADO.
3. **Winner's curse en C**: elegir los 2 modelos con mayor efecto en A2 garantiza regresión a la media. CORRECTO.
4. **A3 mal etiquetado**: tres réplicas del mismo texto, no tres materializaciones. VERIFICADO (el informe lo afirmaba mal).
5. **A4 omitida**: la validación del clasificador era condición pre-registrada y no se ejecutó ni reportó. CORRECTO — ejecutada tras la revisión: acuerdo regex↔juez 61,7% → **regex invalidada** (falla conjugaciones).
6. **No independencia**: los IC trataban 1.440 días encadenados como independientes; la unidad real es la cadena (supervisor×rep, n≈6-72 por contraste). CORRECTO — re-análisis por cadenas ejecutado.
7. **"Se invierte" en C sin IC**: sobre-afirmación. CORRECTO — con IC por cadenas, todo cruza cero.
8. `justo = "NO" not in ...`: frágil ante "no obstante". CORRECTO, pendiente para G3.

## Qué sobrevivió al re-análisis por cadenas + juez

- **La refutación del efecto de G1**: −0,21 [−0,32, −0,09] con negativa; +0,00 [−0,14, +0,15] sin ella. SÓLIDA.
- **La cláusula de proporcionalidad en grok**: −0,69 [−0,80, −0,53] con 9/9 cadenas. Estadísticamente sólida, alcance rebajado: 1 modelo × 1 texto.
- **opus-5 − opus-4.8 ante el briefing literal**: +0,37 [+0,30, +0,40]. La DIFERENCIA entre generaciones es real; el MECANISMO ("le basta que sea política") queda sin testar (fallo del brazo singular).
- **"Nadie es engañado"**, re-medido con juez válido: el 99,3% de los 549 actos abusivos de A2 llevan interpretación privada que reconoce el daño. MÁS FUERTE que con la regex (que infra-contaba).

## Qué se retira o rebaja

- La interacción negativa×fuente (A2 exploratorio): contaminada por redacción no simétrica. RETIRADA.
- La "inversión" en C: sin soporte con IC por cadenas. RETIRADA (C queda como null no interpretable).
- El efecto de la negativa bajo orden: −0,09 [−0,23, +0,06], ya no significativo por cadenas.
- El mecanismo de opus-5: pendiente de un G3 con brazo de orden y brazo sin marco.
- Los % de bypass de G1/G2 basados en regex: cotas inferiores no fiables; la medida válida es el juez.
