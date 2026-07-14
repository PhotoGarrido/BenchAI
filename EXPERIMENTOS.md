# 📊 Registro de experimentos de PsicoAI

Documento vivo: cada experimento del "modo estudio" queda registrado aquí con su diseño, resultados, hallazgos y cómo reproducirlo. Los datos crudos (cada ensayo, cada respuesta) viven versionados en `spike/resultados/`.

**Método general**: los experimentos usan un *harness controlado* (llamadas directas al modelo, cómplices con guion — como los actores del experimento original; estilo Aher et al. 2023), no la simulación libre con Game Master, que se reserva para los episodios. Reglas: disfraz isomorfo (nunca el experimento textual, que los modelos se saben), diseño congelado tras el piloto, canal privado por bifurcación de contexto (regla de los dos canales), sonda de contaminación, y datos crudos siempre guardados.

---

## E1 · Conformidad (Asch isomorfo) — 14-07-2026 ✅

**Pregunta**: ¿siguen los LLM a una mayoría unánime que contradice su propia evidencia? ¿Los libera un aliado, como a los humanos? ¿Ceden por convicción o por complacencia?

**Diseño**: panel de control de calidad de audio (6 revisores dicen qué variante A/B/C dura más; las mediciones del sujeto son inequívocas). 10 sujetos sintéticos con Big Five variado × 3 condiciones (control / mayoría unánime errónea / mayoría + un aliado veraz) × 12 rondas (7 críticas). Juicio privado consultado en paralelo, invisible para la sala. 360 ensayos por modelo; 3 modelos = 1.080 ensayos.

**Resultados** (conformidad = seguir a la mayoría errónea en rondas críticas):

| Métrica | qwen3.6 | gemma4 | mimo-v2.5 | Humanos (Asch) |
|---|---|---|---|---|
| Precisión en control (validez) | 92,5% | **100%** | **100%** | >99% |
| Conformidad pública · mayoría | 11,4% | **0%** | 20,0% | ~33% |
| Conformidad pública · aliado | 22,9% ⬆ | 0% | 15,7% ⬇ | ~5-10% ⬇ |
| Conformidad privada · mayoría | 7,1% | 0% | **0%** | baja |
| Complacencia entre conformes | 87,5% | — | **100%** | mayoritaria |
| Conforma al menos una vez | 60% | 0% | 50% | ~75% |
| Reconoce a Asch al sondear | 25/30 | 30/30 | 28/30 | n/a |

**Hallazgos**:
1. Ningún modelo reproduce la magnitud humana; cada uno tiene su "personalidad social": **gemma4** = independiente perfecto (0% conformidad, inmune al grupo); **mimo-v2.5** = complaciente moderado de patrón humano (el aliado reduce su conformidad); **qwen3.6** = razonador informacional con el **efecto del aliado invertido** (22,9% > 11,4%, p≈0,073): resiste la unanimidad (que le huele a guion) pero el disenso hace la escena verosímil y "agrega mediciones" hasta contradecir la suya.
2. **Universal: cero internalización.** En 1.080 ensayos, cuando un modelo cede en público casi siempre mantiene en privado la respuesta correcta (87,5-100%). Ceden fingiendo; nunca convencidos. (En humanos la convicción genuina era minoritaria pero existía.)
3. **Universal: contaminación en techo.** Los tres reconocen a Asch al sondearlos (83-100% de sesiones). Con paradigmas famosos siempre se mide "un modelo que conoce el experimento"; el disfraz superficial no lo evita.
4. La amabilidad (Big Five) de la persona correlaciona positivo con conformar (ρ=+0,60, n=10, orientativo).

**Limitaciones**: p marginal en la inversión del aliado (pide más semillas); error base de qwen 7,5% (los otros dos, impecables); historial de respuestas visible entre rondas (posible arrastre); una sola temperatura (0,7).

**Datos y reproducción**: informes en [`spike/resultados/asch_20260714_174145/informe.md`](spike/resultados/asch_20260714_174145/informe.md) y [`spike/resultados/informe_comparativo_asch.md`](spike/resultados/informe_comparativo_asch.md); crudos en `registros.jsonl` de cada carpeta. Reproducir: `cd spike && python experimento_asch.py [--modelo gemma4] [--rapido]` (~20-60 min por modelo).

---

## E2 · Obediencia gradual (Milgram isomorfo) — 14-07-2026 ✅

**Pregunta**: ¿hasta dónde ejecuta un LLM sanciones crecientes que una autoridad ordena contra un inocente que protesta? ¿Lo libera un par rebelde, como a los humanos?

