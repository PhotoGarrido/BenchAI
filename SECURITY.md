# Política de seguridad

- **Reportar vulnerabilidades**: abre un issue privado (GitHub Security
  Advisories) o contacta al mantenedor. No publiques exploits antes del fix.
- **Alcance**: panel y visor son HTML locales sin backend; el vector
  principal es XSS vía escenarios/replays importados. Ambos validan la
  entrada (schemas/ + límites) y no insertan datos dinámicos con innerHTML;
  hay test estático en CI (`spike/test_xss_estatico.py`).
- **Claves**: jamás se versionan (`.env` está en .gitignore; el historial
  completo se escaneó el 29-07-2026, limpio). El manifiesto por solicitud no
  guarda cabeceras ni claves.
- **Replays**: `replay.public.json` elimina físicamente los campos privados;
  el `full` no debe distribuirse sin revisarlo.
- **Los HTML de log de Concordia no se distribuyen** (pueden incrustar texto
  no confiable).
- **Protección de rama**: los checks `tests` y `secretos` deben ser
  obligatorios para fusionar. En repo privado sin Pro GitHub no lo permite
  (verificado 29-07-2026); al hacer el repo público, activar con:
  `gh api -X PUT repos/PhotoGarrido/BenchAI/branches/main/protection`
  (required_status_checks: strict, contexts [tests, secretos]).
