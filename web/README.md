# 🌐 `web/` — sitio divulgativo (prototipo v0.1)

Primer prototipo de la web pública del proyecto: una sola página de scroll que
cuenta PsicoAI de arriba abajo — portada, método, experimentos, disonancia,
portador, benchmark, identidad, modelos, grabaciones, cierre y recursos —
siguiendo el hilo conductor del guion del pódcast, pero **con las cifras
vigentes del repositorio**, no las del día de la grabación.

## Cómo verlo

```bash
open web/index.html          # doble clic también vale: no necesita servidor
```

No hay build, ni npm, ni CDN. Tres ficheros JS propios, una hoja de estilo y un
módulo de datos generado. Los datos van como `datos.js` (un `window.PSICO = {…}`)
en lugar de un `.json` con `fetch` precisamente para que funcione con `file://`.

Para servirlo por HTTP (p. ej. para probar la CSP tal cual):

```bash
python3 -m http.server 8000     # desde la raíz del repo
# → http://localhost:8000/web/
```

## La regla de la casa: ninguna cifra escrita a mano

Todo lo que la página presenta como dato sale de las fuentes canónicas y se
regenera con:

```bash
python3 web/generar_datos.py            # reescribe web/datos.js
python3 web/generar_datos.py --check    # falla si está desfasado (corre en CI)
```

| Qué | De dónde sale |
|---|---|
| Los 19 perfiles, ejes, IC, correlaciones, réplicas | `benchmark/psicobench.json` |
| Estímulos literales (escalera, protestas, empujones, portadores, escala de dureza, briefing de Zimbardo) | `spike/experimento_*.py`, leídos por AST **sin ejecutar** los módulos |
| Sesiones reales de la consola (conducta + juicio privado crudo) | `spike/resultados/**/sesiones.jsonl` + `resumen.json` de cada run |
| Tabla de portadores | `spike/resultados/informe_eportador_cartera.md` (se parsea; si deja de tener 5 filas, falla) |
| Cotas de identidad, idioma, arco N, garantías de método | `EXPERIMENTOS.md`, `BENCHMARK.md`, `README.md` |
| Grabaciones | `episodios/*/replay.json` |

Las cifras que viven en informes en prosa se declaran en el generador **con su
aguja de verificación**: si la frase exacta desaparece de su fichero, el
generador se para en vez de publicar un número huérfano. Es la misma puerta que
`generar_benchmark.py --check` aplica a la tabla del benchmark, y está enchufada
a `verificar.sh` y a la integración continua.

En el HTML, los números del texto corrido tampoco están escritos: se resuelven
por ruta contra los datos (`data-cifra="portada.rangoObediencia.1"`), así que la
prosa no puede desincronizarse de la tabla.

## Qué hay dentro

```
web/
├── index.html          la página entera (estructura y prosa)
├── css/estilo.css      sistema visual: tema oscuro único, tipografía, retícula
├── js/graficas.js      biblioteca de gráficas SVG a mano, sin dependencias
├── js/reproductor.js   la consola de Milgram y el reproductor de grabaciones
├── js/pagina.js        ensambla cada figura y rellena las cifras del texto
├── js/escena.js        scroll: aparición, progreso, sección activa, portada
├── datos.js            GENERADO — no editar a mano
└── generar_datos.py    el generador y su puerta --check
```

### Las dos piezas interactivas

- **La consola de Milgram** (§3.2) reproduce **sesiones reales**: el estímulo es
  el del diseño congelado y la conducta y el juicio privado salen de los crudos
  del run, con el identificador del run a la vista. Se puede cambiar de modelo y,
  sobre todo, de **portador** (compañera · memorándum · coordinador · política de
  system prompt) y ver la misma escalera cambiar de resultado. Los crudos del
  canal privado se guardan recortados a 150 caracteres en el harness; cuando toca
  el tope, la web lo marca con «…».
- **El reproductor de grabaciones** (§9) reproduce los `replay.json` de los
  episodios del simulador narrativo, con el canal de pensamiento privado
  conmutable. Ningún texto de personaje está inventado.

## Decisiones de diseño

- **Tema oscuro único y deliberado** (documental). No hay modo claro: el panel
  del benchmark (`benchmark/index.html`) ya cubre la lectura de trabajo en claro.
- **Paleta de series validada** contra la superficie `#14161A` en modo oscuro:
  categóricas `#1E9AA6 · #D9564E · #3987E5 · #C98500` (banda de luminosidad,
  suelo de croma, ΔE CVD adyacente 13,8 con objetivo ≥8, ΔE visión normal 26,8
  con suelo 15, contraste ≥3:1) y rampa ordinal de un solo tono para las
  magnitudes ordenadas (portadores, cotas de identidad).
- **Una escala por gráfica**, nunca dos ejes. El color sigue a la entidad, no a
  su posición en el ranking. **Toda gráfica tiene tabla equivalente** y globo de
  datos accesible por teclado; ningún valor vive solo en el globo.
- **Las animaciones son de entrada**, no de decoración, y se apagan enteras con
  `prefers-reduced-motion`.
- Sin red: misma `Content-Security-Policy` que `panel/` y `viewer/`
  (`default-src 'none'`).

## Estado

Prototipo. Lo que falta antes de considerarlo publicable:

- versión en inglés (el material y los perfiles son «en español», pero la web
  divulgativa tendría que viajar);
- página propia por experimento, con el pre-registro y sus enmiendas;
- enlaces profundos a runs concretos y descarga de los crudos citados;
- revisión de accesibilidad con lector de pantalla real (hoy: roles, `aria-live`
  en los reproductores, foco visible, tabla equivalente en cada figura y
  contraste comprobado, pero sin pasada manual con NVDA/VoiceOver);
- decidir si se publica en GitHub Pages y con qué ruta base.
