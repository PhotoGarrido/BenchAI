# Plan de publicación — respuesta a la revisión externa del 27-07-2026

**Origen**: revisión externa humana intensiva (27-07). Veredicto aceptado: repo público NO-GO, preprint NO-GO, demo privada GO, hasta cerrar los P0. Este plan discute cada hallazgo (aceptado / matizado), lo convierte en tareas con esfuerzo estimado, y define las puertas de salida. Regla heredada de la revisión: *el repositorio contiene la evidencia del rigor; el preprint no puede resumirla con frases más limpias que los artefactos*.

**Triaje de los 25 hallazgos**: 21 aceptados (2 de ellos me corrigen a mí directamente: la frase del reproceso y la descripción del canal privado — mi revisión asistida del manuscrito no los vio; la humana sí), 3 aceptados-ya-declarados como deuda de fases pendientes (elevados de prioridad), 1 matizado con evidencia (la CI sí está verde y asociada al último commit; faltan las protecciones).

---

## Fase R1 · Integridad científica (0 $ · ~1-2 días) — bloquea el preprint

| # | Tarea | Hallazgo | Esfuerzo |
|---|---|---|---|
| R1.1 | **`preprint/auditoria_reproceso.md`**: definición exacta de «decisión» vs «campo»; las 19 `conducta_cambia` una a una con `errata_id`, si afectan a agregados (recomputar la disonancia de gemini/glm de milgram con las 8 sondas corregidas) y qué tablas cambian; inventario de auditabilidad por experimento (G2: 2.700+2.700 campos sin raw → conducta de G2 NO re-derivable, se declara) | 1 | 3-4 h |
| R1.2 | **Reescribir la frase del reproceso en el preprint** según la fórmula del revisor («19 reclasificaciones auditadas; se especifica cuáles afectan a agregados») y declarar los raws ausentes de G2 en §6 y §8 | 1 | 30 min |
| R1.3 | **Separar las tres medidas privadas** en método y resultados: juicio pre-acción (Asch) / conducta pública / evaluación post-acción con glosa (Milgram, G2, G-final); renombrar «convicción privada»/«disonancia» según corresponda y añadir la limitación (racionalización, consistencia retrospectiva) | 9 | 2-3 h |
| R1.4 | **Tabla maestra de modelos**: modelo, proveedor, gateway, fechas, experimentos, n cadenas, n decisiones, raw disponible, en qué afirmación transversal entra, motivo de exclusión. Cada titular del preprint con su denominador (16 con canal privado / 19 en ≥1 paradigma / 4 en el confirmatorio); corregir el «batería de 19» huérfano de §3.3 | 11 | 2-3 h |
| R1.5 | **Rebajar lenguaje** según la tabla del revisor (universal→«en todos los modelos evaluados», firma de especie→«patrón transversal en esta muestra», crueldad→«ejecución de acciones clasificadas como dañinas», motores independientes→«factores con efectos diferenciados en este diseño», etc.) | 10 | 1-2 h |
| R1.6 | **κ como «validación confirmatoria fallida»** con análisis de sensibilidad descriptivo; PABAK no la sustituye. Plan v2 (2 codificadores, muestra equilibrada, 2ª familia de juez) declarado como trabajo futuro | 12 | 1 h |
| R1.7 | **IC condicionados al banco de tareas** + ejecutar leave-one-content-out y leave-one-persona-out desde fixtures (gratis) + declarar la selección de modelos por abuso base como condición de la inferencia | 13 | 2-3 h |
| R1.8 | **«Revisión adversarial asistida por modelo»** en METODO.md y preprint; reservar «externa» para humanos independientes | 14 | 30 min |
| R1.9 | **Referencias completas** (Nature 2026 exacta, DOIs, Concordia/SOTOPIA) | 15 | 1 h |

**Puerta R1**: un lector puede ir de cada cifra del preprint al artefacto que la genera sin encontrar ninguna frase más fuerte que el artefacto.

## Fase R2 · Seguridad y contratos (0 $ · ~1-2 días) — bloquea el repo público

| # | Tarea | Hallazgo | Esfuerzo |
|---|---|---|---|
| R2.1 | **Panel sin `innerHTML` con datos dinámicos** (confirmado en `panel/index.html`): `createElement`+`textContent`, `addEventListener` en vez de `onclick=`, CSP, y test con payloads XSS en CI | 3 | 3-4 h |
| R2.2 | **JSON Schema de escenario y replay** (`schemas/*.schema.json`) validado en panel (antes de descargar), motor (antes de ejecutar) y visor (antes de cargar), con límites de tamaño/agentes/eventos/caracteres | 7 | 3-4 h |
| R2.3 | **`replay.full.json` / `replay.public.json`** con borrado físico de pensamientos; renombrar el botón del visor («Mostrar monólogo privado generado») | 23 | 2 h |
| R2.4 | **Escaneo de secretos en todo el historial git** (gitleaks/trufflehog) + secret/dependency scanning en CI + branch protection con checks obligatorios | CI | 1-2 h |
| R2.5 | **`sample_choice` sin imputación**: opción neutra reservada `NO_ACTION` registrada como `choice_state: INVALIDA` (o excepción tipada), test específico en el barrido narrativo | 4 | 2 h |

