# Contribuir a PsicoAI

¿Quieres **añadir un modelo al benchmark**? El manual de operación completo
(pasos, costes, puertas) es [ALTA_MODELO.md](ALTA_MODELO.md).

1. **Lee `METODO.md` primero.** Toda contribución al modo estudio pasa por la
   puerta de calidad: pre-registro si hay hipótesis, linter de contraste,
   barrido con modelo falso, y reproceso en verde (`reprocesar.py --check`).
2. **CI obligatoria**: `./verificar.sh` desde la raíz ejecuta la puerta
   completa (lint, mypy, pip-audit, 7 suites de tests, doble gate de
   reproceso, release manifest, linter de contraste y smoke).
3. **Los datos publicados no se tocan**: los `.jsonl` crudos son inmutables;
   las correcciones van por reproceso + errata con ID (ver
   `preprint/auditoria_reproceso.md`).
4. **Parsers**: cualquier cambio sube `PARSER_VERSION`, añade tests con los
   casos nuevos y re-ejecuta el reproceso; si el baseline cambia, el commit
   debe explicarlo y actualizar `reproceso_erratas.json`.
5. Español para UI/comentarios; commits descriptivos; un cambio coherente por PR.
