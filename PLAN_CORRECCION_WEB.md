# Plan de corrección — auditoría independiente de la web (W1)

**Origen**: auditoría externa de la web (18-08-2026) sobre `origin/main`
(`b0690d5`) y producción en benchai.tech. **Veredicto del auditor**: NO-GO como
publicación estable; apta como research preview tras cerrar bloqueantes.
**Veredicto aceptado.** Cada hallazgo de abajo se ha verificado de forma
independiente antes de triarlo: los cinco bloqueantes se reprodujeron
(comando/línea citados); los rechazos llevan su evidencia.

**Triaje**: 5 bloqueantes aceptados · ~20 hallazgos de prioridad alta aceptados
(2 matizados) · 4 rechazados con justificación · 4 matizados/aplazados.

Una nota de método antes del plan: **la revisión global previa (18-08) no cazó
B1–B4 porque verificó estados HTTP y conteos de nodos, no flujos reales** — el
visor daba 200 sin ejecutar su JS, y el panel del benchmark «tenía 36 filas y 4
pestañas» sin que nadie mirase la geometría del radar ni la semántica del
ranking. La corrección sistémica es el punto 2 del auditor (smoke con navegador
real contra las reglas reales de Vercel), y por eso va en la fase 1, no en la 3.

---

## Fase 1 · Bloqueantes (todos aceptados, todos reproducidos)

### B1 · Visor roto en `/viewer` — ACEPTADO

Reproducido: la página servida usa `src="app.js"`; con `cleanUrls` la ruta es
`/viewer` (sin barra), el relativo resuelve a `/app.js` → **404** (verificado);
`/viewer/app.js` → 200. El visor queda vacío.

**Causa de fondo**: `viewer/index.html` debe seguir funcionando con doble clic
(`file://`), así que la ruta relativa es correcta *en el repo* — el fallo es del
**empaquetado**, que lo sirve bajo una URL sin directorio.

**Solución**: `publicar.py` reescribe `src="app.js"` → `src="/viewer/app.js"`
solo en la copia publicada (mismo patrón que ya usa para `../`). El fichero del
repo no se toca. Smoke posterior: cargar `/viewer` en navegador y exigir 0
recursos 404 + replay montado.

### B2 · Medición no clasificable con puesto 5 — ACEPTADO

Reproducido: [plantilla_benchmark.html:283](spike/plantilla_benchmark.html) hace
`e.posicion == null ? String(i + 1)` — el D-8b excluye a `qwen3.6` de la
clasificación (`posicion: null`, y así lo publica el JSON y `BENCHMARK.md` con
`n/c`) y el panel le inventa el puesto por índice de fila. **Tergiversación
material**, y además contradice al propio artefacto canónico de al lado.

**Solución**: la celda muestra `n/c` con nota de exclusión (título accesible,
no solo `title`), y la fila queda fuera de cualquier lógica de orden por puesto.
Se corrige en la plantilla y se regenera con `generar_benchmark.py` (el linaje
actualiza solo el hash del HTML). Se añade un caso al `--check`: ninguna entrada
con `posicion: null` puede renderizar un número.

### B3 · Radar de 8 ejes con geometría de 6 — ACEPTADO

Reproducido: tres sitios con `i * Math.PI / 3`
([plantilla:347,383,390](spike/plantilla_benchmark.html)) — paso de hexágono.
Con 8 ejes, los ejes 7 y 8 se superponen a 1 y 2: **el gráfico es
geométricamente falso** aunque la tabla sea correcta. Herencia del panel
hexágono v0.1 que ninguna puerta vigilaba (el `--check` compara bytes, no
geometría).

**Solución**: `2 * Math.PI / EJES.length` en polígonos, rejilla, radios y
etiquetas — derivado del número real de ejes, no constante. Y un canario en el
generador: si `ejes.length × paso ≠ 2π`, no se genera.

### B4 · Método del panel desfasado — ACEPTADO

