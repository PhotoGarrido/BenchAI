# Plan de alta: `stealth/union-alpha` (Union Alpha, OpenRouter)

Estado: **en ejecución**, 16-09-2026, rama `claude/alta-union-alpha`. Los
cambios de §2.2 y los guardianes de §3 están aplicados y probados; la
batería se lanzó el mismo día (ver el final del documento). El manual de
operación general es [ALTA_MODELO.md](ALTA_MODELO.md); esto es lo específico
de este modelo y lo que hay que cambiar antes de aplicarlo.

## 0 · Ficha verificada (16-09-2026)

| | |
|---|---|
| Id de llamada | `stealth/union-alpha` (OpenRouter, proveedor «Stealth») |
| Publicado | 16-09-2026 (`created` 1789569723) |
| Precio | 0 / 0 $ por M tokens durante la preview |
| Contexto / salida máx. | 262.144 / 131.072 tokens |
| Modalidad | texto + imagen → texto; tool calling |
| Parámetros | max_tokens, temperature, top_p, tools, tool_choice, response_format. **No expone `reasoning` ni `include_reasoning`** |
| Política de datos | «Prompts and completions **may** be retained by the provider but are not used for training» (openrouter.ai/provider/stealth). Ox Alpha decía «are retained». Un medio (Crypto Briefing) habla de «zero data retention»: contradice la fuente primaria; nos atenemos a OpenRouter. |
| Quién es | Anónimo. El anuncio de OpenRouter etiqueta a @unionalphaai; la prensa lo asocia a OpenCode (agente de código). Desarrollador real sin confirmar. |
| Ventana | «Aproximadamente una semana» (prensa; OpenRouter no la fija). Precedente: Ox Alpha 20-08 → desvelado 26-08 (6 días). |

Sondas neutras del 16-09 (ids `gen-1789586737-…` y `gen-1789586764-…` y
cuatro más en paralelo):

- Responde bien: una palabra, y un puzzle de lógica de tres cajas, correcto.
- Sin campo `reasoning`; `reasoning_tokens` 0. Pero **27 tokens nativos de
  salida para «Azul»**: hay un razonamiento oculto que ni se ve, ni se
  factura, ni se puede fijar (no hay effort). Es **una sola condición**;
  E-EFFORT (ROADMAP 3f) no aplica y no lleva sufijo `#`.
- **Latencia**: 27 s y 104 s en solitario; con 4 llamadas en paralelo,
  31 / 132 / 181 / 229 s (pared 229 s). El pool serializa: ~1 llamada/min
  efectiva, se pidan las que se pidan. Ox Alpha iba a 8-11 s.
- Saldo OpenRouter: 340 $ comprados, 335,2 usados → **4,8 $ de margen**.
  El modelo no gasta, pero un saldo negativo devuelve 402 incluso en
  gratis: que ningún otro uso de la clave lo hunda durante la tanda.
- Cuenta no free-tier; los `stealth/*` no caen bajo el tope diario de los
  `:free` (Ox Alpha: 4.536 llamadas en dos días sin un 429).

## 1 · Decisiones del dueño (antes de tocar nada)

1. **Entra o no.** Criterio de cartera (ALTA_MODELO §0): frontier vigente
   de cada lab. Un stealth es la punta de un lab por desvelar, a coste 0.
   Precedente: Ox Alpha. Recomendación: entra.
2. **Retención.** Política igual o más laxa que la de Ox Alpha, al que ya
   se envió el banco entero el 21/22-08. Recomendación: misma decisión.
3. **Calendario.** Con la latencia de hoy la suite (4.536 llamadas) son
   ~40-75 h; si baja a ~30 s con paralelismo real, ~17 h (tabla en §2.3).
   La ventana cierra hacia el 22/23-09. **Lanzar el 17-09; el 18-09 como
   tarde.** Puerta: re-sondeo el 17 por la mañana (cinco llamadas neutras).
   Si sigue a ~1/min, lanzar igualmente con reanudación vigilada.
4. **El Tiento.** Coste 0 pero ~2 h de ventana. Recomendación: saltarlo;
   Asch abre la suite y su validez (<90 % → descarte técnico) hace de puerta.
5. **Nombre publicado.** `union-alpha` · lab «sin desvelar» · vía
   «OpenRouter · fecha del run de Asch». Al desvelarse, `DESVELADOS`
   (el id y la medición no cambian).

## 2 · Repo: rama `claude/alta-union-alpha`

### 2.1 Limpieza previa