## Fase R3 · Reproducibilidad de ingeniería (0 $ · ~1 día)

| # | Tarea | Hallazgo | Esfuerzo |
|---|---|---|---|
| R3.1 | `RunManifest` como clase con context manager (estado `completed/failed/cancelled`, cierre con recuento y hashes), sin global; captura de errores de serialización | 16 | 2 h |
| R3.2 | Activar manifiesto en `run_spike.py` con hashes de escenario/system prompt | 5 | 1 h |
| R3.3 | Manifiesto con `messages` completos (incl. system), `model_returned`, endpoint redactado, hashes de harness, versiones de dependencias | 6 | 1-2 h |
| R3.4 | Escritura atómica (`.tmp` → validar → rename) + `run_status.json`; nombres de fichero `proveedor__modelo` y timestamps con microsegundos | 17, 18 | 2 h |
| R3.5 | **`release_manifest.json`** con hashes de los datasets exactos de cada tabla del preprint; `analizar_*.py --manifest` obligatorio para cifras publicables (sin selección silenciosa del último dir) | 19 | 2-3 h |
| R3.6 | **CI doble gate**: `--check-regression` (golden-file actual) + `--check-publication` (falla ante `conducta_cambia` sin `errata_id`, datos confirmatorios sin raw, filas sin `parser_version`, divergencia manifest↔tablas) | 2 | 2-3 h |
| R3.7 | Ventana de memoria explícita en episodios (sustituir `history_length=1M`), evento `constraint_violation` en el exportador, eventos estructurados desde el motor (no regex) — *alcance episodios; no bloquea preprint* | 20-22 | 1 día |

## Fase R4 · Publicación (decisiones de David + ~½ día)

| # | Tarea | Hallazgo |
|---|---|---|
| R4.1 | **LICENSE** (decisión: código Apache-2.0/MIT; datos y replays CC BY 4.0; preprint CC BY) + SECURITY, CONTRIBUTING, CITATION.cff, CHANGELOG, CODE_OF_CONDUCT | 8 |
| R4.2 | **README reescrito** con la jerarquía del revisor (qué es / qué no es / estado / demo / banco / resultados / reproducibilidad / limitaciones) | 25 |
| R4.3 | **Ficha de riesgo de estereotipos**: variables sensibles documentadas con sus plantillas de verbalización, análisis de sensibilidad con/sin demografía desde fixtures, «atractivo» retirado salvo hipótesis explícita en diseños futuros | 24 |
| R4.4 | Research Card + tag `v0.1.0-alpha` («research preview») | — |

## Checklist de salida (la del revisor, adoptada) — estado 29-07-2026

- [x] 19 reclasificaciones documentadas y reconciliadas (`preprint/auditoria_reproceso.md` + `reproceso_erratas.json`; disonancia gemini/glm regenerada vía resumen_v2)
- [x] No se afirma re-derivabilidad donde faltan raws (G2 declarado NO re-derivable en preprint §6/§8 y auditoría)
- [x] Panel sin datos editables en `innerHTML` + test XSS estático en CI
- [x] `sample_choice` sin imputar opción 0 (NO_ACTION registrado como INVALIDA + test)
- [x] Motor principal con manifiesto completo (RunManifest con hashes y estado final; escritura atómica)
- [x] Schemas de escenario y replay validados en panel/motor/visor + límites de carga
- [x] Denominadores 17/16/4-6 inequívocos + tabla maestra (preprint §2)
- [x] κ presentada como validación confirmatoria FALLIDA (preprint §6, sin rescate retrospectivo)
- [x] Sin referencias provisionales (Hewitt et al. 2026 + DOIs completos)
- [x] LICENSE (Apache-2.0 + CC BY 4.0 datos) y capa OSS completa
- [x] CI verde con doble gate, XSS, schemas, mypy, pip-audit y gitleaks; secret scan del historial local: 2.038 blobs limpios. *Protección de rama: requiere repo público/Pro (comando documentado en SECURITY.md)*
- [x] Un tercero regenera las tablas desde `release_manifest.json` (hashes sha256; `analizar_gfinal.py --manifest`) sin red

**Pendiente fuera del código** (decisiones/acciones de David): elegir venue del preprint, segunda revisión externa humana antes del GO público definitivo, y activar la protección de rama al publicar el repo.

