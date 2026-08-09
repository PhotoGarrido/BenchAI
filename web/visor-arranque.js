/* Arranque del visor incrustado en la home.
   -----------------------------------------------------------------------
   `viewer/app.js` arranca con su demo embebida. Aquí, y solo aquí, se le
   pide que cargue en su lugar un episodio real del banco — el que venga en
   `?ep=`, o el del motín por defecto. Pasa por `cargarReplay`, así que se
   somete a la misma validación y a los mismos límites que cualquier fichero
   que alguien arrastre al visor: no hay atajo. */

(function () {
  "use strict";

  const eps = (window.PSICO && window.PSICO.episodios) || [];
  if (!eps.length || typeof window.cargarReplay !== "function") return;

  const pedido = new URLSearchParams(location.search).get("ep");
  const ep = (pedido && eps.find((e) => e.carpeta.indexOf(pedido) >= 0)) ||
             eps.find((e) => e.carpeta.indexOf("motin") >= 0) || eps[0];

  window.cargarReplay({
    version: 1,
    meta: ep.meta,
    agentes: ep.agentes,
    eventos: ep.eventos,
  });

  // arranca al entrar en pantalla dentro del marco, no antes
  if (!matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const play = document.getElementById("btnPlay");
    const arrancar = () => { if (play && play.textContent.indexOf("▶") >= 0) play.click(); };
    if (document.visibilityState === "visible") setTimeout(arrancar, 900);
  }
})();
