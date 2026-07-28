# Contribuir a PsicoAI

1. **Lee `METODO.md` primero.** Toda contribución al modo estudio pasa por la
   puerta de calidad: pre-registro si hay hipótesis, linter de contraste,
   barrido con modelo falso, y reproceso en verde (`reprocesar.py --check`).
2. **CI obligatoria**: `cd spike && python test_parsers.py &&
   python test_parsers_tipados.py && python test_manifiesto.py &&
   python test_barrido_falso.py && python test_linter_contraste.py &&
   python test_xss_estatico.py && python reprocesar.py --check`.
3. **Los datos publicados no se tocan**: los `.jsonl` crudos son inmutables;
   las correcciones van por reproceso + errata con ID (ver
   `preprint/auditoria_reproceso.md`).
4. **Parsers**: cualquier cambio sube `PARSER_VERSION`, añade tests con los
   casos nuevos y re-ejecuta el reproceso; si el baseline cambia, el commit
   debe explicarlo y actualizar `reproceso_erratas.json`.
5. Español para UI/comentarios; commits descriptivos; un cambio coherente por PR.
