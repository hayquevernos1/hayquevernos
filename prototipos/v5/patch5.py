"""Parches v5 sobre los journeys v4: marca 2026, cuenta al final, datos conectados al shell."""
import re
from pathlib import Path
D = Path('/home/claude/hqv/v5')

def rep(s, a, b, count=1):
    assert a in s, 'NO ENCONTRADO: ' + a[:90]
    return s.replace(a, b, count)

FONT_OLD = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Figtree:wght@400;500;600;700&display=swap">'
FONT_NEW = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap">'

def brand(s):
    s = rep(s, FONT_OLD, FONT_NEW)
    i = s.index('</style>') + len('</style>')
    s = s[:i] + '\n<link rel="stylesheet" href="marca.css">' + s[i:]
    return s

# ------------------------------------------------------------ PROVEEDOR
r = (D / 'reg_src.html').read_text()
r = brand(r)
r = rep(r, '<script src="catalogo.js"></script>', '<script src="config.js"></script>\n<script src="catalogo.js"></script>')
# Contacto de la persona en el primer paso (nombre, WhatsApp, correo): con esto se crea la cuenta al publicar
r = rep(r, ''' <div class="row"><div class="field"><label class="lbl" for="f-wa">📱 WhatsApp</label>''',
 ''' <div class="sub-box" style="display:grid;gap:10px;padding:14px"><span class="lbl">🙋 Tus datos de contacto</span><span class="hint">Con estos datos creamos tu cuenta al publicar. Tus clientes solo ven el WhatsApp de tu negocio.</span>
 <div class="row"><div class="field"><label class="lbl" for="f-owner">Tu nombre</label><input type="text" id="f-owner" autocomplete="name" class="${MISS(filled(b.owner||""))}" value="${esc(b.owner||"")}" placeholder="Quien atiende a los clientes"></div>
 <div class="field"><label class="lbl" for="f-email">Correo</label><input type="email" id="f-email" autocomplete="email" class="${MISS(EMAIL_OK(S.account.email))}" value="${esc(S.account.email)}" placeholder="tunegocio@gmail.com"></div></div></div>
 <div class="row"><div class="field"><label class="lbl" for="f-wa">📱 WhatsApp</label>''')
r = rep(r, ''' [["f-name","name"],["f-wa","whatsapp"],["f-about","about"],["f-since","since"]].forEach(([i,k])=>{$(i).oninput=$(i).onchange=e=>{b[k]=e.target.value;changed();};});''',
 ''' [["f-name","name"],["f-wa","whatsapp"],["f-about","about"],["f-since","since"],["f-owner","owner"]].forEach(([i,k])=>{$(i).oninput=$(i).onchange=e=>{b[k]=e.target.value;changed();};});
 $("f-email").oninput=e=>{S.account.email=e.target.value.trim();changed();};''')
r = rep(r, '''if(id==="biz"){const b=S.biz;if(!filled(b.name))m.push("Nombre");''',
 '''if(id==="biz"){const b=S.biz;if(!filled(b.name))m.push("Nombre");if(!filled(b.owner||""))m.push("Tu nombre");if(!EMAIL_OK(S.account.email))m.push("Tu correo");''')
