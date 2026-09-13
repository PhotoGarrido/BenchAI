# Plan · una superficie propia para PsicoBench (web con foco en el benchmark)

**Fecha**: 13-09-2026 · **Rama**: `cartera-septiembre` · **Estado**: investigación previa y propuesta de diseño; nada construido todavía.

**La idea**: además de la home divulgativa (`/`) y del sitio largo (`/completo`), una tercera superficie **solo del benchmark**, bien diseñada, con gráficos, tablas y ejemplos, pensada para enganchar por la vía de la «personalidad» / psicología social de los modelos. Este documento recoge (1) qué hay hoy, (2) qué datos existen ya para dibujar, (3) cómo lo hacen LM Arena, Artificial Analysis y los benchmarks conductuales con web propia, (4) la propuesta de diseño y (5) un plan por fases, cada una publicable por sí sola.

---

## 1 · Estado actual: tres superficies, tres estéticas, un mismo dato

Hoy PsicoBench se ve en tres sitios distintos, con tres lenguajes visuales y sin una superficie propia:

| Superficie | Ruta | Qué muestra del benchmark | Estética | Problema para «enganchar» |
|---|---|---|---|---|
| Home divulgativa | `/` (`web/home.html`, sección `#psicobench`) | Una «lámina» con octógono (dos modelos superpuestos, fichas laterales) + tabla global clicable | Editorial cálida, fondo oscuro, monoespaciada en etiquetas | Es un bloque a mitad de una página larga: el benchmark llega en la posición 7 de 11 secciones |
| Sitio largo | `/completo` (`web/index.html`, sección `#benchmark`) | Octógono, fichas de fiabilidad (×ruido, 10,3 puntos), tabla ISS con IC, matriz de correlaciones, aviso «qué NO es» | Misma familia editorial, fondo claro | Es la sección 06 de 11: el lector tiene que llegar hasta ahí |
| Panel del benchmark | `/benchmark` (generado por `spike/generar_benchmark.py` desde `spike/plantilla_benchmark.html`) | Cuatro pestañas: Clasificación (tabla con celdas de calor), Radar comparador (A vs B + tabla de diferencias), Mapas (dos dispersiones fijas: «las dos obediencias» y «los dos motores de crueldad»), Método | Serif claro, denso, tono de informe | Es el más completo pero **no tiene narrativa**: ni ejemplos, ni «por qué importa», ni entrada suave. El párrafo introductorio de la clasificación son 12 líneas de doctrina antes del primer dato |

Lo que ya funciona y hay que conservar:

- **La tabla autogenerada** con posiciones por solapamiento de IC (`=1`, `=5`, `=16`, `n/c`): es honesta y ningún leaderboard de los revisados lo hace exactamente así (el más cercano es el *Rank Spread* de LM Arena y el *rank by upper bound* de Scale).
- **El radar A-vs-B con tabla de diferencias por eje**: es el patrón «comparador» que LM Arena y Artificial Analysis ofrecen, ya resuelto.
- **Las dos dispersiones con nombre propio** («las dos obediencias», «los dos motores de crueldad»): cada una cuenta un hallazgo, no es un gráfico genérico. Ese es el patrón a multiplicar.
- **La cadena de linaje** (`linaje.json`, `--check` en CI, canary, manifiestos): el punto de venta declarado en `PLAN_PSICOBENCH.md` §4 es «el benchmark auditable, no el leaderboard».
- **La doctrina** (no es ranking de calidad; se miden versiones, no nombres; empate = no distinguible): tiene que sobrevivir intacta en la nueva superficie o el diseño la traiciona.
- **Las primitivas de `web/js/graficas.js`**: `figura()` con tabla alternativa accesible, tooltip (`globo`), navegación por teclado (`navegable`), formato español de cifras. La nueva página debe reutilizarlas, no reinventarlas.

## 2 · Inventario: qué datos hay ya para dibujar sin medir nada nuevo

Todo lo siguiente está en `benchmark/psicobench.json` (v0.4, 23 entradas) o en los crudos versionados, y por tanto puede llegar a la web por `web/generar_datos.py` sin escribir una cifra a mano:

