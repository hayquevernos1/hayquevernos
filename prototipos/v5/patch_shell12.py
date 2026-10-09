"""v8 · Vuelta 3 · Mi negocio del proveedor (comentarios de Diego en Miro, 8 oct 2026 noche). Correr DESPUÉS de patch_shell11.py.
- Tres pestañas: Mis servicios · Mi venue · Event planner (según lo que ofrece).
- Cada pestaña en tres tiempos: Por venir (agenda con fecha cerrada / cerrada con disponibilidad) · En proceso (solicitudes y
  postulaciones) · Celebradas (récord, promedio e insignias).
- Solicitud = aviso de un evento que encaja: ficha + «Descripción del proyecto» (al lado en web, debajo en celular).
  «Rechazar» (blanco, izq., con motivo) · «Postular» (verde, der.). Postular pide plan Pro; ya en Pro ve el proyecto completo.
- Postulaciones con tracker: Postulado → Visto → En WhatsApp → Seleccionado / No seleccionado / Sin comentarios (24 h). Botón borrar.
- Planner: pre-aceptación con Aceptado / Rechazado + motivo + cuánto cobró (para investigación) → pasa a
  Mis fiestas › Las fiestas de mis clientes, donde ve a su cliente y a los proveedores liberados y confirma quién queda.
- Botones «Ver como anfitrión» / «Ver como proveedor» para entender los dos lados."""
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
    a = ms[-1].start() + 1
    n = re.search(r'\n(function |let |const |/\*)', s[a + 10:])
    b = a + 10 + n.start() + 1
    s = s[:a] + new.strip('\n') + '\n' + s[b:]


CSS = '''
/* ===== v8 · Mi negocio ===== */
.nb-sub button[aria-selected="true"]{background:var(--prov)!important;color:#fff!important}
.solc{background:var(--card);border-radius:22px;box-shadow:var(--hqv-clay-sm);overflow:hidden;outline:3px solid transparent}
.solc.on{outline-color:var(--prov)}
.solc .sh{background:var(--prov);color:#fff;padding:12px 14px;display:grid;gap:3px;cursor:pointer}
.solc .sh small{opacity:.92;font-size:12px}
.solc .sb{padding:10px 12px;display:grid;gap:8px}
.cli{display:flex;gap:10px;align-items:center;background:var(--paper);border-radius:14px;padding:8px 10px}
.cli .av{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:var(--card);font-weight:900}
.rp{display:flex;gap:8px}.rp .btn{flex:1}
.btn.white{background:#fff!important;color:#1a1033!important;box-shadow:var(--hqv-clay-sm)}
.trk{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin:4px 0}
.trk span{display:grid;justify-items:center;gap:4px;font-size:11px;font-weight:800;color:var(--muted);text-align:center}
.trk span i{width:100%;height:6px;border-radius:99px;background:#e6e1f5}
.trk span.on{color:#1a1033}.trk span.on i{background:var(--prov)}
.trk span.ok i{background:var(--cta)}.trk span.no i{background:#c0264b}.trk span.mute i{background:#9b94b5}
.lockd{display:flex;gap:10px;align-items:flex-start;background:var(--hqv-vainilla);color:#3A2E00;border-radius:16px;padding:12px}
.agd2{display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:var(--paper);border-radius:16px;padding:10px 12px}
.agd2 .grow{flex:1;min-width:150px;display:grid}
.kpi3{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.kpi3 div{background:var(--paper);border-radius:16px;padding:10px;display:grid;text-align:center}.kpi3 b{font-size:20px}
.proto .who{display:flex;gap:4px}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# ---------- plan Pro con contexto y acción al terminar
rep('function planModal(){const m=$("modal");let bill="anual";', 'function planModal(after,why){const m=$("modal");let bill="anual";')
rep('''<h2>⭐ Plan Pro</h2><span class="hint">Un solo pago te da acceso a todos los clientes interesados. No pagas por cada uno.</span>''',
    '''<h2>⭐ Plan Pro</h2>${why?`<div class="soft"><b>${why}</b></div>`:""}<span class="hint">Tu sitio web sigue siendo gratis. Con Pro te postulas a todos los eventos que encajan contigo y ves sus datos completos. No pagas por cada uno.</span>''')
rep('''inbox("negocio","⭐ Ya eres Pro. Ahora ves los datos de cada anfitrión interesado.");confetti();drawAcct();};''',
    '''inbox("negocio","⭐ Ya eres Pro. Ahora te postulas y ves los proyectos completos.");confetti();drawAcct();after&&after();};''')

# ---------- Mi negocio
func('drawNegocio', r'''
const VTS=[["services","svc","🎉 Mis servicios"],["venue","venue","🏡 Mi venue"],["planner","planner","📋 Event planner"]];
const NO_WHY=["Ya tengo esa fecha ocupada","No cubro esa zona","El presupuesto no me alcanza","No ofrezco exactamente eso","Muy poca anticipación","Otro"];
const PL_WHY_OK=["El proyecto me encanta","Es mi especialidad","Buen presupuesto","Cliente claro y organizado","Otro"];
const PL_WHY_NO=["Fecha ocupada","Fuera de mi zona","Presupuesto muy bajo","No es mi especialidad","Otro"];
const STG=["Postulado","Visto","En WhatsApp"];
function negState(){U.neg=U.neg||{vt:null,sol:[],post:[],agenda:[],removed:0,sel:null};const t=(U.site&&U.site.tipos)||["services"];const ok=VTS.filter(v=>t.includes(v[0]));if(!ok.some(v=>v[1]===U.neg.vt))U.neg.vt=ok[0][1];return ok;}
function solFicha(r,on){return`<div class="solc ${on?"on":""}" id="sol-${r.id}"><div class="sh" data-so="${r.id}" role="button" tabindex="0"><small>${r.kind==="planner"?"📋 Te eligieron como event planner":"🔔 Evento que encaja contigo"} · quedan ${Math.max(0,Math.ceil((r.dl-now())/36e5))} h</small>
  <b style="font-size:16px">${esc(r.occ)} · ${r.guests} invitados · ${fdate(r.date)}</b><small>📍 ${esc(r.zona)} · a ${r.km} km${r.kind==="planner"?` · pre-cotización ${money(r.total)}`:` · ${esc(r.svc)}`}</small></div>
  <div class="sb"><b style="font-size:13.5px">${r.kind==="planner"?`Tu cliente te eligió entre ${r.interes} perfiles. Tienes 24 h para responder.`:`${r.interes} proveedores interesados en el evento de ${esc(r.cli.n)}. ¿Te sumas?`}</b>
  <div class="cli"><span class="av">${esc(r.cli.n[0])}</span><span style="display:grid;flex:1"><span class="hint" style="font-weight:800">Tu cliente</span><b>${esc(r.cli.n)}</b><span class="hint">⭐ ${r.cli.stars} como anfitrión · ${r.cli.ev} ${r.cli.ev===1?"fiesta":"fiestas"} con ¡HQV!${r.cli.ver?" · ✓ verificado":""}</span></span></div>
  ${r.kind==="planner"?plDecide(r):r.st==="postulada"?`<div class="row" style="gap:8px;align-items:center"><span class="st go">✓ Postulado</span>${U.plan!=="pro"?`<button class="btn cta sm" type="button" data-spo="${r.id}">Activar Pro para ver el proyecto</button>`:""}${(U.neg.post.find(x=>x.sid===r.id)||{}).stage===0?`<button class="link" type="button" data-sret="${r.id}" style="font-size:12.5px">Retirar postulación</button>`:""}</div>`:`<div class="rp"><button class="btn white sm" type="button" data-sno="${r.id}">Rechazar</button><button class="btn cta sm" type="button" data-spo="${r.id}">Postular</button></div>`}
  ${r.rej?`<div class="rate"><b>¿Por qué no te interesa?</b><div class="chips why">${NO_WHY.map(t=>`<button class="chip" type="button" data-sw="${r.id}|${t}" aria-pressed="${(r.why||[]).includes(t)}">${t}</button>`).join("")}</div><button class="btn host sm" type="button" data-sok="${r.id}">Guardar</button></div>`:""}</div></div>`;}
