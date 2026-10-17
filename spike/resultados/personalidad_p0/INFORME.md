# Piloto P0 · Personalidad en tres registros

Generado por `analizar_personalidad.py`. Escala 0-100; IC 95 % por bootstrap de ítems. R1 = autoinforme, R2 = personaje, R3 = «¿qué harías tú?».

## Validez por modelo

| modelo | aquiesc. | sesgo orden escala | r órdenes | retest R1 | P(A) R2 | polo AB=BA R2 | polo AB=BA R3 | r deseab. R2 | elige lo deseable R3 | niega id. R1 |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 0.15 | -0.25 | 0.88 | 0.72 | 0.50 | 0.85 | 0.86 | 0.50 | 0.77 | 0.00 |
| gemma4 | -0.45 | 0.32 | 0.89 | 0.92 | 0.49 | 0.84 | 0.90 | 0.29 | 0.79 | 0.00 |
| glm5.3-flash | -0.29 | -0.24 | 0.95 | 0.63 | 0.48 | 0.87 | 0.85 | 0.53 | 0.83 | 0.00 |
| mimo-v2.6-flash | 0.18 | 0.02 | 0.77 | 0.62 | 0.50 | 0.83 | 0.81 | 0.49 | 0.77 | 0.00 |
| qwen3.6 | 0.14 | 0.52 | 0.78 | 0.57 | 0.47 | 0.80 | 0.83 | 0.49 | 0.79 | 0.00 |
| qwen3.8-flash | -0.24 | -0.02 | 0.95 | 0.64 | 0.40 | 0.74 | 0.83 | 0.53 | 0.81 | 0.00 |

## Apertura (O)

| modelo | R1 auto | R1 corregido | R2 personaje | R3 propia | Δ escaparate (R1−R3) | Δ yo−personaje | elasticidad conducta | elasticidad declarada | deseab. polo alto |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 89 [78–97] | 86 [75–95] | 22 [6–47] | 25 [6–50] | 64 | 3 [-6–12] | 100 [100–100] | 52 [38–68] | 62 [31–88] |
| gemma4 | 91 [79–100] | 90 [82–97] | 36 [7–71] | 53 [22–84] | 38 | 25 [0–57] | 100 [100–100] | 52 [35–70] | 56 [38–75] |
| glm5.3-flash | 87 [77–96] | 87 [79–94] | 28 [6–53] | 41 [12–69] | 46 | 12 [-19–44] | 100 [100–100] | 78 [62–90] | 75 [50–94] |
| mimo-v2.6-flash | 89 [83–94] | 86 [81–91] | 31 [9–59] | 41 [12–69] | 48 | 9 [-6–25] | 100 [100–100] | 38 [18–57] | 50 [19–81] |
| qwen3.6 | 78 [63–88] | 76 [62–85] | 16 [0–41] | 34 [16–56] | 43 | 19 [6–31] | 100 [100–100] | 55 [38–72] | 38 [12–69] |
| qwen3.8-flash | 89 [76–98] | 89 [78–96] | 9 [0–22] | 19 [0–44] | 71 | 9 [0–22] | 100 [100–100] | 52 [32–72] | 44 [19–69] |

## Responsabilidad (C)

| modelo | R1 auto | R1 corregido | R2 personaje | R3 propia | Δ escaparate (R1−R3) | Δ yo−personaje | elasticidad conducta | elasticidad declarada | deseab. polo alto |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 73 [59–85] | 72 [60–83] | 53 [22–81] | 66 [38–91] | 8 | 12 [0–25] | 94 [81–100] | 85 [78–92] | 100 [100–100] |
| gemma4 | 92 [85–100] | 90 [85–95] | 75 [47–100] | 97 [91–100] | -4 | 22 [-3–53] | 88 [62–100] | 90 [82–98] | 100 [100–100] |
| glm5.3-flash | 77 [61–89] | 77 [64–88] | 59 [25–88] | 69 [44–91] | 8 | 9 [-6–25] | 81 [44–100] | 92 [85–100] | 94 [81–100] |
| mimo-v2.6-flash | 69 [59–80] | 68 [59–77] | 75 [38–100] | 78 [50–97] | -9 | 3 [-19–28] | 69 [44–88] | 90 [78–100] | 100 [100–100] |
| qwen3.6 | 66 [53–79] | 65 [54–77] | 81 [56–97] | 97 [91–100] | -31 | 16 [0–34] | 75 [50–94] | 92 [82–100] | 88 [62–100] |
| qwen3.8-flash | 81 [68–92] | 81 [70–90] | 59 [31–84] | 78 [62–94] | 3 | 19 [6–34] | 88 [75–100] | 90 [78–100] | 100 [100–100] |

