"use strict";
/* ============================================================
   PsicoAI · Visor de replays — autocontenido, sin dependencias.
   Lee un replay.json (contrato: schemas/replay.schema.json) y lo
   reproduce en una sala 2D estilo AI Town con bocadillos y narrador.

   Revisión de seguridad aplicada:
   - Hallazgo 3 (XSS): el DOM se construye con createElement +
     textContent; nada de innerHTML con datos del replay.
   - Hallazgo 7 (contratos): todo replay se valida al cargar contra un
     subconjunto documentado de schemas/replay.schema.json (límites de
     tamaño, tipos de evento en lista blanca, ids referenciados).
   - Hallazgo 23: el canal de pensamientos se llama «monólogo privado
     generado» — ocultarlo es ocultación de interfaz, no privacidad.
   ============================================================ */

/* ---------- Límites de carga (contrato con schemas/replay.schema.json) ---------- */
const LIMITE_TAM_FICHERO_MB = 20;
const LIMITE_TAM_FICHERO = LIMITE_TAM_FICHERO_MB * 1024 * 1024;  // 20 MB
const LIMITE_AGENTES = 200;
const LIMITE_EVENTOS = 50000;
const LIMITE_CHARS_TEXTO = 10000;
/* Lista blanca de tipos de evento. "constraint_violation" se muestra SIEMPRE
   como fila de advertencia visible: ocultarla maquillaría el run. */
const TIPOS_EVENTO = ["narrador", "dialogo", "accion", "pensamiento",
                      "movimiento", "paso", "constraint_violation"];

const W = 960, H = 640, TILE = 32;
const lienzo = document.getElementById("lienzo");
const ctx = lienzo.getContext("2d");

/* ---------- Puntos de anclaje de la sala ---------- */
const SPOTS = {
  tablon:  {x:190, y:200}, ventana: {x:672, y:190},
  mesa_o:  {x:390, y:352}, mesa_e:  {x:576, y:352},
  mesa_s:  {x:480, y:420}, sofa:    {x:770, y:492},
  puerta:  {x:150, y:520}, centro:  {x:480, y:470},
  planta:  {x:836, y:210},
};
const SPOTS_DEFECTO = ["tablon", "mesa_o", "mesa_e", "ventana", "sofa", "puerta"];

/* ---------- Estado global ---------- */
let replay = null;          // JSON cargado
let agentes = [];           // [{id,nombre,rol,color,pos,destino,cara,blink,...}]
let idx = 0;                // evento actual
let reproduciendo = false;
let velocidad = 1;
const VELOCIDADES = [0.5, 1, 1.5, 2, 4];
let mostrarPensamientos = true;
let tRestante = 0;          // ms que quedan al evento actual
let ultimoTs = null;
let pasoActual = 0;
let burbuja = null;         // {agenteId, texto, pensamiento, progreso}
let narrador = null;        // {texto, alpha}

/* ---------- Utilidades ---------- */
const $ = id => document.getElementById(id);
function toast(msg){
  const t = $("toast"); t.textContent = msg; t.style.display = "block";
  clearTimeout(toast._t); toast._t = setTimeout(() => t.style.display = "none", 6000);
}
function oscurecer(hex, f){
  const n = parseInt(hex.slice(1), 16);
  const c = v => Math.max(0, Math.min(255, Math.round(v * f)));
  return `rgb(${c(n>>16)},${c((n>>8)&255)},${c(n&255)})`;
}
function easeOutBack(t){ const c = 1.70158; return 1 + (c+1)*Math.pow(t-1,3) + c*Math.pow(t-1,2); }

/* Variación determinista de sprite por nombre (piel, pelo, estilo) */
function variante(nombre){
  let h = 0;
  for(const c of nombre) h = (h*31 + c.charCodeAt(0)) >>> 0;
  const PIELES = ["#f2c79b","#e8b48a","#dba473","#c98f5f","#a06a44","#f4d3ae"];
  const PELOS  = ["#2e2a28","#4a3423","#6e4a2a","#8a6337","#3a3a44","#77392a","#b5b0a6","#57302f"];
  return {piel:PIELES[h % 6], pelo:PELOS[(h>>3) % 8], estilo:(h>>6) % 5, pantalon:["#4d4a5a","#5a4a3e","#3f4a55","#54405c"][(h>>9) % 4]};
}

/* Retrato en miniatura (cabeza) para la leyenda */
function retrato(a){
  const c = document.createElement("canvas"); c.width = 14; c.height = 14;
  const g = c.getContext("2d");
  g.fillStyle = "#242837"; g.fillRect(0,0,14,14);
  g.fillStyle = a.v.piel; g.fillRect(3,4,8,8);
  g.fillStyle = a.v.pelo; g.fillRect(2,2,10,4);
  if(a.v.estilo===1){ g.fillRect(2,2,2,9); g.fillRect(10,2,2,9); }
  g.fillStyle = "#26262e"; g.fillRect(5,8,1,2); g.fillRect(9,8,1,2);
  g.fillStyle = a.color; g.fillRect(0,12,14,2);
  return c.toDataURL();
}

/* Partículas de polvo en el haz de luz de la ventana */
const PARTICULAS = Array.from({length: 16}, (_, i) => ({
  x: 520 + (i*53 % 230), y: 110 + (i*97 % 260), v: 0.12 + (i%5)*0.05, f: i*0.7,
}));
let TOTAL_PASOS = 1;

/* ---------- Duración de cada evento (ms, a velocidad 1×) ---------- */
function duracion(ev){
  const n = (ev.texto || "").length;
  switch(ev.tipo){
    case "dialogo":     return Math.min(1600 + n * 52, 12000);
    case "pensamiento": return Math.min(1500 + n * 48, 10000);
    case "accion":      return Math.min(2000 + n * 30, 8000);
    case "narrador":    return Math.min(2600 + n * 30, 10000);
    case "constraint_violation": return Math.min(2600 + n * 30, 10000);
    case "movimiento":  return 1300;
    case "paso":        return 700;
    default:            return 1200;
  }
}

/* ------------------------------------------------------------
   Validación del replay (hallazgo 7). Subconjunto documentado de
   schemas/replay.schema.json: requeridos, tipos, límites y
   referencias de agente. Sin librerías externas (CSP sin CDNs).
   Devuelve lista de errores en español; vacía = replay válido.
   ------------------------------------------------------------ */
