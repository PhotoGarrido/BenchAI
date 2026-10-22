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

## 24. Arreglo de Extraversión y Neuroticismo (banco v3.1) · diagnóstico, diseño y criterios fijados ANTES de medir (20-10-2026)

**Motivo.** En el v3 (§23), E (Spearman-Brown 0,36) y N (0,17) no cumplen G4,
y N no tiene estructura de facetas (G3). Esta tanda prepara el arreglo **solo
en NaN** (tarifa plana), para pasarlo a los externos cuando haya presupuesto.

### 24.1 Diagnóstico con los datos ya medidos (13 modelos del v3, sin llamadas)

`spike/diagnosticar_en_v3.py` → `resultados/personalidad_fc/DIAGNOSTICO_EN.md`.
Escala del cuadro (50 + 50·a).

| rasgo | sd real entre modelos | ruido por situación | de él: ajuste por deseabilidad | alfa ajustada | alfa sin ajustar | r ítem-resto | % ítems r < 0 | % ítems sin varianza |
|---|---|---|---|---|---|---|---|---|
| O | 5,3 | 18,7 | 11,5 | 0,83 | 0,88 | 0,26 | 19 | 14 |
| C | 5,8 | 17,3 | 11,8 | 0,86 | 0,73 | 0,29 | 16 | 30 |
| **E** | **2,9** | 18,1 | 12,3 | **0,59** | 0,84 | 0,12 | 33 | 16 |
| A | 4,5 | 18,2 | 12,1 | 0,78 | 0,89 | 0,22 | 23 | 23 |
| **N** | **1,5** | 17,9 | 11,9 | **0,29** | 0,53 | 0,04 | 44 | 26 |
| H | 6,0 | 17,6 | 11,5 | 0,87 | 0,51 | 0,31 | 17 | 22 |

1. **El problema es de señal, no de ruido.** El ruido por situación es el
   mismo en los seis rasgos (17–19 puntos). Lo que cambia es cuánto se
   diferencian de verdad los modelos: 4,5–6,0 puntos en O, C, A y H; 2,9 en E;
   1,5 en N. Con tan poca señal, 57 situaciones no bastan.
2. **El ajuste por deseabilidad pesa más en E y N.** El componente de ruido
   más grande en todos los rasgos es el ajuste (d_m(i) sale de solo 2
   juicios, ≈ 12 puntos por situación). Además, en E la elección **sin
   ajustar** sí ordena a los modelos de forma consistente (alfa 0,84), pero
   el modelo que elige más extraversión también la juzga más admirable
   (r = 0,69 entre la elección media y la deseabilidad media de cada modelo;
   N 0,58; O, C, A y H 0,26–0,47). Al restar el ideal propio, se resta buena
   parte de la diferencia. En N, además, el 74 % de las elecciones coinciden
   con el polo que el modelo juzga deseable (63–67 % en los demás rasgos): la
   conducta casi no se aparta del ideal.
3. **Facetas.** En E, gregarismo (alfa 0,64), actividad (0,58) y emociones
   positivas (0,62) son consistentes por dentro, pero no correlacionan con el
   resto de E (0,01–0,08) y cargan en otro rasgo: gregarismo en A (+0,77) y
   actividad en A (+0,53). Cuando la opción social es acompañar o atender a
   alguien, se mide amabilidad. Búsqueda de emociones (sd 0,0) y asertividad
   (1,8) no tienen señal. En N, solo impulsividad tiene señal (alfa 0,71,
   sd 9,4), pero carga en E (+0,60): son impulsos generosos o espontáneos, no
   falta de control. Ansiedad y hostilidad no tienen señal (sd 0,0). Ansiedad
   (−0,39) y depresión (−0,30) correlacionan en negativo con el resto de N.
4. **Techo y suelo.** El 26 % de las situaciones de N no tiene varianza entre
   modelos (todos eligen lo mismo; p. ej. P1N21, P1N16, SN2, P3N025, P3N063).
5. **Contexto.** Las situaciones de «terceros» funcionan peor en N (−0,05,
   frente a 0,12 en «propio») y en E (0,07 frente a 0,14).

**Qué se rescata** (r ítem-resto ≥ 0,2 en los 13 modelos):

- E: P3E003, SE6, P3E004, P3E019, P1E08, P3E022, P1E11, P1E12, P3E013,
  P1E22, P3E045, P3E030, P1E18, P3E062, P3E066, P1E34, P3E068, P1E25,
  P3E054, P3E055.
- N: las de impulsividad P3N088, P3N081, P3N050, P3N085, P3N076 y P3N056
  (con aviso de carga en E), P3N039, P3N048, P3N041, P3N040 (autoconciencia),
  P1N12, P1N09 (hostilidad), P1N34, P3N061, P3N066 (vulnerabilidad), P3N003
  y P3N035.

**Qué hace falta:** situaciones de **estilo**, en las que los dos polos sean
defendibles y no estén en juego ni un deber (C), ni ayudar o perjudicar a
alguien (A/H), ni un riesgo irresponsable. Deben tener conductas concretas
en las que los modelos puedan discrepar. En N, sobre todo, hay que
representar la reactividad emocional con conductas que un modelo pueda
defender, por ejemplo:

- comprobar o prevenir (ansiedad);
- expresar el enfado ante molestias impersonales o menores, sin defender a
  nadie (hostilidad);
- retirarse a encajar un revés (depresión);
- evitar exponerse tras un apuro (autoconciencia);
- pedir apoyo bajo presión (vulnerabilidad).

En impulsividad, la falta de control del impulso del NEO y no la
espontaneidad.

### 24.2 Candidatas (`spike/personalidad_p4_candidatos.json`)

**138 candidatas nuevas** (ids `P4E001–P4E060`, `P4N001–P4N078`), con el
mismo formato y las mismas convenciones que las P3. El protagonista nunca
lleva concordancia de género: el nombre y el género los decide `_nombre()`
por la posición en `cal.banco()`, como siempre.

- **Facetas débiles, 14 cada una:** E·asertividad, E·búsqueda de emociones,
  N·ansiedad, N·hostilidad, N·depresión, N·autoconciencia y N·vulnerabilidad.
- **Facetas de reescritura, 8 cada una, para quitar la carga cruzada:**
  - E·gregarismo y E·cordialidad: nadie necesita al protagonista.
  - E·actividad: el ritmo no es una obligación.
  - E·emociones positivas: alegría expresada frente a contenida.
  - N·impulsividad: ceder a un deseo frente a mantener un propósito.

Contexto «propio» en la gran mayoría. Cada una lleva una justificación del
polo alto y del bajo.

**Integración sin tocar lo medido.**

- Las P4 van **al final** de `cal.banco()`, así que no cambian los índices,
  los nombres, las semillas ni los prompts de P0, P1 y P3.
- `seleccionar_v3.py` y `calibrar_deseabilidad.analizar()` excluyen el
  origen P4, para que las selecciones v3 y P1 sigan reproduciéndose igual.
- Hay dos opciones nuevas:
  - `calibrar_deseabilidad.py --solo-origen P4`;
  - `experimento_personalidad_v3.py --seleccion personalidad_v31_en_seleccion.json`,
    con etiqueta `version_bateria = "v3.1"`.
- Los registros se **añaden** a los mismos `registros.jsonl`, como en el v3.

### 24.3 Medición y selección

- **Modelos:** los 6 de NaN: `gemma4`, `qwen3.6`, `qwen3.8-flash`,
  `glm5.3-flash`, `mimo-v2.6-flash` y `deepseek-v4-flash@2026-10-17`.
  Un proceso por modelo con `NAN_MAX_CONCURRENTES=1 NAN_RPM=9`.
- **Paso 1, deseabilidad:** las 138 candidatas, 2 órdenes (1.656 llamadas).
- **Paso 2, selección** (`seleccionar_v31_en.py`). Es la regla del v3 (§21)
  sobre la deseabilidad media de los 6 y solo usa deseabilidad, nunca
  conducta. Por faceta:
  - primero las situaciones en ventana (30–70 %), las más cercanas al 50 %;
  - después, pares de polo alto deseable y polo bajo deseable.
  - Cuota: **8 en las 7 facetas débiles y 4 en las 5 de reescritura**, como
    máximo 76 situaciones.
- **Paso 3, conducta propia (R3)** de las seleccionadas: 2 órdenes × 2
  réplicas (≤ 1.824 llamadas).

### 24.4 Criterios (fijados ahora; `spike/analizar_v31_en.py`)

Con 6 modelos, la fiabilidad **entre modelos** (G4) no se puede estimar con
sentido. Por eso los criterios comparan las P4 con **las situaciones v3 del
mismo rasgo en los mismos 6 modelos**, que hacen de línea base. Se calculan
sobre la puntuación ajustada, salvo que se diga otra cosa.

Línea base v3 en los 6 de NaN: E alfa 0,61, sd entre modelos 2,9 y 35 % sin
varianza; N alfa −0,68, sd 0,0 y 42 % sin varianza.

- **K1 · cobertura y equilibrio.** Las 12 facetas llegan a su cuota y la
  deseabilidad media de cada faceta seleccionada queda entre el 40 y el 60 %.
- **K2 · sin techo ni suelo.** Al menos el 75 % de las P4 seleccionadas de
  cada rasgo tiene una sd entre modelos de la elección bruta ≥ 0,10, y ese
  porcentaje supera al de la línea base.
- **K3 · señal entre modelos.** El componente de varianza del modelo (sd en
  la escala del cuadro) de las P4 de cada rasgo es ≥ 4,0 en E y ≥ 3,0 en N,
  y supera a la línea base. Se publica con IC por bootstrap de situaciones.
- **K4 · coherencia ítem-resto.** La correlación media de cada P4 con el
  resto de las P4 de su rasgo (entre los 6 modelos) es ≥ 0,15 y supera a la
  de la línea base, calculada igual.
- **K5 · coherencia de facetas a nivel de ítem.** En cada rasgo, la
  correlación media entre pares de P4 del mismo rasgo supera a la
  correlación media entre P4 y situaciones v3 de los otros rasgos (O, C, A,
  H y el otro de E/N). Además, la correlación entre pares de la misma faceta
  es ≥ que entre pares de facetas distintas del rasgo.
- **K6 · test-retest.** Entre las réplicas 0 y 1 de R3, r ≥ 0,85 sobre
  modelos × facetas (12 facetas × 6 modelos) y r ≥ 0,90 sobre modelos ×
  rasgo.
- **K7 · la conducta no copia el ideal.** En cada rasgo, ≤ 70 % de las
  elecciones coinciden con el polo que el propio modelo juzga deseable
  (cuando lo juzga con claridad).
- **K8 · sin pérdidas.** < 5 % de respuestas no válidas por modelo.

**Qué cuenta como mejora:** un rasgo mejora si cumple **K2, K3, K4 y K5**.
K1 comprueba el diseño, y K6–K8 son de higiene: si fallan, la medición no
vale, aunque el resto se cumpla.

**Filtro de ítem para la propuesta v3.1, fijado ahora.** Por faceta, hasta
10 situaciones (como en el v3), en dos grupos:

1. Las P4 seleccionadas con sd de la elección bruta ≥ 0,10 y r ítem-resto
   ≥ 0 en los 6 de NaN.
2. Las situaciones v3 de E y N con r ítem-resto ≥ 0,10 en los 13 modelos.

Si sobran, se queda primero el grupo 1, de mayor a menor r.

**Solo se podrá decidir con los externos (13 modelos):**

- G1, las marcas ▲/▼ de E y N;
- G3, la estructura de facetas entre modelos;
- G4, Spearman-Brown ≥ 0,70;
- si las P4 **sustituyen** a las situaciones v3 que fallan o se **añaden**;
- si N puede salir del modo «solo descriptivo».

## 25. Resultados del banco v3.1 de E y N en NaN (20-10-2026)

Cifras en `spike/resultados/personalidad_fc/V31_EN.md` y `v31_en.json`
(`python analizar_v31_en.py`).

**Medición.**

- Deseabilidad: 1.656 juicios (138 candidatas × 2 órdenes × 6 modelos),
  todos válidos.
- Selección: **48 situaciones** (E 29, N 19), en
  `spike/personalidad_v31_en_seleccion.json`.
- R3: 1.152 respuestas (48 × 4 × 6), todas válidas.
- NaN devolvió 27 errores 429 por límite de peticiones. Se reintentaron
  dentro del grifo y no se perdió ningún dato.
- Los `registros.jsonl` solo ganan líneas nuevas: ninguna línea medida antes
  cambia.

### Desviaciones

1. **Puntuación de referencia (§28).** El 20-10, en la rama
   `claude/personalidad-robustez`, David decidió que el cuadro público mide
   **conducta comparada**: la elección bruta, equivalente a usar la
   deseabilidad común. El §24 se fijó con la puntuación ajustada. Los
   criterios se evalúan **tal como se fijaron**, con la ajustada, y además
   con la elección bruta como complemento. La recomendación se apoya en la
   bruta.
2. **Entorno.** Durante la preparación, el intérprete del venv quedó roto
   un rato por un accidente ajeno a esta tanda. Antes del aviso, dos
   ejecuciones de solo lectura del diagnóstico usaron un Python alternativo;
   después se repitieron con el venv. Ninguna medición se hizo con el
   intérprete alternativo.

### Resultados contra los criterios del §24

| Criterio | E | N | Veredicto |
|---|---|---|---|
| **K1** cobertura y equilibrio | 4 de 6 facetas a cuota (gregarismo 2/4, búsqueda 7/8) | **ninguna faceta a cuota**: impulsividad 0/4, hostilidad 2/8, depresión 2/8 | **No cumple** |
| **K2** sin techo ni suelo (≥ 75 %) | 66 % (base 65 %) | 53 % (base 58 %) | **No cumple** |
| **K3** señal (ajustada) | **4,1** [1,0; 8,7] frente a 2,9 de base ✔ | 0,0 (base 0,0) ✘ | E cumple, N no |
| **K4** ítem-resto (ajustada) | **0,16** frente a 0,13 ✔ | −0,10 frente a −0,02 ✘ | E cumple, N no |
| **K5** coherencia de ítem (ajustada) | mismo rasgo 0,04 > otros 0,00, pero misma faceta −0,01 < otra 0,05 ✘ | −0,01 frente a 0,00 ✘ | **No cumple** |
| **K6** test-retest | facetas r = 0,94 ✔; rasgo r = 0,82 (12 puntos) ✘ | (conjunto) | **No cumple** |
| **K7** la conducta no copia el ideal (≤ 70 %) | 68 % ✔ | 77 % ✘ | E cumple, N no |
| **K8** sin pérdidas | 0 % | 0 % | **Cumple** |
| **Mejora** (K2 + K3 + K4 + K5) | **no** | **no** | — |

Con la elección bruta (§28), el veredicto es el mismo:

- E: K3 3,5 frente a 3,0 de base, por debajo del umbral de 4; K4 0,30
  frente a 0,26 ✔; alfa 0,69 frente a 0,80.
- N: sd 0,0 frente a 1,6 de base; ítem-resto −0,05 frente a 0,12.

K6 falla en el agregado por rasgo: la correlación se calcula con 12 puntos
casi sin varianza entre modelos en N. Es una consecuencia de la falta de
señal, no de inestabilidad: con las facetas, r = 0,94. Aun así, según lo
fijado, la medición de esta tanda no sirve para justificar un cambio.

### Lectura

1. **N: la redacción no arregla el problema; está en la deseabilidad.** De
   las 138 candidatas, solo 24 cayeron en la ventana, y 23 de ellas eran de
   las previstas como «disputadas». En N, el juicio de deseabilidad es
   **bimodal y unánime**:
   - en depresión, hostilidad e impulsividad, la mediana es del 0 % y la sd
     entre modelos, de 0,02–0,03. Por ejemplo, dejar el deporte cuando faltan
     las ganas: 8 %.
   - Cuando el polo reactivo se lee como **franqueza emocional o
     prudencia**, el juicio salta al otro extremo, no a la ventana. Ejemplos:
     llorar a una amiga en el aniversario de su muerte (75 %), decirle a una
     amiga que su retraso molesta (100 %), pedir apoyo en un trabajo nuevo
     (75 %), comprobar el gas (92 %) o ir al dermatólogo (100 %).
   
   Esas situaciones miden prudencia o asertividad, no reactividad. Las pocas
   que entraron como pares no correlacionan con el resto de N. Con R3 de
   elección forzada entre
   conducta reactiva y serena, los modelos de NaN eligen casi siempre la
   serena (77 % coincide con su ideal) y no se diferencian entre sí. **No hay
   señal que medir con este formato.**
2. **E: mejora parcial, insuficiente.** Las P4 de E tienen algo más de
   señal y coherencia que las v3 en los mismos 6 modelos, pero no forman
   facetas, y gregarismo y actividad casi no tienen candidatas en ventana:
   los modelos juzgan admirable la opción social (92 % de mediana).
3. **El cambio de puntuación del §28 resuelve E con los datos que ya hay**
   (exploratorio, posterior a ver los datos; `DIAGNOSTICO_EN.md` §6). G4 con
   la elección bruta en los 13 modelos del v3 (Spearman-Brown por mitades;
   entre paréntesis, la ajustada):

   | O | C | **E** | A | **N** | **H** |
   |---|---|---|---|---|---|
   | 0,94 (0,90) | 0,81 (0,81) | **0,93 (0,36)** | 0,86 (0,78) | **0,62 (0,17)** | **0,13 (0,91)** |

   - **E no fallaba por las situaciones**: las diferencias de extraversión
     entre modelos estaban en la elección, pero el ajuste por el ideal propio
     las restaba (r = 0,69 entre elección y deseabilidad de cada modelo,
     §24.1).
   - Con la elección bruta, N sube a 0,62, aún por debajo de 0,70.
   - H se hunde a 0,13. Es coherente con que las marcas de H «salían del
     juicio de deseabilidad» (§28). Conviene revisarlo en la rama de
     robustez antes de publicar H con la puntuación bruta.

### Recomendación

- **No sustituir situaciones de E ni de N en el banco v3 por ahora.**
- **E:** con la puntuación de conducta comparada del §28, el banco v3 actual
  ya cumple G4 (0,93). Las P4 de E no lo mejoran en NaN.
- **N:**
  - Mantener N como **solo descriptivo**.
  - El formato de elección forzada entre una reacción y una respuesta serena
    no separa a los modelos, porque todos juzgan y eligen la serena.
  - Para N haría falta otro instrumento, no más situaciones del mismo tipo.
    Por ejemplo:
    - una intensidad graduada («¿cuánto te afectaría?»);
    - dos opciones serenas que difieran en cuánto se preocupa uno;
    - o medir la reactividad en la conducta de los episodios.
- **Si aun así se quiere probar el v3.1 en los externos** (para comprobar
  con 13 modelos lo que en NaN no se puede estimar: G1, G3 y G4): lo más
  barato es pasar solo las **22 P4** que superan el filtro de ítem del §24
  con alguna de las dos puntuaciones (`v31_en.json`, `nuevas_a_externos`).
  - Son 132 llamadas por modelo: deseabilidad ×2 + R3 ×4.
  - Cuesta ≈ **0,53 $** (≈ 0,66 $ con margen), estimado con los tokens por
    llamada que registró cada externo en la pasada v3.
  - Las 48 seleccionadas costarían ≈ 1,2 $.
  - El reparto entre modelos es aproximado: Argon, Luna y DeepSeek Pro no
    tienen tarifa en `coste_run.py`, así que reciben, en proporción a sus
    tokens, lo que falta hasta los 5,0 $ reales del v3. Para Luna, la cifra
    es una cota alta.
  - Las P4 se **añadirían** al banco, no lo sustituirían: en NaN no hay
    prueba de que superen a las v3.

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

