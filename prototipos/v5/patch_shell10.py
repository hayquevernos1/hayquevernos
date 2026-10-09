"""v8 · Vuelta 1 · Cuenta del anfitrión (comentarios de Diego en Miro, 8 oct 2026 noche).
Correr DESPUÉS de patch_shell9.py. Edita shell.html en su lugar.
- «Mis fiestas» en tres tiempos: Por celebrar (agenda) · En proceso (fichas con versiones Ver/Descargar/✕ y
  «Descripción del proyecto» al lado en web, debajo de la ficha en celular) · Celebradas (récord + insignias).
- Subsecciones «Mis fiestas personales» / «Las fiestas de mis clientes» para event planners.
- Invitaciones: en azul para pre-cotizar (si no hay fiestas) y en morado para abrir tu negocio (si no hay negocio).
- Planner: perfil completo al tocar su foto, animación de deslizar, aviso de confirmación, planner como contacto principal.
- Proveedores: «¿Quedó en tu evento?» Sí → seleccionado (se califica un día después) · No → motivos de selección múltiple + comentario.
- Encuesta post-fiesta solo para seleccionados (incluido el planner).
- Botones de conversión en verde. Cuenta: nombre + apellidos, copy nuevo; bienvenida con «Continuar». Pro $99 / $1,069."""
import re
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:110]
    s = s.replace(a, b, count)


def func(name, new):
    global s
    ms = list(re.finditer(r'\nfunction ' + re.escape(name) + r'\(', s))
    assert ms, 'NO HAY FUNCIÓN ' + name
    m = ms[-1]
    a = m.start() + 1
    n = re.search(r'\n(function |let |const |/\*)', s[a + 10:])
    b = a + 10 + n.start() + 1
    s = s[:a] + new.strip('\n') + '\n' + s[b:]


