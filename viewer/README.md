# Visor de replays de PsicoAI

HTML autocontenido (sin dependencias, sin build): ábrelo directamente en el navegador con doble clic, o sírvelo con cualquier servidor estático.

- Al abrir carga una **demo embebida** ("El Centro Aldaba — Día 1").
- Para ver una sesión real: botón **«Cargar replay.json»** o arrastra el fichero a la ventana. Cada run de `spike/run_spike.py` deja su `replay.json` en `spike/runs/<id>/`.
- Controles: espacio = play/pausa · ←/→ = evento anterior/siguiente · botón de velocidad (0.5×–4×) · botón 💭 muestra/oculta los pensamientos privados · clic en cualquier evento del feed salta a ese momento.

El contrato del formato `replay.json` está documentado en `PROPUESTA.md` §9. El visor tolera tipos de evento desconocidos (aparecen solo en el feed), de modo que el formato puede crecer sin romper replays antiguos.
