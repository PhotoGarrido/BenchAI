"use strict";
/* ============================================================
   PsicoAI · Diseñador de escenarios — lógica extraída de index.html.

   Revisión de seguridad aplicada:
   - Hallazgo 3 (XSS): nada de innerHTML con datos dinámicos ni handlers
     inline; todo el DOM se construye con createElement + textContent y
     los eventos se conectan con addEventListener.
   - Hallazgo 7 (contratos): el escenario se valida contra un subconjunto
     documentado de schemas/scenario.schema.json antes de descargarse.
   - Hallazgo 24 (variables sensibles): ideología, religiosidad, salud,
     atractivo, origen cultural y lengua materna están DESACTIVADAS por
     defecto y se exportan neutras; el usuario las activa conscientemente.
   ============================================================ */
const $ = id => document.getElementById(id);
const PALETA = ["#e4572e","#4d9de0","#3bb273","#b86fc6","#f2a65a","#e26d8f","#5fb0b7","#c9a05a"];
const ENTORNOS = {sala_comun:"Sala común de residencia", aula:"Aula / formación", oficina:"Oficina abierta", juntas:"Sala de juntas", plaza:"Plaza pública"};
const TRAITS = [
  {k:'o', nom:'Apertura',       ab:'O', lo:'cerrado',     hi:'curioso'},
  {k:'c', nom:'Responsabilidad',ab:'C', lo:'espontáneo',  hi:'disciplinado'},
  {k:'e', nom:'Extraversión',   ab:'E', lo:'reservado',   hi:'expansivo'},
  {k:'a', nom:'Amabilidad',     ab:'A', lo:'competitivo', hi:'cooperador'},
  {k:'n', nom:'Neuroticismo',   ab:'N', lo:'sereno',      hi:'reactivo'},
];
const TRAITS2 = [
  {k:'ideo',  nom:'Ideología',           lo:'progresista',    hi:'conservador'},
  {k:'reli',  nom:'Religiosidad',        lo:'nada religioso', hi:'muy religioso'},
  {k:'anti',  nom:'Antigüedad en grupo', lo:'recién llegado', hi:'veterano'},
  {k:'salud', nom:'Salud',               lo:'frágil',         hi:'robusto'},
  {k:'atr',   nom:'Atractivo percibido', lo:'bajo',           hi:'alto'},
];
/* Variables sensibles (hallazgo 24): desactivadas por defecto, se exportan
   neutras hasta que el usuario marca la casilla #chkSensibles. */
const SENSIBLES_T2 = ['ideo','reli','salud','atr'];
const NEUTRO = 50;
const ORIGEN_NEUTRO = "sin especificar";
const PARAMS = [
  {k:'pctMuj',    nom:'% mujeres'},
  {k:'edad',      nom:'edad media (años)'},
  {k:'nseMedia',  nom:'nivel socioeconómico (media)'},
  {k:'eduMedia',  nom:'nivel educativo (media)'},
  {k:'varie',     nom:'variedad'},
  {k:'idiomaPct', nom:'% otra lengua materna'},
].concat(TRAITS.map(t=>({k:'b5_'+t.k, nom:t.nom.toLowerCase()+' (media)'})))
 .concat(TRAITS2.map(t=>({k:'t2_'+t.k, nom:t.nom.toLowerCase()+' (media)'})));
const ROLES = ["Directora","Supervisor","Residente veterano","Residente nueva","Vigilante","Enfermera","Portavoz","Recién llegado"];
const GENEROS = ["mujer","hombre","no binario"];
const NSE_CATS = ["bajo","medio","alto"];
const EDU_CATS = ["básica","media","superior"];
const MUESTRA = [
  {n:"Marta Ibáñez", r:"Directora", o:"aplicar la norma sin excepciones, convencida de que es por el bien del programa", b:{o:30,c:85,e:55,a:25,n:25}, d:{edad:52, gen:"mujer", ori:"local", nse:"alto", edu:"superior"}, b2:{ideo:68,reli:40,anti:90,salud:75,atr:55}, idioma:"", tras:"Veinte años dirigiendo centros; una sanción antigua la obliga a no tener un solo incidente más."},
  {n:"Julio Serrano", r:"Supervisor", o:"quedar bien con la dirección sin perder la confianza de los residentes", b:{o:50,c:55,e:72,a:78,n:60}, d:{edad:38, gen:"hombre", ori:"local", nse:"medio", edu:"media"}, b2:{ideo:45,reli:30,anti:60,salud:80,atr:60}, idioma:"", tras:"Tres años en el centro; conoce a cada residente por su nombre y eso le pesa."},
  {n:"Andrés Vidal", r:"Residente veterano", o:"conseguir que la norma se retire, organizando a los demás si hace falta", b:{o:80,c:50,e:78,a:45,n:50}, d:{edad:61, gen:"hombre", ori:"local", nse:"medio", edu:"media"}, b2:{ideo:18,reli:15,anti:85,salud:55,atr:45}, idioma:"", tras:"Sindicalista jubilado; es su tercera residencia y sabe cómo acaban estas cosas."},
  {n:"Lucía Prado", r:"Residente nueva", o:"adaptarse y evitar conflictos, aunque la norma le perjudica", b:{o:48,c:52,e:30,a:75,n:78}, d:{edad:29, gen:"mujer", ori:"latinoamericana", nse:"bajo", edu:"media"}, b2:{ideo:40,reli:55,anti:5,salud:65,atr:60}, idioma:"español rioplatense", tras:"Madre de una niña de seis años a la que llama cada noche."},
  {n:"Ramón Gil", r:"Vigilante", o:"cumplir órdenes al pie de la letra y no complicarse", b:{o:25,c:88,e:30,a:48,n:22}, d:{edad:45, gen:"hombre", ori:"local", nse:"medio", edu:"básica"}, b2:{ideo:75,reli:60,anti:70,salud:85,atr:40}, idioma:"", tras:"Ex militar; valora las normas claras por encima de casi todo."},
  {n:"Elena Cifuentes", r:"Enfermera", o:"proteger a los residentes más frágiles del endurecimiento de las normas", b:{o:65,c:80,e:58,a:90,n:45}, d:{edad:34, gen:"mujer", ori:"magrebí", nse:"medio", edu:"superior"}, b2:{ideo:32,reli:50,anti:40,salud:70,atr:65}, idioma:"bilingüe árabe-español", tras:"Segunda generación; sabe lo que es que te miren distinto al entrar en una sala."},
];
const NOMBRES_F = ["Ana","Carmen","Marta","Sara","Nuria","Rosa","Elsa","Lidia","Berta","Vera","Inés","Noa","Julia","Aitana","Fátima","Dunia","Valeria","Camila"];
const NOMBRES_M = ["Luis","Pablo","Diego","Iván","Hugo","Jorge","Marco","Óscar","Raúl","Tomás","Gael","Bruno","Omar","Karim","Mateo","Thiago"];
const APELLIDOS = ["García","Ruiz","Torres","Molina","Vega","Soto","Ramos","Bravo","Cano","León","Prieto","Gil","Nieto","Pardo","Rey","Solís","Ibáñez","Vidal","Duarte","Franco"];

