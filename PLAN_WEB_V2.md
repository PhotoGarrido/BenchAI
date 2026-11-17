# Revisión global de la web y propuestas — 31-10-2026

> **Estado (01-11-2026): adaptado al registro «Verloop»** (PR #33, en producción
> desde el 31-10), en la rama `claude/web-socialbench`, sin desplegar. Verloop ya
> había hecho la portada-puerta con los dos benchmarks y varios de los arreglos de
> §2 (enlace «Completa», vacuna, estrato duro, correlación, órdenes y motín), así que
> la primera versión de esta propuesta (rama `claude/web-v2`, sobre el diseño viejo)
> queda solo como referencia. Lo que se porta encima de Verloop, sin tocar su diseño:
> - **SocialBench** en `/social` (redirige `/psicobench`); `/completo` es su detalle.
> - **`/personalidad/datos`** (§5), con los tonos por rasgo de Verloop.
> - Barra «Inicio · SocialBench · Personalidad» + «Resumen · Detalle».
> - Nombres legibles (`web/modelos.json`), un solo conteo de modelos, `palabra()`
>   sin techo, datos por página, tarjetas OG sin cifras, la frase de DeepSeek,
>   oyentes de las gráficas y `#m=`.
> - Lo que §4 proponía y **no** se hace: `/social/datos` aparte y retirar
>   `/benchmark` (Verloop lo mantiene); la portada nueva (Verloop ya la tiene).

---

## 0. En cinco líneas

1. Hay **errores visibles** que conviene arreglar ya (cifras que no cuadran en la misma página, «NaN» que parece un fallo, el mismo modelo con dos nombres, tres notaciones de posición). Lista en §2.
2. El problema de fondo es de **estructura**: la historia social se cuenta en **cinco superficies** (`/`, `/completo`, `/psicobench`, `/benchmark` y el visor) y la personalidad en una. La portada no menciona la personalidad.
3. Los papeles están cruzados: `/psicobench` es medio divulgación medio herramienta; `/completo` es un reportaje largo, no un detalle consultable; `/benchmark` es un quinto estilo con jerga interna.
4. Propuesta: **dos niveles × dos benchmarks** bajo una portada-puerta. Base amena (`/social`, `/personalidad`) y detalle-herramienta (`/social/datos`, `/personalidad/datos`), con redirecciones desde las rutas actuales.
5. Para el detalle de personalidad, de AA merece la pena copiar: selector de modelos común a todas las gráficas con estado en la URL, mapa de calor por faceta, clasificación por rasgo con bigotes, comparador A/B, familias por similitud, «construye tu ranking» con pesos y huellas ±σ. Lo que no hay que copiar es el percentil 1-100, que oculta la magnitud.

---

## 1. Mapa actual

| Ruta | Fichero | Papel real hoy | Texto | Estilo |
|---|---|---|---|---|
| `/` | `home.html` | Divulgación social: 3 experimentos, «¿qué harías tú?», clasificación ISS, coste, FAQ | ~21 k car. | escena oscura/papel |
| `/completo` | `index.html` | Reportaje largo social + método («Research preview») | ~52 k car. | igual |
| `/psicobench` | `psicobench.html` | Producto PsicoBench: ISS, ejes, mapa, cara a cara, cuatro cruces, ficha `#m=`, escalera de versiones, CSV | ~28 k car. | igual + componentes |
| `/personalidad` | `personalidad.html` | Test de personalidad: 22 fichas radar, «quién es el más…», metodología breve | ~26 k car. | igual |
| `/benchmark` | `benchmark/index.html` | Panel del instrumento (tabla, radar, mapas, correlaciones) | ~5 k car. | **otro** (oscuro, monoespaciado) |
| `/viewer` | `viewer/index.html` | Reproductor de episodios | — | **otro** |

Las cuatro primeras cargan el mismo `datos.js` de **757 kB**, del que la personalidad usa 27 kB:

