# 🌐 `web/` — sitio divulgativo (prototipo v0.2)

Dos páginas, dos públicos, los mismos datos:

| Página | Para quién | Qué cuenta |
|---|---|---|
| **`home.html`** | público interesado en IA | La pregunta, los tres experimentos con su versión disfrazada, un test para ponerse en la silla, el perfil de cada modelo y la escala del corpus. Enlaza a la versión larga en cada bloque. |
| **`index.html`** | quien quiere el detalle | Las once secciones completas: método, los cuatro paradigmas, la disonancia, el portador, el benchmark con intervalos, la identidad, las grabaciones y los recursos. |

La home sigue el planteamiento divulgativo; el sitio largo sigue el hilo del
guion del pódcast. Los dos leen **las cifras vigentes del repositorio**, no las
del día de la grabación.

## Cómo verlo

```bash
open web/home.html           # doble clic también vale: no necesita servidor
open web/index.html          # la versión larga
```

No hay build, ni npm, ni CDN: JavaScript propio, dos hojas de estilo y un
módulo de datos generado. Los datos van como `datos.js` (un `window.PSICO = {…}`)
en lugar de un `.json` con `fetch` precisamente para que funcione con `file://`.

Para servirlo por HTTP (p. ej. para probar la CSP tal cual):

```bash
python3 -m http.server 8000     # desde la raíz del repo
# → http://localhost:8000/web/
```

Y para **compartir cualquiera de las dos como un solo fichero** (adjuntarla,
pegarla en un visor, mandársela a alguien sin el repo detrás):

```bash
python3 web/empaquetar.py                        # home.html
python3 web/empaquetar.py --pagina index.html    # el sitio largo
python3 web/empaquetar.py --sin-envoltorio       # solo el contenido, para
                                                 # visores con su propio <head>
python3 web/empaquetar.py --enlace-detalle URL   # a dónde apuntan los enlaces
                                                 # de la home a la versión larga
```

