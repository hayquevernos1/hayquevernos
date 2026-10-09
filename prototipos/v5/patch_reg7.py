"""v8 · Vuelta 2 · Registro del proveedor (comentarios de Diego en Miro, bloque 3). reg6.html → reg7.html
P01 inicio limpio (logo + ¿qué ofreces?) · P02 redes con «Otro», ¿recibes clientes en tu negocio?, banner y emblema de fundador
P03 varias formas de cobro en la misma ficha + imagen de promoción para redes
P04 venue: redes prellenadas, «Otro» tipo y amenidades repetibles, horario por día, horario y precios juntos,
    servicios del venue por categoría → subcategoría (incluido / en parte / con costo / no incluido) + ¿puede sustituirlo?,
    anticipo número + %/$, cancelación (archivo, link o texto), devolución del depósito en garantía
P05 planner: redes prellenadas, récord e insignias, sugerencias dentro de la bio, varias tarifas con unidad, anticipo, ¿negociable?
P07/P08 imagen con QR para redes · sitio público con pestañas por vertical, insignias y promedio de estrellas."""
import re
from pathlib import Path
SRC = Path('/home/claude/hqv/v5/reg6.html')
DST = Path('/home/claude/hqv/v5/reg7.html')
s = SRC.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:120]
    s = s.replace(a, b, count)


def func(name, new):
    global s
    m = re.search(r'\nfunction ' + re.escape(name) + r'\(', s)
    assert m, 'NO HAY FUNCIÓN ' + name
    a = m.start() + 1
    n = re.search(r'\n(function |let |const |async function |/\*|//|document\.|\$\()', s[a + 10:])
    b = a + 10 + n.start() + 1
    s = s[:a] + new.strip('\n') + '\n' + s[b:]


CSS = r'''
/* ===== v8 · vuelta 2 ===== */
:root{--cta:#0E8F45;--cta-d:#0B7639}
.btn.cta,.cta-g{background:var(--cta)!important;color:#fff!important}
#home .home-top h1,#home .home-top .lead,#home .home-top .ball,#home .perks,#home .soon,#goConc{display:none!important}
#home .home-top{justify-content:center;text-align:center}#home .home-top>div{justify-items:center}#home .home-top .logo{margin:0 auto;width:min(360px,70vw);height:auto}
#home .pick-card h2{text-align:center}
#goProv{background:var(--cta);color:#fff}
.links{display:grid;gap:8px}.links .lk{display:grid;grid-template-columns:140px 1fr auto;gap:8px;align-items:center}
@media(max-width:560px){.links .lk{grid-template-columns:1fr auto}.links .lk select{grid-column:1/-1}}
.sgroup{background:var(--paper,#F6F3FF);border-radius:18px;padding:12px;display:grid;gap:8px}
.sgroup .urow{display:grid;gap:6px;background:#fff;border-radius:14px;padding:10px}
.sgroup .urow-h{display:flex;justify-content:space-between;align-items:center;font-size:13px;font-weight:800}
.dlimg{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.polc{background:#fff;border-radius:18px;padding:12px;display:grid;gap:8px;box-shadow:0 1px 0 #ece8f8}
.polc .q{font-size:12.5px;font-weight:800;color:var(--muted)}
.hrs{display:grid;gap:6px}.hrs .hr{display:grid;grid-template-columns:90px 1fr 1fr;gap:8px;align-items:center;font-size:13.5px}
.fees{display:grid;gap:10px}.fee{background:#fff;border-radius:16px;padding:10px;display:grid;gap:8px;box-shadow:0 1px 0 #ece8f8}
.sugg{display:flex;gap:6px;flex-wrap:wrap}.sugg button{border:1px dashed #b9a8f0;background:#fff;border-radius:99px;padding:5px 10px;font-size:12.5px;font-weight:700;cursor:pointer}
.rec{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.rec div{background:#fff;border-radius:14px;padding:10px;text-align:center;display:grid;gap:2px}.rec b{font-size:18px}
.embs{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.embs img{width:40px}
.vtabs{display:flex;gap:6px;flex-wrap:wrap;position:sticky;top:0;z-index:2;background:inherit;padding:6px 0}
.vtabs button{border:0;border-radius:99px;padding:8px 14px;font-weight:900;font-size:13px;background:#efeaff;color:#2a1a55;cursor:pointer}
.vtabs button[aria-selected="true"]{background:#7B2CBF;color:#fff}
.vpane[hidden]{display:none!important}
.ms-emb{display:flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:12.5px;font-weight:800}
.ms-emb img{width:34px}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]
rep('<script src="conversiones.js"></script>', '<script src="conversiones.js"></script>\n<script src="qr.js"></script>')

# ---------- pasos con nombre de cada vertical
rep('''if(S.types.services)l.push({id:"svc",t:"Servicios",e:"🎉",child:true});if(S.types.venue)l.push({id:"venue",t:"Venue",e:"🏡",child:true});if(S.types.planner)l.push({id:"planner",t:"Planner",e:"📋",child:true});''',
    '''if(S.types.services)l.push({id:"svc",t:"Mis servicios",e:"🎉",child:true});if(S.types.venue)l.push({id:"venue",t:"Mi venue",e:"🏡",child:true});if(S.types.planner)l.push({id:"planner",t:"Mi perfil de planner",e:"📋",child:true});''')

# ---------- normalización: campos nuevos para estados viejos y ejemplo
NORM = r'''
const LINK_TYPES=["Sitio web","YouTube","Pinterest","LinkedIn","X (Twitter)","Otro"];
const POL_MAP={"Comida":"Alimentos","Con alcohol":"Bebidas y barra","Sin alcohol":"Bebidas y barra","Postres":"Alimentos","Música":"Música y espectáculos","Luz y show":"Audio, video e iluminación","Mobiliario":"Mobiliario y equipo de banquete","Decoración":"Decoración y flores","Staff":"Personal"};
const FEE_UNITS=[["evento","Por evento"],["hora","Por hora"],["invitado","Por invitado"],["porcentaje","% del total de la fiesta"],["otro","Otro"]];
const BIO_SUGG=["Mi superpoder en una fiesta es…","La fiesta más épica que he organizado…","Nunca llego a un evento sin…","Lo que más disfruto de organizar es…","Mis clientes dicen que…"];
function normPol(p){if(!p)p={offer:"",price:"",per:"evento",own:"",fee:""};
 if(p.incl===undefined){p.incl=p.offer==="inc"?"inc":p.offer==="costo"?"costo":p.offer==="no"?"noinc":"";p.detail="";p.subs=[];
  p.subst=p.own==="no"?"no":p.own?"si":"";p.substMode=p.own==="cuota"?"cuota":p.own==="si"?"libre":"";p.substOther="";p.feeUnit="evento";p.feeNote="";p.modeOther="";}
 return p;}
function syncPol(p,ext){p.offer=p.incl==="inc"||p.incl==="parte"?"inc":p.incl==="costo"?"costo":p.incl==="noinc"?"no":"";
 if(p.incl==="noinc"){p.own=ext==="no"?"no":ext?"si":"";return;}
 p.own=p.subst==="no"?"no":(p.subst==="si"||p.subst==="parcial"||p.subst==="otro")?(p.substMode==="cuota"?"cuota":"si"):"";}
function ensureState(){const b=S.biz,v=S.venue,p=S.planner;
 if(!b.links)b.links=[];if(b.visits===undefined)b.visits=null;
 ["instagram","tiktok","facebook"].forEach(f=>{if(v[f]===undefined)v[f]="";if(p[f]===undefined)p[f]="";});
 if(!v.links)v.links=[];if(!p.links)p.links=[];
 if(v.socialFromBiz===undefined){v.socialFromBiz=!v.instagram&&!v.tiktok&&!v.facebook;}
 if(v.socialFromBiz){v.instagram=b.instagram;v.tiktok=b.tiktok;v.facebook=b.facebook;v.links=b.links.map(x=>({...x}));}
 if(p.socialFromBiz===undefined)p.socialFromBiz=true;
 if(p.socialFromBiz){p.instagram=b.instagram;p.tiktok=b.tiktok;p.facebook=b.facebook;p.links=b.links.map(x=>({...x}));}
 if(v.typeOther===undefined)v.typeOther="";if(!v.featsOther)v.featsOther=[];if(v.sameHours===undefined)v.sameHours=true;if(!v.hoursByDay)v.hoursByDay={};
 POLICY_SVCS.forEach(([x])=>{v.policy[x]=normPol(v.policy[x]);});if(v.extAll===undefined)v.extAll="";if(v.extAllNote===undefined)v.extAllNote="";
 POLICY_SVCS.forEach(([x])=>syncPol(v.policy[x],v.extAll));
 if(v.depositN===undefined){const m=String(v.deposit||"").match(/\d+/);v.depositN=m?m[0]:"";v.depositU="%";}
 if(v.cancelLink===undefined){v.cancelLink="";v.cancelFile=null;}
 if(v.guarRetN===undefined){v.guarRetN="";v.guarRetU="días";}
 if(!p.fees)p.fees=[{amount:p.fee||"",unit:"evento",other:"",note:p.feeNote||""}];
 if(p.depositN===undefined){p.depositN="";p.depositU="%";}if(p.negotiable===undefined)p.negotiable=null;
 p.fee=p.fees[0]?p.fees[0].amount:"";v.deposit=v.depositN?(v.depositU==="%"?v.depositN+"%":money(v.depositN)):"";}