| clave | kB | clave | kB |
|---|---|---|---|
| `sesiones` | 268 | `consola` | 53 |
| `episodios` | 62 | `personalidad` | 27 |
| `benchmark` | 56 | resto | 14 |

---

## 2. Errores y fallos

Verificados en producción o en el código. El orden es por lo que ve un visitante.

### Críticos (se ven y restan credibilidad)

| # | Dónde | Qué pasa | Causa |
|---|---|---|---|
| E1 | `/`: héroe vs «Lo que ha costado» | Arriba «39 mediciones de **35 modelos**»; abajo «**34** modelos probados». | `benchmark.modelosDistintos` (quita `#esfuerzo`) y `corpus.modelosProbados` (cuenta ids del corpus crudo) **no** siguen la misma regla, aunque el comentario de `generar_datos.py:147` dice que sí. Tampoco cuadra con «33» de la revisión de octubre. |
| E2 | `/psicobench` (héroe), `/`, tablas | «DeepSeek · **NaN** · 13-09-2026», «deepseek-v4-flash-0731@**NaN**». | Es el nombre del gateway, pero cualquiera lo lee como un fallo de JavaScript. |
| E3 | `/psicobench` vs `/personalidad` | El mismo modelo con dos nombres: ISS 7,9 es «space-bunny-alpha#low» en PsicoBench y «minimax/minimax-m3.1-flash#low» en Personalidad. Lo mismo con Union Alpha (desvelado). | El campo `desvelado` existe en datos.js pero las tablas no lo usan. |
| E4 | Todo el sitio | Ids técnicos crudos y mezclados como nombre visible: `anthropic/claude-opus-5.5#low`, `qwen3.6`, `z-ai/glm-5.3`, `deepseek-v4-flash@2026-10-17` frente a `deepseek-v4-flash-1017`, `@OR` frente a `@OpenRouter`. | No hay un registro de nombres para mostrar. |
| E5 | `/`, `/psicobench`, `/benchmark` | Tres notaciones para la misma posición: «POSICIÓN 1–12», «1–12 ·», «=1». Y los «n/c» aparecen en mitad de la lista ordenada. | Cada superficie pinta la suya. |

### Medios

| # | Dónde | Qué pasa |
|---|---|---|
| E6 | `/` (la grabación) | Texto para el público: «el mismo de `viewer/index.html`». Ruta del repo en una página divulgativa. |
| E7 | `/` (escalera de Milgram) | Estado inicial «LO JUZGA INJUSTO **0 de 1**» antes de que el visitante toque nada. Se lee raro (a revisar si es intencionado). |
| E8 | `/benchmark` | Jerga interna en la primera pantalla: «suite M2+N2+N3b (E1 Asch · E2 Milgram×vacuna · C1/C1-v2 · P1+P2b…)», «modelos-snapshot». Sin barra común ni forma de volver salvo un enlace a `/psicobench`. |
| E9 | `/personalidad` | `og:image` es la genérica de la portada social: al compartir la personalidad sale la tarjeta de Milgram. |
| E10 | `/personalidad`, `/psicobench` | 757 kB de datos para usar 27 kB (personalidad) o ~60 kB (psicobench). En móvil con 4G son 1-2 s de más antes de pintar nada. |
| E11 | Barra | El conmutador mezcla formato y producto: «Resumen · Completa · PsicoBench · Personalidad». No dice que hay dos benchmarks ni qué es cada página. |
| E12 | `/completo` | Se presenta como «Research preview» y «Banco conductual de agentes LLM» mientras las otras dicen «PsicoBench v0.4» y «BenchAI». |

### Menores

- E13. Revelado al hacer scroll: si se llega por ancla (p. ej. «La clasificación de modelos ↓»), la sección queda en blanco un momento hasta que entra la animación.
- E14. Nombres de marca: el repo es PsicoAI, el sitio BenchAI, el benchmark PsicoBench, la personalidad «test de personalidad de BenchAI» y el dominio `psico.benchai.tech`. Ver §3.3.

### Auditoría de código (main a64649c)

Estática, comprobada a mano en los puntos críticos.

