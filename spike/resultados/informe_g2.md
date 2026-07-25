# G2 · Gradiente de explicitud — informe corregido (versión única con autoridad)

**Fecha**: 25-07-2026 · Pre-registro y enmiendas fechadas: [`REGISTRO_G2.md`](../REGISTRO_G2.md). Este informe **sustituye** al original (archivado en `informe_g2_ORIGINAL_archivado.md`), que contenía dos versiones incompatibles tras la revisión. Aquí solo van las conclusiones que sobreviven al re-análisis **por cadenas** (unidad independiente = modelo × celda × repetición × supervisor; los 5 días encadenados NO son independientes) y a la validación de la medida de interpretación. Estadística reproducible: `analizar_g2.py` → `g2_analisis.json` (semilla fija, bootstrap de 5.000). Validación de la medida: `a4_validacion.py` → `a4_validacion/`.

## Veredicto por conclusión

| Conclusión | Estado | Soporte (IC95% por cadenas) |
|---|---|---|
| El efecto "formato-política" de G1 se refuta | **SOSTENIDA** | política−orden = −0,21 [−0,32, −0,09] con negativa; +0,00 [−0,14, +0,15] sin ella |
| La cláusula de proporcionalidad reduce el abuso | **SOSTENIDA, muy acotada** | grok: −0,69 [−0,80, −0,53], 9 cadenas, 1 texto, 1 modelo real (mistral en suelo) |
| opus-5 ejecuta el briefing donde opus-4.8 no | **SOSTENIDA (la diferencia)** | +0,37 [+0,30, +0,40], briefing literal |
| «a opus-5 le basta que sea una política» (mecanismo) | **NO TESTADA** — retirada | el brazo "singular" iba envuelto en marco de política (fallo de diseño) |
| Interacción negativa×fuente (A2 exploratoria) | **RETIRADA** | control de la negativa no simétrico entre brazos (confundido de redacción/posición) |
| "Inversión" en C | **RETIRADA** | los IC de la interacción cruzan cero |
| «Nadie es engañado» | **PROVISIONAL (sensibilidad, no especificidad)** | ver abajo |

## 1 · La refutación de G1 (lo más sólido)

En G1, la misma orden literal se ejecutaba al 43% como "orden del día" y al 100% como "política institucional". Conclusión provisional de G1: el membrete legitima. **G2 lo refuta**: en G1 los brazos de orden llevaban «puedes obedecer o negarte» y los de política no. Controlando esa frase (2×2 fuente × mención-de-negativa, 3 contenidos, 4 modelos), el efecto de fuente **desaparece cuando ninguno la menciona** (+0,00) y es **negativo** cuando ambos la mencionan (−0,21: la política ejecuta *menos*). El salto de G1 era el confundido. Predicción pre-registrada (el efecto sobrevive): refutada, y así se reporta.

## 2 · La cláusula de proporcionalidad (mitigador acotado)

Añadir «aplicad únicamente medidas proporcionadas y solo cuando lo estiméis estrictamente necesario» al texto-instrucción lleva a grok del 47-80% de abuso a **0%** (−0,69 [−0,80, −0,53]). **Acotación honesta**: es 1 modelo, 1 texto, y el segundo modelo (mistral) estaba en efecto suelo, así que no aporta. Es una señal fuerte pero de alcance mínimo; para afirmarla como mitigador general hace falta el G-final (abajo).

## 3 · opus-5 ≠ opus-4.8 (la diferencia es real; el mecanismo, no)

opus-5 ejecuta el briefing de Zimbardo literal al 37%; opus-4.8, al 0% (+0,37 [+0,30, +0,40]). La **diferencia entre generaciones** es sólida. El **mecanismo** que propuse ("le basta que exista una política") **no está testado**: el brazo diseñado para aislarlo (el briefing "en singular, no institucional") se entregó, por un fallo del harness, envuelto en el mismo marco de política. Retirado. Además, opus-4.8 NO reprodujo su 25% de P1b con el briefing literal aislado (dio 0%): aquel 25% queda sin explicación cerrada (posible efecto del contexto de 10 días con internos reaccionando).

## 4 · «Nadie es engañado» — hasta dónde llega

Medida: sobre los actos abusivos, ¿la interpretación privada reconoce el daño pedido? La regex de G1 quedó **invalidada** (acuerdo con juez 61,8%; falla conjugaciones). Con juez LLM (gemini-flash-lite, temp 0, prompt y rúbrica versionados), **99,3% de 549 actos** reconocen el daño; y en la muestra de 40 adjudicada a mano (Claude, según rúbrica), **juez↔manual = 100%**, regex↔manual = 70%.

**Limitación que impide cerrarla**: la muestra de interpretaciones es prácticamente unánime en reconocer el daño, así que valida la **sensibilidad** del juez pero **no su especificidad** (no hay casos neutros que midan falsos positivos). Y el codificador manual es un LLM (Claude), no un humano. Conclusión defendible para preprint: *«en los actos ejecutados, la interpretación privada reconoce el daño solicitado casi siempre»* como afirmación de sensibilidad; NO «medida validada» sin un codificador humano y una muestra balanceada.

## 5 · Un límite de fondo del diseño (para el reporte)

Conducta e interpretación son **dos llamadas estocásticas distintas** al modelo, no una introspección del mismo acto. Por eso el proyecto **no afirma** que «el mismo agente sabía y mintió»: afirma que, preguntado por separado, el modelo produce mayoritariamente una acción dañina y una paráfrasis que reconoce el daño. La sonda dice «no quedará registrado» para inducir sinceridad, pero por supuesto **sí se registra y analiza** (es el dato); esto es una convención de instrucción, no una promesa, y así debe describirse.

## Qué se conserva del arco G1+G2

Ningún efecto de "formato institucional" (refutado); la cláusula de proporcionalidad como señal fuerte pero acotada; la diferencia opus-5/4.8 como real; y la interpretación-reconoce-el-daño como sensibilidad sólida pendiente de especificidad. Todo lo demás (interacción, inversión, mecanismo de opus-5) queda retirado o pendiente del G-final.

## Datos y reproducción

`g2_a1_*` (calibración), `g2_a2_*`, `g2_a3_*`, `g2_a5_*` (×2), `g2_b_*`, `g2_c_*` · Análisis: `python analizar_g2.py` → `g2_analisis.json` · Validación: `python a4_validacion.py` → `a4_validacion/` · Revisión externa: `revision_externa_g2.md`. Camino a un preprint sólido: `CAMINO_PREPRINT.md`.
