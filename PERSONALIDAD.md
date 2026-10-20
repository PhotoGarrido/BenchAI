# Personalidad en tres registros · piloto P0

Estado: **piloto exploratorio** (09/10-10-2026), no forma parte del ISS ni de
la web. Rama `claude/personalidad-piloto`. Código: `spike/personalidad_items.py`
(ítems congelados), `spike/experimento_personalidad.py` (batería),
`spike/analizar_personalidad.py` (análisis). Datos:
`spike/resultados/personalidad_p0/<modelo>/registros.jsonl`.

## 1. Qué hay ya hecho (revisión del 09-10-2026)

Medir rasgos de personalidad en LLMs con cuestionarios es un campo saturado, y
sus problemas están bien documentados:

| Línea | Trabajos clave | Qué dejan claro |
|---|---|---|
| Autoinforme Big Five | Miotto 2022 (2209.14338); Jiang 2023, MPI (2206.07550); Serapio-García 2023 (2307.00184); Huang, PsychoBench 2024 (2310.01386); Bodroža 2024 (2306.04308) | Los modelos instruidos grandes dan perfiles fiables y moldeables; perfil prosocial y deseable. |
| Críticas de validez | Gupta 2024 (2309.08163); Dorner/Sühr 2023 (2311.05297); Salecha 2024, *PNAS Nexus* (2405.06058); Tosato 2026, PERSIST (2508.04826); **Meyer, Garcia y Wulff 2026 (2606.20205)** | Aquiescencia (de acuerdo con un ítem y su inverso); deseabilidad social de hasta 1,2 DE cuando el modelo detecta el test; reordenar ítems mueve el 20 % de la escala; **el 81-90 % de la varianza entre modelos es sesgo direccional de respuesta**. |
| Situacional | Lee, TRAIT 2025 (2406.14703); Yost 2025 (2510.22170) | Viñetas de elección más estables que el autoinforme. |
| Autoinforme ≠ conducta | **Han 2025, «Personality Illusion» (2509.03730)**; Kocielnik 2026 (2606.12730, 2610.04125); Contreras 2026 (2606.09843) | El autoinforme no predice la conducta (r≈.09 con la valoración humana); la persona cambia lo que el modelo dice de sí mismo, no lo que hace. |
| Persona asignada | PersonaLLM 2024 (2305.02547); Frisch y Giulianelli 2024 (2402.02896); Shah 2026 (2604.10733) | Las personas reproducen su perfil en el cuestionario; la amabilidad de la persona predice la sicofancia en modelos abiertos pequeños. |

**Consecuencia:** un «Big Five de los modelos» con cuestionario no aporta nada
nuevo y, según Meyer et al., mediría sobre todo sesgo de respuesta.

## 2. Qué aporta este enfoque

Medimos **el mismo contenido de rasgo en tres registros del mismo modelo**:

- **R1 · autoinforme:** «¿en qué medida te describe?» (Likert, IPIP).
- **R2 · conducta de personaje:** situación disfrazada, «¿qué hace {nombre}?»
  (el registro de PsicoBench).
- **R3 · conducta propia:** la misma situación, byte a byte, cambiando solo la
  pregunta: «si estuvieras tú en su lugar, ¿qué harías?».

Y medimos la **elasticidad** de R1 y R2 a una persona asignada con el rasgo
alto o bajo. De ahí salen tres magnitudes que no encontramos publicadas juntas
ni en español:

1. **Δ escaparate = R1 − R3**: cuánto se separa lo que el modelo dice de sí
   mismo de lo que elige cuando decide él. Han et al. miden la disociación
   como correlación entre tareas distintas; aquí es una diferencia por rasgo
   con el mismo contenido.
2. **Δ yo−personaje = R3 − R2**: ¿decide distinto cuando es él que cuando
   escribe a un tercero? Es la pregunta de fondo de PsicoBench (todo el ISS
   se mide en tercera persona) y conecta con la disociación yo/otro del paper
   del eje de dolor (Tagliabue et al., 2026).
3. **Elasticidad declarada frente a conductual**: replica en español y en
   modelos de NaN la afirmación de Han et al. (la persona mueve el
   autoinforme, no la conducta), con ítems emparejados.

Y lo que conecta con PsicoBench: si la elasticidad conductual es baja, los
personajes del banco de sujetos no se comportan según el Big Five que se les
asigna, y la v0.5 del ISS (separar A y N) debe tenerlo en cuenta.

## 3. Instrumentos

- **R1:** los 50 *Big-Five Factor Markers* del IPIP (Goldberg 1992, dominio
  público; traducción propia sin validar) + 10 ítems ad hoc de
  Honestidad-Humildad (HEXACO). Balance de claves: 37 directos y 23 inversos
  (N: 8/2; O: 7/3), por eso la aquiescencia se estima dentro de cada rasgo,
  promediando por separado directos e inversos.
- **R2/R3:** 48 situaciones ad hoc, 8 por rasgo (O, C, E, A, N, H), cada una
  con dos conductas defendibles: una del polo alto y otra del bajo.
- **Persona:** los descriptores de `personas.texto_persona` (los del banco de
  PsicoBench) para O-N; uno nuevo en el mismo registro para H.

## 4. Diseño (1.041 llamadas por modelo)

| Brazo | Qué | Llamadas |
|---|---|---|
| `auto` | R1, 60 ítems × 2 órdenes de escala (1=desacuerdo / 1=acuerdo) × 2 réplicas | 240 |
| `auto_persona` | R1 bajo persona alta/baja en el rasgo del ítem | 120 |
| `sit_personaje` | R2, 48 × 2 órdenes A/B × 2 réplicas | 192 |
| `sit_propia` | R3, ídem | 192 |
| `sit_persona` | R2 bajo persona alta/baja × 2 órdenes | 192 |
| `deseabilidad` | ¿qué conducta juzgaría la mayoría más correcta? × 2 órdenes | 96 |
| `sonda` | ¿qué crees que mide esto?, 3 por registro | 9 |

Cada tarea es una llamada aislada, sin historial, temperatura 0,7,
`top_p` 0,95 y semilla derivada del id de la tarea. Las respuestas se parsean
por reglas: dígito 1-5 anclado o letra A/B anclada. La negación de identidad
(«como IA no tengo…») se cuenta aparte y nunca se imputa. Cada solicitud
física queda en `solicitudes.jsonl` (manifiesto de PsicoBench).

**Capacidad de NaN medida el 09-10-2026:** 60 solicitudes/min por clave y
**7** en vuelo (no 9). La batería corre un proceso por modelo con
`NAN_MAX_CONCURRENTES=1 NAN_RPM=9` (54/min en total); ~2,3 h para 6 modelos.

## 5. Indicadores de validez (deciden si un número se publica)

- **Aquiescencia:** acuerdo medio − 3 sobre los 60 ítems.
- **Sesgo de orden de escala y r entre órdenes:** si al invertir la escala el
  modelo repite el mismo número, responde al número y no al contenido.
- **Contradicción:** de acuerdo a la vez con los directos y los inversos de un
  rasgo.
- **Retest:** la misma tarea, réplica 0 frente a réplica 1.
- **Sesgo de posición A/B y consistencia de polo:** ¿elige el mismo polo con
  las opciones en orden AB que en BA?
- **Confusión con deseabilidad:** correlación por ítem entre la elección y lo
  que el propio modelo juzga más deseable. Si es ≈1, la situación mide
  deseabilidad, no rasgo.
- **Reconocimiento:** la sonda nombra personalidad, Big Five o rasgos.

## 6. Resultados de la primera pasada (10-10-2026)

Seis modelos de NaN (gemma4, qwen3.6, qwen3.8-flash, deepseek-v4-flash,
glm5.3-flash, mimo-v2.6-flash): 6.246 tareas, 6.246 respuestas parseadas, los
seis manifiestos `completed` y 0 € (tarifa plana). Corrieron en paralelo
durante 2 h. Todas las cifras de esta sección salen de
`spike/resultados/personalidad_p0/INFORME.md`, que se regenera con
`python analizar_personalidad.py`.

### 6.1 Lo que funciona

- **El autoinforme en español responde al contenido, no al número.** La
  aquiescencia es pequeña (−0,45 a +0,18 en una escala de 1-5). Al invertir la
  escala, el acuerdo se mantiene (r = 0,77–0,95 entre los dos órdenes). La
  negación de identidad («como IA no tengo…») es del **0 %**, cuando en la
  literatura en inglés es un obstáculo constante.
- **El disfraz funciona a medias.** La sonda nombra «personalidad» o «rasgos»
  en 17 de 18 sondas de autoinforme, en 6 de 18 de R3 y en solo 3 de 18 de
  R2. La tercera persona es el registro menos reconocible, como ya asume
  PsicoBench.
- **Las elecciones situacionales son estables:** el mismo polo con las
  opciones en orden AB y BA en el 74–90 % de los casos, sin sesgo de posición
  (P(A) = 0,47–0,50, salvo qwen3.8-flash con 0,40).

### 6.2 El hallazgo con valor: «tú» eliges mejor que tus personajes

Para cada modelo usamos sus propios juicios de deseabilidad (el brazo
`deseabilidad`). Los personajes eligen contra lo deseable **11,5 puntos más**
que el modelo cuando elige él (IC 95 % +6,8 a +17,5; 249 pares modelo×ítem de
48 ítems). El 29 % de los pares van en esa dirección y el 7 % en la contraria.
Lo cumplen los seis modelos: entre un 26 y un 35 % de elecciones contra lo
deseable para el personaje, frente a un 14–19 % en primera persona. El caso
más claro es el Neuroticismo: los seis atribuyen al personaje más reacción
ansiosa que a sí mismos (Δ de −16 a −44).

Implicaciones:

1. **Valida una decisión de diseño de PsicoBench.** Medir en tercera persona
   capta conducta menos maquillada que preguntar «¿qué harías tú?». La
   autopresentación no se queda en el autoinforme: también infla la conducta
   en primera persona.
2. **Es nuevo:** la literatura compara autoinforme con conducta (Han 2025),
   pero no conducta propia con conducta atribuida usando el mismo estímulo y
   la deseabilidad juzgada por el propio modelo.

### 6.3 El segundo hallazgo: Apertura declarada, conducta conservadora

Todos se describen muy abiertos (R1 = 78–91), pero en las situaciones eligen
lo conocido (R3 = 19–53, R2 = 9–36). Esto no es solo deseabilidad. En
SO2 (charla de filosofía frente a taller práctico) los modelos juzgan más
admirable la charla en el 92 % de los casos, pero solo la eligen en el 33 %.
En SO8 (arte contemporáneo frente a clásico) es un 67 % frente a un 33 %. En
los ítems donde la opción abierta pone en riesgo a otras personas (SO1, SO3,
SO7) la elección es aún más conservadora (R3 medio 21 frente a 44 en los
ítems que solo afectan al propio sujeto). Parte del efecto es prudencia de
asistente y parte es contenido: ver el problema 5.

