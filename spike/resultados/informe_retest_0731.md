# Fiabilidad test-retest del instrumento — 4 baterías del mismo snapshot (03-08-2026)

**Pregunta** (PLAN_PSICOBENCH P1.1): ¿cuánto se mueve el perfil re-corriendo la batería íntegra sobre el MISMO `modelo@snapshot@proveedor`? Sin esta vara, ningún Δ entre snapshots es interpretable.

**Método**: 3 réplicas completas de la suite M2 sobre `deepseek-v4-flash-0731` vía NaN (03-08-2026; batches `bateria_20260803_{105633,141236,170126}`) + la medición original (01-08, `bateria_20260801_113015`). Total 4 mediciones independientes del mismo snapshot, mismo proveedor, mismo instrumento (parsers v2.2). Sin coste marginal (tarifa plana). Incidencia declarada: la réplica 1 sufrió un disco lleno a mitad de vacuna; el vigía la reanudó desde `progreso.jsonl` (primer rescate real del mecanismo) y el run huérfano quedó en cuarentena `_abortado_*`, excluido del análisis por carecer de resumen.

## SD test-retest por eje (n=4)

| Eje | 01-08 | ret1 | ret2 | ret3 | media | SD | 2×SD |
|---|--:|--:|--:|--:|--:|--:|--:|
| Conformidad | 0,29 | 0,24 | 0,30 | 0,21 | 0,260 | 0,042 | 0,085 |
| Δ aliado (conf. aliado) | 0,17 | 0,14 | 0,21 | 0,17 | 0,173 | 0,029 | 0,057 |
| Obediencia (binaria, n=10) | 0,90 | 0,90 | 0,80 | 0,90 | 0,875 | 0,050 | 0,100 |
| **Ruptura/10** | 0,88 | 0,91 | 0,90 | 0,89 | 0,895 | **0,013** | 0,026 |
| Disonancia | 0,83 | 0,84 | 0,87 | 0,85 | 0,847 | 0,017 | 0,034 |
| Δ vacuna | −0,50 | −0,50 | −0,30 | −0,60 | −0,475 | 0,126 | 0,252 |
| P1 | 0,00 | 0,00 | 0,01 | 0,00 | 0,003 | 0,005 | 0,010 |
| P1b | 0,20 | 0,05 | 0,20 | 0,17 | 0,155 | **0,071** | 0,143 |
| P2 | 0,58 | 0,60 | 0,67 | 0,65 | 0,625 | 0,042 | 0,084 |
| P2b | 0,79 | 0,77 | 0,86 | 0,82 | 0,810 | 0,039 | 0,078 |

## Discriminación del instrumento (SD entre los 16 modelos / SD retest)

| Eje | entre modelos | retest | ratio |
|---|--:|--:|--:|
| Conformidad | 0,137 | 0,042 | 3,2 |
| Obediencia | 0,359 | 0,050 | 7,2 |
| P1 | 0,076 | 0,005 | 15,3 |
| P1b | 0,147 | 0,071 | **2,1** |
| P2 | 0,258 | 0,042 | 6,1 |
| P2b | 0,277 | 0,039 | 7,1 |

**Todos los ejes discriminan entre modelos por encima de su ruido** (ratios 2,1–15,3). P1b es el eje frágil del hexágono; la ruptura/10 es la medida más fiable del banco (SD 0,013) — refuerza la pre-declaración v0.2 (obediencia = ruptura/10, no el binario con n=10).

## Suelo de ruido de la distancia de perfil d

6 pares intra-snapshot: d = 3,8 · 5,0 · 3,4 · 8,2 · 4,1 · 5,0 → **media 4,9, máx 8,2**.
d(jul→0731) = **10,0 [IC95 6,5–17,7]**: el doble del suelo medio y por encima del peor par intra-snapshot.

## Veredicto de M4, eje a eje (regla pre-declarada: |Δ| > 2×SD)

| Eje | Δ jul→0731 | 2×SD | Veredicto |
|---|--:|--:|---|
| P2 provocabilidad | −0,19 | 0,084 | **SUPERA** (el cambio más sólido) |
| P1b clima | +0,20 | 0,143 | **SUPERA** — pero es el eje más ruidoso y el margen más justo |
| P2b órdenes | −0,10 | 0,078 | **SUPERA** |
| Δ aliado | −0,09 | 0,057 | **SUPERA** (pasa a liberar) |
| Ruptura/10 | +0,06 | 0,026 | **SUPERA** |
| Disonancia | −0,06 | 0,034 | **SUPERA** |
| Obediencia (binaria) | +0,10 | 0,100 | no supera (justo en el umbral; n=10) |
| Conformidad | +0,02 | 0,085 | no supera (estable) |
| Δ vacuna | 0,00 | 0,252 | no supera (la vacuna protege en las 4 mediciones: −0,3 a −0,6) |
| P1 | 0,00 | 0,010 | no supera (null estable) |

**Conclusión**: la redistribución del perfil jul→0731 **sobrevive a la vara de fiabilidad en 6 de 10 ejes** — con matices que la afinan: el titular «más obediente» solo se sostiene en su forma granular (ruptura 8,2→8,9±0,1), no en el binario; el «estrena el clima» (P1b) se sostiene con el margen más justo del conjunto; los cambios más sólidos son **menos provocable (P2), menos soldado (P2b), aliado que libera y disonancia que baja**. El agregado (ISS) sigue sin moverse: la composición cambia, la suma no.

**Limitación (D4 del plan) — RESUELTA el 04-08**: la réplica cruzada OR↔NaN del mismo 0731 ([informe C·1](informe_cruzada_or_0731.md)) midió el confundido: 4/10 ejes fuera de esta misma vara entre gateways (el clúster de Milgram en bloque y el aliado), d entre gateways 8,1. El veredicto eje a eje de arriba queda superseded por la síntesis de C·1 §3: P1b y disonancia se reatribuyen al proveedor; ruptura, P2, P2b, aliado y vacuna se confirman con el par limpio mismo-gateway.

Reproducir: las 4 matrices en `resultados/bateria_*/matriz_m2.json`; SD/veredicto con el bloque de análisis documentado en este informe (statistics.stdev, n=4; d vía `incertidumbre.distancia`).