**Orden de ejecución**: R1 (preprint deja de contradecir artefactos) → R2 (seguridad) → R3 (reproducibilidad) → R4 (decisiones de licencia/venue + release). R1+R2+R3 no requieren API ni presupuesto; R4 requiere dos decisiones de David (licencias, venue).

---

## Anexo · Auditoría de terceros del 31-07 (v0.1.0-alpha) — triaje y cierre

Verificada punto a punto el 31-07. **Confirmados y corregidos** (commit del 31-07): P0.1 `sample_choice` devolvía índice de acción real con texto NO_ACTION → ahora opción neutra coherente o `RespuestaIlegibleError`; P0.2 los 6 harness no cerraban el manifiesto → cierre completed/failed en `__main__` + `cerrar_activo`; P0.3 el motor no validaba escenario → `cargar_y_validar_escenario` ANTES de modelos + neutralización de sensibles del lado motor; P0.4 `reproceso.json` desactualizado (52.410) frente a la cifra citada (55.470) → JSON canónico regenerado con G-final; P0.5 manifiestos confirmatorios sin estado final → limitación declarada en auditoría §3-bis y preprint (no se reescriben crudos); P1.6 `constraint_violation` sin `texto` + canary recursivo en replay público; P1.9 prisión preguntaba la sonda tras fallo; P1.2 gate de erratas con campos/duplicados/huérfanas; P1.4 ContextVar; P1.10 bootstrap emparejado añadido como SENSIBILIDAD (no sustituye al pre-registrado: los 4 modelos negativos significativos, incluido deepseek −0,12 [−0,22, −0,03]); autoría Nature corregida (Ashokkumar primero); lenguaje ontológico acotado; pins de CI y gitleaks por SHA; `verificar.sh` como puerta de un solo comando; test de escenario corrupto contra el runner real; sinks XSS ampliados. **Matizado**: la CI del HEAD estaba verde (runs verificados con gh autenticado; el auditor no pudo acceder por credencial caducada — limitación suya declarada, no hallazgo). Tag de la versión corregida: `v0.1.1-alpha` (los tags no se mueven).

---

## Anexo · Reauditoría 31-07 (v0.1.1) — triaje y cierre

Reauditoría externa intensiva sobre `v0.1.1-alpha` (commit `07121b1`), dictamen NO-GO con cuatro bloqueantes «demostrados por ejecución adversarial». **Cada afirmación se verificó de forma independiente reproduciendo sus pruebas adversariales en este repositorio antes de tocar nada**; el cierre es el tag `v0.1.2-alpha`.

### Confirmados y corregidos (los cuatro P0 reproducidos + resto)

