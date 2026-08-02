# 🔬 PsicoBench: análisis crítico y camino a la publicación

Autocrítica del benchmark v0.1 con ojos de revisor hostil (02-08-2026). Veredicto corto: **el andamiaje de trazabilidad es publicable hoy; las cifras aún no lo son como benchmark**. Tres cosas lo bloquean: no reportamos incertidumbre, no hemos medido la fiabilidad del instrumento (test-retest) y el ISS mezcla ejes con n que difieren en un orden de magnitud. Todo es corregible; la mayor parte, con coste 0 o casi.

---

## 1 · Debilidades del instrumento actual

### BLOQUEANTES para publicar cifras

**D1 · Sin incertidumbre: el benchmark publica puntos donde hay nubes.**
Los n reales por eje (verificados en crudos, batch 0731): Obediencia **n=10 sesiones** (0,90 = 9/10; Wilson 95% ≈ [0,60, 0,98]); Conformidad n=70 ensayos críticos; ejes de prisión n≈160 registros/variante. Consecuencias directas:
- La diferencia estrella de M4 «obediencia 0,80→0,90» es **8/10 vs 9/10: indistinguible**. Tal cual está, no se puede publicar como cambio.
- Posiciones 8-11 de la clasificación (ISS 27,7–29,8) son empates estadísticos presentados como orden.
- *Remedio (coste 0)*: IC bootstrap por eje e ISS (semilla fija, desde crudos), `n` por celda en `psicobench.json`, barras de error en el panel, y regla editorial: dos entradas cuyos IC de ISS se solapan comparten puesto.

**D2 · Fiabilidad no medida: no sabemos cuánto mide el metro.**
Nunca hemos corrido la batería dos veces sobre el MISMO snapshot. Sin varianza test-retest no podemos afirmar que la «redistribución del perfil» de M4 supere el ruido de muestreo + temperatura (los harness muestrean a T>0). Es la amenaza nº1 a la línea «la versión cambia la conducta».
- *Remedio (coste ≈0 en NaN)*: 3 réplicas completas de la batería sobre 0731 (tarifa plana, ~8 h máquina) → SD por eje e ICC. Criterio pre-declarado: un Δ entre snapshots solo se publica si supera 2×SD test-retest de ese eje.

**D3 · El ISS está desequilibrado por construcción.**
4 de los 6 ejes salen del mismo paradigma (prisión P1/P1b/P2/P2b): el índice pondera 4× la prisión, 1× Asch y 1× Milgram, y mezcla n=10 con n=160. Además la crónica se mide y no puntúa.
- *Remedio (coste 0, decisión de diseño para v0.2)*: (a) calcular la matriz de correlaciones entre ejes sobre las 16 entradas y publicarla; (b) ISS jerárquico: media de paradigmas, no de ejes — `ISS = media(Asch, Milgram, media(P1,P1b,P2,P2b), Crónica?)`; (c) sustituir el eje binario de obediencia por `ruptura_media/10` (usa los 10 niveles de la escalera: mucha más información con el mismo n). Cambio de instrumento ⇒ sube la versión del benchmark, con tabla puente v0.1→v0.2.

**D4 · M4 confunde gateway con snapshot.**
El comparador de la réplica generacional se midió vía OpenRouter (23-07) y el 0731 vía NaN. La réplica cruzada OR≈NaN respalda que el gateway no distorsiona, pero se hizo con otro par. El Δ publicado lleva el confundido dentro.
- *Remedio (~10 $)*: batería del 0731 vía OpenRouter cuando esté disponible (o del v4-flash actual de OR vía NaN) → separa los dos factores. Riesgo conocido: OR puede actualizar silenciosamente su v4-flash al 0731 — comprobar `model_returned` en manifests antes de gastar. Mientras: M4 se publica con la limitación declarada.

### ALTAS (no bloquean, condicionan el alcance)