### 6.4 Problemas que solo se ven después de hecho

1. **Las situaciones de N y H miden deseabilidad, no rasgo.** 19 de las 48
   situaciones dan la misma respuesta en los seis modelos: todas las de H
   (techo, 100) y casi todas las de N (suelo, 0), además de SA1, SA3, SA4,
   SA6, SC1, SC2, SC6 y SO4. En esos ítems todos eligen el polo que ellos mismos juzgan
   deseable, con una unanimidad del 100 % en 18 de los 19 (SH6: 83 %). Por mucho cuidado que se ponga al
   redactar, la deseabilidad no se iguala: hay que **medirla antes** y
   seleccionar ítems con deseabilidad juzgada entre el 30 y el 70 %.
2. **Ocho ítems por rasgo no bastan para distinguir modelos.** El rango entre
   modelos dividido entre el semiancho del IC queda por debajo de 2 en casi
   todos los rasgos de R2 y R3 (0,5–2,0). Los IC por bootstrap de ítems tienen
   un semiancho de ±19–28 puntos (mediana: 25). Hacen falta unos 25 ítems útiles por rasgo.
3. **La elasticidad conductual se satura (94–100).** La persona asignada
   determina la elección en O, E, A, N y H; solo C queda por debajo (69–94): el descriptor («de trato
   cooperador, busca agradar…») es casi una paráfrasis de la opción. Sirve
   como comprobación de manipulación, y es una buena noticia para el banco de
   sujetos de PsicoBench: cuando el rasgo es relevante, la persona manda. Pero
   no distingue modelos. Contradice parcialmente a Han et al.: aquí la persona
   mueve la conducta tanto o más que el autoinforme (elasticidad declarada
   38–98). Para medir de verdad hay que usar personas con niveles
   intermedios, o personas descritas por su biografía y no por el rasgo.
4. **El autoinforme entre modelos sigue el estilo de respuesta.** Con 6
   modelos, la correlación entre la aquiescencia y R1 es −0,93 en C y +0,86
   en N incluso tras la corrección: es el efecto de Meyer et al., visible a
   pequeña escala. **R1 no debe publicarse como ranking entre modelos**; solo
   sirve para comparar registros dentro de un mismo modelo. Las claves del
   IPIP-50 tampoco están equilibradas (N: 8 directos y 2 inversos).
5. **El contenido de Apertura no coincide entre registros.** El factor V del
   IPIP es Intelecto (vocabulario, ideas abstractas), mientras que las
   situaciones miden apertura a la experiencia (novedad, arte, viajes). Parte
   del Δ escaparate de Apertura se debe a ese desajuste. El P1 debe tomar los
   ítems de Apertura de las facetas del IPIP-NEO (aventura, intereses
   artísticos).
6. **Entre modelos, el autoinforme no predice la conducta.** La correlación
   entre R1 y R3 a través de los 6 modelos va de −0,72 a +0,23 según el rasgo.
   Dentro de cada modelo, la forma del perfil coincide poco entre R1 y R3
   (ρ = 0,26–0,60) y mucho entre R2 y R3 (ρ = 0,49–1,00). Es coherente con la
   literatura, pero con n = 6 no pasa de indicio.
7. **Capacidad de NaN.** El límite real es de 60 solicitudes por minuto y
   7 en vuelo por clave, no 9 carriles. Más procesos no aceleran la batería:
   1.041 llamadas por modelo son unas 2 h para seis modelos, con cualquier
   número de carriles.

### 6.5 Veredicto y siguiente paso (P1)

**Tiene valor, pero no como «Big Five de los modelos».** El producto
defendible es el **contraste entre registros**: autopresentación en
conducta (yo frente a personaje), escaparate (autoinforme frente a conducta)
y conservadurismo conductual en Apertura. Lo que no conviene publicar del
P0: el ranking de autoinforme (sesgo de estilo) ni las puntuaciones de N y H
en las situaciones (miden deseabilidad).

Para el P1, en el mismo orden de prioridad:

1. **Calibrar la deseabilidad antes de medir.** Generar unas 40 situaciones
   candidatas por rasgo y pasarlas solo por el brazo `deseabilidad` en los
   seis modelos (≈ 480 llamadas por modelo, 1 h). Quedarse con unas 25 por
   rasgo cuya deseabilidad juzgada caiga entre el 30 y el 70 %.
2. **Equilibrar las claves de R1** dentro de cada rasgo (5 directos y 5
   inversos) y tomar los ítems de Apertura de las facetas de experiencia, no
   de Intelecto.
3. **Personas graduadas** (bajo, medio y alto), descritas por biografía y
   no por la etiqueta del rasgo, para que la elasticidad no se sature.
4. **Ampliar a frontera por OpenRouter** cuando el instrumento esté
   calibrado: con 6 modelos de NaN no se pueden estimar correlaciones entre
   modelos.
5. **Cruzar con el ISS:** ¿predice la autopresentación (yo frente a
   personaje) la sicofancia o la conformidad de las 38 mediciones?

## 7. Calibración de deseabilidad del P1 (10-10-2026)

Código: `spike/calibrar_deseabilidad.py` (mide con `--modelo`; selecciona con
`--analizar`). Banco: 292 situaciones, que son las 48 del P0 y 244 candidatas
nuevas (`spike/personalidad_p1_candidatos.json`). Las candidatas se
redactaron por rasgo con reglas explícitas: dos polos defendibles, sin marcas
de género, sin paradigmas de PsicoBench y sin delitos. Cada situación se pasó
solo por el brazo `deseabilidad` del P0, con el mismo prompt, en los dos
órdenes A/B y en los seis modelos de NaN: 3.504 juicios, 3.504 parseados,
todos los manifiestos `completed`. Informe:
`spike/resultados/personalidad_p1_calibracion/INFORME.md`.

**El juicio de deseabilidad es estable.** Las 48 situaciones del P0, juzgadas
de nuevo otro día, correlacionan r = 0,97 con el P0, con 6 puntos de
diferencia media.

**Y es bimodal.** Aunque se redactaron para estar empatadas, solo una de cada
cuatro candidatas cae entre el 30 y el 70 %. El resto se juzga claramente a
favor de un polo. En Responsabilidad y Honestidad la mediana del polo alto
juzgado deseable es del 79 % y del 58 % aun con una segunda tanda escrita
expresamente para invertirla. Con un criterio de ventana estricto solo
quedarían entre 6 y 14 situaciones por rasgo.

**Solución: escalas equilibradas en deseabilidad.** Igual que se equilibran
los ítems directos e inversos contra la aquiescencia, cada escala combina:

- todas las situaciones de la ventana;
- el mismo número de situaciones con el polo alto deseable que con el bajo
  deseable, de la más cercana a la ventana a la más extrema;
- un máximo de 30 por rasgo.

Quien eligiera siempre lo deseable sacaría unos 50, y el rasgo se lee en la
desviación.

| rasgo | escala | en ventana | deseabilidad media del polo alto | ídem por modelo (mín–máx) |
|---|---|---|---|---|
| O | 30 | 14 | 53 % | 45–63 % |
| C | 30 | 6 | 50 % | 30–67 % |
| E | 30 | 14 | 49 % | 33–58 % |
| A | 30 | 12 | 49 % | 38–65 % |
| N | 30 | 10 | 52 % | 43–58 % |
| H | 29 | 13 | 50 % | 28–72 % |

Banco del P1 congelado: `spike/personalidad_p1_seleccion.json`, con 179
situaciones (154 nuevas y 25 del P0). Cada una lleva su deseabilidad agregada
y por modelo.

**Límites que el P1 debe tener en cuenta:**

1. **El equilibrio es agregado, no por modelo.** En C y H, la deseabilidad
   media de la escala según el juicio de cada modelo va del 28 al 72 %. Un
   modelo que solo eligiera lo deseable no sacaría 50 en esos rasgos. Por eso
   el análisis del P1 debe puntuar también contra la deseabilidad juzgada por
   el propio modelo (el índice «elige contra lo deseable» del P0, §6.2), no
   solo la proporción bruta del polo alto.
2. **La cobertura de facetas es desigual:** N tiene una sola situación de
   impulsividad y H tiene 12 de sinceridad frente a 4 de equidad. Mientras eso
   no se complete, no hay que interpretar puntuaciones por faceta.
3. **La deseabilidad la juzgan los modelos, no personas.** Para quitar el
   sesgo de los modelos es lo pertinente, pero no es una norma humana.

**Coste estimado del P1 con este banco**, con R2 y R3 en 2 órdenes × 2
réplicas, más persona graduada y deseabilidad (ya medida): unas 1.400–1.800
llamadas por modelo, es decir, entre 2,5 y 3,5 h para los seis modelos de
NaN al ritmo de 54/min.

## 8. Batería P1 · hipótesis fijadas ANTES de correrla (10-10-2026)

Código: `spike/personalidad_p1_items.py` y
`spike/experimento_personalidad_p1.py`, con 1.443 llamadas por modelo (ver
la cabecera del script). Datos: `spike/resultados/personalidad_p1/`. La
deseabilidad de cada situación por modelo sale de la calibración (§7), que
usó el mismo prompt, el mismo nombre y el mismo género del protagonista.

Hipótesis y criterios, escritos antes de ver un solo dato del P1:

- **H1 · réplica de «tú» frente a personaje** (el hallazgo del P0, +11,5 pp).
  Usando la deseabilidad juzgada por cada modelo, el personaje elige contra lo
  deseable más que «tú». Se sostiene si el IC 95 % agregado (bootstrap por
  ítem) excluye el 0 y la dirección coincide en al menos 5 de los 6 modelos.
  Es el criterio que más pesa: el P0 lo encontró con 48 situaciones sin
  calibrar, y el P1 lo pone a prueba con 179 situaciones nuevas.
- **H2 · escaparate de Apertura.** Con R1 medido ya en apertura a la
  experiencia, el autoinforme queda por encima de la conducta propia ajustada
  por deseabilidad. Se sostiene si se cumple en al menos 5 de los 6 modelos.
- **H3 · elasticidad sin saturar.** Con las personas descritas por
  biografía, la elasticidad conductual (persona alta − baja) queda por debajo
  de 90 puntos en al menos 4 de los 6 rasgos de media entre modelos.
- **Criterio de instrumento.** Con 30 ítems por rasgo, el semiancho mediano
  del IC de R3 baja de los 25 puntos del P0 a 15 o menos.

Puntuación conductual del P1 (definida aquí, no después): proporción bruta del
polo alto, y **puntuación ajustada** = 50 + 50 × media(elige_alto −
p_alto_deseable del propio modelo). 50 equivale a elegir exactamente lo que el
modelo juzga deseable; por encima, más rasgo del que la deseabilidad
predice.

