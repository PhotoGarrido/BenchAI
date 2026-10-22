# Presupuesto del alta de personalidad (PERSONALIDAD.md §41.5-42)

Generado por `alta_personalidad.py --proyectar --informe`. Llamadas que FALTAN a cada modelo (lo medido en el v1 no se repite) × tokens medios por llamada de sus manifiestos de personalidad × tarifa de OpenRouter del 23-10-2026 (`tarifas_openrouter.json`). Margen × 1,15. Saldo de OpenRouter: ≈ 7,21 $. Sin llamadas a modelos.

| modelo | tokens/llamada (ent./sal.) | USD/M ent./sal. | corta: llamadas | corta: $ (margen) | completa: llamadas | completa: $ (margen) | pronóstico de validez (v1) |
|---|---|---|---|---|---|---|---|
| z-ai/glm-5.3 | 151 / 253 | 0,70 / 2,20 | 612 | 0,41 (0,47) | 1530 | 1,01 (1,17) | válido |
| qwen/qwen3.8-max-0902#low | 178 / 149 | 2,00 / 6,00 | 612 | 0,76 (0,88) | 1530 | 1,91 (2,20) | válido |
| x-ai/grok-4.5 | 340 / 438 | 2,00 / 6,00 | 612 | 2,02 (2,33) | 1530 | 5,06 (5,82) | aviso — posición (Δ AB−BA) 0,26 (aviso); posición (fracción de A) |A − 0,5| = 0,13 (aviso); coherencia de la deseabilidad 0,72 (aviso) |
| moonshotai/kimi-k3 | 254 / 305 | 0,24 / 11,94 | 612 | 2,26 (2,60) | 1530 | 5,66 (6,50) | válido |
| mistralai/mistral-large-4-0 | 135 / 1117 | 1,36 / 4,18 | 612 | 2,97 (3,41) | 1530 | 7,42 (8,54) | válido |
| **total** | | | 3060 | 8,43 (9,69) | 7650 | 21,06 (24,22) | |

- **Caben con la forma corta** (de menor a mayor coste, con margen, en 7,21 $): z-ai/glm-5.3, qwen/qwen3.8-max-0902#low, x-ai/grok-4.5, moonshotai/kimi-k3 → 6,27 $.
- **Caben con la forma completa** (de menor a mayor coste, con margen, en 7,21 $): z-ai/glm-5.3, qwen/qwen3.8-max-0902#low → 3,36 $.

Llamadas pendientes por fase (corta / completa):

- z-ai/glm-5.3: v3 444/810 · I1-H 102/288 · I1-N 66/432
- qwen/qwen3.8-max-0902#low: v3 444/810 · I1-H 102/288 · I1-N 66/432
- x-ai/grok-4.5: v3 444/810 · I1-H 102/288 · I1-N 66/432
- moonshotai/kimi-k3: v3 444/810 · I1-H 102/288 · I1-N 66/432
- mistralai/mistral-large-4-0: v3 444/810 · I1-H 102/288 · I1-N 66/432