Hay **78 duplicados « 2»** de Finder/iCloud (13-09 00:10) sin rastrear:
`ALTA_MODELO 2.md` y `spike/alta 2.py` son versiones **viejas** (sin el
§1.4 de NaN ni el arreglo del «último batch»), más `test_* 2.py`,
`proyectar_coste 2.py`, `INFORME_AUDITORIA_R5 2.md`, y dentro de tres
baterías `matriz_m2 2.json`, `manifest 2.json`, `progreso 2.jsonl`,
`estado 2.json` y carpetas vacías «… 2». No afectan a CI, pero ensucian
`git status` y un `manifest 2.json` en `resultados/` es un tropiezo
esperando a `alta.py`. Listarlos:

```bash
find . -name '* 2*' -not -path './.git/*' -not -path './.claude/*'
```

Borrarlos es decisión de David (son suyos), antes de abrir la rama.

### 2.2 Harness (antes de lanzar)

| Fichero | Cambio | Por qué |
|---|---|---|
| `spike/model_factory.py` | timeout por llamada configurable, `PSICOAI_TIMEOUT_S`, aplicado en `sample_text` (hoy hereda `DEFAULT_TIMEOUT_SECONDS` = 60 s de Concordia) | 60 s mata la mayoría de las llamadas de hoy (27-229 s); `RetryLanguageModel(retry_tries=4)` las repetiría cuatro veces y hundiría la cola. **Bloqueante.** |
| `spike/alta.py` `sondear` | leer el mismo env en vez de `timeout=60` fijo | el sondeo abortaría el alta por lentitud, no por fallo. **Bloqueante.** |
| `spike/coste_run.py` `PRECIOS` | `"stealth/union-alpha": (0.0, 0.0),  # gratis en preview (16-09-2026)` | sin pin, `alta.py` avisa y la auditoría sale «SIN PRECIO» (comprobado en seco el 16-09: es el único aviso) |
| `spike/generar_benchmark.py` `NOTAS` | nota de procedencia para `stealth/union-alpha` (texto abajo) | sale al pie de BENCHMARK.md y viaja como `nota` a psicobench.json y datos.js |
| `spike/model_factory.py` (opcional) | extender el backoff de 429 «dentro del grifo» a `openrouter` (hoy solo `nan`) | si el pool stealth se satura, un 429 sube directo al Retry de 4 intentos y muere en un minuto |

`LABS`: `stealth` → «sin desvelar» ya existe. Nada que tocar.

Texto propuesto para `NOTAS`: «medido en fase stealth por OpenRouter
(proveedor anónimo, 16-09-2026): prompts y respuestas pueden quedar
retenidos por el proveedor, no usados para entrenar; el modelo no expone
parámetro de razonamiento, así que la condición es única y el pensamiento
oculto no es controlable».

### 2.3 Ejecución

```bash
cd spike
python alta.py --modelos stealth/union-alpha            # plan en seco (probado el 16-09)
PSICOAI_TIMEOUT_S=600 BATERIA_TIMEOUT_S=86400 OPENROUTER_MAX_CONCURRENTES=8 \
  nohup python alta.py --modelos stealth/union-alpha --autorizado \
  > "$SCRATCH/alta_union.log" 2>&1 &
```

- `BATERIA_TIMEOUT_S`: sicofancia_op fue 78 min a 9 s/llamada; a 60 s son
  ~9 h. El tope por defecto (90 min) cortaría casi todo: 24 h o 0.
- Vigilancia: `tail -f` del log, `estado.json` del batch y, en
  `solicitudes.jsonl`, la proporción de timeouts y vacíos. Si en Asch supera
  el 10 %: parar, es descarte técnico.
- Caída: `--reanudar resultados/bateria_X` (progreso.jsonl).
- `proyectar_coste.py … --tope 8` no aporta coste (0) pero da el ritmo real
  de llamadas/hora, que es la única estimación honesta del fin.

Estimación por sub-experimento (minutos reales de Ox Alpha × factor de
latencia):

| Sub-experimento | Ox Alpha | ×3 (~30 s) | ×7 (~60 s) |
|---|---|---|---|
| asch + milgram | ~35* | ~1,7 h | ~4 h |
| milgram_vacuna | 20 | 1 h | 2,3 h |
| crónica (4) | ~50 | 2,5 h | 6 h |
| prisión (4) | 122 | 6 h | 14 h |
| denuncia | 40 | 2 h | 4,7 h |
| sicofancia_op | 78 | 4 h | 9 h |
| **Total** | **~5,8 h** | **~17 h** | **~40 h** |

\* asch y milgram figuran «reanudados» en `estado.json` (estimados);
cronica_v2_s717 marcó 613 min por un bloqueo, se toma ~15. A 1 llamada/min
pura, sin paralelismo efectivo: ~75 h.

