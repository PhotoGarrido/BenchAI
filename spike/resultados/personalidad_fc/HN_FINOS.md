# Instrumentos finos para H y N en NaN (PERSONALIDAD.md §34)

Generado por `analizar_personalidad_hn_finos.py` sin llamadas a modelos. 6 modelos de NaN: gemma4, qwen3.6, qwen3.8-flash, glm5.3-flash, mimo-v2.6-flash, deepseek-v4-flash@2026-10-17. Puntuación 0–1 con 1 = polo alto; sd entre modelos ×50. Línea base (v3, elección bruta, mismos 6): H sd 0.3, N sd 1.6. R = 2.19 (§34.3).

## K1 · pérdidas por modelo e instrumento

| modelo | I1 | I2 | I3 |
|---|---|---|---|
| gemma4 | 0.0 % | 0.0 % | 7.1 % |
| qwen3.6 | 0.0 % | 0.0 % | 0.0 % |
| qwen3.8-flash | 0.0 % | 0.0 % | 0.0 % |
| glm5.3-flash | 0.1 % | 0.0 % | 0.0 % |
| mimo-v2.6-flash | 0.1 % | 0.0 % | 0.0 % |
| deepseek-v4-flash@2026-10-17 | 0.0 % | 0.0 % | 0.0 % |

## Escalas: K2–K10

