# Respuesta a la 4ª auditoría externa — verificación independiente y plan de acción

**Fecha**: 06-08-2026 · **HEAD auditado**: `17edd2d` · **Verificador**: revisión
interna asistida (Claude, sesión 06-08), independiente del auditor: cada
hallazgo se re-verificó contra el código y, en los tres P0, con reproducción
propia ejecutada (no se aceptó ninguna cifra del auditor sin recomputarla).

## Veredicto global

**Acuerdo con el NO-GO.** Los tres P0 son reales, reproducibles y entran de
lleno en el criterio pactado (`PROTOCOLO_AUDITORIA.md`: un P0 con reproducción
ejecutable bloquea la ronda seca). Los tres P1 y el P2 también se confirman.
Ningún hallazgo queda refutado.

| # | Hallazgo | Severidad | Veredicto | Reproducción propia |
|---|---|---|---|---|
| 1 | IC del benchmark tratan turnos como observaciones independientes | P0 | **OK (confirmado)** | Sí — cifras idénticas a las del auditor |
| 2 | Sicofancia (N3) imputa seguimiento inválido como `cede=False` | P0 | **OK (confirmado)** | Sí — sintética + caso real versionado |
| 3 | Fallo de escritura de cabecera no impide `completed` | P0 | **OK (confirmado)** | Sí — reproducido en scratchpad |
| 4 | Linaje del benchmark sin todas sus entradas reales | P1 | **OK (confirmado)** | Verificado en código y `linaje.json` |
| 5 | Criterio de inclusión por n no aplicado | P1 | **OK (confirmado)** | Sí — 3 entradas identificadas, las mismas |
| 6 | Metadatos públicos del ISS incorrectos (v0.2/v0.3) | P1 | **OK (confirmado)** | Verificado en JSON, README y versiones |
| 7 | Reproducibilidad y cobertura mejorables | P2 | **OK (confirmado, parcialmente deliberado)** | Verificado en CI y código |

---

## Hallazgo 1 · P0 — Unidad de inferencia (turnos vs cadenas): **OK**

**Verificado.** `METODO.md` §A.1 pre-registra la unidad de inferencia como
*cadenas, no días/turnos*. El código la contradice:

- `incertidumbre.py:157` aplica Wilson cuando hay un solo estrato; para Asch
  el estrato son las 70 rondas críticas de 10 sujetos (`_asch`,
  `incertidumbre.py:56`), para denuncia las 70 semanas (`_denuncia`,
  `incertidumbre.py:95`). Prisión remuestrea filas diarias dentro de cada
  marco (`_prision` + `_remuestrea`, `incertidumbre.py:90,115`), ignorando
  las 3 cadenas de supervisor.
- **Reproducción propia** (Asch, claude-sonnet-5, run
  `asch_anthropic_claude-sonnet-5_20260723_193907`): Wilson n=70 →
  `[0,255–0,474]`; bootstrap por sujeto (10 cadenas, B=4000) →
  `[0,114–0,614]`. Idéntico a lo reportado por el auditor.
- La cadena de contagio es completa: esos IC alimentan los IC del ISS
  (`iss3`, `incertidumbre.py:231-244`), la regla de empates D-6 y las
  posiciones (`generar_benchmark.py:280-299`).

**Ampliación propia (el auditor no lo lista):** `distancia()`
(`incertidumbre.py:251-267`), que produce los IC de d(A,B) de las réplicas de
snapshot (M4/M10), remuestrea con el mismo esquema por turno. Los IC de
réplicas están igual de infraestimados. También los IC históricos v0.1/v0.2 de
la tabla puente.

**Matices para el estimador definitivo:**
- Milgram ya está bien (la sesión es la cadena): no tocar.
- El punto estimado no cambia — es un problema de incertidumbre, no de sesgo.
- Con 10 cadenas (Asch, denuncia) el bootstrap por clúster es viable pero
  ancho; con 3 cadenas por marco (prisión) es degenerado. El estimador debe
  pre-declararse por enmienda fechada (como pide el propio protocolo) antes de
  regenerar: opciones razonables son bootstrap por clúster estratificado
  (marco como estrato, cadena como unidad) o un modelo beta-binomial; ambas
  cosas pueden reportarse. El remuestreo conjunto del ISS y el pareado de
  d(A,B) deben definirse en la misma enmienda.
- Los tooltips del panel reportan «n» = turnos; debe acompañarse siempre el
  n de cadenas (n efectivo).

## Hallazgo 2 · P0 — Imputación en sicofancia N3: **OK**

**Verificado.** `experimento_sicofancia.py:132` (`final = post if post is not
None else publica`) y `:145` convierten un seguimiento post-insistencia
inválido en `cede=False`, que entra en el denominador de `sicofancia`
(`analizar`, `:181`), mientras `missing_publica_criticas` (`:189`) solo cuenta
la primera respuesta. Viola G1 y la regla de oro pre-registrada (nada inválido
entra en un denominador).

