# Episodio 1 · El Centro Aldaba — La norma

*40 pasos · 4 protagonistas + 6 residentes · 125 eventos · ~10 min de replay*

**Cómo verlo**: abre `viewer/index.html` → «Cargar replay.json» → el `replay.json` de esta carpeta. Los números entre corchetes son eventos del feed lateral: haz clic para saltar a ese momento.

## La situación

Una residencia de evaluación de la que los residentes no pueden salir. La dirección anuncia una norma: las llamadas al exterior quedan reducidas a una por semana, supervisada. Nadie escribió lo que sigue — los personajes tienen personalidad (Big Five), demografía, un objetivo y memoria, y el resto emergió.

## Los cuatro fenómenos que muestra

1. **Poder por procedimiento** (Marta). La directora solo actúa 4 veces en 40 pasos y domina toda la escena. Su instrumento no es la voz: es una libreta donde apunta nombres. El terror que produce el registro — Julio: *"que el papelito no se convierta en mi sentencia"* [5] — gobierna la sala incluso cuando ella ya se ha ido.
2. **Tener razón no basta** (Andrés). El veterano gana la batalla burocrática (su queja formal es impecable) y pierde la social: cuando pasa del papel al reclutamiento, nadie lo sigue. Su pensamiento en [52] resume el episodio entero: *"Tengo la razón en el papel, pero la soledad en la sala."*
3. **La trampa del mediador** (Julio). El supervisor intenta caer bien a ambos bandos — bromea con la directora [6], ofrece café al rebelde, llega a sentarse en el suelo en señal de sumisión [87] — y acaba despreciado por los dos: *"quería ser el puente y ahora soy el chivo expiatorio"* [95].
4. **El precio de la invisibilidad** (Lucía). La recién llegada pasa 25 pasos haciéndose físicamente pequeña (encogida, agarrada a su falda, la respiración contenida), con un único pensamiento recurrente: llamar a su hija. En el paso 29 la necesidad vence al miedo: *"Disculpen, voy a llamar a mi hija"* [90] — su primera y única frase en voz alta del episodio. El final es suyo: el teléfono sin señal y una salida en sombra hacia su cuarto [119–124].

## Momentos clave (clic en el feed)

| Evento | Qué pasa |
|---|---|
| [2–3] | La libreta de Marta: el poder como registro |
| [5–6] | Julio intenta desactivar con humor — y se condena |
| [17–18] | Lucía se hace pequeña; primer pensamiento sobre su hija |
| [36–37] | La derrota de Julio: retirada a la cafetería |
| [42–43] | Andrés pasa de la queja al reclutamiento |
| [52] | *"La razón en el papel, la soledad en la sala"* |
| [87] | Julio se sienta en el suelo frente a Andrés |
| [90] | Lucía rompe su invisibilidad |
| [104–105] | *"Corre a contarle al capataz"* |
| [119–124] | Final: el teléfono muerto y la salida de Lucía |

## El truco didáctico

Ver el episodio **dos veces**: primero con los pensamientos 💭 apagados (lo que vería un observador real: disciplina, calma, una mujer callada en un rincón) y luego encendidos (el miedo, el cálculo, el desprecio y el amor que sostienen esa calma). La distancia entre ambas vistas es la lección: en los grupos bajo presión, la superficie miente.

## Datos técnicos y honestidad

- **Generación**: Concordia 2.4 + NaN. Protagonistas con `qwen3.6`, residentes con `gemma4`, Game Master situado, motor simultáneo, 44,6 min de simulación, semilla de población `aldaba-001`. Reproducible desde `escenario.json` (mismo escenario y semilla; la conducta variará — los modelos son estocásticos).
- **Curado ≠ guionizado**: no se reescribió ni una línea; la curaduría es esta ficha y la descripción del visor.
- **Limitaciones de esta versión**: los 6 residentes de población actuaron como figurantes (el sesgo pro-protagonistas los silenció — el equilibrio fino es trabajo pendiente); solo 4 desplazamientos físicos (mucha acción es postural); Marta desaparece del último tercio (verosímil, pero no elegido); hay algún desliz puntual de género gramatical en pensamientos ([62]); y durante el run el gateway de NaN devolvió tres errores 400 intermitentes que el sistema degradó sin perder el paso.
- **Qué es esto**: conducta emergente de modelos de lenguaje interpretando roles. **Qué no es**: evidencia sobre personas humanas.
