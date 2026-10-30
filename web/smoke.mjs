/* ===========================================================================
   BenchAI · smoke de la web publicada — sin dependencias
   ---------------------------------------------------------------------------
   La lección de la auditoría W1: verificar estados HTTP y contar nodos no es
   verificar la web. El visor devolvía 200 con su JavaScript en 404, el radar
   dibujaba 8 ejes con geometría de 6, y ningún check lo vio porque ninguno
   ABRÍA la página. Esto la abre.

   Chrome headless vía CDP puro (Node ≥22: fetch y WebSocket nativos, cero
   dependencias — la política de la casa). Por cada ruta: recursos ≥400,
   excepciones, console.error, y aserciones de contenido por página.

     node web/smoke.mjs                       # contra https://benchai.tech
     node web/smoke.mjs http://127.0.0.1:8743 # contra publicacion/ en local
                                              #   (`python3 web/servir.py`)
   =========================================================================== */

import { spawn } from "node:child_process";
import { readFileSync, existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const ARGS = process.argv.slice(2);
const BASE = (ARGS.find((a) => !a.startsWith("--")) || "https://benchai.tech").replace(/\/$/, "");

const CHROME = process.env.CHROME || [
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium-browser",
  "/usr/bin/chromium",
].find(existsSync);
if (!CHROME) {
  console.error("smoke: no encuentro Chrome (define CHROME=)");
  process.exit(2);
}

/* Las aserciones devuelven null si pasan, o el texto del fallo. Se evalúan
   dentro de la página, con la consola ya tranquila. */
const RUTAS = [
  {
    ruta: "/personalidad",
    aserciones: `(() => {
      const f = [];
      const P = (window.PSICO || {}).personalidad;
      if (!P) return ["window.PSICO.personalidad no cargó"];
      if (document.querySelectorAll(".superficies a").length !== 4) f.push("falta el conmutador de las cuatro superficies");
      if (!document.querySelector('.superficies a[aria-current="page"]')?.textContent.includes("Personalidad")) f.push("el conmutador no marca Personalidad");
      if (!document.getElementById("progreso")) f.push("sin barra de progreso");
      if (!(document.getElementById("v-edicion")?.textContent || "").includes(P.fecha)) f.push("la barra no lleva la fecha de la edición");
      // la portada: el radar animado con el polígono de un modelo sobre el panel
      if (!document.querySelector("#pr-lienzo svg polygon.poligono-m")) f.push("el radar de la portada no dibujó el polígono");
      if (document.querySelectorAll("#pr-lienzo .rp-fantasma").length !== P.nModelos) f.push("la portada no dibuja el panel entero de fondo");
      // las fichas: una por modelo, un radar por ficha con seis vértices, y
      // tantas marcas pintadas (vértice, línea y adjetivo firme) como
      // marcas robustas declaran los datos, ni una más
      const fichas = Array.from(document.querySelectorAll("#fichas-host article.ficha-m"));
      if (fichas.length !== P.nModelos) f.push("fichas: " + fichas.length + " (los datos declaran " + P.nModelos + ")");
      const sinRadar = fichas.filter(a => a.querySelectorAll("svg.radar-p").length !== 1 || a.querySelectorAll("svg.radar-p circle.vertice").length !== P.rasgos.length);
      if (sinRadar.length) f.push("fichas sin su radar de " + P.rasgos.length + " vértices: " + sinRadar.map(a => a.dataset.id).join(", "));
      const vert = document.querySelectorAll("#fichas-host circle.vertice.con-marca").length;
      const lineas = document.querySelectorAll("#fichas-host .rasgo-l.sube, #fichas-host .rasgo-l.baja").length;
      const firmes = document.querySelectorAll("#fichas-host .desc b.firme").length;
      if (vert !== P.robustas || lineas !== P.robustas || firmes !== P.robustas) f.push("marcas pintadas: vértices " + vert + ", líneas " + lineas + ", frases " + firmes + " (robustas: " + P.robustas + ")");
      // y cada una en su sitio: el vértice marcado de cada ficha es el rasgo con marca en los datos
      const mal = P.modelos.filter(m => {
        const a = document.querySelector('#fichas-host article.ficha-m[data-id="' + CSS.escape(m.id) + '"]');
        const pintadas = Array.from(a ? a.querySelectorAll("circle.vertice.con-marca") : []).map(c => c.dataset.rasgo).sort().join("");
        return pintadas !== P.rasgos.filter(r => m.rasgos[r.clave].marca).map(r => r.clave).sort().join("");
      }).map(m => m.id);
      if (mal.length) f.push("vértices marcados que no casan con los datos: " + mal.join(", "));
      if (document.querySelectorAll("#fichas-host .fm-rasgos li").length !== P.nModelos * P.rasgos.length) f.push("falta alguna línea de rasgo");
      if (fichas.some(a => !a.querySelector(".fm-desc")?.textContent.trim())) f.push("alguna ficha sin descripción general");
      const equilibrados = P.modelos.filter(m => !P.rasgos.some(r => m.rasgos[r.clave].marca)).length;
      if (fichas.filter(a => a.querySelector(".fm-desc").textContent.startsWith("Perfil equilibrado")).length !== equilibrados) f.push("los perfiles sin marcas no dicen «perfil equilibrado»: esperaba " + equilibrados);
      const avisos = P.modelos.filter(m => m.validez === "aviso").length;
      if (document.querySelectorAll("#fichas-host .cautela").length !== avisos) f.push("avisos ⚠ explicados: esperaba " + avisos);
      // el ISS enlaza a la ficha de /psicobench de cada modelo que lo tiene
      const conISS = P.modelos.filter(m => m.psicobench).length;
      if (document.querySelectorAll('#fichas-host a.iss[href*="#m="]').length !== conISS) f.push("enlaces a la ficha de PsicoBench: esperaba " + conISS);
      if (document.querySelectorAll("#tabla-comparar tbody tr").length !== P.nModelos) f.push("la tabla de comparación no tiene un modelo por fila");
      // curiosidades: las de rasgo con su tira y las del panel
      const curio = document.querySelectorAll("#curiosidades-host .curio");
      if (curio.length < 10) f.push("curiosidades montadas: " + curio.length + " (esperaba ≥10)");
      if (Array.from(curio).some(c => !c.querySelector(".curio-quien")?.textContent.trim())) f.push("alguna curiosidad sin protagonista");
      if (document.querySelectorAll("#curiosidades-host .tira-c i.uno").length < 6) f.push("las tiras de las curiosidades no montaron");
      // qué es y metodología
      if (!document.querySelector("#ejemplo-ficha svg.radar-p")) f.push("el ejemplo de cómo leer una ficha no dibujó su radar");
      if (document.querySelectorAll("#comprobaciones li").length !== P.comprobaciones.length) f.push("faltan comprobaciones explicadas");
      if (document.querySelectorAll("#fuera-host li").length !== P.fuera.length) f.push("modelos fuera: esperaba " + P.fuera.length);
      if (document.querySelectorAll("#limites-host li").length < 4) f.push("las limitaciones no montaron");
      if (!document.querySelector('a[href*="PERSONALIDAD.md"]')) f.push("no enlaza PERSONALIDAD.md");
      return f;
    })()`,
    preparar: `(() => {
      // filtrar por el primer laboratorio
      Array.from(document.querySelectorAll("#mandos-fichas .chip-lab")).find(b => b.dataset.lab === window.PSICO.personalidad.labs[0])?.click();
      return true;
    })()`,
    aserciones2: `(() => {
      const f = [];
      const P = window.PSICO.personalidad, lab = P.labs[0];
      const visibles = () => Array.from(document.querySelectorAll("#fichas-host article.ficha-m")).filter(a => !a.hidden);
      let n = visibles().length, esperado = P.modelos.filter(m => m.lab === lab).length;
      if (n !== esperado) f.push("filtro por " + lab + ": " + n + " fichas (esperaba " + esperado + ")");
      if (visibles().some(a => a.dataset.lab !== lab)) f.push("el filtro deja ver fichas de otro laboratorio");
      // vuelta a todos, ordenar por el último rasgo de más a menos, y buscar
      document.querySelector("#mandos-fichas button.chip:not(.chip-lab)")?.click();
      const t = P.rasgos[P.rasgos.length - 1].clave, sel = document.querySelector("#mandos-fichas select.sel-orden");
      sel.value = "+" + t; sel.dispatchEvent(new Event("change"));
      const ids = visibles().map(a => a.dataset.id);
      if (ids.length !== P.nModelos) f.push("tras «Todos» se ven " + ids.length + " fichas");
      const v = ids.map(id => P.modelos.find(m => m.id === id).rasgos[t].dif);
      if (v.some((x, i) => i && x > v[i - 1])) f.push("el orden por " + t + " no es de más a menos");
      const buscar = document.querySelector("#mandos-fichas input.buscar-f"), q = P.modelos[0].id;
      buscar.value = q; buscar.dispatchEvent(new Event("input"));
      n = visibles().length; esperado = P.modelos.filter(m => (m.id + " " + m.lab).toLowerCase().includes(q.toLowerCase())).length;
      if (n !== esperado) f.push("búsqueda «" + q + "»: " + n + " fichas (esperaba " + esperado + ")");
      return f;
    })()`,
  },
  {
    ruta: "/benchmark",
    aserciones: `(() => {
      const f = [];
      // B2: posicion null ⇔ celda n/c, derivado de los datos — sin nombrar
      // modelos (el hardcode de qwen3.6 rompía en cuanto se re-midiera o
      // entrara otra medición del mismo alias). OJO: DATOS es const de
      // script, NO window.DATOS — el B3 original caía en su fallback sin
      // que nadie lo viera.
      const D = typeof DATOS !== "undefined" ? DATOS : null;
      if (!D || !Array.isArray(D.entradas)) f.push("no veo DATOS.entradas");
      const sinPos = ((D || {}).entradas || [])
        .filter(e => e.posicion == null).length;
      const filas = Array.from(document.querySelectorAll(
        "#sec-clasificacion tbody tr"));
      if (!filas.length) f.push("la tabla clasificatoria no tiene filas");
      const primeras = filas.map(tr =>
        (tr.querySelector("td")?.textContent || "").trim());
      const nc = primeras.filter(c => c === "n/c").length;
      if (nc !== sinPos)
        f.push("celdas n/c: " + nc + " (los datos declaran " + sinPos +
               " entradas sin posición)");
      const raras = primeras.filter(c => c !== "n/c" && !/^=?\\d+$/.test(c));
      if (raras.length)
        f.push("celdas de puesto ilegibles: " + raras.join(", "));
      // B3: tantas puntas de eje como ejes declaren los datos, sin solapes
      // (sin fallback: si los datos no se ven, eso ES el fallo)
      const ejes = D && Array.isArray(D.ejes) ? D.ejes.length : -1;
      const lineas = document.querySelectorAll(".radar-svg line");
      if (lineas.length !== ejes) f.push("radios del radar: " + lineas.length + " (esperaba " + ejes + ")");
      const puntas = new Set(Array.from(lineas).map(l =>
        l.getAttribute("x2") + "," + l.getAttribute("y2")));
      if (puntas.size !== lineas.length)
        f.push("radios superpuestos: " + puntas.size + " puntas únicas de " + lineas.length);
      // B4: el denominador del método sale de los datos
      const sec = document.getElementById("sec-metodo");
      if (sec) {
        sec.closest("body"); // método puede estar oculto: renderiza al pulsar
      }
      return f;
    })()`,
    preparar: `(() => {
      // el método y el radar renderizan al entrar en su pestaña
      const botones = Array.from(document.querySelectorAll("nav button"));
      botones.forEach(b => b.click());
      return true;
    })()`,
    aserciones2: `(() => {
      const f = [];
      const met = document.getElementById("sec-metodo").textContent;
      const n = document.querySelectorAll("tbody tr").length ? undefined : f.push("sin filas");
      if (!/Correlaciones entre ejes \\(\\d+ mediciones\\)/.test(met))
        f.push("falta el denominador dinámico en el método");
      if (met.includes("(16 mediciones)")) f.push("el método sigue diciendo 16 mediciones");
      if (!met.includes("E-IC-1")) f.push("el método no cita la unidad de remuestreo (E-IC-1)");
      return f;
    })()`,
  },
  {
    ruta: "/viewer",
    aserciones: `(() => {
      const f = [];
      if (!document.getElementById("lienzo")) f.push("sin canvas #lienzo");
      const feed = document.getElementById("feed");
      if (feed && !feed.children.length) f.push("el feed está vacío");
      if (!document.getElementById("tituloSesion")?.textContent.trim())
        f.push("sin título de sesión: el replay no cargó");
      return f;
    })()`,
  },
];

/* Las cuatro páginas «Verloop» (PLAN_PSICOBENCH_VERLOOP.md y
   PLAN_WEB_VERLOOP.md), en producción desde el 30-10-2026. */
RUTAS.push({
  ruta: "/psicobench",
  aserciones: `(() => {
    const f = [];
    const P = window.PSICO;
    if (!P) return ["window.PSICO no cargó"];
    const n = P.benchmark.entradas.length;
    // portada en dos bloques: el titular y, debajo, la lámina como ficha
    if (!document.querySelector("#portada h1")) f.push("sin titular de portada");
    const s = document.querySelector("#lamina-octogono svg");
    if (!s) f.push("la lámina no montó");
    else {
      if (s.querySelectorAll(".perfil-fondo").length !== n) f.push("perfiles finos de la lámina: " + s.querySelectorAll(".perfil-fondo").length + " (esperaba " + n + ")");
      if (s.querySelectorAll(".cuna").length !== 8) f.push("la lámina no tiene ocho sectores de eje");
      if (!s.querySelector("polygon.perfil")) f.push("la lámina no dibuja el perfil");
    }
    if (!document.getElementById("lm-nombre")?.textContent.trim() || document.getElementById("lm-nombre").textContent === "—") f.push("la ficha de la lámina no tiene medición");
    if (!document.getElementById("lm-ant") || !document.getElementById("lm-sig") || !document.getElementById("lamina-polvo")) f.push("faltan las flechas o el lienzo del chasquido");
    if (document.querySelectorAll("#perfil .cifras li").length !== 4) f.push("las cuatro cifras no están");
    if (!document.getElementById("ultima-medicion")?.textContent.trim()) f.push("sin fecha de última medición");
    if (document.querySelectorAll(".superficies a").length !== 4) f.push("falta el conmutador de las cuatro superficies");
    if (!Array.from(document.querySelectorAll(".superficies a")).some(a => a.getAttribute("href") === "/completo")) f.push("el conmutador no lleva a /completo");
    // como en /psicobench: la ficha lleva su línea de personalidad si y solo si la medición está en el cuadro
    const idF = document.querySelector("#mandos-ficha select")?.value;
    const enCuadro = (P.personalidad || { modelos: [] }).modelos.some(m => m.psicobench === idF);
    if (enCuadro !== !!document.querySelector(".ficha-hoja .ficha-personalidad a[href*='personalidad']")) f.push("la línea de personalidad de la ficha no cuadra con el cuadro");
    if (!document.getElementById("progreso")) f.push("sin barra de progreso");
    // 01: componentes y ranking descompuesto, con la fórmula que cuadra
    if (document.querySelectorAll("#componentes .componente").length !== 4) f.push("los cuatro componentes del índice no montaron");
    if (document.querySelectorAll("#ranking-iss rect.segmento").length < n) f.push("el ranking del índice no dibuja la descomposición");
    const mal = P.benchmark.entradas.filter(e => Math.abs(((e.ejes.conf + e.ejes.sico) / 2 + e.rupturaMedia / 10 + (e.ejes.auto + e.ejes.brief + e.ejes.prov + e.ejes.sold) / 4 + e.ejes.denu) / 4 * 100 - e.iss) >= 0.15).map(e => e.id);
    if (mal.length) f.push("la fórmula del ISS no cuadra en: " + mal.join(", "));
    // 02: pestañas y barras en el tono del eje
    if (document.querySelectorAll("#mandos-ejes .pestana").length !== P.benchmark.ejes.length) f.push("pestañas de eje incompletas");
    if (document.querySelectorAll("#ranking rect.marca").length !== n) f.push("barras del ranking de eje: " + document.querySelectorAll("#ranking rect.marca").length);
    // 03: el mapa, con una celda de tono por eje y valor
    const filas = Array.from(document.querySelectorAll("table.mapa tbody tr.fila"));
    if (filas.length !== n) f.push("filas del mapa: " + filas.length + " (esperaba " + n + ")");
    const nc = filas.filter(tr => (tr.querySelector("td.pos")?.textContent || "").trim() === "n/c").length;
    if (nc !== P.benchmark.entradas.filter(e => e.posicion == null).length) f.push("celdas n/c no cuadran con los datos");
    if (document.querySelectorAll("table.mapa td.c").length < n * 9) f.push("celdas de eje y reconoce incompletas");
    const conValor = P.benchmark.entradas.reduce((a, e) => a + Object.values(e.ejes).filter(v => v > 0).length + (e.reconocimiento > 0 ? 1 : 0), 0);
    if (document.querySelectorAll("table.mapa td.c.tono").length !== conValor) f.push("celdas en tono: " + document.querySelectorAll("table.mapa td.c.tono").length + " (esperaba " + conValor + ")");
    // 04: cara a cara y sesiones
    // con halo, cada perfil lleva además su copia difuminada (.halo)
    if (document.querySelectorAll("#radar-ab .capa-perfil polygon:not(.halo)").length !== 2) f.push("el radar A/B no tiene dos perfiles");
    if (document.querySelectorAll("table.deltas tbody tr").length !== 9) f.push("la tabla de deltas no tiene 8 ejes + índice");
    if (document.querySelectorAll(".sesion").length !== 2 || document.querySelectorAll(".sesion .tira").length < 2) f.push("las sesiones o sus tiras no montaron");
    // 05: tres mapas con nombre (sin el de réplicas) con un punto por medición
    if (document.querySelectorAll("#mapas-host figure.viz").length !== 3) f.push("mapas con nombre: " + document.querySelectorAll("#mapas-host figure.viz").length + " (esperaba 3)");
    if (document.querySelectorAll("#mapas-host circle.punto").length !== 3 * n) f.push("puntos de los mapas: esperaba " + (3 * n));
    // 06: la ficha; y la escalera de versiones ya no está
    if (document.querySelectorAll(".ficha-hoja .ficha-ejes li").length !== 8) f.push("la ficha no tiene los ocho ejes");
    if (document.getElementById("versiones") || document.getElementById("escalera-host")) f.push("la escalera de versiones sigue en la página");
    if (document.querySelectorAll("section.bloque").length !== 7) f.push("secciones: " + document.querySelectorAll("section.bloque").length + " (esperaba 7)");
    return f;
  })()`,
  preparar: `(() => {
    document.querySelector("table.mapa tbody tr.fila .abrir")?.click();
    document.getElementById("lm-sig")?.click();
    return true;
  })()`,
  aserciones2: `(() => {
    const f = [];
    const det = document.querySelector("table.mapa tr.detalle");
    if (!det || det.querySelectorAll(".d-eje").length < 8) f.push("el detalle de la fila no se abrió con sus ocho ejes");
    if (!document.getElementById("lamina").dataset.transicion && !document.getElementById("lamina").dataset.particulas) f.push("la flecha de la lámina no arrancó el chasquido");
    return f;
  })()`,
});

RUTAS.push({
  ruta: "/completo",
  aserciones: `(() => {
    const f = [];
    if (!window.PSICO) return ["window.PSICO no cargó"];
    if (!document.body.classList.contains("verloop")) f.push("sin el registro Verloop");
    // las mismas piezas que la vigente: figuras, consola y grabación
    const n = document.querySelectorAll("figure.viz").length;
    if (n < 14) f.push("figuras montadas: " + n + " (esperaba ≥14)");
    if (!document.querySelectorAll("#consola-milgram *").length) f.push("la consola no montó");
    if (!document.querySelectorAll("#grabacion *").length) f.push("la grabación no montó");
    // portada en dos bloques: el titular y, debajo, las cifras y la escalera viva
    if (document.querySelector("#portada .panel-escalera")) f.push("la escalera sigue dentro de la portada");
    if (document.querySelectorAll("#escalera.vistazo .cifras li").length !== 4) f.push("las cuatro cifras no están bajo el titular");
    if (!document.querySelectorAll("#pe-peldanos > *").length) f.push("la escalera animada no montó");
    // el conmutador lleva a las hermanas por su ruta limpia
    const sup = Array.from(document.querySelectorAll(".superficies a")).map(a => a.getAttribute("href"));
    if (sup.length !== 4) f.push("falta el conmutador de las cuatro superficies");
    if (!sup.includes("/psicobench")) f.push("el conmutador no lleva a /psicobench: " + sup.join(" "));
    return f;
  })()`,
});

// /personalidad: las comprobaciones de la página anterior (el contenido no
// cambió) y, encima, las de la versión «Verloop»
{
  const i = RUTAS.findIndex((r) => r.ruta === "/personalidad");
  const base = RUTAS[i];
  const nuevas = `(() => {
    const f = [];
    const P = (window.PSICO || {}).personalidad;
    if (!document.body.classList.contains("verloop")) f.push("sin el registro Verloop");
    if (document.querySelector("#portada #pr-lienzo")) f.push("la ficha sigue dentro de la portada");
    if (document.querySelectorAll("#perfil.vistazo .cifras li").length !== 4) f.push("las cuatro cifras no están bajo el titular");
    if (!document.getElementById("lp-ant") || !document.getElementById("lp-sig") || !document.getElementById("lp-polvo")) f.push("faltan las flechas o el lienzo del chasquido");
    const nombre = document.getElementById("pr-nombre")?.textContent;
    const m = P && P.modelos.find((x) => x.id.split("/").pop() === nombre);
    if (!m) f.push("la ficha grande no muestra un modelo del cuadro: " + nombre);
    else if (document.querySelectorAll("#lp-marcas li:not(.ninguna)").length !== P.rasgos.filter((r) => m.rasgos[r.clave].marca).length) f.push("las marcas de la ficha grande no casan con los datos de " + m.id);
    const sup = Array.from(document.querySelectorAll(".superficies a")).map((a) => a.getAttribute("href"));
    if (!sup.includes("/psicobench") || !sup.includes("/personalidad")) f.push("el conmutador no lleva a las hermanas: " + sup.join(" "));
    if (!document.querySelector('#fichas-host a.iss[href^="/psicobench#m="]')) f.push("el ISS de las fichas no lleva a /psicobench");
    return f;
  })()`;
  RUTAS[i] = { ...base,
    aserciones: `(() => [].concat(${base.aserciones}, ${nuevas}))()`,
    preparar: `(() => { const r = (${base.preparar}); document.getElementById("lp-sig")?.click(); return r; })()`,
    aserciones2: `(() => [].concat(${base.aserciones2}, document.getElementById("lamina-p").dataset.particulas ? [] : ["la flecha de la ficha no arrancó el chasquido"]))()`,
  };
}

RUTAS.push({
  ruta: "/",
  aserciones: `(() => {
    const f = [];
    const D = window.PSICO;
    if (!D || !D.personalidad) return ["window.PSICO (con personalidad) no cargó"];
    const B = D.benchmark, P = D.personalidad;
    if (!document.body.classList.contains("verloop")) f.push("sin el registro Verloop");
    const sup = Array.from(document.querySelectorAll(".superficies a")).map((a) => a.getAttribute("href"));
    ["/", "/completo", "/psicobench", "/personalidad"].forEach((r) => { if (!sup.includes(r)) f.push("el conmutador no lleva a " + r); });
    if (!document.querySelector('.superficies a[aria-current="page"]')?.textContent.includes("Resumen")) f.push("el conmutador no marca Resumen");
    // cifras y los dos benchmarks, con sus gráficas vivas
    const vacias = Array.from(document.querySelectorAll("#banco .cifras .n")).filter((n) => !n.textContent.trim() || n.textContent === "—");
    if (vacias.length) f.push("cifras del banco vacías: " + vacias.length);
    if (document.querySelectorAll("#mini-iss circle").length !== B.entradas.length) f.push("la tira del ISS no tiene un punto por medición");
    if (document.querySelectorAll("#mini-rasgos circle").length !== P.nModelos * P.rasgos.length) f.push("las tiras de rasgos no tienen un punto por modelo y rasgo");
    if (document.querySelectorAll("#mini-rasgos circle.firme").length !== P.robustas) f.push("los puntos firmes no son las " + P.robustas + " marcas robustas");
    if (!document.getElementById("puente").hidden && document.querySelectorAll("#puente-rasgos li").length !== P.rasgos.length) f.push("el puente no lleva un rasgo por fila");
    // los clásicos, el test y los hallazgos, todos con su cifra
    const sinCifra = Array.from(document.querySelectorAll("#como dd, #hallazgos .dato")).filter((n) => !n.textContent.trim());
    if (sinCifra.length) f.push("cifras sin rellenar en cómo se mide u hallazgos: " + sinCifra.length);
    if (!document.querySelector("#quiz .cuerpo .pregunta") || !document.querySelectorAll("#quiz .reproductor-clips .clip").length) f.push("el test «Ponte en la silla» no montó");
    if (document.querySelectorAll(".lecturas a.lectura").length !== 4) f.push("faltan las cuatro lecturas");
    return f;
  })()`,
});

const ORDEN = ["/", "/completo", "/psicobench", "/personalidad", "/benchmark", "/viewer"];
RUTAS.sort((a, b) => ORDEN.indexOf(a.ruta) - ORDEN.indexOf(b.ruta));

/* ── arranque de Chrome con puerto de depuración ─────────────────────────── */
const perfil = mkdtempSync(join(tmpdir(), "smoke-chrome-"));
const chrome = spawn(CHROME, [
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--remote-debugging-port=0", `--user-data-dir=${perfil}`, "about:blank",
], { stdio: ["ignore", "ignore", "pipe"] });

const puerto = await new Promise((res, rej) => {
  let err = "";
  chrome.stderr.on("data", (d) => {
    err += d;
    const m = err.match(/DevTools listening on ws:\/\/127\.0\.0\.1:(\d+)\//);
    if (m) res(Number(m[1]));
  });
  chrome.on("exit", () => rej(new Error("Chrome murió al arrancar:\n" + err)));
  setTimeout(() => rej(new Error("Chrome no abrió el puerto de depuración")), 15000);
});

function cdp(ws) {
  let id = 0;
  const pendientes = new Map(), oyentes = [];
  ws.addEventListener("message", (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pendientes.has(m.id)) {
      const { res, rej } = pendientes.get(m.id);
      pendientes.delete(m.id);
      m.error ? rej(new Error(m.error.message)) : res(m.result);
    } else if (m.method) oyentes.forEach((f) => f(m));
  });
  return {
    enviar: (method, params = {}) => new Promise((res, rej) => {
      pendientes.set(++id, { res, rej });
      ws.send(JSON.stringify({ id, method, params }));
    }),
    on: (f) => oyentes.push(f),
  };
}

async function probarRuta(spec) {
  const url = BASE + spec.ruta;
  const t = await fetch(`http://127.0.0.1:${puerto}/json/new?${new URLSearchParams({ url: "about:blank" })}`,
    { method: "PUT" }).then((r) => r.json());
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = () => rej(new Error("ws")); });
  const c = cdp(ws);

  const fallos = [];
  c.on((m) => {
    if (m.method === "Network.responseReceived") {
      const r = m.params.response;
      if (r.status >= 400) fallos.push(`recurso ${r.status}: ${r.url.replace(BASE, "")}`);
    }
    if (m.method === "Network.loadingFailed" && !m.params.canceled)
      fallos.push(`recurso falló: ${m.params.errorText}`);
    if (m.method === "Runtime.exceptionThrown")
      fallos.push(`excepción: ${m.params.exceptionDetails.text} ${
        m.params.exceptionDetails.exception?.description?.split("\n")[0] || ""}`);
    if (m.method === "Runtime.consoleAPICalled" && m.params.type === "error")
      fallos.push(`console.error: ${m.params.args.map((a) => a.value ?? a.description).join(" ").slice(0, 120)}`);
  });

  await c.enviar("Network.enable");
  await c.enviar("Runtime.enable");
  await c.enviar("Page.enable");
  const cargada = new Promise((res) => c.on((m) => m.method === "Page.loadEventFired" && res()));
  await c.enviar("Page.navigate", { url });
  await cargada;
  await new Promise((r) => setTimeout(r, 1200));   // deja asentar los montajes

  async function evalua(expr, etiqueta) {
    const { result } = await c.enviar("Runtime.evaluate",
      { expression: expr, returnByValue: true });
    (result.value || []).forEach((f) => fallos.push(`${etiqueta}: ${f}`));
  }
  await evalua(spec.aserciones, "aserción");

  // móvil: a 390px ninguna página puede desbordar el viewport
  await c.enviar("Emulation.setDeviceMetricsOverride",
    { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  const recargada = new Promise((res) => c.on((m) => m.method === "Page.loadEventFired" && res()));
  await c.enviar("Page.reload");
  await recargada;
  await new Promise((r) => setTimeout(r, 900));
  await evalua(`(() => {
    const d = document.documentElement;
    const extra = d.scrollWidth - d.clientWidth;
    const f = extra > 2 ? ["desborde horizontal a 390px: " + extra + "px"] : [];
    // la barra es fija y el documento recorta en horizontal: un conmutador
    // que no cabe no desborda la página, se corta sin avisar. Se mide aparte.
    const ult = document.querySelector(".superficies a:last-child");
    if (ult && ult.getBoundingClientRect().right > d.clientWidth + 1) f.push("el conmutador de superficies no cabe a 390px");
    return f;
  })()`, "móvil");
  await c.enviar("Emulation.clearDeviceMetricsOverride");
  if (spec.preparar) {
    await c.enviar("Runtime.evaluate", { expression: spec.preparar });
    await new Promise((r) => setTimeout(r, 500));
    if (spec.aserciones2) await evalua(spec.aserciones2, "aserción");
  }

  ws.close();
  await fetch(`http://127.0.0.1:${puerto}/json/close/${t.id}`).catch(() => {});
  return fallos;
}

let total = 0;
for (const spec of RUTAS) {
  const fallos = await probarRuta(spec).catch((e) => [`no se pudo probar: ${e.message}`]);
  const ok = fallos.length === 0;
  console.log(`${ok ? "  ok " : "FALLA"} ${spec.ruta}`);
  fallos.forEach((f) => console.log(`        · ${f}`));
  total += fallos.length;
}

chrome.kill();
await new Promise((r) => { chrome.on("exit", r); setTimeout(r, 3000); });
rmSync(perfil, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
console.log(total === 0 ? "\nSMOKE: OK" : `\nSMOKE: ${total} fallo(s)`);
process.exit(total === 0 ? 0 : 1);