| escala | n | sd modelos [IC] | ruido | ρ₁ | alfa | SB particiones (mediana) | ítem-resto (% < 0) | retest | elige lo deseable | facetas (n · sd) | r E v3 / C v3 | k 0,70 / 0,80 con los 13 (R) | k 0,70 con R = 1 | entra |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| I1-H · GR · banda | 37 | 2.2 [1.1; 3.8] ✘ | 6.8 | 0.096 | 0.80 | 0.88 | 0.26 (27 %) ✘ | 0.74 ✘ | 67 % ✔ | desin 12·1.3 · equid 5·0.9 · modes 9·3.5 · since 11·3.7 ✔ | -0.53 / -0.82 | 10 / 17 ✔ | 22 | no |
| I1-H · GR · completa | 48 | 1.8 [1.0; 3.1] ✘ | 7.1 | 0.060 | 0.76 | 0.84 | 0.23 (38 %) ✘ | 0.83 ✘ | 72 % ✘ | desin 12·1.3 · equid 12·0.9 · modes 12·2.8 · since 12·3.2 ✘ | -0.75 / -0.72 | 17 / 28 ✔ | 36 | no |
| I1-N · GR · banda | 42 | 1.3 [0.8; 2.4] ✘ | 6.3 | 0.043 | 0.66 | 0.75 | 0.17 (33 %) ✘ | 0.74 ✘ | 85 % ✘ | ansie 10·2.7 · autoc 4·3.6 · depre 9·1.0 · hosti 7·0.0 · impul 6·2.0 · vulne 6·2.0 ✔ | +0.63 / -0.00 | 24 / 40 ✔ | 51 | no |
| I1-N · GR · completa | 72 | 2.2 [1.7; 3.0] ✘ | 5.9 | 0.125 | 0.91 | 0.95 | 0.33 (21 %) ✔ | 0.81 ✘ | 92 % ✘ | ansie 12·2.3 · autoc 12·3.2 · depre 12·1.5 · hosti 12·2.0 · impul 12·3.8 · vulne 12·2.7 ✔ | +0.50 / -0.33 | 7 / 13 ✔ | 16 | no |
| I2-H · GR · banda | 24 | 1.0 [0.0; 2.9] ✘ | 7.1 | 0.019 | 0.32 | 0.48 | 0.17 (42 %) ✘ | 0.66 ✘ | 81 % ✘ | explo 3·0.0 · lealt 3·3.2 · modes 7·0.0 · piado 6·0.0 · tacto 5·4.0 ✔ | -0.42 / -0.11 | 54 / 93 ✔ | 118 | no |
| I2-H · GR · completa | 40 | 2.1 [1.5; 3.1] ✘ | 6.3 | 0.103 | 0.82 | 0.87 | 0.35 (20 %) ✔ | 0.74 ✘ | 89 % ✘ | explo 8·2.0 · lealt 8·3.2 · modes 8·1.2 · piado 8·0.0 · tacto 8·3.8 ✔ | -0.52 / +0.13 | 9 / 16 ✔ | 20 | no |
| I1+I2-H · GR · banda | 61 | 1.5 [0.7; 2.6] ✘ | 7.0 | 0.042 | 0.73 | 0.81 | 0.20 (33 %) ✘ | 0.72 ✘ | 72 % ✘ | desin 12·1.3 · equid 5·0.9 · explo 3·0.0 · lealt 3·3.2 · modes 9·3.5 · modes 7·0.0 · piado 6·0.0 · since 11·3.7 · tacto 5·4.0 ✔ | -0.64 / -0.76 | 24 / 42 ✔ | 53 | no |
| I1+I2-H · GR · completa | 88 | 1.6 [1.1; 2.3] ✘ | 6.8 | 0.053 | 0.83 | 0.89 | 0.25 (25 %) ✔ | 0.81 ✘ | 80 % ✘ | desin 12·1.3 · equid 12·0.9 · explo 8·2.0 · lealt 8·3.2 · modes 12·2.8 · modes 8·1.2 · piado 8·0.0 · since 12·3.2 · tacto 8·3.8 ✔ | -0.79 / -0.38 | 19 / 33 ✔ | 42 | no |
| I1-H · BI · banda | 12 | 9.7 [7.0; 14.2] ✔ | 14.5 | 0.310 | 0.84 | 0.89 | 0.51 (8 %) ✔ | 0.69 ✘ | 73 % ✘ | desin 3·6.2 · equid 2·10.2 · modes 4·9.4 · since 3·18.0 ✔ | -0.42 / -0.89 | 2 / 4 ✔ | 5 | no |
| I1-H · BI · completa | 24 | 5.5 [3.3; 8.7] ✔ | 12.2 | 0.168 | 0.83 | 0.90 | 0.44 (12 %) ✔ | 0.84 ✘ | 79 % ✘ | desin 6·5.9 · equid 6·5.0 · modes 6·6.0 · since 6·8.6 ✔ | -0.43 / -0.90 | 5 / 9 ✔ | 12 | no |
| I1-N · BI · banda | 12 | 0.0 [0.0; 7.2] ✘ | 15.3 | 0.000 | -1.25 | -1.36 | -0.12 (67 %) ✘ | 0.76 ✘ | 69 % ✔ | ansie 4·0.0 · depre 4·0.0 · hosti 4·0.0 ✘ | +0.06 / +0.44 | — / — ✘ | — | no |
| I1-N · BI · completa | 36 | 0.0 [0.0; 2.8] ✘ | 8.9 | 0.000 | -0.50 | -0.47 | 0.02 (53 %) ✘ | 0.91 ✔ | 91 % ✘ | ansie 6·0.0 · autoc 6·0.0 · depre 6·0.0 · hosti 6·0.0 · impul 6·1.6 · vulne 6·0.0 ✔ | +0.13 / +0.39 | — / — ✘ | — | no |
| I2-H · BI · banda | 12 | 1.2 [0.0; 4.9] ✘ | 8.1 | 0.021 | 0.20 | 0.38 | 0.11 (38 %) ✘ | 0.81 ✘ | 90 % ✘ | explo 2·8.5 · lealt 4·0.0 · modes 4·0.0 · piado 2·4.6 ✔ | +0.02 / -0.53 | 50 / 85 ✔ | 109 | no |
| I2-H · BI · completa | 20 | 0.7 [0.0; 3.0] ✘ | 6.3 | 0.012 | 0.20 | 0.35 | 0.11 (38 %) ✘ | 0.83 ✘ | 90 % ✘ | explo 4·3.5 · lealt 4·0.0 · modes 4·0.0 · piado 4·1.9 · tacto 4·0.0 ✘ | +0.02 / -0.53 | 87 / 149 ✘ | 190 | no |
| I1+I2-H · BI · banda | 12 | 9.3 [6.3; 13.9] ✔ | 14.7 | 0.285 | 0.83 | 0.87 | 0.48 (8 %) ✔ | 0.68 ✘ | 70 % ✘ | desin 2·0.0 · equid 2·10.2 · modes 4·9.4 · modes 1·— · since 3·18.0 ✔ | -0.33 / -0.91 | 3 / 5 ✔ | 6 | no |
| I1+I2-H · BI · completa | 44 | 3.4 [2.0; 5.5] ✘ | 10.2 | 0.099 | 0.83 | 0.90 | 0.37 (12 %) ✔ | 0.85 ✔ | 84 % ✘ | desin 6·5.9 · equid 6·5.0 · explo 4·3.5 · lealt 4·0.0 · modes 6·6.0 · modes 4·0.0 · piado 4·1.9 · since 6·8.6 · tacto 4·0.0 ✔ | -0.38 / -0.89 | 10 / 17 ✔ | 21 | no |
| I3-H · elección forzada | 22 | 2.3 [0.0; 6.5] ✘ | 12.3 | 0.034 | 0.43 | 0.61 | 0.13 (47 %) ✘ | 0.70 ✘ | — | desin 5·4.7 · equid 5·0.0 · modes 6·0.0 · since 6·0.0 ✘ | -0.68 / -0.52 | 31 / 52 ✔ | 67 | no |
| I3-N · elección forzada | 23 | 0.0 [0.0; 5.5] ✘ | 12.9 | 0.000 | -0.07 | 0.08 | 0.03 (52 %) ✘ | 0.62 ✘ | — | ansie 4·3.6 · autoc 4·0.0 · depre 4·3.4 · hosti 3·0.0 · impul 4·0.0 · vulne 4·0.0 ✔ | +0.31 / +0.96 **veto** | — / — ✘ | — | no |