Reproducido: «Correlaciones entre ejes (16 mediciones)» escrito a mano
([plantilla:615](spike/plantilla_benchmark.html)) con 19 entradas en el JSON; y
la atribución de Wilson ([plantilla:579](spike/plantilla_benchmark.html)) no
coincide con lo que `BENCHMARK.md` declara por eje. Es exactamente la clase de
desfase texto-dato que el proyecto persigue — pero la prosa del panel quedó
fuera del perímetro del generador.

**Solución**: el denominador se interpola desde `entradas.length`; la frase de
estimadores se genera desde la misma fuente que `BENCHMARK.md` (o, mínimo, se
corrige y se le pone aguja de verificación como a las cifras de la web
divulgativa). La regla del auditor es la nuestra: **el método público se genera,
no se escribe**.

### B5 · TLS roto en `www.benchai.tech` — ACEPTADO

Reproducido: `curl` exit 60 (certificado no cubre el hostname). El DNS de
`www` existe (Vercel lo crea con el dominio) pero el proyecto no lo tiene
asignado, así que no hay certificado emitido.

**Solución**: añadir `www.benchai.tech` al proyecto (emite certificado) con
redirección 308 al ápex. Un comando (`vercel domains add`); verificación con
`curl` y con el smoke.

---

## Fase 1-bis · Prioridad alta aceptada (correcciones con dueño claro)

**Accesibilidad y móvil** — todos aceptados; dos son errores míos recientes:

| Hallazgo | Verificación | Solución |
|---|---|---|
| Peldaños de la botonera como `div` clicables sin teclado ni rol | Confirmado — [home.js](web/js/home.js), error mío del refactor | `<button>` nativos con `aria-pressed`; el CSS ya está |
| Cifras animadas arrancan en 0 fuera del viewport | Confirmado — `animar()` pinta 0 hasta el IntersectionObserver | El valor final se escribe en el DOM desde el inicio; la animación pasa a ser capa visual (y ya se apaga con `prefers-reduced-motion`) |
| Flechas de gráficas vuelven al primer dato | Confirmado — [graficas.js:122](web/js/graficas.js): `blur` en fase captura resetea `i` al mover el foco entre marcas internas | Ignorar `blur` cuando `relatedTarget` sigue dentro del svg |
| Foco invisible en botones de ordenar (`all: unset`) | Aceptado | `:focus-visible` explícito tras el reset |
| Teclado en pestañas/filas/cabeceras del panel | Aceptado | Patrón WAI-ARIA tabs + `aria-sort`; denominadores fuera de `title` (texto visible o `aria-describedby`) |
| Visor sin H1, canvas sin nombre, slider sin etiqueta, feed con `div` clicables, autoplay ignora `prefers-reduced-motion` | Aceptado | Pasada de roles/etiquetas al visor; autoplay condicionado a la media query |
| Visor 651 px en viewport de 390; panel lateral desaparece <900 px; botonera recortada en 390 | Aceptado | Quitar mínimos fijos, apilar paneles en columna, permitir scroll horizontal SOLO dentro de la botonera |

**Integridad científica y editorial** — aceptados:

| Hallazgo | Verificación | Solución |
|---|---|---|
| «19 modelos» = 19 mediciones de **18** modelos | Confirmado con los datos | La tira de portada pasa a «mediciones» y el generador emite ambas cifras (`mediciones=19`, `modelosDistintos=18`) para poder decir «19 mediciones de 18 modelos» |
| «18 de 19» escrito a mano ([home.html:182](web/home.html)) | Confirmado — viola la regla de la casa | Se deriva en `generar_datos.py` (mismo cómputo que ya hace la apuesta) y entra por `data-cifra` |
| Lenguaje categórico («pasa exactamente lo mismo», «replican la ley de Milgram», «obedecerá del todo») | Aceptado — es la regla R1.5 del propio proyecto aplicada a la web | Pasada de acotación: «en esta muestra y protocolo…», con lista cerrada de frases |
| «Hemos construido mentes que…» ([index.html:685](web/index.html)) y «su conciencia, si quieres llamarla así» ([index.html:417](web/index.html)) | Confirmado | Se reescriben las dos. Ver el matiz sobre el término «pensamiento privado» abajo |
| README desfasado (7 ejes / v0.3) | Confirmado ([README.md:15](README.md)) | Actualizar a 8 ejes / v0.4; la cifra entra en la pasada de agujas |

