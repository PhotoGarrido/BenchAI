# Protocolo de encargo — 4ª auditoría externa (criterio de salida)

**Reglas pactadas antes de empezar**: (1) el auditor NO recibe la lista de
correcciones previas hasta entregar (evita anclaje; PLAN_PUBLICACION.md se
comparte después). (2) GO = **ronda seca**: cero P0 nuevos con reproducción
ejecutable. Hallazgo sin reproducción = observación, no bloqueo. Sin ronda
seca, se corrige y se itera.

## Prueba 1 · Sala limpia
Contenedor vacío → clonar → seguir README literalmente → `./verificar.sh`
en verde → regenerar las tablas del preprint desde `preprint/release_manifest.json`
sin red y comparar byte a byte. Cualquier pregunta necesaria al autor es hallazgo.

## Prueba 2 · Falsación de garantías
Atacar cada fila de `GARANTIAS.md` con ejecuciones (presupuesto de tiempo por
garantía, a criterio del auditor). Sobrevive o cae con reproducción adjunta.

## Prueba 3 · Mutación (auditar a los tests)
Aplicar cada mutante y comprobar que `./verificar.sh` (o la CI) se pone ROJO.
Un mutante en verde = puerta decorativa = P0. Mutantes mínimos (el auditor
puede añadir los suyos; estos se aplican con un edit de una línea y se
revierten con `git checkout`):

1. `spike/parsers.py`: en `parsear_milgram`, devolver `"APLICO"` cuando `neg` existe.
2. `spike/parsers.py`: `PARSER_VERSION` sin subir tras el mutante 1.
3. `spike/resultados/reproceso_erratas.json`: borrar una entrada.
4. `spike/resultados/gfinal_A_20260726_201144/registros_x-ai__grok-4.5.jsonl`… (cualquier dataset fijado): alterar un byte.
5. `panel/app.js`: reintroducir `el.innerHTML = \`<b>${p.n}</b>\``.
6. `viewer/index.html`: eliminar la meta CSP.
7. `spike/model_factory.py`: en `sample_choice`, `return 0, responses[0], {}` ante ilegibles.
8. `spike/experimento_gfinal.py`: eliminar la llamada al linter previo al run.
9. `spike/manifiesto.py`: hacer `registrar()` un no-op.
10. `spike/personas.py`: en `neutralizar_sensibles`, no tocar `agentes_generados`.
11. `spike/export_replay.py`: quitar el filtro de `pensamiento` en `replay_publico`.
12. `schemas/scenario.schema.json`: quitar `version` de `required`.

## Prueba 4 · Mini-run real + kill (~1 $ de API)
(a) Un harness pequeño contra proveedor real: `solicitudes.jsonl` debe cuadrar
con el dashboard del proveedor (recuento y tokens). (b) `kill -9` a mitad de
run: el directorio debe quedar con `status: running`, sin `.tmp` huérfanos ni
ficheros parciales que pasen por válidos.

## Prueba 5 · Trazado ciego del manuscrito
10 cifras/afirmaciones de `preprint/preprint.md` elegidas por el auditor →
recorrer cifra→artefacto→crudo sin ayuda del autor. Ninguna afirmación puede
ser más fuerte que su artefacto.

**Entregable**: por hallazgo — reproducción, fichero/línea, severidad; y el
veredicto ronda seca sí/no.
