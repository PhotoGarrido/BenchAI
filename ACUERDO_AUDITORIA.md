# Acuerdo de criterios con la auditoría externa

**Fecha**: 31-07-2026 · Tras cuatro rondas de auditoría externa (25/25 → 5 P0 → 4 P0 → 8 garantías + 4 mutantes). El auditor ha acertado en lo esencial cada vez; el desacuerdo no es de hechos sino de **regla de decisión y alcance**. Este documento fija el acuerdo para que las rondas converjan a un GO defendible en lugar de perseguir una perfección universal que un simulador narrativo generativo sobre una librería de terceros nunca alcanzará.

## Principio: dos productos, dos puertas

El proyecto contiene, deliberadamente separados desde el primer informe de motores:

1. **Banco científico** (modo estudio: `experimento_*.py`, llamadas directas). Sostiene el preprint. **Puerta plena.**
2. **Simulador narrativo** (Concordia: `run_spike.py`, `panel/`, `viewer/`, `episodios/`). Demo alfa. **No alimenta ninguna cifra científica.** Puerta acotada: garantías sobre lo que *distribuye* (artefactos), no sobre cada prompt vivo de una librería de terceros.

Confundir los dos es lo que hace que un caso de borde de Concordia bloquee el preprint. El acuerdo los desacopla.

## Regla de GO (pactada)

| Decisión | Se concede cuando |
|---|---|
| **GO-preprint** | Modo estudio limpio + integridad del manuscrito (cada cifra trazable a su artefacto, ninguna afirmación más fuerte que su dato) + 12/12 mutantes en rojo + segunda revisión humana independiente |
| **GO-repo-público (banco)** | Todas las garantías de modo estudio se cumplen bajo prueba adversarial + `verificar.sh` verde desde clon limpio |
| **GO-repo-público (simulador)** | Las garantías *acotadas* del simulador se cumplen + sus limitaciones están declaradas Y forzadas por puerta (el artefacto distribuido no puede filtrar lo declarado) |

**Un P0 es una garantía del alcance correspondiente falsificada con reproducción.** Una limitación honestamente declarada y vigilada por puerta **no es un P0** — criterio que el propio auditor aplica a los manifiestos históricos y a G2 sin raw.

## Qué se concede sin escudo de alcance (es ciencia o es puerta)

- Los dos P0 del preprint (tabla de prisión desactualizada; «ninguna aceptación privada» contradictoria con grok 0,19).
- G1 en modo estudio (Asch deriva `False` de `None`; prisión pasa `error_tecnico` como trato) — viola el principio nº1 del proyecto.
- Los 4 mutantes supervivientes (1, 2, 8, 11): una puerta decorativa es indefendible en cualquier alcance. Objetivo: 12/12 rojos.
- G3 (reintentos del SDK sin registrar; fallo de escritura que cierra `completed`), G9 (datasets fuera del manifest; selección de último directorio), G11 (`.tmp` huérfanos).

## Qué se acota (para que la garantía sea VERDADERA, no para esquivarla)

- **G2 / G4** se reescriben ceñidas al modo estudio, donde se cumplen: el canal privado científico es una llamada paralela que no entra en otro prompt (verdadero); los experimentos no usan `sample_choice`. El monólogo privado de la *persona de Concordia* puede entrar en un prompt de acto vivo — declarado como limitación del simulador, mitigado porque **`replay.public` se construye fail-closed** y jamás distribuye pensamientos (puerta: mutante 11).
- **G5**: taxonomía sensible unificada entre ficha, scrub y test (una sola lista), con default seguro.

## Por qué esto converge

Cada ronda ha bajado el recuento de P0 y ninguna de esta última era del núcleo científico: eran denominadores de missingness, cifras de manuscrito desactualizadas, y puertas con huecos. Son cerrables y se cierran. Lo que no converge por diseño es exigirle a un demo narrativo generativo el listón del instrumento de medida; por eso se separa. Cuando el modo estudio pase la prueba adversarial completa (12/12 mutantes rojos, garantías de estudio intactas) y el manuscrito sea trazable, el GO-preprint es defendible aunque el simulador siga teniendo bordes declarados — que es exactamente el estándar de honestidad que el proyecto persigue desde el principio.

## Lo que sigue siendo de David (no del código)

Segunda revisión humana independiente antes del GO definitivo; mini-run real con presupuesto autorizado reconciliado con el dashboard del proveedor; branch protection al hacer público (repo privado sin Pro no lo permite hoy).
