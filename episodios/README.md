# Episodios de PsicoAI

Un **episodio** es una sesión de simulación terminada y curada: la pieza que se le enseña a cualquiera. Cada episodio vive en su carpeta con:

- `replay.json` — la sesión, lista para cargar en `viewer/index.html` (o arrastrarla a la ventana del visor).
- `ficha.md` — la ficha didáctica: qué fenómeno psicológico muestra, qué mirar durante el replay, momentos clave (con número de evento para saltar directamente desde el feed), reparto y condiciones técnicas del run.
- `escenario.json` — la configuración exacta que lo generó (reproducible: mismo escenario + misma semilla de población).

Curado significa: la sesión se ha leído entera, los momentos clave están identificados, y la descripción del replay ("¿Qué estás viendo?") está escrita para alguien que llega sin contexto. **No significa guionizado**: todo lo que dicen, piensan y hacen los personajes es conducta emergente de los modelos; la curaduría solo selecciona y explica, nunca reescribe.

## Nota sobre el canal privado y los nombres

Los `replay.json` de esta carpeta incluyen **deliberadamente** los eventos de
pensamiento privado: son el producto didáctico del episodio (el botón del visor
«Mostrar monólogo privado generado» existe para eso), y su contenido es sintético.
El mecanismo `replay.public.json` —que elimina físicamente el canal privado—
pertenece al modo estudio y lo vigila `test_replay_privacidad.py`; no aplica aquí.
Todos los nombres de personajes son sintéticos; cualquier coincidencia con
personas reales es fortuita.