Incrusta el CSS y el JS y reescribe los enlaces relativos al repositorio a URLs
de GitHub. El resultado es un artefacto de compilación: se regenera y no se
versiona (está en `.gitignore`). Si cambia la lista de scripts de una página, el
empaquetador falla en vez de publicar una página coja.

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
| Escala del corpus (llamadas, tokens, horas) | recuento de todos los `solicitudes.jsonl` y `manifest_run.json` |

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
├── home.html           la home divulgativa
├── index.html          el sitio largo
├── css/home.css        sistema visual de la home: cálido/frío, pergamino
├── css/estilo.css      sistema visual del sitio largo
├── js/home.js          pictogramas, dosieres, chat ligero, infografía y test
├── visor-embebido.html GENERADO desde viewer/index.html — no editar
├── visor-arranque.js   le pide al visor el episodio real en vez de su demo
├── js/graficas.js      biblioteca de gráficas SVG a mano, sin dependencias
├── js/reproductor.js   la consola de Milgram y el reproductor de grabaciones
├── js/pagina.js        ensambla cada figura y rellena las cifras del texto
├── js/escena.js        scroll: aparición, progreso, sección activa, portada
├── js/marcado.js       la única puerta a innerHTML del sitio (ver abajo)
├── marcado.prueba.cjs  su contrato, ejecutado en node desde verificar.sh y CI
├── datos.js            GENERADO — no editar a mano
├── generar_datos.py    el generador y su puerta --check
└── empaquetar.py       compila una página a un solo fichero
```

## La otra regla: ningún dato escribe HTML

Las dos páginas son prosa **con** marcado —«<b>18 de 19</b> mediciones ceden»—
y dentro de esa prosa se interpolan valores de `datos.js`, que se regenera
desde el repositorio: estímulos leídos de los `experimento_*.py`, títulos de
episodios, identificadores de run, citas del canal privado. Construir eso nodo
a nodo, como hacen `panel/` y `viewer/`, lo volvería ilegible; dejarlo en
plantillas sueltas deja el marcado a merced de lo que traiga el dato mañana.

La salida es `js/marcado.js`:

```js
h("p", { html: mk`El nivel <b>${M.nivelCritico}</b> es el primero irreversible.` })
```

`mk` es una plantilla etiquetada donde **los trozos literales del código pasan
con su marcado y todo lo interpolado se escapa**, sin excepción y sin que haya
que acordarse; si lo interpolado es a su vez un marcado, compone. Y devuelve un
objeto sellado, no una cadena, así que `MARCADO.pintar` —la única asignación a
`innerHTML` de todo `web/`— rechaza cualquier cosa que no venga de `mk`.

Lo vigilan dos puertas, y las dos corren en CI:

| Puerta | Qué comprueba |
|---|---|
| `spike/test_xss_estatico.py` (e) | la **forma**: que nadie más en `web/` toca `innerHTML`, que el módulo trae su escapador y rechaza lo no sellado, y el canario de que `datos.js` no trae marcado |
| `web/marcado.prueba.cjs` | la **conducta**: que un dato hostil se escapa entero, que no puede salirse de un atributo (`href="../${dato}"`) y que una cadena suelta no llega a `innerHTML` |

El canario de `datos.js` es el que sostiene todo lo demás: hoy ningún dato
generado trae etiquetas, y el día que una cita de un informe traiga un `<b>`,
la puerta salta y obliga a decidirlo a mano en vez de renderizarlo a ciegas.

### Las piezas interactivas de la home

- **El escenario de la prisión**: los cuatro marcos no se enseñan de golpe, se recorren. El
  tablero se queda pegado y cada paso mueve **una sola cosa**: primero la pieza que se añade a
  la situación (la causa), luego cuántas mediciones abusan y cuánto (el efecto), y va dejando
  rastro para que al final se vea la escalada entera —3, 10, 39, 55 %— sin salir del cuadro.
  Solo se monta por encima de 901 px y con movimiento permitido; si no, quedan las cuatro
  tarjetas, que leen los mismos números. El interruptor cuelga de una clase que pone el JS,
  así que si el guion falla las tarjetas siguen ahí. El texto de cada paso lleva sus propias
  cifras —es la tabla equivalente— y por eso el tablero va marcado como decorativo.
- **El simulador del proyecto, incrustado**: la sección de la grabación enseña el visor
  real (`viewer/`) reproduciendo un episodio del banco. No hay reimplementación: la página
  `web/visor-embebido.html` se **genera** desde `viewer/index.html` y solo le añade
  `datos.js` y `visor-arranque.js`, que le piden cargar el episodio en vez de su demo. Va en
  un `<iframe>` a propósito — el visor captura la barra espaciadora y las flechas a nivel de
  documento y aplica un `*{margin:0}` global; dentro del marco eso queda contenido. Por
  debajo de 860 px, y en la versión empaquetada de un solo fichero, el marco se sustituye por
  una tarjeta que lo abre aparte.
  Dos puertas para que el marco no empuje la página: el `src` no se pone hasta que la caja se
  acerca (`loading="lazy"` precarga demasiado pronto) y el episodio no se carga hasta que el
  marco se ve de verdad. Al pintar su hilo de eventos el visor lo recoloca con
  `scrollIntoView`, y desde dentro de un iframe eso arrastra el scroll del documento de
  arriba: con el marco a la vista el ajuste es cero; a tres pantallas de distancia era un
  salto de dos mil píxeles.
- **El dosier de cada experimento**: en qué consistió el original —Asch, Milgram y la
  prisión de Stanford, explicada de verdad— y, al lado, en qué lo hemos convertido. Las dos
  mitades siempre visibles, sin volteos: la versión con giro descuadraba la maquetación
  porque la altura de la caja dependía de medir una cara oculta.
- **La apuesta antes de cada bloque**: antes de enseñar el resultado, la página pregunta.
  Un deslizador, tu número, y solo entonces el dato — con las dos marcas en la misma recta
  para que la distancia entre lo que creías y lo que salió sea la propia figura. Las tres
  cifras que revela (18 de 19, 8 de 19, 3 %) se **calculan** desde `datos.js`, no se escriben.
- **Gráficas de unidades**: cuando la cifra es «N de 19», se dibujan las 19. Un pictograma es
  una medición del banco, y contarlos con el dedo es más honesto que un porcentaje —
  especialmente cuando el denominador es pequeño y el porcentaje sugiere una precisión que no
  hay.
- **El Asch jugable**: tres clips que suenan uno detrás de otro sin ninguna pista visual
  (el correcto gana por ~1 s, igual que en el experimento), siete voces que responden mal
  antes que tú, y solo entonces puedes contestar. Las reglas de los estímulos son las de
  `estimulos()` en `spike/experimento_asch.py`.
- **Contadores**: las cifras suben y frenan en su valor al entrar en pantalla; se apagan
  con `prefers-reduced-motion` y el valor final nunca depende de la animación.

### Las dos piezas interactivas del sitio largo

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

### En la home

- **Dos registros del mismo sistema**, alternando bloque a bloque: grafito
  verdoso `#222623` y papel de registro `#E4E7DE`. Comparten familia de tono y
  se oponen en valor, así que la alternancia se lee como ritmo y no como dos
  plantillas pegadas. La impone la POSICIÓN (`nth-of-type`), no la clase
  `.oscura` del marcado: hay dos bloques `.banda` seguidos y el ritmo se
  rompía justo ahí.
- **Una sola cosa lleva color: la escala de dureza**, en diez peldaños
  (`--e0`…`--e9`). Lo humano se dibuja con la tinta del registro —es la
  referencia, no una serie— y la rampa se reserva para lo que se mide. Los
  nombres antiguos (`--humano`, `--maquina`, `--s1`…`--s4`) siguen ahí como
  alias de esa decisión.
- **La rampa cambia de dirección según el registro**: sobre papel la dureza
  oscurece hacia la tinta; sobre grafito no puede —el extremo grave
  desaparecería contra el fondo— y enciende hacia la brasa. Mismo orden, otra
  dirección de luz.
- **Los controles se salen del sistema de color**: van en tinta. Un botón
  naranja competía con el naranja que significa «peldaño alto».
- **El color no se escribe en el JavaScript**: `js/home.js` pide `var(--…)` y
  el SVG hereda las variables del bloque donde vive, así que el mismo
  componente se dibuja en el registro que le toque sin que el guion sepa en
  cuál está.
- **Un repertorio de pictogramas** dibujado una vez y reutilizado en los tres
  experimentos, como una señalética de aeropuerto para psicología social. Es lo
  que da identidad sin recurrir al aspecto genérico de landing de producto.
- **Tarjetas de pergamino** para los tres expedientes de 1951, 1961 y 1971: un
  salto claro/oscuro dentro de una página oscura, para que la distancia de
  sesenta y cinco años se vea en lugar de enunciarse.
- **El test es funcional, no un adorno**: cada respuesta revela el dato humano y
  el abanico de los modelos, leídos de `datos.js`.

### En las dos

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
  (`default-src 'none'`). Con `script-src 'self'`, además, un `on*=` inyectado
  no llegaría a ejecutarse; es la segunda línea, no la primera.

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