**SEO, marca, confianza** — aceptados: metas/canonical/OG para `/benchmark` y
`/viewer` (vía plantilla y `publicar.py`); restos de marca «PsicoAI» en visor y
panel → BenchAI donde es marca (PsicoBench se queda como instrumento, con una
línea que explica la relación); bloque de colofón con autoría, contacto, fecha,
**SHA de despliegue** y cita (CITATION ya existe); JSON-LD `Dataset` en
`/benchmark`; `/favicon.svg` como fichero además del data-URI.

**Seguridad/privacidad** — aceptados: `chmod 600` del `.env` local (trivial);
párrafo de política de privacidad sobre logs del hosting; **revisión legal de
CC BY 4.0 sobre outputs de proveedores → tarea de David** (fuera de mi alcance;
señalo que LICENSE-DATOS puede necesitar una cláusula por proveedor).

**Operación** — aceptados (la crítica a la CI es certera): el `publicar.py
--check` en CI compara una regeneración contra otra — **es casi tautológico en
CI** (solo caza crashes y no-determinismo; en local sí es significativo). Se
acepta el paquete completo del auditor: Playwright contra las reglas reales de
Vercel (rutas, recursos 2xx, consola limpia, 390/768/1440), axe, despliegue
automatizado desde main verde con SHA publicado y smoke post-deploy que
verifique **lo desplegado**, no lo generado.

---

## Rechazados, con justificación

### R1 · «Sustituir todos los nombres de sujetos por pseudónimos» — NO APLICA la sustitución; SÍ una mitigación distinta

El hallazgo de fondo es real: «Irene Vallejo» coincide con una escritora
pública, y está en el **diseño congelado**
([experimento_asch.py:51](spike/experimento_asch.py), con Big Five asignado) y
en los crudos de decenas de runs cuyos hashes fija el release manifest. La
clave ciega de la κ y las hojas de etiquetado también la contienen.

Renombrar retroactivamente exigiría reescribir crudos fijados por sha256 —
exactamente lo que `GARANTIAS.md` promete no hacer jamás — o romper la
trazabilidad cifra→crudo que es el activo del proyecto. **La cura sería peor
que la enfermedad.**

Lo que sí se hace: (a) descargo visible en la web y en el README de episodios —
«todos los sujetos son sintéticos; cualquier coincidencia con personas reales
es fortuita»; (b) en la web, «(nombre sintético)» en la primera mención de un
sujeto; (c) **regla para diseños futuros**: la lista de nombres se contrasta
contra figuras públicas antes de congelar. La coincidencia fue un descuido de
diseño; la respuesta honesta es declararla, no reescribir la historia.

### R2 · «`replay.public.json` por defecto en los episodios» — NO APLICA como riesgo

El auditor lo reconoce: los pensamientos de los episodios son sintéticos e
intencionados. Hay que decirlo más fuerte: **el canal privado ES el producto
didáctico de los episodios** — el botón del visor se llama «Mostrar monólogo
privado generado» y la disonancia pública/privada es lo que el episodio enseña.
`replay.public.json` existe para el **modo estudio** y su puerta
(`test_replay_privacidad.py`, G8) vigila ese perímetro, que no es este.

Aplicar el default propuesto rompería el producto sin proteger nada. Lo que sí
se acepta: una nota en `episodios/README.md` declarando que estos replays
incluyen deliberadamente el canal privado didáctico, para que el nombre
genérico no invite a confusión.

### R3 · «Decidir si el correo y las rutas locales del historial siguen públicos» — YA DECIDIDO, NO APLICA reabrirlo

