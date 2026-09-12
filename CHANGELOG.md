# Changelog

## Sin versión (herramienta, no instrumento) · El alta deja de ser artesanía · 21-08-2026

- **`spike/alta.py` + [ALTA_MODELO.md](ALTA_MODELO.md)**: añadir un modelo pasa
  de ~7 pasos en 3 lanzadores con 3 JSON a mano a un comando con dos fases —
  plan con proyección de coste (se detiene sin `--autorizado`, regla de
  presupuesto de la casa) y ejecución con cableado completo (mapas N2/N3b,
  matriz, fuente, regeneración). Jamás pisa una clave existente de los mapas
  (son por alias, los comparten entradas históricas). Contrato offline en
  `test_alta.py`, cableado en `verificar.sh` y CI.
- **`bateria.py` alcanza al octógono**: N2 denuncia y N3b sicofancia de
  opinión entran en la SUITE — un batch nuevo trae los 13 sub-experimentos
  con reanudación y timeout; las carteras históricas no se tocan.
- **Denominadores con fuente**: los conteos del banco escritos a mano en
  prosa y metas («19 mediciones», «nueve laboratorios») quedan o derivados
  (apuesta de la home, metas del panel vía `__N_MEDICIONES__` con canario) o
  vigilados (`vigilar_denominadores` en `generar_datos.py`: si el banco crece
  y la prosa no, la generación se para). Las actas históricas fechadas quedan
  fuera a propósito.
- **Smoke sin nombres propios**: la aserción del panel deja de citar a
  qwen3.6 y verifica la invariante real (posición null ⇔ celda n/c, contada
  desde los datos). De paso cae un falso verde: `DATOS` es const de script,
  no `window.DATOS`, y el chequeo del radar llevaba desde su estreno cayendo
  en su fallback sin mirar los datos.

## v0.4.0-alpha · Octógono · 06-08-2026

- **M13 · el ISS v0.4 ejecutado tal cual se pre-declaró**: la sicofancia de
  opinión entra al índice como octavo eje, agrupada con la conformidad en un
  componente «cesión a iguales» — media de (media(conf, sico), ruptura/10,
  prisión, denuncia) / 4 sobre 19 entradas, con puente cuádruple v0.1→v0.4
  byte-idéntico en los tramos históricos.
- **El hallazgo es el estrato**: el brazo duro está en suelo en las 19
  mediciones (0,00–0,08) y **todo el eje lo produce el estrato amable** (hasta
  1,00 en grok). La sicofancia de opinión no es propiedad del modelo a secas
  sino del par modelo × personalidad asignada; los estratos se publican con IC.
- r(sico, conf) = 0,70 fuera de muestra, frente al 0,72 con el que se
  pre-declaró la agrupación: la estructura elegida queda validada.
- Movimientos reales de posición: sol −3 y grok −9; el resto, renumeración de
  anclas. Integración respetando E-IC-1 (remuestreo por cadenas), conciliación
  19/19 en los dos ejes nuevos y todas las puertas re-verificadas.

## v0.1.5-alpha · Respuesta a la 4ª auditoría externa · 06-08-2026

Tres P0 cerrados con reproducción, tres P1 y el P2 atendidos.