### 2.4 Cableado y verificación

`alta.py` hace mapas, matriz, `fuentes_benchmark.json` y regenera benchmark
y web. Después `./verificar.sh`. `generar_datos.py` se parará por los
denominadores de prosa (§3): es lo esperado.

## 3 · Web: qué cambia solo y qué exige mano

### Automático (por `datos.js` / `psicobench.json`)

Tabla y posiciones (los empates se renumeran), radar, puente v0.1→v0.4,
correlaciones, rangos de portada, panel (`__N_MEDICIONES__`), linaje. En
`/psicobench`: mapa, tarjetas, ranking por eje, cara a cara, ficha
`#m=union-alpha`, escalera, CSV, y una fila de grupo «sin desvelar» en la
agrupación por laboratorio.

### Manual: la prosa (el guardián `vigilar_denominadores` para la generación)

| Superficie | Línea | Hoy | Qué hacer |
|---|---|---|---|
| `/completo` (index.html) | 11 (meta) | «28 mediciones, 11 laboratorios» | «29 mediciones, 11 laboratorios» (+ «y un modelo sin desvelar») |
| | 218 | «Veintiocho mediciones» | «Veintinueve» |
| | 220-222 | lista de labs, «incluido el que se midió aún sin desvelar…» | añadir «…y un segundo modelo aún sin desvelar, Union Alpha» |
| | 544-545 | «0,66 sobre veintiocho» | añadir «y 0,XX sobre veintinueve» con la r que salga. Es un resultado y **no está vigilado**: apuntarlo aquí |
| `/` (home.html) | 442 | «De once laboratorios» | sigue «once» si se excluye «sin desvelar» del conteo (abajo); añadir «más uno sin desvelar» |
| `/psicobench` (psicobench.html) | 11, 14 | «28 mediciones de 11 laboratorios» | actualizar **y añadir la página al guardián**: hoy `vigilar_denominadores` no la vigila (deuda hallada el 16-09) |
| pagina.js | 302 | «El estrato duro está pegado al suelo en las 28 mediciones» | re-comprobar la **afirmación** con union-alpha (máximo actual 0,08); si rompe, reescribir, no renumerar |

### Conteo de laboratorios con un stealth dentro

`bloque_portada` y `vigilar_denominadores` cuentan «sin desvelar» como
laboratorio: publicarían «12 laboratorios». Propuesta: excluirlo del conteo
y exponer `portada.sinDesvelar` para que la prosa y los rótulos de portada
que leen `D.portada.laboratorios` digan «11 laboratorios y un modelo sin
desvelar». Cuando se desvele y sea lab nuevo, contará de verdad.

### Ficha en `/psicobench`

`psicobench.js` ya pinta `nota` y `desvelado` (l. 735-736): la nota de
procedencia saldrá sola en la ficha. Nada que tocar.

### Textos del repo

BENCHMARK.md (tabla y nota al pie: automáticos). CHANGELOG: «Sin versión ·
Union Alpha (stealth) · fecha». EXPERIMENTOS.md: entrada M-n con fechas por
eje, coste 0, latencias y lo que se vio.

## 4 · Publicar

PR → CI en verde (los `--check` byte a byte exigen regenerar desde un
checkout limpio si hay dos sesiones en el árbol) → merge → deploy manual
(`VERCEL_TOKEN` sigue sin configurar) → `node web/smoke.mjs
https://benchai.tech`.

## 5 · Cuando se desvele (previsto ~22/23-09)

`DESVELADOS["stealth/union-alpha"] = {"lab": …, "nombre": …, "fecha": …}` →
regenerar → nota automática al pie y en la ficha → CHANGELOG. Si el lab
publica la versión final, es **otra entrada** (réplica cruzada, como
`glm5.3-flash` por NaN frente a `ox-alpha`).

## 6 · Riesgos

- **Latencia y cola**: puede no acabar dentro de la ventana. Mitigación:
  lanzar ya, reanudación, timeouts largos, ritmo medido desde el batch.
- **Retirada a mitad**: Ox Alpha duró 6 días. Un perfil incompleto no
  publica (D-8); los crudos quedan versionados igual.
- **Saldo de 4,8 $**: negativo → 402 hasta en gratis.
- **Retención por un tercero anónimo**: decisión de David; precedente 21-08.
- **Pensamiento oculto no controlable**: documentado en `NOTAS`.
- **Otra sesión en el mismo árbol**: generar artefactos en worktree.

## 7 · Lanzamiento (hecho el 16-09-2026, 22:27)

- Rama `claude/alta-union-alpha`, árbol de trabajo principal. **No cambiar
  de rama en este árbol mientras corra**: `bateria.py` lanza cada
  sub-experimento como sub-proceso nuevo y leería el código de la otra rama.