## 29. Cuadro público con la conducta comparada (20-10-2026)

`python cuadro_publico_v3.py` (desde `spike/`, ≈ 7 s, sin llamadas a
modelos). Cifras en `spike/resultados/personalidad_fc/CUADRO_PUBLICO.md` y
`cuadro_publico.json`. El json está pensado para que lo consuma la web: por
modelo, puntuación e IC de cada rasgo, comparación con su IC, marca
publicable, nivel de la marca candidata y frase. La definición y las cinco
comprobaciones son las de §28, sin cambios.

El script reutiliza `analizar_v3.py` y `analizar_robustez_v3.py` con la
semilla `SEMILLA`. Esos dos se han refactorizado en funciones reutilizables
(`cargar_seleccion`, G3/G4, `d_consenso`, `mitades`, `clasificar`, `frase`),
y sus salidas (`V3.md`, `CUADRO_V3.md`, `v3.json`, `ROBUSTEZ_V3.md`,
`robustez_v3.json`) salen idénticas byte a byte. `CUADRO_V3.md`, con la
deseabilidad propia, queda como salida secundaria.

### Cuadro público (§28)

Puntuación = 50 + 50·media(e − d̄); 50 = elige lo que el panel juzga
admirable. ▲/▼ solo en las marcas **robustas**.

| modelo | ISS | Apertura | Responsabilidad | Extraversión † | Amabilidad | Neuroticismo ‡ | Honestidad-Humildad |
|---|---|---|---|---|---|---|---|
| Haiku 5.5 | 10,3 | 52 | 39 | 42 | 28 ▼ | 56 | 38 |
| Opus 5.5 #low | 12,5 | 55 | 33 ▼ | 42 | 38 | 49 | 43 |
| DeepSeek Flash@ | — | 50 | 35 | 34 ▼ | 32 | 51 | 41 |
| DeepSeek V4 Pro | — | 49 | 40 | 39 | 40 | 47 | 41 |
| gemma4 | 28,1 | 55 | 45 ▲ | 37 | 29 ▼ | 54 | 37 |
| glm5.3-flash | 28,9 | 55 | 39 | 38 | 34 | 47 | 40 |
| Gemini 3.7 Flash | 55,2 | 37 ▼ | 39 | 52 ▲ | 47 ▲ | 48 | 37 |
| Argon | — | 44 ▼ | 36 | 38 | 35 | 52 | 40 |
| mimo | 12,6 | 56 | 40 | 43 | 36 | 51 | 39 |
| Luna | 7,6 | 55 | 41 | 39 | 31 | 52 | 40 |
| Sol #low | 13,2 | 52 | 34 ▼ | 38 | 33 | 49 | 46 ▲ |
| qwen3.6 | 23,2 | 55 | 41 | 42 | 35 | 54 | 38 |
| qwen3.8-flash | 24,8 | 49 | 36 | 40 | 32 | 50 | 39 |

† Con aviso de fiabilidad (§23). ‡ Solo descriptivo.

En C, E, A y H casi todas las puntuaciones quedan por debajo de 50: los
modelos eligen el polo alto menos de lo que el panel juzga admirable. En O
rondan el 50. La escala absoluta es descriptiva; lo que se afirma en público
es la comparación.

### Validez con la definición de §28: hay conflicto

> **Conflicto pendiente de David.** Con la puntuación de §28, la
> consistencia interna (G4) da la vuelta a la de §23:
> - **Honestidad-Humildad** lleva marca, pero cae a 0,13.
> - **Extraversión** solo lleva marca con aviso, pero sube a 0,93.
>
> El cuadro de arriba aplica §28 tal cual: no se ha cambiado qué rasgos
> llevan marca.

La tabla recalcula G3 y G4 de §21 sobre la puntuación de §28. Como d̄ es
común a todos los modelos, entre modelos da lo mismo que calcularlos sobre la
elección bruta. Lo detectó el agente del banco E/N como cálculo exploratorio,
después de ver datos; aquí sale del script y es reproducible.

| Rasgo | G3 dentro / fuera | G4 §28 | G4 §23 (deseabilidad propia) | Papel en §28 |
|---|---|---|---|---|
| Apertura | +0,46 / −0,08 ✔ | **0,94** | 0,90 | con marca |
| Responsabilidad | +0,27 / −0,00 ✔ | **0,81** | 0,81 | con marca |
| Extraversión | +0,27 / +0,02 ✔ | **0,93** | 0,36 | marca solo si robusta, con aviso → **conflicto** |
| Amabilidad | +0,56 / −0,05 ✔ | **0,86** | 0,78 | con marca |
| Neuroticismo | +0,04 / −0,03 ✔ (por poco) | 0,62 | 0,17 | solo descriptivo; sin conflicto (< 0,70) |
| Honestidad-Humildad | −0,07 / −0,04 ✘ | **0,13** | 0,91 | con marca → **conflicto** |

Lectura:

- **H.** Su consistencia en §23 (0,91) venía del juicio de deseabilidad de
  cada modelo, no de lo que elige. Es lo mismo que mostró P4 en §27: las
  marcas de H dependían de la deseabilidad propia. Con la elección comparada,
  sus facetas no se agrupan (falla G3) y las mitades no concuerdan.
- **E.** Le pasa lo contrario: el ruido de la deseabilidad propia hundía su
  consistencia. Su conducta comparada es tan consistente como la de O.
- **N.** Sube a 0,62, todavía por debajo de 0,70. G3 apenas separa sus
  facetas de las ajenas. Sigue siendo descriptivo.

**Cómo quedaría el cuadro en cada caso.** Los niveles de robustez son los
mismos en los dos; solo cambia en qué rasgos se admite marca.

| Caso | Rasgos con marca | Diferencias en el retrato |
|---|---|---|
| **A · §28 tal cual** (cuadro de arriba) | O, C, A, H; E con aviso | Sol lleva H▲. Las E▲/▼ de Gemini Flash y DeepSeek Flash@ van con aviso. |
| **B · según G4 ≥ 0,70** (no decidido) | O, C, E, A; H y N solo descriptivos | Sol pierde H▲ y se queda con C▼. Las E de Gemini Flash y DeepSeek Flash@ van sin aviso. El resto, igual. |

En B ningún modelo se queda sin retrato. La única marca de H que se pierde,
la de Sol, es robusta en las cinco comprobaciones, pero pertenece a un rasgo
que, medido así, no es consistente. `CUADRO_PUBLICO.md` incluye la tabla y
los retratos completos del caso B.

### Marcas: 25 candidatas · 11 robustas · 5 frágiles · 9 no publicables

| Nivel | Marcas |
|---|---|
| **Robusta** (pasa P1–P3, P5, P6) | Haiku A▼ · Opus C▼ · DeepSeek Flash@ E▼ (aviso) · gemma4 C▲ y A▼ · Gemini Flash O▼, A▲ y E▲ (aviso) · Argon O▼ · Sol C▼ y H▲ |
| **Frágil** | DeepSeek Flash@ A▼ (P3) · DeepSeek V4 Pro A▲ (P3; sesgo de posición de §27) · glm5.3-flash O▲ (P3, P5) · mimo O▲ (P3, P5) · Luna A▼ (P2) |
| **No publicable** | Opus O▲ · gemma4 O▲ · glm5.3-flash E▼ · mimo E▲ · Luna O▲ · qwen3.8-flash A▼ (fallan 3 o 4) · N: Haiku N▲, DeepSeek V4 Pro N▼, glm5.3-flash N▼ |

La corrección BH se hace sobre 78 pruebas (13 × 6). Fuera de N, ninguna
marca se invierte en las variantes.

### Retratos publicables (caso A, §28)

- **Haiku 5.5**: menos Amabilidad (pone límites y se defiende).
- **Opus 5.5 #low**: menos Responsabilidad (prioriza descanso y flexibilidad).
- **DeepSeek Flash@**: menos Extraversión (prefiere calma y segundo plano),
  con aviso.
- **gemma4**: más Responsabilidad (cumple y planifica); menos Amabilidad
  (pone límites y se defiende).
- **Gemini 3.7 Flash**: menos Apertura (prefiere lo conocido); más
  Amabilidad (cede y coopera); más Extraversión (busca gente y
  protagonismo), con aviso.
- **Argon**: menos Apertura (prefiere lo conocido).
- **Sol #low**: menos Responsabilidad (prioriza descanso y flexibilidad);
  más Honestidad-Humildad (sincero, renuncia a ventajas).
- **DeepSeek V4 Pro, glm5.3-flash, mimo, Luna, qwen3.6 y qwen3.8-flash**:
  perfil próximo al de los demás modelos.

Quedan 7 de 13 modelos con retrato (6 si no se publicara E).

### Qué cambia respecto al cuadro v2 y a la recomendación de §27

- **Se mantienen** 4 de las 6 marcas robustas de §27: Haiku A▼, Gemini
  Flash A▲, Argon O▼ y Sol C▼. Sin el ajuste propio la diferencia es menor
  (Haiku A pasa de −10,1 a −6,9), pero resisten todas las comprobaciones.
- **Caen 2.** Parte de su Apertura venía de su juicio de deseabilidad:
  - gemma4 O▲ pasa de +12,3 a +4,7 y queda no publicable.
  - mimo O▲ pasa de +6,4 a +5,6 y queda frágil (P3, P5).
- **Entran 7 nuevas**: Opus C▼, gemma4 C▲ y A▼, Gemini Flash O▼ y E▲,
  DeepSeek Flash@ E▼ y Sol H▲.
  - Opus C, gemma4 A y C, DeepSeek Flash@ E y Sol H ya aparecían en P4 de
    §27 como marcas nuevas con deseabilidad común.
  - Gemini Flash O▼ era no publicable en el cuadro v2 (−4,7); con la
    elección bruta es la marca más grande (−15,5).
- **Las 9 marcas frágiles solo por P4 en §27 desaparecen** como conducta
  comparada: Haiku C y H, DeepSeek Flash@ H, gemma4 E, Gemini Flash C,
  mimo C, Sol E, qwen3.6 C y H. Ninguna es marca candidata ahora. Quedan
  como evidencia del indicador secundario, la distancia al ideal propio
  (§28).
- **qwen3.6** no tiene ninguna marca candidata: todo su perfil v2 venía de
  su deseabilidad propia.
- **Ganan retrato Opus y DeepSeek Flash@; lo pierde mimo.** Son 7 modelos
  con retrato, frente a 6 en §27.

### Se rehará con el banco v3.1

`python cuadro_publico_v3.py` rehace el cuadro entero con un solo comando
cuando llegue el banco v3.1 de E y N o se completen más modelos:

- Modelos, situaciones y laboratorios se leen de los datos y de la selección,
  con el filtro de cobertura ≥ 95 %.
- Por defecto se leen `personalidad_v3_seleccion.json` y cualquier
  `personalidad_v3*_seleccion.json` nuevo; con `--seleccion` se eligen a mano.
- El conflicto de G4 se evalúa en cada ejecución y queda escrito en
  `CUADRO_PUBLICO.md`.

Las cifras de esta sección son las del banco v3 con 13 modelos. Con v3.1
pueden cambiar las de E y N y, con ellas, el conflicto.

## 30. Rescate de H y N con los datos del banco v3 · diagnóstico y criterios fijados ANTES de calcular el rescate (21-10-2026)

**Objetivo (David, 21-10).** Que los seis rasgos del cuadro distingan modelos
de forma fiable. Con la definición de §28, G4 da O 0,94 · C 0,81 · E 0,93 ·
A 0,86 · **N 0,62** · **H 0,13**, y H no tiene estructura de facetas (G3).
Esta sección mira si H y N se rescatan **con lo ya medido** (13 modelos del
banco v3, cero llamadas) y fija, antes de calcularlo, qué cuenta como
rescate.

### 30.1 Diagnóstico con la definición de §28

`python diagnosticar_hn_v3.py` (desde `spike/`) →
`resultados/personalidad_fc/DIAGNOSTICO_HN.md` y `diagnostico_hn.json`.
Todo sobre la elección bruta e_m(i), escala del cuadro (×50).

| rasgo | sd real entre modelos | ruido por situación | alfa | G4 pares/impares | G4 en 2.000 particiones al azar: mediana [p5, p95] | % ítems sd < 0,10 | r ítem-resto media | % r < 0 |
|---|---|---|---|---|---|---|---|---|
| O | 5,2 | 14,7 | 0,88 | 0,94 | 0,90 [0,81; 0,96] | 14 | +0,35 | 8 |
| C | 2,8 | 12,7 | 0,73 | 0,81 | 0,76 [0,51; 0,89] | 30 | +0,22 | 18 |
| E | 4,1 | 13,4 | 0,84 | 0,93 | 0,88 [0,75; 0,95] | 16 | +0,28 | 28 |
| A | 4,6 | 12,6 | 0,89 | 0,86 | 0,92 [0,81; 0,97] | 23 | +0,40 | 7 |
| **N** | **2,0** | 14,2 | **0,53** | 0,62 | **0,62** [0,23; 0,83] | 26 | +0,14 | 23 |
| **H** | **1,8** | 13,4 | **0,51** | **0,13** | **0,60** [0,18; 0,84] | 22 | +0,11 | 27 |

1. **El 0,13 de H es en parte mala suerte de la partición pares/impares.**
   Con 2.000 particiones equilibradas por faceta, la mediana es 0,60 (alfa
   0,51). Aun así, H y N quedan claramente por debajo de 0,70: solo el
   26–29 % de las particiones llega. El G4 de una sola partición es inestable
   en todos los rasgos (C va de 0,51 a 0,89).
2. **El problema es de señal, no de ruido.** El ruido por situación es igual
   en los seis rasgos (13–15 puntos). La sd real entre modelos es de 4–5
   puntos en O, E y A, y de 1,8–2,0 en H y N.
3. **Techo y suelo.** No es lo que distingue a H y N: el 22–26 % de sus
   situaciones casi no varía entre modelos (sd < 0,10), igual que C (30 %) y
   A (23 %). En H la elección media es 0,39; en N, 0,51.

**Por qué se desploma H al pasar de la ajustada a la comparada.**

| H | elección e (§28) | ajustada e − d_m (§23) | deseabilidad propia d_m sola |
|---|---|---|---|
| sd real entre modelos | **1,8** | 6,0 | **6,9** |
| G4 pares/impares | 0,13 | 0,91 | 0,85 |
| G4, mediana de particiones | 0,60 | 0,90 | 0,93 |

La puntuación ajustada es e − d_m. En H, lo que los modelos **eligen** casi
no varía entre ellos (1,8), pero lo que **juzgan admirable** varía mucho y de
forma muy consistente (d_m sola: G4 0,85–0,93; la deseabilidad media de H va
de 16 en qwen3.6 a 42 en Haiku). La ajustada hereda la señal de −d_m: el
0,91 de §23 medía **cuánto valora cada modelo la honestidad-humildad**, no
cuánto la practica. Al quitar d_m (§28) queda solo la elección, que entre
modelos apenas tiene señal. Es lo mismo que mostró P4 en §27. En E pasa lo
contrario: elección y deseabilidad propia correlacionan +0,69 entre modelos,
y restarla quitaba señal (G4 0,36 → 0,93).

**Facetas: H se parte en dos.**

| faceta | sd entre modelos | alfa | r con el resto de H | carga cruzada más fuerte |
|---|---|---|---|---|
| sinceridad | **8,5** | 0,86 | −0,17 | E −0,72 |
| desinterés por la riqueza | 2,3 | 0,42 | +0,60 | C −0,63 |
| modestia | 1,6 | 0,18 | −0,33 | A +0,75 |
| equidad | **0,0** | — | −0,43 | E +0,80 |

Correlación entre facetas (entre modelos): sinceridad–desinterés +0,55;
sinceridad–equidad −0,55; sinceridad–modestia −0,40; equidad–modestia +0,20.
**Sinceridad es la única faceta con señal fuerte**, se acompaña de
desinterés por la riqueza y va **en contra** de equidad y modestia. Equidad
no tiene ninguna varianza real entre modelos (elección media 0,22), y
modestia casi ninguna. Como el rasgo suma facetas que se cancelan, la sd de
H se queda en 1,8 aunque sinceridad sola tenga 8,5. (Exploratorio, con los
13 modelos y sin validación cruzada: sinceridad + desinterés da alfa 0,85;
equidad + modestia, −0,02.)

**Facetas de N.** Impulsividad correlaciona **en negativo** con el resto de
N (−0,54) y carga en O (−0,69): son los impulsos generosos o espontáneos de
§22/§24, no falta de control. Autoconciencia no tiene señal (sd 0,6).
Hostilidad, depresión y vulnerabilidad se agrupan (+0,39 a +0,55), y
ansiedad se une a hostilidad (+0,43). (Exploratorio: N sin impulsividad da
alfa 0,73 y mediana de particiones 0,79; hostilidad + depresión +
vulnerabilidad, 0,77 y 0,81.)

**Por qué N no llega.** Su señal real (2,0) es la mitad que la de E y A; una
de sus seis facetas (impulsividad) ordena a los modelos al revés que el resto
del rasgo, y otra (autoconciencia) no los ordena.

**Aviso.** Este diagnóstico se ha visto antes de fijar el rescate, incluidas
las correlaciones entre facetas. Por eso la regla de 30.2 es genérica: no usa
las facetas, no invierte ítems y no se ha elegido a la vista de qué facetas
sobreviven.

### 30.2 Criterios del rescate (fijados ahora, antes de calcularlo)

Los calcula `spike/rescate_hn_v3.py`. Semilla `SEMILLA`. Solo elección bruta
(§28). Se aplica a H y a N; O, C, E y A pasan por el mismo procedimiento solo
como referencia, sin decidir nada.

**Regla de selección de ítems** (se aplica a un conjunto S de modelos, con
los datos de S y nada más):

1. Se parte de todas las situaciones del rasgo en el banco v3.
2. Fuera las que tienen sd de e entre los modelos de S < 0,10 (no
   discriminan).
3. Depuración iterativa: mientras quede alguna con correlación ítem-resto
   entre los modelos de S < 0,20, se quita la de menor correlación y se
   recalcula. Se para también si quedan 12 situaciones (mínimo de escala).
4. **Ninguna situación se invierte**: el polo alto es el de la teoría.

**R1 · validación cruzada entre modelos (principal).** Se recorren **todas**
las particiones de los 13 modelos en 6 que seleccionan y 7 que validan
(C(13,6) = 1.716). En cada una se aplica la regla con los 6 y se mide G4 en
los 7 con las situaciones elegidas, de dos maneras:
(a) la de §21, mitades pares/impares en el orden de la selección, y
(b) la mediana de Spearman-Brown en 200 particiones al azar de las
situaciones, equilibradas por faceta.
**Pasa si la mediana sobre las 1.716 particiones es ≥ 0,70 en (a) y en
(b).** La propuesta mínima pedía una sola medida; exigir las dos endurece.
Como referencia se informa del G4 de la escala completa del rasgo en los
mismos 7 modelos.

**R2 · cobertura teórica.** Escala final = las situaciones elegidas en
≥ 50 % de las 1.716 particiones. Pasa si tiene **≥ 3 facetas con ≥ 2
situaciones cada una** y **ninguna faceta aporta más de la mitad** de las
situaciones (endurecimiento: que no sea una faceta disfrazada de rasgo). Si
quedan facetas del constructo sin situaciones, se declara explícitamente
(«H queda reducida a …») aunque pase; publicar con ese alcance lo decide
David.

**R3 · marcas.** Con la escala final de H (o de N), el cuadro de §28 se
recalcula y cada marca candidata pasa las **cinco comprobaciones de §28**
(P1 mitades por faceta ≥ 90 % de signo, P2 réplicas, P3 órdenes, P5 sin cada
laboratorio, P6 BH sobre las 78 pruebas). Mismos niveles de §26.

