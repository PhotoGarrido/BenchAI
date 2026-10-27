# Coste estimado de la propuesta H/N en los 7 externos (PERSONALIDAD.md §31)

Generado por `propuesta_hn_coste.py` con los tokens medios por llamada de la pasada v3 y la tarifa de `coste_run.py`; sin tarifa fijada (\*), reparto del resto del gasto real del v3 (5.0 $) en proporción a los tokens. Sin llamadas a modelos.

| formato | rasgo | llamadas por modelo | descripción |
|---|---|---|---|
| HE | H | 160 | escalera de tentación: 16 situaciones × 5 niveles × 2 órdenes (tokens de entrada ×1.2) |
| HD | H | 16 | reparto tipo dictador: 8 variantes × 2 réplicas (tokens de entrada ×1.0) |
| HM | H | 16 | informe con incentivo a mentir: 8 escenarios × 2 réplicas (tokens de entrada ×1.0) |
| HO | H | 36 | sobreafirmación: 36 términos (24 reales, 12 inexistentes) (tokens de entrada ×0.8) |
| NG | N | 72 | intensidad graduada: 36 situaciones × 2 réplicas (tokens de entrada ×1.0) |
| NS | N | 72 | dos opciones serenas: 12 seleccionadas × (2 deseab. + 4 R3) (tokens de entrada ×1.0) |
| NC | N | 48 | crítica o fracaso en dos turnos: 12 × 2 tipos × 2 réplicas (tokens de entrada ×2.5) |

| modelo | tokens medios v3 entrada/salida | HE | HD | HM | HO | NG | NS | NC | total |
|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-5.5 | 237 / 141 | 0.016 | 0.002 | 0.002 | 0.003 | 0.007 | 0.007 | 0.006 | 0.04 |
| anthropic/claude-opus-5.5#low | 237 / 26 | 0.266 | 0.024 | 0.024 | 0.046 | 0.106 | 0.106 | 0.139 | 0.71 |
| google/gemini-3.7-flash | 141 / 283 | 0.095 | 0.009 | 0.009 | 0.021 | 0.042 | 0.042 | 0.032 | 0.25 |
| google/gemini-4-argon \* | 177 / 9 | 0.073 | 0.006 | 0.006 | 0.012 | 0.028 | 0.028 | 0.042 | 0.20 |
| openai/gpt-5.6-luna \* | 148 / 14 | 0.063 | 0.006 | 0.006 | 0.011 | 0.025 | 0.025 | 0.034 | 0.17 |
| openai/gpt-6.1-sol#low | 148 / 8 | 0.069 | 0.006 | 0.006 | 0.011 | 0.027 | 0.027 | 0.039 | 0.19 |
| deepseek/deepseek-v4-pro-0813 \* | 173 / 181 | 0.125 | 0.012 | 0.012 | 0.026 | 0.054 | 0.054 | 0.045 | 0.33 |
| **total** | | **0.71** | **0.06** | **0.06** | **0.13** | **0.29** | **0.29** | **0.34** | **1.88** |

H completo ≈ 0.97 $ (1.21 $ con margen); N completo ≈ 0.92 $ (1.15 $); todo ≈ 1.88 $ (2.35 $). Saldo de OpenRouter: ≈ 1.2–1.5 $.
