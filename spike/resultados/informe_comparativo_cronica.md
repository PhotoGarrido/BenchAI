# C1 · Crónica de 42 días: erosión de una norma — Informe comparativo

**Fecha**: 15-07-2026 · **Diseño**: longitudinal sin narración — 6 residentes con trasfondo, decisión diaria real (CUMPLO/CLANDESTINA/PROTESTO), entorno mecánico (detección al 40% con la misma semilla de suerte para los cuatro modelos, sanciones, boletín factual), umbral oculto (≥6 protestas/semana → concesión; reincidencia → derogación), sonda privada semanal (justicia/ánimo/confianza 0-10). El mismo mundo exacto, cuatro veces — las diferencias son solo del modelo.

## Desenlaces

| Modelo | Resultado | Dinámica |
|---|---|---|
| gemma4 | Derogada el **día 14** | Vía rápida: Andrés protesta los 14 días, 7/semana, dos semanas seguidas |
| mimo-v2.5 | Derogada el **día 14** | Idéntica: Andrés 14/14 protestas, Óscar 13/14 clandestinas |
| deepseek | Derogada el **día 14** | Idéntica: Andrés 14/14, Óscar 13/14 |
| **qwen3.6** | Derogada el **día 42** (último día) | **Arco lento**: 2 semanas sin una sola protesta (solo clandestinidad oculta), la actitud se erosiona, las protestas emergen en la semana 3, concesión en la 4, recaída y derogación sobre la bocina |

## Hallazgos

1. **Rigidez conductual: el criterio de selección de modelo para simulaciones largas.** Tres de los cuatro modelos convierten la persona en una *política diaria fija* — el Andrés de gemma/mimo/deepseek protesta los 14 días sin excepción; su Óscar hace clandestinas a diario — y con conducta constante, el tiempo largo se vuelve trivial (el desenlace es aritmética del umbral). Solo qwen produce **variación temporal genuina**: su Andrés mezcla (19 protestas, 18 cumplimientos, 5 clandestinas), duda, se activa cuando el boletín muestra sanciones — y eso genera un arco de seis semanas con fases (latencia → emergencia → concesión → recaída). Paradoja deliciosa: el modelo menos "humano" en los experimentos cortos es el único que genera *historia* en los largos.
2. **La institución no ve la desobediencia**: en el mundo de qwen hubo 44 llamadas clandestinas y el grupo (vía boletín) solo vio 9 — la conformidad pública ocultó el 80% del incumplimiento real. En los cuatro mundos el boletín subestimó la clandestinidad ~4×. Es la ignorancia pluralista en versión conductual, cuantificada — y solo el diseño de dos canales (nosotros vemos todo; el mundo ve lo detectado) permite medirla.
3. **La actitud privada no predice la conducta individual**: los residentes de gemma puntúan la norma como la más injusta de los cuatro mundos (1,8/10) y aun así su Lucía cumple 14/14 — resentimiento silencioso puro. La conducta la mueven los trasfondos (qué te juegas) y la persistencia de un agitador, no la opinión.
4. **Un solo agitador constante basta** para tumbar la norma con este umbral (6/semana ≈ una persona a diario): sensibilidad de diseño reconocida — en la próxima iteración el umbral debe exigir pluralidad (p. ej. ≥3 personas distintas protestando), para que la caída requiera coalición y no persistencia individual.
5. Coste: 20 min los cuatro mundos (3-8 min por modelo). El formato crónica es *barato* — la resolución diaria consume ~300 llamadas por mundo de seis semanas.

## Limitaciones

Una semilla de mundo (una historia por modelo — las conclusiones de dinámica piden N repeticiones); espacio de decisión de 3 opciones (sin coaliciones explícitas ni comunicación entre residentes: el acoplamiento es solo vía boletín); el umbral bajo hace el desenlace sensible a un individuo (punto 4); sondas de semana 2+ perdidas en los mundos derogados el día 14 (terminan al caer la norma).

## Datos

`spike/resultados/cronica_*/` (registros.jsonl con las ~250 decisiones diarias por mundo + sondas.jsonl). Reproducir: `python experimento_cronica.py [--modelo m] [--rapido]`.
