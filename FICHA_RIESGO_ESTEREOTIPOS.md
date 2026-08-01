# Ficha de riesgo: variables sensibles y estereotipos

**Origen**: revisión externa 27-07, hallazgo 24. Las personas sintéticas del proyecto incluyen atributos sensibles que se verbalizan en los prompts; esta ficha los inventaría, documenta sus plantillas y declara las reglas de uso.

## Taxonomía única (reauditoría 31-07)

El proyecto usa **UNA sola lista** de variables sensibles, compartida por esta
ficha, el scrub del motor (`spike/personas.py::neutralizar_sensibles`) y su
test (`spike/test_sensibles.py`). Antes había una contradicción (la ficha
agrupaba NSE con educación; el test declaraba educación no sensible); se
resuelve así:

- **SENSIBLES** (se neutralizan en TODAS sus formas —protagonista, agente
  generado, media de población y variante— cuando `variables_sensibles` no es
  `true`): **origen cultural, nivel socioeconómico (NSE), ideología,
  religiosidad, salud, atractivo, idioma**.
- **DE DISEÑO** (constantes del experimento, NUNCA se neutralizan): **edad,
  género, educación**. Son factores del diseño reportados en la tabla de
  sujetos, no categorías que el motor deba ocultar; su presencia es
  deliberada y trazable en git.

## Inventario de variables

| Variable | Clase | Dónde se verbaliza | Riesgo | Estado |
|---|---|---|---|---|
| Big Five (o,c,e,a,n) | diseño | `spike/personas.py::texto_persona` | bajo (rasgos, no categorías protegidas) | activa; es la manipulación principal de personas |
| Edad, género | diseño | ídem | medio (estereotipos de rol) | activa; se reporta en tabla de sujetos |
| Educación | diseño | ídem («básicos/medios/superiores») | medio | activa; factor de diseño, no se neutraliza (constante entre brazos) |
| Origen cultural | **sensible** | ídem («local», «latinoamericano/a», «magrebí») | **alto** (estereotipo étnico-cultural) | activa en los diseños históricos; **neutralizada por defecto** |
| Nivel socioeconómico (NSE) | **sensible** | ídem, y como media de población | medio-alto | **neutralizada por defecto** en todas sus formas (`nse`, `nse_media`, variante `nseMedia`) |
| Ideología, religiosidad, salud, atractivo, idioma | **sensible** | plantillas del panel | **alto**; «atractivo» verbaliza valores bajos como descripción física negativa | **neutralizadas por defecto**; «atractivo» no se usa en ningún experimento del modo estudio y queda prohibida salvo hipótesis pre-registrada explícita |

**Default seguro (motor)**: `run_spike.cargar_y_validar_escenario` neutraliza
los sensibles salvo `variables_sensibles: true` explícito (un JSON sin el flag
—antiguo u hostil— queda neutro y se avisa). El texto libre (`trasfondo`) es
contenido de diseño controlado por el autor y NO se escanea por semántica
sensible: la garantía G5 se acota a los campos ESTRUCTURADOS (ver `GARANTIAS.md`).

## Reglas (vigentes desde 29-07-2026)

1. **Separación experimental/decorativa**: solo entra en un experimento la variable que una hipótesis pre-registrada manipula o controla; el resto no se verbaliza.
2. **Sensibles OFF por defecto** en el diseñador de escenarios; activarlas es un acto consciente del diseñador.
3. **Las plantillas exactas de verbalización están versionadas** (`personas.py`) y cualquier cambio queda en git: la frase que convierte un número en descripción ES parte del instrumento.
4. **Ninguna conclusión por categoría sensible**: el proyecto no publica afirmaciones del tipo «las personas de origen X conforman más»; los atributos demográficos de los sujetos históricos son constantes de diseño (10 perfiles fijos), no factores muestreados, y no soportan esa inferencia.

## Análisis de sensibilidad

- Existente (exploratorio, declarado en E1): la amabilidad (Big Five) correlaciona con conformar (ρ=+0,60, n=10 personas, orientativo — n minúsculo, sin control demográfico).
- Los diseños confirmatorios (G2, G-final) usan **3 supervisores fijos** cuyos atributos son constantes entre brazos: la demografía no puede confundir los contrastes (misma persona en ambos brazos); puede, como declara el preprint §7, condicionar la generalización.
- **Pendiente (requiere presupuesto)**: réplica del módulo A del G-final con personas demográficamente neutras (sin origen/nse/educación) para medir si los niveles absolutos dependen de la demografía verbalizada. Declarado como trabajo futuro en el preprint; no bloquea las conclusiones actuales porque todos los contrastes son intra-persona.
