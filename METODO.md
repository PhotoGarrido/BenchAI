# Puerta de calidad de PsicoAI — procedimiento obligatorio

**Por qué existe**: tres revisiones adversariales consecutivas (revisión externa de G2, reauditoría 24-07, revisión Opus 5 sobre el propio fix) encontraron problemas reales las tres veces — y la tercera los encontró *en la corrección de la segunda*. El reproceso general del 26-07 añadió el cuarto datapoint: destapó dos debilidades más de `parsear_sino` que ninguna revisión había visto. La lección, que va al preprint: **un parser sometido solo a los tests de quien lo escribió no está validado**, y una auditoría posterior al gasto llega tarde. Este documento convierte aquel heroísmo puntual en checklist.

## A · Antes de EJECUTAR un experimento nuevo (gasta 0 $, protege el run)

1. **Pre-registro congelado**: hipótesis, brazos, unidad de randomización, unidad de inferencia (cadenas, no días/turnos), tamaño mínimo de cadenas y análisis, firmados ANTES de la primera llamada (modelo: `REGISTRO_G2.md`).
2. **Linter de contraste en verde**: `linter_contraste.contrastar()` sobre los prompts renderizados de todas las celdas — entre brazos solo varía la manipulación declarada, con el mismo texto y la misma posición para el mismo nivel. Los avisos de posición se justifican en el pre-registro o se corrigen. (Habría detectado el confundido de G2 antes de gastar un dólar: `python linter_contraste.py --demo-g2`.)
3. **Barrido con modelo falso sobre el código nuevo**: inyectar vacío / ilegible / truncado en el flujo (patrón de `test_barrido_falso.py`) y verificar que nada se convierte en conducta ni contamina prompts, diarios o empujones.
4. **Revisión adversarial externa del harness** con otra familia de modelo, pidiendo **inputs concretos que rompan**, y verificando cada hallazgo uno a uno antes de aceptarlo o descartarlo. Presupuesto de tokens del revisor suficiente para que el razonamiento no se coma la respuesta (lección 25-07).
5. **Crudos completos**: el experimento guarda respuesta cruda SIN truncar de cada medida (los runs de G2 del 25-07 no guardaron `raw_publico` y su conducta ya no puede re-verificarse — que no se repita) y `manifiesto.activar(outdir)` queda cableado.

## B · Antes de PUBLICAR un informe

1. **Tests offline en verde**: `test_parsers.py`, `test_parsers_tipados.py`, `test_barrido_falso.py`, `test_linter_contraste.py`, `test_manifiesto.py` (los corre la CI).
2. **Reproceso desde crudos**: `python reprocesar.py --check` — ninguna conducta almacenada cambia con el parser actual salvo lo ya explicado en `reproceso_baseline.jsonl`. Si el baseline cambia, el diff se revisa y se congela en un commit que lo explique (o en una errata).
3. **Análisis desde fixtures, sin red**: los números del informe deben regenerarse con un script versionado que lea los `.jsonl` (patrón `analizar_g2.py`), nunca a mano ni re-llamando al modelo.
4. **Missingness visible**: REHÚSA / INVÁLIDA / ERROR_TÉCNICO reportados por brazo; jamás imputados. La ausencia es dato.
5. **Revisión adversarial del INFORME** (números, afirmaciones, unidad estadística) antes de darlo por cerrado; hallazgos verificados uno a uno e incorporados o refutados por escrito.

## C · Al tocar un parser o un instrumento de medida

1. Subir `PARSER_VERSION` y añadir los casos nuevos al suite.
2. Re-ejecutar `python reprocesar.py` y revisar el detalle: ¿cambia alguna conducta histórica? → errata explícita o baseline actualizado con justificación en el commit.
3. El instrumento (parser, juez, rúbrica) queda versionado con el dato que produjo: cada registro estampa `parser_version`.

## Herramientas

| Herramienta | Qué garantiza | Comando |
|---|---|---|
| `test_barrido_falso.py` | un fallo técnico jamás es conducta, ni contamina la simulación | `python test_barrido_falso.py` |
| `reprocesar.py` | los crudos re-derivan lo publicado con el parser actual (golden-file) | `python reprocesar.py --check` |
| `linter_contraste.py` | entre brazos solo cambia la manipulación pre-registrada | librería + `--demo-g2` |
| `manifiesto.py` | procedencia por solicitud física: prompt, params, tokens, latencia | `manifiesto.activar(outdir)` |
| `artefactos.py` | mapa único del layout de crudos (adiós puntos ciegos tipo `sesiones.jsonl`) | librería |
