/* ===========================================================================
   BenchAI · prueba de interacción de la versión en preparación de PsicoBench
   ---------------------------------------------------------------------------
   Abre /psicobench-nueva en Chrome headless y comprueba que sobrevive todo lo
   que la página vigente deja hacer (PLAN_PSICOBENCH_VERLOOP.md, fase 4): la
   dirección #m= en los dos sentidos, los selectores A/B y el intercambio, las
   pestañas de eje, las pruebas de sesión, la reordenación y los filtros del
   mapa, la fila desplegable, la descarga CSV y el enlace al JSON, la barra
   de progreso, el menú de secciones y, en estrecho, que nada desborde. Sin
   dependencias, como web/smoke.mjs. No se publica: es de la previa.

     python3 web/publicar.py --previa && python3 web/servir_previa.py &
     node web/previa_interaccion.prueba.mjs http://127.0.0.1:8743/psicobench-nueva
   =========================================================================== */
import { spawn } from "node:child_process";
import { existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const URL_ = process.argv[2] || "http://127.0.0.1:8743/psicobench-nueva";
const CHROME = process.env.CHROME || [
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium",
].find(existsSync);
if (!CHROME) { console.error("prueba: no encuentro Chrome (define CHROME=)"); process.exit(2); }
const perfil = mkdtempSync(join(tmpdir(), "int-"));
const puerto = 9650 + Math.floor(Math.random() * 140);
const ch = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${puerto}`, `--user-data-dir=${perfil}`,
  "--no-first-run", "--no-default-browser-check", "about:blank"], { stdio: "ignore" });
const dormir = (ms) => new Promise((r) => setTimeout(r, ms));
let ws;
for (let i = 0; i < 50 && !ws; i++) {
  try { const l = await (await fetch(`http://127.0.0.1:${puerto}/json/list`)).json(); const p = l.find((x) => x.type === "page"); if (p) ws = new WebSocket(p.webSocketDebuggerUrl); }
  catch { await dormir(200); }
}
await new Promise((r) => ws.addEventListener("open", r));
let id = 0; const esperas = new Map(); const errores = [];
ws.addEventListener("message", (m) => {
  const d = JSON.parse(m.data);
  if (d.id && esperas.has(d.id)) { esperas.get(d.id)(d); esperas.delete(d.id); }
  if (d.method === "Runtime.exceptionThrown") errores.push(d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text);
  if (d.method === "Runtime.consoleAPICalled" && d.params.type === "error") errores.push(d.params.args.map((a) => a.value || a.description).join(" "));
  if (d.method === "Log.entryAdded" && d.params.entry.level === "error") errores.push(d.params.entry.text);
});
const cdp = (method, params = {}) => new Promise((r) => { const n = ++id; esperas.set(n, r); ws.send(JSON.stringify({ id: n, method, params })); });
const ev = async (e) => { const r = await cdp("Runtime.evaluate", { expression: e, returnByValue: true, awaitPromise: true }); if (r.result.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description || "eval"); return r.result.result.value; };
const fallos = []; const ok = (c, m) => { console.log((c ? "  ok  " : " FAIL ") + m); if (!c) fallos.push(m); };

