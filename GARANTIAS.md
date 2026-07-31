# Garantías falsables de PsicoAI

Cada fila es una promesa OPERATIVA del repositorio: falsable con una ejecución.
Si un auditor rompe una, es un P0 con reproducción. Versión: v0.1.2-alpha.

| # | Garantía | Dónde se afirma | Puerta que la vigila |
|---|---|---|---|
| G1 | Ninguna respuesta vacía/ilegible/truncada se convierte en conducta, ni en el dato ni dentro de la simulación (diarios, empujones, boletines) | METODO, preprint §2 | `test_barrido_falso.py` |
| G2 | Ni la pregunta ni la respuesta del canal privado entran jamás en otro prompt | preprint §2 | barrido (canal privado) |
| G3 | El manifiesto registra CADA solicitud física (mensajes completos con system, tokens, modelo devuelto), también en pools de hilos, y cierra con estado final completed/failed | preprint §2/§8 | `test_manifiesto.py`, `test_manifiesto_pool.py` |
| G4 | `sample_choice` nunca devuelve un índice de acción real ante ilegibles: opción neutra coherente índice/texto o excepción tipada | auditoría 31-07 | `test_manifiesto.py` |
| G5 | `variables_sensibles` desactivado (o ausente) neutraliza TODOS los atributos sensibles — protagonistas, población generada y variantes — aunque el JSON venga hostil | FICHA_RIESGO | `test_sensibles.py` |
| G6 | Panel→schema→motor sin fisuras: lo que el panel exporta valida; lo que no valida no llega a construir modelos ni gastar | SECURITY, schemas/ | `test_schemas.py` |
| G7 | Ningún dato dinámico se inserta como HTML en panel/visor; CSP activa; sinks prohibidos ausentes | SECURITY | `test_xss_estatico.py` |
| G8 | Los replays escritos (full/public/alias) validan contra su schema, y el público no contiene NINGÚN texto privado | SECURITY, hallazgo 23 | validación en exportador + canary |
| G9 | Toda cifra del preprint se regenera desde datasets fijados por sha256, sin red, sin selección silenciosa de directorios | preprint §8 | `release_manifest.py --verificar`, `--manifest` |
| G10 | Ninguna reclasificación de conducta existe sin errata identificada (1:1, sin huérfanas); toda desviación nueva del reproceso rompe la CI | auditoría reproceso | `reprocesar.py --check` y `--check-publication` |
| G11 | Un run interrumpido (SIGKILL incluido) es distinguible de uno completo y no deja ficheros que parezcan válidos | manifiesto/atómica | escritura atómica + status |
| G12 | El historial git completo está libre de secretos, y la CI lo re-escanea entero en cada push | SECURITY | job `secretos` (log debe decir >1 commits) |

Límites declarados (no son garantías): conducta de G2 no re-derivable (sin raw);
manifiestos confirmatorios del 26-07 sin estado final; κ del juez no validada
según su umbral; branch protection pendiente de repo público.