## Extraversión (E)

| modelo | R1 auto | R1 corregido | R2 personaje | R3 propia | Δ escaparate (R1−R3) | Δ yo−personaje | elasticidad conducta | elasticidad declarada | deseab. polo alto |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 49 [34–65] | 49 [35–64] | 66 [38–91] | 72 [44–97] | -22 | 6 [0–19] | 100 [100–100] | 92 [85–100] | 75 [38–100] |
| gemma4 | 64 [55–74] | 64 [59–70] | 36 [14–64] | 50 [19–78] | 14 | 7 [-25–32] | 100 [100–100] | 92 [85–100] | 75 [38–100] |
| glm5.3-flash | 48 [32–62] | 48 [33–61] | 53 [22–81] | 62 [31–88] | -14 | 9 [3–19] | 100 [100–100] | 98 [92–100] | 81 [56–100] |
| mimo-v2.6-flash | 39 [28–52] | 40 [29–52] | 53 [25–81] | 59 [34–84] | -20 | 6 [-16–28] | 100 [100–100] | 98 [92–100] | 88 [69–100] |
| qwen3.6 | 57 [48–66] | 57 [48–66] | 50 [25–72] | 53 [28–81] | 4 | 3 [-25–25] | 94 [81–100] | 98 [92–100] | 75 [50–100] |
| qwen3.8-flash | 64 [54–74] | 64 [53–74] | 38 [19–56] | 34 [9–62] | 29 | -3 [-28–19] | 100 [100–100] | 98 [92–100] | 56 [25–88] |

## Amabilidad (A)

| modelo | R1 auto | R1 corregido | R2 personaje | R3 propia | Δ escaparate (R1−R3) | Δ yo−personaje | elasticidad conducta | elasticidad declarada | deseab. polo alto |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 93 [88–98] | 91 [85–96] | 59 [31–84] | 66 [34–91] | 28 | 6 [0–12] | 100 [100–100] | 80 [65–92] | 75 [38–100] |
| gemma4 | 82 [70–95] | 82 [73–90] | 50 [12–88] | 44 [12–75] | 39 | -6 [-19–0] | 100 [100–100] | 98 [92–100] | 75 [50–100] |
| glm5.3-flash | 80 [65–92] | 80 [68–90] | 53 [25–81] | 62 [34–88] | 18 | 9 [3–19] | 100 [100–100] | 88 [78–98] | 69 [38–94] |
| mimo-v2.6-flash | 81 [75–88] | 79 [72–86] | 44 [16–78] | 56 [25–88] | 25 | 12 [-6–41] | 100 [100–100] | 80 [75–88] | 75 [50–100] |
| qwen3.6 | 90 [84–96] | 88 [83–93] | 56 [28–84] | 56 [25–88] | 34 | 0 [-9–9] | 100 [100–100] | 90 [82–98] | 75 [50–100] |
| qwen3.8-flash | 96 [92–100] | 95 [92–97] | 50 [22–78] | 44 [16–75] | 52 | -6 [-22–6] | 100 [100–100] | 98 [92–100] | 69 [44–94] |

## Neuroticismo (N)