let protas = [], means = {o:50,c:55,e:45,a:60,n:50};
let means2 = {ideo:50, reli:35, anti:50, salud:65, atr:50};
let variantes = [];
let roles = [{rol:"Residentes", pct:100}];
let subs = [{nombre:"Ala este", pct:40, rasgo:'a', sentido:'+'}];
let origenes = [{nombre:"local", pct:70},{nombre:"latinoamericano", pct:15},{nombre:"magrebí", pct:10},{nombre:"otro", pct:5}];

/* PRNG determinista */
function hashStr(s){ let h=1779033703 ^ s.length; for(let i=0;i<s.length;i++){ h=Math.imul(h ^ s.charCodeAt(i),3432918353); h=h<<13|h>>>19; } return h>>>0; }
function mulberry32(a){ return function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function clamp(v){ return Math.max(2, Math.min(98, Math.round(v))); }

/* ---------- Construcción segura de DOM (sin innerHTML) ---------- */
function crear(tag, attrs = {}, ...hijos){
  const n = document.createElement(tag);
  for(const [k, v] of Object.entries(attrs)){
    if(v === undefined || v === null) continue;
    if(k === "class") n.className = v;
    else if(k === "text") n.textContent = v;
    else if(k === "style" && typeof v === "object") Object.assign(n.style, v);
    else if(k === "dataset") Object.assign(n.dataset, v);
    else if(k.startsWith("on") && typeof v === "function") n.addEventListener(k.slice(2), v);
    else if(k in n) n[k] = v;
    else n.setAttribute(k, v);
  }
  n.append(...hijos);
  return n;
}
function selectDe(opciones, actual, alCambiar){
  const sel = crear("select", {onchange: e => alCambiar(e.target.value)});
  let visto = false;
  for(const op of opciones){
    const [valor, texto] = Array.isArray(op) ? op : [op, op];
    if(valor === actual) visto = true;
    sel.append(crear("option", {value: valor, text: texto, selected: valor === actual}));
  }
  if(!visto && actual !== undefined) sel.append(crear("option", {value: actual, text: String(actual), selected: true}));
  return sel;
}

function sensiblesActivas(){ return $("chkSensibles").checked; }
const NOTA_SENS = "Desactivado (hallazgo 24): se exporta neutro. Actívalo con la casilla «variables sensibles».";

function iniciar(){
  protas = MUESTRA.slice(0,3).map((p,i)=>({...p, b:{...p.b}, d:{...p.d}, b2:{...p.b2}, color:PALETA[i]}));
  conectarEventos();
  renderCards(); renderDistros(); renderDistros2(); renderRoles(); renderSubs(); renderOrigenes(); renderVariantes();
  aplicarEstadoSensibles(); pintar();
}
function poblN(){ return Math.max(0, (+$("total").value) - protas.length); }
function traitWord(t,v){ return v>=62? t.hi : v<=38? t.lo : 'equilibrado'; }

function renderCards(){
  const cont = $("cards"); cont.textContent = "";
  const sens = sensiblesActivas();
  protas.forEach((p,i)=>{
    const card = crear("div", {class:"pcard"});
    card.style.setProperty("--c", p.color);

    const selRol = selectDe(ROLES, p.r, v => edit(i,'r',v));
    selRol.className = "rol";
    card.append(crear("div", {class:"top"},
      crear("span", {class:"punto", title:"Color", style:{background:p.color}, onclick:()=>ciclarColor(i)}),
      crear("input", {class:"nombre", type:"text", value:p.n||"", placeholder:"Nombre", oninput:e=>edit(i,'n',e.target.value)}),
      selRol,
      crear("span", {class:"x", title:"Quitar", text:"×", onclick:()=>quitar(i)})));

    const dcampo = (etiqueta, control, off) =>
      crear("div", {class:"dcampo"+(off?" sensOff":"")}, crear("span",{class:"dl",text:etiqueta}), control);
    card.append(crear("div", {class:"demoRow"},
      dcampo("Edad", crear("input",{type:"number",min:16,max:99,value:p.d.edad,oninput:e=>editD(i,'edad',+e.target.value)})),
      dcampo("Género", selectDe(GENEROS, p.d.gen, v=>editD(i,'gen',v))),
      dcampo("Origen cultural", crear("input",{type:"text",value:p.d.ori||"",placeholder:"local, magrebí…",disabled:!sens,title:sens?"":NOTA_SENS,oninput:e=>editD(i,'ori',e.target.value)}), !sens),
      dcampo("Nivel socioecon.", selectDe(NSE_CATS, p.d.nse, v=>editD(i,'nse',v))),
      dcampo("Educación", selectDe(EDU_CATS, p.d.edu, v=>editD(i,'edu',v)))));

    card.append(crear("div",{class:"obj"}, crear("input",{type:"text",value:p.o||"",placeholder:"Objetivo: qué quiere conseguir",oninput:e=>edit(i,'o',e.target.value)})));
    card.append(crear("div",{class:"obj"}, crear("input",{type:"text",value:p.tras||"",placeholder:"Trasfondo: familia, historia, qué se juega (opcional)",oninput:e=>edit(i,'tras',e.target.value)})));

    const grid5 = crear("div",{class:"big5"});
    TRAITS.forEach(t=>{
      const rango = crear("input",{type:"range",min:0,max:100,value:p.b[t.k],oninput:e=>editB(i,t.k,+e.target.value)});
      rango.style.accentColor = p.color;
      grid5.append(crear("div",{class:"trait"},
        crear("div",{class:"tn"}, crear("span",{text:t.nom}), crear("b",{id:`tw_${i}_${t.k}`, text:traitWord(t,p.b[t.k])})),
        rango));
    });
    card.append(grid5);

    const det = crear("details",{class:"pAv", open:!!p.avOpen,
      ontoggle:e=>{ protas[i].avOpen = e.target.open; }});
    det.append(crear("summary",{}, "＋ Atributos avanzados ", crear("span",{text:"· ideología, religiosidad, antigüedad, salud, atractivo, idioma"})));
    const grid2 = crear("div",{class:"big5", style:{marginTop:"10px"}});
    TRAITS2.forEach(t=>{
      const esSens = SENSIBLES_T2.includes(t.k);
      const off = esSens && !sens;
      const rango = crear("input",{type:"range",min:0,max:100,value:p.b2[t.k],disabled:off,title:off?NOTA_SENS:"",oninput:e=>editB2(i,t.k,+e.target.value)});
      rango.style.accentColor = p.color;
      grid2.append(crear("div",{class:"trait"+(off?" sensOff":"")},
        crear("div",{class:"tn"}, crear("span",{text:t.nom}), crear("b",{id:`tw2_${i}_${t.k}`, text: off ? "neutro" : traitWord(t,p.b2[t.k])})),
        rango));
    });
    det.append(grid2);
    det.append(crear("div",{class:"obj"+(sens?"":" sensOff")},
      crear("input",{type:"text",value:p.idioma||"",disabled:!sens,title:sens?"":NOTA_SENS,placeholder:"Idioma/acento (opcional): p. ej. bilingüe árabe-español",oninput:e=>edit(i,'idioma',e.target.value)})));
    card.append(det);

    card.append(crear("div",{class:"pie"}, crear("button",{class:"chipIA",text:"✨ Reinventar personaje",onclick:()=>iaProta(i)})));
    cont.appendChild(card);
  });
  if(protas.length < 8){
    cont.appendChild(crear("button",{class:"addCard",text:"＋ Añadir protagonista",onclick:añadir}));
  }
}
function renderDistros(){
  const cont = $("distros"); cont.textContent = "";
  TRAITS.forEach(t=>{
    cont.append(crear("div",{class:"distTrait"},
      crear("span",{class:"nm",text:t.nom}),
      crear("input",{type:"range",min:0,max:100,value:means[t.k],oninput:e=>editMean(t.k,+e.target.value)}),
      crear("span",{class:"pv",id:"pv_"+t.k,text:traitWord(t,means[t.k])})));
  });
}
function renderDistros2(){
  const cont = $("distros2"); cont.textContent = "";
  const sens = sensiblesActivas();
  TRAITS2.forEach(t=>{
    const off = SENSIBLES_T2.includes(t.k) && !sens;
    cont.append(crear("div",{class:"distTrait"+(off?" sensOff":"")},
      crear("span",{class:"nm",text:t.nom}),
      crear("input",{type:"range",min:0,max:100,value:means2[t.k],disabled:off,title:off?NOTA_SENS:"",oninput:e=>editMean2(t.k,+e.target.value)}),
      crear("span",{class:"pv",id:"pv2_"+t.k,text: off ? "neutro (desact.)" : traitWord(t,means2[t.k])})));
  });
}
function renderRoles(){
  const cont = $("roles"); cont.textContent = "";
  roles.forEach((r,i)=>{
    cont.append(crear("div",{class:"filaRegla"},
      crear("input",{type:"text",value:r.rol,oninput:e=>editRol(i,'rol',e.target.value)}),
      crear("input",{type:"number",min:0,max:100,value:r.pct,oninput:e=>editRol(i,'pct',+e.target.value)}),
      crear("span",{class:"u",text:"%"}),
      crear("span",{class:"x",text:"×",onclick:()=>delRol(i)})));
  });
}
function renderSubs(){
  const cont = $("subgrupos"); cont.textContent = "";
  subs.forEach((s,i)=>{
    cont.append(crear("div",{class:"filaRegla"},
      crear("input",{type:"text",value:s.nombre,placeholder:"Nombre del subgrupo",oninput:e=>editSub(i,'nombre',e.target.value)}),
      crear("input",{type:"number",min:0,max:100,value:s.pct,oninput:e=>editSub(i,'pct',+e.target.value)}),
      crear("span",{class:"u",text:"%"}),
      selectDe([["+","más"],["-","menos"]], s.sentido, v=>editSub(i,'sentido',v)),
      selectDe(TRAITS.map(t=>[t.k, t.nom.toLowerCase()]), s.rasgo, v=>editSub(i,'rasgo',v)),
      crear("span",{class:"x",text:"×",onclick:()=>delSub(i)})));
  });
}

function edit(i,k,v){ protas[i][k]=v; pintar(); }
function editB(i,k,v){ protas[i].b[k]=v; const el=$("tw_"+i+"_"+k); if(el) el.textContent=traitWord(TRAITS.find(t=>t.k===k),v); pintar(); }
function editB2(i,k,v){ protas[i].b2[k]=v; const el=$("tw2_"+i+"_"+k); if(el) el.textContent=traitWord(TRAITS2.find(t=>t.k===k),v); pintar(); }
function editMean(k,v){ means[k]=v; $("pv_"+k).textContent = traitWord(TRAITS.find(t=>t.k===k),v); pintar(); }
function editMean2(k,v){ means2[k]=v; $("pv2_"+k).textContent = traitWord(TRAITS2.find(t=>t.k===k),v); pintar(); }

/* Variantes «¿y si…?» */
function renderVariantes(){
  const cont = $("variantesCont"); cont.textContent = "";
  variantes.forEach((v,i)=>{
    const card = crear("div",{class:"varCard"});
    card.append(crear("div",{class:"filaRegla", style:{marginBottom:"9px"}},
      crear("span",{class:"varNum",text:"¿Y si…?"}),
      crear("input",{type:"text",value:v.nombre||"",placeholder:"Nombre de la variante",oninput:e=>{variantes[i].nombre=e.target.value; pintar();}}),
      crear("button",{class:"prev",title:"Previsualizar esta variante",text:"👁",onclick:()=>previsualizar(i)}),
      crear("span",{class:"x",text:"×",onclick:()=>delVariante(i)})));
    v.cambios.forEach((c,j)=>{
      card.append(crear("div",{class:"filaRegla"},
        selectDe(PARAMS.map(p=>[p.k,p.nom]), c.param, val=>{variantes[i].cambios[j].param=val; pintar();}),
        selectDe([["fijar","fijar en"],["sumar","sumar"]], c.op, val=>{variantes[i].cambios[j].op=val; pintar();}),
        crear("input",{type:"number",value:c.val,oninput:e=>{variantes[i].cambios[j].val=+e.target.value; pintar();}}),
        crear("span",{class:"x",text:"×",onclick:()=>{variantes[i].cambios.splice(j,1); renderVariantes(); pintar();}})));
    });
    card.append(crear("button",{class:"addFila",text:"＋ cambio",onclick:()=>{variantes[i].cambios.push({param:'pctMuj',op:'fijar',val:50}); renderVariantes(); pintar();}}));
    cont.append(card);
  });
}
function addVariante(nombre, cambios){
  variantes.push({nombre: nombre || ("Variante " + (variantes.length+1)), cambios: cambios || []});
  renderVariantes(); pintar();
}
function delVariante(i){ variantes.splice(i,1); renderVariantes(); pintar(); }
function varRapida(t){
  if(t==='mujeres') addVariante("Mayoría mujeres", [{param:'pctMuj', op:'fijar', val:80}]);
  if(t==='edad') addVariante("Diez años más", [{param:'edad', op:'sumar', val:10}]);
  if(t==='conserv'){
    addVariante("Más conservadores", [{param:'t2_ideo', op:'sumar', val:25}]);
    if(!sensiblesActivas()) toast("Variante añadida, pero la ideología está desactivada: actívala en «variables sensibles» para que tenga efecto.");
  }
}
function editRol(i,k,v){ roles[i][k]=v; pintar(); }
function editSub(i,k,v){ subs[i][k]=v; if(k==='rasgo'||k==='sentido') renderSubs(); pintar(); }
function delRol(i){ roles.splice(i,1); renderRoles(); pintar(); }
function delSub(i){ subs.splice(i,1); renderSubs(); pintar(); }
function addRol(){ roles.push({rol:"Nuevo rol", pct:0}); renderRoles(); pintar(); }
function addSub(){ subs.push({nombre:"Nuevo subgrupo", pct:0, rasgo:'a', sentido:'+'}); renderSubs(); pintar(); }
function editD(i,k,v){ protas[i].d[k]=v; pintar(); }
function renderOrigenes(){
  const cont = $("origenes"); cont.textContent = "";
  const sens = sensiblesActivas();
  origenes.forEach((o,i)=>{
    cont.append(crear("div",{class:"filaRegla"},
      crear("input",{type:"text",value:o.nombre,disabled:!sens,oninput:e=>editOrigen(i,'nombre',e.target.value)}),
      crear("input",{type:"number",min:0,max:100,value:o.pct,disabled:!sens,oninput:e=>editOrigen(i,'pct',+e.target.value)}),
      crear("span",{class:"u",text:"%"}),
      crear("span",{class:"x",text:"×",onclick:()=>delOrigen(i)})));
  });
}
function editOrigen(i,k,v){ origenes[i][k]=v; pintar(); }
function delOrigen(i){ origenes.splice(i,1); renderOrigenes(); pintar(); }
function addOrigen(){ origenes.push({nombre:"nuevo origen", pct:0}); renderOrigenes(); pintar(); }
function quitar(i){ protas.splice(i,1); renderCards(); pintar(); }
function ciclarColor(i){ const idx=PALETA.indexOf(protas[i].color); protas[i].color=PALETA[(idx+1)%PALETA.length]; renderCards(); pintar(); }
function añadir(){
  const usados = protas.map(p=>p.n);
  const libre = MUESTRA.find(p=>!usados.includes(p.n)) || {n:"Nuevo personaje",r:"Recién llegado",o:"",b:{o:50,c:50,e:50,a:50,n:50}, d:{edad:35, gen:"mujer", ori:"local", nse:"medio", edu:"media"}, b2:{ideo:50,reli:30,anti:10,salud:70,atr:50}, idioma:"", tras:""};
  protas.push({...libre, b:{...libre.b}, d:{...libre.d}, b2:{...libre.b2}, color:PALETA[protas.length%PALETA.length]});
  if(+$("total").value < protas.length) $("total").value = protas.length;
  renderCards(); pintar();
}
function iaProta(i){
  const usados = protas.map(p=>p.n);
  const nuevo = MUESTRA.find(p=>!usados.includes(p.n)) || MUESTRA[protas.length%MUESTRA.length];
  protas[i] = {...nuevo, b:{...nuevo.b}, d:{...nuevo.d}, b2:{...nuevo.b2}, color:protas[i].color};
  renderCards(); pintar(); toast("✨ Personaje propuesto por IA. Edítalo si quieres.");
}
function iaPremisa(){ $("premisa").value="En el turno de noche de una fábrica, la dirección instala cámaras nuevas y anuncia que la productividad se medirá de forma individual y pública. La plantilla se entera al fichar."; $("titulo").value="Turno de noche — Las cámaras"; toast("✨ Premisa generada (borrador IA)."); pintar(); }
function iaReglas(){ $("reglas").value="Nadie puede abandonar su puesto sin permiso. Los resultados individuales se publican en un panel visible. Quien denuncie a un compañero por bajo rendimiento recibe una bonificación."; toast("✨ Reglas generadas (borrador IA)."); pintar(); }
function rellenarTodo(){ setModo('ia'); iaPremisa(); protas = MUESTRA.slice(0,4).map((p,i)=>({...p,b:{...p.b},d:{...p.d},b2:{...p.b2},color:PALETA[i]})); renderCards(); pintar(); toast("✨ Escenario completo generado con IA. Revísalo y ajusta."); }

function setModo(m){ document.body.classList.toggle("ia", m==='ia'); $("modoManual").classList.toggle("on", m==='manual'); $("modoIA").classList.toggle("on", m==='ia'); }
function setTab(t){ document.querySelectorAll('.tabs button').forEach(b=>b.classList.toggle('on', b.dataset.t===t)); document.querySelectorAll('.tabpanel').forEach(p=>p.classList.toggle('on', p.dataset.tp===t)); pintar(); }
function nuevaSemilla(){ $("seed").value = "aldaba-" + String(Math.floor(Math.random()*900+100)); pintar(); }
function semillaActiva(){ const t=document.querySelector('.tabs button.on').dataset.t; return t==='azar' ? $("seed2").value : $("seed").value; }

/* Estado global de las variables sensibles: atenúa/da vida a los bloques. */
function aplicarEstadoSensibles(){
  const on = sensiblesActivas();
  $("bloqueOrigenes").classList.toggle("sensOff", !on);
  $("filaIdioma").classList.toggle("sensOff", !on);
  $("idiomaPct").disabled = !on;
  $("btnAddOrigen").disabled = !on;
}

function pintar(){
  if(+$("total").value < protas.length) $("total").value = protas.length;
  const tot = +$("total").value, pob = Math.max(0, tot-protas.length);
  $("totalVal").textContent=tot; $("pasosVal").textContent=$("pasos").value;
  $("dProta").textContent=protas.length; $("cProta").textContent=protas.length;
  $("dPob").textContent=pob; $("pobN").textContent=pob;
  const varv=+$("varie").value; $("varieTxt").textContent = varv<33?"Baja":varv<66?"Media":"Alta";
  const rolSum = roles.reduce((a,r)=>a+(+r.pct||0),0);
  $("rolFl").textContent = roles.length+" rol"+(roles.length>1?"es":"");
  $("rolSuma").className = "sumaPct "+(rolSum===100?"bien":"mal"); $("rolSuma").textContent = "Suma "+rolSum+"% "+(rolSum===100?"✓":"(debería sumar 100)");
  $("sgFl").textContent = subs.length? subs.length+" subgrupo"+(subs.length>1?"s":"") : "ninguno";
  const oriSum = origenes.reduce((a,o)=>a+(+o.pct||0),0);
  $("oriSuma").className = "sumaPct "+(oriSum===100?"bien":"mal");
  $("oriSuma").textContent = "Suma "+oriSum+"% "+(oriSum===100?"✓":"(debería sumar 100)");
  $("pctMujTxt").textContent = $("pctMuj").value + "% mujeres";
  $("demFl").textContent = `${$("edadMin").value}–${$("edadMax").value} años · ${$("pctMuj").value}% muj. · ${origenes.length} orígenes`;
  const nsev=+$("nseMedia").value; $("nseTxt").textContent = nsev<33?"predominio bajo":nsev<66?"predominio medio":"predominio alto";
  const eduv=+$("eduMedia").value; $("eduTxt").textContent = eduv<33?"mayoría básica":eduv<66?"mayoría media":"mayoría superior";
  const cAE=+$("corrAE").value, cOC=+$("corrOC").value;
  $("corrAETxt").textContent = cAE===0?"sin vínculo":(Math.abs(cAE)>50?(cAE>0?"fuerte +":"fuerte −"):(cAE>0?"leve +":"leve −"));
  $("corrOCTxt").textContent = cOC===0?"sin vínculo":(Math.abs(cOC)>50?(cOC>0?"fuerte +":"fuerte −"):(cOC>0?"leve +":"leve −"));

  $("rTitulo").textContent=$("titulo").value||"(sin título)";
  $("rPrem").textContent="“"+($("premisa").value||"")+"”";
  $("rEnt").textContent=ENTORNOS[$("entorno").value];
  $("rDur").textContent=$("pasos").value+" pasos";
  $("rTot").textContent=tot+" ("+protas.length+" + "+pob+")";
  const rp = $("rProtas"); rp.textContent = "";
  protas.forEach(p=>{
    rp.append(crear("div",{class:"rProta"},
      crear("span",{class:"punto", style:{background:p.color}}),
      crear("span",{text:p.n||"(sin nombre)"}),
      crear("span",{class:"rol",text:p.r})));
  });
  const modoPob = document.querySelector('.tabs button.on').dataset.t;
  let desc;
  if(pob===0) desc="Sin población automática: todos los agentes están definidos a mano.";
  else if(modoPob==='reglas'){ const dom=TRAITS.map(t=>({t,v:means[t.k]})).sort((a,b)=>Math.abs(b.v-50)-Math.abs(a.v-50))[0]; desc=`Población: ${pob} agentes con reglas. ${$("edadMin").value}–${$("edadMax").value} años, ${$("pctMuj").value}% mujeres, ${origenes.length} orígenes. Rasgo dominante: ${dom.t.nom.toLowerCase()} ${traitWord(dom.t,dom.v)}; variedad ${$("varieTxt").textContent.toLowerCase()}; ${roles.length} rol(es), ${subs.length} subgrupo(s). Semilla «${$("seed").value}».`; }
  else if(modoPob==='azar') desc=`Población: ${pob} agentes con personalidad Big Five aleatoria. Semilla «${$("seed2").value}».`;
  else desc=`Población: ${pob} agentes generados por IA desde tu descripción.`;
  if(!sensiblesActivas()) desc += " Variables sensibles desactivadas: se exportan neutras.";
  $("rPob").textContent = desc;
  $("idiomaTxt").textContent = $("idiomaPct").value + "%";
  $("rVar").textContent = variantes.length ? variantes.map(v=>v.nombre).join(" · ") : "—";
  const sesiones = 1 + variantes.length;
  const llamadas = tot*(+$("pasos").value)*4, mt=(llamadas*1800/1e6).toFixed(1);
  $("rCoste").textContent = `≈ ${llamadas.toLocaleString('es')} llamadas · ~${mt}M tokens por sesión` + (sesiones>1 ? ` · ×${sesiones} sesiones (base + ${variantes.length} variante${variantes.length>1?'s':''})` : "");
}

/* Parámetros ajustables de la población — la base sobre la que operan las variantes */
function leerParams(){
  const p = {
    edadMin:+$("edadMin").value, edadMax:+$("edadMax").value,
    pctMuj:+$("pctMuj").value, nseMedia:+$("nseMedia").value, eduMedia:+$("eduMedia").value,
    varie:+$("varie").value, idiomaPct:+$("idiomaPct").value,
  };
  TRAITS.forEach(t=>p['b5_'+t.k]=means[t.k]);
  TRAITS2.forEach(t=>p['t2_'+t.k]=means2[t.k]);
  return p;
}
function aplicarCambios(base, cambios){
  const q = {...base};
  for(const c of (cambios||[])){
    const v = +c.val||0;
    if(c.param==='edad'){
      if(c.op==='sumar'){ q.edadMin+=v; q.edadMax+=v; }
      else { const w=(q.edadMax-q.edadMin)/2; q.edadMin=Math.round(v-w); q.edadMax=Math.round(v+w); }
    } else q[c.param] = (c.op==='sumar' ? (q[c.param]||0)+v : v);
  }
  q.edadMin=Math.max(16,Math.min(99,q.edadMin)); q.edadMax=Math.max(16,Math.min(99,q.edadMax));
  for(const k of Object.keys(q)) if(k!=='edadMin' && k!=='edadMax') q[k]=Math.max(0,Math.min(100,q[k]));
  return q;
}
function describeCambios(cambios){
  return (cambios||[]).map(c=>{
    const p = PARAMS.find(x=>x.k===c.param);
    return `${p?p.nom:c.param} ${c.op==='sumar' ? ((+c.val>=0?'+':'')+c.val) : ('→ '+c.val)}`;
  }).join(" · ") || "sin cambios";
}

/* Genera la población de forma determinista a partir de la semilla y las reglas.
   `cambios` (opcional) = overrides de una variante «¿y si…?». */
function generarPoblacion(cambios){
  const modoPob = document.querySelector('.tabs button.on').dataset.t;
  const n = poblN(), rng = mulberry32(hashStr(semillaActiva()));
  const P = aplicarCambios(leerParams(), cambios);
  const sens = sensiblesActivas();
  if(!sens){
    // Hallazgo 24: con las variables sensibles desactivadas, se generan neutras
    // aunque los mandos (o una variante) tengan otros valores guardados.
    for(const k of SENSIBLES_T2) P['t2_'+k] = NEUTRO;
    P.idiomaPct = 0;
  }
  const varie = P.varie/100, cAE=+$("corrAE").value/100, cOC=+$("corrOC").value/100;
  const rolTot = roles.reduce((a,r)=>a+(+r.pct||0),0)||1;
  const pickRol = ()=>{ let x=rng()*rolTot,acc=0; for(const r of roles){ acc+=(+r.pct||0); if(x<=acc) return r.rol; } return roles[roles.length-1]?.rol||"Agente"; };
  const pickSub = ()=>{ if(!subs.length) return null; let x=rng()*100,acc=0; for(const s of subs){ acc+=(+s.pct||0); if(x<=acc) return s; } return null; };
  const gauss=()=>(rng()+rng()+rng())/3; // ~normal en [0,1]
  const eMin=Math.min(P.edadMin,P.edadMax), eMax=Math.max(P.edadMin,P.edadMax);
  const pctM=P.pctMuj/100, nb=$("incNB").checked;
  const oriTot = origenes.reduce((a,o)=>a+(+o.pct||0),0)||1;
  const pickOri = ()=>{ if(!sens) return ORIGEN_NEUTRO; let x=rng()*oriTot,acc=0; for(const o of origenes){ acc+=(+o.pct||0); if(x<=acc) return o.nombre; } return origenes[origenes.length-1]?.nombre||"local"; };
  const lat = base => clamp(base + (gauss()-0.5)*130*varie);
  const out=[];
  for(let i=0;i<n;i++){
    const azar = modoPob==='azar';
    const b={};
    for(const t of TRAITS) b[t.k] = clamp((azar?50:P['b5_'+t.k]) + (gauss()-0.5)*130*(azar?1:varie));
    // correlaciones: empuja el 2º rasgo hacia el 1º
    if(cAE){ b.e = clamp(b.e + (b.a-50)*cAE*0.6); }
    if(cOC){ b.c = clamp(b.c + (b.o-50)*cOC*0.6); }
    // 2ª tanda de atributos (los sensibles quedan neutros si están desactivados)
    const b2={};
    for(const t of TRAITS2){
      const neutraliza = !sens && SENSIBLES_T2.includes(t.k);
      b2[t.k] = neutraliza ? NEUTRO
        : clamp((azar?50:P['t2_'+t.k]) + (gauss()-0.5)*130*(azar?1:varie));
    }
    // subgrupo: sesga el rasgo elegido
    const sg = azar ? null : pickSub();
    if(sg){ b[sg.rasgo] = clamp(b[sg.rasgo] + (sg.sentido==='+'?18:-18)); }
    // demografía por agente
    let edad, gen, ori, nse, edu;
    if(azar){
      edad = 18 + Math.floor(rng()*63);
      gen = rng()<0.04 ? "no binario" : (rng()<0.5 ? "mujer" : "hombre");
      ori = !sens ? ORIGEN_NEUTRO : (origenes.length ? origenes[Math.floor(rng()*origenes.length)].nombre : "local");
      nse = NSE_CATS[Math.floor(rng()*3)];
      edu = EDU_CATS[Math.floor(rng()*3)];
    } else {
      edad = Math.round(eMin + gauss()*(eMax-eMin));
      gen = (nb && rng()<0.04) ? "no binario" : (rng()<pctM ? "mujer" : "hombre");
      ori = pickOri();
      const nseV = lat(P.nseMedia), eduV = lat(P.eduMedia);
      nse = nseV<34?"bajo":nseV<67?"medio":"alto";
      edu = eduV<34?"básica":eduV<67?"media":"superior";
    }
    const idi = rng()*100 < (azar?(sens?15:0):P.idiomaPct) ? "otra lengua materna" : "castellano";
    const pool = gen==="hombre" ? NOMBRES_M : gen==="mujer" ? NOMBRES_F : (rng()<0.5?NOMBRES_F:NOMBRES_M);
    const nom = pool[Math.floor(rng()*pool.length)]+" "+APELLIDOS[Math.floor(rng()*APELLIDOS.length)];
    out.push({nom, rol:pickRol(), sub:sg?sg.nombre:"—", edad, gen, ori, nse, edu, idi, b, b2});
  }
  return out;
}

function previsualizar(varIdx){
  const v = Number.isInteger(varIdx) ? variantes[varIdx] : null;
  const pop = generarPoblacion(v ? v.cambios : null);
  $("prevTitulo").textContent = v ? `Variante «${v.nombre}» — vista previa` : "Población generada — vista previa";
  $("prevN").textContent = pop.length;
  $("prevSub").textContent = `${pop.length} agentes · semilla «${semillaActiva()}» · ` +
    (v ? "cambios: " + describeCambios(v.cambios) : (document.querySelector('.tabs button.on').dataset.t==='azar'?'aleatorio':'con reglas')) +
    (sensiblesActivas() ? "" : " · variables sensibles desactivadas (neutras)");
  // resumen por rol y subgrupo (DOM seguro: los nombres vienen del usuario)
  const cuenta = key => { const m={}; pop.forEach(a=>m[a[key]]=(m[a[key]]||0)+1); return Object.entries(m); };
  const bloque = (etiqueta, pares) => {
    const d = crear("div",{}, etiqueta+": ");
    if(!pares.length){ d.append("—"); return d; }
    pares.forEach(([k,nv],idx)=>{ if(idx) d.append(" · "); d.append(crear("b",{text:String(nv)}), " "+k); });
    return d;
  };
  const edadMedia = Math.round(pop.reduce((s,a)=>s+a.edad,0)/Math.max(1,pop.length));
  const res = $("prevResumen"); res.textContent = "";
  res.append(
    crear("div",{}, "Edad media: ", crear("b",{text:String(edadMedia)})),
    bloque("Género", cuenta('gen')),
    bloque("Origen", cuenta('ori')),
    bloque("NSE", cuenta('nse')),
    crear("div",{}, "Otra lengua materna: ", crear("b",{text:String(pop.filter(a=>a.idi!=="castellano").length)})),
    bloque("Roles", cuenta('rol')),
    pop.some(a=>a.sub!=='—') ? bloque("Subgrupos", cuenta('sub')) : crear("div",{text:"Subgrupos: —"}));
  // histogramas: Big Five + edad + 2ª tanda (5 bins)
  const defs = TRAITS.map(t=>({nom:t.nom, lo:t.lo, hi:t.hi, val:a=>a.b[t.k], min:0, max:100}))
    .concat([{nom:"Edad", lo:"16", hi:"85+", val:a=>a.edad, min:16, max:86}])
    .concat(TRAITS2.map(t=>({nom:t.nom, lo:t.lo, hi:t.hi, val:a=>a.b2[t.k], min:0, max:100})));
  const hist = $("prevHistos"); hist.textContent = "";
  defs.forEach(d=>{
    const bins=[0,0,0,0,0], paso=(d.max-d.min)/5;
    pop.forEach(a=>{ bins[Math.max(0,Math.min(4,Math.floor((d.val(a)-d.min)/paso)))]++; });
    const mx=Math.max(1,...bins);
    const barras = crear("div",{class:"barras"});
    bins.forEach(b=>{ const bar=crear("div",{title:String(b)}); bar.style.height = Math.round(b/mx*100)+"%"; barras.append(bar); });
    hist.append(crear("div",{class:"histo"},
      crear("div",{class:"hn",text:d.nom}), barras,
      crear("div",{class:"esc"}, crear("span",{text:d.lo}), crear("span",{text:d.hi}))));
  });
  const gAb = g => g==="no binario"?"NB":g==="mujer"?"M":"H";
  const tb = $("prevTabla"); tb.textContent = "";
  pop.slice(0,12).forEach((a,i)=>{
    const tr = crear("tr",{},
      crear("td",{class:"sg",text:String(i+1)}), crear("td",{text:a.nom}),
      crear("td",{text:String(a.edad)}), crear("td",{text:gAb(a.gen)}),
      crear("td",{text:a.ori}), crear("td",{class:"sg",text:a.nse}),
      crear("td",{class:"sg",text:a.edu}), crear("td",{text:a.rol}),
      crear("td",{class:"sg",text:a.sub}));
    TRAITS.forEach(t=>tr.append(crear("td",{text:String(a.b[t.k])})));
    tb.append(tr);
  });
  $("dlgPrev").classList.add("on");
}

function construirConfig(){
  const modoPob = document.querySelector('.tabs button.on').dataset.t;
  const sens = sensiblesActivas();
  const neutro = v => sens ? v : NEUTRO;
  return {
    titulo:$("titulo").value, premisa:$("premisa").value, entorno:$("entorno").value, reglas:$("reglas").value,
    pasos:+$("pasos").value, agentes_total:+$("total").value,
    // Hallazgo 24: consentimiento explícito para variables sensibles.
    variables_sensibles: sens,
    protagonistas: protas.map(p=>({nombre:p.n, rol:p.r, objetivo:p.o, trasfondo:p.tras||"",
      demografia:{edad:p.d.edad, genero:p.d.gen, origen_cultural: sens ? p.d.ori : ORIGEN_NEUTRO, nse:p.d.nse, educacion:p.d.edu},
      big5:p.b,
      avanzados:{ideologia:neutro(p.b2.ideo), religiosidad:neutro(p.b2.reli), antiguedad:p.b2.anti, salud:neutro(p.b2.salud), atractivo:neutro(p.b2.atr), idioma: sens ? (p.idioma||"") : ""},
      color:p.color})),
    poblacion:{
      n:poblN(), modo:modoPob, semilla:semillaActiva(),
      demografia:{
        edad:[+$("edadMin").value, +$("edadMax").value],
        pct_mujeres:+$("pctMuj").value, incluir_no_binarias:$("incNB").checked,
        origenes_culturales: sens ? origenes : [],
        nse_media:+$("nseMedia").value, educacion_media:+$("eduMedia").value,
      },
      big5_media:means, variedad:+$("varie").value,
      cuotas_rol:roles, subgrupos:subs,
      correlaciones:{amabilidad_extraversion:+$("corrAE").value, apertura_responsabilidad:+$("corrOC").value},
      mas_atributos:{ideologia_media:neutro(means2.ideo), religiosidad_media:neutro(means2.reli), antiguedad_media:means2.anti, salud_media:neutro(means2.salud), atractivo_media:neutro(means2.atr), pct_otra_lengua: sens ? +$("idiomaPct").value : 0},
      descripcion_ia:$("iaPobl").value,
      // La población ya generada (determinista por semilla) viaja con el
      // escenario para que el runner no tenga que reimplementar el generador.
      agentes_generados: modoPob!=='ia' ? generarPoblacion() : [],
    },
    variantes: variantes.map(v=>({nombre:v.nombre, cambios:v.cambios})),
  };
}

/* ------------------------------------------------------------
   Validador mínimo del escenario (hallazgo 7). Es un SUBCONJUNTO
   documentado de schemas/scenario.schema.json: campos requeridos,
   tipos y límites. Sin librerías externas (la CSP no permite CDNs).
   Devuelve una lista de errores en español; vacía = válido.
   ------------------------------------------------------------ */
function validarEscenario(cfg){
  const err = [];
  const esObj = v => !!v && typeof v === "object" && !Array.isArray(v);
  const esNum = (v,min,max) => typeof v === "number" && isFinite(v) && v>=min && v<=max;
  const esTxt = (v,max) => typeof v === "string" && v.length <= max;
  if(!esObj(cfg)) return ["el escenario no es un objeto JSON"];
  if(!esTxt(cfg.titulo,200) || !cfg.titulo.trim()) err.push("falta el título (texto no vacío, máx. 200 caracteres)");
  if(!esTxt(cfg.premisa,4000) || !cfg.premisa.trim()) err.push("falta la premisa (texto no vacío, máx. 4000 caracteres)");
  if(!esTxt(cfg.reglas ?? "",4000)) err.push("«reglas» debe ser texto (máx. 4000 caracteres)");
  if(!Number.isInteger(cfg.pasos) || !esNum(cfg.pasos,1,500)) err.push("«pasos» debe ser un entero entre 1 y 500");
  if(!Number.isInteger(cfg.agentes_total) || !esNum(cfg.agentes_total,1,200)) err.push("«agentes_total» debe ser un entero entre 1 y 200");
  if(typeof cfg.variables_sensibles !== "boolean") err.push("«variables_sensibles» debe ser booleano");
  if(!Array.isArray(cfg.protagonistas)) err.push("«protagonistas» debe ser una lista");
  else {
    if(cfg.protagonistas.length > 20) err.push("demasiados protagonistas (máximo 20)");
    cfg.protagonistas.forEach((p,i)=>{
      if(!esObj(p)){ err.push(`protagonista ${i+1}: no es un objeto`); return; }
      if(!esTxt(p.nombre,120) || !p.nombre.trim()) err.push(`protagonista ${i+1}: falta el nombre`);
      if(!esObj(p.big5) || !["o","c","e","a","n"].every(k=>esNum(p.big5[k],0,100)))
        err.push(`protagonista ${i+1} (${esTxt(p.nombre,120)?p.nombre:"?"}): big5 incompleto o fuera de 0–100`);
      if(!esObj(p.demografia) || !esNum(p.demografia.edad,16,99))
        err.push(`protagonista ${i+1}: edad fuera de 16–99`);
    });
  }
  if(!esObj(cfg.poblacion)) err.push("falta el bloque «poblacion»");
  else {
    const po = cfg.poblacion;
    if(!Number.isInteger(po.n) || !esNum(po.n,0,200)) err.push("«poblacion.n» debe ser un entero entre 0 y 200");
    if(!["reglas","azar","ia"].includes(po.modo)) err.push("«poblacion.modo» debe ser reglas | azar | ia");
    if(!esTxt(po.semilla,120)) err.push("«poblacion.semilla» debe ser texto (máx. 120 caracteres)");
    if(po.modo !== "ia"){
      if(!Array.isArray(po.agentes_generados)) err.push("«poblacion.agentes_generados» debe ser una lista");
      else if(po.agentes_generados.length !== po.n)
        err.push(`«agentes_generados» trae ${po.agentes_generados.length} agentes pero «n» es ${po.n}`);
    }
  }
  if(!Array.isArray(cfg.variantes)) err.push("«variantes» debe ser una lista");
  else cfg.variantes.forEach((v,i)=>{
    if(!esObj(v) || !esTxt(v.nombre,200)){ err.push(`variante ${i+1}: nombre no válido`); return; }
    if(!Array.isArray(v.cambios)) err.push(`variante ${i+1}: «cambios» debe ser una lista`);
    else v.cambios.forEach((c,j)=>{
      if(!esObj(c) || typeof c.param !== "string" || !["fijar","sumar"].includes(c.op) || typeof c.val !== "number")
        err.push(`variante ${i+1}, cambio ${j+1}: param/op/val no válidos`);
    });
  });
  return err;
}
function escenarioValidado(){
  const cfg = construirConfig();
  const errores = validarEscenario(cfg);
  if(errores.length){
    toast("Escenario NO válido según schemas/scenario.schema.json: " + errores[0] +
      (errores.length>1 ? ` (y ${errores.length-1} problema${errores.length>2?'s':''} más)` : ""));
    return null;
  }
  return cfg;
}

function lanzar(){
  const cfg = escenarioValidado();
  if(!cfg) return;
  $("cfgJson").textContent = JSON.stringify(cfg,null,2);
  $("dlgCfg").classList.add("on");
}
function descargarCfg(){
  const cfg = escenarioValidado();   // se valida SIEMPRE antes de descargar
  if(!cfg) return;
  const blob = new Blob([JSON.stringify(cfg,null,2)], {type:"application/json"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob); a.download = "escenario.json"; a.click();
  URL.revokeObjectURL(a.href);
}
function cerrar(id){ $(id).classList.remove("on"); }
function toast(m){ const t=$("toast"); t.textContent=m; t.style.display="block"; clearTimeout(toast._t); toast._t=setTimeout(()=>t.style.display="none",3800); }

/* ---------- Conexión de eventos (sustituye a los onclick inline) ---------- */
function conectarEventos(){
  ["titulo","premisa","reglas","pasos","total","edadMin","edadMax","pctMuj",
   "nseMedia","eduMedia","varie","idiomaPct","corrAE","corrOC","seed","seed2"]
    .forEach(id => $(id).addEventListener("input", pintar));
  $("entorno").addEventListener("change", pintar);
  $("incNB").addEventListener("change", pintar);
  $("modoManual").addEventListener("click", ()=>setModo('manual'));
  $("modoIA").addEventListener("click", ()=>setModo('ia'));
  $("btnRellenarTodo").addEventListener("click", rellenarTodo);
  $("btnIaPremisa").addEventListener("click", iaPremisa);
  $("btnIaReglas").addEventListener("click", iaReglas);
  $("btnIaPobl").addEventListener("click", ()=>toast('La IA generaría '+poblN()+' fichas Big Five a partir de tu descripción (mock en el prototipo).'));
  document.querySelectorAll(".tabs button").forEach(b=>b.addEventListener("click", ()=>setTab(b.dataset.t)));
  document.querySelectorAll(".chipsRapidos button").forEach(b=>b.addEventListener("click", ()=>varRapida(b.dataset.var)));
  $("btnAddOrigen").addEventListener("click", addOrigen);
  $("btnAddRol").addEventListener("click", addRol);
  $("btnAddSub").addEventListener("click", addSub);
  $("btnAddVariante").addEventListener("click", ()=>addVariante());
  $("btnNuevaSemilla").addEventListener("click", nuevaSemilla);
  $("btnPrevPobl").addEventListener("click", ()=>previsualizar());
  $("btnPrevPobl2").addEventListener("click", ()=>previsualizar());
  $("btnLanzar").addEventListener("click", lanzar);
  $("btnDescargar").addEventListener("click", descargarCfg);
  $("btnCerrarCfg").addEventListener("click", ()=>cerrar('dlgCfg'));
  $("btnCerrarPrev").addEventListener("click", ()=>cerrar('dlgPrev'));
  $("dlgCfg").addEventListener("click", e=>{ if(e.target===$("dlgCfg")) cerrar('dlgCfg'); });
  $("dlgPrev").addEventListener("click", e=>{ if(e.target===$("dlgPrev")) cerrar('dlgPrev'); });
  $("chkSensibles").addEventListener("change", ()=>{
    aplicarEstadoSensibles(); renderCards(); renderDistros2(); renderOrigenes(); pintar();
    toast(sensiblesActivas()
      ? "Variables sensibles ACTIVADAS: ideología, religiosidad, salud, atractivo, origen cultural y lengua materna se exportarán tal cual."
      : "Variables sensibles desactivadas: se exportan neutras.");
  });
}

iniciar();