function plDecide(r){const d=r.dec||{};return`<div class="rate"><b>¿Aceptas a este cliente?</b><div class="seg" role="group"><button type="button" data-pd="${r.id}|no" aria-pressed="${d.v==="no"}">Rechazado</button><button type="button" data-pd="${r.id}|si" aria-pressed="${d.v==="si"}">Aceptado</button></div>
  ${d.v?`<span class="hint">${d.v==="si"?"¿Por qué lo aceptas?":"¿Por qué lo rechazas?"} Nos ayuda a mejorar a quién te mostramos.</span><div class="chips why">${(d.v==="si"?PL_WHY_OK:PL_WHY_NO).map(t=>`<button class="chip" type="button" data-pw="${r.id}|${t}" aria-pressed="${(d.why||[]).includes(t)}">${t}</button>`).join("")}</div>`:""}
  ${d.v==="si"?`<div class="soft"><b>🤝 ¡Bien! Cuéntanos en 10 segundos</b><span class="hint">Solo para fines de investigación: no se le muestra a nadie.</span>
   <div class="row" style="gap:8px;flex-wrap:wrap"><input type="number" min="0" id="pc-${r.id}" value="${esc(d.cobro||"")}" placeholder="$ ¿Cuánto vas a cobrar?" style="flex:1 1 140px"><select id="pu-${r.id}" style="flex:1 1 140px">${[["evento","por evento"],["hora","por hora"],["invitado","por invitado"],["porcentaje","% del total"]].map(([v,t])=>`<option value="${v}" ${d.unit===v?"selected":""}>${t}</option>`).join("")}</select></div>
   <span class="hint">La pre-cotización de ${money(r.total)} te pareció…</span><div class="seg" role="group">${[["corto","Corta"],["bien","Bien"],["sobrado","Sobrada"]].map(([v,t])=>`<button type="button" data-pq="${r.id}|${v}" aria-pressed="${d.q===v}">${t}</button>`).join("")}</div></div>`:""}
  ${d.v?`<button class="btn ${d.v==="si"?"cta":"host"} sm" type="button" data-pok="${r.id}">${d.v==="si"?"Guardar y pasar a mis fiestas":"Guardar"}</button>`:""}</div>`;}
