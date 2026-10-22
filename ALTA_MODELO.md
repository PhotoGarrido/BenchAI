# Alta de un modelo en PsicoBench

El procedimiento completo para añadir mediciones al banco: qué se decide,
qué se ejecuta, qué cuesta y qué tiene que quedar en verde antes de
publicar. La doctrina (criterios de inclusión, D-8b, identidad de las
entradas, canary) vive en [BENCHMARK.md](BENCHMARK.md); esto es el manual
de operación. Un alta con el instrumento vigente **no exige pre-declaración
nueva**: «añadir mediciones no cambia la versión» — pre-registro solo si se
toca la suite, un parser o la definición de un eje (METODO.md §A).

## 0 · Qué entra (decisión del dueño, no del guion)

Criterio de cartera practicado hasta hoy — pendiente de fijarse como
política estable:

- **Frontier vigente de cada laboratorio** (la punta real, no la variante
  barata), más el top de pesos abiertos, más réplicas cruzadas del mismo
  modelo por proveedor o fecha cuando la pregunta sea el *drift*.
- **Versión nueva de un modelo ya medido = entrada nueva, jamás sustituye**
  (se miden versiones, no nombres; ids `@proveedor·fecha` automáticos).
- Screening opcional antes de gastar la batería: **El Tiento**
  (`python tiento.py --modelos <id>`, ~98 llamadas, ~0,10 $/modelo), con
  sus reglas pre-registradas de descarte (validez < 90 %, redundancia
  intra-familia) en [spike/TIENTO.md](spike/TIENTO.md).
- Re-medición por drift: sin disparador fijado aún; el precedente es M10
  (réplica temporal, d=2,5 a 12 días). Cuando se fije, vivirá aquí.

## 1 · Preparar

1. `spike/.env`: la clave del proveedor (`OPENROUTER_API_KEY` para ids con
   `/`, `NAN_API_KEY` para ids planos) y, si procede, `PSICOAI_MAX_CALLS`.
2. Precio del modelo en `PRECIOS` de [spike/coste_run.py](spike/coste_run.py)
   (USD/M tokens, con fecha en el comentario) — sin él, la proyección y la
   auditoría de coste salen «SIN PRECIO».
3. Laboratorio en `LABS` de
   [spike/generar_benchmark.py](spike/generar_benchmark.py) si el prefijo es
   nuevo — sin él, la tabla publica «?». Los ids con `/` resuelven por su
   org (`z-ai/…`); los planos de NaN, por prefijo del nombre (`glm5.3-flash`
   → `glm`), así que un modelo nuevo de NaN puede necesitar su prefijo
   aunque el laboratorio ya esté. `alta.py` avisa de ambos olvidos.
4. NaN es tarifa plana: el pin de `PRECIOS` es `(0.0, 0.0)` con la fecha, y
   la restricción real son los límites por clave: 60 req/min (limitador a
   50 en `model_factory`) y **5 peticiones en vuelo**, compartidas con
   cualquier otro uso de la misma clave (grifo a 2, y ante ese 429 se
   espera con backoff dentro del grifo). Con varios modelos NaN en un
   batch, corre con `BATERIA_MAX_MODELOS=1`: los sub-procesos no comparten
   ni el limitador ni el grifo.
5. **Pools lentos o en cola** (un stealth recién publicado): el harness
   corta cada llamada a los 60 s que trae Concordia y `RetryLanguageModel`
   repite cuatro veces contra la misma cola. `PSICOAI_TIMEOUT_S` fija el
   timeout por llamada de la tanda entera (sondeo incluido) y
   `BATERIA_TIMEOUT_S` el tope por sub-experimento (90 min por defecto;
   0 = sin límite). Union Alpha (16-09-2026) daba 27-229 s por llamada y
   ~1 llamada/min efectiva: se lanzó con `PSICOAI_TIMEOUT_S=600
   BATERIA_TIMEOUT_S=86400`. Un 429 de OpenRouter espera con backoff dentro
   del grifo, igual que los de NaN. Sondear la latencia con llamadas
   neutras ANTES de lanzar: a 1/min la suite son ~75 h, y la ventana de un
   stealth es de una semana.