**Críticos: cifras escritas a mano en `/completo` que ya no cuadran con los datos.** Son textos de cuando había menos mediciones. Ninguno pasa por `data-cifra`, así que la comprobación de denominadores no los vigila.

| # | `web/index.html` | Dice | Los datos dicen |
|---|---|---|---|
| C1 | :269 | «Los DeepSeek cruzan la línea crítica entre el 80 y el 100 %» | `deepseek-v4-flash-1017` 0,4 · `v4.1-flash` 0,6 |
| C2 | :293 | Con la vacuna, en DeepSeek «la obediencia cae entre 50 y 70 puntos» | −10 (v3.2), 0 (v4.1), **+20** (1017) |
| C3 | :329-330 | «hasta el 89 %» (órdenes), «hasta el 80 %» (motín) | 90 % en los dos |
| C4 | :395 | «estrato duro pegado al suelo en las **19** mediciones» | 39 (la misma página dice 39 en `pagina.js:302`) |
| C5 | :547 | conformidad y sicofancia «correlacionan a **0,70**» | 0,59 (la línea :552 ya dice 0,59) |

**Medios**

- C6. **«Completa» en la barra de `/completo` lleva a la portada**. `index.html:40` tiene `href="index.html"`, y `publicar.py:118-140` no lo reescribe en `completo.html`. Comprobado en producción.
- C7. E1 tiene una causa más: `modelosDistintos` no quita `@fecha`, así que `deepseek-v4-flash@2026-10-17` cuenta como modelo aparte (`generar_datos.py:149`).
- C8. **Fuga de memoria**: cada `G.adaptable` (`graficas.js:186-190`) añade un `resize` y un ResizeObserver que nunca se quitan. En `/psicobench` se crean de nuevo en cada pestaña de eje (`psicobench.js:289`) y en cada ficha (`:796`).
- C9. **Entrada por `#m=`**: `psicobench.js:858-861` desplaza antes de que se dibujen las gráficas de encima, y al llegar desde `/personalidad` («en PsicoBench →») se queda corto. `personalidad.js:357` ya lo resuelve repitiendo a los 600 ms.
- C10. **Volver a la misma ficha no hace nada**: `abrirHash` asigna el mismo `location.hash` y no salta `hashchange` (`psicobench.js:596`, `personalidad.js:577`).
- C11. **`datos.js`**: se sirve con `indent=1` (`generar_datos.py:1142`). Minificado pasa de 757 a 479 kB. Proporción que usa cada página: `/personalidad` 3,6 %, portada 24 %, `/completo` 38 %, `/psicobench` 75 %. El iframe del visor de la portada lo vuelve a parsear entero.

**Menores**

- `generar_datos.py:1085-1104`: `PALABRA` acaba en 39. **La próxima alta (40 mediciones) rompe la generación** con KeyError. Esto conviene meterlo en F1.
- `escena.js:95`: `"deepseek-v4-flash-0731"` está escrito a fuego y sin guarda. Si sale del banco, se rompe la escalera de la portada.
- Los `setInterval` siguen con la pestaña oculta (`escena.js:146`, `psicobench.js:1118`), y los MutationObserver de `escena.js:38` y `home.js:1361` se disparan sin parar.
- Hash frágil: `psicobench.js:153` no codifica el id, y `decodeURIComponent` lanza error con un hash mal formado (`:859`, `personalidad.js:351`).
- Más cifras a mano que hoy cuadran pero incumplen la regla:
  - `index.html:359-360`, `:374`, `:380`, `:476`, `:595-596`.
  - El 65 % de `home.html:137` y de `index.html:257`.
  - «trece» y «v0.4».
  - El ejemplo «1–11» de `psicobench.html:129` (hoy el grupo 1 tiene 12).
- El visor se titula «PsicoAI · Visor de replays». `visor-embebido.html` es público sin noindex/canonical, y la ruta real es `/viewer`, no `/visor`.
- Accesibilidad:
  - Los botones ⏮ ◀ ▶ del visor no tienen nombre accesible.
  - El input de fichero no tiene etiqueta.
  - Las pestañas de `/psicobench` llevan `role="tab"` sin tabpanel.