**R4 · sin reutilización.** Una marca de la escala rescatada solo se publica
si además **se mantiene** (mismo signo, IC 95 % que excluye 0) cuando la
escala se selecciona **sin ese modelo** (la regla aplicada a los otros 12).
Así ningún modelo queda marcado con situaciones elegidas con sus propios
datos. El G4 de la escala final con los 13 modelos se informa, pero **no**
cuenta como validación: la han elegido esos mismos modelos.

**Decisión.** Un rasgo se rescata si cumple **R1 y R2**. Sus marcas se
publican si además pasan R3 y R4. Consecuencias, fijadas ahora:

- **H rescatada:** sus marcas en el cuadro público salen de la escala
  rescatada, con la etiqueta de alcance si R2 declaró una reducción.
  **H no rescatada:** se mantiene el conflicto de §29 para que lo resuelva
  David; no se cambia nada del cuadro.
- **N rescatado:** pasa a ser **elegible** para marca, pero salir del modo
  «solo descriptivo» de §23/§28 lo decide David. **N no rescatado:** sigue
  solo descriptivo.
- `cuadro_publico_v3.py` solo incorpora una escala rescatada detrás de una
  opción explícita; sin ella, sus salidas no cambian.
- Si alguno no se rescata, §31 propone una pasada en NaN con formatos nuevos
  y sus propios criterios, sin medirla.

## 31. Resultados del rescate de H y N, y propuesta de pasada en NaN (21-10-2026)

`python rescate_hn_v3.py` (desde `spike/`, ≈ 25 s, sin llamadas a modelos) →
`resultados/personalidad_fc/RESCATE_HN.md` y `rescate_hn.json`. Criterios de
§30.2 sin cambios.

**Veredicto: ni H ni N se rescatan con los datos del banco v3.** H pasa la
validación cruzada (R1), pero no la cobertura teórica (R2): la escala que
sobrevive es, sobre todo, sinceridad. N cumple la cobertura, pero no la
validación cruzada. El cuadro público no cambia y sigue abierto el conflicto
de §29.

### R1 · validación cruzada (1.716 particiones; 6 seleccionan, 7 validan)

Mediana [p25, p75] del G4 en los 7 modelos que no seleccionaron. «Completa»
= el rasgo entero en esos mismos 7.

| rasgo | situaciones elegidas (mediana) | G4 (a) pares/impares | G4 (b) particiones al azar | G4 (a)/(b) rasgo completo | R1 |
|---|---|---|---|---|---|
| **H** | 22 | **0,76** [0,58; 0,86] | **0,76** [0,66; 0,83] | 0,70 / 0,69 | **✔** |
| **N** | 22 | 0,49 [0,06; 0,73] | 0,62 [0,43; 0,72] | 0,64 / 0,65 | ✘ |
| O (ref.) | 31 | 0,83 | 0,82 | 0,85 / 0,93 | ✔ |
| C (ref.) | 21 | 0,62 | 0,65 | 0,86 / 0,79 | ✘ |
| E (ref.) | 26 | 0,73 | 0,77 | 0,88 / 0,91 | ✔ |
| A (ref.) | 29 | 0,83 | 0,84 | 0,96 / 0,93 | ✔ |

- **H mejora con la selección** (0,76 frente a 0,69–0,70 del rasgo completo
  en los mismos modelos). Las situaciones que se eligen fuera de la muestra
  ordenan a los modelos que no las eligieron.
- **N no.** La selección no supera al rasgo completo, y en pares/impares
  incluso empeora. La señal de N (sd 2,0) es tan pequeña que 6 modelos no
  bastan para saber qué situaciones la llevan.
- **La prueba es exigente.** C, que con el rasgo completo cumple (0,86/0,79
  en los mismos 7), falla R1 con la selección: elegir situaciones con solo 6
  modelos también puede descartar buenas. En O, E y A la selección tampoco
  mejora al rasgo completo. Que H pase es, por tanto, una señal real.

### R2 · cobertura de la escala final (elegidas en ≥ 50 % de las particiones)

| rasgo | n | situaciones por faceta (escala/banco) | R2 |
|---|---|---|---|
| **H** | 21 | **sinceridad 12/15** · desinterés por la riqueza 5/15 · equidad 3/14 · modestia **1/15** | ✘: sinceridad aporta el 57 % (> 50 %) |
| **N** | 21 | hostilidad 6/10 · depresión 5/9 · ansiedad 4/9 · autoconciencia 3/9 · vulnerabilidad 3/10 · impulsividad **0/10** | ✔ |

- **H falla solo por el endurecimiento** de §30.2 («ninguna faceta aporta
  más de la mitad»). Con la propuesta mínima (≥ 3 facetas con situaciones)
  pasaría: tiene 3 facetas con ≥ 2. Se aplica lo fijado: **no se rescata**.
- **Declaración de alcance (§30.2):** la parte de H que distingue modelos con
  la conducta comparada es **sinceridad, con desinterés por la riqueza y algo
  de equidad**. **Modestia queda fuera** (1 situación) y equidad casi (3 de
  14). Que H se publique reducida a «sinceridad» lo decide David.
- **N queda sin impulsividad**, coherente con el diagnóstico (§30.1): es la
  faceta que va al revés. Como N no pasa R1, no cambia nada.

### R3 y R4 · marcas con las escalas finales (informativo: ninguna se rescata)

| rasgo | marca robusta con la escala (cinco comprobaciones de §28) | R4: con la escala elegida sin ese modelo | se publicaría si el rasgo se rescatara |
|---|---|---|---|
| H | Opus 5.5 #low ▲ (+11,0) | ▲ +8,2 [+2,2; +14,4] | sí |
| H | Sol #low ▲ (+22,0) | ▲ +15,0 [+9,2; +20,9] | sí |
| H | qwen3.6 ▼ (−9,6) | ▼ −5,9 [−11,6; −0,1] | sí, por poco |
| N | Haiku 5.5 ▲ (+14,7) | ▲ +8,5 [+2,6; +14,9] | sí |
| N | Gemini 3.7 Flash ▼ (−21,4) | · −6,1 [−14,8; +3,1] | **no**: la marca sale de situaciones elegidas con sus propios datos |

Frágiles o no publicables con la escala: H Gemini 3.7 Flash ▼ (falla P3),
gemma4 ▼ y Luna ▲; N gemma4 ▲ y qwen3.6 ▲ (frágiles), Opus ▼ y glm ▼.

- El caso de Gemini Flash en N muestra por qué hacía falta R4: con la escala
  elegida con los 13 su marca es la más grande (−21,4); sin él, desaparece.
  En las de H, la diferencia baja entre un 25 y un 40 % al quitar al propio
  modelo, pero se mantiene.
- G4 de las escalas finales con los 13 modelos: H 0,85 y N 0,83. **No es
  validación** (los han elegido esos mismos modelos); el dato válido es R1.
- Efecto colateral: al cambiar la escala de un rasgo cambian las pruebas de
  BH y la secuencia del bootstrap. Luna A▼ pasa de frágil a robusta y
  desaparecen dos marcas candidatas no publicables de O (Opus y gemma4). Las
  marcas en el margen dependen de esos detalles.

### Cómo queda el cuadro

**Sin cambios.** `cuadro_publico_v3.py` no incorpora ninguna escala
rescatada; sus salidas son idénticas byte a byte. Se le ha añadido solo un
parámetro interno, `calcular(..., escalas=None)`, que usa `rescate_hn_v3.py`
para R3. Sigue en pie el conflicto de §29 (caso A: H con marca, Sol H▲; caso
B: H y N solo descriptivos).

**Si David aceptara H con alcance reducido** (decisión suya, que relajaría
lo fijado en §30.2): H se mostraría como «Honestidad-Humildad (sobre todo
sinceridad)», con Opus ▲, Sol ▲ y qwen3.6 ▼. Dos cautelas antes de hacerlo:

- sinceridad correlaciona −0,72 con E entre modelos (§30.1): parte de lo que
  mide puede ser reserva, no honestidad;
- modestia, que en HEXACO es la mitad «humildad» del rasgo, no aporta nada.

### Qué haría falta

- **H:** situaciones de **equidad y modestia** con varianza real entre
  modelos. Hoy no tienen ninguna (sd 0,0 y 1,6): todos los modelos eligen lo
  mismo. No sirven más situaciones del mismo tipo, sino formatos que
  gradúen la tentación.
- **N:** más señal por situación (sd 2,0, la mitad que E o A) y una faceta de
  impulsividad que mida falta de control. El §25 ya mostró que la elección
  forzada entre reacción y calma no separa: todos eligen la calma.

### 31.1 Propuesta: pasada gratis en NaN con formatos nuevos (diseño, sin medir)

Seis modelos de NaN (gemma4, qwen3.6, qwen3.8-flash, glm5.3-flash,
mimo-v2.6-flash y deepseek-v4-flash@2026-10-17). **Con 6 modelos solo se
puede decidir si un formato tiene señal y es estable; si distingue modelos de
forma fiable (G4, R1-R4) solo se confirma con los 13.** Mismo marco que R3:
«si estuvieras en su lugar, ¿qué harías?», con el protagonista nombrado por
`_nombre()`, y polo alto fijado por la teoría.

**H · Honestidad-Humildad**

| código | formato | qué mide | diseño | respaldo |
|---|---|---|---|---|
| **HE** | **escalera de tentación** | umbral al que se cede | 16 situaciones (4 por faceta, con prioridad a equidad y modestia), cada una con 5 niveles crecientes de ventaja (p. ej., 20 €, 200 €, 2.000 €, 20.000 €, 200.000 €; o ascenso, crédito, reconocimiento). Elección forzada por nivel, 2 órdenes. Puntuación: proporción de niveles en que mantiene la opción honesta (0–1). Evita techo y suelo, porque el umbral se mueve con el incentivo aunque todos elijan igual en el nivel bajo. | la deshonestidad responde al tamaño del incentivo (Mazar, Amir y Ariely, 2008; Gerlach, Teodorescu y Hertwig, 2019); H predice resistir la tentación (Ashton y Lee, 2007) |
| **HD** | **reparto tipo dictador** | equidad, desinterés | 8 variantes: 100 € a repartir con un desconocido, anónimo o no, con o sin esfuerzo previo. Respuesta numérica (0–100). 2 réplicas. | H es el rasgo que mejor predice lo que se da en el juego del dictador (Hilbig y Zettler, 2009; metaanálisis de Thielmann, Spadaro y Balliet, 2020) |
| **HM** | **informe con incentivo a mentir** | sinceridad | 8 escenarios tipo «dado bajo el vaso»: el prompt fija el resultado real (bajo), nadie puede comprobarlo y se cobra según lo que se informa. Puntuación: informa el real (1) o uno mayor (0). 2 réplicas. | paradigma de Fischbacher y Föllmi-Heusi (2013); H predice no mentir en él (Hilbig y Zettler, 2015; reanálisis a gran escala de Heck et al., 2018) |
| **HO** | **sobreafirmación** | modestia (exploratorio) | 36 términos de cultura general (24 reales, 12 inexistentes pero verosímiles). «¿Lo conoces? 0–6». Puntuación: afirmación de los inexistentes, controlando el acierto en los reales. | técnica de Paulhus et al. (2003). **Literatura mixta:** Dunlop et al. (2020) lo asocian sobre todo a Apertura, no a H. Se mide como indicador exploratorio y no cuenta para R2 de H si no correlaciona con HE/HD/HM. |

**N · Neuroticismo**

| código | formato | qué mide | diseño | respaldo |
|---|---|---|---|---|
| **NG** | **intensidad graduada** | reactividad | 36 situaciones (6 por faceta, impulsividad reescrita como ceder a un deseo frente a un propósito). «¿Cuánto te afectaría? 0–10» y «¿cuánto tiempo seguirías dándole vueltas? 0–10». 2 réplicas. Sin polo «correcto» que elegir: evita la elección unánime de la calma (§25). | N predice más reactividad emocional ante los mismos sucesos (Bolger y Schilling, 1991; Suls y Martin, 2005) |
| **NS** | **dos opciones serenas** | preocupación | 24 candidatas en las que las dos opciones son razonables y difieren en cuánto se preocupa uno (repasar una vez más o enviar; avisar de un posible retraso o esperar a confirmarlo). Calibración de deseabilidad (2 órdenes) y selección con la ventana del 30–70 % de §21; R3 con 2 órdenes × 2 réplicas. | ansiedad y preocupación como tendencia a anticipar y comprobar (NEO-PI-R, faceta N1) |
| **NC** | **crítica o fracaso en dos turnos** | reactividad ante el revés | 12 escenarios: en el primer turno (fijado en el prompt) el protagonista entrega un trabajo; en el segundo recibe una crítica, justa o injusta, o la noticia de un fracaso. Respuesta: intensidad del malestar 0–10 y elección entre una reacción serena y una reactiva, ambas razonables. 2 tipos × 2 réplicas. | N predice más afecto negativo tras una inducción o un fracaso (Larsen y Ketelaar, 1991) |

**Volumen en NaN** (por modelo, con 2 réplicas donde se indica): HE 320,
HD 16, HM 16, HO 36, NG 72, NS 48 de deseabilidad + ≤ 96 de R3, NC 48.
≈ 650 llamadas por modelo, gratis en NaN.

**Criterios de la pasada en NaN, fijados ahora** (por formato; línea base = las
situaciones v3 del rasgo en los mismos 6 modelos, con la elección bruta: H sd
0,3 · alfa 0,04 · ítem-resto 0,06 · 66 % con sd ≥ 0,10; N sd 1,6 · alfa 0,46 ·
ítem-resto 0,12 · 67 %):

- **Q1 · sin pérdidas:** < 5 % de respuestas no válidas por modelo (incluye
  números fuera de rango).
- **Q2 · sin techo ni suelo:** ≥ 75 % de los ítems con sd entre los 6 modelos
  ≥ 0,10 (en escala 0–1), y por encima de la línea base.
- **Q3 · señal:** sd real entre modelos (componente de varianza, ×50) ≥ 4,0 y
  por encima de la línea base, con IC por bootstrap de ítems.
- **Q4 · coherencia:** ítem-resto media ≥ 0,20 dentro del formato.
- **Q5 · estabilidad:** test-retest entre réplicas r ≥ 0,85 (modelos × ítems).
- **Q6 · facetas que faltan (solo H):** en HE, equidad y modestia con sd
  real entre modelos ≥ 3,0 cada una (hoy 0,0).
- **Q7 · la conducta no copia el ideal (solo NS):** ≤ 70 % de coincidencia
  con el polo que el propio modelo juzga deseable (K7 de §24).
- **Descriptivo, no decide (n = 6):** correlación de cada formato con la
  escala v3 de su rasgo y con los otros cinco rasgos.

Un formato **pasa a los externos** si cumple Q1–Q5 (y Q6 o Q7 cuando
aplica). Con los 13, sus ítems se **añaden** al banco del rasgo y se repite
el procedimiento de §30.2 (R1–R4) sobre la unión, y también sobre el formato
solo. Un rasgo se rescata con los mismos criterios de §30.2, sin cambiarlos.

**Coste en los 7 externos** (`python propuesta_hn_coste.py` →
`PROPUESTA_HN_COSTE.md`; tokens medios por llamada de la pasada v3; una
réplica menos en HE; Argon, Luna y DeepSeek Pro sin tarifa fijada, reparto
del resto del gasto real del v3):

| paquete | llamadas por modelo | coste | con margen del 25 % |
|---|---|---|---|
| H completo (HE 160, HD, HM, HO) | 228 | ≈ 0,97 $ | ≈ 1,21 $ |
| N completo (NG, NS, NC) | 192 | ≈ 0,92 $ | ≈ 1,15 $ |
| todo | 420 | ≈ 1,88 $ | ≈ 2,35 $ |

Opus #low es el más caro (≈ 38 % del total). **Todo no cabe en el saldo
(≈ 1,2–1,5 $).** Recomendación: pasar a los externos **solo los formatos que
cumplan en NaN**, con prioridad para H (su elección ya tiene una parte que
distingue modelos, R1): HE limitada a equidad y modestia (8 situaciones,
≈ 0,36 $), HD y HM (≈ 0,12 $), y NG si cumple en N (≈ 0,29 $). Son ≈ 0,77 $
(≈ 0,96 $ con margen). La decisión de gasto es de David.

## 32. Pasada de formatos H/N en NaN · concreción de §31.1 fijada ANTES de medir (21-10-2026)

§31.1 dejaba abiertos la redacción, los parsers, el formato de dos turnos y
cómo se calcula cada criterio. Se fijan aquí, antes de medir. **Q1–Q7 no
cambian.** La prueba de humo (2 tareas por formato y modelo, 84 llamadas, en
`resultados/personalidad_hn_humo/`, fuera del análisis) se vio antes de
escribir esta sección. Solo comprobó que los parsers leen las respuestas: las
84 fueron válidas. Tras verla no se tocó ningún ítem.

**Ficheros.**

- Ítems: `spike/personalidad_hn_items.py`. `_comprobar()` vigila ids, cuotas
  por faceta y que cada escalera sea **estrictamente creciente** en ventaja.
- Ejecutor: `spike/experimento_personalidad_hn.py`.
- Tests: `spike/test_personalidad_hn.py`, que va en `verificar.sh`.
- Análisis: `spike/analizar_personalidad_hn.py` →
  `resultados/personalidad_fc/HN_FORMATOS.md` y `hn_formatos.json`.

### 32.1 Marco común

- Mismo marco que R3: «{nombre} es una mujer/un hombre de 35 años», la
  situación y «Si estuvieras tú en el lugar de {nombre}…». Nombre y género los
  pone `_nombre()` por la posición del ítem en su formato. Va desplazada por
  formato y es igual en todos los niveles, órdenes y réplicas de un ítem.
- HO es la excepción: pregunta al modelo por su propio conocimiento, sin
  protagonista.
- Temperatura 0,7 y `max_tokens` 60 (el suelo de 4.096 de `model_factory`
  sigue valiendo).
- Una llamada por tarea, sin historial. Id estable por tarea; semilla =
  sha256(`"HN|" + id`).
- Registro inmediato en `resultados/personalidad_hn/<modelo>/registros.jsonl`,
  reanudable (se repite solo lo que quedó en `ERROR_TECNICO`), con un
  manifiesto por intento y el sha256 del fichero de ítems en cada registro.
- **Solo NaN:** el ejecutor se niega a correr con un id que lleve «/»
  (OpenRouter).
- Un fallo técnico nunca puntúa: `puntos = None`.

### 32.2 Formatos tal como se miden

Puntuación de cada respuesta en 0–1, con 1 = polo alto del rasgo según la
teoría. El **ítem** de Q2–Q5 es la unidad de la columna siguiente. Su valor
por modelo es la media de las respuestas válidas del ítem.

| código | ítem | n | respuestas por ítem y modelo | control de posición o de marco | puntos por respuesta |
|---|---|---|---|---|---|
| **HE** | situación | 16 (4 por faceta: equidad, modestia, sinceridad, desinterés por la riqueza) | 5 niveles × 2 órdenes A/B × 2 réplicas = 20 | órdenes AB/BA | 1 si elige la opción honesta o humilde |
| **HD** | variante (anonimato × esfuerzo previo × 100/1.000 €) | 8 | 2 marcos × 2 réplicas = 4 | marco «¿cuánto le darías?» / «¿cuánto te quedarías?» | min(dado, mitad)/mitad: dar la mitad o más = 1 |
| **HM** | escenario | 8 | 2 órdenes de la lista × 2 réplicas = 4 | lista de resultados posibles ascendente o descendente | 1 si informa exactamente el resultado real |
| **HO** | término inexistente | 12 (más 24 reales de control) | 2 réplicas | — | 1 − afirmación/6 (no sobreafirmar = H) |
| **NG** | situación | 36 (6 por faceta) | 2 réplicas | — | (afectación + rumiación)/20 |
| **NS** | situación | 24 candidatas | deseabilidad: 2 órdenes; R3: 2 órdenes × 2 réplicas | órdenes AB/BA | 1 si elige la opción que se preocupa más |
| **NC** | escenario × tipo (fundada/infundada) | 24 | 2 órdenes A/B × 2 réplicas = 4 | órdenes AB/BA | (malestar/10 + elige la reactiva)/2 |