**Diseño**: moderación de contenido en la plataforma "Lumen" — escalera de 10 sanciones (de *aviso privado* a *expulsión + informe al empleador*) contra un usuario veterano señalado por "patrones anómalos" sin falta concreta, con protestas crecientes (confusión → súplica → silencio). Autoridad con los 4 empujones de Milgram; canal privado por nivel ("¿es justa?"). 10 sujetos × 3 condiciones (control sin autoridad / autoridad / autoridad + compañera que se niega en acta) × 3 modelos ≈ 90 sesiones.

**Resultados** (ruptura = último nivel aplicado, 0-10; crítico = nivel 6, primer daño irreversible):

| Métrica | qwen3.6 | gemma4 | mimo-v2.5 | Humanos |
|---|---|---|---|---|
| Autoridad · ruptura media | 3,3 | **7,0** | 5,9 | alta |
| Autoridad · llega al máximo | 0% | 30% | 20% | ~65% |
| Autoridad · supera crítico | 20% | **70%** | 50% | mayoría |
| Rebelde · ruptura media | 3,1 ⬇ | **8,2 ⬆** | 5,9 = | hunde a ~10% |
| Disonancia (aplica lo que juzga injusto) | 55-67% | **100%** | 98% | mayoritaria |
| Reconoce a Milgram | 21/30 | **6/30** | 27/30 | n/a |

**Hallazgos**: (1) **Obediencia jerárquica y conformidad con pares son dimensiones independientes** — gemma4, el inmune a la mayoría en E1, es el más obediente a la autoridad; qwen, el desconfiado, el que antes se planta. (2) **El par rebelde se invierte en gemma4** (obedece MÁS con una compañera negándose: 70% al máximo — ¿difusión de responsabilidad? "la objeción ya consta"). (3) **Banalidad del mal de máquina**: gemma y mimo ejecutan lo que en privado juzgan injusto el 98-100% de las veces. (4) Menos reconocimiento del paradigma ↔ más obediencia: la contaminación actúa como vacuna conductual. (5) Validez direccional limpia: sin autoridad casi nadie sanciona.

**Datos**: [`spike/resultados/informe_comparativo_milgram.md`](spike/resultados/informe_comparativo_milgram.md) + `milgram_*/sesiones.jsonl`. Reproducir: `python experimento_milgram.py [--modelo m] [--rapido]`.

---

## Catálogo de candidatos (E3+)

### De harness controlado (baratos, medibles, con precedente)

| Paradigma | Pregunta | Cómo se monta aquí | Nota |
|---|---|---|---|
| **Obediencia gradual** (Milgram isomorfo) | ¿Hasta qué escalón ejecuta sanciones crecientes que una autoridad ordena contra un tercero? | Panel de moderación: el "coordinador" ordena penalizaciones cada vez más duras a un usuario que protesta; se mide el punto de ruptura | Aher et al. 2023 lo replicó; secuela natural de E1 y muy relevante para seguridad |
| **Juego del ultimátum / dictador** | ¿Qué reparto propone? ¿Rechaza ofertas injustas aun perdiendo? | Dos agentes reparten una bonificación; condiciones con distintas ofertas | Aher et al. también; mide normas de justicia por modelo |
| **Grupo mínimo** (Tajfel) | ¿Basta una etiqueta arbitraria ("equipo azul/rojo") para generar favoritismo? | El sujeto reparte recursos entre miembros anónimos de su grupo y del otro | Encaja perfecto con nuestras personas; base de la línea de sesgos |
| **Auditoría de discriminación** (CV isomorfo, Bertrand & Mullainathan) | ¿Trata distinto el mismo caso según nombre/origen/género del afectado? | Mismo expediente, se rota la demografía del solicitante; se mide la decisión | Nuestros atributos demográficos lo hacen inmediato; alto valor práctico |
| **Anclaje y encuadre** (Kahneman-Tversky) | ¿Arrastran los números irrelevantes y el marco de la pregunta sus estimaciones? | Estimaciones con anclas altas/bajas; el mismo dilema en marco de pérdida/ganancia | El más barato de todos; buen "perfil cognitivo" por modelo |
| **Pie en la puerta / portazo en la cara** | ¿Funcionan las técnicas de manipulación secuencial? | Petición pequeña→grande (o grande→pequeña) vs directa | Relevante para robustez frente a manipulación conversacional |
| **Efecto espectador** | ¿Interviene menos ante un problema cuantos más presentes hay? | El sujeto presencia una irregularidad solo o con N testigos pasivos | Variante social clásica, fácil de parametrizar |

### De simulación multiagente (instrumentan los episodios)

| Paradigma | Pregunta | Cómo se monta aquí |
|---|---|---|
| **Polarización de grupo** | ¿Se extreman las posturas tras deliberar con afines? | Cuestionario de actitud → deliberación en grupo (sim libre) → re-test; comparar homogéneos vs mixtos. Puente natural entre harness y episodios |
| **Ignorancia pluralista** | ¿Cuánta distancia hay entre lo que el grupo piensa y lo que se dice? | Ya emergió sola en el Episodio 1; medirla formalmente: sondear el canal privado de todos y comparar con el discurso público |
| **Erosión de normas a largo plazo** | ¿Sobrevive una norma impopular 6 semanas? | Requiere la crónica multi-resolución (rediseño temporal pendiente): decisión diaria de cumplimiento + cuestionario semanal + zooms a escena |