const __exampleState=exampleState;
exampleState=function(){const x=__exampleState();x.biz.links=[{t:"Sitio web",u:"lupitadulces.mx"}];x.biz.visits=true;
 const v=x.venue;v.socialFromBiz=false;v.links=[];v.typeOther="";v.featsOther=["Planta de luz"];v.sameHours=false;v.hoursByDay={jue:{open:"16:00",limit:"22:00"},vie:{open:"16:00",limit:"23:00"},sab:{open:"12:00",limit:"23:59"},dom:{open:"12:00",limit:"20:00"}};
 v.depositN="50";v.depositU="%";v.cancelLink="";v.cancelFile={name:"Politica_cancelacion_TerrazaLupita.pdf",size:182000};v.cancel="Reembolso del anticipo con 30 días de aviso.";v.guarRetN="3";v.guarRetU="días";v.extAll="si";
 Object.keys(v.policy).forEach(k=>{v.policy[k]=normPol(v.policy[k]);});
 v.policy["Mobiliario"].subs=["Cristalería","Cubertería"];v.policy["Mobiliario"].incl="parte";v.policy["Mobiliario"].detail="60 sillas Tiffany y 6 mesas redondas";
 v.policy["Con alcohol"].substMode="cuota";v.policy["Con alcohol"].feeUnit="botella";v.policy["Con alcohol"].fee="150";v.policy["Con alcohol"].feeNote="Descorche";
 v.policy["Música"].subs=["DJ"];
 const p=x.planner;p.socialFromBiz=true;p.fees=[{amount:"6000",unit:"evento",other:"",note:"Hasta 50 invitados"},{amount:"10",unit:"porcentaje",other:"",note:"Fiestas de más de 100 invitados"}];p.depositN="30";p.depositU="%";p.negotiable=true;
 p.bio="Me encanta que nadie note que hubo estrés detrás de una fiesta perfecta. Mi superpoder en una fiesta es leer a los invitados y saber cuándo subir la música.";
 return x;};
'''
rep('\nfunction emptyState(){', NORM + '\nfunction emptyState(){')
rep('function render(){renderTimeline();renderStep();preview();}', 'function render(){ensureState();renderTimeline();renderStep();preview();}')
rep('function preview(){const st=$("site");', 'function preview(){ensureState();const st=$("site");')
rep('function showPublic(from){lastView=from;', 'function showPublic(from){ensureState();lastView=from;')

# ---------- redes: Instagram, TikTok, Facebook + «Otro» repetible
func('socialHtml', r'''
function socialHtml(o,k,note){o.links=o.links||[];return`<div class="field"><span class="lbl">🔗 Redes sociales y links <span class="opt">(opcional)</span></span>${note?`<span class="hint">${note}</span>`:""}<div class="row">
 <input type="text" id="ig-${k}" value="${esc(o.instagram)}" placeholder="📸 Instagram: @tunegocio" aria-label="Instagram">
 <input type="text" id="tt-${k}" value="${esc(o.tiktok)}" placeholder="🎵 TikTok: @tunegocio" aria-label="TikTok">
 <input type="text" id="fb-${k}" value="${esc(o.facebook)}" placeholder="👍 Facebook: tu página" aria-label="Facebook"></div>
 <div class="links" id="lk-${k}">${o.links.map((x,i)=>`<div class="lk" data-i="${i}"><select class="lk-t" aria-label="Tipo de link">${LINK_TYPES.map(t=>`<option ${t===x.t?"selected":""}>${t}</option>`).join("")}</select><input type="text" class="lk-u" value="${esc(x.u)}" placeholder="Pega tu link" aria-label="Link"><button type="button" class="link bad lk-rm">✕</button></div>`).join("")}</div>
 <button type="button" class="link" id="lka-${k}" style="justify-self:start">+ Agregar otro link (sitio web, YouTube…)</button></div>`;}''')
func('bindSocial', r'''
function bindSocial(o,k,redraw,onEdit){[["ig-","instagram"],["tt-","tiktok"],["fb-","facebook"]].forEach(([p,f])=>$(p+k).oninput=e=>{o[f]=e.target.value;onEdit&&onEdit();changed();});
 const box=$("lk-"+k);if(box)box.querySelectorAll(".lk").forEach(r=>{const x=o.links[+r.dataset.i];r.querySelector(".lk-t").onchange=e=>{x.t=e.target.value;onEdit&&onEdit();changed();};r.querySelector(".lk-u").oninput=e=>{x.u=e.target.value;onEdit&&onEdit();changed();};r.querySelector(".lk-rm").onclick=()=>{o.links.splice(+r.dataset.i,1);onEdit&&onEdit();(redraw||render)();changed();};});
 const a=$("lka-"+k);if(a)a.onclick=()=>{o.links.push({t:"Sitio web",u:""});onEdit&&onEdit();(redraw||render)();changed();};}''')
rep('''const socialRow=o=>{const s=[["📸",o.instagram],["🎵",o.tiktok],["👍",o.facebook]].filter(x=>filled(x[1]));''',
    '''const socialRow=o=>{const s=[["📸",o.instagram],["🎵",o.tiktok],["👍",o.facebook],...(o.links||[]).filter(x=>filled(x.u)).map(x=>["🔗",x.u])].filter(x=>filled(x[1]));''')

# ---------- Mi negocio: ¿recibes clientes en tu negocio?
rep('''${addrHtml(b.addr,"biz","Ubicación de tu negocio")}''',
    '''${addrHtml(b.addr,"biz","Ubicación de tu negocio")}
 <div class="field"><span class="lbl">🏪 ¿Puedes recibir clientes en tu negocio?</span><span class="hint">Por ejemplo, para degustaciones, ver muestras o firmar contrato.</span><div class="${MISS(b.visits!==null)}" style="width:fit-content;border-radius:99px">${ynHtml("bv",b.visits)}</div></div>''')
rep('''bindAvatar(b,"biz","avatar");bindSocial(b,"biz");bindAddr(b.addr,"biz",drawBiz);bindNav();}''',
    '''bindAvatar(b,"biz","avatar");bindSocial(b,"biz",drawBiz);bindYN("bv",x=>{b.visits=x;drawBiz();changed();});bindAddr(b.addr,"biz",drawBiz);bindNav();}''')
rep('''if(!b.showAddr)m.push("Qué parte de tu dirección mostrar");}''', '''if(!b.showAddr)m.push("Qué parte de tu dirección mostrar");if(b.visits===null||b.visits===undefined)m.push("¿Recibes clientes en tu negocio?");}''')

# ---------- servicios: varias formas de cobrar en la misma ficha
func('lineHtml', r'''
function lineHtml(s,k,x,j){const f=famOf(x.u);
 return`<div class="urow sline" data-j="${j}"><div class="urow-h"><span>${esc(x.u==="__otra"?"Otra forma":uLabel(x.u))}</span><button type="button" class="link bad sl-rm" aria-label="Quitar esta forma de cobro">✕</button></div>
  ${x.u==="__otra"?`<input type="text" class="sl-uo${MISS(filled(x.uo))}" list="dlUnits" value="${esc(x.uo)}" placeholder="Escribe tu unidad: por charola, por metro…" aria-label="Otra unidad para ${esc(x.n)}">`:''}
  <div class="sl-f">
   <label class="sl-p"><span>${f==="porcentaje"?"%":"$"}</span><input type="number" min="0" step="any" class="sl-price${MISS(filled(x.price))}" value="${esc(x.price)}" placeholder="${f==="porcentaje"?"porcentaje":"precio"}" aria-label="Precio de ${esc(x.n)} ${esc(lineLabel(x))}"> <small class="opt">${esc(f==="porcentaje"?uLabel(x.u).slice(2):lineLabel(x))}</small></label>
   ${f==="paquete"?`<label>¿Para cuántas personas? <input type="number" min="1" class="sl-pkgP${MISS(+x.pkgP>0)}" value="${esc(x.pkgP)}"></label><label>¿Cuántas horas incluye? <input type="number" min="0" step="any" class="sl-pkgH" value="${esc(x.pkgH)}"> <span class="opt">(opcional)</span></label>`:''}
   ${f==="cantidad"||f==="espacio"||f==="otra"?`<label>Cada ${esc(uNoun(x))} alcanza para <input type="number" min="0" step="any" class="sl-yield" value="${esc(x.yieldP)}"> personas <span class="opt">(opcional)</span></label>`:''}
  </div><div class="sl-hv">${hostView(x,s.cat)}</div></div>`;}
