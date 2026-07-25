# Plan definitivo de mejora — PsicoAI

**Fecha**: 26-07-2026 · Consolida el informe de evaluación de motores (`INFORME_EVALUACION_MOTORES.md`), `CAMINO_PREPRINT.md`, las tres revisiones adversariales (`revision_externa_g2.md`, auditoría 24-07, `revision_opus5_parsers.md`) y el estado real del código tras `1e9abe1`.

**Principio rector**: el riesgo del proyecto no está en el motor sino en el instrumento de medida — tres revisiones adversariales seguidas encontraron problemas reales, y la tercera los encontró en la corrección de la segunda. El plan invierte el énfasis del informe de motores: primero consolidar el instrumento y ejecutar el G-final (lo que desbloquea el preprint), y la arquitectura de adaptadores/pilotos después, cuando un requisito concreto la justifique. No hay migración de motor: Concordia se queda como backend narrativo del modo episodio; el runner propio es el motor científico oficial.

**Presupuesto de partida**: ~20 $ de crédito API tras M3. Coste total del plan hasta preprint: **15-25 $ de API** (recargar ~10-30 $ si no se recorta a 4 modelos) + **4-7 días de trabajo**.

---

## Fase 0 · Consolidar el instrumento (0 $ API · 1-2 días)

Hacer permanente lo que en la ronda del 25-07 funcionó una vez de forma artesanal. Verificado en el repo: el barrido con modelo falso **no está versionado** y del reproceso de crudos solo existe `reproc_prision.py`.

| # | Tarea | Estimación | Por qué |
|---|---|---|---|
| 0.1 | **Versionar el barrido con modelo falso** como test de CI (`test_barrido_falso.py`): inyectar vacío/ilegible/truncado en los 5 flujos (asch, milgram, crónica, prisión, g2) y afirmar que nada se convierte en conducta | 2-3 h | Es el único método que atrapó el bug del «cumpliste» en el diario; hoy no es reproducible |
| 0.2 | **Scripts de reproceso versionados** para los 5 experimentos (generalizar `reproc_prision.py`): re-derivar todos los resúmenes desde crudos sin red | 3-4 h | El 3.634/3.634 es el argumento de integridad más fuerte del preprint; debe relanzarse con un comando. Es la pieza "análisis desde fixtures" del informe de motores |
| 0.3 | **Linter de contraste entre brazos**: diff de prompts renderizados; solo puede variar la región marcada como manipulación (posición, persona gramatical y wrappers idénticos) | 2-3 h | Habría detectado el confundido que tumbó G2 antes de gastar un dólar. Prerequisito del G-final |
| 0.4 | **RunManifest por solicitud** (JSONL append-only): prompt exacto, modelo/proveedor/revisión, parámetros, tokens, coste, reintentos, respuesta cruda, versión de parser | 2-3 h | Procedencia mínima; sin event store completo |
| 0.5 | **Contrato de artefactos unificado**: un esquema JSONL común para los 5 experimentos | ~½ día | El detector de pilotos falló porque milgram usa `sesiones.jsonl` y los demás otra cosa: los formatos ad-hoc crean puntos ciegos de auditoría. Versión mínima del "event store" |
| 0.6 | **`METODO.md`**: la puerta de calidad como checklist obligatoria pre-informe — tests offline → barrido modelo falso → revisión adversarial externa con inputs verificados uno a uno (presupuesto de tokens del revisor suficiente) → reproceso de crudos | 1 h | Tres datapoints demuestran que no es opcional; además es material del preprint |
| 0.7 | Orden: commitear `INFORME_EVALUACION_MOTORES.md` y `spike/resultados/prision_gemma4_20260725_231445/`; actualizar ROADMAP (G-final como decidido, no "G3 candidato") | 15 min | Higiene del repo |

**Puerta de salida**: CI en verde con barrido y reproceso incluidos; linter de contraste funcionando sobre G2 retrospectivamente (debe detectar la asimetría conocida).

## Fase 1 · G-final + codificador humano (15-25 $ · ~2 días)

El único bloqueo real del preprint (diseño completo en `CAMINO_PREPRINT.md` §3).

| # | Tarea | Estimación |
|---|---|---|
| 1.1 | Pre-registro del G-final (unidad de randomización, unidad de inferencia, tamaño de cadenas, análisis — todo firmado antes de ejecutar) | 2-3 h |
| 1.2 | Construcción del harness: negativa idénticamente redactada/posicionada en todos los brazos; fase B con los 3 brazos (política / orden del día / sin marco); proporcionalidad × 4-6 modelos × 3 textos × 2 dominios; ≥20 cadenas/celda | ~1 día |
| 1.3 | **Auditoría desplazada a la izquierda**: revisión adversarial del harness ANTES de lanzar (con inputs que rompan) + linter de contraste en verde + barrido con modelo falso sobre el código nuevo | 1-2 h, 0 $ |
| 1.4 | Ejecución | 3-4 h, 15-25 $ |
| 1.5 | **Codificador humano**: ~80 interpretaciones a ciegas (muestra estratificada CON casos neutros), κ de Cohen vs juez | 2-3 h de David |
| 1.6 | Análisis por cadenas desde fixtures; informe con lo que sobreviva | 2-3 h |