Entra en el paquete si cumple K1, K2, K4, K5, K6, K7 (salvo I3) y K10 sin veto de K8 (§34.3). k = situaciones necesarias para esa fiabilidad entre modelos.

## Banda de dificultad

| escala · formato | candidatas | en banda 0,25–0,75 | seleccionadas |
|---|---|---|---|
| I1-H|GR | 48 | 37 | 37 |
| I1-N|GR | 72 | 42 | 42 |
| I2-H|GR | 40 | 24 | 24 |
| I1+I2-H|GR | 88 | 61 | 61 |
| I1-H|BI | 24 | 10 | 12 |
| I1-N|BI | 36 | 5 | 12 |
| I2-H|BI | 20 | 1 | 12 |
| I1+I2-H|BI | 44 | 11 | 12 |

## Selección cruzada (graduado): banda con una réplica, señal con la otra

| escala | banda rep. 0 → mide rep. 1: n · sd · alfa | banda rep. 1 → mide rep. 0 |
|---|---|---|
| I1-H | 39 · 2.0 · 0.73 | 37 · 2.5 · 0.80 |
| I1-N | 44 · 1.5 · 0.66 | 44 · 1.4 · 0.63 |
| I2-H | 23 · 1.4 · 0.39 | 25 · 1.1 · 0.34 |
| I1+I2-H | 62 · 1.6 · 0.71 | 62 · 1.7 · 0.74 |

## K9 · graduado frente a binario (subconjunto común, sin banda)

| ítems | n | ρ₁ graduado | ρ₁ binario | razón [IC] | sd modelos GR / BI | ruido GR / BI | retest GR / BI | r perfiles GR–BI | gana el graduado |
|---|---|---|---|---|---|---|---|---|---|
| todas | 80 | 0.005 | 0.017 | 0.30 [0.00; —] | 0.5 / 1.3 | 6.5 / 9.9 | 0.86 / 0.91 | 0.76 | ✘ |
| H | 44 | 0.045 | 0.099 | 0.46 [0.10; 1.91] | 1.4 / 3.4 | 6.6 / 10.2 | 0.78 / 0.85 | 0.23 | ✘ |
| N | 36 | 0.060 | 0.000 | — [0.57; —] | 1.5 / 0.0 | 6.0 / 8.9 | 0.84 / 0.91 | -0.19 | ✘ |