| Dato | Dónde está | Qué visualización habilita |
|---|---|---|
| 8 ejes × 23 mediciones, proporción 0–1 | `entradas[].ejes` | Tabla, heatmap modelo×eje, radar, barras por eje |
| IC 95 % por eje y por ISS, con `n` y `n_cadenas` | `entradas[].ejes_ic`, `iss_ic` | Bigotes en barras, bandas en el ranking por eje, tooltip de fiabilidad |
| Posiciones con empates por solapamiento | `entradas[].posicion` (y `_v01/_v02/_v03`) | Ranking honesto; «escalera» de versiones |
| Tabla puente v0.1→v0.4 | `iss_v01…iss_v03` + posiciones | Timeline por versión del instrumento (*bump chart*) |
| Secundarias: disonancia, efecto aliado, vacuna, objeción, reconocimiento, complacencia, ruptura media, quiebres, sico amables/duros con IC | `entradas[].secundarias` | Dispersiones con nombre (ya existe una), díptico amables/duros, columna de contaminación |
| Matriz de correlaciones 8×8 | `correlaciones` | Heatmap de estructura del índice (ya en `/completo`) |
| Réplicas con d e IC (misma familia, distinto snapshot/gateway) | `replicas` | Gráfico «el nombre no es el modelo»: pares unidos por línea |
| Lab, proveedor, fecha, `desvelado`, `nota` | `entradas[]` | Filtros por lab; insignias; nota al pie (ox-alpha → GLM-5.3-Flash) |
| Ids de run por paradigma | `entradas[].runs` | Enlace desde cada celda a la evidencia cruda (repo) |
| **Texto privado citable** por sesión (Milgram `privada_raw`, prisión `raw`/`desc`, denuncia, sicofancia) | `spike/resultados/**/sesiones.jsonl`, `registros_carcel.jsonl` | **Ejemplos en línea**: la frase con la que un modelo aplica o rehúsa. La web ya publica extractos así en la «consola» del portador (4 sujetos, `bloque_consola` de `generar_datos.py`), luego el mecanismo y la decisión editorial existen |
| Estímulos literales (extraídos por AST de `spike/experimento_*.py`) | `datos.js` → `milgram`, `asch`, `prision`, `arcoN` | Mostrar el estímulo exacto junto al resultado |
| Anclas humanas (Asch ~33 %, Milgram ~65 %) | Pendiente D13 en `PLAN_PSICOBENCH.md` | Bandas de referencia en cada eje, con el caveat de que no son comparables |
| Corpus (runs, llamadas, horas, tokens) | `datos.js` → `corpus` | Tira de «escala» al pie |

Lo que **no** hay y condiciona el diseño: coste por modelo (no está en el JSON público; Artificial Analysis vive de ese eje), latencia agregada (está en `solicitudes.jsonl`, sin agregar), fechas de lanzamiento de los modelos (solo la de medición), y licencia/open-weights por entrada (deducible del lab, no es campo). Ninguno bloquea; los dos últimos son campos baratos de añadir a `fuentes_benchmark.json` si se quieren los filtros de LiveBench/Arena.

---

## 3 · Cómo lo hacen los demás (investigación del 13-09-2026)

Método: visita real con navegador y `fetch` (capturas y HTML), no de memoria. **No cargaron** y se describen por su repo o documentación: SWE-bench (shell React sin SSR), Spiral-Bench/EQ-Bench (timeout), Open LLM Leaderboard (iframe; además fue **retirado en marzo de 2025**), y la ficha de modelo de LM Arena (404; los nombres de la tabla enlazan a la nota de prensa del proveedor). Los gráficos de Arena bajo la tabla existen en el HTML pero un modal de cookies impidió capturarlos.

### 3.1 Los generalistas