function groupHtml(s,k,n,idxs){const sub=subOf(s.cat,n),allowed=(sub&&sub.u.length?sub.u:COMMON_UNITS).slice().sort((p,q)=>urank(p)-urank(q));
 idxs.forEach(j=>{const u=s.subs[j].u;if(u&&u!=="__otra"&&!allowed.includes(u))allowed.push(u);});
 const has=u=>idxs.some(j=>s.subs[j].u===u),set=idxs.filter(j=>s.subs[j].u);
 return`<div class="sgroup" data-n="${esc(n)}"><div class="sl-top"><b>${esc(n)}${NEW_SUBS.has(n)?' <small>· nuevo</small>':''}</b><button type="button" class="link bad sg-rm" aria-label="Quitar ${esc(n)}">✕ Quitar</button></div>
  <span class="mini-l">¿Cómo lo cobras? <span class="opt">Elige una o varias formas</span></span>
  <div class="chips unit-chips${MISS(set.length>0)}">${allowed.map(u=>`<button type="button" class="chip sg-u" data-u="${esc(u)}" aria-pressed="${has(u)}">${TICK}${esc(uLabel(u))}</button>`).join("")}<button type="button" class="chip new sg-u" data-u="__otra" aria-pressed="${has("__otra")}">${TICK}✏️ Otra</button></div>
  ${set.map(j=>lineHtml(s,k,s.subs[j],j)).join("")}</div>`;}''')
rep('''<span class="hint">¿Cobras de dos formas? Usa <b>+ Otra forma de cobrar</b>.</span><div class="slines">${s.subs.map((x,j)=>lineHtml(s,k,x,j)).join("")}</div></div>''',
    '''<span class="hint">¿Cobras de varias formas? Elige todas: cada una tiene su propio precio.</span><div class="slines" style="display:grid;gap:10px">${(()=>{const g=[];s.subs.forEach((x,j)=>{let G=g.find(y=>y.n===x.n);if(!G){G={n:x.n,idx:[]};g.push(G);}G.idx.push(j);});return g.map(G=>groupHtml(s,k,G.n,G.idx)).join("");})()}</div></div>''')
s, n = re.subn(r'el\.querySelectorAll\("\.sline"\)\.forEach\(L=>\{.*?s\.subs\.splice\(e\+1,0,blankLine\(x\.n\)\);redraw\(\);changed\(\);\};\}\);',
    r'''el.querySelectorAll(".sgroup").forEach(G=>{const n=G.dataset.n;const idx=()=>s.subs.map((y,j)=>y.n===n?j:-1).filter(j=>j>=0);
   G.querySelector(".sg-rm").onclick=()=>{s.subs=s.subs.filter(y=>y.n!==n);redraw();changed();};
   G.querySelectorAll(".sg-u").forEach(c=>c.onclick=()=>{const u=c.dataset.u,ids=idx(),on=ids.find(j=>s.subs[j].u===u);
    if(on!==undefined){if(ids.length>1)s.subs.splice(on,1);else{const x=s.subs[on];x.u="";x.uo="";x.price="";x.unit="";}}
    else{const empty=ids.find(j=>!s.subs[j].u);if(empty!==undefined){s.subs[empty].u=u;s.subs[empty].unit=lineLabel(s.subs[empty]);}else{const nl=blankLine(n);nl.u=u;nl.unit=lineLabel(nl);s.subs.splice(ids[ids.length-1]+1,0,nl);}}
    redraw();changed();if(u==="__otra")setTimeout(()=>{const b=document.querySelector(`#svcList .box[data-i="${i}"] .sl-uo`);b&&b.focus();},0);});});
  el.querySelectorAll(".sline").forEach(L=>{const j=+L.dataset.j,x=s.subs[j],hv=()=>{const h=L.querySelector(".sl-hv");if(h)h.innerHTML=hostView(x,s.cat);};
   const uo=L.querySelector(".sl-uo");if(uo){uo.oninput=e=>{x.uo=e.target.value;x.unit=lineLabel(x);changed();};
    uo.onchange=()=>{const v=x.uo.trim();if(!v)return;const cu=canonUnit(v);if(cu){x.u=cu;x.uo="";}else{NEW_UNITS.add(v);hqvTrack("catalogo_propuesta",{tipo:"unidad",sub:x.n,valor:v});}x.unit=lineLabel(x);redraw();changed();};}
   [["sl-price","price"],["sl-pkgP","pkgP"],["sl-pkgH","pkgH"],["sl-yield","yieldP"]].forEach(([c,f])=>{const q=L.querySelector("."+c);if(q)q.oninput=e=>{x[f]=e.target.value;hv();changed();};});
   L.querySelector(".sl-rm").onclick=()=>{const ids=s.subs.map((y,jj)=>y.n===x.n?jj:-1).filter(jj=>jj>=0);if(ids.length>1)s.subs.splice(j,1);else{x.u="";x.uo="";x.price="";x.unit="";}redraw();changed();};});''',
    s, count=1, flags=re.S)
assert n == 1, 'binding de líneas'

# ---------- promoción: descargar imagen para redes
func('promoHtml', r'''
function promoHtml(p,k,anchor){const link=`hayquevernos.com/${slug(S.biz.name)}#promo-${anchor}`;
 return`<div class="field"><span class="lbl">🏷️ ¿Tienes alguna promoción?</span><div class="${MISS(p.has!==null)}" style="width:fit-content;border-radius:99px">${ynHtml("pr-"+k,p.has)}</div>
 ${p.has?`<div class="sub-box"><input type="text" id="pw-${k}" class="${MISS(filled(p.what))}" value="${esc(p.what)}" placeholder="¿En qué consiste? 10% de descuento, 2x1…" aria-label="Promoción">
 <div class="row"><input type="text" id="pt-${k}" class="${MISS(filled(p.terms))}" value="${esc(p.terms)}" placeholder="Condiciones" aria-label="Condiciones"><div class="field"><label class="hint" for="pu-${k}">Válida hasta</label><input type="date" id="pu-${k}" class="${MISS(filled(p.until))}" value="${esc(p.until)}"></div></div>
 <div class="copyline"><span>🔗 Link de tu promo:</span><code id="pl-${k}">${esc(link)}</code><button type="button" class="btn sm" id="pc-${k}">Copiar</button></div>
 <div class="dlimg"><button type="button" class="btn sm cta" id="pd-${k}">⬇️ Descargar imagen para redes</button><span class="hint">Con tu promo, tu link y un código QR, lista para Instagram, Facebook o tu estado de WhatsApp.</span></div>
 <span class="hint" id="pm-${k}" aria-live="polite">Compártelo por WhatsApp o redes: lleva directo a esta promo en tu sitio.</span></div>`:''}</div>`;}''')
rep('''const c=$("pc-"+k);if(c)c.onclick=()=>copyText("https://"+$("pl-"+k).textContent,$("pm-"+k));}''',
    '''const c=$("pc-"+k);if(c)c.onclick=()=>copyText("https://"+$("pl-"+k).textContent,$("pm-"+k));
 const d=$("pd-"+k);if(d)d.onclick=async()=>{const url=await hqvShareImage({logo:"img/logo.webp",kicker:S.biz.name||"Mi negocio",title:p.what||"Promoción",sub:[p.terms,p.until?"Válida hasta el "+new Date(p.until+"T12:00").toLocaleDateString("es-MX",{day:"numeric",month:"long"}):""].filter(Boolean).join(" · "),url:$("pl-"+k).textContent,foot:"Escanea y aparta tu fecha por WhatsApp"});hqvDownload(url,"promo-"+slug(S.biz.name)+".png");hqvTrack("imagen_promo_descargada");};}''')
ex = 'async function shareSite(){const url=await hqvShareImage({logo:"img/logo.webp",kicker:"Encuéntranos en ¡Hay que vernos!",title:S.biz.name||"Mi negocio",sub:S.biz.about||"",url:"hayquevernos.com/"+slug(S.biz.name),foot:"Escanea, conoce mis servicios y cotiza por WhatsApp"});hqvDownload(url,"sitio-"+slug(S.biz.name)+".png");hqvTrack("imagen_sitio_descargada");}\n'
rep('async function copyText(', ex + 'async function copyText(')

# ---------- venue completo
func('drawVenue', r'''
function polCard(s,e,p,k){const cat=POL_MAP[s],subs=cat&&catOf(cat)?catOf(cat).s.map(x=>x.n).slice(0,14):[];const inc=p.incl&&p.incl!=="noinc";
 return`<div class="polc${MISS(polOk(p))}" data-s="${esc(s)}"><b>${e} ${esc(s)}</b>
  <span class="q">¿Está incluido en tu renta o paquetes?</span><div class="chips">${[["inc","✅ Incluido"],["parte","🟡 Incluido en parte"],["costo","💲 Con costo extra"],["noinc","➖ No incluido"]].map(([v,t])=>`<button type="button" class="chip p-in" data-v="${v}" aria-pressed="${p.incl===v}">${TICK}${t}</button>`).join("")}</div>
  ${p.incl==="parte"?`<input type="text" class="p-det" value="${esc(p.detail)}" placeholder="¿Qué parte incluye? Ej. 60 sillas y 6 mesas" aria-label="Detalle de lo incluido">`:""}
  ${p.incl==="costo"?`<div class="row"><input type="number" min="0" class="ppr" value="${esc(p.price)}" placeholder="$ precio" aria-label="Precio de ${esc(s)}"><select class="pper" aria-label="Cómo lo cobras">${[["evento","por evento"],["persona","por persona"],["hora","por hora"]].map(([v,t])=>`<option value="${v}" ${p.per===v?"selected":""}>${t}</option>`).join("")}</select></div>`:""}
  ${inc&&subs.length?`<span class="q">¿Qué incluye? <span class="opt">(opcional)</span></span><div class="chips">${subs.map(n=>`<button type="button" class="chip p-sub" data-n="${esc(n)}" aria-pressed="${(p.subs||[]).includes(n)}">${TICK}${esc(n)}</button>`).join("")}</div>`:""}
  ${inc?`<span class="q">¿El cliente puede sustituirlo con un proveedor externo?</span><div class="chips">${[["si","Sí"],["no","No"],["parcial","Parcial"],["otro","Otro"]].map(([v,t])=>`<button type="button" class="chip p-sb" data-v="${v}" aria-pressed="${p.subst===v}">${TICK}${t}</button>`).join("")}</div>
   ${p.subst==="otro"||p.subst==="parcial"?`<input type="text" class="p-sbo" value="${esc(p.substOther)}" placeholder="${p.subst==="parcial"?"¿Qué sí puede traer?":"Explícalo"}" aria-label="Detalle de sustitución">`:""}
   ${p.subst==="si"||p.subst==="parcial"?`<div class="chips">${[["libre","🆓 Libre"],["cuota","🎟️ Con cuota"],["otro","Otro"]].map(([v,t])=>`<button type="button" class="chip p-sm" data-v="${v}" aria-pressed="${p.substMode===v}">${TICK}${t}</button>`).join("")}</div>
    ${p.substMode==="cuota"?`<div class="row"><input type="number" min="0" class="pfee" value="${esc(p.fee)}" placeholder="$ cuota" aria-label="Cuota"><select class="pfu" aria-label="Unidad de la cuota">${["evento","persona","botella","hora"].map(u=>`<option value="${u}" ${p.feeUnit===u?"selected":""}>por ${u}</option>`).join("")}</select></div><input type="text" class="pfn" value="${esc(p.feeNote)}" placeholder="Nota: descorche, derecho de piso… (opcional)" aria-label="Nota de la cuota">`:""}
    ${p.substMode==="otro"?`<input type="text" class="pmo" value="${esc(p.modeOther)}" placeholder="Explícalo" aria-label="Otra condición">`:""}`:""}`:""}</div>`;}