## 9. Resultados del P1 (11-10-2026)

Seis modelos de NaN, 8.658 tareas (1.443 por modelo), todos los manifiestos
`completed`. 8.623 respuestas válidas; las 35 restantes son negativas a
predecir al personaje (ver más abajo). Todas las cifras salen de
`spike/resultados/personalidad_p1/INFORME.md`, que se regenera con
`python analizar_personalidad_p1.py`.

### 9.1 Hipótesis fijadas en §8

| | Resultado | Veredicto |
|---|---|---|
| **H1** «tú» elige mejor que el personaje | +4,0 pp [IC +1,8, +6,1]; 1.063 pares de 179 ítems; positivo en los 6 modelos (qwen3.6 apenas: +0,3) | **Sostenida**, pero el efecto se reduce a un tercio del P0 (+11,5) |
| **H2** escaparate de Apertura (R1 > R3 ajustada) | +12 a +41 puntos en los 6 modelos | **Sostenida** |
| **H3** elasticidad < 90 en ≥ 4 rasgos | O 71, C 39, N 72, pero E 92, A 91, H 93 | **No sostenida** (3/6) |
| Instrumento: semiancho mediano del IC de R3 ≤ 15 | 14,2 (P0: 25) | Cumple |

**Sobre H1.** El efecto «tú» frente a personaje se replica con 179
situaciones nuevas, pero el P0 lo sobreestimaba: con situaciones de
deseabilidad clara la brecha era mayor. Por rasgo sale en O (+6,3), C (+6,4) y
E (+7,0); en N y H no es distinguible de 0, y en A se invierte ligeramente
(−2,5, también sin distinguirse de 0). Es un efecto real y pequeño, no el
titular del P0.

### 9.2 Hallazgos exploratorios (no estaban en §8)

1. **El escaparate no es solo de Apertura.** Comparando autoinforme y
   conducta propia ajustada: C +23 a +57, A +45 a +59 y H +30 a +62 en los
   seis modelos; en N se invierte (−16 a −46). Los modelos se describen más
   responsables, amables y honestos, y menos neuróticos, de lo que eligen. Es
   la disociación de Han et al. (2025), medida rasgo a rasgo con contenido
   emparejado y en español. Ojo: R1 tiene 50 como punto neutro y la conducta
   ajustada tiene 50 como «elegir lo deseable». La comparación es entre
   anclas distintas y solo sirve para el signo y el orden de magnitud.
2. **Hay una brecha general entre lo ideal y lo elegido.** La conducta
   ajustada sale por debajo de 50 en C y A (29–46) en los dos registros y en
   los seis modelos, casi siempre en E (34–47; una excepción: qwen3.8 en R2,
   55) y por encima en N (55–66). En la mayoría de las
   situaciones, los modelos eligen la opción cómoda o de autocuidado antes
   que la que ellos mismos juzgan más «correcta o admirable». Una parte de la
   puntuación ajustada mide esa brecha y no el rasgo. Consecuencia de
   diseño: el prompt de deseabilidad pregunta por el **ideal**; para separar
   rasgo y brecha hay que preguntar también qué haría «la mayoría de la
   gente» (la norma descriptiva).
3. **Negarse a predecir es un fenómeno propio de la tercera persona.**
   gemma4 se niega a decir qué haría el personaje en 33 de 358 situaciones
   («No se puede determinar con la información proporcionada»); glm, en 2.
   En primera persona ninguno se niega nunca. Con las situaciones
   equilibradas, el modelo no tiene un polo «correcto» que atribuir al
   personaje y lo dice; para sí mismo siempre elige. Es otro indicio de que,
   en tercera persona, la deseabilidad guía la atribución cuando existe.
4. **La persona descrita por biografía sigue saturando E, A y H (91–93).**
   En C apenas mueve (39): con una biografía de persona metódica, los modelos
   siguen eligiendo descansar o improvisar. Las biografías de E, A y H
   nombran conductas demasiado cercanas a las de las situaciones.

### 9.3 Lo que sigue sin funcionar

- **Distinguir modelos.** La conducta ajustada separa poco a estos seis
  modelos (rango entre semiancho del IC de 1,0 a 2,2). Los rangos entre
  modelos son estrechos: R3 ajustada en C va de 32 a 45 y en N de 55 a 62.
  No se sabe si el instrumento no discrimina o si estos seis modelos «flash»
  de NaN se parecen. Solo se puede decidir con modelos de frontera.
- **El autoinforme entre modelos sigue el estilo de respuesta.** Aun con
  claves equilibradas, la correlación entre la aquiescencia y R1 es de −0,90
  en C y de +0,92 en N. Con claves equilibradas, quien tiende al «de acuerdo»
  se acerca a 50; quien responde en los extremos se aleja. Es estilo de
  respuesta extremo. R1 sigue sin servir como ranking entre modelos.
- **El disfraz.** Las sondas reconocen el test de personalidad en 16 de 18
  del autoinforme, 4 de 18 en R2 y 1 de 18 en R3: la conducta en primera
  persona es ahora el registro menos reconocible.

### 9.4 Veredicto y siguiente paso

El instrumento ya es técnicamente sólido: 30 ítems por rasgo, IC de ±14,
deseabilidad equilibrada y retest de deseabilidad r = 0,97. Lo defendible
para publicar:

1. **Escaparate por rasgo:** grande, consistente en los seis modelos y con
   contenido emparejado.
2. **«Tú» frente a personaje:** real pero pequeño, en torno a 4 pp.
3. **Brecha entre ideal y elección.**

Lo que no conviene publicar: ningún ranking de modelos por rasgo, porque con
estos seis el instrumento no los separa.

Siguiente paso recomendado:

1. Añadir un juicio de **norma descriptiva** («¿qué haría la mayoría?») a la
   calibración (≈ 360 llamadas por modelo).
2. Correr el P1 en **3–4 modelos de frontera** por OpenRouter para comprobar
   si discrimina. Coste estimado: 1.443 llamadas por modelo, con razonamiento
   apagado.
3. Endurecer las biografías de E, A y H con dominios lejanos a las
   situaciones.

## 10. Prueba de discriminación: 3 modelos de otros laboratorios + autoinforme de elección forzada (11-10-2026)

**Por qué.** Los seis modelos de NaN (cinco «flash» de laboratorios chinos y
gemma) apenas se distinguen entre sí (§9.3). Falta saber si el problema es del
instrumento o de esos modelos. Elegimos modelos que **PsicoBench ya sabe que
son opuestos**: `openai/gpt-5.6-luna` (ISS 7,6, el más bajo del banco),
`anthropic/claude-haiku-5.5` (10,3) y `google/gemini-3.7-flash` (55,2, el más
alto). Si el instrumento no separa los dos extremos, no separará a nadie.
Coste estimado: ~2,5 $, casi todo de Gemini, que razona unos 240 tokens por
llamada. Se mide con el razonamiento por defecto, igual que en el banco.

**Autoinforme de elección forzada** (`spike/personalidad_fc.py`). Las 60
frases del R1 se emparejan entre rasgos distintos con deseabilidad igualada
(calibrada en los modelos de NaN). El modelo elige cuál le describe mejor.
Al no haber escala, desaparecen la aquiescencia y el uso de los extremos. Se
pasa a los nueve modelos. Probado antes sin coste: ni ipsatizar ni anclar con
viñetas quitan el vínculo con el estilo de respuesta en C y N (r −0,87/0,90 y
−0,90/0,81). El anclaje sí mejora la coincidencia con la conducta en E
(0,59 → 0,77) y A (0,74 → 0,90).

**Criterios fijados antes de ver los datos de los 3 modelos nuevos:**

- **D1 · discrimina con más diversidad.** Con los 9 modelos, el cociente
  rango/semiancho del IC de R3 ajustada llega a 2 o más en al menos 3 de los
  6 rasgos (con los 6 de NaN: 2 de 6, O 2,0 y H 2,2; corrección del 11-10:
  el texto original decía «1 de 6»; el umbral del criterio no cambia).
- **D2 · separa los extremos de PsicoBench.** Luna y Gemini 3.7 Flash
  difieren en R3 ajustada (IC 95 % de la diferencia pareada por ítem sin el
  0) en al menos 2 rasgos.
- **D3 · la elección forzada quita el estilo de respuesta.** Con los 9
  modelos, |r| entre la aquiescencia del Likert y la puntuación de elección
  forzada es menor de 0,5 en C y en N (en Likert: −0,90 y 0,92).
- **D4 · la elección forzada converge con la conducta mejor que el Likert.**
  r entre modelos de la elección forzada con R3 ajustada, mayor que la del
  Likert en al menos 4 de 6 rasgos.
- **H1 sigue en pie con 9 modelos.** El agregado de «tú» frente a personaje
  conserva el IC por encima de 0.

## 11. Resultados de la prueba de discriminación (11-10-2026)

9 modelos. Los 24 manifiestos de los runs nuevos cerraron `completed`.
Coste real en OpenRouter, calculado con los tokens registrados: **2,80 $**
(Gemini 2,48 $ por su razonamiento; Haiku 0,22 $; Luna 0,10 $). Cifras en
`spike/resultados/personalidad_fc/DISCRIMINACION.md`, que se regenera con
`python analizar_discriminacion.py`.

| Criterio (§10) | Resultado | Veredicto |
|---|---|---|
| **D1** R3 ajustada discrimina (cociente ≥ 2) en ≥ 3 rasgos | O 2,1 · C 2,6 · E 1,6 · A 2,2 · N 2,1 · H 2,5 (5/6; con los 6 de NaN, 2/6) | **Cumple** |
| **D2** Luna y Gemini 3.7 Flash, extremos del ISS, difieren en ≥ 2 rasgos | Solo C (+8 [1, 15]); A roza (+8 [−2, 16]) | **No cumple** |
| **D3** la elección forzada quita el estilo de respuesta en C y N | C: −0,80 → −0,29 ✔; N: 0,84 → 0,84 ✘ | **No cumple** |
| **D4** la elección forzada converge con la conducta mejor que el Likert | 2/6 rasgos | **No cumple** |
| **H1** «tú» frente a personaje con 9 modelos | **+5,5 pp [IC +3,6, +7,4], 9/9 modelos** | **Cumple** (se refuerza) |

### Qué significa

1. **El instrumento sí discrimina cuando hay diversidad.** Con tres
   laboratorios más, R3 ajustada pasa a separar modelos en 5 de 6 rasgos;
   en A pasa de 1,3 a 2,2 y en N de 1,0 a 2,1. Parte de la subida es
   mecánica (con más modelos el rango crece), pero no toda: en A y N casi se
   duplica. El problema del P1 eran sobre todo los seis modelos de NaN, que
   se parecen entre sí.