function solDesc(r){const pro=U.plan==="pro";const open=r.st==="postulada"&&pro;
 if(r.kind==="planner")return`<div class="box"><h2>${em("sparkles")} ${esc(r.occ)} de ${esc(r.cli.n)}</h2><span class="hint">${fdate(r.date)} · ${r.start}–${r.end} · ${r.guests} invitados · ${esc(r.zona)}</span>
  <div class="kpi3"><div><b>${money(r.total)}</b><span class="hint">pre-cotización</span></div><div><b>${money(Math.round(r.total/r.guests))}</b><span class="hint">por persona</span></div><div><b>${r.svcs.length}</b><span class="hint">servicios</span></div></div>
  <div class="why">${r.svcs.map(x=>`<span>${esc(x)}</span>`).join("")}</div><span class="hint">Cuando aceptes y tu cliente confirme el trato, les liberamos a los dos los contactos de ${r.interes} proveedores.</span></div>`;
 return`<div class="box"><h2>${em("sparkles")} ${esc(r.svc)} para ${esc(r.occ.toLowerCase())}</h2>
  <div class="kpi3"><div><b>${r.guests}</b><span class="hint">invitados</span></div><div><b>${fdate(r.date)}</b><span class="hint">${r.start}–${r.end}</span></div><div><b>${open?money(r.est):"$ ••••"}</b><span class="hint">cálculo ¡HQV! de tu servicio</span></div></div>
  <span class="hint">📍 ${esc(r.zona)} · a ${r.km} km de tu negocio · ${esc(r.lugar)}</span>
  ${open?`<div style="display:grid;gap:6px"><b>Lo que pide</b><div class="why">${r.subs.map(x=>`<span>${esc(x)}</span>`).join("")}</div>${r.nota?`<div class="soft"><b>Nota del anfitrión</b><span>«${esc(r.nota)}»</span></div>`:""}
   <span class="hint">Pre-cotización total de la fiesta: ${money(r.total)} (${money(Math.round(r.total/r.guests))} por persona).</span>
   <div class="contact-note">💬 <span><b>El anfitrión da el primer paso.</b> Ya ve tu perfil y tu WhatsApp en su cuenta. En cuanto te escriba lo verás en el tracker de tu postulación.</span></div></div>`
  :`<div class="lockd">${em("locked")}<span><b>${r.st==="postulada"?"Activa Pro para ver el proyecto completo.":"Postúlate para ver el proyecto completo."}</b> Lo que pide exactamente, la nota del anfitrión, el presupuesto y tu cálculo. Y tu WhatsApp aparece en su cuenta para que te escriba.</span></div>`}</div>`;}
function postHtml(x){const fin=x.fin;const cls=i=>i<=x.stage?"on":"";
 return`<div class="solc"><div class="sh" style="cursor:default"><small>${esc(x.svc)}</small><b>${esc(x.ev)}</b><small>${fdate(x.date)}</small></div><div class="sb">
  <div class="trk">${STG.map((t,i)=>`<span class="${cls(i)}"><i></i>${t}</span>`).join("")}<span class="${fin==="sel"?"on ok":fin==="nosel"?"on no":fin==="sin"?"on mute":""}"><i></i>${fin==="sel"?"Seleccionado":fin==="nosel"?"No seleccionado":fin==="sin"?"Sin comentarios":"Resultado"}</span></div>
  ${fin==="nosel"?`<div class="soft"><b>Motivos del anfitrión</b><span>${esc((x.why||[]).join(" · "))}</span>${x.com?`<span>«${esc(x.com)}»</span>`:""}</div>`:""}
  ${fin==="sin"?`<span class="hint">Pasaron 24 h sin respuesta. Puedes darle seguimiento por WhatsApp o borrarla.</span>`:""}
  ${fin==="sel"?`<span class="hint">🎉 ¡Quedaste! Marcamos ${fdate(x.date)} en tu agenda como fecha cerrada.</span>`:""}
  <div class="row" style="gap:6px;flex-wrap:wrap">${!fin?`<button class="sim" type="button" data-ps="${x.id}">Simular siguiente paso</button>`:""}<span style="flex:1"></span><button class="btn white sm" type="button" data-pdel="${x.id}">🗑️ Borrar</button></div></div></div>`;}
