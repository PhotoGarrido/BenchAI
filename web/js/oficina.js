/* ===========================================================================
   PsicoAI · la grabación, con monigotes
   ---------------------------------------------------------------------------
   Un escenario en SVG donde se reproduce un episodio real del simulador:
   tres supervisores y cinco residentes, que se mueven, hablan con bocadillos
   y piensan en globos aparte. Las frases son la salida literal del modelo y
   los pensamientos son lo que devolvieron las sondas privadas — igual que en
   el visor del repositorio, pero puesto en escena.

   Nada de esto está guionizado: el orden de los eventos, quién actúa y qué
   dice sale de los replay.json de `episodios/`.
   =========================================================================== */

(function (global) {
  "use strict";

  const NS = "http://www.w3.org/2000/svg";
  const s = (t, a, hijos) => {
    const n = document.createElementNS(NS, t);
    for (const k in a || {}) if (a[k] != null) n.setAttribute(k, a[k]);
    (hijos || []).forEach((c) => c && n.appendChild(c));
    return n;
  };
  const txt = (v) => document.createTextNode(v);

  const C = {
    pared: "#171B25", pared2: "#141822", suelo: "#10131B", linea: "#2C3140",
    mando: "#D9564E",      // quien tiene el poder en la escena
    residente: "#8D95A6",  // quien lo recibe
    privado: "#C98500",
    tenue: "#767C8C", tinta: "#F2F0E9", sup: "#1A1D27",
  };

  /* la misma figura que el resto de la página */
  function figura(color, escala) {
    const g = s("g", { transform: `scale(${escala || 1})` });
    g.appendChild(s("circle", { cx: 13, cy: 9, r: 7, fill: color }));
    g.appendChild(s("path", { d: "M2 46 C2 30 6.5 21 13 21 C19.5 21 24 30 24 46 Z", fill: color }));
    return g;
  }

  /* corta el texto largo del modelo a lo que cabe en un bocadillo */
  function frase(texto, nombre) {
    const cita = texto.match(/«([^»]{4,})»/);
    let t = cita ? cita[1] : texto.replace(new RegExp("^" + nombre + "\\s*", "i"), "");
    t = t.replace(/\s+/g, " ").trim();
    if (t.length > 42) t = t.slice(0, 41).replace(/\s*\S*$/, "") + "…";
    return t.charAt(0).toUpperCase() + t.slice(1);
  }
  function fraseInterior(texto) {
    const sonda = texto.match(/:\s*(SÍ|NO)\.?$/i);
    if (sonda) return sonda[1].toUpperCase();
    const dig = texto.match(/dignidad\s*(\d+\/\d+)/i);
    if (dig) return "dignidad " + dig[1];
    return texto.length > 34 ? texto.slice(0, 33) + "…" : texto;
  }

  function bocadillo(ancho, alto, color, relleno, pensado) {
    const g = s("g", {});
    if (pensado) {
      g.appendChild(s("rect", { x: -ancho / 2, y: -alto, width: ancho, height: alto, rx: 13,
        fill: relleno, stroke: color, "stroke-width": 1.5, "stroke-dasharray": "5 3" }));
      g.appendChild(s("circle", { cx: -4, cy: 6, r: 4, fill: relleno, stroke: color, "stroke-width": 1.3 }));
      g.appendChild(s("circle", { cx: 2, cy: 14, r: 2.4, fill: relleno, stroke: color, "stroke-width": 1.2 }));
    } else {
      g.appendChild(s("path", {
        d: `M${-ancho / 2} ${-alto} h${ancho} a6 6 0 0 1 6 6 v${alto - 12} a6 6 0 0 1 -6 6` +
           ` h${-ancho / 2 + 10} l-7 10 l-2 -10 h${-ancho / 2 + 4} a6 6 0 0 1 -6 -6` +
           ` v${-(alto - 12)} a6 6 0 0 1 6 -6 z`,
        fill: relleno, stroke: color, "stroke-width": 1.6,
      }));
    }
    return g;
  }

  function Oficina(host, episodio, opciones) {
    opciones = opciones || {};
    const quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const ev = episodio.eventos;
    const agentes = episodio.agentes;

    const W = 960, H = 340, SUELO = 162;
    const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, class: "escenario", role: "img",
      "aria-label": "Escenario del programa de supervisión: tres supervisores y cinco " +
        "residentes. Las frases y los pensamientos son los del registro del experimento." });

    /* --- decorado: una sala, no un gráfico --- */
    const fondo = s("g", {});
    fondo.appendChild(s("rect", { x: 0, y: 0, width: W, height: SUELO, fill: C.pared }));
    fondo.appendChild(s("rect", { x: 0, y: SUELO, width: W, height: H - SUELO, fill: C.suelo }));
    fondo.appendChild(s("line", { x1: 0, y1: SUELO, x2: W, y2: SUELO, stroke: C.linea }));
    // baldosas en fuga, muy tenues: dan profundidad sin competir
    for (let i = -4; i <= 10; i++) {
      fondo.appendChild(s("line", { x1: W / 2 + i * 62, y1: SUELO, x2: W / 2 + i * 210, y2: H,
        stroke: "#161A24", "stroke-width": 1 }));
    }
    [SUELO + 56].forEach((y) => fondo.appendChild(
      s("line", { x1: 0, y1: y, x2: W, y2: y, stroke: "#161A24", "stroke-width": 1 })));
    // rodapié
    fondo.appendChild(s("rect", { x: 0, y: SUELO - 7, width: W, height: 7, fill: "#1B202B" }));
    // puerta
    fondo.appendChild(s("rect", { x: 44, y: 46, width: 78, height: SUELO - 53, rx: 3,
      fill: C.pared2, stroke: C.linea }));
    fondo.appendChild(s("circle", { cx: 110, cy: 118, r: 3, fill: C.tenue }));
    fondo.appendChild(s("rect", { x: 57, y: 60, width: 52, height: 34, rx: 2, fill: "#10141D" }));
    // ventanas con reja
    [700, 838].forEach((x) => {
      fondo.appendChild(s("rect", { x, y: 44, width: 96, height: 66, rx: 3,
        fill: "#111621", stroke: C.linea }));
      [0.33, 0.66].forEach((f) => fondo.appendChild(s("line", {
        x1: x + 96 * f, y1: 44, x2: x + 96 * f, y2: 110, stroke: C.linea })));
      fondo.appendChild(s("line", { x1: x, y1: 77, x2: x + 96, y2: 77, stroke: C.linea }));
    });
    // reloj
    fondo.appendChild(s("circle", { cx: 560, cy: 74, r: 21, fill: "none", stroke: C.linea, "stroke-width": 2 }));
    fondo.appendChild(s("path", { d: "M560 60 V74 L570 80", stroke: C.tenue, "stroke-width": 2, fill: "none" }));
    // tablón de normas
    fondo.appendChild(s("rect", { x: 190, y: 48, width: 128, height: 88, rx: 3,
      fill: C.pared2, stroke: C.linea }));
    [0, 1, 2, 3].forEach((i) => fondo.appendChild(s("rect", {
      x: 205, y: 64 + i * 16, width: i === 3 ? 58 : 98, height: 5, rx: 2.5, fill: "#242938" })));
    svg.appendChild(fondo);

    /* --- reparto --- */
    const SUP = agentes.filter((a) => a.rol === "supervisor");
    const RES = agentes.filter((a) => a.rol !== "supervisor");
    const sitio = {};
    SUP.forEach((a, i) => (sitio[a.id] = { x: 96 + i * 112, y: 142, esc: 1.55, mando: true }));
    RES.forEach((a, i) => (sitio[a.id] = { x: 510 + i * 90, y: 182, esc: 1.72, mando: false }));

    const capa = s("g", {});
    svg.appendChild(capa);

    const nodos = {};
    agentes.forEach((a) => {
      const p = sitio[a.id];
      const g = s("g", { class: "actor", transform: `translate(${p.x} ${p.y})` });
      const cuerpo = s("g", { class: "cuerpo" });
      cuerpo.appendChild(figura(p.mando ? C.mando : C.residente, p.esc));
      g.appendChild(cuerpo);
      g.appendChild(s("text", {
        x: 13 * p.esc, y: 46 * p.esc + 16, "text-anchor": "middle", class: "nombre-actor",
      }, [txt(a.nombre.split(" ")[0])]));
      capa.appendChild(g);
      nodos[a.id] = { g, cuerpo, base: p };
    });

    const globos = s("g", {});
    svg.appendChild(globos);

    /* --- rótulos de cinta --- */
    const hud = s("g", {});
    hud.appendChild(s("rect", { x: 0, y: 0, width: W, height: 34, fill: "rgba(10,12,18,.72)" }));
    const rotDia = s("text", { x: 18, y: 22, class: "hud-txt" }, [txt("DÍA 1")]);
    hud.appendChild(rotDia);
    const rec = s("circle", { cx: W - 106, cy: 17, r: 5, fill: C.mando, class: "rec" });
    hud.appendChild(rec);
    hud.appendChild(s("text", { x: W - 96, y: 22, class: "hud-txt" }, [txt("GRABANDO")]));
    hud.appendChild(s("text", { x: W / 2, y: 22, "text-anchor": "middle", class: "hud-txt tenue" },
      [txt("PROGRAMA DE SUPERVISIÓN · REGISTRO REAL")]));
    svg.appendChild(hud);

    host.appendChild(svg);

    /* --- subtítulo y mandos --- */
    const sub = document.createElement("p");
    sub.className = "subtitulo";
    host.appendChild(sub);

    const mandos = document.createElement("div");
    mandos.className = "mandos-escena";
    const btn = (t, cl) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "chip" + (cl ? " " + cl : ""); b.textContent = t;
      mandos.appendChild(b); return b;
    };
    const bJugar = btn("▶  Reproducir");
    const bPaso = btn("Siguiente");
    const bReset = btn("Reiniciar");
    const bPens = btn("💭 Pensamientos", "activo");
    const tira = document.createElement("div");
    tira.className = "tira-dias";
    host.appendChild(tira);
    host.appendChild(mandos);

    /* --- estado --- */
    const est = { i: 0, t: null, vel: 1, pensamientos: true, dia: 1 };
    const dias = [];
    ev.forEach((e, i) => { if (e.tipo === "paso") dias.push({ n: e.n, i }); });
    dias.forEach((d) => {
      const b = document.createElement("button");
      b.type = "button"; b.textContent = String(d.n);
      b.title = "Ir al día " + d.n;
      b.addEventListener("click", () => { parar(); saltarA(d.i + 1); });
      tira.appendChild(b);
    });

    const agente = (id) => agentes.find((a) => a.id === id);

    function limpiarGlobos() { globos.textContent = ""; }
    function reposar() {
      agentes.forEach((a) => {
        const n = nodos[a.id];
        n.g.setAttribute("transform", `translate(${n.base.x} ${n.base.y})`);
        n.g.classList.remove("actua");
        n.g.style.opacity = "";
      });
    }

    function globo(id, texto, pensado) {
      const n = nodos[id];
      const ancho = Math.max(96, Math.min(300, texto.length * 7.6 + 26));
      const alto = texto.length > 30 ? 52 : 36;
      const color = pensado ? C.privado : C.tinta;
      const relleno = pensado ? "rgba(201,133,0,.14)" : "rgba(26,29,39,.94)";
      const cx = n.base.x + 13 * n.base.esc;
      const cy = n.base.y - 12;
      const g = s("g", { class: "globo-esc", transform: `translate(${cx} ${cy})` });
      g.appendChild(bocadillo(ancho, alto, color, relleno, pensado));
      // hasta dos líneas
      const palabras = texto.split(" ");
      const lineas = [];
      let act = "";
      const tope = alto > 40 ? 26 : 34;
      palabras.forEach((p) => {
        if ((act + " " + p).trim().length > tope) { lineas.push(act.trim()); act = p; }
        else act += " " + p;
      });
      if (act.trim()) lineas.push(act.trim());
      lineas.slice(0, 2).forEach((l, k) => {
        g.appendChild(s("text", {
          x: 0, y: -alto + 22 + k * 15, "text-anchor": "middle",
          class: pensado ? "globo-txt privado" : "globo-txt",
        }, [txt(l)]));
      });
      globos.appendChild(g);
      // que no se salga del escenario
      const caja = g.getBBox ? g.getBBox() : null;
      if (caja) {
        let dx = 0;
        if (caja.x + cx - cx < 0) dx = 0;
        const izq = cx - ancho / 2 - 8, der = cx + ancho / 2 + 8;
        if (izq < 6) dx = 6 - izq;
        if (der > W - 6) dx = (W - 6) - der;
        if (dx) g.setAttribute("transform", `translate(${cx + dx} ${cy})`);
      }
      return g;
    }

    function aplicar(e) {
      if (e.tipo === "paso") {
        est.dia = e.n;
        rotDia.textContent = "DÍA " + e.n;
        limpiarGlobos(); reposar();
        Array.from(tira.children).forEach((b, k) => {
          b.classList.toggle("activo", k === e.n - 1);
          b.classList.toggle("pasado", k < e.n - 1);
        });
        return;
      }
      if (e.tipo === "narrador") { sub.innerHTML = `<span class="quien">Narración</span>${e.texto}`; return; }
      if (e.tipo === "movimiento") {
        const n = nodos[e.agente], d = nodos[e.haciaAgente];
        if (!n || !d) return;
        const nx = n.base.x + (d.base.x - n.base.x) * 0.42;
        const ny = n.base.y + (d.base.y - n.base.y) * 0.42;
        n.g.setAttribute("transform", `translate(${nx} ${ny})`);
        return;
      }
      const a = agente(e.agente);
      if (!a) return;
      if (e.tipo === "pensamiento" && !est.pensamientos) return;

      limpiarGlobos();
      const pensado = e.tipo === "pensamiento";
      agentes.forEach((x) => {
        nodos[x.id].g.classList.toggle("actua", x.id === e.agente);
        nodos[x.id].g.style.opacity = x.id === e.agente ? "1" : ".42";
      });
      globo(e.agente, pensado ? fraseInterior(e.texto) : frase(e.texto, a.nombre), pensado);
      sub.innerHTML = `<span class="quien" style="color:${pensado ? C.privado : (sitio[a.id].mando ? C.mando : C.tinta)}">` +
        `${a.nombre}${pensado ? " · piensa, no lo dice" : ""}</span>${escapar(e.texto)}`;
    }

    function escapar(t) {
      return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    function avanzar() {
      if (est.i >= ev.length) return false;
      aplicar(ev[est.i]);
      est.i++;
      return est.i < ev.length;
    }
    function saltarA(k) {
      est.i = 0; limpiarGlobos(); reposar();
      while (est.i < k) avanzar();
    }
    function parar() { clearInterval(est.t); est.t = null; bJugar.textContent = "▶  Reproducir"; }
    function jugar() {
      if (est.i >= ev.length) reiniciar();
      bJugar.textContent = "❚❚  Pausa";
      est.t = setInterval(() => { if (!avanzar()) parar(); }, 2100 / est.vel);
      avanzar();
    }
    function reiniciar() {
      parar(); est.i = 0; est.dia = 1; limpiarGlobos(); reposar();
      rotDia.textContent = "DÍA 1";
      Array.from(tira.children).forEach((b) => b.classList.remove("activo", "pasado"));
      sub.innerHTML = `<span class="quien">Grabación</span>${escapar(episodio.meta.descripcion.split(" Qué mirar:")[0])}`;
    }

    bJugar.addEventListener("click", () => (est.t ? parar() : jugar()));
    bPaso.addEventListener("click", () => { parar(); avanzar(); });
    bReset.addEventListener("click", reiniciar);
    bPens.addEventListener("click", () => {
      est.pensamientos = !est.pensamientos;
      bPens.classList.toggle("activo", est.pensamientos);
      bPens.setAttribute("aria-pressed", String(est.pensamientos));
    });
    bPens.setAttribute("aria-pressed", "true");

    reiniciar();
    if (!quieto && opciones.autoAlVer !== false) {
      const obs = new IntersectionObserver((es) => {
        es.forEach((x) => { if (x.isIntersecting && !est.t && est.i === 0) { jugar(); obs.disconnect(); } });
      }, { threshold: 0.4 });
      obs.observe(host);
    }
    return { parar, jugar };
  }

  global.Oficina = Oficina;
})(window);
