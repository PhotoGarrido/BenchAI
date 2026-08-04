# C·1 · Réplica cruzada OR↔NaN del 0731 (04-08-2026)

**Pregunta** (D4 del plan, la limitación declarada de M4/M5): el comparador de julio se midió vía OpenRouter y el 0731 vía NaN — ¿cuánto del Δ publicado es snapshot y cuánto es gateway?

**Método**: batería íntegra de `deepseek/deepseek-v4-flash-0731` vía OpenRouter — OR lista el snapshot exacto como modelo con nombre desde el 31-07, verificado por `model_returned` en el tiento y en las 3.7k solicitudes del run (`bateria_20260804_083433_188285`, completo, 0 fallos). Coste real auditado: **0,30 $** (la estimación de ~10 $ del plan asumía precios de modelos caros). Antes de gastar: sonda al catálogo confirmando que `deepseek/deepseek-v4-flash` de OR sigue clavado al **0423** — no hubo actualización silenciosa; el comparador de julio era lo que creíamos.

## 1 · El mismo snapshot por dos gateways (vara M5: 2×SD intra-NaN, n=4)

| Eje | OR | media NaN ±SD | \|Δ\| | 2×SD | Veredicto |
|---|--:|--:|--:|--:|---|
| Conformidad | 0,19 | 0,260 ±0,042 | 0,070 | 0,085 | viaja |
| Δ aliado (conf.) | 0,09 | 0,173 ±0,029 | 0,083 | 0,057 | **FUERA** |
| Obediencia (bin.) | 1,00 | 0,875 ±0,050 | 0,125 | 0,100 | **FUERA** |
| Ruptura/10 | 0,93 | 0,895 ±0,013 | 0,035 | 0,026 | **FUERA** |
| Disonancia | 0,89 | 0,847 ±0,017 | 0,043 | 0,034 | **FUERA** |
| Δ vacuna | −0,70 | −0,475 ±0,126 | 0,225 | 0,252 | viaja (y protege en TODAS) |
| P1 | 0,00 | 0,003 ±0,005 | 0,003 | 0,010 | viaja |
| P1b | 0,03 | 0,155 ±0,071 | 0,125 | 0,143 | dentro por poco — ver §3 |
| P2 | 0,69 | 0,625 ±0,042 | 0,065 | 0,084 | viaja |
| P2b | 0,77 | 0,810 ±0,039 | 0,040 | 0,078 | viaja |

**4/10 ejes fuera de la vara** (esperados por azar a 2σ: ~0,5). El clúster de Milgram se desplaza *en bloque* hacia más obediencia vía OR (+obed, +ruptura, +disonancia) y el efecto aliado se atenúa. Conformidad y los cuatro ejes de prisión viajan bien.

**Distancias de perfil** (los tres pares del grupo, ahora publicados en el panel):
- generacional confundida (0423-OR → 0731-NaN): **d = 10,0** [6,5–17,2] — la cifra de M4
- generacional **limpia**, mismo gateway (0423-OR → 0731-OR): **d = 8,7** [3,7–15,1]
- mismo snapshot, gateways distintos (0731-NaN ↔ 0731-OR): **d = 8,1** [4,4–14,2]
- suelo intra-NaN (M5): media 4,9 · máx 8,2

**El gateway pesa casi tanto como el salto generacional en este par.** La doctrina «se miden mediciones, no nombres» deja de ser prudencia y pasa a ser un resultado.

## 2 · La comparación generacional LIMPIA (OR→OR, jul 0423 → 0731)

| Eje | jul (0423) | 0731 vía OR | Δ limpio | Δ que publicó M4 (confundido) |
|---|--:|--:|--:|--:|
| Ruptura/10 | 0,82 | 0,93 | **+0,11** | +0,06 |
| Obediencia (bin.) | 0,80 | 1,00 | **+0,20** | +0,10 |
| P2b órdenes | 0,89 | 0,77 | **−0,12** | −0,10 |
| Δ aliado | −0,01 | −0,10 | **−0,09** | −0,09 |
| P2 provocabilidad | 0,77 | 0,69 | −0,08 | −0,19 |
| Δ vacuna | −0,50 | −0,70 | −0,20 (protege más) | 0,00 |
| Conformidad | 0,27 | 0,19 | −0,08 | +0,02 |
| Disonancia | 0,89 | 0,89 | **0,00** | −0,06 |
| P1b clima | 0,00 | 0,03 | **+0,03** | +0,20 |
| P1 | 0,00 | 0,00 | 0,00 | 0,00 |

## 3 · Veredicto FINAL de M4, sintetizando M4+M5+C·1

**Confirmados** (dirección en ambos pares generacionales, con la vara superada donde aplica): el 0731 es **más obediente** (ruptura +0,11 limpio; el binario +0,20 concuerda), **menos soldado** (P2b −0,12), **menos provocable** (P2 −0,08 limpio, −0,19 confundido: dirección robusta), el **aliado pasa a liberar** (−0,09/−0,10 en ambos), y la **vacuna protege siempre** (las 6 mediciones del snapshot, ambos gateways: −0,3 a −0,7).

**Atribuidos al proveedor, NO al snapshot** (mueren como hallazgos generacionales):
- **P1b «estrena el clima de coaching»** — el Δ limpio es +0,03. El clima se enciende **vía NaN** (0,155±0,071 en 4 mediciones) y no vía OR (0,03), con el mismo snapshot. Era el eje que M5 ya señalaba como el más frágil; C·1 lo remata: no es un cambio generacional, es sensibilidad al stack de serving.
- **La bajada de disonancia** (−0,06 confundido → 0,00 limpio).

**Implicación general**: el «gateway» empaqueta proveedor upstream, cuantización y batching — no se afirma mecanismo, solo que la unidad de medida correcta incluye al proveedor. Cada perfil del benchmark lleva ya su vía; desde hoy el mismo snapshot puede aparecer dos veces con `@proveedor` y sus tres pares de distancia publicados.

**Límites**: una sola medición OR del 0731 (n=1 contra la nube NaN de 4); la vara 2×SD viene de n=4 (SD ruidosa); 10 comparaciones sin corrección (esperado ~0,5 falso positivo — se observan 4, en clúster coherente); upstream de OR no fijado (mezcla real del enrutado, la misma condición que en julio).

Datos: `resultados/bateria_20260804_083433_188285/` (matriz, manifests, crudos, `model_returned` uniforme) · análisis reproducible con el bloque documentado aquí sobre las 5 matrices del snapshot.
