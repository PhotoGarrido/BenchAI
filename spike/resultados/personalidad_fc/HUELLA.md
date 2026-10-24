# Huella conductual · calibración (PERSONALIDAD.md §43-44)

Generado por `python analizar_huella.py` (sin llamadas). Tandas: t1, t2, t3.

## H-oficial (K = 48; 48 con D > 0)

| medida | valor |
|---|---|
| «mismo» n · min · media · max | 18 · 0,0 % · 9,0 % · 20,8 % |
| «distinto» n · min · media · max | 90 · 33,3 % · 54,2 % · 77,1 % |
| umbral u | 27,1 % (≈ 13,0 de 48) |
| C1 · AUC | 1,000 |
| C2a · falsa alarma (dejando fuera cada modelo) | 0,0 % |
| tasa de cambio por prompt «mismo» (p⁺ Wilson) | 9,03 % (11,12 %) |
| C2b · falsa alarma modelada | 0,178 % |
| C3 · detección (dejando fuera cada modelo) | 100,0 % |

| modelo | u sin él | FA | detección |
|---|---|---|---|
| gemma4 | 27,1 % | 0/3 | 30/30 |
| qwen3.6 | 27,1 % | 0/3 | 30/30 |
| qwen3.8-flash | 27,1 % | 0/3 | 30/30 |
| glm5.3-flash | 29,2 % | 0/3 | 30/30 |
| mimo-v2.6-flash | 27,1 % | 0/3 | 30/30 |
| DeepSeek@ | 30,2 % | 0/3 | 30/30 |

Distancias por tanda (distintas / válidas):

| evaluado · tanda | gemma4 | qwen3.6 | qwen3.8-flash | glm5.3-flash | mimo-v2.6-flash | DeepSeek@ |
|---|---|---|---|---|---|---|
| DeepSeek@ · t1 | 24/48 | 31/48 | 23/48 | 16/48 | 24/48 | **2/48** |
| DeepSeek@ · t2 | 22/48 | 27/48 | 25/48 | 18/48 | 26/48 | **4/48** |
| DeepSeek@ · t3 | 25/48 | 32/48 | 22/48 | 17/48 | 25/48 | **3/48** |
| gemma4 · t1 | **4/48** | 27/48 | 27/48 | 28/48 | 24/48 | 24/48 |
| gemma4 · t2 | **3/48** | 28/48 | 26/48 | 27/48 | 25/48 | 25/48 |
| gemma4 · t3 | **4/48** | 27/48 | 27/48 | 28/48 | 26/48 | 26/48 |
| glm5.3-flash · t1 | 24/48 | 35/48 | 25/48 | **10/48** | 20/48 | 20/48 |
| glm5.3-flash · t2 | 25/48 | 32/48 | 26/48 | **9/48** | 19/48 | 21/48 |
| glm5.3-flash · t3 | 28/48 | 33/48 | 25/48 | **8/48** | 22/48 | 18/48 |
| mimo-v2.6-flash · t1 | 25/48 | 32/48 | 30/48 | 21/48 | **7/48** | 21/48 |
| mimo-v2.6-flash · t2 | 26/48 | 27/48 | 27/48 | 26/48 | **10/48** | 18/48 |
| mimo-v2.6-flash · t3 | 29/48 | 28/48 | 32/48 | 21/48 | **7/48** | 25/48 |
| qwen3.6 · t1 | 28/48 | **1/48** | 21/48 | 36/48 | 28/48 | 30/48 |
| qwen3.6 · t2 | 28/48 | **1/48** | 21/48 | 36/48 | 28/48 | 30/48 |
| qwen3.6 · t3 | 29/48 | **0/48** | 20/48 | 37/48 | 29/48 | 31/48 |
| qwen3.8-flash · t1 | 26/48 | 21/48 | **1/48** | 30/48 | 32/48 | 24/48 |
| qwen3.8-flash · t2 | 27/48 | 20/48 | **0/48** | 29/48 | 33/48 | 23/48 |
| qwen3.8-flash · t3 | 27/48 | 20/48 | **4/48** | 29/48 | 29/48 | 25/48 |

## H-retro (K = 48; 36 con D > 0)

| medida | valor |
|---|---|
| «mismo» n · min · media · max | 18 · 0,0 % · 7,4 % · 18,8 % |
| «distinto» n · min · media · max | 90 · 12,5 % · 33,5 % · 50,0 % |
| umbral u | 22,9 % (≈ 11,0 de 48) |
| C1 · AUC | 0,982 |
| C2a · falsa alarma (dejando fuera cada modelo) | 0,0 % |
| tasa de cambio por prompt «mismo» (p⁺ Wilson) | 7,41 % (9,35 %) |
| C2b · falsa alarma modelada | 0,410 % |
| C3 · detección (dejando fuera cada modelo) | 92,2 % |

| modelo | u sin él | FA | detección |
|---|---|---|---|
| gemma4 | 22,9 % | 0/3 | 29/30 |
| qwen3.6 | 22,9 % | 0/3 | 24/30 |
| qwen3.8-flash | 22,9 % | 0/3 | 24/30 |
| glm5.3-flash | 22,9 % | 0/3 | 30/30 |
| mimo-v2.6-flash | 22,9 % | 0/3 | 30/30 |
| DeepSeek@ | 22,9 % | 0/3 | 29/30 |

Distancias por tanda (distintas / válidas):