## ¿Conducta, ideal o estilo? (n = 6, descriptivo)

r del perfil de cada escala con el perfil de deseabilidad propia (mismos ítems, prompt DS) y con la extremosidad del graduado de cada modelo (media de |puntos − 50|/50).

| escala | r con la deseabilidad propia | r con la extremosidad | r ítems elección–deseabilidad |
|---|---|---|---|
| I1-H · GR · banda | 0.62 | -0.65 | 0.36 |
| I1-H · GR · completa | 0.58 | -0.46 | 0.49 |
| I1-N · GR · banda | 0.40 | -0.19 | 0.79 |
| I1-N · GR · completa | 0.18 | -0.50 | 0.78 |
| I2-H · GR · banda | -0.34 | 0.49 | 0.73 |
| I2-H · GR · completa | -0.38 | 0.55 | 0.75 |
| I1+I2-H · GR · banda | 0.44 | -0.37 | 0.47 |
| I1+I2-H · GR · completa | 0.16 | 0.04 | 0.58 |
| I1-H · BI · banda | 0.70 | -0.80 | 0.12 |
| I1-H · BI · completa | 0.81 | -0.85 | 0.42 |
| I1-N · BI · banda | -0.09 | 0.62 | 0.54 |
| I1-N · BI · completa | -0.31 | 0.73 | 0.85 |
| I2-H · BI · banda | 0.52 | -0.22 | 0.74 |
| I2-H · BI · completa | 0.44 | -0.22 | 0.60 |
| I1+I2-H · BI · banda | 0.72 | -0.78 | 0.24 |
| I1+I2-H · BI · completa | 0.81 | -0.79 | 0.51 |
| I3-H · elección forzada | — | -0.20 | — |
| I3-N · elección forzada | — | 0.82 | — |

## Perfil por modelo (×50)

| escala | gemma4 | qwen3.6 | qwen3.8-flash | glm5.3-flash | mimo-v2.6-flash | deepseek-v4-flash@2026-10-17 |
|---|---|---|---|---|---|---|
| I1-H · GR · banda | 22.6 | 24.6 | 25.3 | 27.4 | 25.0 | 29.8 |
| I1-H · GR · completa | 26.5 | 27.3 | 27.9 | 29.0 | 26.2 | 31.8 |
| I1-N · GR · banda | 19.2 | 21.9 | 19.5 | 21.3 | 23.7 | 20.5 |
| I1-N · GR · completa | 13.0 | 16.4 | 15.2 | 17.2 | 20.1 | 16.3 |
| I2-H · GR · banda | 30.7 | 31.6 | 31.6 | 30.0 | 27.0 | 31.2 |
| I2-H · GR · completa | 36.8 | 36.4 | 35.9 | 34.8 | 30.5 | 35.8 |
| I1+I2-H · GR · banda | 25.8 | 27.4 | 27.8 | 28.4 | 25.8 | 30.3 |
| I1+I2-H · GR · completa | 31.2 | 31.4 | 31.5 | 31.6 | 28.1 | 33.6 |
| I1-H · BI · banda | 14.6 | 19.8 | 33.3 | 39.6 | 27.1 | 40.6 |
| I1-H · BI · completa | 24.5 | 26.0 | 34.9 | 37.5 | 31.8 | 39.1 |
| I1-N · BI · banda | 30.2 | 29.2 | 26.0 | 21.9 | 27.1 | 28.1 |
| I1-N · BI · completa | 14.2 | 14.9 | 12.8 | 11.5 | 13.2 | 13.9 |
| I2-H · BI · banda | 37.5 | 40.6 | 43.8 | 43.8 | 38.5 | 39.6 |
| I2-H · BI · completa | 42.5 | 44.4 | 46.2 | 46.2 | 43.1 | 43.8 |
| I1+I2-H · BI · banda | 11.5 | 18.8 | 32.3 | 36.5 | 25.0 | 36.5 |
| I1+I2-H · BI · completa | 32.7 | 34.4 | 40.1 | 41.5 | 36.9 | 41.2 |
| I3-H · elección forzada | 31.2 | 33.5 | 31.2 | 33.0 | 30.1 | 39.8 |
| I3-N · elección forzada | 19.6 | 19.0 | 14.1 | 15.8 | 15.8 | 13.0 |

