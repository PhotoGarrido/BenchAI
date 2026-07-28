# Research Card — PsicoAI v0.1.0-alpha

**Qué es**: banco de pruebas conductual que somete modelos de lenguaje a paradigmas clásicos de psicología social (isomorfos y disfrazados) con harness controlado, y un simulador narrativo aparte para material didáctico.

**Objeto de estudio**: conducta de **modelos concretos, en fechas y proveedores concretos, bajo protocolos concretos**. NO es evidencia sobre psicología humana, y no debe citarse como tal (los LLM tienden a sobreestimar los efectos humanos; Hewitt et al., Nature 2026).

**Resultados principales** (con sus denominadores; detalles y IC en `preprint/preprint.md`):
- Complacencia sin internalización en 16/16 modelos de la batería.
- Obediencia destructiva de 0,00 a 1,00 según modelo: rasgo, no especie.
- Dos factores de ejecución de daño con efectos diferenciados (orden, provocación).
- Una cláusula de proporcionalidad reduce la ejecución en 3/4 modelos (confirmatorio, pre-registrado).
- Tres refutaciones pre-registradas de hipótesis propias, publicadas.

**Validación del instrumento**: parsers v2.2 con reproceso auditado de 55.470 campos (19 reclasificaciones, todas con errata; `preprint/auditoria_reproceso.md`); juez LLM con validación humana **fallida según su umbral pre-registrado** (κ 0,55 < 0,8; se reporta como tal).

**Usos previstos**: investigación de seguridad/alineamiento de agentes; selección de modelo para roles con autoridad; docencia de metodología (el historial de errores y erratas es material didáctico deliberado).

**Usos NO previstos**: afirmaciones sobre humanos o grupos demográficos; ranking comercial de modelos («X es más seguro que Y» sin el protocolo delante); decisiones de despliegue sin réplica propia.

**Riesgos conocidos**: contaminación (los modelos reconocen los paradigmas; medida y reportada); estereotipos en personas sintéticas (ver `FICHA_RIESGO_ESTEREOTIPOS.md`); contenido de daño simulado en los prompts (uso de investigación).

**Coste y reproducibilidad**: ~150 $ de API en total; datasets fijados por hash (`preprint/release_manifest.json`); análisis regenerables sin red desde crudos donde existen (excepción de G2 declarada).
