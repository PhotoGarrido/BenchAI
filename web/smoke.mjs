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
     node web/smoke.mjs http://localhost:3000 # contra un serve local
   =========================================================================== */

import { spawn } from "node:child_process";
import { readFileSync, existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const BASE = (process.argv[2] || "https://benchai.tech").replace(/\/$/, "");

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
    ruta: "/",
    aserciones: `(() => {
      const f = [];
      if (!window.PSICO) f.push("window.PSICO no cargó");
      if (!document.querySelector(".botonera .llave-b")) f.push("la botonera no montó");
      if (!document.querySelector(".firmas .fila-f")) f.push("las firmas no montaron");
      return f;
    })()`,
  },
  {
    ruta: "/completo",
    aserciones: `(() => {
      const f = [];
      const n = document.querySelectorAll("figure.viz").length;
      if (n < 14) f.push("figuras montadas: " + n + " (esperaba ≥14)");
      if (!document.querySelectorAll("#consola-milgram *").length) f.push("la consola no montó");
      return f;
    })()`,
  },
  {
    ruta: "/psicobench",
    aserciones: `(() => {
      const f = [];
      if (!window.PSICO) f.push("window.PSICO no cargó");
      const n = (window.PSICO || { benchmark: { entradas: [] } }).benchmark.entradas.length;
      const filas = Array.from(document.querySelectorAll("table.mapa tbody tr.fila"));
      if (filas.length !== n) f.push("filas del mapa: " + filas.length + " (los datos declaran " + n + ")");
      // el rango de posición sale de los datos: tantas n/c como entradas sin posición
      const sinPos = (window.PSICO || { benchmark: { entradas: [] } }).benchmark.entradas
        .filter(e => e.posicion == null).length;
      const nc = filas.filter(tr => (tr.querySelector("td.pos")?.textContent || "").trim() === "n/c").length;
      if (nc !== sinPos) f.push("celdas n/c: " + nc + " (esperaba " + sinPos + ")");
      const raras = filas.map(tr => (tr.querySelector("td.pos")?.textContent || "").trim())
        .filter(c => c !== "n/c" && !/^\\d+(–\\d+)?$/.test(c));
      if (raras.length) f.push("rangos de posición ilegibles: " + raras.join(", "));
      const celdas = document.querySelectorAll("table.mapa td.c").length;
      if (celdas < n * 8) f.push("celdas de eje: " + celdas + " (esperaba ≥ " + (n * 8) + ")");
      if (!document.getElementById("ultima-medicion")?.textContent.trim()) f.push("sin fecha de última medición");
      // El índice: cuatro componentes, y la descomposición dibujada solo si
      // cuadra con el ISS publicado (si el instrumento cambia de fórmula, salta)
      if (document.querySelectorAll("#componentes .componente").length !== 4) f.push("los cuatro componentes del índice no montaron");
      const segs = document.querySelectorAll("#ranking-iss rect.segmento").length;
      if (segs < n) f.push("el ranking del índice no dibuja la descomposición (" + segs + " segmentos): ¿ha cambiado la fórmula del ISS?");
      const P = window.PSICO;
      if (P) {
        const mal = P.benchmark.entradas.filter(e => {
          const calc = ((e.ejes.conf + e.ejes.sico) / 2 + e.rupturaMedia / 10 + (e.ejes.auto + e.ejes.brief + e.ejes.prov + e.ejes.sold) / 4 + e.ejes.denu) / 4 * 100;
          return Math.abs(calc - e.iss) >= 0.15;
        }).map(e => e.id);
        if (mal.length) f.push("la fórmula del ISS que dibuja la web no cuadra con el publicado en: " + mal.join(", "));
      }
      // F1: una pestaña por eje y el ranking del eje elegido, con una barra
      // etiquetada por medición y su IC
      const pestanas = document.querySelectorAll("#mandos-ejes .pestana").length;
      const ejes = (window.PSICO || { benchmark: { ejes: [] } }).benchmark.ejes.length;
      if (pestanas !== ejes) f.push("pestañas de eje: " + pestanas + " (esperaba " + ejes + ")");
      if (!document.querySelector("#mandos-ejes .pestana[aria-pressed=\\"true\\"]")) f.push("ninguna pestaña de eje activa");
      const barras = document.querySelectorAll("#ranking rect.marca").length;
      if (barras !== n) f.push("barras del ranking: " + barras + " (esperaba " + n + ")");
      // F2: dos sesiones lado a lado con sus tiras
      if (document.querySelectorAll(".sesion").length !== 2) f.push("las dos sesiones no montaron");
      if (document.querySelectorAll(".sesion .tira").length < 2) f.push("las tiras de sesión no montaron");
      // F3: radar A/B con dos polígonos de perfil, deltas por eje, cuatro mapas
      if (document.querySelectorAll("#radar-ab .capa-perfil polygon").length !== 2) f.push("el radar A/B no tiene dos perfiles");
      if (document.querySelectorAll("table.deltas tbody tr").length !== 9) f.push("la tabla de deltas no tiene 8 ejes + índice");
      if (document.querySelectorAll("#mapas-host figure.viz").length !== 4) f.push("mapas con nombre: " + document.querySelectorAll("#mapas-host figure.viz").length + " (esperaba 4)");
      if (document.querySelectorAll("#mapas-host circle.punto").length !== 3 * n) f.push("puntos de los mapas: esperaba " + (3 * n));
      // F4: ficha montada con sus ocho ejes y la escalera con una línea por medición
      if (document.querySelectorAll(".ficha-hoja .ficha-ejes li").length !== 8) f.push("la ficha no tiene los ocho ejes");
      if (document.querySelectorAll("#escalera-host .linea-v").length !== n) f.push("escalera de versiones: esperaba " + n + " líneas");
      return f;
    })()`,
    preparar: `(() => {
      // abrir la primera fila: el detalle con IC y n tiene que montar
      document.querySelector("table.mapa tbody tr.fila .abrir")?.click();
      return true;
    })()`,
    aserciones2: `(() => {
      const f = [];
      const det = document.querySelector("table.mapa tr.detalle");
      if (!det) f.push("el detalle de la fila no se abrió");
      else if (det.querySelectorAll(".d-eje").length < 8) f.push("el detalle no trae los ocho ejes");
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
    return extra > 2 ? ["desborde horizontal a 390px: " + extra + "px"] : [];
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
