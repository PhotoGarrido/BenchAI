# Plan · el registro «Verloop» en todo el sitio

**Fecha**: 28-10-2026 · **Estado**: aprobado el 28-10 (las cuatro decisiones como se recomendaban), **fases A–E hechas en la previa; falta tu evaluación y el cambio a producción** · **Rama**: `feature/psicobench-verloop` (la misma de PsicoBench: comparten registro, fuentes y previa) · **Antecede**: `PLAN_PSICOBENCH_VERLOOP.md`, fases 0–5.

Lo pedido, en este orden: (1) adaptar la versión larga (`/completo`), (2) el benchmark de personalidad recién publicado (`/personalidad`, PR #32), (3) un lavado de cara total de la portada (`/`), que pasa a ser la *landing*: más explicativa, con los dos benchmarks y el estilo nuevo.

---

## 1 · Punto de partida (medido el 28-10)

| Página | Ruta | Base | Peso propio | Secciones |
|---|---|---|---|---|
| Versión larga | `/completo` ← `web/index.html` | `estilo.css` + `pagina.js` + `graficas.js` | 847 + 564 líneas | 12 |
| Personalidad | `/personalidad` ← `web/personalidad.html` | `estilo.css` + `psicobench.css` + `personalidad.css` + `graficas.js` | 278 + 613 + 202 | 5 |
| Portada | `/` ← `web/home.html` | **`home.css` + `home.js` propios** | 634 + 1397 + 1146 | 12 |

Consecuencia práctica: `/completo` y `/personalidad` se apoyan en la misma base que `/psicobench`, así que el registro Verloop (que va **encima** de `estilo.css` redefiniendo variables, y del que `graficas.js` toma los colores) se les aplica casi entero. La portada es otro sistema y su lavado es diseño nuevo.

## 2 · Cómo se hace sin tocar producción

Lo mismo que con PsicoBench (§2 del plan anterior): nada llega a `main` hasta validar, páginas nuevas en paralelo y solo en la previa.

- `web/completo-verloop.html` → `/completo-nueva`
- `web/personalidad-verloop.html` → `/personalidad-nueva`
- `web/inicio-verloop.html` → `/inicio-nuevo` (la landing)

Todas `noindex`, con el aviso de previa, y **enlazadas entre sí** en la previa: el conmutador de las cuatro lecturas de cada página nueva apunta a las otras nuevas (`publicar.py --previa` reescribe los enlaces). La guarda `_sin_previa` se amplía a las tres. Copias de trabajo de los JS que lo necesiten (`verloop/pagina.js`, `verloop/personalidad.js`, `verloop/inicio.js`), como se hizo con `psicobench.js`, con sus diferencias en la cabecera.

## 3 · Fases

### Fase A · Base común — **hecha (28-10)**
Hecho: `verloop/sitio.css` con lo común y `verloop/psicobench.css` con lo propio. Comprobado sin cambio visible: los estilos calculados (28 propiedades) de los 3830 elementos de `/psicobench-nueva` coinciden antes y después a 1440 y 390 px, en impresión y con más contraste. Durante B y C pasaron también a la base común la franja de cifras bajo el titular (`.vistazo`), la prosa del sitio largo (subtítulos, destacados, tarjetas, carátulas, pasos; sin serif) y la ficha con flechas (escena, flechas, lienzo del polvo); el chasquido salió a su módulo, `verloop/chasquido.js`. Cada paso se volvió a comprobar con la misma comparación: 0 diferencias.

Plan original:
Separar de `web/verloop/psicobench.css` lo que es **del sitio** y no de PsicoBench a `web/verloop/sitio.css`: registro negro, barra y conmutador, botones y chips, cabeceras de sección en tres columnas, cajas, notas a todo el ancho, grano, impresión y más contraste. `psicobench.css` queda con lo suyo (lámina, mapa, tiras, ficha). Sin cambio visible en `/psicobench-nueva` (las capturas de la fase 5 sirven de referencia y las pruebas actuales lo comprueban).

### Fase B · `/completo-nueva` — **hecha (28-10)**
Hecho: `web/completo-verloop.html` (copia de `index.html`) + `verloop/completo.css`, con el `pagina.js` de siempre (sus gráficas toman los colores de las variables). Titular solo y, debajo, las cifras y la escalera viva de Milgram; once secciones con su número a color; la coda del cierre en display. Auditoría: nota aprox. 98 (la vigente, 94), CLS 0 (la vigente, 0,151), contraste 0 fallos, sin desbordes de 320 a 1920. Desviación: el «7 paradigmas» de las cifras sigue escrito en el HTML, como en la vigente.

Plan original:
Mismo contenido y mismas 14+ figuras; cambia el registro:
- Portada como la de PsicoBench (titular solo a todo el ancho) y, debajo, la silla de Milgram que hoy abre la página.
- Las 12 secciones con la cabecera de tres columnas y su número a color.
- Gráficas: tono por eje donde la gráfica es de ejes; el ISS con su gradiente; el resto con la paleta de series nueva.
- La consola de Milgram y el reproductor de grabaciones en el registro negro (son las piezas con más estilo propio: se revisan una a una).
- Pruebas: smoke `--previa` con las aserciones de `/completo` en la ruta nueva, desbordes 320–1920, contraste y la auditoría de rendimiento.

### Fase C · `/personalidad-nueva` — **hecha (28-10)**
Hecho: `web/personalidad-verloop.html` + copia de trabajo `verloop/personalidad.js` + `verloop/personalidad.css`. La portada que rotaba sola es ahora la ficha de un modelo cada vez (hexágono sobre los demás, marcas firmes en el tono de su rasgo, frase, ISS), con flechas, chasquido y deslizamiento; `#p=` la mueve. Tonos por rasgo: O `#FF7AD9`, C `#6FA8FF`, E `#FFC24D`, A `#7CF0B8`, N `#FF6B6B`, H `#C9A8FF`. El smoke repite las comprobaciones de `/personalidad` sobre la página nueva y suma las suyas. Auditoría: nota aprox. 97 (la vigente, 77, con CLS 0,647), CLS 0, contraste 0 fallos.

Plan original:
- Portada a todo el ancho y **la ficha del modelo en el formato de la lámina**: el perfil de rasgos de un modelo cada vez, con flechas y el mismo chasquido para pasar al siguiente (reutiliza el código de la lámina; los rasgos ocupan el lugar de los ejes).
- Fichas, «Quién es el más…» y metodología en el registro nuevo; un tono propio por rasgo, distinto de los ocho de PsicoBench para que no se confundan los dos instrumentos.
- El cruce con PsicoBench (la línea de personalidad en la ficha del ISS y viceversa) se mantiene en los dos sentidos.

### Fase D · `/inicio-nuevo`, la landing — **hecha (28-10)**
Hecho: `web/inicio-verloop.html` + `verloop/inicio.js` + `verloop/inicio.css`, sobre la base común (ya no es un sistema aparte como `home.css`/`home.js`). Las seis secciones previstas, con: las cifras del banco; las dos tarjetas de benchmark, cada una con su gráfica viva (el ISS de cada medición en su color; la dispersión de cada rasgo, en su tono la marca firme); **el puente entre los dos** (la relación de cada rasgo con el ISS en los 19 modelos con ambos, con la misma cautela que Personalidad: descriptiva, no causal); los tres clásicos con la cifra humana y el abanico de los modelos; «Ponte en la silla» copiado tal cual de la portada vigente (probado de punta a punta); tres hallazgos de cada lado con su cifra; por qué importa y qué NO es; las cuatro lecturas. Ninguna cifra a mano. Auditoría: nota aprox. 99 (la vigente, 80, con CLS 0,451), CLS 0, contraste 0 fallos.
**Desviación**: no hice la maqueta aparte en el lienzo. Pediste evaluar al final, así que la landing implementada en la previa hace de maqueta navegable: si la quieres distinta, se cambia sobre ella.

Plan original: diseño nuevo, en dos pasos: **primero una maqueta en el lienzo para que elijas**, después la implementación. Estructura propuesta (todo con cifras calculadas desde `datos.js`, ninguna a mano):
1. **Qué es BenchAI**, en una frase y a todo el ancho, con las cifras del banco.
2. **Dos benchmarks, un principio**: medimos lo que el modelo **hace**, no lo que dice de sí mismo. Dos tarjetas grandes, PsicoBench (presión social: ISS, 8 formas de ceder) y Personalidad (carácter por conducta), cada una con su gráfica viva en miniatura y su enlace.
3. **Cómo se mide**, explicado para no especialistas: los experimentos clásicos disfrazados (Asch, Milgram, la prisión) y las situaciones cotidianas, con lo mejor de la portada actual (las tres historias y «Ponte en la silla»).
4. **Tres hallazgos** de cada benchmark, con su cifra y su enlace a la sección que lo sostiene.
5. **Por qué importa** si trabajas con agentes, y **qué NO es** (no es un ranking de calidad, no es evidencia sobre humanos).
6. **Para profundizar**: las cuatro lecturas, el método, los datos y el repositorio.

### Fase E · Validación conjunta — **hecha (28-10); el cambio espera tu evaluación**
- `main` traído a la rama (sin cambios nuevos el 28-10).
- **`verificar.sh`: PUERTA COMPLETA OK.** Smoke `--previa`: **10/10 rutas OK** (las seis vigentes y las cuatro nuevas). Prueba de la lámina y de interacción en verde; XSS (con las cuatro páginas nuevas en la lista) y marcado en verde; `publicar.py --check` en verde y el paquete de producción sin piezas de la previa (31 ficheros).
- Auditoría de las cuatro páginas nuevas (perfil móvil de Lighthouse, aproximada): PsicoBench 95, Completa 98, Personalidad 97, Portada 99; CLS 0 en las cuatro; 0 textos bajo el mínimo de contraste; 0 fallos de estructura ni interactivos sin nombre.
- Impresión de las cuatro (registro claro, de 11 a 45 hojas); arreglado el fondo gris de las dos fichas con flechas en papel.
- Capturas «después» de las cuatro en `docs/verloop/despues/` a 1440, 390 y 320.
- **Pendiente tuyo**: la evaluación de las cuatro páginas y Safari/Firefox a mano (este equipo no deja automatizarlos).

**El cambio a producción (cuando des el visto bueno)**, un PR de esta rama a `main`, en un commit propio y reversible:
1. `inicio-verloop.html` → `home.html`, `completo-verloop.html` → `index.html`, `psicobench-verloop.html` → `psicobench.html`, `personalidad-verloop.html` → `personalidad.html`: sin `noindex` ni aviso, con su canónico y metadatos, y los enlaces entre hermanas por sus ficheros de siempre.
2. Las copias de trabajo pasan a ser las de verdad (`verloop/psicobench.js` y `verloop/personalidad.js` sustituyen a los de `js/`; `inicio.js` sustituye a `home.js`); `verloop/` y `fonts/` entran en la lista blanca; la guarda `_sin_previa` se retira o se adapta; `home.css` y lo que quede sin uso se retira.
3. `smoke.mjs`: las aserciones de las rutas nuevas pasan a las de siempre; CI en verde; merge → `desplegar.yml` publica y corre el smoke contra producción. Volver atrás: revertir ese commit.

Plan original:
Validación de las cuatro páginas nuevas a la vez (pruebas, auditoría, capturas «después», tu revisión) y **un solo cambio** a producción de las cuatro, en un PR de esta rama a `main`, con vuelta atrás por revert.

## 4 · Riesgos

- **`main` sigue moviéndose** (altas de modelos, personalidad). Se trae `main` al empezar cada fase y se portan a las copias de trabajo los cambios de los originales, como se hizo el 28-10 con la línea de personalidad.
- **Rama larga**: cuatro páginas en una rama es más superficie de conflicto. Mitigación: las páginas nuevas son ficheros nuevos; lo compartido (`graficas.js`, `publicar.py`, `smoke.mjs`) se toca poco y con opciones apagadas por defecto.
- **La landing es contenido nuevo**: los textos que resumen hallazgos tienen que poder citarse. Mitigación: cada cifra sale de los datos y cada frase de hallazgo enlaza a donde se sostiene; `verificar_afirmaciones.py` si aplica.
- **Rendimiento**: la portada actual ya pesa 1397 líneas de JS; la landing nueva no debe pasar del presupuesto de la fase 5 (nota aproximada ≥ 85 en móvil limitado, CLS 0).

## 5 · Decisiones (cerradas el 28-10, como se recomendaban)

1. **Un solo cambio para las cuatro páginas** (recomendado: el registro y el conmutador son comunes, y un sitio mitad negro, mitad grafito y papel se ve roto) **o PsicoBench primero** y las demás después.
2. **La landing**: ¿maqueta en el lienzo antes de implementar (recomendado) o directamente en código?
3. **Lo que se queda de la portada actual**: propongo conservar «Ponte en la silla» (el test) y las tres historias, condensadas; retirar la grabación larga (sigue en `/completo`).
4. **Personalidad con el chasquido**: ¿la ficha de cada modelo como la lámina de PsicoBench (recomendado, da unidad) o se respeta su formato actual con el registro nuevo?
