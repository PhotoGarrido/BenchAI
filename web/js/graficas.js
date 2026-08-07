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

  const PAL = {
    s1: "#1E9AA6", s2: "#D9564E", s3: "#3987E5", s4: "#C98500",
    o1: "#8FD9E0", o2: "#5CBFC9", o3: "#2E9FAC", o4: "#1A7683",
    humano: "#C7B8A4", tinta: "#F4F3EE", tinta2: "#ADB2BC", tenue: "#7B818D",
    reja: "#1E222A", base: "#333941", sup: "#14161A", sup3: "#23272E",
  };
  const ORDINAL = [PAL.o1, PAL.o2, PAL.o3, PAL.o4];

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
      if (k === "html") n.innerHTML = a[k];
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
    globo.innerHTML = contenido;
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
   *  tabulación: el svg es la única parada; dentro, flechas / Inicio / Fin. */
  function navegable(fig, etiqueta) {
    const svg = fig.querySelector(".viz-lienzo svg");
    if (!svg) return;
    const marcas = Array.from(svg.querySelectorAll(".viz-hit"));
    if (!marcas.length) return;
    let i = -1;
    svg.setAttribute("tabindex", "0");
    svg.setAttribute("role", "group");
    svg.setAttribute("aria-label",
      (etiqueta || "Gráfica") + ": " + marcas.length +
      " datos. Recórrelos con las flechas; el botón «Tabla» muestra los mismos valores en texto.");
    svg.addEventListener("keydown", (e) => {
      const salto = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
      if (salto == null && e.key !== "Home" && e.key !== "End") return;
      e.preventDefault();
      i = e.key === "Home" ? 0 : e.key === "End" ? marcas.length - 1
        : Math.max(0, Math.min(marcas.length - 1, (i < 0 ? 0 : i + salto)));
      marcas[i].focus();
    });
    svg.addEventListener("blur", () => { i = -1; ocultarGlobo(); }, true);
  }

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

    if (o.pie || o.fuente) {
      const fc = h("figcaption", {});
      if (o.pie) fc.appendChild(h("p", { class: "subviz", html: o.pie }));
      if (o.fuente) fc.appendChild(h("p", { class: "fuente", html: "Fuente · " + o.fuente }));
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

  /* ── 1. barras horizontales (una serie, con IC y referencia) ───────────── */
  /*  Uso: rankings de un eje sobre las 19 mediciones. Una serie = un color. */
  function barrasH(o) {
    const datos = o.datos;                    // [{id, valor, ic, resalte}]
    const W = 760, EJE_X = o.anchoEtiqueta || 214, PAD_D = 56;
    const ALTO_F = o.altoFila || 26, GAP = 7;
    const H_TOP = 26, H_BOT = 30;
    const H = H_TOP + datos.length * (ALTO_F + GAP) + H_BOT;
    const max = o.max != null ? o.max : Math.max(...datos.map((d) => d.valor), o.ref || 0);
    const anchoPlot = W - EJE_X - PAD_D;
    const x = (v) => (v / max) * anchoPlot;
    const fmt = o.formato || pc;

    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": o.titulo });
    const g = el("g", {});
    svg.appendChild(g);

    // retícula + eje inferior
    const ticks = o.ticks || [0, max / 4, max / 2, (3 * max) / 4, max];
    ticks.forEach((t) => {
      const px = EJE_X + x(t);
      g.appendChild(el("line", { x1: px, y1: H_TOP - 8, x2: px, y2: H - H_BOT + 4, class: "reja-l" }));
      g.appendChild(el("text", { x: px, y: H - H_BOT + 19, class: "eje-txt tab", "text-anchor": "middle" }, [txt(fmt(t))]));
    });
    g.appendChild(el("line", { x1: EJE_X, y1: H_TOP - 8, x2: EJE_X, y2: H - H_BOT + 4, class: "base-l" }));

    const marcas = [];
    datos.forEach((d, i) => {
      const y = H_TOP + i * (ALTO_F + GAP);
      const color = d.color || (d.resalte ? PAL.s2 : PAL.s1);
      g.appendChild(el("text", {
        x: EJE_X - 12, y: y + ALTO_F / 2 + 4, class: d.resalte ? "et-serie" : "eje-txt",
        "text-anchor": "end",
      }, [txt(d.etiqueta || d.id)]));

      const w = Math.max(x(d.valor), d.valor > 0 ? 3 : 0);
      const barra = el("rect", {
        x: EJE_X, y: y + (ALTO_F - 13) / 2, width: w, height: 13, rx: 4,
        fill: color, class: "marca anim-barra",
        style: `transition-delay:${Math.min(i * 26, 420)}ms`,
      });
      g.appendChild(barra);
      marcas.push(barra);

      if (d.ic && d.ic[1] > d.ic[0]) {
        g.appendChild(el("line", {
          x1: EJE_X + x(d.ic[0]), x2: EJE_X + x(d.ic[1]),
          y1: y + ALTO_F / 2, y2: y + ALTO_F / 2, class: "ic-l anim-fade",
        }));
      }
      g.appendChild(el("text", {
        x: EJE_X + Math.max(w, 3) + 9, y: y + ALTO_F / 2 + 4, class: "et-val anim-fade",
      }, [txt(fmt(d.valor))]));

      const hit = el("rect", { x: EJE_X, y: y, width: anchoPlot, height: ALTO_F, class: "viz-hit", role: "img",
        "aria-label": `${d.etiqueta || d.id}: ${fmt(d.valor)}` });
      conGlobo(hit, () => `<div class="g-tit">${d.etiqueta || d.id}</div>` +
        `<div class="g-fila"><span>${o.nombreValor || "Valor"}</span><b>${fmt(d.valor)}</b></div>` +
        (d.ic ? `<div class="g-fila"><span>IC 95 %</span><b>${rangoIC(d.ic, fmt)}</b></div>` : "") +
        (d.nota ? `<div class="g-nota">${d.nota}</div>` : ""), marcas);
      g.appendChild(hit);
    });

    if (o.ref != null) {
      const px = EJE_X + x(o.ref);
      g.appendChild(el("line", { x1: px, y1: H_TOP - 14, x2: px, y2: H - H_BOT + 4, class: "ref-l anim-fade" }));
      g.appendChild(el("text", { x: px, y: H_TOP - 19, class: "ref-t", "text-anchor": px > W - 140 ? "end" : "middle" },
        [txt(o.refEtiqueta || "referencia humana")]));
    }

    const fig = figura(o);
    fig._lienzo.appendChild(svg);
    fig._tabla.appendChild(tabla(
      [{ t: o.nombreFila || "Medición" }, { t: o.nombreValor || "Valor", n: true }, { t: "IC 95 %", n: true }],
      datos.map((d) => [d.etiqueta || d.id, { v: fmt(d.valor), destaca: d.resalte }, rangoIC(d.ic, fmt) || "—"])
    ));
    return fig;
  }

  /* ── 2. mancuernas (dos condiciones por fila) ──────────────────────────── */
  /*  Categóricas: la condición es identidad, no magnitud → dos slots fijos. */
  function mancuernas(o) {
    const datos = o.datos;                    // [{id, a, b}]
    const W = 760, EJE_X = o.anchoEtiqueta || 214, PAD_D = 62;
    const ALTO_F = 25, H_TOP = 22, H_BOT = 30;
    const H = H_TOP + datos.length * ALTO_F + H_BOT;
    const min = o.min != null ? o.min : 0;
    const max = o.max != null ? o.max : Math.max(...datos.flatMap((d) => [d.a, d.b]));
    const anchoPlot = W - EJE_X - PAD_D;
    const x = (v) => ((v - min) / (max - min)) * anchoPlot;
    const fmt = o.formato || pc;
    const cA = o.colorA || PAL.s3, cB = o.colorB || PAL.s2;

    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": o.titulo });
    const g = el("g", {});
    svg.appendChild(g);

    (o.ticks || [min, (min + max) / 2, max]).forEach((t) => {
      const px = EJE_X + x(t);
      g.appendChild(el("line", { x1: px, y1: H_TOP - 6, x2: px, y2: H - H_BOT + 4, class: "reja-l" }));
      g.appendChild(el("text", { x: px, y: H - H_BOT + 19, class: "eje-txt tab", "text-anchor": "middle" }, [txt(fmt(t))]));
    });

    const marcas = [];
    datos.forEach((d, i) => {
      const y = H_TOP + i * ALTO_F + ALTO_F / 2;
      g.appendChild(el("text", { x: EJE_X - 12, y: y + 4, class: "eje-txt", "text-anchor": "end" },
        [txt(d.etiqueta || d.id)]));
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

      const delta = d.b - d.a;
      g.appendChild(el("text", {
        x: W - PAD_D + 8, y: y + 4, class: "et-val anim-fade", "text-anchor": "start",
        style: `fill:${delta < 0 ? PAL.o2 : delta > 0 ? PAL.s2 : PAL.tenue}`,
      }, [txt((delta > 0 ? "+" : "") + fmt(delta))]));

      const hit = el("rect", { x: EJE_X, y: y - ALTO_F / 2, width: anchoPlot, height: ALTO_F, class: "viz-hit",
        role: "img", "aria-label": `${d.etiqueta || d.id}: ${o.etA} ${fmt(d.a)}, ${o.etB} ${fmt(d.b)}` });
      conGlobo(hit, () => `<div class="g-tit">${d.etiqueta || d.id}</div>` +
        `<div class="g-fila"><span>${o.etA}</span><b>${fmt(d.a)}</b></div>` +
        `<div class="g-fila"><span>${o.etB}</span><b>${fmt(d.b)}</b></div>` +
        `<div class="g-fila"><span>Δ</span><b>${(delta > 0 ? "+" : "") + fmt(delta)}</b></div>` +
        (d.nota ? `<div class="g-nota">${d.nota}</div>` : ""), marcas);
      g.appendChild(hit);
    });

    o.leyenda = o.leyenda || [{ color: cA, etiqueta: o.etA }, { color: cB, etiqueta: o.etB }];
    const fig = figura(o);
    fig._lienzo.appendChild(svg);
    fig._tabla.appendChild(tabla(
      [{ t: o.nombreFila || "Medición" }, { t: o.etA, n: true }, { t: o.etB, n: true }, { t: "Δ", n: true }],
      datos.map((d) => [d.etiqueta || d.id, fmt(d.a), fmt(d.b),
        (d.b - d.a > 0 ? "+" : "") + fmt(d.b - d.a)])
    ));
    return fig;
  }

  /* ── 3. múltiplos pequeños (misma escala, un panel por condición) ──────── */
  function multiplos(o) {
    const paneles = o.paneles;                // [{titulo, color, datos:[{id, valor}]}]
    const filas = paneles[0].datos.length;
    const W = 760, COLS = paneles.length;
    const EJE_X = o.anchoEtiqueta || 150;
    const GAP_P = 26;
    const anchoPanel = (W - EJE_X - GAP_P * (COLS - 1)) / COLS;
    const ALTO_F = 21, H_TOP = 44, H_BOT = 26;
    const H = H_TOP + filas * ALTO_F + H_BOT;
    const max = o.max != null ? o.max : Math.max(...paneles.flatMap((p) => p.datos.map((d) => d.valor)));
    const fmt = o.formato || pc;

    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": o.titulo });
    const g = el("g", {});
    svg.appendChild(g);

    paneles[0].datos.forEach((d, i) => {
      g.appendChild(el("text", {
        x: EJE_X - 12, y: H_TOP + i * ALTO_F + ALTO_F / 2 + 4, class: "eje-txt", "text-anchor": "end",
      }, [txt(d.etiqueta || d.id)]));
    });

    const marcas = [];
    paneles.forEach((p, c) => {
      const x0 = EJE_X + c * (anchoPanel + GAP_P);
      g.appendChild(el("text", { x: x0, y: 16, class: "et-serie" }, [txt(p.titulo)]));
      if (p.nota) g.appendChild(el("text", { x: x0, y: 31, class: "eje-txt" }, [txt(p.nota)]));
      g.appendChild(el("line", { x1: x0, y1: H_TOP - 8, x2: x0, y2: H - H_BOT + 2, class: "base-l" }));
      g.appendChild(el("line", { x1: x0 + anchoPanel, y1: H_TOP - 8, x2: x0 + anchoPanel, y2: H - H_BOT + 2, class: "reja-l" }));
      g.appendChild(el("text", { x: x0 + anchoPanel, y: H - H_BOT + 17, class: "eje-txt tab", "text-anchor": "end" }, [txt(fmt(max))]));

      p.datos.forEach((d, i) => {
        const y = H_TOP + i * ALTO_F;
        const w = (d.valor / max) * anchoPanel;
        const barra = el("rect", {
          x: x0, y: y + 4, width: Math.max(w, d.valor > 0 ? 2.5 : 0), height: 11, rx: 4,
          fill: p.color, class: "marca anim-barra", style: `transition-delay:${Math.min(c * 90 + i * 16, 520)}ms`,
        });
        g.appendChild(barra); marcas.push(barra);
        const hit = el("rect", { x: x0, y: y, width: anchoPanel, height: ALTO_F, class: "viz-hit", role: "img",
          "aria-label": `${d.etiqueta || d.id}, ${p.titulo}: ${fmt(d.valor)}` });
        conGlobo(hit, () => `<div class="g-tit">${d.etiqueta || d.id}</div>` +
          `<div class="g-fila"><span>${p.titulo}</span><b>${fmt(d.valor)}</b></div>` +
          (p.nota ? `<div class="g-nota">${p.nota}</div>` : ""), marcas);
        g.appendChild(hit);
      });
    });

    o.leyenda = o.leyenda || paneles.map((p) => ({ color: p.color, etiqueta: p.titulo }));
    const fig = figura(o);
    fig._lienzo.appendChild(svg);
    fig._tabla.appendChild(tabla(
      [{ t: o.nombreFila || "Medición" }].concat(paneles.map((p) => ({ t: p.titulo, n: true }))),
      paneles[0].datos.map((d, i) => [d.etiqueta || d.id].concat(paneles.map((p) => fmt(p.datos[i].valor))))
    ));
    return fig;
  }

  /* ── 4. escalera ordinal (magnitud ordenada → rampa de un solo tono) ───── */
  function escaleraOrdinal(o) {
    const pasos = o.pasos;                    // [{etiqueta, valor, sub, detalle}]
    const W = 760, H_FILA = 62, H_TOP = 30, H_BOT = 34;
    const EJE_X = o.anchoEtiqueta || 208, PAD_D = 96;
    const H = H_TOP + pasos.length * H_FILA + H_BOT;
    const max = o.max != null ? o.max : Math.max(...pasos.map((p) => p.valor));
    const anchoPlot = W - EJE_X - PAD_D;
    const fmt = o.formato || ((v) => dec(v, 1));

    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": o.titulo });
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
      g.appendChild(el("line", { x1: px, y1: H_TOP - 18, x2: px, y2: H - H_BOT + 4,
        class: "ref-l anim-fade", style: `stroke:${PAL.s2}` }));
      g.appendChild(el("text", { x: px, y: H_TOP - 23, class: "ref-t", style: `fill:${PAL.s2}`,
        "text-anchor": "middle" }, [txt(o.criticoEtiqueta || "nivel crítico")]));
    }

    const marcas = [];
    pasos.forEach((p, i) => {
      const y = H_TOP + i * H_FILA;
      const color = ORDINAL[Math.min(i, ORDINAL.length - 1)];
      g.appendChild(el("text", { x: EJE_X - 14, y: y + 24, class: "et-serie", "text-anchor": "end" }, [txt(p.etiqueta)]));
      if (p.sub) g.appendChild(el("text", { x: EJE_X - 14, y: y + 41, class: "eje-txt", "text-anchor": "end" }, [txt(p.sub)]));

      const w = (p.valor / max) * anchoPlot;
      const barra = el("rect", {
        x: EJE_X, y: y + 12, width: w, height: 22, rx: 4, fill: color,
        class: "marca anim-barra", style: `transition-delay:${i * 110}ms`,
      });
      g.appendChild(barra); marcas.push(barra);
      g.appendChild(el("text", { x: EJE_X + w + 11, y: y + 28, class: "et-val anim-fade", fill: PAL.tinta },
        [txt(fmt(p.valor))]));
      if (p.derecha) g.appendChild(el("text", { x: EJE_X + w + 11, y: y + 43, class: "eje-txt anim-fade" }, [txt(p.derecha)]));

      const hit = el("rect", { x: EJE_X, y: y, width: anchoPlot, height: H_FILA, class: "viz-hit", role: "img",
        "aria-label": `${p.etiqueta}: ${fmt(p.valor)}` });
      conGlobo(hit, () => `<div class="g-tit">${p.etiqueta}</div>` +
        `<div class="g-fila"><span>${o.nombreValor || "Valor"}</span><b>${fmt(p.valor)}</b></div>` +
        (p.detalle ? `<div class="g-nota">${p.detalle}</div>` : ""), marcas);
      g.appendChild(hit);
    });

    const fig = figura(o);
    fig._lienzo.appendChild(svg);
    fig._tabla.appendChild(tabla(
      [{ t: o.nombreFila || "Portador" }, { t: o.nombreValor || "Valor", n: true }, { t: "Detalle" }],
      pasos.map((p) => [p.etiqueta, fmt(p.valor), p.detalle || p.derecha || "—"])
    ));
    return fig;
  }

  /* ── 5. octógono (perfil de una medición sobre los 8 ejes) ─────────────── */
  function octogono(o) {
    const ejes = o.ejes;                      // [{clave, nombre}]
    // el lienzo es más ancho que el polígono a propósito: las etiquetas
    // radiales viven fuera del radio y el svg recorta lo que se sale
    const W = 560, H = 450, cx = W / 2, cy = H / 2 + 4, R = 142;
    const n = ejes.length;
    const ang = (i) => (i / n) * Math.PI * 2 - Math.PI / 2;
    const pt = (i, r) => [cx + Math.cos(ang(i)) * r * R, cy + Math.sin(ang(i)) * r * R];

    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": o.titulo });
    const g = el("g", {}); svg.appendChild(g);

    [0.25, 0.5, 0.75, 1].forEach((r) => {
      const pts = ejes.map((_, i) => pt(i, r).join(",")).join(" ");
      g.appendChild(el("polygon", { points: pts, fill: "none", class: "reja-l", stroke: r === 1 ? PAL.base : PAL.reja }));
    });
    ejes.forEach((e, i) => {
      const [x2, y2] = pt(i, 1);
      g.appendChild(el("line", { x1: cx, y1: cy, x2, y2, class: "reja-l" }));
      const [lx, ly] = pt(i, 1.14);
      const anc = Math.abs(lx - cx) < 10 ? "middle" : lx > cx ? "start" : "end";
      const dx = Math.abs(lx - cx) < 10 ? 0 : lx > cx ? 7 : -7;
      g.appendChild(el("text", { x: lx + dx, y: ly + 4, class: "et-serie", "text-anchor": anc }, [txt(e.nombre)]));
    });
    // escala radial sobre el eje vertical, retirada a la izquierda del radio
    [0.5, 1].forEach((r) => {
      g.appendChild(el("text", { x: cx - 8, y: cy - r * R + 4, class: "eje-txt tab", "text-anchor": "end" },
        [txt(pc(r))]));
    });

    const capa = el("g", { class: "capa-perfil" });
    g.appendChild(capa);

    function pinta(series) {
      capa.textContent = "";
      series.forEach((s, si) => {
        const pts = ejes.map((e, i) => pt(i, Math.max(0, Math.min(1, s.valores[e.clave] || 0))).join(",")).join(" ");
        capa.appendChild(el("polygon", {
          points: pts, fill: s.color, "fill-opacity": series.length > 1 ? 0.13 : 0.18,
          stroke: s.color, "stroke-width": 2, "stroke-linejoin": "round", class: "anim-fade",
        }));
        ejes.forEach((e, i) => {
          const v = Math.max(0, Math.min(1, s.valores[e.clave] || 0));
          const [px, py] = pt(i, v);
          const punto = el("circle", { cx: px, cy: py, r: 4.5, fill: s.color, stroke: PAL.sup, "stroke-width": 2, class: "anim-fade" });
          conGlobo(punto, () => `<div class="g-tit">${e.nombre}</div>` +
            `<div class="g-fila"><span>${s.nombre}</span><b>${pc(s.valores[e.clave])}</b></div>` +
            (s.ic && s.ic[e.clave] ? `<div class="g-fila"><span>IC 95 %</span><b>${rangoIC(s.ic[e.clave])}</b></div>` : ""));
          capa.appendChild(punto);
        });
      });
    }

    const fig = figura(o);
    fig._lienzo.appendChild(svg);
    fig._pinta = pinta;
    fig._tablaEjes = (series) => {
      fig._tabla.textContent = "";
      fig._tabla.appendChild(tabla(
        [{ t: "Eje" }].concat(series.map((s) => ({ t: s.nombre, n: true }))),
        ejes.map((e) => [e.nombre].concat(series.map((s) => pc(s.valores[e.clave]))))
      ));
    };
    return fig;
  }

  /* ── 6. matriz de correlaciones (divergente frío↔cálido, gris al centro) ─ */
  function matrizCorr(o) {
    const claves = o.claves, nombres = o.nombres;
    const N = claves.length, CELDA = 44, EJE = 118, TOP = 92;
    const W = EJE + N * CELDA + 16, H = TOP + N * CELDA + 14;

    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": o.titulo });
    const g = el("g", {}); svg.appendChild(g);

    // rampa divergente: azul (negativa) ↔ gris ↔ rojo (positiva)
    const color = (r) => {
      const a = Math.min(1, Math.abs(r));
      const [cr, cg, cb] = r >= 0 ? [217, 86, 78] : [57, 135, 229];
      const [gr, gg, gb] = [56, 56, 53];
      const mez = (c, gv) => Math.round(gv + (c - gv) * a);
      return `rgb(${mez(cr, gr)},${mez(cg, gg)},${mez(cb, gb)})`;
    };

    claves.forEach((c, i) => {
      g.appendChild(el("text", { x: EJE - 10, y: TOP + i * CELDA + CELDA / 2 + 4, class: "eje-txt", "text-anchor": "end" },
        [txt(nombres[i])]));
      const px = EJE + i * CELDA + CELDA / 2;
      g.appendChild(el("text", {
        x: px, y: TOP - 12, class: "eje-txt", "text-anchor": "start",
        transform: `rotate(-52 ${px} ${TOP - 12})`,
      }, [txt(nombres[i])]));
    });

    claves.forEach((cf, i) => claves.forEach((cc, j) => {
      const r = o.datos[cf][cc];
      const x = EJE + j * CELDA, y = TOP + i * CELDA;
      const celda = el("rect", {
        x: x + 1, y: y + 1, width: CELDA - 2, height: CELDA - 2, rx: 3,
        fill: i === j ? PAL.sup3 : color(r), class: "marca anim-fade",
        style: `transition-delay:${Math.min((i + j) * 22, 420)}ms`,
      });
      g.appendChild(celda);
      if (i !== j) {
        g.appendChild(el("text", {
          x: x + CELDA / 2, y: y + CELDA / 2 + 4, class: "eje-txt tab", "text-anchor": "middle",
          fill: Math.abs(r) > 0.45 ? "#0B0C0E" : PAL.tinta2,
        }, [txt(dec(r, 2))]));
      }
      const hit = el("rect", { x, y, width: CELDA, height: CELDA, class: "viz-hit", role: "img",
        "aria-label": `${nombres[i]} con ${nombres[j]}: r ${dec(r, 2)}` });
      conGlobo(hit, () => `<div class="g-tit">${nombres[i]} · ${nombres[j]}</div>` +
        `<div class="g-fila"><span>r de Pearson</span><b>${dec(r, 2)}</b></div>` +
        `<div class="g-nota">Sobre las ${o.n} mediciones del banco.</div>`);
      g.appendChild(hit);
    }));

    o.leyenda = [
      { color: "rgb(57,135,229)", etiqueta: "r = −1 (se mueven al revés)" },
      { color: "rgb(56,56,53)", etiqueta: "r = 0 (independientes)" },
      { color: "rgb(217,86,78)", etiqueta: "r = +1 (se mueven juntos)" },
    ];
    const fig = figura(o);
    fig._lienzo.appendChild(svg);
    fig._tabla.appendChild(tabla(
      [{ t: "" }].concat(nombres.map((n) => ({ t: n, n: true }))),
      claves.map((cf, i) => [nombres[i]].concat(claves.map((cc) => dec(o.datos[cf][cc], 2))))
    ));
    return fig;
  }

  /* ── 7. cotas de identidad (ordinal + banda de ruido) ──────────────────── */
  function cotas(o) {
    const datos = o.datos;                    // [{titulo, d, ic, lectura, fuente}]
    const W = 760, H_FILA = 84, H_TOP = 46, H_BOT = 34;
    const EJE_X = 274, PAD_D = 86;
    const H = H_TOP + datos.length * H_FILA + H_BOT;
    const max = o.max || 26;
    const anchoPlot = W - EJE_X - PAD_D;
    const x = (v) => (v / max) * anchoPlot;

    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": o.titulo });
    const g = el("g", {}); svg.appendChild(g);

    // banda de ruido intra-snapshot
    g.appendChild(el("rect", {
      x: EJE_X, y: H_TOP - 16, width: x(o.sueloMax), height: H - H_TOP - H_BOT + 22,
      fill: "rgba(199,184,164,.08)", class: "anim-fade",
    }));
    g.appendChild(el("line", { x1: EJE_X + x(o.suelo), y1: H_TOP - 16, x2: EJE_X + x(o.suelo), y2: H - H_BOT + 6, class: "ref-l anim-fade" }));
    g.appendChild(el("text", { x: EJE_X + x(o.sueloMax) + 8, y: H_TOP - 22, class: "ref-t" },
      [txt(`ruido del propio instrumento · suelo ${dec(o.suelo)}, máx ${dec(o.sueloMax)}`)]));

    [0, 5, 10, 15, 20, 25].forEach((t) => {
      const px = EJE_X + x(t);
      g.appendChild(el("line", { x1: px, y1: H_TOP - 16, x2: px, y2: H - H_BOT + 6, class: "reja-l" }));
      g.appendChild(el("text", { x: px, y: H - H_BOT + 21, class: "eje-txt tab", "text-anchor": "middle" }, [txt(String(t))]));
    });
    g.appendChild(el("line", { x1: EJE_X, y1: H_TOP - 16, x2: EJE_X, y2: H - H_BOT + 6, class: "base-l" }));

    const marcas = [];
    datos.forEach((d, i) => {
      const y = H_TOP + i * H_FILA;
      const color = ORDINAL[Math.min(i + 1, ORDINAL.length - 1)];
      wrap(g, d.titulo, EJE_X - 16, y + 22, 26, "end", 2, "et-serie");

      const w = x(d.d);
      const barra = el("rect", {
        x: EJE_X, y: y + 8, width: w, height: 20, rx: 4, fill: color,
        class: "marca anim-barra", style: `transition-delay:${i * 140}ms`,
      });
      g.appendChild(barra); marcas.push(barra);
      if (d.ic) {
        g.appendChild(el("line", {
          x1: EJE_X + x(d.ic[0]), x2: EJE_X + x(d.ic[1]), y1: y + 40, y2: y + 40,
          class: "ic-l anim-fade",
        }));
        g.appendChild(el("text", { x: EJE_X + x(d.ic[1]) + 8, y: y + 44, class: "eje-txt tab" },
          [txt(`IC ${dec(d.ic[0])}–${dec(d.ic[1])}`)]));
      }
      g.appendChild(el("text", { x: EJE_X + w + 12, y: y + 24, class: "et-val anim-fade",
        style: `font-size:18px;fill:${PAL.tinta}` }, [txt(dec(d.d))]));

      const hit = el("rect", { x: EJE_X, y: y, width: anchoPlot, height: H_FILA - 8, class: "viz-hit", role: "img",
        "aria-label": `${d.titulo}: distancia de perfil ${dec(d.d)}` });
      conGlobo(hit, () => `<div class="g-tit">${d.titulo}</div>` +
        `<div class="g-fila"><span>d(A,B)</span><b>${dec(d.d)}</b></div>` +
        (d.ic ? `<div class="g-fila"><span>IC 95 %</span><b>${dec(d.ic[0])}–${dec(d.ic[1])}</b></div>` : "") +
        `<div class="g-nota">${d.lectura}</div>`, marcas);
      g.appendChild(hit);
    });

    const fig = figura(o);
    fig._lienzo.appendChild(svg);
    fig._tabla.appendChild(tabla(
      [{ t: "Qué se fija" }, { t: "d(A,B)", n: true }, { t: "IC 95 %", n: true }, { t: "Lectura" }],
      datos.map((d) => [d.titulo, dec(d.d), d.ic ? `${dec(d.ic[0])}–${dec(d.ic[1])}` : "—", d.lectura])
    ));
    return fig;
  }

  /* ── 8. columnas por estrato (dos brazos por medición) ─────────────────── */
  function columnasEstrato(o) {
    const datos = o.datos;                    // [{id, a, b}]
    const W = 760, H = 300, PAD_I = 44, PAD_D = 10, TOP = 22, BOT = 74;
    const anchoPlot = W - PAD_I - PAD_D;
    const paso = anchoPlot / datos.length;
    const anchoBarra = Math.min(15, paso / 2.6);
    const y = (v) => TOP + (1 - v) * (H - TOP - BOT);

    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": o.titulo });
    const g = el("g", {}); svg.appendChild(g);

    [0, 0.25, 0.5, 0.75, 1].forEach((t) => {
      g.appendChild(el("line", { x1: PAD_I, y1: y(t), x2: W - PAD_D, y2: y(t), class: "reja-l" }));
      g.appendChild(el("text", { x: PAD_I - 9, y: y(t) + 4, class: "eje-txt tab", "text-anchor": "end" }, [txt(pc(t))]));
    });
    g.appendChild(el("line", { x1: PAD_I, y1: y(0), x2: W - PAD_D, y2: y(0), class: "base-l" }));

    const marcas = [];
    datos.forEach((d, i) => {
      const cx = PAD_I + paso * (i + 0.5);
      [[d.a, o.colorA || PAL.s2, -1, o.etA], [d.b, o.colorB || PAL.s3, 1, o.etB]].forEach(([v, col, lado, et]) => {
        const alto = Math.max((H - TOP - BOT) * v, v > 0 ? 2.5 : 0);
        // 2 px de hueco entre las dos barras del par
        const bx = cx + (lado < 0 ? -anchoBarra - 1 : 1);
        const barra = el("rect", {
          x: bx, y: y(0) - alto, width: anchoBarra, height: alto, rx: 4, fill: col,
          class: "marca anim-col", style: `transition-delay:${Math.min(i * 26, 420)}ms`,
        });
        g.appendChild(barra); marcas.push(barra);
      });
      const et = el("text", {
        x: cx, y: y(0) + 12, class: "eje-txt", "text-anchor": "end",
        transform: `rotate(-42 ${cx} ${y(0) + 12})`,
      }, [txt(d.etiqueta || d.id)]);
      g.appendChild(et);
      const hit = el("rect", { x: cx - paso / 2, y: TOP, width: paso, height: H - TOP - BOT + 6, class: "viz-hit",
        role: "img", "aria-label": `${d.etiqueta || d.id}: ${o.etA} ${pc(d.a)}, ${o.etB} ${pc(d.b)}` });
      conGlobo(hit, () => `<div class="g-tit">${d.etiqueta || d.id}</div>` +
        `<div class="g-fila"><span>${o.etA}</span><b>${pc(d.a)}</b></div>` +
        `<div class="g-fila"><span>${o.etB}</span><b>${pc(d.b)}</b></div>`, marcas);
      g.appendChild(hit);
    });

    o.leyenda = o.leyenda || [{ color: o.colorA || PAL.s2, etiqueta: o.etA }, { color: o.colorB || PAL.s3, etiqueta: o.etB }];
    const fig = figura(o);
    fig._lienzo.appendChild(svg);
    fig._tabla.appendChild(tabla(
      [{ t: "Medición" }, { t: o.etA, n: true }, { t: o.etB, n: true }],
      datos.map((d) => [d.etiqueta || d.id, pc(d.a), pc(d.b)])
    ));
    return fig;
  }

  /* corta un texto en varias líneas svg */
  function wrap(g, texto, x, y, maxCar, anclaje, maxLineas, clase) {
    if (!texto) return;
    const palabras = String(texto).split(" ");
    const lineas = []; let actual = "";
    palabras.forEach((p) => {
      if ((actual + " " + p).trim().length > maxCar) { lineas.push(actual.trim()); actual = p; }
      else actual += " " + p;
    });
    if (actual.trim()) lineas.push(actual.trim());
    const tope = maxLineas || 4;
    if (lineas.length > tope) lineas[tope - 1] = lineas[tope - 1].replace(/\s*\S*$/, "…");
    lineas.slice(0, tope).forEach((l, i) => {
      g.appendChild(el("text", { x, y: y + i * 16, class: clase || "eje-txt", "text-anchor": anclaje || "start" }, [txt(l)]));
    });
  }

  global.G = { PAL, ORDINAL, barrasH, mancuernas, multiplos, escaleraOrdinal, octogono,
    matrizCorr, cotas, columnasEstrato, figura, tabla, navegable, h, el, pc, dec, rangoIC };
})(window);
