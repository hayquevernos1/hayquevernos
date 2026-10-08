"""v7 · Bloque 2 (cuenta del anfitrión). Correr DESPUÉS de patch_shell7.py. Edita shell.html en su lugar.
Fichas de fiesta con versiones, agenda compacta arriba, «Contactar proveedores» → pago personalizado,
planner elegido desde el cotizador (siguientes pasos, ¿harás equipo?, 3 opciones, $99 por 3 más o ser tu propio planner),
proveedores con «¿Quedó en tu evento?» + calificación obligatoria, encuesta por servicio con insignia, fiesta celebrada."""
import re
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()


def rep(a, b):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:110]
    s = s.replace(a, b, 1)


def func(name, new):
    """Reemplaza la función completa `name` (desde 'function name(' hasta la siguiente declaración de nivel superior)."""
    global s
    m = re.search(r'\nfunction ' + re.escape(name) + r'\(', s)
    assert m, 'NO HAY FUNCIÓN ' + name
    a = m.start() + 1
    n = re.search(r'\n(function |let |const |/\*)', s[a + 10:])
    b = a + 10 + n.start() + 1
    s = s[:a] + new.strip('\n') + '\n' + s[b:]


CSS = '''
/* v7 · cuenta del anfitrión */
.agbar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:var(--card);border-radius:22px;padding:10px 14px;box-shadow:var(--hqv-clay-sm);margin-bottom:14px}
.agbar b{font-size:14px;display:flex;gap:6px;align-items:center}
.agbar input{flex:1 1 150px;padding:8px 12px;border-radius:99px}
.agbar input[type=date]{flex:0 1 150px}
.subtabs{display:flex;gap:6px;margin-bottom:12px;flex-wrap:wrap}
.subtabs button{border:0;border-radius:99px;padding:8px 14px;font-weight:900;font-size:13.5px;background:var(--paper);box-shadow:var(--hqv-clay-sm)}
.subtabs button[aria-selected="true"]{background:var(--host);color:#fff}
.evc{background:var(--card);border-radius:24px;box-shadow:var(--hqv-clay-sm);padding:12px 14px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.evc .grow{flex:1;min-width:180px;display:grid;gap:2px}
.evc .ver{font-size:11.5px;font-weight:900;background:var(--hqv-vainilla);color:#3A2E00;border-radius:99px;padding:2px 8px;margin-left:6px}
.ico{display:flex;gap:4px}
.ico button,.ico a{border:0;background:var(--paper);border-radius:12px;width:36px;height:36px;display:grid;place-items:center;font-size:16px;box-shadow:var(--hqv-clay-sm);text-decoration:none}
.evc.done{background:var(--hqv-menta)}
.evc.agd{background:var(--paper);box-shadow:none}
.vers{display:grid;gap:8px}
.vers .evc{box-shadow:none;background:var(--paper)}
.vers .evc.cur{outline:2px solid var(--host)}
.nsteps{display:grid;gap:8px;margin:0;padding:0;list-style:none;counter-reset:n}
.nsteps li{display:grid;grid-template-columns:30px 1fr;gap:10px;align-items:start;font-size:14px}
.nsteps li::before{counter-increment:n;content:counter(n);width:30px;height:30px;border-radius:50%;background:var(--host);color:#fff;font-weight:900;display:grid;place-items:center}
.nsteps b{display:block;font-size:12px;letter-spacing:.06em}
.plcard{background:var(--paper);border-radius:22px;padding:14px;display:grid;gap:8px;touch-action:pan-y;user-select:none;transition:transform .25s}
.plcard .hd{display:flex;gap:12px;align-items:center}
.plcard .av{width:56px;height:56px;border-radius:50%;display:grid;place-items:center;font-size:30px;background:var(--card);box-shadow:var(--hqv-clay-sm);overflow:hidden}
.plcard .av img{width:100%}
.yn2{display:flex;gap:8px;flex-wrap:wrap}
.yn2 .btn{flex:1}
.rate{display:grid;gap:8px;background:var(--card);border-radius:18px;padding:12px}
.rate .stars button{font-size:24px}
.svsvc{display:grid;grid-template-columns:1fr 130px;gap:8px;align-items:center;font-size:13.5px}
.svsvc input{padding:7px 10px}
.emb{display:flex;gap:12px;align-items:center}
.emb img{width:64px}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# ---------- modelo del evento: el planner viene del cotizador
func('newEvent', r'''
function normPl(p){if(!p)return null;return{n:p.n,img:p.c?`img/c_${p.c}.webp`:null,emo:p.e||"📋",z:p.z,y:p.y,r:p.r,fee:p.fee||p.f,sp:Array.isArray(p.sp)?p.sp.join(" · "):p.sp,b:p.b||""};}
function newEvent(f){seed=Math.floor(f.total)%9973+11;const rows=(f.rows||[]).filter(r=>r.k!=="Planner"&&(r.amt>0||r.pend));
 const provs={};rows.forEach(r=>provs[r.k]=providersFor(r));const interes=Object.values(provs).reduce((a,l)=>a+l.length,0);
 const pl=normPl(f.planner);
 return{id:"e"+now(),t:now(),f,provs,interes,opts:{prov:true,planner:!!pl},paid:null,
  planner:{state:null,cur:pl,tried:[],round:1,extra:false},late:false,showAll:{},rate:{},removed:0,check:{}};}''')

# ---------- cuenta: agenda compacta siempre arriba en «Mis fiestas»
rep('''if(U.tab==="fiestas")return U.sides.fiestas?(U.eventId&&getEv()?drawEvent(p):drawFiestas(p)):drawInvite(p,"fiestas");''',
    '''if(U.tab==="fiestas"){if(!U.sides.fiestas)return drawInvite(p,"fiestas");p.insertAdjacentHTML("beforebegin",agendaBar());bindAgenda();return U.eventId&&getEv()?drawEvent(p):drawFiestas(p);}''')

func('agendaBox', r'''
function agendaBar(){return`<form class="agbar" id="agF"><b>${em("spiral_calendar")} Agenda una fecha</b><input type="text" id="agW" placeholder="¿Qué celebras? Ej. cumpleaños de mi mamá" aria-label="Qué celebras"><input type="date" id="agD" aria-label="Fecha"><button class="btn host sm" type="submit" id="agAdd">Agendar</button><span class="hint" id="agMsg" aria-live="polite" style="width:100%" hidden></span></form>`;}
function agendaBox(){return"";}''')
func('bindAgenda', r'''
function bindAgenda(){const f=$("agF");if(!f)return;f.onsubmit=ev=>{ev.preventDefault();const w=$("agW").value.trim(),d=$("agD").value;if(!w||!d){$("agMsg").hidden=false;$("agMsg").textContent="Escribe qué celebras y la fecha.";return;}U.agenda.push({w,d});track("agenda_fecha");drawAcct();toast("📅 Listo. Te avisamos "+RG.diasRecordatorio+" días antes, aquí y por correo.");};}''')

# ---------- «Mis fiestas»: fichas + fiestas celebradas + agenda + «Organizo para otros»
func('drawFiestas', r'''
function evCard(e){const f=e.f,v=(e.versions||[]).length||1,past=daysTo(f.date)<0;
 if(past&&e.surveyDone)return`<div class="evc done"><img class="em lg" src="img/e_party_popper.webp" alt=""><span class="grow"><b>🏅 Fiesta celebrada</b><span class="hint">${esc(f.nombre||f.occ)} · ${fdate(f.date)}</span></span></div>`;
 return`<div class="evc"><span class="grow" style="cursor:pointer" data-ev="${e.id}"><b>${esc(f.nombre||f.occ)}<span class="ver">v${v}</span></b><span class="hint">${esc(f.occ)} · ${f.guests} invitados · ${fdate(f.date)}</span><span class="hint">Calculada el ${new Date((e.versions&&e.versions[0]&&e.versions[0].t)||e.t||now()).toLocaleDateString("es-MX",{day:"numeric",month:"short"})} · ${money(f.total)}</span></span>
  ${evState(e)}<span class="ico"><button type="button" data-send="${e.id}" title="Reenviar a mi correo" aria-label="Reenviar">📤</button><button type="button" data-dl="${e.id}" title="Descargar PDF" aria-label="Descargar">⬇️</button><button type="button" data-del="${e.id}" title="Borrar" aria-label="Borrar">🗑️</button></span>
  <button class="btn host sm" type="button" data-ev="${e.id}">Abrir →</button></div>`;}