- **P0-1 · IC por cadena** (enmienda E-IC-1 + adenda E-IC-1b): el estimador remuestreaba turnos como observaciones independientes contra la unidad de inferencia pre-registrada. Ningún punto cambia; el IC del ISS se ensancha ×1,44 (mediana) y 9 de 19 etiquetas de posición cambian. Errata: `spike/resultados/ERRATA_ic_cadenas.md`. PsicoBench → v0.3.1.
- **P0-2 · E-N3-cede-v2**: sicofancia (N3) imputaba un seguimiento inválido como `cede=False`; ahora sale del denominador y se reporta como missing. El arco N entra en `artefactos.py`, el reproceso (55.545 → 93.422 campos) y el barrido falso.
- **P0-3 · manifiesto fail-closed**: un fallo al escribir la cabecera ya no permite cerrar `completed`; el de la cabecera inicial aborta el run antes de gastar (`CabeceraNoEscritaError`).
- **P1**: linaje con los 321 crudos y `denuncia_runs.json` firmados; 18 runs de denuncia en el release manifest (uno se perdía por colisión de clave); umbral duro de clasificación por n (D-8b, deja `qwen3.6` fuera de posiciones); metadatos del ISS corregidos y versión unificada con puerta propia (`test_version_unica.py`).
- **Método**: nuevo punto A.6 — ningún experimento ejecuta su primer run pagado fuera del perímetro de puertas.

## v0.3.0-alpha · Heptágono · 05-08-2026

- **M12 · sicofancia de opinión (E2 cierre)**: 11 mediciones (2,84 $ la
  cartera; un run perdido por reinicio del sistema, en cuarentena y
  re-medido). El eje más discriminante del banco: 0,00–0,50 con control
  0,00 en todas — qwen-35b 0,50, sonnet-5 0,45, sol 0,40 (los asistentes
  estrella), opus-5 0,12, haiku/gemma/qwen@NaN 0,00. Díptico completo con
  la perceptiva; gradiente intra-nombre replicado en eje virgen (qwen
  0,00@NaN vs 0,50@OR); complacencia 0,96–1,00; persona×modelo:
  r(amabilidad, cesión)=0,91 con colinealidad a/n declarada. Octógono
  v0.4 pendiente de pre-declaración. informe_sicofancia_opinion.md.

- **E3 · ISS v0.3 (heptágono)**: la denuncia (N2) entra como cuarto
  paradigma — índice = (Asch + ruptura/10 + media de prisión + Denuncia)/4 —
  tras demostrar estructura discriminante en M9+M11; eje medido para las 19
  entradas (denuncia_runs.json, fecha por eje declarada; heterogeneidad
  temporal asumida y visible, acotada por la réplica qwen d=2,5). Tabla
  puente triple v0.1→v0.2→v0.3 (índices históricos byte-reproducibles);
  IC v0.3 por bootstrap jerárquico de 4 componentes (stream iss3);
  conciliación del eje contra crudos con Wilson n≈70. Movimientos: grok −6
  (silencio 0,40 le pesa), qwen-OR +6, deepseeks cierran 41-43. La
  sicofancia perceptiva queda FUERA del índice por suelo uniforme (regla
  de REGISTRO_N sobre su propia criatura).
- **E2 · sicofancia de OPINIÓN (enmienda N3b)**: piloto NaN — la predicción
  pre-registrada acierta: discrimina donde la perceptiva daba suelo
  (deepseek 0,16 · mimo 0,08 · gemma/qwen 0,00, control 0,00 limpio,
  complacencia 1,00 — acomodación pública pura); rango 0,16 ≥ corte →
  cartera OR en vuelo.
- **E4 · preprint/psicobench.md v0.1**: borrador del preprint del benchmark
  (instrumento + cadena de auditabilidad + fiabilidad + las tres cotas de
  la identidad + factoriales), pendiente de revisión externa humana.

## v0.2.0-alpha · ISS jerárquico · 05-08-2026

- **M11 · cartera OR de denuncia y sicofancia**: 7 modelos (frontier sol y
  opus-5 incluidos) × 2 ejes, 14 runs, 0 fallos, 3,80 $. Sicofancia
  perceptiva: suelo universal 0,00 en los 7 (70/70 insistencias sostenidas)
  → muere como eje, se corona como hallazgo (el coro dobla 0,13-0,43, la
  consulta uno-a-uno 0,00 — trans-gama y trans-proveedor). Denuncia:
  confirmado (silencio 0,03-0,33 en 11 mediciones, candidato a séptimo eje
  v0.3); el coste social del canal es modulador con dirección por modelo
  (sube en 6, neutro en 3, qwen-35b lo invierte −0,33). informe_cartera_n.md.

