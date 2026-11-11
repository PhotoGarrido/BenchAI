/* ===========================================================================
   BenchAI · Personalidad, los datos (/personalidad/datos)
   ---------------------------------------------------------------------------
   El explorador del test de personalidad. Las fichas (/personalidad) cuentan
   cada modelo; esta página sirve para buscar: mapa de rasgos, clasificación
   por rasgo con su intervalo, comparador, huellas, familias, situaciones
   reales, ranking a medida, la relación con el ISS, la validez y la tabla.

   Un solo selector de modelos manda sobre todas las gráficas, y el estado
   (modelos, rasgo, pareja, pesos…) vive en la URL: cualquier vista se puede
   enlazar. Todo sale de `PSICO.personalidad`; nada se escribe a mano.
   =========================================================================== */
(() => {
  "use strict";
  const D = window.PSICO;
  if (!D || !D.personalidad) return;
  const P = D.personalidad;
  const { mk, une, pintar } = window.MARCADO;
  const { h, el, conGlobo, navegable, adaptable, anchoMax, anchoTexto } = G;
  const T = (s) => document.createTextNode(s);
  const ES = new Intl.NumberFormat("es-ES");
  const dec = (v, n = 1) => (v == null ? "—" : new Intl.NumberFormat("es-ES", { minimumFractionDigits: n, maximumFractionDigits: n }).format(v));
  // «+3», «−6» y nunca «−0»: el signo se decide sobre la cifra ya redondeada
  const firmado = (v, n = 1) => {
    const r = Number(Math.abs(v).toFixed(n));
    return (r === 0 ? "" : v > 0 ? "+" : "−") + dec(r, n);
  };

  const RASGOS = P.rasgos;
  // el tono de cada rasgo, el mismo que en /personalidad (verloop/personalidad.js)
  const TONO_R = { O: "#FF7AD9", C: "#6FA8FF", E: "#FFC24D", A: "#7CF0B8", N: "#FF6B6B", H: "#C9A8FF" };
  const R = Object.fromEntries(RASGOS.map((r) => [r.clave, r]));
  const MODELOS = P.modelos;
  const POR_ID = new Map(MODELOS.map((m) => [m.id, m]));

  document.getElementById("v-edicion").textContent = `Cuadro ${P.banco || ""} · ${P.fecha}`.replace("  ", " ");
  document.querySelectorAll("[data-cifra]").forEach((n) => {
    const v = n.dataset.cifra.split(".").reduce((o, k) => (o == null ? o : o[k]), D);
    n.textContent = v == null ? "—" : ES.format(v);
  });

  /* ── rutas a las otras páginas (local: fichero; publicada: ruta limpia) ── */
  const publicada = !!document.querySelector('.superficies a[href="/social"]');
  const RUTA = { "psicobench.html": "/social", "personalidad.html": "/personalidad" };
  const enlace = (f, hash = "") => (publicada ? RUTA[f] : f) + hash;

  /* ── estadística del panel (siempre sobre el panel entero, para que una
     selección no cambie las escalas ni el significado de una σ) ─────────── */
  const media = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
  const sd = (xs) => { const m = media(xs); return Math.sqrt(media(xs.map((x) => (x - m) ** 2))); };
  const EST = Object.fromEntries(RASGOS.map((r) => {
    const ps = MODELOS.map((m) => m.rasgos[r.clave].p);
    return [r.clave, { media: media(ps), sd: sd(ps) }];
  }));
  const z = (m, t) => (m.rasgos[t].p - EST[t].media) / EST[t].sd;
  const MAXDIF = Math.max(...MODELOS.flatMap((m) => RASGOS.map((r) => Math.abs(m.rasgos[r.clave].dif))));
  const marcas = (m) => RASGOS.filter((r) => m.rasgos[r.clave].marca).length;

  /* ══ estado, en la URL ══════════════════════════════════════════════════ */
  const Q = new URLSearchParams(location.search);
  const estado = {
    sel: new Set((Q.get("m") || "").split(",").filter(Boolean).map(decodeURIComponent).filter((id) => POR_ID.has(id))),
    rasgo: R[Q.get("r")] ? Q.get("r") : "H",
    vista: ["dif", "p", "pct"].includes(Q.get("v")) ? Q.get("v") : "dif",
    orden: { k: Q.get("o") || "lab", dir: Q.get("d") === "asc" ? 1 : -1 },
    a: POR_ID.has(Q.get("a")) ? Q.get("a") : null,
    b: POR_ID.has(Q.get("b")) ? Q.get("b") : null,
    pesos: Object.fromEntries(RASGOS.map((r) => [r.clave, 0])),
    issRasgo: R[Q.get("x")] ? Q.get("x") : "C",
    ejRasgo: R[Q.get("e")] ? Q.get("e") : "",
  };
  if (!estado.sel.size) MODELOS.forEach((m) => estado.sel.add(m.id));
  (Q.get("w") || "").split(",").forEach((par) => {
    const t = par[0], v = Number(par.slice(1));
    if (R[t] && Number.isInteger(v) && Math.abs(v) <= 2) estado.pesos[t] = v;
  });
  // la pareja de entrada: los dos modelos más distintos del panel
  if (!estado.a || !estado.b) {
    let mejor = [MODELOS[0], MODELOS[1]], dmax = -1;
    MODELOS.forEach((x, i) => MODELOS.slice(i + 1).forEach((y) => {
      const d = RASGOS.reduce((s, r) => s + (z(x, r.clave) - z(y, r.clave)) ** 2, 0);
      if (d > dmax) { dmax = d; mejor = [x, y]; }
    }));
    estado.a = estado.a || mejor[0].id;
    estado.b = estado.b || mejor[1].id;
  }

  function guardarURL() {
    const q = new URLSearchParams();
    if (estado.sel.size !== MODELOS.length) q.set("m", Array.from(estado.sel).map(encodeURIComponent).join(","));
    if (estado.rasgo !== "H") q.set("r", estado.rasgo);
    if (estado.vista !== "dif") q.set("v", estado.vista);
    if (estado.orden.k !== "lab") { q.set("o", estado.orden.k); q.set("d", estado.orden.dir > 0 ? "asc" : "desc"); }
    q.set("a", estado.a); q.set("b", estado.b);
    const w = RASGOS.filter((r) => estado.pesos[r.clave]).map((r) => r.clave + estado.pesos[r.clave]).join(",");
    if (w) q.set("w", w);
    if (estado.issRasgo !== "C") q.set("x", estado.issRasgo);
    if (estado.ejRasgo) q.set("e", estado.ejRasgo);
    history.replaceState(null, "", location.pathname + "?" + q.toString() + location.hash);
  }

  const seleccion = () => MODELOS.filter((m) => estado.sel.has(m.id));
  const pintores = [];
  const repintar = () => { guardarURL(); pintores.forEach((f) => f()); };

  /* ══ utilidades de figura: enlace, CSV y pestañas ═══════════════════════ */
  const csvTexto = (cab, filas) => {
    const q = (v) => (v == null ? "" : /[",\n]/.test(String(v)) ? '"' + String(v).replace(/"/g, '""') + '"' : String(v));
    return "﻿" + [cab].concat(filas).map((f) => f.map(q).join(",")).join("\n");
  };
  function descargar(nombre, texto) {
    const url = URL.createObjectURL(new Blob([texto], { type: "text/csv;charset=utf-8" }));
    const a = h("a", { href: url, download: nombre });
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  }
  function utiles(ancla, csv) {
    const enl = h("button", { type: "button", class: "chip", title: "Copia un enlace a esta gráfica, tal como la ves", text: "Enlace" });
    enl.addEventListener("click", async () => {
      guardarURL();
      const url = location.href.split("#")[0] + "#" + ancla;
      try { await navigator.clipboard.writeText(url); enl.textContent = "Copiado ✓"; }
      catch { history.replaceState(null, "", url); enl.textContent = "En la barra ✓"; }
      setTimeout(() => (enl.textContent = "Enlace"), 1600);
    });
    const out = [enl];
    if (csv) {
      const b = h("button", { type: "button", class: "chip", title: "Los datos de esta gráfica (coma, punto decimal, UTF-8)", text: "CSV" });
      b.addEventListener("click", () => { const [nombre, cab, filas] = csv(); descargar(nombre, csvTexto(cab, filas)); });
      out.push(b);
    }
    return out;
  }
  function pestanas(opciones, actual, alElegir, etiqueta) {
    const caja = h("div", { class: "pestanas-d", role: "group", "aria-label": etiqueta });
    opciones.forEach(([k, t]) => {
      const b = h("button", { type: "button", class: "chip", "aria-pressed": String(k === actual()), text: t });
      b.addEventListener("click", () => {
        alElegir(k);
        caja.querySelectorAll("button").forEach((x, i) => x.setAttribute("aria-pressed", String(opciones[i][0] === actual())));
      });
      caja.appendChild(b);
    });
    return caja;
  }
  const opcionesRasgo = RASGOS.map((r) => [r.clave, r.nombre]);
  const nombreRasgo = (t) => R[t].nombre;
  const polo = (t, v) => (v >= 0 ? R[t].alto : R[t].bajo);

  /* ══ el selector global de modelos ══════════════════════════════════════ */
  (function selectorGlobal() {
    const host = document.getElementById("selector-global");
    const boton = h("button", { type: "button", class: "chip sg-boton", "aria-expanded": "false", "aria-controls": "sg-panel" });
    const panel = h("div", { class: "sg-panel", id: "sg-panel", hidden: "" });
    const acciones = h("div", { class: "sg-acciones" });
    const todos = h("button", { type: "button", class: "chip", text: "Todos" });
    const ninguno = h("button", { type: "button", class: "chip", text: "Ninguno" });
    acciones.append(todos, ninguno, h("span", { class: "sg-sep", text: "Por laboratorio:" }));
    const cajas = new Map();
    const lista = h("div", { class: "sg-lista" });
    P.labs.forEach((lab) => {
      const ms = MODELOS.filter((m) => m.lab === lab);
      const chipLab = h("button", { type: "button", class: "chip", text: `${lab} (${ms.length})` });
      chipLab.addEventListener("click", () => {
        const todosDentro = ms.every((m) => estado.sel.has(m.id));
        ms.forEach((m) => (todosDentro ? estado.sel.delete(m.id) : estado.sel.add(m.id)));
        sincroniza(); repintar();
      });
      acciones.appendChild(chipLab);
      const grupo = h("fieldset", { class: "sg-grupo" }, [h("legend", { text: lab })]);
      ms.forEach((m) => {
        const c = h("input", { type: "checkbox", value: m.id });
        c.addEventListener("change", () => { c.checked ? estado.sel.add(m.id) : estado.sel.delete(m.id); sincroniza(); repintar(); });
        cajas.set(m.id, c);
        grupo.appendChild(h("label", {}, [c, T(" " + m.etiqueta)]));
      });
      lista.appendChild(grupo);
    });
    todos.addEventListener("click", () => { MODELOS.forEach((m) => estado.sel.add(m.id)); sincroniza(); repintar(); });
    ninguno.addEventListener("click", () => { estado.sel.clear(); sincroniza(); repintar(); });
    panel.append(acciones, lista);
    function sincroniza() {
      cajas.forEach((c, id) => (c.checked = estado.sel.has(id)));
      boton.textContent = `Modelos: ${estado.sel.size} de ${MODELOS.length} ▾`;
    }
    boton.addEventListener("click", () => {
      const abre = panel.hasAttribute("hidden");
      abre ? panel.removeAttribute("hidden") : panel.setAttribute("hidden", "");
      boton.setAttribute("aria-expanded", String(abre));
    });
    host.append(h("div", { class: "sg-fila" }, [boton,
      h("span", { class: "sg-nota", text: "La selección manda sobre todas las gráficas de la página y queda en el enlace." })]), panel);
    sincroniza();
  })();

  const vacio = (host, texto = "Elige al menos un modelo en el selector de arriba.") =>
    host.replaceChildren(h("p", { class: "nota sin-datos", text: texto }));

  /* ══ 01 · mapa de rasgos (tabla de calor) ═══════════════════════════════ */
  (function mapa() {
    const host = document.getElementById("mapa-host");
    const fig = G.figura({
      titulo: "Los seis rasgos, modelo a modelo", sinTabla: true,
      sub: "▲ ▼ diferencia firme · el color es la distancia a la media de los demás",
      controles: [pestanas([["dif", "Diferencia"], ["p", "Puntuación"], ["pct", "Percentil"]], () => estado.vista,
        (k) => { estado.vista = k; repintar(); }, "Qué cifra enseña cada celda"),
      ...utiles("mapa", () => ["personalidad_mapa.csv", ["modelo", "etiqueta", "lab", ...RASGOS.flatMap((r) => [r.clave, r.clave + "_dif", r.clave + "_marca"])],
        seleccion().map((m) => [m.id, m.etiqueta, m.lab, ...RASGOS.flatMap((r) => [m.rasgos[r.clave].p, m.rasgos[r.clave].dif, m.rasgos[r.clave].marca])])])],
      fuente: mk`Personalidad ${P.banco || ""} · ${P.fuente}`,
      pie: mk`<b>Diferencia</b>: puntos frente a la media de los demás modelos. <b>Puntuación</b>: de 0 a 100, con qué frecuencia elige el polo alto. <b>Percentil</b>: su lugar entre los modelos seleccionados (100 = el que más).`,
    });
    host.appendChild(fig);
    const color = (v) => {
      const k = Math.min(1, Math.abs(v)) * 72;
      return `color-mix(in srgb, var(${v >= 0 ? "--pd-sube" : "--pd-baja"}) ${k.toFixed(0)}%, transparent)`;
    };
    function pinta() {
      const ms = seleccion();
      if (!ms.length) { fig._lienzo.replaceChildren(h("p", { class: "nota sin-datos", text: "Elige al menos un modelo." })); return; }
      const pct = {};
      RASGOS.forEach((r) => {
        const orden = ms.slice().sort((a, b) => a.rasgos[r.clave].p - b.rasgos[r.clave].p);
        orden.forEach((m, i) => { (pct[m.id] = pct[m.id] || {})[r.clave] = ms.length > 1 ? (i / (ms.length - 1)) * 100 : 50; });
      });
      const valor = (m, t) => (estado.vista === "dif" ? m.rasgos[t].dif : estado.vista === "p" ? m.rasgos[t].p : pct[m.id][t]);
      const llave = (m) => (estado.orden.k === "lab" ? m.lab + "|" + m.etiqueta : estado.orden.k === "nombre" ? m.etiqueta
        : estado.orden.k === "firmes" ? marcas(m) : valor(m, estado.orden.k));
      const filas = ms.slice().sort((a, b) => {
        const x = llave(a), y = llave(b);
        const c = typeof x === "string" ? x.localeCompare(y, "es") : x - y;
        return (estado.orden.k === "lab" || estado.orden.k === "nombre" ? 1 : estado.orden.dir) * c;
      });
      const cab = (k, t, clase = "") => {
        const activo = estado.orden.k === k;
        const flecha = activo && k !== "lab" && k !== "nombre" ? (estado.orden.dir > 0 ? " ↑" : " ↓") : "";
        // los rasgos, con su nombre a lo ancho y su letra en estrecho
        const b = h("button", { type: "button", class: "orden-cab", title: R[k] ? "Ordenar por " + R[k].nombre : "Ordenar" },
          R[k] ? [h("span", { class: "largo", text: t + flecha }), h("span", { class: "corto", text: k + flecha })] : [T(t + flecha)]);
        b.addEventListener("click", () => {
          estado.orden = { k, dir: activo ? -estado.orden.dir : -1 };
          repintar();
        });
        return h("th", { scope: "col", class: clase, style: R[k] ? `--c:${TONO_R[k]}` : null, "aria-sort": activo ? (estado.orden.dir > 0 ? "ascending" : "descending") : "none" }, [b]);
      };
      const t = h("table", { class: "datos mapa-p" });
      t.appendChild(h("thead", {}, [h("tr", {}, [cab("nombre", "Modelo"), cab("lab", "Lab"),
        ...RASGOS.map((r) => cab(r.clave, r.nombre, "n")), cab("firmes", "Firmes", "n")])]));
      const tb = h("tbody");
      filas.forEach((m) => {
        const tr = h("tr", { class: "fila-m", tabindex: "0", title: "Llevar al comparador" }, [
          h("th", { scope: "row", class: "mod" }, [h("span", { text: m.etiqueta }),
            m.validez === "aviso" ? h("span", { class: "aviso-v", title: m.aviso, text: " ⚠" }) : T("")]),
          h("td", { class: "lab", text: m.lab })]);
        RASGOS.forEach((r) => {
          const x = m.rasgos[r.clave], v = valor(m, r.clave);
          const txt = estado.vista === "dif" ? firmado(v, 0) : dec(v, 0);
          const intens = estado.vista === "dif" ? x.dif / MAXDIF : estado.vista === "p" ? (x.p - EST[r.clave].media) / (3 * EST[r.clave].sd) : (v - 50) / 50;
          tr.appendChild(h("td", {
            class: "n celda" + (x.marca ? " firme" : ""), style: `background:${color(intens)}`,
            title: `${r.nombre}: ${dec(x.p, 0)} [${dec(x.ic[0], 0)}–${dec(x.ic[1], 0)}] · ${firmado(x.dif)} frente a la media de los demás [${firmado(x.difIC[0])}; ${firmado(x.difIC[1])}]${x.marca ? " · diferencia firme" : ""}`,
          }, [T(txt), x.marca ? h("span", { class: "mk", text: " " + x.marca }) : T("")]));
        });
        tr.appendChild(h("td", { class: "n", text: String(marcas(m)) }));
        const ir = () => { estado.a = m.id; repintar(); document.getElementById("comparar").scrollIntoView({ behavior: "smooth" }); };
        tr.addEventListener("click", ir);
        tr.addEventListener("keydown", (ev) => { if (ev.key === "Enter") ir(); });
        tb.appendChild(tr);
      });
      t.appendChild(tb);
      fig._lienzo.replaceChildren(h("div", { class: "tabla-envuelta mapa-envuelta" }, [t]));
    }
    pintores.push(pinta);
  })();

  /* ══ 02 · clasificación por rasgo (puntos con intervalo) ════════════════ */
  (function porRasgo() {
    const host = document.getElementById("rasgo-host");
    const fig = G.figura({
      titulo: "Puntuación por rasgo, con su intervalo al 95 %",
      sub: " ",
      controles: [pestanas(opcionesRasgo, () => estado.rasgo, (k) => { estado.rasgo = k; repintar(); }, "Rasgo"),
        ...utiles("rasgo", () => [`personalidad_${estado.rasgo}.csv`, ["modelo", "etiqueta", "lab", "puntuacion", "ic_bajo", "ic_alto", "dif", "marca"],
          seleccion().map((m) => { const x = m.rasgos[estado.rasgo]; return [m.id, m.etiqueta, m.lab, x.p, x.ic[0], x.ic[1], x.dif, x.marca]; })])],
      fuente: mk`Personalidad ${P.banco || ""} · ${P.fuente}`,
    });
    host.appendChild(fig);
    const sub = fig.querySelector(".subviz");
    function dibujar(W) {
      const t = estado.rasgo, ms = seleccion().slice().sort((a, b) => b.rasgos[t].p - a.rasgos[t].p);
      const svg = el("svg", { viewBox: `0 0 ${W} 40`, width: W, role: "img", style: `--c:${TONO_R[t]}` });
      if (!ms.length) return svg;
      const etiquetas = ms.map((m) => m.etiqueta);
      const encima = W < 560;
      const x0 = encima ? 4 : Math.ceil(anchoMax(etiquetas, "eje")) + 18, x1 = W - 34;
      const fila = encima ? 34 : 24, top = 30, H = top + ms.length * fila + 8;
      const lo = Math.floor((Math.min(...ms.map((m) => m.rasgos[t].ic[0])) - 2) / 5) * 5;
      const hi = Math.ceil((Math.max(...ms.map((m) => m.rasgos[t].ic[1])) + 2) / 5) * 5;
      const X = (v) => x0 + ((v - lo) / (hi - lo)) * (x1 - x0);
      svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
      svg.setAttribute("aria-label", `${R[t].nombre}: ${ms.length} modelos ordenados de más a menos, con su intervalo de confianza`);
      for (let v = lo; v <= hi; v += (hi - lo > 40 ? 10 : 5)) {
        svg.appendChild(el("line", { x1: X(v), x2: X(v), y1: top - 6, y2: H - 6, class: "reja-v" }));
        svg.appendChild(el("text", { x: X(v), y: top - 12, class: "eje-txt", "text-anchor": "middle" }, [T(String(v))]));
      }
      const mu = EST[t].media;
      svg.appendChild(el("line", { x1: X(mu), x2: X(mu), y1: top - 6, y2: H - 6, class: "linea-media" }));
      svg.appendChild(el("text", { x: X(mu) + 4, y: H - 2, class: "eje-txt" }, [T("media " + dec(mu, 0))]));
      const marcasSvg = [];
      ms.forEach((m, i) => {
        const x = m.rasgos[t], y = top + i * fila + (encima ? 22 : 12);
        const g = el("g", { class: "marca fila-r" + (x.marca ? " firme" : "") });
        g.appendChild(el("rect", { x: 0, y: y - (encima ? 20 : 11), width: W, height: fila, class: "fondo-fila" }));
        g.appendChild(el("text", encima ? { x: x0, y: y - 9, class: "eje-txt et-fila" } : { x: x0 - 12, y: y + 4, class: "eje-txt et-fila", "text-anchor": "end" }, [T(m.etiqueta)]));
        g.appendChild(el("line", { x1: X(x.ic[0]), x2: X(x.ic[1]), y1: y, y2: y, class: "bigote" }));
        g.appendChild(el("circle", { cx: X(x.p), cy: y, r: 5, class: "punto-r" }));
        if (x.marca) g.appendChild(el("text", { x: Math.min(X(x.ic[1]) + 8, W - 14), y: y + 4, class: "marca-txt" }, [T(x.marca)]));
        conGlobo(g, () => mk`<div class="g-tit">${m.etiqueta} · ${R[t].nombre}</div>
          <div class="g-fila"><span>Puntuación</span><b>${dec(x.p, 1)}</b></div>
          <div class="g-fila"><span>Intervalo 95 %</span><b>${dec(x.ic[0], 1)} – ${dec(x.ic[1], 1)}</b></div>
          <div class="g-fila"><span>Frente a los demás</span><b>${firmado(x.dif)}</b></div>
          <div class="g-nota">${x.marca ? (x.marca === "▲" ? "Diferencia firme: más que los demás · " + R[t].alto : "Diferencia firme: menos que los demás · " + R[t].bajo) : "Sin diferencia firme con los demás"}</div>`, marcasSvg);
        marcasSvg.push(g);
        svg.appendChild(g);
      });
      return svg;
    }
    adaptable(fig, dibujar);
    fig._nav = "Clasificación por rasgo: flechas para recorrer los modelos";
    function pinta() {
      const t = estado.rasgo;
      sub.textContent = `${R[t].nombre}: más alto = ${R[t].alto}; más bajo = ${R[t].bajo}.`;
      if (fig._redibujar) fig._redibujar();
      fig._tabla.replaceChildren(G.tabla(["Modelo", "Lab", { t: "Puntuación", n: 1 }, { t: "IC 95 %", n: 1 }, { t: "Frente a la media", n: 1 }, "Marca"],
        seleccion().slice().sort((a, b) => b.rasgos[t].p - a.rasgos[t].p).map((m) => {
          const x = m.rasgos[t];
          return [m.etiqueta, m.lab, dec(x.p, 1), `${dec(x.ic[0], 1)} – ${dec(x.ic[1], 1)}`, firmado(x.dif), x.marca || ""];
        })));
    }
    pintores.push(pinta);
  })();

  /* ── el radar (el mismo dibujo que /personalidad: 0,5 + dif/(2·máx|dif|)) */
  const radio = (d) => 0.5 + d / (2 * MAXDIF);
  function radar(capas, tam = 260) {
    const c = tam / 2, Rr = tam / 2 - 30;
    const pt = (i, r) => [c + Rr * r * Math.sin((i * Math.PI) / 3), c - Rr * r * Math.cos((i * Math.PI) / 3)];
    const pol = (rs) => rs.map((r, i) => pt(i, r).map((v) => v.toFixed(1)).join(",")).join(" ");
    const svg = el("svg", { viewBox: `0 0 ${tam} ${tam}`, class: "radar-d", role: "img",
      "aria-label": "Radar: " + capas.map((k) => k.m.etiqueta).join(" frente a ") + ", sobre la media de los demás" });
    svg.appendChild(el("polygon", { points: pol(Array(6).fill(1)), class: "anillo" }));
    RASGOS.forEach((r, i) => {
      const [x, y] = pt(i, 1);
      svg.appendChild(el("line", { x1: c, y1: c, x2: x, y2: y, class: "radio-l" }));
      const [tx, ty] = pt(i, 1.16);
      svg.appendChild(el("text", { x: tx, y: ty + 4, class: "vert", "text-anchor": "middle" }, [T(r.clave)]));
    });
    svg.appendChild(el("polygon", { points: pol(Array(6).fill(0.5)), class: "media" }));
    capas.forEach((k) => svg.appendChild(el("polygon", { points: pol(RASGOS.map((r) => radio(k.m.rasgos[r.clave].dif))), class: "perfil " + k.clase })));
    return svg;
  }

  /* ══ 03 · comparar dos modelos ══════════════════════════════════════════ */
  (function comparar() {
    const host = document.getElementById("comparar-host");
    const opciones = (actual) => MODELOS.slice().sort((a, b) => a.etiqueta.localeCompare(b.etiqueta, "es"))
      .map((m) => h("option", { value: m.id, text: m.etiqueta, ...(m.id === actual ? { selected: "" } : {}) }));
    const selA = h("select", { class: "chip sel-a", "aria-label": "Modelo A" }, opciones(estado.a));
    const selB = h("select", { class: "chip sel-b", "aria-label": "Modelo B" }, opciones(estado.b));
    const cambia = h("button", { type: "button", class: "chip", title: "Intercambiar", text: "⇄" });
    selA.addEventListener("change", () => { estado.a = selA.value; repintar(); });
    selB.addEventListener("change", () => { estado.b = selB.value; repintar(); });
    cambia.addEventListener("click", () => { [estado.a, estado.b] = [estado.b, estado.a]; repintar(); });
    const fig = G.figura({
      titulo: "A frente a B, rasgo a rasgo", sinTabla: false,
      controles: [h("span", { class: "llave a" }), selA, cambia, h("span", { class: "llave b" }), selB,
        ...utiles("comparar", () => {
          const a = POR_ID.get(estado.a), b = POR_ID.get(estado.b);
          return ["personalidad_comparar.csv", ["rasgo", "a", "a_p", "a_ic_bajo", "a_ic_alto", "b", "b_p", "b_ic_bajo", "b_ic_alto"],
            RASGOS.map((r) => [r.clave, a.etiqueta, a.rasgos[r.clave].p, ...a.rasgos[r.clave].ic, b.etiqueta, b.rasgos[r.clave].p, ...b.rasgos[r.clave].ic])];
        })],
      fuente: mk`Personalidad ${P.banco || ""} · ${P.fuente}`,
      pie: mk`Intervalos al 95 %. <b>Diferencia clara</b>: los dos intervalos no se tocan. Las marcas ▲ ▼ de cada modelo son otra cosa: frente a la media de todos los demás, con cinco comprobaciones más.`,
    });
    host.appendChild(fig);
    const rejilla = h("div", { class: "comparar-rejilla" });
    fig._lienzo.replaceChildren(rejilla);
    function pinta() {
      selA.value = estado.a; selB.value = estado.b;
      const a = POR_ID.get(estado.a), b = POR_ID.get(estado.b);
      const izq = h("div", { class: "cmp-radar" }, [radar([{ m: b, clase: "b" }, { m: a, clase: "a" }]),
        h("p", { class: "nota" }, [h("span", { class: "llave a" }), T(" " + a.etiqueta + "  "), h("span", { class: "llave b" }), T(" " + b.etiqueta)])]);
      const filas = h("div", { class: "cmp-filas" });
      let claras = 0;
      RASGOS.forEach((r) => {
        const x = a.rasgos[r.clave], y = b.rasgos[r.clave];
        const lo = Math.min(x.ic[0], y.ic[0]) - 3, hi = Math.max(x.ic[1], y.ic[1]) + 3;
        const sep = x.ic[0] > y.ic[1] ? "a" : y.ic[0] > x.ic[1] ? "b" : null;
        if (sep) claras++;
        const pos = (v) => ((v - lo) / (hi - lo)) * 100 + "%";
        const pista = h("div", { class: "cmp-pista" }, [
          h("span", { class: "cmp-ic a", style: `left:${pos(x.ic[0])};width:calc(${pos(x.ic[1])} - ${pos(x.ic[0])})` }),
          h("span", { class: "cmp-ic b", style: `left:${pos(y.ic[0])};width:calc(${pos(y.ic[1])} - ${pos(y.ic[0])})` }),
          h("span", { class: "cmp-pt a", style: `left:${pos(x.p)}`, title: `${a.etiqueta}: ${dec(x.p, 1)} [${dec(x.ic[0], 1)}–${dec(x.ic[1], 1)}]` }),
          h("span", { class: "cmp-pt b", style: `left:${pos(y.p)}`, title: `${b.etiqueta}: ${dec(y.p, 1)} [${dec(y.ic[0], 1)}–${dec(y.ic[1], 1)}]` })]);
        const quien = sep === "a" ? a : sep === "b" ? b : null;
        filas.appendChild(h("div", { class: "cmp-fila" + (sep ? " clara" : "") }, [
          h("div", { class: "cmp-rasgo" }, [h("b", { text: r.nombre }), h("small", { text: `A ${dec(x.p, 0)}${x.marca ? " " + x.marca : ""} · B ${dec(y.p, 0)}${y.marca ? " " + y.marca : ""}` })]),
          pista,
          h("div", { class: "cmp-veredicto", text: quien ? `${quien === a ? "A" : "B"}: ${R[r.clave].alto}` : "sin diferencia clara" })]));
      });
      const resumen = h("p", { class: "cmp-resumen" });
      pintar(resumen, claras ? mk`Diferencia clara en <b>${claras}</b> de ${RASGOS.length} rasgos.` : mk`Ninguna diferencia clara: con estos intervalos, sus perfiles no se distinguen.`);
      rejilla.replaceChildren(izq, h("div", {}, [filas, resumen]));
      fig._tabla.replaceChildren(G.tabla(["Rasgo", { t: "A", n: 1 }, { t: "IC A", n: 1 }, { t: "B", n: 1 }, { t: "IC B", n: 1 }, "Lectura"],
        RASGOS.map((r) => {
          const x = a.rasgos[r.clave], y = b.rasgos[r.clave];
          const sep = x.ic[0] > y.ic[1] ? "A más" : y.ic[0] > x.ic[1] ? "B más" : "sin diferencia clara";
          return [r.nombre, dec(x.p, 1), `${dec(x.ic[0], 1)} – ${dec(x.ic[1], 1)}`, dec(y.p, 1), `${dec(y.ic[0], 1)} – ${dec(y.ic[1], 1)}`, sep];
        })));
    }
    pintores.push(pinta);
  })();

  /* ══ 04 · huellas ═══════════════════════════════════════════════════════ */
  (function huellas() {
    const host = document.getElementById("huellas-host");
    const fig = G.figura({
      titulo: "Seis rasgos en σ, de lo que más distingue a lo que menos", sinTabla: true,
      controles: utiles("huellas", () => ["personalidad_huellas.csv", ["modelo", "etiqueta", ...RASGOS.map((r) => r.clave + "_z")],
        seleccion().map((m) => [m.id, m.etiqueta, ...RASGOS.map((r) => z(m, r.clave).toFixed(3))])]),
      fuente: mk`Personalidad ${P.banco || ""} · σ = desviación típica del panel de ${ES.format(MODELOS.length)} modelos`,
    });
    host.appendChild(fig);
    const maxZ = Math.max(...MODELOS.flatMap((m) => RASGOS.map((r) => Math.abs(z(m, r.clave)))));
    function pinta() {
      const ms = seleccion();
      if (!ms.length) { vacio(fig._lienzo); return; }
      fig._lienzo.replaceChildren(h("div", { class: "huellas" }, ms.map((m) => {
        const orden = RASGOS.slice().sort((p, q) => Math.abs(z(m, q.clave)) - Math.abs(z(m, p.clave)));
        return h("article", { class: "huella-m" }, [
          h("p", { class: "hm-cab" }, [h("b", { text: m.etiqueta }), h("span", { text: m.lab })]),
          h("ul", {}, orden.map((r) => {
            const v = z(m, r.clave), anch = (Math.abs(v) / maxZ) * 50;
            return h("li", { title: `${r.nombre}: ${firmado(v, 2)} σ · ${v >= 0 ? r.alto : r.bajo}` }, [
              h("span", { class: "hm-r", text: r.nombre }),
              h("span", { class: "hm-pista" }, [h("i", { class: v >= 0 ? "sube" : "baja", style: v >= 0 ? `left:50%;width:${anch}%` : `left:${50 - anch}%;width:${anch}%` })]),
              h("span", { class: "hm-v", text: firmado(v, 1) + "σ" + (m.rasgos[r.clave].marca ? " " + m.rasgos[r.clave].marca : "") })]);
          }))]);
      })));
    }
    pintores.push(pinta);
  })();

  /* ══ 05 · familias (árbol de enlace medio) ══════════════════════════════ */
  (function familias() {
    const host = document.getElementById("familias-host");
    const fig = G.figura({
      titulo: "Árbol de parecidos entre perfiles",
      sub: "Distancia euclídea entre los seis rasgos estandarizados; enlace medio",
      controles: utiles("familias"),
      fuente: mk`Personalidad ${P.banco || ""} · calculado en el navegador con los datos de la tabla`,
    });
    host.appendChild(fig);
    function arbol(ms) {
      const dist = (x, y) => Math.sqrt(RASGOS.reduce((s, r) => s + (z(x, r.clave) - z(y, r.clave)) ** 2, 0));
      let grupos = ms.map((m) => ({ hojas: [m], alto: 0, m }));
      const d = (g1, g2) => media(g1.hojas.flatMap((x) => g2.hojas.map((y) => dist(x, y))));
      while (grupos.length > 1) {
        let mejor = null;
        for (let i = 0; i < grupos.length; i++) for (let j = i + 1; j < grupos.length; j++) {
          const v = d(grupos[i], grupos[j]);
          if (!mejor || v < mejor.v) mejor = { i, j, v };
        }
        const nuevo = { hojas: grupos[mejor.i].hojas.concat(grupos[mejor.j].hojas), alto: mejor.v, hijos: [grupos[mejor.i], grupos[mejor.j]] };
        grupos = grupos.filter((_, k) => k !== mejor.i && k !== mejor.j).concat([nuevo]);
      }
      return grupos[0];
    }
    function dibujar(W) {
      const ms = seleccion();
      const svg = el("svg", { viewBox: `0 0 ${W} 40`, width: W, role: "img", "aria-label": "Árbol de parecidos entre los modelos seleccionados" });
      if (ms.length < 2) { svg.appendChild(el("text", { x: 4, y: 24, class: "eje-txt" }, [T("Hacen falta al menos dos modelos.")])); return svg; }
      const raiz = arbol(ms);
      const orden = raiz.hojas;
      const fila = 22, top = 24, H = top + orden.length * fila + 22;
      const etiq = orden.map((m) => m.etiqueta + " · " + m.lab);
      const anchoEt = Math.min(W * 0.55, Math.ceil(anchoMax(etiq, "eje")) + 14);
      const x0 = anchoEt, x1 = W - 12, max = raiz.alto || 1;
      const X = (v) => x0 + (v / max) * (x1 - x0);
      svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
      const yDe = new Map(orden.map((m, i) => [m.id, top + i * fila + fila / 2]));
      const marcasSvg = [];
      orden.forEach((m) => {
        const g = el("g", { class: "marca" });
        g.appendChild(el("text", { x: x0 - 8, y: yDe.get(m.id) + 4, class: "eje-txt et-fila", "text-anchor": "end" }, [T(m.etiqueta)]));
        conGlobo(g, () => mk`<div class="g-tit">${m.etiqueta}</div><div class="g-nota">${m.lab} · ${m.frase || "perfil equilibrado"}</div>`, marcasSvg);
        marcasSvg.push(g);
        svg.appendChild(g);
      });
      const pinta = (n) => {
        if (!n.hijos) return { y: yDe.get(n.m.id), x: X(0) };
        const [p, q] = n.hijos.map(pinta);
        const x = X(n.alto);
        svg.appendChild(el("path", { d: `M${p.x},${p.y}H${x}V${q.y}H${q.x}`, class: "rama" }));
        return { y: (p.y + q.y) / 2, x };
      };
      pinta(raiz);
      for (let v = 0; v <= max + 1e-9; v += max > 4 ? 1 : 0.5) {
        svg.appendChild(el("text", { x: X(v), y: H - 4, class: "eje-txt", "text-anchor": "middle" }, [T(dec(v, max > 4 ? 0 : 1))]));
      }
      svg.appendChild(el("text", { x: x1, y: 12, class: "eje-txt", "text-anchor": "end" }, [T("distancia →")]));
      return svg;
    }
    adaptable(fig, dibujar);
    pintores.push(() => fig._redibujar && fig._redibujar());
  })();

  /* ══ 06 · situaciones reales ════════════════════════════════════════════ */
  (function ejemplos() {
    const host = document.getElementById("ejemplos-host");
    const E = P.ejemplos;
    if (!E || !E.situaciones.length) { vacio(host, "Sin situaciones de ejemplo en esta edición."); return; }
    const mandos = pestanas([["", "Todos"], ...opcionesRasgo], () => estado.ejRasgo, (k) => { estado.ejRasgo = k; repintar(); }, "Rasgo de las situaciones");
    const caja = h("div", { class: "ejemplos" });
    const pie = h("p", { class: "fuente" });
    pintar(pie, mk`Selección: ${E.criterio}. Fuente · ${E.fuente}`);
    host.append(h("div", { class: "acciones-viz ej-mandos" }, [mandos, ...utiles("ejemplos")]), caja, pie);
    function pinta() {
      const sel = estado.sel;
      const sits = E.situaciones.filter((s) => !estado.ejRasgo || s.rasgo === estado.ejRasgo);
      caja.replaceChildren(...sits.map((s) => {
        const els = s.elecciones.filter((x) => sel.has(x.modelo) && x.alto != null)
          .map((x) => ({ m: POR_ID.get(x.modelo), v: x.alto, n: x.n })).sort((p, q) => q.v - p.v || p.m.etiqueta.localeCompare(q.m.etiqueta, "es"));
        const grupo = (filtro, titulo, clase) => {
          const ms = els.filter(filtro);
          return h("div", { class: "ej-grupo " + clase }, [h("p", { class: "ej-g-tit", text: `${titulo} · ${ms.length}` }),
            h("ul", {}, ms.map((x) => h("li", { title: `${x.m.etiqueta}: polo alto en ${dec(x.v * 100, 0)} % de ${x.n} respuestas válidas` }, [
              T(x.m.etiqueta), clase === "mixto" ? h("small", { text: " " + dec(x.v * 100, 0) + " %" }) : T("")])))]);
        };
        return h("article", { class: "ejemplo", style: `--c:${TONO_R[s.rasgo]}` }, [
          h("p", { class: "ej-cab" }, [h("span", { class: "ej-rasgo", style: `--c:${TONO_R[s.rasgo]}`, text: R[s.rasgo].nombre }), h("span", { class: "ej-faceta", text: s.faceta.replace(/_/g, " ") }), h("code", { text: s.id })]),
          h("p", { class: "ej-sit", text: s.situacion }),
          h("div", { class: "ej-opciones" }, [
            h("div", { class: "ej-op alto" }, [h("span", { class: "ej-k", text: "Polo alto · " + R[s.rasgo].alto }), h("p", { text: "«" + s.alto + "»" })]),
            h("div", { class: "ej-op bajo" }, [h("span", { class: "ej-k", text: "Polo bajo · " + R[s.rasgo].bajo }), h("p", { text: "«" + s.bajo + "»" })])]),
          h("div", { class: "ej-grupos" }, [
            grupo((x) => x.v === 1, "Siempre el alto", "alto"),
            grupo((x) => x.v > 0 && x.v < 1, "Depende", "mixto"),
            grupo((x) => x.v === 0, "Siempre el bajo", "bajo")])]);
      }));
    }
    pintores.push(pinta);
  })();

  /* ══ 07 · ranking a medida ══════════════════════════════════════════════ */
  (function ranking() {
    const host = document.getElementById("ranking-host");
    const PLANTILLAS = [
      ["Atención al cliente", { A: 2, N: -2, C: 1 }],
      ["Agente con acceso a dinero", { H: 2, C: 2, N: -1 }],
      ["Asistente de investigación", { O: 2, H: 1, C: 1 }],
      ["Compañero creativo", { O: 2, E: 1, A: 1 }],
      ["Negociador", { A: -1, E: 1, N: -1 }],
    ];
    const mandos = h("div", { class: "pesos" });
    const botones = {};
    RASGOS.forEach((r) => {
      const fila = h("div", { class: "peso", role: "group", "aria-label": "Peso de " + r.nombre }, [h("span", { class: "peso-n", text: r.nombre })]);
      botones[r.clave] = [-2, -1, 0, 1, 2].map((v) => {
        const b = h("button", { type: "button", class: "chip peso-b", text: v > 0 ? "+" + v : v < 0 ? "−" + -v : "0", "aria-pressed": "false" });
        b.addEventListener("click", () => { estado.pesos[r.clave] = v; repintar(); });
        fila.appendChild(b);
        return b;
      });
      mandos.appendChild(fila);
    });
    const plantillas = h("div", { class: "plantillas" }, [h("span", { class: "nota", text: "Plantillas:" }),
      ...PLANTILLAS.map(([t, w]) => {
        const b = h("button", { type: "button", class: "chip", text: t, title: Object.entries(w).map(([k, v]) => `${R[k].nombre} ${v > 0 ? "+" : "−"}${Math.abs(v)}`).join(" · ") });
        b.addEventListener("click", () => { RASGOS.forEach((r) => (estado.pesos[r.clave] = w[r.clave] || 0)); repintar(); });
        return b;
      }),
      (() => { const b = h("button", { type: "button", class: "chip", text: "Borrar" }); b.addEventListener("click", () => { RASGOS.forEach((r) => (estado.pesos[r.clave] = 0)); repintar(); }); return b; })()]);
    const puntua = (m) => {
      const w = estado.pesos, tot = RASGOS.reduce((s, r) => s + Math.abs(w[r.clave]), 0);
      return tot ? RASGOS.reduce((s, r) => s + w[r.clave] * z(m, r.clave), 0) / tot : 0;
    };
    const fig = G.figura({
      titulo: "Tu ranking", sinTabla: true,
      controles: utiles("ranking", () => ["personalidad_ranking.csv", ["modelo", "etiqueta", "puntuacion_z", ...RASGOS.map((r) => "peso_" + r.clave)],
        seleccion().map((m) => [m.id, m.etiqueta, puntua(m).toFixed(3), ...RASGOS.map((r) => estado.pesos[r.clave])])]),
      pie: mk`La cifra es la media ponderada de los rasgos estandarizados (en σ del panel): 0 es un modelo típico. Un peso negativo premia el polo bajo del rasgo.`,
    });
    host.append(h("div", { class: "ranking-mandos" }, [mandos, plantillas]), fig);
    function pinta() {
      RASGOS.forEach((r) => botones[r.clave].forEach((b, i) => b.setAttribute("aria-pressed", String([-2, -1, 0, 1, 2][i] === estado.pesos[r.clave]))));
      const ms = seleccion();
      if (!RASGOS.some((r) => estado.pesos[r.clave])) { vacio(fig._lienzo, "Da peso a algún rasgo, o elige una plantilla."); return; }
      if (!ms.length) { vacio(fig._lienzo); return; }
      const filas = ms.map((m) => ({ m, v: puntua(m) })).sort((a, b) => b.v - a.v);
      const max = Math.max(0.5, ...filas.map((f) => Math.abs(f.v)));
      fig._lienzo.replaceChildren(h("ol", { class: "rk" }, filas.map((f, i) => h("li", { class: i < 3 ? "podio" : "" }, [
        h("span", { class: "rk-i", text: String(i + 1) }),
        h("span", { class: "rk-n" }, [h("b", { text: f.m.etiqueta }), h("small", { text: f.m.lab })]),
        h("span", { class: "rk-pista" }, [h("i", { class: f.v >= 0 ? "sube" : "baja",
          style: f.v >= 0 ? `left:50%;width:${(f.v / max) * 50}%` : `left:${50 + (f.v / max) * 50}%;width:${(-f.v / max) * 50}%` })]),
        h("span", { class: "rk-v", text: firmado(f.v, 2) })]))));
    }
    pintores.push(pinta);
  })();

  /* ══ 08 · personalidad e ISS ════════════════════════════════════════════ */
  (function conISS() {
    const host = document.getElementById("iss-host");
    const pearson = (xs, ys) => {
      const mx = media(xs), my = media(ys);
      const num = xs.reduce((s, x, i) => s + (x - mx) * (ys[i] - my), 0);
      const den = Math.sqrt(xs.reduce((s, x) => s + (x - mx) ** 2, 0) * ys.reduce((s, y) => s + (y - my) ** 2, 0));
      return den ? num / den : null;
    };
    const fig = G.figura({
      titulo: "Un rasgo frente al ISS",
      sub: " ",
      controles: [pestanas(opcionesRasgo, () => estado.issRasgo, (k) => { estado.issRasgo = k; repintar(); }, "Rasgo en el eje horizontal"),
        ...utiles("iss", () => ["personalidad_iss.csv", ["modelo", "etiqueta", estado.issRasgo, "iss", "medicion_socialbench"],
          seleccion().filter((m) => m.iss != null).map((m) => [m.id, m.etiqueta, m.rasgos[estado.issRasgo].p, m.iss, m.psicobench])])],
      fuente: mk`Personalidad ${P.banco || ""} · ISS de SocialBench`,
      pie: mk`Pulsa un punto para abrir su medición en SocialBench. † el ISS es de la versión preliminar (stealth) del modelo.`,
    });
    host.appendChild(fig);
    const sub = fig.querySelector(".subviz");
    function dibujar(W) {
      const t = estado.issRasgo, ms = seleccion().filter((m) => m.iss != null);
      const H = Math.max(260, Math.min(420, W * 0.6));
      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, role: "img", style: `--c:${TONO_R[t]}`, "aria-label": `${R[t].nombre} frente al ISS, ${ms.length} modelos` });
      if (ms.length < 2) { svg.appendChild(el("text", { x: 4, y: 24, class: "eje-txt" }, [T("Hacen falta al menos dos modelos con ISS.")])); return svg; }
      const pad = { l: 44, r: 16, t: 14, b: 36 };
      const xs = ms.map((m) => m.rasgos[t].p), ys = ms.map((m) => m.iss);
      const xlo = Math.floor(Math.min(...xs) / 5) * 5 - 2, xhi = Math.ceil(Math.max(...xs) / 5) * 5 + 2;
      const yhi = Math.ceil(Math.max(...ys) / 10) * 10;
      const X = (v) => pad.l + ((v - xlo) / (xhi - xlo)) * (W - pad.l - pad.r);
      const Y = (v) => H - pad.b - (v / yhi) * (H - pad.t - pad.b);
      for (let v = 0; v <= yhi; v += 10) {
        svg.appendChild(el("line", { x1: pad.l, x2: W - pad.r, y1: Y(v), y2: Y(v), class: "reja-v" }));
        svg.appendChild(el("text", { x: pad.l - 8, y: Y(v) + 4, class: "eje-txt", "text-anchor": "end" }, [T(String(v))]));
      }
      for (let v = Math.ceil(xlo / 5) * 5; v <= xhi; v += 5) svg.appendChild(el("text", { x: X(v), y: H - pad.b + 18, class: "eje-txt", "text-anchor": "middle" }, [T(String(v))]));
      svg.appendChild(el("text", { x: W - pad.r, y: H - 4, class: "eje-txt", "text-anchor": "end" }, [T(R[t].nombre + " →")]));
      svg.appendChild(el("text", { x: pad.l, y: pad.t - 2, class: "eje-txt" }, [T("ISS ↑ (cede más)")]));
      // recta de mínimos cuadrados, solo como guía
      const mx = media(xs), my = media(ys);
      const pend = xs.reduce((s, x, i) => s + (x - mx) * (ys[i] - my), 0) / xs.reduce((s, x) => s + (x - mx) ** 2, 0);
      if (isFinite(pend)) svg.appendChild(el("line", { x1: X(xlo), y1: Y(my + pend * (xlo - mx)), x2: X(xhi), y2: Y(my + pend * (xhi - mx)), class: "linea-media" }));
      const marcasSvg = [];
      // rótulo fijo solo en los dos extremos del ISS; el resto, al pasar por encima
      const extremos = new Set([...ms].sort((a, b) => a.iss - b.iss).filter((_, i, arr) => i === 0 || i === arr.length - 1).map((m) => m.id));
      ms.forEach((m) => {
        const g = el("g", { class: "marca punto-iss" });
        const cx = X(m.rasgos[t].p), cy = Y(m.iss);
        g.appendChild(el("circle", { cx, cy, r: 6, class: "punto-r" + (m.rasgos[t].marca ? " firme" : "") }));
        if (extremos.has(m.id)) g.appendChild(el("text", { x: cx + (cx > W * 0.7 ? -9 : 9), y: cy + 4, class: "punto-et", "text-anchor": cx > W * 0.7 ? "end" : "start" }, [T(m.etiqueta + (m.issDe ? " †" : ""))]));
        conGlobo(g, () => mk`<div class="g-tit">${m.etiqueta}${m.issDe ? " †" : ""}</div>
          <div class="g-fila"><span>${R[t].nombre}</span><b>${dec(m.rasgos[t].p, 1)}${m.rasgos[t].marca ? " " + m.rasgos[t].marca : ""}</b></div>
          <div class="g-fila"><span>ISS</span><b>${dec(m.iss, 1)}</b></div>
          <div class="g-nota">Pulsa para abrir su medición en SocialBench</div>`, marcasSvg);
        g.addEventListener("click", () => { location.href = enlace("psicobench.html", "#m=" + encodeURIComponent(m.psicobench)); });
        marcasSvg.push(g);
        svg.appendChild(g);
      });
      return svg;
    }
    adaptable(fig, dibujar);
    fig._nav = "Rasgo frente al ISS: flechas para recorrer los modelos";
    function pinta() {
      const t = estado.issRasgo, ms = seleccion().filter((m) => m.iss != null);
      const r = ms.length > 2 ? pearson(ms.map((m) => m.rasgos[t].p), ms.map((m) => m.iss)) : null;
      const todo = P.relacionISS[t];
      sub.textContent = `r = ${r == null ? "—" : dec(r, 2)} con ${ms.length} modelos seleccionados` +
        (ms.length !== todo.n ? ` (con los ${todo.n} del panel: r = ${dec(todo.r, 2)})` : "") + ". Descriptivo, sin contraste.";
      if (fig._redibujar) fig._redibujar();
      fig._tabla.replaceChildren(G.tabla(["Modelo", { t: R[t].nombre, n: 1 }, { t: "ISS", n: 1 }],
        ms.slice().sort((a, b) => a.iss - b.iss).map((m) => [m.etiqueta + (m.issDe ? " †" : ""), dec(m.rasgos[t].p, 1), dec(m.iss, 1)])));
    }
    pintores.push(pinta);
  })();

  /* ══ 09 · validez ═══════════════════════════════════════════════════════ */
  (function validez() {
    const host = document.getElementById("validez-host");
    const claves = Object.keys(P.nombreIndice);
    const fig = G.figura({
      titulo: "Índices de validez por modelo", sinTabla: true,
      sub: "Cada índice con su umbral de aviso y de «no interpretable»; un modelo con algún «no interpretable» no entra en el cuadro",
      controles: utiles("validez", () => ["personalidad_validez.csv", ["modelo", "etiqueta", ...claves, "validez"],
        MODELOS.map((m) => [m.id, m.etiqueta, ...claves.map((k) => m.indices[k]), m.validez])]),
      fuente: mk`Personalidad ${P.banco || ""} · PERSONALIDAD.md §41.2`,
    });
    host.appendChild(fig);
    const umbral = (k) => { const [a, b] = P.umbrales[k]; return a < b ? `aviso > ${dec(a, 2)} · fuera > ${dec(b, 2)}` : `aviso < ${dec(a, 2)} · fuera < ${dec(b, 2)}`; };
    function pinta() {
      const ms = seleccion();
      const t = h("table", { class: "datos validez-t" });
      t.appendChild(h("thead", {}, [h("tr", {}, [h("th", { scope: "col", text: "Modelo" }),
        ...claves.map((k) => h("th", { scope: "col", class: "n", title: umbral(k) }, [T(P.nombreIndice[k]), h("small", { text: umbral(k) })])),
        h("th", { scope: "col", text: "Estado" })])]));
      t.appendChild(h("tbody", {}, ms.map((m) => h("tr", {}, [h("th", { scope: "row", text: m.etiqueta }),
        ...claves.map((k) => h("td", { class: "n nivel-" + (m.niveles[k] || "").replace(/\s+/g, "-"), text: dec(m.indices[k], 2) })),
        h("td", { class: "estado-" + m.validez, text: m.validez === "aviso" ? "⚠ aviso" : m.validez })]))));
      const fuera = h("div", { class: "fuera-d" }, [h("p", { class: "ej-g-tit", text: `Medidos, pero sin ficha · ${P.fuera.length}` }),
        h("ul", {}, P.fuera.map((f) => h("li", {}, [h("b", { text: f.etiqueta }), T(` — ${f.tipo}: ${f.motivo}`)])))]);
      fig._lienzo.replaceChildren(h("div", { class: "tabla-envuelta" }, [t]), fuera);
    }
    pintores.push(pinta);
  })();

  /* ══ 10 · la tabla completa ═════════════════════════════════════════════ */
  (function tabla() {
    const host = document.getElementById("tabla-host");
    const csv = () => ["personalidad_cuadro.csv",
      ["modelo", "etiqueta", "lab", "iss", "medicion_socialbench", "validez",
        ...RASGOS.flatMap((r) => [r.clave, r.clave + "_ic_bajo", r.clave + "_ic_alto", r.clave + "_dif", r.clave + "_dif_ic_bajo", r.clave + "_dif_ic_alto", r.clave + "_marca"])],
      MODELOS.map((m) => [m.id, m.etiqueta, m.lab, m.iss, m.psicobench, m.validez,
        ...RASGOS.flatMap((r) => { const x = m.rasgos[r.clave]; return [x.p, x.ic[0], x.ic[1], x.dif, x.difIC[0], x.difIC[1], x.marca]; })])];
    const fig = G.figura({
      titulo: "El cuadro entero", sinTabla: true,
      sub: "Puntuación [intervalo] · diferencia con la media de los demás. El CSV lleva todos los modelos, con o sin selección",
      controles: utiles("tabla", csv),
      fuente: mk`Personalidad ${P.banco || ""} · ${P.fuente}`,
    });
    host.appendChild(fig);
    function pinta() {
      const ms = seleccion().slice().sort((a, b) => a.lab.localeCompare(b.lab) || a.etiqueta.localeCompare(b.etiqueta, "es"));
      if (!ms.length) { vacio(fig._lienzo); return; }
      const t = h("table", { class: "datos tabla-cuadro" });
      t.appendChild(h("thead", {}, [h("tr", {}, [h("th", { scope: "col", text: "Modelo" }), h("th", { scope: "col", text: "Lab" }), h("th", { scope: "col", class: "n", text: "ISS" }),
        ...RASGOS.map((r) => h("th", { scope: "col", class: "n", text: r.nombre }))])]));
      t.appendChild(h("tbody", {}, ms.map((m) => h("tr", {}, [h("th", { scope: "row", text: m.etiqueta }), h("td", { text: m.lab }),
        h("td", { class: "n", text: m.iss == null ? "—" : dec(m.iss, 1) }),
        ...RASGOS.map((r) => {
          const x = m.rasgos[r.clave];
          return h("td", { class: "n" + (x.marca ? " firme" : "") }, [h("b", { text: dec(x.p, 0) }), h("small", { text: ` [${dec(x.ic[0], 0)}–${dec(x.ic[1], 0)}] ${firmado(x.dif)}${x.marca ? " " + x.marca : ""}` })]);
        })]))));
      fig._lienzo.replaceChildren(h("div", { class: "tabla-envuelta" }, [t]));
    }
    pintores.push(pinta);
  })();

  /* ══ 11 · método ════════════════════════════════════════════════════════ */
  (function metodo() {
    const host = document.getElementById("metodo-host");
    const caja = (titulo, cuerpo) => { const d = h("div", { class: "metodo-c" }, [h("h3", { text: titulo })]); const p = h("p"); pintar(p, cuerpo); d.appendChild(p); return d; };
    host.append(
      caja("Qué se mide", mk`La <b>conducta</b>: en cada situación, cuál de dos salidas razonables elige el modelo. La puntuación de un rasgo es la frecuencia con que elige su polo alto (0-100), y la marca compara a cada modelo con la <b>media de los demás</b>, no con un ideal. Así no se mide lo deseable que se cree el modelo, sino lo que hace distinto del resto.`),
      caja("Cuándo una diferencia es firme", mk`Su intervalo excluye el cero y además pasa ${ES.format(P.comprobaciones.length)} comprobaciones de robustez (mitades al azar, réplicas, orden de las opciones, quitar laboratorios y corrección por comparaciones múltiples, q < ${dec(P.q, 2)}). Hay <b>${ES.format(P.robustas)}</b> de ${ES.format(P.candidatas)} candidatas. <a href="${enlace("personalidad.html", "#metodologia")}">Las comprobaciones, una a una →</a>`),
      caja("Qué no es", mk`No es un test clínico ni dice que un modelo «sienta» nada. No es una nota: ningún perfil es mejor que otro, depende del trabajo. Y no se usan percentiles como cifra principal: dicen quién está por encima, pero no cuánto, y cambian cada vez que entra un modelo.`),
      caja("Fuentes", mk`Método completo, decisiones y lo que salió mal: <a href="${publicada ? "https://github.com/PhotoGarrido/BenchAI/blob/main/PERSONALIDAD.md" : "../PERSONALIDAD.md"}">PERSONALIDAD.md</a> (§${P.seccion}). Datos: <code>${P.fuente}</code> y <code>${P.ejemplos ? P.ejemplos.fuente : ""}</code>.`),
    );
  })();

  repintar();
})();
