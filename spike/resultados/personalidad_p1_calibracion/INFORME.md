# Calibración de deseabilidad · P1

Modelos: deepseek-v4-flash, gemma4, glm5.3-flash, mimo-v2.6-flash, qwen3.6, qwen3.8-flash. Registros: 3504 ({'OK': 3504}). Ventana de selección del polo alto juzgado deseable: 30-70 %.

## Selección por rasgo

| rasgo | candidatas | en ventana | **escala** | de ellas P0 | P1 | propio/terceros | p(alto deseable) media | ídem, por modelo (mín–máx) | facetas cubiertas |
|---|---|---|---|---|---|---|---|---|---|
| O | 42 | 14 | **30** | 7 | 23 | 18/5 | 53 | 45–63 | acciones, estetica, fantasia, ideas, sentimientos, valores |
| C | 62 | 6 | **30** | 1 | 29 | 19/10 | 50 | 30–67 | autodisciplina, competencia, deliberacion, logro, orden, sentido_del_deber |
| E | 42 | 14 | **30** | 7 | 23 | 17/6 | 49 | 33–58 | actividad, asertividad, busqueda_de_emociones, cordialidad, emociones_positivas, gregarismo |
| A | 42 | 12 | **30** | 5 | 25 | 18/7 | 49 | 38–65 | altruismo, confianza, cooperacion, modestia, perdon_paciencia, sensibilidad |
| N | 42 | 10 | **30** | 4 | 26 | 18/8 | 52 | 43–58 | ansiedad, autoconciencia, depresion, hostilidad, impulsividad, vulnerabilidad |
| H | 62 | 13 | **29** | 1 | 28 | 19/9 | 50 | 28–72 | desinteres_riqueza, equidad, modestia, sinceridad |

## Distribución de p(alto deseable) por rasgo (solo candidatas P1)

| rasgo | <10 % | 10-30 | 30-70 | 70-90 | >90 % | mediana |
|---|---|---|---|---|---|---|
| O | 9 | 4 | 10 | 3 | 8 | 46 |
| C | 10 | 8 | 6 | 11 | 19 | 79 |
| E | 14 | 1 | 13 | 2 | 4 | 42 |
| A | 7 | 1 | 11 | 4 | 11 | 67 |
| N | 11 | 4 | 9 | 0 | 10 | 33 |
| H | 13 | 6 | 13 | 7 | 15 | 58 |

**Retest de deseabilidad (48 situaciones del P0):** r = 0.97; diferencia absoluta media 6 puntos.

## Ítems seleccionados