CSS = '''
/* ===== v8 · cuenta ===== */
:root{--cta:#0E8F45;--cta-d:#0B7639}
.btn.cta{background:var(--cta)!important;color:#fff!important;box-shadow:0 8px 18px rgba(14,143,69,.28)}
.btn.cta:hover{background:var(--cta-d)!important}
.fhead{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px}
.fhead h2{font-size:clamp(22px,3vw,28px)}
.tsec{display:grid;gap:12px;margin-top:22px}
.tlab{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;font-size:18px;font-weight:900;margin:0}
.tlab .hint{font-weight:600}
.tsec .agbar{margin:0}
.fgrid{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:18px;align-items:start}
.flist{display:grid;gap:12px;align-content:start}
.fch{background:var(--card);border-radius:24px;box-shadow:var(--hqv-clay-sm);overflow:hidden;outline:3px solid transparent;transition:outline-color .2s}
.fch.on{outline-color:var(--host)}
.fch .fh{background:var(--host);color:#fff;padding:14px 16px;display:grid;gap:2px;cursor:pointer;position:relative}
.fch .fh small{font-size:12px;opacity:.92}
.fch .fh .n{display:flex;align-items:baseline;gap:8px}
.fch .fh .n b{font-size:30px;font-weight:900;line-height:1.05}
.fch .fh .st{position:absolute;top:12px;right:12px}
.fch .fv{display:grid;gap:6px;padding:10px 12px 12px}
.vr{display:flex;align-items:center;gap:8px;background:var(--paper);border-radius:14px;padding:8px 10px}
.vr .grow{flex:1;min-width:0;display:grid}
.vr .grow small{color:var(--muted);font-size:12px}
.vr .ico button{width:auto;min-width:34px;padding:0 10px;height:32px;font-size:13px;font-weight:800}
.fdet{display:grid;gap:14px;align-content:start}
.fdet .dtitle{font-size:12px;font-weight:900;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}

@media (max-width:860px){.fgrid{grid-template-columns:1fr}.flist .fdet{background:var(--paper);border-radius:22px;padding:12px;margin-top:-4px}}
.donec{display:flex;gap:12px;align-items:center;background:var(--hqv-menta);border-radius:20px;padding:12px 14px}
.donec .grow{flex:1;display:grid}
.empty{display:grid;justify-items:start;gap:8px;background:var(--paper);border-radius:20px;padding:14px}
.why{display:flex;flex-wrap:wrap;gap:6px}
.why .chip{font-size:12.5px}
.contact-note{display:flex;gap:10px;align-items:flex-start;background:var(--hqv-cielo);color:#00283A;border-radius:18px;padding:12px 14px;font-size:14px}
.plcard .av{cursor:pointer}
.plcard.hint-anim{animation:plcHint 2.4s ease-in-out 2 .6s}
@keyframes plcHint{0%,100%{transform:none}15%{transform:translateX(26px) rotate(3deg)}30%{transform:none}45%{transform:translateX(-26px) rotate(-3deg)}60%{transform:none}}
@media (prefers-reduced-motion:reduce){.plcard.hint-anim{animation:none}}
.swl{display:flex;justify-content:space-between;font-size:12px;font-weight:900;color:var(--muted)}
.doc{background:#fff;color:#1a1033;border-radius:10px;box-shadow:0 2px 0 #e7e3f3,0 18px 40px rgba(30,20,90,.18);padding:26px 24px;display:grid;gap:12px;max-width:560px;width:100%;text-align:left;font-size:13.5px}
.doc .dh{display:flex;justify-content:space-between;align-items:center;gap:10px;border-bottom:2px solid #efeaff;padding-bottom:10px}
.doc .dh img{height:40px}
.doc table{width:100%;border-collapse:collapse}
.doc td{padding:6px 0;border-bottom:1px solid #f0edf7;vertical-align:top}
.doc td:last-child{text-align:right;white-space:nowrap}
.doc .tot{display:flex;justify-content:space-between;font-weight:900;font-size:16px}
.doc .pp{font-size:28px;font-weight:900;color:var(--host)}
.doc .foot{font-size:11px;color:#6b6585}
.sheet.wide{max-width:640px}
.ppf{display:grid;gap:12px;text-align:left}
.ppf .top{display:flex;gap:14px;align-items:center}
.ppf .top .av{width:84px;height:84px;border-radius:50%;overflow:hidden;background:var(--paper);display:grid;place-items:center;font-size:42px}
.ppf .top .av img{width:100%}
.ppf .kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.ppf .kpis div{background:var(--paper);border-radius:14px;padding:8px;text-align:center;display:grid}
.ppf .kpis b{font-size:18px}
.ppf .gal{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.ppf .gal span{aspect-ratio:1;border-radius:12px;display:grid;place-items:center;font-size:30px;background:var(--hqv-cielo)}
.ppf .embs{display:flex;gap:10px;flex-wrap:wrap}
.ppf .embs img{width:46px}
.inv{border-radius:32px;color:#fff;padding:28px;display:grid;gap:14px;justify-items:start;box-shadow:var(--hqv-clay);max-width:760px}
.inv h2{font-size:clamp(26px,4vw,36px);line-height:1.1}
.inv.fs{background:var(--host)}.inv.nb{background:var(--prov)}
.inv ul{margin:0;padding-left:18px;display:grid;gap:4px}
.inv .btn{font-size:17px;padding:15px 22px}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# ---------- la cuenta ya no pinta la agenda arriba ni abre una página aparte para cada fiesta
rep('''if(U.tab==="fiestas"){if(!U.sides.fiestas)return drawInvite(p,"fiestas");p.insertAdjacentHTML("beforebegin",agendaBar());bindAgenda();return U.eventId&&getEv()?drawEvent(p):drawFiestas(p);}''',
    '''if(U.tab==="fiestas"){if(!U.sides.fiestas&&!(U.plannerJobs||[]).length)return drawInvite(p,"fiestas");return drawFiestas(p);}''')

# ---------- invitaciones (azul para pre-cotizar, morado para abrir tu negocio)
func('drawInvite', r'''
function drawInvite(p,k){const fs=k==="fiestas";
 p.innerHTML=`<div class="inv ${fs?"fs":"nb"}">
  <img src="img/${fs?"c_05":"c_01"}.webp" alt="" style="width:110px">
  <h2>${fs?"¿Y tu próxima fiesta?":"¿Tienes un negocio de fiestas o eventos?"}</h2>
  <span style="font-size:16px">${fs?"Además de trabajar en fiestas, también puedes organizar las tuyas. Calcula gratis cuánto cuesta y encuentra a los proveedores que sí cumplen lo que pides.":"Crea tu sitio web gratis y recibe pre-cotizaciones de clientes reales, directo en tu WhatsApp."}</span>
  <ul>${(fs?["Presupuesto en minutos, gratis","Precios reales del mercado","Proveedores que cumplen lo que pides"]:["Sitio web gratis para siempre","Más visibilidad y clientes","Servicios, venue y event planner en un mismo lugar"]).map(x=>`<li>${x}</li>`).join("")}</ul>
  <button class="btn cta" type="button" id="act">${fs?"Pre-cotizar mi fiesta gratis →":"Crear mi sitio web gratis →"}</button>
  <span style="font-size:13px;font-weight:700;opacity:.95">Usamos tu misma cuenta: no tienes que volver a registrarte.</span></div>`;
 $("act").onclick=()=>{track("invitacion_cruzada",{a:fs?"anfitrion":"proveedor"});show("home");goSide(fs?"hs":"pv");};}''')

# ---------- «Mis fiestas»: futuro · presente · pasado
func('drawFiestas', r'''
function fichaHtml(e,on){const f=e.f;e.versions=e.versions||[{f,t:e.t||now()}];
 return`<div class="fch ${on?"on":""}" id="f-${e.id}"><div class="fh" data-ev="${e.id}" role="button" tabindex="0" aria-label="Ver la descripción de ${esc(f.nombre||f.occ)}"><small>${esc(f.nombre||f.occ)} · ${f.guests.toLocaleString("es-MX")} invitados · ${fdate(f.date)}</small>
  <span class="n"><b>${money(f.pp)}</b><span>por persona</span></span><small>Total aproximado ${money(f.total)}</small>${evState(e)}</div>
  <div class="fv">${e.versions.map((v,i)=>`<div class="vr"><span class="grow"><b>Versión ${e.versions.length-i}${i===0?" · actual":""}</b><small>${new Date(v.t).toLocaleDateString("es-MX",{day:"numeric",month:"short",hour:"2-digit",minute:"2-digit"})} · ${money(v.f.total)} · ${v.f.guests} invitados</small></span>
   <span class="ico"><button type="button" data-vw="${e.id}|${i}">Ver</button><button type="button" data-vd="${e.id}|${i}" aria-label="Descargar PDF" title="Descargar PDF">⬇️</button><button type="button" data-vx="${e.id}|${i}" aria-label="Borrar versión" title="Borrar">✕</button></span></div>`).join("")}</div></div>`;}
