"""v10 · Una sola cuenta para todos (Diego, 8 oct 2026). Correr DESPUÉS de patch_shell12.py.
La cuenta es exactamente la misma para anfitrión, proveedor, venue o planner. Lo único que cambia es la puerta por la que
llegó: decide en qué pestaña aterriza y qué invitación ve primero.
- Mis fiestas: siempre con «Mis fiestas personales» / «Las fiestas de mis clientes». Si no hay fiestas, invitación azul;
  si no es planner, en «de mis clientes» ve la invitación morada para activar su perfil de planner.
- Mi negocio: siempre con «Mis servicios» / «Mi venue» / «Event planner». Si no tiene sitio, o la pestaña no está
  activada, ve la invitación morada de esa pestaña (crear sitio o agregarla a su sitio)."""
import re
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:110]
    s = s.replace(a, b, count)


CSS = '''
/* ===== v10 · una sola cuenta ===== */
.hello .one{font-size:13px;color:var(--muted);font-weight:700}
.subtabs .new{font-size:10px;background:var(--hqv-lima);color:#1A2600;border-radius:99px;padding:1px 7px;margin-left:4px}
.inv.mini{max-width:none;border-radius:32px!important}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# ---------- saludo: recordatorio de que es una sola cuenta
rep('''<span class="hint">Nivel ${lvl==="n2"?"Fiestero":"Invitado"}</span></span></div></div>''',
    '''<span class="hint">Nivel ${lvl==="n2"?"Fiestero":"Invitado"}</span></span><span class="one">Una sola cuenta para tus fiestas y tu negocio.</span></div></div>''')

# ---------- drawAcct: las dos pestañas siempre con su estructura completa
rep('''if(U.tab==="fiestas"){if(!U.sides.fiestas&&!(U.plannerJobs||[]).length)return drawInvite(p,"fiestas");return drawFiestas(p);}''',
    '''if(U.tab==="fiestas")return drawFiestas(p);''')
rep('''if(U.tab==="negocio")return U.sides.negocio?drawNegocio(p):drawInvite(p,"negocio");''',
    '''if(U.tab==="negocio")return drawNegocio(p);''')

# ---------- Mis fiestas: sub-pestañas siempre
rep('''U.sub=U.sub||"mias";if(!isPl)U.sub="mias";''', '''U.sub=U.sub||"mias";''')
rep('''const tabs=isPl?`<div class="subtabs" role="tablist">''', '''const tabs=true?`<div class="subtabs" role="tablist">''')
rep('''📋 Las fiestas de mis clientes</button></div>`:"";''',
    '''📋 Las fiestas de mis clientes${isPl?"":'<span class="new">Activar</span>'}</button></div>`:"";''')
rep('''`).join("")||'<div class="empty"><span class="hint">Cuando aceptes a un cliente en Mi negocio › Event planner, su fiesta aparece aquí.</span></div>'}</div></section>`;''',
    '''`).join("")||(isPl?'<div class="empty"><span class="hint">Cuando aceptes a un cliente en Mi negocio › Event planner, su fiesta aparece aquí.</span></div>':plInvHtml())}</div></section>`;
  const pa=$("plAct");if(pa)pa.onclick=()=>actVertical("planner");''')
rep('''${isPl?"Mis fiestas personales":"Mis fiestas"}</h2>''', '''Mis fiestas personales</h2>''')

# ---------- Mi negocio: tres pestañas siempre; invitación cuando no hay sitio o la pestaña no está activa
rep('''function negState(){U.neg=U.neg||{vt:null,sol:[],post:[],agenda:[],removed:0,sel:null};const t=(U.site&&U.site.tipos)||["services"];const ok=VTS.filter(v=>t.includes(v[0]));if(!ok.some(v=>v[1]===U.neg.vt))U.neg.vt=ok[0][1];return ok;}''',
    '''function negState(){U.neg=U.neg||{vt:null,sol:[],post:[],agenda:[],removed:0,sel:null};const t=(U.site&&U.site.tipos)||[];const ok=VTS.filter(v=>t.includes(v[0]));if(!VTS.some(v=>v[1]===U.neg.vt))U.neg.vt=(ok[0]||VTS[0])[1];return ok;}
