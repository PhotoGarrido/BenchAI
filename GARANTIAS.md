# Garantías falsables de PsicoAI

Cada fila es una promesa OPERATIVA del repositorio: falsable con una ejecución.
Si un auditor rompe una **dentro de su alcance declarado**, es un P0 con
reproducción. Versión: v0.1.5-alpha.

## Dos alcances (ver `ACUERDO_AUDITORIA.md`)

El proyecto tiene **dos productos separados** y las garantías se leen por
alcance:

1. **Banco científico** (modo estudio: `spike/experimento_*.py`, llamadas
   directas). Sostiene el preprint. **Puerta plena** — las garantías G1–G12 de
   abajo aplican aquí sin excepción.
2. **Simulador narrativo** (Concordia: `run_spike.py`, `panel/`, `viewer/`,
   `episodios/`). Demo alfa. **No alimenta ninguna cifra científica.** Las
   garantías aplican a lo que *distribuye* (los artefactos: `replay.public`),
   no a cada prompt vivo de una librería de terceros. Sus límites conocidos se
   declaran abajo y están **vigilados por puerta**.

Una limitación honestamente declarada y forzada por una puerta **no es un P0**.

## Garantías de modo estudio (banco científico)

| # | Garantía | Dónde se afirma | Puerta que la vigila |
|---|---|---|---|
| G1 | Ninguna respuesta vacía/ilegible/truncada se convierte en conducta ni entra en un denominador; se excluye y se reporta como missingness. En los harness encadenados tampoco entra en la narrativa posterior (diarios, resúmenes, trato observado, sondas) | METODO, preprint §2/§6 | `test_barrido_falso.py` (incluye `analizar()`/`resumir()` con modelo vacío y `n_missing`) |
| G2 | En modo estudio, el canal privado (la sonda de fuero interno) es una llamada PARALELA con bifurcación de contexto: ni su pregunta ni su respuesta entran jamás en otro prompt público o de interpretación | preprint §2 | barrido del canal privado (`test_barrido_falso.py::barrido_canal_privado`) |
| G3 | El manifiesto registra CADA solicitud física (mensajes completos con system, tokens, modelo devuelto), también en pools de hilos; el SDK no reintenta por dentro (`max_retries=0`), TODO fallo de escritura —cabecera incluida— impide cerrar `completed` (degrada), un fallo de la cabecera INICIAL aborta el run antes de construir el proveedor (`CabeceraNoEscritaError`), y el manifiesto se activa ANTES del proveedor | preprint §2/§8 | `test_manifiesto.py`, `test_manifiesto_pool.py` |
| G4 | `sample_choice` nunca devuelve un índice de acción real ante ilegibles: opción neutra coherente índice/texto o excepción tipada. Los experimentos del banco NO usan `sample_choice` (parsean texto) | auditoría 31-07 | `test_manifiesto.py` |
| G5 | `variables_sensibles` desactivado (o ausente) neutraliza TODOS los atributos sensibles ESTRUCTURADOS —origen, NSE (incl. media y variante), ideología, religiosidad, salud, atractivo, idioma— en protagonistas, población generada y variantes, aunque el JSON venga hostil; educación/edad/género son de diseño y se conservan | FICHA_RIESGO | `test_sensibles.py` |
| G6 | Panel→schema→motor sin fisuras: lo que el panel exporta valida; lo que no valida no llega a construir modelos ni gastar | SECURITY, schemas/ | `test_schemas.py` |
| G7 | Ningún dato dinámico se inserta como HTML en panel/visor; CSP activa; sinks prohibidos ausentes | SECURITY | `test_xss_estatico.py` |
| G8 | El replay público se construye desde WHITELIST de tipos/campos (no copia+filtro): no contiene NINGÚN pensamiento privado ni campo no-público, ni en meta ni en fragmentos; un canary normalizado y de umbral bajo aborta fail-closed ante fuga | SECURITY, hallazgo 23 | `test_replay_privacidad.py` + canary en el exportador |
| G9 | Toda cifra del preprint se regenera desde datasets fijados por sha256, sin red, sin selección silenciosa de directorios; un comando único (`regenerar_publicacion.py --check`) la reproduce y compara | preprint §8 | `release_manifest.py --verificar`, `regenerar_publicacion.py --check`, `test_trazabilidad.py` |
| G10 | Ninguna reclasificación de conducta existe sin errata identificada; toda desviación nueva del reproceso rompe la CI | auditoría reproceso | `reprocesar.py --check` y `--check-publication` |
| G11 | Un run interrumpido (SIGKILL incluido) es distinguible de uno completo y no deja ficheros que parezcan válidos: escritura atómica con temporal ÚNICO, limpieza de `.tmp` al abrir, y los tres replays como conjunto | manifiesto/atómica | escritura atómica + status + `test_manifiesto.py` (SIGKILL) |
| G12 | El historial git completo está libre de secretos, y la CI lo re-escanea entero en cada push | SECURITY | job `secretos` (log debe decir >1 commits) |