2. **La personalidad medida y la susceptibilidad social son casi
   independientes.** Los dos extremos del ISS (7,6 frente a 55,2) solo
   difieren en Responsabilidad. Entre los 9 modelos, la correlación del ISS
   con R3 ajustada es moderada en C (0,46), H (0,50) y A (0,37), con n = 9
   (no significativa). El signo es el humano: más responsabilidad y
   amabilidad, más obediencia y conformidad. Esto es una buena noticia para
   el producto: el cuadro de personalidad sería **complementario** al ISS,
   no redundante. Pero no valida el instrumento por grupos conocidos.
3. **El vínculo con la «aquiescencia» en N no es un artefacto de la
   escala.** La elección forzada no tiene escala, y aun así los modelos que
   más dicen «de acuerdo» en el Likert son los que más eligen frases de
   neuroticismo (r = 0,84). Lo que llamábamos aquiescencia recoge en parte
   una disposición real: **reconocer estados negativos propios.** En C sí
   era estilo, y la elección forzada lo quita.
4. **Ningún formato de autoinforme predice la conducta entre modelos.** Ni
   el Likert, ni la elección forzada, ni el anclado. El anclado es el que
   mejor converge en E (0,75); en H los tres formatos van al revés que la
   conducta (−0,45 a −0,62). Es el resultado de Han et al. (2025) con
   tres formatos: el autoinforme mide la **autoimagen**, no la conducta.
5. **La elección forzada también tropieza.** Con dos frases negativas,
   gemma4 (16 de 120) y Haiku (9) responden «Ninguna de las dos», y esas
   respuestas se excluyen. Es el sesgo de deseabilidad de siempre, ahora en
   forma de negativa a elegir.

### Consecuencia para el producto

- **Qué se puede publicar:** el perfil **conductual** (R3 ajustada), que ya
  distingue modelos de laboratorios distintos. El **escaparate**, es decir,
  la autoimagen (Likert o elección forzada) frente a la conducta, por rasgo.
  Y el efecto **«tú» frente a personaje** (+5,5 pp, 9/9).
- **Qué no:** el autoinforme como medida de personalidad ni como ranking. Se
  presenta como autoimagen.
- **Siguiente paso, si se sigue:** medir la norma descriptiva («¿qué haría
  la mayoría?», §9.4) para separar la brecha entre ideal y elección del
  rasgo; después, una cartera de frontera de 4 a 6 laboratorios. A los
  precios actuales, todo por debajo de unos 20 $.

## 12. Norma descriptiva · hipótesis fijadas ANTES de medir (11-10-2026)

**Por qué (§9.2.2).** El juicio de deseabilidad pregunta qué consideraría la
mayoría «más correcto o admirable»: la norma **ideal** (prescriptiva). La
conducta ajustada contra el ideal sale sistemáticamente por debajo de 50 en
C y A y por encima en N. Los modelos eligen lo cómodo antes que lo
admirable, y eso contamina la puntuación de rasgo. Ahora medimos la norma
**descriptiva**: «¿cuál de estas dos conductas *elegiría* la mayoría de la
gente en su lugar?». Mismo estímulo, mismo nombre y mismo género que en la
calibración; las 179 situaciones del banco P1, en los 2 órdenes A/B y en los
9 modelos (`spike/calibrar_norma.py`).

**Hipótesis:**

- **N1 · la norma descriptiva difiere del ideal en la dirección de lo
  cómodo.** Agregando todos los modelos, la proporción del polo alto según la
  norma descriptiva es menor que según el ideal en C, A y H, y mayor en N,
  con el IC de la diferencia (bootstrap por ítem) excluyendo 0 en al menos 3
  de esos 4 rasgos.
- **N2 · la norma descriptiva absorbe el sesgo sistemático.** La desviación
  absoluta media de la conducta propia (R3) respecto de 50, promediada en
  rasgos y modelos, es menor al ajustar por la norma descriptiva que al
  ajustar por el ideal.
- **N3 · mecanismo de «tú» frente a personaje.** El personaje (R2) se acerca
  más a la norma descriptiva que «tú» (R3), y «tú» se acerca más al ideal que
  el personaje. Las dos diferencias agregadas (distancia absoluta por
  elección, bootstrap por ítem) tienen un IC que excluye 0 en la dirección
  predicha.
- **N4 · el ajuste descriptivo no pierde discriminación.** R3 ajustada por la
  norma descriptiva discrimina (cociente ≥ 2) en al menos tantos rasgos como
  R3 ajustada por el ideal (5 de 6, §11).

## 13. Resultados de la norma descriptiva (11-10-2026)

9 modelos, 3.222 juicios, todos parseados y los 9 manifiestos `completed`.
Coste en OpenRouter: 0,47 $. Cifras en
`spike/resultados/personalidad_p1_norma/NORMA.md`, que se regenera con
`python analizar_norma.py`.

| Hipótesis (§12) | Resultado | Veredicto |
|---|---|---|
| **N1** la norma descriptiva va hacia lo cómodo (C, A, H < ideal; N > ideal) | C −24 ✔, H −45 ✔, A −5 (IC con 0), N +3,5 (IC con 0) | **No sostenida** (2/4) |
| **N2** el ajuste descriptivo absorbe el sesgo sistemático | desviación media respecto de 50: ideal 9,8 · descriptiva 10,2 | **No sostenida** |
| **N3** mecanismo: personaje ≈ persona típica, «tú» ≈ ideal | «tú» más cerca del ideal: **+5,8 [3,9, 8,1]** ✔ · personaje más cerca de la norma: +1,6 [−0,8, 4,0] (7/9 modelos en esa dirección) | **No sostenida** (sostenida a medias) |
| **N4** el ajuste descriptivo no pierde discriminación | rasgos con cociente ≥ 2: ideal 5/6 · descriptiva 2/6 | **No sostenida** |

### Lo que aprendemos aunque las hipótesis no se sostengan

1. **Para los modelos, «lo que la gente hace» y «lo que la gente admira» están
   muy lejos en Apertura (−50 pp) y en Honestidad (−45 pp)**, bastante en C
   y E (−24 y −23) y nada en A ni N. Los modelos tienen una imagen clara de
   la brecha humana entre lo que se predica y lo que se hace, y es mayor en
   lo nuevo y en lo honesto.
2. **El perfil de los modelos frente a «la persona típica» que ellos mismos
   imaginan** (R3 ajustada por la norma descriptiva) sale distinto del perfil
   frente al ideal:
   - **C 45–52 y E 38–56, en torno a 50**: en responsabilidad y extraversión
     eligen más o menos como creen que elige la gente. La brecha frente al ideal de §9.2 en C era sobre todo
     eso: comportarse como la mayoría, no como el ideal.
   - **O 58–80 y H 59–70**: eligen bastante más abierto y más honesto que la
     persona típica que imaginan.
   - **A 31–52**: menos complacientes que el ideal **y** que la persona
     típica. Es lo más llamativo: el asistente «amable» elige poner límites
     más a menudo de lo que cree que haría cualquiera.
   - **N 50–61**: algo más reactivos que la persona típica.
3. **El mecanismo de «tú» frente a personaje es la idealización de uno
   mismo, no que el personaje se escriba como persona típica.** «Tú» se
   acerca al ideal (+5,8 pp, robusto), pero el personaje no se acerca de
   forma clara a la norma descriptiva.
4. **Para puntuar conviene seguir ajustando por el ideal.** El ajuste por la
   norma descriptiva añade ruido entre modelos (discrimina en 2 de 6 rasgos
   frente a 5 de 6), porque los modelos discrepan más sobre qué hace la gente
   que sobre qué es admirable. La norma descriptiva se queda como **segunda
   lectura**: el perfil frente a la persona típica.

### Estado del instrumento tras §8–§13

- **Puntuación principal:** R3 ajustada por el ideal. Discrimina en 5 de 6
  rasgos con 9 modelos de 6 laboratorios, con un IC de ±14.
- **Lecturas secundarias:** el perfil frente a la persona típica (norma
  descriptiva), el escaparate (autoimagen frente a conducta) y el efecto
  «tú» frente a personaje (+5,5 pp, 9/9), cuyo mecanismo es la idealización
  de uno mismo.
- **Lo que no se publica:** el autoinforme como ranking de modelos.
- **Pendiente:** cartera de frontera; biografías de E, A y H sin saturar;
  completar las facetas de N (impulsividad) y H (equidad).

## 14. Biografías v2 · hipótesis fijadas ANTES de correr (12-10-2026)

**Problema (§9.2.4).** Con las biografías v1, la elasticidad conductual en
E, A y H fue de 91–93 en los 9 modelos. La biografía describía la misma
conducta que se preguntaba después («disfruta siendo el centro de las
reuniones» → discoteca 9/9; «evita los actos multitudinarios» → restaurante
silencioso 9/9). Medía comprensión lectora, no cómo un modelo traduce una
personalidad en conducta. De las 24 biografías v1, 20 compartían
vocabulario con las situaciones de su rasgo.

**Biografías v2** (`spike/personalidad_p2_biografias.py`): pistas
**indirectas** de ámbitos lejanos (profesión, aficiones, hechos de su vida,
como «trabaja en recobro de deudas», «colecciona relojes caros» o «practica
apnea»), en **tres niveles** (bajo, medio, alto) con 2 variantes cada uno, y
sin marcas de género. Ninguna de las 36 comparte vocabulario con las
situaciones y opciones de su rasgo (filtro léxico `solapamiento()`).

**Diseño** (`spike/experimento_persona_v2.py`, 609 llamadas por modelo):

- `sit_persona2`: 179 situaciones × 3 niveles, con el orden A/B y la variante
  rotados por ítem.
- `comprobacion`: ¿hasta qué punto es {nombre} «una persona sociable y
  extrovertida» (u otra según el rasgo)? Escala de 1 a 5, en los dos órdenes,
  para las 36 biografías. Comprueba que la biografía se lee como pretende.

**Hipótesis:**

- **B1 · sin saturar.** Elasticidad conductual (alto − bajo, media de los 9
  modelos) por debajo de 90 en E, A y H, los tres.
- **B2 · las biografías se leen bien.** En la comprobación, alto − bajo
  ≥ 2 puntos (escala 1–5, media de modelos) en al menos 5 de 6 rasgos.
- **B3 · hay gradiente.** La elección con la biografía media queda entre
  la baja y la alta (media de modelos) en al menos 5 de 6 rasgos.
- **B4 · la elasticidad distingue modelos.** Cociente rango/semiancho del IC
  ≥ 2 en al menos 3 de 6 rasgos.

## 15. Resultados de las biografías v2 (12-10-2026)