## K8 · correlación del perfil con el v3 (n = 6, descriptivo; veto si |r| ≥ 0,80 con E en H o con C en N)

| escala | O | C | E | A | N | H | sinceridad v3 | I3 |
|---|---|---|---|---|---|---|---|---|
| I1-H · GR · banda | -0.47 | -0.82 | -0.53 | +0.10 | -0.61 | +0.97 | +0.94 | 0.81 |
| I1-H · GR · completa | -0.60 | -0.72 | -0.75 | -0.24 | -0.43 | +0.84 | +0.89 | 0.92 |
| I1-N · GR · banda | +0.56 | -0.00 | +0.63 | +0.92 | -0.11 | +0.15 | -0.08 | 0.00 |
| I1-N · GR · completa | +0.30 | -0.33 | +0.50 | +0.88 | -0.40 | +0.43 | +0.23 | -0.35 |
| I2-H · GR · banda | -0.61 | -0.11 | -0.42 | -0.55 | +0.22 | -0.10 | +0.05 | 0.43 |
| I2-H · GR · completa | -0.41 | +0.13 | -0.52 | -0.68 | +0.30 | -0.22 | -0.08 | 0.36 |
| I1+I2-H · GR · banda | -0.65 | -0.76 | -0.64 | -0.14 | -0.45 | +0.81 | +0.84 | 0.88 |
| I1+I2-H · GR · completa | -0.62 | -0.38 | -0.79 | -0.56 | -0.09 | +0.40 | +0.52 | 0.80 |
| I1-H · BI · banda | -0.52 | -0.89 | -0.42 | +0.13 | -0.85 | +0.95 | +0.92 | 0.52 |
| I1-H · BI · completa | -0.54 | -0.90 | -0.43 | +0.09 | -0.84 | +0.95 | +0.94 | 0.51 |
| I1-N · BI · banda | +0.04 | +0.44 | +0.06 | -0.37 | +0.96 | -0.58 | -0.40 | 0.46 |
| I1-N · BI · completa | +0.04 | +0.39 | +0.13 | -0.20 | +0.95 | -0.53 | -0.41 | 0.48 |
| I2-H · BI · banda | -0.46 | -0.53 | +0.02 | +0.20 | -0.69 | +0.35 | +0.29 | -0.03 |
| I2-H · BI · completa | -0.46 | -0.53 | +0.02 | +0.20 | -0.69 | +0.35 | +0.29 | -0.03 |
| I1+I2-H · BI · banda | -0.55 | -0.91 | -0.33 | +0.19 | -0.85 | +0.92 | +0.88 | 0.47 |
| I1+I2-H · BI · completa | -0.56 | -0.89 | -0.38 | +0.12 | -0.87 | +0.91 | +0.88 | 0.44 |
| I3-H · elección forzada | -0.45 | -0.52 | -0.68 | -0.23 | -0.08 | +0.66 | +0.72 | — |
| I3-N · elección forzada | +0.69 | +0.96 | +0.31 | -0.04 | +0.65 | -0.85 | -0.92 | — |

## Facetas de las escalas en banda (graduado)

