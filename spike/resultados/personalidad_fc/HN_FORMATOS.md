# Pasada de formatos H/N en NaN (PERSONALIDAD.md §31.1, §32)

Generado por `analizar_personalidad_hn.py` sin llamadas a modelos. 6 modelos de NaN: gemma4, qwen3.6, qwen3.8-flash, glm5.3-flash, mimo-v2.6-flash, deepseek-v4-flash@2026-10-17. Puntuación 0–1 con 1 = polo alto del rasgo; sd entre modelos en la escala del cuadro (×50). Línea base: situaciones v3 del rasgo en los mismos 6 modelos, elección bruta.

## Q1–Q7 por formato

| formato | rasgo | ítems | Q1 pérdidas máx. | Q2 % ítems sd ≥ 0,10 | Q3 sd modelos [IC 95 %] | Q4 ítem-resto | Q5 retest | Q6/Q7 | alfa | media | pasa |
|---|---|---|---|---|---|---|---|---|---|---|---|
| *línea base v3* | H | 59 | — | 66 % | 0.3 [0.0; 3.0] | 0.06 | — | — | 0.04 | 0.37 | — |
| *línea base v3* | N | 57 | — | 67 % | 1.6 [0.0; 4.0] | 0.12 | — | — | 0.46 | 0.52 | — |
| HE · escalera de tentación | H | 16 | 0.0 % ✔ | 44 % ✘ | 6.1 [2.3; 10.4] ✔ | 0.61 ✔ | 0.97 ✔ | equidad 2.2 · modestia 2.8 ✘ | 0.85 | 0.67 | no |
| HD · reparto tipo dictador | H | 8 | 0.0 % ✔ | 100 % ✔ | 8.1 [6.8; 10.1] ✔ | 0.76 ✔ | 0.64 ✘ | — | 0.92 | 0.84 | no |
| HM · informe con incentivo a mentir | H | 8 | 0.0 % ✔ | 50 % ✘ | 3.7 [0.0; 12.7] ✘ | 0.23 ✔ | 0.95 ✔ | — | 0.38 | 0.33 | no |
| HO · sobreafirmación (exploratorio) | H | 12 | 0.0 % ✔ | 92 % ✔ | 6.7 [3.3; 11.2] ✔ | 0.46 ✔ | 0.51 ✘ | — | 0.78 | 0.84 | no |
| NG · intensidad graduada | N | 36 | 1.4 % ✔ | 44 % ✘ | 2.4 [1.7; 3.2] ✘ | 0.40 ✔ | 0.78 ✘ | — | 0.87 | 0.58 | no |
| NS · dos opciones serenas | N | 12 | 0.0 % ✔ | 83 % ✔ | 5.2 [2.6; 9.7] ✔ | 0.36 ✔ | 0.83 ✘ | elige lo deseable 70 % ✘ | 0.68 | 0.58 | no |
| NC · crítica o fracaso en dos turnos | N | 24 | 3.1 % ✔ | 12 % ✘ | 2.5 [1.6; 3.6] ✘ | 0.56 ✔ | 0.76 ✘ | — | 0.90 | 0.31 | no |
| NS24 · dos opciones serenas (las 24, informativo) | N | 24 | 0.0 % ✔ | 67 % ✘ | 2.6 [0.0; 5.7] ✘ | 0.21 ✔ | 0.85 ✘ | elige lo deseable 84 % ✘ | 0.60 | 0.76 | — |

Pasa a los externos si cumple Q1–Q5, y Q6 (HE) o Q7 (NS) cuando aplica (§31.1).

## Perfil por modelo (media del formato ×50)

| modelo | HE | HD | HM | HO | NG | NS | NC | NS24 |
|---|---|---|---|---|---|---|---|---|
| gemma4 | 22.0 | 50.0 | 12.5 | 45.8 | 29.0 | 31.2 | 17.2 | 40.1 |
| qwen3.6 | 30.5 | 35.9 | 14.1 | 28.5 | 27.4 | 36.5 | 18.1 | 42.2 |
| qwen3.8-flash | 32.2 | 42.7 | 12.5 | 38.2 | 27.3 | 27.1 | 12.8 | 36.5 |
| glm5.3-flash | 39.4 | 47.3 | 25.0 | 43.8 | 26.6 | 29.2 | 11.7 | 39.1 |
| mimo-v2.6-flash | 36.7 | 48.4 | 12.5 | 45.5 | 31.8 | 31.2 | 16.2 | 38.5 |
| deepseek-v4-flash@2026-10-17 | 39.2 | 28.4 | 23.4 | 50.0 | 32.5 | 17.7 | 16.9 | 32.3 |

## HE por faceta y por nivel

| faceta | sd modelos [IC] | elección honesta media | nivel 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|
| todas | — | — | 0.66 | 0.68 | 0.66 | 0.66 | 0.67 |
| equidad | 2.2 [0.0; 12.8] | 0.89 | 0.85 | 0.90 | 0.91 | 0.89 | 0.92 |
| modestia | 2.8 [0.0; 9.7] | 0.39 | 0.44 | 0.41 | 0.39 | 0.36 | 0.38 |
| sinceridad | 12.6 [1.4; 20.8] | 0.74 | 0.71 | 0.75 | 0.72 | 0.76 | 0.78 |
| desinteres_riqueza | 0.0 [0.0; 12.5] | 0.64 | 0.65 | 0.66 | 0.65 | 0.64 | 0.60 |

