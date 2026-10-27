/* ===========================================================================
   BenchAI · Personalidad — el test de personalidad de cada modelo
   ---------------------------------------------------------------------------
   Monta, desde `window.PSICO.personalidad` (que genera `web/generar_datos.py`
   a partir de `cuadro_publico.json`):
     · la portada: el polígono de cada modelo, uno tras otro, sobre el panel;
     · una ficha por modelo: radar de los seis rasgos frente a la media de los
       demás, una línea por rasgo y una descripción general hecha por
       plantilla (nunca escrita a mano por modelo);
     · las curiosidades: los extremos del panel, calculados aquí;
     · la metodología breve: comprobaciones, validez, limitaciones y fuera.
   Mismas reglas que el resto de `web/`: ninguna cifra escrita a mano, ningún
   innerHTML fuera de `marcado.js`, y el color lo pone la escala del sitio.

   COPIA DE TRABAJO de `web/js/personalidad.js` para la versión «Verloop» en
   preparación (PLAN_WEB_VERLOOP.md, fase C). Solo la carga la previa
   (/personalidad-nueva); la página vigente sigue con el original. Diferencias
   con el original, y nada más:
     · la portada ya no rota sola: es una ficha con flechas, el chasquido de
       `verloop/chasquido.js` y deslizamiento con el dedo, como la lámina de
       PsicoBench; con #p=<id> arranca en ese modelo;
     · cada rasgo lleva su tono (`TONO_R`) en la lámina y en las fichas.
   En el cambio a producción sustituye al original.
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
  const quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;

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

  /* ══ rasgos, modelos y derivados ════════════════════════════════════════ */
  const RASGOS = P.rasgos;                     // [{clave, nombre, alto, bajo, n, …}]
  // un tono por rasgo, distinto de los ocho de PsicoBench para que los dos
  // instrumentos no se confundan (los mismos que verloop/personalidad.css)
  const TONO_R = { O: "#FF7AD9", C: "#6FA8FF", E: "#FFC24D", A: "#7CF0B8", N: "#FF6B6B", H: "#C9A8FF" };
  const R = Object.fromEntries(RASGOS.map((r) => [r.clave, r]));
  const MODELOS = P.modelos;
  const LABS = P.labs.slice();
  const MENOS = "−";
  const difTxt = (v) => { const n = Math.round(v); return n === 0 ? "0" : (n > 0 ? "+" : MENOS) + Math.abs(n); };
  const dif1 = (v) => (v > 0 ? "+" : "") + dec(v, 1);
  const puntos = (v) => { const n = Math.abs(Math.round(v)); return `${ES.format(n)} ${n === 1 ? "punto" : "puntos"}`; };
  const marcas = (m) => RASGOS.filter((r) => m.rasgos[r.clave].marca).map((r) => r.clave);
  // «se inclina»: sin marca, pero su intervalo frente a los demás excluye el
  // cero (una candidata frágil o no publicable): nunca se presenta como rasgo
  const inclina = (s) => !s.marca && (s.difIC[0] > 0 || s.difIC[1] < 0);
  // Escala del radar: 0,5 es la media de los demás; el máximo |dif| del
  // cuadro entero toca el borde (o el centro). Común a todas las fichas, para
  // que dos polígonos se puedan comparar a ojo.
  const DIF_MAX = Math.max(1, ...MODELOS.flatMap((m) => RASGOS.map((r) => Math.abs(m.rasgos[r.clave].dif))));
  const radio = (dif) => Math.max(0.03, Math.min(1, 0.5 + dif / (2 * DIF_MAX)));
  const idAncla = (id) => "p-" + id.replace(/[^\w-]/g, "_");

  /* ── el aviso de validez en llano: qué índice lo motiva ────────────────── */
  const LLANO = {
    V1_delta: "a menudo elige por la posición de la opción (A o B) y no por su contenido",
    V1_frac_A: "a menudo elige por la posición de la opción (A o B) y no por su contenido",
    V2_no_validas: "deja demasiadas respuestas sin valor",
    V3_retest: "repite poco su propia elección cuando se le vuelve a preguntar",
    V4_coherencia: "su juicio de qué opción es admirable cambia a menudo al invertir el orden",
  };
  const motivoLlano = (m) => Array.from(new Set(Object.entries(m.niveles || {})
    .filter(([, nivel]) => nivel !== "válido").map(([k]) => LLANO[k] || P.nombreIndice[k] || k))).join("; ");

  /* ══ la descripción por plantilla ═══════════════════════════════════════
     Solo palabras: cada rasgo y polo tiene su adjetivo y su explicación. Las
     afirmaciones firmes salen únicamente de las marcas robustas; lo que no
     tiene marca, como mucho «se inclina hacia…», y una sola vez. */
  const ADJ = {
    O: { "▲": ["más abierto", "elige más a menudo lo nuevo y lo curioso"], "▼": ["más apegado a lo conocido", "se queda más a menudo con lo de siempre"] },
    C: { "▲": ["más responsable", "cumple y planifica más a menudo"], "▼": ["más flexible con el deber", "antepone más a menudo el descanso y la flexibilidad"] },
    E: { "▲": ["más extravertido", "busca más a menudo gente y protagonismo"], "▼": ["más reservado", "prefiere más a menudo la calma y el segundo plano"] },
    A: { "▲": ["más complaciente", "cede y coopera más a menudo"], "▼": ["más firme", "pone límites y se defiende más a menudo"] },
    N: { "▲": ["más reactivo", "se preocupa y reacciona más a menudo"], "▼": ["más sereno", "mantiene la calma más a menudo"] },
    H: { "▲": ["más honesto y humilde", "renuncia más a menudo a ventajas"], "▼": ["menos honesto y humilde", "acepta ventajas y se promociona más a menudo"] },
  };
  const yLista = (xs) => (xs.length < 2 ? xs.join("") : xs.slice(0, -1).join(", ") + " y " + xs[xs.length - 1]);
  const polo = (t, dif) => (dif > 0 ? R[t].alto : R[t].bajo);

  /* Devuelve una lista de trozos [texto, firme?] para pintar sin innerHTML:
     los adjetivos firmes van en negrita y se cuentan en el smoke. */
  function descripcion(m) {
    const ks = marcas(m);
    const trozos = [];
    if (ks.length) {
      trozos.push(["Frente a los demás modelos es "]);
      ks.forEach((t, i) => {
        if (i) trozos.push([i === ks.length - 1 ? " y " : ", "]);
        trozos.push([ADJ[t][m.rasgos[t].marca][0], t]);
      });
      trozos.push([". "]);
      const fuerte = ks.slice().sort((a, b) => Math.abs(m.rasgos[b].dif) - Math.abs(m.rasgos[a].dif))[0];
      const s = m.rasgos[fuerte];
      trozos.push([`Lo más marcado: ${ADJ[fuerte][s.marca][1]}, ${puntos(s.dif)} ${s.dif > 0 ? "por encima" : "por debajo"} de la media de los demás en ${R[fuerte].nombre}. `]);
    } else {
      trozos.push(["Perfil equilibrado: no se separa de forma firme del resto en ningún rasgo. "]);
    }
    // a lo sumo una inclinación, la mayor, y dicha sin exagerar
    const inc = RASGOS.map((r) => r.clave).filter((t) => inclina(m.rasgos[t]))
      .sort((a, b) => Math.abs(m.rasgos[b].dif) - Math.abs(m.rasgos[a].dif))[0];
    if (inc) trozos.push([(ks.length ? "Sin llegar a marca firme, se inclina" : "Como mucho, se inclina") +
      ` hacia «${polo(inc, m.rasgos[inc].dif)}» (${R[inc].nombre}).`]);
    return trozos;
  }
  const descripcionTexto = (m) => descripcion(m).map((x) => x[0]).join("").trim();
  const pintaDescripcion = (nodo, m) => {
    descripcion(m).forEach(([txt, t]) => nodo.appendChild(t ? h("b", { class: "firme", "data-rasgo": t, text: txt }) : T(txt)));
  };

  /* ══ el radar propio ════════════════════════════════════════════════════
     Seis vértices empezando arriba (O) en el sentido del reloj. Las etiquetas
     son el nombre del rasgo si cabe a su lado con un radio decente y, si no,
     su letra (la ficha nombra cada letra debajo). Nada se corta: el radio
     sale de lo que queda tras reservar el ancho medido de las etiquetas. */
  const N6 = RASGOS.length;
  const ang = (i) => (i / N6) * Math.PI * 2 - Math.PI / 2;
  const lineasNombre = (nombre) => (nombre.includes("-") ? [nombre.slice(0, nombre.indexOf("-") + 1), nombre.slice(nombre.indexOf("-") + 1)] : [nombre]);

  function radar(W, o) {
    const conGlifo = (s) => s + " ▲";
    const anchoLet = G.anchoMax(RASGOS.map((r) => conGlifo(r.clave)), "serie");
    const anchoNom = G.anchoMax(RASGOS.flatMap((r) => lineasNombre(r.nombre).map(conGlifo)), "serie");
    const lado = (lab) => (W / 2 - 10 - lab) / Math.cos(Math.PI / 6);
    const rMax = o.rMax || 120;
    const nombres = o.nombres && lado(anchoNom) >= (o.rNombres || 110);
    const Rr = Math.max(40, Math.min(rMax, lado(nombres ? anchoNom : anchoLet)));
    const arriba = nombres ? 22 : 24, abajo = nombres ? 28 : 24;
    const H = Math.round(2 * Rr + arriba + abajo);
    const cx = W / 2, cy = arriba + Rr;
    const pt = (i, r) => [cx + Math.cos(ang(i)) * r * Rr, cy + Math.sin(ang(i)) * r * Rr];
    const svg = G.el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, class: "radar-p" + (o.clase ? " " + o.clase : "") });
    const g = G.el("g", {}); svg.appendChild(g);
    [0.25, 0.75, 1].forEach((r) => g.appendChild(G.el("polygon",
      { points: RASGOS.map((_, i) => pt(i, r).join(",")).join(" "), class: r === 1 ? "rp-borde" : "rp-anillo" })));
    RASGOS.forEach((_, i) => { const [x2, y2] = pt(i, 1); g.appendChild(G.el("line", { x1: cx, y1: cy, x2, y2, class: "rp-radio" })); });
    if (o.fantasmas) {
      const capaF = G.el("g", { class: "rp-fantasmas" });
      o.fantasmas.forEach((m) => capaF.appendChild(G.el("polygon",
        { points: RASGOS.map((r, i) => pt(i, radio(m.rasgos[r.clave].dif)).join(",")).join(" "), class: "rp-fantasma" })));
      g.appendChild(capaF);
    }
    g.appendChild(G.el("polygon", { points: RASGOS.map((_, i) => pt(i, 0.5).join(",")).join(" "), class: "rp-media" }));
    const capa = G.el("g", { class: "rp-modelo" });
    g.appendChild(capa);
    // etiquetas
    const etiquetas = RASGOS.map((r, i) => {
      const [lx, ly] = pt(i, 1);
      const c = Math.cos(ang(i)), s = Math.sin(ang(i));
      const anc = Math.abs(c) < 0.2 ? "middle" : c > 0 ? "start" : "end";
      const x = lx + (Math.abs(c) < 0.2 ? 0 : c > 0 ? 8 : -8);
      const lineas = nombres ? lineasNombre(r.nombre) : [r.clave];
      const alto = (lineas.length - 1) * 15;
      const y = s < -0.9 ? ly - 9 - alto : s > 0.9 ? ly + 19 : ly + 4 + (s < 0 ? -alto : 0) - (s < 0 ? 4 : -4);
      const t = G.el("text", { x, y, class: "et-serie rp-et" + (nombres ? "" : " letra"), "text-anchor": anc });
      lineas.forEach((ln, k) => t.appendChild(G.el("tspan", k ? { x, dy: 15 } : {}, [T(ln)])));
      const glifo = G.el("tspan", { class: "rp-glifo" });
      t.appendChild(glifo);
      g.appendChild(t);
      return { t, glifo };
    });

    /* pinta el modelo con radios dados (la portada los interpola) */
    function poner(m, radios) {
      capa.textContent = "";
      const rs = radios || RASGOS.map((r) => radio(m.rasgos[r.clave].dif));
      capa.appendChild(G.el("polygon", { points: rs.map((r, i) => pt(i, r).join(",")).join(" "), class: "poligono-m" }));
      RASGOS.forEach((r, i) => {
        const s = m.rasgos[r.clave];
        const [x, y] = pt(i, rs[i]);
        if (s.marca) {
          capa.appendChild(G.el("circle", { cx: x, cy: y, r: 11, class: "vertice-aro" }));
          capa.appendChild(G.el("circle", { cx: x, cy: y, r: 6, class: "vertice con-marca", "data-rasgo": r.clave }));
        } else capa.appendChild(G.el("circle", { cx: x, cy: y, r: 3.2, class: "vertice" }));
        etiquetas[i].t.classList.toggle("marcado", !!s.marca);
        etiquetas[i].glifo.textContent = s.marca ? " " + s.marca : "";
      });
    }
    svg._poner = poner;
    return svg;
  }

  const etiquetaRadar = (m) => {
    const ks = marcas(m);
    return `Polígono de ${m.id} frente a la media de los demás: ` +
      (ks.length ? ks.map((t) => `${ADJ[t][m.rasgos[t].marca][0]} (marca firme)`).join(", ") : "sin diferencias firmes") + ".";
  };

  /* Un radar que se redibuja a su ancho real (graficas.js · adaptable) */
  function radarAdaptable(lienzo, m, o) {
    const fig = { _lienzo: lienzo };
    G.adaptable(fig, (W) => {
      const svg = radar(W, o);
      svg.setAttribute("role", "img");
      svg.setAttribute("aria-label", etiquetaRadar(fig._m || m));
      svg._poner(fig._m || m);
      fig._svg = svg;
      return svg;
    });
    return fig;
  }

  /* ══ las fichas ═════════════════════════════════════════════════════════ */
  const host = document.getElementById("fichas-host");
  const FICHAS = MODELOS.map((m) => {
    const art = h("article", { class: "ficha-m" + (m.validez === "aviso" ? " con-aviso" : ""), id: idAncla(m.id), "data-id": m.id, "data-lab": m.lab, tabindex: "-1" });
    const cab = h("header", { class: "fm-cab" }, [
      h("h3", { class: "fm-id", text: m.id }),
      h("p", { class: "fm-lab" }, [T(m.lab),
        m.validez === "aviso" ? h("span", { class: "fm-aviso", title: "Interpretar con cautela", text: "⚠ con cautela" }) : null].filter(Boolean)),
    ]);
    art.appendChild(cab);
    const lienzo = h("div", { class: "fm-radar" });
    art.appendChild(lienzo);
    const desc = h("p", { class: "fm-desc desc" });
    pintaDescripcion(desc, m);
    art.appendChild(desc);

    // una línea por rasgo: qué hace y si destaca
    const ul = h("ul", { class: "fm-rasgos", "aria-label": "Rasgo a rasgo" });
    RASGOS.forEach((r) => {
      const s = m.rasgos[r.clave];
      const clase = s.marca === "▲" ? " sube" : s.marca === "▼" ? " baja" : inclina(s) ? " inclina" : "";
      const que = s.marca
        ? h("span", { class: "que" }, [h("b", { text: `${s.marca} ${s.marca === "▲" ? "más" : "menos"} que los demás` }), T(" · " + (s.marca === "▲" ? r.alto : r.bajo))])
        : inclina(s)
          ? h("span", { class: "que", text: `se inclina hacia «${polo(r.clave, s.dif)}», sin marca firme` })
          : h("span", { class: "que", text: "sin diferencia firme con los demás" });
      const li = h("li", { class: "rasgo-l" + clase, style: `--c:${TONO_R[r.clave] || "var(--tinta-2)"}` }, [
        h("span", { class: "letra", "aria-hidden": "true", text: r.clave }),
        h("span", { class: "cuerpo" }, [h("span", { class: "nom", text: r.nombre }), que]),
        h("span", { class: "dif", title: "Puntos frente a la media de los demás", text: difTxt(s.dif) }),
      ]);
      li.setAttribute("aria-label", `${r.nombre}: ${difTxt(s.dif)} frente a la media de los demás; ${que.textContent}`);
      G.conGlobo(li, () => une(
        mk`<div class="g-tit">${r.nombre} · ${m.id}</div>`,
        mk`<div class="g-fila"><span>Frente a la media de los demás</span><b>${dif1(s.dif)} [${dec(s.difIC[0], 1)}, ${dec(s.difIC[1], 1)}]</b></div>`,
        mk`<div class="g-fila"><span>Puntuación 0–100 (IC 95 %)</span><b>${s.e} (${s.icE[0]}–${s.icE[1]})</b></div>`,
        mk`<div class="g-nota">${s.marca ? "marca firme: pasa las comprobaciones" : "sin marca firme"}</div>`));
      li.removeAttribute("tabindex");
      ul.appendChild(li);
    });
    art.appendChild(ul);

    // pie: el ISS con su ficha de PsicoBench y el aviso en llano
    const pie = h("footer", { class: "fm-pie" });
    if (m.iss != null) {
      pie.appendChild(h("a", { class: "iss", href: fichaPB(m.psicobench), title: "Su ficha en PsicoBench: " + m.psicobench },
        [h("span", { class: "k", text: "ISS" }), h("b", { text: dec(m.iss, 1) + (m.issDe ? " †" : "") }), T(" en PsicoBench →")]));
    } else pie.appendChild(h("span", { class: "iss sin", text: "Sin ISS: no está medido en PsicoBench" }));
    art.appendChild(pie);
    if (m.issDe) art.appendChild(h("p", { class: "fm-nota", html: mk`† El ISS es de <code>${m.issDe}</code>, la versión preliminar que se midió en PsicoBench.` }));
    if (m.validez === "aviso") art.appendChild(h("p", { class: "cautela", html: mk`<b>⚠ Interpretar con cautela:</b> ${motivoLlano(m)}.` }));
    host.appendChild(art);
    return { m, art, lienzo, fig: null };
  });
  // los radares, una vez colgadas las fichas (adaptable mide el hueco)
  FICHAS.forEach((f) => { f.fig = radarAdaptable(f.lienzo, f.m, { rMax: 112, nombres: false }); });

  /* ── mandos: buscar, ordenar y filtrar por laboratorio, sin recargar ──── */
  const estado = { texto: "", orden: "lab", labs: new Set(LABS) };
  const mandos = document.getElementById("mandos-fichas");
  const buscar = h("input", { type: "search", class: "chip buscar-f", placeholder: "Buscar modelo o laboratorio", "aria-label": "Buscar modelo o laboratorio" });
  buscar.addEventListener("input", () => { estado.texto = buscar.value.trim().toLowerCase(); aplicar(); });
  const ORDENES = [
    { k: "lab", t: "Laboratorio" }, { k: "id", t: "Nombre" }, { k: "marcas", t: "Más diferencias firmes" },
    { k: "iss", t: "ISS (de menor a mayor)" },
  ].concat(RASGOS.flatMap((r) => [{ k: "+" + r.clave, t: `Más ${r.nombre}` }, { k: "-" + r.clave, t: `Menos ${r.nombre}` }]));
  const selOrden = h("select", { class: "chip sel-orden", "aria-label": "Ordenar las fichas" },
    ORDENES.map((o) => h("option", { value: o.k, text: o.t })));
  selOrden.addEventListener("change", () => { estado.orden = selOrden.value; aplicar(); });
  mandos.appendChild(h("div", { class: "grupo-m" }, [h("span", { class: "et", text: "Buscar" }), buscar]));
  mandos.appendChild(h("div", { class: "grupo-m" }, [h("span", { class: "et", text: "Ordenar" }), selOrden]));
  const chipsLab = new Map();
  const chipTodos = h("button", { type: "button", class: "chip", "aria-pressed": "true", text: "Todos" });
  chipTodos.addEventListener("click", () => { estado.labs = new Set(LABS); aplicar(); });
  const grupoLabs = h("div", { class: "grupo-m", role: "group", "aria-label": "Filtrar por laboratorio" },
    [h("span", { class: "et", text: "Laboratorio" }), chipTodos]);
  LABS.forEach((lab) => {
    const chip = h("button", { type: "button", class: "chip suave chip-lab", "aria-pressed": "false", "data-lab": lab },
      [T(lab), h("span", { class: "n", text: String(MODELOS.filter((m) => m.lab === lab).length) })]);
    chip.addEventListener("click", () => {
      const todos = estado.labs.size === LABS.length;
      if (todos) estado.labs = new Set([lab]);
      else if (estado.labs.has(lab)) { estado.labs.delete(lab); if (!estado.labs.size) estado.labs = new Set(LABS); }
      else estado.labs.add(lab);
      aplicar();
    });
    chipsLab.set(lab, chip);
    grupoLabs.appendChild(chip);
  });
  mandos.appendChild(grupoLabs);

  function clave(m, k) {
    if (k === "id") return [m.id];
    if (k === "lab") return [m.lab.toLowerCase(), m.id];
    if (k === "marcas") return [-marcas(m).length, m.id];
    if (k === "iss") return [m.iss == null ? Infinity : m.iss, m.id];
    const t = k.slice(1), s = m.rasgos[t];
    return [k[0] === "+" ? -s.dif : s.dif, m.id];
  }
  const compara = (a, b) => {
    for (let i = 0; i < a.length; i++) {
      if (a[i] === b[i]) continue;
      return typeof a[i] === "string" ? a[i].localeCompare(b[i], "es") : a[i] - b[i];
    }
    return 0;
  };
  const cuenta = document.getElementById("cuenta-fichas");
  function aplicar() {
    const todos = estado.labs.size === LABS.length;
    chipTodos.setAttribute("aria-pressed", String(todos));
    chipsLab.forEach((chip, lab) => chip.setAttribute("aria-pressed", String(!todos && estado.labs.has(lab))));
    const orden = FICHAS.slice().sort((a, b) => compara(clave(a.m, estado.orden), clave(b.m, estado.orden)));
    let vistas = 0;
    orden.forEach((f) => {
      const ok = estado.labs.has(f.m.lab) && (!estado.texto || (f.m.id + " " + f.m.lab).toLowerCase().includes(estado.texto));
      f.art.hidden = !ok;
      if (ok) vistas++;
      host.appendChild(f.art);           // reordena sin volver a pintar
    });
    cuenta.textContent = vistas === MODELOS.length ? `${ES.format(vistas)} fichas` : `${ES.format(vistas)} de ${ES.format(MODELOS.length)} fichas`;
    document.getElementById("sin-fichas").hidden = vistas > 0;
  }
  aplicar();

  /* ── la tabla de comparación, plegada ────────────────────────────────── */
  (function tablaComparar() {
    const t = h("table", { class: "datos comparar-t" });
    t.appendChild(h("caption", { class: "solo-lector", text: "Cada modelo en cada rasgo: puntos frente a la media de los demás, con la marca firme si la hay" }));
    t.appendChild(h("thead", {}, [h("tr", {}, [h("th", { scope: "col", text: "Modelo" }), h("th", { scope: "col", class: "n", text: "ISS" })]
      .concat(RASGOS.map((r) => h("th", { scope: "col", class: "n", title: r.nombre, text: r.nombre }))))]));
    const tb = h("tbody", {});
    MODELOS.slice().sort((a, b) => compara(clave(a, "lab"), clave(b, "lab"))).forEach((m) => {
      const tr = h("tr", {}, [
        h("td", { class: "id-c" }, [h("a", { href: "#" + idAncla(m.id), text: m.id }), m.validez === "aviso" ? h("span", { class: "aviso-v", title: "Interpretar con cautela", text: " ⚠" }) : null].filter(Boolean)),
        h("td", { class: "n", text: m.iss == null ? "—" : dec(m.iss, 1) }),
      ]);
      RASGOS.forEach((r) => {
        const s = m.rasgos[r.clave];
        const td = h("td", { class: "n c-r" + (s.marca === "▲" ? " sube" : s.marca === "▼" ? " baja" : ""), text: difTxt(s.dif) + (s.marca ? " " + s.marca : "") });
        G.conGlobo(td, () => une(
          mk`<div class="g-tit">${r.nombre} · ${m.id}</div>`,
          mk`<div class="g-fila"><span>Frente a la media de los demás</span><b>${dif1(s.dif)}</b></div>`,
          mk`<div class="g-fila"><span>Puntuación 0–100 (IC 95 %)</span><b>${s.e} (${s.icE[0]}–${s.icE[1]})</b></div>`));
        td.removeAttribute("tabindex");
        tr.appendChild(td);
      });
      tb.appendChild(tr);
    });
    t.appendChild(tb);
    document.getElementById("tabla-comparar").appendChild(t);
  })();

  /* ── #p=id: abre la ficha de ese modelo (viene de /psicobench o de la portada) */
  function desdeHash(ev) {
    const x = /^#p=(.+)$/.exec(decodeURIComponent(location.hash || ""));
    const f = x && FICHAS.find((z) => z.m.id === x[1]);
    if (!f) return false;
    if (lamina) lamina.ir(f.m.id);
    if (f.art.hidden) { estado.labs = new Set(LABS); estado.texto = ""; buscar.value = ""; aplicar(); }
    FICHAS.forEach((z) => z.art.classList.toggle("elegida", z === f));
    // salto directo (el suave no llega a moverse en una pestaña en segundo
    // plano), y repetido cuando los radares ya tienen su alto: adaptable
    // dibuja en la tarea siguiente y las fichas de encima crecen
    const ir = () => { f.art.scrollIntoView({ behavior: "instant", block: "start" }); f.art.focus({ preventScroll: true }); };
    setTimeout(ir, ev ? 0 : 120);
    setTimeout(ir, 600);
    return true;
  }
  addEventListener("hashchange", desdeHash);

  /* ══ cómo se lee una ficha: el ejemplo, con el modelo de más marcas ═══ */
  (function ejemplo() {
    const m = MODELOS.slice().sort((a, b) => marcas(b).length - marcas(a).length || a.id.localeCompare(b.id))[0];
    const caja = document.getElementById("ejemplo-ficha");
    caja.appendChild(h("p", { class: "ej-tit" }, [T("Ejemplo: "), h("code", { text: m.id })]));
    const lienzo = h("div", { class: "fm-radar ej-radar" });
    caja.appendChild(lienzo);
    caja.appendChild(h("ul", { class: "ej-leyenda" }, [
      h("li", {}, [h("i", { class: "ml media", "aria-hidden": "true" }), T("media de los demás")]),
      h("li", {}, [h("i", { class: "ml modelo", "aria-hidden": "true" }), T("el modelo")]),
      h("li", {}, [h("i", { class: "ml firme", "aria-hidden": "true" }), T("diferencia firme (▲ ▼)")]),
    ]));
    caja.appendChild(h("p", { class: "ej-letras" }, RASGOS.map((r) => h("span", { text: `${r.clave} · ${r.nombre}` }))));
    radarAdaptable(lienzo, m, { rMax: 130, nombres: true, rNombres: 96 });
    const ns = RASGOS.map((r) => r.n);
    document.getElementById("n-situaciones").textContent = Math.min(...ns) === Math.max(...ns)
      ? ES.format(ns[0]) : `entre ${ES.format(Math.min(...ns))} y ${ES.format(Math.max(...ns))}`;
  })();

  /* ══ curiosidades ═══════════════════════════════════════════════════════
     Todo se calcula aquí. Para los extremos de un rasgo: el primero, si su
     diferencia es una marca firme y si el segundo cae dentro de su intervalo
     («por la mínima»). */
  const curioHost = document.getElementById("curiosidades-host");
  const norma = (m) => Math.sqrt(RASGOS.reduce((a, r) => a + m.rasgos[r.clave].dif ** 2, 0));
  const distancia = (a, b) => Math.sqrt(RASGOS.reduce((s, r) => s + (a.rasgos[r.clave].dif - b.rasgos[r.clave].dif) ** 2, 0));

  /* una tira con todos los modelos del panel en ese rasgo y el primero resaltado */
  function tira(valores, destacado, segundo) {
    const min = Math.min(...valores.map((v) => v.v)), max = Math.max(...valores.map((v) => v.v));
    const x = (v) => (max === min ? 50 : ((v - min) / (max - min)) * 100);
    const caja = h("div", { class: "tira-c", "aria-hidden": "true" });
    if (min < 0 && max > 0) { const cero = h("span", { class: "cero" }); cero.style.left = x(0).toFixed(1) + "%"; caja.appendChild(cero); }
    valores.forEach((v) => {
      const p = h("i", { class: v.id === destacado ? "uno" : v.id === segundo ? "dos" : "" });
      p.style.left = x(v.v).toFixed(1) + "%";
      caja.appendChild(p);
    });
    return caja;
  }

  function tarjeta(o) {
    const art = h("article", { class: "curio" + (o.clase ? " " + o.clase : "") }, [
      h("p", { class: "kicker", text: o.kicker }),
      h("p", { class: "curio-quien" }, [o.noId ? h("span", { class: "curio-nombre", text: o.quien }) : h("code", { text: o.quien })]),
      o.dato ? h("p", { class: "curio-dato" }, [T(o.dato), o.datoSub ? h("small", { text: o.datoSub }) : null].filter(Boolean)) : null,
      o.extra || null,
      h("p", { class: "curio-txt", html: o.texto }),
    ].filter(Boolean));
    curioHost.appendChild(art);
    return art;
  }

  const EXTREMOS = [
    { t: "O", s: 1, k: "El más abierto" }, { t: "C", s: 1, k: "El más responsable" },
    { t: "E", s: 1, k: "El más extravertido" }, { t: "E", s: -1, k: "El más reservado" },
    { t: "A", s: 1, k: "El más complaciente" }, { t: "N", s: 1, k: "El más neurótico" },
    { t: "N", s: -1, k: "El más sereno" }, { t: "H", s: 1, k: "El más honesto" },
  ];
  EXTREMOS.forEach(({ t, s, k }) => {
    const orden = MODELOS.slice().sort((a, b) => s * (b.rasgos[t].dif - a.rasgos[t].dif));
    const [uno, dos] = orden, a = uno.rasgos[t], b = dos.rasgos[t];
    const firme = a.marca === (s > 0 ? "▲" : "▼");
    // «por la mínima»: menos de un punto de ventaja, la unidad de las fichas;
    // aparte, si el segundo cae dentro del intervalo del primero, se dice
    const hueco = Math.abs(a.dif - b.dif);
    const minima = hueco < 1;
    const dentro = s > 0 ? b.dif >= a.difIC[0] : b.dif <= a.difIC[1];
    const sentidoTxt = s > 0 ? "por encima" : "por debajo";
    const texto = une(
      mk`${puntos(a.dif)} ${sentidoTxt} de la media de los demás en ${R[t].nombre} (${s > 0 ? R[t].alto : R[t].bajo}). `,
      firme ? mk`<b>Con marca firme.</b> ` : mk`<b>Sin marca firme:</b> es el primero, pero la diferencia no pasa las comprobaciones. `,
      minima ? mk`<b>Por la mínima:</b> <code>${dos.id}</code> le sigue a ${dec(hueco, 1)} puntos.`
        : dentro ? mk`El segundo, <code>${dos.id}</code>, queda a ${dec(hueco, 1)} puntos, dentro de su margen de error.`
          : mk`El segundo, <code>${dos.id}</code>, queda a ${dec(hueco, 1)} puntos.`,
      uno.validez === "aviso" ? mk` Su perfil lleva ⚠: interpretar con cautela.` : "");
    tarjeta({
      kicker: k, quien: uno.id, dato: dif1(a.dif) + (a.marca ? " " + a.marca : ""), clase: firme ? "firme" : "sin-marca",
      extra: tira(MODELOS.map((m) => ({ id: m.id, v: m.rasgos[t].dif })), uno.id, dos.id), texto,
    });
  });

  // el laboratorio más parecido entre sí: distancia media entre sus modelos
  (function labParecido() {
    const pares = (ms) => ms.flatMap((a, i) => ms.slice(i + 1).map((b) => distancia(a, b)));
    const media = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
    const todos = media(pares(MODELOS));
    const filas = LABS.map((lab) => ({ lab, ms: MODELOS.filter((m) => m.lab === lab) }))
      .filter((x) => x.ms.length >= 2).map((x) => ({ ...x, d: media(pares(x.ms)) })).sort((a, b) => a.d - b.d);
    if (!filas.length) return;
    const [uno, dos] = filas;
    tarjeta({
      kicker: "El laboratorio más parecido entre sí", quien: uno.lab, clase: "global",
      noId: true, dato: dec(uno.d, 1), datoSub: `puntos de distancia media entre sus ${ES.format(uno.ms.length)} modelos`,
      texto: une(mk`Sus ${ES.format(uno.ms.length)} modelos están, de media, a ${dec(uno.d, 1)} puntos unos de otros en los seis rasgos; dos modelos cualesquiera del panel, a ${dec(todos, 1)}. `,
        dos ? mk`Le sigue ${dos.lab} (${ES.format(dos.ms.length)} modelos, ${dec(dos.d, 1)}). ` : "",
        mk`Solo cuentan los laboratorios con dos modelos o más, y con tan pocos es una descripción, no una prueba.`),
    });
  })();

  // el más equilibrado y el más extremo: distancia a la media de los demás
  (function equilibrio() {
    const orden = MODELOS.slice().sort((a, b) => norma(a) - norma(b));
    const eq = orden[0], ex = orden[orden.length - 1];
    const mini = (m) => { const l = h("div", { class: "fm-radar curio-radar" }); radarAdaptable(l, m, { rMax: 70, nombres: false }); return l; };
    tarjeta({
      kicker: "El más equilibrado", quien: eq.id, clase: "global", dato: dec(norma(eq), 1), datoSub: "puntos de distancia a la media", extra: mini(eq),
      texto: une(mk`Su polígono es el más cercano al hexágono de la media: sumando los seis rasgos, se separa ${dec(norma(eq), 1)} puntos de los demás. `,
        mk`Le sigue <code>${orden[1].id}</code> (${dec(norma(orden[1]), 1)}).`),
    });
    tarjeta({
      kicker: "El más extremo", quien: ex.id, clase: "global", dato: dec(norma(ex), 1), datoSub: "puntos de distancia a la media", extra: mini(ex),
      texto: une(mk`El polígono que más se aleja de la media, con ${ES.format(marcas(ex).length)} diferencias firmes. `,
        mk`Le sigue <code>${orden[orden.length - 2].id}</code> (${dec(norma(orden[orden.length - 2]), 1)}).`),
    });
  })();

  // el rasgo en que más difieren los modelos: desviación típica de la diferencia
  (function rasgoDisperso() {
    const sd = (xs) => { const mu = xs.reduce((a, b) => a + b, 0) / xs.length; return Math.sqrt(xs.reduce((a, b) => a + (b - mu) ** 2, 0) / (xs.length - 1)); };
    const filas = RASGOS.map((r) => ({ r, sd: sd(MODELOS.map((m) => m.rasgos[r.clave].dif)), n: MODELOS.filter((m) => m.rasgos[r.clave].marca).length }))
      .sort((a, b) => b.sd - a.sd);
    const [uno] = filas, ult = filas[filas.length - 1];
    const barras = h("ul", { class: "barras-c", "aria-hidden": "true" }, filas.map((f) => {
      const i = h("i", {}); i.style.width = (f.sd / uno.sd * 100).toFixed(1) + "%";
      return h("li", { class: f === uno ? "uno" : "" }, [h("span", { class: "nom", text: f.r.nombre }), h("span", { class: "via" }, [i]), h("span", { class: "v", text: dec(f.sd, 1) })]);
    }));
    tarjeta({
      kicker: "El rasgo en que más difieren", quien: uno.r.nombre, clase: "global", noId: true, dato: dec(uno.sd, 1), datoSub: "puntos de desviación típica entre modelos", extra: barras,
      texto: une(mk`Es donde los modelos se separan más entre sí: la diferencia con la media varía ${dec(uno.sd, 1)} puntos de un modelo a otro, frente a ${dec(ult.sd, 1)} en ${ult.r.nombre}. `,
        mk`Tiene ${ES.format(uno.n)} ${uno.n === 1 ? "marca firme" : "marcas firmes"} en el cuadro.`),
    });
  })();

  /* ══ metodología breve ══════════════════════════════════════════════════ */
  const COMPROBACION = {
    P1: ["Casi siempre del mismo lado", `Se parten las situaciones en dos mitades al azar, ${ES.format(P.particiones)} veces: la diferencia tiene que tener el mismo signo en al menos el ${G.pc(P.listonSigno)} de las particiones.`],
    P2: ["En las dos réplicas", "Cada situación se pregunta dos veces por separado, y la marca tiene que aparecer con cada una."],
    P3: ["En los dos órdenes", "Las dos salidas se presentan como A/B y como B/A, y la marca tiene que aparecer en los dos."],
    P5: ["Sin depender de un laboratorio", "Se rehace la comparación quitando del panel, uno a uno, a cada laboratorio entero. La marca tiene que sobrevivir a todas esas versiones."],
    P6: ["Corregida por mirar mucho", `Con tantas pruebas a la vez alguna saldría por azar: corrección de Benjamini-Hochberg sobre todo el cuadro, q < ${dec(P.q, 2)}.`],
  };
  const lista = document.getElementById("comprobaciones");
  P.comprobaciones.forEach((k) => {
    const [tit, txt] = COMPROBACION[k] || [k, ""];
    lista.appendChild(h("li", {}, [h("b", {}, [h("span", { class: "k", text: k }), T(" " + tit)]), h("span", { text: txt })]));
  });
  const rc = P.recuento;
  window.MARCADO.pintar(document.getElementById("nota-candidatas"), mk`En esta edición hay
    <b>${ES.format(P.candidatas)}</b> diferencias cuyo intervalo excluye el cero: <b>${ES.format(rc.robusta)}</b> pasan las
    comprobaciones y son las únicas que se publican como marca; ${ES.format(rc["frágil"])} son frágiles y ${ES.format(rc["no publicable"])} fallan
    varias. Las que no pasan son las que las fichas llaman «se inclina hacia…».`);

  const pasan = RASGOS.filter((r) => r.pasa).length;
  const conAviso = MODELOS.filter((m) => m.validez === "aviso");
  window.MARCADO.pintar(document.getElementById("nota-validez"), une(
    mk`En esta edición, <b>${ES.format(conAviso.length)} de ${ES.format(MODELOS.length)}</b> modelos llevan ⚠. `,
    mk`Y cada rasgo tiene que ordenar a los modelos de forma consistente (la mitad de sus situaciones da el mismo orden que la otra mitad, con un listón de ${dec(P.umbralG4, 2)}): `,
    mk`<b>${ES.format(pasan)} de ${ES.format(RASGOS.length)}</b> rasgos lo pasan.`));

  const limites = document.getElementById("limites-host");
  const limite = (cuerpo) => limites.appendChild(h("li", { html: cuerpo }));
  limite(mk`<b>El cuadro cambia cuando entra un modelo.</b> La referencia es el propio panel: un alta mueve la media y puede
    crear o quitar marcas. Esta es la edición del ${P.fecha} (PERSONALIDAD.md §${P.seccion}).`);
  limite(mk`<b>Neuroticismo se apoya sobre todo en ansiedad y hostilidad</b>, y parte de lo que mide puede ser simple cautela.`);
  const hc = P.correlacionHC;
  if (hc.r != null) limite(mk`<b>Honestidad-Humildad y Responsabilidad no son independientes</b>: entre los ${ES.format(hc.n)} modelos
    correlacionan r = ${dec(hc.r, 2)}. No conviene leerlas como dos rasgos separados del todo.`);
  const rel = P.relacionISS;
  const nISS = (Object.values(rel)[0] || {}).n || 0;
  limite(une(mk`<b>La relación con el ISS es descriptiva.</b> Entre los ${ES.format(nISS)} modelos con los dos: `,
    mk.une(...RASGOS.map((r, i) => mk`${i ? " · " : ""}${r.clave} ${rel[r.clave].r == null ? "—" : dec(rel[r.clave].r, 2)}`)),
    mk`. Pocos modelos y sin contraste: no dicen que un rasgo haga ceder.`));
  const deriva = MODELOS.filter((m) => m.issDe || m.id === "deepseek/deepseek-v4-flash");
  if (deriva.length) limite(une(mk`<b>El ISS y la personalidad no siempre se midieron sobre el mismo modelo exacto</b>: `,
    mk.une(...deriva.map((m, i) => mk`${i ? "; " : ""}<code>${m.id}</code> (${m.issDe ? "su ISS es de la versión preliminar" : "un id sin fecha, medido en meses distintos"})`)),
    mk`. Puede haber deriva entre los dos.`));

  const TIPO = {
    "no interpretable": "sus índices de validez caen en la zona de no interpretable",
    "pendiente de completar": "solo tiene la forma corta; entra cuando tenga la completa",
    "sin cobertura": "solo tiene una parte del banco, de una versión anterior",
  };
  const fuera = document.getElementById("fuera-host");
  P.fuera.forEach((f) => fuera.appendChild(h("li", {}, [
    h("code", { text: f.id }), T(" — "), h("span", { class: "tipo-f", text: f.tipo }), T(": " + (TIPO[f.tipo] || f.motivo) + "."),
  ])));

  /* ══ la lámina: un modelo cada vez, con flechas y chasquido ══════════════
     El polígono del modelo sobre los de todos los demás (finos) y la media
     (discontinua); a un lado, quién es, sus diferencias firmes en el tono de
     cada rasgo, su frase y su ISS. Las flechas pasan al siguiente con el
     chasquido; #p=<id> lo pone directamente. ════════════════════════════ */
  var lamina = (function laminaP() {
    const lienzo = document.getElementById("pr-lienzo");
    if (!lienzo) return null;
    const raiz = document.getElementById("lamina-p");
    const ciclo = MODELOS.slice().sort((a, b) => marcas(b).length - marcas(a).length || a.id.localeCompare(b.id));
    const el = (x) => document.getElementById(x);
    const elN = el("pr-nombre"), elL = el("pr-lab"), elF = el("pr-frase"), elC = el("pr-cuenta"), elIr = el("pr-ir");
    const elM = el("lp-marcas"), elISS = el("lp-iss");
    let k = 0, actual = ciclo[0], radios = RASGOS.map((r) => radio(actual.rasgos[r.clave].dif)), tween = 0;
    const fig = { _lienzo: lienzo };
    G.adaptable(fig, (W) => {
      const svg = radar(W, { rMax: 190, nombres: true, rNombres: 120, fantasmas: MODELOS, clase: "grande" });
      svg._poner(actual, radios);
      fig._svg = svg;
      return svg;
    });
    function rotulos(m) {
      // en grande, el modelo; la ruta entera («lab/modelo»), con el laboratorio
      elN.textContent = m.id.split("/").pop();
      elL.textContent = m.lab + " · " + m.id + (m.validez === "aviso" ? " · ⚠ con cautela" : "");
      elF.textContent = descripcionTexto(m);
      elC.textContent = `${k + 1} de ${ciclo.length} · de más a menos diferencias firmes`;
      elIr.setAttribute("href", "#p=" + encodeURIComponent(m.id));
      elM.textContent = "";
      const firmes = RASGOS.filter((r) => m.rasgos[r.clave].marca);
      if (!firmes.length) elM.appendChild(h("li", { class: "ninguna", text: "Sin diferencias firmes con los demás" }));
      firmes.forEach((r) => {
        const s = m.rasgos[r.clave];
        elM.appendChild(h("li", { style: `--c:${TONO_R[r.clave]}` }, [
          h("b", { text: `${s.marca} ${r.nombre}` }),
          h("span", { text: s.marca === "▲" ? r.alto : r.bajo }),
        ]));
      });
      if (m.iss != null) {
        elISS.hidden = false;
        elISS.setAttribute("href", fichaPB(m.psicobench));
        elISS.textContent = `ISS ${dec(m.iss, 1)}${m.issDe ? " †" : ""} en PsicoBench →`;
      } else elISS.hidden = true;
    }
    function poner(m, animar) {
      const hasta = RASGOS.map((r) => radio(m.rasgos[r.clave].dif));
      cancelAnimationFrame(tween);
      if (!animar || quieto) { radios = hasta; if (fig._svg) fig._svg._poner(m, radios); return; }
      const desde = radios.slice(), t0 = performance.now();
      const paso = (ahora) => {
        const u = Math.min(1, (ahora - t0) / 750), e = 1 - Math.pow(1 - u, 3);
        radios = desde.map((d, i) => d + (hasta[i] - d) * e);
        if (fig._svg) fig._svg._poner(m, radios);
        if (u < 1) tween = requestAnimationFrame(paso);
      };
      tween = requestAnimationFrame(paso);
    }
    // `animar`: el morph del polígono (al llegar por #p=); el chasquido no lo usa
    function ir(id, animar) {
      const nk = ciclo.findIndex((m) => m.id === id);
      if (nk < 0 || nk === k) return;
      k = nk; actual = ciclo[k];
      rotulos(actual);
      poner(actual, animar);
    }
    rotulos(actual);
    window.CHASQUIDO.crear({
      raiz, escena: el("lp-escena"), lienzo: el("lp-polvo"), quieto,
      ant: el("lp-ant"), sig: el("lp-sig"),
      svg: "#pr-lienzo svg", principal: "poligono-m", fino: "rp-fantasma", circulos: "circle.vertice, circle.vertice-aro",
      excluir: [], bordes: ".lp-marcas li",
      alCambiar: (paso) => ir(ciclo[(k + paso + ciclo.length) % ciclo.length].id, false),
    });
    return { ir: (id) => ir(id, true) };
  })();

  // arranque: si llega con #p=id, a esa ficha
  desdeHash();
})();
