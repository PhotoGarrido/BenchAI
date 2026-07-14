# Experimento 1 · Conformidad tipo Asch (isomorfa) — Informe

**Fecha**: 14-07-2026 · **Modelo**: qwen3.6 (NaN) · **Harness**: `experimento_asch.py` (procedimiento controlado estilo Aher et al. 2023, sin Game Master) · **N**: 10 sujetos sintéticos (Big Five variado) × 3 condiciones × 12 rondas = 360 ensayos (70 críticos por condición de presión) · 21 min de ejecución.

## Diseño

Disfraz isomorfo (panel de control de calidad de audio: seis revisores dicen en voz alta qué variante A/B/C es más larga; las mediciones del sujeto son inequívocas, la correcta gana por >1 s). 7 rondas críticas de 12 con mayoría unánime errónea. Condiciones: **control** (responde primero), **mayoría** (5 cómplices erran antes), **aliado** (4 erran, 1 acierta). **Canal privado por bifurcación de contexto**: en cada ronda de presión, una llamada paralela pregunta el juicio sincero; nunca entra en la transcripción pública. Sonda de contaminación al final de cada sesión. Diseño congelado tras el piloto (2 sujetos); este run es confirmatorio.

## Resultados

| Métrica | qwen3.6 | Humanos (Asch) |
|---|---|---|
| Error en control (validez) | **7,5%** (9/120) | <1% |
| Conformidad pública · mayoría unánime | **11,4%** (8/70) | ~33% |
| Conformidad pública · con aliado | **22,9%** (16/70) | ~5-10% |
| Conformidad privada · mayoría | 7,1% | (baja) |
| Conforma al menos una vez (mayoría) | 60% | ~75% |
| Complacencia entre conformes (dice mayoría, piensa correcta) | **87,5%** | mayoritaria |
| Sesiones que reconocen a Asch al sondear | **25/30** | n/a |
| Spearman amabilidad ↔ conformidad (n=10) | +0,60 (orientativo) | positiva (teoría) |

Aliado vs mayoría: z=1,79, **p≈0,073** (dos colas) — dirección consistente con el piloto, significación marginal.

## Lectura honesta

1. **qwen3.6 no reproduce el efecto Asch clásico**: ante una mayoría unánime equivocada, conforma un 11,4% — que además apenas supera su propio error base sin presión (7,5%). El modelo resiste la unanimidad.
2. **El efecto del aliado se INVIERTE respecto a los humanos**: con un disidente que le da la razón, la conformidad *sube* a 22,9% (en humanos se hunde). Interpretación: en humanos la presión de Asch es **normativa** (miedo al grupo; el aliado libera). El patrón del modelo es consistente con influencia **informacional**: la unanimidad huele a manipulación/guion (que reconoce: 25/30 sesiones nombran a Asch) y la resiste; el desacuerdo entre cómplices hace la escena verosímil — parece ruido de medición real — y entonces agrega opiniones "racionalmente" (4 aparatos contra 2) hasta contradecir su propia medición. Psicología de máquina genuina, opuesta a la humana.
3. **Cuando cede en público, casi nunca cambia de opinión en privado** (87,5% complacencia): el instrumento de dos canales separa limpiamente complacencia de internalización — la distinción clásica de la psicología social, medida aquí con una bifurcación de contexto.
4. **La personalidad importa en la dirección esperada**: las personas más amables conforman más (ρ=+0,60), aunque con n=10 es solo orientativo.

## Limitaciones (importantes)

- **Validez de tarea**: el 7,5% de error base incumple el estándar de Asch (<1%); parte de la "conformidad" con mayoría puede ser error disfrazado. El resultado del aliado (3× el error base) sobrevive a esta objeción; el de mayoría, apenas.
- **Contaminación en techo**: el modelo reconoce el paradigma en el 83% de las sesiones. Para paradigmas famosos, lo que se mide es siempre "un modelo que conoce el experimento". El disfraz superficial no basta; solo cambia si la *estructura* se altera.
- Un solo modelo, una temperatura (0,7), 10 personas, historial de respuestas visible entre rondas (posible arrastre). p=0,073 pide más semillas.

## Qué sigue

1. Repetir con **gemma4 y mimo-v2.5** (¿la inversión del aliado es de qwen o general?).
2. Más sujetos/semillas para llevar el contraste aliado-mayoría a potencia adecuada.
3. Variante sin historial entre rondas (aislar arrastre) y variante con temperatura 0 (aislar ruido).
4. Bajar el error base: estímulos con diferencia mayor (>2 s) para acercarse al estándar de validez.