## NG por faceta

| faceta | sd modelos | media |
|---|---|---|
| ansiedad | 0.0 | 0.61 |
| hostilidad | 3.8 | 0.53 |
| depresion | 2.0 | 0.67 |
| autoconciencia | 5.3 | 0.36 |
| impulsividad | 2.9 | 0.63 |
| vulnerabilidad | 2.1 | 0.69 |

## Componentes y descriptivos por modelo

| modelo | HD % dado | HM exceso medio | HO afirmación reales / inexistentes (0–6) | NC malestar (0–10) | NC elige reactiva | % A en HE | % A en NS | % A en NC |
|---|---|---|---|---|---|---|---|---|
| gemma4 | 50 | +5.12 | 6.00 / 0.50 | 6.56 | 3 % | 48 % | 43 % | 49 % |
| qwen3.6 | 36 | +4.19 | 6.00 / 2.58 | 6.72 | 6 % | 44 % | 55 % | 49 % |
| qwen3.8-flash | 45 | +4.22 | 5.92 / 1.42 | 4.92 | 2 % | 44 % | 44 % | 48 % |
| glm5.3-flash | 47 | +3.88 | 5.42 / 0.75 | 4.69 | 0 % | 45 % | 43 % | 50 % |
| mimo-v2.6-flash | 48 | +5.12 | 5.79 / 0.54 | 6.08 | 4 % | 50 % | 54 % | 48 % |
| deepseek-v4-flash@2026-10-17 | 28 | +4.00 | 5.79 / 0.00 | 6.15 | 6 % | 48 % | 40 % | 44 % |

HO frente a la media de HE, HD, HM: r = +0.45 (umbral de §32.4: +0,50).

NS: 12 situaciones evaluadas (ventana 30–70 % o las 12 más cercanas al 50 %): NS11, NS23, NS17, NS09, NS08, NS20, NS22, NS21, NS07, NS19, NS04, NS01.

## Descriptivo (n = 6): correlación del perfil de cada formato con la elección v3 por rasgo y con la deseabilidad propia de H

| formato | O | C | E | A | N | H | deseabilidad propia H (v3) |
|---|---|---|---|---|---|---|---|
| HE | -0.19 | -0.77 | -0.10 | +0.54 | -0.77 | +0.91 | +0.39 |
| HD | +0.58 | +0.57 | +0.32 | +0.05 | -0.12 | -0.47 | +0.33 |
| HM | -0.13 | -0.46 | -0.67 | +0.02 | -0.68 | +0.83 | +0.41 |
| HO | -0.02 | -0.22 | -0.63 | -0.38 | -0.35 | +0.52 | +0.36 |
| NG | -0.01 | -0.24 | -0.19 | -0.03 | +0.17 | +0.35 | -0.33 |
| NS | +0.66 | +0.74 | +0.75 | +0.42 | +0.39 | -0.78 | -0.37 |
| NC | +0.26 | +0.42 | +0.11 | -0.07 | +0.87 | -0.40 | -0.96 |
| NS24 | +0.71 | +0.81 | +0.60 | +0.33 | +0.37 | -0.77 | -0.35 |

Correlación entre formatos (perfiles por modelo, n = 6): HE–HD -0.36 · HE–HM +0.69 · HE–HO +0.27 · HE–NG +0.26 · HE–NS -0.49 · HE–NC -0.41 · HD–HM -0.38 · HD–HO +0.10 · HD–NG -0.31 · HD–NS +0.53 · HD–NC -0.36 · HM–HO +0.40 · HM–NG +0.04 · HM–NS -0.57 · HM–NC -0.36 · HO–NG +0.65 · HO–NS -0.70 · HO–NC -0.12 · NG–NS -0.53 · NG–NC +0.51 · NS–NC +0.17

## Coste de pasar cada formato a los 7 externos

Tokens medios por llamada medidos aquí, divididos por los de las llamadas v3 de los mismos modelos en NaN (157 de entrada / 1.8 de salida), por la tarifa y los tokens v3 de cada externo (`propuesta_hn_coste.py`).

| formato | llamadas por modelo | factor entrada / salida | coste en los 7 | pasa |
|---|---|---|---|---|
| HE | 160 | 1.08 / 1.01 | 0.673 $ | no |
| HD | 32 | 1.20 / 1.53 | 0.176 $ | no |
| HM | 32 | 1.13 / 1.18 | 0.148 $ | no |
| HO | 72 | 0.83 / 1.27 | 0.305 $ | no |
| NG | 72 | 1.09 / 2.61 | 0.538 $ | no |
| NS | 72 | 0.91 / 1.00 | 0.277 $ | no |
| NC | 96 | 1.44 / 2.12 | 0.689 $ | no |

Formatos que pasan: ≈ 0.00 $ (0.00 $ con margen del 25 %).