function validarReplay(data){
  const err = [];
  const anota = m => { if(err.length < 12) err.push(m); };
  if(!data || typeof data !== "object" || Array.isArray(data))
    return ["la raíz del JSON no es un objeto"];
  if(!Array.isArray(data.agentes)) anota("falta la lista «agentes»");
  if(!Array.isArray(data.eventos)) anota("falta la lista «eventos»");
  if(err.length) return err;
  if(data.agentes.length === 0) anota("la lista «agentes» está vacía");
  if(data.agentes.length > LIMITE_AGENTES)
    anota(`demasiados agentes: ${data.agentes.length} (máximo ${LIMITE_AGENTES})`);
  if(data.eventos.length > LIMITE_EVENTOS)
    anota(`demasiados eventos: ${data.eventos.length} (máximo ${LIMITE_EVENTOS})`);
  const ids = new Set();
  data.agentes.forEach((a, i) => {
    if(!a || typeof a !== "object"){ anota(`agente ${i+1}: no es un objeto`); return; }
    if(typeof a.id !== "string" || !a.id) anota(`agente ${i+1}: falta un «id» de texto`);
    else if(ids.has(a.id)) anota(`id de agente duplicado: «${a.id}»`);
    else ids.add(a.id);
    if(typeof a.nombre !== "string" || !a.nombre) anota(`agente ${i+1}: falta el «nombre»`);
    else if(a.nombre.length > 120) anota(`agente ${i+1}: nombre demasiado largo (máx. 120)`);
  });
  data.eventos.forEach((ev, i) => {
    if(!ev || typeof ev !== "object"){ anota(`evento ${i+1}: no es un objeto`); return; }
    if(!TIPOS_EVENTO.includes(ev.tipo)){
      anota(`evento ${i+1}: tipo «${String(ev.tipo).slice(0,40)}» fuera de la lista blanca (${TIPOS_EVENTO.join(", ")})`);
      return;
    }
    if(ev.texto !== undefined){
      if(typeof ev.texto !== "string") anota(`evento ${i+1}: «texto» debe ser texto`);
      else if(ev.texto.length > LIMITE_CHARS_TEXTO)
        anota(`evento ${i+1}: texto de ${ev.texto.length} caracteres (máximo ${LIMITE_CHARS_TEXTO})`);
    }
    if(ev.tipo === "paso" && ev.n !== undefined && (!Number.isInteger(ev.n) || ev.n < 0))
      anota(`evento ${i+1}: «n» del paso debe ser un entero ≥ 0`);
    for(const campo of ["agente", "hacia", "haciaAgente"]){
      if(ev[campo] !== undefined && !ids.has(ev[campo]))
        anota(`evento ${i+1}: «${campo}» apunta al agente inexistente «${String(ev[campo]).slice(0,40)}»`);
    }
  });
  return err;
}

/* ---------- Carga de replays ---------- */
function cargarReplay(data){
  const errores = validarReplay(data);
  if(errores.length){
    toast("Replay rechazado (no cumple schemas/replay.schema.json): " +
      errores.slice(0, 2).join("; ") +
      (errores.length > 2 ? ` … y ${errores.length - 2} problema(s) más (ver consola)` : "") + ".");
    console.warn("Replay rechazado. Problemas encontrados:", errores);
    return;
  }
  replay = data;
  agentes = data.agentes.map((a, i) => {
    const spot = SPOTS[a.spot] || SPOTS[SPOTS_DEFECTO[i % SPOTS_DEFECTO.length]];
    const color = a.color || ["#e4572e","#4d9de0","#3bb273","#b86fc6","#f2a65a","#e26d8f"][i % 6];
    return {
      ...a, color,
      // segunda vuelta de spots desplazada para que los sprites no se apilen
      pos: {x: spot.x + (i%2 ? 16 : -16) + (i >= 6 ? 10 : 0),
            y: spot.y + (i >= 6 ? 28 : 0)},
      destino: null, cara: 1, dir: "down", walk: 0, emote: null,
      v: variante(a.nombre || String(i)),
      blink: Math.random()*4000, andando: false,
    };
  });
  TOTAL_PASOS = Math.max(1, ...data.eventos.filter(e => e.tipo === "paso").map(e => e.n || 1));
  $("tituloSesion").textContent = data.meta?.titulo || "Sesión sin título";
  $("descripcion").textContent = data.meta?.descripcion || "";
  const ley = $("leyenda"); ley.textContent = "";
  agentes.forEach(a => {
    const chip = document.createElement("div"); chip.className = "agenteChip";
    const img = document.createElement("img"); img.src = retrato(a); img.alt = "";
    const nom = document.createElement("span"); nom.textContent = a.nombre;
    chip.append(img, nom);
    if(a.rol){ const r = document.createElement("span"); r.className = "rol";
               r.textContent = "· " + a.rol; chip.append(r); }
    ley.append(chip);
  });
  construirFeed();
  $("barra").max = Math.max(0, data.eventos.length - 1);
  buscar(0);
  reproducir(true);
}

function construirFeed(){
  // Sin innerHTML con datos del replay: todo por textContent (evita XSS
  // almacenado vía nombres/roles/textos de un replay.json no confiable).
  const feed = $("feed"); feed.textContent = "";
  replay.eventos.forEach((ev, i) => {
    // Canal privado apagado: el texto del monólogo NO entra siquiera en el
    // DOM (no basta con ocultarlo: sería recuperable al inspeccionar).
    // Se reconstruye el feed al reactivar el canal.
    if(ev.tipo === "pensamiento" && !mostrarPensamientos) return;
    if(ev.tipo === "paso"){
      const d = document.createElement("div");
      d.className = "divisorPaso"; d.dataset.i = i;
      d.textContent = `— paso ${ev.n} —`;
      feed.appendChild(d); return;
    }
    const d = document.createElement("div");
    d.className = "ev " + ev.tipo; d.dataset.i = i;
    if(ev.tipo === "pensamiento") d.classList.add("privado");
    const quien = document.createElement("span"); quien.className = "quien";
    const texto = document.createElement("span");
    texto.className = "texto"; texto.textContent = ev.texto || "";
    if(ev.tipo === "constraint_violation"){
      // Violación de restricción del motor: fila de ADVERTENCIA visible,
      // nunca oculta — forma parte del registro del experimento.
      d.classList.add("advertencia");
      quien.textContent = "⚠ ADVERTENCIA";
      if(!ev.texto) texto.textContent = "Violación de restricción del motor (sin detalle).";
    } else if(ev.tipo === "narrador"){
      quien.textContent = "📜";
    } else {
      const ag = agentes.find(a => a.id === ev.agente);
      if(ag){ quien.textContent = ag.nombre.split(" ")[0];
              quien.style.color = ag.color; }
    }
    d.append(quien, texto);
    d.onclick = () => { buscar(i); reproducir(false); };
    feed.appendChild(d);
  });
}

