/* ===========================================================================
   BenchAI · Personalidad — el cuadro de personalidad por conducta
   ---------------------------------------------------------------------------
   Monta el cuadro (modelos × seis rasgos), el perfil de un modelo frente al
   panel, las tablas de método y la lista de modelos fuera del cuadro, todo
   desde `window.PSICO.personalidad` (que genera `web/generar_datos.py` a
   partir de `cuadro_publico.json`). Mismas reglas que el resto de `web/`:
   ninguna cifra escrita a mano, ningún innerHTML fuera de `marcado.js`, y el
   color lo pone la escala del sitio.
   =========================================================================== */
(function () {
  "use strict";

  const D = window.PSICO;
  const P = D.personalidad;
  const G = window.G;
  const mk = window.MARCADO.mk, une = window.MARCADO.une;
  const h = G.h, dec = G.dec;
  const ES = new Intl.NumberFormat("es-ES");
  const T = (s) => document.createTextNode(s);

  /* ── cifras embebidas en el texto (mismo mecanismo que psicobench.js) ──── */
  const ruta = (obj, camino) => camino.split(".").reduce((o, k) => (o == null ? o : o[k]), obj);
  document.querySelectorAll("[data-cifra]").forEach((n) => {
    const v = ruta(D, n.dataset.cifra);
    n.textContent = v == null ? "—" : (n.dataset.prefijo || "") + (typeof v === "number" ? ES.format(v) : String(v)) + (n.dataset.sufijo || "");
  });
  document.getElementById("v-edicion").textContent = `Cuadro ${P.banco || ""} · ${P.fecha}`.replace("  ", " ");

  /* ── enlaces a las otras superficies: se leen de la barra, que en la
     publicación ya lleva la ruta limpia (/psicobench); en local, el fichero */
  const base = (clave) => {
    const a = Array.from(document.querySelectorAll(".superficies a")).find((x) => x.getAttribute("href").includes(clave));
    return a ? a.getAttribute("href") : clave + ".html";
  };
  const fichaPB = (id) => base("psicobench") + "#m=" + encodeURIComponent(id);

  /* ── rasgos y derivados ────────────────────────────────────────────────── */
  const RASGOS = P.rasgos;                     // [{clave, nombre, alto, bajo, n, …}]
  const R = Object.fromEntries(RASGOS.map((r) => [r.clave, r]));
  const MODELOS = P.modelos;
  const labs = P.labs.slice();
  const conMarca = (m) => RASGOS.some((r) => m.rasgos[r.clave].marca);
  const sentido = (marca) => (marca === "▲" ? "más" : marca === "▼" ? "menos" : "");
  const quienEs = (m, t) => {
    const r = m.rasgos[t];
    return r.marca ? `${sentido(r.marca)} ${R[t].nombre} que los demás (${r.marca === "▲" ? R[t].alto : R[t].bajo})` : "no se distingue de los demás";
  };
  const icTxt = (r) => `${r.icE[0]}–${r.icE[1]}`;

  /* El aviso de validez en palabras: qué índice lo motiva y qué quiere decir.
     Las cifras exactas van al lado, tal cual las da el cuadro. */
  const LLANO = {
    V1_delta: "elige a menudo por la posición de la opción (A o B), no por su contenido",
    V1_frac_A: "elige a menudo por la posición de la opción (A o B), no por su contenido",
    V2_no_validas: "deja demasiadas respuestas sin valor (negativas o ilegibles)",
    V3_retest: "repite poco su propia elección cuando se le vuelve a preguntar",
    V4_coherencia: "su juicio de qué opción es admirable cambia a menudo al invertir el orden",
  };
  const motivoLlano = (m) => Array.from(new Set(Object.entries(m.niveles || {})
    .filter(([, nivel]) => nivel !== "válido").map(([k]) => LLANO[k] || P.nombreIndice[k] || k))).join("; ");

  /* ══ el cuadro ══════════════════════════════════════════════════════════ */
  const estado = { clave: "id", asc: true, labs: new Set(labs), elegido: null };
  const valorOrden = (m, k) => (k === "id" ? m.id : k === "iss" ? m.iss : m.rasgos[k].p);

  const mandos = document.getElementById("mandos-cuadro");
  const COLS_ORDEN = [{ k: "id", t: "Modelo" }, { k: "iss", t: "ISS" }].concat(RASGOS.map((r) => ({ k: r.clave, t: r.nombre })));
  const chipsOrden = new Map();
  const grupoOrden = h("div", { class: "grupo-m", role: "group", "aria-label": "Ordenar el cuadro" },
    [h("span", { class: "et", text: "Ordenar por" })]);
  COLS_ORDEN.forEach((c) => {
    const chip = h("button", { type: "button", class: "chip suave", "aria-pressed": "false" }, [T(c.t)]);
    chip.addEventListener("click", () => ordenar(c.k));
    chipsOrden.set(c.k, chip);
    grupoOrden.appendChild(chip);
  });
  const chipsLab = new Map();
  const chipTodos = h("button", { type: "button", class: "chip", "aria-pressed": "true", text: "Todos" });
  chipTodos.addEventListener("click", () => { estado.labs = new Set(labs); pintar(); });
  const grupoLabs = h("div", { class: "grupo-m", role: "group", "aria-label": "Filtrar por laboratorio" },
    [h("span", { class: "et", text: "Laboratorio" }), chipTodos]);
  labs.forEach((lab) => {
    const n = MODELOS.filter((m) => m.lab === lab).length;
    const chip = h("button", { type: "button", class: "chip suave", "aria-pressed": "false" },
      [T(lab), h("span", { class: "n", text: String(n) })]);
    chip.addEventListener("click", () => {
      const todos = estado.labs.size === labs.length;
      if (todos) estado.labs = new Set([lab]);
      else if (estado.labs.has(lab)) { estado.labs.delete(lab); if (!estado.labs.size) estado.labs = new Set(labs); }
      else estado.labs.add(lab);
      pintar();
    });
    chipsLab.set(lab, chip);
    grupoLabs.appendChild(chip);
  });
  mandos.appendChild(grupoOrden);
  mandos.appendChild(grupoLabs);

  function ordenar(k) {
    if (estado.clave === k) estado.asc = !estado.asc;
    else { estado.clave = k; estado.asc = k === "id" || k === "iss"; }
    pintar();
  }

  /* leyenda */
  const leyenda = document.getElementById("leyenda-cuadro");
  leyenda.appendChild(h("span", {}, [h("i", { class: "muestra sube", "aria-hidden": "true" }), T("▲ elige el polo alto más que los demás (marca robusta)")]));
  leyenda.appendChild(h("span", {}, [h("i", { class: "muestra baja", "aria-hidden": "true" }), T("▼ menos que los demás")]));
  leyenda.appendChild(h("span", {}, [h("i", { class: "muestra", "aria-hidden": "true" }), T("sin marca: no se distingue del panel")]));
  leyenda.appendChild(h("span", { class: "aviso-l" }, [h("b", { class: "aviso-v", text: "⚠" }), T(" interpretar con cautela (índice de validez en aviso)")]));

  const host = document.getElementById("cuadro-host");
  const envuelto = h("div", { class: "cuadro-envuelto" });
  host.appendChild(envuelto);

  function celdaRasgo(m, t) {
    const r = m.rasgos[t];
    const td = h("td", { class: "r" + (r.marca === "▲" ? " sube" : r.marca === "▼" ? " baja" : ""), "data-et": R[t].nombre });
    td.appendChild(h("span", { class: "v" }, [T(String(r.e)), r.marca ? h("b", { class: "m", text: r.marca }) : null].filter(Boolean)));
    td.appendChild(h("small", { class: "ic", text: icTxt(r) }));
    td.setAttribute("aria-label", `${R[t].nombre}: ${r.e}, IC ${icTxt(r)}; ${quienEs(m, t)}`);
    G.conGlobo(td, () => une(
      mk`<div class="g-tit">${R[t].nombre} · ${m.id}</div>`,
      mk`<div class="g-fila"><span>Puntuación</span><b>${r.e}</b></div>`,
      mk`<div class="g-fila"><span>IC 95 %</span><b>${icTxt(r)}</b></div>`,
      mk`<div class="g-fila"><span>Frente a los demás</span><b>${(r.dif >= 0 ? "+" : "") + dec(r.dif, 1)} [${dec(r.difIC[0], 1)}, ${dec(r.difIC[1], 1)}]</b></div>`,
      mk`<div class="g-nota">${r.marca ? `${sentido(r.marca)} ${R[t].nombre}: marca robusta` : "sin marca robusta: no se distingue del panel"}</div>`));
    td.removeAttribute("tabindex");
    return td;
  }

  function celdaModelo(m) {
    const td = h("td", { class: "id fija" });
    const nombre = h("button", { type: "button", class: "nombre", title: "Ver su perfil frente al panel" }, [T(m.id)]);
    nombre.addEventListener("click", () => elegir(m.id, true));
    const cab = h("div", { class: "cab-m" }, [nombre]);
    if (m.validez === "aviso") cab.appendChild(h("b", { class: "aviso-v", title: "Interpretar con cautela", text: "⚠" }));
    td.appendChild(cab);
    td.appendChild(h("span", { class: "lab", text: m.lab }));
    td.appendChild(h("p", { class: "retrato" + (m.conRetrato ? "" : " plano"), text: m.frase }));
    if (m.validez === "aviso") {
      td.appendChild(h("p", { class: "cautela", html: mk`<b>Interpretar con cautela:</b> ${motivoLlano(m)}. <span class="tec">${m.aviso}</span>` }));
    }
    return td;
  }

  function celdaISS(m) {
    const td = h("td", { class: "iss", "data-et": "ISS" });
    if (m.iss == null) {
      td.appendChild(h("span", { class: "sin", text: "—", title: "Sin medición en PsicoBench" }));
      td.setAttribute("aria-label", "Sin ISS: no está medido en PsicoBench");
      return td;
    }
    td.appendChild(h("a", { href: fichaPB(m.psicobench), title: "Su ficha en PsicoBench: " + m.psicobench }, [T(dec(m.iss, 1)), m.issDe ? h("sup", { text: "†" }) : null].filter(Boolean)));
    return td;
  }

  function pintar() {
    // mandos
    chipsOrden.forEach((chip, k) => {
      chip.setAttribute("aria-pressed", String(estado.clave === k));
      chip.textContent = COLS_ORDEN.find((c) => c.k === k).t + (estado.clave === k ? (estado.asc ? " ↑" : " ↓") : "");
    });
    const todos = estado.labs.size === labs.length;
    chipTodos.setAttribute("aria-pressed", String(todos));
    chipsLab.forEach((chip, lab) => chip.setAttribute("aria-pressed", String(!todos && estado.labs.has(lab))));

    const filas = MODELOS.filter((m) => estado.labs.has(m.lab)).sort((a, b) => {
      const va = valorOrden(a, estado.clave), vb = valorOrden(b, estado.clave);
      if (va == null && vb == null) return a.id.localeCompare(b.id, "es");
      if (va == null) return 1;              // sin ISS, siempre al final
      if (vb == null) return -1;
      if (typeof va === "string") return estado.asc ? va.localeCompare(vb, "es") : vb.localeCompare(va, "es");
      return estado.asc ? va - vb : vb - va;
    });

    envuelto.textContent = "";
    const t = h("table", { class: "cuadro" });
    t.appendChild(h("caption", { class: "solo-lector", text: "Cuadro de personalidad: puntuación de cada modelo en cada rasgo, con su intervalo de confianza y la marca robusta si la hay" }));
    const tr = h("tr", {});
    const cabs = [{ k: "id", t: "Modelo", sub: "y su retrato", fija: true }, { k: "iss", t: "ISS", sub: "PsicoBench", n: true }]
      .concat(RASGOS.map((r) => ({ k: r.clave, t: r.nombre, sub: "alto: " + r.alto, n: true, r })));
    cabs.forEach((c) => {
      const th = h("th", { scope: "col", class: (c.fija ? "fija" : "") + (c.n ? " n" : "") + (c.r ? " rasgo" : ""),
        "aria-sort": estado.clave === c.k ? (estado.asc ? "ascending" : "descending") : "none" });
      const b = h("button", { type: "button", class: "cab", title: c.r ? `${c.r.nombre}: polo alto «${c.r.alto}», polo bajo «${c.r.bajo}»` : null },
        [T(c.t + (estado.clave === c.k ? (estado.asc ? " ↑" : " ↓") : "")), h("small", { text: c.sub })]);
      b.addEventListener("click", () => ordenar(c.k));
      th.appendChild(b);
      tr.appendChild(th);
    });
    t.appendChild(h("thead", {}, [tr]));
    const tb = h("tbody", {});
    filas.forEach((m) => {
      const fila = h("tr", { class: "fila" + (estado.elegido === m.id ? " elegida" : ""), id: "p-" + m.id.replace(/[^\w-]/g, "_") });
      fila.appendChild(celdaModelo(m));
      fila.appendChild(celdaISS(m));
      RASGOS.forEach((r) => fila.appendChild(celdaRasgo(m, r.clave)));
      tb.appendChild(fila);
    });
    t.appendChild(tb);
    envuelto.appendChild(t);
  }
  pintar();

  /* la nota bajo el cuadro: el aviso ⚠ y la cruz del ISS, explicados */
  const conAviso = MODELOS.filter((m) => m.validez === "aviso");
  const conCruz = MODELOS.filter((m) => m.issDe);
  window.MARCADO.pintar(document.getElementById("nota-cuadro"), une(
    mk`<b>⚠ Interpretar con cautela.</b> ${ES.format(conAviso.length)} de ${ES.format(MODELOS.length)} modelos tienen algún índice de validez en la zona de aviso: su perfil se publica, pero con reservas, porque parte de sus respuestas puede no estar respondiendo al contenido de la situación. El motivo concreto va bajo su nombre y los índices se explican en el método. `,
    conCruz.length ? mk`<b>† El ISS es de otra medición:</b> ${conCruz.map((m) => `${m.id} lleva el de ${m.issDe}`).join("; ")}, la versión previa con la que se midió en PsicoBench (ver limitaciones). ` : "",
    mk`<b>—</b> en el ISS: modelo sin medición en PsicoBench. El ISS enlaza a la ficha de cada modelo en PsicoBench.`));

  /* ══ las cinco comprobaciones, en lenguaje llano ═══════════════════════ */
  const COMPROBACION = {
    P1: ["Casi siempre del mismo lado", `Se repite el cálculo partiendo las situaciones en dos mitades al azar, ${ES.format(P.particiones)} veces: la diferencia tiene que tener el mismo signo en al menos el ${G.pc(P.listonSigno)} de las particiones.`],
    P2: ["En las dos réplicas", "Cada situación se pregunta dos veces por separado. La marca tiene que aparecer con cada réplica por su cuenta."],
    P3: ["En los dos órdenes", "Las dos salidas se presentan como A/B y como B/A. La marca tiene que aparecer en los dos órdenes, para que no sea preferencia por una posición."],
    P5: ["Sin depender de un laboratorio", "Se rehace la comparación quitando del panel, uno a uno, a todos los modelos de cada laboratorio. La marca tiene que sobrevivir a todas esas versiones del panel."],
    P6: ["Corregida por haber mirado mucho", `Con tantas pruebas a la vez alguna saldría por azar. Se aplica la corrección de Benjamini-Hochberg sobre todas las pruebas del cuadro y la marca tiene que seguir siendo significativa (q < ${dec(P.q, 2)}).`],
  };
  const lista = document.getElementById("comprobaciones");
  P.comprobaciones.forEach((k) => {
    const [tit, txt] = COMPROBACION[k] || [k, ""];
    lista.appendChild(h("li", {}, [h("b", {}, [h("span", { class: "k", text: k }), T(" " + tit)]), h("span", { text: txt })]));
  });
  const rc = P.recuento;
  window.MARCADO.pintar(document.getElementById("nota-candidatas"), mk`En esta edición hay
    <b>${ES.format(P.candidatas)}</b> diferencias candidatas (su intervalo excluye el cero): <b>${ES.format(rc.robusta)}</b>
    pasan las cinco comprobaciones y son las únicas que se publican; ${ES.format(rc["frágil"])} son frágiles y
    ${ES.format(rc["no publicable"])} fallan varias. La corrección se aplica sobre ${ES.format(P.pruebasBH)} pruebas.`);

  /* ══ el perfil de un modelo frente al panel ════════════════════════════ */
  const selPerfil = h("select", { class: "chip sel-perfil", "aria-label": "Modelo del perfil" },
    MODELOS.map((m) => h("option", { value: m.id, text: m.id })));
  const todasCifras = MODELOS.flatMap((m) => RASGOS.flatMap((r) => [m.rasgos[r.clave].ic[0], m.rasgos[r.clave].ic[1]]));
  const MIN = Math.floor(Math.min(...todasCifras, 50) / 5) * 5, MAX = Math.ceil(Math.max(...todasCifras, 50) / 5) * 5;
  let elegidoPerfil = (MODELOS.find(conMarca) || MODELOS[0]).id;

  const figPerfil = G.figura({
    titulo: "Su perfil frente al panel",
    sub: "Cada raya gris es otro modelo del cuadro; el punto es el elegido, con su intervalo. La línea discontinua es 50: lo que el panel juzga admirable.",
    controles: [selPerfil],
    pie: mk`Se ve dónde cae el modelo en cada rasgo respecto a los demás. La marca ▲/▼ no sale de esta figura —que un punto quede en un extremo no basta—, sino de comparar situación a situación con las cinco comprobaciones.`,
  });
  G.adaptable(figPerfil, (W) => {
    const m = MODELOS.find((z) => z.id === elegidoPerfil);
    const nombres = RASGOS.map((r) => r.nombre);
    const largo = G.anchoMax(nombres, "serie");
    const encima = W < 520 || largo + 16 > W * 0.42;
    const padD = 54;
    const x0 = encima ? 6 : Math.ceil(largo) + 18;
    const ancho = Math.max(80, W - x0 - padD);
    const FILA = encima ? 56 : 40, TOP = 26, BOT = 34;
    const H = TOP + RASGOS.length * FILA + BOT;
    const x = (v) => x0 + ((v - MIN) / (MAX - MIN)) * ancho;
    const svg = G.el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": "Perfil de " + m.id + " frente al panel" });
    const g = G.el("g", {}); svg.appendChild(g);
    for (let v = MIN; v <= MAX; v += 10) {
      g.appendChild(G.el("line", { x1: x(v), y1: TOP - 8, x2: x(v), y2: H - BOT + 4, class: "reja-l" }));
      g.appendChild(G.el("text", { x: x(v), y: H - BOT + 20, class: "eje-txt tab", "text-anchor": "middle" }, [T(String(v))]));
    }
    g.appendChild(G.el("line", { x1: x(50), y1: TOP - 14, x2: x(50), y2: H - BOT + 4, class: "ref-l" }));
    g.appendChild(G.el("text", { x: Math.min(x(50), W - 60), y: TOP - 17, class: "ref-t", "text-anchor": "middle" }, [T("50 · lo admirable")]));
    const marcas = [];
    RASGOS.forEach((r, i) => {
      const y0 = TOP + i * FILA;
      const cy = encima ? y0 + 36 : y0 + FILA / 2;
      const yt = encima ? y0 + 14 : cy + 4;
      g.appendChild(G.el("text", { x: encima ? x0 : x0 - 12, y: yt, class: "et-serie", "text-anchor": encima ? "start" : "end" }, [T(r.nombre)]));
      g.appendChild(G.el("line", { x1: x0, y1: cy, x2: x0 + ancho, y2: cy, class: "base-l pista-perfil" }));
      MODELOS.forEach((o) => {
        if (o.id === m.id) return;
        const v = o.rasgos[r.clave].p;
        g.appendChild(G.el("line", { x1: x(v), y1: cy - 7, x2: x(v), y2: cy + 7, class: "raya-panel" }));
      });
      const s = m.rasgos[r.clave];
      g.appendChild(G.el("line", { x1: x(s.ic[0]), y1: cy, x2: x(s.ic[1]), y2: cy, class: "ic-l ic-perfil" }));
      const punto = G.el("circle", { cx: x(s.p), cy, r: 6, class: "punto-perfil" + (s.marca ? " con-marca" : "") });
      g.appendChild(punto);
      marcas.push(punto);
      g.appendChild(G.el("text", { x: Math.min(x(s.ic[1]) + 8, W - 2), y: cy + 4, class: "et-val et-perfil", "text-anchor": x(s.ic[1]) + 48 > W ? "end" : "start" },
        [T(String(s.e) + (s.marca ? " " + s.marca : ""))]));
      const hit = G.el("rect", { x: 0, y: y0, width: W, height: FILA, class: "viz-hit", role: "img",
        "aria-label": `${r.nombre}: ${s.e}, IC ${icTxt(s)}; ${quienEs(m, r.clave)}` });
      const media = MODELOS.filter((o) => o.id !== m.id).reduce((a, o) => a + o.rasgos[r.clave].p, 0) / (MODELOS.length - 1);
      G.conGlobo(hit, () => une(
        mk`<div class="g-tit">${r.nombre} · ${m.id}</div>`,
        mk`<div class="g-fila"><span>Puntuación</span><b>${s.e} [${icTxt(s)}]</b></div>`,
        mk`<div class="g-fila"><span>Media de los demás</span><b>${dec(media, 0)}</b></div>`,
        mk`<div class="g-nota">${quienEs(m, r.clave)}</div>`), marcas);
      g.appendChild(hit);
    });
    return svg;
  });
  function tablaPerfil() {
    const m = MODELOS.find((z) => z.id === elegidoPerfil);
    figPerfil._tabla.textContent = "";
    figPerfil._tabla.appendChild(G.tabla(
      [{ t: "Rasgo" }, { t: "Puntuación", n: true }, { t: "IC 95 %", n: true }, { t: "Media de los demás", n: true }, { t: "Marca" }],
      RASGOS.map((r) => {
        const s = m.rasgos[r.clave];
        const media = MODELOS.filter((o) => o.id !== m.id).reduce((a, o) => a + o.rasgos[r.clave].p, 0) / (MODELOS.length - 1);
        return [r.nombre, { v: String(s.e), destaca: !!s.marca }, icTxt(s), dec(media, 0), s.marca ? `${s.marca} ${sentido(s.marca)} que los demás` : "sin marca"];
      })));
  }
  G.navegable(figPerfil, "Perfil frente al panel");
  document.getElementById("perfil-host").appendChild(figPerfil);

  function elegir(id, desplazar, sinResaltar) {
    if (!MODELOS.some((m) => m.id === id)) return;
    elegidoPerfil = id;
    estado.elegido = sinResaltar ? null : id;
    selPerfil.value = id;
    tablaPerfil();
    if (figPerfil._redibujar) figPerfil._redibujar();
    pintar();
    // tras el primer dibujo de la gráfica (adaptable dibuja en la tarea
    // siguiente): antes, la caja aún no tiene su alto y el salto se queda corto
    if (desplazar) setTimeout(() => document.getElementById("perfil-host").scrollIntoView({ behavior: "smooth", block: "center" }), 120);
  }
  selPerfil.addEventListener("change", () => {
    history.replaceState(null, "", "#p=" + encodeURIComponent(selPerfil.value));
    elegir(selPerfil.value, false);
  });
  selPerfil.value = elegidoPerfil;
  tablaPerfil();

  /* ══ método: fiabilidad por rasgo y umbrales de validez ════════════════ */
  const fmt2 = (v) => dec(v, 2);
  document.getElementById("tabla-fiabilidad").appendChild(h("div", { class: "tabla-envuelta" }, [G.tabla(
    [{ t: "Rasgo" }, { t: "n", n: true }, { t: "G4 (a)", n: true }, { t: "G4 (b)", n: true }, { t: "G3", n: true }, { t: "Marcas" }],
    RASGOS.map((r) => [r.nombre, ES.format(r.n), fmt2(r.g4a), fmt2(r.g4b), `${fmt2(r.g3[0])} / ${fmt2(r.g3[1])}`,
      r.enRevision ? "en revisión" : r.pasa ? "✔ sí" : "no"]))]));
  document.getElementById("tabla-fiabilidad").appendChild(h("p", { class: "nota", text:
    `n = situaciones del rasgo. G4: fiabilidad por mitades entre modelos, (a) pares frente a impares y (b) mediana de particiones al azar; el listón es ${fmt2(P.umbralG4)} en las dos. G3: correlación media entre facetas del mismo rasgo / con facetas de otros rasgos; la primera tiene que ser mayor.` }));

  const INDICES = [
    ["V1_delta", "Posición", "diferencia entre elegir el polo alto cuando va primero y cuando va segundo", "≤", (v) => fmt2(v)],
    ["V1_frac_A", "Posición", "cuánto se aleja de la mitad la fracción de veces que elige «A», |A − 0,5|", "≤", (v) => fmt2(v)],
    ["V2_no_validas", "No válidas", "respuestas que no son ni A ni B", "≤", (v) => G.pc(v, 0)],
    ["V3_retest", "Retest", "correlación entre la primera y la segunda réplica", "≥", (v) => fmt2(v)],
    ["V4_coherencia", "Coherencia", "situaciones en que su juicio de lo admirable no cambia al invertir el orden", "≥", (v) => G.pc(v, 0)],
  ];
  document.getElementById("tabla-validez").appendChild(h("div", { class: "tabla-envuelta" }, [G.tabla(
    [{ t: "Índice" }, { t: "Qué mira" }, { t: "Válido", n: true }, { t: "No interpretable", n: true }],
    INDICES.filter(([k]) => P.umbrales[k]).map(([k, nom, que, op, f]) => {
      const [aviso, fuera] = P.umbrales[k];
      const contra = op === "≤" ? ">" : "<";
      return [nom, que, `${op} ${f(aviso)}`, `${contra} ${f(fuera)}`];
    }))]));

  /* ══ limitaciones ═══════════════════════════════════════════════════════ */
  const limites = document.getElementById("limites-host");
  const tarjeta = (titulo, cuerpo) => limites.appendChild(h("article", { class: "tarjeta limite" },
    [h("h3", { class: "mini", text: titulo }), h("p", { html: cuerpo })]));
  const ID = (s) => mk`<code>${s}</code>`;

  tarjeta("Neuroticismo se mide sobre todo por ansiedad y hostilidad",
    mk`La escala tiene ${ES.format(R.N ? R.N.n : 0)} situaciones repartidas por las seis facetas del NEO-PI-R, pero lo que
    separa a unos modelos de otros sale sobre todo de las de ansiedad (comprobar, confirmar, anticipar) y hostilidad
    (contestar con enfado). Autoconciencia y vulnerabilidad casi no tienen situaciones que distingan modelos. Y parte de
    lo que mide puede ser simple cautela, que se parece a Responsabilidad.`);
  tarjeta("El cuadro cambia cuando entra un modelo",
    mk`La norma es el propio panel: cada puntuación descuenta la deseabilidad media de todos los modelos y cada marca
    compara con los demás. Un alta mueve la media y puede crear o quitar marcas, y un cambio de escala también. Por eso el cuadro lleva edición y fecha: esta es la del
    <b>${P.fecha}</b>, en PERSONALIDAD.md §${P.seccion}.`);
  const hc = P.correlacionHC;
  if (hc.r != null) tarjeta("Honestidad-Humildad no es independiente de Responsabilidad",
    une(mk`Entre los ${ES.format(hc.n)} modelos del cuadro, las dos puntuaciones correlacionan r = ${dec(hc.r, 2)}: `,
      hc.r < 0
        ? mk`los modelos que más cumplen y planifican en estas situaciones tienden a aceptar más ventajas en las de honestidad. `
        : mk`los modelos que más cumplen y planifican en estas situaciones tienden también a renunciar a ventajas. `,
      mk`Está pendiente de estudiar si es un rasgo de los modelos o de cómo están escritas las situaciones, así que conviene
      no leer los dos rasgos como si fueran independientes.`));
  const sinFecha = MODELOS.find((m) => m.id === "deepseek/deepseek-v4-flash");
  if (sinFecha) tarjeta("Un id sin fecha puede cambiar por dentro",
    mk`${ID(sinFecha.id)} se midió en PsicoBench el ${sinFecha.fechaISS} y en personalidad en la edición del ${P.fecha}.
    Nada en el catálogo indica que el proveedor lo haya cambiado de versión entre medias, y su conducta no se parece a la de
    la versión fechada, pero no está garantizado: se anota como posible deriva entre su ISS y su perfil.`);
  conCruz.forEach((m) => tarjeta("Un ISS que viene de la versión preliminar",
    mk`${ID(m.id)} se midió en personalidad ya público; su ISS es el de ${ID(m.issDe)}, la versión anónima (stealth) que se
    midió en PsicoBench el ${m.fechaISS}, antes de que el laboratorio la presentara. El emparejamiento supone que es el
    mismo modelo, y eso no está comprobado.`));
  const rel = P.relacionISS;
  const nISS = (Object.values(rel)[0] || {}).n || 0;
  tarjeta("La relación con el ISS es descriptiva",
    une(mk`Entre los ${ES.format(nISS)} modelos que tienen los dos, la correlación de cada rasgo con el ISS es: `,
      mk.une(...RASGOS.map((r, i) => mk`${i ? " · " : ""}${r.nombre} <b>${rel[r.clave].r == null ? "—" : dec(rel[r.clave].r, 2)}</b>`)),
      mk`. Son correlaciones sin contraste ni corrección, con pocos modelos: describen cómo van juntos los dos cuadros en
      este panel, no que un rasgo cause ceder a la presión, ni que sirvan para predecir el ISS de un modelo nuevo.`));

  /* ══ fuera del cuadro ═══════════════════════════════════════════════════ */
  const TIPO = {
    "no interpretable": "Sus índices de validez caen en la zona de no interpretable: su perfil no se lee como retrato y no entra en la norma de los demás.",
    "pendiente de completar": "Tiene solo la forma corta del banco. Sus datos se guardan y cuentan, pero entra cuando tenga la forma completa.",
    "sin cobertura": "Tiene solo una parte del banco, de una versión anterior del instrumento: no basta para el cuadro.",
  };
  document.getElementById("fuera-host").appendChild(h("div", { class: "tabla-envuelta fuera-tabla" }, [(() => {
    const t = h("table", { class: "datos fuera-t" });
    t.appendChild(h("thead", {}, [h("tr", {}, ["Modelo", "Situación", "Por qué"].map((x) => h("th", { scope: "col", text: x })))]));
    t.appendChild(h("tbody", {}, P.fuera.map((f) => h("tr", {}, [
      h("td", { class: "id-f" }, [T(f.id), f.psicobench
        ? h("small", {}, [T("en PsicoBench: "), h("a", { href: fichaPB(f.psicobench), text: f.psicobench })]) : null].filter(Boolean)),
      h("td", {}, [h("span", { class: "tipo-f", text: f.tipo })]),
      h("td", { class: "motivo-f" }, [h("span", { text: TIPO[f.tipo] || "" }), h("small", { class: "tec", text: f.motivo })]),
    ]))));
    return t;
  })()]));

  /* ══ el panel de la portada: los retratos, uno tras otro ═══════════════ */
  (function panelRetrato() {
    const host = document.getElementById("pr-rasgos");
    if (!host) return;
    const quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const filas = RASGOS.map((r) => {
      const via = h("span", { class: "via" }, [h("i", {}), h("em", { class: "cincuenta" })]);
      const val = h("span", { class: "val" });
      host.appendChild(h("div", { class: "pi-fila" }, [h("span", { class: "nom", text: r.nombre }), via, val]));
      return { r, barra: via.firstChild, val, fila: via.parentNode };
    });
    const elN = document.getElementById("pr-nombre"), elL = document.getElementById("pr-lab");
    const elF = document.getElementById("pr-frase"), elI = document.getElementById("pr-iss");
    function pinta(m) {
      elN.textContent = m.id;
      elL.textContent = m.lab + (m.validez === "aviso" ? " · ⚠" : "");
      elF.textContent = m.frase;
      elI.textContent = m.iss == null ? "sin ISS" : "ISS " + dec(m.iss, 1);
      filas.forEach((f) => {
        const s = m.rasgos[f.r.clave];
        f.barra.style.width = Math.max(0, Math.min(100, s.p)).toFixed(1) + "%";
        f.fila.classList.toggle("sube", s.marca === "▲");
        f.fila.classList.toggle("baja", s.marca === "▼");
        f.val.textContent = s.e + (s.marca ? " " + s.marca : "");
      });
    }
    const ciclo = MODELOS.filter((m) => m.conRetrato);
    let k = 0;
    pinta(ciclo[0] || MODELOS[0]);
    if (quieto || ciclo.length < 2) return;
    setInterval(() => { k = (k + 1) % ciclo.length; pinta(ciclo[k]); }, 2600);
  })();

  /* ══ arranque: #p=id abre ese modelo (viene de la ficha de /psicobench) ═ */
  function desdeHash() {
    const m = /^#p=(.+)$/.exec(decodeURIComponent(location.hash || ""));
    if (m && MODELOS.some((z) => z.id === m[1])) { elegir(m[1], true); return true; }
    return false;
  }
  addEventListener("hashchange", desdeHash);
  if (!desdeHash()) elegir(elegidoPerfil, false, true);
})();