function drawFiestas(p){const isPl=(U.site&&(U.site.tipos||[]).includes("planner"))||(U.plannerJobs||[]).length;U.sub=U.sub||"mias";if(!isPl)U.sub="mias";
 const done=e=>daysTo(e.f.date)<0&&e.surveyDone,act=U.events.filter(e=>!done(e)),cel=U.events.filter(done);
 if(!act.some(e=>e.id===U.eventId))U.eventId=act[0]?act[0].id:null;
 const mob=matchMedia("(max-width:860px)").matches,sel=act.find(e=>e.id===U.eventId);
 const det=`<div class="fdet"><span class="dtitle">Descripción del proyecto</span><div id="evRight" style="display:grid;gap:14px"></div></div>`;
 const tabs=isPl?`<div class="subtabs" role="tablist"><button type="button" role="tab" data-sub="mias" aria-selected="${U.sub==="mias"}">🎉 Mis fiestas personales</button><button type="button" role="tab" data-sub="otros" aria-selected="${U.sub==="otros"}">📋 Las fiestas de mis clientes</button></div>`:"";
 if(U.sub==="otros"){p.innerHTML=`${tabs}<div class="fhead"><h2>${em("magic_wand")} Las fiestas de mis clientes</h2></div><span class="hint">Las fiestas que organizas como event planner, después de que aceptaste y tu cliente confirmó el trato.</span>
  <section class="tsec"><h3 class="tlab">🎈 En proceso</h3><div class="flist">${(U.plannerJobs||[]).map(j=>`<div class="fch"><div class="fh"><small>${esc(j.nombre)} · ${j.guests} invitados · ${fdate(j.date)}</small><span class="n"><b>${money(j.total/j.guests)}</b><span>por persona</span></span><small>Total pre-cotizado ${money(j.total)} · tu cobro ${money(j.cobro||0)}</small><span class="st go">En progreso</span></div>
   <div class="fv"><div class="vr"><span class="grow"><b>Tu cliente: ${esc(j.cliente)}</b><small>Le das seguimiento por WhatsApp junto con sus proveedores.</small></span><span class="ico"><button type="button" data-job="${esc(j.nombre)}">Ver</button></span></div></div></div>`).join("")||'<div class="empty"><span class="hint">Cuando aceptes a un cliente en Mi negocio › Event planner, su fiesta aparece aquí.</span></div>'}</div></section>`;
  p.querySelectorAll("[data-sub]").forEach(b=>b.onclick=()=>{U.sub=b.dataset.sub;drawAcct();});
  p.querySelectorAll("[data-job]").forEach(b=>b.onclick=()=>toast("📋 Aquí verás la descripción del proyecto de tu cliente."));return;}
 p.innerHTML=`${tabs}<div class="fhead"><h2>${em("party_popper")} ${isPl?"Mis fiestas personales":"Mis fiestas"}</h2><button class="btn cta sm" type="button" id="newEv">＋ Pre-cotizar otra fiesta</button></div>
  <section class="tsec"><h3 class="tlab">🔮 Por celebrar <span class="hint">Agenda las fiestas que quieres pre-cotizar más adelante. Te avisamos ${RG.diasRecordatorio} días antes.</span></h3>
   ${agendaBar()}${U.agenda.length?`<div class="list">${U.agenda.map(x=>`<div class="evc agd"><img class="em lg" src="img/e_birthday_cake.webp" alt=""><span class="grow"><b>${esc(x.w)}</b><span class="hint">${fdate(x.d)} · faltan ${Math.max(0,daysTo(x.d))} días</span></span><button class="btn ghost sm" type="button" data-agq="${esc(x.w)}">Pre-cotizar</button></div>`).join("")}</div>`:""}</section>
  <section class="tsec"><h3 class="tlab">🎈 En proceso <span class="hint">Tus pre-cotizaciones con sus versiones. Toca una ficha para ver la descripción del proyecto.</span></h3>
   ${act.length?`<div class="fgrid"><div class="flist">${act.map(e=>fichaHtml(e,e.id===U.eventId)+(mob&&e.id===U.eventId?det:"")).join("")}</div>${!mob&&sel?det:""}</div>`:`<div class="empty"><span class="hint">No tienes fiestas en proceso.</span><button class="btn cta sm" type="button" data-agq="nueva">Pre-cotizar una fiesta</button></div>`}</section>
  <section class="tsec"><h3 class="tlab">🏅 Celebradas <span class="hint">Tu récord con ¡Hay que vernos!: cada fiesta te acerca a nuevas insignias.</span></h3>
   ${cel.length?`<div class="list">${cel.map(e=>`<div class="donec"><img class="em lg" src="img/e_party_popper.webp" alt=""><span class="grow"><b>${esc(e.f.nombre||e.f.occ)}</b><span class="hint">${fdate(e.f.date)} · ${e.f.guests} invitados</span></span><img src="img/b_fundador.webp" alt="Insignia Co-constructor" style="width:42px"></div>`).join("")}</div><span class="hint">🏅 ${cel.length} ${cel.length===1?"fiesta celebrada":"fiestas celebradas"} · faltan ${Math.max(0,3-cel.length)} para el nivel Fiestero.</span>`:'<div class="empty"><span class="hint">Aquí quedarán las fiestas que ya celebraste. Cuéntanos cómo te fue en cada una y gana insignias.</span></div>'}</section>`;
 bindAgenda();
 p.querySelectorAll("[data-sub]").forEach(b=>b.onclick=()=>{U.sub=b.dataset.sub;drawAcct();});
 p.querySelectorAll(".fh[data-ev]").forEach(b=>{const go=()=>{U.eventId=b.dataset.ev;drawAcct();if(mob)setTimeout(()=>{const d=$("f-"+U.eventId);if(d)d.scrollIntoView({behavior:"smooth",block:"start"});},50);};b.onclick=go;b.onkeydown=ev=>{if(ev.key==="Enter")go();};});
 p.querySelectorAll("[data-vw]").forEach(b=>b.onclick=()=>{const[id,i]=b.dataset.vw.split("|");docModal(U.events.find(x=>x.id===id),+i);});
 p.querySelectorAll("[data-vd]").forEach(b=>b.onclick=()=>toast("⬇️ En el sitio real aquí se descarga el PDF de esta versión."));
 p.querySelectorAll("[data-vx]").forEach(b=>b.onclick=()=>{const[id,i]=b.dataset.vx.split("|"),e=U.events.find(x=>x.id===id),last=e.versions.length===1;
  confirmModal(last?`¿Borrar «${esc(e.f.nombre||e.f.occ)}»? Es su única versión, así que se borra la fiesta completa.`:`¿Borrar la versión ${e.versions.length-(+i)} de «${esc(e.f.nombre||e.f.occ)}»?`,last?"Sí, borrar la fiesta":"Sí, borrar la versión",()=>{
   if(last){U.events=U.events.filter(x=>x.id!==id);toast("🗑️ Fiesta borrada");}else{e.versions.splice(+i,1);e.f=e.versions[0].f;toast("🗑️ Versión borrada");}drawAcct();});});
 p.querySelectorAll("[data-agq]").forEach(b=>b.onclick=()=>openJourney("fiestas",true));
 const n=$("newEv");if(n)n.onclick=()=>openJourney("fiestas",true);
 if(sel)renderDetail(sel);}