function drawVenue(){const v=S.venue,k="v",b=S.biz;const isR=v.mode==="renta"||v.mode==="ambos",isP=v.mode==="paquetes"||v.mode==="ambos";
 const pol=POLICY_SVCS.map(([x,e])=>polCard(x,e,v.policy[x],k)).join("");
 const pk=v.packages.map((x,i)=>`<div class="pkg${MISS(pkgOk(x))}" data-i="${i}"><div class="row"><input type="text" class="pk-n" value="${esc(x.name)}" placeholder="Nombre: Paquete 1, Plata, Básico…" aria-label="Nombre del paquete"><input type="number" min="0" class="pk-p" value="${esc(x.price)}" placeholder="$ precio" aria-label="Precio del paquete"></div>
  <div class="row"><select class="pk-per" aria-label="Cómo se cobra">${[["persona","por persona"],["total","precio total"]].map(([val,t])=>`<option value="${val}" ${x.per===val?'selected':''}>${t}</option>`).join("")}</select><input type="number" min="0" class="pk-m" value="${esc(x.min)}" placeholder="Mínimo de invitados (opcional)" aria-label="Mínimo de invitados"></div>
  <span class="mini-l">Este paquete incluye</span><div class="chips">${POLICY_SVCS.map(([s2,e])=>`<button type="button" class="chip pk-i" data-s="${esc(s2)}" aria-pressed="${x.inc.includes(s2)}">${TICK}${e} ${esc(s2)}</button>`).join("")}</div>
  <button type="button" class="link bad pk-rm">Quitar paquete</button></div>`).join("");
 const days=HQV.DAYS.filter(([d])=>v.days.includes(d));
 $("stepBody").innerHTML=`<div class="panel"><span class="crumb">Mi negocio › Mi venue</span><h2>Mi venue 🏡</h2>
 <div class="alert info">💡 <span><b>¿Qué es un venue?</b> Cualquier lugar donde se puede hacer una fiesta: terraza, jardín, salón, roof, casa o restaurante que rentas para eventos.</span></div>
 <div class="field"><label class="lbl" for="v-name">Nombre del lugar</label><input type="text" id="v-name" class="${MISS(filled(v.name))}" value="${esc(v.name)}" placeholder="Terraza Las Flores"></div>
 ${avatarHtml(v,"vav","avatar","🖼️ Foto de logo o perfil del lugar")}
 ${socialHtml(v,"v",v.socialFromBiz?"Pusimos las redes de tu negocio. Si tu venue tiene redes propias, cámbialas aquí y solo se actualizan en la sección del venue.":"Estas redes son solo de tu venue.")}
 ${addrHtml(v.addr,"v","Dirección del lugar")}
 <div class="field"><span class="lbl">Tipo de espacio</span><div class="cats${MISS(!!v.type&&(v.type!=="__otro"||filled(v.typeOther)))}">${HQV.VENUE_TYPES.map(([t,e])=>`<button type="button" class="cat vt" data-t="${esc(t)}" aria-pressed="${v.type===t}"><span class="emo">${e}</span><span>${esc(t)}</span></button>`).join("")}<button type="button" class="cat vt" data-t="__otro" aria-pressed="${v.type==="__otro"}"><span class="emo">✏️</span><span>Otro</span></button></div>
  ${v.type==="__otro"?`<input type="text" id="v-tother" value="${esc(v.typeOther)}" placeholder="¿Qué tipo de espacio es?" aria-label="Otro tipo de espacio">`:""}</div>
 <div class="field"><span class="lbl">👥 ¿Cuántas personas caben?</span><div class="row"><div class="field"><label class="hint" for="v-seat">🪑 Sentadas</label><input type="number" id="v-seat" min="1" class="${MISS(+v.seated>0)}" value="${esc(v.seated)}"></div><div class="field"><label class="hint" for="v-stand">🕺 De pie</label><input type="number" id="v-stand" min="1" class="${MISS(+v.standing>0)}" value="${esc(v.standing)}"></div></div><span class="hint">Calculamos uno con el otro (de pie ≈ 1.5 × sentadas). Ajústalo si en tu lugar es distinto.</span></div>
 <div class="field"><label class="lbl" for="v-area">📐 Tamaño</label><select id="v-area" class="${MISS(!!v.area)}"><option value="">Elige</option>${["6 a 12 m²","13 a 20 m²","21 a 30 m²","31 a 40 m²","41 a 50 m²","51 a 60 m²","61 a 100 m²","101 a 300 m²","Más de 300 m²"].map(t=>`<option ${t===v.area?'selected':''}>${t}</option>`).join("")}</select></div>
 <div class="field"><span class="lbl">🏠 ¿Con qué cuenta tu espacio?</span><span class="hint">Los anfitriones buscan con esta misma lista. Lo que no marques, no aparecerá en sus búsquedas.</span><div class="chips${MISS(v.features.length>0||v.featsOther.some(filled))}" style="border-radius:14px">${HQV.VENUE_FEATS.map(([id,e,t])=>`<button type="button" class="chip ft" data-f="${id}" aria-pressed="${v.features.includes(id)}">${TICK}${e} ${esc(t)}</button>`).join("")}</div>
  <div style="display:grid;gap:6px">${v.featsOther.map((x,i)=>`<div class="row fo" data-i="${i}"><input type="text" class="fo-in" value="${esc(x)}" placeholder="Otra amenidad" aria-label="Otra amenidad"><button type="button" class="link bad fo-rm">✕</button></div>`).join("")}<button type="button" class="link" id="fo-add" style="justify-self:start">+ Otra amenidad</button></div></div>
 <div class="field"><span class="lbl">🚻 Baños</span><div class="row${MISS(+v.baths.m+ +v.baths.w+ +v.baths.g>0)}" style="border-radius:12px">${[["m","🚹 Hombres"],["w","🚺 Mujeres"],["g","🚻 Generales"]].map(([f,t])=>`<div class="field"><label class="hint" for="vb-${f}">${t}</label><input type="number" min="0" id="vb-${f}" value="${esc(v.baths[f])}" placeholder="0"></div>`).join("")}</div></div>

 <div class="field"><span class="lbl">🕒 Horario y precios</span><div class="sub-box" style="display:grid;gap:12px">
  <span class="hint">¿Qué días rentas?</span><div class="chips${MISS(v.days.length>0)}" style="border-radius:14px">${HQV.DAYS.map(([d,t])=>`<button type="button" class="chip vd" data-d="${d}" aria-pressed="${v.days.includes(d)}">${TICK}${t}</button>`).join("")}</div>
  <div class="chips" style="width:fit-content;border-radius:99px"><button type="button" class="chip sh" data-v="1" aria-pressed="${v.sameHours}">${TICK}Mismo horario todos los días</button><button type="button" class="chip sh" data-v="0" aria-pressed="${!v.sameHours}">${TICK}Horario por día</button></div>
  ${v.sameHours?`<div class="row"><div class="field"><label class="hint" for="v-open">Pueden empezar desde</label><input type="time" id="v-open" class="${MISS(filled(v.open))}" value="${esc(v.open)}"></div><div class="field"><label class="hint" for="v-limit">Hora límite (todos fuera)</label><input type="time" id="v-limit" class="${MISS(filled(v.limit))}" value="${esc(v.limit)}"></div></div>`
   :`<div class="hrs">${days.map(([d,t])=>{const h=v.hoursByDay[d]||{open:v.open,limit:v.limit};return`<div class="hr" data-d="${d}"><b>${t}</b><input type="time" class="hd-o" value="${esc(h.open||"")}" aria-label="Desde, ${t}"><input type="time" class="hd-l" value="${esc(h.limit||"")}" aria-label="Hora límite, ${t}"></div>`;}).join("")||'<span class="hint">Primero elige los días.</span>'}</div>`}
  <div class="row"><div class="field"><label class="hint" for="v-hincl">Horas de fiesta incluidas</label><input type="number" id="v-hincl" min="1" max="24" class="${MISS(+v.hoursIncl>0)}" value="${esc(v.hoursIncl)}"></div>
   <div class="field"><label class="hint" for="v-xh">Cada hora extra $</label><input type="number" id="v-xh" min="0" class="${MISS(filled(v.extraHour))}" value="${esc(v.extraHour)}"></div></div>
  <span class="hint">📏 Estándar ¡HQV!: además de las horas de fiesta, ½ hora para montar y ½ hora para desmontar sin costo.</span>
  <span class="lbl" style="font-size:14px">💲 ¿Cómo cobras?</span><div class="chips${MISS(!!v.mode)}" style="border-radius:14px">${[["renta","🏠 Renta del espacio"],["paquetes","📦 Paquetes"],["ambos","Las dos"]].map(([val,t])=>`<button type="button" class="chip vm" data-v="${val}" aria-pressed="${v.mode===val}">${TICK}${t}</button>`).join("")}</div>
  ${isR?`<div class="row"><input type="number" min="0" id="r-price" class="${MISS(filled(v.rent.price))}" value="${esc(v.rent.price)}" placeholder="$ precio de renta" aria-label="Precio de renta"><select id="r-per" aria-label="Cómo cobras la renta">${[["evento",`por evento (${v.hoursIncl||5} h incluidas)`],["hora","por hora"],["persona","por persona"]].map(([val,t])=>`<option value="${val}" ${v.rent.per===val?'selected':''}>${t}</option>`).join("")}</select></div>
   <div class="row"><div class="field"><label class="hint" for="r-upto">Incluye hasta (invitados) <span class="opt">opcional</span></label><input type="number" min="0" id="r-upto" value="${esc(v.rent.upTo)}" placeholder="Ej. 60"></div><div class="field"><label class="hint" for="r-pxg">Cada invitado extra $</label><input type="number" min="0" id="r-pxg" value="${esc(v.rent.perExtraGuest)}" placeholder="Ej. 150" ${filled(v.rent.upTo)?'':'disabled'}></div></div>`:''}
  ${isP?`<b style="font-size:14px">📦 Mis paquetes</b>${pk||''}${v.packages.length<4?`<button type="button" class="btn ghost sm" id="pk-add">+ Agregar paquete</button>`:''}`:''}
  <span class="hint">¿Tu precio es negociable?</span><div class="chips${MISS(v.negotiable!==null)}" style="width:fit-content;border-radius:99px">${[[true,"🤝 Sí, se puede platicar"],[false,"Precio fijo"]].map(([val,t])=>`<button type="button" class="chip neg" data-v="${val}" aria-pressed="${v.negotiable===val}">${TICK}${t}</button>`).join("")}</div>
  <details><summary class="hint" style="cursor:pointer"><b>📈 Ajustes de precio y espacios extra</b> (opcional)</summary><div style="display:grid;gap:8px;margin-top:8px">
   <span class="hint">¿Cobras distinto según el día? Pon el porcentaje de más (+) o de menos (−).</span>
   <div class="dayadj">${days.map(([d,t])=>`<label><span>${t}</span><input type="number" step="5" class="adj-d" data-d="${d}" value="${esc(v.adj.day[d]||"")}" placeholder="0 %" aria-label="Ajuste ${HQV.DAY_NAMES[d]}"></label>`).join("")||'<span class="hint">Primero elige los días que rentas.</span>'}</div>
   <div class="field"><label class="hint" for="adj-dt">Si la fiesta es de día (termina antes de las 7 pm), % de ajuste</label><input type="number" step="5" id="adj-dt" value="${esc(v.adj.daytime)}" placeholder="Ej. −10"></div>
   ${v.spaces.map((x,i)=>`<div class="row sp-row" data-i="${i}"><input type="text" class="sp-n" value="${esc(x.name)}" placeholder="Nombre del espacio" aria-label="Espacio extra"><input type="number" min="0" class="sp-p" value="${esc(x.price)}" placeholder="$ por evento" aria-label="Precio del espacio extra"><button type="button" class="link bad sp-rm">Quitar</button></div>`).join("")}
   <button type="button" class="btn ghost sm" id="sp-add" style="width:fit-content">+ Espacio extra (salón VIP, alberca…)</button></div></details>
 </div></div>

 <div class="field"><span class="lbl">🔄 Servicios en tu venue</span><span class="hint">Para cada servicio dinos si está incluido y si el cliente puede traer a su propio proveedor. Así solo te llegan fiestas que sí puedes atender.</span><div style="display:grid;gap:10px">${pol}</div>
  <div class="polc${MISS(!!v.extAll)}"><b>🚪 ¿Todos los servicios que no incluyes los puede traer el cliente con proveedores externos?</b><div class="chips">${[["si","Sí, todos"],["algunos","Solo algunos"],["no","No"]].map(([x,t])=>`<button type="button" class="chip p-ext" data-v="${x}" aria-pressed="${v.extAll===x}">${TICK}${t}</button>`).join("")}</div>
   ${v.extAll==="algunos"?`<input type="text" id="v-extn" value="${esc(v.extAllNote)}" placeholder="¿Cuáles sí y cuáles no?" aria-label="Cuáles servicios externos">`:""}</div></div>

 <div class="field"><span class="lbl">📝 Condiciones para rentarlo</span><div class="sub-box" style="display:grid;gap:12px">
  <div class="field"><span class="hint">💳 Anticipo para apartar</span><div class="row"><input type="number" min="0" id="v-depn" class="${MISS(filled(v.depositN))}" value="${esc(v.depositN)}" placeholder="Ej. 50" aria-label="Anticipo"><select id="v-depu" aria-label="Unidad del anticipo"><option value="%" ${v.depositU==="%"?"selected":""}>% del total</option><option value="$" ${v.depositU==="$"?"selected":""}>pesos ($)</option></select></div></div>
  <div class="row"><div class="field"><label class="hint" for="v-adv">Reservar con (días de anticipación)</label><input type="number" id="v-adv" min="0" class="${MISS(filled(v.advance))}" value="${esc(v.advance)}"></div>
   <div class="field"><label class="hint" for="v-guar">Depósito en garantía $ <span class="opt">(opcional)</span></label><input type="number" id="v-guar" min="0" value="${esc(v.guarantee)}"></div></div>
  ${filled(v.guarantee)?`<div class="field"><span class="hint">🔐 Devolución del depósito en garantía</span><div class="row"><input type="number" min="0" id="v-grn" value="${esc(v.guarRetN)}" placeholder="Ej. 3" aria-label="Tiempo de devolución"><select id="v-gru" aria-label="Unidad">${["horas","días","semanas"].map(u=>`<option ${v.guarRetU===u?"selected":""}>${u}</option>`).join("")}</select></div><span class="hint">Después del evento.</span></div>`:""}
  <div class="field"><span class="hint">↩️ Política de cancelación y devolución</span><span class="hint">Sube tu documento, pega un link o, si no la tienes por escrito, descríbela.</span>
   <div class="up-top"><label class="pick">📎 Subir documento<input type="file" id="v-cfile" accept="application/pdf,image/jpeg,image/png"></label><span class="specs"><span><b>PDF, JPG o PNG</b></span><span>hasta <b>10 MB</b></span></span></div>
   ${v.cancelFile?`<span class="file-chip">📄 ${esc(v.cancelFile.name)} · ${kb(v.cancelFile.size)} <button type="button" class="link bad" id="v-crm">Quitar</button></span>`:""}
   <input type="url" id="v-clink" value="${esc(v.cancelLink)}" placeholder="🔗 o pega el link a tu política" aria-label="Link de la política de cancelación">
   <textarea id="v-cancel" placeholder="o descríbela: reembolso del anticipo con 30 días de aviso…">${esc(v.cancel)}</textarea><div id="cmsg"></div></div>
  <div class="field"><span class="hint">📄 Documentos que pides al cliente</span><div class="chips${MISS(v.docsNone||v.docs.length>0||filled(v.docsOther))}" style="border-radius:14px">${DOCS.map(d=>`<button type="button" class="chip doc" data-d="${esc(d)}" aria-pressed="${v.docs.includes(d)}" ${v.docsNone?'disabled':''}>${TICK}${esc(d)}</button>`).join("")}<button type="button" class="chip" id="docNone" aria-pressed="${v.docsNone}">${TICK}No pido documentos</button></div>
   ${v.docsNone?'':`<input type="text" id="v-docs" value="${esc(v.docsOther)}" placeholder="Otro documento (opcional)">`}</div>
  <div class="field"><label class="hint" for="v-rules">📌 Reglas del lugar: escríbelas o sube tu reglamento</label><textarea id="v-rules" class="${MISS(filled(v.rulesText)||!!v.rulesFile)}" placeholder="Sin confeti, volumen moderado después de las 22:00…">${esc(v.rulesText)}</textarea>
   <div class="up-top"><label class="pick">📎 Subir reglamento<input type="file" id="v-rfile" accept="application/pdf,image/jpeg,image/png"></label><span class="specs"><span><b>PDF, JPG o PNG</b></span><span>hasta <b>10 MB</b></span></span></div>
   ${v.rulesFile?`<span class="file-chip">📄 ${esc(v.rulesFile.name)} · ${kb(v.rulesFile.size)} <button type="button" class="link bad" id="v-rrm">Quitar</button></span>`:''}<div id="rmsg"></div></div></div></div>
 <div class="stdbox" id="stdbox">${venueStdRows(v)}</div>
 ${promoHtml(v.promo,k,"venue")}
 <div class="field"><span class="lbl">📷 Fotos del lugar</span><span class="hint">Una desde cada esquina, de día y de noche, y montado como para un evento.</span>${uploaderHtml(k,"photo",v.photos,v.photos.length>0)}</div>
 ${navHtml()}</div>`;
 const redraw=()=>{const y=scrollY;drawVenue();scrollTo({top:y});};
 const ch=()=>{ensureState();changed();const bx=$("stdbox");if(bx)bx.innerHTML=venueStdRows(v);};
 [["v-name","name"],["v-area","area"],["v-open","open"],["v-limit","limit"],["v-hincl","hoursIncl"],["v-xh","extraHour"],["v-adv","advance"],["v-guar","guarantee"],["v-cancel","cancel"],["v-rules","rulesText"],["v-depn","depositN"],["v-depu","depositU"],["v-clink","cancelLink"],["v-grn","guarRetN"],["v-gru","guarRetU"],["v-tother","typeOther"],["v-extn","extAllNote"]].forEach(([i,f])=>{const el=$(i);if(el)el.oninput=el.onchange=e=>{v[f]=e.target.value;ch();};});
 $("v-guar").onchange=()=>redraw();
 $("v-seat").oninput=e=>{v.seated=e.target.value;v.standing=+v.seated>0?String(Math.round(+v.seated*1.5)):"";$("v-stand").value=v.standing;ch();};
 $("v-stand").oninput=e=>{v.standing=e.target.value;v.seated=+v.standing>0?String(Math.round(+v.standing/1.5)):"";$("v-seat").value=v.seated;ch();};
 ["m","w","g"].forEach(f=>$("vb-"+f).oninput=e=>{v.baths[f]=e.target.value;ch();});
 document.querySelectorAll(".vt").forEach(t=>t.onclick=()=>{v.type=t.dataset.t;redraw();changed();});
 document.querySelectorAll(".ft").forEach(c=>c.onclick=()=>{const f=c.dataset.f;v.features=v.features.includes(f)?v.features.filter(x=>x!==f):[...v.features,f];c.setAttribute("aria-pressed",v.features.includes(f));ch();});
 document.querySelectorAll(".fo").forEach(r=>{const i=+r.dataset.i;r.querySelector(".fo-in").oninput=e=>{v.featsOther[i]=e.target.value;ch();};r.querySelector(".fo-rm").onclick=()=>{v.featsOther.splice(i,1);redraw();changed();};});
 $("fo-add").onclick=()=>{v.featsOther.push("");redraw();setTimeout(()=>{const l=[...document.querySelectorAll(".fo-in")].pop();l&&l.focus();},0);};
 document.querySelectorAll(".vd").forEach(c=>c.onclick=()=>{const d=c.dataset.d;v.days=v.days.includes(d)?v.days.filter(x=>x!==d):HQV.DAYS.map(x=>x[0]).filter(x=>x===d||v.days.includes(x));redraw();changed();});
 document.querySelectorAll(".sh").forEach(c=>c.onclick=()=>{v.sameHours=c.dataset.v==="1";redraw();changed();});
 document.querySelectorAll(".hr").forEach(r=>{const d=r.dataset.d,h=v.hoursByDay[d]=v.hoursByDay[d]||{open:v.open,limit:v.limit};r.querySelector(".hd-o").oninput=e=>{h.open=e.target.value;ch();};r.querySelector(".hd-l").oninput=e=>{h.limit=e.target.value;ch();};});
 document.querySelectorAll(".vm").forEach(c=>c.onclick=()=>{v.mode=c.dataset.v;if((v.mode==="paquetes"||v.mode==="ambos")&&!v.packages.length)v.packages.push(blankPkg());redraw();changed();});
 const rp=$("r-price");if(rp){rp.oninput=e=>{v.rent.price=e.target.value;ch();};$("r-per").onchange=e=>{v.rent.per=e.target.value;ch();};$("r-upto").oninput=e=>{v.rent.upTo=e.target.value;$("r-pxg").disabled=!filled(v.rent.upTo);ch();};$("r-pxg").oninput=e=>{v.rent.perExtraGuest=e.target.value;ch();};}
 document.querySelectorAll(".pkg").forEach(box=>{const x=v.packages[+box.dataset.i];const q=s2=>box.querySelector(s2);
  q(".pk-n").oninput=e=>{x.name=e.target.value;ch();};q(".pk-p").oninput=e=>{x.price=e.target.value;ch();};q(".pk-per").onchange=e=>{x.per=e.target.value;ch();};q(".pk-m").oninput=e=>{x.min=e.target.value;ch();};
  box.querySelectorAll(".pk-i").forEach(c=>c.onclick=()=>{const s2=c.dataset.s;x.inc=x.inc.includes(s2)?x.inc.filter(y=>y!==s2):[...x.inc,s2];c.setAttribute("aria-pressed",x.inc.includes(s2));ch();});
  q(".pk-rm").onclick=()=>{v.packages.splice(+box.dataset.i,1);redraw();changed();};});
 const pa=$("pk-add");if(pa)pa.onclick=()=>{v.packages.push(blankPkg());redraw();changed();};
 document.querySelectorAll(".adj-d").forEach(i=>i.oninput=()=>{v.adj.day[i.dataset.d]=i.value;ch();});
 $("adj-dt").oninput=e=>{v.adj.daytime=e.target.value;ch();};
 document.querySelectorAll(".sp-row").forEach(r=>{const x=v.spaces[+r.dataset.i];r.querySelector(".sp-n").oninput=e=>{x.name=e.target.value;ch();};r.querySelector(".sp-p").oninput=e=>{x.price=e.target.value;ch();};r.querySelector(".sp-rm").onclick=()=>{v.spaces.splice(+r.dataset.i,1);redraw();changed();};});
 $("sp-add").onclick=()=>{v.spaces.push({name:"",price:""});redraw();changed();};
 document.querySelectorAll(".neg").forEach(c=>c.onclick=()=>{v.negotiable=c.dataset.v==="true";document.querySelectorAll(".neg").forEach(x=>x.setAttribute("aria-pressed",x===c));ch();});
 document.querySelectorAll(".polc[data-s]").forEach(box=>{const p=v.policy[box.dataset.s];const on=(sel,f)=>box.querySelectorAll(sel).forEach(c=>c.onclick=()=>{f(c);redraw();changed();});
  on(".p-in",c=>{p.incl=c.dataset.v;});on(".p-sb",c=>{p.subst=c.dataset.v;if(p.subst==="si"&&!p.substMode)p.substMode="libre";});on(".p-sm",c=>{p.substMode=c.dataset.v;});
  on(".p-sub",c=>{const n=c.dataset.n;p.subs=(p.subs||[]).includes(n)?p.subs.filter(y=>y!==n):[...(p.subs||[]),n];});
  [[".p-det","detail"],[".ppr","price"],[".pper","per"],[".pfee","fee"],[".pfu","feeUnit"],[".pfn","feeNote"],[".p-sbo","substOther"],[".pmo","modeOther"]].forEach(([sel,f])=>{const el=box.querySelector(sel);if(el)el.oninput=el.onchange=e=>{p[f]=e.target.value;ch();};});});
 document.querySelectorAll(".p-ext").forEach(c=>c.onclick=()=>{v.extAll=c.dataset.v;redraw();changed();});
 document.querySelectorAll(".doc").forEach(c=>c.onclick=()=>{const d=c.dataset.d;v.docs=v.docs.includes(d)?v.docs.filter(x=>x!==d):[...v.docs,d];c.setAttribute("aria-pressed",v.docs.includes(d));ch();});
 $("docNone").onclick=()=>{v.docsNone=!v.docsNone;if(v.docsNone){v.docs=[];v.docsOther="";}redraw();changed();};
 const dO=$("v-docs");if(dO)dO.oninput=e=>{v.docsOther=e.target.value;ch();};
 const upf=(id,msgId,set)=>{$(id).onchange=e=>{const f=e.target.files[0];e.target.value="";if(!f)return;const okT=["application/pdf","image/jpeg","image/png"];
  if(!okT.includes(f.type)){$(msgId).innerHTML=`<div class="alert bad">❌ <span>"${esc(f.name)}" no es PDF, JPG ni PNG. Si es un Word, guárdalo como PDF y vuelve a subirlo.</span></div>`;return;}
  if(f.size>10*1048576){$(msgId).innerHTML=`<div class="alert bad">❌ <span>"${esc(f.name)}" pesa ${kb(f.size)}; el máximo es 10 MB.</span></div>`;return;}
  set({name:f.name,size:f.size});redraw();changed();};};
 upf("v-rfile","rmsg",x=>v.rulesFile=x);upf("v-cfile","cmsg",x=>v.cancelFile=x);
 const rr=$("v-rrm");if(rr)rr.onclick=()=>{v.rulesFile=null;redraw();changed();};
 const cr=$("v-crm");if(cr)cr.onclick=()=>{v.cancelFile=null;redraw();changed();};
 bindAvatar(v,"vav","avatar");bindSocial(v,"v",redraw,()=>{v.socialFromBiz=false;});bindAddr(v.addr,"v",redraw);bindPromo(v.promo,k,redraw);bindUploader(k,"photo",v.photos,redraw);bindNav();}''')
rep('''const polOk=p=>!!p.offer&&!!p.own&&(p.offer!=="costo"||filled(p.price))&&(p.own!=="cuota"||filled(p.fee));''',
    '''const polOk=p=>!!p.incl&&(p.incl==="noinc"||!!p.subst)&&(p.incl!=="costo"||filled(p.price))&&(p.incl!=="parte"||filled(p.detail))&&(!(p.subst==="si"||p.subst==="parcial")||!!p.substMode)&&(p.substMode!=="cuota"||!(p.subst==="si"||p.subst==="parcial")||filled(p.fee));''')
rep('''if(!v.type)m.push("Tipo de espacio");''', '''if(!v.type||(v.type==="__otro"&&!filled(v.typeOther)))m.push("Tipo de espacio");''')
rep('''if(!v.days.length)m.push("Días que rentas");if(!filled(v.open)||!filled(v.limit))m.push("Horario");''',
    '''if(!v.days.length)m.push("Días que rentas");if(v.sameHours?(!filled(v.open)||!filled(v.limit)):v.days.some(d=>!(v.hoursByDay[d]&&filled(v.hoursByDay[d].open)&&filled(v.hoursByDay[d].limit))))m.push("Horario");''')
rep('''if(!v.features.length)m.push("Con qué cuenta tu espacio");''', '''if(!v.features.length&&!(v.featsOther||[]).some(filled))m.push("Con qué cuenta tu espacio");''')
rep('''POLICY_SVCS.forEach(([sv])=>{if(!polOk(v.policy[sv]))m.push(`${sv}: si lo ofreces y si pueden traerlo`);});
  if(!v.deposit)m.push("Anticipo");''',
    '''POLICY_SVCS.forEach(([sv])=>{if(!polOk(v.policy[sv]))m.push(`${sv}: si está incluido y si pueden sustituirlo`);});if(!v.extAll)m.push("¿Pueden traer los servicios que no incluyes?");
  if(!filled(v.depositN))m.push("Anticipo");''')

# ---------- planner
func('drawPlanner', r'''
function drawPlanner(){const p=S.planner,k="pl",yrs=[];for(let y=yearNow;y>=1970;y--)yrs.push(y);
 const extra=p.specialties.filter(x=>!PLANNER_SPECS.includes(x));const ev=demo?DEMO_REV.events:0,rt=demo?DEMO_REV.rating:0;
 $("stepBody").innerHTML=`<div class="panel"><span class="crumb">Mi negocio › Mi perfil de planner</span><h2>Mi perfil de planner 📋</h2><p class="sub">Aquí los anfitriones te conocen a ti. Que se note tu personalidad.</p>
 <div class="sub-box" style="display:grid;gap:10px"><b style="font-size:14px">🏅 Tu récord en ¡Hay que vernos!</b><div class="rec"><div><b>${ev}</b><span class="hint">eventos cerrados</span></div><div><b>${rt?"⭐ "+rt:"—"}</b><span class="hint">calificación promedio</span></div><div><b>${demo?12:0}</b><span class="hint">encuestas contestadas</span></div></div>
  <div class="embs"><img src="img/b_fundador.webp" alt="Fundador"><img src="img/b_responde_ya.webp" alt="Responde ya" style="${demo?"":"filter:grayscale(1);opacity:.45"}"><img src="img/b_verificado.webp" alt="Verificado" style="${demo?"":"filter:grayscale(1);opacity:.45"}"><span class="hint">Contesta la encuesta después de cada evento y gana la insignia <b>Co-constructor</b>.</span></div></div>
 ${avatarHtml(p,"face","face","🤳 Tu foto (no tu logo)")}
 <div class="row"><div class="field"><label class="lbl" for="pl-name">Tu nombre</label><input type="text" id="pl-name" class="${MISS(filled(p.person))}" value="${esc(p.person)}"></div>
  <div class="field"><label class="lbl" for="pl-since">Organizo eventos desde</label><select id="pl-since" class="${MISS(!!p.since)}"><option value="">Año</option>${yrs.map(y=>`<option ${String(y)===String(p.since)?'selected':''}>${y}</option>`).join("")}</select></div></div>
 ${socialHtml(p,k,p.socialFromBiz?"Pusimos las redes de tu negocio. Si como planner tienes redes propias, cámbialas aquí.":"Estas redes son solo de tu perfil de planner.")}
 <div class="field"><label class="lbl" for="pl-bio">💬 Tu bio</label><span class="hint">¿No sabes por dónde empezar? Toca una idea y complétala con tus palabras.</span><div class="sugg">${BIO_SUGG.map(q=>`<button type="button" class="bs" data-q="${esc(q)}">${esc(q)}</button>`).join("")}</div>
  <textarea id="pl-bio" class="${MISS(filled(p.bio))}" rows="5" placeholder="Cuéntales quién eres y cómo trabajas">${esc(p.bio)}</textarea></div>
 <div class="field"><span class="lbl">💲 ¿Cómo cobras?</span><span class="hint">¿Tienes más de una forma de cobrar? Agrégalas todas.</span><div class="fees">${p.fees.map((f,i)=>`<div class="fee" data-i="${i}"><div class="row"><input type="number" min="0" class="fe-a${MISS(filled(f.amount))}" value="${esc(f.amount)}" placeholder="${f.unit==="porcentaje"?"%":"$"} tarifa" aria-label="Tarifa"><select class="fe-u" aria-label="Unidad">${FEE_UNITS.map(([u,t])=>`<option value="${u}" ${f.unit===u?"selected":""}>${t}</option>`).join("")}</select></div>
   ${f.unit==="otro"?`<input type="text" class="fe-o" value="${esc(f.other)}" placeholder="¿Cómo cobras? Ej. por día de evento" aria-label="Otra unidad">`:""}
   <input type="text" class="fe-n" value="${esc(f.note)}" placeholder="¿Para qué tipo o tamaño de evento? (opcional)" aria-label="Nota"><button type="button" class="link bad fe-rm" style="justify-self:start" ${p.fees.length<2?"hidden":""}>Quitar esta tarifa</button></div>`).join("")}</div>
  <button type="button" class="link" id="fe-add" style="justify-self:start">+ Otra forma de cobrar</button></div>
 <div class="row"><div class="field"><span class="lbl">💳 Anticipo para apartar</span><div class="row"><input type="number" min="0" id="pl-depn" class="${MISS(filled(p.depositN))}" value="${esc(p.depositN)}" placeholder="Ej. 30" aria-label="Anticipo"><select id="pl-depu" aria-label="Unidad"><option value="%" ${p.depositU==="%"?"selected":""}>% del total</option><option value="$" ${p.depositU==="$"?"selected":""}>pesos ($)</option></select></div></div>
  <div class="field"><span class="lbl">🤝 ¿Tus costos son negociables?</span><div class="chips${MISS(p.negotiable!==null)}" style="width:fit-content;border-radius:99px">${[[true,"Sí, se puede platicar"],[false,"Precio fijo"]].map(([val,t])=>`<button type="button" class="chip pneg" data-v="${val}" aria-pressed="${p.negotiable===val}">${TICK}${t}</button>`).join("")}</div></div></div>
 <div class="field"><span class="lbl">⭐ Me especializo en</span><div class="chips${MISS(p.specialties.length>0)}" style="border-radius:14px">${PLANNER_SPECS.concat(extra).map(t=>`<button type="button" class="chip ps" data-t="${esc(t)}" aria-pressed="${p.specialties.includes(t)}">${TICK}${esc(t)}</button>`).join("")}<button type="button" class="chip new" id="ps-new">+ Otra especialidad</button></div>
  <div style="display:flex;gap:8px" id="psw" hidden><input type="text" id="ps-in" placeholder="Escribe tu especialidad"><button type="button" class="btn sm" id="ps-add">Agregar</button></div></div>
 ${zonesHtml(p.zones,"pl","¿Dónde trabajas como planner?")}
 ${promoHtml(p.promo,k,"planner")}
 <div class="field"><span class="lbl">📷 Fotos de eventos que organizaste</span>${uploaderHtml(k,"photo",p.photos,p.photos.length>0)}</div>
 ${navHtml()}</div>`;
 const redraw=()=>{const y=scrollY;drawPlanner();scrollTo({top:y});};
 [["pl-name","person"],["pl-since","since"],["pl-bio","bio"],["pl-depn","depositN"],["pl-depu","depositU"]].forEach(([i,f])=>{$(i).oninput=$(i).onchange=e=>{p[f]=e.target.value;changed();};});
 document.querySelectorAll(".bs").forEach(b=>b.onclick=()=>{const t=$("pl-bio");t.value=(t.value.trim()?t.value.trim()+" ":"")+b.dataset.q.replace("…"," ");p.bio=t.value;t.focus();t.setSelectionRange(t.value.length,t.value.length);changed();});
 document.querySelectorAll(".fee").forEach(r=>{const f=p.fees[+r.dataset.i];r.querySelector(".fe-a").oninput=e=>{f.amount=e.target.value;ensureState();changed();};r.querySelector(".fe-u").onchange=e=>{f.unit=e.target.value;redraw();changed();};
  const o=r.querySelector(".fe-o");if(o)o.oninput=e=>{f.other=e.target.value;changed();};r.querySelector(".fe-n").oninput=e=>{f.note=e.target.value;changed();};r.querySelector(".fe-rm").onclick=()=>{p.fees.splice(+r.dataset.i,1);redraw();changed();};});
 $("fe-add").onclick=()=>{p.fees.push({amount:"",unit:"evento",other:"",note:""});redraw();changed();};
 document.querySelectorAll(".pneg").forEach(c=>c.onclick=()=>{p.negotiable=c.dataset.v==="true";redraw();changed();});
 document.querySelectorAll(".ps").forEach(c=>c.onclick=()=>{const t=c.dataset.t;p.specialties=p.specialties.includes(t)?p.specialties.filter(x=>x!==t):[...p.specialties,t];c.setAttribute("aria-pressed",p.specialties.includes(t));changed();});
 const addSp=()=>{const t=$("ps-in").value.trim();if(t&&!p.specialties.includes(t))p.specialties.push(t);redraw();changed();};
 $("ps-new").onclick=()=>{$("psw").hidden=false;$("ps-in").focus();};$("ps-add").onclick=addSp;$("ps-in").onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();addSp();}};
 bindAvatar(p,"face","face");bindSocial(p,k,redraw,()=>{p.socialFromBiz=false;});bindZones(p.zones,"pl",redraw);bindPromo(p.promo,k,redraw);bindUploader(k,"photo",p.photos,redraw);bindNav();}''')
rep('''if(!filled(p.bio))m.push("Tu bio");if(!p.prompts.some(filled))m.push("Al menos una frase");
  if(!filled(p.fee))m.push("Tarifa");''',
    '''if(!filled(p.bio))m.push("Tu bio");
  if(!(p.fees||[]).length||!p.fees.every(f=>filled(f.amount)&&(f.unit!=="otro"||filled(f.other))))m.push("Tarifa");if(!filled(p.depositN))m.push("Anticipo");if(p.negotiable===null||p.negotiable===undefined)m.push("¿Costos negociables?");''')

# ---------- sitio: banner nuevo, insignias y promedio, pestañas por vertical
rep('''out.push(`<div class="net"><img src="${BALL}" alt=""><span>Parte de la red de proveedores <b style="background:none;color:inherit;padding:0">¡Hay que vernos!</b></span><b>Crea tu sitio gratis →</b></div>`);''',
    '''out.push(`<div class="net"><img src="${BALL}" alt=""><span>¿Eres proveedor de eventos sociales o corporativos? Súmate a la red <b style="background:none;color:inherit;padding:0">¡Hay que vernos!</b></span><b>Crear mi sitio →</b></div>`);''')
rep('''<div class="ms-tags"><span class="f">⭐ Fundador</span>''',
    '''<div class="ms-emb"><img src="img/b_fundador.webp" alt="">Fundador #38${demo?`<img src="img/b_responde_ya.webp" alt="">Responde ya<img src="img/b_verificado.webp" alt="">Verificado · ⭐ ${DEMO_REV.rating} promedio`:""}</div><div class="ms-tags">${b.visits?'<span>🏪 Recibe clientes en su local</span>':""}''')