function drawFiestas(p){const isPl=U.site&&(U.site.tipos||[]).includes("planner");U.sub=U.sub||"mias";
 const mine=U.events.slice().sort((a,b)=>(a.f.nombre||a.f.occ).localeCompare(b.f.nombre||b.f.occ)||b.t-a.t),celebradas=U.events.filter(e=>daysTo(e.f.date)<0&&e.surveyDone).length;
 p.innerHTML=`${isPl?`<div class="subtabs" role="tablist"><button type="button" role="tab" data-sub="mias" aria-selected="${U.sub==="mias"}">🎉 Mis fiestas</button><button type="button" role="tab" data-sub="otros" aria-selected="${U.sub==="otros"}">📋 Organizo para otros</button></div>`:""}
 ${U.sub==="otros"&&isPl?`<div class="box"><h2>${em("magic_wand")} Fiestas que organizo</h2><span class="hint">Las fiestas de tus clientes, después de que aceptaste y ambos confirmaron el trato.</span>
   <div class="list">${(U.plannerJobs||[]).map(j=>`<div class="evc"><span class="grow"><b>${esc(j.nombre)}</b><span class="hint">Cliente: ${esc(j.cliente)} · ${j.guests} invitados · ${fdate(j.date)}</span><span class="hint">Pre-cotización: ${money(j.total)} · cobraste ${money(j.cobro||0)}</span></span><span class="st go">En progreso</span></div>`).join("")||'<span class="hint">Cuando aceptes a un cliente en Mi negocio, su fiesta aparece aquí.</span>'}</div></div>`:
 `<div class="box"><h2>${em("party_popper")} Mis fiestas</h2><span class="hint">Tus pre-cotizaciones se guardan aquí con sus versiones. Se borran solas un día después de cada fiesta.</span>
   <div class="list">${mine.map(evCard).join("")||'<span class="hint">Aún no tienes fiestas.</span>'}</div>
   ${celebradas?`<span class="hint">🏅 ${celebradas} ${celebradas===1?"fiesta celebrada":"fiestas celebradas"} con ¡Hay que vernos!</span>`:""}
   <button class="btn host" type="button" id="newEv">＋ Pre-cotizar otra fiesta</button></div>
  ${U.agenda.length?`<div class="box"><h3>${em("spiral_calendar")} Fechas agendadas</h3><div class="list">${U.agenda.map(x=>`<div class="evc agd"><img class="em lg" src="img/e_birthday_cake.webp" alt=""><span class="grow"><b>${esc(x.w)}</b><span class="hint">${fdate(x.d)} · te avisamos ${RG.diasRecordatorio} días antes</span></span><button class="btn ghost sm" type="button" data-agq="${esc(x.w)}">Pre-cotizar</button></div>`).join("")}</div></div>`:""}`}`;
 p.querySelectorAll("[data-sub]").forEach(b=>b.onclick=()=>{U.sub=b.dataset.sub;drawAcct();});
 p.querySelectorAll("[data-ev]").forEach(b=>b.onclick=()=>{U.eventId=b.dataset.ev;drawAcct();});
 p.querySelectorAll("[data-send]").forEach(b=>b.onclick=()=>toast("📤 Te la reenviamos a tu correo."));
 p.querySelectorAll("[data-dl]").forEach(b=>b.onclick=()=>toast("⬇️ En el sitio real aquí se descarga el PDF."));
 p.querySelectorAll("[data-del]").forEach(b=>b.onclick=()=>{U.events=U.events.filter(x=>x.id!==b.dataset.del);toast("🗑️ Pre-cotización borrada");drawAcct();});
 p.querySelectorAll("[data-agq]").forEach(b=>b.onclick=()=>openJourney("fiestas",true));
 const n=$("newEv");if(n)n.onclick=()=>openJourney("fiestas",true);}''')
func('evState', r'''
function evState(e){if(daysTo(e.f.date)<0)return e.surveyDone?'<span class="st go">Celebrada ✓</span>':'<span class="st wait">Cuéntanos cómo te fue</span>';if(!e.paid)return'<span class="st new">Pre-cotizada</span>';const s=e.planner.state;if(e.paid==="prov"||s==="liberado"||s==="propio")return'<span class="st go">Organizando</span>';return'<span class="st wait">Con tu planner</span>';}''')

# ---------- detalle de una fiesta
func('drawEvent', r'''
function drawEvent(p){const e=getEv(),f=e.f;const past=daysTo(f.date)<0;e.versions=e.versions||[{f,t:e.t||now()}];
 p.innerHTML=`<button class="pill sm" type="button" id="evBack">← Mis fiestas</button>
 <div class="grid2">
  <div style="display:grid;gap:16px;min-width:0">
   <div class="hero"><small>${esc(f.nombre||f.occ)} · ${f.guests.toLocaleString("es-MX")} invitados · ${fdate(f.date)} · ${f.hours} h</small>
    <span class="big">${money(f.pp)}</span><span>por persona</span><span class="tt">Total aproximado: ${money(f.total)}</span></div>
   <div class="box"><h3>${em("spiral_calendar")} Versiones de tu pre-cotización</h3><span class="hint">Cada vez que recalculas guardamos una versión nueva. Se borran solas un día después de tu fiesta.</span>
    <div class="vers">${e.versions.map((v,i)=>`<div class="evc ${i===0?"cur":""}"><span class="grow"><b>Versión ${e.versions.length-i}${i===0?" · actual":""}</b><span class="hint">${new Date(v.t).toLocaleDateString("es-MX",{day:"numeric",month:"short",hour:"2-digit",minute:"2-digit"})} · ${money(v.f.total)} · ${v.f.guests} invitados</span></span>
     <span class="ico"><button type="button" data-vs="${i}" aria-label="Reenviar">📤</button><button type="button" data-vd="${i}" aria-label="Descargar">⬇️</button>${e.versions.length>1?`<button type="button" data-vx="${i}" aria-label="Borrar">🗑️</button>`:""}</span></div>`).join("")}</div>
    <button class="btn ghost sm" type="button" id="evEdit" style="justify-self:start">🔄 Recalcular (crea una versión nueva)</button></div>
   <div class="box"><h3>Así se reparte</h3><div class="brk">${f.rows.map(r=>`<div><span>${r.e} ${esc(r.label)}</span><span>${r.pend?"Por cotizar":money(r.amt)}</span></div>`).join("")}</div></div>
   ${past?"":`<button class="sim" type="button" id="evPast" style="justify-self:start">Simular: ya pasó mi fiesta</button>`}
  </div>
  <div style="display:grid;gap:16px;min-width:0" id="evRight"></div>
 </div>`;
 $("evBack").onclick=()=>{U.eventId=null;drawAcct();};$("evEdit").onclick=()=>openJourney("fiestas",true,e.id);
 p.querySelectorAll("[data-vs]").forEach(b=>b.onclick=()=>toast("📤 Te reenviamos esta versión a tu correo."));
 p.querySelectorAll("[data-vd]").forEach(b=>b.onclick=()=>toast("⬇️ En el sitio real aquí se descarga el PDF."));
 p.querySelectorAll("[data-vx]").forEach(b=>b.onclick=()=>{e.versions.splice(+b.dataset.vx,1);e.f=e.versions[0].f;drawAcct();});
 const ep=$("evPast");if(ep)ep.onclick=()=>{f.date=new Date(now()-864e5).toISOString().slice(0,10);inbox("fiestas",`🎉 ¿Cómo te fue en «${f.nombre||f.occ}»? Cuéntanos y gana tu insignia.`);drawAcct();};
 const R=$("evRight");
 if(past){R.innerHTML=e.surveyDone?`<div class="box" style="background:var(--hqv-menta)"><h2>${em("glowing_star")} ¡Gracias por contarnos!</h2><span>Ganaste la insignia <b>Co-constructor ¡HQV!</b> y créditos para tu próxima fiesta. Tu información ayuda a que todos calculemos mejor.</span></div>`:surveyBox(e);bindSurvey(e);return;}
 if(!e.paid){R.innerHTML=interestBox(e,true);const c=$("contact");if(c)c.onclick=()=>startPay(e);return;}
 if(e.paid==="planner"&&!["liberado","propio"].includes(e.planner.state)){R.innerHTML=plannerBox(e)+interestBox(e,false);bindPlanner(e);return;}
 R.innerHTML=(e.planner.state==="liberado"?plannerBox(e):"")+provListBox(e,e.planner.state==="liberado")+(e.planner.state==="propio"||e.paid==="prov"?`<div class="box"><h3>${em("magic_wand")} ¿Quieres un event planner?</h3><span class="hint">Puedes sumar a uno cuando quieras. Conoce 3 perfiles por ${money(PR.plannerDespues)}; cuando ambos confirmen el trato, le liberamos tus proveedores.</span><button class="btn ghost" type="button" id="late">Conocer event planners · ${money(PR.plannerDespues)}</button></div>`:"");
 if(e.planner.state==="liberado")bindPlanner(e);bindProvList(e);const l=$("late");if(l)l.onclick=()=>startPay(e,"late");}''')

func('interestBox', r'''
function interestBox(e,pre){const ks=Object.keys(e.provs),pl=e.opts.planner&&e.planner.cur;
 return`<div class="box"><h2>${em("star-struck")} ${e.interes} proveedores interesados</h2><span class="hint">Cerca de ti y disponibles para tu fecha. ${pre?"Sus datos se muestran al contactarlos.":"Se liberan cuando tu planner confirme el trato."}</span>
 <div class="int">${ks.map(k=>`<div class="ln"><span>${e.provs[k][0].emo} ${esc(k)}</span><span class="st vis">${e.provs[k].length} interesados</span></div>`).join("")}</div>
 <div class="list">${ks.slice(0,2).map(k=>e.provs[k].slice(0,2).map((x,i)=>provCard(x,i,true,e)).join("")).join("")}</div>
 ${pre?`<button class="btn host" type="button" id="contact" style="justify-self:stretch">${pl?`Contactar a ${esc(first(pl.n))} + proveedores →`:"Contactar proveedores →"}</button><span class="hint" style="text-align:center">Pago único: ${money(pl?PR.proveedoresMasPlanner:PR.desbloquearProveedores)}</span>`:`<div class="lock">${em("locked")}<span>Tu planner y tú los verán al mismo tiempo.</span></div>`}</div>`;}''')

# ---------- tarjeta de proveedor: ¿quedó en tu evento? + calificación obligatoria
func('provCard', r'''
function provCard(x,i,blur,e){const wa=`https://wa.me/525500000000?text=${encodeURIComponent(`Hola, vi tu perfil en ¡Hay que vernos! Este anfitrión cotiza con ${Math.max(0,daysTo(e.f.date))} días de anticipación para conseguir precios preferentes.`)}`;
 const key=x.nm,r=(e.rate||{})[key];
 return`<div class="prov"><div class="tp"><span class="av">${x.emo}</span><span class="grow" style="flex:1;min-width:0"><span class="rk">#${i+1} en compatibilidad${x.nuevo?" · Nuevo":""}</span><b class="${blur?"blur":""}">${esc(x.nm)}</b></span><b>${x.price==null?"Por cotizar":money(x.price)}</b></div>
 <div class="why"><span>📍 a ${x.km} km</span><span>⚡ responde en ${x.resp<60?x.resp+" min":Math.round(x.resp/60)+" h"}</span><span>⭐ ${x.rate} (${x.rev})</span>${x.fit>.8?"<span>✅ dentro de tu presupuesto</span>":""}${x.badges.map(b=>`<span><img src="img/b_${b}.webp" alt=""> ${{fundador:"Fundador",verificado:"Verificado",responde_ya:"Responde ya"}[b]}</span>`).join("")}</div>
 ${blur?"":`<div class="row"><a class="btn wa sm" href="${wa}" target="_blank" rel="noopener">💬 WhatsApp</a><span class="hint">¿Quedó en tu evento?</span><span class="yn2" style="flex:0 0 auto"><button class="btn sm ${r&&r.sel===true?"host":"ghost"}" type="button" data-sel="${esc(key)}|1">Sí</button><button class="btn sm ${r&&r.sel===false?"host":"ghost"}" type="button" data-sel="${esc(key)}|0">No</button></span></div>
  ${r&&r.sel!=null&&!r.done?`<div class="rate"><b>Califica a ${esc(x.nm)}</b><div class="stars">${[1,2,3,4,5].map(n=>`<button type="button" data-rs="${esc(key)}|${n}" aria-pressed="${(r.stars||0)>=n}" aria-label="${n} estrellas">⭐</button>`).join("")}</div>
   <div class="chips">${["Contratado","Cotizamos pero no cerramos","No respondió","Otro"].map(t=>`<button class="chip" type="button" data-rst="${esc(key)}|${t}" aria-pressed="${r.st===t}">${t}</button>`).join("")}</div>
   <input type="text" data-rpub="${esc(key)}" value="${esc(r.pub||"")}" placeholder="Comentario público (aparece en su sitio)">
   <input type="text" data-rpri="${esc(key)}" value="${esc(r.pri||"")}" placeholder="Comentario privado (solo lo ve el proveedor)">
   <button class="btn host sm" type="button" data-rok="${esc(key)}">Guardar calificación</button></div>`:""}
  ${r&&r.done?`<span class="st go" style="justify-self:start">✓ Calificado · ${"⭐".repeat(r.stars)}</span>`:""}`}</div>`;}''')
func('provListBox', r'''
function provListBox(e,withPlanner){const ks=Object.keys(e.provs),N=RG.proveedoresVisiblesPorServicio,pl=e.planner.cur;
 return`<div class="box"><h2>${em("handshake")} Tus proveedores</h2><span class="hint">${withPlanner&&pl?`${esc(first(pl.n))} también ve estos contactos y les dará seguimiento.`:"Ordenados para ti: cercanía, presupuesto, calificación, insignias y rapidez."} Cuando platiques con cada uno, dinos si quedó en tu evento y califícalo.</span>
 ${e.removed?`<span class="hint">🗂️ ${e.removed} ${e.removed===1?"proveedor descartado y calificado":"proveedores descartados y calificados"}.</span>`:""}
 ${ks.map(k=>{const l=e.provs[k],all=e.showAll[k];if(!l.length)return"";return`<div class="svc-h"><h3>${l[0].emo} ${esc(k)}</h3><span class="hint">${l.length} interesados</span></div>
  <div class="list">${l.slice(0,all?l.length:Math.min(N,3)).map((x,i)=>provCard(x,i,false,e)).join("")}</div>
  ${l.length>3&&!all?`<button class="pill sm" type="button" data-all="${esc(k)}">Ver a los ${l.length} interesados →</button>`:""}`;}).join("")}</div>`;}''')
func('bindProvList', r'''
function bindProvList(e){e.rate=e.rate||{};const R=k=>e.rate[k]=e.rate[k]||{};
 document.querySelectorAll("[data-all]").forEach(b=>b.onclick=()=>{e.showAll[b.dataset.all]=true;drawAcct();});
 document.querySelectorAll("[data-sel]").forEach(b=>b.onclick=()=>{const[k,v]=b.dataset.sel.split("|");Object.assign(R(k),{sel:v==="1",done:false});drawAcct();});
 document.querySelectorAll("[data-rs]").forEach(b=>b.onclick=()=>{const[k,n]=b.dataset.rs.split("|");R(k).stars=+n;b.parentNode.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",+x.dataset.rs.split("|")[1]<=+n));});
 document.querySelectorAll("[data-rst]").forEach(b=>b.onclick=()=>{const[k,t]=b.dataset.rst.split("|");R(k).st=t;b.parentNode.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",x===b));});
 document.querySelectorAll("[data-rpub]").forEach(i=>i.oninput=()=>{R(i.dataset.rpub).pub=i.value;});
 document.querySelectorAll("[data-rpri]").forEach(i=>i.oninput=()=>{R(i.dataset.rpri).pri=i.value;});
 document.querySelectorAll("[data-rok]").forEach(b=>b.onclick=()=>{const k=b.dataset.rok,r=R(k);if(!r.stars||!r.st){toast("⭐ Pon estrellas y cómo quedó la conversación");return;}r.done=true;
  track("proveedor_calificado",{seleccionado:r.sel,estrellas:r.stars,estatus:r.st});
  if(r.sel===false){Object.keys(e.provs).forEach(c=>{e.provs[c]=e.provs[c].filter(x=>x.nm!==k);});e.removed=(e.removed||0)+1;toast("🗂️ Gracias. Le avisamos al proveedor y lo quitamos de tu lista.");}
  else toast("🎉 ¡Listo! Le avisamos al proveedor.");drawAcct();});}''')
s = s.replace('${!e.paid||e.paid==="prov"?checklistBox(e):""}', '')

# ---------- event planner: siguientes pasos, ¿harás equipo?, 3 opciones, $99 por 3 más o ser tu propio planner
func('plannerBox', r'''
function plCardHtml(p,extra=""){return`<div class="plcard" id="plcard"><div class="hd"><span class="av">${p.img?`<img src="${p.img}" alt="">`:p.emo}</span><span style="flex:1;min-width:0"><b style="font-size:17px">${esc(p.n)}</b><span class="hint" style="display:block">⭐ ${p.r} · ${p.y} años · ${esc(p.z||"")}</span></span><b>Desde ${money(p.fee)}</b></div>${p.b?`<span>${esc(p.b)}</span>`:""}<span class="hint">${esc(p.sp||"")}</span>${extra}</div>`;}
function plPool(e){const t=e.planner.tried.map(x=>x.n);return PLANNERS.map(normPl).filter(p=>!t.includes(p.n)&&(!e.planner.cur||p.n!==e.planner.cur.n));}
function plannerBox(e){const P=e.planner,pk=P.cur,H=RG.horasRespuestaPlanner,usados=P.tried.length%3,quedan=3-usados;
 const pasos=`<ol class="nsteps"><li><span><b>CONTACTO</b>Tu event planner te contactará por WhatsApp en menos de ${H} h para platicar la pre-cotización y negociar entre ustedes.</span></li><li><span><b>CONFIRMACIÓN</b>Después de platicar, dinos si quieres o no hacer equipo con él o ella. Tienes 3 opciones en total.</span></li><li><span><b>ACCIÓN</b>Cuando tengamos su confirmación, les liberamos los contactos de los proveedores a los dos.</span></li></ol>`;
 let body="";const st=P.state||"esperando";
 if(st==="esperando")body=`${pasos}${plCardHtml(pk)}<button class="sim" type="button" id="sOk">Simular: ${esc(first(pk.n))} te escribió por WhatsApp</button>`;
 if(st==="decidir")body=`${plCardHtml(pk)}<b>¿Harás equipo con ${esc(first(pk.n))}?</b><div class="yn2"><button class="btn host" type="button" id="pYes">Sí, trabajaremos juntos</button><button class="btn ghost" type="button" id="pNo">No, quiero otra opción</button></div><span class="hint">Te ${quedan===1?"queda 1 opción":`quedan ${quedan} opciones`} de esta ronda.</span>`;
 if(st==="confirmando")body=`${plCardHtml(pk)}<div class="soft"><b>Perfecto.</b><span>Una vez que tu event planner nos confirme el trato, liberaremos el contacto de los proveedores.</span></div><button class="sim" type="button" id="sConf">Simular: ${esc(first(pk.n))} confirmó el trato</button>`;
 if(st==="elige"){const pool=plPool(e);P.idx=(P.idx||0)%Math.max(1,pool.length);const c=pool[P.idx];
  body=c?`<span class="hint">Elige a otra persona. Desliza o usa los botones.</span>${plCardHtml(c)}<div class="yn2"><button class="btn ghost" type="button" id="plNext">✕ Siguiente</button><button class="btn host" type="button" id="plPick">💙 Elegir</button></div>`:`<span class="hint">Ya no hay más perfiles disponibles en tu zona.</span>`;}
 if(st==="agotado")body=`<div class="soft"><b>Ya conociste a tus 3 opciones.</b><span>¿Quieres conocer 3 perfiles más o prefieres ser tu propio event planner?</span></div><div class="yn2"><button class="btn host" type="button" id="plMore">Ver 3 perfiles más · ${money(PR.plannerDespues)}</button><button class="btn ghost" type="button" id="plOwn">Yo organizo</button></div><span class="hint">Si organizas tú, te liberamos tus proveedores ahora y la invitación a contratar un planner queda abierta.</span>`;
 if(st==="liberado")body=`${plCardHtml(pk,`<span class="st go" style="justify-self:start">Hicieron equipo · ya ve a tus proveedores</span>`)}`;
 return`<div class="box"><h2>${em("magic_wand")} ${st==="esperando"?"Siguientes pasos":"Tu event planner"}</h2>${body}</div>`;}''')
func('bindPlanner', r'''
function bindPlanner(e){const P=e.planner;clearInterval(pTick);const on=(id,fn)=>{const b=$(id);if(b)b.onclick=fn;};const nm=()=>first(P.cur.n);
 on("sOk",()=>{P.state="decidir";inbox("fiestas",`💬 1. CONTACTO: ${P.cur.n} te escribió por WhatsApp.`);drawAcct();});
 on("pYes",()=>{P.state="confirmando";track("planner_equipo",{si:true});inbox("fiestas",`🤝 2. CONFIRMACIÓN: le preguntamos a ${P.cur.n} para cerrar el trato.`);drawAcct();});
 on("pNo",()=>{P.tried.push(P.cur);track("planner_equipo",{si:false});P.cur=null;P.idx=0;P.state=P.tried.length%3===0?"agotado":"elige";drawAcct();});
 on("sConf",()=>{P.state="liberado";track("proveedores_liberados",{via:"planner"});inbox("fiestas",`🔓 3. ACCIÓN: liberamos tus proveedores para ti y para ${P.cur.n}.`);confetti();drawAcct();});
 on("plNext",()=>{P.idx=(P.idx||0)+1;drawAcct();});
 on("plPick",()=>{const c=plPool(e)[P.idx||0];P.cur=c;P.state="esperando";inbox("fiestas",`📋 Le avisamos a ${c.n}. Te escribirá en menos de ${RG.horasRespuestaPlanner} h.`);drawAcct();});
 on("plMore",()=>startPay(e,"more"));
 on("plOwn",()=>{P.state="propio";e.opts.planner=false;track("propio_planner");inbox("fiestas","🔓 Eres tu propio planner: ya puedes contactar a tus proveedores.");confetti();drawAcct();});
 const cd=$("plcard");if(cd&&$("plNext")){let x0=null;cd.onpointerdown=ev=>{x0=ev.clientX;cd.setPointerCapture(ev.pointerId);};cd.onpointermove=ev=>{if(x0!==null)cd.style.transform=`translateX(${ev.clientX-x0}px) rotate(${(ev.clientX-x0)/20}deg)`;};
  cd.onpointerup=ev=>{const dx=ev.clientX-(x0??ev.clientX);x0=null;cd.style.transform="";if(dx>90)$("plPick").click();else if(dx<-90)$("plNext").click();};}}''')

# ---------- pago con título según lo que eligió
func('payModal', r'''
function payModal(e,kind){const pl=e.opts.planner&&e.planner.cur;
 const amt=kind==="late"||kind==="more"?PR.plannerDespues:pl?PR.proveedoresMasPlanner:PR.desbloquearProveedores;
 const what=kind==="more"?"3 perfiles más de event planner":kind==="late"?"Conoce event planners":pl?"Contactos de Event Planner + Proveedores":"Contacto de proveedores";
 const m=$("modal");let method="Tarjeta";
 const draw=()=>{m.innerHTML=`<div class="sheet"><h2>${em("locked")} ${esc(what)}</h2>
  <div class="soft"><span class="row" style="justify-content:space-between"><b>${esc(e.f.nombre||e.f.occ)}</b><b>${money(amt)}</b></span><span class="hint">${fdate(e.f.date)} · ${e.f.guests} invitados${pl&&!kind?` · con ${esc(pl.n)}`:""}</span></div>
  <div class="field"><span class="l">¿Cómo quieres pagar?</span><div class="chips">${["Tarjeta","Transferencia","OXXO"].map(x=>`<button class="chip" type="button" data-m="${x}" aria-pressed="${x===method}">${x}</button>`).join("")}</div></div>
  <div class="soft hint">En el prototipo no se piden ni se guardan datos de pago. En el sitio real esta parte la procesa una pasarela de pagos certificada.</div>
  <button class="btn host" type="button" id="doPay">Pagar ${money(amt)} (simulado)</button><button class="pill sm" type="button" id="pX">Cancelar</button></div>`;
  m.querySelectorAll("[data-m]").forEach(b=>b.onclick=()=>{method=b.dataset.m;draw();});$("pX").onclick=()=>m.hidden=true;
  $("doPay").onclick=()=>{m.hidden=true;track("pago",{tipo:kind||(pl?"planner":"prov"),monto:amt});
   if(kind==="more"){e.planner.state="elige";e.planner.idx=0;inbox("fiestas","📋 Elige entre 3 perfiles nuevos de event planner.");}
   else if(kind==="late"){e.late=true;e.paid="planner";e.opts.planner=true;e.planner.state="elige";e.planner.idx=0;inbox("fiestas","📋 Elige a tu event planner.");}
   else{e.paid=pl?"planner":"prov";if(pl){e.planner.state="esperando";inbox("fiestas",`📋 Le avisamos a ${pl.n} con el total de tu pre-cotización (${money(e.f.total)}). Te escribirá en menos de ${RG.horasRespuestaPlanner} h.`);}else inbox("fiestas","🔓 Ya puedes contactar a tus proveedores.");}
   confetti();toast("✅ Pago recibido. ¡Gracias!");drawAcct();};};
 draw();m.hidden=false;}''')

# ---------- encuesta post-fiesta: costo real por servicio + insignia
func('surveyBox', r'''
function surveyBox(e){const f=e.f;const svcs=(f.servicios&&f.servicios.length?f.servicios.flatMap(c=>c.subs.map(x=>({k:c.cat,n:x.n,est:x.estimado}))):f.rows.filter(r=>r.k!=="Venue").map(r=>({k:r.k,n:r.label,est:r.amt}))).slice(0,8);
 const v=e.sv||(e.sv={real:Object.fromEntries(svcs.map(x=>[x.n,x.est||""])),fit:{},stars:0,note:""});
 return`<div class="box" id="svBox" style="background:var(--hqv-vainilla)"><h2>${em("party_popper")} ¿Cómo te fue en tu fiesta?</h2>
  <div class="emb"><img src="img/b_fundador.webp" alt=""><span class="hint">Cuéntanos lo que realmente pagaste por cada servicio y gana la insignia <b>Co-constructor ¡HQV!</b> y créditos para tu próxima fiesta. Con tus datos, todos calculamos mejor.</span></div>
  <div class="svq"><b>💸 ¿Cuánto pagaste por cada servicio?</b><span class="hint">Ya pusimos nuestro cálculo; corrígelo si fue distinto.</span>
   ${svcs.map(x=>`<div class="svsvc"><span>${esc(x.n)}</span><input type="number" min="0" data-real="${esc(x.n)}" value="${esc(v.real[x.n])}" aria-label="Pagado por ${esc(x.n)}"></div>`).join("")}
   <div class="svsvc"><b>Total</b><b id="svTot">${money(Object.values(v.real).reduce((a,b)=>a+(+b||0),0))}</b></div></div>
  ${svcs.slice(0,4).map(x=>`<div class="svq"><b>¿Alcanzó ${esc(x.n.toLowerCase())}?</b><div class="seg" data-fit="${esc(x.n)}">${FIT.map(([k,t])=>`<button type="button" data-v="${k}" aria-pressed="${v.fit[x.n]===k}">${t}</button>`).join("")}</div></div>`).join("")}
  <div class="svq"><b>⭐ ¿Cómo calificas tu fiesta en general?</b><div class="stars">${[1,2,3,4,5].map(n=>`<button type="button" data-st="${n}" aria-pressed="${v.stars>=n}" aria-label="${n} estrellas">⭐</button>`).join("")}</div>
   <input type="text" id="svNote" value="${esc(v.note)}" placeholder="¿Algo que debamos saber? (opcional)"></div>
  <button class="btn host" type="button" id="svSend">Enviar y ganar mi insignia</button></div>`;}''')
func('bindSurvey', r'''
function bindSurvey(e){const v=e.sv,b=$("svBox");if(!b)return;
 b.querySelectorAll("[data-real]").forEach(i=>i.oninput=()=>{v.real[i.dataset.real]=+i.value||0;$("svTot").textContent=money(Object.values(v.real).reduce((a,x)=>a+(+x||0),0));});
 $("svNote").oninput=x=>{v.note=x.target.value;};
 b.querySelectorAll("[data-fit]").forEach(g=>g.querySelectorAll("button").forEach(x=>x.onclick=()=>{v.fit[g.dataset.fit]=x.dataset.v;g.querySelectorAll("button").forEach(y=>y.setAttribute("aria-pressed",y===x));}));
 b.querySelectorAll("[data-st]").forEach(x=>x.onclick=()=>{v.stars=+x.dataset.st;b.querySelectorAll("[data-st]").forEach(y=>y.setAttribute("aria-pressed",+y.dataset.st<=v.stars));});
 $("svSend").onclick=()=>{if(!v.stars){toast("⭐ Califica tu fiesta para enviar");return;}e.surveyDone=true;const real=Object.values(v.real).reduce((a,x)=>a+(+x||0),0);
  track("encuesta_post_fiesta",{occ:e.f.occ,invitados:e.f.guests,estimado:e.f.total,real,diferencia_pct:e.f.total?Math.round((real-e.f.total)/e.f.total*100):0,por_servicio:v.real,alcanzo:v.fit,estrellas:v.stars});
  U.hostBadge=true;inbox("fiestas","🏅 Ganaste la insignia Co-constructor ¡HQV! y créditos para tu próxima fiesta.");confetti();drawAcct();};}''')

# ---------- demo: planner en una fiesta y un trabajo como planner
rep('''const pe=newEvent(past);pe.paid="prov";U.events=[newEvent(f),pe];''',
    '''f.nombre="El cumple 40 de Diego";f.planner={n:"Ana",e:"👩🏻",z:"CDMX sur",y:9,r:4.9,f:6000,sp:["Bodas pequeñas","Cumpleaños"],b:"Ex coordinadora de hotel. Me obsesionan los tiempos y que nadie note el estrés."};past.nombre="Baby shower de Sofi";
 const pe=newEvent(past);pe.paid="prov";const fe=newEvent(f);fe.versions=[{f,t:now()-2*864e5}];U.events=[fe,pe];
 U.plannerJobs=[{nombre:"Los XV de Valeria",cliente:"Laura M.",guests:150,date:new Date(now()+60*864e5).toISOString().slice(0,10),total:186000,cobro:12000}];''')
P.write_text(s)
print('shell8 ok', len(s))