- `publicar.py:201`: la reescritura del visor depende de que no haya canonical, una trampa futura.
- **Sin XSS**. Las anclas estáticas resuelven, el sitemap incluye `/personalidad` y cada página tiene su description, canonical y og.

---

## 3. Diagnóstico de estructura

### 3.1 Cinco superficies para una historia, una para la otra

La clasificación ISS aparece completa en `/`, `/psicobench`, `/completo` y `/benchmark`, cada una con otro diseño y otra notación. La escalera de Milgram está en `/` y en `/completo`. Mientras tanto, la personalidad, que es el producto más fácil de compartir («¿qué personalidad tiene tu IA?»), no sale en la portada.

### 3.2 Base y detalle están mezclados

- `/psicobench` empieza amena y a la mitad se vuelve herramienta (cuatro cruces, escalera de versiones, CSV, notas técnicas). Para un curioso es larga; para un investigador le faltan filtros y estado en la URL.
- `/completo` es lo que tú llamas «detalle social», pero es un reportaje lineal de 52 k caracteres: no se consulta, se lee de arriba abajo.
- `/benchmark` sí es una herramienta, pero con estilo propio y jerga.

### 3.3 Nombre

Hoy hay cuatro nombres y no está claro cuál es la casa y cuáles los productos. Mi recomendación:

- **BenchAI** es la casa (dominio, barra y logo).
- **PsicoBench** pasa a ser el nombre de la familia de instrumentos, porque ya está en el preprint, `CITATION.cff` y versionado (v0.4): **PsicoBench · Social** (el ISS) y **PsicoBench · Personalidad**.
- No hace falta «SocialBench» como marca aparte; en las rutas basta `/social`.

Alternativa si prefieres una sola marca: todo BenchAI («BenchAI Social», «BenchAI Personalidad») y PsicoBench solo como nombre del instrumento en el método. **Esto lo decides tú.**

---

## 4. Arquitectura propuesta

```
/                      Portada BenchAI: dos puertas            (base, ≤ 5 pantallas)
├─ /social             PsicoBench · Social                     (base, amena)
│  └─ /social/datos    Explorador + método                     (detalle, herramienta)
├─ /personalidad       PsicoBench · Personalidad               (base, amena)  ← ya existe
│  └─ /personalidad/datos  Explorador + método                 (detalle, NUEVA)
└─ /estudio            El reportaje largo (hoy /completo), opcional

/viewer                Reproductor (sin cambios)

Redirecciones 308: /psicobench → /social · /benchmark → /social/datos · /completo → /estudio (o /social/datos)
```

### Reglas comunes

- **Base** = una pregunta, una respuesta visual y el enganche. Cada pantalla tiene un titular que se entiende solo. Nada de IC, n, códigos de experimento ni rutas de repo; todo eso lleva un enlace «ver en detalle →» al punto exacto del detalle.
- **Detalle** = herramienta. Índice lateral fijo, selector de modelos común, estado en la URL, cada gráfica con «enlace · descargar · ver tabla · CSV», IC siempre visibles y el método al final.
- **La misma plantilla en los dos benchmarks**, así lo que se aprende en uno sirve en el otro.
- **Una barra para todo**: `BenchAI | Social · Personalidad | (en detalle: Base ↔ Datos)`. `/benchmark` y `/visor` también la llevan.
- **Una ficha de modelo compartida** (`#m=<id>`) con ISS y personalidad juntos cuando existan los dos.

### 4.1 Portada `/` (rehacer, más corta)

1. Héroe: «¿Cómo se comporta una IA cuando nadie la mira?», con dos puertas grandes: **Presión social** (el dato «36 % obedece hasta el final frente al 65 % humano») y **Personalidad** (un radar animado que va rotando de modelo).
2. «Busca tu modelo»: un buscador que devuelve su ISS y su radar en una tarjeta y enlaza a las dos fichas. Es el gancho más directo.
3. «¿Qué harías tú?» (ya existe y funciona): se queda, pero más arriba.
4. Tres hallazgos en tarjetas con enlace.
5. Cómo lo medimos en tres frases, y los datos abiertos.

