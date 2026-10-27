/* ===========================================================================
   BenchAI · «Verloop» · el chasquido
   ---------------------------------------------------------------------------
   La transición de las fichas con flechas (la lámina de PsicoBench, la de
   Personalidad): la escena se borra con una máscara desde el lado pulsado
   mientras lo que se ve se deshace en polvo que vuela hacia ese lado; a
   mitad cambia el contenido (lo hace la página, en `alCambiar(paso)`, sin
   animación propia) y entra desde el lado contrario, enfocándose. Sin
   bibliotecas ni rasterizar el DOM: el polvo se muestrea de la geometría y
   los textos que hay en pantalla, cada grano con su color, y se pinta en un
   lienzo encima. Con movimiento reducido, el cambio es instantáneo.

     CHASQUIDO.crear({
       raiz, escena, lienzo,            // la ficha, lo que se borra, el lienzo del polvo
       alCambiar: (paso) => …,          // ±1: pinta la ficha siguiente / anterior
       ant, sig,                        // los botones de las flechas (opcional)
       svg: "#… svg", principal: "perfil", fino: "perfil-fino",
       circulos: "circle.vertice", excluir: ["halo"], bordes: ".caja",
     })  →  { chasquido(paso, lado) }

   Estado visible para las pruebas: `raiz.dataset.transicion` («polvo»,
   «revela» o vacío) y `raiz.dataset.particulas`.
   =========================================================================== */