- **P0.2 · ContextVar y pools** — REPRODUCIDO: un `RunManifest` activo + worker de `ThreadPoolExecutor` → `completed`, `solicitudes=0`, sin `solicitudes.jsonl`. Corregido con `manifiesto.map_paralelo` (una copia de contexto por tarea, sin reentrar la misma `Context`) en prisión, crónica, g2, g-final, gradiente y tiento; `test_manifiesto_pool.py` cuenta solicitudes físicas EXACTAS en los 6 entrypoints (completed y failed) y prueba dos runs concurrentes sin mezcla. Gradiente, tiento, jueces, A4 y retests integrados al manifiesto; batería/relanzador declarados orquestadores (inventario en `preprint/auditoria_reproceso.md` §3-ter).
- **P0.3 · Contrato panel→schema→motor** — REPRODUCIDO: el schema exigía `version` sin definirla (aceptaba null/texto/999) y ni el panel la emitía ni el integrado/fixture la tenían. Corregido: `version` como entero `const 1` en el schema; el panel la emite (`construirConfig`) y la comprueba (`validarEscenario`); `ESCENARIO_DEFECTO` y `escenario_test.json` la declaran y el integrado pasa por `cargar_y_validar_escenario` como cualquier `--config`; `jsonschema` añadido a `requirements.txt`; `test_schemas.py` valida la forma exacta del export del panel, el integrado y el rechazo de versiones ausentes o de otro tipo.
- **P1.8/P0 · Sensibles OFF** — REPRODUCIDO: canarios en `poblacion.agentes_generados` sobrevivían y se verbalizaban (el scrub iteraba `poblacion` como lista siendo objeto). Corregido: `neutralizar_sensibles` recursivo por la estructura real (protagonistas, agentes generados, distribuciones de población, `mas_atributos`, variantes — con filtro de cambios `t2_*`/`idiomaPct` —, formas legacy); política de DEFAULT SEGURO en el motor (neutraliza salvo `variables_sensibles: true` explícito, con aviso si falta el flag; los escenarios del repo declaran `true` conscientemente, así que ninguno histórico legítimo cambia — política documentada en el schema); canarios en `test_sensibles.py`.
- **P0.4 · Cifra pública del reproceso** — CONFIRMADO por aritmética del JSON (55.470+19+43+2+11 = 55.545 con raw; 5.472 sin raw). Sustituida en resumen ES, abstract EN y §8 del preprint, README y Research Card por la fórmula completa, con una precisión ADICIONAL que la reauditoría no hizo: de los 5.472 sin raw, 5.400 son la conducta de G2 y 72 son de Asch (el artefacto desglosa por campo).
- **P0.5 · Manifiestos históricos** — CONFIRMADO (verificado contra el artefacto: exactamente 5 registros con `respuesta: null` sin campo `error` en A; 0 con `model_returned` en A y B). Limitación ampliada en la auditoría §3-bis.
- **P1.6 · Exportador** — REPRODUCIDO (`agente: null` en `constraint_violation` sin actor; jsonschema lo rechaza). Corregido: la clave se omite cuando no hay actor; full/public/alias se validan contra `replay.schema.json` ANTES de escribir; el diálogo de atribución ambigua (contrato del hallazgo 22) queda contemplado en el schema (`anyOf` agente/atribución=ambigua); tests de borde en `test_schemas.py`.
- **P1.10 · Sensibilidad no determinista** — REPRODUCIDO (`PYTHONHASHSEED` 1 vs 999 → IC de deepseek [−0,222,−0,025] vs [−0,222,−0,031]). Corregido con `sorted()` sobre la intersección de claves; verificado con dos procesos y hash seeds distintos → bytes idénticos (test permanente `test_robustez_determinista.py`); `gfinal_robustez.json` regenerado determinista y AÑADIDO al release manifest. Los IC emparejados redondeados que cita el preprint no cambian (deepseek −0,12 [−0,22, −0,03]).
- **Falso verde XSS** — REPRODUCIDO (la salida directa no contenía «ampliación de sinks»). Bloque `__main__` movido al final; `verificar.sh` y la CI exigen la línea «ampliación de sinks: OK» en la salida.
- **Falso verde gitleaks** — la action (aun con `fetch-depth: 0`) escaneaba el rango del evento, no el historial. Sustituida por un paso propio: binario v8.24.3 pineado por sha256, `gitleaks detect --log-opts=--all`, y una aserción en el job que FALLA si el log no declara >1 commit escaneado (verificado en el run de v0.1.2).
- **P1.1 · Colisiones de outdir** — microsegundos en `run_spike` y en todos los harnesses que seguían en segundos (asch/milgram/prisión/crónica/gradiente/tiento/retests).
- **P1.12 · Instalación limpia y metadatos** — README instala `requirements-ci.txt` (con ruff añadido) además del runtime; secuencia probada en un venv limpio; `verificar.sh` con `"$PY"` entrecomillado; README/CITATION.cff/CHANGELOG/Research Card en `v0.1.2-alpha` con entradas de changelog para v0.1.1 y v0.1.2.
- **P2 · pins y pip-audit** — `actions/checkout` (v4.2.2) y `setup-python` (v5.3.0) pineadas por SHA (resueltos contra la API de GitHub); pip-audit adicional sobre `requirements.txt` con `--no-deps` (resolver las transitivas de torch es impracticable en CI; exclusión documentada en THIRD_PARTY_NOTICES.md).
- **Preprint** — cabecera «v0.3 · 31-07-2026» con nota de la reauditoría; «la versión sí la cambia», «la resistencia es rasgo del modelo» y «la cláusula frena a los que dudan» reformuladas condicionadas al protocolo/muestra; Research Card «rasgo, no especie» → condicionado.

### Refutados con evidencia

- Ninguno frontal: **todas las afirmaciones técnicas centrales de la reauditoría se reprodujeron**. Dos precisiones menores donde el artefacto corrige el texto de la reauditoría: (1) «5.472 sin raw de G2» — el desglose real es 5.400 de G2 + 72 de Asch (documentado así); (2) el IC emparejado de deepseek citado como variable entre ejecuciones queda, ya determinista, en los mismos valores redondeados que publicaba el preprint (−0,12 [−0,22, −0,03]), de modo que no había cifra publicada errónea por este punto, solo irreproducibilidad del artefacto.

### Estructuralmente imposible ahora

- **Protección de rama con checks obligatorios**: requiere repo público o plan Pro (documentado en SECURITY.md); queda como acción de publicación.
- **Segunda revisión humana independiente** y elección de venue: decisiones de David, fuera del código.
- **Test de navegador real para XSS** (sugerido por la reauditoría como refuerzo): fuera del alcance de esta CI offline; el estático ampliado + CSP + schemas quedan como cobertura actual y el refuerzo se anota como deuda.