function confirmModal(msg,yes,fn){const m=$("modal");m.innerHTML=`<div class="sheet"><h2>¿Seguro?</h2><span>${msg}</span><div class="yn2"><button class="btn ghost" type="button" id="cfNo">Cancelar</button><button class="btn" type="button" id="cfYes" style="background:var(--bad);color:#fff">${yes}</button></div></div>`;
 m.hidden=false;$("cfNo").onclick=()=>m.hidden=true;$("cfYes").onclick=()=>{m.hidden=true;fn();};}
function docModal(e,i){const v=e.versions[i]||e.versions[0],f=v.f,m=$("modal");
 m.innerHTML=`<div class="sheet wide" style="background:var(--paper)"><div class="doc"><div class="dh"><img src="img/logo.webp" alt="¡Hay que vernos!"><span style="text-align:right"><b>Pre-cotización</b><br><small>Versión ${e.versions.length-i} · ${new Date(v.t).toLocaleDateString("es-MX",{day:"numeric",month:"long",year:"numeric"})}</small></span></div>
  <div><b style="font-size:17px">${esc(f.nombre||f.occ)}</b><br>${esc(f.occ)} · ${f.guests.toLocaleString("es-MX")} invitados · ${fdate(f.date)}${f.start?` · ${f.start} a ${f.end}`:""}${f.zona?` · ${esc(f.zona)}`:""}<br>Para: ${esc(U.name)} ${esc(U.last||"")}</div>
  <div><span class="pp">${money(f.pp)}</span> por persona<br><small>Total aproximado ${money(f.total)} por el total de invitados</small></div>
  <table>${(f.rows||[]).map(r=>`<tr><td>${r.e} ${esc(r.label)}${r.subs&&r.subs.length?`<br><small style="color:#6b6585">${r.subs.map(esc).join(" · ")}</small>`:""}</td><td>${r.pend?"Por cotizar":`${money(r.amt/f.guests)} p/p<br><small>${money(r.amt)}</small>`}</td></tr>`).join("")}</table>
  <div class="tot"><span>Total aproximado</span><span>${money(f.total)}</span></div>
  ${f.planner?`<div>📋 Event planner elegido: <b>${esc(f.planner.n)}</b></div>`:""}
  <p class="foot">Cálculo con precios promedio del mercado en tu zona. No es una cotización formal: el precio final lo acuerdas con cada proveedor. hayquevernos.com</p></div>
  <div class="yn2"><button class="btn ghost" type="button" id="dX">Cerrar</button><button class="btn" type="button" id="dD">⬇️ Descargar PDF</button></div></div>`;
 m.hidden=false;$("dX").onclick=()=>m.hidden=true;$("dD").onclick=()=>toast("⬇️ En el sitio real aquí se descarga el PDF.");track("pdf_visto");}
function plannerProfile(pk,onBack){const m=$("modal");const p=pk||{};
 m.innerHTML=`<div class="sheet wide"><div class="ppf"><div class="top"><span class="av">${p.img?`<img src="${p.img}" alt="">`:p.emo||"📋"}</span><span style="display:grid;gap:2px"><span class="hint">Perfil de event planner</span><b style="font-size:22px">${esc(p.n)}</b><span>⭐ ${p.r} · ${p.y} años de experiencia · ${esc(p.z||"")}</span><span class="hint">hayquevernos.com/${esc(String(p.n||"").toLowerCase().replace(/[^a-z]+/g,"-"))}</span></span></div>
  <span>${esc(p.b||"Me encargo de que tu fiesta salga como la imaginas: tiempos, proveedores y presupuesto bajo control.")}</span>
  <div class="kpis"><div><b>${Math.round((p.y||3)*4.5)}</b><span class="hint">eventos cerrados con ¡HQV!</span></div><div><b>⭐ ${p.r}</b><span class="hint">calificación global</span></div><div><b>Desde ${money(p.fee||5000)}</b><span class="hint">por evento</span></div></div>
  <div><b>Especialidades</b><br><span class="hint">${esc(p.sp||"Bodas · Cumpleaños · Corporativos")}</span></div>
  <div class="gal"><span>💐</span><span>🎂</span><span>🥂</span></div>
  <div><b>Insignias</b><div class="embs"><img src="img/b_fundador.webp" alt="Fundador"><img src="img/b_responde_ya.webp" alt="Responde ya"><img src="img/b_verificado.webp" alt="Verificado"></div></div></div>
  <button class="btn ghost" type="button" id="ppBack">← Regresar</button></div>`;
 m.hidden=false;$("ppBack").onclick=()=>{m.hidden=true;onBack&&onBack();};track("perfil_planner_visto");}
function renderDetail(e){const R=$("evRight");if(!R)return;const f=e.f,past=daysTo(f.date)<0,P=e.planner;
 let h="";
 if(past)h=e.surveyDone?`<div class="box" style="background:var(--hqv-menta)"><h2>${em("glowing_star")} ¡Gracias por contarnos!</h2><span>Ganaste la insignia <b>Co-constructor ¡HQV!</b> y créditos para tu próxima fiesta.</span></div>`:surveyBox(e);
 else if(!e.paid)h=interestBox(e,true);
 else if(e.paid==="planner"&&!["liberado","propio"].includes(P.state))h=plannerBox(e)+interestBox(e,false);
 else h=(P.state==="liberado"?plannerBox(e):e.paid==="prov"||P.state==="propio"?provSteps():"")+provListBox(e,P.state==="liberado")+(P.state==="propio"||e.paid==="prov"?`<div class="box"><h3>${em("magic_wand")} ¿Quieres un event planner?</h3><span class="hint">Puedes sumar a uno cuando quieras. Conoce 3 perfiles por ${money(PR.plannerDespues)}; cuando ambos confirmen el trato, le liberamos tus proveedores.</span><button class="btn ghost" type="button" id="late">Conocer event planners · ${money(PR.plannerDespues)}</button></div>`:"");
 h+=`<details class="box"><summary><b>Así se reparte</b> <span class="hint">· ${money(f.total)}</span></summary><div class="brk" style="margin-top:8px">${f.rows.map(r=>`<div><span>${r.e} ${esc(r.label)}</span><span>${r.pend?"Por cotizar":`${money(r.amt/f.guests)} por persona · ${money(r.amt)}`}</span></div>`).join("")}</div></details>
  <div class="row" style="gap:8px;flex-wrap:wrap"><button class="pill sm" type="button" id="evEdit">🔄 Recalcular (crea una versión nueva)</button>${past?"":`<button class="sim" type="button" id="evPast">Simular: ya pasó mi fiesta</button>`}</div>`;
 R.innerHTML=h;
 $("evEdit").onclick=()=>openJourney("fiestas",true,e.id);
 const ep=$("evPast");if(ep)ep.onclick=()=>{f.date=new Date(now()-864e5).toISOString().slice(0,10);inbox("fiestas",`🎉 ¿Cómo te fue en «${f.nombre||f.occ}»? Cuéntanos y gana tu insignia.`);drawAcct();};
 if(past){if(!e.surveyDone)bindSurvey(e);return;}
 if(!e.paid){const c=$("contact");if(c)c.onclick=()=>startPay(e);return;}
 if(e.paid==="planner"&&!["liberado","propio"].includes(P.state)){bindPlanner(e);return;}
 if(P.state==="liberado")bindPlanner(e);bindProvList(e);const l=$("late");if(l)l.onclick=()=>startPay(e,"late");}