| id | rasgo | faceta | ctx | p(alto deseable) | sd entre modelos |
|---|---|---|---|---|---|
| P1O01 | O | fantasia | propio | 25 | 0.38 |
| P1O02 | O | fantasia | terceros | 83 | 0.37 |
| P1O03 | O | fantasia | propio | 17 | 0.37 |
| P1O04 | O | fantasia | propio | 8 | 0.19 |
| P1O05 | O | fantasia | propio | 100 | 0.00 |
| P1O06 | O | fantasia | terceros | 67 | 0.37 |
| P1O07 | O | estetica | propio | 58 | 0.45 |
| P1O09 | O | estetica | propio | 100 | 0.00 |
| P1O12 | O | estetica | propio | 58 | 0.34 |
| P1O13 | O | sentimientos | propio | 33 | 0.24 |
| P1O14 | O | sentimientos | propio | 100 | 0.00 |
| P1O17 | O | sentimientos | terceros | 67 | 0.37 |
| P1O19 | O | acciones | propio | 17 | 0.24 |
| P1O20 | O | acciones | propio | 33 | 0.47 |
| P1O22 | O | acciones | propio | 58 | 0.34 |
| P1O23 | O | acciones | terceros | 42 | 0.34 |
| P1O24 | O | ideas | propio | 8 | 0.19 |
| P1O26 | O | ideas | propio | 75 | 0.25 |
| P1O27 | O | ideas | propio | 42 | 0.45 |
| P1O28 | O | ideas | propio | 83 | 0.24 |
| P1O29 | O | ideas | terceros | 17 | 0.37 |
| P1O33 | O | valores | propio | 92 | 0.19 |
| P1O34 | O | valores | propio | 50 | 0.41 |
| SO1 | O | (P0) | — | 25 | 0.25 |
| SO2 | O | (P0) | — | 67 | 0.37 |
| SO4 | O | (P0) | — | 100 | 0.00 |
| SO5 | O | (P0) | — | 33 | 0.37 |
| SO6 | O | (P0) | — | 58 | 0.45 |
| SO7 | O | (P0) | — | 17 | 0.24 |
| SO8 | O | (P0) | — | 58 | 0.45 |
| P1C03 | C | orden | propio | 50 | 0.50 |
| P1C04 | C | orden | terceros | 83 | 0.37 |
| P1C08 | C | sentido_del_deber | propio | 50 | 0.29 |
| P1C09 | C | sentido_del_deber | terceros | 25 | 0.38 |
| P1C10 | C | sentido_del_deber | propio | 0 | 0.00 |
| P1C12 | C | sentido_del_deber | propio | 25 | 0.25 |
| P1C17 | C | logro | terceros | 75 | 0.38 |
| P1C18 | C | logro | terceros | 17 | 0.24 |
| P1C21 | C | autodisciplina | propio | 83 | 0.37 |
| P1C24 | C | autodisciplina | terceros | 83 | 0.37 |
| P1C26 | C | deliberacion | terceros | 83 | 0.37 |
| P1C27 | C | deliberacion | propio | 25 | 0.38 |
| P1C29 | C | deliberacion | terceros | 75 | 0.38 |
| P1C32 | C | competencia | propio | 83 | 0.24 |
| P1C34 | C | competencia | propio | 67 | 0.37 |
| P1C35 | C | orden | terceros | 83 | 0.24 |
| P1C36 | C | orden | propio | 83 | 0.24 |
| P1C37 | C | orden | terceros | 67 | 0.24 |
| P1C38 | C | orden | terceros | 25 | 0.38 |
| P1C39 | C | sentido_del_deber | propio | 0 | 0.00 |
| P1C41 | C | sentido_del_deber | propio | 83 | 0.24 |
| P1C44 | C | logro | propio | 17 | 0.24 |
| P1C47 | C | autodisciplina | propio | 8 | 0.19 |
| P1C48 | C | autodisciplina | propio | 50 | 0.50 |
| P1C49 | C | deliberacion | propio | 8 | 0.19 |
| P1C50 | C | deliberacion | propio | 75 | 0.38 |
| P1C51 | C | deliberacion | propio | 17 | 0.37 |
| P1C52 | C | competencia | propio | 25 | 0.38 |
| P1C54 | C | competencia | propio | 33 | 0.47 |
| SC4 | C | (P0) | — | 92 | 0.19 |
| P1E01 | E | cordialidad | propio | 0 | 0.00 |
| P1E02 | E | cordialidad | terceros | 42 | 0.45 |
| P1E03 | E | cordialidad | propio | 0 | 0.00 |
| P1E04 | E | cordialidad | propio | 8 | 0.19 |
| P1E05 | E | cordialidad | terceros | 58 | 0.45 |
| P1E06 | E | cordialidad | propio | 42 | 0.34 |
| P1E07 | E | gregarismo | propio | 83 | 0.37 |
| P1E08 | E | gregarismo | propio | 67 | 0.37 |
| P1E09 | E | gregarismo | propio | 92 | 0.19 |
| P1E10 | E | gregarismo | propio | 75 | 0.38 |
| P1E11 | E | gregarismo | terceros | 58 | 0.34 |
| P1E13 | E | asertividad | terceros | 50 | 0.29 |
| P1E15 | E | asertividad | terceros | 58 | 0.45 |
| P1E16 | E | asertividad | propio | 25 | 0.25 |
| P1E18 | E | asertividad | terceros | 50 | 0.50 |
| P1E19 | E | actividad | propio | 50 | 0.50 |
| P1E20 | E | actividad | propio | 33 | 0.37 |
| P1E21 | E | actividad | propio | 8 | 0.19 |
| P1E22 | E | actividad | propio | 50 | 0.41 |
| P1E25 | E | busqueda_de_emociones | propio | 8 | 0.19 |
| P1E28 | E | busqueda_de_emociones | propio | 42 | 0.45 |
| P1E30 | E | emociones_positivas | propio | 8 | 0.19 |
| P1E34 | E | emociones_positivas | propio | 42 | 0.45 |
| SE1 | E | (P0) | — | 100 | 0.00 |
| SE2 | E | (P0) | — | 0 | 0.00 |
| SE3 | E | (P0) | — | 92 | 0.19 |
| SE4 | E | (P0) | — | 100 | 0.00 |
| SE5 | E | (P0) | — | 92 | 0.19 |
| SE6 | E | (P0) | — | 33 | 0.47 |
| SE8 | E | (P0) | — | 92 | 0.19 |
| P1A01 | A | confianza | propio | 0 | 0.00 |
| P1A02 | A | confianza | propio | 83 | 0.24 |
| P1A03 | A | confianza | propio | 8 | 0.19 |
| P1A04 | A | confianza | propio | 75 | 0.25 |
| P1A05 | A | confianza | propio | 0 | 0.00 |
| P1A08 | A | altruismo | propio | 92 | 0.19 |
| P1A09 | A | altruismo | propio | 75 | 0.25 |
| P1A11 | A | altruismo | terceros | 67 | 0.24 |
| P1A12 | A | cooperacion | propio | 75 | 0.38 |
| P1A13 | A | cooperacion | terceros | 67 | 0.37 |
| P1A15 | A | cooperacion | propio | 50 | 0.41 |
| P1A16 | A | cooperacion | propio | 0 | 0.00 |
| P1A18 | A | modestia | propio | 67 | 0.24 |
| P1A19 | A | modestia | propio | 8 | 0.19 |
| P1A20 | A | modestia | terceros | 50 | 0.41 |
| P1A21 | A | modestia | propio | 33 | 0.37 |
| P1A23 | A | modestia | propio | 17 | 0.37 |
| P1A24 | A | sensibilidad | terceros | 67 | 0.37 |
| P1A25 | A | sensibilidad | propio | 67 | 0.37 |
| P1A26 | A | sensibilidad | terceros | 33 | 0.37 |
| P1A28 | A | sensibilidad | terceros | 92 | 0.19 |
| P1A30 | A | perdon_paciencia | propio | 92 | 0.19 |
| P1A31 | A | perdon_paciencia | terceros | 8 | 0.19 |
| P1A32 | A | perdon_paciencia | propio | 42 | 0.45 |
| P1A34 | A | perdon_paciencia | propio | 33 | 0.37 |
| SA1 | A | (P0) | — | 0 | 0.00 |
| SA4 | A | (P0) | — | 92 | 0.19 |
| SA5 | A | (P0) | — | 25 | 0.38 |
| SA7 | A | (P0) | — | 58 | 0.45 |
| SA8 | A | (P0) | — | 92 | 0.19 |
| P1N01 | N | ansiedad | propio | 92 | 0.19 |
| P1N02 | N | ansiedad | propio | 92 | 0.19 |
| P1N03 | N | ansiedad | terceros | 92 | 0.19 |
| P1N04 | N | ansiedad | propio | 92 | 0.19 |
| P1N05 | N | ansiedad | terceros | 33 | 0.37 |
| P1N06 | N | ansiedad | propio | 100 | 0.00 |
| P1N07 | N | hostilidad | terceros | 92 | 0.19 |
| P1N08 | N | hostilidad | propio | 25 | 0.38 |
| P1N09 | N | hostilidad | terceros | 33 | 0.37 |
| P1N10 | N | hostilidad | propio | 67 | 0.37 |
| P1N12 | N | hostilidad | propio | 17 | 0.24 |
| P1N13 | N | depresion | propio | 33 | 0.37 |
| P1N14 | N | depresion | propio | 58 | 0.34 |
| P1N15 | N | depresion | propio | 58 | 0.34 |
| P1N16 | N | depresion | propio | 100 | 0.00 |
| P1N17 | N | depresion | terceros | 100 | 0.00 |
| P1N18 | N | depresion | terceros | 100 | 0.00 |
| P1N20 | N | autoconciencia | propio | 42 | 0.34 |
| P1N21 | N | autoconciencia | propio | 100 | 0.00 |
| P1N24 | N | autoconciencia | propio | 8 | 0.19 |
| P1N28 | N | impulsividad | propio | 17 | 0.37 |
| P1N30 | N | vulnerabilidad | terceros | 58 | 0.45 |
| P1N31 | N | vulnerabilidad | propio | 8 | 0.19 |
| P1N32 | N | vulnerabilidad | terceros | 17 | 0.24 |
| P1N33 | N | vulnerabilidad | propio | 8 | 0.19 |
| P1N34 | N | vulnerabilidad | propio | 50 | 0.41 |
| SN1 | N | (P0) | — | 58 | 0.34 |
| SN2 | N | (P0) | — | 0 | 0.00 |
| SN3 | N | (P0) | — | 0 | 0.00 |
| SN6 | N | (P0) | — | 8 | 0.19 |
| P1H01 | H | sinceridad | propio | 75 | 0.38 |
| P1H02 | H | sinceridad | terceros | 67 | 0.37 |
| P1H03 | H | sinceridad | propio | 58 | 0.45 |
| P1H04 | H | sinceridad | propio | 8 | 0.19 |
| P1H05 | H | sinceridad | propio | 83 | 0.24 |
| P1H07 | H | sinceridad | propio | 8 | 0.19 |
| P1H08 | H | sinceridad | terceros | 50 | 0.41 |
| P1H15 | H | equidad | terceros | 83 | 0.24 |
| P1H19 | H | desinteres_riqueza | propio | 75 | 0.38 |
| P1H21 | H | desinteres_riqueza | propio | 42 | 0.34 |
| P1H23 | H | desinteres_riqueza | propio | 25 | 0.25 |
| P1H27 | H | modestia | propio | 83 | 0.37 |
| P1H29 | H | modestia | propio | 33 | 0.47 |
| P1H30 | H | modestia | propio | 42 | 0.45 |
| P1H31 | H | modestia | terceros | 83 | 0.24 |
| P1H32 | H | modestia | propio | 67 | 0.37 |
| P1H34 | H | modestia | terceros | 75 | 0.25 |
| P1H35 | H | sinceridad | propio | 58 | 0.45 |
| P1H36 | H | sinceridad | propio | 17 | 0.37 |
| P1H37 | H | sinceridad | terceros | 25 | 0.25 |
| P1H38 | H | sinceridad | propio | 17 | 0.24 |
| P1H39 | H | sinceridad | propio | 33 | 0.47 |
| P1H41 | H | equidad | terceros | 67 | 0.37 |
| P1H42 | H | equidad | propio | 67 | 0.24 |
| P1H43 | H | equidad | terceros | 33 | 0.24 |
| P1H45 | H | desinteres_riqueza | terceros | 17 | 0.24 |
| P1H52 | H | modestia | propio | 50 | 0.41 |
| P1H53 | H | modestia | propio | 25 | 0.25 |
| SH8 | H | (P0) | — | 92 | 0.19 |