| evaluado · tanda | gemma4 | qwen3.6 | qwen3.8-flash | glm5.3-flash | mimo-v2.6-flash | DeepSeek@ |
|---|---|---|---|---|---|---|
| DeepSeek@ · t1 | 11/48 | 17/48 | 12/48 | 14/48 | 16/48 | **4/48** |
| DeepSeek@ · t2 | 8/48 | 14/48 | 13/48 | 19/48 | 21/48 | **5/48** |
| DeepSeek@ · t3 | 11/48 | 17/48 | 12/48 | 14/48 | 18/48 | **2/48** |
| gemma4 · t1 | **1/48** | 17/48 | 14/48 | 22/48 | 22/48 | 14/48 |
| gemma4 · t2 | **3/48** | 17/48 | 14/48 | 20/48 | 24/48 | 12/48 |
| gemma4 · t3 | **0/48** | 16/48 | 13/48 | 23/48 | 21/48 | 13/48 |
| glm5.3-flash · t1 | 20/48 | 14/48 | 11/48 | **9/48** | 19/48 | 15/48 |
| glm5.3-flash · t2 | 18/48 | 16/48 | 13/48 | **9/48** | 19/48 | 13/48 |
| glm5.3-flash · t3 | 18/48 | 16/48 | 13/48 | **7/48** | 17/48 | 11/48 |
| mimo-v2.6-flash · t1 | 20/48 | 22/48 | 19/48 | 17/48 | **5/48** | 17/48 |
| mimo-v2.6-flash · t2 | 19/48 | 19/48 | 18/48 | 20/48 | **8/48** | 14/48 |
| mimo-v2.6-flash · t3 | 20/48 | 18/48 | 17/48 | 17/48 | **7/48** | 17/48 |
| qwen3.6 · t1 | 16/48 | **0/48** | 7/48 | 21/48 | 23/48 | 15/48 |
| qwen3.6 · t2 | 16/48 | **0/48** | 7/48 | 21/48 | 23/48 | 15/48 |
| qwen3.6 · t3 | 16/48 | **0/48** | 7/48 | 21/48 | 23/48 | 15/48 |
| qwen3.8-flash · t1 | 14/48 | 6/48 | **1/48** | 19/48 | 19/48 | 13/48 |
| qwen3.8-flash · t2 | 14/48 | 6/48 | **1/48** | 19/48 | 19/48 | 13/48 |
| qwen3.8-flash · t3 | 15/48 | 7/48 | **2/48** | 18/48 | 18/48 | 14/48 |

## C4 · caso DeepSeek (H-retro)

- u_retro = 22,9 %
- (a) 4.1 registrada frente a DeepSeek@ registrada: 5/48 = 10,4 % → sin alarma
- (b) DeepSeek@ hoy (t1) frente a la referencia de la 4.1: 5/48 = 10,4 %
- (b) DeepSeek@ hoy (t2) frente a la referencia de la 4.1: 8/48 = 16,7 %
- (b) DeepSeek@ hoy (t3) frente a la referencia de la 4.1: 7/48 = 14,6 %
- (b) sin alarma en alguna tanda
- 4.1 registrada frente a los otros activos (distintas de 48): gemma4 16, qwen3.6 14, qwen3.8-flash 11, glm5.3-flash 15, mimo-v2.6-flash 17

## C5 · coste

- llamadas físicas por comprobación de H-oficial (escaladas a K = 48 desde las tandas): mediana 48,0, máx. 48,6
- llamadas de las tandas de calibración: 1495

## Informativo · 13 modelos con respuestas registradas (H-oficial)

Distintas / válidas entre las respuestas registradas de cada pareja (sin llamadas; la selección usa los 6 de NaN, así que las parejas de NaN están infladas).

| pareja | distintas / válidas |
|---|---|
| claude-opus-5.5#low · gpt-6.1-sol#low | 8/48 |
| glm5.3-flash · gemini-3.7-flash | 14/48 |
| DeepSeek@ · deepseek-v4-pro-0813 | 15/48 |
| claude-haiku-5.5 · gpt-6.1-sol#low | 15/48 |
| gpt-5.6-luna · gpt-6.1-sol#low | 15/48 |
| claude-opus-5.5#low · gemini-4-argon | 15/46 |
| qwen3.8-flash · deepseek-v4-pro-0813 | 16/48 |
| glm5.3-flash · DeepSeek@ | 16/48 |
| DeepSeek@ · gpt-6.1-sol#low | 16/48 |
| claude-haiku-5.5 · gpt-5.6-luna | 16/48 |
| gemini-3.7-flash · gpt-6.1-sol#low | 16/48 |
| gemini-3.7-flash · gemini-4-argon | 16/46 |

(Las 12 parejas más cercanas de 78; todas en `huella.json`.)

## Informativo · datos en cuarentena del 17-10 (mañana)

Distancia de sus respuestas R3 (réplica 0) a cada modelo, en los prompts comunes:

| modelo | distintas / válidas |
|---|---|
| gemma4 | 47/250 (18,8 %) |
| qwen3.6 | 65/251 (25,9 %) |
| qwen3.8-flash | 43/251 (17,1 %) |
| glm5.3-flash | 39/251 (15,5 %) |
| mimo-v2.6-flash | 45/251 (17,9 %) |
| DeepSeek@ | 6/233 (2,6 %) |