Decisión consciente, tomada y comunicada el 18-08 antes de abrir el repo:
reescribir el historial rompe los tags firmados, los hashes de los manifests y
la cadena completa de auditoría (R1–R5). El correo, además, es **requisito** del
polite pool de CrossRef en `verificar_citas.py`. Queda registrado aquí como
decisión, que es lo que el auditor pedía («decidir conscientemente»).

### R4 · «Retirar el visor del sitemap hasta arreglarlo» — NO APLICA

Sería tratar el síntoma: el visor se arregla en esta misma fase (B1). Retirarlo
y volverlo a meter son dos despliegues para no esperar uno.

---

## Matizados / aplazados, con justificación

### M1 · Dividir `datos.js` por ruta — APLAZADO como decisión de diseño

`datos.js` único es deliberado: funciona con `file://` (requisito documentado
del sitio), es UNA fuente verificada por `--check`, y la transferencia real es
pequeña — la propia auditoría mide respuestas comprimidas de 10–35 KB y TTFB de
90–320 ms. El «doble download» del iframe es una revalidación 304 (misma URL,
caché HTTP). Se reevalúa si el corpus crece un orden de magnitud; hoy el coste
de build y de superficie de error supera el beneficio.

### M2 · Fingerprint de assets — APLAZADO a la fase de pipeline

Con 304s y este tamaño, `must-revalidate` es correcto y barato. Tiene sentido
hacerlo junto al despliegue automatizado (fase 3), no antes.

### M3 · «Pensamiento privado» como término — MATIZADO

«Canal privado» / «pensamiento privado» es el término del instrumento en todo
el corpus congelado (docs, botón del visor, replays, preprint). La FAQ de la
web ya lo acota correctamente («no medimos estados internos, medimos una
respuesta elicitada en contexto separado»), y el auditor mismo da esa
explicación por buena. Renombrar el constructo a estas alturas introduciría el
desfase término-artefacto que se nos pide evitar. **Se corrigen las dos frases
que sí sobrepasan** (mentes, conciencia — arriba) y se mantiene el término
técnico con su acotación.

### M4 · Virtualizar el visor (50k eventos) — MATIZADO

50.000 es el **límite defensivo de carga** (validación de fichero hostil), no
el tamaño real: los replays publicados tienen cientos de eventos. Virtualizar
para el caso hostil es sobre-ingeniería. **Sí se acepta lo barato y real**:
parar el `requestAnimationFrame` en pausa y con la pestaña oculta.

### M5 · Resumen ejecutivo / recuento de palabras — MATIZADO

La home ES el resumen del sitio largo (ese es el diseño de dos páginas). Se
revisará la navegación interna tras la pasada de lenguaje, pero no se acepta
como principio que 7.400 palabras sobren en la versión que se llama «completa».

---

## Orden de ejecución

| Fase | Contenido | Esfuerzo | Dueño |
|---|---|---|---|
| **1** | B1–B5 + smoke Playwright mínimo (rutas, recursos 2xx, consola limpia) que los habría cazado | ~½ día | yo |
| **1-bis** | Accesibilidad aceptada (botonera, cifras, blur, foco, visor, móvil) | ~½ día | yo |
| **2** | Integridad editorial: cifras derivadas, 19/18, lenguaje, mentes/conciencia, README, descargo de nombres sintéticos | ~½ día | yo (pasada de lenguaje: propuesta mía, visto bueno de David) |
| **3** | SEO/confianza (metas, colofón con SHA, JSON-LD, favicon) + pipeline: deploy automatizado desde main verde, smoke post-deploy contra producción, axe | ~1 día | yo |
| **4** | Pasada manual VoiceOver/NVDA · revisión legal CC BY por proveedor · visto bueno final | — | David / tercero |

Criterio de salida de cada fase: puerta completa en verde + smoke en verde
contra **producción**. El GO a «publicación estable» lo da la fase 4, no la 3 —
coherente con el dictamen del auditor, que se acepta.