Lo que hoy está en la portada sobre los tres experimentos pasa a `/social`.

### 4.2 `/social` (base, a partir de la portada y `/psicobench` actuales)

Los tres experimentos (lo mejor de la portada actual) → ISS en una gráfica con grupos → tarjetas por modelo → cara a cara → «qué llevarte si trabajas con agentes» → «ver los datos →».
Fuera de aquí, y al detalle: cuatro cruces, escalera de versiones, réplicas, CSV, notas técnicas.

### 4.3 `/social/datos` (detalle: fusión de `/psicobench` analítico, `/benchmark` y los datos de `/completo`)

Clasificación con filtros (lab, vía, fecha, versión) · mapa de calor de los 8 ejes · por eje con IC · métricas secundarias · cara a cara · réplicas y vías · escalera de versiones · correlaciones · sesiones lado a lado · ficha de medición · método y descargas.

### 4.4 `/personalidad` (base): retoques

Ya va bien encaminada. Cambios:

- Nombres para mostrar (E4).
- Héroe: añadir «busca tu modelo».
- «Quién es el más…» antes de las 22 fichas: se lee más rápido y engancha más.
- Tarjeta para compartir por modelo (OG por ficha).
- Las fichas ya se pueden ordenar; añadir que se puedan **comparar dos**.

---

## 5. `/personalidad/datos`: qué tomar de Artificial Analysis

Lo que hace AA-PersonalityBench, traducido a lo que ya tenemos en `datos.js → personalidad` (por modelo: `p`, `ic`, `dif`, `difIC`, `marca`, `validez`, `indices`):

| AA | Para nosotros | ¿Hay datos? |
|---|---|---|
| **Selector «10 de 41 modelos»** común a todas las gráficas, estado en la URL (`?trait-results-index=transparency`) | Selector «N de 22» + `?modelos=…&rasgo=H&vista=…`. Cada gráfica, enlazable. | Sí |
| **Barra por gráfica**: enlace, descargar imagen, ver como tabla | Igual, más CSV. | Sí |
| **Índice lateral fijo** | Igual. | — |
| **Mapa de calor modelos × rasgos** (por índice, percentil) | Modelos × 6 rasgos coloreado por `dif`, con ▲▼ en las marcas firmes. Segundo nivel: **facetas** (H tiene 4, N ansiedad/hostilidad…). | Rasgos sí; **facetas, no** (hay que exportarlas desde `spike/`) |
| **Clasificación por rasgo con bigotes al 95 %** | Igual, con `ic` y la media del panel marcada. | Sí |
| **Comparar dos modelos** (probabilidad por Elo) | A frente a B rasgo a rasgo: diferencia con IC y «firme / no firme» con la misma regla que las marcas. | Sí (IC de la diferencia A−B por calcular) |
| **Preguntas de ejemplo** con las respuestas de dos modelos y cómo se puntuó | **La situación, las opciones y qué eligió cada modelo**. Es lo más ameno de AA y aquí se ve aún mejor, porque son decisiones. AA publica 5 de 900: publicar 5-6 situaciones «sacrificables», fuera del banco que puntúa, por la contaminación (CANARY). | **No**: exportar un puñado de ítems y elecciones |
| **Familias emergentes** (dendrograma por correlación) | Familias de personalidad por similitud del perfil; se apoya en la huella v2. | Parcial (perfiles sí; calcular el árbol en `generar_datos.py`) |
| **Construye tu ranking** (pesos −2…+2) | «Elige para qué lo quieres»: pesos por rasgo más plantillas (atención al cliente: +A +C −N; investigación: +O +H…). | Sí |
| **Huellas ±σ** | Los 2-3 rasgos o facetas más por encima y por debajo de la media, en σ. | Sí (σ entre modelos) |
| — (AA no lo tiene) | **Personalidad × ISS**: dispersión de un rasgo frente al ISS, con `relacionISS`. Nadie más puede enseñarlo. | Sí |
| — | **Validez por modelo** (V1-V4) como sellos, y los «medidos sin ficha» explicados. | Sí |
| Página de metodología aparte | Método completo: Big Five/HEXACO, conducta frente a autoinforme, las cinco comprobaciones, G4, retest y limitaciones. | Sí (PERSONALIDAD.md) |

