# ⚖️ Posiciones — qué puede sostener la evidencia de PsicoAI

Documento vivo. Cada hallazgo del proyecto vive en **una** de cuatro categorías según su fuerza epistémica, con puntero a la evidencia y con la condición explícita que lo movería de sitio. Reglas del fichero:

1. **Los desacuerdos no se promedian ni se ocultan**: una dirección incompatible entre modelos o diseños es una posición propia, no ruido.
2. **Nada sube de categoría sin réplica** (otro diseño, otra cartera u otro banco) o sin test pre-registrado; el entusiasmo del informe de turno no puntúa.
3. **Toda posición declara qué la movería** — si no sabemos qué evidencia la cambiaría, no es una posición científica.
4. Las refutaciones se conservan aquí para siempre: son producto, no vergüenza.

Última revisión: 02-08-2026 · fuentes canónicas: [`EXPERIMENTOS.md`](EXPERIMENTOS.md), [`BENCHMARK.md`](BENCHMARK.md), [`preprint/preprint.md`](preprint/preprint.md).

---

## 1 · Establecido

*Patrones con réplica entre diseños/carteras y sin contraejemplo vigente.*

| Posición | Evidencia | Lo movería |
|---|---|---|
| **Complacencia sin internalización**: cuando un modelo cede en público, casi siempre conserva en privado el juicio correcto. La firma de especie del proyecto. | E1 (3 modelos, 1.080 ensayos, 87,5–100%) + M2 (16/16, complacencia ≈1,0) | Un modelo que internalice de verdad (conformidad privada ≈ pública) en ≥2 paradigmas |
| **La susceptibilidad social es rasgo del modelo, no de los LLM**: obediencia de 0,00 a 1,00 en la misma escalera; conformidad de 0 a 43%. | E2 + M2 (Milgram 0,00–1,00); E1 + M2 (Asch) | Convergencia de perfiles al repetir con protocolos nuevos (indicaría artefacto del banco) |
| **Obediencia jerárquica ⊥ conformidad de pares**: los dos ejes sociales disocian por modelo. | E1×E2 (gemma inmune al grupo y máximo obediente; qwen al revés) + M2 | Correlación alta y estable entre ambos ejes en la cartera ampliada |
| **Dos motores de crueldad independientes**: el conflicto (motín) y la orden explícita disparan a modelos distintos; el poder a secas casi nunca. | Trilogía P1→P2b, 16 modelos; mapa de cuadrantes | Que P2 y P2b converjan en carteras nuevas; o que P1>0 se vuelva la norma |
| **El perfil social es propiedad de la versión, no del nombre**: escalera Anthropic con 5 peldaños = 5 perfiles; réplica de snapshot 0731 redistribuye el perfil; el gateway no lo distorsiona (OR ≈ NaN). | M3 + M4 + réplica cruzada M2 | Dos snapshots consecutivos de ≥2 familias con perfil idéntico por ejes |
| **Recordar la opción de negarse reduce la ejecución.** | G2 + G-final (todos los modelos y dominios probados) | Un modelo/dominio donde la negativa explícita no reduzca (o aumente) |
| **Validez direccional del instrumento**: sin autoridad casi nadie sanciona; los controles se comportan. | E2 (control 1,6–2,5), M2, precisión de control Asch 0,99–1,0 | Controles sucios en re-ejecuciones (invalidaría celdas, no la doctrina) |
| **Fiabilidad del instrumento**: todos los ejes discriminan entre modelos por encima de su ruido test-retest (ratios 2,1–15,3; 4 baterías del mismo snapshot). Las medidas granulares (ruptura/10, SD 0,013) superan a las binarias. | M5 (informe_retest_0731.md) | Ratios <2 al repetir el retest en otro modelo/proveedor → degradaría ejes concretos |
| **El portador de la orden disocia la obediencia y la política impersonal es el portador más fuerte**: `system` ≥ coordinador presente > memo ≈ relevo de par, replicado en 5/5 modelos y 2 proveedores (M7 piloto + M8 cartera); donde hay margen, la política lleva al techo con ~0 empujones; el portador modula el cumplimiento sin mover el juicio privado (disonancia 0,66–1,0) ni crear obediencia donde no la hay (haiku en suelo con los 4) | M7 + M8 (informe_eportador_cartera.md) | Un modelo con `par` > coordinador o `system` muy por debajo de la persona rompería la escalera; un segundo disfraz para portadores acotaría la generalidad |

## 2 · Señal condicionada

*Efectos reales pero dependientes de modelo, texto, cartera o n; se citan siempre con su condición.*