function drawNegocio(p){const s=U.site||{},pro=U.plan==="pro",ok=negState(),N=U.neg,vt=N.vt,mob=matchMedia("(max-width:860px)").matches;
 const sol=N.sol.filter(r=>r.vt===vt&&r.st!=="rechazada"&&r.st!=="aceptada"),post=N.post.filter(x=>x.vt===vt),ag=N.agenda.filter(a=>a.vt===vt).sort((a,b)=>a.d.localeCompare(b.d));
 if(!sol.some(r=>r.id===N.sel))N.sel=sol[0]?sol[0].id:null;const sel=sol.find(r=>r.id===N.sel);
 const det=sel?`<div class="fdet"><span class="dtitle">Descripción del proyecto</span>${solDesc(sel)}</div>`:"";
 const cel=post.filter(x=>x.fin==="sel"&&daysTo(x.date)<0).length+(vt==="svc"?(U.neg.celebradas||0):0);
 p.innerHTML=`<div class="box" style="background:var(--prov);color:#fff"><div class="fhead" style="margin:0"><h2>${em("rocket")} ${esc(s.negocio||"Mi negocio")}</h2><span class="row" style="gap:6px">${U.founder?`<span class="tag2">⭐ Fundador #${U.founder}</span>`:""}<span class="tag2 ${pro?"ok":""}">Plan ${pro?"Pro":"Gratis"}</span></span></div>
   <span style="background:rgba(255,255,255,.18);border-radius:99px;padding:4px 12px;font-weight:800;word-break:break-all;justify-self:start">${esc(s.url||"hayquevernos.com/minegocio")}</span>
   <div class="row" style="gap:8px;flex-wrap:wrap"><button class="btn ghost sm" type="button" id="sEdit">✏️ Editar mi sitio</button><button class="btn ghost sm" type="button" id="sCopy">🔗 Copiar link</button><button class="btn ghost sm" type="button" id="sImg">⬇️ Imagen para redes</button>${pro?"":`<button class="btn cta sm" type="button" id="sPro">⭐ Pasar a Pro</button>`}</div></div>
 ${ok.length>1?`<div class="subtabs nb-sub" role="tablist" style="margin-top:14px">${ok.map(([,id,t])=>`<button type="button" role="tab" data-nv="${id}" aria-selected="${vt===id}">${t}</button>`).join("")}</div>`:""}
 <section class="tsec"><h3 class="tlab">🔮 Por venir <span class="hint">Tu agenda. Las fechas cerradas les avisan a otros anfitriones si estás disponible.</span></h3>
  ${ag.map((a,i)=>`<div class="agd2"><img class="em lg" src="img/e_spiral_calendar.webp" alt="" onerror="this.remove()"><span class="grow"><b>${fdate(a.d)}</b><span class="hint">${esc(a.ev)}</span></span><div class="seg" role="group"><button type="button" data-ag="${a.d}|cerrada" aria-pressed="${a.st==="cerrada"}">Fecha cerrada</button><button type="button" data-ag="${a.d}|disp" aria-pressed="${a.st==="disp"}">Cerrada con disponibilidad</button></div></div>`).join("")||'<div class="empty"><span class="hint">Aún no tienes fechas. Cuando quedes seleccionado, la fecha se marca sola.</span></div>'}
  <div class="row" style="gap:8px"><input type="date" id="blD" aria-label="Fecha ocupada" style="flex:1 1 160px"><button class="btn ghost sm" type="button" id="blAdd">Cerrar una fecha</button></div></section>
 <section class="tsec"><h3 class="tlab">🎈 En proceso <span class="hint">${vt==="planner"?"Clientes que te eligieron como su event planner.":"Eventos que encajan contigo. Postúlate y el anfitrión verá tu WhatsApp."}</span></h3>
  <b>${em("megaphone")} Solicitudes</b>
  ${sol.length?`<div class="fgrid"><div class="flist">${sol.map(r=>solFicha(r,r.id===N.sel)+(mob&&r.id===N.sel?det:"")).join("")}</div>${!mob?det:""}</div>`:`<div class="empty"><span class="hint">No tienes solicitudes nuevas. Te avisamos aquí y por correo en cuanto llegue una.</span></div>`}
  ${N.removed?`<span class="hint">🗂️ ${N.removed} ${N.removed===1?"solicitud descartada":"solicitudes descartadas"}.</span>`:""}
  <div class="row"><button class="sim" type="button" id="sReq">Simular: me llegó una solicitud</button></div>
  ${vt!=="planner"?`<b style="margin-top:8px">${em("trophy")} Mis postulaciones</b>${post.length?`<div class="flist">${post.map(postHtml).join("")}</div>`:'<div class="empty"><span class="hint">Cuando te postules a un evento, aquí ves en qué va.</span></div>'}`:`<span class="hint">Los clientes que aceptes pasan a <b>Mis fiestas › Las fiestas de mis clientes</b>.</span>`}</section>
 <section class="tsec"><h3 class="tlab">🏅 Celebradas <span class="hint">Tu récord con ¡Hay que vernos!</span></h3>
  <div class="kpi3"><div><b>${cel}</b><span class="hint">eventos celebrados</span></div><div><b>${cel?"⭐ 4.9":"—"}</b><span class="hint">calificación promedio</span></div><div><b>${post.filter(x=>x.fin==="sel").length}</b><span class="hint">veces seleccionado</span></div></div>
  <div class="badges">${[["fundador","Fundador",!!U.founder],["perfil_100","Perfil 100%",(s.completo||0)>=100],["responde_ya","Responde ya",false],["verificado","Verificado",false],["consentido","Consentido",false],["50_fiestas","50 fiestas",false]].map(([b,t,on])=>`<figure class="${on?"":"off"}"><img src="img/b_${b}.webp" alt=""><figcaption>${t}</figcaption></figure>`).join("")}</div>
  <div class="soft"><b>${em("light_bulb")} Consejos para que te elijan más</b><span>• Los que responden en menos de 1 h se eligen el doble.</span><span>• Agrega 3 fotos más: los perfiles con 5 fotos o más reciben más solicitudes.</span><span>• Contesta la encuesta después de cada evento y gana la insignia Co-constructor.</span></div></section>`;
 $("sEdit").onclick=()=>openJourney("negocio",true);
 $("sCopy").onclick=()=>{const u="https://"+(s.url||"");(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(()=>toast("🔗 Link copiado"),()=>toast(u));};
 $("sImg").onclick=async()=>{const u=await hqvShareImage({logo:"img/logo.webp",kicker:"Encuéntranos en ¡Hay que vernos!",title:s.negocio||"Mi negocio",url:s.url||"hayquevernos.com",foot:"Escanea, conoce mis servicios y cotiza por WhatsApp"});hqvDownload(u,"sitio.png");};
 const pb=$("sPro");if(pb)pb.onclick=()=>planModal();
 p.querySelectorAll("[data-nv]").forEach(b=>b.onclick=()=>{N.vt=b.dataset.nv;N.sel=null;drawAcct();});
 p.querySelectorAll("[data-so]").forEach(b=>b.onclick=()=>{N.sel=+b.dataset.so;drawAcct();if(mob)setTimeout(()=>{const d=$("sol-"+N.sel);d&&d.scrollIntoView({behavior:"smooth",block:"start"});},50);});
 const R=id=>N.sol.find(r=>r.id===+id);
 p.querySelectorAll("[data-sno]").forEach(b=>b.onclick=()=>{R(b.dataset.sno).rej=true;drawAcct();});
 p.querySelectorAll("[data-sw]").forEach(b=>b.onclick=()=>{const[id,t]=b.dataset.sw.split("|"),r=R(id);r.why=r.why||[];r.why=r.why.includes(t)?r.why.filter(x=>x!==t):[...r.why,t];b.setAttribute("aria-pressed",r.why.includes(t));});
 p.querySelectorAll("[data-sok]").forEach(b=>b.onclick=()=>{const r=R(b.dataset.sok);if(!(r.why||[]).length){toast("Elige al menos un motivo");return;}r.st="rechazada";N.removed++;track("solicitud_rechazada",{motivos:r.why});toast("🗂️ Listo. Ya no verás esta solicitud.");drawAcct();});
 const postular=r=>{r.st="postulada";N.post.unshift({id:now()+Math.floor(Math.random()*999),sid:r.id,vt:r.vt,ev:`${r.occ} de ${r.cli.n} · ${r.guests} invitados`,svc:r.svc,date:r.date,stage:0,fin:null});
  track("postulacion",{vt:r.vt,svc:r.svc});inbox("negocio",`📨 Te postulaste a «${r.occ} de ${r.cli.n}». El anfitrión ya ve tu WhatsApp.`);toast("📨 ¡Postulado! Ahora ves el proyecto completo.");drawAcct();};
 p.querySelectorAll("[data-spo]").forEach(b=>b.onclick=()=>{const r=R(b.dataset.spo);if(r.st==="postulada"){planModal(()=>drawAcct(),"Activa Pro para ver el proyecto completo.");return;}if(U.plan!=="pro"){planModal(()=>postular(r),"Para postularte y ver el proyecto completo necesitas el plan Pro.");return;}postular(r);});
 p.querySelectorAll("[data-sret]").forEach(x=>x.onclick=()=>{const r=R(x.dataset.sret);r.st="nueva";N.post=N.post.filter(y=>y.sid!==r.id);toast("Retiraste tu postulación.");drawAcct();});
 p.querySelectorAll("[data-pd]").forEach(b=>b.onclick=()=>{const[id,v]=b.dataset.pd.split("|"),r=R(id);r.dec={v,why:[]};drawAcct();});
 p.querySelectorAll("[data-pw]").forEach(b=>b.onclick=()=>{const[id,t]=b.dataset.pw.split("|"),d=R(id).dec;d.why=d.why.includes(t)?d.why.filter(x=>x!==t):[...d.why,t];b.setAttribute("aria-pressed",d.why.includes(t));});
 p.querySelectorAll("[data-pq]").forEach(b=>b.onclick=()=>{const[id,v]=b.dataset.pq.split("|"),r=R(id);r.dec.q=v;r.dec.cobro=($("pc-"+id)||{}).value||r.dec.cobro;r.dec.unit=($("pu-"+id)||{}).value||r.dec.unit;drawAcct();});
 p.querySelectorAll("[data-pok]").forEach(b=>b.onclick=()=>{const id=b.dataset.pok,r=R(id),d=r.dec;if(!d.why.length){toast("Elige al menos un motivo");return;}
  if(d.v==="no"){r.st="rechazada";N.removed++;track("planner_rechaza",{motivos:d.why});toast("Listo. Le avisamos a tu cliente para que elija otra opción.");drawAcct();return;}
  d.cobro=($("pc-"+id)||{}).value||d.cobro;d.unit=($("pu-"+id)||{}).value||d.unit||"evento";if(!d.cobro){toast("Dinos cuánto vas a cobrar");return;}if(!d.q){toast("Dinos qué te pareció la pre-cotización");return;}
  r.st="aceptada";U.plannerJobs=U.plannerJobs||[];U.plannerJobs.unshift({nombre:`${r.occ} de ${r.cli.n}`,cliente:r.cli.n,guests:r.guests,date:r.date,total:r.total,cobro:+d.cobro,unit:d.unit,svcs:r.svcs,nuevo:true});
  N.agenda.push({d:r.date,ev:`${r.occ} de ${r.cli.n} (event planner)`,st:"cerrada",vt:"planner"});
  track("planner_acepta",{motivos:d.why,cobro:+d.cobro,unidad:d.unit,precotizacion:d.q});inbox("fiestas",`📋 «${r.occ} de ${r.cli.n}» ya está en Mis fiestas › Las fiestas de mis clientes. Esperamos la confirmación de tu cliente.`);
  toast("🤝 ¡Aceptado! Lo encuentras en Mis fiestas › Las fiestas de mis clientes.");U.tab="fiestas";U.sub="otros";U.jobSel=U.plannerJobs[0].nombre;drawAcct();});
 p.querySelectorAll("[data-ps]").forEach(b=>b.onclick=()=>{const x=N.post.find(y=>y.id===+b.dataset.ps);
  if(x.stage<2){x.stage++;toast(x.stage===1?"👀 El anfitrión vio tu perfil.":"💬 El anfitrión te escribió por WhatsApp.");}
  else{const k=(N.post.indexOf(x))%3;x.fin=["sel","nosel","sin"][k];if(x.fin==="sel"){N.agenda.push({d:x.date,ev:x.ev,st:"cerrada",vt:x.vt});toast("🎉 ¡Te seleccionaron!");}
   if(x.fin==="nosel"){x.why=["Precio fuera de mi presupuesto","Elegí a otro proveedor"];x.com="Nos encantó tu propuesta, pero se salió del presupuesto.";}}drawAcct();});
 p.querySelectorAll("[data-pdel]").forEach(b=>b.onclick=()=>confirmModal("¿Borrar esta postulación de tu lista?","Sí, borrar",()=>{N.post=N.post.filter(y=>y.id!==+b.dataset.pdel);drawAcct();}));
 p.querySelectorAll("[data-ag]").forEach(b=>b.onclick=()=>{const[d,st]=b.dataset.ag.split("|");const a=N.agenda.find(x=>x.d===d&&x.vt===vt);a.st=st;toast(st==="disp"?"🟢 Seguirás saliendo en búsquedas con «Fecha cerrada con disponibilidad».":"🔒 Saldrás con «Fecha cerrada» en esa fecha.");drawAcct();});
 $("blAdd").onclick=()=>{const d=$("blD").value;if(!d)return;N.agenda.push({d,ev:"Fecha ocupada (fuera de ¡HQV!)",st:"cerrada",vt});drawAcct();toast("📅 Fecha cerrada");};
 $("sReq").onclick=()=>{seedSol(vt,1);inbox("negocio",vt==="planner"?"📋 Un anfitrión te eligió como su event planner. Tienes 24 h.":"🔔 Un evento encaja contigo. Tienes 24 h para postularte.");drawAcct();};}
function seedSol(vt,n){U.neg=U.neg||{vt,sol:[],post:[],agenda:[],removed:0,sel:null};const C=[{n:"Mariana López",stars:4.8,ev:2,ver:true},{n:"Laura Méndez",stars:5,ev:1,ver:true},{n:"Grupo Andrés",stars:4.6,ev:4,ver:false},{n:"Carlos Pérez",stars:4.9,ev:3,ver:true}];
 const E=[["Boda",120,"Jardín en San Ángel"],["15 años",150,"Salón en Coyoacán"],["Cumpleaños",40,"Casa en Tlalpan"],["Posada de oficina",80,"Terraza en Polanco"]];
 const SV={svc:[["Mesas de dulces",["Mesas de dulces","Galletas decoradas"],10500],["Carritos de alimentos",["Carritos de alimentos"],7200]],venue:[["Renta del venue",["Terraza","Mobiliario incluido"],26000]],planner:[["Event planner",[],0]]};
 for(let i=0;i<n;i++){const k=U.neg.sol.length,e=E[k%E.length],c=C[k%C.length],sv=SV[vt][k%SV[vt].length],total=[182000,186000,52000,96000][k%4];
  U.neg.sol.unshift({id:now()+k*7+Math.floor(Math.random()*999),vt,kind:vt==="planner"?"planner":"svc",occ:e[0],guests:e[1],lugar:e[2],date:new Date(now()+(45+k*12)*864e5).toISOString().slice(0,10),start:"18:00",end:"01:00",zona:["Álvaro Obregón","Coyoacán","Tlalpan","Miguel Hidalgo"][k%4],km:[3.2,6.8,12,4.5][k%4],
   dl:now()+(24-k*3)*36e5,st:"nueva",cli:c,interes:[42,38,17,26][k%4],svc:sv[0],subs:sv[1],est:sv[2],total,nota:["Que combine con flores blancas y eucalipto 🌿","Somos 150 y queremos algo divertido para los chavos","",""][k%4],svcs:["Venue","Alimentos","Música","Decoración","Bebidas"].slice(0,3+k%3)});}}''')

# ---------- «Las fiestas de mis clientes»: ficha con descripción del proyecto y proveedores liberados
rep('''p.querySelectorAll("[data-job]").forEach(b=>b.onclick=()=>toast("📋 Aquí verás la descripción del proyecto de tu cliente."));return;}''',
    '''p.querySelectorAll("[data-job]").forEach(b=>b.onclick=()=>{U.jobSel=b.dataset.job;drawAcct();});
  const jj=(U.plannerJobs||[]).find(j=>j.nombre===U.jobSel)||(U.plannerJobs||[])[0];if(jj){p.insertAdjacentHTML("beforeend",jobDetailHtml(jj));bindJob(jj);}return;}
function jobEvent(j){if(j.e)return j.e;const f={nombre:j.nombre,occ:j.nombre.split(" de ")[0],kind:"social",guests:j.guests,date:j.date,hours:6,total:j.total,pp:Math.round(j.total/j.guests),zona:"Coyoacán",
  rows:[{k:"Venue",e:"🏛️",label:"Venue",amt:Math.round(j.total*.38)},{k:"Alimentos",e:"🍽️",label:"Alimentos",amt:Math.round(j.total*.24)},{k:"Música y espectáculos",e:"🎧",label:"Música y espectáculos",amt:Math.round(j.total*.08)},{k:"Decoración y flores",e:"💐",label:"Decoración y flores",amt:Math.round(j.total*.06)}]};
 const e=newEvent(f);e.paid="planner";e.planner.state="liberado";j.e=e;return e;}
function jobDetailHtml(j){const e=jobEvent(j);const lib=j.confirmado!==false;
 return`<section class="tsec"><span class="dtitle" style="font-size:12px;font-weight:900;letter-spacing:.1em;color:var(--muted)">DESCRIPCIÓN DEL PROYECTO · ${esc(j.nombre).toUpperCase()}</span>
  <div class="box"><div class="cli"><span class="av">${esc(j.cliente[0])}</span><span style="display:grid;flex:1"><span class="hint" style="font-weight:800">Tu cliente</span><b>${esc(j.cliente)}</b><span class="hint">${fdate(j.date)} · ${j.guests} invitados · pre-cotización ${money(j.total)} · tu cobro ${money(j.cobro||0)}</span></span><a class="btn wa sm" href="https://wa.me/525500000000" target="_blank" rel="noopener">💬 WhatsApp</a></div>
   <div class="contact-note">🤝 <span><b>Tanto los proveedores como tu cliente anfitrión esperan que tú des el primer paso.</b> Contáctalos y confirma quiénes quedan seleccionados en tu evento.</span></div></div>
  ${provListBox(e,false)}</section>`;}
function bindJob(j){bindProvList(j.e);}''')
# la lista de proveedores se pinta para el planner: el texto cambia si quien la ve es el planner
rep('''function provListBox(e,withPlanner){''', '''function provListBox(e,withPlanner){if(!U.events.includes(e)&&!withPlanner){const ks=Object.keys(e.provs);return`<div class="box"><h2>${em("handshake")} Proveedores de tu cliente</h2><span class="hint">Tu cliente también ve estos contactos. Lo que califiques aquí se refleja en su cuenta: él ya no tiene que hacerlo.</span>${e.removed?`<span class="hint">🗂️ ${e.removed} descartados.</span>`:""}${ks.map(k=>{const l=e.provs[k];if(!l.length)return"";return`<div class="svc-h"><h3>${l[0].emo} ${esc(k)}</h3><span class="hint">${l.length} disponibles</span></div><div class="list">${l.slice(0,3).map((x,i)=>provCard(x,i,false,e)).join("")}</div>`;}).join("")}</div>`;}''')

# ---------- demo del proveedor y botones «Ver como»
rep('''<button class="pill sm" type="button" id="demo">Ver con datos de ejemplo</button>''',
    '''<span class="who"><button class="pill sm" type="button" id="demo">👀 Ver como anfitrión</button><button class="pill sm" type="button" id="demoP">👀 Ver como proveedor</button></span>''')
rep('''$("demo").onclick=demoUser;''', '''$("demo").onclick=demoUser;
function demoProv(){U=fresh();Object.assign(U,{account:"cuenta",name:"Lupita Ramírez",last:"Ramírez",wa:"5512345678",email:"lupita@ejemplo.com",founder:38,plan:"gratis"});
 U.sides={fiestas:false,negocio:true};U.site={nombre:"Lupita Ramírez",negocio:"Lupita Dulces y Antojos",url:"hayquevernos.com/lupita-dulces-y-antojos",tipos:["services","venue","planner"],servicios:[{cat:"Alimentos"}],completo:100};
 U.neg={vt:"svc",sol:[],post:[],agenda:[],removed:0,sel:null};seedSol("svc",2);seedSol("venue",1);seedSol("planner",1);
 U.neg.post=[{id:1,vt:"svc",ev:"Cumpleaños de Carlos P. · 40 invitados",svc:"Mesas de dulces",date:new Date(now()+30*864e5).toISOString().slice(0,10),stage:2,fin:null},
  {id:2,vt:"svc",ev:"Baby shower de Sofi · 30 invitados",svc:"Galletas decoradas",date:new Date(now()+20*864e5).toISOString().slice(0,10),stage:2,fin:"sel"},
  {id:3,vt:"svc",ev:"Boda de Ana y Leo · 120 invitados",svc:"Mesas de dulces",date:new Date(now()+50*864e5).toISOString().slice(0,10),stage:2,fin:"nosel",why:["Precio fuera de mi presupuesto","Elegí a otro proveedor"],com:"Nos encantó tu propuesta, pero se salió del presupuesto."},
  {id:4,vt:"svc",ev:"Posada de oficina · 80 invitados",svc:"Carritos de alimentos",date:new Date(now()+70*864e5).toISOString().slice(0,10),stage:1,fin:"sin"}];
 U.neg.agenda=[{d:U.neg.post[1].date,ev:U.neg.post[1].ev,st:"cerrada",vt:"svc"},{d:new Date(now()+9*864e5).toISOString().slice(0,10),ev:"Fecha ocupada (fuera de ¡HQV!)",st:"disp",vt:"svc"}];U.neg.celebradas=46;
 U.plannerJobs=[{nombre:"Los XV de Valeria",cliente:"Laura Méndez",guests:150,date:new Date(now()+60*864e5).toISOString().slice(0,10),total:186000,cobro:12000}];
 inbox("negocio","🔔 Tienes 2 eventos que encajan contigo. Postúlate en menos de 24 h.");U.tab="negocio";closeJourney();show("acct");}
$("demoP").onclick=demoProv;''')
# el negocio publicado también trae solicitudes de ejemplo para ver la dinámica
rep('''U.sides.negocio=true;U.site=x;U.founder=U.founder||38;U.tab="negocio";''', '''U.sides.negocio=true;U.site=x;U.founder=U.founder||38;U.tab="negocio";U.neg=null;negState();(x.tipos||["services"]).forEach(t=>{const id=t==="services"?"svc":t;seedSol(id,id==="svc"?2:1);});''')
# Mis fiestas: un proveedor con trabajos de planner también ve sus fiestas de clientes
rep(''' p.innerHTML=`${tabs}<div class="fhead"><h2>${em("party_popper")} ${isPl?"Mis fiestas personales":"Mis fiestas"}</h2>''',
    ''' if(!U.sides.fiestas){drawInvite(p,"fiestas");p.insertAdjacentHTML("afterbegin",tabs);p.querySelectorAll("[data-sub]").forEach(b=>b.onclick=()=>{U.sub=b.dataset.sub;drawAcct();});return;}
 p.innerHTML=`${tabs}<div class="fhead"><h2>${em("party_popper")} ${isPl?"Mis fiestas personales":"Mis fiestas"}</h2>''')

P.write_text(s)
print('shell12 ok', len(s))

# ---------- cliente nuevo del planner: espera la confirmación del anfitrión antes de liberar proveedores
s = P.read_text()
s = s.replace('<span class="st go">En progreso</span></div>', '${j.nuevo&&!j.conf?`<span class="st wait">Esperando a tu cliente</span>`:`<span class="st go">En progreso</span>`}</div>', 1)
s = s.replace('''  ${provListBox(e,false)}</section>`;}''', '''  ${j.nuevo&&!j.conf?`<div class="box"><div class="lockd">${em("hourglass_not_done")}<span><b>Esperando a que ${esc(j.cliente)} confirme el trato y pague.</b> En cuanto lo haga, les liberamos a los dos los contactos de los proveedores y te avisamos aquí y por correo.</span></div><button class="sim" type="button" id="jConf">Simular: tu cliente confirmó y pagó</button></div>`:provListBox(e,false)}</section>`;}''', 1)
s = s.replace('function bindJob(j){bindProvList(j.e);}', 'function bindJob(j){const c=$("jConf");if(c){c.onclick=()=>{j.conf=true;confetti();inbox("fiestas",`🔓 ${j.cliente} confirmó. Ya ves a sus proveedores.`);drawAcct();};return;}bindProvList(j.e);}', 1)
P.write_text(s)
print('jobs ok')