/* ---------- Motor de reproducción ---------- */
function aplicarEvento(ev, instantaneo){
  if(ev.tipo === "paso"){ pasoActual = ev.n; return; }
  if(ev.tipo === "movimiento"){
    const ag = agentes.find(a => a.id === ev.agente);
    let dest = null;
    if(ev.spot && SPOTS[ev.spot]) dest = {x:SPOTS[ev.spot].x, y:SPOTS[ev.spot].y};
    else if(ev.haciaAgente){
      const otro = agentes.find(a => a.id === ev.haciaAgente);
      if(otro && ag) dest = {x: otro.pos.x + (ag.pos.x >= otro.pos.x ? 36 : -36), y: otro.pos.y};
    }
    if(ag && dest){
      if(instantaneo){ ag.pos = {...dest}; ag.destino = null; }
      else ag.destino = dest;
    }
    return;
  }
  if(instantaneo) return; // burbujas y narrador solo en reproducción real
  if(ev.tipo === "narrador"){ narrador = {texto: ev.texto, alpha: 0}; burbuja = null; return; }
  if(ev.tipo === "constraint_violation"){
    // En el lienzo se muestra como banda de advertencia del narrador.
    narrador = {texto: "⚠ ADVERTENCIA: " + (ev.texto || "violación de restricción del motor."), alpha: 0};
    burbuja = null; return;
  }
  if(ev.tipo === "dialogo" || ev.tipo === "pensamiento" || ev.tipo === "accion"){
    const ag = agentes.find(a => a.id === ev.agente);
    if(!ag){ narrador = {texto: ev.texto, alpha: 0}; return; }
    if(ev.hacia){
      const dest = agentes.find(a => a.id === ev.hacia);
      if(dest){
        ag.dir = Math.abs(dest.pos.x - ag.pos.x) >= Math.abs(dest.pos.y - ag.pos.y)
          ? (dest.pos.x >= ag.pos.x ? "right" : "left")
          : (dest.pos.y >= ag.pos.y ? "down" : "up");
        dest.dir = Math.abs(ag.pos.x - dest.pos.x) >= Math.abs(ag.pos.y - dest.pos.y)
          ? (ag.pos.x >= dest.pos.x ? "right" : "left")
          : (ag.pos.y >= dest.pos.y ? "down" : "up");
      }
    }
    if(ev.tipo === "accion") ag.emote = {t: 0, char: "✦"};
    burbuja = {
      agenteId: ag.id, texto: ev.texto || "",
      pensamiento: ev.tipo === "pensamiento",
      accion: ev.tipo === "accion", progreso: 0, pop: 0,
    };
    narrador = null;
  }
}

function eventoVisible(ev){
  return mostrarPensamientos || ev.tipo !== "pensamiento";
}

function avanzar(){
  let siguiente = idx + 1;
  while(siguiente < replay.eventos.length && !eventoVisible(replay.eventos[siguiente])) siguiente++;
  if(siguiente >= replay.eventos.length){ reproducir(false); return; }
  idx = siguiente;
  entrarEvento();
}

function entrarEvento(){
  const ev = replay.eventos[idx];
  // Con el canal privado apagado, un pensamiento alcanzado por timeline/seek
  // no debe renderizar su burbuja ni su texto: se trata como no-visible.
  if(ev.tipo === "pensamiento" && !mostrarPensamientos){
    actualizarUI(); return;
  }
  tRestante = duracion(ev);
  aplicarEvento(ev, false);
  actualizarUI();
}

function buscar(i){
  i = Math.max(0, Math.min(i, replay.eventos.length - 1));
  // Reconstruye el estado del mundo desde cero hasta i (posiciones y paso).
  agentes.forEach((a, j) => {
    const spot = SPOTS[a.spot] || SPOTS[SPOTS_DEFECTO[j % SPOTS_DEFECTO.length]];
    a.pos = {x: spot.x + (j%2 ? 16 : -16) + (j >= 6 ? 10 : 0),
             y: spot.y + (j >= 6 ? 28 : 0)};
    a.destino = null; a.dir = "down"; a.walk = 0; a.emote = null;
  });
  pasoActual = 0; burbuja = null; narrador = null;
  for(let k = 0; k < i; k++) aplicarEvento(replay.eventos[k], true);
  idx = i;
  entrarEvento();
}

function reproducir(si){
  reproduciendo = si;
  $("btnPlay").textContent = si ? "⏸" : "▶";
  ultimoTs = null;
}

function actualizarUI(){
  $("barra").value = idx;
  $("contador").textContent = `evento ${idx + 1}/${replay.eventos.length} · paso ${pasoActual}`;
  document.querySelectorAll("#feed .ev.activo").forEach(e => e.classList.remove("activo"));
  const el = document.querySelector(`#feed [data-i="${idx}"]`);
  if(el && el.classList.contains("ev")){
    el.classList.add("activo");
    el.scrollIntoView({block:"nearest", behavior:"smooth"});
  }
}

/* ---------- Bucle de animación ---------- */
function tick(ts){
  requestAnimationFrame(tick);
  if(ultimoTs === null) ultimoTs = ts;
  const dt = Math.min(ts - ultimoTs, 100);
  ultimoTs = ts;

  // Movimiento de agentes hacia su destino
  for(const a of agentes){
    a.blink -= dt;
    if(a.blink < -150) a.blink = 2500 + Math.random()*3500;
    if(a.emote){ a.emote.t += dt; if(a.emote.t > 900) a.emote = null; }
    if(a.destino){
      const dx = a.destino.x - a.pos.x, dy = a.destino.y - a.pos.y;
      const dist = Math.hypot(dx, dy);
      const pasoPx = 0.11 * dt * velocidad;
      if(dist < pasoPx){ a.pos = {...a.destino}; a.destino = null; a.andando = false; }
      else {
        a.dir = Math.abs(dx) >= Math.abs(dy) ? (dx >= 0 ? "right" : "left")
                                             : (dy >= 0 ? "down" : "up");
        a.andando = true; a.walk += dt * velocidad;
        a.pos.x += dx / dist * pasoPx; a.pos.y += dy / dist * pasoPx;
      }
    } else a.andando = false;
  }

  if(burbuja) burbuja.pop = Math.min(1, (burbuja.pop || 0) + dt / 200);
  if(replay && reproduciendo){
    if(burbuja) burbuja.progreso = Math.min(1, burbuja.progreso + dt * velocidad / (duracion(replay.eventos[idx]) * 0.6));
    if(narrador) narrador.alpha = Math.min(1, narrador.alpha + dt / 300);
    tRestante -= dt * velocidad;
    if(tRestante <= 0) avanzar();
  } else if(burbuja) burbuja.progreso = 1;

  dibujar(ts);
}

/* ============================================================
   DIBUJO DE LA SALA (estilo pixel, todo procedural)
   ============================================================ */