**D5 · Un solo disfraz por paradigma.** La lección de G2 (−0,69 en el texto-pico vs −0,2/−0,3 al generalizar) dice que la varianza entre-textos es grande. Cada eje descansa en UNA operacionalización; el perfil podría ser en parte «perfil ante este guion».
- *Remedio (~5-10 $)*: segunda variante isomorfa del paradigma más barato (Milgram, dominio distinto) sobre 4 modelos → varianza entre-disfraz publicada como parte del error del instrumento.

**D6 · Un solo idioma.** Todo en español. Los perfiles pueden no viajar a otras lenguas.
- *Remedio (~3-5 $)*: Milgram en inglés sobre 3-4 modelos → o «el perfil viaja» o limitación cuantificada.

**D7 · Contaminación medida pero no integrada.** Tenemos sondas de reconocimiento por sesión (0731: 10/10 nombran a Milgram) y no aparecen en el benchmark.
- *Remedio (coste 0)*: columna `reconocimiento` por entrada + correlación reconocimiento↔ejes en el panel. Es covariable, no excusa: se publica al lado del dato.

**D8 · La objeción explícita no puntúa.** Un 0% de abuso por REHUSA («me niego») y un 0% por ejecución tibia son conductas distintas (caso haiku, 24-07). El benchmark las funde.
- *Remedio (coste 0)*: `tasa_objecion` (proporción REHUSA) como métrica propia desde crudos — separa «resistente que objeta» de «resistente que esquiva».

**D9 · Publicar el benchmark lo desgasta.** En cuanto los disfraces sean públicos, entran en corpus de entrenamiento: el benchmark se contamina a sí mismo (benchmark rot).
- *Remedio (coste 0 ahora)*: (a) string canario tipo BIG-bench en todos los ficheros de harness y datos publicados (detectable en corpus); (b) política declarada de rotación de disfraces por versión; (c) variante hold-out no publicada de cada paradigma, reservada para arbitrar sospechas de memorización.

### MEDIAS (ingeniería y honestidad de ficha)

- **D10 · Extensibilidad hardcodeada**: `FUENTES` vive en el código; añadir una medición exige tocar `generar_benchmark.py`. → `benchmark/fuentes.json` (lista de matrices + proveedor) y guía «añade tu modelo» (bateria → analisis --dir → fuentes.json → --check).
- **D11 · Metadatos incompletos por entrada**: faltan `n` por eje, temperatura/top_p, `parser_version`, commit del harness. Todo existe en manifests/crudos; hay que aflorarlo a `psicobench.json`.
- **D12 · Disonancia solo de Milgram**: la prisión también tiene canal privado y no se reporta. → `disonancia_prision` secundaria.
- **D13 · Sin anclas humanas en el panel**: bandas de referencia (Asch ~33%, Milgram ~65% al máximo) con el caveat de Ashokkumar harían legible el «¿actúan como humanos?» de un vistazo.
- **D14 · `complacencia≈1,0` universal**: no discrimina (es la firma de especie). Mantener como constante declarada, no como columna que parece métrica.

---

## 2 · Aspectos NO medidos (huecos del constructo)

El hexágono actual es **presión social pura sobre terceros**. Faltan, por valor práctico decreciente y con su experimento:

| # | Dimensión | Pregunta | Diseño (isomorfo, disfrazado) | Coste est. |
|---|---|---|---|---|
| N1 | **Venalidad** | ¿Se corrompe por interés propio, sin presión social? | Reparto/auditoría donde favorecer al que ofrece contrapartida beneficia al agente; gradiente de soborno | piloto NaN 0 $ · cartera ~12-15 $ |
| N2 | **Denuncia (whistleblowing)** | ¿Escala una irregularidad de su autoridad pudiendo callar? | Canal de denuncia disponible con coste social; medir uso y umbral | ídem |
| N3 | **Sicofancia al usuario** | ¿Cede ante el USUARIO como cede ante la mayoría? (el eje más relevante para despliegue real) | Asch invertido: el interlocutor directo sostiene el error, sin mayoría | ídem |
| N4 | **Vigilancia/observabilidad** | ¿Cambia la conducta si cree que lo auditan? (eval-awareness conductual) | Mismas celdas P2b ± aviso de registro/auditoría | ~8 $ (reusa harness) |
| N5 | **Favoritismo de grupo mínimo** (Tajfel) | ¿Basta una etiqueta arbitraria para sesgar el reparto? | Ya diseñado en el catálogo E3+ | ~10 $ |
| N6 | **Manipulación secuencial** | ¿Funcionan pie-en-la-puerta / portazo? | Petición pequeña→grande vs directa | ~8 $ |
| N7 | **Engaño estratégico** | ¿Miente a un tercero si el objetivo lo premia? | Negociación con información asimétrica | ~12 $ |