(function () {
  "use strict";
  function crear(o) {
    /* ── (27-10): las flechas mueven la ficha ENTERA. La escena
       se borra desde el lado pulsado mientras lo que se ve se deshace en
       polvo que vuela hacia ese lado; la medición nueva entra desde el lado
       contrario. Sin bibliotecas ni rasterizar el DOM: el polvo se muestrea
       de la geometría y los textos que hay en pantalla, cada grano con su
       color, y se pinta en un lienzo encima. Un clic de ratón en un perfil
       fino, la ficha o la dirección siguen con el morph del octógono. ── */
    const { raiz, escena, lienzo } = o;
    const ctx = lienzo && lienzo.getContext ? lienzo.getContext("2d") : null;
    const quieto = o.quieto != null ? o.quieto : matchMedia("(prefers-reduced-motion: reduce)").matches;
    const excluir = o.excluir || [];
    let ocupado = false, pendiente = null;

    function muestras() {
      const base = lienzo.getBoundingClientRect(), pts = [];
      const pon = (x, y, color, a) => { if (a > 0.03) pts.push({ x: x - base.left, y: y - base.top, color, a: Math.min(1, a) }); };
      const op = (cs, prop) => (parseFloat(cs.opacity) || 0) * (cs[prop] === "" ? 1 : parseFloat(cs[prop]));
      const svg = escena.querySelector(o.svg || "svg");
      if (svg && svg.getScreenCTM()) {
        const m = svg.getScreenCTM(), aP = (x, y) => new DOMPoint(x, y).matrixTransform(m);
        svg.querySelectorAll("polygon, polyline, line").forEach((n) => {
          if (excluir.some((c) => n.classList.contains(c))) return;
          const cs = getComputedStyle(n);
          if (cs.display === "none" || cs.visibility === "hidden") return;
          const vs = n.tagName === "line"
            ? [aP(+n.getAttribute("x1"), +n.getAttribute("y1")), aP(+n.getAttribute("x2"), +n.getAttribute("y2"))]
            : Array.from(n.points, (q) => aP(q.x, q.y));
          if (vs.length < 2) return;
          const principal = n.classList.contains(o.principal || "perfil");
          if (cs.stroke && cs.stroke !== "none") {
            const a = op(cs, "strokeOpacity"), cerrado = n.tagName === "polygon" ? vs.concat([vs[0]]) : vs;
            const pasoL = principal ? 1.4 : n.classList.contains(o.fino || "perfil-fino") ? 4 : 3;
            for (let i = 1; i < cerrado.length; i++) {
              const p0 = cerrado[i - 1], p1 = cerrado[i], L = Math.hypot(p1.x - p0.x, p1.y - p0.y);
              for (let t = 0; t < L; t += pasoL) pon(p0.x + (p1.x - p0.x) * t / L, p0.y + (p1.y - p0.y) * t / L, cs.stroke, a * (principal ? 1 : 1.6));
            }
          }
          // el relleno del perfil principal, a puñados dentro del polígono
          if (principal && cs.fill && cs.fill !== "none") {
            const xs = vs.map((q) => q.x), ys = vs.map((q) => q.y);
            const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
            const dentro = (x, y) => { let c = false; for (let i = 0, j = vs.length - 1; i < vs.length; j = i++) {
              if ((vs[i].y > y) !== (vs[j].y > y) && x < (vs[j].x - vs[i].x) * (y - vs[i].y) / (vs[j].y - vs[i].y) + vs[i].x) c = !c; } return c; };
            const n2 = Math.min(1600, Math.round((x1 - x0) * (y1 - y0) / 60));
            for (let i = 0; i < n2; i++) { const x = x0 + Math.random() * (x1 - x0), y = y0 + Math.random() * (y1 - y0); if (dentro(x, y)) pon(x, y, cs.fill, 0.5); }
          }
        });
        svg.querySelectorAll((o.circulos || "circle.vertice") + ", text").forEach((n) => {
          const cs = getComputedStyle(n), r = n.getBoundingClientRect(), c = n.tagName === "text" ? cs.fill : cs.stroke;
          const cuantos = Math.round(r.width * r.height / (n.tagName === "text" ? 9 : 4));
          for (let i = 0; i < cuantos; i++) pon(r.left + Math.random() * r.width, r.top + Math.random() * r.height, c, op(cs, "fillOpacity") * 0.9);
        });
      }
      // los textos de las tarjetas, renglón a renglón, con su color
      const paseo = document.createTreeWalker(escena, NodeFilter.SHOW_TEXT), rango = document.createRange();
      for (let t = paseo.nextNode(); t; t = paseo.nextNode()) {
        if (!t.textContent.trim() || t.parentElement.closest("svg")) continue;
        const cs = getComputedStyle(t.parentElement);
        if (cs.visibility === "hidden" || cs.display === "none") continue;
        rango.selectNodeContents(t);
        Array.from(rango.getClientRects()).forEach((r) => {
          const cuantos = Math.round(r.width * r.height / 7);
          for (let i = 0; i < cuantos; i++) pon(r.left + Math.random() * r.width, r.top + r.height * (0.18 + Math.random() * 0.64), cs.color, 0.85);
        });
      }
      // el borde de las cajas que lo tengan
      escena.querySelectorAll(o.bordes || ".ll-caja").forEach((b) => {
        const r = b.getBoundingClientRect(), c = getComputedStyle(b).borderTopColor;
        for (let x = 0; x < r.width; x += 3) { pon(r.left + x, r.top, c, 0.8); pon(r.left + x, r.bottom, c, 0.8); }
        for (let y = 0; y < r.height; y += 3) { pon(r.left, r.top + y, c, 0.8); pon(r.right, r.top + y, c, 0.8); }
      });
      // tope de granos: por encima, se diezma al azar
      const TOPE = 9000, quedan = pts.length > TOPE ? pts.filter(() => Math.random() < TOPE / pts.length) : pts;
      return quedan.sort((a, b) => (a.color < b.color ? -1 : a.color > b.color ? 1 : 0));
    }

    // la máscara deja ver la escena desde el lado contrario al pulsado hasta
    // `pos` (en %), con un filo de 8 puntos
    const mascara = (lado, pos) => {
      const g = pos >= 104 ? "" : `linear-gradient(${lado > 0 ? 90 : 270}deg, #000 ${pos - 4}%, transparent ${pos + 4}%)`;
      escena.style.webkitMaskImage = g; escena.style.maskImage = g;
    };

    // `paso`: ±1 en el orden de la ficha; `lado`: ±1, hacia dónde vuela el polvo
    function chasquido(paso, lado) {
      if (quieto || !ctx) { o.alCambiar(paso); return; }
      if (ocupado) { pendiente = [paso, lado]; return; }
      ocupado = true;
      raiz.dataset.transicion = "polvo";
      const r = lienzo.getBoundingClientRect(), dpr = Math.min(2, devicePixelRatio || 1);
      lienzo.width = Math.round(r.width * dpr); lienzo.height = Math.round(r.height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const pts = muestras(), er = escena.getBoundingClientRect(), x0 = er.left - r.left, W = er.width || 1;
      const BARRIDO = 640, ENTRA = 600;
      pts.forEach((q) => {
        const f = lado > 0 ? (x0 + W - q.x) / W : (q.x - x0) / W;
        q.t0 = Math.max(0, Math.min(1, f)) * BARRIDO + Math.random() * 70;
        q.v = 40 + Math.random() * 180; q.ac = 260 + Math.random() * 620; q.sube = 10 + Math.random() * 110;
        q.vida = 600 + Math.random() * 700; q.fase = Math.random() * 6.3; q.tam = Math.random() < 0.22 ? 2.4 : 1.5;
      });
      raiz.dataset.particulas = String(pts.length);
      const t0 = performance.now();
      let cambiado = false, revela0 = 0, entrada = false;
      const cuadro = (ahora) => {
        const t = ahora - t0;
        if (!cambiado) {
          // 1 · la escena se borra desde el lado pulsado
          mascara(lado, (1 - Math.min(1, t / BARRIDO)) * 108 - 4);
          if (t >= BARRIDO + 80) {
            cambiado = true; revela0 = ahora;
            o.alCambiar(paso);
            raiz.dataset.transicion = "revela";
          }
        } else if (!entrada) {
          // 2 · la nueva entra desde el lado contrario, enfocándose
          const c = Math.min(1, (ahora - revela0) / ENTRA), f = 1 - Math.pow(1 - c, 3);
          mascara(lado, f * 108 - 4);
          escena.style.transform = `translateX(${-lado * 36 * (1 - f)}px)`;
          escena.style.filter = f < 1 ? `blur(${(1 - f) * 6}px)` : "";
          if (c >= 1) { entrada = true; escena.style.transform = ""; escena.style.filter = ""; mascara(lado, 200); }
        }
        // el polvo: cada grano sale cuando el filo lo alcanza
        ctx.clearRect(0, 0, r.width, r.height);
        let vivos = 0, color = "";
        for (const q of pts) {
          const e = t - q.t0;
          if (e < 0) { vivos++; continue; }
          if (e > q.vida) continue;
          vivos++;
          const u = e / 1000;
          if (q.color !== color) { color = q.color; ctx.fillStyle = color; }
          ctx.globalAlpha = q.a * (1 - Math.pow(e / q.vida, 1.5));
          ctx.fillRect(q.x + lado * (q.v * u + 0.5 * q.ac * u * u), q.y - q.sube * u + Math.sin(q.fase + e / 120) * 10 * u, q.tam, q.tam);
        }
        ctx.globalAlpha = 1;
        if (vivos || !entrada) { requestAnimationFrame(cuadro); return; }
        ctx.clearRect(0, 0, r.width, r.height);
        raiz.dataset.transicion = "";
        ocupado = false;
        if (pendiente) { const [pp, ll] = pendiente; pendiente = null; chasquido(pp, ll); }
      };
      requestAnimationFrame(cuadro);
    }

    if (o.ant) o.ant.addEventListener("click", () => chasquido(-1, -1));
    if (o.sig) o.sig.addEventListener("click", () => chasquido(1, 1));
    // con el dedo, deslizar la ficha: el polvo sigue al dedo y deslizar a la
    // izquierda es «siguiente», como en cualquier carrusel
    let toque = null;
    escena.addEventListener("pointerdown", (ev) => { if (ev.pointerType === "touch") toque = [ev.clientX, ev.clientY]; });
    escena.addEventListener("pointercancel", () => { toque = null; });
    escena.addEventListener("pointerup", (ev) => {
      if (!toque || ev.pointerType !== "touch") return;
      const dx = ev.clientX - toque[0], dy = ev.clientY - toque[1];
      toque = null;
      if (Math.abs(dx) > 60 && Math.abs(dx) > 1.5 * Math.abs(dy)) chasquido(dx < 0 ? 1 : -1, dx < 0 ? -1 : 1);
    });
    return { chasquido };
  }
  window.CHASQUIDO = { crear };
})();
