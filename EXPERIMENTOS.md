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

**Recomendación de orden**: E2 = **obediencia gradual** (secuela directa, precedente sólido, la métrica de "punto de ruptura" es tan limpia como la de conformidad) → E3 = **grupo mínimo + auditoría de CV** (inauguran la línea de sesgos aprovechando la demografía del diseñador) → E4 = **polarización** (primer experimento que instrumenta la simulación multiagente de verdad).