Regla de admisión (ya doctrina): ningún eje nuevo entra sin pre-registro, linter de contraste, barrido con modelo falso y piloto en NaN a coste 0.

---

## 3 · Plan por fases

**P0 · Rigor con datos existentes — 0 $, ~1 día** *(desbloquea D1, D3a, D7, D8, D10, D11, D12, D14, D9a)*
1. IC bootstrap por eje e ISS + `n` por celda + metadatos (temp, parser_version, commit) en `psicobench.json`; barras de error y empates por solapamiento en el panel.
2. Matriz de correlaciones entre ejes (16 entradas) publicada → decisión razonada del ISS v0.2 (jerárquico + ruptura/10), pre-declarada antes de recalcular.
3. `tasa_objecion`, `reconocimiento` y `disonancia_prision` desde crudos.
4. `fuentes.json` + guía «añade tu modelo»; canary string en harness y datos.
5. Métrica formal de distancia entre perfiles `d(A,B)` (media |Δ| por eje, con IC) — la que usarán réplicas y snapshots.

**P1 · Fiabilidad del metro — ~0-15 $, decide qué es publicable** *(D2, D4, D5, D6)*
1. **Test-retest**: 3 réplicas de batería sobre 0731 vía NaN → SD/ICC por eje. Criterio: Δ publicable ⇔ Δ > 2×SD. Re-evaluar M4 con esta vara y actualizar POSICIONES.md (la redistribución sube a establecido o baja a sugerencia).
2. Réplica cruzada del 0731 (OR↔NaN) verificando `model_returned` → cierra D4: ~10 $.
3. Segunda variante de Milgram (4 modelos) → varianza entre-disfraz: ~5 $.
4. Milgram en inglés (3 modelos) → portabilidad de idioma: ~3 $.

**P2 · Ensanchar el constructo — 15-30 $** *(§2)*
Piloto N1-N3 en los 4 NaN (0 $) → los 2 ejes más discriminantes a la cartera OR (~25 $). El hexágono pasa a octógono en v0.2 con tabla puente.

**P3 · Publicación**
1. Recalcular todo como v0.2 (ISS jerárquico + IC + fiabilidad); congelar con release manifest + linaje.
2. Nota/preprint propio del benchmark («perfil conductual social de LLM: instrumento, fiabilidad y 16+ mediciones») — distinto del preprint de hallazgos; PsyArXiv/arXiv cs.CY + panel público (GitHub Pages desde `benchmark/`).
3. Puerta de salida (GO/NO-GO pre-declarado): IC en toda cifra publicada · test-retest reportado · ISS v0.2 justificado con la matriz de correlaciones · M4 re-evaluado contra la vara de fiabilidad · canary + política de rotación publicadas · revisión externa humana (SETUP_PSICOAI.txt) en verde · `--check` de linaje y adjudicación 0 pendientes en CI.

---

## 4 · Lo que ya está bien (y hay que conservar)

Unidad = medición (no nombre) · «no es ranking de calidad» declarado · missingness como dato · linaje sha256 verificado en CI · tabla autogenerada (imposible desfase texto-datos) · refutaciones publicadas · crudos + manifests por solicitud · adjudicación firmada. Ningún benchmark conductual publicado que conozcamos trae esta cadena de trazabilidad completa: **es nuestra ventaja diferencial — el punto de venta es «el benchmark auditable», no «el leaderboard»**.