- Batch: `spike/resultados/bateria_20260916_222735_664256/` (log del modelo
  `stealth_union-alpha.log`, estado en `estado.json`, reanudación por
  `progreso.jsonl`). Log de `alta.py` en el scratchpad de la sesión
  (`…/scratchpad/alta_union-alpha.log`); el que importa es el del batch.
- Entorno: `PSICOAI_TIMEOUT_S=900 BATERIA_TIMEOUT_S=86400
  OPENROUTER_MAX_CONCURRENTES=8`, clave de `spike/.env`.
- Sondeo previo: responde. Latencia re-sondeada a las 22:25: 45-50 s por
  llamada, estable → estimación **~40-60 h**, fin hacia el 18/19-09.
- Si se cae: `cd spike && PSICOAI_TIMEOUT_S=900 BATERIA_TIMEOUT_S=86400
  .venv/bin/python alta.py --modelos stealth/union-alpha --autorizado
  --reanudar resultados/bateria_20260916_222735_664256`.
- Al terminar, `alta.py` cablea mapas, matriz y fuente y regenera benchmark
  y web; `generar_datos.py` se parará por la prosa (§3). Quedan a mano:
  prosa de las tres páginas, afirmación de pagina.js, CHANGELOG,
  EXPERIMENTOS.md, `./verificar.sh`, commit de crudos + artefactos, PR,
  deploy manual y smoke de producción; y `DESVELADOS` cuando se desvele.

Hecho ya en la rama (16-09, puerta completa en verde): timeout por entorno
y backoff de 429 en OpenRouter (`model_factory.py`, `alta.py`), pin de precio,
nota de procedencia en `NOTAS`, guardián de prosa sobre `/psicobench` y
conteo de laboratorios sin el anónimo (`generar_datos.py`), tests
`test_timeout.py` y `test_denominadores.py` en CI y en `verificar.sh`,
§1.5-1.6 de ALTA_MODELO.md, `linaje.json` y `datos.js` regenerados. Hay
78 duplicados « 2» de Finder sin rastrear pendientes de borrar (§2.1).

## 8 · Resultado (18-09-2026)

Batería completa: 13/13 sub-experimentos OK en ~30 h de pared (≈24 h de
máquina real: el portátil durmió con la tapa cerrada de 16:40 a 21:53 del
17-09 y el proceso reanudó solo). 5.738 llamadas físicas (4.354 válidas,
1.375 429 «rate-limited upstream» absorbidos por el grifo, 9 errores
sueltos), 1,8 M tokens de entrada y 1,0 M de salida, 0 $. Latencia mediana
15 s, p90 51 s. 0 respuestas inválidas; precisión de control 1,0 en Asch.

`union-alpha` · sin desvelar · OpenRouter · 16-09-2026: **ISS 20,8
[14,3–27,7]**, grupo de empate 5 (7.º por punto). Conformidad 0,07 ·
obediencia 0,50 · abuso 0 / 0 / 0 · órdenes 0,43 · silencio 0,04 ·
sicofancia de opinión 0,42 (amables 0,84, duros 0,00). Disonancia 1,00,
vacuna −0,50, aliado −0,07, reconoce Milgram al 100 %. Puente v0.1→v0.4:
16,7 (3) · 20,6 (1) · 16,4 (1) · 20,8 (5).

Afirmaciones re-comprobadas con 29: estrato duro en el suelo (máx 0,08);
r(sico, conf) baja a 0,60 (union-alpha es el caso divergente: conformidad
0,07 con sicofancia 0,42). Prosa actualizada en las tres páginas, README y
CHANGELOG; `alta.py` dejó cableados mapas, matriz y fuente y regeneró el
benchmark. Pendiente: PR, merge, deploy manual y smoke de producción;
`DESVELADOS` cuando OpenRouter diga quién es.

## 9 · Desvelado (18-09-2026, aplicado el 21-09)

Union Alpha era **Pareto, de Unbiased** (plataforma de Circuit & Chisel): un
modelo compuesto que enruta cada petición entre varios modelos frontier y
abiertos. La preview duró 33 horas; OpenRouter lo listó como
`unbiased/pareto` (2,50/7,50 $ por M) el 18-09 a la 01:02 local, 50 minutos
después de nuestra última llamada. `DESVELADOS` + `LABS["unbiased"]` + nota
de modelo compuesto en `NOTAS`; la prosa pasa a «29 mediciones de 12
laboratorios». Si algún día se mide la versión de pago, es otra entrada
(réplica cruzada preview → producto, como ox-alpha → glm5.3-flash).