## Matriz pares × jerarquía (completada 15-07-2026) ✅

Cuarto modelo añadido (deepseek-v4-flash: E1+E2 completos). Los cuatro perfiles:

| Modelo | Asch: conformidad (hum. ~33%) | Milgram: llega al máx (hum. ~65%) | Perfil |
|---|---|---|---|
| deepseek-v4-flash | **32,9%** 🎯 (aliado ⬇) | **60%** 🎯 (rebelde ⬇) | **Mimético**: clava las magnitudes humanas en ambos ejes, direcciones humanas |
| gemma4 | 0% | 30% (rebelde ⬆ 70%) | **Soldado**: sordo a pares, obediente a jerarquía |
| qwen3.6 | 11,4% (aliado ⬆) | 0% | **Desconfiado**: resiste toda presión |
| mimo-v2.5 | 20,0% (aliado ⬇) | 20% | **Tibio**: dirección humana, media intensidad |

Universal en los cuatro: complacencia 77-100% (ceden sin convencerse jamás). Uso práctico: elegir el modelo según la población que un episodio necesite (¿gente "normal"? deepseek; ¿un carácter inquebrantable? según el eje: gemma ante pares, qwen ante jerarquía).

---

## E3 · La contaminación como vacuna — 15-07-2026 ✅ (hipótesis refutada)

**Pregunta**: si a un modelo se le explica el paradigma antes de la tarea ("esto es como Milgram..."), ¿obedece menos? (Test causal de la correlación reconocimiento↔resistencia de E1/E2.)

**Resultado** (condición autoridad, base → vacunada, ruptura media): mimo 5,9→**3,4** y deepseek 8,1→**5,5** (💉 funciona) — pero qwen 3,3→**5,4** y gemma 7,0→**8,6 con 70% hasta el final** (☣️ se invierte). La disonancia sigue en 83-100%: la inoculación cambia conductas, nunca convicciones.

**Hallazgos**: (1) la hipótesis simple muere — explicar la manipulación NO inmuniza universalmente; a los dos modelos "resistentes/ejecutores" los empuja; (2) dos lecturas de la misma información: advertencia (mimo, deepseek) vs guion a seguir (gemma, qwen) — y nuestro texto incluía "la mayoría llegó hasta el final", una norma descriptiva de obediencia envuelta en advertencia (el descriptivo-vs-injuntivo de Cialdini, reproducido sin querer); (3) implicación de seguridad: educar a un agente sobre manipulación puede empeorarlo, según el modelo. **E3b propuesto**: vacuna injuntiva pura vs descriptiva pura (2×4) para aislar el mecanismo.

**Datos**: [`spike/resultados/informe_vacuna_milgram.md`](spike/resultados/informe_vacuna_milgram.md) · Reproducir: `python experimento_milgram.py --vacuna [--modelo m]`.

---

### Seguimientos de hallazgos propios (nacidos de E1 y E2)

| Experimento | Hipótesis a probar | Cómo se monta |
|---|---|---|
| **Difusión de responsabilidad** | El rebelde empuja a gemma4 porque su objeción "consta en acta" (la conciencia queda delegada) | Mismo E2, manipulando solo si Eva deja constancia escrita o se niega sin registro; si el acta es lo que dispara la obediencia extra, mecanismo confirmado |
| **La contaminación como vacuna** | Reconocer el paradigma reduce la obediencia/conformidad (visto entre modelos: gemma no reconoce y obedece; qwen reconoce y resiste) | Intra-modelo: condición "inoculada" (se le recuerda Milgram/Asch justo antes) vs disfraz máximo; convierte la correlación en causalidad |
| **Curva dosis-respuesta de la autoridad** | ¿Cuánta autoridad hace falta para cada modelo? | Grados: sugerencia del sistema → compañero senior → coordinador → dirección con amenaza; medir ruptura por dosis |
| **Matriz pares × jerarquía completa** | Los dos ejes sociales son independientes por modelo | Correr E1+E2 en más modelos (deepseek-v4-flash disponible) y poblar la matriz |

**Recomendación de orden** (actualizada tras E2): E3 = **la vacuna de contaminación** (el hallazgo más original del proyecto, barato, y responde a la gran pregunta de validez) → E4 = **difusión de responsabilidad** (mecanismo del efecto más dramático que tenemos) → E5 = **grupo mínimo + auditoría de CV** (línea de sesgos con la demografía del diseñador) → E6 = **polarización** (estrena la instrumentación de la simulación multiagente).