| Posición | Condición conocida | Evidencia | Lo movería |
|---|---|---|---|
| **La cláusula de proporcionalidad mitiga el abuso** (−0,2/−0,3) | Significativa en 3/4 modelos (deepseek direccional n.s.); magnitud menor que el texto-pico de G2 (−0,69) | G-final H1, pre-registrado, IC bootstrap | A confirmar en deepseek con n mayor → subiría; un dominio donde no reduzca → condición nueva |
| **La vacuna de contaminación cambia la obediencia** | La **dirección depende del modelo**: protege a deepseek (las 4 mediciones del 0731: −0,3 a −0,6; magnitud variable, SD 0,13) y sol (−0,3); empeora a qwen y gemma (E3) | E3 + M2 + M4 + M5 | Mecanismo que prediga la dirección por modelo → establecería la versión condicionada |
| **El aliado disidente libera** (dirección humana) | Mayoritaria en la cartera (Δ negativos); invertida en qwen-M1 (p≈0,073) | E1 + matriz M2 (Δ aliado) | Réplica de la inversión de qwen con semillas → pasaría a desacuerdo real documentado |
| **El poder a secas sí corrompe a algunos** (null de P1 roto) | 4/16 modelos (gemini 18%, glm 17%, fable 10%, kimi 7%); contingente a versión | M2; contradice el null de julio (4 modelos NaN) | Estabilidad del subconjunto entre snapshots → establecido para esos modelos |
| **La norma erosiona o resiste según la cartera**: 10/12 OR derogan; 0/16 mundos NaN la derogaban | Sensible a cartera y configuración | C1/C1-v2 vs M2 | Aislar qué variable (modelo vs config) explica la inversión |
| **El agregado engaña en las réplicas de snapshot**: ISS casi idéntico con composición redistribuida (v0.1: 44,7–46,0; **sigue valiendo bajo el v0.2 jerárquico: 49,8–52,1 con IC solapados**) — tras cerrar el confundido de gateway (M6), la redistribución queda **confirmada en 5 ejes con el par limpio mismo-gateway** (ruptura +0,11, P2b −0,12, aliado −0,09, P2 −0,08, vacuna que protege siempre) y **2 ejes se reatribuyen al proveedor** (P1b, disonancia) | n=1 par de snapshots (un solo modelo) | M4 + M5 + M6 + E1 | Un segundo par intra-nombre en otro modelo → establecido |
| **El proveedor/gateway desplaza ejes concretos del perfil**: mismo snapshot 0731 por OR y NaN difiere en 4/10 ejes (clúster Milgram en bloque hacia más obediencia; P1b se enciende solo vía NaN), d=8,1 ≈ salto generacional limpio 8,7; conformidad y prisión viajan bien | n=1 par mismo-snapshot (el par qwen de M10 es intra-nombre, no separa variante de serving); upstream de OR sin fijar | M6 + M10 | Un segundo par con snapshot FIJADO → establecido; fijar upstream aislaría el mecanismo |
| **El nombre comercial sin snapshot no identifica al modelo**: qwen3.6 por NaN vs qwen3.6-35b por OR el mismo día → d=22,1 (obediencia 0,00 vs 0,70; la vacuna cambia de signo), mientras el mismo nombre+proveedor a 12 días replica con d=2,5 | un solo nombre; variante de NaN opaca (indistinguible de serving — y esa opacidad es parte del hallazgo) | M10 | Un segundo nombre con proveedor opaco mostrando d grande → establecido |
| *(promovida a establecido el 04-08 tras la cartera M8 — ver §1)* | | M7→M8 | |
| **El eje de obediencia es robusto al disfraz isomorfo** (Δ≤0,9 en 6/7 modelos, dos proveedores) con error entre-disfraz medido ~±1 de ruptura; excepción: gemma4 (−1,1) | n=1 run/celda salvo base deepseek ×4; comparadores de julio para 3 modelos NaN | M7 | Segunda pareja de disfraces o réplica de gemma4 → acotaría si la excepción es estable |
| **El idioma es condición de medida de primera clase**: Δ≤1,1 en 6/7, pero mimo-v2.5 en inglés se transforma (+3,4 de ruptura; su control sube igual — **replicado ×3**: 9,3/9,2/9,2) y las direcciones son mixtas entre modelos | solo es↔en; identidades traducidas (texto_persona_en) | M7 + réplicas 04-08 | Un tercer idioma y un segundo modelo transformado → establecido |
| **El coro dobla; la consulta uno-a-uno no** (sicofancia perceptiva): 10 de 11 mediciones en suelo absoluto — 0,00 en los 7 modelos OR incluidos sol y opus-5 (70/70 insistencias sostenidas por modelo) — mientras los mismos modelos ceden a la mayoría de E1 (0,13–0,43). Trans-gama y trans-proveedor; contra la predicción pre-registrada. Como eje de benchmark NO discrimina (celda medida con resultado nulo, fuera del índice); la sicofancia de *opinión* queda sin medir | sicofancia solo perceptiva (evidencia objetiva propia); n=1 run/celda; única excepción qwen@NaN 0,20 | M9 + M11 | Un modelo que ceda al usuario contra su propia evidencia lo rompería; la variante de opinión es otro constructo (v0.3) |
| **La denuncia discrimina y el coste social del canal es un modulador con dirección por modelo**: silencio 0,03–0,33 en 11 mediciones; el coste sube el silencio en 6 (4 NaN + haiku + deepseek), es neutro en 3 (sol/opus/sonnet) y qwen3.6-35b lo INVIERTE (−0,33: confidencial calla, público denuncia). La disonancia del silencio va de 0,00 a 1,00 — en unos la conducta sigue al coste, en otros al juicio | n=1 run/celda; un solo disfraz; sin IC en piloto/cartera | M9 + M11 | Candidato a séptimo eje del índice en v0.3; un segundo disfraz y IC decidirían establecido |

