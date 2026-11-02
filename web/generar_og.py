#!/usr/bin/env python3
"""Dibuja las tarjetas para compartir (og:image, 1200×630) de la web.

  python3 web/generar_og.py     # reescribe web/og.png, og-social.png y og-personalidad.png

Las tarjetas NO llevan cifras a propósito: la anterior decía «19 mediciones de
nueve laboratorios» con el banco en 39 y trece, y nada la vigilaba porque una
imagen no pasa por `generar_datos.py`. Un titular sin denominadores no caduca
con cada alta.

Se dibujan en HTML con las fuentes del sistema que usa el sitio y se
fotografían con Chrome sin cabeza (el mismo que usa `smoke.mjs`); no hace falta
ninguna dependencia. No forma parte del --check: es un artefacto de diseño que
se regenera a mano cuando cambia el texto de una tarjeta.
"""

from __future__ import annotations

import math
import os
import pathlib
import subprocess
import tempfile

WEB = pathlib.Path(__file__).resolve().parent

CHROME = os.environ.get("CHROME") or next(
    (c for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                 "/usr/bin/google-chrome", "/usr/bin/chromium") if pathlib.Path(c).exists()), None)

FUENTES = WEB / "fonts"
BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:"BSD";src:url("%(fuentes)s/big-shoulders-display.woff2") format("woff2");font-weight:100 900}
@font-face{font-family:"IT";src:url("%(fuentes)s/inter-tight.woff2") format("woff2");font-weight:100 900}
@font-face{font-family:"JBM";src:url("%(fuentes)s/jetbrains-mono.woff2") format("woff2");font-weight:100 800}
*{margin:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden}
body{background:#07070A;color:#FFFFFF;font-family:"IT",system-ui,sans-serif;padding:70px 80px;position:relative;
  background-image:radial-gradient(60%% 70%% at 85%% 10%%,rgba(180,108,255,.22),transparent 70%%),
  radial-gradient(50%% 60%% at 10%% 100%%,rgba(74,242,255,.14),transparent 70%%)}
.ceja{font:600 19px/1 "JBM",monospace;letter-spacing:.24em;color:#9A97A6;text-transform:uppercase}
h1{font:900 104px/.92 "BSD",Impact,sans-serif;text-transform:uppercase;margin-top:26px;max-width:%(ancho)spx}
h1 em{font-style:normal;background:linear-gradient(90deg,#4AF2FF 0%%,#7B3DFF 30%%,#FF3D8A 55%%,#FF8A1F 80%%,#FFD36E 100%%);
  -webkit-background-clip:text;background-clip:text;color:transparent}
p{font-size:28px;line-height:1.36;color:#C9C6D4;margin-top:26px;max-width:%(ancho_p)spx}
.firma{position:absolute;left:80px;bottom:54px;display:flex;align-items:center;gap:14px;
  font:900 34px/1 "BSD",sans-serif;letter-spacing:.04em}
.firma i{width:22px;height:22px;border-radius:3px;background:linear-gradient(180deg,#FF8A1F 0 25%%,#FF3D8A 25%% 50%%,#B46CFF 50%% 75%%,#4AF2FF 75%% 100%%)}
.firma small{font:500 20px/1 "JBM",monospace;color:#9A97A6;letter-spacing:0;margin-left:12px}
.motivo{position:absolute;right:80px;bottom:44px}
</style></head><body>%(cuerpo)s</body></html>"""

FIRMA = '<div class="firma"><i></i>BENCHAI<small>benchai.tech</small></div>'
# el ISS de Verloop: de cian a naranja
ESCALA = ["#4AF2FF", "#5FC8FF", "#7B3DFF", "#9A55FF", "#B46CFF", "#D454C4", "#FF3D8A", "#FF5C63", "#FF7A3D", "#FF8A1F"]


def barras() -> str:
    r = "".join(f'<rect x="{i * 31}" y="{120 - 12 * (i + 1)}" width="24" height="{12 * (i + 1)}" rx="2" fill="{c}"/>'
                for i, c in enumerate(ESCALA))
    return f'<svg class="motivo" width="310" height="122" viewBox="0 0 310 122">{r}</svg>'


def hexagono() -> str:
    cx, cy, R = 150, 150, 120
    def pol(radios):
        return " ".join(f"{cx + R * r * math.sin(i * math.pi / 3):.1f},{cy - R * r * math.cos(i * math.pi / 3):.1f}"
                        for i, r in enumerate(radios))
    anillos = "".join(f'<polygon points="{pol([k] * 6)}" fill="none" stroke="#2A2833" stroke-width="2"/>' for k in (.33, .66, 1))
    media = f'<polygon points="{pol([.6] * 6)}" fill="none" stroke="#9A97A6" stroke-width="2.5" stroke-dasharray="7 6"/>'
    perfil = f'<polygon points="{pol([.82, .48, .7, .9, .4, .78])}" fill="rgba(201,168,255,.22)" stroke="#C9A8FF" stroke-width="4"/>'
    return f'<svg class="motivo" style="bottom:50px" width="300" height="300" viewBox="0 0 300 300">{anillos}{media}{perfil}</svg>'


TARJETAS = {
    "og.png": dict(ancho=900, ancho_p=640, cuerpo=(
        '<p class="ceja">BenchAI</p>'
        '<h1>Lo que una IA <em>hace</em> bajo presión, medido</h1>'
        '<p>Dos benchmarks de conducta: SocialBench y el test de personalidad.</p>'
        + FIRMA + barras())),
    "og-social.png": dict(ancho=980, ancho_p=640, cuerpo=(
        '<p class="ceja">SocialBench</p>'
        '<h1>La silla de Milgram, <em>con máquinas</em></h1>'
        '<p>Los experimentos clásicos de la psicología social, disfrazados. Quién cede al grupo, quién obedece y quién abusa del poder.</p>'
        + FIRMA + barras())),
    "og-personalidad.png": dict(ancho=760, ancho_p=640, cuerpo=(
        '<p class="ceja">Test de personalidad</p>'
        '<h1>¿Qué personalidad tiene <em>cada IA?</em></h1>'
        '<p>Los cinco grandes rasgos y la honestidad, medidos por lo que cada modelo elige, no por lo que dice de sí mismo.</p>'
        + FIRMA + hexagono())),
}


def main() -> int:
    if not CHROME:
        raise SystemExit("[generar_og] no encuentro Chrome (define CHROME=)")
    with tempfile.TemporaryDirectory() as tmp:
        for nombre, t in TARJETAS.items():
            html = pathlib.Path(tmp) / (nombre + ".html")
            html.write_text(BASE % dict(t, fuentes=FUENTES.as_uri()), encoding="utf-8")
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=1", "--window-size=1200,630",
                            f"--screenshot={WEB / nombre}", html.as_uri()],
                           check=True, capture_output=True, timeout=60)
            print(f"[generar_og] {nombre}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