rep('''if(S.types.services){const sv=S.services.filter(s=>s.subs.length);
  out.push(`<div style="display:grid;gap:8px"><h3>🎉 Servicios</h3>''',
    '''const VT=[S.types.services&&["svc","🎉 Mis servicios"],S.types.venue&&["venue","🏡 Mi venue"],S.types.planner&&["planner","📋 Event planner"]].filter(Boolean);
 if(VT.length>1)out.push(`<div class="vtabs" role="tablist">${VT.map(([id,t],i)=>`<button type="button" role="tab" data-vt="${id}" aria-selected="${i===0}">${t}</button>`).join("")}</div>`);
 const VP=(id,html)=>`<div class="vpane" data-vp="${id}" ${VT.length>1&&VT[0][0]!==id?"hidden":""}>${html}</div>`;
 if(S.types.services){const sv=S.services.filter(s=>s.subs.length);
  out.push(VP("svc",`<div style="display:grid;gap:8px"><h3>🎉 Servicios</h3>''')
rep('''${zonesText(S.svcZones)?`<small style="color:var(--muted);font-size:12px">🗺️ Servicio en: ${esc(zonesText(S.svcZones))}</small>`:''}</div>`);}''',
    '''${zonesText(S.svcZones)?`<small style="color:var(--muted);font-size:12px">🗺️ Servicio en: ${esc(zonesText(S.svcZones))}</small>`:''}</div>`));}''')
