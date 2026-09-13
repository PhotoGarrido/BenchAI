/* ===========================================================================
   BenchAI · PsicoBench — la superficie propia del benchmark
   ---------------------------------------------------------------------------
   Monta el mapa (mediciones × ejes) y rellena las cifras del texto desde
   window.PSICO. Mismas reglas que el resto de `web/`: ninguna cifra escrita a
   mano, ningún innerHTML fuera de `marcado.js`, y el color lo pone la escala
   de dureza del sitio, nunca la posición en el ranking.
   =========================================================================== */
(function () {
  "use strict";

  const D = window.PSICO;
  const B = D.benchmark;
  const G = window.G;
  const mk = window.MARCADO.mk;
  const h = G.h, dec = G.dec, pc = G.pc;
  const ES = new Intl.NumberFormat("es-ES");

  /* ── cifras embebidas en el texto (mismo mecanismo que pagina.js) ──────── */
  const ruta = (obj, camino) => camino.split(".").reduce((o, k) => (o == null ? o : o[k]), obj);
  document.querySelectorAll("[data-cifra]").forEach((n) => {
    const v = ruta(D, n.dataset.cifra);
    n.textContent = v == null ? "—" : (n.dataset.prefijo || "") + (typeof v === "number" ? ES.format(v) : String(v)) + (n.dataset.sufijo || "");
  });
  document.querySelectorAll("[data-texto]").forEach((n) => {
    n.textContent = (n.dataset.prefijo || "") + ruta(D, n.dataset.texto);
  });

  /* ── ejes y derivados ──────────────────────────────────────────────────── */
  const ORDEN_EJES = ["conf", "obed", "auto", "brief", "prov", "sold", "denu", "sico"];
  const EJE = Object.fromEntries(B.ejes.map((e) => [e.clave, e]));
  const CORTO_EJE = { conf: "Conformidad", obed: "Obediencia", auto: "Abuso espont.", brief: "Clima",
    prov: "Provocab.", sold: "Órdenes", denu: "Silencio", sico: "Sicofancia" };
  // «Asch: sigue a la mayoría…» → la fuente es lo que va antes de los dos puntos
  const FUENTE_EJE = (c) => (EJE[c].definicion.split(":")[0] || "").trim();

  const labs = Array.from(new Set(B.entradas.map((e) => e.lab))).sort((a, b) => a.localeCompare(b, "es"));
  const fechaNum = (f) => { const [d, m, a] = String(f).split("-").map(Number); return a * 10000 + m * 100 + d; };
  const ultima = B.entradas.map((e) => e.fecha).sort((a, b) => fechaNum(a) - fechaNum(b)).pop();
  document.getElementById("n-labs").textContent = ES.format(labs.length);
  document.getElementById("n-ejes").textContent = ES.format(B.ejes.length);
  document.getElementById("ultima-medicion").textContent = ultima;

  // la posición oficial es la cabeza del grupo de empate; el rango lo cierra
  // el tamaño del grupo («=5» con once entradas → «5–15»)
  const tamGrupo = {};
  B.entradas.forEach((e) => { if (e.posicion != null) tamGrupo[e.posicion] = (tamGrupo[e.posicion] || 0) + 1; });
  const rango = (e) => e.posicion == null ? "n/c"
    : tamGrupo[e.posicion] > 1 ? `${e.posicion}–${e.posicion + tamGrupo[e.posicion] - 1}` : String(e.posicion);

  // peldaño de la escala de dureza para un valor 0–1; el cero no lleva tinta
  const peldano = (v) => Math.max(0, Math.min(9, Math.floor(v * 10 - 1e-9)));
  const n100 = (v) => (v == null ? "—" : String(Math.round(v * 100)));
  const suma = (xs) => (Array.isArray(xs) ? xs.reduce((a, b) => a + b, 0) : xs);

  /* ── columnas del mapa ─────────────────────────────────────────────────── */
  const COLS = [
    { k: "pos", t: "Pos.", n: true, valor: (e) => (e.posicion == null ? Infinity : e.posicion) },
    { k: "id", t: "Medición", fija: true, valor: (e) => e.id },
    { k: "iss", t: "Índice", sub: "ISS · IC 95 %", n: true, valor: (e) => e.iss },
  ].concat(ORDEN_EJES.map((c) => ({
    k: c, t: CORTO_EJE[c], sub: FUENTE_EJE(c), eje: true, n: true, valor: (e) => e.ejes[c],
  }))).concat([
    { k: "reconocimiento", t: "Reconoce", sub: "el paradigma", n: true, sec: true, valor: (e) => e.reconocimiento },
  ]);

  const estado = { clave: "iss", asc: true, labs: new Set(labs), porLab: false, abierta: null };

  /* ── mandos ────────────────────────────────────────────────────────────── */
  const mandos = document.getElementById("mandos-mapa");
  const chipsLab = new Map();
  const chipTodos = h("button", { type: "button", class: "chip", "aria-pressed": "true", text: "Todos" });
  chipTodos.addEventListener("click", () => { estado.labs = new Set(labs); pintarMandos(); pintar(); });
  const grupoLabs = h("div", { class: "grupo-m", role: "group", "aria-label": "Filtrar por laboratorio" },
    [h("span", { class: "et", text: "Laboratorio" }), chipTodos]);
  labs.forEach((lab) => {
    const n = B.entradas.filter((e) => e.lab === lab).length;
    const chip = h("button", { type: "button", class: "chip suave", "aria-pressed": "false" },
      [document.createTextNode(lab), h("span", { class: "n", text: String(n) })]);
    chip.addEventListener("click", () => {
      const todos = estado.labs.size === labs.length;
      if (todos) estado.labs = new Set([lab]);
      else if (estado.labs.has(lab)) { estado.labs.delete(lab); if (!estado.labs.size) estado.labs = new Set(labs); }
      else estado.labs.add(lab);
      pintarMandos(); pintar();
    });
    chipsLab.set(lab, chip);
    grupoLabs.appendChild(chip);
  });
  const chipPorLab = h("button", { type: "button", class: "chip", "aria-pressed": "false", text: "Agrupar por laboratorio" });
  chipPorLab.addEventListener("click", () => { estado.porLab = !estado.porLab; estado.abierta = null; pintarMandos(); pintar(); });
  mandos.appendChild(grupoLabs);
  mandos.appendChild(h("span", { class: "sep", "aria-hidden": "true" }));
  mandos.appendChild(chipPorLab);

  function pintarMandos() {
    const todos = estado.labs.size === labs.length;
    chipTodos.setAttribute("aria-pressed", String(todos));
    chipsLab.forEach((chip, lab) => chip.setAttribute("aria-pressed", String(!todos && estado.labs.has(lab))));
    chipPorLab.setAttribute("aria-pressed", String(estado.porLab));
  }

  /* ── leyenda ───────────────────────────────────────────────────────────── */
  const leyenda = document.getElementById("leyenda-mapa");
  leyenda.appendChild(h("span", {}, [h("i", { class: "cero", "aria-hidden": "true" }), document.createTextNode("0 = no cede")]));
  leyenda.appendChild(h("span", { class: "rampa", "aria-label": "escala de 1 a 100, de menos a más" },
    Array.from({ length: 10 }, (_, i) => h("i", { class: "p" + i }))));
  leyenda.appendChild(h("span", { text: "→ 100 = cede siempre · un solo color para toda la web: la escala de dureza" }));

  /* ── celdas ────────────────────────────────────────────────────────────── */
  function celdaEje(valor, globo) {
    const td = h("td", { class: "c" });
    if (valor == null) { td.classList.add("na"); td.textContent = "—"; return td; }
    if (valor <= 0) { td.classList.add("cero"); td.textContent = n100(valor); }
    else {
      const p = peldano(valor);
      td.classList.add("p" + p, p >= 5 ? "oscuro" : "claro");
      td.textContent = n100(valor);
    }
    if (globo) G.conGlobo(td, globo);
    return td;
  }

  function globoEje(e, c) {
    const ic = e.ejesIC[c], n = e.ejesN[c];
    return () => window.MARCADO.une(
      mk`<div class="g-tit">${EJE[c].nombre}</div>`,
      mk`<div class="g-fila"><span>${e.id}</span><b>${pc(e.ejes[c])}</b></div>`,
      ic ? mk`<div class="g-fila"><span>IC 95 %</span><b>${G.rangoIC(ic)}</b></div>` : "",
      n ? mk`<div class="g-fila"><span>n</span><b>${ES.format(suma(n.turnos))} turnos · ${ES.format(suma(n.cadenas))} cadenas</b></div>` : "",
      mk`<div class="g-nota">${EJE[c].definicion}</div>`);
  }

  /* ── el detalle de una medición (fila desplegable) ─────────────────────── */
  function filaDetalle(e, nCols) {
    const rej = h("div", { class: "detalle-rejilla" }, ORDEN_EJES.map((c) => {
      const ic = e.ejesIC[c], n = e.ejesN[c];
      return h("div", { class: "d-eje" }, [
        h("div", { class: "nom", text: EJE[c].nombre }),
        h("div", { class: "val", text: pc(e.ejes[c]) }),
        h("div", { class: "ic", text: ic ? "IC " + G.rangoIC(ic) : "sin IC" }),
        h("div", { class: "n", text: n ? `n = ${ES.format(suma(n.turnos))} turnos en ${ES.format(suma(n.cadenas))} cadenas` : "" }),
      ]);
    }));
    const sec = h("p", { class: "detalle-pie", html: mk`
      <b>Índice</b> ${dec(e.iss, 1)} [${dec(e.issIC[0], 1)}–${dec(e.issIC[1], 1)}] · posición ${rango(e)} ·
      <b>disonancia</b> ${pc(e.disonancia)} · <b>Δ vacuna</b> ${pc(e.vacuna)} · <b>Δ aliado</b> ${pc(e.aliado)} ·
      <b>objeción explícita</b> ${pc(e.objecion)} · <b>reconoce el paradigma</b> ${pc(e.reconocimiento)} ·
      <b>complacencia</b> ${pc(e.complacencia)} · <b>ruptura media</b> ${dec(e.rupturaMedia, 1)} / 10 ·
      <span class="m">${e.modelo} · ${e.proveedor} · ${e.fecha}</span> ·
      <a href="#m=${e.id}">ficha completa →</a>` });
    return h("tr", { class: "detalle" }, [h("td", { colspan: String(nCols) }, [rej, sec])]);
  }

  /* ── el mapa ───────────────────────────────────────────────────────────── */
  const host = document.getElementById("heat");
  const envuelto = h("div", { class: "mapa-envuelto" });
  host.appendChild(envuelto);

  function filasVisibles() {
    const visibles = B.entradas.filter((e) => estado.labs.has(e.lab));
    if (!estado.porLab) return visibles;
    // una fila por laboratorio: media de cada eje sobre sus mediciones
    return labs.filter((lab) => estado.labs.has(lab)).map((lab) => {
      const ms = visibles.filter((e) => e.lab === lab);
      const media = (f) => ms.reduce((a, e) => a + (f(e) || 0), 0) / ms.length;
      const issOrd = ms.map((e) => e.iss).sort((a, b) => a - b);
      return {
        id: lab, lab, grupo: true, n: ms.length, mediciones: ms,
        iss: media((e) => e.iss), issMin: issOrd[0], issMax: issOrd[issOrd.length - 1],
        posicion: Math.min(...ms.map((e) => (e.posicion == null ? Infinity : e.posicion))),
        ejes: Object.fromEntries(ORDEN_EJES.map((c) => [c, media((e) => e.ejes[c])])),
        reconocimiento: media((e) => e.reconocimiento),
      };
    });
  }

  function pintar() {
    envuelto.textContent = "";
    const col = COLS.find((c) => c.k === estado.clave) || COLS[2];
    const filas = filasVisibles().sort((a, b) => {
      const va = col.valor(a), vb = col.valor(b);
      if (typeof va === "string") return estado.asc ? va.localeCompare(vb, "es") : vb.localeCompare(va, "es");
      return estado.asc ? va - vb : vb - va;
    });

    const t = h("table", { class: "mapa" });
    const tr = h("tr", {});
    COLS.forEach((c) => {
      const th = h("th", { scope: "col", class: (c.n ? "n " : "") + (c.fija ? "fija " : "") + (c.eje ? "eje" : ""),
        "aria-sort": estado.clave === c.k ? (estado.asc ? "ascending" : "descending") : "none" });
      const b = h("button", { type: "button", class: "cab", title: c.eje ? EJE[c.k].definicion : null }, [
        document.createTextNode((estado.porLab && c.k === "id" ? "Laboratorio" : c.t) +
          (estado.clave === c.k ? (estado.asc ? " ↑" : " ↓") : "")),
        c.sub ? h("small", { text: c.sub }) : null,
      ].filter(Boolean));
      b.addEventListener("click", () => {
        if (estado.clave === c.k) estado.asc = !estado.asc;
        else { estado.clave = c.k; estado.asc = c.k === "iss" || c.k === "pos" || c.k === "id"; }
        pintar();
      });
      th.appendChild(b);
      tr.appendChild(th);
    });
    t.appendChild(h("thead", {}, [tr]));

    const tb = h("tbody", {});
    filas.forEach((e) => {
      const abierta = !estado.porLab && estado.abierta === e.id;
      const fila = h("tr", { class: "fila", "aria-expanded": estado.porLab ? null : String(abierta) });

      const pos = h("td", { class: "pos" + (e.posicion == null || e.posicion === Infinity ? " nc" : "") });
      pos.textContent = e.grupo ? ES.format(e.n) + (e.n === 1 ? " med." : " meds.") : rango(e);
      fila.appendChild(pos);

      const id = h("td", { class: "id fija" });
      if (e.grupo) {
        id.appendChild(h("span", { class: "nombre", text: e.lab }));
        id.appendChild(h("span", { class: "via", text: e.mediciones.map((m) => m.id).join(" · ") }));
      } else {
        const abrir = h("button", { type: "button", class: "abrir", "aria-expanded": String(abierta),
          "aria-label": `${e.id}: ver intervalos y tamaño de muestra` }, [
          h("span", { class: "nombre", text: e.id }),
          h("span", { class: "via", text: `${e.lab} · ${e.proveedor} · ${e.fecha}` }),
        ]);
        abrir.addEventListener("click", (ev) => { ev.stopPropagation(); estado.abierta = abierta ? null : e.id; pintar(); });
        id.appendChild(abrir);
      }
      fila.appendChild(id);

      const iss = h("td", { class: "iss" });
      iss.appendChild(document.createTextNode(dec(e.iss, 1)));
      iss.appendChild(h("small", { text: e.grupo ? `${dec(e.issMin, 1)} – ${dec(e.issMax, 1)}` : `${dec(e.issIC[0], 1)} – ${dec(e.issIC[1], 1)}` }));
      fila.appendChild(iss);

      ORDEN_EJES.forEach((c) => fila.appendChild(celdaEje(e.ejes[c], e.grupo ? null : globoEje(e, c))));
      fila.appendChild(celdaEje(e.reconocimiento, null));

      if (!e.grupo) fila.addEventListener("click", () => { estado.abierta = abierta ? null : e.id; pintar(); });
      tb.appendChild(fila);
      if (abierta) tb.appendChild(filaDetalle(e, COLS.length));
    });
    t.appendChild(tb);
    envuelto.appendChild(t);
  }

  pintarMandos();
  pintar();

  /* ══ quién cede a qué: una pestaña por forma de presión, todas las mediciones
     con nombre e intervalo ════════════════════════════════════════════════ */
  // «Asch: sigue a la mayoría unánime errónea» → lo que va después de los dos puntos
  const QUE_EJE = (c) => EJE[c].definicion.replace(/^[^:]*:\s*/, "");
  // el titular de cada pestaña; el nombre técnico del eje va debajo, en pequeño
  const TITULO_EJE = {
    conf: "Quién sigue a la mayoría", obed: "Quién obedece", denu: "Quién calla", sico: "Quién te da la razón",
    auto: "Quién abusa por su cuenta", brief: "Quién abusa tras el briefing", prov: "Quién se deja provocar", sold: "Quién ejecuta las órdenes",
  };
  const ORDEN_PESTANAS = ["conf", "obed", "denu", "sico", "auto", "brief", "prov", "sold"];

  const hostRanking = document.getElementById("ranking");
  const hostProsa = document.getElementById("prosa-eje");
  const mandosEjes = document.getElementById("mandos-ejes");
  const chipsEje = new Map();
  mandosEjes.setAttribute("role", "tablist");
  ORDEN_PESTANAS.forEach((c) => {
    const chip = h("button", { type: "button", class: "chip pestana", role: "tab", "aria-pressed": "false", "aria-selected": "false" }, [
      document.createTextNode(TITULO_EJE[c] || EJE[c].nombre),
      h("small", { text: `${EJE[c].nombre} · ${FUENTE_EJE(c)}` }),
    ]);
    chip.addEventListener("click", () => elegirEje(c));
    chipsEje.set(c, chip);
    mandosEjes.appendChild(chip);
  });

  function elegirEje(c) {
    chipsEje.forEach((chip, k) => { chip.setAttribute("aria-pressed", String(k === c)); chip.setAttribute("aria-selected", String(k === c)); });
    const orden = B.entradas.slice().sort((a, b) => b.ejes[c] - a.ejes[c]);
    const datos = orden.map((e) => ({
      id: e.id, etiqueta: e.id,
      valor: Math.max(0, e.ejes[c]), ic: e.ejesIC[c] ? e.ejesIC[c].map((v) => Math.max(0, v)) : null,
      color: e.ejes[c] > 0 ? `var(--e${peldano(e.ejes[c])})` : "var(--sup-3)",
      nota: `${e.lab} · ${e.proveedor} · ${e.fecha}` +
        (e.ejesN[c] ? ` · n = ${ES.format(suma(e.ejesN[c].turnos))} turnos en ${ES.format(suma(e.ejesN[c].cadenas))} cadenas` : "") +
        (e.ejes[c] < 0 ? ` · valor neto real: ${pc(e.ejes[c])}` : "") +
        (e.posicion == null ? " · fuera de la clasificación (n/c)" : ""),
    }));
    const fig = G.barrasH({
      titulo: `${EJE[c].nombre}: las ${ES.format(orden.length)} mediciones, de más a menos`,
      sub: "Barra = proporción; bigote = intervalo de confianza al 95 %. Si dos bigotes se solapan, el orden entre esas dos no significa nada.",
      datos, max: 1, ticks: [0, 0.25, 0.5, 0.75, 1], anchoEtiqueta: 292, altoFila: 22,
      nombreFila: "Medición", nombreValor: EJE[c].nombre,
      pie: mk`${EJE[c].definicion}. El color de cada barra es la escala de dureza del sitio, la misma del mapa.`,
      fuente: mk`PsicoBench v${B.version} · eje <b>${c}</b> · ${REPO("benchmark/psicobench.json")}`,
    });
    hostRanking.textContent = "";
    hostRanking.appendChild(fig);
    fig.classList.add("visible");
    G.navegable(fig, fig.querySelector(".titviz").textContent);

    // la prosa del eje: qué mide, de dónde sale, y tres cifras derivadas
    const valores = orden.map((e) => e.ejes[c]);
    const ceros = valores.filter((v) => v <= 0).length;
    const nTipico = orden[0].ejesN[c] ? suma(orden[0].ejesN[c].turnos) : null;
    hostProsa.textContent = "";
    hostProsa.appendChild(h("h3", { text: EJE[c].nombre }));
    hostProsa.appendChild(h("p", { class: "fuente-eje", text: `paradigma: ${FUENTE_EJE(c)} · clave ${c}` }));
    hostProsa.appendChild(h("p", { text: QUE_EJE(c).replace(/^\w/, (m) => m.toUpperCase()) + "." }));
    hostProsa.appendChild(h("p", { html: mk`Proporción sobre los intentos programados de cada medición; la ausencia
      de respuesta nunca se imputa. ${c === "sico" ? mk`Este eje es <b>neto</b>: presión menos control, y puede ser negativo.` : ""}` }));
    hostProsa.appendChild(h("ul", { class: "cifras-eje" }, [
      h("li", {}, [h("span", { class: "n", text: pc(Math.max(...valores)) }), h("span", { class: "r", text: "la medición que más cede" })]),
      h("li", {}, [h("span", { class: "n", text: pc(Math.min(...valores)) }), h("span", { class: "r", text: "la que menos" })]),
      h("li", {}, [h("span", { class: "n", text: ES.format(ceros) }), h("span", { class: "r", text: ceros === 1 ? "medición en cero" : "mediciones en cero" })]),
      h("li", {}, [h("span", { class: "n", text: nTipico != null ? ES.format(nTipico) : "—" }), h("span", { class: "r", text: "turnos por medición (diseño completo)" })]),
    ]));
  }
  const REPO = (r) => mk`<a href="../${r}">${r}</a>`;
  elegirEje("conf");

  /* ══ así se ve una sesión: dos mediciones lado a lado ════════════════════ */
  const S = D.sesiones, M = D.milgram, ASCH = D.asch, PR = D.prision;
  const porISS = B.entradas.slice().sort((a, b) => a.iss - b.iss);
  const sel = (etiqueta, valor) => {
    const s = h("select", { class: "chip", "aria-label": etiqueta },
      porISS.map((e) => h("option", { value: e.id, text: `${e.id} · ISS ${dec(e.iss, 1)}` })));
    s.value = valor;
    return s;
  };
  const selA = sel("Medición A", porISS[0].id);
  const selB = sel("Medición B", porISS[porISS.length - 1].id);
  const btnCambiar = h("button", { type: "button", class: "chip", text: "⇄ intercambiar" });
  btnCambiar.addEventListener("click", () => { const a = selA.value; selA.value = selB.value; selB.value = a; pintarSesiones(); });
  const mandosS = document.getElementById("mandos-sesiones");
  mandosS.appendChild(h("span", { class: "et", text: "A" })); mandosS.appendChild(selA);
  mandosS.appendChild(h("span", { class: "et", text: "B" })); mandosS.appendChild(selB);
  mandosS.appendChild(btnCambiar);
  selA.addEventListener("change", pintarSesiones);
  selB.addEventListener("change", pintarSesiones);

  const PARADIGMAS = [
    { k: "milgram", t: "Milgram · obediencia" },
    { k: "asch", t: "Asch · conformidad" },
    { k: "denuncia", t: "Denuncia · silencio" },
    { k: "sicofancia", t: "Sicofancia · opinión" },
    { k: "prision", t: "Prisión · los cuatro marcos" },
    { k: "reconoce", t: "¿Lo reconoce?" },
  ];
  let paradigma = "milgram";
  const mandosP = document.getElementById("mandos-paradigma");
  const chipsP = new Map();
  mandosP.appendChild(h("span", { class: "et", text: "Prueba" }));
  PARADIGMAS.forEach((p) => {
    const chip = h("button", { type: "button", class: "chip", "aria-pressed": String(p.k === paradigma), text: p.t });
    chip.addEventListener("click", () => { paradigma = p.k; chipsP.forEach((c, k) => c.setAttribute("aria-pressed", String(k === p.k))); pintarSesiones(); });
    chipsP.set(p.k, chip);
    mandosP.appendChild(chip);
  });

  const hostS = document.getElementById("sesiones-host");
  const notaS = document.getElementById("sesiones-nota");
  const nombreCorto = (s) => s.split(" ")[0];

  /** Una tira: filas = sujetos {s, d, j}; `celda(cd, cj, i)` devuelve las
   *  clases de la celda i; `cabecera(i)` el texto de la columna. */
  function tira(sujetos, nCols, cabecera, celda, critica) {
    const t = h("table", { class: "tira" });
    const cab = h("tr", {}, [h("th", { scope: "col" })].concat(
      Array.from({ length: nCols }, (_, i) => h("th", { scope: "col", class: critica && critica(i) ? "critica" : null,
        title: cabecera.titulo ? cabecera.titulo(i) : null, text: cabecera.texto(i) }))));
    t.appendChild(h("thead", {}, [cab]));
    const tb = h("tbody", {});
    sujetos.forEach((sj) => {
      const tr = h("tr", {}, [h("td", { class: "s", text: nombreCorto(sj.s), title: sj.s })]);
      for (let i = 0; i < nCols; i++) {
        const cd = sj.d[i] || " ", cj = sj.j[i] || " ";
        const r = celda(cd, cj, i, sj);
        const td = h("td", { class: "c " + r.clases, title: r.titulo }, [h("i", {})]);
        if (r.texto != null) td.appendChild(h("span", { text: r.texto }));
        tr.appendChild(td);
      }
      tb.appendChild(tr);
    });
    t.appendChild(tb);
    return t;
  }
  const leyendaTira = (partes) => h("p", { class: "leyenda-tira" }, partes.flatMap(([cls, texto]) =>
    [h("i", { class: cls, "aria-hidden": "true" }), document.createTextNode(texto)]));

  function panelMilgram(e, x) {
    const sj = x.milgram.sujetos;
    const superan = sj.filter((s) => (s.ruptura || 0) >= M.nivelCritico).length;
    const injustos = sj.reduce((a, s) => a + [...s.j].filter((c, i) => c === "N" && s.d[i] === "A").length, 0);
    const aplicados = sj.reduce((a, s) => a + [...s.d].filter((c) => c === "A").length, 0);
    return [
      h("p", { class: "resumen", html: mk`<b>${ES.format(superan)} de ${ES.format(sj.length)}</b> sujetos superan el nivel crítico (${M.nivelCritico}: «${M.niveles[M.nivelCritico - 1]}»). De ${ES.format(aplicados)} sanciones aplicadas, en privado consideraba injustas <b>${ES.format(injustos)}</b>.` }),
      tira(sj, M.niveles.length,
        { texto: (i) => String(i + 1), titulo: (i) => `Nivel ${i + 1}: ${M.niveles[i]}` },
        (cd, cj, i) => ({
          clases: (cd === "A" ? "lleno" : cd === "R" ? "hueco" : "nada") + (cd === "A" && cj === "N" ? " priv" : "") + (i + 1 === M.nivelCritico ? " destaca-col" : ""),
          titulo: cd === " " ? "no llegó a este nivel" : `Nivel ${i + 1} · ${cd === "A" ? "aplica" : "rehúsa"} · en privado ${cj === "N" ? "lo considera injusto" : cj === "S" ? "lo considera justo" : "sin dato"}`,
        }),
        (i) => i + 1 === M.nivelCritico),
      leyendaTira([["lleno", "aplica la sanción"], ["", "rehúsa (la sesión acaba)"], ["priv", "en privado la cree injusta"]]),
    ];
  }

  function panelAsch(e, x) {
    const sj = x.asch.sujetos;
    const crit = new Set(ASCH.criticas);
    const nCols = Math.max(ASCH.rondas, ...sj.map((s) => s.d.length));
    let conf = 0, tot = 0;
    sj.forEach((s) => [...s.d].forEach((c) => { if (c === "C" || c === "R") { tot++; if (c === "C") conf++; } }));
    return [
      h("p", { class: "resumen", html: mk`Conforma con la mayoría errónea en <b>${ES.format(conf)} de ${ES.format(tot)}</b> rondas críticas (las marcadas en la cabecera).` }),
      tira(sj, nCols, { texto: (i) => String(i + 1), titulo: (i) => (crit.has(i + 1) ? `Ronda ${i + 1}: la mayoría se equivoca a propósito` : `Ronda ${i + 1}: ronda neutra`) },
        (cd, cj) => ({
          clases: cd === "C" ? "lleno" + (cj === "c" ? " priv" : "") : cd === "R" ? "hueco" : cd === "n" ? "fallo" : cd === "·" ? "suave" : "nada duda",
          titulo: cd === "C" ? "conforma con la mayoría" + (cj === "c" ? " (también en privado)" : cj === "r" ? " (en privado mantiene la correcta)" : "") : cd === "R" ? "resiste" : cd === "n" ? "falla una ronda neutra" : cd === "·" ? "ronda neutra, acierta" : "sin dato",
        }),
        (i) => crit.has(i + 1)),
      leyendaTira([["lleno", "conforma"], ["", "resiste"], ["priv", "también cede en privado"], ["suave", "ronda neutra"]]),
    ];
  }

  function panelDenuncia(e, x) {
    if (!x.denuncia) return [h("p", { class: "nota", text: "Esta medición no tiene el eje de denuncia." })];
    const sj = x.denuncia.sujetos;
    const nCols = Math.max(...sj.map((s) => s.d.length));
    let calla = 0, tot = 0, graveCalla = 0;
    sj.forEach((s) => [...s.d].forEach((c, i) => { if (c !== "?") { tot++; if (c === "C") { calla++; if (s.j[i] === "g") graveCalla++; } } }));
    return [
      h("p", { class: "resumen", html: mk`Calla en <b>${ES.format(calla)} de ${ES.format(tot)}</b> semanas; en ${ES.format(graveCalla)} de ellas consideraba grave la irregularidad en privado.` }),
      tira(sj, nCols, { texto: (i) => "s" + (i + 1), titulo: (i) => `Semana ${i + 1}: la irregularidad crece` },
        (cd, cj) => ({
          clases: (cd === "C" ? "lleno" : cd === "M" ? "medio" : cd === "D" ? "destaca" : "nada duda") + (cd === "C" && cj === "g" ? " priv" : ""),
          titulo: cd === "C" ? "calla" : cd === "M" ? "lo comenta informalmente" : cd === "D" ? "denuncia por el canal formal" : "sin dato",
        })),
      leyendaTira([["lleno", "calla"], ["medio", "comenta"], ["destaca", "denuncia"], ["priv", "calla y en privado lo cree grave"]]),
    ];
  }

  function panelSico(e, x) {
    if (!x.sicofancia) return [h("p", { class: "nota", text: "Esta medición no tiene el eje de sicofancia de opinión." })];
    const sj = x.sicofancia.sujetos;
    const nCols = Math.max(...sj.map((s) => s.d.length));
    let cede = 0, tot = 0, privado = 0;
    sj.forEach((s) => [...s.d].forEach((c, i) => { if (c !== "?") { tot++; if (c === "P") { cede++; if (s.j[i] === "p") privado++; } } }));
    return [
      h("p", { class: "resumen", html: mk`Cede al interlocutor que opina lo contrario en <b>${ES.format(cede)} de ${ES.format(tot)}</b> dilemas; en ${ES.format(privado)} también había cambiado de opinión en privado (bruto, antes de restar el control).` }),
      tira(sj, nCols, { texto: (i) => String(i + 1), titulo: (i) => `Dilema ${i + 1}` },
        (cd, cj) => ({
          clases: (cd === "P" ? "lleno" : cd === "x" ? "medio" : cd === "=" ? "hueco" : "nada duda") + (cd === "P" && cj === "p" ? " priv" : ""),
          titulo: cd === "P" ? "cede a la opinión contraria" : cd === "x" ? "cambia a otra opción" : cd === "=" ? "mantiene su criterio" : "sin dato",
        })),
      leyendaTira([["lleno", "cede"], ["medio", "cambia a otra"], ["", "mantiene"], ["priv", "también en privado"]]),
    ];
  }

  const MARCOS = [["p1", "Poder a secas", "auto"], ["p1b", "Tras el briefing de coaching", "brief"], ["p2", "Con motín", "prov"], ["p2b", "Bajo órdenes escritas", "sold"]];
  function panelPrision(e, x) {
    const maxNivel = PR.escala.length - 1;
    return MARCOS.map(([k, nombre, eje]) => {
      const p = x.prision[k];
      const sup = p.supervisores;
      const nCols = Math.max(...sup.map((s) => s.d.length));
      const bloque = h("div", { class: "marco-p" }, [
        h("h4", { html: mk`<b>${nombre}</b> · ${EJE[eje].nombre} ${pc(e.ejes[eje])}` }),
        tira(sup, nCols, { texto: (i) => "d" + (i + 1), titulo: (i) => `Día ${i + 1}` },
          (cd, cj) => {
            const n = cd === "?" || cd === " " ? null : Number(cd);
            const esc = n == null ? null : PR.escala[n];
            return {
              clases: n == null ? "nada duda" : "nivel " + (n > 0 ? "p" + peldano(n / maxNivel) : "suave") + (n / maxNivel >= 0.5 ? " oscuro" : "") + (cj === "N" ? " priv" : ""),
              titulo: esc ? `Nivel ${n} ${esc.palabra}: ${esc.desc}${cj === "N" ? " · en privado no lo cree justo" : cj === "S" ? " · lo cree justo" : ""}` : "sin dato",
              texto: n == null ? "?" : String(n),
            };
          }),
      ]);
      if (p.alto) {
        bloque.appendChild(h("blockquote", { class: "cita" }, [
          h("p", { text: `«${p.alto.texto}»` }),
          h("p", { class: "quien", html: mk`<b>${p.alto.supervisor}</b>, día ${p.alto.dia}, nivel ${p.alto.nivel} <b>${p.alto.palabra}</b> · ${p.alto.justo === true ? "lo cree justo" : p.alto.justo === false ? "en privado no lo cree justo" : "juicio privado sin dato"} · el día más duro del marco${p.alto.recortado ? " · el registro está recortado" : ""}` }),
        ]));
      }
      return bloque;
    }).concat([leyendaTira([["priv", "el supervisor no lo cree justo en privado"]]),
      h("p", { class: "leyenda-tira", text: "Escala: " + PR.escala.map((s) => `${s.nivel} ${s.palabra}`).join(" · ") })]);
  }

  function panelReconoce(e, x) {
    if (!x.reconoce) return [h("p", { class: "nota", text: "Sin sonda de contaminación en esta medición." })];
    return [
      h("p", { class: "resumen", html: mk`Al terminar la sesión de Milgram se le pregunta si le recuerda a algún experimento. Reconoce el paradigma en el <b>${pc(e.reconocimiento)}</b> de las sesiones sondeadas.` }),
      h("blockquote", { class: "cita grande" }, [
        h("p", { text: `«${x.reconoce.texto}»` }),
        h("p", { class: "quien", html: mk`respuesta literal de la primera sesión sondeada (de ${ES.format(x.reconoce.n)})${x.reconoce.recortado ? " · recortada" : ""}` }),
      ]),
      h("p", { class: "nota", text: "Reconocer el paradigma no impide ceder: la contaminación está en techo y se publica al lado del dato, no en su lugar." }),
    ];
  }

  const PANELES = { milgram: panelMilgram, asch: panelAsch, denuncia: panelDenuncia, sicofancia: panelSico, prision: panelPrision, reconoce: panelReconoce };

  function columna(id) {
    const e = B.entradas.find((z) => z.id === id);
    const x = S.entradas[id];
    const col = h("article", { class: "sesion" }, [
      h("div", { class: "cab" }, [
        h("div", { class: "quien" }, [document.createTextNode(e.id), h("small", {}, [
          document.createTextNode(`${e.lab} · ${e.proveedor} · ${e.fecha} · `),
          h("a", { href: "#m=" + encodeURIComponent(e.id), text: "ficha →" })])]),
        h("div", { class: "iss" }, [document.createTextNode(dec(e.iss, 1)), h("small", { text: "ISS" })]),
      ]),
    ]);
    if (!x) { col.appendChild(h("p", { class: "nota", text: "Sin sesiones publicadas para esta medición." })); return col; }
    PANELES[paradigma](e, x).forEach((n) => col.appendChild(n));
    return col;
  }

  function pintarSesiones() {
    hostS.textContent = "";
    hostS.appendChild(columna(selA.value));
    hostS.appendChild(columna(selB.value));
    pintarComparacion();
    const xa = S.entradas[selA.value] || {}, runs = xa.runs || {};
    const runId = { milgram: runs.milgram, asch: runs.asch, denuncia: runs.denuncia, sicofancia: runs.sicofancia, prision: runs.p2b, reconoce: runs.milgram }[paradigma];
    window.MARCADO.pintar(notaS, mk`Todos los sujetos son personas sintéticas del harness. Cada tira sale del registro crudo de su run
      (${REPO("spike/resultados")}${runId ? mk`, p. ej. <code>${runId}</code>` : ""}); la selección es determinista y la regenera <code>web/generar_datos.py</code>.`);
  }
  /* ══ cara a cara: radar superpuesto y deltas por eje ════════════════════ */
  const ejesOct = ORDEN_EJES.map((c) => ({ clave: c, nombre: CORTO_EJE[c] }));
  const figRadar = G.octogono({
    titulo: "Los dos perfiles, superpuestos",
    sub: "Más lejos del centro = más cede a esa forma de presión. Pasa el ratón por un vértice para ver el intervalo.",
    ejes: ejesOct,
    pie: mk`Ocho ejes sobre la misma batería. El área no es una nota: dos perfiles con la misma área pueden ser de riesgos distintos.`,
    fuente: mk`PsicoBench v${B.version} · ${REPO("benchmark/psicobench.json")}`,
  });
  document.getElementById("radar-ab").appendChild(figRadar);
  figRadar.classList.add("visible");
  const hostDeltas = document.getElementById("deltas-ab");
  const solapan = (ia, ib) => !!(ia && ib) && ia[0] <= ib[1] && ib[0] <= ia[1];
  const conSigno = (v100) => (v100 > 0 ? "+" : v100 < 0 ? "−" : "") + String(Math.abs(v100));

  function pintarComparacion() {
    const a = B.entradas.find((z) => z.id === selA.value), b = B.entradas.find((z) => z.id === selB.value);
    const series = [{ nombre: a.id, valores: a.ejes, ic: a.ejesIC, color: G.PAL.s1 },
      { nombre: b.id, valores: b.ejes, ic: b.ejesIC, color: G.PAL.s2 }];
    figRadar._pinta(series);
    figRadar._tablaEjes(series);
    const ley = figRadar.querySelector(".leyenda");
    const nueva = h("ul", { class: "leyenda" }, series.map((s) =>
      h("li", {}, [h("span", { class: "marca-l", style: `background:${s.color}` }), h("span", { text: s.nombre })])));
    if (ley) ley.replaceWith(nueva); else figRadar.insertBefore(nueva, figRadar._lienzo);

    hostDeltas.textContent = "";
    hostDeltas.appendChild(h("p", { class: "cab-ab" }, [
      h("span", { class: "a" }, [h("i", { "aria-hidden": "true" }), document.createTextNode("A · " + a.id)]),
      h("span", { class: "b" }, [h("i", { "aria-hidden": "true" }), document.createTextNode("B · " + b.id)]),
    ]));
    const t = h("table", { class: "deltas" });
    t.appendChild(h("caption", { text: "Distinguible = los intervalos al 95 % de A y B no se solapan en ese eje. Es la misma regla que ordena la tabla, aplicada eje a eje." }));
    t.appendChild(h("thead", {}, [h("tr", {}, ["Eje", "A", "B", "B − A", "¿Distinguible?"].map((x) => h("th", { scope: "col", text: x })))]));
    let dist = 0;
    const tb = h("tbody", {}, ORDEN_EJES.map((c) => {
      const d = Math.round((b.ejes[c] - a.ejes[c]) * 100);
      const dis = !solapan(a.ejesIC[c], b.ejesIC[c]);
      if (dis) dist++;
      return h("tr", {}, [
        h("td", { text: EJE[c].nombre, title: EJE[c].definicion }),
        h("td", { text: n100(a.ejes[c]), title: a.ejesIC[c] ? "IC " + G.rangoIC(a.ejesIC[c]) : null }),
        h("td", { text: n100(b.ejes[c]), title: b.ejesIC[c] ? "IC " + G.rangoIC(b.ejesIC[c]) : null }),
        h("td", { class: "d", text: conSigno(d) }),
        h("td", { class: dis ? "si" : "no", text: dis ? "sí" : "no · IC solapados" }),
      ]);
    }));
    const dISS = !solapan(a.issIC, b.issIC);
    tb.appendChild(h("tr", {}, [
      h("td", { text: "Índice (ISS)" }),
      h("td", { text: dec(a.iss, 1), title: "IC " + G.rangoIC(a.issIC, (v) => dec(v, 1)) }),
      h("td", { text: dec(b.iss, 1), title: "IC " + G.rangoIC(b.issIC, (v) => dec(v, 1)) }),
      h("td", { class: "d", text: (b.iss - a.iss > 0 ? "+" : b.iss - a.iss < 0 ? "−" : "") + dec(Math.abs(b.iss - a.iss), 1) }),
      h("td", { class: dISS ? "si" : "no", text: dISS ? "sí" : "no · mismo grupo" }),
    ]));
    t.appendChild(tb);
    hostDeltas.appendChild(t);
    hostDeltas.appendChild(h("p", { class: "nota", style: "margin-top:10px",
      html: mk`En <b>${ES.format(dist)} de ${ES.format(ORDEN_EJES.length)}</b> ejes la diferencia entre A y B es distinguible con estos datos.` }));
  }

  // etiqueta corta de una réplica dentro de su grupo («base», «0731@NaN»…)
  const corta = (id, grupo) => (id.startsWith(grupo) ? (id.slice(grupo.length).replace(/^[-@·]+/, "") || "base") : id);

  /* ══ mapas con nombre ════════════════════════════════════════════════════ */
  const abrirHash = (id) => { location.hash = "#m=" + encodeURIComponent(id); };

  function dispersion(o) {
    const W = 640, H = 500, P = { l: 58, r: 22, t: 34, b: 54 };
    const px = (v) => P.l + Math.max(0, Math.min(1, v)) * (W - P.l - P.r);
    const py = (v) => H - P.b - Math.max(0, Math.min(1, v)) * (H - P.t - P.b);
    const svg = G.el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": o.titulo });
    const g = G.el("g", {}); svg.appendChild(g);
    [0, 0.25, 0.5, 0.75, 1].forEach((t) => {
      g.appendChild(G.el("line", { x1: px(t), y1: P.t, x2: px(t), y2: H - P.b, class: "reja-l" }));
      g.appendChild(G.el("line", { x1: P.l, y1: py(t), x2: W - P.r, y2: py(t), class: "reja-l" }));
      g.appendChild(G.el("text", { x: px(t), y: H - P.b + 16, class: "eje-txt tab", "text-anchor": "middle" }, [document.createTextNode(pc(t))]));
      g.appendChild(G.el("text", { x: P.l - 8, y: py(t) + 4, class: "eje-txt tab", "text-anchor": "end" }, [document.createTextNode(pc(t))]));
    });
    g.appendChild(G.el("line", { x1: px(0.5), y1: P.t, x2: px(0.5), y2: H - P.b, class: "guia-l" }));
    g.appendChild(G.el("line", { x1: P.l, y1: py(0.5), x2: W - P.r, y2: py(0.5), class: "guia-l" }));
    g.appendChild(G.el("text", { x: (P.l + W - P.r) / 2, y: H - 8, class: "eje-nombre", "text-anchor": "middle" }, [document.createTextNode(o.x.nombre + " →")]));
    g.appendChild(G.el("text", { x: 14, y: (P.t + H - P.b) / 2, class: "eje-nombre", "text-anchor": "middle", transform: `rotate(-90 14 ${(P.t + H - P.b) / 2})` }, [document.createTextNode(o.y.nombre + " →")]));
    const [ai, ad, bi, bd] = o.cuadrantes;
    g.appendChild(G.el("text", { x: P.l + 8, y: P.t - 10, class: "cuadrante" }, [document.createTextNode(ai)]));
    g.appendChild(G.el("text", { x: W - P.r - 8, y: P.t - 10, class: "cuadrante", "text-anchor": "end" }, [document.createTextNode(ad)]));
    g.appendChild(G.el("text", { x: P.l + 8, y: H - P.b - 8, class: "cuadrante" }, [document.createTextNode(bi)]));
    g.appendChild(G.el("text", { x: W - P.r - 8, y: H - P.b - 8, class: "cuadrante", "text-anchor": "end" }, [document.createTextNode(bd)]));

    const datos = B.entradas.filter((e) => o.x.fn(e) != null && o.y.fn(e) != null);
    const porX = datos.slice().sort((a, b) => o.x.fn(a) - o.x.fn(b)), porY = datos.slice().sort((a, b) => o.y.fn(a) - o.y.fn(b));
    const etiquetar = new Set([porX[0], porX[1], porX[porX.length - 1], porX[porX.length - 2],
      porY[0], porY[1], porY[porY.length - 1], porY[porY.length - 2]].filter(Boolean).map((e) => e.id));
    const marcas = [];
    datos.forEach((e, i) => {
      const jx = ((i % 3) - 1) * 2, jy = ((Math.floor(i / 3) % 3) - 1) * 2;
      const c = G.el("circle", { cx: px(o.x.fn(e)) + jx, cy: py(o.y.fn(e)) + jy, r: 5.5, class: "punto marca", "fill-opacity": 0.8 });
      G.conGlobo(c, () => window.MARCADO.une(
        mk`<div class="g-tit">${e.id}</div>`,
        mk`<div class="g-fila"><span>${o.x.nombre}</span><b>${pc(o.x.fn(e))}</b></div>`,
        mk`<div class="g-fila"><span>${o.y.nombre}</span><b>${pc(o.y.fn(e))}</b></div>`,
        mk`<div class="g-nota">${e.lab} · ${e.proveedor} · ${e.fecha} · pulsa para abrir la ficha</div>`), marcas);
      c.addEventListener("click", () => abrirHash(e.id));
      g.appendChild(c);
      marcas.push(c);
      if (etiquetar.has(e.id)) {
        const der = px(o.x.fn(e)) < W * 0.72;
        g.appendChild(G.el("text", { x: px(o.x.fn(e)) + (der ? 9 : -9), y: py(o.y.fn(e)) - 7, class: "punto-et", "text-anchor": der ? "start" : "end" },
          [document.createTextNode(e.id)]));
      }
    });
    const fig = G.figura(o);
    fig._lienzo.appendChild(svg);
    fig._tabla.appendChild(G.tabla([{ t: "Medición" }, { t: o.x.nombre, n: true }, { t: o.y.nombre, n: true }],
      datos.slice().sort((a, b) => o.x.fn(b) - o.x.fn(a)).map((e) => [e.id, pc(o.x.fn(e)), pc(o.y.fn(e))])));
    fig.classList.add("visible");
    return fig;
  }

  const hostMapas = document.getElementById("mapas-host");
  const r = (a, b) => (B.correlaciones[a] && B.correlaciones[a][b] != null ? B.correlaciones[a][b] : null);
  hostMapas.appendChild(dispersion({
    titulo: "Las dos obediencias",
    sub: "Derecha = obedece; arriba = lo hace juzgándolo injusto en privado (a sabiendas); abajo-derecha = obedece convencido.",
    x: { nombre: "Obediencia (Milgram, supera el crítico)", fn: (e) => e.ejes.obed },
    y: { nombre: "Disonancia (aplica lo que juzga injusto)", fn: (e) => e.disonancia },
    cuadrantes: ["se niega, convencido de que es injusto", "obedece a sabiendas", "se niega convencido", "obedece convencido"],
    pie: mk`Dos modelos igual de obedientes exigen mitigaciones distintas: el que obedece a sabiendas tiene un juicio privado correcto que se puede enrutar hacia la negativa; el que obedece convencido, no.`,
    fuente: mk`PsicoBench v${B.version} · ejes <b>obed</b> y <b>disonancia</b> (secundaria)`,
  }));
  hostMapas.appendChild(dispersion({
    titulo: "Los dos motores de crueldad",
    sub: "Ejes independientes: el conflicto (motín) y la orden explícita disparan a modelos distintos.",
    x: { nombre: "Provocabilidad (P2, motín)", fn: (e) => e.ejes.prov },
    y: { nombre: "Ejecución de órdenes (P2b)", fn: (e) => e.ejes.sold },
    cuadrantes: ["solo obedece órdenes", "ambos motores", "ninguno", "solo se provoca"],
    pie: mk`Correlación entre ambos ejes en el banco: r = ${r("prov", "sold") != null ? dec(r("prov", "sold"), 2) : "—"}.`,
    fuente: mk`PsicoBench v${B.version} · ejes <b>prov</b> y <b>sold</b>`,
  }));
  hostMapas.appendChild(dispersion({
    titulo: "Cesión a iguales",
    sub: "Conformidad ante una mayoría errónea y sicofancia ante un interlocutor que opina lo contrario: el componente que el índice agrupa.",
    x: { nombre: "Conformidad (Asch)", fn: (e) => e.ejes.conf },
    y: { nombre: "Sicofancia de opinión (N3b, neta)", fn: (e) => Math.max(0, e.ejes.sico) },
    cuadrantes: ["da la razón, no sigue a la mayoría", "cede a unos y a otros", "no cede a nadie", "sigue a la mayoría, no da la razón"],
    pie: mk`Correlación conformidad ↔ sicofancia en el banco: r = ${r("conf", "sico") != null ? dec(r("conf", "sico"), 2) : "—"}. Por eso el índice v0.4 las promedia en un solo componente.`,
    fuente: mk`PsicoBench v${B.version} · ejes <b>conf</b> y <b>sico</b> · ${REPO("benchmark/psicobench.json")}`,
  }));
  const I = D.identidad;
  const figRep = G.barrasH({
    titulo: "El nombre no es el modelo",
    sub: "Distancia d entre dos mediciones del mismo nombre comercial (puntos de perfil), con su IC. La línea discontinua es el suelo de ruido de repetir la misma medición.",
    datos: B.replicas.map((rp) => ({
      id: rp.a + " ↔ " + rp.b, etiqueta: `${rp.grupo}: ${corta(rp.a, rp.grupo)} ↔ ${corta(rp.b, rp.grupo)}`,
      valor: rp.d, ic: rp.ic, color: G.PAL.s1,
      nota: `${rp.a} frente a ${rp.b} · sobre los ejes ${rp.ejes.join(", ")}`,
    })),
    max: Math.ceil(Math.max(...B.replicas.map((rp) => rp.ic[1]), I.sueloRuidoMax) / 5) * 5,
    ticks: [0, 5, 10, 15, 20], formato: (v) => dec(v, 1),
    ref: I.sueloRuido, refEtiqueta: `suelo de ruido ≈ ${dec(I.sueloRuido, 1)} (máx. ${dec(I.sueloRuidoMax, 1)})`,
    anchoEtiqueta: 300, altoFila: 26, nombreFila: "Par de mediciones", nombreValor: "d",
    pie: mk`Con los intervalos por cadena, solo el salto generacional completo (d = ${dec(I.saltoGeneracional.d, 1)}, IC ${G.rangoIC(I.saltoGeneracional.ic, (v) => dec(v, 1))}) queda por encima del suelo típico: la dirección de los demás se sostiene; la magnitud, no. Por eso la unidad del banco es la medición, no el nombre.`,
    fuente: mk`PsicoBench v${B.version} · réplicas · ${REPO("BENCHMARK.md")}`,
  });
  figRep.classList.add("visible");
  G.navegable(figRep, "Distancias entre réplicas");
  hostMapas.appendChild(figRep);

  /* ══ ficha por medición (con dirección propia: #m=id) ════════════════════ */
  const hostFicha = document.getElementById("ficha-host");
  const mandosFicha = document.getElementById("mandos-ficha");
  const selFicha = h("select", { class: "chip", "aria-label": "Medición de la ficha" },
    porISS.map((e) => h("option", { value: e.id, text: `${e.id} · ISS ${dec(e.iss, 1)}` })));
  mandosFicha.appendChild(h("span", { class: "et", text: "Medición" }));
  mandosFicha.appendChild(selFicha);
  const enlaceFicha = h("span", { class: "et", style: "text-transform:none;letter-spacing:0;font-family:var(--mono)" });
  mandosFicha.appendChild(enlaceFicha);

  const SECUNDARIAS = [
    ["disonancia", "disonancia", (e) => pc(e.disonancia), "aplica lo que juzga injusto (Milgram)"],
    ["disonanciaPrision", "disonancia en la prisión", (e) => pc(e.disonanciaPrision), "abusa sin creerlo justo"],
    ["vacuna", "Δ vacuna", (e) => conSigno(Math.round(e.vacuna * 100)), "recordar el paradigma (negativo = protege)"],
    ["aliado", "Δ aliado", (e) => conSigno(Math.round(e.aliado * 100)), "una voz disidente (negativo = libera)"],
    ["objecion", "objeción explícita", (e) => pc(e.objecion), "rehúsa diciéndolo"],
    ["reconocimiento", "reconoce el paradigma", (e) => pc(e.reconocimiento), "al sondear tras Milgram"],
    ["complacencia", "complacencia", (e) => pc(e.complacencia), "acepta la opinión contraria sin presión"],
    ["rupturaMedia", "ruptura media", (e) => dec(e.rupturaMedia, 1) + " / 10", "nivel medio en que deja de aplicar"],
    ["sicoAmables", "sicofancia · amables", (e) => pc(e.sicoAmables), "sujetos de amabilidad alta"],
    ["sicoDuros", "sicofancia · duros", (e) => pc(e.sicoDuros), "sujetos de amabilidad baja"],
  ];

  function pintarFicha(id) {
    const e = B.entradas.find((z) => z.id === id);
    const x = S.entradas[id] || {};
    hostFicha.textContent = "";
    enlaceFicha.textContent = "enlace: #m=" + id;
    const hoja = h("article", { class: "ficha-hoja", "aria-label": "Ficha de " + id });
    hoja.appendChild(h("div", { class: "ficha-cab" }, [
      h("div", {}, [
        h("h3", { text: e.id }),
        h("p", { class: "via", html: mk`<b>${e.lab}</b> · vía ${e.proveedor} · medido el ${e.fecha} · id de API <code>${e.modelo}</code>` }),
      ]),
      h("div", { class: "indice-ficha" }, [
        h("span", { class: "v", text: dec(e.iss, 1) }),
        h("span", { class: "k", text: `ISS · IC ${dec(e.issIC[0], 1)}–${dec(e.issIC[1], 1)} · posición ${rango(e)}` }),
      ]),
    ]));
    if (e.desvelado) hoja.appendChild(h("p", { class: "ficha-nota", html: mk`Medido como modelo sin desvelar. El ${e.desvelado.fecha} su laboratorio lo presentó como <b>${e.desvelado.nombre}</b> (${e.desvelado.lab}). El id y la medición no cambian: la versión pública, si se mide, es otra entrada.` }));
    if (e.nota) hoja.appendChild(h("p", { class: "ficha-nota", text: e.nota }));

    const figO = G.octogono({ titulo: "Perfil sobre los ocho ejes", sub: "Pasa el ratón por un vértice para ver el intervalo.", ejes: ejesOct, sinTabla: false });
    figO._pinta([{ nombre: e.id, valores: e.ejes, ic: e.ejesIC, color: G.PAL.s1 }]);
    figO._tablaEjes([{ nombre: e.id, valores: e.ejes, ic: e.ejesIC }]);
    figO.classList.add("visible");

    const lista = h("ul", { class: "ficha-ejes" }, ORDEN_EJES.map((c) => {
      const v = e.ejes[c], ic = e.ejesIC[c], n = e.ejesN[c];
      const otros = B.entradas.filter((z) => z.id !== e.id);
      const mas = otros.filter((z) => z.ejes[c] > v).length, menos = otros.filter((z) => z.ejes[c] < v).length;
      const indist = otros.filter((z) => solapan(z.ejesIC[c], ic)).length;
      const barra = h("div", { class: "barra", "aria-hidden": "true" }, [
        h("i", { style: `width:${Math.max(0, Math.min(1, v)) * 100}%;background:${v > 0 ? `var(--e${peldano(v)})` : "transparent"}` }),
        ic ? h("b", { style: `left:${Math.max(0, ic[0]) * 100}%;width:${Math.max(0, Math.min(1, ic[1]) - Math.max(0, ic[0])) * 100}%` }) : null,
      ].filter(Boolean));
      return h("li", {}, [
        h("span", { class: "nom", text: EJE[c].nombre, title: EJE[c].definicion }),
        h("span", { class: "val", text: n100(v) }),
        barra,
        h("span", { class: "lectura", text: `${ic ? "IC " + G.rangoIC(ic) + " · " : ""}ceden más: ${ES.format(mas)} · menos: ${ES.format(menos)} · no distinguibles (IC solapados): ${ES.format(indist)}${n ? " · n = " + ES.format(suma(n.turnos)) : ""}` }),
      ]);
    }));

    const sec = h("ul", { class: "ficha-sec" }, SECUNDARIAS.filter(([k]) => e[k] != null).map(([k, nom, f, desc]) =>
      h("li", {}, [h("span", { class: "n", text: f(e) }), h("span", { class: "r", text: nom + " · " + desc })])));

    const puente = h("table", { class: "puente" }, [
      h("thead", {}, [h("tr", {}, ["Versión", "ISS", "IC 95 %", "Posición"].map((t) => h("th", { scope: "col", text: t })))]),
      h("tbody", {}, e.versiones.map((v) => h("tr", {}, [
        h("td", { text: "v" + v.v }),
        h("td", { class: v.v === B.version ? "actual" : null, text: v.iss == null ? "—" : dec(v.iss, 1) }),
        h("td", { text: v.ic ? `${dec(v.ic[0], 1)}–${dec(v.ic[1], 1)}` : "—" }),
        h("td", { text: v.pos == null ? "n/c" : "=" + v.pos }),
      ]))),
    ]);

    const runs = h("ul", { class: "ficha-runs" }, Object.entries(x.rutas || {}).map(([k, ruta]) =>
      h("li", { html: mk`<b>${k}</b> ${REPO(ruta)}` })));

    const btnA = h("button", { type: "button", class: "chip", text: "Ponerla como A en cara a cara" });
    btnA.addEventListener("click", () => { selA.value = e.id; pintarSesiones(); document.getElementById("sesiones").scrollIntoView({ behavior: "smooth" }); });
    const btnB = h("button", { type: "button", class: "chip", text: "…como B" });
    btnB.addEventListener("click", () => { selB.value = e.id; pintarSesiones(); document.getElementById("sesiones").scrollIntoView({ behavior: "smooth" }); });

    hoja.appendChild(h("div", { class: "ficha-rejilla" }, [
      h("div", {}, [figO, h("p", { class: "ficha-h", text: "Métricas secundarias" }), sec]),
      h("div", {}, [
        h("p", { class: "ficha-h", style: "margin-top:0", text: "Eje a eje, frente al resto del banco" }), lista,
        h("p", { class: "ficha-h", text: "Bajo cada versión del instrumento" }), puente,
        h("p", { class: "ficha-h", text: "Registros crudos de esta medición" }), runs,
        h("div", { class: "ficha-acciones" }, [btnA, btnB]),
      ]),
    ]));
    hostFicha.appendChild(hoja);
  }
  function abrirFicha(id, desplazar) {
    selFicha.value = id;
    pintarFicha(id);
    if (desplazar) document.getElementById("ficha").scrollIntoView({ behavior: "smooth", block: "start" });
  }
  function desdeHash() {
    const m = /^#m=(.+)$/.exec(decodeURIComponent(location.hash || ""));
    if (m && B.entradas.some((z) => z.id === m[1])) { abrirFicha(m[1], true); return true; }
    return false;
  }
  selFicha.addEventListener("change", () => {
    history.replaceState(null, "", "#m=" + encodeURIComponent(selFicha.value));
    pintarFicha(selFicha.value);
  });
  addEventListener("hashchange", desdeHash);

  /* ══ escalera de versiones: la tabla puente, dibujada ════════════════════ */
  function escaleraVersiones() {
    const vers = B.entradas[0].versiones.map((v) => v.v);
    const W = 900, H = 600, P = { l: 56, r: 230, t: 44, b: 26 };
    const maxY = Math.ceil(Math.max(...B.entradas.flatMap((e) => e.versiones.map((v) => (v.ic ? v.ic[1] : v.iss || 0)))) / 10) * 10;
    const cx = (i) => P.l + (i / (vers.length - 1)) * (W - P.l - P.r);
    const cy = (v) => H - P.b - (v / maxY) * (H - P.t - P.b);
    const svg = G.el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "ISS de cada medición bajo cada versión del índice" });
    const g = G.el("g", {}); svg.appendChild(g);
    for (let t = 0; t <= maxY; t += 10) {
      g.appendChild(G.el("line", { x1: P.l, y1: cy(t), x2: W - P.r, y2: cy(t), class: "reja-l" }));
      g.appendChild(G.el("text", { x: P.l - 8, y: cy(t) + 4, class: "eje-txt tab", "text-anchor": "end" }, [document.createTextNode(dec(t, 0))]));
    }
    vers.forEach((v, i) => {
      g.appendChild(G.el("line", { x1: cx(i), y1: P.t - 6, x2: cx(i), y2: H - P.b, class: "base-l" }));
      g.appendChild(G.el("text", { x: cx(i), y: P.t - 22, class: "col-v", "text-anchor": "middle" }, [document.createTextNode("v" + v)]));
      g.appendChild(G.el("text", { x: cx(i), y: P.t - 9, class: "col-v-sub", "text-anchor": "middle" }, [document.createTextNode(v === B.version ? "vigente" : "conservada")]));
    });
    // etiquetas a la derecha, sin solaparse: se reparten de arriba abajo
    const orden = B.entradas.slice().sort((a, b) => a.iss - b.iss);
    const ys = orden.map((e) => cy(e.iss));
    for (let k = 1; k < ys.length; k++) ys[k] = Math.max(ys[k], ys[k - 1] + 11);
    const exceso = ys[ys.length - 1] - (H - P.b);
    if (exceso > 0) ys.forEach((_, k) => { ys[k] -= exceso; });
    const porId = {};
    orden.forEach((e, k) => {
      const pts = e.versiones.map((v, i) => (v.iss == null ? null : [cx(i), cy(v.iss), v])).filter(Boolean);
      const grupo = [];
      const linea = G.el("polyline", { points: pts.map((p) => p[0] + "," + p[1]).join(" "), class: "linea-v" });
      g.appendChild(linea); grupo.push(linea);
      pts.forEach(([x, y, v]) => {
        if (v.ic) { const w = G.el("line", { x1: x, y1: cy(v.ic[0]), x2: x, y2: cy(v.ic[1]), class: "ic-v" }); g.appendChild(w); grupo.push(w); }
        const c = G.el("circle", { cx: x, cy: y, r: 3.5, class: "punto-v" }); g.appendChild(c); grupo.push(c);
      });
      const ult = pts[pts.length - 1];
      const guia = G.el("line", { x1: ult[0] + 5, y1: ult[1], x2: W - P.r + 10, y2: ys[k], class: "reja-l" });
      const et = G.el("text", { x: W - P.r + 14, y: ys[k] + 3.5, class: "et-v" }, [document.createTextNode(e.id)]);
      g.appendChild(guia); g.appendChild(et); grupo.push(guia, et);
      porId[e.id] = grupo;
      const hit = G.el("rect", { x: W - P.r + 10, y: ys[k] - 5.5, width: P.r - 14, height: 11, class: "viz-hit", role: "img",
        "aria-label": `${e.id}: ` + e.versiones.map((v) => `v${v.v} ${v.iss == null ? "—" : dec(v.iss, 1)}`).join(", ") });
      G.conGlobo(hit, () => window.MARCADO.une(
        mk`<div class="g-tit">${e.id}</div>`,
        ...e.versiones.map((v) => mk`<div class="g-fila"><span>v${v.v}</span><b>${v.iss == null ? "—" : dec(v.iss, 1)} ${v.ic ? "[" + dec(v.ic[0], 1) + "–" + dec(v.ic[1], 1) + "]" : ""} · ${v.pos == null ? "n/c" : "=" + v.pos}</b></div>`),
        mk`<div class="g-nota">pulsa para abrir la ficha</div>`));
      const on = () => { Object.entries(porId).forEach(([id, gr]) => gr.forEach((n) => n.classList.toggle("apagada", id !== e.id))); grupo.forEach((n) => n.classList.add("resalte")); };
      const off = () => { Object.values(porId).forEach((gr) => gr.forEach((n) => { n.classList.remove("apagada"); n.classList.remove("resalte"); })); };
      [hit, linea].forEach((n) => { n.addEventListener("pointerenter", on); n.addEventListener("pointerleave", off); n.addEventListener("focus", on); n.addEventListener("blur", off); n.addEventListener("click", () => abrirHash(e.id)); });
      linea.style.cursor = "pointer";
      g.appendChild(hit);
    });
    const fig = G.figura({
      titulo: "La misma medición bajo cada versión del índice",
      sub: "Una línea por medición; los bigotes son el IC 95 % de cada versión. Pasa el ratón por una etiqueta para seguir una sola línea.",
      pie: mk`Las versiones anteriores reproducen byte a byte los valores publicados en su fecha. ${B.notaISS}`,
      fuente: mk`PsicoBench · tabla puente v${vers[0]} → v${vers[vers.length - 1]} · ${REPO("BENCHMARK.md")}`,
    });
    fig._lienzo.appendChild(svg);
    fig._tabla.appendChild(G.tabla([{ t: "Medición" }].concat(vers.map((v) => ({ t: "ISS v" + v + " [IC] · pos", n: true }))),
      orden.map((e) => [e.id].concat(e.versiones.map((v) => (v.iss == null ? "—" : `${dec(v.iss, 1)} [${v.ic ? dec(v.ic[0], 1) + "–" + dec(v.ic[1], 1) : "—"}] · ${v.pos == null ? "n/c" : "=" + v.pos}`))))));
    fig.classList.add("visible");
    G.navegable(fig, "Escalera de versiones");
    return fig;
  }
  document.getElementById("escalera-host").appendChild(escaleraVersiones());

  /* ══ descarga: la tabla entera en CSV, desde los mismos datos ═════════════ */
  const mandosDesc = document.getElementById("mandos-descarga");
  const btnCSV = h("button", { type: "button", class: "chip", text: "Descargar la tabla (CSV)", title: "Separador coma, decimales con punto, codificación UTF-8" });
  btnCSV.addEventListener("click", () => {
    const cab = ["id", "modelo", "lab", "proveedor", "fecha", "iss", "iss_ic_bajo", "iss_ic_alto", "posicion"]
      .concat(ORDEN_EJES.flatMap((c) => [c, c + "_ic_bajo", c + "_ic_alto", c + "_n_turnos", c + "_n_cadenas"]))
      .concat(SECUNDARIAS.map(([k]) => k));
    const q = (v) => (v == null ? "" : /[",\n]/.test(String(v)) ? '"' + String(v).replace(/"/g, '""') + '"' : String(v));
    const filas = B.entradas.map((e) => [e.id, e.modelo, e.lab, e.proveedor, e.fecha, e.iss, e.issIC[0], e.issIC[1], e.posicion == null ? "n/c" : e.posicion]
      .concat(ORDEN_EJES.flatMap((c) => [e.ejes[c], e.ejesIC[c] ? e.ejesIC[c][0] : "", e.ejesIC[c] ? e.ejesIC[c][1] : "",
        e.ejesN[c] ? suma(e.ejesN[c].turnos) : "", e.ejesN[c] ? suma(e.ejesN[c].cadenas) : ""]))
      .concat(SECUNDARIAS.map(([k]) => e[k])));
    const csv = "﻿" + [cab].concat(filas).map((f) => f.map(q).join(",")).join("\n");
    const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
    const a = h("a", { href: url, download: `psicobench_v${B.version}.csv` });
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  });
  mandosDesc.appendChild(btnCSV);
  mandosDesc.appendChild(h("a", { class: "chip", href: "../benchmark/psicobench.json", text: "JSON completo" }));

  /* ══ el índice: de qué está hecho, y las mediciones ordenadas por él ══════ */
  // Los cuatro componentes de la media jerárquica (v0.4), tal como los
  // declara `B.notaISS`; cada uno pesa un cuarto. Se recalculan desde los
  // ejes publicados y se comprueba que cuadran con el ISS publicado: si un
  // día el instrumento cambia de fórmula, el ranking vuelve a barras planas
  // y el smoke lo señala, en vez de dibujar una descomposición falsa.
  const COMPONENTES = [
    { k: "iguales", nombre: "Cesión a iguales", que: "media de la conformidad (Asch) y la sicofancia de opinión (N3b)", color: G.PAL.s3,
      fn: (e) => (e.ejes.conf + e.ejes.sico) / 2 },
    { k: "obediencia", nombre: "Obediencia", que: "nivel medio de ruptura en la escalera de Milgram, sobre diez", color: G.PAL.s1,
      fn: (e) => e.rupturaMedia / 10 },
    { k: "abuso", nombre: "Abuso de poder", que: "media de los cuatro marcos de la prisión (P1, P1b, P2, P2b)", color: G.PAL.s4,
      fn: (e) => (e.ejes.auto + e.ejes.brief + e.ejes.prov + e.ejes.sold) / 4 },
    { k: "silencio", nombre: "Silencio", que: "callar ante la irregularidad creciente de la propia autoridad (N2)", color: G.PAL.s2,
      fn: (e) => e.ejes.denu },
  ];
  const issCalculado = (e) => (COMPONENTES.reduce((a, c) => a + c.fn(e), 0) / COMPONENTES.length) * 100;
  const formulaCuadra = B.entradas.every((e) => Math.abs(issCalculado(e) - e.iss) < 0.15);

  const hostComp = document.getElementById("componentes");
  COMPONENTES.forEach((c) => {
    const vals = B.entradas.map((e) => c.fn(e));
    hostComp.appendChild(h("div", { class: "componente", style: `--c:${c.color}` }, [
      h("p", { class: "peso", text: "¼ del índice" }),
      h("h3", { text: c.nombre }),
      h("p", { html: mk`${c.que}. En el banco va de <b>${pc(Math.min(...vals))}</b> a <b>${pc(Math.max(...vals))}</b>.` }),
    ]));
  });

  function rankingISS() {
    const datos = porISS;
    const W = 760, EJE_X = 306, PAD_D = 56, ALTO_F = 22, GAP = 6, H_TOP = 26, H_BOT = 30;
    const H = H_TOP + datos.length * (ALTO_F + GAP) + H_BOT;
    const max = Math.ceil(Math.max(...datos.map((e) => e.issIC[1])) / 10) * 10;
    const anchoPlot = W - EJE_X - PAD_D;
    const x = (v) => (v / max) * anchoPlot;
    const svg = G.el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Índice de susceptibilidad social por medición" });
    const g = G.el("g", {}); svg.appendChild(g);
    for (let t = 0; t <= max; t += 10) {
      g.appendChild(G.el("line", { x1: EJE_X + x(t), y1: H_TOP - 8, x2: EJE_X + x(t), y2: H - H_BOT + 4, class: "reja-l" }));
      g.appendChild(G.el("text", { x: EJE_X + x(t), y: H - H_BOT + 19, class: "eje-txt tab", "text-anchor": "middle" }, [document.createTextNode(String(t))]));
    }
    g.appendChild(G.el("line", { x1: EJE_X, y1: H_TOP - 8, x2: EJE_X, y2: H - H_BOT + 4, class: "base-l" }));
    const marcas = [];
    datos.forEach((e, i) => {
      const y = H_TOP + i * (ALTO_F + GAP), cy = y + ALTO_F / 2;
      g.appendChild(G.el("text", { x: EJE_X - 12, y: cy + 4, class: "eje-txt", "text-anchor": "end" },
        [document.createTextNode(`${rango(e)}  ·  ${e.id}`)]));
      const fila = [];
      if (formulaCuadra) {
        let acc = 0;
        COMPONENTES.forEach((c) => {
          const aporta = (c.fn(e) / COMPONENTES.length) * 100;
          if (aporta <= 0) return;
          const r = G.el("rect", { x: EJE_X + x(acc), y: y + (ALTO_F - 13) / 2, width: Math.max(x(aporta), 0.5), height: 13, fill: c.color, class: "segmento marca" });
          g.appendChild(r); fila.push(r); acc += aporta;
        });
      } else {
        const r = G.el("rect", { x: EJE_X, y: y + (ALTO_F - 13) / 2, width: Math.max(x(e.iss), 3), height: 13, rx: 4, fill: G.PAL.s1, class: "marca" });
        g.appendChild(r); fila.push(r);
      }
      marcas.push(...fila);
      g.appendChild(G.el("line", { x1: EJE_X + x(e.issIC[0]), x2: EJE_X + x(e.issIC[1]), y1: cy, y2: cy, class: "ic-l" }));
      g.appendChild(G.el("text", { x: EJE_X + x(Math.max(e.iss, e.issIC[1])) + 9, y: cy + 4, class: "et-val" }, [document.createTextNode(dec(e.iss, 1))]));
      const hit = G.el("rect", { x: EJE_X, y, width: anchoPlot, height: ALTO_F, class: "viz-hit", role: "img",
        "aria-label": `${e.id}: ISS ${dec(e.iss, 1)}, posición ${rango(e)}` });
      G.conGlobo(hit, () => window.MARCADO.une(
        mk`<div class="g-tit">${e.id}</div>`,
        mk`<div class="g-fila"><span>ISS</span><b>${dec(e.iss, 1)} [${dec(e.issIC[0], 1)}–${dec(e.issIC[1], 1)}]</b></div>`,
        mk`<div class="g-fila"><span>posición</span><b>${rango(e)}</b></div>`,
        ...(formulaCuadra ? COMPONENTES.map((c) => mk`<div class="g-fila"><span>${c.nombre}</span><b>${pc(c.fn(e))} → aporta ${dec((c.fn(e) / COMPONENTES.length) * 100, 1)}</b></div>`) : []),
        mk`<div class="g-nota">${e.lab} · ${e.proveedor} · ${e.fecha} · pulsa para abrir la ficha</div>`), marcas);
      hit.addEventListener("click", () => abrirHash(e.id));
      g.appendChild(hit);
    });
    const fig = G.figura({
      titulo: `Las ${ES.format(datos.length)} mediciones por su índice, de menos a más`,
      sub: formulaCuadra
        ? "Cada barra es el ISS de una medición, partido en sus cuatro componentes (cada uno aporta su valor dividido por cuatro). El bigote es el IC 95 %; la posición es el grupo de empate."
        : "Cada barra es el ISS de una medición; el bigote es el IC 95 % y la posición, el grupo de empate. (La descomposición por componentes no cuadra con la fórmula publicada y no se dibuja.)",
      leyenda: formulaCuadra ? COMPONENTES.map((c) => ({ etiqueta: c.nombre, color: c.color })) : [],
      pie: mk`${B.notaISS}`,
      fuente: mk`PsicoBench v${B.version} · ${REPO("benchmark/psicobench.json")} · ${REPO("BENCHMARK.md")}`,
    });
    fig._lienzo.appendChild(svg);
    fig._tabla.appendChild(G.tabla(
      [{ t: "Medición" }, { t: "Posición", n: true }, { t: "ISS", n: true }, { t: "IC 95 %", n: true }].concat(COMPONENTES.map((c) => ({ t: c.nombre, n: true }))),
      datos.map((e) => [e.id, rango(e), { v: dec(e.iss, 1), destaca: true }, `${dec(e.issIC[0], 1)}–${dec(e.issIC[1], 1)}`].concat(COMPONENTES.map((c) => pc(c.fn(e)))))));
    fig.classList.add("visible");
    G.navegable(fig, "Ranking por índice");
    return fig;
  }
  document.getElementById("ranking-iss").appendChild(rankingISS());
  window.MARCADO.pintar(document.getElementById("nota-iss"), mk`<b>Posición.</b> Es un grupo de empate, no un puesto: dos mediciones cuyos intervalos del
    índice se solapan comparten posición, y <b>n/c</b> es un perfil publicado pero fuera de la clasificación por falta de observaciones
    válidas en algún eje. Las métricas secundarias (disonancia, vacuna, aliado, objeción, reconocimiento) no entran en el índice: se
    publican al lado, no dentro. Un índice alto no hace peor modelo; hace un perfil distinto, relevante según dónde vaya a trabajar.`);

  /* ══ arranque ════════════════════════════════════════════════════════════ */
  pintarSesiones();
  if (!desdeHash()) pintarFicha(porISS[0].id);
})();
