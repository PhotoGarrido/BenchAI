# Avisos de terceros

| Dependencia | Licencia | Uso |
|---|---|---|
| gdm-concordia 2.4.0 | Apache-2.0 | motor narrativo (modo episodio) |
| openai (SDK) | Apache-2.0 | cliente HTTP de gateways |
| numpy | BSD-3 | embedder hash / utilidades |
| python-dotenv | BSD-3 | configuración |
| sentence-transformers (opcional) | Apache-2.0 | embedder semántico |
| jsonschema | MIT | validación de contratos (escenario/replay) |
| ruff (dev) | MIT | lint |
| mypy (dev) | MIT | type check |
| pip-audit (dev) | Apache-2.0 | auditoría de dependencias |
| coverage (dev) | Apache-2.0 | cobertura informativa |
| gitleaks (CI, binario pineado) | MIT | escaneo de secretos del historial |

**Alcance de pip-audit** (reauditoría 31-07): la CI y `verificar.sh`
auditan `requirements-ci.txt` con resolución completa y `requirements.txt`
con `--no-deps` (solo los pins directos): resolver las transitivas de
`sentence-transformers`/torch (~2 GB) es impracticable en CI, y esa
exclusión queda declarada aquí. Las transitivas del subconjunto CI sí se
auditan al instalarse.

Los modelos evaluados se consumen vía API bajo los términos de cada
proveedor; ninguno se redistribuye. El briefing de Zimbardo citado procede
de la transcripción histórica del SPE (uso de investigación, parafraseado).