rep('''out.push(`<div style="display:grid;gap:8px"><h3>🏡 Venue</h3><div class="ms-item">''', '''out.push(VP("venue",`<div style="display:grid;gap:8px"><h3>🏡 Venue</h3><div class="ms-item">''')
rep('''${promoBlock(v.promo,"venue")}${strip(v.photos)}</div></div>`);}''', '''${promoBlock(v.promo,"venue")}${strip(v.photos)}</div></div>`));}''')
rep('''<div><b style="font-size:15px">${esc(v.name||"Tu venue")}</b><br><small>${vt?vt[1]+" "+esc(vt[0]):''}</small></div>''',
    '''<div><b style="font-size:15px">${esc(v.name||"Tu venue")}</b><br><small>${vt?vt[1]+" "+esc(vt[0]):v.type==="__otro"?"✨ "+esc(v.typeOther):''}</small></div>''')
rep('''${v.limit?`<span>🕒 ${esc(v.open||"")}${v.open?" a ":"Hasta las "}${esc(v.limit)}</span>`:''}''',
    '''${v.sameHours===false?v.days.map(d=>{const h=v.hoursByDay[d];return h&&h.limit?`<span>🕒 ${HQV.DAYS.find(x=>x[0]===d)[1]} ${esc(h.open)}–${esc(h.limit)}</span>`:"";}).join(""):v.limit?`<span>🕒 ${esc(v.open||"")}${v.open?" a ":"Hasta las "}${esc(v.limit)}</span>`:''}${(v.featsOther||[]).filter(filled).map(x=>`<span>✨ ${esc(x)}</span>`).join("")}''')
