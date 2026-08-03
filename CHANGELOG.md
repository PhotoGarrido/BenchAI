# Changelog

## v0.1.4-alpha · PsicoBench + réplica de snapshot · 01-08-2026

- **PsicoBench v0.1**: el proyecto formaliza su benchmark de perfil social.
  `BENCHMARK.md` (doctrina modelo@snapshot@proveedor, utilidad práctica,
  criterios de inclusión), `benchmark/psicobench.json` + `benchmark/index.html`
  (panel autocontenido: clasificación ordenable, radar comparador A/B, mapas
  «las dos obediencias» y «los dos motores de crueldad», método), todo
  autogenerado por `spike/generar_benchmark.py` desde las matrices — con
  `--check` en CI para que tabla y panel no puedan desfasarse de los datos.
- **M4 · réplica de snapshot** (EXPERIMENTOS.md): batería íntegra sobre
  deepseek-v4-flash-0731 vía NaN (11/11 OK, 2,6 h, batch aislado, primera
  reanudación real por `progreso.jsonl`). El agregado se conserva (ISS
  45,5→46,0) pero el perfil se redistribuye (obediencia 0,80→0,90, P1b
  0→0,20, P2 0,77→0,58, Δ aliado −0,01→−0,12); la vacuna replica (Δ −0,5).
  Incluye corrección de registro del mensaje del commit `d2405c5` (comparó
  contra cifras recordadas, no archivadas).
- **Fix del agregador**: `analisis_bateria._es_rapido` descartaba como humo
  los runs `--vacuna` válidos (10 sesiones por diseño, un solo brazo);
  umbral propio (6) y matriz del batch 0731 regenerada con `vacuna_delta`.
  La matriz raíz pineada no se toca.
- **Trazabilidad operativa (02-08)** — principios adoptados tras revisar
  sistemas de revisión trazables, abstraídos a nuestro instrumento:
  - `benchmark/linaje.json`: derivación verificable del benchmark (sha256 y
    tamaño de matrices de entrada, transformación y salidas); el `--check`
    de CI verifica la cadena, no solo el resultado.
  - `POSICIONES.md`: todo hallazgo vive en una categoría epistémica
    (establecido / condicionado / desacuerdo real / abierto) con su
    evidencia y «qué lo movería»; los desacuerdos no se promedian.
    METODO.md §B lo exige para publicar.
  - `spike/adjudicacion.py` (+ tests): las discrepancias entre jueces no se
    resuelven en silencio — decisión firmada (decisión + razón + quién) o
    INVALIDA; corrección solo por sustitución; `--check` en CI y
    verificar.sh exige 0 pendientes para cerrar publicación.
  - `spike/vigia.py` (+ tests): una batería caída se reanuda sola desde
    `progreso.jsonl` (modelos desde el manifest del batch) con
    notificación macOS y tope de relanzamientos.
  - `SETUP_PSICOAI.txt`: instalación acompañada por agente con pruebas de
    aceptación explícitas — pensada para el segundo revisor externo.
- **P0 del plan PsicoBench (03-08)** — el benchmark gana incertidumbre y
  cadena de evidencia (test-retest ×3 del 0731 corriendo en paralelo):
  - `spike/incertidumbre.py`: n reales e IC 95% por eje (Wilson mono-estrato,
    bootstrap estratificado sembrado en prisión), IC del ISS y distancia
    d(A,B) por bootstrap conjunto, con **conciliación dura contra crudos**
    (16/16 entradas conciliadas; `ConciliacionError` tumba el `--check`).
    Corrección de registro: el n de prisión es 30+30 por variante (no ~160).
    Hallazgo: d(jul→0731) = 10,0 puntos [6,5–17,7] — la redistribución del
    perfil es real aunque los ISS se solapen ([39,7–50,0] vs [41,1–50,0]).
  - Métricas nuevas desde crudos: `tasa_objecion` (REHUSA ≠ ejecución tibia),
    `reconocimiento_milgram` (contaminación como covariable, 0,27–1,0) y
    `disonancia_prision` (0,01–0,41: discrimina donde la de Milgram satura).
  - Correlaciones entre ejes publicadas (P1↔P1b 0,76; P2↔P2b 0,53;
    Asch↔Milgram 0,23) + **pre-declaración congelada del ISS v0.2**
    (jerárquico por paradigma; obediencia = ruptura/10) en BENCHMARK.md.
  - `spike/fuentes_benchmark.json` (añadir modelos sin tocar código) + guía;
    cadena canaria GUID en harness, datos y `CANARY.txt` + política de
    rotación; mapa de cobertura portador×estrategia×daño con las celdas no
    cubiertas a la vista; regla de empates por solapamiento de IC.
  - `spike/verificar_citas.py`: bibliografía 11/11 verificada contra
    Crossref/arXiv (caché firmada por hash → `--check` sin red en CI);
    cazó y obligó a robustecer el matching (PMLR vía arXiv, apellidos
    compuestos). `spike/verificar_afirmaciones.py`: 13 anclas de evidencia
    en Resumen/§4/§5 del preprint, CPR 13/13 = 100%, puerta en CI.