| escala | faceta | n | sd modelos | media | r con el resto |
|---|---|---|---|---|---|
| I1-H · GR · banda | desinteres_riqueza | 12 | 1.3 | 0.57 | 0.74 |
| I1-H · GR · banda | equidad | 5 | 0.9 | 0.55 | -0.22 |
| I1-H · GR · banda | modestia | 9 | 3.5 | 0.47 | 0.79 |
| I1-H · GR · banda | sinceridad | 11 | 3.7 | 0.48 | 0.47 |
| I1-N · GR · banda | ansiedad | 10 | 2.7 | 0.55 | -0.14 |
| I1-N · GR · banda | autoconciencia | 4 | 3.6 | 0.29 | 0.86 |
| I1-N · GR · banda | depresion | 9 | 1.0 | 0.43 | 0.20 |
| I1-N · GR · banda | hostilidad | 7 | 0.0 | 0.42 | 0.32 |
| I1-N · GR · banda | impulsividad | 6 | 2.0 | 0.37 | 0.81 |
| I1-N · GR · banda | vulnerabilidad | 6 | 2.0 | 0.33 | 0.36 |
| I2-H · GR · banda | explotar | 3 | 0.0 | 0.64 | -0.15 |
| I2-H · GR · banda | lealtad | 3 | 3.2 | 0.66 | 0.37 |
| I2-H · GR · banda | modestia_util | 7 | 0.0 | 0.55 | -0.27 |
| I2-H · GR · banda | piadosa | 6 | 0.0 | 0.56 | 0.08 |
| I2-H · GR · banda | tacto | 5 | 4.0 | 0.70 | 0.80 |
| I1+I2-H · GR · banda | desinteres_riqueza | 12 | 1.3 | 0.57 | 0.78 |
| I1+I2-H · GR · banda | equidad | 5 | 0.9 | 0.55 | -0.28 |
| I1+I2-H · GR · banda | explotar | 3 | 0.0 | 0.64 | -0.36 |
| I1+I2-H · GR · banda | lealtad | 3 | 3.2 | 0.66 | -0.03 |
| I1+I2-H · GR · banda | modestia | 9 | 3.5 | 0.47 | 0.76 |
| I1+I2-H · GR · banda | modestia_util | 7 | 0.0 | 0.55 | -0.32 |
| I1+I2-H · GR · banda | piadosa | 6 | 0.0 | 0.56 | 0.50 |
| I1+I2-H · GR · banda | sinceridad | 11 | 3.7 | 0.48 | 0.34 |
| I1+I2-H · GR · banda | tacto | 5 | 4.0 | 0.70 | 0.38 |
| I3-H · elección forzada | desinteres_riqueza | 5 | 4.7 | 0.61 | 0.12 |
| I3-H · elección forzada | equidad | 5 | 0.0 | 0.62 | 0.63 |
| I3-H · elección forzada | modestia | 6 | 0.0 | 0.55 | 0.53 |
| I3-H · elección forzada | sinceridad | 6 | 0.0 | 0.85 | 0.63 |
| I3-N · elección forzada | ansiedad | 4 | 3.6 | 0.26 | -0.46 |
| I3-N · elección forzada | autoconciencia | 4 | 0.0 | 0.34 | 0.41 |
| I3-N · elección forzada | depresion | 4 | 3.4 | 0.25 | 0.14 |
| I3-N · elección forzada | hostilidad | 3 | 0.0 | 0.47 | -0.55 |
| I3-N · elección forzada | impulsividad | 4 | 0.0 | 0.39 | 0.39 |
| I3-N · elección forzada | vulnerabilidad | 4 | 0.0 | 0.27 | 0.71 |

I3: |Δ deseabilidad| media en las parejas = 0.50 (escala 1–5).

## Graduado: uso de la escala por modelo

| modelo | respuestas | media de puntos a A | % 50 | % 0 o 100 | valores distintos | % «A» en BI y FC |
|---|---|---|---|---|---|---|
| gemma4 | 640 | 49.8 | 5 % | 29 % | 12 | 47 % |
| qwen3.6 | 640 | 51.1 | 5 % | 30 % | 17 | 51 % |
| qwen3.8-flash | 640 | 45.4 | 1 % | 15 % | 22 | 46 % |
| glm5.3-flash | 639 | 57.6 | 1 % | 4 % | 20 | 45 % |
| mimo-v2.6-flash | 639 | 63.8 | 1 % | 1 % | 21 | 46 % |
| deepseek-v4-flash@2026-10-17 | 640 | 50.3 | 3 % | 6 % | 21 | 47 % |

