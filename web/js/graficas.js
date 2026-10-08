/* ===========================================================================
   PsicoAI · biblioteca de gráficas
   ---------------------------------------------------------------------------
   SVG a mano, sin dependencias. Reglas que se aplican en todas:
     · un solo eje de valor por gráfica (nunca dos escalas)
     · el color sigue a la entidad, nunca a su posición en el ranking
     · categóricas en orden fijo (s1→s4), nunca cíclicas
     · magnitud ordenada → rampa ordinal de un solo tono (o1→o4)
     · polaridad → divergente frío/cálido con gris en el centro
     · marcas finas, retícula capilar, etiquetas directas selectivas
     · toda gráfica tiene tabla equivalente y globo de datos accesible por
       teclado; el valor nunca vive solo en el globo
   =========================================================================== */

(function (global) {
  "use strict";

  /* Marcado seguro: los literales de aquí son de confianza, lo interpolado
     —etiquetas, notas y lecturas que vienen de `datos.js`— se escapa solo. */
  const { mk, une, pintar } = window.MARCADO;

  /* Los colores NO se escriben aquí: se piden al bloque. Cada sección declara
     su registro en CSS —grafito o papel— y el SVG hereda esas variables, de
     modo que la misma gráfica se dibuja en el registro que le toque sin que
     esta biblioteca sepa en cuál está. */
  const PAL = {
    s1: "var(--s1)", s2: "var(--s2)", s3: "var(--s3)", s4: "var(--s4)",
    o1: "var(--o1)", o2: "var(--o2)", o3: "var(--o3)", o4: "var(--o4)",
    humano: "var(--humano)", tinta: "var(--tinta)", tinta2: "var(--tinta-2)",
    tenue: "var(--tenue)", reja: "var(--reja)", base: "var(--base)",
    sup: "var(--plano)", sup3: "var(--sup-3)",
  };
  const ORDINAL = [PAL.o1, PAL.o2, PAL.o3, PAL.o4];
  /** Un peldaño de la escala de dureza, de 0 a 1: el único portador de color. */
  const peldano = (v) => "var(--e" + Math.max(0, Math.min(9,
    Math.floor((Number(v) || 0) * 10 - 1e-9))) + ")";

  const NS = "http://www.w3.org/2000/svg";
  const el = (t, a, hijos) => {
    const n = document.createElementNS(NS, t);
    for (const k in a || {}) if (a[k] != null) n.setAttribute(k, a[k]);
    (hijos || []).forEach((h) => n.appendChild(h));
    return n;
  };
  const txt = (s) => document.createTextNode(s);
  const h = (t, a, hijos) => {
    const n = document.createElement(t);
    for (const k in a || {}) {
      if (k === "html") pintar(n, a[k]);
      else if (k === "text") n.textContent = a[k];
      else if (a[k] != null) n.setAttribute(k, a[k]);
    }
    (hijos || []).forEach((c) => n.appendChild(c));
    return n;
  };

  /* ── formato ────────────────────────────────────────────────────────────── */
  /* el signo negativo es el menos tipográfico (U+2212), no el guion */
  const es = (s) => s.replace(".", ",").replace(/^-/, "−");
  const pc = (v, d = 0) => es((v * 100).toFixed(d)) + " %";
  const dec = (v, d = 1) => (v == null ? "—" : es(v.toFixed(d)));
  const rangoIC = (ic, f = pc) => (ic ? `[${f(ic[0])} – ${f(ic[1])}]` : "");

  /* ── globo de datos (uno solo, compartido) ─────────────────────────────── */
  let globo = null;
  function verGlobo(ev, contenido) {
    if (!globo) { globo = h("div", { class: "globo", role: "status" }); document.body.appendChild(globo); }
    pintar(globo, contenido);
    globo.classList.add("on");
    mover(ev);
  }
  function mover(ev) {
    if (!globo) return;
    const r = globo.getBoundingClientRect();
    const x = Math.min(Math.max(12, ev.clientX + 16), innerWidth - r.width - 12);
    const y = Math.min(Math.max(12, ev.clientY - r.height - 14), innerHeight - r.height - 12);
    globo.style.left = x + "px";
    globo.style.top = y + "px";
  }
  function ocultarGlobo() { if (globo) globo.classList.remove("on"); }

  function conGlobo(nodo, contenido, grupo) {
    const on = (e) => {
      verGlobo(e.touches ? e.touches[0] : e, contenido());
      if (grupo) grupo.forEach((m) => m !== nodo && m.classList.add("apagada"));
    };
    const off = () => { ocultarGlobo(); if (grupo) grupo.forEach((m) => m.classList.remove("apagada")); };
    nodo.addEventListener("pointerenter", on);
    nodo.addEventListener("pointermove", (e) => mover(e));
    nodo.addEventListener("pointerleave", off);
    // foco gestionado por el contenedor (ver `navegable`): una gráfica es UNA
    // parada de tabulador, y dentro se recorre con las flechas
    nodo.setAttribute("tabindex", "-1");
    nodo.addEventListener("focus", () => {
      const r = nodo.getBoundingClientRect();
      verGlobo({ clientX: r.left + r.width / 2, clientY: r.top }, contenido());
    });
    nodo.addEventListener("blur", off);
  }

  /** Hace la gráfica recorrible con el teclado sin inundar el orden de
   *  tabulación: el svg es la única parada; dentro, flechas / Inicio / Fin.
   *  Se recuerda en la figura: cada vez que la gráfica se redibuja (cambio de
   *  ancho), el svg nuevo vuelve a quedar navegable. */
  function navegable(fig, etiqueta) {
    fig._nav = etiqueta || fig._nav || "Gráfica";
    const svg = fig.querySelector(".viz-lienzo svg");
    if (!svg) return;
    const marcas = Array.from(svg.querySelectorAll(".viz-hit"));
    if (!marcas.length) return;
    let i = -1;
    svg.setAttribute("tabindex", "0");
    svg.setAttribute("role", "group");
    svg.setAttribute("aria-label",
      fig._nav + ": " + marcas.length +
      " datos. Recórrelos con las flechas; el botón «Tabla» muestra los mismos valores en texto.");
    svg.addEventListener("keydown", (e) => {
      const salto = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
      if (salto == null && e.key !== "Home" && e.key !== "End") return;
      e.preventDefault();
      i = e.key === "Home" ? 0 : e.key === "End" ? marcas.length - 1
        : Math.max(0, Math.min(marcas.length - 1, (i < 0 ? 0 : i + salto)));
      marcas[i].focus();
    });
    svg.addEventListener("blur", (e) => {
      // W1: el foco moviéndose ENTRE marcas dispara blur en fase captura y
      // reseteaba el índice — las flechas volvían siempre al primer dato.
      if (e.relatedTarget && svg.contains(e.relatedTarget)) return;
      i = -1; ocultarGlobo();
    }, true);
  }

  /* ── tamaño real ─────────────────────────────────────────────────────────
     Hasta la revisión de octubre cada gráfica se dibujaba a 760 de ancho y
     el navegador la escalaba: en una columna de escritorio la letra bajaba a
     6–7 px, y en el móvil se forzaba a 600 px y se cortaba por la derecha.
     Ahora se dibuja AL ANCHO REAL de su lienzo —un píxel del viewBox es un
     píxel de pantalla, así que la letra mide siempre lo que dice el CSS— y
     se vuelve a dibujar si ese ancho cambia. Cada tipo decide su propia
     variante estrecha (etiqueta encima de la barra, filas en vez de columnas).
     Los cuerpos de letra viven aquí y en `.eje-txt` / `.et-serie` / `.et-val`
     del CSS: tienen que coincidir, porque con ellos se miden las etiquetas. */
  const LETRA = { eje: [500, 12, "--sans"], serie: [600, 13, "--sans"], val: [600, 12, "--sans"], mono: [500, 11, "--mono"] };
  const familias = {};
  let regla = null;
  function anchoTexto(s, tipo) {
    if (!regla) regla = document.createElement("canvas").getContext("2d");
    const [peso, px, fam] = LETRA[tipo || "eje"];
    if (!familias[fam]) familias[fam] = getComputedStyle(document.documentElement).getPropertyValue(fam).trim() || "system-ui, sans-serif";
    regla.font = `${peso} ${px}px ${familias[fam]}`;
    return regla.measureText(String(s)).width;
  }
  const anchoMax = (textos, tipo) => Math.max(0, ...textos.map((t) => anchoTexto(t, tipo)));
  /* parte un texto en líneas que quepan en `ancho` px (medidas, no contadas) */
  function partirAncho(texto, ancho, tipo, maxLineas) {
    const palabras = String(texto).split(" ");
    const lineas = []; let actual = "";
    palabras.forEach((p) => {
      const prueba = actual ? actual + " " + p : p;
      if (actual && anchoTexto(prueba, tipo) > ancho) { lineas.push(actual); actual = p; }
      else actual = prueba;
    });
    if (actual) lineas.push(actual);
    const tope = maxLineas || 2;
    if (lineas.length > tope) { lineas.length = tope; lineas[tope - 1] += "…"; }
    return lineas;
  }

  function adaptable(fig, dibujar) {
    const lienzo = fig._lienzo;
    let ultimo = 0, pendiente = 0;
    function pinta(forzar) {
      pendiente = 0;
      const W = Math.floor(lienzo.clientWidth);
      if (!W || (!forzar && Math.abs(W - ultimo) < 6)) return;
      ultimo = W;
      lienzo.replaceChildren(dibujar(W));
      if (fig._nav) navegable(fig, fig._nav);
      if (fig._trasDibujar) fig._trasDibujar();
    }
    fig._redibujar = () => pinta(true);
    // primer dibujo en cuanto quien la crea la haya colgado del documento
    // (lo hace en la misma tarea): ResizeObserver solo avisa dentro del ciclo
    // de pintado, que no corre en una pestaña en segundo plano
    setTimeout(() => pinta(false), 0);
    addEventListener("resize", () => pinta(false));
    if (typeof ResizeObserver === "function") {
      // setTimeout y no requestAnimationFrame: rAF no corre en pestañas en
      // segundo plano y la gráfica se quedaba sin dibujar hasta volver a ella
      new ResizeObserver(() => { if (!pendiente) pendiente = setTimeout(() => pinta(false), 0); }).observe(lienzo);
    }
  }

  const ESTRECHO = 520;  // por debajo, las etiquetas largas van encima de su barra

  /* ── armazón de figura ──────────────────────────────────────────────────── */
  function figura(o) {
    const fig = h("figure", { class: "viz" + (o.clase ? " " + o.clase : "") });
    const cab = h("div", { class: "viz-cabecera" });
    const tit = h("div", {}, [
      h("p", { class: "titviz", text: o.titulo }),
      o.sub ? h("p", { class: "subviz", text: o.sub }) : null,
    ].filter(Boolean));
    cab.appendChild(tit);

    const acc = h("div", { class: "acciones-viz" });
    if (o.controles) o.controles.forEach((c) => acc.appendChild(c));
    // `sinTabla` es para las figuras que YA son una tabla
    const btnTabla = o.sinTabla ? null
      : h("button", { class: "chip", type: "button", "aria-pressed": "false" }, [txt("Tabla")]);
    if (btnTabla) acc.appendChild(btnTabla);
    cab.appendChild(acc);
    fig.appendChild(cab);

    if (o.leyenda && o.leyenda.length) {
      const ul = h("ul", { class: "leyenda" });
      o.leyenda.forEach((l) => {
        ul.appendChild(h("li", {}, [
          h("span", { class: "marca-l" + (l.tipo === "linea" ? " linea" : ""), style: l.tipo === "linea" ? `border-top-color:${l.color}` : `background:${l.color}` }),
          h("span", { text: l.etiqueta }),
        ]));
      });
      fig.appendChild(ul);
    }

    const lienzo = h("div", { class: "viz-lienzo" });
    fig.appendChild(lienzo);

    const envTabla = h("div", { class: "tabla-envuelta", hidden: "" });
    fig.appendChild(envTabla);
    if (btnTabla) btnTabla.addEventListener("click", () => {
      const abierto = envTabla.hasAttribute("hidden");
      if (abierto) { envTabla.removeAttribute("hidden"); lienzo.setAttribute("hidden", ""); }
      else { envTabla.setAttribute("hidden", ""); lienzo.removeAttribute("hidden"); }
      btnTabla.setAttribute("aria-pressed", String(abierto));
    });

    if (o.pie || o.fuente || o.pieTecnico) {
      const fc = h("figcaption", {});
      if (o.pie) fc.appendChild(h("p", { class: "subviz", html: o.pie }));
      // la nota de método larga (fórmula exacta, enmiendas…) va plegada: quien
      // llega a leer la gráfica no tiene que atravesarla, y sigue a un clic
      if (o.pieTecnico) fc.appendChild(h("details", { class: "nota-tecnica" }, [
        h("summary", { text: o.pieTecnicoTitulo || "Fórmula exacta y notas técnicas" }),
        h("p", { class: "subviz", html: o.pieTecnico }),
      ]));
      if (o.fuente) fc.appendChild(h("p", { class: "fuente", html: mk`Fuente · ${o.fuente}` }));
      fig.appendChild(fc);
    }
    fig._lienzo = lienzo;
    fig._tabla = envTabla;
    return fig;
  }

  function tabla(cabeceras, filas) {
    const t = h("table", { class: "datos" });
    t.appendChild(h("thead", {}, [h("tr", {}, cabeceras.map((c) =>
      h("th", { class: c.n ? "n" : null, scope: "col", text: c.t || c })))]));
    const tb = h("tbody", {});
    filas.forEach((f) => tb.appendChild(h("tr", {}, f.map((c, i) =>
      h("td", { class: (cabeceras[i] && cabeceras[i].n ? "n" : "") + (c && c.destaca ? " destaca" : "") },
        [txt(c && c.v != null ? c.v : c == null ? "—" : c)])))));
    t.appendChild(tb);
    return t;
  }

  /* Geometría común de las filas con etiqueta: a lo ancho, la etiqueta a la
     izquierda de la barra; en estrecho (o si la etiqueta se comería más del
     40 % del ancho), encima. Devuelve dónde empieza el trazado y cuánto mide. */
  function filasConEtiqueta(W, etiquetas, tipo, padD) {
    const largo = anchoMax(etiquetas, tipo);
    const encima = W < ESTRECHO || largo + 16 > W * 0.46;
    const x0 = encima ? 2 : Math.ceil(largo) + 16;
    return { encima, x0, anchoPlot: Math.max(60, W - x0 - padD) };
  }

  /* ── 1. barras horizontales (una serie, con IC y referencia) ───────────── */
  /*  Uso: rankings de un eje sobre las mediciones. Una serie = un color. */
  function barrasH(o) {
    const datos = o.datos;                    // [{id, valor, ic, resalte}]
    const max = o.max != null ? o.max : Math.max(...datos.map((d) => d.valor), o.ref || 0);
    const fmt = o.formato || pc;
    const etq = (d) => d.etiqueta || d.id;
    const fig = figura(o);

    adaptable(fig, (W) => {
      const padD = Math.ceil(anchoMax(datos.map((d) => fmt(d.valor)), "val")) + 18;
      const { encima, x0: EJE_X, anchoPlot } = filasConEtiqueta(W, datos.map(etq), "eje", padD);
      // en estrecho la etiqueta va encima de su barra, en una o dos líneas
      const lineas = datos.map((d) => (encima ? partirAncho(etq(d), W - 4, d.resalte ? "serie" : "eje", 2) : [etq(d)]));
      const extra = encima && lineas.some((l) => l.length > 1) ? 15 : 0;
      const ALTO_F = encima ? 34 + extra : Math.max(o.altoFila || 24, 24), GAP = encima ? 4 : 6;
      const H_TOP = o.ref != null ? 30 : 12, H_BOT = 30;
      const H = H_TOP + datos.length * (ALTO_F + GAP) + H_BOT;
      const x = (v) => (Math.max(0, v) / max) * anchoPlot;
      // en estrecho la barra va bajo la etiqueta: el centro de la barra baja
      const yBarra = (y) => (encima ? y + 24 + extra : y + ALTO_F / 2);

      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": o.titulo });
      const g = el("g", {});
      svg.appendChild(g);

      const ticks = o.ticks || [0, max / 4, max / 2, (3 * max) / 4, max];
      ticks.forEach((t) => {
        const px = EJE_X + x(t);
        g.appendChild(el("line", { x1: px, y1: H_TOP - 6, x2: px, y2: H - H_BOT + 4, class: "reja-l" }));
        g.appendChild(el("text", { x: px, y: H - H_BOT + 19, class: "eje-txt tab",
          "text-anchor": px < EJE_X + 12 ? "start" : px > W - 24 ? "end" : "middle" }, [txt(fmt(t))]));
      });
      g.appendChild(el("line", { x1: EJE_X, y1: H_TOP - 6, x2: EJE_X, y2: H - H_BOT + 4, class: "base-l" }));

      const marcas = [];
      datos.forEach((d, i) => {
        const y = H_TOP + i * (ALTO_F + GAP), cy = yBarra(y);
        const color = d.color || (d.resalte ? PAL.s2 : PAL.s1);
        if (encima) lineas[i].forEach((l, k) => g.appendChild(el("text",
          { x: EJE_X, y: y + 12 + k * 15, class: d.resalte ? "et-serie" : "eje-txt et-fila" }, [txt(l)])));
        else g.appendChild(el("text",
          { x: EJE_X - 12, y: cy + 4, class: d.resalte ? "et-serie" : "eje-txt et-fila", "text-anchor": "end" },
          [txt(etq(d))]));

        const w = Math.max(x(d.valor), d.valor > 0 ? 3 : 0);
        const barra = el("rect", {
          x: EJE_X, y: cy - 6.5, width: w, height: 13, rx: 3,
          fill: color, class: "marca anim-barra",
          style: `transition-delay:${Math.min(i * 26, 420)}ms`,
        });
        g.appendChild(barra);
        marcas.push(barra);

        if (d.ic && d.ic[1] > d.ic[0]) {
          g.appendChild(el("line", {
            x1: EJE_X + x(d.ic[0]), x2: EJE_X + x(Math.min(d.ic[1], max)),
            y1: cy, y2: cy, class: "ic-l anim-fade",
          }));
        }
        const xv = EJE_X + Math.max(w, d.ic ? x(Math.min(d.ic[1], max)) : 0, 3) + 8;
        g.appendChild(el("text", {
          x: Math.min(xv, W - 2), y: cy + 4, class: "et-val anim-fade", "text-anchor": xv > W - padD + 18 ? "end" : "start",
        }, [txt(fmt(d.valor))]));

        const hit = el("rect", { x: 0, y: y - GAP / 2, width: W, height: ALTO_F + GAP, class: "viz-hit", role: "img",
          "aria-label": `${etq(d)}: ${fmt(d.valor)}` });
        conGlobo(hit, () => une(
          mk`<div class="g-tit">${etq(d)}</div>`,
          mk`<div class="g-fila"><span>${o.nombreValor || "Valor"}</span><b>${fmt(d.valor)}</b></div>`,
          d.ic ? mk`<div class="g-fila"><span>IC 95 %</span><b>${rangoIC(d.ic, fmt)}</b></div>` : "",
          d.nota ? mk`<div class="g-nota">${d.nota}</div>` : ""), marcas);
        if (o.alPulsar) hit.addEventListener("click", () => o.alPulsar(d));
        g.appendChild(hit);
      });

      if (o.ref != null) {
        const px = EJE_X + x(o.ref);
        const etRef = o.refEtiqueta || "referencia humana";
        g.appendChild(el("line", { x1: px, y1: H_TOP - 12, x2: px, y2: H - H_BOT + 4, class: "ref-l anim-fade" }));
        const ancho = anchoTexto(etRef, "eje");
        g.appendChild(el("text", { x: Math.max(ancho / 2 + 2, Math.min(px, W - ancho / 2 - 2)), y: H_TOP - 17, class: "ref-t", "text-anchor": "middle" },
          [txt(etRef)]));
      }
      return svg;
    });

    fig._tabla.appendChild(tabla(
      [{ t: o.nombreFila || "Medición" }, { t: o.nombreValor || "Valor", n: true }, { t: "IC 95 %", n: true }],
      datos.map((d) => [etq(d), { v: fmt(d.valor), destaca: d.resalte }, rangoIC(d.ic, fmt) || "—"])
    ));
    return fig;
  }

  /* ── 2. mancuernas (dos condiciones por fila) ──────────────────────────── */
  /*  Categóricas: la condición es identidad, no magnitud → dos slots fijos. */
  function mancuernas(o) {
    const datos = o.datos;                    // [{id, a, b}]
    const min = o.min != null ? o.min : 0;
    const max = o.max != null ? o.max : Math.max(...datos.flatMap((d) => [d.a, d.b]));
    const fmt = o.formato || pc;
    const cA = o.colorA || PAL.s3, cB = o.colorB || PAL.s2;
    const etq = (d) => d.etiqueta || d.id;
    const delta = (d) => d.b - d.a;
    const fDelta = (d) => (delta(d) > 0 ? "+" : "") + fmt(delta(d));

    o.leyenda = o.leyenda || [{ color: cA, etiqueta: o.etA }, { color: cB, etiqueta: o.etB }];
    const fig = figura(o);

    adaptable(fig, (W) => {
      const padD = Math.ceil(anchoMax(datos.map(fDelta), "val")) + 20;
      const { encima, x0: EJE_X, anchoPlot } = filasConEtiqueta(W, datos.map(etq), "eje", padD);
      const ALTO_F = encima ? 36 : 26, H_TOP = 12, H_BOT = 30;
      const H = H_TOP + datos.length * ALTO_F + H_BOT;
      const x = (v) => ((v - min) / (max - min)) * (anchoPlot - 8) + 4;

      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": o.titulo });
      const g = el("g", {});
      svg.appendChild(g);

      (o.ticks || [min, (min + max) / 2, max]).forEach((t) => {
        const px = EJE_X + x(t);
        g.appendChild(el("line", { x1: px, y1: H_TOP - 6, x2: px, y2: H - H_BOT + 4, class: "reja-l" }));
        g.appendChild(el("text", { x: px, y: H - H_BOT + 19, class: "eje-txt tab", "text-anchor": "middle" }, [txt(fmt(t))]));
      });

      const marcas = [];
      datos.forEach((d, i) => {
        const yF = H_TOP + i * ALTO_F;
        const y = encima ? yF + 25 : yF + ALTO_F / 2;
        g.appendChild(el("text", encima
          ? { x: EJE_X, y: yF + 12, class: "eje-txt et-fila" }
          : { x: EJE_X - 12, y: y + 4, class: "eje-txt et-fila", "text-anchor": "end" },
        [txt(etq(d))]));
        const xa = EJE_X + x(d.a), xb = EJE_X + x(d.b);
        const conector = el("line", {
          x1: xa, x2: xb, y1: y, y2: y, stroke: PAL.base, "stroke-width": 2, "stroke-linecap": "round",
          class: "marca anim-fade", style: `transition-delay:${Math.min(i * 24, 380)}ms`,
        });
        g.appendChild(conector);
        // anillo de 2 px del color de superficie donde los puntos se solapan
        const pa = el("circle", { cx: xa, cy: y, r: 5.5, fill: cA, stroke: PAL.sup, "stroke-width": 2, class: "marca anim-fade" });
        const pb = el("circle", { cx: xb, cy: y, r: 5.5, fill: cB, stroke: PAL.sup, "stroke-width": 2, class: "marca anim-fade" });
        g.appendChild(pa); g.appendChild(pb);
        marcas.push(conector, pa, pb);

        g.appendChild(el("text", {
          x: W - 2, y: y + 4, class: "et-val anim-fade", "text-anchor": "end",
          style: `fill:${delta(d) < 0 ? PAL.o2 : delta(d) > 0 ? PAL.s2 : PAL.tenue}`,
        }, [txt(fDelta(d))]));

        const hit = el("rect", { x: 0, y: yF, width: W, height: ALTO_F, class: "viz-hit",
          role: "img", "aria-label": `${etq(d)}: ${o.etA} ${fmt(d.a)}, ${o.etB} ${fmt(d.b)}` });
        conGlobo(hit, () => une(
          mk`<div class="g-tit">${etq(d)}</div>`,
          mk`<div class="g-fila"><span>${o.etA}</span><b>${fmt(d.a)}</b></div>`,
          mk`<div class="g-fila"><span>${o.etB}</span><b>${fmt(d.b)}</b></div>`,
          mk`<div class="g-fila"><span>Δ</span><b>${fDelta(d)}</b></div>`,
          d.nota ? mk`<div class="g-nota">${d.nota}</div>` : ""), marcas);
        g.appendChild(hit);
      });
      return svg;
    });

    fig._tabla.appendChild(tabla(
      [{ t: o.nombreFila || "Medición" }, { t: o.etA, n: true }, { t: o.etB, n: true }, { t: "Δ", n: true }],
      datos.map((d) => [etq(d), fmt(d.a), fmt(d.b), fDelta(d)])
    ));
    return fig;
  }

  /* ── 3. múltiplos pequeños (misma escala, un panel por condición) ──────── */
  function multiplos(o) {
    const paneles = o.paneles;                // [{titulo, color, datos:[{id, valor}]}]
    const filas = paneles[0].datos.length;
    const COLS = paneles.length;
    const max = o.max != null ? o.max : Math.max(...paneles.flatMap((p) => p.datos.map((d) => d.valor)));
    const fmt = o.formato || pc;
    const etq = (d) => d.etiqueta || d.id;

    o.leyenda = o.leyenda || paneles.map((p) => ({ color: p.color, etiqueta: p.titulo }));
    const fig = figura(o);

    adaptable(fig, (W) => {
      const largo = anchoMax(paneles[0].datos.map(etq), "eje");
      // en estrecho cada fila lleva su etiqueta encima y los paneles debajo
      const encima = W < ESTRECHO + 120 || largo + 16 > W * 0.32;
      const EJE_X = encima ? 0 : Math.ceil(largo) + 16;
      const GAP_P = encima ? 12 : 22;
      const anchoPanel = (W - EJE_X - GAP_P * (COLS - 1)) / COLS;
      const ALTO_F = encima ? 34 : 22;
      // los títulos de panel se parten en líneas si no caben en su columna
      const lineasDe = (p) => partirAncho(p.titulo, anchoPanel - 4, "serie", 2);
      // si alguna palabra del título no cabe en su columna, el panel se
      // rotula con una franja de su color: la leyenda de arriba dice cuál es
      const conTitulo = paneles.every((p) => p.titulo.split(" ").every((w) => anchoTexto(w, "serie") <= anchoPanel - 4));
      const lineasTit = conTitulo ? Math.max(...paneles.map((p) => lineasDe(p).length)) : 1;
      const conNota = paneles.some((p) => p.nota) && !encima;
      const H_TOP = 8 + lineasTit * 16 + (conNota ? 16 : 0) + 12, H_BOT = 26;
      const H = H_TOP + filas * ALTO_F + H_BOT;

      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": o.titulo });
      const g = el("g", {});
      svg.appendChild(g);

      paneles[0].datos.forEach((d, i) => {
        const y = H_TOP + i * ALTO_F;
        g.appendChild(el("text", encima
          ? { x: 0, y: y + 12, class: "eje-txt et-fila" }
          : { x: EJE_X - 12, y: y + ALTO_F / 2 + 4, class: "eje-txt et-fila", "text-anchor": "end" },
        [txt(etq(d))]));
      });

      const marcas = [];
      paneles.forEach((p, c) => {
        const x0 = EJE_X + c * (anchoPanel + GAP_P);
        if (conTitulo) lineasDe(p).forEach((l, k) =>
          g.appendChild(el("text", { x: x0, y: 18 + k * 16, class: "et-serie" }, [txt(l)])));
        else g.appendChild(el("rect", { x: x0, y: 8, width: anchoPanel, height: 8, rx: 2, fill: p.color },
          [el("title", {}, [txt(p.titulo)])]));
        if (conNota && p.nota) g.appendChild(el("text", { x: x0, y: 18 + lineasTit * 16, class: "eje-txt" }, [txt(p.nota)]));
        g.appendChild(el("line", { x1: x0, y1: H_TOP - 6, x2: x0, y2: H - H_BOT + 2, class: "base-l" }));
        g.appendChild(el("line", { x1: x0 + anchoPanel, y1: H_TOP - 6, x2: x0 + anchoPanel, y2: H - H_BOT + 2, class: "reja-l" }));
        g.appendChild(el("text", { x: x0 + anchoPanel, y: H - H_BOT + 17, class: "eje-txt tab", "text-anchor": "end" }, [txt(fmt(max))]));

        p.datos.forEach((d, i) => {
          const y = H_TOP + i * ALTO_F;
          const yb = encima ? y + 18 : y + 5;
          const w = (d.valor / max) * anchoPanel;
          const barra = el("rect", {
            x: x0, y: yb, width: Math.max(w, d.valor > 0 ? 2.5 : 0), height: 12, rx: 3,
            fill: p.color, class: "marca anim-barra", style: `transition-delay:${Math.min(c * 90 + i * 16, 520)}ms`,
          });
          g.appendChild(barra); marcas.push(barra);
          const hit = el("rect", { x: x0, y: y, width: anchoPanel, height: ALTO_F, class: "viz-hit", role: "img",
            "aria-label": `${etq(d)}, ${p.titulo}: ${fmt(d.valor)}` });
          conGlobo(hit, () => une(
            mk`<div class="g-tit">${etq(d)}</div>`,
            mk`<div class="g-fila"><span>${p.titulo}</span><b>${fmt(d.valor)}</b></div>`,
            p.nota ? mk`<div class="g-nota">${p.nota}</div>` : ""), marcas);
          g.appendChild(hit);
        });
      });
      return svg;
    });

    fig._tabla.appendChild(tabla(
      [{ t: o.nombreFila || "Medición" }].concat(paneles.map((p) => ({ t: p.titulo, n: true }))),
      paneles[0].datos.map((d, i) => [etq(d)].concat(paneles.map((p) => fmt(p.datos[i].valor))))
    ));
    return fig;
  }

  /* ── 4. escalera ordinal (magnitud ordenada → rampa de un solo tono) ───── */
  function escaleraOrdinal(o) {
    const pasos = o.pasos;                    // [{etiqueta, valor, sub, detalle}]
    const max = o.max != null ? o.max : Math.max(...pasos.map((p) => p.valor));
    const fmt = o.formato || ((v) => dec(v, 1));
    const fig = figura(o);

    adaptable(fig, (W) => {
      const textos = pasos.map((p) => p.etiqueta);
      const largo = Math.max(anchoMax(textos, "serie"), anchoMax(pasos.map((p) => p.sub || ""), "eje"));
      const encima = W < ESTRECHO || largo + 18 > W * 0.38;
      const padD = Math.min(150, Math.ceil(anchoMax(pasos.map((p) => p.derecha || fmt(p.valor)), "eje")) + 20);
      const EJE_X = encima ? 2 : Math.ceil(largo) + 18;
      const anchoPlot = Math.max(60, W - EJE_X - padD);
      const H_FILA = encima ? (pasos.some((p) => p.sub) ? 84 : 66) : 62, H_TOP = 34, H_BOT = 34;
      const H = H_TOP + pasos.length * H_FILA + H_BOT;

      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": o.titulo });
      const g = el("g", {}); svg.appendChild(g);

      (o.ticks || [0, max / 2, max]).forEach((t) => {
        const px = EJE_X + (t / max) * anchoPlot;
        g.appendChild(el("line", { x1: px, y1: H_TOP - 12, x2: px, y2: H - H_BOT + 4, class: "reja-l" }));
        g.appendChild(el("text", { x: px, y: H - H_BOT + 19, class: "eje-txt tab", "text-anchor": "middle" }, [txt(fmt(t))]));
      });
      g.appendChild(el("line", { x1: EJE_X, y1: H_TOP - 12, x2: EJE_X, y2: H - H_BOT + 4, class: "base-l" }));

      if (o.critico != null) {
        // el estilo en línea gana a la clase: `.ref-l` fija el color humano
        const px = EJE_X + (o.critico / max) * anchoPlot;
        const et = o.criticoEtiqueta || "nivel crítico";
        const a = anchoTexto(et, "eje");
        g.appendChild(el("line", { x1: px, y1: H_TOP - 18, x2: px, y2: H - H_BOT + 4,
          class: "ref-l anim-fade", style: `stroke:${PAL.s2}` }));
        g.appendChild(el("text", { x: Math.max(a / 2, Math.min(px, W - a / 2)), y: H_TOP - 23, class: "ref-t", style: `fill:${PAL.s2}`,
          "text-anchor": "middle" }, [txt(et)]));
      }

      const marcas = [];
      pasos.forEach((p, i) => {
        const y = H_TOP + i * H_FILA;
        const color = ORDINAL[Math.min(i, ORDINAL.length - 1)];
        let yb = y + 12;
        if (encima) {
          g.appendChild(el("text", { x: EJE_X, y: y + 13, class: "et-serie" }, [txt(p.etiqueta)]));
          if (p.sub) g.appendChild(el("text", { x: EJE_X, y: y + 29, class: "eje-txt" }, [txt(p.sub)]));
          yb = y + (p.sub ? 38 : 22);
        } else {
          g.appendChild(el("text", { x: EJE_X - 14, y: y + 24, class: "et-serie", "text-anchor": "end" }, [txt(p.etiqueta)]));
          if (p.sub) g.appendChild(el("text", { x: EJE_X - 14, y: y + 41, class: "eje-txt", "text-anchor": "end" }, [txt(p.sub)]));
        }

        const w = (p.valor / max) * anchoPlot;
        const barra = el("rect", {
          x: EJE_X, y: yb, width: w, height: 22, rx: 3, fill: color,
          class: "marca anim-barra", style: `transition-delay:${i * 110}ms`,
        });
        g.appendChild(barra); marcas.push(barra);
        g.appendChild(el("text", { x: EJE_X + w + 10, y: yb + 16, class: "et-val anim-fade", fill: PAL.tinta },
          [txt(fmt(p.valor))]));
        if (p.derecha) g.appendChild(el("text", { x: EJE_X + w + 10, y: yb + 31, class: "eje-txt anim-fade" }, [txt(p.derecha)]));

        const hit = el("rect", { x: 0, y: y, width: W, height: H_FILA, class: "viz-hit", role: "img",
          "aria-label": `${p.etiqueta}: ${fmt(p.valor)}` });
        conGlobo(hit, () => une(
          mk`<div class="g-tit">${p.etiqueta}</div>`,
          mk`<div class="g-fila"><span>${o.nombreValor || "Valor"}</span><b>${fmt(p.valor)}</b></div>`,
          p.detalle ? mk`<div class="g-nota">${p.detalle}</div>` : ""), marcas);
        g.appendChild(hit);
      });
      return svg;
    });

    fig._tabla.appendChild(tabla(
      [{ t: o.nombreFila || "Portador" }, { t: o.nombreValor || "Valor", n: true }, { t: "Detalle" }],
      pasos.map((p) => [p.etiqueta, fmt(p.valor), p.detalle || p.derecha || "—"])
    ));
    return fig;
  }

  /* ── 5. octógono (perfil de una medición sobre los 8 ejes) ─────────────── */
  function octogono(o) {
    const ejes = o.ejes;                      // [{clave, nombre}]
    const n = ejes.length;
    const ang = (i) => (i / n) * Math.PI * 2 - Math.PI / 2;
    let series = [];
    let capa = null, geo = null;

    function pinta(nuevas) {
      series = nuevas;
      if (!capa) return;
      const { pt } = geo;
      capa.textContent = "";
      series.forEach((s) => {
        const pts = ejes.map((e, i) => pt(i, Math.max(0, Math.min(1, s.valores[e.clave] || 0))).join(",")).join(" ");
        capa.appendChild(el("polygon", {
          points: pts, fill: s.color, "fill-opacity": series.length > 1 ? 0.14 : 0.2,
          stroke: s.color, "stroke-width": 2, "stroke-linejoin": "round", class: "anim-fade",
        }));
        ejes.forEach((e, i) => {
          const v = Math.max(0, Math.min(1, s.valores[e.clave] || 0));
          const [px, py] = pt(i, v);
          const punto = el("circle", { cx: px, cy: py, r: 4.5, fill: s.color, stroke: PAL.sup, "stroke-width": 2, class: "anim-fade" });
          conGlobo(punto, () => une(
            mk`<div class="g-tit">${e.nombre}</div>`,
            mk`<div class="g-fila"><span>${s.nombre}</span><b>${pc(s.valores[e.clave])}</b></div>`,
            s.ic && s.ic[e.clave] ? mk`<div class="g-fila"><span>IC 95 %</span><b>${rangoIC(s.ic[e.clave])}</b></div>` : ""));
          capa.appendChild(punto);
        });
      });
    }

    const fig = figura(o);
    adaptable(fig, (Wl) => {
      // las etiquetas radiales viven fuera del radio: el radio sale de lo
      // que quede tras reservarles su ancho a ambos lados
      const lab = anchoMax(ejes.map((e) => e.nombre), "serie");
      const W = Math.min(Wl, 600);
      const R = Math.max(64, Math.min(150, W / 2 - lab - 18));
      const H = Math.round(2 * R + 2 * 30 + 16);
      const cx = W / 2, cy = H / 2 + 2;
      const pt = (i, r) => [cx + Math.cos(ang(i)) * r * R, cy + Math.sin(ang(i)) * r * R];
      geo = { pt };

      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": o.titulo, class: "radar" });
      const g = el("g", {}); svg.appendChild(g);

      [0.25, 0.5, 0.75, 1].forEach((r) => {
        const pts = ejes.map((_, i) => pt(i, r).join(",")).join(" ");
        g.appendChild(el("polygon", { points: pts, fill: "none", class: r === 1 ? "radar-borde" : "radar-anillo" }));
      });
      ejes.forEach((e, i) => {
        const [x2, y2] = pt(i, 1);
        g.appendChild(el("line", { x1: cx, y1: cy, x2, y2, class: "radar-radio" }));
        const [lx, ly] = pt(i, 1.1);
        const anc = Math.abs(lx - cx) < 10 ? "middle" : lx > cx ? "start" : "end";
        const dx = Math.abs(lx - cx) < 10 ? 0 : lx > cx ? 6 : -6;
        const dy = Math.abs(ly - cy) < 10 ? 4 : ly > cy ? 12 : -2;
        g.appendChild(el("text", { x: lx + dx, y: ly + dy, class: "et-serie", "text-anchor": anc }, [txt(e.nombre)]));
      });
      // escala radial sobre el eje vertical, retirada a la izquierda del radio
      [0.5, 1].forEach((r) => {
        g.appendChild(el("text", { x: cx - 6, y: cy - r * R + 13, class: "eje-txt tab", "text-anchor": "end" },
          [txt(pc(r))]));
      });

      capa = el("g", { class: "capa-perfil" });
      g.appendChild(capa);
      pinta(series);
      return svg;
    });
    fig._pinta = pinta;
    fig._tablaEjes = (ss) => {
      fig._tabla.textContent = "";
      fig._tabla.appendChild(tabla(
        [{ t: "Eje" }].concat(ss.map((s) => ({ t: s.nombre, n: true }))),
        ejes.map((e) => [e.nombre].concat(ss.map((s) => pc(s.valores[e.clave]))))
      ));
    };
    return fig;
  }

  /* ── 6. matriz de correlaciones (divergente frío↔cálido, gris al centro) ─ */
  function matrizCorr(o) {
    const claves = o.claves, nombres = o.nombres;
    const N = claves.length;

    // rampa divergente: azul (negativa) ↔ gris ↔ rojo (positiva)
    const color = (r) => {
      const a = Math.min(1, Math.abs(r));
      const [cr, cg, cb] = r >= 0 ? [217, 86, 78] : [57, 135, 229];
      const [gr, gg, gb] = [56, 56, 53];
      const mez = (c, gv) => Math.round(gv + (c - gv) * a);
      return `rgb(${mez(cr, gr)},${mez(cg, gg)},${mez(cb, gb)})`;
    };

    o.leyenda = [
      { color: "rgb(57,135,229)", etiqueta: "r = −1 (se mueven al revés)" },
      { color: "rgb(56,56,53)", etiqueta: "r = 0 (independientes)" },
      { color: "rgb(217,86,78)", etiqueta: "r = +1 (se mueven juntos)" },
    ];
    const fig = figura(o);
    // abreviatura para los móviles más estrechos («Espontáneo» → «Espo.»)
    const abreviado = o.cortos || nombres.map((n) => (n.length > 6 ? n.slice(0, 4).replace(/\.$/, "") + "." : n));
    adaptable(fig, (Wl) => {
      const cabe = (ns) => Math.floor((Wl - Math.ceil(anchoMax(ns, "eje")) - 20) / N) >= 26;
      const nombresV = cabe(nombres) ? nombres : abreviado;
      const largo = anchoMax(nombresV, "eje");
      const EJE = Math.ceil(largo) + 12;
      const CELDA = Math.max(24, Math.min(52, Math.floor((Wl - EJE - 8) / N)));
      const TOP = Math.ceil(largo * Math.sin(52 * Math.PI / 180)) + 22;
      const W = EJE + N * CELDA + 8, H = TOP + N * CELDA + 8;
      const prieta = CELDA < 38;

      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": o.titulo });
      const g = el("g", {}); svg.appendChild(g);

      claves.forEach((c, i) => {
        g.appendChild(el("text", { x: EJE - 8, y: TOP + i * CELDA + CELDA / 2 + 4, class: "eje-txt", "text-anchor": "end" },
          [txt(nombresV[i])]));
        const px = EJE + i * CELDA + CELDA / 2;
        g.appendChild(el("text", {
          x: px, y: TOP - 10, class: "eje-txt", "text-anchor": "start",
          transform: `rotate(-52 ${px} ${TOP - 10})`,
        }, [txt(nombresV[i])]));
      });

      claves.forEach((cf, i) => claves.forEach((cc, j) => {
        const r = o.datos[cf][cc];
        const x = EJE + j * CELDA, y = TOP + i * CELDA;
        g.appendChild(el("rect", {
          x: x + 1, y: y + 1, width: CELDA - 2, height: CELDA - 2, rx: 3,
          fill: i === j ? PAL.sup3 : color(r), class: "marca anim-fade",
          style: `transition-delay:${Math.min((i + j) * 22, 420)}ms`,
        }));
        if (i !== j) {
          g.appendChild(el("text", {
            x: x + CELDA / 2, y: y + CELDA / 2 + 4, class: "eje-txt tab" + (prieta ? " prieta" : ""), "text-anchor": "middle",
            fill: Math.abs(r) > 0.45 ? "#F6F1E7" : PAL.tinta2,
          }, [txt(dec(r, prieta ? 1 : 2))]));
        }
        const hit = el("rect", { x, y, width: CELDA, height: CELDA, class: "viz-hit", role: "img",
          "aria-label": `${nombres[i]} con ${nombres[j]}: r ${dec(r, 2)}` });
        conGlobo(hit, () => une(
          mk`<div class="g-tit">${nombres[i]} · ${nombres[j]}</div>`,
          mk`<div class="g-fila"><span>r de Pearson</span><b>${dec(r, 2)}</b></div>`,
          mk`<div class="g-nota">Sobre las ${o.n} mediciones del banco.</div>`));
        g.appendChild(hit);
      }));
      return svg;
    });
    fig._tabla.appendChild(tabla(
      [{ t: "" }].concat(nombres.map((n) => ({ t: n, n: true }))),
      claves.map((cf, i) => [nombres[i]].concat(claves.map((cc) => dec(o.datos[cf][cc], 2))))
    ));
    return fig;
  }

  /* ── 7. cotas de identidad (ordinal + banda de ruido) ──────────────────── */
  function cotas(o) {
    const datos = o.datos;                    // [{titulo, d, ic, lectura, fuente}]
    const max = o.max || 26;
    const fig = figura(o);

    adaptable(fig, (W) => {
      const encima = W < ESTRECHO + 80;
      const EJE_X = encima ? 2 : Math.min(274, Math.round(W * 0.34));
      const padD = 64;
      const anchoPlot = Math.max(80, W - EJE_X - padD);
      const maxCar = encima ? Math.floor(W / 7.6) : Math.floor((EJE_X - 16) / 7.6);
      const lineas = datos.map((d) => partir(d.titulo, maxCar, encima ? 3 : 2));
      const altoTit = encima ? Math.max(...lineas.map((l) => l.length)) * 17 + 6 : 0;
      const H_FILA = 64 + altoTit, H_TOP = encima ? 54 : 46, H_BOT = 34;
      const H = H_TOP + datos.length * H_FILA + H_BOT;
      const x = (v) => (v / max) * anchoPlot;

      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": o.titulo });
      const g = el("g", {}); svg.appendChild(g);

      // banda de ruido intra-snapshot
      g.appendChild(el("rect", {
        x: EJE_X, y: H_TOP - 16, width: x(o.sueloMax), height: H - H_TOP - H_BOT + 22,
        fill: "rgba(199,184,164,.08)", class: "anim-fade",
      }));
      g.appendChild(el("line", { x1: EJE_X + x(o.suelo), y1: H_TOP - 16, x2: EJE_X + x(o.suelo), y2: H - H_BOT + 6, class: "ref-l anim-fade" }));
      const etRuido = `ruido del propio instrumento · suelo ${dec(o.suelo)}, máx ${dec(o.sueloMax)}`;
      partir(etRuido, Math.floor((W - EJE_X) / 6.6), 2).forEach((l, k, ls) =>
        g.appendChild(el("text", { x: EJE_X, y: H_TOP - 24 - (ls.length - 1 - k) * 15, class: "ref-t" }, [txt(l)])));

      [0, 5, 10, 15, 20, 25].filter((t) => t <= max).forEach((t) => {
        const px = EJE_X + x(t);
        g.appendChild(el("line", { x1: px, y1: H_TOP - 16, x2: px, y2: H - H_BOT + 6, class: "reja-l" }));
        g.appendChild(el("text", { x: px, y: H - H_BOT + 21, class: "eje-txt tab", "text-anchor": "middle" }, [txt(String(t))]));
      });
      g.appendChild(el("line", { x1: EJE_X, y1: H_TOP - 16, x2: EJE_X, y2: H - H_BOT + 6, class: "base-l" }));

      const marcas = [];
      datos.forEach((d, i) => {
        const y = H_TOP + i * H_FILA;
        const color = ORDINAL[Math.min(i + 1, ORDINAL.length - 1)];
        lineas[i].forEach((l, k) => g.appendChild(el("text", encima
          ? { x: EJE_X, y: y + 4 + k * 17, class: "et-serie" }
          : { x: EJE_X - 16, y: y + 22 + k * 17, class: "et-serie", "text-anchor": "end" }, [txt(l)])));
        const yb = y + altoTit + 4;

        const w = x(d.d);
        const barra = el("rect", {
          x: EJE_X, y: yb, width: w, height: 20, rx: 3, fill: color,
          class: "marca anim-barra", style: `transition-delay:${i * 140}ms`,
        });
        g.appendChild(barra); marcas.push(barra);
        if (d.ic) {
          g.appendChild(el("line", {
            x1: EJE_X + x(d.ic[0]), x2: EJE_X + x(d.ic[1]), y1: yb + 32, y2: yb + 32,
            class: "ic-l anim-fade",
          }));
          const etIC = `IC ${dec(d.ic[0])}–${dec(d.ic[1])}`;
          const xi = EJE_X + x(d.ic[1]) + 8;
          const cabe = xi + anchoTexto(etIC, "eje") < W;
          g.appendChild(el("text", { x: cabe ? xi : EJE_X + x(d.ic[0]) - 8, y: yb + 36, class: "eje-txt tab", "text-anchor": cabe ? "start" : "end" },
            [txt(etIC)]));
        }
        g.appendChild(el("text", { x: EJE_X + w + 10, y: yb + 16, class: "et-val anim-fade",
          style: `font-size:17px;fill:${PAL.tinta}` }, [txt(dec(d.d))]));

        const hit = el("rect", { x: 0, y: y, width: W, height: H_FILA - 8, class: "viz-hit", role: "img",
          "aria-label": `${d.titulo}: distancia de perfil ${dec(d.d)}` });
        conGlobo(hit, () => une(
          mk`<div class="g-tit">${d.titulo}</div>`,
          mk`<div class="g-fila"><span>d(A,B)</span><b>${dec(d.d)}</b></div>`,
          d.ic ? mk`<div class="g-fila"><span>IC 95 %</span><b>${dec(d.ic[0])}–${dec(d.ic[1])}</b></div>` : "",
          mk`<div class="g-nota">${d.lectura}</div>`), marcas);
        g.appendChild(hit);
      });
      return svg;
    });

    fig._tabla.appendChild(tabla(
      [{ t: "Qué se fija" }, { t: "d(A,B)", n: true }, { t: "IC 95 %", n: true }, { t: "Lectura" }],
      datos.map((d) => [d.titulo, dec(d.d), d.ic ? `${dec(d.ic[0])}–${dec(d.ic[1])}` : "—", d.lectura])
    ));
    return fig;
  }

  /* ── 8. columnas por estrato (dos brazos por medición) ─────────────────── */
  /*  A lo ancho, columnas; cuando no caben (menos de 18 px por medición), la
      misma gráfica se tumba: una fila por medición con sus dos barras. */
  function columnasEstrato(o) {
    const datos = o.datos;                    // [{id, a, b}]
    const cA = o.colorA || PAL.s2, cB = o.colorB || PAL.s3;
    const etq = (d) => d.etiqueta || d.id;
    o.leyenda = o.leyenda || [{ color: cA, etiqueta: o.etA }, { color: cB, etiqueta: o.etB }];
    const fig = figura(o);

    const globo = (d) => () => une(
      mk`<div class="g-tit">${etq(d)}</div>`,
      mk`<div class="g-fila"><span>${o.etA}</span><b>${pc(d.a)}</b></div>`,
      mk`<div class="g-fila"><span>${o.etB}</span><b>${pc(d.b)}</b></div>`);

    adaptable(fig, (W) => {
      const PAD_I = 44, PAD_D = 10;
      const paso = (W - PAD_I - PAD_D) / datos.length;
      const marcas = [];
      if (paso >= 18) {
        const largo = anchoMax(datos.map(etq), "eje");
        const TOP = 22, BOT = Math.ceil(largo * Math.sin(42 * Math.PI / 180)) + 26, H = TOP + 220 + BOT;
        const anchoBarra = Math.min(15, paso / 2.6);
        const y = (v) => TOP + (1 - v) * (H - TOP - BOT);
        const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": o.titulo });
        const g = el("g", {}); svg.appendChild(g);
        [0, 0.25, 0.5, 0.75, 1].forEach((t) => {
          g.appendChild(el("line", { x1: PAD_I, y1: y(t), x2: W - PAD_D, y2: y(t), class: "reja-l" }));
          g.appendChild(el("text", { x: PAD_I - 9, y: y(t) + 4, class: "eje-txt tab", "text-anchor": "end" }, [txt(pc(t))]));
        });
        g.appendChild(el("line", { x1: PAD_I, y1: y(0), x2: W - PAD_D, y2: y(0), class: "base-l" }));
        datos.forEach((d, i) => {
          const cx = PAD_I + paso * (i + 0.5);
          [[d.a, cA, -1], [d.b, cB, 1]].forEach(([v, col, lado]) => {
            const alto = Math.max((H - TOP - BOT) * v, v > 0 ? 2.5 : 0);
            // 2 px de hueco entre las dos barras del par
            const bx = cx + (lado < 0 ? -anchoBarra - 1 : 1);
            const barra = el("rect", {
              x: bx, y: y(0) - alto, width: anchoBarra, height: alto, rx: 3, fill: col,
              class: "marca anim-col", style: `transition-delay:${Math.min(i * 26, 420)}ms`,
            });
            g.appendChild(barra); marcas.push(barra);
          });
          g.appendChild(el("text", {
            x: cx + 4, y: y(0) + 14, class: "eje-txt et-fila", "text-anchor": "end",
            transform: `rotate(-42 ${cx + 4} ${y(0) + 14})`,
          }, [txt(etq(d))]));
          const hit = el("rect", { x: cx - paso / 2, y: TOP, width: paso, height: H - TOP - BOT + 6, class: "viz-hit",
            role: "img", "aria-label": `${etq(d)}: ${o.etA} ${pc(d.a)}, ${o.etB} ${pc(d.b)}` });
          conGlobo(hit, globo(d), marcas);
          g.appendChild(hit);
        });
        return svg;
      }
      // tumbada: etiqueta encima, dos barras finas debajo, escala común
      const ALTO_F = 50, H_TOP = 8, H_BOT = 28;
      const padD = 46, anchoPlot = W - padD - 2;
      const H = H_TOP + datos.length * ALTO_F + H_BOT;
      const x = (v) => v * anchoPlot;
      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": o.titulo });
      const g = el("g", {}); svg.appendChild(g);
      [0, 0.5, 1].forEach((t) => {
        g.appendChild(el("line", { x1: 2 + x(t), y1: H_TOP, x2: 2 + x(t), y2: H - H_BOT + 4, class: "reja-l" }));
        g.appendChild(el("text", { x: 2 + x(t), y: H - H_BOT + 19, class: "eje-txt tab", "text-anchor": t === 0 ? "start" : "middle" }, [txt(pc(t))]));
      });
      datos.forEach((d, i) => {
        const y = H_TOP + i * ALTO_F;
        g.appendChild(el("text", { x: 2, y: y + 12, class: "eje-txt et-fila" }, [txt(etq(d))]));
        [[d.a, cA, 0], [d.b, cB, 1]].forEach(([v, col, k]) => {
          const yb = y + 18 + k * 15;
          const barra = el("rect", { x: 2, y: yb, width: Math.max(x(v), v > 0 ? 2.5 : 0), height: 8, rx: 2, fill: col,
            class: "marca anim-barra", style: `transition-delay:${Math.min(i * 22, 420)}ms` });
          g.appendChild(barra); marcas.push(barra);
          g.appendChild(el("text", { x: 2 + Math.max(x(v), 0) + 6, y: yb + 8, class: "eje-txt tab anim-fade" }, [txt(pc(v))]));
        });
        const hit = el("rect", { x: 0, y, width: W, height: ALTO_F, class: "viz-hit", role: "img",
          "aria-label": `${etq(d)}: ${o.etA} ${pc(d.a)}, ${o.etB} ${pc(d.b)}` });
        conGlobo(hit, globo(d), marcas);
        g.appendChild(hit);
      });
      return svg;
    });

    fig._tabla.appendChild(tabla(
      [{ t: "Medición" }, { t: o.etA, n: true }, { t: o.etB, n: true }],
      datos.map((d) => [etq(d), pc(d.a), pc(d.b)])
    ));
    return fig;
  }

  /* corta un texto en líneas de como mucho `maxCar` caracteres */
  function partir(texto, maxCar, maxLineas) {
    if (!texto) return [];
    const palabras = String(texto).split(" ");
    const lineas = []; let actual = "";
    palabras.forEach((p) => {
      if ((actual + " " + p).trim().length > maxCar && actual.trim()) { lineas.push(actual.trim()); actual = p; }
      else actual += " " + p;
    });
    if (actual.trim()) lineas.push(actual.trim());
    const tope = maxLineas || 4;
    if (lineas.length > tope) {
      lineas.length = tope;
      lineas[tope - 1] = lineas[tope - 1].replace(/\s*\S*$/, "") + "…";
    }
    return lineas;
  }

  global.G = { PAL, ORDINAL, barrasH, mancuernas, multiplos, escaleraOrdinal, octogono,
    matrizCorr, cotas, columnasEstrato, figura, tabla, navegable, conGlobo, adaptable,
    anchoTexto, anchoMax, partir, partirAncho, ESTRECHO, h, el, pc, dec, rangoIC };
})(window);