- **E1 · ISS v0.2 (pre-declaración del 03-08, ejecutada tal cual)**: índice
  jerárquico por paradigma — media de (Asch, ruptura/10 de Milgram, media
  de los 4 ejes de prisión) — sustituyendo la media plana que sobreponderaba
  la prisión 4/6 y el binario supera-crítico de n=10. IC nuevo por bootstrap
  jerárquico conciliado (componente ruptura conciliado contra la matriz;
  semilla v0.1 intacta: la tabla puente reproduce byte a byte lo publicado).
  **Tabla puente v0.1→v0.2 autogenerada** en BENCHMARK.md; posiciones y
  empates recalculados (cabeza: cuádruple empate opus-4.8/haiku/luna/sol —
  luna pierde el nº 1 en solitario porque su ruptura granular 2,1 revela lo
  que el binario 0 % ocultaba; sonnet-5 y los qwen de OR bajan al subir el
  peso de Milgram; los deepseek cierran la tabla ~50). Panel v0.2 con el
  v0.1 en tooltip. Los M-informes históricos citan ISS v0.1 (su valor en la
  fecha); la tabla puente los mapea. CPR 13/13, adjudicación 0, --check OK.

## Sin versionar · C+D en curso · 04-08-2026

- **C·4 alineamiento método-código**: auditoría sistemática docs↔código
  (agente auditor + verificación manual). Núcleo alineado (18 coincidencias
  con fichero:línea); 9 discrepancias tratadas: D-1 canal privado perdido
  imputado como no-disonante (arreglado en Milgram/Asch/prisión; impacto
  medido 4/4467, 0/601, 0/2457 → ninguna cifra publicada cambia), D-2
  missingness de Milgram desglosado por condición×estado, D-3
  `disonancia_prision` con convención única «entre aplicados» (nivel≥2;
  rango 0,01–0,41 → 0,17–1,0; benchmark regenerado y conciliado), D-6 regla
  de empates implementada en tabla y panel («=n» por solapamiento con el
  ancla del grupo), D-7 párrafo residual del panel eliminado, D-8 puerta de
  completitud impuesta en el generador, D-9 cifra de C1-v2 rectificada con
  crudos (~3.000 decisiones + ~440 sondas, no «~7.500»), D-4/D-5
  documentados (Recon solo Milgram; acepta el fenómeno sin nombrar el
  paradigma). METODO §A-6 declara top_p/max_tokens reales (deuda D11).
  `informe_alineamiento_c4.md` · reprocesar --check: 55.470 decisiones
  intactas con parsers v2.3.
- **M6 · réplica cruzada OR↔NaN del 0731 (C·1)**: batería íntegra del
  snapshot exacto vía OpenRouter (0,30 $ auditado; `model_returned`
  uniforme; sin actualización silenciosa del v4-flash de OR, sigue en 0423).
  El gateway pesa casi tanto como la generación: d mismo-snapshot 8,1 ≈
  d generacional limpio 8,7 (confundido de M4: 10,0); 4/10 ejes fuera de la
  vara 2×SD entre gateways (clúster Milgram en bloque, aliado). Veredicto
  final de M4: 5 ejes confirmados con el par limpio (ruptura +0,11, P2b
  −0,12, aliado −0,09, P2 −0,08, vacuna −0,3..−0,7 siempre protege); P1b
  «estrena el clima» y la bajada de disonancia se reatribuyen al proveedor.
  PsicoBench pasa a 17 mediciones con ids `@proveedor`, los 3 pares de
  distancia del grupo publicados, orden cronológico real de fechas y
  doctrina de BENCHMARK actualizada («el gateway no distorsiona» no
  generaliza). `informe_cruzada_or_0731.md`.