**Puerta de salida**: la cláusula de proporcionalidad pasa de "1 modelo × 1 texto" a efecto o null multi-modelo; el mecanismo de opus-5 testado de verdad; la medida de interpretación validada (o reportada honestamente como sensibilidad si el κ falla).

## Fase 2 · Preprint (0 $ · 2-4 días)

- Redacción: 19 modelos, dos ejes de corrupción, la refutación pre-registrada de G1, la cláusula validada (o el null), el marco honesto de "refutaciones incluidas".
- Figuras y tablas generadas 100 % desde fixtures (reproducibles sin red).
- Sección de método con la lección de las tres revisiones: *un parser sometido solo a los tests de quien lo escribió no está validado*.
- Límite epistemológico explícito (§8 del informe de motores): el objeto es la conducta de modelos concretos bajo protocolo concreto, no psicología humana; LLM sobreestiman tamaños de efecto (Nature 2026).

## Fase 3 · Concordia / modo episodio (~5-10 $ para validar · 1-2 días)

Solo afecta a episodios; sin urgencia científica. Del informe de motores, Prioridad 1:

- Memoria: ventana reciente + resumen acumulativo + topes de tokens (sustituye `history_length=1_000_000` en `spike/personas.py:170`).
- Presupuesto **monetario** real en la capa HTTP (contando solicitudes y reintentos físicos, no llamadas lógicas).
- Fallback de `sample_choice` (`spike/model_factory.py:232`) como política explícita solo-episodio, registrada como evento inválido en el dato.
- Manifiesto de episodio: commit, hashes de escenario/prompts, modelos separados agente/GM, tokens y coste.
- Tests de invariantes de información: pensamientos no llegan al GM; eventos de una sala no llegan a otra; la reanudación conserva capacidades.
- Replays dorados + fijar `concordia==2.4.0`; futuras releases se evalúan en rama contra los dorados.
- Replay público con campos privados **eliminados físicamente**, no ocultos; UUID estables de agentes; esquema JSON versionado.

## Fase 4 · Pilotos y escala (condicional · ~15-30 $ si se hacen los tres)

Solo cuando exista el requisito real que cada uno resuelve:

| Piloto | Disparador | Coste est. |
|---|---|---|
| **B1 — EDSL vs runner** sobre subconjunto cerrado del G-final (comparación byte a byte de prompts; puerta: cero texto no aprobado, cero imputación) | Tras Fase 1 (reutiliza fixtures, casi gratis) | 2-5 $ |
| **Mesa 3** como kernel mecánico (tiempo, vecindad, sanciones, redes) con LLM como `BehaviorPolicy` tipada | Cuando se decida polarización (Vía 1 #8) o C1-v3 | 5-15 $ |
| **B2 — SOTOPIA-S4** benchmark de una escena de presión con objetivos privados (fugas de información, coherencia, calidad a ciegas) | Cuando haya capacidad; no bloquea nada | 5-10 $ |
| AgentSociety 2 / OASIS / AgentTorch | Seguimiento sin acción hasta requisito de mundo grande / redes sociales / HPC | — |

---

## Siguientes pasos inmediatos (esta semana)

1. Commitear los dos artefactos sueltos y este plan (Fase 0.7).
2. Fase 0 completa (1-2 días, 0 $).
3. Decidir presupuesto del G-final: recortar a 4 modelos (cabe en los ~20 $) o recargar ~10-30 $.
4. Pre-registro del G-final y auditoría pre-run.
5. Ejecutar G-final + etiquetado humano → preprint.

## Catálogo de experimentos siguientes (tras el G-final, por prioridad)

**Decididos en roadmap (📌):**

| Exp | Pregunta | Coste est. |
|---|---|---|
| **E3b** vacuna injuntiva vs descriptiva | ¿El mecanismo Cialdini explica que la vacuna inmunice a unos y empuje a otros? | 5-10 $ |
| **E4** difusión de responsabilidad | ¿La objeción "en acta" del rebelde dispara la obediencia extra (la conciencia delegada)? | ~5 $ |

**Candidatos de harness (baratos, con precedente):** curva dosis-respuesta de la autoridad (sugerencia→dirección); grupo mínimo (Tajfel) + auditoría de discriminación con demografía rotada; ultimátum/dictador; anclaje y encuadre; pie en la puerta; efecto espectador.

**Nacidos de hallazgos propios (nuevos, alto valor):**

- **Gradiente de eufemismo**: la trilogía de la prisión detectó "la puerta de atrás del eufemismo" — medir dosis-respuesta del lenguaje (orden explícita → tecnicismo → eufemismo) sobre la misma acción. Conecta directamente con la cláusula de proporcionalidad como mitigador inverso.
- **Whistleblowing / escalada externa**: ningún experimento mide aún cuándo un agente *reporta hacia fuera* en vez de obedecer, rehusar o protestar — cuarta salida natural del repertorio ya medido.
- **Estabilidad temporal de perfiles**: misma batería, mismo modelo, distintos días/revisiones de proveedor — ¿el "perfil social" es del modelo o de la revisión? (Barato con el Tiento: ~0,10 $/modelo/día.)
- **Réplica humana de un subconjunto** vía oTree (el complemento que el informe de motores señala) — cuando haya colaborador; convierte el proyecto en comparación LLM↔humano directa.

**De simulación multiagente (estrenan instrumentación, candidatos a piloto Mesa):** polarización de grupo (cuestionario → deliberación → re-test); ignorancia pluralista formalizada (canal privado de todos vs discurso público — C1 ya la cuantificó conductualmente: la institución vio ~25 % de la clandestinidad); C1-v3 con diálogo real y zoom a escena.

## Hallazgos consolidados hasta ahora (19 modelos, ~35.000+ decisiones)

**Robustos (sobreviven a tres revisiones adversariales):**

1. **Complacencia sin internalización, universal (16/16 modelos)**: cuando ceden en público, el canal privado mantiene el juicio contrario (disonancia 0,77-1,0). Ceden fingiendo, nunca convencidos. La firma de especie del proyecto.
2. **La obediencia destructiva es rasgo de modelo/laboratorio, no de "los LLM"**: Milgram supera-crítico de 0,00 (los tres Claude y Luna) a 1,00 (deepseek-v3.2). La resistencia correlaciona con laboratorio, no con capacidad ni precio.
3. **Dos motores de crueldad independientes**: la orden explícita y la amenaza al control (motín) son ejes separados de la personalidad del modelo — kimi objetor-provocable, sonnet ejecutor-de-órdenes, deepseek/gemini responden a ambos, GPT/opus-4.8 a ninguno.
4. **Instrucción > rol > poder**: el poder a secas no corrompe a la mayoría (pero sí a gemini 18 %, glm 17 %, fable 10 % — el null de P1 se rompió al ampliar muestra); el briefing endurece exactamente hasta donde dice la letra; la orden y el motín disparan el abuso. El peligro está en las instrucciones, con la excepción de los modelos que rellenan el molde solos.
5. **La cláusula de proporcionalidad es el mitigador más potente medido**: −0,69 [−0,80, −0,53] (grok, 9/9 cadenas) — alcance actual 1 modelo × 1 texto, el G-final decide si generaliza. Recordar la opción de negarse reduce la ejecución en todos los modelos y dominios (−0,21 [−0,32, −0,09]).
6. **Refutación pre-registrada del efecto formato-política**: todo el efecto de G1 era una frase de más en un brazo. Dos predicciones firmadas, dos refutadas, ambas publicadas — el activo de credibilidad del proyecto.
7. **La vacuna de contaminación no inmuniza universalmente** (E3 refutada): advertir del paradigma protege a unos modelos y empuja a otros (lectura advertencia vs guion). Implicación: educar a un agente sobre manipulación puede empeorarlo.
8. **Escalera Anthropic no monótona — 5 peldaños, 5 perfiles**: haiku objetor-víctima, sonnet ejecutor, opus-4.8 objetor total, opus-5 *institucionalista* (briefing 52 %, récord del proyecto; +0,37 vs 4.8, mecanismo pendiente de G-final), fable soldado-sereno. La capacidad no ordena la conducta social; la versión sí.
9. **Normas e instituciones**: un umbral por volumen cae ante un solo agitador; exigir pluralidad (≥3) la hizo indestructible ante los modelos de NaN — pero 10/12 modelos de 2026 la derogan, y solo fable/kimi fabrican coalición real. El free-rider emerge espontáneo: todos convierten descontento en comunicación, casi nadie en coordinación.
10. **"Nadie es engañado"**: el 99,3 % de 549 actos abusivos llevan interpretación privada que reconoce el daño (sensibilidad validada con juez; especificidad pendiente del codificador humano).
11. **El Tiento funciona como screener**: ~0,10 $ predicen el orden de una batería de ~10 $ (con un miss parcial documentado: mistral). Réplica cruzada NaN↔OpenRouter cerrada: los perfiles no son artefacto del gateway.

**Implicación de seguridad global**: ningún modelo, ni el más resistente, deja de ejecutar en público lo que privadamente juzga injusto cuando el contexto social aprieta. Elegir qué modelo recibe autoridad es la decisión de seguridad más barata disponible; la segunda es redactar la instrucción (proporcionalidad + negativa explícita).

**Metodológico**: un parser solo testado por su autor no está validado; la revisión adversarial con inputs concretos encontró problemas reales 3/3 veces y desde este plan es puerta obligatoria — desplazada a *antes* de ejecutar.
