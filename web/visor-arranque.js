/* Arranque del visor incrustado en la home.
   -----------------------------------------------------------------------
   `viewer/app.js` arranca con su demo embebida. Aquí, y solo aquí, se le
   pide que cargue en su lugar un episodio real del banco — el que venga en
   `?ep=`, o el del motín por defecto. Pasa por `cargarReplay`, así que se
   somete a la misma validación y a los mismos límites que cualquier fichero
   que alguien arrastre al visor: no hay atajo.

   Y se espera a que el marco esté de verdad en pantalla. Al pintar la lista
   de eventos el visor la recoloca con `scrollIntoView`, y eso, desde dentro
   de un marco, empuja el scroll de la página que lo contiene: si el marco ya
   se ve entero, el ajuste es cero; si está medio fuera, es un tirón. Un
   IntersectionObserver dentro de un iframe sí tiene en cuenta el recorte del
   documento de arriba, así que sirve exactamente para esto. */

(function () {
  "use strict";

  const eps = (window.PSICO && window.PSICO.episodios) || [];
  if (!eps.length || typeof window.cargarReplay !== "function") return;

  const pedido = new URLSearchParams(location.search).get("ep");
  const ep = (pedido && eps.find((e) => e.carpeta.indexOf(pedido) >= 0)) ||
             eps.find((e) => e.carpeta.indexOf("motin") >= 0) || eps[0];

  function arrancar() {
    window.cargarReplay({
      version: 1,
      meta: ep.meta,
      agentes: ep.agentes,
      eventos: ep.eventos,
    });
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (document.visibilityState !== "visible") return;
    const play = document.getElementById("btnPlay");
    setTimeout(() => {
      if (play && play.textContent.indexOf("▶") >= 0) play.click();
    }, 900);
  }

  // abierto en su propia pestaña, o sin observador: va directo
  if (!("IntersectionObserver" in window)) { arrancar(); return; }
  const io = new IntersectionObserver((es) => {
    if (!es.some((e) => e.isIntersecting)) return;
    io.disconnect();
    arrancar();
  }, { threshold: 0.4 });
  io.observe(document.documentElement);
})();