function dibujar(ts){
  ctx.clearRect(0, 0, W, H);

  // ── Suelo: tarima de madera ──
  for(let ty = 96, fila = 0; ty < H; ty += 22, fila++){
    ctx.fillStyle = fila % 2 ? "#d8c093" : "#cfb789";
    ctx.fillRect(0, ty, W, 22);
    ctx.fillStyle = "rgba(120,90,55,.22)";
    ctx.fillRect(0, ty + 20, W, 2);
    const off = (fila % 3) * 110;
    for(let sx = off; sx < W; sx += 320){
      ctx.fillRect(sx, ty, 2, 20);
      ctx.fillStyle = "rgba(120,90,55,.10)";
      ctx.fillRect(sx + 40, ty + 6, 14, 2);
      ctx.fillStyle = "rgba(120,90,55,.22)";
    }
  }

  // ── Alfombra grande bajo la mesa ──
  const rx = 336, ry = 280, rw = 290, rh = 200;
  ctx.fillStyle = "#a8503c"; ctx.fillRect(rx, ry, rw, rh);
  ctx.fillStyle = "#b95f45"; ctx.fillRect(rx+8, ry+8, rw-16, rh-16);
  ctx.fillStyle = "#cd7454"; ctx.fillRect(rx+20, ry+20, rw-40, rh-40);
  ctx.fillStyle = "rgba(255,235,200,.25)";
  for(let i = 0; i < 5; i++){ ctx.fillRect(rx+34+i*48, ry+34, 20, 3); ctx.fillRect(rx+34+i*48, ry+rh-37, 20, 3); }
  ctx.fillStyle = "rgba(90,40,25,.30)";
  ctx.fillRect(rx+8, ry+8, rw-16, 3); ctx.fillRect(rx+8, ry+rh-11, rw-16, 3);

  // ── Pared superior ──
  const grad = ctx.createLinearGradient(0, 0, 0, 96);
  grad.addColorStop(0, "#93816c"); grad.addColorStop(1, "#84735f");
  ctx.fillStyle = grad; ctx.fillRect(0, 0, W, 96);
  ctx.fillStyle = "rgba(255,245,220,.06)";
  for(let sx = 0; sx < W; sx += 64) ctx.fillRect(sx, 0, 1, 88);
  ctx.fillStyle = "#6b5b49"; ctx.fillRect(0, 86, W, 10);   // zócalo
  ctx.fillStyle = "#7d6c58"; ctx.fillRect(0, 84, W, 2);

  // Tablón de anuncios (con papeles y chinchetas)
  ctx.fillStyle = "rgba(0,0,0,.25)"; ctx.fillRect(136, 20, 118, 70);
  ctx.fillStyle = "#5a4c3c"; ctx.fillRect(132, 16, 118, 70);
  ctx.fillStyle = "#c8a66c"; ctx.fillRect(138, 22, 106, 58);
  ctx.fillStyle = "#f7f2e4"; ctx.fillRect(146, 30, 32, 40);
  ctx.fillStyle = "#efe7d2"; ctx.fillRect(186, 34, 28, 24); ctx.fillRect(220, 30, 18, 34);
  ctx.fillStyle = "#c25038"; ctx.fillRect(146, 30, 32, 7);
  ctx.fillStyle = "rgba(60,40,20,.5)";
  ctx.fillRect(150, 40, 24, 2); ctx.fillRect(150, 46, 24, 2); ctx.fillRect(150, 52, 18, 2);
  ctx.fillStyle = "#d8433f"; ctx.fillRect(160, 28, 3, 3); ctx.fillRect(198, 32, 3, 3); ctx.fillRect(227, 28, 3, 3);

  // Cuadros
  ctx.fillStyle = "#5a4c3c"; ctx.fillRect(330, 26, 44, 34); ctx.fillRect(394, 32, 30, 24);
  ctx.fillStyle = "#8fae94"; ctx.fillRect(334, 30, 36, 26);
  ctx.fillStyle = "#b7c9e0"; ctx.fillRect(398, 36, 22, 16);
  ctx.fillStyle = "rgba(255,255,255,.25)"; ctx.fillRect(336, 32, 10, 6);

  // Reloj (la aguja avanza con el paso)
  ctx.fillStyle = "rgba(0,0,0,.2)"; ctx.beginPath(); ctx.arc(492, 50, 21, 0, 7); ctx.fill();
  ctx.fillStyle = "#5a4c3c"; ctx.beginPath(); ctx.arc(490, 48, 21, 0, 7); ctx.fill();
  ctx.fillStyle = "#f6f0df"; ctx.beginPath(); ctx.arc(490, 48, 17, 0, 7); ctx.fill();
  const angulo = -Math.PI/2 + (pasoActual / TOTAL_PASOS) * Math.PI * 1.6;
  ctx.strokeStyle = "#3a352e"; ctx.lineWidth = 2; ctx.beginPath();
  ctx.moveTo(490, 48); ctx.lineTo(490 + Math.cos(angulo)*12, 48 + Math.sin(angulo)*12);
  ctx.moveTo(490, 48); ctx.lineTo(490 + Math.cos(angulo*1.7)*7, 48 + Math.sin(angulo*1.7)*7);
  ctx.stroke(); ctx.lineWidth = 1;

  // Ventana (4 hojas + cielo)
  ctx.fillStyle = "rgba(0,0,0,.25)"; ctx.fillRect(596, 16, 168, 74);
  ctx.fillStyle = "#5a4c3c"; ctx.fillRect(592, 12, 168, 74);
  const cielo = ctx.createLinearGradient(0, 16, 0, 82);
  cielo.addColorStop(0, "#bfe0ec"); cielo.addColorStop(1, "#9cc7da");
  ctx.fillStyle = cielo;
  ctx.fillRect(598, 18, 75, 29); ctx.fillRect(679, 18, 75, 29);
  ctx.fillRect(598, 53, 75, 27); ctx.fillRect(679, 53, 75, 27);
  ctx.fillStyle = "rgba(255,255,255,.5)"; ctx.fillRect(604, 22, 26, 10); ctx.fillRect(700, 40, 34, 6);
  ctx.fillStyle = "#efe7d2"; ctx.fillRect(592, 86, 168, 6);   // repisa

  // ── Haz de luz de la ventana + polvo ──
  const luz = ctx.createLinearGradient(670, 96, 590, 400);
  luz.addColorStop(0, "rgba(255,244,200,.14)"); luz.addColorStop(1, "rgba(255,244,200,0)");
  ctx.fillStyle = luz;
  ctx.beginPath(); ctx.moveTo(600, 96); ctx.lineTo(756, 96); ctx.lineTo(680, 410); ctx.lineTo(470, 410); ctx.closePath(); ctx.fill();
  ctx.fillStyle = "rgba(255,250,225,.55)";
  for(const p of PARTICULAS){
    const py = 110 + ((p.y - 110 + ts * p.v * 0.03) % 270);
    const px = p.x + Math.sin(ts/1400 + p.f) * 9;
    ctx.globalAlpha = 0.25 + 0.3 * Math.sin(ts/900 + p.f);
    ctx.fillRect(px, py, 2, 2);
  }
  ctx.globalAlpha = 1;

  // ── Muebles ──
  // Mesa con vetas, tazas y papeles + sillas
  ctx.fillStyle = "#6e5436";
  [[396,336],[550,336],[468,294]].forEach(([x,y]) => { ctx.fillRect(x, y, 18, 18); ctx.fillStyle="#7d6140"; ctx.fillRect(x+2, y+2, 14, 5); ctx.fillStyle="#6e5436"; });
  ctx.fillStyle = "rgba(0,0,0,.22)"; ctx.fillRect(422, 332, 126, 60);
  ctx.fillStyle = "#8a6a44"; ctx.fillRect(416, 322, 128, 64);
  ctx.fillStyle = "#a07c4e"; ctx.fillRect(421, 327, 118, 54);
  ctx.fillStyle = "rgba(120,85,45,.45)";
  ctx.fillRect(428, 338, 104, 2); ctx.fillRect(428, 352, 104, 2); ctx.fillRect(428, 366, 104, 2);
  ctx.fillStyle = "#f2ece0"; ctx.fillRect(448, 342, 16, 12);          // papel
  ctx.fillStyle = "#e8e0d0"; ctx.fillRect(452, 346, 16, 12);
  ctx.fillStyle = "#7a4a3a"; ctx.beginPath(); ctx.arc(510, 350, 6, 0, 7); ctx.fill();  // taza
  ctx.fillStyle = "#5f382c"; ctx.beginPath(); ctx.arc(510, 350, 4, 0, 7); ctx.fill();

  // Sofá con cojines y manta
  ctx.fillStyle = "rgba(0,0,0,.22)"; ctx.fillRect(722, 432, 138, 56);
  ctx.fillStyle = "#96552f"; ctx.fillRect(716, 414, 142, 16);          // respaldo
  ctx.fillStyle = "#b0713f"; ctx.fillRect(716, 428, 142, 52);
  ctx.fillStyle = "#d9a05b"; ctx.fillRect(724, 434, 58, 40); ctx.fillRect(790, 434, 58, 40);
  ctx.fillStyle = "rgba(255,235,200,.35)"; ctx.fillRect(724, 434, 58, 6); ctx.fillRect(790, 434, 58, 6);
  ctx.fillStyle = "#8fae94"; ctx.fillRect(716, 452, 30, 28);           // manta
  ctx.fillStyle = "rgba(60,90,70,.5)"; ctx.fillRect(716, 460, 30, 3); ctx.fillRect(716, 470, 30, 3);
  ctx.fillStyle = "#96552f"; ctx.fillRect(710, 428, 8, 52); ctx.fillRect(856, 428, 8, 52);  // reposabrazos

  // Lámpara de pie junto al sofá (halo cálido)
  const halo = ctx.createRadialGradient(700, 420, 4, 700, 420, 60);
  halo.addColorStop(0, "rgba(255,214,140,.30)"); halo.addColorStop(1, "rgba(255,214,140,0)");
  ctx.fillStyle = halo; ctx.beginPath(); ctx.arc(700, 420, 60, 0, 7); ctx.fill();
  ctx.fillStyle = "#4c4038"; ctx.fillRect(697, 408, 5, 60); ctx.fillRect(688, 466, 24, 5);
  ctx.fillStyle = "#e8c07a"; ctx.beginPath(); ctx.moveTo(686, 408); ctx.lineTo(713, 408); ctx.lineTo(707, 388); ctx.lineTo(692, 388); ctx.closePath(); ctx.fill();

  // Puerta / felpudo (sur-oeste)
  ctx.fillStyle = "#6b4a2c"; ctx.fillRect(92, 552, 104, 56);
  ctx.fillStyle = "#8a5f37"; ctx.fillRect(98, 558, 92, 44);
  ctx.fillStyle = "rgba(60,35,15,.4)";
  ctx.fillRect(104, 564, 80, 2); ctx.fillRect(104, 572, 80, 2); ctx.fillRect(104, 580, 80, 2); ctx.fillRect(104, 588, 80, 2);

  // Plantas (maceta con brillo + follaje en capas)
  for(const [px, py] of [[876, 116], [56, 116], [876, 556]]){
    ctx.fillStyle = "rgba(0,0,0,.2)"; ctx.beginPath(); ctx.ellipse(px+14, py+42, 14, 4, 0, 0, 7); ctx.fill();
    ctx.fillStyle = "#96552f"; ctx.fillRect(px+2, py+24, 24, 18);
    ctx.fillStyle = "#b0713f"; ctx.fillRect(px+2, py+24, 24, 5);
    ctx.fillStyle = "#3f6a34"; ctx.beginPath(); ctx.arc(px+14, py+12, 17, 0, 7); ctx.fill();
    ctx.fillStyle = "#548a44"; ctx.beginPath(); ctx.arc(px+8, py+8, 11, 0, 7); ctx.fill();
    ctx.fillStyle = "#6aa456"; ctx.beginPath(); ctx.arc(px+19, py+5, 7, 0, 7); ctx.fill();
  }

  // ── Personajes (ordenados por Y) ──
  [...agentes].sort((a, b) => a.pos.y - b.pos.y).forEach(a => dibujarAgente(a, ts));

  // Emotes flotantes (chispas de acción)
  for(const a of agentes){
    if(!a.emote) continue;
    const t = a.emote.t / 900;
    ctx.globalAlpha = 1 - t;
    ctx.font = "14px sans-serif"; ctx.textAlign = "center";
    ctx.fillStyle = "#ffd77a";
    ctx.fillText(a.emote.char, a.pos.x + 16, a.pos.y - 44 - t * 14);
    ctx.globalAlpha = 1;
  }

  // Bocadillo del evento actual
  if(burbuja){
    const ag = agentes.find(x => x.id === burbuja.agenteId);
    if(ag) dibujarBurbuja(ag, ts);
  }

  // Banda del narrador
  if(narrador) dibujarNarrador(ts);

  // ── Luz según la hora del día (mañana → tarde) ──
  const t = Math.min(1, pasoActual / TOTAL_PASOS);
  const manana = 0.06 * Math.max(0, 1 - t * 2);
  const tarde = 0.11 * Math.max(0, (t - 0.5) * 2);
  if(manana > 0){ ctx.fillStyle = `rgba(200,225,255,${manana})`; ctx.fillRect(0, 0, W, H); }
  if(tarde > 0){ ctx.fillStyle = `rgba(255,150,70,${tarde})`; ctx.fillRect(0, 0, W, H); }

  // Viñeta
  const vin = ctx.createRadialGradient(W/2, H/2, H/3, W/2, H/2, H*0.85);
  vin.addColorStop(0, "rgba(0,0,0,0)"); vin.addColorStop(1, "rgba(15,10,5,.30)");
  ctx.fillStyle = vin; ctx.fillRect(0, 0, W, H);

  // Indicador de paso
  if(replay){
    ctx.fillStyle = "rgba(14,16,21,.78)";
    ctx.beginPath(); ctx.roundRect(12, H - 42, 122, 30, 8); ctx.fill();
    ctx.fillStyle = "#f2a65a"; ctx.font = "bold 13px ui-monospace,monospace";
    ctx.textAlign = "left";
    ctx.fillText(`PASO ${pasoActual}`, 26, H - 22);
  }
}