await cdp("Page.enable"); await cdp("Runtime.enable"); await cdp("Log.enable");
const vista = (w, h) => cdp("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 768 });
const cargar = async (sufijo = "") => { await cdp("Page.navigate", { url: URL_ + sufijo }); await dormir(2600); };
const pulsar = (sel) => ev(`(() => { const n = ${sel}; if (!n) return false; n.click(); return true; })()`);
const texto = (sel) => ev(`(${sel} || {}).textContent`);
await vista(1440, 900);

// 1 · #m= en los dos sentidos: dirección → ficha y lámina; ficha → dirección
await cargar("#m=claude-opus-5");
let r = await ev(`({ f: document.querySelector('#mandos-ficha select').value, l: document.getElementById('lm-nombre').textContent, h: document.querySelector('.ficha-hoja h3').textContent })`);
ok(r.f === "claude-opus-5" && r.l === "claude-opus-5" && r.h === "claude-opus-5", `#m=claude-opus-5 abre ficha y lámina (${r.f} / ${r.l})`);
await ev(`(() => { const s = document.querySelector('#mandos-ficha select'); s.value = 'grok-4.5'; s.dispatchEvent(new Event('change')); })()`);
await dormir(1100);
r = await ev(`({ h: location.hash, l: document.getElementById('lm-nombre').textContent, f: document.querySelector('.ficha-hoja h3').textContent })`);
ok(r.h === "#m=grok-4.5" && r.l === "grok-4.5" && r.f === "grok-4.5", `el selector de la ficha mueve la dirección y la lámina (${r.h}, ${r.l})`);
await ev(`location.hash = '#m=' + encodeURIComponent('gemini-3.7-flash')`); await dormir(1100);
r = await ev(`({ f: document.querySelector('.ficha-hoja h3').textContent, l: document.getElementById('lm-nombre').textContent })`);
ok(r.f === "gemini-3.7-flash" && r.l === "gemini-3.7-flash", "un cambio de dirección mueve ficha y lámina");
await cargar("#m=no-existe");
ok((await ev(`document.getElementById('lm-nombre').textContent`)) !== "no-existe" && !/no-existe/.test(await texto(`document.querySelector('.ficha-hoja h3')`)), "un #m= desconocido no rompe la página");

// 2 · cara a cara: selectores, intercambio y botones de la ficha
await cargar();
const ab = () => ev(`({ a: document.querySelector('#mandos-sesiones select:nth-of-type(1)').value, b: document.querySelector('#mandos-sesiones select:nth-of-type(2)').value,
  ca: document.querySelector('#deltas-ab .cab-ab .a').textContent, cb: document.querySelector('#deltas-ab .cab-ab .b').textContent,
  sa: document.querySelectorAll('#sesiones-host .sesion .quien')[0].firstChild.textContent, sb: document.querySelectorAll('#sesiones-host .sesion .quien')[1].firstChild.textContent,
  filas: document.querySelectorAll('#deltas-ab table.deltas tbody tr').length })`);
let s0 = await ab();
ok(s0.ca.endsWith(s0.a) && s0.cb.endsWith(s0.b) && s0.sa === s0.a && s0.sb === s0.b && s0.filas === 9, `A/B arrancan coherentes (${s0.a} · ${s0.b}, 9 filas de deltas)`);
await pulsar(`[...document.querySelectorAll('#mandos-sesiones button')].find((b) => /intercambiar/.test(b.textContent))`);
let s1 = await ab();
ok(s1.a === s0.b && s1.b === s0.a && s1.sa === s0.b && s1.ca.endsWith(s0.b), "⇄ intercambia selectores, deltas y sesiones");
await ev(`(() => { const s = document.querySelector('#mandos-sesiones select:nth-of-type(1)'); s.value = 'kimi-k3'; s.dispatchEvent(new Event('change')); })()`);
s1 = await ab();
ok(s1.a === "kimi-k3" && s1.sa === "kimi-k3" && s1.ca.endsWith("kimi-k3"), "cambiar A repinta deltas y sesiones");
await pulsar(`[...document.querySelectorAll('.ficha-acciones button')].find((b) => /como B/.test(b.textContent))`);
ok((await ab()).b === (await ev(`document.querySelector('#mandos-ficha select').value`)), "«…como B» de la ficha lleva la medición al selector B");

// 3 · las pruebas de sesión: todas pintan, con su tono
const pruebas = await ev(`[...document.querySelectorAll('#mandos-paradigma button')].map((b) => b.textContent)`);
for (const p of pruebas) {
  await pulsar(`[...document.querySelectorAll('#mandos-paradigma button')].find((b) => b.textContent === ${JSON.stringify(p)})`);
  r = await ev(`({ cols: document.querySelectorAll('#sesiones-host .sesion').length, tiras: document.querySelectorAll('#sesiones-host .tira').length, citas: document.querySelectorAll('#sesiones-host .cita').length, notas: document.querySelectorAll('#sesiones-host .sesion > .nota').length, tono: getComputedStyle(document.getElementById('sesiones-host')).getPropertyValue('--tono').trim() })`);
  ok(r.cols === 2 && (r.tiras + r.citas + r.notas) > 0 && /^#/.test(r.tono), `prueba «${p}»: dos columnas con contenido (${r.tiras} tiras, ${r.citas} citas), tono ${r.tono}`);
}

// 4 · pestañas de eje: una seleccionada, título y tono del eje
const pestanas = await ev(`document.querySelectorAll('#mandos-ejes [role=tab]').length`);
ok(pestanas === 8, `ocho pestañas de eje (${pestanas})`);
await pulsar(`document.querySelectorAll('#mandos-ejes [role=tab]')[1]`);
r = await ev(`({ sel: [...document.querySelectorAll('#mandos-ejes [role=tab]')].filter((t) => t.getAttribute('aria-selected') === 'true').length, tit: document.querySelector('#ranking .titviz').textContent, h3: document.querySelector('#prosa-eje h3').textContent, barras: document.querySelectorAll('#ranking svg rect.marca').length, c: getComputedStyle(document.getElementById('prosa-eje')).getPropertyValue('--c').trim() })`);
ok(r.sel === 1 && /^Obediencia/.test(r.tit) && r.h3 === "Obediencia" && r.c.toUpperCase() === "#7B3DFF", `la segunda pestaña pinta Obediencia en su tono (${r.c}, ${r.barras} barras)`);

// 5 · el mapa: reordenar, filtrar, agrupar y desplegar
const filas = () => ev(`document.querySelectorAll('#heat table.mapa tbody tr.fila').length`);
ok((await filas()) === 39, "el mapa arranca con las 39 mediciones");
await pulsar(`[...document.querySelectorAll('#heat thead th')].find((t) => /Conformidad/.test(t.textContent)).querySelector('button')`);
r = await ev(`(() => { const th = [...document.querySelectorAll('#heat thead th')].find((t) => /Conformidad/.test(t.textContent)); const i = [...th.parentElement.children].indexOf(th); const v = [...document.querySelectorAll('#heat tbody tr.fila')].map((f) => +f.children[i].textContent); return { sort: th.getAttribute('aria-sort'), v }; })()`);
ok(r.sort === "descending" && r.v.every((x, k) => k === 0 || r.v[k - 1] >= x), `una cabecera de eje ordena de más a menos (${r.v.slice(0, 3).join(", ")}…)`);
await pulsar(`[...document.querySelectorAll('#heat thead th')].find((t) => /Conformidad/.test(t.textContent)).querySelector('button')`);
ok((await ev(`[...document.querySelectorAll('#heat thead th')].find((t) => /Conformidad/.test(t.textContent)).getAttribute('aria-sort')`)) === "ascending", "un segundo clic invierte el orden");
const lab = await ev(`(() => { const c = [...document.querySelectorAll('#mandos-mapa .grupo-m button')][1]; c.click(); return { n: +c.querySelector('.n').textContent, lab: c.firstChild.textContent }; })()`);
ok((await filas()) === lab.n, `filtrar por ${lab.lab} deja ${lab.n} filas`);
await pulsar(`[...document.querySelectorAll('#mandos-mapa button')].find((b) => b.textContent === 'Todos')`);
ok((await filas()) === 39, "«Todos» devuelve las 39");
await pulsar(`[...document.querySelectorAll('#mandos-mapa button')].find((b) => /Agrupar/.test(b.textContent))`);
const nLabs = await ev(`document.querySelectorAll('#mandos-mapa .grupo-m button').length - 1`);
ok((await filas()) === nLabs, `agrupar deja una fila por laboratorio (${nLabs})`);
await pulsar(`[...document.querySelectorAll('#mandos-mapa button')].find((b) => /Agrupar/.test(b.textContent))`);
await pulsar(`document.querySelector('#heat tbody tr.fila button.abrir')`);
r = await ev(`({ det: document.querySelectorAll('#heat tr.detalle').length, exp: document.querySelector('#heat tbody tr.fila button.abrir').getAttribute('aria-expanded'), ejes: document.querySelectorAll('#heat tr.detalle .d-eje').length })`);
ok(r.det === 1 && r.exp === "true" && r.ejes === 8, "una fila se despliega con sus ocho ejes");
r = await ev(`(() => { const td = document.querySelector('#heat tbody td.c.tono'); const cs = getComputedStyle(td); return { bg: cs.backgroundColor, c: cs.color }; })()`);
ok(/rgb/.test(r.bg) && r.bg !== "rgba(0, 0, 0, 0)", `las celdas llevan su tono (${r.bg} con texto ${r.c})`);

// 6 · descarga: el CSV sale de los datos, con cabecera y 39 filas
r = await ev(`new Promise((res) => {
  const orig = URL.createObjectURL; const clic = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () { if (!this.download) clic.call(this); };
  URL.createObjectURL = (b) => { b.text().then((t) => { URL.createObjectURL = orig; HTMLAnchorElement.prototype.click = clic; res({ t: t.replace(/^\\uFEFF/, ''), tipo: b.type }); }); return 'blob:prueba'; };
  [...document.querySelectorAll('#mandos-descarga button')].find((b) => /CSV/.test(b.textContent)).click();
})`);
const lineas = r.t.split("\n");
ok(/^text\/csv/.test(r.tipo) && /^id,modelo,lab,proveedor,fecha,iss/.test(lineas[0]) && lineas.length === 40, `el CSV tiene cabecera y 39 filas (${lineas.length - 1})`);
const hrefJSON = await ev(`[...document.querySelectorAll('#mandos-descarga a')].find((a) => /JSON/.test(a.textContent)).href`);
const resp = await fetch(hrefJSON);
ok(resp.ok && Array.isArray((await resp.json()).entradas ?? [1]), `el enlace al JSON responde (${new URL(hrefJSON).pathname}, ${resp.status})`);

// 7 · progreso de lectura y menú de secciones
// el sitio desplaza con `scroll-behavior: smooth`: aquí se salta sin animación
await ev(`document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo(0, 0)`); await dormir(300);
const p0 = await ev(`parseFloat(document.getElementById('progreso').style.width) || 0`);
await ev(`document.getElementById('mapa').scrollIntoView()`); await dormir(500);
r = await ev(`({ p: parseFloat(document.getElementById('progreso').style.width), act: (document.querySelector('.navmini a[aria-current=true]') || {}).getAttribute?.('href') })`);
ok(r.p > p0 && r.p > 5 && r.p < 95, `la barra de progreso avanza (${p0.toFixed(0)} % → ${r.p.toFixed(0)} %)`);
ok(r.act === "#mapa", `el menú marca la sección a la vista (${r.act})`);

// 8 · estrecho: sin desbordes y con el mapa desplazable dentro de su caja
for (const [w, hh] of [[390, 844], [320, 640]]) {
  await vista(w, hh); await cargar();
  r = await ev(`(() => { const W = document.documentElement.clientWidth; const env = document.querySelector('.mapa-envuelto'); const cs = getComputedStyle(env);
    return { sw: document.documentElement.scrollWidth, W, scroll: env.scrollWidth > env.clientWidth && /auto|scroll/.test(cs.overflowX), halo: [...document.querySelectorAll('.radar .halo')].every((n) => getComputedStyle(n).display === 'none'),
      h1: parseFloat(getComputedStyle(document.querySelector('.portada h1')).fontSize), una: getComputedStyle(document.querySelector('.metodo-cajas')).gridTemplateColumns.split(' ').length }; })()`);
  ok(r.sw === r.W, `${w} px: sin scroll horizontal (${r.sw} = ${r.W})`);
  ok(r.scroll, `${w} px: la tabla del mapa se desplaza dentro de su caja`);
  ok(r.halo, `${w} px: sin halo en los octógonos`);
  ok(r.una === 1, `${w} px: el método a una columna`);
  console.log(`       (${w} px: titular de portada a ${r.h1} px)`);
}
// en táctil no hay hover: un toque sobre un eje lo enciende
await cdp("Emulation.setTouchEmulationEnabled", { enabled: true, maxTouchPoints: 5 });
await vista(390, 844); await cargar();
await ev(`document.documentElement.style.scrollBehavior = 'auto'; document.querySelector('#lamina-octogono svg').scrollIntoView({ block: 'center' })`); await dormir(300);
const g = await ev(`(() => { const s = document.querySelector('#lamina-octogono svg'); const r = s.getBoundingClientRect(); const lin = s.querySelectorAll('.radar-radio')[1]; const k = r.width / s.viewBox.baseVal.width; return { x: r.left + (+lin.getAttribute('x1') + (+lin.getAttribute('x2') - +lin.getAttribute('x1')) * 0.6) * k, y: r.top + (+lin.getAttribute('y1') + (+lin.getAttribute('y2') - +lin.getAttribute('y1')) * 0.6) * k }; })()`);
await dormir(300);
const n0 = await ev(`document.getElementById('lm-nombre').textContent`);
await cdp("Input.dispatchTouchEvent", { type: "touchStart", touchPoints: [{ x: g.x, y: g.y }] });
await cdp("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
await dormir(500);
r = await ev(`({ t: document.getElementById('ll-titulo').textContent, n: document.getElementById('lm-nombre').textContent })`);
ok(r.t === "Obediencia", `390 px táctil: un toque en el eje lo lee y la lectura se queda (${r.t})`);
ok(r.n === n0, `390 px táctil: el toque no cambia de medición aunque caiga en un perfil fino (${r.n})`);
await pulsar(`document.getElementById('lm-sig')`); await dormir(1100);
ok((await ev(`document.getElementById('lm-nombre').textContent`)) !== n0, "390 px táctil: ▶ sí cambia de medición");
// deslizar la ficha con el dedo hacia la izquierda es «siguiente»
await dormir(1800);
const antesDesliz = await ev(`document.getElementById('lm-nombre').textContent`);
const pie = await ev(`(() => { const r = document.querySelector('.lamina-pie').getBoundingClientRect(); return { x: r.left + r.width * 0.8, y: r.top + 20 }; })()`);
await cdp("Input.dispatchTouchEvent", { type: "touchStart", touchPoints: [{ x: pie.x, y: pie.y }] });
for (let i = 1; i <= 6; i++) await cdp("Input.dispatchTouchEvent", { type: "touchMove", touchPoints: [{ x: pie.x - i * 30, y: pie.y + i }] });
await cdp("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
await dormir(2600);
const trasDesliz = await ev(`document.getElementById('lm-nombre').textContent`);
ok(trasDesliz !== antesDesliz, `390 px táctil: deslizar la ficha a la izquierda pasa a la siguiente (${antesDesliz} → ${trasDesliz})`);
await cdp("Emulation.setTouchEmulationEnabled", { enabled: false });

// 9 · estados: movimiento reducido, más contraste e impresión
await vista(1440, 900);
await cdp("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
await cargar();
r = await ev(`({ ocultos: [...document.querySelectorAll('.aparece')].filter((n) => getComputedStyle(n).opacity !== '1').length, total: document.querySelectorAll('.aparece').length })`);
ok(r.ocultos === 0, `con movimiento reducido todo está a la vista sin hacer scroll (${r.total} bloques)`);
await cdp("Emulation.setEmulatedMedia", { features: [{ name: "prefers-contrast", value: "more" }] }); await dormir(300);
r = await ev(`({ grano: getComputedStyle(document.querySelector('.portada'), '::after').display, fondo: getComputedStyle(document.querySelector('.portada .fondo')).display, em: getComputedStyle(document.querySelector('.portada h1 em')).webkitTextStrokeWidth })`);
ok(r.grano === "none" && r.fondo === "none" && r.em === "0px", "con más contraste: sin grano, sin resplandores y sin texto hueco");
await cdp("Emulation.setEmulatedMedia", { media: "print", features: [] }); await dormir(300);
r = await ev(`({ fondo: getComputedStyle(document.body).backgroundColor, tinta: getComputedStyle(document.querySelector('h2.titulo')).color, barra: getComputedStyle(document.getElementById('barra')).display, aviso: getComputedStyle(document.querySelector('.v-previa')).display, mandos: getComputedStyle(document.getElementById('mandos-mapa')).display, enlace: getComputedStyle(document.querySelector('.caja-metodo a')).color, esquema: getComputedStyle(document.documentElement).colorScheme })`);
ok(r.fondo === "rgb(255, 255, 255)" && r.tinta === "rgb(0, 0, 0)" && r.esquema === "light", `al imprimir, registro claro (${r.fondo}, texto ${r.tinta}, esquema ${r.esquema})`);
ok(r.barra === "none" && r.aviso === "none" && r.mandos === "none", "al imprimir, sin barra, sin aviso de previa y sin mandos");
ok(r.enlace === "rgb(0, 0, 0)", "al imprimir, los enlaces se leen");
const pdf = await cdp("Page.printToPDF", { printBackground: true, preferCSSPageSize: true });
const paginas = (Buffer.from(pdf.result.data, "base64").toString("latin1").match(/\/Type\s*\/Page[^s]/g) || []).length;
ok(paginas >= 15 && paginas <= 40, `el PDF sale con ${paginas} páginas`);
await cdp("Emulation.setEmulatedMedia", { media: "", features: [] });

ok(errores.length === 0, `sin errores de consola${errores.length ? ": " + errores.join(" | ") : ""}`);
console.log(fallos.length ? `\nINTERACCIÓN: ${fallos.length} fallo(s)` : "\nINTERACCIÓN: todo OK");
ws.close(); ch.kill(); await dormir(300); rmSync(perfil, { recursive: true, force: true });
process.exit(fallos.length ? 1 : 0);
