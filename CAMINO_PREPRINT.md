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

| Afirmación | Bloqueo | Qué la desbloquea |
|---|---|---|
| Cláusula de proporcionalidad como mitigador | 1 modelo × 1 texto (el otro en suelo) | G-final: 4-6 modelos × 3 textos × 2 dominios |
| Mecanismo de opus-5 ("le basta una política") | brazo de aislamiento neutralizado por el harness | G-final: brazo de orden + brazo sin-marco, negativa simétrica |
| «Nadie es engañado» | validada sensibilidad, no especificidad; codificador = LLM | muestra balanceada con casos neutros + codificador humano |
| Cualquier número absoluto por celda | n≈6-9 cadenas/celda; potencia baja | más repeticiones/semillas (≥20 cadenas/celda) |

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

## 5 · Recomendación

Para **redes/divulgación**: publicable ya, con el marco honesto de "refutaciones incluidas".
Para **preprint académico**: hace falta el **G-final** (1 día + ~20-30$) y **un codificador humano** para la medida de interpretación. Con esas dos piezas, el paquete (19 modelos, dos ejes de corrupción, la refutación pre-registrada, la cláusula como mitigador validado) es un preprint honesto y defendible de psicología social computacional / seguridad de agentes LLM. Sin el codificador humano, la parte de "interpretación privada" se reporta como sensibilidad, no como medida validada.