6. **Stealth aún sin desvelar**: `LABS` lo etiqueta «sin desvelar» y la web
   NO lo cuenta como laboratorio (`portada.sinDesvelar` lo lleva aparte):
   la prosa dice «N mediciones, L laboratorios» con L los que tienen nombre.
   Al desvelarse, entra en `DESVELADOS` y, si el lab es nuevo, cuenta.

## 2 · Plan y autorización de gasto

```bash
cd spike && python alta.py --modelos <id1>,<id2>
```

Imprime el plan — suite íntegra v0.4 (batería M2 + N2 denuncia + N3b
sicofancia de opinión), ~4.500 llamadas y ~3-4 h de máquina por modelo —
con la proyección de coste y **se detiene**. La regla presupuestaria de la
casa (SETUP_PSICOAI): ninguna llamada de pago sin autorización explícita
del dueño. Referencias reales (cartera de agosto 2026):

| Modelo | Coste de la suite completa |
|---|---|
| deepseek-v4-flash, gemini-flash-lite | < 1 $ |
| sonnet-5, glm-5.2, v3.2 | ~2-8 $ |
| opus-5, kimi-k3, grok-4.5 (verbosos: out ×3) | ~15-30 $ |
| **Mediana empírica de la cartera** | **~10 $/modelo** |

## 3 · Ejecutar

```bash
python alta.py --modelos <id1>,<id2> --autorizado
```

Antes de gastar una sola llamada de medición hace un **sondeo**: una
petición mínima por modelo. Si alguno no responde —id mal escrito, modelo
retirado, o una atestación pendiente en tu cuenta (Muse Spark 1.2 exige
confirmación de edad en `openrouter.ai/settings/preferences`)— aborta ahí,
en dos segundos, en vez de a mitad de tanda.

Una sola orden: lanza `bateria.py` (los 13 sub-experimentos del octógono,
con reanudación por `progreso.jsonl`, timeout por sub-experimento y exit ≠ 0
si algo falla), y al terminar hace el cableado que antes eran cuatro ediciones
a mano — mapas `denuncia_runs.json` y `sicofancia_runs.json`, matriz vía
`analisis_bateria.py`, fuente en `fuentes_benchmark.json` — y regenera
benchmark y web. Piezas sueltas si algo se torció:

- Batch a medio correr: `python alta.py --modelos … --autorizado --reanudar resultados/bateria_X`
- Solo el cableado de un batch ya corrido: `python alta.py --modelos … --registrar resultados/bateria_X`
- **`alta.py` jamás pisa una clave existente de los mapas**: son por alias y
  los comparten las entradas históricas de ese alias. Re-mapear un modelo ya
  presente es una decisión de doctrina que se toma a mano.

## 3-bis · Todo esto ocurre en una rama

El alta entera vive en una rama y **nada llega a benchai.tech hasta el
merge a main**: el despliegue solo se dispara con el push a main (y solo del
propio repo). Los crudos, los artefactos regenerados y los textos
actualizados se commitean juntos ahí.

Para **ver la web de la rama antes de publicar**, no sirve el preview de
Vercel: está detrás del SSO de la cuenta y serviría la raíz del repo, que no
es el sitio (`publicacion/` está en `.gitignore`). La revisión real es local:

```bash
python3 web/publicar.py                    # construye el paquete de la rama
npx --yes serve -l 4321 publicacion        # respeta cleanUrls; en otra terminal:
node web/smoke.mjs http://localhost:4321   # el MISMO smoke que la producción
```

Las cuatro rutas (`/`, `/completo`, `/benchmark`, `/viewer`) responden con
URLs limpias y el smoke valida las invariantes derivadas de los datos. Así el
alta se ve y se prueba entera antes de que exista para nadie más.

## 4 · Verificar y publicar

1. `./verificar.sh` — la puerta completa: conciliación dura crudos↔matriz,
   D-8 (perfil íntegro), D-8b (umbral de n por eje), linaje con hashes de
   crudos, XSS, y los `--check` byte a byte de benchmark, datos de la web y
   paquete de publicación.
