/* ===========================================================================
   PsicoAI · orquestación de la escena
   ---------------------------------------------------------------------------
   Aparición de bloques y marcas al hacer scroll, barra de progreso, sección
   activa en el menú y la escalera animada de la portada. Todo se degrada a
   estático si el visitante pide movimiento reducido.
   =========================================================================== */

(function () {
  "use strict";

  const D = window.PSICO;
  const quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ── 1. aparición al entrar en pantalla ────────────────────────────────── */

  const observador = new IntersectionObserver((entradas) => {
    entradas.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add("visible");
      observador.unobserve(e.target);
    });
  }, { rootMargin: "0px 0px -12% 0px", threshold: 0.12 });

  function observar() {
    document.querySelectorAll(".aparece:not(.visible), figure.viz:not(.visible)")
      .forEach((n) => (quieto ? n.classList.add("visible") : observador.observe(n)));
  }
  observar();
  // las figuras se inyectan por JS después del primer barrido
  new MutationObserver(observar).observe(document.body, { childList: true, subtree: true });

  /* ── 2. barra de progreso y sección activa ─────────────────────────────── */

  const barra = document.getElementById("barra");
  const progreso = document.getElementById("progreso");
  const enlaces = Array.from(document.querySelectorAll(".navmini a"));
  const secciones = enlaces
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);

  let pendiente = false;
  function alScroll() {
    if (pendiente) return;
    pendiente = true;
    requestAnimationFrame(() => {
      pendiente = false;
      const y = scrollY;
      const total = document.documentElement.scrollHeight - innerHeight;
      progreso.style.width = (total > 0 ? Math.min(1, y / total) * 100 : 0) + "%";
      barra.classList.toggle("pegada", y > 20);

      let activa = -1;
      secciones.forEach((s, i) => { if (s.getBoundingClientRect().top <= innerHeight * 0.36) activa = i; });
      enlaces.forEach((a, i) => {
        if (i === activa) a.setAttribute("aria-current", "true");
        else a.removeAttribute("aria-current");
      });
    });
  }
  addEventListener("scroll", alScroll, { passive: true });
  addEventListener("resize", alScroll);
  alScroll();

  /* ── 3. la escalera de la portada ──────────────────────────────────────── */
  /*  Reproduce, en bucle, una sesión REAL: la primera del run de deepseek
      -v4-flash-0731 con la política en el system prompt — la celda que llega
      al final con cero insistencias. El texto de cada peldaño y cada protesta
      sale del diseño congelado; el juicio privado, del registro crudo.        */

  (function escaleraPortada() {
    const M = D.milgram;
    const host = document.getElementById("pe-peldanos");
    if (!host) return;

    const celda = D.consola.modelos.find((m) => m.clave === "deepseek-v4-flash-0731");
    const sesion = celda.portadores.system.sesiones[D.consola.sujetos[0]];

    document.getElementById("pe-victima").textContent = M.victima;

    const peldanos = M.niveles.map((desc, i) => {
      const n = i + 1;
      const fila = document.createElement("div");
      fila.className = "peldano" + (n === M.nivelCritico ? " critico" : "");
      fila.innerHTML =
        `<span class="num">${String(n).padStart(2, "0")}</span>` +
        `<span class="via"><i></i></span>` +
        `<span class="et"></span>`;
      fila.querySelector(".et").textContent = desc;
      host.appendChild(fila);
      if (n === M.nivelCritico) {
        const marca = document.createElement("div");
        marca.className = "linea-critica";
        marca.appendChild(document.createTextNode("primer daño irreversible"));
        host.appendChild(marca);
      }
      return fila;
    });

    const elProtesta = document.getElementById("pe-protesta");
    const elPrivado = document.getElementById("pe-privado");
    const elSello = document.getElementById("pe-sello");

    function pinta(k) {
      peldanos.forEach((p, i) => p.classList.toggle("on", i < k));
      const reg = sesion.registros[k - 1];
      if (!reg) {
        elProtesta.textContent = "«" + (M.protestas["1"] || "") + "»";
        elPrivado.textContent = "—";
        elSello.hidden = true;
        return;
      }
      const protesta = M.protestas[String(reg.nivel - 1)];
      elProtesta.textContent = protesta
        ? protesta
        : `Alerta nº ${reg.nivel}. La política del turno requiere la siguiente sanción de la escala.`;
      elPrivado.textContent = reg.justa === false ? "no es justa" : reg.justa === true ? "sí es justa" : "sin dato";
      elSello.hidden = !(reg.disonancia && reg.decision === "APLICO");
    }

    if (quieto) { pinta(sesion.registros.length); return; }

    let k = 0;
    pinta(0);
    setInterval(() => {
      k = k >= sesion.registros.length ? 0 : k + 1;
      pinta(k);
    }, 1100);
  })();

  /* ── 4. cortesía: parar los reproductores si la pestaña se oculta ──────── */

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      document.querySelectorAll(".mandos .chip").forEach((b) => {
        if (b.textContent.indexOf("Pausa") === 0 || b.textContent.indexOf("❚❚") === 0) b.click();
      });
    }
  });
})();