- **M5 · fiabilidad test-retest (03-08)**: 3 réplicas de la batería íntegra
  sobre el 0731 vía NaN (0 $ marginal; el vigía rescató la réplica 1 de un
  disco lleno). El instrumento discrimina entre modelos 2,1–15,3× por
  encima de su ruido; suelo de d intra-snapshot ≈5 (máx 8,2) vs
  d(jul→0731)=10,0. Veredicto M4 con la regla |Δ|>2×SD: la redistribución
  sobrevive en 6/10 ejes (P2 −0,19 el más sólido; P1b con el margen más
  justo); la obediencia binaria no (solo su forma granular ruptura/10,
  SD 0,013 — refuerza la pre-declaración v0.2). `informe_retest_0731.md`.

## v0.1.3-alpha · Research Preview · 01-08-2026

Cierre de la **ronda seca** de la 4ª auditoría externa (31-07). El auditor
falsificó 8 garantías y dejó 4 mutantes vivos; todo confirmado por
reproducción y corregido, más las dos contradicciones del manuscrito.

- **12/12 mutantes ponen la puerta en ROJO** (antes 8/12). Nuevas puertas:
  `test_parsers_contrato.py` (corpus golden con negativas milgram sin
  «aplicar» + candado que liga `PARSER_VERSION` a un hash del comportamiento —
  mutantes 1 y 2), `test_gfinal_linter.py` (el linter aborta ANTES de
  `build_model` — mutante 8), `test_replay_privacidad.py` + `replay_publico`
  reescrito por whitelist con canary normalizado (mutante 11).
- **G1 · missingness fuera de conducta y narrativa (modo estudio)**:
  `experimento_asch.analizar` excluye los `None` de todos los denominadores y
  reporta `n_missing` por medida (12 vacías ya no dan conformidad 0,0);
  prisión ya no pasa el marcador `error_tecnico` como trato observado por los
  internos; g2 alineado con g-final (sonda privada no se pregunta tras fallo,
  sin «respuesta poco clara» en el diario). Nuevos casos en
  `test_barrido_falso.py` que ejecutan `analizar()`/`resumir()` con modelo
  vacío.
- **G3 · manifiesto honesto**: cliente OpenAI con `max_retries=0` (los
  reintentos físicos = líneas del JSONL; el SDK ya no reintenta en silencio);
  un fallo de escritura degrada el estado final (nunca `completed`) y no sube
  el contador; los seis harness activan el manifiesto ANTES del proveedor; el
  juez de A4 registra tokens. Tests: 500→500→200 = 3 líneas, fallo de disco →
  `degraded`, objeto de `build_model` fail-closed.
- **G4 producción**: `LimiteFailClosed` envuelve el `CallLimitLanguageModel`
  de Concordia y LANZA al agotar el límite en vez de devolver la opción 0 (una
  acción real); probado sobre el objeto que devuelve `build_model`.
- **G5 · taxonomía sensible única** entre ficha, scrub y test: sensibles =
  origen, NSE (incl. `nse_media`/`nseMedia`), ideología, religiosidad, salud,
  atractivo, idioma; de diseño = edad, género, educación; default seguro.
- **G9 · trazabilidad**: `analizar_g2 --manifest` toma los datasets del
  release_manifest (no el último dir por glob); 8 datasets de prisión + la
  matriz de la batería añadidos al manifest; nuevo `regenerar_publicacion.py
  --check` regenera y compara toda cifra citable; `test_trazabilidad.py` (un
  decoy no cambia la cifra en modo manifest).
- **G11 · SIGKILL**: escritura atómica con temporal ÚNICO (`mkstemp`), limpieza
  de `.tmp` huérfanos al abrir, y los tres replays como transacción; test que
  mata el proceso entre escritura y replace.
- **Preprint (ronda seca)**: tabla de prisión §3.3 regenerada desde los
  datasets fijados (media de los dos marcos, parser anclado, gemma
  post-ERRATA: qwen 15/73, gemma 90/78, mimo 1/14, deepseek 81/85 — el
  preprint anterior citaba el marco-peor); la afirmación de «ninguna
  aceptación privada» sustituida por la distribución real por modelo (grok
  0,19 como caso de baja disonancia), coherente en abstract, §3.3 y §4.
- **GARANTIAS/PROTOCOLO/ACUERDO** reescritos por alcance (banco vs simulador);
  los límites del simulador Concordia declarados y vigilados por puerta.

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
