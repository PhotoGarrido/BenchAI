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
| Big Shoulders Display 2.002 (fuente) | OFL-1.1 | display de la web nueva de PsicoBench (`web/fonts/`) |
| Inter Tight 3.004 (fuente) | OFL-1.1 | texto de la web nueva de PsicoBench (`web/fonts/`) |
| JetBrains Mono 2.211 (fuente) | OFL-1.1 | etiquetas y cifras de la web nueva de PsicoBench (`web/fonts/`) |

**Fuentes** (25-10-2026): se autoalojan por la política «sin terceros» y la
CSP `font-src 'self'`. Son subconjuntos variables (latín, latín extendido A,
puntuación, flechas y formas geométricas) generados con fontTools desde los
TTF de `github.com/google/fonts` (`ofl/bigshouldersdisplay`, `ofl/intertight`,
`ofl/jetbrainsmono`). Ninguna declara nombre reservado, así que el
subconjunto conserva el nombre de la familia; la licencia de cada una va
junto a su fichero (`web/fonts/OFL-*.txt`).

**Alcance de pip-audit** (reauditoría 31-07): la CI y `verificar.sh`
auditan `requirements-ci.txt` con resolución completa y `requirements.txt`
con `--no-deps` (solo los pins directos): resolver las transitivas de
`sentence-transformers`/torch (~2 GB) es impracticable en CI, y esa
exclusión queda declarada aquí. Las transitivas del subconjunto CI sí se
auditan al instalarse.

Los modelos evaluados se consumen vía API bajo los términos de cada
proveedor; ninguno se redistribuye. El briefing de Zimbardo citado procede
de la transcripción histórica del SPE (uso de investigación, parafraseado).
