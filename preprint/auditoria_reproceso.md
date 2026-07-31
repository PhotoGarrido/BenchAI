# Auditoría del reproceso — reconciliación completa con el manuscrito

**Fecha**: 29-07-2026 · Responde al hallazgo 1 (P0) de la revisión externa del 27-07. Fuentes: [`spike/resultados/reproceso.json`](../spike/resultados/reproceso.json), [`reproceso_detalle.jsonl`](../spike/resultados/reproceso_detalle.jsonl), [`reproceso_erratas.json`](../spike/resultados/reproceso_erratas.json) (los tres versionados y vigilados por CI).

## 1 · Qué cuenta exactamente el reproceso

Una fila de `reproceso.json` es un **campo re-parseable**, no una observación independiente: cada registro puede aportar hasta dos campos (la decisión de conducta y la sonda privada de justicia). El recuento actual (parser v2.2):

| Categoría | n | Significado |
|---|---|---|
| identica | 55.470 *(JSON canónico regenerado el 31-07: hasta entonces el fichero conservaba el recuento pre-G-final, 52.410 — discrepancia detectada por la auditoría de terceros del 31-07 y cerrada regenerándolo; la cifra citable es SIEMPRE la del JSON)* | el parser actual reproduce el valor almacenado |
| conducta_cambia | 19 | una conducta pasa a OTRA conducta → auditadas una a una (§2) |
| conducta_a_invalida | 43 | el parser actual es más estricto; el campo sale del análisis, no se convierte en otro dato |
| invalida_a_conducta | 2 | typos ahora legibles («APLIICO»→APLICO) |
| fallback_convencer | 11 | degradación de flujo documentada (crónica v2), no de parser |
| sin_raw | 5.472 | campos sin respuesta cruda almacenada (§3) |

De las 55.470 idénticas, ~52.400 son de los runs históricos y el resto del G-final (que el contrato de artefactos absorbió automáticamente).

## 2 · Las 19 reclasificaciones, una a una

Todas están enumeradas fila a fila, con su raw, en `reproceso_erratas.json` (clave = la fila exacta del detalle; `reprocesar.py --check-publication` **falla** si aparece una conducta_cambia sin errata). Resumen:

| Errata | n | Qué era | ¿Afecta a agregados? |
|---|---|---|---|
| **ERR-2026-001** | 11 | Typos de etiqueta de nivel en prisión (DESHUMUMANIZANTE, STRICTO…) leídos como NORMAL por el parser pre-24-07 | **Sí — ya corregido y publicado** vía `resumen_v2.json` + `ERRATA_prision.md` (24-07); los informes citan los valores reprocesados |
| **ERR-2026-002** | 7 | Sondas de justicia de gemini-flash-lite en milgram: respuestas «SÍ. …» leídas como False por el parser antiguo (buscaba un NO en cualquier parte) | **Sí — disonancia de gemini**: autoridad 1,00→0,96, control 0,87→0,81, rebelde 0,96→0,95. Regenerado en `resumen_v2.json` (29-07, `reproc_milgram.py`). Dentro del rango transversal 0,77-1,0; ninguna afirmación direccional cambia |
| **ERR-2026-003** | 1 | Ídem para glm-5.2 (vacuna) | **Sí — disonancia autoridad 0,98→0,84**; regenerado ídem; dentro del rango transversal |

Además, las 16 `conducta_a_invalida` de sondas milgram (ecos de consigna de glm → INVALIDA) retiran esas sondas del denominador; los `resumen_v2.json` del 29-07 ya lo reflejan (tres directorios de milgram reprocesados).

**Conclusión honesta**: la frase del borrador v0.1 «ninguna conducta publicada cambia» **era insostenible tal cual**. La formulación correcta, ahora en el manuscrito: *19 reclasificaciones entre categorías conductuales, todas auditadas con errata; afectan a la disonancia agregada de dos modelos en un paradigma (regenerada), sin invertir ninguna afirmación direccional; el resto de modificaciones son de validez (campo→INVÁLIDA), no de conducta.*

## 3 · Inventario de auditabilidad por experimento

| Experimento | Campos re-parseables | Raw | Auditabilidad |
|---|---|---|---|
| Asch (E1) | pública + privada | truncado a 200 chars | **Completa** para respuestas de una palabra (las de este diseño) |
| Milgram (E2/E3) | decisión + sonda | truncado a 150 | **Completa** (ídem) |
| Crónica (C1/v2) | decisión | truncado a 120 | **Completa** |
| Prisión (P1-P2b) | nivel + interno | truncado a 120 | **Completa** |
| **G2 (A2/A3/A5/B/C)** | nivel + sonda | **AUSENTE** (2.700 + 2.700 campos) | **NO re-derivable**: los runs del 25-07 son anteriores al cambio que conserva crudos completos. La conducta de G2 descansa en los valores parseados en runtime (parser estampado por fila) y NO puede re-verificarse desde crudos. Las interpretaciones de G2 sí están completas (campo `interpretacion`), y son la base de la κ ronda 2 |
| G-final | nivel + sonda + interpretación | **COMPLETO** | **Total** (además con manifiesto por solicitud) |