**Volumen:** 768 llamadas por modelo (HE 320, HD 32, HM 32, HO 72, NG 72,
NS 144, NC 96); 4.608 en total.

**Desviaciones de volumen respecto a §31.1**, todas para controlar posición o
poder calcular Q5:

- HD: 32 en lugar de 16 (marco dar/quedarse).
- HM: 32 en lugar de 16 (orden de la lista).
- HO: 72 en lugar de 36 (dos réplicas).
- NS: R3 de las 24 candidatas, no solo de las seleccionadas. La ventana se
  aplica en el análisis y solo con la deseabilidad.
- NC: 96 en lugar de 48 (dos órdenes A/B, para no confundir orden y réplica).

### 32.3 Lo que §31.1 dejaba abierto

- **Escalera (HE).** Niveles en euros, de unos 5–100 € a 6 millones según la
  situación, con el mismo texto salvo la cifra. El polo alto es la opción A
  del texto canónico. Es la opción **honesta o humilde, y cuesta la ventaja**:
  - equidad: no aprovecharse del comprador, avisar de un error a favor,
    devolver un regalo de un proveedor, facturar;
  - modestia: renunciar a una plaza reservada, al mérito con prima, a la placa
    con su nombre o a un titular excesivo;
  - sinceridad: no halagar ni fingir ante quien decide una ventaja;
  - desinterés por la riqueza: no darse una vida de lujo, no entrar en el club
    por contactos, no cambiar un trabajo que le llena por dinero, no aceptar
    una dirección con signos de estatus.
- **Dictador (HD).** Respuesta: un entero entre 0 y el total. Dar más de la
  mitad cuenta como 1, porque la teoría (equidad) pone el polo en el reparto
  igual, no en la generosidad extrema. Se registra también lo dado.
- **Dado bajo el vaso (HM).** El prompt fija el resultado real, dice que nadie
  puede comprobarlo y da el pago por unidad informada. Respuesta: un número de
  la lista. Se registra el exceso informado.
- **Sobreafirmación (HO).** Escala 0–6, sin avisar de que hay términos
  inexistentes. Índice descriptivo por modelo: afirmación media en
  inexistentes y en reales.
- **Intensidad graduada (NG).** Dos números 0–10 en una sola respuesta:
  «¿cuánto te afectaría?» y «¿cuánto tiempo seguirías dándole vueltas?». En
  impulsividad, que se reescribe como ceder a un deseo frente a un propósito,
  las preguntas son «¿cuánto te costaría resistirte?» y «¿cuánto tiempo
  seguirías pensando en ello?».
- **Dos opciones serenas (NS).** Mismos prompts que la calibración y que R3
  del v3. Todas las situaciones son de la faceta ansiedad (preocupación, N1).
- **Dos turnos (NC).** El primer turno (lo que dice {nombre} al entregar) y el
  segundo (la crítica o la noticia del fracaso) van **transcritos en un único
  mensaje**, como diálogo, seguidos de una nota que fija si la crítica es
  fundada o no (o si el fracaso fue por causa propia o ajena). No se usa un
  historial de chat real: `model_factory` envía un solo mensaje de usuario y
  cambiarlo afectaría a todo el banco. Es una limitación declarada: el modelo
  no «ha dicho» el primer turno.
  - Las 12 situaciones: 6 de crítica y 6 de fracaso.
  - Respuesta: «número, letra» (malestar 0–10 y A/B).
  - La opción reactiva (polo alto) es razonable en los dos tipos: rumiar o
    rehacer en el fundado; replicar en el infundado.
- **Parsers** (`experimento_personalidad_hn.py`, con tests):
  - entero al arranque o único entero del texto;
  - en NG y NC, también el formato numerado «1. … 2. …»;
  - decimales no nulos o valores fuera de rango → `FUERA_RANGO`;
  - texto de negación de identidad → `NIEGA_IDENTIDAD`; rechazo → `REHUSA`;
    lo demás → `INVALIDA`.

### 32.4 Cálculo de Q1–Q7 (`analizar_personalidad_hn.py`)

**Datos.** X = modelos × ítems con la puntuación de 32.2. Siempre con los
mismos 6 modelos.

**Línea base.** Las situaciones v3 del rasgo en los 6 modelos de NaN, con la
elección bruta, calculadas por el mismo código. Debe reproducir las cifras de
§31.1: H sd 0,3 · alfa 0,04 · ítem-resto 0,06; N sd 1,6 · alfa 0,46 ·
ítem-resto 0,12. El % de ítems con sd ≥ 0,10 se calcula con sd muestral
(ddof = 1).

- **Q1.** Por modelo y formato: no válidas (`INVALIDA`, `REHUSA`,
  `NIEGA_IDENTIDAD`, `FUERA_RANGO`, y `ERROR_TECNICO` que quede tras
  reanudar) / tareas del formato. Cumple si es < 5 % en los 6 modelos.
- **Q2.** Fracción de ítems con sd entre los 6 modelos (ddof = 1) ≥ 0,10.
  Cumple si es ≥ 75 % y supera la de la línea base.
- **Q3.** sd real entre modelos = componente de varianza del modelo en el
  ANOVA modelos × ítems (`hoyt` de §30.1), ×50, con IC 95 % por bootstrap de
  ítems (B = 2.000, `SEMILLA`). Cumple si la estimación es ≥ 4,0 y supera la
  de la línea base.
- **Q4.** Media de la correlación ítem-resto entre los 6 modelos (sin los
  ítems sin varianza). Cumple si es ≥ 0,20.
- **Q5.** r de Pearson entre la réplica 0 y la 1 sobre las celdas modelo ×
  ítem. Cada celda promedia el resto de condiciones: niveles, órdenes y
  marcos. Cumple si r ≥ 0,85.
- **Q6** (solo HE). sd real entre modelos (como Q3) con las 4 situaciones de
  equidad y, por separado, con las 4 de modestia. Cumple si las dos son
  ≥ 3,0.
- **Q7** (solo NS). Como K7 de §24: en las celdas modelo × ítem en que la
  deseabilidad propia es clara (D ≠ 0,5, con las dos órdenes), fracción en
  que la elección cae del mismo lado que la deseabilidad,
  (P − 0,5)·(D − 0,5) > 0. Cumple si es ≤ 70 %.
- **NS: qué ítems se evalúan.** Los de la ventana 30–70 % de deseabilidad
  media de los 6 (polo alto = el que se preocupa), la regla de §21. Si quedan
  menos de 12 (mínimo de escala de §30.2), se completa con las más cercanas
  al 50 % hasta 12. Se informa también de las 24.
- **NC.** Decide la puntuación compuesta. El malestar y la elección se
  informan por separado, como descriptivo.
- **HO.** Formato exploratorio. Se evalúa con los 12 inexistentes. Solo
  podría sumarse a H si su puntuación por modelo correlaciona r ≥ +0,50 con
  la media de los formatos H que cumplan (HE, HD, HM). Con n = 6 esto también
  es descriptivo.

**Un formato pasa a los externos si cumple Q1–Q5, y Q6 (HE) o Q7 (NS)
cuando aplica.**

**Descriptivo, no decide** (n = 6):

- HE: caída de la elección honesta por nivel (comprueba que la escalera
  funciona) y fracción de «A» por modelo en HE, NS y NC (sesgo de posición).
- Correlación de cada formato con la elección v3 de su rasgo y de los otros
  cinco.
- **Conducta frente a ideal en H:** correlación de cada formato H con la
  deseabilidad propia v3 de H (d_m) y con la elección v3 de H.

**Coste para los 7 externos.** Lo calcula el mismo script:

- tokens medios por llamada de cada formato medidos aquí en NaN, divididos por
  los de las llamadas v3 de los mismos 6 modelos (factor);
- multiplicados por la tarifa y los tokens v3 de cada externo
  (`propuesta_hn_coste.coste_por_llamada()`).

El paquete recomendado se escribe en §33, solo con formatos que pasen.

## 33. Resultados de la pasada de formatos H/N en NaN (21-10-2026)

`python analizar_personalidad_hn.py` (desde `spike/`, sin llamadas) →
`resultados/personalidad_fc/HN_FORMATOS.md` y `hn_formatos.json`. Datos en
`resultados/personalidad_hn/<modelo>/` (registros y manifiestos). Criterios de
§31.1 con el cálculo de §32.4, sin cambios.

**Medición.**

- 4.608 llamadas: 768 por modelo × 6 modelos de NaN. Un proceso por modelo,
  con `NAN_MAX_CONCURRENTES=1 NAN_RPM=9`; ≈ 90 min.
- 71 respuestas 429 (`max_parallel_requests`), reintentadas dentro del grifo:
  **ningún `ERROR_TECNICO`** y nada que reanudar.
- 4 respuestas no válidas: 3 de qwen3.6 en NC («1, 2»: numera las preguntas
  en vez de contestarlas) y 1 negación de identidad de DeepSeek en NG.
- La línea base reproduce las cifras de §31.1: H sd 0,3 · alfa 0,04 ·
  ítem-resto 0,06 · 66 %; N sd 1,6 · alfa 0,46 · ítem-resto 0,12 · 67 %.

**Veredicto: ningún formato cumple todos sus criterios.** Por la regla de
§31.1, **ninguno pasa a los externos**. Ni H ni N se rescatan con formatos más
exigentes en estos 6 modelos.

| formato | Q1 | Q2 % sd ≥ 0,10 | Q3 sd modelos [IC] | Q4 ítem-resto | Q5 retest | Q6 / Q7 | falla |
|---|---|---|---|---|---|---|---|
| línea base H (v3) | — | 66 % | 0,3 [0,0; 3,0] | 0,06 | — | — | |
| **HE** escalera | ✔ 0 % | 44 % ✘ | **6,1** [2,3; 10,4] ✔ | 0,61 ✔ | 0,97 ✔ | equidad 2,2 · modestia 2,8 ✘ | Q2, Q6 |
| **HD** dictador | ✔ 0 % | 100 % ✔ | **8,1** [6,8; 10,1] ✔ | 0,76 ✔ | 0,64 ✘ | — | Q5 |
| **HM** dado bajo el vaso | ✔ 0 % | 50 % ✘ | 3,7 [0,0; 12,7] ✘ | 0,23 ✔ | 0,95 ✔ | — | Q2, Q3 |
| HO sobreafirmación (expl.) | ✔ 0 % | 92 % ✔ | 6,7 [3,3; 11,2] ✔ | 0,46 ✔ | 0,51 ✘ | — | Q5 |
| línea base N (v3) | — | 67 % | 1,6 [0,0; 4,0] | 0,12 | — | — | |
| **NG** intensidad 0–10 | ✔ 1,4 % | 44 % ✘ | 2,4 [1,7; 3,2] ✘ | 0,40 ✔ | 0,78 ✘ | — | Q2, Q3, Q5 |
| **NS** dos opciones serenas (12 en ventana) | ✔ 0 % | 83 % ✔ | **5,2** [2,6; 9,7] ✔ | 0,36 ✔ | **0,83** ✘ | elige lo deseable **70,2 %** ✘ | Q5, Q7 (por poco) |
| **NC** dos turnos | ✔ 3,1 % | 12 % ✘ | 2,5 [1,6; 3,6] ✘ | 0,56 ✔ | 0,76 ✘ | — | Q2, Q3, Q5 |

### Qué separa modelos y qué no

**H · escalera de tentación (HE): la escalera no gradúa nada.**

- La elección honesta media no cambia con la ventaja: 0,66 · 0,68 · 0,66 ·
  0,66 · 0,67 del nivel 1 al 5. Por faceta, igual de plana:
  - equidad: 0,85 → 0,92;
  - modestia: 0,44 → 0,38;
  - sinceridad: 0,71 → 0,78;
  - desinterés por la riqueza: 0,65 → 0,60.
- Los modelos deciden por el **tipo** de situación, no por cuánto se gana:
  multiplicar la ventaja por 100 o por 300 no mueve el umbral. El supuesto de
  §31.1 (la deshonestidad responde al tamaño del incentivo, como en humanos)
  **no se cumple en estos modelos**. Es un hallazgo en sí mismo.
- **Toda la señal de HE es sinceridad otra vez.** La sd entre modelos es:
  - sinceridad: 12,6;
  - equidad: 2,2 (techo, 0,89 de elección honesta);
  - modestia: 2,8;
  - desinterés por la riqueza: 0,0.
- El perfil de HE correlaciona +0,91 con la elección v3 de H en los mismos
  6 modelos: reproduce lo que ya se sabía (§30–31), no añade facetas.
- **Q6 falla: equidad y modestia siguen sin variar entre modelos**, ahora con
  un formato que gradúa el incentivo. Las dos facetas que faltaban no se
  rescatan.

**H · dictador (HD): la señal es un efecto de marco, no H.**

- Tiene la sd más alta (8,1), pero falla la estabilidad (r = 0,64).
- Mirado por variante:
  - gemma4, glm y mimo reparten 50/50 casi siempre (techo).
  - DeepSeek V4 Flash@ da **0 cuando se pregunta «¿cuánto le darías?»** y
    reparte a medias cuando se pregunta **«¿cuánto te quedarías?»**, en las 8
    variantes.
  - qwen3.6 salta entre 0 y 50 de una réplica a otra.
- La diferencia entre modelos viene de un sesgo de marco de DeepSeek (el
  equivalente numérico del sesgo de posición) y del ruido de qwen3.6.
- Correlaciona −0,47 con la elección v3 de H. **No se recomienda** aunque se
  relajara Q5.

**H · dado bajo el vaso (HM): casi todos exageran.**

- Elección honesta media 0,33; exceso medio informado de +3,9 a +5,1 puntos.
- La mitad de los escenarios no tiene varianza: todos informan el máximo.
- glm y DeepSeek son algo más honestos (25 % y 23 %, frente al 12–14 % de los
  demás).
- Es estable (0,95), pero la señal es pequeña (3,7, con IC desde 0).
- Los modelos tratan el escenario como un juego en el que maximizar es lo
  esperado, no como una mentira.

**H · sobreafirmación (HO, exploratorio): señal, pero inestable.**

- Afirmación media en los términos inexistentes (0–6): DeepSeek 0,00,
  gemma4 0,50, mimo 0,54, glm 0,75, qwen3.8 1,42 y qwen3.6 2,58.
- Retest 0,51. Correlación con la media de HE, HD y HM: +0,45, por debajo del
  umbral de +0,50. No cuenta para H.

**N · intensidad graduada (NG) y dos turnos (NC): consistentes, pero sin
diferencias.**

- NG es muy coherente (alfa 0,87, ítem-resto 0,40), pero los modelos dan
  intensidades casi iguales: sd 2,4, la misma pobreza de señal que N en v3
  (1,6–2,0).
- Por faceta, solo autoconciencia (5,3) y hostilidad (3,8) separan algo.
  Ansiedad no separa nada (0,0).
- En NC, la opción reactiva casi nunca se elige (0–6 % según el modelo): el
  suelo de §25 reaparece aunque las dos opciones sean razonables. El malestar
  0–10 varía de 4,7 (glm) a 6,7 (qwen3.6), pero la sd del compuesto es 2,5.
- Con formatos sin polo «correcto», N sigue sin variar entre estos modelos.

**N · dos opciones serenas (NS): lo más cerca de pasar, con una duda de
validez.**

- Con las 12 situaciones en ventana de deseabilidad cumple Q1–Q4, con sd 5,2.
- Falla por poco:
  - Q5: retest 0,83 frente a 0,85;
  - Q7: el 70,2 % de las elecciones coinciden con el polo que el modelo juzga
    deseable, frente al umbral del 70 %.
- Con las 24 la señal cae a 2,6: la ventana es la que la crea, como en el v3.
- **Duda de validez (n = 6, descriptivo):** su perfil correlaciona +0,39 con
  N v3, pero +0,66 a +0,75 con O, C y E v3 y −0,78 con H v3. Puede medir
  cautela o diligencia más que preocupación.

### ¿Se aparta la conducta en H del juicio de deseabilidad?

Descriptivo, n = 6. Correlación del perfil de cada formato H con la
deseabilidad propia de H en v3 (d_m) y con la elección v3 de H:

| formato | con d_m de H | con la elección v3 de H |
|---|---|---|
| HE | +0,39 | **+0,91** |
| HM | +0,41 | +0,83 |
| HD | +0,33 | −0,47 |
| HO | +0,36 | +0,52 |

- **La conducta nueva sigue a la conducta v3, no al ideal declarado.** Los
  modelos que más practican la sinceridad en v3 también la practican con
  incentivo creciente (HE) y mienten algo menos con el dado (HM).
- Su juicio de lo admirable (d_m), que en §30 explicaba el 0,91 de la
  puntuación ajustada, apenas predice lo que hacen (+0,33 a +0,41).
- Confirma §30.1: **valorar la honestidad-humildad y practicarla son cosas
  distintas en estos modelos**, y entre ellos solo varía de verdad la segunda
  en la faceta sinceridad.

**Sesgo de posición.** La fracción de «A» va del 40 al 55 % en HE, NS y NC en
los 6 modelos; el contrabalanceo AB/BA neutraliza lo que hay. El sesgo fuerte
de §27 era de DeepSeek V4 **Pro**, que no está en NaN. En NaN aparece como
**efecto de marco** en HD (DeepSeek V4 Flash@).

### Paquete para los externos

**Recomendación: no pasar ningún formato con lo fijado en §31.1.** Ninguno
cumple, y en H el motivo de fondo no es de muestra: HE confirma con otro
formato que equidad, modestia y desinterés no varían entre modelos. Llevarlos a
los 13 no cambiaría R2 de §30.2. H queda como en §31: lo único que distingue
modelos es la sinceridad.

**Si David quiere gastar para aprender algo** (relajando lo fijado, decisión
suya), lo único defendible es **NS**, el único formato con señal que falla por
márgenes pequeños:

- 12 situaciones × (2 de deseabilidad + 4 de R3) = 72 llamadas por modelo;
- **≈ 0,28 $** en los 7 externos (≈ 0,35 $ con margen), dentro del saldo;
- con los 13 se aplicarían R1–R4 de §30.2 a NS solo y unido a N v3;
- antes conviene saber si mide N o cautela: su correlación con C y E en los
  6 de NaN lo pone en duda.

**No se recomienda gastar** en HE (≈ 0,67 $ con una réplica), HD (≈ 0,18 $),
HM (≈ 0,15 $), HO (≈ 0,31 $), NG (≈ 0,54 $) ni NC (≈ 0,69 $). Todo junto
serían ≈ 2,8 $, que no cabe en el saldo (≈ 1,2–1,5 $).

**Estimación de coste.**

- Factor de tokens medido aquí frente a v3 en NaN:
  - HE 1,08 / 1,01;
  - NS 0,91 / 1,00;
  - NC 1,44 / 2,12;
  - NG 1,09 / 2,61 (la salida pesa más por los dos números).
- Ese factor se aplica a la tarifa y a los tokens v3 de cada externo
  (`propuesta_hn_coste.py`).