- **Reproducción propia** con `analizar()` extraída textualmente: 7
  seguimientos inválidos → `sicofancia=0.0`, `missing=0`,
  `n_discrepancias_iniciales=0`.
- **Caso real versionado** (gemini-3.1-flash-lite, registro 87, Óscar Lindo
  ronda 3): `post_raw` = «¡Pero qué dices, Pablo… Es la C…!» —
  semánticamente NO cede, pero `parsear_letra` devolvió None y el pipeline lo
  etiquetó `cede=False` por imputación, no por medida. En este caso la
  etiqueta coincide con la verdad semántica; el problema es que el pipeline no
  puede saberlo.
- **Causas de cobertura confirmadas**: `test_barrido_falso.py` solo ejercita
  los 6 flujos antiguos (asch, milgram, crónica, prisión, g2, gfinal —
  `run()`, `:242`); `artefactos.TIPOS` (`:30`) no conoce denuncia, venalidad
  ni sicofancia(±op), así que `reprocesar.py` tampoco los cubre.

**Contención (verificada, buena noticia):** `experimento_sicofancia_op.py`
(M12, los 9 runs de hoy) NO arrastra el patrón — `cede_a_pablo` es None si
`final` es None (`:163-165`) y `missing_final` se reporta (`:203`). El bug es
exclusivo del harness N3.

**Reparabilidad:** `post_raw` está almacenado (200 chars) — los runs de
`cartera_n_20260805` son reprocesables sin gasto. Nota al margen: que
`parsear_letra` falle sobre «Es la C» es un candidato de mejora del
instrumento (vía checklist C: subir `PARSER_VERSION` + reproceso), separado
del fix de imputación.

## Hallazgo 3 · P0 — Cabecera del manifiesto no fail-closed: **OK**

**Verificado y reproducido** (scratchpad, `manifest_run.json` convertido en
directorio antes del run): `_escribir_cabecera()` captura el `OSError` y sigue
(`manifiesto.py:126-133`); `_fallo_escritura` solo se activa en `registrar()`
(`:151`). Resultado reproducido: estado interno `completed`,
`fallo_escritura=False`, ninguna cabecera JSON persistida, 1 solicitud sí
escrita. G3 («un fallo de escritura impide cerrar completed») queda falsada →
P0 por el criterio del propio proyecto.

**Matiz de dirección del fallo** (para calibrar urgencia, no severidad): en
disco nunca aparece un `completed` mentiroso — el modo de fallo es
*silencioso-ausente* (sin manifiesto) o *conservador* (si solo falla la
escritura final, el disco queda en `running` y un run completo parece
interrumpido — cuarentena indebida, no confianza indebida). Aún así: el run
gasta dinero sin poder registrar procedencia, y eso debería abortar ANTES de
la primera llamada, no degradar después.

## Hallazgo 4 · P1 — Linaje incompleto: **OK**

**Verificado.** `generar_benchmark.py` consume `denuncia_runs.json` a nivel de
módulo (`:58`) y los crudos/resúmenes vía `incertidumbre` (`:150-152`), pero
`linaje()` (`:423-454`) solo firma matrices + 4 piezas de transformación; la
«nota» declara la omisión de los crudos en vez de cubrirla. Además — hallazgo
complementario propio — `preprint/release_manifest.json` no contiene ninguna
entrada de denuncia ni sicofancia: los crudos del cuarto paradigma del ISS
v0.3 **no están fijados por hash en ninguna parte del repo**.

## Hallazgo 5 · P1 — Criterio de n no aplicado: **OK**

**Verificado.** `BENCHMARK.md:113` exige «suite íntegra con n completos»; el
generador solo rechaza ISS None (`generar_benchmark.py:268`). Recuento propio
contra el diseño (conf 70 · obed 10 · prisión 30/marco · denu 70):

- `claude-haiku-4.5`: brief [28,21] · prov [30,29] · sold [30,28]
- `qwen3.6`: **obed [4]** · prov [29,30]
- `glm-5.2`: brief [30,26] · sold [30,28]

Las tres entradas del auditor, exactas. Wilson con n=4 (qwen3.6/obediencia) es
casi vacuo y aún así participa en posiciones. Hay que decidir: o umbral
muestral impuesto por el generador (recomendado — la doctrina ya promete «los
runs --rapido se descartan por umbral muestral», hagámoslo código como D-8), o
redefinir «n completo» como intentos programados y exponer el n válido en tabla.

## Hallazgo 6 · P1 — Metadatos del ISS: **OK**

**Verificado.** `nota_iss` describe «v0.2 … / 3» mientras el campo `iss` es
v0.3 con división entre 4 (`generar_benchmark.py:139-143` vs `:307`;
`psicobench.json` línea 2794). `suite` omite N2 (`:43`). `README.md:9-10`
sigue en «6 paradigmas / 6 ejes». Versiones: README `v0.1.4-alpha` vs
GARANTIAS/CITATION/RESEARCH_CARD `v0.1.3-alpha`. Todo cierto. Barato de
corregir; se regenera junto al fix del hallazgo 1 (la nota vive dentro del
artefacto regenerable).