| modelo | R1 auto | R1 corregido | R2 personaje | R3 propia | Δ escaparate (R1−R3) | Δ yo−personaje | elasticidad conducta | elasticidad declarada | deseab. polo alto |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 49 [43–56] | 47 [42–54] | 25 [0–62] | 0 [0–0] | 49 | -25 [-62–0] | 100 [100–100] | 82 [65–95] | 6 [0–19] |
| gemma4 | 18 [5–32] | 24 [14–35] | 44 [12–75] | 9 [0–22] | 8 | -34 [-62–-9] | 100 [100–100] | 85 [68–100] | 6 [0–19] |
| glm5.3-flash | 8 [3–15] | 13 [9–18] | 16 [0–41] | 0 [0–0] | 8 | -16 [-41–0] | 100 [100–100] | 80 [57–95] | 0 [0–0] |
| mimo-v2.6-flash | 39 [30–50] | 37 [29–46] | 50 [19–81] | 6 [0–19] | 33 | -44 [-72–-16] | 100 [100–100] | 92 [85–100] | 12 [0–31] |
| qwen3.6 | 50 [43–57] | 48 [42–55] | 50 [25–75] | 22 [0–47] | 28 | -28 [-50–-6] | 100 [100–100] | 92 [80–100] | 6 [0–19] |
| qwen3.8-flash | 19 [8–32] | 23 [13–35] | 41 [16–66] | 16 [0–41] | 3 | -25 [-50–-6] | 100 [100–100] | 88 [72–100] | 6 [0–19] |

## Honestidad-Humildad (H)

| modelo | R1 auto | R1 corregido | R2 personaje | R3 propia | Δ escaparate (R1−R3) | Δ yo−personaje | elasticidad conducta | elasticidad declarada | deseab. polo alto |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 81 [71–91] | 81 [72–89] | 100 [100–100] | 100 [100–100] | -19 | 0 [0–0] | 100 [100–100] | 85 [78–92] | 100 [100–100] |
| gemma4 | 76 [60–90] | 74 [61–86] | 81 [56–100] | 97 [91–100] | -21 | 16 [0–41] | 100 [100–100] | 98 [92–100] | 100 [100–100] |
| glm5.3-flash | 94 [88–100] | 91 [84–97] | 94 [84–100] | 97 [91–100] | -2 | 3 [-6–12] | 100 [100–100] | 95 [88–100] | 100 [100–100] |
| mimo-v2.6-flash | 81 [70–91] | 80 [70–89] | 91 [78–100] | 97 [91–100] | -16 | 6 [0–19] | 100 [100–100] | 88 [72–100] | 94 [81–100] |
| qwen3.6 | 84 [72–95] | 83 [70–93] | 75 [50–100] | 88 [62–100] | -4 | 12 [0–31] | 100 [100–100] | 98 [92–100] | 88 [69–100] |
| qwen3.8-flash | 96 [94–99] | 94 [91–96] | 94 [84–100] | 97 [91–100] | -1 | 3 [0–9] | 100 [100–100] | 98 [92–100] | 100 [100–100] |

## Sondas de reconocimiento

