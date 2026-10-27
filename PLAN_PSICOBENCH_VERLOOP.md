# Plan · rediseño de `/psicobench` en la línea «Verloop»

**Fecha**: 24-10-2026 (aprobado el 25-10-2026) · **Estado**: en implementación, **fases 0 a 5 hechas; falta tu validación (y Safari/Firefox a mano)** · **Rama**: `feature/psicobench-verloop` (desde `main`; el repo no tiene `develop`) · **Diseño de referencia**: lienzo «BenchAI · tres direcciones», pizarra *PsicoBench · /psicobench en la línea Verloop* con la portada «Lámina A · Morph» (octógono de un solo modelo, animado).

**Qué se rediseña**: solo la superficie `/psicobench`. La home (`/`) y el sitio largo (`/completo`) no se tocan en esta rama; si la dirección gusta, se extiende después con los mismos tokens.

**Qué no cambia**: ni una cifra. Todo sigue saliendo de `benchmark/psicobench.json` → `web/generar_datos.py` → `datos.js`; la doctrina (medición ≠ modelo, empates por IC, n/c, «no es un ranking de calidad») y las ocho secciones se conservan tal cual. Las primitivas de `web/js/graficas.js` (`figura()` con tabla alternativa, `globo`, `navegable`, formato español) se reutilizan y, donde haga falta, se extienden con opciones; no se bifurcan.

**Regla de despliegue**: la versión nueva **no se publica** en benchai.tech hasta que esté validada entera. Hasta entonces vive en paralelo a la vigente y solo se ve en una previa (§2). El cambio a producción es un paso aparte, con su propio PR (§7).

---

## 1 · Lo que define la dirección (resumen visual)

| Elemento | Hoy | Verloop |
|---|---|---|
| Fondo | Carbón cálido / crema | Negro `#07070A`, cajas `#0F0E14`, bordes `#2A2833` |
| Display | Condensada en mayúsculas | **Big Shoulders Display 900**, mayúsculas, interlineado **0,94** (0,86 en el lienzo; en navegador las tildes de las mayúsculas tocaban la línea de arriba) |
| Texto / etiquetas | Sans + mono | **Inter Tight** (cuerpo) + **JetBrains Mono** (etiquetas, cifras tabulares) |
| Color de datos | Una «escala de dureza» única | **Un tono por eje** (8 tonos espectrales) con saturación = valor; negro = cero. ISS en gradiente cian → violeta → magenta → naranja |
| Portada | Hero + panel del ISS | **Lámina A · Morph**: columna de copy a la izquierda (titular a 118 px, párrafo, CTAs, contadores) y, a la derecha, el octógono a media página con **un solo modelo** sobre los 39 perfiles finos. **Animado**: al cambiar de modelo el perfil se transforma (los ocho vértices se interpolan en 900 ms, el ISS cuenta hasta el nuevo valor, el halo y el borde cambian al color del ISS) y una onda circular sale del centro con un destello del polígono; el nombre entra con un barrido. Al pasar por un eje, su etiqueta se desplaza y crece, el radio toma el color del eje, el vértice se agranda, el sector se ilumina y la lectura (nombre, paradigma, definición, valor con IC y n) entra deslizándose. Modelo anterior/siguiente con botones o pulsando un perfil fino |
| Textura | Ninguna | Grano (feTurbulence) al 22 % en modo overlay sobre portada y paneles de color |
| Gráficas | Serif claro, denso | Mismas gráficas; barras con gradiente, bigotes blancos, octógono con halo difuminado, mapas con cuadrantes rotulados |

---

## 2 · Despliegue en sombra: cómo se mantiene fuera de producción

Producción solo se publica desde `main`: `.github/workflows/desplegar.yml` corre tras la CI verde de un push a `main` y despliega el paquete de lista blanca de `web/publicar.py`; los despliegues automáticos de Git en Vercel están apagados (`vercel.json`). Sobre eso, tres capas:

1. **La rama no se fusiona con `main` hasta el cambio.** Todo el trabajo de las fases 1–5 vive en `feature/psicobench-verloop`. La rama **no tiene upstream** configurado, así que un `git push` sin argumentos no puede ir a `main` por accidente. Para no divergir de las altas de modelos que lleguen a `main`, se trae `main` a la rama (`git merge origin/main`) al empezar cada fase.
2. **La página nueva vive en paralelo a la vigente.** `web/psicobench.html` no se toca. La nueva es `web/psicobench-verloop.html` (`noindex, nofollow`, canónico a `/psicobench`, aviso visible de «versión en preparación»), con sus piezas en `web/verloop/` y las fuentes en `web/fonts/`. Ninguna de las tres rutas está en la lista blanca del paquete de producción.
3. **Guarda en el paquete.** `publicar.py` se para si alguna pieza de la previa aparece en `publicacion/` (`_sin_previa`), y `--check` lo comprueba en CI. Así, aunque la rama se fusionara por error, la página nueva no saldría.