r = rep(r, 'function missing(id){const m=[];', 'const EMAIL_OK=e=>/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(e||"");\nfunction missing(id){const m=[];')
r = rep(r, ' account:{email:""}};}', ' account:{email:"lupita@ejemplo.com"}};}')  # ejemplo
r = rep(r, 'biz:{name:"Lupita Dulces y Antojos",', 'biz:{owner:"Lupita Ramírez",name:"Lupita Dulces y Antojos",')
# Publicar = crear la cuenta en el mismo clic (transparente)
i = r.index(' if(id==="publish"){')
j = r.index('  bindNav();}}', i) + len('  bindNav();}}')
r = r[:i] + ''' if(id==="publish"){const b=S.biz,faltan=missing("biz");
  $("stepBody").innerHTML=`<div class="panel"><h2>¡A publicar! 🚀</h2><p class="sub">Tu sitio y tu cuenta de ¡Hay que vernos! se crean juntos, con un solo clic. No tienes que llenar nada más.</p>
   <div class="sub-box" style="display:grid;gap:6px;padding:14px"><span>🙋 <b>${esc(b.owner||"—")}</b></span><span>📱 ${esc(b.whatsapp||"—")}</span><span>✉️ ${esc(S.account.email||"—")}</span><span>🔗 hayquevernos.com/${esc(slug(b.name))}</span></div>
   ${faltan.length?`<p class="err">Antes de publicar completa en el paso Mi negocio: ${esc(faltan.join(", "))}.</p>`:''}
   <label class="chk"><input type="checkbox" id="a-mk" ${S.account.mk?"checked":""}><span>Quiero recibir novedades, cursos y promociones de ¡Hay que vernos! <span class="opt">(opcional)</span></span></label>
   <button class="btn big" type="button" id="pubBtn" ${faltan.length?"disabled":""}>Publicar mi sitio gratis 🎉</button>
   <p class="hint" style="margin:0">Al publicar se crea tu cuenta de ¡Hay que vernos! con los datos que ya nos diste y aceptas los <a href="#" onclick="return false">Términos para proveedores</a> y el <a href="#" onclick="return false">Aviso de privacidad</a>. Te avisaremos por WhatsApp cuando un anfitrión busque lo que ofreces.</p>
   ${navHtml(true)}</div>`;
  $("a-mk").onchange=e=>{S.account.mk=e.target.checked;};
  $("pubBtn").onclick=()=>{if(missing("biz").length)return;publish();};
  bindNav();}}''' + r[j:]
r = rep(r, '''function publish(){try{parent.postMessage({hqv:"negocio-publicado",nombre:S.biz.name},"*");}catch(_){}''',
 '''function publish(){const datos={nombre:S.biz.owner||"",negocio:S.biz.name,wa:S.biz.whatsapp.replace(/\\D/g,"").slice(-10),email:S.account.email,marketing:!!S.account.mk,
  tipos:Object.keys(S.types).filter(k=>S.types[k]),servicios:S.services.map(s=>({cat:s.cat,subs:s.subs.map(x=>({n:x.n,precio:x.price}))})).filter(s=>s.cat),
  zona:(S.biz.addr&&(S.biz.addr.muni||S.biz.addr.state))||"",url:"hayquevernos.com/"+slug(S.biz.name),completo:completeness()};
 hqvTrack("sitio_publicado",{tipos:datos.tipos,completo:datos.completo});
 if(parent!==window){try{parent.postMessage({hqv:"negocio-publicado",datos},"*");}catch(_){}return;}''')
# Atajo pagado: "Háganmelo ustedes"
r = rep(r, '''<button class="cta off" type="button" id="goProv">Empezar mi sitio gratis <span aria-hidden="true">→</span></button>''',
 '''<button class="cta off" type="button" id="goProv">Empezar mi sitio gratis <span aria-hidden="true">→</span></button>
    <button class="link" type="button" id="goConc" style="justify-self:center">⏱️ ¿Sin tiempo? <b>Lo armamos por ti</b></button>''')
r = rep(r, 'drawTypes();preview();loadCP();', '''$("goConc").onclick=()=>{hqvTrack("concierge_click",{lado:"proveedor"});if(parent!==window)parent.postMessage({hqv:"concierge",lado:"proveedor"},"*");};
if(ACCT){S.biz.owner=S.biz.owner||ACCT_NAME;S.account.email=S.account.email||(QS.get("email")||"");}
drawTypes();preview();loadCP();hqvTrack("proveedor_inicio");''')
(D / 'reg5.html').write_text(r)

# ------------------------------------------------------------ ANFITRIÓN (cotizador)
c = (D / 'cot_src.html').read_text()
c = brand(c)
c = rep(c, '<script src="catalogo.js"></script>', '<script src="config.js"></script>\n<script src="catalogo.js"></script>') if '<script src="catalogo.js"></script>' in c else c
# Inicio: solo el nombre (crea la cuenta invitada) + atajo "Organízamelo"
c = rep(c, '''<button class="btn big" type="button" id="start">Calcular mi fiesta →</button></div>`;$("start").onclick=()=>go("fiesta");return;}''',
 '''<div class="field" style="width:min(340px,100%);text-align:left"><label class="lbl" for="nm0">¿Cómo te llamas? <span class="opt">(opcional)</span></label><input type="text" id="nm0" autocomplete="given-name" maxlength="40" value="${esc(S.name)}" placeholder="Así personalizo tu fiesta"></div>
  <button class="btn big" type="button" id="start">Calcular mi fiesta →</button>
  <button class="link-btn" type="button" id="goConc">⏱️ ¿Sin tiempo? Organízamelo con un experto</button></div>`;
  $("start").onclick=()=>{S.name=$("nm0").value.trim();hqvTrack("cotizador_inicio",{con_nombre:!!S.name});try{if(parent!==window)parent.postMessage({hqv:"invitado",nombre:S.name},"*");}catch(_){}go("fiesta");};
  $("nm0").onkeydown=e=>{if(e.key==="Enter")$("start").click();};
  $("goConc").onclick=()=>{hqvTrack("concierge_click",{lado:"anfitrion"});if(parent!==window)parent.postMessage({hqv:"concierge",lado:"anfitrion"},"*");};return;}''')