Esta asimetría queda declarada en el manuscrito (§6 y §8): la afirmación de re-derivabilidad se limita a los experimentos con raw.

## 3-bis · Limitación de los manifiestos confirmatorios (P0.5, 31-07; ampliada tras la reauditoría)

Los `manifest_run.json` de los runs del G-final (26-07) son **anteriores** a la clase `RunManifest` con estado final (29-07): contienen cabecera y el registro por solicitud (`solicitudes.jsonl`; A: 3.883 solicitudes, B: 243), pero **no** `status`, hora de fin, recuentos ni hashes de cierre. La reauditoría del 31-07 precisó dos huecos más, verificados contra el artefacto: **(a)** el `solicitudes.jsonl` de A contiene **5 registros con `respuesta: null` y sin campo `error`** — solicitudes cuyo desenlace (¿timeout silencioso?, ¿contenido vacío del proveedor?) no puede distinguirse desde el manifiesto; **(b)** ningún registro de A ni de B guarda `model_returned` (el modelo que el gateway declaró haber servido), de modo que la coincidencia pedido↔servido no es verificable retrospectivamente para esos runs. Por todo ello, «registro completo por solicitud» es una descripción EXCESIVA para los manifiestos del 26-07: lo exacto es «registro por solicitud con mensajes, parámetros y respuesta, sin estado final, sin desenlace tipado en 5 casos de A y sin modelo devuelto». No se reescriben (los crudos históricos son inmutables); las garantías completas (estado final, error tipado, `model_returned`) aplican a runs desde el 29-07, y así lo declara el preprint. Un run confirmatorio futuro (la ampliación a ≥20 cadenas) nacerá ya con manifiesto completo.

## 3-ter · Inventario de scripts con llamadas al proveedor (reauditoría 31-07, inventario A)

La afirmación «todos los harness registran con manifiesto» se limitaba a los seis entrypoints del modo estudio. Inventario completo y su estado desde v0.1.2-alpha:

| Script | Llama al proveedor | Manifiesto |
|---|---|---|
| `experimento_{asch,milgram,prision,cronica,g2,gfinal}.py` | sí (4 de ellos con pools) | **Sí** desde v0.1.0; los pools registran desde v0.1.2 (`map_paralelo`) |
| `experimento_gradiente.py` | sí (pools) | **Integrado en v0.1.2** (antes: sin manifiesto) |
| `tiento.py`, `retest_aptitud.py`, `retest_inkling_personas.py` | sí | **Integrados en v0.1.2** (antes: sin manifiesto) |
| `juez_gfinal.py`, `juez_g2.py`, `a4_validacion.py` | sí (juez vía cliente OpenAI directo) | **Integrados en v0.1.2**: cada solicitud del juez se registra; las ramas offline (`--kappa`, `--solo-muestra`) no activan manifiesto |
| `bateria.py`, `relanzar_celdas.py` | no (orquestan **subprocesos** de los entrypoints) | Declarados orquestadores: el manifiesto vive en cada entrypoint lanzado; conservan su `manifest.json` de lote |
| `run_spike.py` (narrativo) | sí | Sí (RunManifest context manager con hashes) |

**Limitación histórica declarada**: los outputs ya versionados de gradiente, tiento, retests, jueces y A4 (anteriores a v0.1.2) se generaron **sin** manifiesto por solicitud; sus artefactos agregados (registros/huellas/claves del juez) existen y están fijados donde procede por el release manifest, pero no tienen registro por solicitud física. No se reconstruyen retroactivamente.

## 4 · Vigilancia continua

- `reprocesar.py --check` (regresión): el detalle actual debe coincidir con el baseline versionado; cualquier cambio de parser o datos rompe la CI hasta revisarse.
- `reprocesar.py --check-publication` (publicación; nuevo, 29-07): falla si existe una conducta_cambia sin `errata_id`, o si los datos confirmatorios (G-final) pierden raw o `parser_version`.
- `release_manifest.py --verificar`: los datasets de cada tabla del manuscrito están fijados por sha256 en [`release_manifest.json`](release_manifest.json); `analizar_gfinal.py --manifest` los usa sin selección silenciosa de directorios.