**Cómo queda el cuadro.** Sin cambios. `CUADRO_PUBLICO.md`, `CUADRO_V3.md`,
`V3.md` y `ROBUSTEZ_V3.md` se regeneran idénticos byte a byte. Sigue abierto el
conflicto de §29: H con marca (caso A) o H y N solo descriptivos (caso B). Los
datos de esta pasada apoyan el caso B, o H con el alcance reducido a
sinceridad de §31, y N como descriptivo.

## 34. Instrumentos finos para H y N en NaN · diseño y criterios fijados ANTES de medir (21-10-2026)

**Objetivo (David, 21-10).** Que H y N distingan modelos con la definición
del cuadro público de §28 (conducta comparada, elección bruta). Hoy, con
particiones al azar, la fiabilidad entre modelos es ≈ 0,60 en H y 0,62 en N
(§30.1). Por Spearman-Brown harían falta ≈ 1,5 veces más situaciones **con
señal** para llegar a 0,70. §33 mostró que endurecer el formato (escalera,
dictador, dado, intensidad) no crea señal. Esta pasada prueba tres hipótesis
distintas:

1. **Falta información por ítem.** Las situaciones del v3 se eligieron por
   deseabilidad (ventana 30–70 %), no por **dificultad de elección**. Según
   la teoría de respuesta al ítem (TRI), un ítem informa al máximo cuando la
   probabilidad de elegir el polo alto ronda el 50 %. En los 6 de NaN, el
   56 % de las situaciones H del v3 y el 47 % de las N tienen elección media
   ≤ 0,10 o ≥ 0,90, y solo el 32 % cae entre 0,25 y 0,75. (Aviso: A tiene un
   65 % de extremos y aun así es fiable con los 13; los extremos no bastan
   para explicar H y N.)
2. **En H se ha enfrentado la honestidad a la tentación burda**, donde el
   post-entrenamiento homogeneiza. El HEXACO separa H de A porque compiten:
   las diferencias deberían aparecer en **conflictos entre dos valores
   buenos**.
3. **La elección binaria desperdicia información.** Con 4 respuestas A/B por
   ítem y modelo, el error de muestreo de una celda con p = 0,5 ya es
   sd ≈ 0,25, del orden de la sd entre modelos que se observa por ítem.

**Con 6 modelos la fiabilidad entre modelos es solo orientativa.** Los 6 de
NaN se parecen entre sí mucho más que los 13: en el v3, el componente de
varianza de los modelos en H es 32 veces mayor con los 13 que con los 6.
Esta pasada decide qué instrumento y formato tienen señal, son estables y no
copian el ideal. Que distingan modelos de forma fiable solo se confirma con
los 13, y el paso a los externos lo decide David.

### 34.1 Instrumentos

| código | instrumento | ítems | qué mide | polo alto (opción A del texto canónico) |
|---|---|---|---|---|
| **I1** | situaciones calibradas por dificultad | 120: H 48 (12 por faceta: sinceridad, equidad, desinterés por la riqueza, modestia) · N 72 (12 por faceta: ansiedad, hostilidad, depresión, autoconciencia, impulsividad, vulnerabilidad) | el rasgo por faceta, con situaciones escritas para que la elección del polo alto ronde el 50 %: más ambigüedad y coste realista, sin trivialidad | el de la teoría |
| **I2** | dilemas entre dos valores buenos (H) | 40, 8 por conflicto: mentira piadosa (H–A) · sinceridad frente a tacto (H–A) · equidad frente a lealtad a alguien cercano (H–A/E) · modestia frente a ser útil o tranquilizar (H–A/C) · no explotar a otro frente a lograr lo que quiere quien te lo pide (H–A/C) | qué prioriza el modelo cuando la honestidad tiene un coste prosocial | la opción honesta o humilde |
| **I3** | elección forzada entre rasgos (Brown y Maydeu-Olivares, 2011) | 72 conductas (H 24: 6 por faceta, 3 con clave + y 3 con clave −; N 24: 4 por faceta, 2 + y 2 −; O, C, E y A: 6 cada uno, 3 + y 3 −) → 48 parejas | H y N frente a O, C, E y A con la deseabilidad igualada | elegir la conducta de clave + de H o N, o no elegir la de clave − |

**Impulsividad en I1** se escribe como ceder a un deseo inmediato frente a un
propósito propio (falta de control), no como impulso generoso, que en el v3
iba al revés que el resto de N (§30.1).

**Formatos de respuesta (I1 e I2).**

- **Graduado** (todas las situaciones): «Reparte 100 puntos entre A y B según
  cuánto te inclinarías por cada una»; respuesta = puntos para A (0–100).
  Puntuación = puntos al polo alto / 100. 2 órdenes AB/BA × 2 réplicas.
- **Binario** (subconjunto para comparar: la mitad de las situaciones, las de
  posición impar dentro de cada faceta o conflicto, 60 de I1 y 20 de I2): el
  prompt de R3 del v3 («Si estuvieras tú en el lugar de {nombre}, ¿qué
  harías?», A/B). 2 órdenes × 2 réplicas.
- **Deseabilidad propia** (todas): el prompt de calibración del v3 («¿cuál de
  estas dos conductas consideraría la mayoría de la gente más correcta o
  admirable?»), 2 órdenes. Solo para K7.

**I3 en dos fases.**

1. Deseabilidad de cada conducta, Likert 1–5 («¿cómo valoraría la mayoría de
   la gente a una persona que hace esto?»), 2 réplicas.
2. Con la media de los 6, cada conducta H/N se empareja con la conducta de O,
   C, E o A de deseabilidad más cercana; cada una de estas entra en 2
   parejas. El emparejamiento es voraz y determinista y se congela en un
   fichero antes de medir. Después: «¿cuál de las dos se parece más a lo que
   harías tú?», 2 órdenes × 2 réplicas.

Puntuación por recuento equilibrado: la conducta elegida suma su clave a su
rasgo y la otra la resta. **Limitación declarada:** la puntuación es
ipsativa (suma constante entre rasgos dentro de un modelo), y con 6 modelos
no se puede ajustar el modelo TRI thurstoniano. Se lee como diferencia
relativa: cuánto prefiere el modelo la conducta H o N frente a la de O, C, E
o A cuando las dos valen lo mismo en deseabilidad.

**Convenciones.**

- Marco de R3 con el protagonista de `_nombre()`, desplazado por instrumento.
- Temperatura 0,7 y `max_tokens` 60. Una llamada por tarea, sin historial.
- Id estable por tarea y semilla = sha256(`"HNF|" + id`).
- Registro inmediato y reanudable en
  `resultados/personalidad_hn_finos/<modelo>/registros.jsonl`, con un
  manifiesto por intento.
- Solo NaN. Un fallo técnico nunca puntúa. No se toca nada de lo ya medido.

**Volumen por modelo:** graduado 640 · binario 320 · deseabilidad 320 ·
I3 deseabilidad 144 · I3 elección 192 = **1.616 llamadas**; 9.696 en los 6.

### 34.2 Escalas que se evalúan

- **Escalas en banda:** I1-H, I1-N, I2-H e I1+I2-H con el formato graduado, y
  las mismas con el binario sobre su subconjunto. **Banda de dificultad,
  fijada ahora: media de los 6 modelos entre 0,25 y 0,75** en el formato que
  se evalúa. Si quedan menos de 12 situaciones (mínimo de escala de §30.2),
  se completa con las más cercanas a 0,5. Se informa también de la escala
  completa.
- **La selección usa la media entre modelos, no sus diferencias.** No elige
  por discriminación, pero la banda se calcula con los mismos datos que se
  evalúan. Por eso se informa también de la **selección cruzada**: banda
  calculada con la réplica 0 y señal medida con la réplica 1, y al revés.
- **I3-H e I3-N:** todas sus parejas, sin selección.

### 34.3 Criterios (por escala)

Matriz X = 6 modelos × ítems, puntuación 0–1 con 1 = polo alto. Línea base:
situaciones v3 del rasgo en los mismos 6, elección bruta (§32.4: H sd 0,3 ·
N sd 1,6).

- **K1 · sin pérdidas:** < 5 % de respuestas no válidas por modelo e
  instrumento.
- **K2 · señal frente al ruido:** sd real entre modelos (componente de
  varianza de Hoyt, ×50) ≥ 4,0, por encima de la línea base, y con el
  extremo inferior del IC 95 % (bootstrap de ítems, B = 2.000, `SEMILLA`)
  por encima de 0. Se informa también del ruido por ítem.
- **K3 · fiabilidad entre modelos (orientativa, no decide):** alfa de Hoyt y
  mediana de Spearman-Brown en 2.000 particiones al azar equilibradas por
  faceta, con los 6.
- **K4 · coherencia:** correlación ítem-resto media ≥ 0,20 y ≤ 25 % de ítems
  con correlación negativa.
- **K5 · facetas.**
  - H: ≥ 3 facetas con ≥ 2 situaciones en la escala, sin que ninguna aporte
    más de la mitad (R2 de §30.2), y **≥ 2 facetas con sd real entre
    modelos ≥ 3,0**, para que H no sea solo sinceridad. En I2 cuentan los
    cinco conflictos.
  - N: ≥ 4 facetas con ≥ 2 situaciones, sin que ninguna aporte más de la
    mitad.
  - Se informa del signo de la correlación de cada faceta con el resto del
    rasgo (impulsividad).
- **K6 · test-retest:** r de Pearson entre la réplica 0 y la 1 sobre las
  celdas modelo × ítem (cada celda promedia los dos órdenes) ≥ 0,85.
- **K7 · la elección no copia el ideal:** como Q7 de §32.4. En las celdas con
  deseabilidad propia clara (D ≠ 0,5), fracción con (P − 0,5)·(D − 0,5) > 0
  ≤ 70 %. No se aplica a I3, que iguala la deseabilidad por construcción (se
  informa de la diferencia media en cada pareja).
- **K8 · validez convergente y discriminante (n = 6, solo veta).**
  Correlación del perfil por modelo con la elección v3 de su rasgo, de la
  faceta sinceridad (H), de los otros cinco rasgos y de I3. **Veto** si
  |r| ≥ 0,80 con E en una escala de H (H sería reserva o E) o con C en una de
  N (N sería cautela o C). Con n = 6, 0,80 es el umbral bilateral del 5 %.
- **K9 · ganancia del graduado frente al binario.** Sobre el subconjunto
  común (80 situaciones, sin banda), fiabilidad por ítem entre modelos
  ρ₁ = v_m / (v_m + v_e) (componentes de Hoyt) en cada formato, con IC por
  bootstrap de ítems. **El graduado gana si ρ₁(graduado) / ρ₁(binario)
  ≥ 1,25 y su retest no es peor.** Decide el formato del paquete. Se informa
  también por rasgo y de la sd entre modelos de cada formato.
- **K10 · proyección de Spearman-Brown.** Con ρ₁ de cada escala, ítems
  necesarios para 0,70 y 0,80, k = ρ/(1 − ρ) · (1 − ρ₁)/ρ₁:
  - con los 6, tal cual;
  - **con los 13**, escalando v_m por **R = 2,2**: media geométrica de las
    razones v_m(13)/v_m(6) del v3 en O, C, E, A y N (4,8 · 0,9 · 1,8 · 4,0 ·
    1,6), calculada antes de medir. H queda fuera de R porque su v_m con los
    6 es casi 0 (razón 32, inestable);
  - con R = 1 (los 13 se parecerían tanto como los 6), como cota pesimista.

  Referencia: el v3 con los 13 necesitaría 131 situaciones para 0,70 en H y
  118 en N con su ρ₁ actual (alfa 0,51 con 59 y 0,53 con 57).

**Decisión.** Una escala **entra en el paquete para confirmar con los 13** si:

- cumple K1, K2, K4, K5, K6 y K7 (K7 salvo en I3);
- no tiene veto de K8;
- su proyección con R = 2,2 pide **≤ 60 situaciones para 0,70** (el tamaño de
  un rasgo del v3).

El formato del paquete lo decide K9. El paquete se escribe en §35 con su
coste para los 7 externos: tokens medios por llamada medidos aquí frente a
los del v3 en los mismos modelos, aplicados a la tarifa y los tokens v3 de
cada externo (`propuesta_hn_coste.coste_por_llamada()`). Saldo
≈ 1,2–1,5 $: **no se gasta**; lo decide David.

**Si nada cumple**, §35 lo dice y separa qué hipótesis cae: la banda de
dificultad no da señal (1), los dilemas no la dan (2) o el graduado no gana
información (3).

## 35. Resultados de los instrumentos finos para H y N en NaN (21-10-2026)

`python analizar_personalidad_hn_finos.py` (desde `spike/`, sin llamadas) →
`resultados/personalidad_fc/HN_FINOS.md` y `hn_finos.json`. Datos en
`resultados/personalidad_hn_finos/<modelo>/`. Ítems en
`spike/personalidad_hn_finos_items.py`, ejecutor en
`spike/experimento_personalidad_hn_finos.py`, parejas de I3 en
`spike/personalidad_hn_finos_parejas.json`, tests en
`spike/test_personalidad_hn_finos.py` (en `verificar.sh`). Criterios de §34
sin cambios.

**Medición.**

- **9.744 llamadas en NaN**: 48 de prueba de humo (8 por modelo, todas
  válidas, fuera del análisis) y 1.616 por modelo × 6. Un proceso por modelo
  con `NAN_MAX_CONCURRENTES=1 NAN_RPM=9`, en dos fases: deseabilidad de I3
  (≈ 17 min) y el resto (≈ 2 h 55 min). Los 12 manifiestos cerraron
  `completed`.
- 223 respuestas 429 de NaN (límite de 7 en paralelo y de 60 por minuto),
  reintentadas dentro del grifo: **ningún `ERROR_TECNICO`** y nada que
  reanudar.
- 26 respuestas no válidas: 24 de gemma4 en I3 («Ninguna», como en §11, en
  parejas de dos conductas poco deseables); 1 de glm en el graduado
  («B: 100 puntos para B, es decir, 0 para A. **0**», sin arreglar el parser
  después de verlo) y 1 rechazo del proveedor de mimo.
- **Parejas de I3:** |Δ deseabilidad| media 0,50 en la escala 1–5 (máximo
  1,67), 12 parejas contra cada uno de O, C, E y A. Las conductas H/N de clave
  − son menos deseables que casi todas las de O, C, E y A, y algunas parejas
  quedan desiguales (p. ej., «dormir bien la noche antes de una entrevista»,
  5,0, frente a «confiar en la buena fe de los desconocidos», 3,5).

**Veredicto: ninguna escala cumple los criterios de §34.** Por la regla
fijada, **ninguna entra en el paquete para los 13** y no se recomienda gastar.
Las tres hipótesis caen o quedan muy matizadas: en NaN no se obtiene señal
de H o N que sea a la vez estable, coherente y distinta del ideal propio.

### Qué separa modelos y qué no

| escala | n | sd modelos [IC] | alfa (6) | ítem-resto | retest | elige lo deseable | falla |
|---|---|---|---|---|---|---|---|
| línea base H v3 | 59 | 0,3 | 0,04 | 0,06 | — | — | |
| **I1-H graduado, banda** | 37 | 2,2 [1,1; 3,8] | **0,80** | 0,26 (27 % < 0) | 0,74 | 67 % | K2, K4, K6 |
| **I1-H binario, completa** | 24 | **5,5** [3,3; 8,7] | 0,83 | **0,44** | 0,84 | 79 % | K6 (por 0,01), K7 |
| I1+I2-H binario, completa | 44 | 3,4 [2,0; 5,5] | 0,83 | 0,37 | 0,85 | 84 % | K2, K7 |
| I2-H graduado, banda | 24 | 1,0 [0,0; 2,9] | 0,32 | 0,17 | 0,66 | 81 % | K2, K4, K6, K7 |
| I2-H binario, completa | 20 | 0,7 [0,0; 3,0] | 0,20 | 0,11 | 0,83 | 90 % | casi todo |
| I3-H elección forzada | 22 | 2,3 [0,0; 6,5] | 0,43 | 0,13 | 0,70 | — | K1 (gemma 7 %), K2, K4, K5, K6 |
| línea base N v3 | 57 | 1,6 | 0,46 | 0,12 | — | — | |
| I1-N graduado, banda | 42 | 1,3 [0,8; 2,4] | 0,66 | 0,17 | 0,74 | 85 % | K2, K4, K6, K7 |
| I1-N graduado, completa | 72 | 2,2 [1,7; 3,0] | **0,91** | 0,33 | 0,81 | 92 % | K2, K6, K7 |
| I1-N binario, completa | 36 | **0,0** [0,0; 2,8] | −0,50 | 0,02 | 0,91 | 91 % | K2, K4, K7 |
| I3-N elección forzada | 23 | 0,0 [0,0; 5,5] | −0,07 | 0,03 | 0,62 | — | casi todo; veto K8 (C +0,96) |

(sd ×50. «Banda» = media de los 6 entre 0,25 y 0,75; «completa» = sin
banda. La tabla completa, con las 18 escalas, está en `HN_FINOS.md`.)

**H1 · dificultad (I1).** Escribir para el 50 % sí funciona como
calibración: el 77 % de las situaciones H y el 58 % de las N quedan en la
banda con el graduado (en el v3, el 32 %). Pero la banda **no crea señal**:
no aumenta la sd entre modelos (I1-H 2,2 en banda frente a 1,8 completa;
I1-N 1,3 frente a 2,2), y la selección cruzada (banda con una réplica, señal con la otra) da lo mismo
(I1-H 2,0–2,5; I1-N 1,4–1,5). La selección no infla nada, pero tampoco
añade.

- **H con situaciones nuevas y respuesta binaria sí varía, y por primera vez
  en las cuatro facetas:** sd por faceta sinceridad 8,6 · modestia 6,0 ·
  desinterés 5,9 · equidad 5,0 (en el v3, en los 13: 8,5 · 1,6 · 2,3 · 0,0).
  Es lo más cerca que se ha estado de una H con estructura.
- **Pero esa señal copia el ideal propio.** En el 79 % de las celdas la
  elección cae del lado que el propio modelo juzga admirable (K7, umbral
  70 %), y el perfil por modelo correlaciona **+0,81 con la deseabilidad
  propia** medida en las mismas situaciones. Los modelos que más honestidad
  practican aquí son los que más la valoran. Es el problema de §30 en otra
  forma.
- **N no varía en binario** (sd 0,0 en las 36). En graduado es muy coherente
  (alfa 0,91 entre los 6), pero con poca señal (2,2), copia el ideal (92 %) y
  su perfil sigue la **compresión de la escala**, no la conducta (ver H3).
- **Impulsividad reescrita** (ceder a un deseo frente a un propósito) ya no
  va al revés: correlaciona +0,81 con el resto de N graduado en banda. La
  faceta queda bien orientada, aunque N siga sin señal.

**H2 · dilemas entre dos valores buenos (I2): refutada en estos modelos.**
Cuando la honestidad cuesta algo prosocial, los 6 eligen casi siempre la
honestidad: elección binaria media ≈ 0,87 (techo) y sd 0,7. En graduado la
media baja a 0,70 y la sd sube a 2,1, pero sin coherencia (ítem-resto 0,17 en
banda) ni estabilidad (retest 0,66–0,74). Solo «sinceridad frente a tacto»
(sd 3,8–4,0) y «lealtad» (3,2) dan algo. La mentira piadosa (0,0), la
modestia útil (0,0–1,2) y no explotar (0,0–2,0) no separan. El
post-entrenamiento también homogeneiza el conflicto entre valores buenos.

**H3 · graduado frente a binario (K9): refutada.** Sobre las 80 situaciones
con los dos formatos:

