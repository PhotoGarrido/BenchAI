/* ===========================================================================
   BenchAI · prueba de la lámina de la versión en preparación de PsicoBench
   ---------------------------------------------------------------------------
   Abre /psicobench-nueva en Chrome headless (requestAnimationFrame a ritmo
   real, que un panel oculto no da) y comprueba la portada «Lámina A · Morph»
   (PLAN_PSICOBENCH_VERLOOP.md, fase 2): perfiles finos, sectores, halo,
   interpolación entre mediciones, contador del ISS, onda, hover, teclado,
   clic en un perfil, arranque desde #m= y movimiento reducido. Sin
   dependencias, como web/smoke.mjs. No se publica: es de la previa.

     python3 web/publicar.py --previa && python3 web/servir_previa.py &
     node web/previa_lamina.prueba.mjs http://127.0.0.1:8743/psicobench-nueva
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
const perfil = mkdtempSync(join(tmpdir(), "lam-"));
const puerto = 9800 + Math.floor(Math.random() * 150);
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
await cdp("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });

async function cargar() { await cdp("Page.navigate", { url: URL_ }); await dormir(2600); }

// 1 · carga y entrada animada
await cargar();
const ini = await ev(`(() => { const s = document.querySelector('#lamina-octogono svg'); return { fondo: s.querySelectorAll('.perfil-fondo').length, cunas: s.querySelectorAll('.cuna').length, vertices: s.querySelectorAll('.vertice').length, halo: s.querySelectorAll('.halo').length, nombre: document.getElementById('lm-nombre').textContent, iss: document.getElementById('lm-iss').textContent, rol: s.getAttribute('role'), tab: s.getAttribute('tabindex') }; })()`);
ok(ini.fondo === 39, `39 perfiles finos (${ini.fondo})`);
ok(ini.cunas === 8 && ini.vertices === 8 && ini.halo === 1, `8 sectores, 8 vértices y 1 halo (${ini.cunas}/${ini.vertices}/${ini.halo})`);
ok(ini.rol === "group" && ini.tab === "0", "el svg es una parada de tabulador navegable");
ok(ini.nombre !== "—" && ini.iss !== "—", `arranca en ${ini.nombre}, ISS ${ini.iss}`);
const fps = await ev(`new Promise(r => { let c = 0; const t0 = performance.now(); const f = () => { c++; performance.now() - t0 < 500 ? requestAnimationFrame(f) : r(c * 2); }; requestAnimationFrame(f); })`);
console.log(`       (${fps} fotogramas/s en este Chrome)`);

// 2 · cambio de medición: la interpolación pasa por valores intermedios
const pt = `document.querySelector('#lamina-octogono polygon.perfil').getAttribute('points')`;
const antes = await ev(pt);
await ev(`document.getElementById('lm-sig').click()`);
const muestras = [];
for (let t = 0; t < 1100; t += 110) { muestras.push({ pts: await ev(pt), iss: await ev(`document.getElementById('lm-iss').textContent`), onda: await ev(`document.querySelectorAll('#lamina-octogono .onda').length`) }); await dormir(110); }
const final = await ev(pt);
const distintos = new Set(muestras.map((m) => m.pts)).size;
ok(final !== antes, "el perfil cambia de forma");
ok(distintos >= 4, `pasa por ${distintos} formas intermedias en ~1 s`);
ok(muestras.slice(0, 3).some((m) => m.onda > 0), "la onda aparece al cambiar");
await dormir(500);
ok((await ev(`document.querySelectorAll('#lamina-octogono .onda').length`)) === 0, "y se retira al terminar");
// el contador del ISS, con un salto amplio (a la medición de ISS más alto)
await ev(`[...document.querySelectorAll('#lamina-octogono .perfil-fondo')].pop().dispatchEvent(new MouseEvent('click', { bubbles: true }))`);
const cuenta = [];
for (let t = 0; t < 1000; t += 100) { cuenta.push(await ev(`document.getElementById('lm-iss').textContent`)); await dormir(100); }
ok(new Set(cuenta).size >= 4, `el ISS cuenta hasta el valor nuevo (${[...new Set(cuenta)].join(" → ")})`);
const sync = await ev(`({ h: location.hash, f: document.querySelector('#mandos-ficha select').value, n: document.getElementById('lm-nombre').textContent })`);
ok(sync.h === "#m=" + encodeURIComponent(sync.n) && sync.f === sync.n, `hash y ficha siguen a la lámina (${sync.h})`);

// 3 · hover real sobre un eje (Obediencia: arriba a la derecha del centro)
const geo = await ev(`(() => { const s = document.querySelector('#lamina-octogono svg'); const r = s.getBoundingClientRect(); const lin = s.querySelectorAll('.radar-radio')[1]; return { x: r.left + (+lin.getAttribute('x1') + +lin.getAttribute('x2') * 2) / 3, y: r.top + (+lin.getAttribute('y1') + +lin.getAttribute('y2') * 2) / 3 }; })()`);
await cdp("Input.dispatchMouseEvent", { type: "mouseMoved", x: geo.x, y: geo.y });
await dormir(400);
const hov = await ev(`({ t: document.getElementById('ll-titulo').textContent, v: document.getElementById('ll-valor').textContent, act: document.querySelectorAll('#lamina-octogono .activo').length })`);
ok(hov.t === "Obediencia" && hov.act === 4, `hover enciende Obediencia (${hov.t}, ${hov.v}, ${hov.act} piezas)`);
await cdp("Input.dispatchMouseEvent", { type: "mouseMoved", x: 5, y: 5 });
await dormir(300);
ok((await ev(`document.getElementById('ll-titulo').textContent`)) === "Pasa por un eje", "al salir, vuelve la lectura general");

// 4 · teclado: foco en el svg y flechas por los ejes
await ev(`document.querySelector('#lamina-octogono svg').focus()`);
for (const k of ["ArrowRight", "ArrowRight", "ArrowRight"]) {
  await cdp("Input.dispatchKeyEvent", { type: "keyDown", key: k, code: k, windowsVirtualKeyCode: 39 });
  await cdp("Input.dispatchKeyEvent", { type: "keyUp", key: k, code: k, windowsVirtualKeyCode: 39 });
  await dormir(120);
}
const tec = await ev(`({ t: document.getElementById('ll-titulo').textContent, vivo: document.getElementById('lamina-lectura').getAttribute('aria-live'), etiqueta: document.activeElement.getAttribute('aria-label') })`);
ok(tec.t === "Abuso espontáneo", `con las flechas llega al tercer eje (${tec.t})`);
ok(tec.vivo === "polite" && /:/.test(tec.etiqueta || ""), `la lectura se anuncia y el sector lleva su valor («${tec.etiqueta}»)`);

// 5 · clic en un perfil fino
const objetivo = await ev(`(() => { const g = document.querySelectorAll('#lamina-octogono .perfil-fondo')[0]; g.dispatchEvent(new MouseEvent('click', { bubbles: true })); return g.querySelector('title').textContent.split(' · ')[0]; })()`);
await dormir(1100);
ok((await ev(`document.getElementById('lm-nombre').textContent`)) === objetivo, `pulsar un perfil fino lleva a ${objetivo}`);

// 6 · con #m= en la dirección, arranca en esa medición
await cdp("Page.navigate", { url: URL_ + "#m=gemini-3.7-flash" }); await dormir(2600);
ok((await ev(`document.getElementById('lm-nombre').textContent`)) === "gemini-3.7-flash", "#m=gemini-3.7-flash arranca en esa medición");

// 7 · movimiento reducido: cambio instantáneo y sin onda
await cdp("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
await cargar();
const a2 = await ev(pt);
await ev(`document.getElementById('lm-ant').click()`);
await dormir(40);
const r2 = await ev(`({ pts: ${pt}, onda: document.querySelectorAll('#lamina-octogono .onda').length })`);
await dormir(400);
ok(r2.pts !== a2 && r2.pts === (await ev(pt)) && r2.onda === 0, "con movimiento reducido el cambio es instantáneo y sin onda");

ok(errores.length === 0, `sin errores de consola${errores.length ? ": " + errores.join(" | ") : ""}`);
console.log(fallos.length ? `\nLÁMINA: ${fallos.length} fallo(s)` : "\nLÁMINA: todo OK");
ws.close(); ch.kill(); await dormir(300); rmSync(perfil, { recursive: true, force: true });
process.exit(fallos.length ? 1 : 0);
