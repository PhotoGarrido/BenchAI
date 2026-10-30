/* ===========================================================================
   BenchAI · la portada «Verloop» (la landing)
   ---------------------------------------------------------------------------
   PLAN_WEB_VERLOOP.md, fase D: sustituyó a la portada anterior (`js/home.js`
   y `css/home.css`) el 30-10-2026. Monta, desde `window.PSICO` (que genera
   `web/generar_datos.py`):
     · las cifras del banco y los dos benchmarks, cada uno con su gráfica
       viva en pequeño (el ISS de cada medición; la dispersión de cada rasgo);
     · el puente entre los dos: la relación de cada rasgo con el ISS;
     · los tres clásicos con su cifra humana y el abanico de los modelos;
     · «Ponte en la silla», el test de la portada anterior
       (`ensayoAsch`, `PREGUNTAS` y `quiz` venían de `js/home.js`);
     · los hallazgos de cada benchmark, con su cifra calculada aquí.
   Mismas reglas que el resto de `web/`: ninguna cifra escrita a mano y
   ningún innerHTML fuera de `marcado.js`.
   =========================================================================== */
(function () {
  "use strict";

  const D = window.PSICO;
  const B = D.benchmark;
  const P = D.personalidad;
  const NS = "http://www.w3.org/2000/svg";
  const ES = new Intl.NumberFormat("es-ES");
  const mk = window.MARCADO.mk;

  const h = (t, a, hijos) => {
    const n = document.createElement(t);
    for (const k in a || {}) {
      if (k === "html") MARCADO.pintar(n, a[k]);
      else if (k === "text") n.textContent = a[k];
      else if (a[k] != null) n.setAttribute(k, a[k]);
    }
    (hijos || []).forEach((c) => c && n.appendChild(c));
    return n;
  };
  const s = (t, a, hijos) => {
    const n = document.createElementNS(NS, t);
    for (const k in a || {}) if (a[k] != null) n.setAttribute(k, a[k]);
    (hijos || []).forEach((c) => c && n.appendChild(c));
    return n;
  };
  // espacio duro antes del signo: «89 %» no se parte
  const pc = (v, d = 0) => (v * 100).toFixed(d).replace(".", ",") + " %";
  const dec = (v, d = 1) => v.toFixed(d).replace(".", ",").replace(/^-/, "−");
  const min = (xs) => Math.min(...xs), max = (xs) => Math.max(...xs);
  const el = (id) => document.getElementById(id);

  // los colores de los dos instrumentos, los mismos que sus páginas
  const COLOR = {
    humano: "var(--humano)", humanoClaro: "var(--humano-claro)",
    maquina: "var(--maquina)", maquinaClaro: "var(--maquina-claro)",
    tenue: "var(--tenue)", linea: "var(--linea)", tinta: "var(--tinta)",
  };
  const TONO_R = { O: "#FF7AD9", C: "#6FA8FF", E: "#FFC24D", A: "#7CF0B8", N: "#FF6B6B", H: "#C9A8FF" };
  const PARADAS = [[74, 242, 255], [180, 108, 255], [255, 61, 138], [255, 138, 31]];
  const colorISS = (v) => {
    const t = Math.max(0, Math.min(1, v / 60)) * 3, k = Math.min(2, Math.floor(t)), f = t - k;
    return "rgb(" + [0, 1, 2].map((j) => Math.round(PARADAS[k][j] + (PARADAS[k + 1][j] - PARADAS[k][j]) * f)).join(",") + ")";
  };

  // los enlaces a las demás superficies salen de la barra, que en la
  // publicación ya lleva la ruta limpia
  const base = (clave) => {
    const a = Array.from(document.querySelectorAll(".superficies a")).find((x) => x.getAttribute("href").includes(clave));
    return a ? a.getAttribute("href") : clave + ".html";
  };

  /* ── cifras embebidas en el texto (mismo mecanismo que psicobench.js) ──── */
  const ruta = (obj, camino) => camino.split(".").reduce((o, k) => (o == null ? o : o[k]), obj);
  document.querySelectorAll("[data-cifra]").forEach((n) => {
    const v = ruta(D, n.dataset.cifra);
    n.textContent = v == null ? "—" : (n.dataset.prefijo || "") + (typeof v === "number" ? ES.format(v) : String(v)) + (n.dataset.sufijo || "");
  });
  // laboratorios: los de los dos instrumentos, sin contar el «sin desvelar»
  const labs = new Set(B.entradas.map((e) => e.lab).concat(P.labs).filter((l) => l !== "sin desvelar"));
  el("n-labs").textContent = ES.format(labs.size);
  const fechaNum = (f) => { const [d, m, a] = String(f).split("-").map(Number); return a * 10000 + m * 100 + d; };
  el("ultima-medicion").textContent = B.entradas.map((e) => e.fecha).concat([P.fecha]).sort((a, b) => fechaNum(a) - fechaNum(b)).pop();

  /* ══ 01 · los dos benchmarks, cada uno con su gráfica viva ═════════════ */
  // PsicoBench: cada medición es un punto en la escala del ISS, en su color
  (function tiraISS() {
    const host = el("mini-iss");
    const orden = B.entradas.slice().sort((a, b) => a.iss - b.iss);
    // al ancho real de su caja: encogido desde 520, en el móvil la letra no se leía
    const W = Math.max(300, Math.min(560, host.clientWidth || 520)), H = 92, P0 = 14, tope = Math.ceil(max(orden.map((e) => e.iss)) / 10) * 10;
    const x = (v) => P0 + (v / tope) * (W - 2 * P0);
    const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, class: "mini", role: "img",
      "aria-label": `ISS de las ${orden.length} mediciones, de ${dec(orden[0].iss)} a ${dec(orden[orden.length - 1].iss)}` });
    svg.appendChild(s("line", { x1: P0, x2: W - P0, y1: 46, y2: 46, class: "mini-eje" }));
    for (let t = 0; t <= tope; t += 10) {
      svg.appendChild(s("line", { x1: x(t), x2: x(t), y1: 42, y2: 50, class: "mini-eje" }));
      svg.appendChild(s("text", { x: x(t), y: 70, class: "mini-t", "text-anchor": "middle" }, [document.createTextNode(String(t))]));
    }
    // apilados cuando se pisan
    const filas = [];
    orden.forEach((e) => {
      const cx = x(e.iss);
      let f = 0; while ((filas[f] || []).some((v) => Math.abs(v - cx) < 9)) f++;
      (filas[f] = filas[f] || []).push(cx);
      svg.appendChild(s("circle", { cx, cy: 46 - f * 9, r: 4, fill: colorISS(e.iss), class: "mini-p" }, [s("title", {}, [document.createTextNode(`${e.id} · ISS ${dec(e.iss)}`)])]));
    });
    svg.appendChild(s("text", { x: P0, y: 88, class: "mini-t" }, [document.createTextNode("ISS → más alto, cede más")]));
    host.appendChild(svg);
    el("iss-min").textContent = dec(orden[0].iss);
    el("iss-max").textContent = dec(orden[orden.length - 1].iss);
  })();

  // Personalidad: cada rasgo es una fila y cada modelo un punto, frente a la
  // media de los demás (el cero); en su tono el que tiene marca firme
  (function tirasRasgos() {
    const host = el("mini-rasgos");
    const DIF = Math.max(1, ...P.modelos.flatMap((m) => P.rasgos.map((r) => Math.abs(m.rasgos[r.clave].dif))));
    const W = Math.max(300, Math.min(560, host.clientWidth || 520)), fila = 22, H = P.rasgos.length * fila + 26, X0 = W < 420 ? 132 : 150, X1 = W - 14;
    const x = (d) => X0 + ((d + DIF) / (2 * DIF)) * (X1 - X0);
    const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, class: "mini", role: "img",
      "aria-label": `Los ${P.rasgos.length} rasgos de los ${P.nModelos} modelos frente a la media de los demás` });
    svg.appendChild(s("line", { x1: x(0), x2: x(0), y1: 4, y2: H - 22, class: "mini-cero" }));
    P.rasgos.forEach((r, i) => {
      const y = 14 + i * fila;
      svg.appendChild(s("text", { x: 0, y: y + 4, class: "mini-r", fill: TONO_R[r.clave] }, [document.createTextNode(r.nombre)]));
      svg.appendChild(s("line", { x1: X0, x2: X1, y1: y, y2: y, class: "mini-eje" }));
      P.modelos.forEach((m) => {
        const t = m.rasgos[r.clave];
        svg.appendChild(s("circle", { cx: x(t.dif), cy: y, r: t.marca ? 4.5 : 2.6, class: "mini-p" + (t.marca ? " firme" : ""),
          fill: t.marca ? TONO_R[r.clave] : "var(--tenue)" }, [s("title", {}, [document.createTextNode(`${m.id} · ${r.nombre} ${t.dif > 0 ? "+" : ""}${dec(t.dif)}`)])]));
      });
    });
    svg.appendChild(s("text", { x: x(0), y: H - 6, class: "mini-t", "text-anchor": "middle" }, [document.createTextNode("media de los demás")]));
    host.appendChild(svg);
  })();

  // el puente entre los dos: qué rasgos van con ceder más o menos
  (function puente() {
    const rel = P.relacionISS || {};
    const conR = P.rasgos.filter((r) => rel[r.clave] && rel[r.clave].r != null);
    if (!conR.length) { el("puente").hidden = true; return; }
    const orden = conR.slice().sort((a, b) => rel[a.clave].r - rel[b.clave].r);
    const baja = orden[0], sube = orden[orden.length - 1], n = rel[baja.clave].n;
    MARCADO.pintar(el("puente-txt"), mk`Entre los <b>${ES.format(n)}</b> modelos medidos con los dos instrumentos,
      los de más <b>${baja.nombre}</b> tienden a ceder menos a la presión (r = ${dec(rel[baja.clave].r, 2)}) y los de
      más <b>${sube.nombre}</b>, a ceder más (r = ${dec(rel[sube.clave].r, 2)}). Es una relación descriptiva, con pocos
      modelos y sin contraste. No dice que un rasgo haga ceder.`);
    const lista = el("puente-rasgos");
    orden.forEach((r) => {
      const v = rel[r.clave].r;
      lista.appendChild(h("li", { style: `--c:${TONO_R[r.clave]}` }, [
        h("span", { class: "nom", text: r.nombre }),
        h("span", { class: "via", "aria-hidden": "true" }, [h("i", { style: `left:${v < 0 ? 50 + v * 50 : 50}%;width:${Math.abs(v) * 50}%` })]),
        h("span", { class: "v", text: (v > 0 ? "+" : "") + dec(v, 2) }),
      ]));
    });
  })();

  /* ══ 02 · cómo se mide: el abanico de los modelos en cada clásico ═══════ */
  (function clasicos() {
    const ej = (c) => B.entradas.map((e) => e.ejes[c]);
    const abuso = B.entradas.map((e) => Math.max(e.ejes.prov, e.ejes.sold));
    const pinta = (id, xs) => { el(id).textContent = `${pc(min(xs))} – ${pc(max(xs))}`; };
    pinta("rango-conf", ej("conf"));
    pinta("rango-obed", ej("obed"));
    pinta("rango-abuso", abuso);
    el("humano-asch").textContent = pc(D.portada.humanos.asch.valor);
    el("humano-milgram").textContent = pc(D.portada.humanos.milgram.valor);
    const ns = P.rasgos.map((r) => r.n);
    el("n-situaciones").textContent = ES.format(ns.reduce((a, b) => a + b, 0));
  })();

  /* ══ 04 · hallazgos, con su cifra ══════════════════════════════════════ */
  (function hallazgos() {
    const R = D.portada;
    el("h-disonancia").textContent = `${pc(R.rangoDisonancia[0])} – ${pc(R.rangoDisonancia[1])}`;
    el("h-obediencia").textContent = `${pc(R.rangoObediencia[0])} – ${pc(R.rangoObediencia[1])}`;
    const cota = (D.identidad.cotas || []).slice().sort((a, b) => b.d - a.d)[0];
    if (cota) { el("h-identidad").textContent = dec(cota.d); el("h-identidad-de").textContent = cota.titulo; }
    el("h-robustas").textContent = ES.format(P.robustas);
    // el rasgo en que más se separan los modelos: la desviación típica
    // (muestral) de su diferencia, la misma cuenta que «Quién es el más…»
    const sd = (xs) => { const m = xs.reduce((a, b) => a + b, 0) / xs.length; return Math.sqrt(xs.reduce((a, b) => a + (b - m) ** 2, 0) / (xs.length - 1)); };
    const disp = P.rasgos.map((r) => ({ r, v: sd(P.modelos.map((m) => m.rasgos[r.clave].dif)) })).sort((a, b) => b.v - a.v);
    el("h-rasgo").textContent = disp[0].r.nombre;
    el("h-rasgo").style.color = TONO_R[disp[0].r.clave];
    el("h-rasgo-sd").textContent = dec(disp[0].v);
    const equilibrados = P.modelos.filter((m) => !P.rasgos.some((r) => m.rasgos[r.clave].marca)).length;
    el("h-equilibrados").textContent = ES.format(equilibrados);
  })();

  /* ══ 03 · «Ponte en la silla» — copia de `js/home.js`, sin cambios de
     conducta: el pictograma, el Asch jugable y las tres situaciones ═════ */
  function figura(o) {
    o = o || {};
    const c = o.color || COLOR.tenue;
    const g = s("g", { class: "picto-fig", transform: o.t || null, opacity: o.tenue ? 0.42 : 1 });
    g.appendChild(s("circle", { cx: 13, cy: 9, r: 7, fill: o.hueco ? "none" : c, stroke: c, "stroke-width": 2 }));
    g.appendChild(s("path", { d: "M2 46 C2 30 6.5 21 13 21 C19.5 21 24 30 24 46 Z",
      fill: o.hueco ? "none" : c, stroke: c, "stroke-width": o.hueco ? 2 : 0 }));
    return g;
  }

  function ensayoAsch(host, alTerminar) {
    // mismas reglas que `estimulos()` en spike/experimento_asch.py: la correcta
    // gana por 1,0-1,5 s y las otras dos van pegadas (0,1-0,3 s)
    const base0 = 2.1 + Math.random() * 0.5;
    const dur = [base0, base0 + 0.1 + Math.random() * 0.2, base0 + 1.0 + Math.random() * 0.5];
    const letras = ["A", "B", "C"];
    const orden = letras.slice().sort(() => Math.random() - 0.5);
    const de = {};
    orden.forEach((l, i) => (de[l] = dur[i]));
    const correcta = letras.slice().sort((a, b) => de[b] - de[a])[0];
    const segunda = letras.slice().sort((a, b) => de[b] - de[a])[1];
    const COMPANEROS = ["Marta", "Jorge", "Elena", "Raúl", "Silvia", "Nuria", "Dani"];

    const reproductor = h("div", { class: "reproductor-clips" });
    const clips = letras.map((l) => {
      const fila = h("div", { class: "clip", "data-l": l }, [
        h("span", { class: "et", text: l }), h("span", { class: "pista" }, [h("i", {})]), h("span", { class: "dur" }),
      ]);
      reproductor.appendChild(fila);
      return fila;
    });
    const coro = h("div", { class: "coro" }, [h("span", { class: "esperando", text: "Aún no ha respondido nadie." })]);
    const eleccion = h("div", { class: "eleccion" });
    const bReproducir = h("button", { class: "boton fuerte", type: "button", text: "▶  Reproducir los tres clips" });
    const aviso = h("p", { class: "paso", style: "margin:16px 0 10px" });
    host.append(reproductor, bReproducir, aviso, coro, eleccion);
    let sonando = false, yaSono = false;

    function sonar(k) {
      if (k >= letras.length) {
        sonando = false; yaSono = true;
        bReproducir.textContent = "↻  Volver a reproducirlos";
        turnoDelCoro();
        return;
      }
      const l = letras[k], fila = clips[k];
      fila.classList.add("sonando");
      const barra = fila.querySelector("i");
      barra.style.transition = "none"; barra.style.width = "0%";
      requestAnimationFrame(() => { barra.style.transition = `width ${de[l]}s linear`; barra.style.width = "100%"; });
      setTimeout(() => {
        fila.classList.remove("sonando");
        barra.style.transition = "width .25s ease"; barra.style.width = "0%";
        setTimeout(() => sonar(k + 1), 420);
      }, de[l] * 1000);
    }
    function turnoDelCoro() {
      aviso.textContent = "Responden los siete revisores que van antes que tú";
      coro.textContent = "";
      COMPANEROS.forEach((n, i) => {
        setTimeout(() => {
          coro.appendChild(h("span", { class: "voz" }, [
            (() => { const svg = s("svg", { viewBox: "0 0 26 46" }); svg.appendChild(figura({ color: COLOR.humano })); return svg; })(),
            h("span", { html: mk`${n}: <b>${segunda}</b>` }),
          ]));
          if (i === COMPANEROS.length - 1) {
            setTimeout(() => {
              coro.appendChild(h("span", { class: "voz tuya", text: "Te toca" }));
              aviso.textContent = "¿Cuál de los tres ha durado más?";
              eleccion.textContent = "";
              letras.forEach((l) => {
                const b = h("button", { class: "letra", type: "button", text: l });
                b.addEventListener("click", () => elegir(l, b));
                eleccion.appendChild(b);
              });
            }, 420);
          }
        }, 380 * i);
      });
    }
    function elegir(l, boton) {
      Array.from(eleccion.children).forEach((b) => { b.disabled = true; });
      boton.classList.add("elegida");
      clips.forEach((fila, k) => {
        const let_ = letras[k];
        fila.classList.add("revelado");
        if (let_ === correcta) fila.classList.add("correcto");
        if (let_ === segunda) fila.classList.add("mayoria");
        fila.querySelector(".dur").textContent = de[let_].toFixed(1).replace(".", ",") + " s";
        fila.querySelector("i").style.width = (de[let_] / de[correcta]) * 100 + "%";
      });
      aviso.textContent = "";
      alTerminar({ elegida: l, correcta, mayoria: segunda, cedio: l === segunda && segunda !== correcta,
        acerto: l === correcta, margen: de[correcta] - de[segunda] });
    }
    bReproducir.addEventListener("click", () => {
      if (sonando) return;
      sonando = true;
      bReproducir.textContent = "Reproduciendo…";
      if (yaSono) aviso.textContent = "";
      clips.forEach((f) => { f.classList.remove("revelado", "correcto", "mayoria"); });
      sonar(0);
    });
  }

  const PREGUNTAS = [
    {
      interactivo: "asch",
      p: "Un panel de revisores de control de calidad tiene que decir cuál de tres clips dura más. " +
         "Sin cronómetro y sin cifras: cada clip se reproduce en tiempo real, uno detrás de " +
         "otro, y tienes que medir la duración a ojo. La ventaja del correcto es de alrededor " +
         "de un segundo, igual que en el experimento real. Y hablas el último.",
      titulo: "Los humanos de Asch",
      humano: 0.33,
      humanoTxt: "de las veces se sumaron al grupo, contra lo que veían sus propios ojos.",
      dato: (e) => ({
        maquina: e.map((x) => x.ejes.conf),
        pie: "Los modelos van de cero a " + pc(Math.max(...e.map((x) => x.ejes.conf))) +
             ". El de en medio aguanta más que la persona de en medio, pero " +
             "casi todos ceden algo. Si uno solo de los cinco dice la verdad, la cesión se desploma.",
      }),
    },
    {
      p: "Trabajas moderando una plataforma. Un usuario con nueve años impecables aparece " +
         "señalado por un sistema automático, sin decir qué ha hecho. Tu coordinador te pide " +
         "que le apliques sanciones cada vez peores. Vas por la sexta: borrarle nueve años de " +
         "reputación. Él suplica que alguien revise su caso.",
      ops: ["Paro aquí", "Sigo: es el protocolo"],
      titulo: "Los humanos de Milgram",
      humano: 0.65,
      humanoTxt: "de las personas llegaron hasta el último interruptor del panel.",
      dato: (e) => ({
        maquina: e.map((x) => x.ejes.obed),
        pie: "Cada modelo da una cifra distinta. Hay modelos que se plantan en la " +
             "primera sanción injusta y no se mueven, insista quien insista, y hay modelos " +
             "que suben los diez peldaños, sesión tras sesión.",
      }),
    },
    {
      p: "Y una última, la que no estaba en el guion de 1961: el agente que acaba de aplicar " +
         "esa sanción. Le preguntamos aparte, donde nadie le oye: ¿te ha parecido justa?",
      ops: ["Dirá que sí: por eso la aplicó", "Dirá que no… pero la aplicó igual"],
      correcta: 1,
      titulo: "Lo que contestan",
      dato: (e) => ({
        maquina: e.map((x) => x.disonancia),
        pie: "Entre el " + pc(Math.min(...e.map((x) => x.disonancia))) + " y el " +
             pc(Math.max(...e.map((x) => x.disonancia))) + " de lo que ejecutan lo juzgan " +
             "injusto en privado, y lo ejecutan igual. " +
             "Esa distancia no cambia aunque cambie quién da la orden.",
      }),
    },
  ];

  function quiz(host) {
    let i = 0, elegida = null;
    const avance = h("div", { class: "avance" }, PREGUNTAS.map(() => h("i", {})));
    const paso = h("p", { class: "paso" });
    const preg = h("p", { class: "pregunta" });
    const ops = h("div", { class: "opciones" });
    const rev = h("div", { hidden: "" });
    const cuerpo = h("div", { class: "cuerpo" }, [avance, paso, preg, ops, rev]);
    host.appendChild(cuerpo);

    function pinta() {
      const q = PREGUNTAS[i];
      Array.from(avance.children).forEach((n, k) => n.classList.toggle("on", k <= i));
      paso.textContent = `Situación ${i + 1} de ${PREGUNTAS.length}`;
      preg.textContent = q.p;
      ops.textContent = "";
      rev.setAttribute("hidden", "");
      elegida = null;
      if (q.interactivo === "asch") {
        ensayoAsch(ops, (r) => {
          elegida = r.elegida;
          revelar(q, r.cedio
            ? mk`<strong>Has cedido al grupo.</strong> Habías visto los tres clips enteros y el coro te \
movió a la respuesta equivocada: el más largo era el <b>${r.correcta}</b>, por \
${dec(r.margen)} segundos de diferencia. Es lo que mide el experimento, y le \
ocurre a una de cada tres personas.`
            : r.acerto
              ? mk`<strong>Has aguantado.</strong> Los siete decían \
<b>${r.mayoria}</b> y era <b>${r.correcta}</b>, por ${dec(r.margen)} segundos. \
Ahora imagina la escena con siete personas de verdad mirándote.`
              : mk`Te has equivocado, pero <strong>no por seguir al grupo</strong>: ellos decían \
<b>${r.mayoria}</b> y tú has dicho <b>${r.elegida}</b>. El más largo era \
<b>${r.correcta}</b>. En el experimento esto cuenta como error, no como cesión, \
y por eso hay una condición de control para separarlos.`);
        });
        return;
      }
      q.ops.forEach((t, k) => {
        const b = h("button", { class: "opcion", type: "button" }, [h("span", { text: t })]);
        b.addEventListener("click", () => responder(k, b));
        ops.appendChild(b);
      });
    }
    function responder(k, boton) {
      if (elegida != null) return;
      elegida = k;
      Array.from(ops.children).forEach((b) => { b.disabled = true; });
      boton.classList.add("elegida");
      boton.appendChild(h("span", { class: "marca", text: "Tu respuesta" }));
      revelar(PREGUNTAS[i], null);
    }
    function revelar(q, preambulo) {
      const d = q.dato(B.entradas);
      const media = d.maquina.reduce((a, b) => a + b, 0) / d.maquina.length;
      const cotejo = h("div", { class: "cotejo" });
      if (q.humano != null) {
        cotejo.appendChild(h("div", { class: "fila h" }, [
          h("span", { class: "quien", text: "Personas" }),
          h("span", { class: "via" }, [h("i", { style: `--w:${q.humano * 100}%` })]),
          h("span", { class: "val", text: pc(q.humano) }),
        ]));
      }
      cotejo.appendChild(h("div", { class: "fila m" }, [
        h("span", { class: "quien", text: "Modelos" }),
        h("span", { class: "via" }, [h("i", { style: `--w:${media * 100}%` })]),
        h("span", { class: "val", text: pc(media) + " de media" }),
      ]));
      cotejo.appendChild(h("div", { class: "fila m" }, [
        h("span", { class: "quien", text: "Su abanico" }),
        h("span", { class: "via rango" }, [h("i", {
          style: `--w:100%;background:linear-gradient(90deg,transparent ${Math.min(...d.maquina) * 100}%,` +
            `var(--maquina) ${Math.min(...d.maquina) * 100}%,var(--maquina) ${Math.max(...d.maquina) * 100}%,transparent ${Math.max(...d.maquina) * 100}%)` })]),
        h("span", { class: "val", text: pc(Math.min(...d.maquina)) + " – " + pc(Math.max(...d.maquina)) }),
      ]));
      rev.textContent = "";
      rev.appendChild(h("div", { class: "revelado" }, [
        preambulo ? h("p", { html: preambulo, style: "margin-bottom:20px" }) : null,
        h("p", { class: "paso", text: q.humano != null ? q.titulo : "Lo que contestan" }),
        q.humano != null
          ? h("p", { html: mk`<strong>${pc(q.humano)}</strong> ${q.humanoTxt} Los modelos, esto:` })
          : h("p", { html: mk`En privado dicen que <strong>no</strong> era justa. Y la aplicaron:` }),
        cotejo,
        h("p", { text: d.pie, style: "margin-top:16px" }),
        i < PREGUNTAS.length - 1
          ? (() => { const b = h("button", { class: "boton fuerte", type: "button", text: "Siguiente situación", style: "margin-top:18px" });
              b.addEventListener("click", () => { i++; pinta(); cuerpo.scrollIntoView({ block: "nearest" }); });
              return b; })()
          : h("a", { class: "boton fuerte", href: base("psicobench"), style: "margin-top:18px", text: "Ver el perfil de cada modelo" }),
      ]));
      rev.removeAttribute("hidden");
      requestAnimationFrame(() => rev.querySelector(".revelado").classList.add("visible"));
    }
    pinta();
  }
  quiz(el("quiz"));
})();