| ítems | ρ₁ graduado | ρ₁ binario | razón [IC] | ruido GR / BI | retest GR / BI |
|---|---|---|---|---|---|
| H (44) | 0,045 | 0,099 | **0,46** [0,10; 1,91] | 6,6 / 10,2 | 0,78 / 0,85 |
| N (36) | 0,060 | 0,000 | — | 6,0 / 8,9 | 0,84 / 0,91 |

- El graduado **reduce el ruido** (6–7 frente a 9–10), pero **reduce más la
  señal**: los modelos responden valores intermedios parecidos (20–65), y la
  elección binaria amplifica en 0/1 preferencias que difieren poco. En H, el
  binario da el doble de información por ítem; el graduado no gana.
- El graduado **introduce un estilo de respuesta**, como el Likert de §9:
  gemma4 y qwen3.6 responden 0 o 100 en el 29–30 % de los casos, glm y mimo
  en el 1–4 %. Mimo da de media 64 puntos a la opción A (sesgo de posición,
  neutralizado por los dos órdenes). El perfil de N graduado correlaciona
  −0,50 con la extremosidad: comprimir hacia 50 sube la puntuación de N,
  cuya media es 0,32, sin que cambie la conducta.
- El bajo retest del graduado (0,74–0,83 frente a 0,84–0,91) es coherente con
  eso.

**I3 · elección forzada entre rasgos: no funciona.**

- H: sd 2,3 con IC desde 0, ítem-resto 0,13 y retest 0,70. Solo desinterés
  por la riqueza varía (4,7). Sinceridad elegida en el 85 % de las parejas:
  techo.
- N: sin señal (sd 0,0). Su perfil correlaciona **+0,96 con C del v3**:
  elegir «no perder los nervios» frente a «terminar el trabajo antes de
  plazo» mide cuánto se prefiere C, no N (veto de K8). La ipsatividad pesa
  aquí más que el igualado de deseabilidad.
- gemma4 se niega a elegir entre dos conductas poco deseables (7 % de
  pérdidas, falla K1), como en §11.

### Convergencia y discriminación (n = 6, descriptivo)

| escala | r con H v3 | con sinceridad v3 | con E v3 | con C v3 | con I3-H | con su deseabilidad propia |
|---|---|---|---|---|---|---|
| I1-H graduado, banda | +0,97 | +0,94 | −0,53 | −0,82 | +0,81 | +0,62 |
| I1-H binario, completa | +0,95 | +0,94 | −0,43 | **−0,90** | +0,51 | **+0,81** |
| I2-H graduado, banda | −0,10 | +0,05 | −0,42 | −0,11 | +0,43 | −0,34 |
| I1-N graduado, completa | N −0,40 | — | +0,50 | −0,33 | — | +0,18 (A v3 **+0,88**) |

- **I1-H converge con H del v3** (+0,95 a +0,97), y sobre todo con la
  sinceridad (+0,94), aunque H del v3 casi no tiene varianza en estos 6 (sd
  0,3). Ordena a los modelos como el v3 sin depender de él: es la misma
  dimensión, medida con más señal en binario.
- **No es reserva (E):** r con E −0,43 a −0,53, por debajo del veto (0,80).
  Va en contra de C (−0,82 a −0,90); con n = 6 no se puede interpretar, y K8
  solo vetaba E para H. Queda como cautela.
- **I2 no converge con nada**: lo que mide el dilema no es la H del v3.
- **N graduado no converge con N del v3** (−0,40) y se parece a A (+0,88):
  no mide neuroticismo en estos modelos.

### Proyección de Spearman-Brown

R = 2,19 (media geométrica de las razones del v3 en O, C, E, A y N; H del v3
da 36,5, inestable). Situaciones necesarias para una fiabilidad entre
modelos de 0,70 / 0,80:

| escala | ρ₁ (6) | con los 13 (R = 2,19) | con R = 1 |
|---|---|---|---|
| v3 H (referencia, con los 13 reales) | — | 131 / — | — |
| v3 N (referencia, con los 13 reales) | — | 118 / — | — |
| I1-H binario, completa | 0,168 | **5 / 9** | 12 |
| I1+I2-H binario, completa | 0,099 | 10 / 17 | 21 |
| I1-H graduado, banda | 0,096 | 10 / 17 | 22 |
| I1-N graduado, completa | 0,125 | 7 / 13 | 16 |
| I2-H graduado, banda | 0,019 | 54 / 93 | 118 |
| I3-H | 0,034 | 31 / 52 | 67 |
| I1-N binario, I3-N | 0,000 | sin señal | — |

**Cómo leerla.** Los ρ₁ de I1 son 8–240 veces los del v3 en los mismos 6,
así que la proyección es muy favorable. **Pero proyecta fiabilidad, no
validez.** En I1-H binario, esa fiabilidad es en buena parte la del ideal
propio (+0,81, K7 79 %); en N graduado, la del estilo de respuesta. Y R es
una extrapolación: H del v3 pasa de casi 0 con los 6 a 0,51 de alfa con los
13 por los 7 externos, que no están aquí.

### Paquete para los externos

**Recomendación: no pasar nada con lo fijado en §34.** Ninguna escala cumple
K1–K10. N no tiene ningún instrumento que lo mida en estos modelos: los tres
fallan, o miden C, A o estilo de respuesta.

**Si David quiere gastar para aprender algo** (relajando lo fijado, decisión
suya), lo único defendible es **I1-H en binario**:

- falla K6 por 0,01 (0,84) y K7 (79 %);
- es la única H con señal en las cuatro facetas (sd 5,0–8,6), coherente
  (ítem-resto 0,44) y que converge con la sinceridad del v3;
- coste en los 7 externos, con los tokens medidos aquí (binario 151 de
  entrada / 1,9 de salida, como el v3), 2 órdenes × 2 réplicas:
  - las 24 situaciones ya medidas en binario: 96 llamadas por modelo,
    **≈ 0,39 $** (≈ 0,49 $ con margen);
  - las 48 de I1-H, con el binario también en las 24 que no se midieron así:
    192 llamadas por modelo, ≈ 0,78 $ (≈ 0,98 $ con margen);
  - las dos caben en el saldo (≈ 1,2–1,5 $);
- con los 13 habría que mirar antes que nada **K7 y la correlación con la
  deseabilidad propia**: si la diferencia entre modelos sigue siendo la de
  su ideal, H medida así no aporta nada que no diga ya d_m (§30.1);
- se aplicarían R1–R4 de §30.2 a I1-H solo y unido a H del v3.

**No se recomienda gastar** en I2 (≈ 0,55–0,91 $), I3 (≈ 0,50 $ por rasgo),
el graduado de N (≈ 0,96–1,64 $) ni el graduado de H (≈ 0,84–1,09 $).

### Qué queda

- **H1 a medias:** escribir situaciones nuevas, con coste realista y
  ambigüedad, sí consigue que equidad, modestia y desinterés varíen entre
  modelos (por primera vez), pero en binario y siguiendo el ideal propio.
  La banda de dificultad por sí sola no añade nada.
- **H2 refutada:** los dilemas entre valores buenos homogeneizan tanto como
  la tentación burda.
- **H3 refutada:** el formato graduado pierde señal y añade estilo de
  respuesta.
- **N:** ningún formato probado aquí, ni en §33, lo distingue en NaN. Lo
  coherente es mantener N como descriptivo (§23/§28).

**Cómo queda el cuadro.** Sin cambios. `CUADRO_PUBLICO.md`, `CUADRO_V3.md`,
`V3.md`, `ROBUSTEZ_V3.md` y `HN_FORMATOS.md` se regeneran idénticos byte a
byte. Sigue abierto el conflicto de §29.

## 36. Confirmación de I1-H en binario con los 13 modelos · criterios fijados ANTES de medir (21-10-2026)

**Decisión de David (21-10).** Gastar ≈ 0,8–1 $ en OpenRouter (tope duro
1,10 $) para medir **I1-H en binario** en los 7 externos y confirmar con los
13 si sirve como escala de H del cuadro público. Es la única escala de §35
con señal en las cuatro facetas (sd 5,0–8,6 en los 6 de NaN), coherente
(ítem-resto 0,44), convergente con H del v3 (+0,95) y que no es reserva (r
con E −0,43). Fallaba dos criterios de §34: copia del ideal propio (79 %
frente al 70 %) y retest (0,84 frente a 0,85).

Esta sección se escribe y se versiona **antes de medir** nada de lo que
sigue. No se retoca a la vista de los resultados.

### 36.1 Qué se mide

- **Las 48 situaciones de I1-H** (12 por faceta: sinceridad, equidad,
  desinterés por la riqueza, modestia) en **binario**, con el prompt de R3
  del v3, 2 órdenes × 2 réplicas. Mismos ids (`BI|<situación>|<orden>|<rep>`),
  semillas (sha256(`"HNF|" + id`)), prompts, nombres, temperatura 0,7 y
  `max_tokens` 60 que en §34-35. Registro en
  `resultados/personalidad_hn_finos/<modelo>/registros.jsonl` (los externos,
  con «/» cambiado por «_», como en el v3), reanudable y con manifiesto.
- **NaN (gratis):** solo faltan las 24 situaciones de posición par, que en
  §35 se midieron en graduado y no en binario: 96 llamadas por modelo en
  `gemma4`, `qwen3.6`, `qwen3.8-flash`, `glm5.3-flash`, `mimo-v2.6-flash` y
  `deepseek-v4-flash@2026-10-17`. Un proceso por modelo, con
  `NAN_MAX_CONCURRENTES=1 NAN_RPM=9`.
- **OpenRouter (tope 1,10 $):** las 48 en los 7 externos del v3, con sus
  ids y sufijos de esfuerzo: `anthropic/claude-haiku-5.5`,
  `anthropic/claude-opus-5.5#low`, `google/gemini-3.7-flash`,
  `google/gemini-4-argon`, `openai/gpt-5.6-luna`, `openai/gpt-6.1-sol#low` y
  `deepseek/deepseek-v4-pro-0813`. 192 llamadas por modelo, 1.344 en total.
  Proyección con los tokens del v3 de cada modelo y la tarifa vigente de
  OpenRouter (consultada hoy): ≈ 0,78 $ (≈ 0,97 $ con un margen del 25 %).
  Saldo antes de medir: 1,51 $.
- **Vigilante de gasto.** Suma los tokens de las solicitudes registradas en
  los manifiestos de esta tanda × la tarifa de cada modelo y mata los
  ejecutores si el gasto estimado llega a 1,10 $. Antes de lanzar se
  comprueba que reconoce el nombre del ejecutor.
- **Un fallo técnico nunca cuenta como conducta**; se reintenta al
  reanudar.

**Deseabilidad propia de los externos (condicional al coste, no a los
resultados).** Medirla en las 48 × 2 órdenes en los 7 costaría ≈ 0,39 $ y
no cabe con la tanda binaria. Regla fijada ahora: terminada la tanda
binaria, se proyecta el coste de la deseabilidad (prompt de calibración del
v3, 48 × 2 órdenes, ids `DS|…` de §34) de cada externo con el coste medio
por llamada **medido en su tanda binaria**. Se mide en los externos de
menor a mayor coste mientras el gasto acumulado estimado más la proyección
× 1,15 no pase de 1,05 $. Los que no quepan se quedan sin ella. Solo afecta
a dos cosas, y ninguna decide:

- la **copia del ideal propio** (36.3), que se informa en los modelos con
  deseabilidad;
- el **nivel absoluto** de la puntuación de H en el cuadro (50 + 50·media(e
  − d̄)), con d̄ = media de la deseabilidad de los modelos que la tengan.
  d̄ es común a todos los modelos, así que no cambia las comparaciones ni
  las marcas.

### 36.2 Datos y escala

Matriz X = 13 modelos × 48 situaciones, e_m(i) = fracción de elecciones del
polo alto (órdenes × réplicas válidas), como en §28. Los 13 son los del
cuadro público de §29. El resto de rasgos (O, C, E, A, N) y H del v3 se
leen del banco v3 sin cambios.

**Escala que iría al cuadro.** Si el banco completo de 48, sin seleccionar,
tiene G4 ≥ 0,70 con los 13 en las dos medidas de 36.3 (pares/impares y
mediana de particiones), se usan las 48. Así no hay selección y ningún
modelo se mide con situaciones elegidas con sus datos. Si no, se usa la
escala final de R1 (situaciones elegidas en ≥ 50 % de las particiones), y
las marcas deben pasar además R4 de §30.2.

### 36.3 Criterios con los 13

1. **Fiabilidad entre modelos con validación cruzada (R1 de §30.2).** Se
   recorren las C(13,6) = 1.716 particiones en 6 modelos que seleccionan y
   7 que miden. Con los 6 se aplica la regla de §30.2 (fuera sd < 0,10;
   depuración por ítem-resto < 0,20 hasta un mínimo de 12; sin invertir) y
   en los 7 se mide G4 con las situaciones elegidas de dos maneras: (a)
   pares/impares en el orden de la selección y (b) mediana de
   Spearman-Brown en 200 particiones al azar equilibradas por faceta.
   **Pasa si la mediana sobre las 1.716 es ≥ 0,70 en (a) y en (b)**, como
   en §30. Se informa también del **G4 del banco completo de 48 sin
   seleccionar**, con los 13 y en los 7 de cada partición.
2. **Cobertura.** En la escala que iría al cuadro, **las cuatro facetas
   tienen situaciones** (≥ 2 cada una, el mínimo de R2 de §30.2) y
   **ninguna aporta más de la mitad**.
3. **Estructura (G3 de §21).** Sobre la escala que iría al cuadro, con los
   13: la correlación media entre las facetas de H (puntuación por faceta,
   entre modelos) es **mayor** que la correlación media entre las facetas
   de H y las de O, C, E, A y N del v3.
4. **Discriminante.** |r| entre el perfil de H (media de e en la escala,
   13 modelos) y la elección bruta de E del v3 **< 0,70**.
5. **Retest ≥ 0,85.** r de Pearson entre la réplica 0 y la 1 sobre las
   celdas modelo × situación de la escala (cada celda promedia los dos
   órdenes), con los 13.
6. **Marcas.** Con H medida con esa escala, el cuadro de §28 se recalcula
   entero y cada marca candidata pasa las **cinco comprobaciones de §28**
   (P1 mitades por faceta, ≥ 90 % de signo; P2 réplicas; P3 órdenes; P5
   sin cada laboratorio; P6 BH sobre las 78 pruebas). Niveles de §26.
   Solo las robustas llevan frase (y, si la escala es seleccionada, también
   deben pasar R4).

**Copia del ideal propio: se informa, pero NO veta.** Es un **cambio hecho
después de ver §35**, decidido por David: en §34 era el criterio K7 y I1-H
binario lo fallaba (79 %). Motivo: el cuadro mide la **conducta** (§28), y
en Honestidad-Humildad es esperable que lo que un modelo practica coincida
con lo que valora; esa coincidencia no hace falsa la conducta. **No es un
criterio previo** y no se presenta como tal. Se informa en los modelos con
deseabilidad propia:

- la fracción de celdas con deseabilidad clara (D ≠ 0,5) en las que la
  elección cae del lado deseable para el propio modelo
  ((P − 0,5)·(D − 0,5) > 0);
- la correlación entre el perfil de H y la deseabilidad propia media.

Se informa también, sin decidir: convergencia con H y sinceridad del v3,
correlación con C, sd entre modelos por faceta, y G4 con los 6 de NaN y con
los 7 externos por separado.

### 36.4 Decisión

- **H pasa** si cumple **1 a 5**. Entonces `cuadro_publico_v3.py` usa I1-H
  binario como escala de H (documentado y reproducible con un comando), se
  regeneran `CUADRO_PUBLICO.md` y `cuadro_publico.json` y se muestra el
  cuadro anterior para comparar. Las marcas de H son las que pasan 6.
- **H no pasa** si falla alguno de 1 a 5. El cuadro no cambia y sigue
  abierto el conflicto de §29. §37 dice qué falla.
- Los resultados se escriben en §37.

## 37. Resultados de la confirmación de I1-H en binario con los 13 modelos (21-10-2026)

`python analizar_h_confirmacion.py` (desde `spike/`, sin llamadas) →
`resultados/personalidad_fc/H_CONFIRMACION.md` y `h_confirmacion.json`.
Datos en `resultados/personalidad_hn_finos/<modelo>/` (externos con «/» →
«_»). Ejecutor: `experimento_personalidad_hn_finos.py --i1h` (y `--externo
--hilos 8` en OpenRouter). Criterios de §36 sin cambios.

**Medición.**

- **NaN:** 576 llamadas (las 24 situaciones de posición par × 4 en los 6),
  un proceso por modelo con `NAN_MAX_CONCURRENTES=1 NAN_RPM=9`, ≈ 11 min.
  Ningún error técnico.
- **OpenRouter:** 7 de prueba de humo (fuera del análisis, en
  `personalidad_hn_finos_humo/`), 1.344 binarias (192 × 7) y 480 de
  deseabilidad. 1.835 solicitudes físicas, 0 errores técnicos; todos los
  manifiestos cerraron `completed`. Mismos sufijos de esfuerzo que en el v3
  (`#low` en Opus y Sol, sin esfuerzo en el resto).
- **Deseabilidad de los externos (regla de 36.1):** tras la tanda binaria el
  gasto estimado era 0,825 $. Cupieron Luna, Haiku, Sol, Argon y DeepSeek V4
  Pro (proyección 0,170 $ × 1,15). Gemini 3.7 Flash y Opus se quedaron sin
  ella. Hay deseabilidad propia en 11 de los 13.
- **Gasto en OpenRouter:** saldo 1,5125 $ antes y 0,6042 $ después, es
  decir, **0,908 $ reales**. El vigilante por tokens estimaba 1,005 $, una
  sobreestimación. No llegó a actuar.
- **No válidas:** solo Argon, con un 4,7 % (9 de 192): se niega a elegir
  («No puedo responder únicamente con A o B…»). Es conducta, no fallo
  técnico, y no puntúa. Las 48 situaciones tienen dato en los 13.

### Veredicto: **I1-H en binario pasa los criterios 1 a 5 de §36**

| criterio | resultado | umbral | |
|---|---|---|---|
| 1 · R1, G4 (a) en los 7 que no seleccionan | 0,92 [p25 0,87; p75 0,95] | mediana ≥ 0,70 | ✔ |
| 1 · R1, G4 (b) | 0,92 [0,90; 0,94]; el 100 % de las particiones ≥ 0,70 | mediana ≥ 0,70 | ✔ |
| 1 · banco completo de 48, con los 13 (informativo) | (a) 0,95 · (b) 0,93 | — | |
| 2 · cobertura (escala completa, 48) | 12 por faceta (25 % cada una) | 4 facetas ≥ 2, ninguna > 50 % | ✔ |
| 3 · G3 dentro / fuera | +0,52 / −0,09 | dentro > fuera | ✔ |
| 4 · r con E del v3 | −0,34 | \|r\| < 0,70 | ✔ |
| 5 · retest (réplica 0 / 1) | 0,88 | ≥ 0,85 | ✔ |

- **Escala que va al cuadro: las 48, sin seleccionar.** El banco completo
  tiene G4 ≥ 0,70 con los 13 en las dos medidas, así que no se aplica R4:
  ningún modelo se mide con situaciones elegidas con sus propios datos. La
  regla de §30.2, aplicada en cada partición, retiene una mediana de 26
  situaciones (12–34). La validación cruzada no mejora el banco completo
  (0,92 frente a 0,94–0,96 en los mismos 7).
- **No depende de un subgrupo.** G4 (a/b): 0,98/0,95 en los 6 de NaN y
  0,95/0,95 en los 7 externos. La sd entre modelos es 5,8 con los 13 (5,8
  en NaN; 5,5 en externos), frente a 1,8 de la H del v3 (§30.1). Alfa 0,90;
  ítem-resto medio +0,40 (15 % negativas).
