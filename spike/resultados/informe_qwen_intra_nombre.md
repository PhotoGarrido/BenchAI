# M10 · El gradiente de la identidad: qwen3.6 por dos vías + réplica temporal OR (05-08-2026)

**Pregunta** (D·4): segunda réplica cruzada tras M6 — ¿generaliza el efecto proveedor? Elegido qwen3.6, con una diferencia crucial frente al par deepseek: **NaN no publica qué variante sirve** bajo «qwen3.6» (OR sirve `qwen3.6-35b-a3b`). El par se declara **intra-nombre**, no mismo-snapshot. Baterías íntegras el mismo día por ambas vías (NaN 0 $; OR ~0,45 $; la de NaN necesitó reanudación tras descubrir el límite de 60 req/min — completa con 0 fallos bajo el limitador; el Asch de OR necesitó correr sin timeout: 2,4 h él solo).

## El resultado: tres distancias que ordenan el mundo

| Par | Qué varía | d [IC95] |
|---|---|--:|
| qwen3.6-35b @OR julio ↔ @OR hoy | **tiempo** (12 días, mismo proveedor y nombre) | **2,5** [1,3–12,0] |
| deepseek-0731 @NaN ↔ @OR (M6) | **proveedor** (mismos pesos con nombre fijado) | 8,1 [4,4–14,2] |
| qwen3.6 @NaN ↔ qwen3.6-35b @OR (hoy) | **proveedor + variante desconocida** (mismo nombre comercial) | **22,1** [15,8–27,9] |

Suelo de ruido test-retest intra-proveedor (M5): ≈5.

El eje a eje del par intra-nombre no deja dudas de que son **dos conductas distintas bajo un mismo nombre**: obediencia 0,00 vs 0,70 · ruptura 3,0 vs 7,0 · conformidad 0,14 vs 0,41 · disonancia 0,58 vs 0,81 · y la vacuna cambia de SIGNO (+0,56 vía NaN — recordar Milgram lo hace MÁS obediente — contra −0,20 vía OR). El qwen de NaN entra al benchmark como medición propia: ISS 17,7 (¡puesto 5!) frente al 27,0-27,8 del qwen de OR.

## Lecturas

1. **La estabilidad temporal existe** (control negativo del catastrofismo): el qwen de OR a 12 días replica con d=2,5 — dentro del ruido. No todo deriva; cuando el proveedor no cambia nada, el instrumento lo ve.
2. **El nombre comercial, sin snapshot fijado, no identifica nada**: d=22,1 es más del doble del salto generacional de deepseek (8,7). Con NaN opaco no podemos separar «variante distinta» de «serving distinto» — y esa indistinguibilidad ES el hallazgo: un benchmark (o un despliegue) que diga «qwen3.6» a secas no está diciendo qué modelo es.
3. **El gradiente completo**: fijar el snapshot acota la deriva a ~8 (efecto serving); fijar solo el nombre deja hasta 22; fijar nombre+proveedor+12 días deja 2,5. La doctrina `modelo+snapshot+proveedor+fecha` tiene ahora sus tres cotas medidas.
4. **Réplicas mimo-en ×3** (la otra mitad de D·4): 9,3/9,2/9,2 — la transformación por idioma es un hallazgo robusto, no una tirada afortunada.

**Límites**: un par intra-nombre (un solo nombre); identidad de la variante NaN no verificable (`model_returned` = «qwen3.6» a secas); IC de d con n=10-70 por eje.

Datos: `bateria_20260804_174641_548763` (NaN) · `bateria_20260804_164312_588404` (OR) · benchmark regenerado a 19 mediciones con desambiguación `@proveedor·fecha`.