function vtOn(id){const t=(U.site&&U.site.tipos)||[];return !!U.sides.negocio&&VTS.some(v=>v[1]===id&&t.includes(v[0]));}
function negTabs(vt){return`<div class="subtabs nb-sub" role="tablist" style="margin-top:14px">${VTS.map(([,id,t])=>`<button type="button" role="tab" data-nv="${id}" aria-selected="${vt===id}">${t}${vtOn(id)?"":'<span class="new">Activar</span>'}</button>`).join("")}</div>`;}
const VT_INV={svc:["c_01","¿Ofreces servicios para fiestas o eventos?","Comida, música, decoración, foto, mobiliario… Publica tus servicios con precios y recibe eventos que encajan contigo, directo en tu WhatsApp.",["Sitio web gratis para siempre","Precios por persona, por pieza o por hora","Solicitudes de clientes reales cerca de ti"]],
 venue:["c_03","¿Tienes un venue?","Salón, jardín, terraza o casa para eventos. Publica capacidad, horarios, precios y políticas, y recibe solicitudes de fechas.",["Tu venue con fotos, horarios y precios","Políticas claras: qué incluye y qué no","Agenda de fechas cerradas"]],
 planner:["c_05","¿Eres event planner?","Crea tu perfil de planner y deja que los anfitriones te elijan para organizar su fiesta completa.",["Tu récord, insignias y redes en un perfil","Clientes que ya pre-cotizaron su fiesta","Coordina a sus proveedores desde tu cuenta"]]};
function actVertical(vt){track("invitacion_cruzada",{a:"proveedor",vt});if(U.site){U.addVt=vt;openJourney("negocio",true);}else{show("home");goSide("pv");}}
function plInvHtml(){const v=VT_INV.planner;return`<div class="inv nb mini"><img src="img/${v[0]}.webp" alt="" style="width:90px"><h2>${v[1]}</h2><span style="font-size:16px">${v[2]} Las fiestas que organices para tus clientes aparecen aquí.</span><button class="btn cta" type="button" id="plAct">${U.site?"Agregar mi perfil de planner →":"Crear mi sitio web gratis →"}</button><span style="font-size:13px;font-weight:700;opacity:.95">Usamos tu misma cuenta: no tienes que volver a registrarte.</span></div>`;}
function negHead(){const s=U.site||{},pro=U.plan==="pro";return`<div class="box" style="background:var(--prov);color:#fff"><div class="fhead" style="margin:0"><h2>${em("rocket")} ${esc(s.negocio||"Mi negocio")}</h2><span class="row" style="gap:6px">${U.founder?`<span class="tag2">⭐ Fundador #${U.founder}</span>`:""}<span class="tag2 ${pro?"ok":""}">Plan ${pro?"Pro":"Gratis"}</span></span></div>
   <span style="background:rgba(255,255,255,.18);border-radius:99px;padding:4px 12px;font-weight:800;word-break:break-all;justify-self:start">${esc(s.url||"hayquevernos.com/minegocio")}</span>
   <div class="row" style="gap:8px;flex-wrap:wrap"><button class="btn ghost sm" type="button" id="sEdit">✏️ Editar mi sitio</button></div></div>`;}
function drawNegOff(p){const N=U.neg,vt=N.vt,v=VT_INV[vt],has=!!(U.sides.negocio&&U.site);
 p.innerHTML=`${has?negHead():""}${negTabs(vt)}<div class="inv nb mini"><img src="img/${v[0]}.webp" alt="" style="width:100px"><h2>${v[1]}</h2><span style="font-size:16px">${v[2]}</span><ul>${v[3].map(x=>`<li>${x}</li>`).join("")}</ul>
  <button class="btn cta" type="button" id="act">${has?"Agregar a mi sitio →":"Crear mi sitio web gratis →"}</button><span style="font-size:13px;font-weight:700;opacity:.95">Usamos tu misma cuenta: no tienes que volver a registrarte.</span></div>`;
 const e=$("sEdit");if(e)e.onclick=()=>openJourney("negocio",true);
 $("act").onclick=()=>actVertical(vt);
 p.querySelectorAll("[data-nv]").forEach(b=>b.onclick=()=>{N.vt=b.dataset.nv;N.sel=null;drawAcct();});}''')
rep('''function drawNegocio(p){const s=U.site||{}''', '''function drawNegocio(p){negState();if(!vtOn(U.neg.vt))return drawNegOff(p);const s=U.site||{}''')
rep('''${ok.length>1?`<div class="subtabs nb-sub" role="tablist" style="margin-top:14px">${ok.map(([,id,t])=>`<button type="button" role="tab" data-nv="${id}" aria-selected="${vt===id}">${t}</button>`).join("")}</div>`:""}''',
    '''${negTabs(vt)}''')

# ---------- versión
s = s.replace('PROTOTIPO v8', 'PROTOTIPO v10')

P.write_text(s)
print('shell13 ok', len(s))

# ---------- cualquier puerta reutiliza la misma cuenta si ya hay sesión
s = P.read_text()
a = 'const q=new URLSearchParams({shell:"1"});if(edit&&U.account){'
assert a in s
s = s.replace(a, 'const q=new URLSearchParams({shell:"1"});if(U.account==="cuenta"||(edit&&U.account)){', 1)
P.write_text(s)
print('misma cuenta en ambas puertas ok')