- **M7 · portador, disfraz e idioma (D·1 + C·2 + C·3)**: tres factoriales de
  la escalera Milgram (NaN 0 $ + OR 0,55 $). Los PORTADORES disocian
  (system 10,0 con 0 empujones > coordinador 8,95 > memo 7,2 ≈ par 7,1;
  disonancia estable — la política impersonal ata más que la persona); el
  DISFRAZ pesa ≤0,9 en 6/7 modelos (error entre-disfraz medido ~±1;
  excepción gemma4 −1,1); el IDIOMA viaja ≤1,1 en 6/7 pero transforma a
  mimo-v2.5 (+3,4, control incluido) ⇒ condición de primera clase, perfiles
  declarados «en español». Operativa: NaN no soporta 3 experimentos
  concurrentes (429); cola secuencial + cuarentenas `_abortado_*`.
  `informe_pilotos_m7.md`.
- **M8 · cartera E-portador (D·3)**: la escalera de portadores replica en
  5/5 modelos y 2 proveedores (12 runs OR, 0,34 $). `system` ≥ coordinador
  en todos (gemini 7,3→10,0 y qwen 6,5→10,0 con ~0 empujones); `par` el más
  débil en todos; haiku en suelo con los 4 portadores (el portador modula,
  no crea); disonancia insensible al portador. Posición promovida a
  ESTABLECIDO; el eje de obediencia gana subíndice de portador.
  `informe_eportador_cartera.md`.
- **M9 · pilotos N1-N3 (D·2)**: 12/12 runs (4 NaN × 3 ejes, 0 $, en serie
  con el limitador). SICOFANCIA: predicción pre-registrada refutada — los 4
  ceden menos al usuario directo que a la mayoría (3/4 en cero); DENUNCIA:
  rango 0,03-0,33, el coste social sube el silencio en 4/4, disonancia del
  silencio 0,5-1,0; VENALIDAD: baja, sin gradiente por precio, disonancia
  venal 1,00 (cesión siempre consciente). Promoción pre-declarada: denuncia
  y sicofancia a cartera OR; venalidad celda medida-no-integrada.
  `informe_pilotos_n.md` · batería qwen@NaN reanudada y completa (0 fallos
  bajo el limitador) · réplicas mimo-en ×3 consolidadas.
- **M10 · gradiente de la identidad (D·4)**: qwen3.6 por ambas vías el
  mismo día — par declarado INTRA-NOMBRE (NaN opaco). d=22,1 entre
  proveedores (obediencia 0,00 vs 0,70; vacuna cambia de signo +0,56/−0,20)
  frente a d=2,5 del mismo nombre+proveedor a 12 días (control negativo:
  la estabilidad temporal existe) y d=8,1 del snapshot fijado (M6). Las
  tres cotas de la identidad medidas; benchmark a 19 mediciones con ids
  `@proveedor·fecha`; qwen@NaN entra con ISS 17,7 (puesto 5). Errata M9
  publicada (comparadores de sicofancia corregidos a mismo-proveedor: el
  veredicto pasa de «refutada 4/4» a «falla en los 2 casos nítidos, qwen
  la cumple por margen mínimo, gemma no informa»).
  `informe_qwen_intra_nombre.md`.
- **Parsers v2.3**: milgram/sino aceptan inglés por parámetro explícito
  (español byte-idéntico; candado versión↔comportamiento regenerado con
  corpus EN bajo contrato).
- **Milgram factorizado en bundles** (diseño v1 congelado, golden test de
  84 prompts byte-idéntico): `--variante reparto` (C·2, disfraz isomorfo en
  cooperativa de reparto), `--idioma en` (C·3, protocolo íntegro traducido,
  identidad incluida), `--portador system|memo|par` (D·1 E-portador; el
  portador system viaja en el mensaje de sistema real vía
  `model_factory.fijar_system_extra`, registrado verbatim en manifiestos).

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
