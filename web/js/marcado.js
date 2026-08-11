/* ===========================================================================
   PsicoAI · marcado seguro
   ---------------------------------------------------------------------------
   La única puerta a innerHTML de todo `web/`. El resto del sitio no puede
   escribir HTML: `web/js/*.js` tiene prohibido `.innerHTML` y la puerta
   estática (`spike/test_xss_estatico.py`) lo comprueba en cada CI.

   El problema que resuelve: las páginas son prosa con marcado —«<b>18 de
   19</b> mediciones ceden»— y construir eso nodo a nodo, como hacen `panel/`
   y `viewer/`, la volvería ilegible. Pero en esa prosa se interpolan valores
   de `datos.js`, y `datos.js` se REGENERA desde el repositorio: estímulos
   leídos de los `experimento_*.py`, títulos de episodios, identificadores de
   run, frases de informes. Hoy ninguno trae marcado —hay un canario que lo
   comprueba—, pero eso es una propiedad de los datos de hoy, no del código.

   La solución es la de siempre en este proyecto: que no dependa de que nadie
   se acuerde. `mk` es una plantilla etiquetada donde

     · los TROZOS LITERALES —los que están escritos en el código— son de
       confianza y pasan tal cual, con su marcado;
     · TODO lo interpolado se escapa, sin excepción y sin que haya que pedirlo;
     · salvo que sea a su vez un marcado, y entonces se compone (así
       `mk`Ceden ${trozo} de 19`` sigue funcionando con `trozo` ya marcado).

   Y devuelve un OBJETO MARCADO, no una cadena: `pintar` rechaza cualquier
   cosa que no lleve la marca, de modo que una cadena construida a mano no
   puede colarse por la misma puerta ni por descuido ni por refactor.

   Uso:
     h("p", { html: mk`El nivel <b>${n}</b> es el primero irreversible.` })
     MARCADO.pintar(nodo, mk`…`)
   Para texto sin marcado no hace falta nada de esto: `text:` y `textContent`.
   =========================================================================== */

(function (global) {
  "use strict";

  const ESCAPES = {
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  };
  const escapar = (v) => String(v).replace(/[&<>"']/g, (c) => ESCAPES[c]);

  const MARCA = "__marcadoSeguro";
  const esMarcado = (v) =>
    v != null && typeof v === "object" && typeof v[MARCA] === "string";

  /** Plantilla etiquetada: literales de confianza, interpolaciones escapadas. */
  function mk(trozos, ...valores) {
    let html = trozos[0];
    for (let i = 0; i < valores.length; i++) {
      const v = valores[i];
      html += (esMarcado(v) ? v[MARCA] : escapar(v)) + trozos[i + 1];
    }
    return { [MARCA]: html };
  }

  /** Une varios marcados (o valores a escapar) en uno solo. */
  mk.une = (...partes) => mk(["", ...partes.map(() => "")], ...partes);

  /**
   * Vuelca un marcado en un nodo, reemplazando su contenido.
   * Es la ÚNICA asignación a innerHTML de `web/`; la puerta estática exige
   * que siga siendo la única y que este fichero traiga su escapador.
   */
  function pintar(nodo, marcado) {
    if (!esMarcado(marcado)) {
      throw new TypeError(
        "MARCADO.pintar: se esperaba un marcado de mk`…`, no "
        + (typeof marcado) + ". Para texto plano usa textContent.");
    }
    nodo.innerHTML = marcado[MARCA];
  }

  global.MARCADO = { mk, une: mk.une, pintar, esMarcado, escapar };
})(window);
