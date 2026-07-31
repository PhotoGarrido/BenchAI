# Changelog

## v0.1.2-alpha · Research Preview · 31-07-2026

Cierre de la reauditoría de terceros del 31-07 sobre v0.1.1-alpha (los
cuatro bloqueantes reproducidos fueron confirmados y corregidos):

- **Manifiesto en pools**: el ContextVar del manifiesto no llegaba a los
  workers de ThreadPoolExecutor y los runs podían terminar `completed` con
  cero solicitudes registradas. Nuevo `manifiesto.map_paralelo` (propaga el
  contexto por tarea) aplicado a prisión, crónica, g2, g-final, gradiente y
  tiento; test que cuenta solicitudes físicas EXACTAS en los 6 entrypoints
  con pool y proveedor falso, completed/failed y dos runs concurrentes sin
  mezcla (`test_manifiesto_pool.py`). Gradiente, tiento, jueces (g2 y
  g-final), A4 y retests integrados al manifiesto; batería y relanzador,
  declarados orquestadores (los entrypoints que lanzan ya registran).
- **Contrato de escenario end-to-end**: `version` DEFINIDA en el schema
  (entero const 1), emitida por el panel (`construirConfig`) y comprobada en
  `validarEscenario`; el escenario integrado del runner y los fixtures la
  declaran y se validan por la misma puerta que un `--config`; `jsonschema`
  añadido al runtime.
- **Sensibles con default seguro**: `neutralizar_sensibles` recorre la
  estructura REAL (poblacion como objeto con `agentes_generados`,
  distribuciones, variantes) de forma recursiva; el motor neutraliza salvo
  `variables_sensibles: true` explícito; canarios en `test_sensibles.py`.
- **Cifra pública del reproceso** unificada con el artefacto: 55.545 campos
  con raw re-derivados (55.470 idénticos); 5.472 campos sin raw (5.400 de
  ellos la conducta de G2) — en preprint (v0.3), README y Research Card.
- **Sensibilidad determinista y fijada**: orden estable en el bootstrap
  emparejado (mismos bytes con PYTHONHASHSEED distinto, con test);
  `gfinal_robustez.json` fijado por hash en el release manifest.
- **Exportador**: valida full/public/alias contra `replay.schema.json`
  ANTES de escribir; sin actor identificable la clave `agente` se omite
  (nunca null); diálogo con atribución ambigua contemplado por el schema.
- **Falsos verdes reparados**: la ampliación de sinks del test XSS se
  ejecuta de verdad (bloque `__main__` al final); gitleaks escanea el
  historial COMPLETO con binario pineado (`--log-opts=--all`).
- Outdirs con microsegundos en todos los harnesses; `verificar.sh` con
  rutas entrecomilladas y pip-audit adicional del runtime (sin resolver
  transitivas de torch, exclusión documentada); actions pineadas por SHA.
- Limitación de manifiestos históricos ampliada (5 respuestas null sin
  campo `error` en A; sin `model_returned`) en la auditoría del reproceso.

## v0.1.1-alpha · Research Preview · 31-07-2026

Respuesta a la auditoría de terceros del 31-07 sobre v0.1.0-alpha:
`sample_choice` sin índice de acción real (opción neutra coherente o
excepción tipada), cierre completed/failed del manifiesto en los 6
entrypoints, validación de escenario en el motor antes de construir
modelos, `reproceso.json` canónico regenerado con G-final, limitación de
manifiestos confirmatorios declarada, `constraint_violation` con texto,
canary anti-fuga en el replay público, bootstrap emparejado como
sensibilidad, autoría de la referencia de Nature corregida. (La
reauditoría posterior del 31-07 encontró regresiones en este lote,
cerradas en v0.1.2-alpha.)

## v0.1.0-alpha · Research Preview · 29-07-2026

Primera versión etiquetada. Investigación sobre CONDUCTA DE MODELOS de
lenguaje bajo protocolos concretos — no sobre humanos.

- 6 paradigmas isomorfos (Asch, Milgram±vacuna, prisión P1-P2b, crónica de
  normas, G1→G2→G-final) sobre 17 modelos de 10 laboratorios.
- Instrumento validado en cadena: parsers tipados v2.2 (3 revisiones
  adversariales + reproceso de 55.470 campos con doble gate en CI), linter de
  contraste, barrido con modelo falso, manifiesto por solicitud con estado
  final, release manifest con hashes.
- Pre-registros congelados con enmiendas fechadas; 3 refutaciones publicadas.
- Validación humana del juez: FALLIDA según umbral pre-registrado (κ 0,55 <
  0,8), reportada como tal con análisis de sensibilidad (auditoría completa
  en preprint/auditoria_reproceso.md).
- Seguridad: panel/visor sin innerHTML dinámico + CSP + schemas con límites;
  replay público con borrado físico de campos privados; historial de git
  escaneado (limpio); sample_choice sin imputación.
- Borrador de preprint v0.2 en preprint/.