**LM Arena** (`arena.ai/leaderboard/text`). Tabla **Rank | Rank Spread | Model | Score | Votes | Price $/M | Context**; bajo el nombre, «Anthropic · Proprietary»; score como «1506 ±5»; **Rank Spread** como rango «1 – 7» (posiciones compatibles con el IC; una fila con pocos votos muestra «6 – 52»). Sidebar con 29 categorías, *Style Control*, licencia, sliders de precio/contexto; toggle **Models | Labs**; cabecera con «Sep 11, 2026 · 8.126.041 votes · 401 models». Bajo la tabla, cinco gráficos: IC del score, heatmap de fracción de victorias A vs B, heatmap de recuento de batallas, media de win-rate, y modo *Pareto* (score vs precio). Claro, crema, serif en títulos, mono en nombres. **Bien**: Rank Spread es la mejor representación del empate estadístico; toggle Models/Labs. **Mal**: 401 filas sin paginación, sin ficha de modelo, heatmaps enterrados, IC solo como texto.

**Artificial Analysis** (`artificialanalysis.ai`). Hero tipográfico serif + **tres tarjetas «Highlights»** (*Intelligence*, *Speed*, *Cost per Task*), cada una con un mini bar chart con **color fijo por lab**. Luego secciones largas: índice en barras (open weights vs proprietary), **scatter índice vs coste con frontera de Pareto y cuadrante «Most attractive»**, líneas «Frontier … over time», barras apiladas de tokens. Ficha de modelo con cuatro tarjetas «#8 / 63», medidores y los mismos gráficos filtrados a comparables. Sin IC: la incertidumbre se sustituye por versionado explícito del índice («v4.3») y enlace a metodología en cada bloque. **Bien**: tarjetas-highlight, scatter con cuadrante explicado, «rank #k / N». **Mal**: scroll infinito, 60 etiquetas rotadas por gráfico.

**Scale SEAL** (`labs.scale.com/leaderboard`). Catálogo de tarjetas por benchmark con top-3, pestañas **All | Agentic | Safety | Frontier**. Por benchmark: **Rank | Model | Score ± CI** («65.40±1.90»); **MASK** (honestidad) ordena por *Rank (Upper Bound)* «agrupando modelos con rendimiento estadísticamente equivalente», y clasifica respuestas en *Lie / Honest / Evade*; **PropensityBench** mide «proporción de escenarios donde el modelo elige la acción desalineada» bajo seis presiones. Cero gráficos. **Bien**: rank por cota superior explicado; *Safety* como familia propia. **Mal**: solo tabla.

**Epoch AI** (`epoch.ai/benchmarks`). Pestañas de vista **Score vs time | vs compute | Forest | Leaderboard**; scatter con color por organización y etiqueta solo en la frontera; panel de ajustes (solo frontera, color por país/organización, filtro de texto); «±1 standard error» documentado; **log viewer** por modelo y benchmark, CSV y API. La mejor referencia de «timeline».

**LiveBench** (`livebench.ai`). **Slider de releases** con puntos; filtros como chips (*Open weights, Show org, Compare, Choose columns*); tabla con «shading = top 5 por columna · click en fila para subtareas»; *Insights* con «Quality vs cost (log): click a model to grey out its kill zone». Sin IC.

**Otros** (patrones puntuales): **Aider** (barra inline en la celda de porcentaje, fila expandible, checkboxes → scatter); **SWE-bench** (cada entrada declara `logs`/`trajs`/`verified`/`oss` con iconos); **METR** (eje log, toggles 50 %/80 %, whiskers, aviso «measurements above 16 hrs are unreliable»); **ARC Prize** (oscuro, *Space Mono*, eje X conmutable **Cost | Release date**, «preview» para no verificados); **Humanity's Last Exam** (columna **Calibration Error ↓** junto a la de acierto, «Judge Model | Dataset Updated», dos preguntas de ejemplo); **Vending-Bench 2** (± en tabla, bandas de 1 SD sobre trayectorias, «Performance vs Release Date +$822/month», y **transcripts embebidos** como pieza narrativa: el «doom loop»); **Kagi** (tabla markdown y nada más: el suelo mínimo).

### 3.2 Los conductuales / de personalidad (lo que más se parece a PsicoBench)