rep('''${p.offer==="inc"?'<em class="st inc">Incluido</em>':''', '''${p.incl==="parte"?`<em class="st inc">Incluido en parte${p.detail?": "+esc(p.detail):""}</em>`:p.offer==="inc"?`<em class="st inc">Incluido${(p.subs||[]).length?": "+esc(p.subs.join(", ")):""}</em>`:''')
rep('''<span>🔐 Depósito en garantía ${money(v.guarantee)}</span>`:''}''', '''<span>🔐 Depósito en garantía ${money(v.guarantee)}${v.guarRetN?` · se devuelve en ${esc(v.guarRetN)} ${esc(v.guarRetU)}`:""}</span>`:''}${v.extAll?`<span>🚪 Proveedores externos: ${v.extAll==="si"?"sí, todos los que no se incluyen":v.extAll==="no"?"no":esc(v.extAllNote||"solo algunos")}</span>`:""}${v.cancelFile?`<span>📎 Política de cancelación (${esc(v.cancelFile.name)})</span>`:""}${v.cancelLink?`<span>🔗 Política de cancelación: ${esc(v.cancelLink)}</span>`:""}''')
rep('''out.push(`<div style="display:grid;gap:8px"><h3>📋 Event planner</h3><div class="planner-card">''', '''out.push(VP("planner",`<div style="display:grid;gap:8px"><h3>📋 Event planner</h3><div class="planner-card">''')
rep('''${PLANNER_PROMPTS.map((q,i)=>filled(p.prompts[i])?`<div class="prompt"><small>${esc(q)}</small>${esc(p.prompts[i])}</div>`:'').join("")}
   <div class="ms-item-top"><b>Coordinación de tu evento</b><span class="price">${filled(p.fee)?`${money(p.fee)} <small>por evento</small>`:'<small>Por cotizar</small>'}</span></div>${p.feeNote?`<small style="color:var(--muted)">${esc(p.feeNote)}</small>`:''}''',
    '''${socialRow(p)}<div class="ms-emb"><img src="img/b_fundador.webp" alt="">${demo?`${DEMO_REV.events} eventos cerrados · ⭐ ${DEMO_REV.rating} promedio`:"Nuevo en ¡HQV!"}</div>
   ${(p.fees||[]).filter(f=>filled(f.amount)).map(f=>`<div class="ms-item-top"><b>Coordinación${f.note?` <small style="font-weight:600;color:var(--muted)">· ${esc(f.note)}</small>`:""}</b><span class="price">${f.unit==="porcentaje"?`${esc(f.amount)}% <small>del total de la fiesta</small>`:`${money(f.amount)} <small>${f.unit==="otro"?esc(f.other):FEE_UNITS.find(x=>x[0]===f.unit)[1].toLowerCase()}</small>`}</span></div>`).join("")||'<div class="ms-item-top"><b>Coordinación de tu evento</b><span class="price"><small>Por cotizar</small></span></div>'}
   <div class="feat">${filled(p.depositN)?`<span>💳 Anticipo ${p.depositU==="%"?esc(p.depositN)+"%":money(p.depositN)}</span>`:""}${p.negotiable?'<span>🤝 Costos negociables</span>':p.negotiable===false?'<span>Precio fijo</span>':""}</div>''')