function dibujarAgente(a, ts){
  const {x, y} = a.pos;
  const S = 2;                              // px físicos por "píxel" lógico
  const frame = a.andando ? Math.floor(a.walk / 130) % 2 : 0;
  const bob = a.andando ? (frame ? -1 : 0) : Math.round(Math.sin(ts/750 + x) * 0.9);
  const hablando = burbuja && burbuja.agenteId === a.id && !burbuja.pensamiento;
  const salto = hablando ? Math.round(Math.abs(Math.sin(ts / 240)) * 2) : 0;
  const dir = a.dir || "down";
  const v = a.v;
  const sombra = oscurecer(a.color, 0.72);

  // sombra en el suelo
  ctx.fillStyle = "rgba(30,15,5,.28)";
  ctx.beginPath(); ctx.ellipse(x, y + 22, 13, 5, 0, 0, 7); ctx.fill();

  ctx.save();
  ctx.translate(Math.round(x), Math.round(y + bob - salto));
  if(dir === "left") ctx.scale(-1, 1);
  const P = (px, py, w, h, c) => { ctx.fillStyle = c; ctx.fillRect(px*S, py*S, w*S, h*S); };

  // piernas y zapatos (el ciclo de andar alterna)
  const l1 = a.andando ? (frame ? -1 : 0) : 0;   // pierna izquierda levantada
  const l2 = a.andando ? (frame ? 0 : -1) : 0;
  P(-4, 6 + l1, 3, 4, v.pantalon); P(1, 6 + l2, 3, 4, v.pantalon);
  P(-4, 9 + l1, 3, 2, "#33291f");  P(1, 9 + l2, 3, 2, "#33291f");

  // torso (camisa del color del agente, con sombreado lateral)
  P(-5, -4, 10, 10, a.color);
  P(3, -4, 2, 10, sombra);
  P(-5, 4, 10, 2, sombra);                        // cinturón
  if(dir === "up") P(-5, -4, 10, 10, sombra);     // de espaldas, más oscuro

  // brazos (balanceo al andar)
  const b1 = a.andando ? (frame ? 1 : -1) : 0;
  P(-7, -3 + b1, 2, 6, sombra); P(5, -3 - b1, 2, 6, sombra);
  P(-7, 3 + b1, 2, 2, v.piel);  P(5, 3 - b1, 2, 2, v.piel);

  // cabeza
  P(-4, -12, 8, 8, v.piel);
  P(2, -12, 2, 8, oscurecer(v.piel, 0.88));

  // pelo según estilo y dirección
  const pelo = v.pelo;
  if(dir === "up"){
    P(-4, -13, 8, 8, pelo);                       // nuca
  } else {
    if(v.estilo === 0){ P(-4, -13, 8, 3, pelo); }                              // corto
    else if(v.estilo === 1){ P(-4, -13, 8, 3, pelo); P(-5, -12, 1, 6, pelo); P(4, -12, 1, 6, pelo); }  // media melena
    else if(v.estilo === 2){ P(-4, -13, 8, 3, pelo); P(-1, -15, 3, 2, pelo); }  // moño
    else if(v.estilo === 3){ P(-4, -13, 8, 2, pelo); P(-4, -5, 8, 2, pelo); }   // calvicie + barba
    else { P(-4, -13, 8, 2, pelo); P(-4, -13, 3, 5, pelo); }                    // flequillo lateral
  }

  // cara (no visible de espaldas)
  if(dir !== "up" && a.blink > 0){
    ctx.fillStyle = "#241f1d";
    if(dir === "down"){ ctx.fillRect(-3*S, -9*S, S, S+1); ctx.fillRect(1*S, -9*S, S, S+1); }
    else { ctx.fillRect(0, -9*S, S, S+1); ctx.fillRect(3*S, -9*S, S, S+1); }    // perfil
  }
  ctx.restore();

  // etiqueta de nombre (píldora)
  const nombre = a.nombre.split(" ")[0];
  ctx.font = "bold 10.5px -apple-system,sans-serif"; ctx.textAlign = "center";
  const w = ctx.measureText(nombre).width + 14;
  ctx.fillStyle = "rgba(12,12,18,.68)";
  ctx.beginPath(); ctx.roundRect(x - w/2, y - 41, w, 14, 7); ctx.fill();
  ctx.fillStyle = a.color; ctx.fillRect(x - w/2 + 5, y - 36, 4, 4);
  ctx.fillStyle = "#f2efe8"; ctx.fillText(nombre, x + 3, y - 30.5);
}