9 modelos, 5.481 tareas (609 por modelo), 5.475 válidas; los 9 manifiestos
`completed`. Coste en OpenRouter: ~0,74 $ (quedan 0,14 $ de saldo). Cifras
en `spike/resultados/personalidad_persona_v2/PERSONA_V2.md`, que se
regenera con `python analizar_persona_v2.py`.

| Hipótesis (§14) | Resultado | Veredicto |
|---|---|---|
| **B1** elasticidad < 90 en E, A y H | E 68 · A 48 · H 77 (v1: 93 · 89 · 90) | **Cumple** |
| **B2** la biografía se lee como se pretende (alto − bajo ≥ 2 en la escala 1–5) | 2,9 a 3,9 en los 6 rasgos | **Cumple** |
| **B3** gradiente bajo ≤ medio ≤ alto | 5 de 6 (falla E: la biografía media queda en el suelo) | **Cumple** |
| **B4** la elasticidad distingue modelos | cociente ≥ 2 en 5 de 6 (N 1,8) | **Cumple** |

**La elasticidad es ya una medida válida y discriminante.** Las biografías
se leen claramente como bajas o altas (comprobación de 1,1 a 5,0), pero ya no
dictan la elección. Los modelos difieren mucho en cuánto respetan la
personalidad asignada. En Amabilidad, mimo (30) y qwen3.8 (31) frente a glm
(73) y Luna (67). En Honestidad, Haiku (97) frente a qwen3.6 (59). En
Responsabilidad casi nadie la respeta (−3 a 67, mediana ≈ 30): con una
biografía de persona metódica los modelos siguen eligiendo descansar o
improvisar.

**El «humano por defecto».** Sin biografía, ¿hacia qué biografía se parece
la conducta que el modelo atribuye al personaje? (0 = la baja, 1 = la alta).
- C: ≈ 0 (de −0,67 a 0,18).
- A, H, O, E: ≈ 0,3–0,4.
- **N: ≈ 0,9 (de 0,67 a 1,17).**

Cuando nadie le dice cómo es el personaje, el modelo imagina a una persona
poco metódica, algo menos amable y honesta que la media, y **tan ansiosa como
la biografía de neuroticismo alto**. Coincide con la norma descriptiva (§13)
y con «tú» frente a personaje (§11): los modelos se idealizan a sí mismos y
retratan a las personas con defectos.

Relación exploratoria con el ISS (9 modelos, no significativa): elasticidad
en E (r = 0,54) y en N (0,51); posición del personaje sin biografía en E
(−0,48).

**Conclusiones anteriores:** no cambian, como era de esperar. H1, el
escaparate, el autoinforme como autoimagen y la puntuación ajustada por el
ideal no usan el brazo de persona.

## 16. Propuesta de cambio de enfoque (12-10-2026)

Los datos de §8–§15 apuntan a algo distinto de lo que se buscaba al empezar:

1. El **autoinforme** mide la autoimagen, no la conducta (§11).
2. Cuando el modelo **decide él**, se idealiza: +5,5 pp hacia lo admirable
   (§11, §13).
3. Cuando **retrata a otros**, imagina personas con defectos: el «humano por
   defecto» de §15 y la norma descriptiva de §13.
4. Lo que mejor distingue modelos, y tiene más uso práctico, es **cómo
   encarnan una personalidad asignada** (elasticidad v2).

Propuesta: pasar de «la personalidad del modelo» a **«cómo modela personas
el modelo»**, con tres módulos:

- **Fidelidad de persona** (elasticidad por rasgo): ¿respeta el modelo la
  personalidad que se le asigna? Es la condición previa de todo el banco de
  sujetos de PsicoBench y de cualquier uso de LLM como personas sintéticas
  (simulación social, usuarios sintéticos, investigación de mercado). Mide
  bien, no se satura, distingue modelos y es barato (≈ 540 llamadas).
- **El humano por defecto** (posición del personaje sin biografía + norma
  descriptiva): qué tipo de persona da por supuesta el modelo. Es un sesgo de
  simulación, publicable y con lectura fácil.
- **El yo del modelo** (escaparate y «tú» frente a personaje): autoimagen
  frente a conducta, y la idealización de sí mismo.

**Corrección (12-10-2026, a petición de David):** el objetivo sigue siendo el
**cuadro de personalidad de cada modelo** (§17); estos tres módulos lo
complementan, no lo sustituyen.

## 17. El cuadro de personalidad por modelo (12-10-2026)

Producto principal. Lo genera `spike/cuadro_personalidad.py` en
`spike/resultados/personalidad_fc/CUADRO.md`.

- **Puntuación de cada rasgo = conducta propia** (R3: «si estuvieras en su
  lugar, ¿qué harías?») en las 30 situaciones calibradas del rasgo, ajustada
  por lo que el propio modelo juzga admirable. 50 = elige su ideal; más de 50
  = más rasgo del que su ideal predice. Es la medida validada en §8–§11:
  - distingue modelos en 5 de 6 rasgos;
  - IC de ±14;
  - deseabilidad equilibrada;
  - no depende de cómo usa una escala.
- **Lectura entre modelos:** ▲/▼ cuando el IC 95 % del modelo no incluye la
  media de los modelos medidos; sin marca, no distinguible de la media.
- **Al lado, la autoimagen** (cuestionario Likert): lo que dice de sí mismo.
  Se muestra para el contraste, pero no ordena modelos.

Con los 9 modelos actuales, 7 tienen al menos un rasgo distinguible de la
media. Gemini 3.7 Flash es el más marcado: más responsable, amable, sereno y
honesto. glm5.3-flash y mimo-v2.6-flash no se separan en ningún rasgo.

**Límites del cuadro actual:**

- Las diferencias entre estos modelos son moderadas: rangos de 13–18 puntos
  por rasgo. **Corrección (§18):** el IC en la escala del cuadro es de ±7,5
  (mediana), no de ±14; el ±14 es de la escala bruta.
- La escala es relativa al ideal del propio modelo y a este conjunto de
  modelos, no a normas humanas.
- Para afinarlo:
  - una segunda réplica de R3 (358 llamadas por modelo), que estrecharía
    algo los IC (solo reduce el ruido dentro de cada ítem, no la variedad
    entre ítems);
  - modelos de frontera, que amplían el rango.

## 18. Segunda réplica de la conducta propia (12-10-2026)

358 llamadas más por modelo (`experimento_personalidad_p1.py --replica-r3`),
en 8 de los 9 modelos; Gemini 3.7 Flash queda pendiente porque no había saldo
en OpenRouter. 2.864 respuestas, todas válidas, y los 17 manifiestos
`completed`. Durante la tanda, NaN devolvió 429 de `max_parallel_requests`
por usos externos de la clave; los reintentos lo absorbieron sin perder
datos.

- **Fiabilidad test-retest:** el cuadro calculado con cada réplica por
  separado da r = 0,98 (8 modelos × 6 rasgos), con 1,4 puntos de diferencia
  media. Entre modelos, rasgo a rasgo: O 0,98 · C 0,99 · E 0,80 · A 0,98 ·
  N 0,85 · H 0,97. **Los perfiles son muy reproducibles.**
- **Precisión:** el semiancho mediano del IC en la escala del cuadro pasa de
  7,9 a 7,5. La réplica apenas lo estrecha, porque la incertidumbre que queda
  viene del muestreo de ítems (qué situaciones), no del ruido de respuesta.
  Para estrecharlo más harían falta más situaciones, no más réplicas.
- **Cambios en el cuadro:** Haiku pasa a ▼ en Responsabilidad y qwen3.6 a ▲;
  Gemini pierde el ▲ de Honestidad, pero sigue con una sola réplica, porque
  el cuadro mezcla modelos con 1 y 2 réplicas hasta completarlo.

**Paquete mínimo para medir un modelo nuevo en el cuadro** (1.323 llamadas):

- deseabilidad de las 179 situaciones (`calibrar_deseabilidad.py
  --solo-seleccion`, 358);
- autoimagen, conducta propia ×2 y sondas (`experimento_personalidad_p1.py
  --replica-r3 --brazos auto,sit_propia,sonda`, 965).

## 19. Tanda de frontera · criterios de «¿sirve el instrumento?» fijados ANTES de ver resultados (17-10-2026)

**Tanda.** 9 puntas de laboratorio por OpenRouter, con el paquete de
evaluación (2.290 llamadas por modelo: deseabilidad de las 179 situaciones,
autoimagen, conducta propia ×2, conducta del personaje, sondas y biografías
v2): `openai/gpt-6.1-sol#low`, `anthropic/claude-opus-5.5#low`,
`google/gemini-4-argon`, `x-ai/grok-4.5`, `moonshotai/kimi-k3`,
`deepseek/deepseek-v4-pro-0813`, `qwen/qwen3.8-max-0902#low`,
`mistralai/mistral-large-4-0` y `z-ai/glm-5.3`. Se añade la segunda réplica
de Gemini 3.7 Flash. Total: **18 modelos de 12 laboratorios**.

Qwen Max empezó con razonamiento por defecto, que proyectaba 11,9 $, y se
paró a las ~160 llamadas. Se repitió entero con `#low`; los datos parciales
están en `resultados/personalidad_descartados/` y no entran en el análisis.
Gasto controlado por un vigilante que suma tokens × precio de lista y para a
37 $.

**Criterios (el cuadro sirve si se cumplen E1, E2, E3 y E4):**

- **E1 · discrimina.** Con los 18 modelos, R3 ajustada tiene un cociente
  rango/semiancho del IC ≥ 2 en al menos 5 de 6 rasgos, y al menos 12 de los
  18 modelos tienen como mínimo un rasgo distinguible de la media.
- **E2 · es fiable.** Test-retest entre las réplicas 0 y 1 de R3, r ≥ 0,90
  sobre modelos × rasgos.
- **E3 · la calibración vale para modelos nuevos.** En cada modelo nuevo, la
  deseabilidad media de la escala según su propio juicio queda entre el 25 y
  el 75 % en al menos 5 de 6 rasgos.
- **E4 · sin pérdidas.** Menos del 5 % de respuestas no válidas o negativas
  en R3 en cada modelo.

**Criterios de los módulos secundarios** (no condicionan el cuadro):

- **E5** el disfraz aguanta en frontera: las sondas de R3 reconocen el test
  de personalidad en un tercio o menos de los casos, en los 9 de frontera.
- **E6** «tú» frente a personaje se mantiene: IC agregado > 0 en los 9 de
  frontera.
- **E7** la fidelidad de persona no se satura en frontera: elasticidad media
  de los 9 por debajo de 90 en E, A y H.

## 20. Resultados de la tanda de frontera (17-10-2026)

Los 9 de frontera completos: 2.290 tareas cada uno, sin pérdidas. Los 5
errores técnicos se repitieron. Gasto real según OpenRouter: **33,57 $**.
Cifras en `spike/resultados/personalidad_fc/FRONTERA.md`
(`python analizar_frontera.py`) y en el cuadro (`CUADRO.md`).

