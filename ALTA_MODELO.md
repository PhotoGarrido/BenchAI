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
   nuevo — sin él, la tabla publica «?». `alta.py` avisa de ambos olvidos.

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
| Denominadores de prosa desfasados | `vigilar_denominadores` en `generar_datos.py` |
| Matriz no registrada en `fuentes_benchmark.json` | **Nadie** — es la lista maestra; `alta.py` lo hace por ti, pero un alta manual a medias es invisible. Revisa el diff. |