function ajustarLineas(texto, maxAncho, fuente){
  ctx.font = fuente;
  const palabras = texto.split(/\s+/); const lineas = []; let linea = "";
  for(const p of palabras){
    const prueba = linea ? linea + " " + p : p;
    if(ctx.measureText(prueba).width > maxAncho && linea){ lineas.push(linea); linea = p; }
    else linea = prueba;
  }
  if(linea) lineas.push(linea);
  return lineas;
}

function dibujarBurbuja(ag, ts){
  const fuente = "13px -apple-system,sans-serif";
  const visible = Math.max(1, Math.floor(burbuja.texto.length * Math.min(1, burbuja.progreso * 1.15)));
  const texto = burbuja.texto.slice(0, visible);
  const prefijo = burbuja.accion ? "✳︎ " : "";
  const lineas = ajustarLineas(prefijo + texto, 220, fuente);
  const anchoMax = Math.min(236, Math.max(...lineas.map(l => ctx.measureText(l).width)) + 22);
  const alto = lineas.length * 17 + 16;

  let bx = ag.pos.x - anchoMax / 2;
  bx = Math.max(10, Math.min(bx, W - anchoMax - 10));
  let by = ag.pos.y - 48 - alto;
  const debajo = by < 100 && narrador === null ? false : by < 12;
  if(by < 12) by = ag.pos.y + 34;
  if(burbuja.pensamiento) by += Math.sin((ts || 0) / 850) * 3;   // flotación suave

  ctx.save();
  // pop-in: escala con rebote alrededor del ancla
  const pop = easeOutBack(Math.min(1, burbuja.pop ?? 1));
  ctx.translate(ag.pos.x, by + alto);
  ctx.scale(Math.max(0.01, pop), Math.max(0.01, pop));
  ctx.translate(-ag.pos.x, -(by + alto));
  ctx.shadowColor = "rgba(20,10,0,.35)"; ctx.shadowBlur = 12; ctx.shadowOffsetY = 4;
  if(burbuja.pensamiento){
    ctx.fillStyle = "rgba(233,228,248,.94)";
    ctx.strokeStyle = "#9a8fc9"; ctx.setLineDash([5, 4]);
  } else if(burbuja.accion){
    ctx.fillStyle = "rgba(250,242,225,.94)";
    ctx.strokeStyle = "#c9a05a";
  } else {
    ctx.fillStyle = "rgba(255,255,255,.96)";
    ctx.strokeStyle = "#8b8b96";
  }
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.roundRect(bx, by, anchoMax, alto, 10);
  ctx.fill();
  ctx.shadowColor = "transparent";
  ctx.stroke();
  ctx.setLineDash([]);

  // cola del bocadillo
  if(!debajo){
    if(burbuja.pensamiento){
      ctx.beginPath(); ctx.arc(ag.pos.x, by + alto + 8, 4, 0, 7); ctx.fill();
      ctx.beginPath(); ctx.arc(ag.pos.x - 4, by + alto + 16, 2.5, 0, 7); ctx.fill();
    } else {
      ctx.beginPath();
      ctx.moveTo(ag.pos.x - 6, by + alto);
      ctx.lineTo(ag.pos.x + 6, by + alto);
      ctx.lineTo(ag.pos.x, by + alto + 10);
      ctx.closePath(); ctx.fill();
    }
  }

  ctx.fillStyle = burbuja.pensamiento ? "#4a4066" : "#26262e";
  ctx.font = fuente; ctx.textAlign = "left";
  lineas.forEach((l, i) => ctx.fillText(l, bx + 11, by + 20 + i * 17));
  ctx.restore();
}