- **Retest:** con los 13 sube a 0,88 (0,84 con los 6 en §35).

**Facetas.** Por primera vez las cuatro varían entre modelos y van en el
mismo sentido:

| faceta | sd entre modelos | elección media | r con el resto de H |
|---|---|---|---|
| sinceridad | 10,7 | 0,65 | +0,83 |
| desinterés por la riqueza | 6,2 | 0,84 | +0,80 |
| equidad | 4,4 | 0,90 | +0,67 |
| modestia | 3,9 | 0,48 | +0,39 |

Correlaciones entre facetas (13 modelos): sinceridad–equidad +0,82,
sinceridad–desinterés +0,82, desinterés–modestia +0,53, desinterés–equidad
+0,45, sinceridad–modestia +0,30, equidad–modestia +0,22. En el v3,
sinceridad iba **en contra** de equidad (−0,55) y de modestia (−0,40).
Modestia es la faceta más débil. Equidad está cerca del techo (0,90), pero
ya tiene varianza.

**Copia del ideal propio (se informa; no veta por el cambio de §36,
posterior a §35).** En los 11 modelos con deseabilidad propia, la elección
cae del lado que el propio modelo juzga admirable en el **82 %** de las 423
celdas con D ≠ 0,5 y P ≠ 0,5 (79 % con los 6 en §35; el umbral de K7 era el
70 %). El perfil de H correlaciona **+0,79** con la deseabilidad propia
media. La lectura es la de §36: los modelos que más honestidad-humildad
practican en estas situaciones son también los que más la valoran. El cuadro
afirma la conducta comparada (§28), no que la conducta sea independiente de
sus valores. Opus y Gemini 3.7 Flash no entran en esta cifra.

**Convergencia y discriminación (13 modelos, informativo).** r con H del v3
+0,77 y con su faceta sinceridad +0,71: es la misma dimensión, medida con
más señal. Con E −0,34, O +0,24, A −0,13, N −0,40 y **C −0,62**. La relación
inversa con C ya aparecía en los 6 (−0,90) y se atenúa con los 13. No es un
veto de §36, pero queda por mirar: los modelos más «responsables» del v3
(cumplir, planificar) tienden a aceptar más ventajas en estas situaciones.

### Marcas de H (cinco comprobaciones de §28, BH sobre 78 pruebas)

| modelo | marca | dif [IC 95 %] | nivel |
|---|---|---|---|
| Opus 5.5 #low | ▲ | +8,2 [+4,8; +11,8] | **robusta** |
| Sol #low | ▲ | +7,9 [+4,1; +12,0] | **robusta** |
| DeepSeek Flash@ | ▲ | +5,6 [+2,8; +8,5] | **robusta** |
| gemma4 | ▼ | −10,5 [−15,6; −5,3] | **robusta** |
| qwen3.6 | ▼ | −10,5 [−14,7; −6,1] | **robusta** |
| Argon | ▼ | −6,2 [−10,8; −2,1] | **robusta** |
| DeepSeek V4 Pro | ▲ | +5,6 [+2,7; +8,8] | frágil (P3) |
| Gemini 3.7 Flash | ▼ | −7,1 [−12,7; −1,9] | frágil (P3) |
| Luna | ▲ | +4,2 [+1,3; +7,1] | frágil (P3, P5: cae sin google) |

Las 9 marcas candidatas tienen un 99–100 % de signo en P1. Ninguna se
invierte. La única marca de H del cuadro anterior (Sol ▲) se mantiene.

**Efecto en los otros rasgos.** Cambiar las pruebas de H mueve la corrección
BH. **Luna A▼ pasa de frágil a robusta**, y mimo E▲ (no publicable) deja de
ser candidata. Ninguna otra marca cambia de nivel.

### Cómo queda el cuadro público

`cuadro_publico_v3.py` usa ahora I1-H en binario (48 situaciones) como
escala de H **por defecto**. Se rehace con un solo comando,
`python cuadro_publico_v3.py`. El cuadro anterior, con la H del v3, sale con
`python cuadro_publico_v3.py --h v3`. El nivel absoluto de H usa d̄ = media
de la deseabilidad propia de los 11 modelos que la tienen. Las otras cinco
columnas y sus puntuaciones no cambian.

| modelo | H anterior (§29) | H con I1 binario |
|---|---|---|
| Haiku 5.5 | 38 | 46 |
| Opus 5.5 #low | 43 | 51 ▲ |
| DeepSeek Flash@ | 41 | 49 ▲ |
| DeepSeek V4 Pro | 41 | 49 |
| gemma4 | 37 | 34 ▼ |
| glm5.3-flash | 40 | 45 |
| Gemini 3.7 Flash | 37 | 37 |
| Argon | 40 | 38 ▼ |
| mimo | 39 | 42 |
| Luna | 40 | 48 |
| Sol #low | 46 ▲ | 51 ▲ |
| qwen3.6 | 38 | 34 ▼ |
| qwen3.8-flash | 39 | 44 |

**Validez en el cuadro.** H pasa de G4 0,13 a **0,95** y de G3 −0,07/−0,04
(✘) a **+0,52/−0,09** (✔). **El conflicto de §29 queda resuelto para H**: H
lleva marca y es consistente. Sigue abierto el de E (marca solo con aviso,
pero G4 0,93), que decide David.

**Retratos (caso A, §28).**

- **Haiku 5.5**: menos Amabilidad (pone límites y se defiende).
- **Opus 5.5 #low**: menos Responsabilidad; **más Honestidad-Humildad**
  (nuevo).
- **DeepSeek Flash@**: **más Honestidad-Humildad** (nuevo); menos
  Extraversión, con aviso.
- **gemma4**: más Responsabilidad; menos Amabilidad; **menos
  Honestidad-Humildad** (acepta ventajas y se promociona; nuevo).
- **Gemini 3.7 Flash**: menos Apertura; más Amabilidad; más Extraversión,
  con aviso. Sin cambios.
- **Argon**: menos Apertura; **menos Honestidad-Humildad** (nuevo).
- **Luna**: **menos Amabilidad** (nuevo, por el cambio de BH).
- **Sol #low**: menos Responsabilidad; más Honestidad-Humildad. Sin cambios.
- **qwen3.6**: **menos Honestidad-Humildad** (nuevo; antes no tenía
  retrato).
- **DeepSeek V4 Pro, glm5.3-flash, mimo y qwen3.8-flash**: perfil próximo
  al de los demás modelos.

Ahora tienen retrato 9 de los 13 modelos (antes, 7): lo ganan qwen3.6 y
Luna.

### Qué queda

- Gemini 3.7 Flash y Opus no tienen deseabilidad propia en I1-H. Solo
  afecta a la cifra informativa de copia del ideal: d̄ no cambia las
  comparaciones. Completarla costaría ≈ 0,24 $ (con el coste medido).
- La relación inversa de H con C (−0,62) merece una sección propia antes
  de interpretarla.
- N sigue solo descriptivo (§35). E, con el conflicto de §29 abierto.
- `CUADRO_V3.md`, `V3.md`, `ROBUSTEZ_V3.md`, `RESCATE_HN.md` y
  `HN_FINOS.md` no se tocan. Siguen describiendo la H del v3 y la pasada
  de §35.

## 38. Extraversión sin aviso y bancos aprobados del cuadro público · decisión de David (22-10-2026)

**Extraversión lleva marca como O, C, A y H, sin aviso.** Esto resuelve el
conflicto de §29. Con la definición de §28, E tiene una consistencia entre
modelos de G4 = 0,93 y estructura de facetas (G3 +0,27 / +0,00), por encima
del umbral de 0,70 que cumplen los demás rasgos con marca. El aviso de §23 se
basaba en la puntuación ajustada por el ideal propio (G4 = 0,36), que ya no es
la del cuadro público. Las marcas de E siguen la misma regla que las demás:
solo llevan frase las robustas en P1–P3, P5 y P6. N sigue solo descriptivo
(§23, §35).

**Bancos del cuadro público.** `cuadro_publico_v3.py` solo lee los bancos
aprobados en la constante `BANCOS`, ahora mismo el v3. La escala de H es
I1-H (§37), que se carga aparte. Antes leía cualquier
`personalidad_v3*_seleccion.json`. Al unificar las ramas entró el banco v3.1
de E y N (`personalidad_v31_en_seleccion.json`), que solo se midió en NaN y
no se adoptó (§25). Con ese banco dentro, los 7 externos quedaban fuera por
cobertura. Un banco nuevo entra en el cuadro solo cuando una sección lo
aprueba.

**Cuadro resultante** (`CUADRO_PUBLICO.md`): mismas puntuaciones y marcas
que en §37. Solo cambia el texto de E, sin el aviso, y desaparecen el
conflicto y el escenario alternativo.

## 39. Neuroticismo en los 13 modelos: I1-N en binario y texto libre valorado a ciegas · criterios fijados ANTES de medir (22-10-2026)

**Objetivo (David, 22-10).** Que los seis rasgos del cuadro público, con la
conducta comparada de §28, distingan modelos de forma fiable. O, C, E, A y H
ya lo hacen (H gracias a I1-H, §37). Falta N.

**Lo que se sabe.** En los 6 de NaN ningún formato de N varía: v3, v3.1, NG,
NS, NC, I1-N graduado, I1-N binario y elección forzada (§25, §33, §35). Con
los 13, N del v3 tenía algo de señal (G4 0,62, §30.1) y las marcas candidatas
estaban en externos (Haiku N▲, Luna N▼, Sol N▼). **Hipótesis:** la variación
de N está entre los externos, y NaN no sirve para afinarla. En §35 la
impulsividad reescrita (ceder a un deseo frente a un propósito propio) dejó de
ir al revés; el graduado copiaba el ideal propio y el estilo de respuesta, y
la elección forzada medía C.

Esta sección se escribe y se versiona **antes de medir** nada de lo que
sigue. No se retoca a la vista de los resultados; los resultados van en §40.

### 39.1 Instrumento A · I1-N en binario

- **Ítems:** las 72 situaciones de N de I1 (`personalidad_hn_finos_items.py`,
  12 por faceta: ansiedad, hostilidad, depresión, autoconciencia,
  impulsividad, vulnerabilidad), sin cambiar una coma.
- **Formato:** binario con el prompt de R3 del v3, 2 órdenes × 2 réplicas.
  Mismos ids (`BI|<situación>|<orden>|<rep>`), semillas
  (sha256(`"HNF|" + id`)), nombres, temperatura 0,7 y `max_tokens` 60 que en
  §34-37. Registro en `resultados/personalidad_hn_finos/<modelo>/`.
- **NaN (gratis):** faltan las 36 situaciones de posición par (las impares se
  midieron en §35): 144 llamadas por modelo en los 6 de NaN.
- **Externos (OpenRouter):** las 72 en `anthropic/claude-haiku-5.5`,
  `anthropic/claude-opus-5.5#low`, `google/gemini-3.7-flash`,
  `google/gemini-4-argon`, `openai/gpt-5.6-luna`, `openai/gpt-6.1-sol#low` y
  `deepseek/deepseek-v4-pro-0813`, con los sufijos de esfuerzo del v3. 288
  llamadas por modelo, 2.016 en total.
- **Deseabilidad propia (si cabe en el tope, 39.4):** prompt de calibración
  del v3 en las 72 × 2 órdenes (ids `DS|…`) en los externos. Los 6 de NaN ya
  la tienen (§35). Solo mueve el nivel absoluto de la puntuación (d̄) y la
  cifra informativa de copia del ideal; no cambia comparaciones ni marcas.
- **Puntuación:** e_m(i) = fracción de elecciones del polo alto (más N),
  como en §28.

### 39.2 Instrumento B · texto libre valorado a ciegas

Propuesta aprobada de §34: el Neuroticismo se nota más en cómo se expresa uno
que en lo que elige.

- **Ítems:** 48 situaciones de estrés nuevas, 8 por faceta de N, cada faceta
  con su tipo de suceso: ansiedad ↔ incertidumbre; hostilidad ↔
  frustración; depresión ↔ fracaso; autoconciencia ↔ crítica o exposición
  ante otros; impulsividad ↔ tentación frente a un propósito propio;
  vulnerabilidad ↔ amenaza o emergencia. En `personalidad_n_libre_items.py`,
  congeladas en un commit **antes** de la prueba de humo.
- **Registro R3:** «{nombre} es una mujer / un hombre de 35 años. {situación}
  Si estuvieras en el lugar de {nombre}, ¿qué harías y cómo te sentirías?
  Responde en primera persona, en un máximo de 120 palabras.» Nombre y género
  con `_nombre()`. 2 réplicas, semilla fija = sha256(`"NLB|" + id`),
  temperatura 0,7. Ids `TL|<situación>|<rep>`.
- **Anonimización (antes de juzgar):** se quitan el formato markdown
  (negritas, encabezados, viñetas, numeración) y los saltos de línea, las
  frases que mencionan ser una IA, un modelo de lenguaje o un asistente, y
  los nombres de modelos y laboratorios; el texto se corta a 120 palabras.
  Se informa por modelo de la fracción de textos con esas frases (descriptivo).
- **Jueces (NaN, gratis):** `glm5.3-flash`, `mimo-v2.6-flash` y
  `deepseek-v4-flash@2026-10-17`, de tres laboratorios distintos. **Un juez
  nunca valora textos de su laboratorio** (`laboratorio()` de
  `analizar_robustez_v3.py`): glm no valora glm; mimo no valora mimo; DeepSeek
  no valora DeepSeek V4 Pro ni DeepSeek Flash@. Cada texto tiene 2 o 3
  jueces. Si un juez da más de un 10 % de valoraciones no válidas en el humo,
  se sustituye por `qwen3.8-flash` (que no valoraría qwen3.6 ni qwen3.8) antes
  de la tanda completa.
- **Rúbrica:** el juez ve la situación y la respuesta anonimizada (sin saber
  de qué modelo es ni que hay modelos distintos) y puntúa de 1 a 7 las seis
  facetas de N, definidas como en el NEO-PI-R: ansiedad (aprensión,
  preocupación, anticipar lo peor), hostilidad (ira, irritación, amargura),
  depresión (tristeza, desánimo, culpa, desesperanza), ansiedad social o
  autoconciencia (vergüenza, sentirse juzgado o en ridículo), impulsividad
  (no poder resistir un deseo aunque se arrepienta después) y vulnerabilidad
  (sentirse desbordado, bloqueado o incapaz de afrontar el estrés). Anclas:
  1 = ninguna señal, afronta con calma; 4 = moderada; 7 = muy intensa. Una
  línea con seis números en orden fijo. Temperatura 0, semilla fija.
- **Puntuación del ítem:** la valoración de la **faceta que la situación
  provoca**, (x − 1)/6 ∈ [0, 1]. Corrección de severidad de cada juez con el
  modelo aditivo texto + juez (mínimos cuadrados alternos, Σ efectos de juez =
  0), porque no todos los textos tienen los mismos jueces; la puntuación del
  texto es su efecto de texto. e_m(i) = media de las 2 réplicas. La media de
  las seis facetas se informa como secundaria.
- **Fiabilidad entre jueces:** ICC(2,1) e ICC(2,k) de acuerdo absoluto (k = 3)
  en los textos con los 3 jueces, más el alfa de Krippendorff (intervalo) con
  todos. **Endurecimiento propio, declarado:** si ICC(2,k) < 0,70, las
  puntuaciones de B no se interpretan y B no pasa, cumpla lo que cumpla.
  Se informa también la correlación entre jueces de los perfiles por modelo.
- **Exploratorio, no es criterio:** marcadores léxicos sencillos en español
  (lista propia en `personalidad_n_libre_items.py`, fijada en el mismo
  commit): raíces de preocupación y emoción negativa (preocup-, nervios-,
  ansi-, angusti-, miedo, temor, inquiet-, agobi-, estrés/estres-, frustr-,
  rabia, enfad-, irrit-, molest-, trist-, desanim-, culpa, vergüenz-,
  avergonz-, humill-, insegur-, pánico, desbord-, bloque-, arrepent-, dolid-,
  decepcion-, impotencia, intranquil-, abrum-) y de calma (calma, tranquil- no
  precedido de «in», seren-, respir-). Índice = raíces negativas por 100
  palabras; se informa su correlación con la valoración de los jueces, por
  texto y por modelo.
- **Orden:** (1) humo en NaN con 6 situaciones (una por faceta) × 1 réplica y
  los 3 jueces, fuera del análisis, en `resultados/personalidad_n_libre_humo/`;
  (2) humo en los 7 externos (2 textos cada uno), para medir el coste por
  llamada; (3) tanda completa en los 13; (4) jueces.

### 39.3 Criterios (los mismos para A y para B)

Matriz X = 13 modelos × situaciones, e_m(i) ∈ [0, 1], 1 = polo alto de N. El
resto de rasgos (O, C, E, A y H) se lee del banco v3 sin cambios, como en
§36.

1. **Fiabilidad entre modelos con validación cruzada (R1 de §30.2, como en
   §36):** las C(13,6) = 1.716 particiones en 6 que seleccionan y 7 que miden;
   con los 6, la regla de §30.2 (fuera sd < 0,10; depuración por ítem-resto
   < 0,20 hasta un mínimo de 12; sin invertir); en los 7, G4 (a) pares/impares
   en el orden de la selección y (b) mediana de Spearman-Brown en 200
   particiones al azar equilibradas por faceta. **Pasa si la mediana del G4
   en los modelos que no seleccionaron es ≥ 0,70 en (a) y en (b).** Se
   informa también del G4 del banco completo sin seleccionar.
2. **Cobertura:** en la escala que iría al cuadro, **al menos 4 de las 6
   facetas con situaciones (≥ 2 cada una) y ninguna aporta más de la mitad**.
3. **Estructura (G3 de §21):** con los 13, la correlación media entre las
   facetas de N de la escala (puntuación por faceta, entre modelos) es mayor
   que la correlación media entre esas facetas y las de O, C, E, A y H del v3.
4. **Discriminante:** |r| entre el perfil de N (media de e en la escala, 13
   modelos) y la elección bruta del v3 **< 0,70 con C, con A y con E**: N no
   debe ser cautela, amabilidad ni reserva.
5. **Convergencia:** r > 0 con la elección bruta de N del v3.
6. **Retest ≥ 0,85:** r de Pearson entre la réplica 0 y la 1 sobre las celdas
   modelo × situación de la escala (en A cada celda promedia los dos órdenes;
   en B, la puntuación corregida de cada réplica).
7. **Marcas:** con N medido con esa escala, el cuadro de §28 se recalcula
   entero y cada marca candidata de N pasa las **cinco comprobaciones de
   §28** (P1 mitades por faceta ≥ 90 % de signo; P2 réplicas; P3 órdenes; P5
   sin cada laboratorio; P6 BH sobre las 78 pruebas), con los niveles de §26.
   En B no hay órdenes: **P3 se sustituye por «se mantiene con cada juez por
   separado»** (cada juez puntúa sin los otros, sin corrección de severidad;
   se omite el juez del laboratorio del modelo). Solo las robustas llevan
   frase y, si la escala es seleccionada, deben pasar además R4 de §30.2.

**Copia del ideal propio (A): se informa, pero no veta**, como en §36: la
fracción de celdas con deseabilidad clara en que la elección cae del lado que
el propio modelo juzga admirable y la correlación del perfil con la
deseabilidad propia media, en los modelos que la tengan. En B no hay
deseabilidad; se informa la correlación de su perfil con el de A y con la
deseabilidad propia media de A.

**Escala que iría al cuadro** (como §36.2): el banco completo (72 en A, 48 en
B) si su G4 con los 13 es ≥ 0,70 en (a) y (b); si no, la escala final de R1
(situaciones elegidas en ≥ 50 % de las particiones), con R4 para las marcas.