**sycophancy-eval** (`sycophancy-eval-smoky.vercel.app`). Hero «How well do models resist social pressure?» con «7 scenarios · 2 languages · 18 models · 544 runs · Last run 2026-09-08». Dos paneles: **Sycophancy Score** (tabla con barra inline, «lower = more resistant») y **radar de 7 dimensiones** con varios modelos superpuestos y *chips* para activar/desactivar. Debajo, **tabla modelo × escenario** con badge **✓ Maintains / ~ Hedges / ✗ Capitulates**, fracción «(2/5)», tipo de juez en cabecera y concordancia entre jueces (*consensus / split / disputed*). Toggle EN/中文. Sin visor de transcripts. Es la referencia más directa.

**SnitchBench** (`snitchbench.t3.gg`). Estética temática de vigilancia (negro, rojo, condensada en mayúsculas, «System: MONITORING · Models: 8 · Total Runs: 640»). **Variantes como pestañas** (*Tame/Bold × Email/CLI*), un solo gráfico de barras agrupadas (contacto con gobierno vs medios). Sin IC ni ejemplos. Lección: un eje de «denuncia» puede ser memorable con una identidad fuerte; la falta de IC lo hace poco citable.

**HumaneBench** (`humanebench.ai`). **Heatmap modelo × principio** (15 × 8 + puntuación global), escala divergente rojo–amarillo–verde de −1 a +1 con número en la celda, etiquetas rotadas 45°, tres secciones por condición (*Bad persona / Good persona / Baseline*) y «steerability» = diferencia entre condiciones. Sin IC ni ejemplos.

**Petri** (Anthropic → Meridian Labs). Barras por dimensión con **IC 95 %** (`unprompted_whistleblowing`, `unprompted_deception_toward_user`…), ablación del whistleblowing (agencia, complicidad del liderazgo, realidad del delito) y un **visor de transcripts** con tres vistas (auditor / objetivo / observador), filtro por dimensión del juez y **citas resaltadas en naranja con resumen del juez en verde**. Es el estándar de «evidencia» para benchmarks conductuales.

**Anthropic, agentic misalignment / persona vectors**. Rejilla de condiciones con ✓ y ⚠ (control / amenaza / conflicto / ambas); citas del razonamiento del modelo en bloques indentados; «rates calculated out of 100 samples» bajo cada figura; transcripts como burbujas de chat con el rasgo inducido.

**Papers sin web** (patrones): **ELEPHANT** (tabla de pares *prompt / respuesta no sicofante / respuesta sicofante*: el «díptico» más pedagógico); **TRAIT** (perfiles de 8 rasgos con IC al 95 %, heatmap de intercorrelación); **PsychoBench** («media ± SD» del modelo frente a *crowd* humano, con test); **HumanAgencyBench** (barras por dimensión con error estándar; los autores **rechazan hacer leaderboard**); **MACHIAVELLI** (radar de daños + scatter Pareto «reward vs harms»); **Moral Machine en LLM** (**radar por familia con área gris = preferencia humana**, violines de «distancia a humanos», líneas por versión); **lechmazur/sycophancy** (columna «Insufficient» para no castigar la abstención).

### 3.3 Lo que se repite en los buenos

1. Una línea de **metadatos de incertidumbre siempre visible** bajo el título: n total, nº de modelos/labs, juez, fecha, versión.
2. **Empate estadístico explícito**: ± en celda, Rank Spread, rank por cota superior.
3. **Colores fijos por lab** en todos los gráficos, un solo acento, fondo claro (Arena, AA, Epoch, LiveBench, HumaneBench, Scale); el oscuro solo en propuestas temáticas (SnitchBench, ARC).
4. **Cada gráfico cuenta una cosa** y lleva su frase («Most attractive quadrant», «kill zone», «doom loop»).
5. Los conductuales que convencen **enseñan la evidencia**: transcript, cita resaltada, badge de conducta por escenario. Los que no (SnitchBench, HumaneBench) se quedan en curiosidad.
6. Nadie combina a la vez IC honestos + ejemplos crudos + linaje verificable. PsicoBench ya tiene lo tercero y lo primero; le falta lo segundo en la web.

---

## 4 · Propuesta de diseño

### 4.1 Decisiones de partida (recomendación)

