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
    ruta: "/benchmark",
    aserciones: `(() => {
      const f = [];
      // B2: la entrada sin posición muestra n/c, jamás un puesto
      const fila = Array.from(document.querySelectorAll("tbody tr"))
        .find(tr => tr.textContent.includes("qwen3.6") && !tr.textContent.includes("35b"));
      if (!fila) f.push("no encuentro la fila de qwen3.6");
      else {
        const celda = fila.querySelector("td").textContent.trim();
        if (celda !== "n/c") f.push("qwen3.6 muestra «" + celda + "» en vez de n/c");
      }
      // B3: tantas puntas de eje como ejes declaren los datos, sin solapes
      const ejes = (window.DATOS || {}).ejes ? DATOS.ejes.length : 8;
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
