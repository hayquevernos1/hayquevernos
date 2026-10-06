"""Genera public/cotizador/index.html a partir de src/cotizador/ (sin dependencias).
Uso: python3 tools/build_cotizador.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "cotizador"

HEAD = """<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Pre-cotiza tu fiesta gratis y conoce el precio por persona. Versión beta con precios de ejemplo.">
<meta property="og:title" content="Pre-cotiza tu fiesta gratis · ¡Hay que vernos!">
<meta property="og:description" content="Calcula el costo de tu fiesta por persona en minutos. Beta: abre el 1 de noviembre.">
<meta property="og:image" content="https://hayquevernos.com/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/img/favicon.png">
<meta name="theme-color" content="#7B2CBF">
"""

def main():
    html = (SRC / "cotizador.src.html").read_text(encoding="utf-8")
    addr = (SRC / "addr.js").read_text(encoding="utf-8")
    # En el sitio, el catálogo de códigos postales se descarga aparte (/data/cp.bin, gzip) para que la página cargue rápido.
    old = 'const bin=Uint8Array.from(atob(CPB64),c=>c.charCodeAt(0));'
    assert old in addr
    addr = addr.replace(old, 'const bin=new Uint8Array(await (await fetch("/data/cp.bin")).arrayBuffer());')
    addr = addr.replace('const CPB64="__CPB64__";\n', "")
    mx = (SRC / "mx.json").read_text(encoding="utf-8").strip()
    logo = "/img/logo.webp"
    ball = "/img/ball.webp"
    for k, v in {"__ADDR__": addr, "__MX__": mx, "__LOGO__": logo, "__BALL__": ball}.items():
        assert html.count(k) == 1, k
        html = html.replace(k, v)
    old_banner = '<b>PROTOTIPO</b><span>Precios y proveedores de ejemplo. Nada se guarda ni se envía.</span>'
    assert old_banner in html
    html = html.replace(old_banner, '<b>BETA</b><span>Demostración con precios y proveedores de ejemplo. Nada se guarda ni se envía. Abre el 1 de noviembre. <a href="/">← Inicio</a></span>')
    html = HEAD + html.replace("</title>", "</title>", 1)
    out = ROOT / "public" / "cotizador" / "index.html"
    out.write_text(html, encoding="utf-8")
    print("OK", out, len(html) // 1024, "KB")

if __name__ == "__main__":
    main()