**La previa** (lo único que enseña la versión nueva):

```bash
python3 web/publicar.py --previa      # publicacion-previa/ (ignorada por git)
python3 web/servir_previa.py          # http://127.0.0.1:8743/psicobench-nueva
```

Es el paquete de producción más `/psicobench-nueva`, `verloop/` y `fonts/`, con un `robots.txt` que cierra todo. `servir_previa.py` sirve rutas limpias como `cleanUrls` de Vercel y manda `Cache-Control: no-store` para que cada `--previa` se vea al recargar. En `.claude/launch.json` queda como servidor «previa».

**Previa compartible** (opcional, solo con tu OK en cada ocasión): un despliegue de Vercel **sin `--prod`** del directorio `publicacion-previa/`, enlazado al proyecto existente con las variables de `desplegar.yml` (`VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`). Da una URL `*.vercel.app` que no se asigna al dominio; Vercel añade `X-Robots-Tag: noindex` a las previews y el `robots.txt` de la previa lo refuerza.

---

## 3 · Restricciones del proyecto que condicionan la implementación

1. **Sin terceros.** El pie dice «este sitio no usa cookies, analítica, formularios ni terceros» y la CSP es `font-src 'self'`. Las fuentes se autoalojan (hecho en la fase 0, ver §4).
2. **Ninguna cifra a mano.** Contadores, perfiles, colores por ISS y lecturas se calculan en el JS desde `B.entradas`. `verificar.sh` y los `--check` de CI deben seguir en verde.
3. **Accesibilidad como está hoy.** Cada `figura()` conserva su tabla alternativa y la navegación por teclado. Contrastes WCAG sobre `#07070A`, medidos: blanco 20,1:1, `#C9C6D4` 12,0:1, `#9A97A6` 7,0:1, `#6F6C7A` 3,9:1 (solo decorativo o ≥ 24 px). Los ocho tonos de eje pasan 4,5:1 sobre negro salvo **Obediencia `#7B3DFF` (3,8:1)**: vale para barras, rellenos y texto ≥ 24 px, nunca para texto pequeño. Celdas de calor con texto negro cuando la saturación supera 0,5. El texto con `-webkit-text-stroke` («a su manera.») lleva relleno de respaldo.
4. **Móvil a 320 px y táctil** (segunda pasada de la revisión web, PR #28): titulares sin guiones automáticos (`hyphens: manual`, solo se parte una palabra que no cabe entera); chips y botones de 44 px; la tabla del mapa mantiene el scroll horizontal con el aviso actual; el halo se desactiva por debajo de 768 px.
5. **Rendimiento.** El grano es un único `<rect>` con filtro y `pointer-events: none`; el halo se dibuja una vez por cambio de modelo, no por hover. Los 39 polígonos del octógono y las 39 polilíneas de la escalera son vectores ligeros; no se añaden librerías.
6. **Ramas.** El repo trabaja con ramas que van a `main` por PR (no hay `develop`). Esta rama sigue el nombre del plan, `feature/psicobench-verloop`, y solo llega a `main` en el cambio (§7).

---

## 4 · Fases (cada una revisable por sí sola en la previa)

### Fase 0 · Preparación — **hecha (25-10-2026)**
- Rama `feature/psicobench-verloop` desde `origin/main` en el worktree `.claude/worktrees/psicobench-verloop`, sin upstream.
- **Fuentes** en `web/fonts/`: subconjuntos variables woff2 generados con fontTools desde los TTF de `github.com/google/fonts` (latín, latín extendido A, puntuación, flechas, formas geométricas y los símbolos `× − ≈ ≤ ≥`). Big Shoulders Display 2.002 (eje 100–900, 56 KB), Inter Tight 3.004 (100–900, 69 KB, con `tnum`), JetBrains Mono 2.211 (100–800, 46 KB): **171 KB en total**. Ninguna declara nombre reservado; la OFL de cada una va junto a su fichero y la tabla de `THIRD_PARTY_NOTICES.md` las recoge. El subconjunto latín de Google Fonts se descartó porque no trae la flecha → que usan todos los enlaces del diseño. Ninguna de las tres tiene ⇄: el diseño usará ↔.
- **Tokens** en `web/verloop/tokens.css`: `@font-face`, variables de color, tipografía, ritmo y utilidades (`.v-big`, `.v-mono`, `.v-num`, `.v-caja`, `.v-chip`, `.v-btn`, `.v-trazo`, `.v-grad-texto`), todo bajo el prefijo `--v-` / `.v-` para que no choque con `estilo.css`.
- **Esqueleto** `web/psicobench-verloop.html`: misma CSP que la vigente, `noindex`, aviso de versión no publicada, muestras tipográficas y de color. Validado en la previa local: las tres familias cargan con la CSP, sin errores de consola, enlaces reescritos a `/`, `/completo` y `/psicobench`, bien a 1440 y a 320 px. La prueba destapó dos fallos ya corregidos: el botón relleno perdía el texto (la regla de color de los enlaces le ganaba en especificidad) y `hyphens: auto` partía «PRE-SIÓN».
- **Previa**: `publicar.py --previa`, guarda `_sin_previa`, `web/servir_previa.py`, `publicacion-previa/` en `.gitignore`, servidor «previa» en `.claude/launch.json`. El test anti-XSS estático incluye la página nueva (sus `.js` ya entraban por el barrido de `web/`).
- **Capturas de referencia** de la página vigente en producción, de página completa: `docs/verloop/antes/psicobench-{1440,390,320}.jpg`. Se toman por tramos de ventana, porque la portada actual se dimensiona con `vh` y estirar la ventana la deformaba.
- Comprobado: paquete de producción construido y al día (`--check`), sin piezas de la previa; ningún fichero de la lista blanca cambia frente a `main`; `marcado.prueba.cjs`, `generar_datos.py --check` y `test_xss_estatico.py` en verde.

### Fase 1 · Tokens y base — **hecha (25-10-2026)**
- **Desviación del plan, a mejor**: no hace falta una paleta `G.PAL.verloop` ni una opción `relleno` en `graficas.js`. La biblioteca no escribe colores —los pide a variables CSS (`--s1…--s4`, `--o1…--o4`, la escala `--e0…--e9`, `--tinta`, `--reja`…)— y mide las etiquetas con `--sans` y `--mono` de `:root`. Así que el tema entero va en CSS y `/`, `/completo` y la `/psicobench` vigente no cambian.
- **Registro Verloop** en `web/verloop/psicobench.css`, encima de `estilo.css` y `psicobench.css` (que siguen dando la estructura): un solo registro negro en lugar de grafito/papel, escala espectral `--e0…--e9` (frío y apagado → caliente y encendido; texto blanco en e0–e1 y negro de e2 en adelante, todo ≥ 4,5:1), series A cian / B magenta, familias nuevas en `:root`, cabeceras de sección con el número grande del color de su bloque, botones y chips en píldora, cajas de 4 px y grano en la portada. Gana por especificidad (`body.verloop`, `.verloop section:nth-of-type(…)`), sin `!important`.
- **`graficas.js`**: un único cambio, la opción `halo` del octógono (copia difuminada bajo cada perfil, con su `<filter>` por figura), apagada por defecto. Es el único fichero de la lista blanca de producción que cambia en la rama.
- **`web/verloop/psicobench.js`**: copia de trabajo del original con dos diferencias, anotadas en su cabecera: los dos octógonos piden `halo`, y al cargar las fuentes autoalojadas se redibujan todas las figuras (el canvas que mide las etiquetas no las pide por sí mismo).
- **`web/psicobench-verloop.html`**: ya es la página completa, generada desde la vigente; solo cambian la cabecera (`noindex`, hojas Verloop), la clase `verloop` del `body`, el aviso flotante de previa (franja inferior en móvil) y el guion de la copia de trabajo.
- **`publicar.py`**: la previa reescribe también el `REPO()` de la copia de trabajo, con la misma función que el original (`_reescribir_repo_js`).
- Ajuste en `tokens.css`: la regla de color de los enlaces se limita a los enlaces sin clase, para no pisar chips ni botones.
- Comprobado: `smoke.mjs` en verde contra la previa local para `/`, `/completo`, `/psicobench`, `/benchmark` y `/viewer` (con el `graficas.js` nuevo); en `/psicobench-nueva`, las 9 figuras dibujadas, los 39 perfiles del mapa, los halos en los dos octógonos, las tres familias cargadas, sin errores de consola y sin desborde horizontal a 390 px; paquete de producción al día, marcado, datos y XSS estático en verde.

### Fase 2 · Portada «Lámina A · Morph» — **hecha (25-10-2026)**

Lo construido, y dónde se apartó de lo previsto (debajo, el plan original):
- **`G.octogono()`** con las opciones `fondo`, `cunas`, `animar`, `anchoMax`, `radioMax`, `tipoEtiqueta`, `claseEtiqueta`, `cortos`/`anchoCortos` y `e.largo`, todas apagadas por defecto: sin ellas el código sigue el camino de siempre, y el smoke de las cinco páginas de producción pasa. En modo lámina los nodos del perfil son persistentes y se actualizan en su sitio (el color transiciona) y la primera vez el perfil crece desde el centro.
- **El eje activo sale del ángulo del puntero** sobre el SVG, no de sectores encima: unos sectores encima habrían tapado el clic a los 39 perfiles finos. Los sectores siguen existiendo como paradas de teclado (`navegable`: el SVG es una parada y las flechas recorren los ocho ejes), con su valor en `aria-label` y el nombre completo del eje.
- **Los perfiles finos son solo de puntero** (`aria-hidden`), con zona de golpe de 8 px y `<title>`: 39 paradas de tabulador serían un muro. Con teclado se cambia de medición con los botones ◀ ▶ (44 px).
- **Medición de arranque**: la de `#m=<id>` si viene en la dirección; si no, la mediana del banco por ISS (un perfil con forma, ni el más plano ni el mayor).
- **Hash compartido en los dos sentidos** (decisión 2): la lámina escribe `#m=<id>` con `replaceState` y repinta la ficha; el selector de la ficha y un cambio de hash mueven la lámina.
- **Tamaño**: el radio sale del ancho y también de la altura de la ventana, para que lámina y tarjetas se vean enteras sin bajar (medido a 1440×900, 1280×800, 1366×768 y 1920×1080); por debajo de 560 px los rótulos pasan a una palabra («CONF.», «OBED.»…) y el radio crece de ~70 a 113 px a 390 px. La lámina se alinea arriba de la portada.
- **Animaciones**: interpolación de 900 ms (`easeOutCubic`) por `requestAnimationFrame`, contador del ISS en paralelo, onda y destello que se retiran a los 1,3 s, nombre con barrido, lectura que sube; hover con rótulo que sale y crece, radio del color del eje, sector iluminado y vértice de 9 px. Con `prefers-reduced-motion`, todo instantáneo y sin onda.
- **Prueba**: `web/previa_lamina.prueba.mjs` (Chrome headless, sin dependencias) comprueba 18 puntos: estructura, 9 formas intermedias en un cambio, contador, onda, hash y ficha, hover real, teclado y anuncio, clic en un perfil, arranque desde `#m=`, movimiento reducido y consola sin errores. El panel del navegador integrado, oculto, da 2 fotogramas por segundo y no sirve para medir la animación.

Plan original:
- Bloque `#portada` en dos columnas: copy (eyebrow, `<h1>` con `clamp(64px, 8.2vw, 118px)`, párrafo, CTAs, contadores con los ids actuales `#n-labs`, `#n-ejes`, `#ultima-medicion`) y la lámina.
- **La lámina reutiliza `G.octogono()`** con tres opciones nuevas más, desactivadas por defecto (`halo` ya existe desde la fase 1): `fondo: "perfiles"` (las 39 polilíneas finas coloreadas por ISS, pulsables), `cunas: true` (ocho sectores invisibles por eje que emiten `hover`/`focus` con el índice) y `animar: true`. El tooltip (`globo`) se amplía a una **lectura fija** bajo la gráfica: nombre y paradigma del eje, definición, valor con IC y n.
- **Animación de cambio de modelo** (`animar: true`): interpolación de los ocho vértices con `requestAnimationFrame` (900 ms, `easeOutCubic`), contador del ISS en paralelo, onda circular y destello del polígono por remontado de nodo, nombre con barrido. Con `prefers-reduced-motion`: cambio instantáneo.
- **Animación de eje**: transiciones CSS sobre `transform` de la etiqueta, `stroke` del radio, `r` del vértice y `fill-opacity` del sector; la lectura entra con `fadeup`.
- **Cambio de modelo**: botones anterior / siguiente (por ISS) y clic sobre un perfil fino (`tabindex="0"` + Enter, zona de golpe de 8 px). El modelo elegido va al hash `#m=<id>`, el mismo de la ficha.
- Teclado y lectores: cada sector de eje es focusable y anuncia la lectura en `aria-live="polite"`.
- El panel flotante del ISS (`#panel-indice`) no pasa a la versión nueva: lo sustituye la tarjeta del modelo.

### Fase 3 · Secciones 01–08, estilo y gráficas — **hecha (26-10-2026)**

Lo construido, y dónde se apartó de lo previsto (debajo, el plan original):
- **Un solo origen de color en la copia de trabajo**: `TONO` (un tono por eje, más «gris» para lo que no entra en el índice), `TONO_TEXTO` (el violeta de obediencia aclarado a `#A98BFF` para texto pequeño), `colorISS` (antes vivía dentro de la lámina) y `tonoEje(eje, v)`, que mezcla del fondo de celda `#15141C` al tono con curva de raíz (`0,3 + 0,7·√v`): el banco vive entre 0 y 50 y una mezcla lineal ahí salía turbia. La tinta encima se elige por contraste; el peor caso de todos los ejes y valores es 4,59:1. La escala espectral única (`peldano`, clases `p0–p9`) deja de usarse en esta página; `graficas.js` no se toca en esta fase.
- **Cabeceras**: rejilla de tres columnas solo desde 1000 px (número y rótulo, título, entradilla); por debajo, como antes.
- **01**: componentes con color fijo (`--v-comp-*`), bigotes blancos en todas las gráficas, y cada tarjeta con una barra del rango que ocupa ese componente en el banco.
- **02**: pestaña, titular de la prosa y cifras en cajas con el tono del eje; las barras, en el tono del eje y más intensas cuanto más cede. El pie ya no habla de «escala de dureza».
- **03**: cada columna con su tono (filete superior en la cabecera y celdas), «reconoce» en gris y separada; leyenda nueva con la rampa y los nueve tonos.
- **04**: «sí» en lima; las tiras toman el tono de la prueba (Milgram, obediencia; Asch, conformidad…), con el punto negro centrado para «en privado la cree injusta»; en la prisión cada día va en el tono de su marco y el punto pasa a la esquina, porque la casilla lleva su número.
- **05**: puntos por ISS (y el ISS en el globo), cuadrantes en mono gris, suelo de ruido de las réplicas en lima discontinua.
- **06**: la hoja lleva el filete y la cifra del ISS en el color de su medición (gradiente de texto desde el cian, 76 px), el octógono también; eje a eje con la cifra y el punto en el tono del eje; secundarias en tarjetas.
- **07**: líneas, puntos y etiquetas en el color del ISS vigente; la separación entre etiquetas ya era de 12,5 px.
- **08**: las cuatro notas del método en cajas numeradas y el aviso «Qué NO es» ocupando dos columnas; el pie ya tenía tres columnas y solo cambia la tipografía de sus títulos.
- **Comprobado**: sin desbordes horizontales de 320 a 1920 px (los 2 px de un texto de SVG a 320 px ya están en la página vigente y no dan scroll), y la batería completa de §2 en verde.

Plan original. Orden de trabajo, de menos a más riesgo:
1. **Cabeceras de sección** (número grande a color + título + párrafo en rejilla de tres columnas) y cajas: solo CSS.
2. **01 El índice**: barras apiladas con los cuatro componentes en gradiente y bigote blanco; tarjetas de componentes con borde superior de color.
3. **02 Quién cede**: chips de eje con borde superior de su tono; panel de cabecera con las cuatro cifras; ranking con bigotes.
4. **03 El mapa**: celdas de calor con el tono del eje, columna «reconoce» en gris; filtros con conteo. Se actualiza la leyenda: ya no es «un solo color para toda la web».
5. **04 Cara a cara**: octógono con halo, tabla de deltas con «sí» en lima; tiras de sesión con el punto negro para «lo juzga injusto».
6. **05 Mapas con nombre**: cuadrantes en mono gris; puntos coloreados por ISS; réplicas con suelo de ruido en lima discontinua.
7. **06 Ficha**: ISS en gradiente de texto (solo cifras ≥ 40 px), diez secundarias en tarjetas, eje a eje con la cifra en el tono del eje; arranca en el modelo del hash `#m=`.
8. **07 Escalera de versiones**: líneas coloreadas por ISS v0.4 y etiquetas a la derecha con separación mínima de 11,5 px.
9. **08 Método** y pie en tres columnas.

### Fase 4 · Interacción, móvil y estados — **hecha (26-10-2026)**

Lo construido, y dónde se apartó de lo previsto (debajo, el plan original):
- **Prueba nueva, `web/previa_interaccion.prueba.mjs`** (Chrome headless, sin dependencias, como la de la lámina): 46 comprobaciones. Cubre `#m=` en los dos sentidos (dirección → ficha y lámina; selector de la ficha → dirección; un id desconocido no rompe), A/B con intercambio y «…como B» desde la ficha, las seis pruebas de sesión con su tono, las ocho pestañas de eje, la reordenación por cabecera en los dos sentidos, el filtro por laboratorio, «Todos» y agrupar, la fila desplegable, el CSV (cabecera y 39 filas, leído del propio blob) y el enlace al JSON, la barra de progreso y la sección activa del menú, 390 y 320 px (sin scroll horizontal, mapa desplazable en su caja, sin halo, método a una columna), el toque en táctil y los tres estados (movimiento reducido, más contraste, impresión con su PDF). Todo pasaba salvo lo táctil.
- **Dos fallos táctiles de la lámina, corregidos en `graficas.js`** (solo afectan al modo lámina, que solo usa la página nueva): al levantar el dedo llegaba `pointerleave` y la lectura del eje se apagaba en el acto (ahora solo apaga la salida del ratón); y un toque para leer un eje caía casi siempre en alguno de los 39 perfiles finos y cambiaba de medición sin querer (ahora, con el dedo, se cambia con ◀ ▶, de 44 px; el clic de ratón sigue eligiendo perfil).
- **Más contraste**: además del grano, fuera resplandores, cristal y el texto hueco del titular; textos secundarios y líneas más claros.
- **Impresión, que la página vigente no tiene**: registro claro (también los tokens propios, o los enlaces salían en blanco), `color-scheme: light` (con `dark` Chrome pinta de negro los márgenes de la hoja), sin barra, aviso, mandos ni botones, cada sección en hoja nueva, gráficas al ancho de la hoja y nunca más altas que ella (un SVG no se parte y, si no cabe, se pisa con lo que sigue), mapa compacto y la cifra de sección con interlineado 1 (con 0,8 se salía de su caja y dejaba una hoja casi en blanco). Sale en 24 hojas A4.
- **Titular a 44 px en móvil, no a 64**: a 390 px, 64 px son ocho líneas y empujan la lámina dos pantallas abajo; 44 px son cinco y se lee de un vistazo.
- **Falsa alarma documentada**: los enlaces relativos al repositorio (`../BENCHMARK.md`) dan 404 en el dominio si se piden tal cual, pero `publicar.py` ya los reescribe a GitHub al empaquetar; en la previa y en producción funcionan.

Plan original:
- Comprobar que sobreviven: hash `#m=`, selectores A/B e intercambio, reordenación por cabecera y filtros de laboratorio, descarga CSV/JSON, progreso de lectura.
- Móvil 390 y 320: titular a 64 px, rejillas a una columna, tabla con scroll, halo desactivado.
- `prefers-reduced-motion`, `prefers-contrast: more` (quitar grano), impresión.

### Ajuste de la portada en dos bloques — **hecho (27-10-2026)**, a petición tuya tras la fase 4
Al ver el esqueleto de la fase 0 (titular solo, a todo el ancho) preferiste esa portada a la de dos columnas. La portada se parte en dos bloques para que cada uno respire:
- **`#portada`**: ceja, titular a todo el ancho (`clamp(52px, 8,2vw, 128px)`, 118 px a 1440), entradilla y botones; el resplandor pasa a ocupar todo el ancho (dentro del marco se le veían los bordes).
- **`#perfil`** (`.lamina-bloque`), justo debajo: las cuatro cifras en una franja grande y, debajo, el octógono a un lado y las dos tarjetas (medición y lectura del eje) al otro. Por debajo de 940 px, una columna; por debajo de 520 px, las tres cifras en fila y la fecha en la suya. El radio del octógono crece (tope 280 px) porque ya no comparte alto con las tarjetas. JS, ids y comportamiento de la lámina no cambian; la prueba de la lámina la trae a la vista antes de usar el ratón.
- Esto deja sin efecto el «titular a 44 px en móvil» de la fase 4: con la lámina en su propio bloque, el titular vuelve a crecer (52 px a 390).

### Ajustes del 27-10 (tras ver la portada en dos bloques)
- **La lámina es la ficha entera**, con una flecha en cada extremo (en estrecho, arriba en las esquinas). Al pulsarla, **el «chasquido»**: la escena se borra con una máscara desde el lado pulsado mientras lo que se ve se deshace en polvo que vuela hacia ese lado; a mitad cambia la medición (sin morph) y entra desde el lado contrario, enfocándose. El polvo no rasteriza el DOM: se muestrea de la geometría y los textos en pantalla (trazos y relleno del perfil, los 39 finos, la rejilla, los rótulos, los textos y el borde de la caja, cada grano con su color; tope de 9000) y se pinta en un lienzo encima. Un segundo clic espera su turno. Con el dedo, deslizar la ficha hace lo mismo (a la izquierda, la siguiente). Con movimiento reducido, cambio instantáneo. El clic en un perfil fino, la ficha y la dirección siguen con el morph. `graficas.js` gana `op.sinAnimar` en el modo lámina.
- **Fuera la sección 07, «Escalera de versiones»** (confundía más que aportaba); el método pasa a ser la 07 y el menú pierde «Versiones». La tabla puente sigue en la ficha de cada medición.
- **Fuera el mapa «El nombre no es el modelo»** (28-10): la sección 05 queda en tres cruces, en fila desde 1180 px; los rótulos de cuadrante pasan a mono de 10 px sin espaciado, que es lo que mide `dispersion` al repartirlos (a 10,5 px con espaciado se pisaban en las columnas estrechas). La doctrina «se miden mediciones, no modelos» sigue en el método.
- **Las notas sueltas de cada sección van a todo el ancho** (la de «Posición.» bajo la clasificación ocupaba seis líneas en la medida de lectura).
- Pruebas: la de la lámina comprueba el chasquido (máscara, polvo pintado, cambio a mitad, limpieza y cola de dos clics con vuelta al final); la de interacción, el deslizamiento táctil.

### Fase 5 · Validación completa — **hecha (28-10-2026), salvo lo que es tuyo**

Resultados, sobre la rama con `main` fusionado (incluye `/personalidad`, PR #32):
- **`main` traído a la rama** (36 commits; un conflicto en la lista HTML del test XSS) y portado a la copia de trabajo lo que `main` cambió en la página vigente: conmutador de cuatro lecturas, pie y la línea de personalidad en la ficha. `publicar.py --previa` reescribe también `personalidad.html` → `/personalidad`.
- **Smoke** con `--previa`: aserciones nuevas para `/psicobench-nueva` (noindex y aviso, lámina con 39 perfiles y 8 sectores, flechas y lienzo, cifras, componentes y fórmula del ISS, pestañas y barras, celdas en tono = valores > 0, radar A/B, deltas, sesiones, tres mapas y 3 × 39 puntos, ficha y su línea de personalidad, sin escalera, siete secciones, la flecha arranca el chasquido). Sin `--previa`, el smoke contra producción no cambia. **7/7 rutas OK.**
- **`verificar.sh` completo: PUERTA COMPLETA OK.** También `publicar.py --check`, `generar_datos.py --check`, `marcado.prueba.cjs`, test XSS, prueba de la lámina (25 comprobaciones) y de interacción (47).
- **Lighthouse no está instalado** y descargarlo es tu decisión; en su lugar, una auditoría propia por CDP con el perfil móvil de Lighthouse (412 × 823, CPU × 4, «slow 4G») y sus curvas de puntuación, **aproximada**: primero dio 74–82 (TBT 495–959 ms, CLS 0,143 por el cambio de fuente del titular) frente a 90 de la vigente. Arreglos: las tres fuentes **precargadas** y sin redibujar las gráficas si ya estaban → **CLS 0, TBT 300–400 ms, nota aproximada 86–90**. Accesibilidad: sin fallos de estructura (lang, título, ids, nombres, alt, h1 y saltos de título) ni interactivos sin nombre en el árbol de accesibilidad; **contraste: 0 textos por debajo del mínimo** de 1126, tras dos arreglos (celdas con negro puro, 4,59:1 en el peor caso; titular hueco con color transparente).
- **Cruzado**: Chrome de escritorio y Android emulado (390, 320 y táctil) automatizados. **Firefox** (158, instalado) no abre su puerto de WebDriver BiDi en este equipo ni termina en modo `-screenshot`, y **Safari** necesita activar la automatización remota con permisos de administrador: los dos quedan para tu revisión a mano (puntos a mirar: máscara del chasquido, `color-mix` en el borde de la ficha, `backdrop-filter`, el texto hueco y el lienzo del polvo).
- **Capturas «después»** en `docs/verloop/despues/` a 1440, 390 y 320.

Plan original:
- `web/smoke.mjs` contra la previa local, con aserciones nuevas para `/psicobench-nueva` (lámina con 39 perfiles y 8 sectores, cambio de modelo, lectura de eje, ocho secciones con sus tablas).
- `marcado.prueba.cjs`, `generar_datos.py --check`, `publicar.py --check`, `test_xss_estatico.py`, `verificar.sh`.
- Lighthouse sobre la previa: accesibilidad ≥ 95, sin errores de contraste; rendimiento en móvil ≥ 85.
- Cruzado en Safari (`mix-blend-mode`, `backdrop-filter`), Firefox y Chrome Android.
- Capturas «después» en `docs/verloop/despues/` a 1440, 390 y 320, frente a las de la fase 0 y a la pizarra del lienzo.
- **Tu validación** sobre la previa (local o compartible). Solo con tu visto bueno se pasa al §7.

**Estimación total**: 8 días de trabajo efectivo, cada fase revisable en la previa.

---

## 5 · Archivos afectados

| Archivo | Hasta el cambio | En el cambio (§7) |
|---|---|---|
| `web/psicobench-verloop.html` | **Nuevo**, solo en la previa | Pasa a ser `web/psicobench.html` |
| `web/verloop/tokens.css` (fase 0), `web/verloop/psicobench.css`, `web/verloop/psicobench.js` (fase 1) | **Nuevos**, solo en la previa | Entran en la lista blanca |
| `web/fonts/*.woff2` + `OFL-*.txt` | **Nuevos** (fase 0), solo en la previa | Entran en la lista blanca |
| `web/js/graficas.js` | Opciones nuevas del octógono, desactivadas por defecto (`halo` en la fase 1); en la fase 4, dos arreglos táctiles que solo tocan el modo lámina | Sin cambios |
| `web/css/estilo.css` | **Intacto**: el registro Verloop va encima | Sin cambios (lo siguen usando `/completo` y la página nueva) |
| `web/psicobench.html`, `web/css/psicobench.css`, `web/js/psicobench.js` | **Intactos** | Se retiran (quedan en el historial para volver atrás) |
| `web/publicar.py` | `--previa` y guarda (fase 0) | Lista blanca nueva; la guarda se adapta |
| `web/servir_previa.py` | **Nuevo** (fase 0) | Se conserva para futuras previas |
| `web/previa_lamina.prueba.mjs` | **Nuevo** (fase 2): prueba de la lámina en Chrome headless | Pasa a apuntar a `/psicobench` |
| `web/previa_interaccion.prueba.mjs` | **Nuevo** (fase 4): interacción, estrecho, táctil y estados | Pasa a apuntar a `/psicobench` |
| `web/smoke.mjs` | Aserciones para `/psicobench-nueva` | Las de `/psicobench` pasan a las nuevas |
| `spike/test_xss_estatico.py` | Incluye la página nueva (fase 0) | Lista de HTML actualizada |
| `web/generar_datos.py` | Sin cambios previstos | Sin cambios |
| `THIRD_PARTY_NOTICES.md` | Fuentes (fase 0) | — |
| `CHANGELOG.md` | — | Entrada de la versión |

---

## 6 · Riesgos y mitigaciones

- **Divergencia con `main`**: las altas de modelos cambian `datos.js` y `psicobench.json` a menudo. Mitigación: `git merge origin/main` al empezar cada fase; la página nueva no escribe cifras a mano, así que absorbe las altas sin tocarla.
- **Filtros SVG en móvil** (`feGaussianBlur` del halo, `feTurbulence` del grano): coste de pintado alto en gamas bajas. Mitigación: halo una vez por cambio de modelo y desactivado por debajo de 768 px; grano desactivado con `prefers-reduced-motion` o `prefers-contrast: more`.
- **Hover sobre 39 polilíneas finas**: zonas de acierto de 1,2 px. Mitigación (hecha en la fase 2): trazo de golpe de 8 px transparente (`pointer-events: stroke`); con teclado y en táctil, los botones ◀ ▶.
- **Texto en gradiente** (`background-clip: text`): pierde contraste en la parte naranja. Mitigación: solo en cifras ≥ 40 px, nunca en cuerpo.
- **Violeta de Obediencia** (`#7B3DFF`, 3,8:1): solo en barras, rellenos y texto ≥ 24 px.
- **Palabras largas en mayúsculas a 320 px** («susceptibilidad», «provocabilidad»): `overflow-wrap: break-word` en los titulares; se revisa cada `<h2>` en la fase 4.
- **Doctrina del color**: la web dice hoy «un solo color para toda la web: la escala de dureza». Con el tono por eje se reescriben esas dos leyendas en la versión nueva.
- **Cambio de personalidad visual solo en una superficie**: `/psicobench` quedará distinta de `/` y `/completo` hasta que se extienda. Se dice en el CHANGELOG.

---

## 7 · El cambio a producción (cuando la fase 5 esté validada)

Un PR propio de `feature/psicobench-verloop` a `main`, preparado y revisado en la previa antes de abrirlo:

1. `git merge origin/main` y previa final.
2. Un commit de cambio: `web/psicobench-verloop.html` → `web/psicobench.html` (sin `noindex` ni aviso, canónico y metadatos de la vigente); `web/verloop/` y `web/fonts/` a la lista blanca; la guarda `_sin_previa` se adapta; se retiran `css/psicobench.css` y `js/psicobench.js` de la versión anterior.
3. `smoke.mjs` con las aserciones nuevas en `/psicobench`; CI en verde.
4. Merge a `main` → `desplegar.yml` publica y corre el smoke contra producción.
5. **Volver atrás**: revertir el commit de cambio y fusionar el revert; la página anterior vuelve íntegra.

---

## 8 · Decisiones (cerradas el 25-10-2026)

1. **Tono por eje** en lugar de la escala de dureza única, reescribiendo las dos leyendas que la mencionan.
2. **El modelo de la portada y el de la ficha comparten el hash `#m=<id>`.**
3. **Se retira el panel del ISS de la portada**; lo sustituye la tarjeta del modelo bajo el octógono. El panel en bucle sigue en `/`.
4. **Fuentes autoalojadas** (hecho en la fase 0).
5. **Alcance**: solo `/psicobench` en esta rama; `/` y `/completo` en ramas posteriores con los mismos tokens.
6. **Despliegue en sombra** (añadida): nada de la versión nueva llega a benchai.tech hasta validarla entera; se valida en la previa y se publica con el cambio del §7.