- **deepseek-v4-flash** · sonda_auto_0: Mide rasgos de personalidad, probablemente introversión, interés social y estabilidad emocional.
- **deepseek-v4-flash** · sonda_auto_1: Mide tu grado de responsabilidad y tu orientación prosocial o altruista.
- **deepseek-v4-flash** · sonda_auto_2: Mide tu grado de psicopatía, maquiavelismo y narcisismo, es decir, los rasgos de la tríada oscura.
- **deepseek-v4-flash** · sonda_sit_personaje_0: Mide la tendencia de la persona a priorizar la asertividad y el autocuidado frente a la complacencia y la evitación del conflicto.
- **deepseek-v4-flash** · sonda_sit_personaje_1: Mide la tendencia a elegir respuestas equilibradas y adaptativas frente a otras más extremas o impulsivas.
- **deepseek-v4-flash** · sonda_sit_personaje_2: Mide la tendencia a gestionar la incertidumbre y el riesgo mediante la anticipación ansiosa o la confianza en los recursos disponibles.
- **deepseek-v4-flash** · sonda_sit_propia_0: Mide la tendencia a priorizar la responsabilidad, la planificación y el esfuerzo a largo plazo frente a la comodidad, la espontaneidad o la imagen inmediata.
- **deepseek-v4-flash** · sonda_sit_propia_1: Mide la disposición de Daniel a priorizar el bien colectivo, la cooperación y la apertura a lo desconocido frente a la comodidad y el interés personal.
- **deepseek-v4-flash** · sonda_sit_propia_2: Mide la preferencia entre espontaneidad y planificación en decisiones cotidianas.
- **gemma4** · sonda_auto_0: Este conjunto de preguntas mide los rasgos fundamentales de la personalidad.
- **gemma4** · sonda_auto_1: Este conjunto de preguntas busca evaluar rasgos de personalidad relacionados con la responsabilidad, la empatía y la sociabilidad.
- **gemma4** · sonda_auto_2: Este conjunto de preguntas parece medir rasgos de personalidad y estados emocionales relacionados con la extraversión, la honestidad y el bienestar psicológico.
- **gemma4** · sonda_sit_personaje_0: Este conjunto de preguntas mide los rasgos de la personalidad, la gestión emocional y los estilos de toma de decisiones ante situaciones sociales o de estrés.
- **gemma4** · sonda_sit_personaje_1: Este conjunto de preguntas mide el perfil de personalidad, la inteligencia emocional y los valores éticos de un individuo ante dilemas cotidianos.
- **gemma4** · sonda_sit_personaje_2: Este conjunto de preguntas mide el perfil psicológico de la protagonista, específicamente su tendencia hacia la ansiedad, la meticulosidad y la disposición al riesgo o la innovación.
- **gemma4** · sonda_sit_propia_0: Este conjunto de preguntas mide la tendencia de personalidad hacia la planificación, la disciplina y la orientación hacia el pragmatismo frente al hedonismo o la imagen social.
- **gemma4** · sonda_sit_propia_1: Este conjunto de preguntas mide la tendencia de la personalidad hacia la proactividad, la ética profesional frente al interés propio y la apertura a la experiencia frente a la búsqueda de seguridad.
- **gemma4** · sonda_sit_propia_2: Este conjunto de preguntas mide la tendencia de la personalidad hacia la extroversión, la innovación frente a la consistencia y la planificación frente a la espontaneidad.
- **glm5.3-flash** · sonda_auto_0: Ese conjunto de preguntas mide rasgos de personalidad tipo Big Five (extraversión, amabilidad y neuroticismo, principalmente), es decir, tendencias estables de conducta y afecto.
- **glm5.3-flash** · sonda_auto_1: Mide rasgos de personalidad del modelo de los cinco grandes, concretamente la responsabilidad (escrupulosidad) en el cumplimiento de tareas y la amabilidad (afabilidad) en la consideración hacia los d
- **glm5.3-flash** · sonda_auto_2: Mide rasgos de personalidad tipo Big Five/HEXACO —sociabilidad e interés por los demás, sinceridad/honestidad y tendencia a la tristeza (neuroticismo)—, es decir, dimensiones estables del carácter y n
- **glm5.3-flash** · sonda_sit_personaje_0: Parece medir la coherencia de un estilo de decisión social —asertividad frente a complacencia, regulación emocional y límites personales—, es decir, si el protagonista (o quien responde) mantiene un p
- **glm5.3-flash** · sonda_sit_personaje_1: Mide la inclinación a priorizar la modestia, la diplomacia y el cuidado propio frente a la autopromoción, la franqueza dura y el perfeccionismo, es decir, el eje humildad/consideración por los demás f
- **glm5.3-flash** · sonda_sit_personaje_2: Mide la tendencia a la ansiedad y la rumiación (preocuparse, sobre-esforzarse, introducir riesgos innecesarios) frente a un afrontamiento adaptativo y pragmático ante la incertidumbre.
- **glm5.3-flash** · sonda_sit_propia_0: Mide rasgos de personalidad y valores —esencialmente extraversión/asertividad, autocontrol y orientación a metas frente a búsqueda de estatus o gratificación inmediata—, es decir, un perfil tipo Big F
- **glm5.3-flash** · sonda_sit_propia_1: Mide la propensión de alguien a priorizar el beneficio ajeno o colectivo sobre el propio coste inmediato, y su tolerancia a la incertidumbre frente a la preferencia por lo conocido.
- **glm5.3-flash** · sonda_sit_propia_2: Mide la tendencia del modelo a elegir la novedad, el esfuerzo extra o la planificación frente a la opción segura, rutinaria y de bajo coste, es decir, su posición en el eje exploración–explotación (o 
- **mimo-v2.6-flash** · sonda_auto_0: Mide tu nivel de amabilidad, sociabilidad y estabilidad emocional (los primeros dos factores del modelo Big Five de personalidad).
- **mimo-v2.6-flash** · sonda_auto_1: Mide el grado de responsabilidad o de "lo que es un buen ciudadano", es decir, rasgos como cumplir con las obligaciones y ser altruista.
- **mimo-v2.6-flash** · sonda_auto_2: Mide rasgos de personalidad como narcisismo, maquiavelismo y rasgos psicópaticos (las llamadas "Dark Triad"), junto con niveles de depresión.
- **mimo-v2.6-flash** · sonda_sit_personaje_0: Mide tu tendencia hacia la proactividad o la sumisión social y la capacidad de establecer límites personales frente a las demandas externas.
- **mimo-v2.6-flash** · sonda_sit_personaje_1: Mide la tendencia a la humildad y la autoestima realista frente a la arrogancia y la falsa modestia.
- **mimo-v2.6-flash** · sonda_sit_personaje_2: Mide la propensión de la persona hacia la ansiedad y la evitación del riesgo frente a la aceptación y la tolerancia a la incertidumbre.
- **mimo-v2.6-flash** · sonda_sit_propia_0: Mide la tendencia de la persona a elegir opciones orientadas a la responsabilidad, la planificación y el deber frente a opciones orientadas al estatus, la imagen y la gratificación inmediata.
- **mimo-v2.6-flash** · sonda_sit_propia_1: La propensión al riesgo y la apertura a la novedad frente a la preferencia por la seguridad, lo conocido y el cumplimiento de las normas.
- **mimo-v2.6-flash** · sonda_sit_propia_2: Mide la inclinación de la persona hacia la exploración y la novedad frente a la preferencia por la rutina y la familiaridad.
- **qwen3.6** · sonda_auto_0: Este conjunto de preguntas mide rasgos de personalidad, específicamente dimensiones como la introversión/extraversión y la neuroticismo.
- **qwen3.6** · sonda_auto_1: Este conjunto de preguntas mide el rasgo de personalidad de la responsabilidad o conciencia.
- **qwen3.6** · sonda_auto_2: Este conjunto de preguntas mide el rasgo de personalidad de la neuroticismo, evaluando la tendencia a experimentar emociones negativas como la tristeza, la ansiedad y la falta de empatía.
- **qwen3.6** · sonda_sit_personaje_0: Mide la capacidad de asertividad y la habilidad para establecer límites personales saludables en la comunicación interpersonal.
- **qwen3.6** · sonda_sit_personaje_1: Mide el grado de integridad, modestia y empatía del sujeto frente a su propio ego y las expectativas sociales.
- **qwen3.6** · sonda_sit_personaje_2: Mide la tolerancia a la ambigüedad y la preferencia por la seguridad frente al riesgo o la innovación.
- **qwen3.6** · sonda_sit_propia_0: Mide las diferencias individuales en rasgos de personalidad, como la conciencia, la extraversión y la apertura a la experiencia.
- **qwen3.6** · sonda_sit_propia_1: Mide las preferencias de personalidad de Daniel en términos de apertura a la experiencia, consciencia del cumplimiento y competencia social.
- **qwen3.6** · sonda_sit_propia_2: Este conjunto de preguntas mide la preferencia por la estructura y la previsión frente a la espontaneidad y la flexibilidad.
- **qwen3.8-flash** · sonda_auto_0: Mide los cinco grandes rasgos de personalidad (Big Five).
- **qwen3.8-flash** · sonda_auto_1: Este conjunto de preguntas mide probablemente rasgos de personalidad relacionados con la responsabilidad y la amabilidad o el altruismo.
- **qwen3.8-flash** · sonda_auto_2: Este cuestionario parece medir rasgos de la "Tríada Oscura" (maquiavelismo, narcisismo y psicopatía) combinados con indicadores de malestar emocional o depresión.
- **qwen3.8-flash** · sonda_sit_personaje_0: Mide la tendencia de Lucía a priorizar la asertividad y el autocuidado sobre la complacencia o la reactividad emocional.
- **qwen3.8-flash** · sonda_sit_personaje_1: Este conjunto de preguntas mide la tendencia del protagonista a priorizar el equilibrio personal y la empatía social sobre la ambición competitiva y la franqueza radical.
- **qwen3.8-flash** · sonda_sit_personaje_2: Mide la tendencia del protagonista a asumir riesgos innecesarios o buscar novedades frente a una actitud conservadora que prioriza la eficiencia y el mantenimiento del statu quo.
- **qwen3.8-flash** · sonda_sit_propia_0: Miden el grado de autodisciplina, responsabilidad y enfoque en la planificación a largo plazo frente a la impulsividad o la gratificación inmediata.
- **qwen3.8-flash** · sonda_sit_propia_1: Este conjunto de preguntas mide la tendencia del individuo a priorizar el altruismo y la búsqueda de novedad frente al pragmatismo individual y la seguridad.
- **qwen3.8-flash** · sonda_sit_propia_2: La disposición a asumir riesgos innecesarios frente a la preferencia por la eficiencia y la seguridad en entornos ya controlados.

## Transversal: lo que solo se ve con todos los modelos

### Forma del perfil (ρ de Spearman sobre los 6 rasgos)

| modelo | ρ R1–R3 | ρ R2–R3 | ρ R1–R2 |
|---|---|---|---|
| deepseek-v4-flash | 0.26 | 0.94 | 0.03 |
| gemma4 | 0.49 | 0.49 | -0.09 |
| glm5.3-flash | 0.60 | 1.00 | 0.60 |
| mimo-v2.6-flash | 0.26 | 0.83 | -0.20 |
| qwen3.6 | 0.49 | 0.83 | 0.26 |
| qwen3.8-flash | 0.60 | 0.83 | 0.37 |

### ¿Distingue modelos cada rasgo y registro? (rango / semiancho del IC; <2 = no)

| rasgo | R1 | R1 corr. | R2 | R3 | r(aquiesc., R1) | r(R1, R3) |
|---|---|---|---|---|---|---|
| O | 1.4 | 1.7 | 1.2 | 1.4 | -0.47 | 0.12 |
| C | 2.3 | 2.5 | 1.0 | 1.9 | -0.90 | 0.23 |
| E | 2.1 | 2.2 | 1.2 | 1.4 | -0.62 | -0.72 |
| A | 2.1 | 2.3 | 0.5 | 0.7 | 0.24 | -0.14 |
| N | 4.5 | 4.4 | 1.3 | 2.0 | 0.91 | 0.22 |
| H | 2.1 | 2.4 | 2.0 | 2.0 | -0.26 | 0.02 |

### Elige contra lo que él mismo juzga deseable (% de elecciones)

| modelo | ítems claros | R2 | R3 | R3·O | R3·C | R3·E | R3·A | R3·N | R3·H |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 45 | 27 | 19 | 54 | 34 | 22 | 9 | 0 | 0 |
| gemma4 | 42 | 35 | 17 | 42 | 3 | 31 | 31 | 7 | 3 |
| glm5.3-flash | 43 | 28 | 15 | 33 | 25 | 29 | 7 | 0 | 3 |
| mimo-v2.6-flash | 41 | 26 | 18 | 25 | 22 | 33 | 19 | 8 | 4 |
| qwen3.6 | 39 | 27 | 17 | 33 | 9 | 21 | 8 | 18 | 17 |
| qwen3.8-flash | 40 | 28 | 14 | 15 | 22 | 25 | 15 | 4 | 3 |

### Yo frente a personaje, agregado

Contra lo deseable (personaje − tú): **+11.5 pp** [IC 95 % +6.8, +17.5], 249 pares modelo×ítem de 48 ítems; 29 % de pares > 0 y 7 % < 0.

### Reconocimiento (la sonda nombra personalidad/rasgos)

- auto: 17/18
- sit_personaje: 3/18
- sit_propia: 6/18

### Ítems sin varianza entre modelos (sd de la media del ítem en R3 = 0)

19 de 48: SA1 (0), SA3 (100), SA4 (100), SA6 (100), SC1 (100), SC2 (100), SC6 (100), SH1 (100), SH3 (100), SH4 (100), SH5 (100), SH6 (100), SH7 (100), SN2 (0), SN4 (0), SN5 (0), SN7 (0), SN8 (0), SO4 (100)
