# Encargo — 5ª auditoría externa (ronda seca sobre la corrección de la R4)

**Objeto**: la etiqueta **`v0.1.5-alpha`** en `main` — anclaje inmutable, para
que lo que audites no se mueva mientras trabajas · **Base de comparación**:
`17edd2d`, el HEAD que auditaste en la R4 · **Fecha del encargo**: 06-08-2026

El diff completo de la ronda es `git diff 17edd2d..v0.1.5-alpha`.

Este encargo hereda `PROTOCOLO_AUDITORIA.md` íntegro. Lo de abajo solo fija el
alcance de ESTA ronda y lo que cambia respecto a la anterior.

## Criterio de salida (sin cambios)

**GO = ronda seca**: cero P0 nuevos con reproducción ejecutable. Un hallazgo sin
reproducción es observación, no bloqueo. Sin ronda seca, se corrige y se itera.

Recordatorio de `GARANTIAS.md`: una limitación **honestamente declarada y
forzada por una puerta** no es un P0. Pero sí lo es una declaración incompleta,
una que la puerta no fuerza de verdad, o una que describe mal lo que ocurre.

## Qué hay en la rama (alcance)

Dos bloques de trabajo, ambos en alcance:

1. **Respuesta a tus 7 hallazgos de la R4.** Los siete se aceptaron; ninguno se
   refutó. Verificar que están cerrados es parte del encargo — **esa lista es
   tuya**, no hace falta que te la devolvamos.
2. **ISS v0.4 (octógono)**: la sicofancia de opinión entra al índice como
   octavo eje, agrupada con la conformidad en un componente «cesión a iguales».
   Estaba pre-declarado y congelado el 06-08 *antes* de medir; se ejecutó
   después de la corrección. Es trabajo nuevo, no auditado nunca.

El árbol es autocontenido: los crudos de los runs nuevos están versionados y
`./verificar.sh` pasa en verde sobre este commit (compruébalo, no nos creas).

## Material sellado hasta que entregues (regla 1 del protocolo)

La regla anti-anclaje del protocolo reserva nuestra narrativa de correcciones
para *después* de la entrega. En esta rama esos documentos **están en el repo**
—no podemos borrarlos sin romper la trazabilidad—, así que la regla se pide por
honor. **No abras, hasta haber entregado tu informe**:

- `PLAN_CORRECCION_R4.md`
- `INFORME_EJECUCION_R4.md`
- `RESPUESTA_AUDITORIA_R4.md`

Si prefieres una copia del árbol sin ellos, pídela y se genera.

**Sí debes leer y atacar** (son producto, no narrativa): `BENCHMARK.md` con sus
enmiendas E-IC-1 / E-IC-1b y el bloque «pendiente E-IC-2»,
`spike/resultados/ERRATA_ic_cadenas.md`, `GARANTIAS.md` con sus límites
declarados, `METODO.md` y `CHANGELOG.md`. Que un documento declare una debilidad
no la exime: comprueba si la declaración es **completa, honesta y forzada**.

## Superficie nueva que merece ensañamiento

No te decimos cómo se arregló nada; sí dónde hay código nuevo, para que no
gastes presupuesto buscándolo:

- `spike/incertidumbre.py` — estimador de incertidumbre reescrito.
- `spike/manifiesto.py` — estado final y escritura.
- `spike/experimento_sicofancia.py` — contabilidad de un experimento del arco N.
- `spike/artefactos.py` + `reprocesar.py` — perímetro de reproceso.
- `spike/generar_benchmark.py`, `spike/release_manifest.py` — linaje, criterios
  de inclusión y fijación de datasets.
- `spike/test_barrido_falso.py`, `spike/test_manifiesto.py`,
  `spike/test_version_unica.py` — puertas nuevas: **audítalas como código, no
  como garantía**. Una puerta que no se pone roja al mutar lo que dice vigilar
  es un P0 (Prueba 3 del protocolo).

## Las cinco pruebas, con lo pendiente de la R4

1. **Sala limpia** — igual que en la R4.
2. **Falsación de garantías** — G3 y G1 se han reescrito; el resto sigue igual.
3. **Mutación** — los 12 mutantes del protocolo **más los tuyos** sobre el
   código nuevo. En la R4 no repetiste los 12: esta vez son especialmente
   pertinentes porque hay puertas nuevas.
4. **Mini-run real + `kill -9`** (~1 $) — **no se ejecutó en la R4**. Es la
   prueba que más nos interesa ahora: conciliación de `solicitudes.jsonl` con el
   dashboard del proveedor, y un SIGKILL a mitad de run. Presupuesto aprobado.
5. **Trazado ciego del manuscrito** — 10 cifras a tu elección. Con el índice
   v0.4 recién ejecutado, las cifras del octógono son terreno fértil.

## Dos preguntas concretas que te pedimos responder

Aparte de lo que encuentres por tu cuenta:

1. **¿Es honesto el tratamiento de los intervalos degenerados?** El benchmark
   publica intervalos de ancho cero en algunos ejes y lo declara. Queremos tu
   juicio sobre si la declaración basta o si publicar `[0,0]` es engañoso
   aunque esté declarado.
2. **¿Aguanta el diseño la unidad de inferencia que declara?** Con 3 cadenas por
   marco en prisión y 10 en el resto, ¿sostiene el banco los intervalos que
   publica, sea cual sea el estimador? Si tu respuesta es que el problema es de
   diseño y no de cálculo, dilo: es más útil que un P0.

## Entregable

Por hallazgo: reproducción ejecutable, fichero/línea, severidad. Y el veredicto
de ronda seca, sí o no. Igual que la R4 — que fue excelente y por eso repetimos.

## Cómo obtener la rama

El repo es privado. Con acceso al remoto:

```bash
git clone <repo> && git checkout v0.1.5-alpha
```

Sin acceso al remoto, un bundle con la ronda completa:

```bash
git bundle create psicoai-r5.bundle 17edd2d..v0.1.5-alpha
```

En ambos casos, lo primero: `./verificar.sh` sobre una copia limpia. Si no sale
`PUERTA COMPLETA: OK`, para y dilo — eso ya es hallazgo.
