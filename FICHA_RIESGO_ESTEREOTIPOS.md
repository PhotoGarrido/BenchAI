# Ficha de riesgo: variables sensibles y estereotipos

**Origen**: revisión externa 27-07, hallazgo 24. Las personas sintéticas del proyecto incluyen atributos sensibles que se verbalizan en los prompts; esta ficha los inventaría, documenta sus plantillas y declara las reglas de uso.

## Inventario de variables

| Variable | Dónde se verbaliza | Riesgo | Estado |
|---|---|---|---|
| Big Five (o,c,e,a,n) | `spike/personas.py::texto_persona` | bajo (rasgos, no categorías protegidas) | activa; es la manipulación principal de personas |
| Edad, género | ídem | medio (estereotipos de rol) | activa; se reporta en tabla de sujetos |
| Origen cultural | ídem («local», «latinoamericano/a», «magrebí») | **alto** (estereotipo étnico-cultural) | activa en los diseños históricos; en el panel queda **desactivada por defecto** |
| Nivel socioeconómico, educación | ídem | medio | ídem |
| Ideología, religiosidad, salud, atractivo | plantillas del panel | **alto**; «atractivo» verbaliza valores bajos como descripción física negativa | **desactivadas por defecto en el panel**; «atractivo» no se usa en ningún experimento del modo estudio y queda prohibida salvo hipótesis pre-registrada explícita |

## Reglas (vigentes desde 29-07-2026)

1. **Separación experimental/decorativa**: solo entra en un experimento la variable que una hipótesis pre-registrada manipula o controla; el resto no se verbaliza.
2. **Sensibles OFF por defecto** en el diseñador de escenarios; activarlas es un acto consciente del diseñador.
3. **Las plantillas exactas de verbalización están versionadas** (`personas.py`) y cualquier cambio queda en git: la frase que convierte un número en descripción ES parte del instrumento.
4. **Ninguna conclusión por categoría sensible**: el proyecto no publica afirmaciones del tipo «las personas de origen X conforman más»; los atributos demográficos de los sujetos históricos son constantes de diseño (10 perfiles fijos), no factores muestreados, y no soportan esa inferencia.

## Análisis de sensibilidad

- Existente (exploratorio, declarado en E1): la amabilidad (Big Five) correlaciona con conformar (ρ=+0,60, n=10 personas, orientativo — n minúsculo, sin control demográfico).
- Los diseños confirmatorios (G2, G-final) usan **3 supervisores fijos** cuyos atributos son constantes entre brazos: la demografía no puede confundir los contrastes (misma persona en ambos brazos); puede, como declara el preprint §7, condicionar la generalización.
- **Pendiente (requiere presupuesto)**: réplica del módulo A del G-final con personas demográficamente neutras (sin origen/nse/educación) para medir si los niveles absolutos dependen de la demografía verbalizada. Declarado como trabajo futuro en el preprint; no bloquea las conclusiones actuales porque todos los contrastes son intra-persona.