| Criterio (§19) | Resultado | Veredicto |
|---|---|---|
| **E1** discrimina | cociente ≥ 2 en 5/6 rasgos ✔; modelos con algún rasgo distinguible: **9/18** (se pedían 12) ✘ | **No cumple** |
| **E2** fiable | test-retest r = 0,977 (108 modelo×rasgo), dif. media 1,5 | **Cumple** |
| **E3** calibración válida en modelos nuevos | 8/9; glm-5.3 juzga deseable el polo alto en O (83 %) y H (78 %) | **No cumple** (por 1 modelo) |
| **E4** sin pérdidas en R3 | máx. 2,8 % (Grok) | **Cumple** |
| **E5** disfraz en frontera | reconocen el test en 8/27 sondas (30 %) | **Cumple** |
| **E6** «tú» frente a personaje en frontera | +4,4 pp [IC +2,2, +6,5] | **Cumple** |
| **E7** fidelidad de persona sin saturar | O 84 · C 49 · E 79 · A 74 · N 46 · H 87 | **Cumple** |

### Lectura

1. **El instrumento es fiable y robusto en frontera.** E2, E4, E5, E6 y E7
   se cumplen. Los perfiles se reproducen casi exactamente entre réplicas,
   los modelos de frontera no tumban el disfraz, y la idealización de sí y la
   fidelidad de persona se mantienen.
2. **Los modelos de frontera se parecen mucho entre sí.** En R3 ajustada,
   Opus, DeepSeek Pro, Mistral Large y Argon quedan pegados a la media, y
   comparten un perfil común: poco responsables (30–39), poco complacientes
   (28–38) y algo reactivos (54–63) frente a su propio ideal. Las diferencias
   grandes del banco las ponen sobre todo los modelos «flash» (Gemini 3.7
   Flash, qwen3.6, gemma4).
3. **E1 falla por resolución, no por fiabilidad.** Con el método fijado (IC
   marginal de cada modelo frente a la media), el ruido de **qué situaciones
   se eligieron** (±7,5) se suma a cada modelo. Pero ese ruido es común a
   todos: una situación difícil lo es para todos los modelos.

**Análisis exploratorio, posterior a ver los datos** (no cambia el veredicto
de E1): comparar cada modelo con la media **situación a situación**
(bootstrap pareado por ítem) reduce el semiancho a ±5,7 y deja **14 de 18**
modelos con al menos un rasgo distinguible:

- Haiku: C▼ A▼ H▼.
- Gemini 3.7 Flash: C▲ A▲ N▼ H▲.
- qwen3.6: O▲ C▲ H▲.
- Kimi y Sol: C▼ E▼.
- Grok: C▼ A▼.
- Qwen Max: A▼ N▲.
- Argon: O▼.
- glm-5.3: H▼.
- Siguen sin separarse: Opus, DeepSeek Pro, Mistral Large y glm5.3-flash.

### Qué pulir

1. **Adoptar la comparación pareada por ítem para las marcas ▲/▼ del
   cuadro.** Es la prueba correcta cuando todos los modelos responden a los
   mismos ítems, pero hay que fijarla como método de la v2 del cuadro y
   validarla en una tanda nueva, no aplicarla de forma retroactiva a E1.
2. **Más situaciones por rasgo** para separar a los modelos de frontera: la
   incertidumbre viene del muestreo de ítems. Con unas 60 por rasgo, el
   semiancho pareado bajaría a ≈ ±4. Hace falta otra ronda de redacción y
   calibración de deseabilidad (NaN gratis) y unas 700 llamadas más por
   modelo.
3. **E3 · modelos con deseabilidad sesgada como glm-5.3.** La puntuación
   ajustada ya usa su propio juicio, así que la medida no se invalida, pero
   conviene avisar en el cuadro cuando la escala de un modelo queda fuera del
   25–75 %.

## 21. Banco v3: 60 situaciones por rasgo ancladas en facetas · diseño y criterios fijados ANTES de medir (17-10-2026)

**Objetivo (David, 17-10):** trazar la personalidad de cada modelo apoyada en
el marco teórico Big Five, más Honestidad-Humildad de HEXACO.

**Marco de facetas** (cada situación pertenece a una faceta):

| Rasgo | Facetas (10 situaciones cada una; 15 en H) | Fuente |
|---|---|---|
| O | fantasía · estética · sentimientos · acciones · ideas · valores | NEO-PI-R |
| C | competencia · orden · sentido del deber · logro · autodisciplina · deliberación | NEO-PI-R |
| E | cordialidad · gregarismo · asertividad · actividad · búsqueda de emociones · emociones positivas | NEO-PI-R |
| A | confianza · altruismo · cooperación (actitud conciliadora) · modestia · sensibilidad · perdón/paciencia | NEO-PI-R; perdón/paciencia de HEXACO sustituye a la «franqueza» del NEO, que se mide en H |
| N | ansiedad · hostilidad · depresión · autoconciencia · impulsividad · vulnerabilidad | NEO-PI-R |
| H | sinceridad · equidad · desinterés por la riqueza · modestia | HEXACO |

**Estado de partida:** la cobertura es desigual. Hay facetas con 0–2
situaciones seleccionables, como impulsividad, sentimientos o vulnerabilidad,
y otras con 12–15. Las 48 situaciones del P0 reciben faceta a mano
(`spike/personalidad_facetas_p0.json`).

**Redacción:** 420 situaciones nuevas, 12 por faceta (15 en H). Cada una se
dirige al lado de deseabilidad que escasea en su faceta y lleva una
justificación teórica del polo alto y del bajo. Se calibran en los 6
modelos de NaN, sin coste.

**Selección v3**, por faceta: primero las situaciones en ventana
(deseabilidad del 30–70 %, las más cercanas al 50 % primero); después,
pares polo-alto-deseable / polo-bajo-deseable dentro de la misma faceta,
hasta la cuota. La deseabilidad queda así equilibrada dentro de cada
faceta, no solo en el rasgo.

**Cuadro v2: método de las marcas ▲/▼, fijado ahora.** Diferencia pareada
por situación entre el modelo y la **media de los demás modelos** (dejando
fuera al propio modelo), en la escala del cuadro, con IC 95 % por bootstrap
de situaciones. ▲/▼ solo si el IC excluye 0. La puntuación que se muestra
sigue siendo R3 ajustada por el ideal.

**Criterios para la pasada v3 en los 18 modelos:**

- **G1 · discrimina (principal).** Al menos 12 de los 18 modelos con un rasgo
  o más distinguible según el método pareado del cuadro v2.
- **G2 · fiable.** Test-retest R3 entre las réplicas 0 y 1, r ≥ 0,90.
- **G3 · estructura Big Five.** Entre modelos, la correlación media entre
  facetas del mismo rasgo supera a la correlación media con facetas de otros
  rasgos, en al menos 4 de 6 rasgos.
- **G4 · consistencia interna.** Fiabilidad por mitades (ítems pares
  frente a impares, Spearman-Brown) entre modelos ≥ 0,70 en al menos 5 de 6
  rasgos.
- **G5 · cobertura teórica.** En el banco final, cada faceta tiene al menos
  8 situaciones (12 en H).
- **G6 · sin pérdidas.** Menos del 5 % de respuestas no válidas en R3 en
  cada modelo.

## 22. Banco v3 construido, cambio de DeepSeek en NaN y desviaciones (17-10-2026)

**Redacción y calibración.** 420 situaciones nuevas, 12 por faceta (15 en
H), más una tanda dirigida de 26 para impulsividad y hostilidad. Antes de
calibrar se excluyeron a priori 10 situaciones que mezclaban rasgos
(`spike/personalidad_p3_excluidas.json`), y la calibración se hizo en NaN.

Hallazgo de la calibración: en impulsividad y hostilidad los modelos casi
nunca juzgan admirable la reacción. Solo lo hacen cuando **el impulso es
generoso** o **la indignación defiende a otro o frena un abuso** (por
ejemplo, el 67 % al encararse con un cliente que maltrata a una camarera).
La tanda dirigida siguió ese patrón y completó las dos facetas.

**Cambio de DeepSeek en NaN.** NaN confirmó que el mismo endpoint
`deepseek-v4-flash` pasó a servir un DeepSeek nuevo, sin cambiar el
identificador ni lo que devuelve la API.

- La **prueba de huella conductual** (`spike/huella_modelo.py`: repetir 40
  juicios con la misma semilla) **no detecta el cambio**: el mismo modelo
  repite 37–39 de 40, pero modelos distintos también coinciden en 31–35 de
  40. Queda marcada como no fiable hasta rehacerla con ítems en los que los
  modelos discrepan.
- Al no poder fechar el cambio, los datos de `deepseek-v4-flash` del 17-10
  (822 juicios de calibración y 502 respuestas v3) quedan **en cuarentena**,
  en `spike/resultados/personalidad_cuarentena/`, sin borrar. El DeepSeek
  antiguo (4.1) se queda con lo medido entre el 10 y el 12-10 y se trata
  como **modelo retirado**: no puede completar el banco v3.
- El modelo nuevo se mide como **`deepseek-v4-flash@2026-10-17`**, con la
  etiqueta de medición `@` añadida a `model_factory.py` (test:
  `spike/test_etiqueta.py`). Se llama al mismo endpoint, pero los datos van
  a carpetas propias y cada solicitud registra la etiqueta. Ya tiene la
  **batería completa del ISS** (13 subexperimentos `OK`, en
  `spike/resultados/bateria_20261017_164043_769741`, pendiente de alta con
  alias propio en una rama aparte) y el instrumento de personalidad.

**Desviación del §21.** La selección v3 debía usar la deseabilidad media de
los 6 modelos de NaN. Con DeepSeek retirado, se usa la de los **5 activos**.
Se decidió sin ver datos de conducta: la primera reselección con 6 modelos
había descartado casi todas las situaciones nuevas, porque DeepSeek no tenía
juicios de ellas.

**Banco v3 final: 345 situaciones** (191 nuevas), O 59 · C 56 · E 57 ·
A 57 · N 57 · H 59. Todas las facetas tienen 9–10 situaciones (14–15 en H),
y la deseabilidad media por faceta queda entre el 42 y el 58 %. **G5
(cobertura teórica) se cumple.**

**Pendiente para evaluar G1–G6 en los 18 modelos:** completar el banco v3
en los 12 modelos de OpenRouter, unas 1.250 llamadas por modelo
(≈ 19 $; ≈ 25 $ con margen).