## Proyección de Spearman-Brown: referencia v3 con los 13

Razones v_m(13)/v_m(6) del v3: O 4.8 · C 0.9 · E 1.8 · A 4.0 · N 1.6 · H 36.5; R = 2.19 (O, C, E, A, N). Situaciones del v3 necesarias para 0,70 con los 13: O 18 · C 49 · E 25 · A 17 · N 118 · H 131.

## Coste en los 7 externos

Tokens medios por llamada medidos aquí frente a los del v3 en los mismos modelos de NaN (157 de entrada / 1.8 de salida): D3 139/1.8 · GR 220/2.6 · FC 116/3.7 · DS 163/1.9 · BI 151/1.9. 2 órdenes × 2 réplicas por ítem.

| escala | entra | ítems | llamadas por modelo | coste en los 7 | k 0,70 con los 13 | coste con k 0,70 ítems |
|---|---|---|---|---|---|---|
| I1-H|GR|banda | no | 37 | 148 | 0.841 $ | 10 | 0.229 $ |
| I1-H|GR|completa | no | 48 | 192 | 1.092 $ | 17 | 0.377 $ |
| I1-N|GR|banda | no | 42 | 168 | 0.955 $ | 24 | 0.535 $ |
| I1-N|GR|completa | no | 72 | 288 | 1.637 $ | 7 | 0.170 $ |
| I2-H|GR|banda | no | 24 | 96 | 0.546 $ | 54 | 1.231 $ |
| I2-H|GR|completa | no | 40 | 160 | 0.910 $ | 9 | 0.211 $ |
| I1+I2-H|GR|banda | no | 61 | 244 | 1.387 $ | 24 | 0.556 $ |
| I1+I2-H|GR|completa | no | 88 | 352 | 2.001 $ | 19 | 0.432 $ |
| I1-H|BI|banda | no | 12 | 48 | 0.195 $ | 2 | 0.038 $ |
| I1-H|BI|completa | no | 24 | 96 | 0.390 $ | 5 | 0.086 $ |
| I1-N|BI|banda | no | 12 | 48 | 0.195 $ | — | — $ |
| I1-N|BI|completa | no | 36 | 144 | 0.584 $ | — | — $ |
| I2-H|BI|banda | no | 12 | 48 | 0.195 $ | 50 | 0.808 $ |
| I2-H|BI|completa | no | 20 | 80 | 0.325 $ | 87 | 1.408 $ |
| I1+I2-H|BI|banda | no | 12 | 48 | 0.195 $ | 3 | 0.043 $ |
| I1+I2-H|BI|completa | no | 44 | 176 | 0.714 $ | 10 | 0.157 $ |
| I3-H|FC|completa | no | 22 | 88 | 0.496 $ | 31 | 0.688 $ |
| I3-N|FC|completa | no | 23 | 92 | 0.518 $ | — | — $ |

Escalas que entran: ≈ 0.00 $ (0.00 $ con margen del 25 %). Saldo de OpenRouter ≈ 1.2–1.5 $.

Respuestas no válidas: 26.
- gemma4 · FC|F3P07|BA|1 · INVALIDA · «Ninguna.»
- gemma4 · FC|F3P07|BA|0 · INVALIDA · «Ninguna.»
- gemma4 · FC|F3P09|AB|1 · INVALIDA · «Ninguna.»
- gemma4 · FC|F3P09|BA|0 · INVALIDA · «Ninguna.»
- gemma4 · FC|F3P02|BA|0 · INVALIDA · «Ninguna.»
- glm5.3-flash · GR|F1-AN02|BA|1 · INVALIDA · «B: 100 puntos para B, es decir, 0 para A.

**0**»
- mimo-v2.6-flash · GR|F1-HO07|AB|1 · INVALIDA · «The request was rejected because it was considered high risk»