function provSteps(){return`<div class="box"><h2>${em("rocket")} Siguientes pasos</h2><ol class="nsteps"><li><span><b>CONTACTO</b>Escríbeles por WhatsApp desde aquí. Los proveedores ya saben de tu fiesta y esperan que tú des el primer paso.</span></li><li><span><b>CONFIRMACIÓN</b>Cuando platiques con cada uno, dinos si quedó o no en tu evento. Así le avisamos y liberas tu lista.</span></li><li><span><b>CALIFICACIÓN</b>Un día después de tu fiesta te pedimos calificar a quienes sí trabajaron contigo.</span></li></ol></div>`;}''')



# ---------- estado de la ficha
func('evState', r'''
function evState(e){if(daysTo(e.f.date)<0)return e.surveyDone?'<span class="st go">Celebrada ✓</span>':'<span class="st wait">Cuéntanos cómo te fue</span>';if(!e.paid)return'<span class="st new">Pre-cotizada</span>';const s=e.planner.state;if(e.paid==="prov"||s==="liberado"||s==="propio")return'<span class="st go">Organizando</span>';return'<span class="st wait">Con tu planner</span>';}''')

# ---------- interés y pago: CTA en verde y título con el planner
func('interestBox', r'''
function interestBox(e,pre){const ks=Object.keys(e.provs),pl=e.opts.planner&&e.planner.cur;
 return`<div class="box"><h2>${em("star-struck")} ${pl?`${esc(first(pl.n))} y ${e.interes} proveedores más están disponibles para tu evento.`:`${e.interes} proveedores están disponibles para tu evento.`}</h2><span class="hint">${pre?"Cumplen con lo que pides, están cerca de ti y libres en tu fecha. Contáctalos.":"Se liberan en cuanto tu event planner confirme el trato."}</span>
 <div class="int">${ks.map(k=>`<div class="ln"><span>${e.provs[k][0].emo} ${esc(k)}</span><span class="st vis">${e.provs[k].length} disponibles</span></div>`).join("")}</div>
 <div class="list">${ks.slice(0,2).map(k=>e.provs[k].slice(0,2).map((x,i)=>provCard(x,i,true,e)).join("")).join("")}</div>
 ${pre?`<button class="btn cta" type="button" id="contact" style="justify-self:stretch">${pl?`Contactar a ${esc(first(pl.n))} + proveedores →`:"Contactar proveedores →"}</button><span class="hint" style="text-align:center">Pago único: ${money(pl?PR.proveedoresMasPlanner:PR.desbloquearProveedores)}</span>`:`<div class="lock">${em("locked")}<span>Tu planner y tú los verán al mismo tiempo.</span></div>`}</div>`;}''')
rep('''<button class="btn host" type="button" id="doPay">''', '''<button class="btn cta" type="button" id="doPay">''')

# ---------- planner: perfil al tocar la foto, animación, confirmación, contacto principal
func('plannerBox', r'''
function plCardHtml(p,extra="",anim=false){return`<div class="plcard${anim?" hint-anim":""}" id="plcard">${anim?'<div class="swl"><span>← Siguiente</span><span>Lo quiero →</span></div>':""}<div class="hd"><span class="av" data-plprof="1" title="Ver su perfil completo">${p.img?`<img src="${p.img}" alt="">`:p.emo}</span><span style="flex:1;min-width:0;cursor:pointer" data-plprof="1"><b style="font-size:17px">${esc(p.n)}</b><span class="hint" style="display:block">⭐ ${p.r} · ${p.y} años · ${esc(p.z||"")} · <u>ver perfil</u></span></span><b>Desde ${money(p.fee)}</b></div>${p.b?`<span>${esc(p.b)}</span>`:""}<span class="hint">${esc(p.sp||"")}</span>${extra}</div>`;}
function plPool(e){const t=e.planner.tried.map(x=>x.n);return PLANNERS.map(normPl).filter(p=>!t.includes(p.n)&&(!e.planner.cur||p.n!==e.planner.cur.n));}
function plannerBox(e){const P=e.planner,pk=P.cur,H=RG.horasRespuestaPlanner,usados=P.tried.length%3,quedan=3-usados;
 const pasos=`<ol class="nsteps"><li><span><b>CONTACTO</b>Tu event planner te escribirá por WhatsApp en menos de ${H} h para platicar tu pre-cotización y negociar entre ustedes.</span></li><li><span><b>CONFIRMACIÓN</b>Después de platicar, dinos si quieres o no hacer equipo con él o ella. Tienes 3 opciones.</span></li><li><span><b>ACCIÓN</b>Cuando tengamos su confirmación, les liberamos a los dos los contactos de tus proveedores.</span></li></ol>`;
 let body="",title="Tu event planner";const st=P.state||"esperando";
 if(st==="esperando"){title="Siguientes pasos";body=`${pasos}${plCardHtml(pk)}<button class="sim" type="button" id="sOk">Simular: ${esc(first(pk.n))} te escribió por WhatsApp</button>`;}
 if(st==="decidir")body=`${plCardHtml(pk)}<b>¿Harás equipo con ${esc(first(pk.n))}?</b><div class="yn2"><button class="btn ghost" type="button" id="pNo">No, quiero otra opción</button><button class="btn cta" type="button" id="pYes">Sí, trabajaremos juntos</button></div><span class="hint">Te ${quedan===1?"queda 1 opción":`quedan ${quedan} opciones`} de esta ronda. Toca su foto para ver su perfil completo.</span>`;
 if(st==="confirmando")body=`${plCardHtml(pk)}<div class="soft"><b>⏳ Falta que ${esc(first(pk.n))} confirme el trato.</b><span>Ya le avisamos. En cuanto confirme, les liberamos a los dos los contactos de tus proveedores y te avisamos aquí y por correo.</span></div><button class="sim" type="button" id="sConf">Simular: ${esc(first(pk.n))} confirmó el trato</button>`;
 if(st==="elige"){const pool=plPool(e);P.idx=(P.idx||0)%Math.max(1,pool.length);const c=pool[P.idx];
  body=c?`<span class="hint">Elige a otra persona. Desliza a la derecha si te gusta o a la izquierda para ver la siguiente.</span>${plCardHtml(c,"",true)}<div class="yn2"><button class="btn ghost" type="button" id="plNext">✕ Siguiente</button><button class="btn cta" type="button" id="plPick">💙 La quiero</button></div>`:`<span class="hint">Ya no hay más perfiles disponibles en tu zona.</span>`;}
 if(st==="agotado")body=`<div class="soft"><b>Ya conociste a tus 3 opciones.</b><span>¿Quieres conocer 3 perfiles más o prefieres ser tu propio event planner?</span></div><div class="yn2"><button class="btn ghost" type="button" id="plOwn">Yo organizo</button><button class="btn cta" type="button" id="plMore">Ver 3 perfiles más · ${money(PR.plannerDespues)}</button></div><span class="hint">Si organizas tú, te liberamos tus proveedores ahora y la invitación a contratar un planner queda abierta.</span>`;
 if(st==="liberado")body=`${plCardHtml(pk,`<span class="st go" style="justify-self:start">Hicieron equipo · ya ve a tus proveedores</span>`)}<div class="contact-note">💙 <span><b>${esc(first(pk.n))} es tu contacto principal.</b> No es necesario que tú contactes a los proveedores: te abrimos sus datos porque pagaste por ellos, pero quien les da seguimiento es tu event planner.</span></div>`;
 return`<div class="box"><h2>${em("magic_wand")} ${title}</h2>${body}</div>`;}''')
rep('''on("plMore",()=>startPay(e,"more"));''', '''on("plMore",()=>startPay(e,"more"));
 document.querySelectorAll("[data-plprof]").forEach(x=>x.onclick=ev=>{ev.stopPropagation();const c=P.state==="elige"?plPool(e)[P.idx||0]:P.cur;plannerProfile(c);});''')

# ---------- proveedores: Sí → seleccionado · No → motivos + comentario (sin estrellas)
WHY = ["Precio fuera de mi presupuesto", "No tenía mi fecha", "Elegí a otro proveedor", "Tardó en responder", "No respondió", "No ofrece lo que busco", "Pocas fotos o reseñas", "Condiciones de pago o anticipo", "Le queda lejos / cobra traslado", "Cambió o se canceló mi evento", "Otro"]
func('provCard', r'''
const WHY_NO=''' + str(WHY).replace("'", '"') + r''';
function provCard(x,i,blur,e){const wa=`https://wa.me/525500000000?text=${encodeURIComponent(`Hola, vi tu perfil en ¡Hay que vernos! y me interesa para mi evento.`)}`;
 const key=x.nm,r=(e.rate||{})[key],pl=e.planner&&e.planner.state==="liberado"&&e.planner.cur;
 const top=`<div class="tp"><span class="av">${x.emo}</span><span class="grow" style="flex:1;min-width:0"><span class="rk">#${i+1} en compatibilidad${x.nuevo?" · Nuevo":""}</span><b class="${blur?"blur":""}">${esc(x.nm)}</b></span><b>${x.price==null?"Por cotizar":money(x.price)}</b></div>
 <div class="why"><span>📍 a ${x.km} km</span><span>⚡ responde en ${x.resp<60?x.resp+" min":Math.round(x.resp/60)+" h"}</span><span>⭐ ${x.rate} (${x.rev})</span>${x.fit>.8?"<span>✅ dentro de tu presupuesto</span>":""}${x.badges.map(b=>`<span><img src="img/b_${b}.webp" alt=""> ${{fundador:"Fundador",verificado:"Verificado",responde_ya:"Responde ya"}[b]}</span>`).join("")}</div>`;
 if(blur)return`<div class="prov">${top}</div>`;
 let low="";
 if(r&&r.byPlanner)low=`<span class="st go" style="justify-self:start">✓ ${r.sel?"Seleccionado":"No seleccionado"} · evaluado por ${esc(first(pl?pl.n:"tu planner"))}</span>`;
 else if(r&&r.sel===true)low=`<span class="st go" style="justify-self:start">✅ Seleccionado · lo calificas un día después de tu fiesta</span>`;
 else if(r&&r.sel===false&&r.done)low="";
 else low=`<div class="row"><a class="btn wa sm" href="${wa}" target="_blank" rel="noopener" data-wa="${esc(key)}">💬 WhatsApp</a><span class="hint">¿Quedó en tu evento?</span><span class="yn2" style="flex:0 0 auto"><button class="btn sm ${r&&r.sel===true?"host":"ghost"}" type="button" data-sel="${esc(key)}|1">Sí</button><button class="btn sm ${r&&r.sel===false?"host":"ghost"}" type="button" data-sel="${esc(key)}|0">No</button></span></div>
  ${r&&r.sel===false?`<div class="rate"><b>¿Por qué no quedó ${esc(x.nm)}?</b><span class="hint">Elige una o varias. Le ayuda a mejorar y nos ayuda a medir.</span><div class="chips why">${WHY_NO.map(t=>`<button class="chip" type="button" data-rw="${esc(key)}|${t}" aria-pressed="${(r.why||[]).includes(t)}">${t}</button>`).join("")}</div>
   <input type="text" data-rpub="${esc(key)}" value="${esc(r.pub||"")}" placeholder="Comentario para el proveedor (opcional)">
   <button class="btn host sm" type="button" data-rok="${esc(key)}">Guardar</button></div>`:""}`;
 return`<div class="prov">${top}${low}</div>`;}''')
func('bindProvList', r'''
function bindProvList(e){e.rate=e.rate||{};const R=k=>e.rate[k]=e.rate[k]||{};
 document.querySelectorAll("[data-all]").forEach(b=>b.onclick=()=>{e.showAll[b.dataset.all]=true;drawAcct();});
 document.querySelectorAll("[data-wa]").forEach(b=>b.addEventListener("click",()=>{R(b.dataset.wa).wa=true;track("whatsapp_proveedor");}));
 document.querySelectorAll("[data-sel]").forEach(b=>b.onclick=()=>{const[k,v]=b.dataset.sel.split("|");const r=R(k);r.sel=v==="1";r.done=r.sel;
  if(r.sel){track("proveedor_seleccionado");toast("🎉 ¡Listo! Le avisamos al proveedor y marcamos tu fecha en su agenda.");}drawAcct();});
 document.querySelectorAll("[data-rw]").forEach(b=>b.onclick=()=>{const[k,t]=b.dataset.rw.split("|"),r=R(k);r.why=r.why||[];r.why=r.why.includes(t)?r.why.filter(x=>x!==t):[...r.why,t];b.setAttribute("aria-pressed",r.why.includes(t));});
 document.querySelectorAll("[data-rpub]").forEach(i=>i.oninput=()=>{R(i.dataset.rpub).pub=i.value;});
 document.querySelectorAll("[data-rok]").forEach(b=>b.onclick=()=>{const k=b.dataset.rok,r=R(k);if(!(r.why||[]).length){toast("Elige al menos un motivo");return;}r.done=true;
  track("proveedor_no_seleccionado",{motivos:r.why,comentario:!!r.pub});
  Object.keys(e.provs).forEach(c=>{e.provs[c]=e.provs[c].filter(x=>x.nm!==k);});e.removed=(e.removed||0)+1;toast("🗂️ Gracias. Le avisamos al proveedor y lo quitamos de tu lista.");drawAcct();});}''')
func('provListBox', r'''
function provListBox(e,withPlanner){const ks=Object.keys(e.provs),N=RG.proveedoresVisiblesPorServicio,pl=e.planner.cur;
 if(withPlanner&&pl&&!e.plDemo){e.plDemo=true;const k=ks[1]||ks[0];if(k&&e.provs[k][0]){e.rate=e.rate||{};e.rate[e.provs[k][0].nm]={sel:true,done:true,byPlanner:true};}}
 return`<div class="box"><h2>${em("handshake")} Tus proveedores</h2><span class="hint">${withPlanner&&pl?`${esc(first(pl.n))} también ve estos contactos y les dará seguimiento; lo que califique uno se refleja en la cuenta del otro.`:"Ordenados para ti: cercanía, presupuesto, calificación, insignias y rapidez."} Dinos quién quedó en tu evento.</span>
 ${e.removed?`<span class="hint">🗂️ ${e.removed} ${e.removed===1?"proveedor descartado":"proveedores descartados"}.</span>`:""}
 ${ks.map(k=>{const l=e.provs[k],all=e.showAll[k];if(!l.length)return"";return`<div class="svc-h"><h3>${l[0].emo} ${esc(k)}</h3><span class="hint">${l.length} disponibles</span></div>
  <div class="list">${l.slice(0,all?l.length:Math.min(N,3)).map((x,i)=>provCard(x,i,false,e)).join("")}</div>
  ${l.length>3&&!all?`<button class="pill sm" type="button" data-all="${esc(k)}">Ver a los ${l.length} disponibles →</button>`:""}`;}).join("")}</div>`;}''')

# ---------- encuesta post-fiesta: solo quienes sí quedaron (incluido el planner)
func('surveyBox', r'''
function surveyBox(e){const f=e.f,rate=e.rate||{};
 let sel=[];Object.keys(e.provs).forEach(k=>e.provs[k].forEach(x=>{if(rate[x.nm]&&rate[x.nm].sel)sel.push({n:x.nm,k,est:x.price||0});}));
 if(!sel.length)Object.keys(e.provs).forEach(k=>{const x=e.provs[k][0];if(x)sel.push({n:x.nm,k,est:x.price||0,ej:true});});
 const pl=e.planner&&e.planner.state==="liberado"&&e.planner.cur;if(pl)sel.unshift({n:pl.n,k:"Event planner",est:pl.fee||0,pl:true});
 sel=sel.slice(0,8);
 const v=e.sv||(e.sv={real:Object.fromEntries(sel.map(x=>[x.n,x.est||""])),st:{},stars:0,note:""});
 return`<div class="box" id="svBox" style="background:var(--hqv-vainilla)"><h2>${em("party_popper")} ¿Cómo te fue en tu fiesta?</h2>
  <div class="emb"><img src="img/b_fundador.webp" alt=""><span class="hint">Califica a quienes trabajaron en tu fiesta y cuéntanos cuánto pagaste. Ganas la insignia <b>Co-constructor ¡HQV!</b> y créditos para tu próxima fiesta.${pl?` Si ${esc(first(pl.n))} ya la contestó, aquí lo verás.`:""}</span></div>
  ${sel.map(x=>`<div class="svq"><b>${x.pl?"📋 ":""}${esc(x.n)} <span class="hint">· ${esc(x.k)}${x.ej?" (ejemplo)":""}</span></b>
   <div class="stars">${[1,2,3,4,5].map(n=>`<button type="button" data-ps="${esc(x.n)}|${n}" aria-pressed="${(v.st[x.n]||0)>=n}" aria-label="${n} estrellas">⭐</button>`).join("")}</div>
   <div class="svsvc"><span>¿Cuánto le pagaste?</span><input type="number" min="0" data-real="${esc(x.n)}" value="${esc(v.real[x.n])}" aria-label="Pagado a ${esc(x.n)}"></div></div>`).join("")}
  <div class="svsvc"><b>Total pagado</b><b id="svTot">${money(Object.values(v.real).reduce((a,b)=>a+(+b||0),0))}</b></div>
  <div class="svq"><b>⭐ ¿Cómo calificas tu fiesta en general?</b><div class="stars">${[1,2,3,4,5].map(n=>`<button type="button" data-st="${n}" aria-pressed="${v.stars>=n}" aria-label="${n} estrellas">⭐</button>`).join("")}</div>
   <input type="text" id="svNote" value="${esc(v.note)}" placeholder="¿Algo que debamos saber? (opcional)"></div>
  <button class="btn cta" type="button" id="svSend">Enviar y ganar mi insignia</button></div>`;}''')
func('bindSurvey', r'''
function bindSurvey(e){const v=e.sv,b=$("svBox");if(!b)return;
 b.querySelectorAll("[data-real]").forEach(i=>i.oninput=()=>{v.real[i.dataset.real]=+i.value||0;$("svTot").textContent=money(Object.values(v.real).reduce((a,x)=>a+(+x||0),0));});
 $("svNote").oninput=x=>{v.note=x.target.value;};
 b.querySelectorAll("[data-ps]").forEach(x=>x.onclick=()=>{const[n,k]=x.dataset.ps.split("|");v.st[n]=+k;x.parentNode.querySelectorAll("button").forEach(y=>y.setAttribute("aria-pressed",+y.dataset.ps.split("|")[1]<=+k));});
 b.querySelectorAll("[data-st]").forEach(x=>x.onclick=()=>{v.stars=+x.dataset.st;b.querySelectorAll("[data-st]").forEach(y=>y.setAttribute("aria-pressed",+y.dataset.st<=v.stars));});
 $("svSend").onclick=()=>{if(!v.stars){toast("⭐ Califica tu fiesta para enviar");return;}e.surveyDone=true;const real=Object.values(v.real).reduce((a,x)=>a+(+x||0),0);
  track("encuesta_post_fiesta",{occ:e.f.occ,invitados:e.f.guests,estimado:e.f.total,real,diferencia_pct:e.f.total?Math.round((real-e.f.total)/e.f.total*100):0,por_proveedor:v.real,estrellas_proveedores:v.st,estrellas:v.stars});
  U.hostBadge=true;inbox("fiestas","🏅 Ganaste la insignia Co-constructor ¡HQV! y créditos para tu próxima fiesta.");confetti();drawAcct();};}''')

# ---------- cuenta: nombre + apellidos, copy nuevo; bienvenida con «Continuar»
rep('''${esc(why||"Para recibir en tu WhatsApp / correo tu pre-cotización, sumarte a nuestra comunidad de anfitriones y acceder a beneficios exclusivos.")}''',
    '''${why?esc(why):"Para recibir tu pre-cotización más <b>beneficios exclusivos</b>."}''')
rep('''<div class="field"><label for="acN">Tu nombre</label><input type="text" id="acN" value="${esc(U.name)}" autocomplete="name"></div>''',
    '''<div class="row" style="gap:10px;flex-wrap:wrap"><div class="field" style="flex:1 1 160px"><label for="acN">Nombre(s)</label><input type="text" id="acN" value="${esc(U.name)}" autocomplete="given-name"></div><div class="field" style="flex:1 1 160px"><label for="acL">Apellidos</label><input type="text" id="acL" value="${esc(U.last||"")}" autocomplete="family-name"></div></div>''')
rep('''if(n.length<2)return err("Escribe tu nombre.");''', '''if(n.length<2)return err("Escribe tu nombre.");if($("acL").value.trim().length<2)return err("Escribe tus apellidos.");''')
rep('''Object.assign(U,{name:n,wa:w,''', '''Object.assign(U,{name:n,last:$("acL").value.trim(),wa:w,''')
rep('''<button class="btn host" type="submit">Guardar y continuar</button>''', '''<button class="btn cta" type="submit">Guardar y continuar</button>''')
rep('''<button class="btn host" type="button" id="obOk">Ver mi fiesta →</button>''', '''<button class="btn cta" type="button" id="obOk">Continuar</button>''')
rep('''<button class="btn" type="button" id="goPro">Activar Pro (simulado)</button>''', '''<button class="btn cta" type="button" id="goPro">Activar Pro (simulado)</button>''')

# ---------- demo: el planner tiene trabajos y el anfitrión tiene apellido
s = s.replace('U.plannerJobs=[{nombre:"Los XV de Valeria"', 'U.last=U.last||"Juárez";U.plannerJobs=[{nombre:"Los XV de Valeria"', 1)

P.write_text(s)
print('shell10 ok', len(s))

# ---------- arreglo: «ya pasó mi fiesta» fallaba de noche por la zona horaria (UTC)
s = P.read_text().replace('f.date=new Date(now()-864e5).toISOString().slice(0,10)', 'f.date=new Date(now()-2*864e5).toISOString().slice(0,10)')
P.write_text(s)
print('fecha ok')

# ---------- arreglos: ids únicos por fiesta (la demo creaba dos con el mismo id) y etiqueta de estado sin encimarse
s = P.read_text().replace('return{id:"e"+now(),', 'return{id:"e"+now()+"_"+Math.floor(Math.random()*1e6),')
s = s.replace('.fch .fh .st{position:absolute;top:12px;right:12px}', '.fch .fh .st{justify-self:start;margin-top:6px}')
P.write_text(s)
print('ids ok')
s = P.read_text().replace('PROTOTIPO v6', 'PROTOTIPO v8')
P.write_text(s)