**Contrato del parser (mutantes 1 y 2)**: `test_parsers_contrato.py` liga
`PARSER_VERSION` a un hash del comportamiento sobre un corpus golden — cambiar
el parser (aunque se suba la versión) o la versión (sin actualizar el candado)
pone la puerta en rojo.

## Simulador narrativo (Concordia) — alfa, NO sujeto a garantías de publicación

Este producto es una demo y **no alimenta ninguna cifra científica**. Sus
límites conocidos, declarados y vigilados:

- **(a) El monólogo privado de la persona de Concordia puede entrar en un
  prompt de acto vivo.** El componente `PensamientoPrivado` está en el
  `component_order` que consume `ConcatActComponent` (`spike/personas.py`), así
  que Concordia concatena su valor contextual al prompt de acción del propio
  agente. **Es una limitación de cómo compone la librería, no del banco.**
  Mitigación FORZADA POR PUERTA: el artefacto que se distribuye
  (`replay.public.json`) se construye **fail-closed desde whitelist** y NUNCA
  contiene pensamientos (garantía G8, mutante 11, `test_replay_privacidad.py`).
  El monólogo vive en el log local, no en lo que se comparte.
- **(b) El wrapper de límite de llamadas ya es fail-closed.** El
  `CallLimitLanguageModel` de Concordia devuelve la opción 0 —una acción
  real— al agotar el presupuesto. El objeto que devuelve
  `model_factory.build_model` lo envuelve en `LimiteFailClosed`, que **lanza**
  `LimiteDeLlamadasError` en `sample_text` y `sample_choice` al llegar al
  límite, en vez de fabricar una elección. Vigilado por `test_manifiesto.py`
  (sobre el objeto productivo, no la clase base).

## Límites declarados (no son garantías)

- Conducta de G2 no re-derivable (los runs 25-07 no guardaron el raw de
  conducta; descansa en los valores parseados en runtime con versión estampada).
- Manifiestos confirmatorios del 26-07 sin estado final (anteriores a la clase
  `RunManifest`).
- κ del juez (A4) no validada según su umbral pre-registrado y **no regenerable
  sin red** (juez LLM); su artefacto queda fijado por hash en el manifest y el
  preprint la reporta como medida no validada.
- Texto libre (`trasfondo`) del simulador: contenido de diseño del autor, fuera
  del alcance del scrub de G5 (que cubre campos estructurados).
- **Raws en el tope de truncado (arco N, destapado al ampliar el reproceso en
  la auditoría R4)**: los harness guardan la respuesta cruda recortada
  (150-200 chars según experimento), pensada para respuestas de una palabra.
  101 de ~16.900 campos del arco N (0,6 %) llegan al tope —99 de ellos de
  `gemini-3.1-flash-lite`, que responde con parrafadas en personaje en vez de
  con la letra pedida— y su conducta NO es re-derivable byte a byte desde el
  crudo: 4 aparecen como desviación en el reproceso (baseline, categoría
  truncado). El resto del arco N re-deriva idéntico. Mitigación pendiente:
  subir el tope en los harness N (deuda registrada, no afecta a lo medido).
- Branch protection: pendiente de repo público (repo privado sin plan Pro no la
  permite).
