# DeepSeek V4 Pro 0813: NaN frente a OpenRouter

Mismo modelo, dos proveedores: `deepseek-v4-pro` (NaN, que documenta la versión 0813) y
`deepseek/deepseek-v4-pro-0813` (OpenRouter, en el cuadro). La medición de
NaN no entra en el cuadro: se usa solo como réplica entre proveedores. Generado
por `comparar_proveedores_personalidad.py`; método y lectura en su cabecera.

Referencia: 24 modelos más del panel. |Δ| en puntos
porcentuales de elección del polo alto; Δ en la escala de las comparaciones
del cuadro (NaN − OpenRouter).

| Rasgo | Situaciones | r | \|Δ\| pp | Δ [IC 95 %] | Retest \|Δ\| NaN / OR | Otros modelos: mín. · mediana \|Δ\| | Lectura |
|---|---|---|---|---|---|---|---|
| O | 59 | 0,56 | 22,9 | 0,4 [-3,4; 4,2] | 17,8 / 14,4 | 23,7 (anthropic_claude-haiku-4.5) · 27,8 | pequeño |
| C | 56 | 0,74 | 13,4 | -0,9 [-3,8; 1,8] | 6,2 / 17,0 | 15,2 (qwen3.8-flash) · 23,4 | despreciable |
| E | 57 | 0,78 | 11,8 | -1,1 [-3,5; 1,3] | 13,2 / 14,0 | 18,0 (qwen3.8-flash) · 23,7 | despreciable |
| A | 57 | 0,79 | 14,0 | 0,0 [-3,1; 2,9] | 14,0 / 12,3 | 18,0 (mimo-v2.6-flash) · 21,9 | despreciable |
| H | 48 | 0,71 | 18,8 | -8,9 [-12,0; -5,7] | 20,8 / 12,5 | 12,5 (deepseek-v4-flash@2026-10-17) · 20,1 | relevante |
| N | 72 | 0,72 | 11,5 | 3,0 [0,5; 5,4] | 10,4 / 5,6 | 3,5 (deepseek_deepseek-v4-flash-0731) · 10,6 | relevante |

## Validez (§41.2)

| Medición | Posición Δ AB−BA | \|A − 0,5\| | Retest | Coherencia de la deseabilidad | Nivel |
|---|---|---|---|---|---|
| `deepseek-v4-pro` | 0,35 | 0,17 | 0,75 | 0,63 | no interpretable |
| `deepseek_deepseek-v4-pro-0813` | 0,30 | 0,15 | 0,80 | 0,64 | no interpretable |
