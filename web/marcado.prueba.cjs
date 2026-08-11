/* ===========================================================================
   Contrato de `web/js/marcado.js`, ejecutado de verdad (node, sin depender de
   nada más). La puerta estática (`spike/test_xss_estatico.py`, apartado e)
   comprueba la FORMA del módulo; esto comprueba su CONDUCTA — que un dato
   hostil se escapa, que no puede salirse de un atributo y que una cadena
   suelta no llega a innerHTML. Corre en `verificar.sh` y en CI.

     node web/marcado.prueba.cjs
   =========================================================================== */
const fs = require("fs");
const path = require("path");
const global_ = {};
const modulo = path.join(__dirname, "js", "marcado.js");
new Function("window", fs.readFileSync(modulo, "utf8"))(global_);
const { mk, une, pintar, escapar } = global_.MARCADO;

let fallos = 0;
const comp = (obtenido, esperado, que) => {
  const ok = obtenido === esperado;
  if (!ok) fallos++;
  console.log(`${ok ? "  ok  " : " FAIL "}${que}` +
    (ok ? "" : `\n        esperaba: ${esperado}\n        obtenido: ${obtenido}`));
};

const nodo = { innerHTML: null };
const html = (m) => { pintar(nodo, m); return nodo.innerHTML; };

// 1 · los literales del código pasan con su marcado
comp(html(mk`Ceden <b>18 de 19</b>.`), "Ceden <b>18 de 19</b>.",
  "el marcado escrito en el código se respeta");

// 2 · lo interpolado se escapa SIEMPRE, sin pedirlo
const hostil = '<img src=x onerror="alert(1)">';
comp(html(mk`Título: ${hostil}`),
  "Título: &lt;img src=x onerror=&quot;alert(1)&quot;&gt;",
  "un dato con etiqueta se escapa entero");

// 3 · y también dentro de un atributo (el caso de REPO(dato))
comp(html(mk`<a href="../${'x" onmouseover="alert(1)'}">r</a>`),
  '<a href="../x&quot; onmouseover=&quot;alert(1)">r</a>',
  "un dato no puede salirse de un atributo");

// 4 · composición: un marcado dentro de otro NO se re-escapa
const trozo = mk`<b>18 de 19</b>`;
comp(html(mk`Ceden ${trozo}.`), "Ceden <b>18 de 19</b>.",
  "un marcado interpolado en otro compone");

// 5 · une() concatena sin separador y admite "" como rama vacía
comp(html(une(mk`<i>a</i>`, "", mk`<b>${"<b>"}</b>`)),
  "<i>a</i><b>&lt;b&gt;</b>", "une compone y escapa las ramas sueltas");

// 6 · una cadena suelta NO puede llegar a innerHTML
try {
  pintar(nodo, "<b>confía en mí</b>");
  console.log(" FAIL una cadena suelta debería ser rechazada");
  fallos++;
} catch (e) {
  comp(e instanceof TypeError, true, "una cadena suelta se rechaza");
}

// 7 · el escapador cubre los cinco caracteres
comp(escapar(`&<>"'`), "&amp;&lt;&gt;&quot;&#39;", "escapa los cinco");

console.log(fallos ? `\n${fallos} FALLOS` : "\nMARCADO: todo OK");
process.exit(fallos ? 1 : 0);