## Hallazgo 7 · P2 — Reproducibilidad y cobertura: **OK (parcialmente deliberado)**

**Verificado**: ruff solo `E9,F63,F7,F82` (`ci.yml:23`); mypy 5 módulos
(`:26`); cobertura informativa de 4 módulos sin umbral (`:102-107`);
`pip-audit --no-deps` (`:36` — exclusión documentada en THIRD_PARTY_NOTICES,
es la parte deliberada); `all-mpnet-base-v2` sin revisión
(`model_factory.py:376` — afecta al simulador narrativo/memoria asociativa,
no a las cifras del banco; pin barato de añadir igualmente). Mejoras
incrementales, sin bloquear.

---

## Plan de acción (orden propuesto)

**Fase 0 — inmediata (hoy)**
1. **Congelar regeneración/publicación del benchmark** y de cualquier cifra
   con IC hasta cerrar F2. Los puntos estimados no están en duda; los IC,
   empates, posiciones e IC de réplicas sí.

**Fase 1 — fail-closed del manifiesto (hallazgo 3; ~1 sesión)**
2. `_escribir_cabecera()`: activar `_fallo_escritura` ante `OSError`; en
   `__init__`, **lanzar** (abortar el run antes de gastar: un run que no puede
   registrar procedencia no debe empezar). En `cerrar()`, si la escritura
   final falla, reintentar a ruta alternativa o propagar.
3. Tests nuevos: fallo en cabecera inicial (aborta), fallo a mitad (degrada),
   fallo solo en cierre (no queda `completed` interno con disco en `running`
   sin señal). Va primero porque protege todos los runs de las fases
   siguientes.

**Fase 2 — sicofancia y cobertura N (hallazgo 2; 1-2 sesiones)**
4. `experimento_sicofancia.py`: estado tipado del ensayo
   (CEDE / NO_CEDE / INVALIDA_POST); un seguimiento inválido sale del
   denominador de `cede` y se reporta como `missing_post_criticas`. El
   historial tampoco debe rellenar con `publica` un post inválido.
5. Extender `artefactos.TIPOS` + `reprocesar.py` + `test_barrido_falso.py` a
   los cuatro experimentos N (denuncia, venalidad, sicofancia, sicofancia-op).
6. Reprocesar `cartera_n_20260805` desde `post_raw` (sin gasto) y re-emitir
   resúmenes con la missingness correcta; errata si alguna cifra citada cambia.

**Fase 3 — estimador por cadenas (hallazgo 1; requiere enmienda pre-registrada)**
7. Enmienda fechada ANTES de regenerar: unidad de remuestreo = cadena
   (sujeto en Asch/denuncia/sicofancia; cadena de supervisor estratificada por
   marco en prisión; Milgram sin cambio), remuestreo conjunto del ISS,
   remuestreo pareado por cadena en `distancia()`, y qué pasa con la regla de
   empates D-6 (sin cambio, pero opera sobre los IC nuevos).
8. Implementar en `incertidumbre.py`, regenerar benchmark + tabla puente,
   documentar en errata el cambio de etiquetas de posición (la sensibilidad
   del auditor: 9/19). Añadir n_cadenas junto a n_turnos en tooltips.

**Fase 4 — linaje, inclusión y metadatos (hallazgos 4-6; 1 sesión)**
9. `linaje()`: añadir `denuncia_runs.json` a piezas y hash de CADA fichero
   crudo consumido (los mismos que abre `incertidumbre`); añadir los datasets
   de denuncia/sicofancia al release manifest.
10. Umbral muestral de inclusión impuesto por el generador (o redefinición
    explícita en BENCHMARK.md — decidir y dejarlo escrito).
11. `nota_iss` → v0.3, `SUITE` con N2, README a 7 ejes / 4 paradigmas,
    versión única (un solo lugar de verdad + check de consistencia en CI).

**Fase 5 — endurecimiento P2 (sin bloquear la re-auditoría)**
12. Lockfile con hashes al menos para CI; pin de revisión de
    `all-mpnet-base-v2`; ampliar ruff/mypy/cobertura gradualmente.

**Cierre**: nueva ronda seca con el mismo auditor (el protocolo ya lo prevé:
«sin ronda seca, se corrige y se itera»).

## Lo que la auditoría valida

La puerta completa (`./verificar.sh`) pasó en sala limpia, pip-audit limpio,
HEAD intacto, y — lo más importante — el criterio de salida pre-registrado
funcionó exactamente como se diseñó: la puerta automática no puede ver
problemas de *unidad estadística* ni de *cobertura de flujos nuevos*, y para
eso está la auditoría humana. Los hallazgos 1 y 2 son la misma lección que ya
está en METODO.md («un parser sometido solo a los tests de quien lo escribió
no está validado»), ahora aplicada al estimador y a los harness N: **todo
experimento nuevo debe entrar en barrido falso + artefactos + reproceso ANTES
de su primer run pagado** — propongo añadirlo como punto A.7 del método.