c = rep(c, 'let screen="intro"', 'if(ACCT&&ACCT_NAME)S.name=ACCT_NAME;\nlet screen="intro"')
c = rep(c, '"¡Hola! Soy <b>Vernie</b> 🪩 Cuéntame de tu fiesta."', '`¡Hola${S.name?", <b>"+esc(S.name.split(" ")[0])+"</b>":""}! Soy <b>Vernie</b> 🪩 Cuéntame de tu fiesta.`')
# Sin pregunta de planner aquí: se decide después de ver el cálculo, en la cuenta
i = c.index('  <div class="field"><span class="lbl">📋 ¿Quieres un event planner?</span>')
j = c.index('  ${navHtml("detalles","Ver mi fiesta 🎉")}')
c = c[:i] + c[j:]
c = rep(c, '''  if(S.wantPlanner===null)m.push("¿Quieres un event planner?");if(S.wantPlanner&&!S.planners.length)m.push("Elige al menos un planner");}''', '  }')
c = rep(c, 'S.wantPlanner=b.dataset.v==="1"', 'S.wantPlanner=b.dataset.v==="1"')  # sin cambio (código muerto inofensivo)
c = rep(c, '${navHtml("presupuesto")}', '${navHtml("presupuesto",needInvoice()?"Siguiente →":"Ver mi fiesta 🎉")}')
c = rep(c, 'bindNav("presupuesto","servicios","detalles")', 'bindNav("presupuesto","servicios",needInvoice()?"detalles":"result")')
# Resultado: "Aquí está tu cálculo" y pasa a la cuenta
c = rep(c, '''   <b style="font-family:var(--f-display);font-size:19px;font-weight:600">¿Te late? Te conectamos con los mejores proveedores para tu fiesta 🤝</b>
   <button class="btn big" type="button" id="send">Conectar con proveedores →</button>''',
 '''   <b style="font-family:var(--f-display);font-size:21px;font-weight:900">¡Aquí está tu cálculo${S.name?", "+esc(S.name.split(" ")[0]):""}! 🎉</b>
   <span style="color:var(--muted);max-width:46ch">Ya lo guardé en tu cuenta. Ahí ves a los proveedores interesados, eliges si quieres un event planner y organizas todo.</span>
   <button class="btn big" type="button" id="send">Ver mi fiesta →</button>''')
c = rep(c, '''  $("send").onclick=()=>{if(ACCT){S.name=S.name||ACCT_NAME||"tú";S.wa=ACCT_WA;go("sent");try{parent.postMessage({hqv:"fiesta-enviada",occ:S.occ},"*");}catch(_){}}else go("signup");};''',
 '''  hqvTrack("calculo_visto",{occ:S.occ,invitados:S.guests,total:Math.round(t)});
  $("send").onclick=()=>{const fiesta={occ:S.occ,kind:S.kind,guests:S.guests,date:S.date,start:S.start,end:S.end,hours:hours(),total:Math.round(t),pp:Math.round(t/S.guests),
    zona:S.hasPlace?((S.place.addr&&(S.place.addr.muni||S.place.addr.state))||""):(S.need.all?S.need.state:S.need.munis.join(", ")),venue:S.hasPlace===false,
    rows:rs.map(r=>({k:r.k,e:r.e,label:r.label,subs:r.subs||[],amt:Math.round(r.amt)})),early:earlyPct()};
   hqvTrack("ver_mi_fiesta",{occ:S.occ});
   if(parent!==window){try{parent.postMessage({hqv:"fiesta-lista",fiesta,nombre:S.name},"*");}catch(_){}}
   else alert("En el sitio real aquí entras a tu cuenta, en Mis fiestas.");};''')
(D / 'cot5.html').write_text(c)
print('ok')