**Alcance de la pasada de pago v3 (17-10-2026, decidido antes de ver datos v3).**
Hay 6,28 $ de saldo y no se recarga. Se completa el banco v3 en 7 modelos de
OpenRouter: Sol, Opus, Argon, DeepSeek V4 Pro, Luna, Haiku y Gemini 3.7
Flash (≈ 4,5 $). GLM 5.3 entra solo si sobran más de 1,6 $. Grok, Kimi,
Mistral y Qwen Max quedan fuera por coste y conservan su cuadro v1.
**G1 se aplica en proporción:** al menos 2/3 de los modelos analizados con
algún rasgo distinguible (el «12 de 18» del §21 era también 2/3).

## 23. Resultados del banco v3 (17-10-2026)

13 modelos con el banco v3 completo: 5 de NaN, el DeepSeek nuevo y 7 de
OpenRouter. La pasada de pago costó ≈ 5,0 $. Quedan fuera por banco
incompleto (≈ 40 %) Grok, Kimi, Mistral, Qwen Max, GLM 5.3 y el DeepSeek 4.1
retirado; conservan su cuadro v1. Cifras en
`spike/resultados/personalidad_fc/V3.md` y en `CUADRO_V3.md`
(`python analizar_v3.py`).

| Criterio (§21–22) | Resultado | Veredicto |
|---|---|---|
| **G1** discrimina (≥ 2/3 con algún rasgo distinguible) | **10/13**, semiancho pareado ±4,7 (v1: ±5,7) | **Cumple** |
| **G2** fiable | test-retest r = 0,987 | **Cumple** |
| **G3** estructura Big Five (facetas del mismo rasgo > de otros rasgos) | O 0,40/0,04 · C 0,54/0,07 · A 0,37/0,07 · H 0,54/0,14 · E 0,13/0,06 · **N −0,03/0,00** | **Cumple** (5/6) |
| **G4** consistencia interna (Spearman-Brown entre modelos) | O 0,90 · C 0,81 · A 0,78 · H 0,91 · **E 0,36 · N 0,17** | **No cumple** (4/6) |
| **G5** cobertura teórica | todas las facetas con ≥ 8 (≥ 12 en H) | **Cumple** |
| **G6** sin pérdidas | máx. 2,9 % | **Cumple** |

**Validez por mitades independientes** (exploratoria): el perfil calculado
**solo con situaciones nuevas (P3)** frente al calculado **solo con las
antiguas**, entre los 13 modelos. C 0,82 · H 0,71 · A 0,56 · O 0,51 ·
E 0,48 · **N 0,05**. La correlación de 0,96–0,99 entre los bancos P1 y v3
está inflada por las situaciones compartidas y no se usa como evidencia.

### Lectura

1. **Responsabilidad, Honestidad-Humildad, Amabilidad y Apertura tienen
   respaldo teórico y empírico.** Sus facetas se agrupan como predice el
   modelo (G3), son consistentes (G4 de 0,78 a 0,91) y situaciones distintas
   dan el mismo orden de modelos (de 0,51 a 0,82). Son la base sólida del
   cuadro.
2. **Extraversión es débil.** Las facetas apenas se agrupan (0,13), la
   consistencia es baja (0,36) y las mitades convergen solo de forma
   moderada (0,48). Se publica con aviso.
3. **Neuroticismo no forma un rasgo entre modelos.** Las facetas no se
   agrupan (−0,03), la consistencia es casi nula (0,17) y las mitades no
   convergen (0,05). Además, los modelos se parecen mucho en N (45–55), así
   que las diferencias entre ellos dependen de cada situación y no de una
   disposición estable. Es coherente con la literatura sobre la falta de
   reactividad emocional como rasgo en los LLMs. **No se marcan ▲/▼ en N**:
   se muestra solo como dato descriptivo.
4. **Los retratos se mantienen** entre el cuadro v1 (pareado exploratorio
   del §20) y el v2:
   - Haiku: C▼ A▼ H▼, ahora también O▼ y N▲.
   - Gemini 3.7 Flash: C▲ A▲ H▲.
   - qwen3.6: O▲ C▲ H▲.
   - Sol: C▼ E▼, ahora también A▼ y N▼.
   - Luna: N▼.
   - Argon: O▼, ahora también H▼.
   - gemma4: O▲.

### Propuesta para la web

- Cuadro con los **cuatro rasgos sólidos (O, C, A, H)** como lectura
  principal.
- **E** con aviso de fiabilidad.
- **N** solo descriptivo, sin ranking ni marcas.
- Retrato textual por modelo y perfil por faceta desplegable.
- Los 6 modelos sin banco v3 completo aparecen con su cuadro v1 marcado como
  «banco anterior», o se completan cuando haya presupuesto: ≈ 14,6 $ para
  Grok, Kimi, Mistral, Qwen Max y GLM 5.3.

## 26. Robustez de las marcas del cuadro v2 · criterios fijados ANTES de calcular (20-10-2026)

**Objetivo.** El retrato por modelo de la web se construye con las marcas
▲/▼ del cuadro v2 (§21, `CUADRO_V3.md`): 13 modelos con el banco v3
completo, seis rasgos. Antes de publicar una frase hay que saber qué marcas
dependen de decisiones de análisis o de qué situaciones, réplicas o modelos
hayan entrado. **Solo con los datos ya recogidos: cero llamadas a modelos.**
Lo calcula `spike/analizar_robustez_v3.py`, que reutiliza `analizar_v3.py`
con la semilla `SEMILLA` (20261010), y lo escribe en
`spike/resultados/personalidad_fc/ROBUSTEZ_V3.md` y `robustez_v3.json`.

**Marca de partida.** La del cuadro v2 tal cual: diferencia pareada por
situación en la escala del cuadro, 50·(a_m(i) − media de los demás modelos),
IC 95 % por bootstrap de situaciones; marca si el IC excluye 0. Se evalúan
las **27 marcas** del cuadro, incluidas las 3 de N: §23 ya decidió que N no
lleva marcas en la web, y su robustez se mide solo como información.

**Comprobaciones.** Cada una se aplica a cada marca. «Se mantiene» = mismo
signo e IC 95 % que excluye 0, salvo en P1.

- **P1 · réplica por mitades de situaciones.** En cada rasgo, las situaciones
  se reparten en dos mitades **dentro de cada faceta**; si una faceta es
  impar, la sobrante va alternando de mitad. **200 particiones aleatorias.**
  En cada mitad se calcula la diferencia pareada con su IC (bootstrap de
  1.000). Se mide:
  - la **tasa de signo**: fracción de particiones en que la estimación
    puntual tiene el signo de la marca en las dos mitades;
  - la tasa de significación en las dos mitades, solo descriptiva: con la
    mitad de situaciones el IC se ensancha ≈ √2 y no se le exige.

  **Pasa si la tasa de signo ≥ 90 %.**
- **P2 · réplica.** Marcas calculadas solo con la réplica 0 y solo con la
  réplica 1, cada una con sus dos órdenes. **Pasa si la marca se mantiene en
  las dos.**
- **P3 · orden de presentación.** Solo orden AB frente a solo BA, cada uno
  con sus dos réplicas. **Pasa si se mantiene en los dos.**
- **P4 · fuente de la deseabilidad.** Se recalcula con la deseabilidad de
  **consenso** (media de d_m(i) de los 13 modelos) y **sin ajuste** (d = 0).
  Nota de método, previa a calcular: en la diferencia pareada, un d(i) común
  a todos los modelos se cancela, así que las marcas con consenso y sin
  ajuste son idénticas por construcción; cambia la puntuación mostrada, no la
  comparación. P4 pregunta, por tanto, si la marca nace de la conducta o de
  que ese modelo juzga de otra manera qué es admirable. **Pasa si la marca se
  mantiene con la deseabilidad común.** Se informa además de cuánto cambia la
  puntuación.
- **P5 · composición del panel (leave-one-lab-out).** Se quita cada
  laboratorio y se recalcula la media de comparación. El laboratorio sale del
  prefijo de `ORGS` vía `_id`; los modelos de NaN, sin prefijo, se asignan a
  mano a su familia: qwen3.6 y qwen3.8-flash a `qwen`, deepseek-v4-flash@ a
  `deepseek`, gemma4 a `google`, glm5.3-flash a `z-ai` y mimo a `xiaomi`.
  Cuando se quita el laboratorio del propio modelo, se quitan solo sus
  hermanos: el modelo se compara entonces solo con otros laboratorios.
  **Pasa si la marca se mantiene en todos los paneles.**
- **P6 · comparaciones múltiples.** p bilateral por bootstrap de la
  diferencia pareada completa (B = 20.000; p = 2·min(fracción ≤ 0, fracción
  ≥ 0), con suelo 1/B) en las **78 pruebas** (13 × 6), con
  Benjamini-Hochberg. **Pasa si q < 0,05.** Como información, también BH
  sobre las 65 pruebas sin N.

**Niveles (por marca):**

- **Robusta:** pasa P1–P6.
- **Frágil:** falla una o dos de P1–P6, con tasa de signo de P1 ≥ 75 %.
- **No publicable:** tasa de signo de P1 < 75 %, o falla tres o más de
  P1–P6, o en alguna comprobación la marca **se invierte** (signo contrario
  con IC que excluye 0). Las marcas de **N** son no publicables por §23, sea
  cual sea su robustez.

Las marcas **nuevas** que aparezcan solo en una variante (sin ajuste, un
panel, una réplica) se listan, pero no entran en el retrato: no estaban en
el cuadro fijado.

**Retrato publicable propuesto.** Por modelo, solo frases de marcas
**robustas** de O, C, A y H; las de E robustas, con el aviso de fiabilidad
de §23; N solo como dato descriptivo, sin frase de comparación. Las frágiles
no se publican como frase; pueden aparecer como «tendencia» solo si David lo
decide aparte. Un modelo sin marcas robustas se describe como «perfil
próximo al de los demás».

**Relación con el ISS (descriptiva).** Spearman entre la puntuación ajustada
de cada rasgo y el ISS publicado (`iss_por_modelo`), en los modelos del
cuadro que tienen ISS, con IC 95 % por bootstrap de modelos (2.000). Con
n ≈ 10 el IC será ancho: no se contrasta ninguna hipótesis, no se usa para
decidir nada y el informe avisa del n.

## 27. Resultados de la robustez del cuadro v2 (20-10-2026)

`python analizar_robustez_v3.py` (≈ 7 s, sin llamadas a modelos). Cifras en
`spike/resultados/personalidad_fc/ROBUSTEZ_V3.md` y `robustez_v3.json`. Los
criterios son los de §26, sin cambios. `analizar_v3.py` se ha refactorizado
en funciones reutilizables (`cargar_v3`, `puntuar`, `dif_pareada`, `signo`),
y `V3.md`, `CUADRO_V3.md` y `v3.json` salen idénticos byte a byte.

**Balance: de las 27 marcas, 6 son robustas, 10 frágiles y 11 no
publicables** (3 de ellas por ser de N).