- **Ruta propia, `/psicobench`**, como quinta superficie pública en `web/publicar.py` (`web/psicobench.html` + `web/js/psicobench.js` + `web/css/psicobench.css`). El panel técnico de `/benchmark` **se conserva** como «panel del instrumento» (es lo que regenera `generar_benchmark.py` y lo que auditan terceros); cuando la nueva superficie tenga paridad, `/benchmark` puede redirigir y el panel vivir en `/benchmark/panel`. Así se puede «ir probando» sin romper nada.
- **Misma regla que la web**: ninguna cifra ni texto de estímulo o de respuesta escrito a mano; todo sale de `generar_datos.py` (con `--check` en CI). Sin build, sin CDN, CSP `'self'`: SVG propio sobre las primitivas de `graficas.js`.
- **Estética**: fondo claro cálido (la familia de `index.html`, no el oscuro de la home), serif en titulares, **monoespaciada para `modelo@proveedor·fecha`** y metadatos, **paleta fija de 10 colores por lab** compartida por todos los gráficos, **una única escala secuencial** (crema → índigo) para «susceptibilidad» y **divergente solo para los Δ** (vacuna, aliado, sicofancia neta). Nunca verde = bueno / rojo = malo en los ejes: contradice la doctrina.
- **Página única con navegación fija** (anclas), no pestañas: los sitios que enganchan (AA, Vending-Bench, HumaneBench) son un scroll con jerarquía; las pestañas del panel actual esconden tres cuartas partes del contenido.
- **Idioma**: español, con los ids de modelo y las claves de eje estables; una versión EN es una fase aparte (todos los referentes son EN; sycophancy-eval resuelve el bilingüe con un toggle).

### 4.2 Guardarraíles de la doctrina, traducidos a diseño

| Doctrina | Regla de diseño |
|---|---|
| No es ranking de calidad | Sin medallas, sin «mejor/peor», sin verde/rojo; el copy dice «más/menos susceptible a X». Las tarjetas del hero se titulan por conducta («Quién cede a la mayoría»), no por «top» |
| Empate = no distinguible | Posición como **rango** («1–4»), como el Rank Spread de Arena; la tabla nunca muestra un «#1» solo |
| Se miden versiones, no nombres | Cada etiqueta lleva `@proveedor · fecha` en mono; las réplicas de la misma familia se dibujan unidas por una línea |
| IC y n siempre | En hover y en la tabla alternativa accesible; bigotes en todas las barras; «n=…» junto al eje |
| Missingness como dato | `n/c` visible como perfil fuera del ranking (hoy `qwen3.6`), con la razón en el tooltip |
| Contaminación en techo | Columna «Reconoce el paradigma» y ancla humana con caveat en el mismo bloque, nunca separadas del dato |
| Auditable | Cada gráfico tiene botón «tabla» y «JSON»; cada celda enlaza al id de run; línea de metadatos con sha corto del `linaje.json` |

### 4.3 Estructura de la página (nueve bloques, de arriba abajo)

**0 · Cabecera fija.** «PsicoBench v0.4 · 23 mediciones · 10 labs · 8 ejes · última medición 22-08-2026 · datos CC BY 4.0» + enlaces *Método · JSON · Repo · Citar*. (Patrón: Arena, sycophancy-eval, HLE.)

**1 · Hero: cuatro tarjetas con mini-barras.** Un titular («Cada modelo cede a la presión a su manera, y se puede medir») y cuatro tarjetas, una por conducta que engancha: *Quién cede a la mayoría* (conformidad), *Quién obedece* (obediencia), *Quién calla* (denuncia), *Quién te da la razón* (sicofancia de opinión). Cada tarjeta: mini-barras de las 23 mediciones ordenadas, color por lab, las tres más altas y las tres más bajas etiquetadas, y un enlace al bloque 3 de ese eje. (Patrón: tarjetas *Highlights* de Artificial Analysis.)

**2 · El mapa: heatmap modelo × eje.** 23 filas × 8 ejes + ISS + Δvac + Δaliado + Reconoce. Número en la celda; escala secuencial; cabecera pegajosa; **ordenable por cualquier columna** (por defecto ISS); filtros por lab (chips con el color del lab) y toggle **Mediciones | Labs** (agregado por lab con rango). Click en celda → ficha del modelo (bloque 7) con el eje resaltado. Sustituye a la tabla del panel como objeto central. (Patrón: HumaneBench + LiveBench *shading* + toggle de Arena.)