## 3 · Desacuerdo real y refutaciones

*Direcciones incompatibles o predicciones firmadas que cayeron. Publicadas, no promediadas.*

| Posición retirada/refutada | Qué la mató | Dónde |
|---|---|---|
| «El membrete institucional legitima» (G1) | El efecto era una frase de más en un brazo; controlado: política − orden = −0,21/+0,00 | G2 pre-registrado |
| Interacción negativa×fuente (hallazgo exploratorio de G2) | No replicó en el confirmatorio; se invirtió en los 2 modelos | G2 fase confirmatoria |
| «A opus-5 le basta que exista una política» (institucionalista puro) | política − sin_marco = +0,11 [−0,07,+0,33]; la orden ejecuta al menos tanto | G-final H2 |
| La vacuna como efecto universal | Direcciones opuestas por modelo (protege/empeora) | E3 |
| «Ninguna aceptación privada» | grok obedece **convencido** (disonancia 0,19→0,08 en G2): existe la obediencia sin disonancia | Reproceso + informe trilogía |
| Derogación tardía de qwen (d42, C1) | No robusta al re-test de sensibilidad post-errata | ERRATA_prision.md |
| La medida de interpretación del G-final | κ juez↔humano 0,32 (y 0,55 en G2) < 0,8 pre-registrado; la sonda heredaba la consigna del menú | G-final E4 — el eslabón humano la cazó |

## 4 · Pregunta abierta

*Donde la evidencia todavía no autoriza conclusión. Cada una con su experimento candidato.*

| Pregunta | Por qué importa | Candidato |
|---|---|---|
| ¿Qué mecanismo explica opus-5 − opus-4.8 = +0,37 en el briefing? | Diferencia real entre versiones hermanas, mecanismo sin testar | G3 (orden/política/sin-marco con negativa simétrica) |
| ¿Qué cambia dentro de un snapshot que **redistribuye** el perfil conservando el agregado? | Es LA pregunta de la línea «versión ≠ nombre» | Más pares intra-nombre (M4×N familias) |
| ¿Por qué el Tiento no predice la disonancia? | El screener ordena carteras pero falla el canal privado (3 avisos: mistral, 0731) | Añadir mini-sonda privada al Tiento y validarla contra batería |
| ¿La objeción «en acta» dispara la difusión de responsabilidad? | Mecanismo del efecto rebelde invertido de gemma | E-difusión (acta escrita vs negativa sin registro) |
| ¿«Nadie es engañado» generaliza más allá de G2? | El G-final no pudo medirlo (κ fallida); hoy descansa solo en G2 | Re-run de la sonda de interpretación corregida + κ nueva |
| ¿El perfil del harness predice la conducta en simulación libre? | Es el puente banco→episodios (validez ecológica interna) | Correlacionar matriz M2 con conducta en episodios GM |
| Dimensiones no exploradas del perfil | El hexágono actual es presión social pura | Venalidad (soborno), autoridad máquina vs humana, vigilancia, Tajfel, engaño estratégico, whistleblowing |

---

**Uso**: los informes y el preprint citan posiciones de §1 sin calificar, las de §2 siempre con su condición, y no citan §3 salvo como refutación. Si un texto del proyecto afirma algo que no está aquí, o lo está en otra categoría, eso es un bug de documentación: se corrige el texto o se actualiza este fichero en el mismo commit.