rep('''${promoBlock(p.promo,"planner")}${strip(p.photos)}</div></div></div>`);}''', '''${promoBlock(p.promo,"planner")}${strip(p.photos)}</div></div></div>`));}''')
rep('''document.body.insertAdjacentHTML("beforeend",`<datalist id="minUnits">''',
    '''document.addEventListener("click",e=>{const t=e.target.closest("[data-vt]");if(!t)return;const root=t.closest(".site,.public-site")||document;root.querySelectorAll("[data-vt]").forEach(x=>x.setAttribute("aria-selected",x===t));root.querySelectorAll("[data-vp]").forEach(x=>x.hidden=x.dataset.vp!==t.dataset.vt);hqvTrack("sitio_pestana",{v:t.dataset.vt});});
document.body.insertAdjacentHTML("beforeend",`<datalist id="minUnits">''')

# ---------- sitio publicado: imagen para redes
rep('''<button class="btn" type="button" id="toPublic">👀 Ver mi sitio como lo ven tus clientes</button>''',
    '''<button class="btn cta" type="button" id="dlSite">⬇️ Descargar imagen para redes (con QR)</button>
    <button class="btn" type="button" id="toPublic">👀 Ver mi sitio como lo ven tus clientes</button>''')
rep('''$("toPublic").onclick=()=>showPublic("published");''', '''$("toPublic").onclick=()=>showPublic("published");$("dlSite").onclick=()=>shareSite();''')
rep('''<button class="cta off" type="button" id="goProv">Empezar mi sitio gratis''', '''<button class="cta off" type="button" id="goProv">Crear mi sitio web gratis''')

DST.write_text(s)
print('reg7 ok', len(s))
