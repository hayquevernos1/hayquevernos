"""v8 · Vuelta 2 · Al publicar desde la cuenta: ventana de «¡Tu sitio ya está en línea!» con link, imagen para redes (QR) y acceso a Mi negocio."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()
def rep(a, b):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:100]
    s = s.replace(a, b, 1)
rep('<script src="config.js"></script>', '<script src="config.js"></script>\n<script src="qr.js"></script>')
rep('toast("🎉 Tu sitio está publicado y tu cuenta quedó creada");return;}', 'pubModal(x);return;}')
rep('\nfunction drawAcct(){', r'''
function pubModal(x){const m=$("modal"),url=x.url||"hayquevernos.com/tu-negocio";
 m.innerHTML=`<div class="sheet"><img src="img/ball.webp" alt="" style="width:80px"><h2>¡${esc(x.negocio||"Tu negocio")} ya está en línea! 🎉</h2>
  <span>Pon este link en la bio de tus redes y en tu WhatsApp para empezar a vender más.</span>
  <div class="soft" style="display:flex;gap:8px;align-items:center;justify-content:space-between;flex-wrap:wrap"><b>${esc(url)}</b><button class="pill sm" type="button" id="pmCopy">Copiar link</button></div>
  <div class="emb"><img src="img/b_fundador.webp" alt=""><span class="hint">Eres <b>proveedor fundador #${U.founder||38}</b>: tu insignia es para siempre.</span></div>
  <button class="btn cta" type="button" id="pmImg">⬇️ Descargar imagen para redes (con QR)</button>
  <div class="yn2"><button class="btn ghost" type="button" id="pmSite">👀 Ver mi sitio</button><button class="btn" type="button" id="pmGo">Ir a Mi negocio →</button></div></div>`;
 m.hidden=false;
 $("pmCopy").onclick=async()=>{try{await navigator.clipboard.writeText("https://"+url);}catch(_){}toast("🔗 Link copiado");};
 $("pmImg").onclick=async()=>{const u=await hqvShareImage({logo:"img/logo.webp",kicker:"Encuéntranos en ¡Hay que vernos!",title:x.negocio||"Mi negocio",sub:x.about||"",url,foot:"Escanea, conoce mis servicios y cotiza por WhatsApp"});hqvDownload(u,"sitio.png");track("imagen_sitio_descargada");};
 $("pmSite").onclick=()=>{m.hidden=true;toast("👀 En el sitio real aquí se abre tu página pública.");};
 $("pmGo").onclick=()=>{m.hidden=true;toast("🎉 Tu sitio está publicado y tu cuenta quedó creada");};}
function drawAcct(){''')
P.write_text(s)
print('shell11 ok')