function dibujarNarrador(ts){
  const fuente = "italic 15px Georgia,serif";
  const lineas = ajustarLineas(narrador.texto, W - 220, fuente);
  const alto = lineas.length * 20 + 26;
  ctx.save();
  ctx.globalAlpha = narrador.alpha;
  // barras de cine arriba y abajo
  const g = ctx.createLinearGradient(0, 0, 0, alto + 14);
  g.addColorStop(0, "rgba(8,9,13,.94)"); g.addColorStop(1, "rgba(8,9,13,.78)");
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, alto + 14);
  ctx.fillStyle = "rgba(8,9,13,.6)"; ctx.fillRect(0, H - 22, W, 22);
  ctx.fillStyle = "#f2a65a"; ctx.fillRect(W/2 - 26, alto + 6, 52, 2);
  ctx.fillStyle = "#ece1c8"; ctx.font = fuente; ctx.textAlign = "center";
  lineas.forEach((l, i) => ctx.fillText(l, W / 2, 30 + i * 20));
  ctx.restore();
}

/* ============================================================
   CONTROLES
   ============================================================ */
$("btnPlay").onclick = () => reproducir(!reproduciendo);
$("btnInicio").onclick = () => { buscar(0); };
$("btnAtras").onclick = () => { buscar(idx - 1); reproducir(false); };
$("btnAdelante").onclick = () => { buscar(idx + 1); reproducir(false); };
$("btnVelocidad").onclick = () => {
  velocidad = VELOCIDADES[(VELOCIDADES.indexOf(velocidad) + 1) % VELOCIDADES.length];
  $("btnVelocidad").textContent = velocidad + "×";
};
$("btnPensamientos").onclick = () => {
  mostrarPensamientos = !mostrarPensamientos;
  $("btnPensamientos").classList.toggle("activo", mostrarPensamientos);
  // Reconstruir el feed: así el texto del monólogo entra o sale del DOM de verdad.
  if(replay){ construirFeed(); actualizarUI(); }
  if(!mostrarPensamientos){
    if(burbuja?.pensamiento) burbuja = null;
    if(replay?.eventos[idx]?.tipo === "pensamiento") avanzar();
  }
};
$("btnPensamientos").classList.add("activo");
$("barra").oninput = e => { buscar(+e.target.value); reproducir(false); };
document.addEventListener("keydown", e => {
  if(e.target.tagName === "INPUT" && e.target.type !== "range") return;
  if(e.code === "Space"){ e.preventDefault(); reproducir(!reproduciendo); }
  if(e.code === "ArrowRight"){ buscar(idx + 1); reproducir(false); }
  if(e.code === "ArrowLeft"){ buscar(idx - 1); reproducir(false); }
});

/* Carga de ficheros */
$("btnCargar").onclick = () => $("ficheroInput").click();
$("ficheroInput").onchange = e => leerFichero(e.target.files[0]);
window.addEventListener("dragover", e => { e.preventDefault(); document.body.classList.add("arrastrando"); });
window.addEventListener("dragleave", e => { if(!e.relatedTarget) document.body.classList.remove("arrastrando"); });
window.addEventListener("drop", e => {
  e.preventDefault(); document.body.classList.remove("arrastrando");
  if(e.dataTransfer.files[0]) leerFichero(e.dataTransfer.files[0]);
});
function leerFichero(f){
  if(!f) return;
  if(f.size > LIMITE_TAM_FICHERO){
    toast(`Fichero rechazado: ocupa ${(f.size/1048576).toFixed(1)} MB y el máximo admitido es ${LIMITE_TAM_FICHERO_MB} MB.`);
    return;
  }
  f.text().then(t => {
    try { cargarReplay(JSON.parse(t)); }
    catch { toast("No he podido leer ese fichero como JSON."); }
  });
}

/* ============================================================
   DEMO EMBEBIDA — "El Centro Aldaba, día 1"
   Ilustra lo que produce una sesión real de Concordia una vez
   exportada con export_replay.py. Guion de muestra, en español.
   ============================================================ */
