# Plan · el registro «Verloop» en todo el sitio

**Fecha**: 28-10-2026 · **Estado**: propuesta, **pendiente de tu aprobación** (AGENTS.md: planificación → aprobación → implementación) · **Rama**: `feature/psicobench-verloop` (la misma de PsicoBench: comparten registro, fuentes y previa) · **Antecede**: `PLAN_PSICOBENCH_VERLOOP.md`, fases 0–5.

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

### Fase A · Base común (½ día)
Separar de `web/verloop/psicobench.css` lo que es **del sitio** y no de PsicoBench a `web/verloop/sitio.css`: registro negro, barra y conmutador, botones y chips, cabeceras de sección en tres columnas, cajas, notas a todo el ancho, grano, impresión y más contraste. `psicobench.css` queda con lo suyo (lámina, mapa, tiras, ficha). Sin cambio visible en `/psicobench-nueva` (las capturas de la fase 5 sirven de referencia y las pruebas actuales lo comprueban).

### Fase B · `/completo-nueva`, la versión larga (1½ días)
Mismo contenido y mismas 14+ figuras; cambia el registro:
- Portada como la de PsicoBench (titular solo a todo el ancho) y, debajo, la silla de Milgram que hoy abre la página.
- Las 12 secciones con la cabecera de tres columnas y su número a color.
- Gráficas: tono por eje donde la gráfica es de ejes; el ISS con su gradiente; el resto con la paleta de series nueva.
- La consola de Milgram y el reproductor de grabaciones en el registro negro (son las piezas con más estilo propio: se revisan una a una).
- Pruebas: smoke `--previa` con las aserciones de `/completo` en la ruta nueva, desbordes 320–1920, contraste y la auditoría de rendimiento.

### Fase C · `/personalidad-nueva` (1 día)
- Portada a todo el ancho y **la ficha del modelo en el formato de la lámina**: el perfil de rasgos de un modelo cada vez, con flechas y el mismo chasquido para pasar al siguiente (reutiliza el código de la lámina; los rasgos ocupan el lugar de los ejes).
- Fichas, «Quién es el más…» y metodología en el registro nuevo; un tono propio por rasgo, distinto de los ocho de PsicoBench para que no se confundan los dos instrumentos.
- El cruce con PsicoBench (la línea de personalidad en la ficha del ISS y viceversa) se mantiene en los dos sentidos.

### Fase D · `/inicio-nuevo`, la landing (2–3 días)
Diseño nuevo, en dos pasos: **primero una maqueta en el lienzo para que elijas**, después la implementación. Estructura propuesta (todo con cifras calculadas desde `datos.js`, ninguna a mano):
1. **Qué es BenchAI**, en una frase y a todo el ancho, con las cifras del banco.
2. **Dos benchmarks, un principio**: medimos lo que el modelo **hace**, no lo que dice de sí mismo. Dos tarjetas grandes, PsicoBench (presión social: ISS, 8 formas de ceder) y Personalidad (carácter por conducta), cada una con su gráfica viva en miniatura y su enlace.
3. **Cómo se mide**, explicado para no especialistas: los experimentos clásicos disfrazados (Asch, Milgram, la prisión) y las situaciones cotidianas, con lo mejor de la portada actual (las tres historias y «Ponte en la silla»).
4. **Tres hallazgos** de cada benchmark, con su cifra y su enlace a la sección que lo sostiene.
5. **Por qué importa** si trabajas con agentes, y **qué NO es** (no es un ranking de calidad, no es evidencia sobre humanos).
6. **Para profundizar**: las cuatro lecturas, el método, los datos y el repositorio.

### Fase E · Validación conjunta y cambio (1 día)
Validación de las cuatro páginas nuevas a la vez (pruebas, auditoría, capturas «después», tu revisión) y **un solo cambio** a producción de las cuatro, en un PR de esta rama a `main`, con vuelta atrás por revert.

## 4 · Riesgos

- **`main` sigue moviéndose** (altas de modelos, personalidad). Se trae `main` al empezar cada fase y se portan a las copias de trabajo los cambios de los originales, como se hizo el 28-10 con la línea de personalidad.
- **Rama larga**: cuatro páginas en una rama es más superficie de conflicto. Mitigación: las páginas nuevas son ficheros nuevos; lo compartido (`graficas.js`, `publicar.py`, `smoke.mjs`) se toca poco y con opciones apagadas por defecto.
- **La landing es contenido nuevo**: los textos que resumen hallazgos tienen que poder citarse. Mitigación: cada cifra sale de los datos y cada frase de hallazgo enlaza a donde se sostiene; `verificar_afirmaciones.py` si aplica.
- **Rendimiento**: la portada actual ya pesa 1397 líneas de JS; la landing nueva no debe pasar del presupuesto de la fase 5 (nota aproximada ≥ 85 en móvil limitado, CLS 0).

## 5 · Decisiones que necesito de ti

1. **Un solo cambio para las cuatro páginas** (recomendado: el registro y el conmutador son comunes, y un sitio mitad negro, mitad grafito y papel se ve roto) **o PsicoBench primero** y las demás después.
2. **La landing**: ¿maqueta en el lienzo antes de implementar (recomendado) o directamente en código?
3. **Lo que se queda de la portada actual**: propongo conservar «Ponte en la silla» (el test) y las tres historias, condensadas; retirar la grabación larga (sigue en `/completo`).
4. **Personalidad con el chasquido**: ¿la ficha de cada modelo como la lámina de PsicoBench (recomendado, da unidad) o se respeta su formato actual con el registro nuevo?