**3 · Ranking por eje.** Selector de eje (8 pestañas pequeñas, o las 8 apiladas); barras horizontales con **bigotes IC 95 %**, «n=» al pie, **rango de posición** en vez de puesto; **banda gris de referencia humana** donde existe (Asch ~33 %, Milgram ~65 %) con el caveat en la propia leyenda; un párrafo de dos líneas por eje que diga qué mide y qué modelo lo ilustra. (Patrón: Petri / HumanAgencyBench + área humana de Moral Machine + D13.)

**4 · Así suena: ejemplos por eje.** Para cada eje, un **díptico**: el estímulo exacto (ya extraído por AST) y dos respuestas reales de dos mediciones distintas, una que sostiene y otra que cede, con la frase clave resaltada y `modelo@proveedor·fecha` + id de run debajo. Selección **determinista y verificada** en `generar_datos.py` (p. ej. Milgram: la primera sesión que aplica en el nivel crítico y la primera que rehúsa, recorte con `LARGO_CRUDO` como en la consola). Los sujetos son personas ficticias del harness (decisión R1 de `PLAN_CORRECCION_WEB.md`), así que no hay problema de privacidad. (Patrón: ELEPHANT tabla 2, Petri citas, Vending-Bench transcripts.) **Es el bloque que ningún generalista tiene y el que más engancha.**

**5 · Comparador.** A vs B: radar superpuesto + tabla de deltas por eje + los dípticos del bloque 4 filtrados a esos dos modelos. Preajustes con nombre: *mismo snapshot, dos gateways* (deepseek 0731 OR vs NaN), *mismo nombre, dos fechas* (qwen 23-07 vs 04-08), *la familia Claude* (haiku / sonnet / opus / fable). Portado del panel actual. (Patrón: Aider checkboxes, Vals *Comparison*.)

**6 · Mapas con nombre.** Cuatro dispersiones, cada una con su frase y cuadrantes anotados en lenguaje llano: *Las dos obediencias* (obediencia vs disonancia, ya existe), *Los dos motores de crueldad* (provocabilidad vs órdenes, ya existe), *Cesión a iguales* (conformidad vs sicofancia, r=0,71: la estructura del índice hecha visible), *El nombre no es el modelo* (réplicas unidas por líneas con su d e IC). (Patrón: AA «Most attractive quadrant», MACHIAVELLI, Moral Machine.)