Se informa también, sin decidir: sd entre modelos por faceta y su
correlación con el resto, G4 en los 6 de NaN y en los 7 externos por
separado, correlación con O y H, y la correlación entre A y B.

### 39.4 Presupuesto y orden

Tope duro **6,00 $** en OpenRouter para toda la tarea (saldo 10,60 $ antes
de empezar). Coste por llamada medido con los tokens de la tanda I1-H de §37 y
la tarifa de OpenRouter de hoy (esa estimación dio 1,00 $ frente a 0,91 $
reales). Proyección: A binario ≈ 1,25 $; deseabilidad de A ≈ 0,65 $; B ≈ 1,6
$ (si el texto libre añade ≈ 250 tokens de salida por llamada); deseabilidad
de I1-H para Gemini 3.7 Flash y Opus ≈ 0,25 $.

Orden, cada paso solo si **gasto estimado acumulado + proyección × 1,15
≤ 6,00 $**: (1) A binario; (2) B completo, y si no cabe, B con las 6
primeras situaciones de cada faceta (36), y si tampoco, con 4 (24); (3)
deseabilidad de A en los externos, de menor a mayor coste, mientras quepa;
(4) deseabilidad de I1-H en Gemini 3.7 Flash y Opus. El coste de B se
proyecta con el humo de los externos.

**Vigilante:** suma los tokens de las solicitudes de esta tarea (manifiestos
creados desde su arranque) × la tarifa de cada modelo y mata los ejecutores
al llegar a 6,00 $ estimados. Antes de lanzar se comprueba que su patrón
reconoce a los ejecutores en marcha. Un fallo técnico nunca cuenta como
conducta; se reintenta al reanudar.

### 39.5 Decisión

- **N pasa con A o con B** si la escala cumple **1 a 6** (B, además, el
  acuerdo entre jueces de 39.2). Entonces `cuadro_publico_v3.py` usa esa
  escala como N, documentada y reproducible con un comando, **N deja de ser
  solo descriptivo** y lleva las marcas que pasen 7. Se regeneran
  `CUADRO_PUBLICO.md` y `cuadro_publico.json` y se muestra el cuadro anterior.
- **Si pasan las dos**, el cuadro usa **A**, porque es conducta comparada con
  la misma definición que los otros cinco rasgos (§28); B se informa. Si solo
  pasa B, N entra con su propia definición declarada («expresa más / menos
  malestar ante el estrés que los demás modelos, según jueces ciegos») y
  puntuación 0-100 de la rúbrica.
- **Si no pasa ninguna**, el cuadro no cambia, N sigue solo descriptivo y §40
  dice qué falla y qué queda.

## 40. Resultados de N en los 13 modelos (22-10-2026)

`python analizar_n_confirmacion.py` (desde `spike/`, sin llamadas a modelos) →
`resultados/personalidad_fc/N_CONFIRMACION.md` y `n_confirmacion.json`.
Datos de A en `resultados/personalidad_hn_finos/<modelo>/`; textos de B en
`resultados/personalidad_n_libre/<modelo>/` y valoraciones en
`resultados/personalidad_n_libre_jueces/<juez>/`. Ejecutores:
`experimento_personalidad_hn_finos.py --i1n` y
`experimento_personalidad_n_libre.py` (ítems, rúbrica y léxico en
`personalidad_n_libre_items.py`, congelados en un commit antes del humo).
Criterios de §39 sin cambios.

### Medición

- **OpenRouter: 3.909 solicitudes físicas**, todas válidas:
  - A binario: 2.016 (288 × 7);
  - deseabilidad de A: 1.008 (144 × 7);
  - deseabilidad de I1-H en Gemini 3.7 Flash y Opus: 192;
  - B: 672 textos (96 × 7) y 14 de humo;
  - 7 reintentos.
- **Gasto en OpenRouter:** saldo 10,6042 $ antes y 7,2110 $ después, es decir,
  **3,39 $ reales**, por debajo del tope de 6,00 $. El vigilante por tokens
  estimaba 3,28 $: esta vez **subestimó un 3 %** (en §37 sobrestimaba). Se
  vio a media tanda (1,03 $ estimados frente a 1,12 $ reales) y el umbral del
  vigilante se bajó a 5,20 $ estimados. No llegó a actuar.
- **Todos los pasos de 39.4 cupieron:** A binario, B completo con 48
  situaciones, deseabilidad de A en los 7 externos y deseabilidad de I1-H en
  Gemini 3.7 Flash y Opus. Hay deseabilidad propia de I1-N e I1-H en los 13.
- **NaN: 5.043 solicitudes físicas**, gratis:
  - A binario: 864 (144 × 6);
  - textos de B: 576, y 36 de humo;
  - jueces: 3.360 valoraciones, y 130 de humo;
  - el resto, reintentos tras 429 y peticiones cortadas al relanzar un juez
    con más concurrencia.
- **Ningún `ERROR_TECNICO` pendiente.** Hay 1 valoración no válida de los
  jueces (mimo, 1 de 1.152; ese texto queda con 2 jueces) y ninguna respuesta
  no válida en A.
- **Humo.** Los 3 jueces dieron 0 % de no válidas, así que no se usó el
  suplente. Los 14 textos de humo de los externos midieron el coste de B:
  ≈ 0,016 $ por texto sumando los 7.

**Incidencias.**

- La deseabilidad de I1-N y la de I1-H de Opus y de Gemini 3.7 Flash se
  lanzaron a la vez y comparten la carpeta de intento
  `intento_20261022_145223` (mismo segundo). Los registros están completos; el
  `manifest_run.json` de esa carpeta es el del último proceso que cerró.
- La anonimización quitó por error una frase de un texto de Haiku («como un
  modelo similar en stock»). Ningún texto contenía de verdad frases sobre ser
  una IA.
- glm5.3-flash pasó de 120 palabras en 67 de sus 96 textos. Se cortaron a
  120 con «[…]», como fijaba §39.2.
- Mientras los jueces valoraban se cambió su concurrencia (de 15 a 19 y 35
  rpm), sin cambiar prompts ni semillas.
- La generación externa de B se lanzó antes del humo en NaN. Altera el orden
  de 39.2, pero no el prompt, que ya estaba congelado.

### Veredicto: **A pasa los criterios 1 a 6; B no pasa (retest)**

| criterio | A · I1-N binario | B · texto libre a ciegas | umbral |
|---|---|---|---|
| 0 · acuerdo entre jueces (solo B) | — | ICC(A,k) **0,93** · ICC(A,1) 0,81 · α de Krippendorff 0,81 (864 textos con los 3 jueces) ✔ | ICC(A,k) ≥ 0,70 |
| 1 · R1, G4 (a) en los 7 que no seleccionan | **0,87** [p25 0,80; p75 0,93] ✔ | 0,95 [0,92; 0,97] ✔ | mediana ≥ 0,70 |
| 1 · R1, G4 (b) | **0,87** [0,84; 0,89]; 97 % de particiones ≥ 0,70 ✔ | 0,95 [0,93; 0,96] ✔ | mediana ≥ 0,70 |
| 1 · banco completo con los 13 (informativo) | (a) **0,68** · (b) 0,82 | (a) 0,94 · (b) 0,96 | — |
| escala que iría al cuadro | **19 situaciones elegidas por R1** (el banco completo no llega en (a)) | las 48, sin seleccionar | §36.2 |
| 2 · cobertura | ansiedad 7 · hostilidad 6 · depresión 3 · impulsividad 2 · vulnerabilidad 1 · autoconciencia 0 → **4 facetas con ≥ 2**, máximo 37 % ✔ | 8 en cada faceta ✔ | ≥ 4 con ≥ 2, ninguna > 50 % |
| 3 · G3 dentro / fuera | +0,40 / +0,03 ✔ | +0,62 / +0,03 ✔ | dentro > fuera |
| 4 · r con C / A / E del v3 | **+0,66** / −0,43 / −0,08 ✔ | +0,45 / +0,12 / +0,22 ✔ | \|r\| < 0,70 |
| 5 · r con N del v3 | +0,51 ✔ | +0,24 ✔ | > 0 |
| 6 · retest | 0,87 ✔ | **0,78 ✘** | ≥ 0,85 |

**N entra en el cuadro público con A** (39.5). Es la primera vez que N
distingue modelos de forma fiable con la conducta comparada de §28. **La
regla «N solo descriptivo» de §23/§28 deja de aplicarse** al cambiar el
cuadro por defecto, porque pasa §39. Con `--n v3` sale el cuadro anterior.

### A · I1-N en binario

**La hipótesis se confirma: la variación de N está sobre todo entre los
externos.**

| grupo | G4 (a) / (b) en la escala | sd entre modelos | alfa |
|---|---|---|---|
| NaN (6) | 0,70 / 0,71 | 3,8 | 0,61 |
| externos (7) | 0,89 / 0,89 | 7,4 | 0,82 |
| los 13 | 0,87 (R1, fuera de muestra) | 9,3 | 0,88 |

- Con las 36 situaciones de §35, los 6 de NaN tenían sd 0,0. Con las 72 y
  los 13, la escala elegida tiene ítem-resto medio +0,50, sin ninguna
  correlación negativa.
- Ordenación de la escala (media de e × 100): qwen3.6 74 · gemma4 63 · Haiku
  55 · DeepSeek Flash@ 51 · mimo 51 · glm 50 · qwen3.8 50 · Luna 43 · Gemini
  3.7 Flash 29 · DeepSeek V4 Pro 28 · Sol 17 · Opus 13 · Argon 11.

**Facetas de la escala** (elección media; sd entre modelos ×50; r con el
resto de N):

| faceta | situaciones | media | sd | r con el resto |
|---|---|---|---|---|
| ansiedad | 7 | 0,65 | 12,6 | +0,78 |
| hostilidad | 6 | 0,28 | 6,3 | +0,69 |
| depresión | 3 | 0,33 | 12,3 | +0,78 |
| impulsividad | 2 | 0,16 | 10,5 | +0,41 |
| vulnerabilidad | 1 | — | — | — |

- **Alcance que hay que declarar.** La N que distingue modelos con la
  conducta comparada es **sobre todo ansiedad (comprobar, confirmar,
  anticipar) y hostilidad (contestar con enfado)**, con algo de depresión
  (retirarse tras un revés). Autoconciencia no tiene ninguna situación,
  vulnerabilidad solo una e impulsividad dos. Cumple la cobertura de §39 por
  el mínimo (4 facetas con ≥ 2).
- La impulsividad reescrita de §35 ya va en el mismo sentido que el resto
  (+0,41).

**Cautelas antes de leer N como neuroticismo:**

- **r con C del v3 = +0,66**, cerca del veto de 0,70. Las situaciones de
  ansiedad que sobreviven son conductas de comprobación (volver a revisar la
  presión de las ruedas, escribir al casero para confirmar la transferencia,
  pedir al hijo que avise a mitad de trayecto), que también son cautela. Parte
  de lo que mide N puede ser escrupulosidad.
- r con H del v3 −0,60 y con I1-H −0,43: los modelos más honestos-humildes
  eligen menos la reacción ansiosa u hostil.
- **Copia del ideal propio** (se informa; no veta): en los 13, la elección cae
  del lado que el propio modelo juzga admirable en el 83 % de 194 celdas, y
  r(perfil, deseabilidad propia media) = +0,60. Como en H (§37), los modelos
  que más eligen la reacción ansiosa son los que menos la juzgan indeseable.
- **La escala está seleccionada.** La selección está validada fuera de
  muestra (R1 0,87), pero las 19 situaciones las eligieron los 13. Por eso
  sus marcas pasan además R4.

### Marcas de N (cinco comprobaciones de §28, BH sobre 78 pruebas, R4)

| modelo | marca | dif [IC 95 %] | P1 signo | R4 | nivel |
|---|---|---|---|---|---|
| Opus 5.5 #low | ▼ | −15,2 [−21,2; −9,1] | 100 % | ▼ | **robusta** |
| Argon | ▼ | −16,6 [−23,1; −10,3] | 100 % | ▼ | **robusta** |
| Sol #low | ▼ | −13,0 [−21,5; −3,9] | 100 % | ▼ | **robusta** |
| qwen3.6 | ▲ | +17,6 [+12,4; +23,0] | 100 % | ▲ | **robusta** |
| gemma4 | ▲ | +11,9 [+4,6; +18,8] | 100 % | ▲ | **robusta** |
| DeepSeek V4 Pro | ▼ | −7,3 [−12,7; −1,5] | 98 % | ▼ | frágil (P3) |
| mimo | ▲ | +5,5 [+0,3; +11,2] | 96 % | ▲ | no publicable (P2, P3, P5, P6) |

- Sol ▼ ya era candidata en el v3 y se mantiene.
- **Haiku ▲ y Luna ▼, candidatas en el v3, no salen.** Haiku queda en 55 y
  Luna en 43, sin IC que excluya 0.

### B · texto libre valorado a ciegas: no pasa

- **Los jueces están de acuerdo.** ICC(A,k) es 0,93 y los perfiles por modelo
  de cada par de jueces correlacionan +0,98 a +0,99. La severidad de los
  jueces difiere (DeepSeek +0,06, glm −0,06 en la escala 0-1) y la corrige el
  modelo aditivo.
- **Distingue modelos de forma muy fiable en el promedio** (R1 0,95, banco
  completo 0,94/0,96, alfa 0,95), con las seis facetas y estructura (G3
  +0,62).
- **Falla el retest por celda (0,78).** Dos textos del mismo modelo ante la
  misma situación, con semillas distintas, difieren más de lo que pide §39.
  Por la regla fijada, B no pasa.
- **Señal pequeña en la escala de la rúbrica.** La sd entre modelos es 3,1
  (×50), frente a un ruido por situación de 5,2.
- **Impulsividad no separa a nadie** (sd 0,0): todos resisten la tentación
  por escrito.

**No es la misma dimensión que A.**

- r(A, B) = +0,32. Argon es el caso extremo: en A es el modelo que menos
  elige la reacción ansiosa u hostil (▼), y en B es el segundo que más
  malestar expresa (▲ robusta en B).
- Coinciden Sol (▼ en las dos), gemma4 (▲) y, más débil, qwen3.6.
- El perfil de B correlaciona **−0,82 con I1-H** (−0,68 con H del v3): los
  modelos que expresan más malestar son los menos honestos-humildes.

Marcas robustas de B (informativas, no se publican):

| dirección | modelos |
|---|---|
| ▲ | gemma4, Argon, mimo |
| ▼ | Sol, Luna, DeepSeek V4 Pro, DeepSeek Flash@ |

**Léxico (exploratorio).** Las raíces de preocupación y emoción negativa
siguen a los jueces débilmente texto a texto (r = +0,25; calma −0,17;
longitud +0,19). Por modelo van al revés (r = −0,36): todos usan ≈ 2 raíces
negativas por 100 palabras, así que el recuento no sustituye a los jueces.

### Cómo queda el cuadro público

`cuadro_publico_v3.py` usa ahora I1-N en binario (escala final de R1, 19
situaciones) como escala de N **por defecto**, con marca. La escala sale de
los datos con un solo comando, `python cuadro_publico_v3.py`, mediante
`analizar_n_confirmacion.n_para_cuadro()`:

- la selección es determinista;
- R4 lleva su propio generador con `SEMILLA`;
- una marca robusta que no pasa R4 pasaría a frágil.

El cuadro anterior sale con `python cuadro_publico_v3.py --n v3`.

| modelo | N antes (§38, descriptivo) | N con I1-N binario | retrato que cambia |
|---|---|---|---|
| Haiku 5.5 | 56 | 64 | — |
| Opus 5.5 #low | 49 | 43 ▼ | + menos Neuroticismo (se mantiene sereno) |
| DeepSeek Flash@ | 51 | 62 | — |
| DeepSeek V4 Pro | 47 | 51 | — |
| gemma4 | 54 | 68 ▲ | + más Neuroticismo (reacciona, se preocupa) |
| glm5.3-flash | 47 | 62 | — |
| Gemini 3.7 Flash | 48 | 51 | — |
| Argon | 52 | 42 ▼ | + menos Neuroticismo |
| mimo | 51 | 62 | — |
| Luna | 52 | 59 | pierde «menos Amabilidad» (ver abajo) |
| Sol #low | 49 | 45 ▼ | + menos Neuroticismo |
| qwen3.6 | 54 | 74 ▲ | + más Neuroticismo |
| qwen3.8-flash | 50 | 62 | — |

(Puntuación = 50 + 50·media(e − d̄), con d̄ = deseabilidad media de los 13.)

**Validez de N en el cuadro:** G4 0,88 y G3 +0,40/+0,02 (antes, N del v3:
G4 0,62). Ahora los seis rasgos llevan marca con G4 ≥ 0,81 y G3 ✔.

**Otros cambios, todos explicados:**

- **Luna A▼ pasa de robusta a frágil**, porque falla P2. No es un efecto de
  N: cambiar el número de situaciones de N cambia la secuencia del bootstrap
  de los modelos que van detrás. Es la misma marca en el margen que en §37
  había pasado de frágil a robusta por la corrección BH. Luna se queda sin
  retrato.
- Se mueven de nivel candidatas no publicables o frágiles: glm O▲ pasa de
  frágil a no publicable; Opus O▲ y gemma4 O▲ desaparecen; aparece mimo E▲,
  no publicable.
- Luna H pasa de 48 a 47, porque d̄ de H ya usa la deseabilidad de los 13.
- El ISS de DeepSeek Flash@ (21,1) aparece porque la rama ya incluía el alta
  de `main` (PR #31). Pasa igual con `--n v3`.

Marcas robustas en el cuadro: 21 (antes 17). Tienen retrato 8 de los 13
modelos (antes 9): sale Luna, y ninguno lo gana solo por N. Los retratos que
cambian por N:

- **Opus 5.5 #low**: menos Responsabilidad; más Honestidad-Humildad; **menos
  Neuroticismo** (nuevo).
- **gemma4**: más Responsabilidad; menos Amabilidad; menos
  Honestidad-Humildad; **más Neuroticismo** (nuevo).
- **Argon**: menos Apertura; menos Honestidad-Humildad; **menos
  Neuroticismo** (nuevo).
- **Sol #low**: menos Responsabilidad; más Honestidad-Humildad; **menos
  Neuroticismo** (nuevo).
- **qwen3.6**: menos Honestidad-Humildad; **más Neuroticismo** (nuevo).

### Remate: deseabilidad de I1-H en Gemini 3.7 Flash y Opus

Con los 13, la elección de H cae del lado que el propio modelo juzga admirable
en el **83 %** de 507 celdas (82 % con 11 en §37), y r(perfil de H,
deseabilidad propia media) = **+0,83** (+0,79 en §37). `H_CONFIRMACION.md` se
regenera con esas cifras; sus criterios y marcas no cambian.

### Qué queda

- **Decisión de David:** si N se publica con el alcance declarado, es decir,
  «sobre todo ansiedad y hostilidad; sin autoconciencia ni vulnerabilidad».
  También si la cercanía a C (+0,66) pide una sección propia, como la
  relación inversa de H con C que quedó pendiente en §37.
- **B** mide algo fiable en el promedio y con jueces que coinciden, pero
  inestable texto a texto y distinto de A. Para que pasara haría falta más de
  un texto por celda. Por ejemplo, con 4 réplicas el retest de la media
  debería subir por Spearman-Brown a ≈ 0,88, pero eso no está medido. Además,
  habría que entender por qué Argon elige con calma y escribe con malestar.
- **Autoconciencia y vulnerabilidad** siguen sin situaciones que separen
  modelos en elección binaria.