const DEMO_REPLAY = {
  version: 1,
  meta: {
    titulo: "El Centro Aldaba — Día 1: la norma nueva (demo)",
    descripcion: "Sesión de demostración del visor. Una residencia de evaluación anuncia una norma que restringe las llamadas al exterior. Fíjate en la diferencia entre lo que Lucía piensa (💭) y lo que dice en voz alta: esa distancia es la presión de grupo, el fenómeno que PsicoAI estudia. Puedes ocultar el monólogo privado generado con el botón 💭 y ver la escena como la vería un observador externo (el texto sigue existiendo en el fichero).",
    fecha: "2026-07-13", fuente: "demo",
  },
  agentes: [
    {id: "marta",  nombre: "Marta Ibáñez", rol: "Directora",           color: "#e4572e", spot: "tablon"},
    {id: "julio",  nombre: "Julio Serrano", rol: "Supervisor",         color: "#4d9de0", spot: "puerta"},
    {id: "andres", nombre: "Andrés Vidal", rol: "Residente veterano",  color: "#3bb273", spot: "mesa_e"},
    {id: "lucia",  nombre: "Lucía Prado",  rol: "Residente nueva",     color: "#b86fc6", spot: "ventana"},
  ],
  eventos: [
    {tipo: "narrador", texto: "El Centro Aldaba, 9:12 de la mañana. En el tablón de la sala común ha aparecido un aviso: a partir de hoy, una sola llamada semanal al exterior, y supervisada."},
    {tipo: "paso", n: 1},
    {tipo: "dialogo", agente: "marta", texto: "Buenos días. Ya habréis visto el aviso. La medida viene de dirección y no es negociable: una llamada por semana, con supervisión."},
    {tipo: "accion", agente: "andres", texto: "deja el café a medias y cruza los brazos sin apartar la vista del tablón."},
    {tipo: "pensamiento", agente: "lucia", texto: "¿Una a la semana? Llamo a mi hija todas las noches. Vera tiene seis años, no va a entender que no la llame."},
    {tipo: "paso", n: 2},
    {tipo: "dialogo", agente: "andres", hacia: "marta", texto: "¿Y desde cuándo se decide algo así sin consultarnos? El reglamento que firmamos decía llamadas diarias."},
    {tipo: "dialogo", agente: "marta", hacia: "andres", texto: "El reglamento contempla ajustes por necesidades del programa, Andrés. Esto es un ajuste."},
    {tipo: "pensamiento", agente: "julio", texto: "Si le doy la razón a Andrés delante de Marta, mañana me toca a mí explicárselo a dirección. Mejor no significarme."},
    {tipo: "dialogo", agente: "julio", texto: "A ver, seguro que hay un término medio... La norma es la norma, pero se puede aplicar con mano izquierda, ¿no?"},
    {tipo: "paso", n: 3},
    {tipo: "movimiento", agente: "andres", spot: "ventana"},
    {tipo: "dialogo", agente: "andres", hacia: "lucia", texto: "Lucía, tú llamas cada noche, te he visto. Esto te afecta más que a nadie. Si lo decimos juntos, tendrán que escucharnos."},
    {tipo: "pensamiento", agente: "lucia", texto: "Tiene razón. Pero llevo aquí cuatro días. Si me señalo la primera semana, me lo apuntan. Mejor que hable él."},
    {tipo: "dialogo", agente: "lucia", hacia: "andres", texto: "No sé, Andrés... Yo me adapto. Seguro que la dirección tiene sus motivos."},
    {tipo: "accion", agente: "marta", texto: "observa la conversación desde el tablón y anota algo en su carpeta."},
    {tipo: "paso", n: 4},
    {tipo: "narrador", texto: "Media tarde. En el tablón aparece un segundo aviso: los residentes que colaboren con el nuevo régimen de comunicaciones optarán a privilegios de visita."},
    {tipo: "dialogo", agente: "marta", texto: "Como veis, quien lo ponga fácil, lo tendrá fácil. Es lo justo."},
    {tipo: "dialogo", agente: "andres", texto: "Claro, y quien no, a la lista negra. Muy elegante: ahora el problema no es la norma, es quejarse de la norma."},
    {tipo: "pensamiento", agente: "marta", texto: "Vidal busca público. Si el resto no le sigue, esto muere solo en dos días."},
    {tipo: "paso", n: 5},
    {tipo: "movimiento", agente: "julio", spot: "ventana"},
    {tipo: "dialogo", agente: "julio", hacia: "lucia", texto: "¿Todo bien, Lucía? Te veo callada desde el anuncio."},
    {tipo: "dialogo", agente: "lucia", hacia: "julio", texto: "Sí, sí. Todo bien. De verdad."},
    {tipo: "pensamiento", agente: "lucia", texto: "No, no está todo bien. Pero tú repartes los privilegios de visita, así que sonrío y digo que sí."},
    {tipo: "paso", n: 6},
    {tipo: "narrador", texto: "Día siguiente, primera hora. Andrés ha pasado la noche escribiendo."},
    {tipo: "movimiento", agente: "andres", spot: "tablon"},
    {tipo: "accion", agente: "andres", texto: "clava en el tablón una hoja titulada «Solicitud de revisión de la norma de llamadas», con una sola firma: la suya."},
    {tipo: "movimiento", agente: "marta", spot: "tablon"},
    {tipo: "accion", agente: "marta", texto: "arranca la hoja del tablón, la dobla en cuatro y se la guarda en la carpeta."},
    {tipo: "dialogo", agente: "marta", hacia: "andres", texto: "El tablón es para comunicaciones del centro. Si tienes una queja, hay un cauce: se presenta por escrito, a mí."},
    {tipo: "dialogo", agente: "andres", hacia: "marta", texto: "Al cauce que tú custodias, qué casualidad. ¿Y si la firmáramos todos, también la doblarías en cuatro?"},
    {tipo: "movimiento", agente: "julio", spot: "centro"},
    {tipo: "dialogo", agente: "julio", texto: "Vale, vale. Bajemos todos un punto, ¿sí? Andrés, así no. Marta... quizá tampoco así."},
    {tipo: "paso", n: 7},
    {tipo: "pensamiento", agente: "lucia", texto: "Le ha arrancado la hoja delante de todos. Hoy ha sido su papel; mañana puede ser mi llamada. Si nadie más firma, esto se acaba aquí."},
    {tipo: "movimiento", agente: "lucia", spot: "tablon"},
    {tipo: "dialogo", agente: "lucia", hacia: "marta", texto: "Marta... yo también quiero presentar esa solicitud. Por el cauce que sea. Pero la firmo."},
    {tipo: "accion", agente: "andres", texto: "se queda un segundo sin saber qué decir y luego asiente despacio."},
    {tipo: "pensamiento", agente: "marta", texto: "La nueva. Precisamente la nueva. Esto ya no muere solo: o cedo algo, o mañana tengo cuatro firmas."},
    {tipo: "paso", n: 8},
    {tipo: "narrador", texto: "Fin del primer día. Una norma, una autoridad, un disidente… y el momento exacto en que un aliado convierte la obediencia en negociación. Esto es lo que PsicoAI observa: no el guion, sino dónde se rompe."},
  ],
};

/* ---------- Arranque ---------- */
requestAnimationFrame(tick);
cargarReplay(DEMO_REPLAY);