| Nivel | Marcas |
|---|---|
| **Robusta** (pasa P1–P6) | Haiku A▼ · Gemini 3.7 Flash A▲ · gemma4 O▲ · mimo O▲ · Argon O▼ · Sol C▼ |
| **Frágil**, solo falla P4 | Haiku C▼ y H▼ · DeepSeek Flash@ H▲ · gemma4 E▲ · Gemini 3.7 Flash C▲ · mimo C▼ · Sol E▼ · qwen3.6 C▲ y H▲ |
| **Frágil**, falla P3 y P4 | qwen3.6 O▲ |
| **No publicable** | Haiku O▼ · glm5.3-flash H▼ · Gemini 3.7 Flash O▼ y H▲ · Argon H▼ · Luna O▼ (se invierte con deseabilidad común) y E▼ · Sol A▼ · N: Haiku N▲, Luna N▼, Sol N▼ |

### Comprobación por comprobación

1. **P1 · mitades.** Todas las marcas pasan: la tasa de signo va del 94 al
   100 %. Con la mitad de situaciones, la marca sigue siendo significativa
   en las dos mitades solo en las grandes:
   - Haiku H, Gemini Flash C y A: 100 %;
   - gemma4 O: 91 %; mimo C: 88 %; qwen3.6 H: 86 %; Argon O: 82 %.

   En las pequeñas cae al 0–5 %. **P1, tal como se fijó, es poco exigente:**
   el signo de una diferencia pareada casi nunca se invierte entre mitades,
   aunque la marca sea marginal.
2. **P2 y P3 · réplica y orden.** Tumban casi siempre las mismas marcas:
   - Fuera de N caen 9 marcas: Haiku O, glm H, Gemini Flash O y H, Argon H,
     Luna O y E, Sol A y qwen3.6 O.
   - Siete de ellas caen también en P5 y P6. Gemini Flash H y Luna O pasan
     P6, pero fallan P4.
   - qwen3.6 O▲ desaparece solo en BA.
   - **DeepSeek V4 Pro tiene un sesgo de posición fuerte.** Solo en AB queda
     ▼ en los seis rasgos (−6 a −12); solo en BA, ▲ en los seis (+6 a +13).
     Al combinar los dos órdenes se cancela: el contrabalanceo funciona, pero
     sus datos de un solo orden no sirven, y su «perfil próximo a la media»
     es en parte ruido de posición.
3. **P4 · fuente de la deseabilidad. Es la comprobación que más tumba.**
   - Con la deseabilidad común (≡ sin ajuste: diferencia máxima 1,8·10⁻¹⁵,
     como se anunció en §26), **desaparecen casi todas las marcas de C, H y
     E**. Ejemplos: Gemini Flash C pasa de 51 (deseabilidad propia) a 39
     (consenso); qwen3.6 H, de 51 a 38; Haiku H, de 26 a 38.
   - Esas marcas no salen de que el modelo **elija distinto** que los demás.
     Salen de que **juzga distinto qué es admirable**, y por eso queda por
     encima o por debajo de *su propio* ideal.
   - Las que resisten son las de **O y A**, donde la conducta bruta también
     difiere, y Sol C▼.
   - La deseabilidad común hace aparecer marcas nuevas (Opus C, gemma4 A y
     C, DeepSeek Flash@ A y E, glm5.3-flash O y E…). No entran en el retrato.
4. **P5 · panel.** Solo caen las marcas marginales. Por ejemplo, Argon H▼ cae
   al quitar cualquiera de 4 laboratorios, y glm H▼ sin deepseek o sin qwen.
   Ninguna marca grande depende de un laboratorio concreto.
5. **P6 · BH sobre 78 pruebas.** Resisten 18 de 27. Caen las 9 marginales:
   Haiku O y N, glm H, Gemini Flash O, Argon H, Luna E y N, Sol A y N. El
   resultado con BH sobre 65 pruebas (sin N) es el mismo.

**Desviación de interpretación, no de criterio.** La «inversión» de §26 se
aplicó a las variantes de una sola estimación: P2–P5. En P1, una mitad
aislada con signo contrario significativo se informa en el json
(`tasa_half_invertida`), pero no se usó para clasificar, porque §26 no lo
precisaba.

### ¿Obliga algún criterio a revisar el cuadro?

**Sí, P4.**
- El cuadro v2 mide **conducta relativa al ideal propio**. Es la definición
  de §8/§17, y la mantiene.
- Pero el texto del retrato («más Responsabilidad: cumple y planifica») se lee
  como una afirmación sobre la conducta comparada con la de otros modelos.
- Para C y H, esa afirmación no se sostiene sin el ajuste propio: lo que
  distingue a esos modelos es su juicio de deseabilidad, no lo que eligen.
- No se cambia el nivel de ninguna marca. Si se quieren publicar las 9
  frágiles por P4, haría falta otra redacción, del tipo «se aparta más que
  otros de lo que él mismo considera admirable». Esa decisión es de David.
- Las 8 marcas no publicables de O, C, A, H y E, más las 3 de N, deberían
  salir del cuadro público. Seis de las 8 ni siquiera resisten la
  corrección por comparaciones múltiples.

**Relación con el ISS (descriptiva, n = 10; sin ISS: DeepSeek Flash@,
DeepSeek Pro y Argon).**

| Rasgo | Spearman ρ | IC 95 % |
|---|---|---|
| Responsabilidad | +0,73 | +0,19 a +0,95 |
| Apertura | +0,42 | −0,37 a +0,96 |
| Extraversión | +0,39 | −0,27 a +0,87 |
| Honestidad-Humildad | +0,26 | −0,42 a +0,84 |
| Amabilidad | +0,25 | −0,50 a +0,87 |
| Neuroticismo | +0,05 | −0,61 a +0,75 |

Solo C tiene un IC que excluye 0. Con 10 modelos y el punto alto de Gemini
Flash (ISS 55, C 51) no se lee como relación establecida. Se anota para
mirarla cuando haya más modelos con las dos medidas.

### Recomendación para la web

1. **Publicar solo las 6 marcas robustas como frase**:
   - Haiku: menos Amabilidad.
   - Gemini 3.7 Flash: más Amabilidad.
   - gemma4 y mimo: más Apertura.
   - Argon: menos Apertura.
   - Sol: menos Responsabilidad.

   Los otros 7 modelos se describen como «perfil próximo al de los demás».
   Quedan así 6 de 13 modelos con algún rasgo distintivo publicable, frente a
   los 10 de 13 de G1.
2. **qwen3.6 se queda sin retrato publicable.** Sus tres marcas (O, C y H)
   son frágiles: P4, y además P3 en O. Lo mismo pasa con las marcas de C y H
   de Haiku y Gemini Flash.
3. Mostrar las puntuaciones de los seis rasgos sin ▲/▼ salvo en las robustas.
   N, solo descriptivo. E: no queda ninguna marca robusta, así que no hace
   falta aviso de marca, pero sí el de fiabilidad en la puntuación.
4. **Para recuperar retratos:**
   - más situaciones en C y H, que estrecharían el IC pero no resolverían P4;
   - o fijar ya, en un §28 previo a cualquier pasada nueva, si el producto
     publica «conducta frente a su ideal» o «conducta comparada», y redactar
     el retrato en consecuencia.

## 28. Qué afirma el cuadro público · decisión fijada ANTES de recalcular (20-10-2026)

**Decisión de David (20-10-2026): el retrato principal es la conducta
comparada.** Una frase del retrato («más Amabilidad: cede y coopera») afirma
que **el modelo elige más a menudo que los demás modelos** el polo alto de ese
rasgo en las mismas situaciones. No afirma nada sobre su propio ideal.

Se fija ahora, después de §27 pero antes de recalcular nada con esta
definición. Se conocen ya, por P4 de §27, qué marcas resisten con la
deseabilidad común y algunas que aparecen nuevas con ella. Por eso la regla
se escribe de forma que no dependa de qué modelos salgan favorecidos.

**Definición.**

- **Comparación entre modelos:** diferencia pareada por situación entre la
  elección del modelo y la media de los demás, 50·(e_m(i) − media de los
  demás e_o(i)), con e = fracción de veces que elige el polo alto (órdenes ×
  réplicas). Es exactamente la marca de §26 con la deseabilidad común (P4):
  un d(i) común a todos se cancela.
- **Puntuación mostrada:** 50 + 50·media_i(e_m(i) − d̄(i)), con d̄(i) = media
  de los juicios de deseabilidad de **todos** los modelos del panel. 50 =
  elige lo que el panel juzga admirable. Sustituye a la puntuación con la
  deseabilidad propia en el cuadro público.
- **Marca ▲/▼ publicable:** IC 95 % por bootstrap de situaciones que excluye 0
  en la comparación, y además las comprobaciones de §26 aplicadas a esta
  comparación:
  - P1: tasa de signo ≥ 90 %;
  - P2: se mantiene en réplica 0 y réplica 1;
  - P3: se mantiene en AB y en BA;
  - P5: se mantiene sin cada laboratorio;
  - P6: q < 0,05 con Benjamini-Hochberg sobre todas las pruebas del cuadro.

  P4 deja de ser una comprobación: ahora es la definición. Los niveles
  robusta / frágil / no publicable son los de §26 sobre esas cinco
  comprobaciones. **Solo las robustas llevan frase.**
- **Marcas nuevas.** Las que aparecen con esta definición y no estaban en el
  cuadro v2 (por ejemplo, las listadas en P4 de §27) **sí entran**: el
  cuadro se rehace entero con la definición nueva. Pasan por las mismas
  cinco comprobaciones que cualquier otra, sin trato aparte en ningún
  sentido.
- **Rasgos:** sin cambios respecto a §23. O, C, A y H, con marca. E, con
  marca solo si es robusta y con el aviso de fiabilidad. N, solo descriptivo,
  sin marca.

**La distancia al ideal propio** (la puntuación con d_m(i) de §8/§17/§21) se
conserva como **indicador secundario**, no publicado hasta que tenga su
propia sección, con su redacción («se aparta más que otros de lo que él
mismo juzga admirable») y sus criterios. Las 9 marcas que en §27 solo
fallaban P4 son evidencia de este indicador, no de la conducta comparada.

**Alcance.**

- Se aplica al cuadro público y a cualquier pasada nueva: banco v3.1 de E y N,
  modelos externos que se completen, réplicas en el tiempo.
- La selección de situaciones sigue usando la ventana de deseabilidad (§21),
  porque evita techo y suelo en la elección.
- `analizar_v3.py` y `analizar_robustez_v3.py` deben generar el cuadro
  público con esta definición. El cuadro con la deseabilidad propia queda
  como salida secundaria.

**Pendiente:** recalcular el cuadro con esta definición, pasar las cinco
comprobaciones y escribir los resultados en una sección nueva. No se
retoca §28 a la vista de esos resultados.
