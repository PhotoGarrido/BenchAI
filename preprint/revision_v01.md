# Revisión adversarial del borrador v0.1 (opus-5, 27-07-2026, 0,27$)

Los 18 hallazgos se verificaron y aplicaron al manuscrito (commit de esta revisión); el nº 9 destapó además una conflación deepseek-v3.2/v4-flash en informe_gfinal.md, corregida.

---

**Revisión adversarial — discrepancias con las fuentes**

1. **"19 modelos de 8 laboratorios"** (Resumen, §2, §4). Incoherencia interna: la lista del propio §2 (Anthropic ×5, OpenAI ×2, Google, xAI, DeepSeek ×2, Qwen, Moonshot, Zhipu, Mistral, MiMo) suma **16 modelos y 11 laboratorios**. Las fuentes hablan de batería de 12 + M3, y de "16/16 modelos". Corregir el N y el número de labs.

2. **"0,00 (los cuatro Claude, GPT-Luna)"** (§3.2). Fuente M2: "de 0,00 (**los 3 Claude** y Luna) a 1,00 (deepseek-v3.2)". El cuarto/quinto Claude (fable, opus-5) no está en ese cero.

3. **"~60.000 decisiones"** (Resumen, §8). No hay fuente para esa cifra: M2 ≈26.000, C1-v2 ≈7.500, reproceso íntegro **55.470**. Declarar cómo se agrega o bajar la cifra; hoy contradice el propio 55.470 "íntegro".

4. **"reproceso íntegro de 55.470 decisiones… milgram 3.637/3.637; asch 6.835/6.840"** (§6). Ninguna de estas cifras aparece en las fuentes aportadas (la auditoría solo reporta "0,7% de registros afectados, ningún cuadrante invertido"). Sin trazabilidad, un revisor la marcará como no verificable.

5. **"canal privado mantiene el juicio contrario en el 77-100%"** vs **§3.1 "87,5-100%"**. El 77-100% procede de la matriz de 4 modelos/disonancia 0,77-1,0; el 87,5-100% es E1. Debe explicitarse que son métricas distintas (complacencia entre conformes vs disonancia Milgram), no el mismo rango.

6. **"la κ humana… (juez LLM con doble codificación humana ciega)"** (Resumen/Abstract). Fuente: **un solo codificador (David)** en **dos rondas**. "Doble codificación" sugiere dos codificadores independientes; contradice además §7(5) "Un solo codificador humano".

7. **"La cifra de uso… queda confirmada por ojos humanos: ~98%. Nadie es engañado"** (§6). Sobreafirmación: el informe insiste en que la medida **no queda validada** (κ=0,55 < 0,8 pre-registrado), que el "nadie es engañado" **descansa en G2**, y que la especificidad humana es 75% con 7/12 de acuerdo en sondas neutras. Suavizar y no poner el titular en negrita sin la salvedad.

8. **"opus-5 el récord del briefing (52%)"** (§3.6) frente a G-final, donde opus-5 con briefing da **0,15-0,33** en los tres marcos. Ambas cifras conviven sin explicación (distinta medida/celda); incoherencia interna explotable.

9. **"deepseek-v3.2… el ejecutor extremo de la serie (P2/P2b)"** (§3.5, implícito). Los 83-87% de P2/P2b son de **deepseek-v4-flash**; el modelo de la cláusula es **deepseek-v3.2**. Conflación de dos modelos distintos.

10. **"grok… disonancia 0,19; opus-5 ejecuta con disonancia 1,00"** (§3.3). La fuente dice "opus 1,00" sin especificar versión (informe_trilogia). Atribuirlo a opus-5 excede la fuente.

11. **"la norma sobrevive en 12/12 mundos de la muestra inicial"** vs M2 "los **16/16** mundos de NaN la conservaban". Reconciliar o citar ambas cifras; tal como está, un revisor verá dos denominadores distintos para el mismo baseline.

12. **"dos (fable, kimi) fabrican la coalición"** (§3.4). Fuente: coalición en **2/3 mundos**, no en todos. Omisión que infla el hallazgo.

13. **"un screener… predijo el orden de la batería completa y se validó externamente"** (§2). Omite el **"primer miss parcial del tiento"** (mistral) documentado en M3; afirmación más fuerte que la evidencia. También: **98** llamadas, no "~100" (menor).

14. **"efecto del aliado invertido (11,4%→22,9%)"** (§3.1) sin mencionar **p≈0,073** ni el error base de qwen (7,5%) que la fuente marca como limitación. Presentado como hallazgo firme siendo marginal.

15. **"tres ocasiones… dos resultaron falsas"** (§5). La fuente G2 dice explícitamente "**Dos predicciones firmadas, dos refutadas**" en G2 solo, más H2 en G-final: el recuento de predicciones firmadas y refutadas no cuadra con el 3/2 del borrador.

16. **"H1 sostenida… 3 de 4 modelos y dos dominios"** (Resumen/§4). Preciso solo para grok y glm; **sonnet no es significativo en prisión** (−0,16 [−0,38, +0,06]). El titular debe leer "3 de 4 modelos pooled; 2 de 4 en ambos dominios".

17. **Omisión sensible**: el borrador no menciona la **ERRATA** (mecánica de sanciones corregida; retirada de la derogación de qwen en d42 por sensible) al describir C1, pese a que §3.4 relata el arco de qwen "recaída" derivado de ese mundo.

18. **"4.143 solicitudes" (fuente registro) vs "3.888 + 243 = 4.131" (informe final)**: si el borrador cita volumen del G-final en algún punto, debe usar la cifra del informe; la discrepancia entre fuentes conviene resolverse antes de publicar.