**7 · Fichas por medición.** Ruta por hash (`#m=gpt-5.6-luna`): radar solo, posición por eje como «k–k′ de 23», secundarias, reconocimiento, lista de runs con enlace al repo, nota (`ox-alpha` desvelado como GLM-5.3-Flash), y una **escalera v0.1→v0.4** de su ISS con IC. (Patrón: ficha de AA «#8 / 63» + banderas de evidencia de SWE-bench.)

**8 · Escalera de versiones.** *Bump chart* de posiciones v0.1→v0.2→v0.3→v0.4 para las 23 mediciones (la tabla puente, dibujada): enseña que el instrumento cambia y el ranking se mueve, y que se conserva el histórico. (Patrón: timeline de Epoch, adaptado: aquí la línea temporal es la del instrumento, no la de los lanzamientos.)

**9 · Método y doctrina.** «Qué NO es» (tal cual está), regla de empates, fiabilidad test-retest (las dos fichas de `/completo`), matriz de correlaciones, linaje y canary, cómo citar, **cómo añadir tu modelo** (`spike/alta.py`), descarga JSON/CSV.

### 4.4 Lo que se deja fuera a propósito

- Coste y velocidad (no son el foco y no están en el JSON público); si algún día entran, van en el bloque 6 como un mapa más, no en la tabla.
- Modo oscuro: opcional en una fase de pulido; los referentes serios son claros.
- Un visor de transcripts completo tipo Petri: el visor de replays (`/viewer`) ya existe para los episodios; para el benchmark basta el díptico + enlace al run. Un visor de sesiones de la batería sería una vía aparte del `ROADMAP.md`.

---

## 5 · Plan por fases (cada una publicable)

| Fase | Entrega | Depende de | Esfuerzo |
|---|---|---|---|
| **F0 · Esqueleto** | `web/psicobench.html/.js/.css`, pieza nueva en `publicar.py` y `sitemap.xml`, cabecera fija (bloque 0), **heatmap** (bloque 2) con orden y filtros, enlaces cruzados desde `/`, `/completo` y `/benchmark`; `smoke.mjs` cubre la ruta | Solo `datos.js` (ya tiene `benchmark.entradas`) | ½–1 día |
| **F1 · Enganche** | Hero con cuatro tarjetas (bloque 1) y **ranking por eje** con IC, n y rango de posición (bloque 3); anclas humanas si se decide D13 | Decisión sobre el caveat de las anclas | 1 día |
| **F2 · Evidencia** | Bloque `citas` en `generar_datos.py` (selección determinista desde `sesiones.jsonl` / `registros_carcel.jsonl`, verificada en `--check`), **dípticos por eje** (bloque 4) | Confirmar que se extiende a todas las mediciones el criterio que ya aplica la consola | 1–2 días |
| **F3 · Profundidad** | Comparador con preajustes (bloque 5), cuatro mapas con nombre (bloque 6), réplicas unidas | Nada nuevo (porta del panel) | 1 día |
| **F4 · Fichas** | Fichas por hash (bloque 7), escalera de versiones (bloque 8), método (bloque 9), descarga CSV, OG image de la página | Nada nuevo | 1 día |
| **F5 · Pulido** | Móvil, tablas alternativas y teclado en todos los gráficos, `--check` de la nueva salida, decisión sobre `/benchmark` → redirección o convivencia | F0–F4 | ½ día |
| **F6 · (opcional) EN** | Toggle ES/EN con las cadenas en `datos.js` | Traducción de ~60 cadenas + ejes | 1 día |

Orden de prioridad si solo se hace una parte: **F0 + F1 + F2**. El heatmap da la vista de conjunto, las tarjetas dan la entrada y los dípticos dan lo que ningún otro leaderboard ofrece.

### Decisiones (respuestas de David, 13-09-2026)

1. **Ruta**: `/psicobench` nueva **conviviendo** con el panel de `/benchmark`. Decidido.
2. **Anclas humanas (D13)**: **no** por ahora; esperar a la revisión externa. Las bandas de referencia quedan fuera de F1.
3. **Ejemplos crudos en la web**: **sí** (13-09). Al construirlo se comprobó que el harness solo guarda decisiones de una palabra (APLICO/RECHAZO, una letra, CALLO/DENUNCIO) y un juicio privado también de una palabra: **no hay frases que citar** salvo en la prisión (el supervisor narra lo que hace) y en la sonda de contaminación. El bloque se llama por eso «Así se ve una sesión» y publica, por medición, la **tira de decisiones de cada sujeto** paso a paso con su juicio privado debajo, más la descripción literal más dura de cada marco de la prisión y la respuesta literal a «¿te recuerda a algún experimento?». Dos mediciones lado a lado (díptico), selección determinista en `generar_datos.py`.
4. **Bilingüe**: **no** de momento. F6 se queda al final.

### Estado de ejecución (13-09-2026)

- **F0 hecha**: `web/psicobench.html`, `web/css/psicobench.css`, `web/js/psicobench.js`; ruta `/psicobench` en `publicar.py`, sitemap, smoke, puerta XSS y empaquetador; enlaces cruzados desde la home, el sitio largo y el panel del instrumento. El mapa: 28 filas ordenables, filtro y agrupación por laboratorio, rango de posición por grupo de empate, fila desplegable con IC y n por eje.
- **F1 hecha**: ranking por eje con IC 95 % (`G.barrasH`), prosa y cifras derivadas por eje. Sin anclas humanas (decisión 2). **Corrección tras la revisión de David (13-09)**: las cuatro tarjetas del hero con mini-barras sin nombre «no se entendían»; se sustituyen por la opción de pestañas: un solo gráfico con una pestaña por forma de presión (las cuatro de titular primero: quién sigue a la mayoría, quién obedece, quién calla, quién te da la razón; luego los cuatro marcos de la prisión) y todas las mediciones con nombre e intervalo. El bloque pasa a ser el 01, justo debajo de la portada, y el mapa el 02.
- **F2 hecha**: bloque `sesiones` en `generar_datos.py` (+~260 kB en `datos.js`, que cargan también la home y el sitio largo) y el bloque «Así se ve una sesión» con seis pruebas (Milgram, Asch, denuncia, sicofancia, los cuatro marcos de la prisión, la sonda).
- **F3 hecha** (13-09, misma tarde): la sección «Cara a cara» reúne el radar A/B superpuesto (`G.octogono`), la tabla de deltas por eje con la regla «distinguible = IC disjuntos», los preajustes derivados de `replicas` (más «menos ↔ más índice») y las sesiones; sección «Mapas con nombre» con tres dispersiones de cuadrantes anotados (las dos obediencias, los dos motores de crueldad, cesión a iguales) y «El nombre no es el modelo» (distancias entre réplicas con IC y el suelo de ruido de `identidad`).
- **F4 hecha**: ficha por medición con dirección propia (`#m=id`: la abren los puntos de los mapas, la escalera, el detalle del mapa y la cabecera de cada sesión), con perfil, lectura eje a eje frente al banco (cuántas ceden más/menos y cuántas no son distinguibles), secundarias, tabla puente propia, runs enlazados (`rutas` nuevas en `sesiones`) y botones para llevarla al cara a cara; «Escalera de versiones» (slopegraph v0.1→v0.4 con IC, resalte por línea, tabla alternativa); descarga CSV desde los mismos datos (`versiones`, `nota` y `desvelado` nuevos en `datos.js`).
- **Revisión de David (13-09, segunda ronda)**: (1) el mapa era demasiado ancho y obligaba a scroll lateral en pantallas normales → cabeceras a dos líneas, ids largos que se parten, celdas más estrechas: la tabla cabe en el marco a 1280 px; (2) fuera los preajustes del cara a cara, que cada uno elija; (3) el ISS pasa a ser el bloque 01, con explicación de qué es (media jerárquica por paradigma, cuatro componentes de un cuarto cada uno) y el ranking de las 28 mediciones **apilado por componentes** (cesión a iguales, obediencia, abuso de poder, silencio), con IC y grupo de empate. La descomposición se recalcula desde los ejes publicados y solo se dibuja si cuadra con el ISS publicado (guardia en el smoke): si el instrumento cambia de fórmula, la web no dibuja una descomposición falsa.
- Pendientes: F5 (pulido, OG image propia de la página, decidir si `/benchmark` redirige). Deuda conocida: `datos.js` ha doblado de tamaño; si molesta en la home, dividir por página (M1 de `PLAN_CORRECCION_WEB.md`).

---

*Fuentes visitadas el 13-09-2026*: arena.ai/leaderboard/text · artificialanalysis.ai (home, /leaderboards/models, /models/claude-opus-4-5) · labs.scale.com/leaderboard (+/mask, +/propensitybench) · huggingface.co/docs/leaderboards/open_llm_leaderboard/about · andonlabs.com/evals/vending-bench y /vending-bench-2 · sycophancy-eval-smoky.vercel.app · github.com/imaknas/sycophancy-eval · snitchbench.t3.gg y snitchbench.com/methodology · humanebench.ai · github.com/sam-paech/spiral-bench · github.com/lechmazur/sycophancy · arxiv.org/html/2505.13995 (ELEPHANT) · arxiv.org/html/2406.14703 (TRAIT) · github.com/CUHK-ARISE/PsychoBench · github.com/BenSturgeon/HumanAgencyBench · aypan17.github.io/machiavelli · journals.plos.org/plosone/article?id=10.1371/journal.pone.0322776 (Moral Machine) · anthropic.com/research/persona-vectors · anthropic.com/research/agentic-misalignment · alignment.anthropic.com/2025/petri · epoch.ai/benchmarks · livebench.ai · github.com/swe-bench/swe-bench.github.io · aider.chat/docs/leaderboards · vals.ai · metr.org/time-horizons · arcprize.org/leaderboard · lastexam.ai · help.kagi.com/kagi/ai/llm-benchmark.html.