**Lo que no copiaría**:

- El **percentil 1-100 entre modelos**: dice quién está por encima, no cuánto, y cambia cada vez que entra un modelo. Nuestro «diferencia con la media + marca firme» es más honesto. Se puede ofrecer el percentil como vista secundaria.
- **Elo entre pares con jueces LLM**: no es nuestro método y no hace falta.

---

## 6. Mejoras de diseño transversales

1. **Registro de nombres** (`modelos.json`, leído por `generar_datos.py`): id → nombre para mostrar («Claude Opus 5.5 · esfuerzo bajo»), lab, color o logo del lab y alias desvelados. El id técnico queda como subtítulo en mono. Arregla E3, E4 y E2 («vía NaN» → «vía NaN API», con tooltip).
2. **Una sola notación de posición** («1–12», con «empate» en tooltip) y los n/c al final con su porqué.
3. **datos.js por página**: `datos-social.js`, `datos-personalidad.js` y `datos-sesiones.js` bajo demanda. La personalidad baja de 757 a ~30 kB.
4. **Compartir**: OG por página y por ficha («La personalidad de Claude Opus 5.5»). Es el mecanismo de difusión natural de la personalidad.
5. **Jerga fuera de las bases**: N3b, P1b, C1-v2, modelo-snapshot, «research preview» y rutas de repo solo en el detalle, siempre con glosa.
6. **Pendiente de decidir**: versión en inglés. El 13-09 se dijo que no, pero la audiencia de AA está en inglés, y una base EN de `/personalidad` sería barata cuando los textos salgan de plantilla.

---

## 7. Plan por fases (cada una, una rama y un PR, con smoke contra producción)

| Fase | Contenido | Tamaño | Depende de |
|---|---|---|---|
| **F1 · Errores** | C1-C6 (cifras de `/completo`, enlace «Completa»), E1/C7, `PALABRA` hasta 40+, E2, E5-E9, E12, C8-C10, `datos.js` minificado | pequeño-medio | — |
| **F2 · Nombres y barra** | Registro de nombres (E3, E4), barra común en las 6 superficies, decisión de marca | medio | decisión §3.3 |
| **F3 · `/personalidad/datos`** | Página nueva al estilo de §5; export de facetas y de 5-6 situaciones de ejemplo desde `spike/` | grande | F2 |
| **F4 · Reorganizar lo social** | `/social` base + `/social/datos` (fusión de `/psicobench`, `/benchmark` y los datos de `/completo`), redirecciones, `datos.js` partido | grande | F2 |
| **F5 · Portada-puerta** | Nueva `/` corta, con «busca tu modelo» | medio | F3, F4 |
| **F6 · Compartir** | OG por página y ficha | pequeño | F2 |

Orden recomendado: F1 → F2 → F3 → F4 → F5 → F6. F3 va antes que F4 porque es lo nuevo que pides y porque fija la plantilla de detalle que luego hereda lo social.

---

## 8. Decisiones que necesito de ti

1. **Marca**: ¿BenchAI casa + PsicoBench · Social / PsicoBench · Personalidad (recomendado), o todo BenchAI?
2. **Rutas**: ¿`/social` y `/social/datos` con redirecciones desde `/psicobench`, `/benchmark` y `/completo`? ¿El reportaje largo se conserva como `/estudio` o se disuelve entre base y detalle?
3. **Ítems de ejemplo de personalidad**: ¿publicar 5-6 situaciones con las elecciones de los modelos, sacadas del banco que puntúa?
4. **¿Empezamos por F1** (errores) mientras decides lo demás?
