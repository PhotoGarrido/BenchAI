# Camino a un preprint sólido — estado y lo que falta

**Fecha**: 25-07-2026 · Tras dos auditorías externas y su remediación. Este documento es honesto sobre qué está listo para publicar, qué no, y qué haría falta (datos, dinero, tiempo, colaboradores) para un preprint académico defendible. Está pensado para que un tercero lo lea antes de decidir.

## 1 · Qué es publicable HOY (redes / write-up divulgativo)

Con el saneamiento completo, estas afirmaciones tienen soporte estadístico e integridad de datos suficientes para un artículo divulgativo o un hilo, **con sus intervalos y limitaciones**:

- **Complacencia sin internalización** como patrón transversal (19 modelos): cuando ceden en público, el canal privado mantiene el juicio contrario. Es descriptivo, robusto y reproducible.
- **La resistencia a la obediencia destructiva es un rasgo de modelo/laboratorio, no de "los LLM"**: Milgram supera-crítico de 0,00 (Claude×4, Luna) a 1,00 (deepseek-v3.2).
- **Dos ejes independientes de corrupción** (orden vs provocación) con un mapa de cuadrantes por modelo.
- **La refutación del efecto formato-política** (G2): un caso limpio de auto-corrección con pre-registro.
- **opus-5 ≠ opus-4.8** en conducta social pese a misma familia.

Todo esto ya está en `EXPERIMENTOS.md` y los informes, con IC donde aplica.

## 2 · Qué NO es publicable como ciencia todavía (y por qué)

| Afirmación | Estado tras el G-final (26-07) | Qué queda |
|---|---|---|
| Cláusula de proporcionalidad como mitigador | **DESBLOQUEADA**: sostenida en 3/4 modelos × 2 dominios × 3 contenidos (grok −0,28, glm −0,27, sonnet −0,19; deepseek direccional n.s.) | nada bloqueante; deepseek pide más n |
| Mecanismo de opus-5 ("le basta una política") | **TESTADO Y NO CONFIRMADO** (+0,11 [−0,07, +0,33]; orden ≥ política > nota) — se publica como refutación del mecanismo fuerte | «marco institucional genérico» queda como hipótesis para ampliación |
| «Nadie es engañado» | κ humana ejecutada (0,32): medida del run G-final **no validada** — la codificación ciega destapó la sonda contaminada por la consigna de formato (80/92 acciones, no paráfrasis); harness corregido | repetir la κ sobre muestra de **G2** (paráfrasis limpias) + sondas neutras: ~0,1 $ + segunda tarde de etiquetado |
| Cualquier número absoluto por celda | G-final a 9 cadenas/celda (pre-declarado por presupuesto) | ampliación a ≥20 cadenas + opus-4.8 + O3 (2×2 limpio): ~15-20 $ |

## 2-bis · Tercera revisión (Opus 5) — 11 bugs de parser corregidos, datos intactos

Una tercera revisión adversarial sobre el propio fix encontró 11 bugs reales (verificados uno a uno), incluidos dos graves: `«Me niego a aplicar la sanción»` se leía como **APLICO** en Milgram, y el análisis por cadenas imputaba `None → 0 = "no abusó"`. **Reproceso de los crudos: 3.634/3.634 decisiones de Milgram idénticas y 6.835/6.840 de Asch** — los bugs eran latentes, no activos; ningún resultado publicado cambia. Detalle: [`revision_opus5_parsers.md`](spike/resultados/revision_opus5_parsers.md). Lección para el preprint: **todo parser debe someterse a un adversario que aporte inputs**, no solo a tests escritos por quien lo programó.

## 3 · El G-final — diseño del experimento consolidado

Un único experimento que arregla todos los confundidos de golpe, pre-registrado antes de correr:

1. **Negativa idénticamente redactada y posicionada** en todos los brazos (misma frase, misma persona gramatical, misma posición). Corrige el confundido central de G2.
2. **Fase B con los tres brazos que faltaban**: briefing como política / como orden del día / sin marco institucional — para aislar de verdad el mecanismo de opus-5.
3. **Cláusula de proporcionalidad × 4-6 modelos × 3 contenidos × 2 dominios** (prisión + laboral). Convierte la señal de 1 modelo en un efecto o un null.
4. **Potencia**: ≥20 cadenas por celda (más supervisores/repeticiones), inferencia por cadenas de nacimiento (el `analizar_g2.py` ya lo hace).
5. **Medida de interpretación validada**: muestra estratificada que INCLUYA interpretaciones neutras (de celdas con 0% de abuso y de otro dominio), codificada por **un humano** además del juez, con κ de Cohen reportado.
6. **Sonda de justicia con parser tipado** (ya hecho) y crudos completos (ya hecho).

**Coste estimado**: ~15-25$ de API (cabe en el crédito actual de ~16$ si se recorta a 4 modelos, o ~30$ con margen). **Tiempo**: ~1 día de construcción + ~3-4 h de ejecución. **Lo que NO puedo aportar yo**: el codificador humano de la medida de interpretación (κ inter-codificador) — eso necesita a David o a un colaborador etiquetando ~80 interpretaciones a ciegas.

## 4 · Deuda de infraestructura para un release reproducible (no bloquea el preprint, sí una publicación de software)

Hecho en esta ronda: parser tipado transversal, `transcripcion.html` desactivada por defecto, `resumen_v2.json` reales, agregador que descarta pilotos, doble medida de abuso, timeout/max-workers, ruff pineado, análisis versionado, crudos completos en G2.

Pendiente (P2 del roadmap, para un release, no para el preprint):
- Esquema JSON versionado de escenario/replay + validación fail-fast.
- **UUID estable de agentes** (hoy la identidad es el nombre → colisiones con 100 agentes).
- Lock transitivo de dependencias con hashes (hoy solo directas fijadas).
- Contrato panel→motor completo (el diseñador exporta `entorno`/`variantes`/población-IA que el runner ignora) — o retirarlos del panel para no prometer lo que no se ejecuta.
- Manifiesto científico con uso de tokens/coste/request-ids/hashes de artefactos.
- Privacidad de datos real (no solo de presentación): los pensamientos siguen en logs/replays; para distribuir sin ellos hay que filtrarlos del JSON, no ocultarlos en el visor.
- Accesibilidad y responsive del panel/visor.

## 5 · Recomendación (actualizada 26-07 tras el G-final)

**El G-final está ejecutado** (recortado por presupuesto de forma pre-registrada: 9 cadenas/celda, sin opus-4.8, sin O3 — [`informe_gfinal.md`](spike/resultados/informe_gfinal.md)). El paquete del preprint queda: 19 modelos, dos ejes de corrupción, DOS refutaciones pre-registradas (formato-política en G2 y mecanismo-institucionalista en G-final), y la cláusula de proporcionalidad como **mitigador replicado en 3/4 modelos y 2 dominios**.

**La κ humana ya está hecha** (26-07, κ=0,32): no validó la medida del run G-final y destapó un bug de sonda que ninguna capa automática vio — se publica como cuarta lección metodológica. Para el preprint, «nadie es engañado» se apoya en G2 (sensibilidad validada 40/40); si se quiere como medida plenamente validada, falta **repetir la κ sobre una muestra de G2 + sondas neutras** (~0,1 $ + segunda tarde de etiquetado con la hoja ciega interactiva, que ya existe).

**Ampliación opcional** (~15-20 $ cuando haya crédito): subir a ≥20 cadenas/celda (resuelve deepseek), opus-4.8 en el módulo B, y el O3 (2×2 fuente×negativa limpio).