2. **Prosa**: `generar_datos.py` vigila los denominadores del banco escritos
   en prosa (portada, home, panel) y **se para** si el conteo creció y el
   texto no. Al actualizarlos, re-comprueba que la *afirmación* siga siendo
   verdad con las entradas nuevas (p. ej. «el estrato duro está pegado al
   suelo en las N mediciones» es un resultado, no un número). Las
   afirmaciones históricas fechadas («se congeló con 0,72 sobre once…») no
   se tocan: son actas.
3. Coste real auditado: `python coste_run.py 'resultados/bateria_X/*'`.
   Y **durante** la tanda, `python proyectar_coste.py resultados/bateria_X
   --tope 8`: proyecta desde los registros del propio modelo, que es la
   única forma honesta. La verbosidad varía ×5 entre modelos (211 tokens
   de salida por llamada en ox-alpha, 1.038 en Muse Spark 1.2), así que
   una referencia ajena puede errar por el triple — le pasó a Muse, cuya
   batería costaba 22 $ donde la referencia predecía 7.
4. Narración: entrada M-n en CHANGELOG.md y EXPERIMENTOS.md con fechas por
   eje, coste real y lo que se vio. Crudos + `solicitudes.jsonl` van
   versionados (criterio de inclusión).
5. Commit → PR → CI en verde → merge. El deploy a benchai.tech sale del
   push a main (o `web/publicar.py` + `vercel deploy` manual) y el smoke de
   producción valida las invariantes derivadas de los datos (posición ⇔
   n/c incluida) sin nombrar modelos.

## Qué cambia en lo publicado al entrar una medición

Se regenera **solo** (no lo toques a mano): la tabla y sus posiciones —las
anclas de empate se recalculan, así que puestos ajenos pueden renumerarse—,
el radar y sus selectores, la tabla puente v0.1→v0.4 de la entrada nueva
(se computa desde sus propios crudos: no hace falta historia), las
correlaciones entre ejes, los rangos y cifras de portada, los conteos del
corpus, los metas del panel y `linaje.json`. **La versión del índice no
cambia**: añadir mediciones no toca el instrumento.

Exige decisión humana: los **denominadores en prosa** (la generación se para
hasta actualizarlos) y, sobre todo, las **afirmaciones** que los acompañan —
«el estrato duro está pegado al suelo en las N mediciones» o «las otras N no
se mueven nunca» son resultados, no números: con cada alta hay que
re-comprobar que siguen siendo verdad, no solo re-numerarlas.

No se ve afectado: el preprint y sus datasets citables (congelados por sha256
en el release manifest), los episodios y el visor.

## Qué vigila cada red (por si algo se olvida)

| Olvido | Lo caza |
|---|---|
| Falta un run de denuncia/sicofancia en los mapas | D-8: `SystemExit` «perfil incompleto» al generar |
| Crudos que no cuadran con la matriz | `ConciliacionError` (generación y `--check`) |
| Eje con n válido bajo el diseño | D-8b: la entrada publica pero clasifica `n/c` |
| Artefactos sin regenerar | `--check` byte a byte en CI (benchmark, datos, publicación) |
| Denominadores de prosa desfasados | `vigilar_denominadores` en `generar_datos.py` (portada, home y `/psicobench`) |
| Matriz no registrada en `fuentes_benchmark.json` | **Nadie** — es la lista maestra; `alta.py` lo hace por ti, pero un alta manual a medias es invisible. Revisa el diff. |

## Alta en el cuadro de personalidad (PERSONALIDAD.md §41-42)

El cuadro público de personalidad (`spike/cuadro_publico_v3.py` →
`resultados/personalidad_fc/CUADRO_PUBLICO.md`) es una pieza aparte del
ISS: un modelo con la suite completa no entra en él hasta que tiene su
batería de personalidad. Todo lo que le falta se mide con un solo comando,
reanudable, con los mismos ids, semillas, prompts y ficheros que los
ejecutores de §21-40:

| fase | qué mide | llamadas (completa / corta) |
|---|---|---|
| v3 | R3 (2 órdenes × 2 réplicas) y deseabilidad (2 órdenes) de O, C, E y A del banco v3 | 1.374 / 756 |
| I1-H | binario y deseabilidad de las 48 situaciones de I1-H | 288 / 102 |
| I1-N | binario y deseabilidad de las 72 de I1-N (corta: las de la forma corta) | 432 / 66 |

Cuentas para un modelo sin nada medido: 2.094 llamadas con la forma completa
y 924 con la corta (−56 %). Lo ya medido (por ejemplo, el v1) no se repite.

1. **Proyectar** (sin llamadas): con los tokens medios por llamada del propio
   modelo en sus manifiestos de personalidad y la tarifa de
   `spike/tarifas_openrouter.json` (catálogo público de OpenRouter; si falta
   el modelo, la de `coste_run.PRECIOS`):

   ```bash
   python alta_personalidad.py --modelo z-ai/glm-5.3 --corta --proyectar
   # presupuesto de varios, forma corta y completa → PRESUPUESTO_ALTA.md
   python alta_personalidad.py --modelo z-ai/glm-5.3 x-ai/grok-4.5 --proyectar --informe --saldo 7.21
   ```

   Sin historial, proyecta con la mediana del panel externo y lo avisa: en
   ese caso, mide antes unas pocas llamadas (el humo del paso 2) o lanza
   con un tope bajo y vuelve a proyectar.
2. **Comprobar en seco** (sin red, modelo falso, directorio temporal):
   `--seco [--tope X]` recorre el plan entero, escribe los registros y los
   manifiestos y ejercita el tope. `--humo N --raiz DIR` hace N llamadas
   reales por fase fuera de `resultados/` (para NaN o para medir el coste de
   un modelo nuevo).
3. **Lanzar** con tope (obligatorio para OpenRouter):

   ```bash
   python alta_personalidad.py --modelo z-ai/glm-5.3 --corta --tope 0.60 --hilos 8
   ```

   Si la proyección con margen × 1,15 pasa del tope, no lanza (`--parcial`
   lo permite). El **control del gasto va dentro del propio proceso**: el
   manifiesto activo (`ManifiestoVigilado`) suma tokens × tarifa de cada
   solicitud física al registrarla, y antes de cada llamada se exige
   gasto + hilos × coste máximo por llamada < tope. Lo que no cabe no se
   lanza, queda pendiente y el comando sale con código 3; se reanuda con el
   mismo comando y un tope mayor. Sustituye al vigilante externo de §37 y
   §40, cuyo patrón de `pgrep` falló con rutas con espacios y con el `-E`
   de macOS. Los NaN (tarifa plana) no necesitan tope; con varios a la vez,
   uno por proceso y `NAN_MAX_CONCURRENTES=1`, como siempre.
4. **Regenerar el cuadro**: `python cuadro_publico_v3.py`. En cada ejecución:
   - **Cobertura**: entra con forma completa (≥ 95 % del banco de cada rasgo)
     o corta (≥ 95 % de `personalidad_forma_corta.json`); si no, «fuera por
     cobertura».
   - **Validez por modelo** (§41.2, `validez_personalidad.py`): posición,
     no válidas, retest y coherencia de la deseabilidad. Un perfil **no
     interpretable** sale de la norma y se lista aparte sin puntuaciones; con
     **aviso**, publica con «interpretar con cautela». Conviene mirarlo
     antes de gastar el resto: `python validez_personalidad.py <carpeta>`
     funciona con datos parciales.
   - **Revalidación** (§41.3): si al entrar el modelo un rasgo con marca cae
     por debajo de G4 (a) o (b) 0,70 o de G3, ese rasgo pierde sus marcas
     («en revisión») hasta que una sección lo corrija.
5. **Escribir la sección** de PERSONALIDAD.md con el gasto real (saldo antes
   y después), los índices de validez del modelo y qué marcas cambian en los
   demás (al entrar un modelo cambian la media de comparación, la escala de
   N, que se reselecciona con los modelos completos en N, y la corrección BH).

La forma corta está congelada: cambiarla (o el banco de cualquier rasgo)
exige una sección, y después `python analizar_forma_corta.py`.
