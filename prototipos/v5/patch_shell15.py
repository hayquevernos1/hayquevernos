"""v13 · Cuenta (Diego, 9 oct 2026). Correr DESPUÉS de patch_shell14.py.
- El event planner se ofrece en la cuenta, después de la pre-cotización: primero se «ilumina» el tracker de proveedores que hacen
  match (borrosos), y al terminar sale un pop-up con la oscuridad de fondo: ¿quieres un event planner? → elegir deslizando →
  «Contactar a X + proveedores» (1.ª conversión). Si dice que no: proveedores borrosos con «Contactar» en cada uno (2.ª conversión).
- Etiqueta «🤝 Negociable» en proveedores y planners que la marcaron (solo cuando es un plus).
- Ficha: nombre del evento resaltado y «✏️ Editar esta pre-cotización»; al editar o repetir una fiesta se pregunta si se actualiza
  (recomendado) o se guardan las dos versiones.
- Por celebrar: fechas populares en un toque. Bandeja: filtros Sobre mis fiestas / Sobre mi negocio. Postulaciones compactas."""
import re
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:120]
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
/* ===== v13 · cuenta ===== */
.btn.cta:hover{background:linear-gradient(135deg,#BEFF00 0%,#FAFA19 100%)!important;filter:brightness(1.05)}
button.link{border:0;background:none;color:#BE0078;font:inherit;font-weight:800;text-decoration:underline;cursor:pointer;padding:2px}
.negt{background:#E6FFF4;color:#00684A;border-radius:99px;padding:2px 9px;font-size:12px;font-weight:900;white-space:nowrap}
.trkm{height:8px;border-radius:99px;background:#eee8fb;overflow:hidden}.trkm i{display:block;height:100%;background:linear-gradient(90deg,#FA1ED2,#FF6905);transition:width .5s}
.int .st.wait{animation:pulse 1.2s ease-in-out infinite}@keyframes pulse{50%{opacity:.45}}
.sheet.plo{max-width:480px;text-align:center;justify-items:center}
.sheet.plo .plcard{width:100%;text-align:left}
.prov .ctp{justify-self:end}
.fch .fh .fnm{font-size:20px;font-weight:900;line-height:1.15;letter-spacing:-.01em}
.popd{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;align-items:center}
.popd .chip{font-size:13px}
.infl{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 4px}
.infl button{border:0;border-radius:99px;padding:8px 14px;font-weight:900;font-size:13.5px;background:#fff;box-shadow:var(--hqv-clay-sm);color:#1a1033}
.infl button[aria-selected="true"]{background:#1a1033;color:#fff}
.infl button.fs[aria-selected="true"]{background:linear-gradient(160deg,#FA1ED2,#FF6905)}
.infl button.nb[aria-selected="true"]{background:linear-gradient(160deg,#9146FF,#FA1ED2)}
.pst{background:#fff;border-radius:18px;padding:10px 12px;display:grid;gap:8px;box-shadow:var(--hqv-clay-sm);border-left:6px solid #9146FF}
.pst.sel{border-left-color:#00A884}.pst.nosel{border-left-color:#c0264b}.pst.sin{border-left-color:#9b94b5}
.pst .pt{display:flex;gap:10px;align-items:center}
.pst .pic{flex:0 0 34px;height:34px;border-radius:50%;background:#EFE6FF;display:grid;place-items:center}
.pst .pt b{display:block;font-size:14.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pst .pt small{display:block;color:var(--muted);font-size:12px}
.pst .pdel{border:0;background:none;font-size:16px;cursor:pointer;padding:4px}
.dots{display:grid;grid-template-columns:repeat(4,1fr);gap:4px}
.dots span{display:grid;gap:3px;font-size:10.5px;font-weight:800;color:var(--muted);text-align:center}
.dots i{height:5px;border-radius:99px;background:#e6e1f5}
.dots .on{color:#1a1033}.dots .on i{background:#9146FF}.dots .ok i{background:#00A884}.dots .no i{background:#c0264b}.dots .mute i{background:#9b94b5}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# ---------- planners negociables
i = s.index('\n', s.index('const PLANNERS=[{n:"Ana Robles"'))
s = s[:i] + '\nPLANNERS.forEach((p,i)=>p.neg=i%2===0);' + s[i:]
rep('fee:p.fee||p.f,sp:', 'neg:!!p.neg,fee:p.fee||p.f,sp:')
func('plCardHtml', r'''
function plCardHtml(p,extra="",anim=false){return`<div class="plcard${anim?" hint-anim":""}" id="plcard"><div class="hd"><span class="av" data-plprof="1" title="Ver su perfil completo">${p.img?`<img src="${p.img}" alt="">`:p.emo}</span><span style="flex:1;min-width:0;cursor:pointer" data-plprof="1"><b style="font-size:17px">${esc(p.n)}</b><span class="hint" style="display:block">⭐ ${p.r} · ${p.y} años · ${esc(p.z||"")} · <u>ver perfil</u></span></span><span style="display:grid;justify-items:end;gap:4px"><b>Desde ${money(p.fee)}</b>${p.neg?'<span class="negt">🤝 Negociable</span>':""}</span></div>${p.b?`<span>${esc(p.b)}</span>`:""}<span class="hint">${esc(p.sp||"")}</span>${extra}</div>`;}
''')
rep('<div><b>Desde ${money(p.fee||5000)}</b><span class="hint">por evento</span></div>',
    '<div><b>Desde ${money(p.fee||5000)}</b><span class="hint">por evento</span>${p.neg?\'<span class="negt" style="justify-self:center">🤝 Negociable</span>\':""}</div>')

# ---------- proveedores negociables + «Contactar» en cada uno
rep('rows.forEach(r=>provs[r.k]=providersFor(r));', 'rows.forEach(r=>{provs[r.k]=providersFor(r);provs[r.k].forEach((x,i)=>x.neg=(x.nm.length+i)%3===0);});')
rep('<span>⭐ ${x.rate} (${x.rev})</span>', '<span>⭐ ${x.rate} (${x.rev})</span>${x.neg?"<span>🤝 Negociable</span>":""}')
rep('if(blur)return`<div class="prov">${top}</div>`;',
    'if(blur)return`<div class="prov">${top}${e&&!e.paid?\'<button class="btn cta sm ctp" type="button">Contactar →</button>\':""}</div>`;')

# ---------- interestBox con tracker y planner elegido
func('interestBox', r'''
function interestBox(e,pre){const ks=Object.keys(e.provs),pl=e.opts.planner&&e.planner.cur,anim=pre&&!e.trk,st=e.trkStep||0;
 const head=anim?`Buscando en la comunidad ¡Hay que vernos!…`:pl?`${esc(first(pl.n))} y ${e.interes} proveedores más están disponibles para tu evento.`:`${e.interes} proveedores están disponibles para tu evento.`;
 const lines=`<div class="int">${ks.map((k,i)=>{const ok=!anim||i<st;return`<div class="ln"><span>${e.provs[k][0].emo} ${esc(k)}</span><span class="st ${ok?"vis":"wait"}" id="tk-${i}">${ok?`✅ ${e.provs[k].length} hacen match`:"⏳ buscando…"}</span></div>`;}).join("")}</div><div class="trkm"><i id="tkM" style="width:${anim?Math.round(st/ks.length*100):100}%"></i></div>`;
 let body;
 if(!pre)body=`<div class="lock">${em("locked")}<span>Tu planner y tú los verán al mismo tiempo.</span></div>`;
 else if(pl)body=`<span class="hint" style="font-weight:900;letter-spacing:.06em">TU EVENT PLANNER</span>${plCardHtml(pl)}
  <button class="btn cta" type="button" id="contact" style="justify-self:stretch">Contactar a ${esc(first(pl.n))} + proveedores →</button>
  <span class="hint" style="text-align:center">Pago único: ${money(PR.proveedoresMasPlanner)} · el cobro de ${esc(first(pl.n))} lo acuerdas directo con él o ella.</span>
  <div class="row" style="gap:14px;justify-content:center"><button class="link" type="button" id="plChg">Ver otros planners</button><button class="link" type="button" id="plSolo">Prefiero organizar yo</button></div>`;
 else body=`${ks.map(k=>`<div class="svc-h"><h3>${e.provs[k][0].emo} ${esc(k)}</h3><span class="hint">${e.provs[k].length} hacen match</span></div><div class="list">${e.provs[k].slice(0,2).map((x,i)=>provCard(x,i,true,e)).join("")}</div>`).join("")}
  <button class="btn cta" type="button" id="contact" style="justify-self:stretch">Contactar proveedores →</button><span class="hint" style="text-align:center">Pago único: ${money(PR.desbloquearProveedores)} · desbloqueas a todos los de tu fiesta.</span>
  <div class="soft" style="text-align:center">📋 <span>¿Prefieres que un event planner organice tu fiesta por ti? <button class="link" type="button" id="plAsk">Conocer event planners</button></span></div>`;
 return`<div class="box"><h2 id="tkH">${em("star-struck")} ${head}</h2><span class="hint">${pre?"Cumplen con lo que pides, están cerca de ti y libres en tu fecha.":"Se liberan en cuanto tu event planner confirme el trato."}</span>
 ${lines}<div id="trkBody" style="display:grid;gap:12px" ${anim?"hidden":""}>${body}</div></div>`;}
let trkTimer=null;
function startTracker(e){clearTimeout(trkTimer);const ks=Object.keys(e.provs),fast=matchMedia("(prefers-reduced-motion: reduce)").matches;
 const tick=()=>{if(U.eventId!==e.id||U.tab!=="fiestas"||U.view!=="acct")return;if(!$("modal").hidden){trkTimer=setTimeout(tick,400);return;}
  e.trkStep=(e.trkStep||0)+1;const i=e.trkStep-1,el=$("tk-"+i),k=ks[i];if(el&&k){el.className="st vis";el.textContent=`✅ ${e.provs[k].length} hacen match`;}
  const m=$("tkM");if(m)m.style.width=Math.round(e.trkStep/ks.length*100)+"%";
  if(e.trkStep>=ks.length){e.trk=true;track("tracker_completo",{proveedores:e.interes});setTimeout(()=>{drawAcct();if(!e.plAsked&&!e.paid)setTimeout(()=>{if(U.eventId===e.id&&U.tab==="fiestas")plOffer(e);},fast?0:700);},fast?0:500);}
  else trkTimer=setTimeout(tick,fast?0:650);};
 trkTimer=setTimeout(tick,fast?0:700);}
function bindInterest(e){const on=(id,fn)=>{const b=$(id);if(b)b.onclick=fn;};
 on("contact",()=>startPay(e));document.querySelectorAll(".ctp").forEach(b=>b.onclick=()=>startPay(e));
 on("plAsk",()=>plOffer(e));on("plChg",()=>plOffer(e,"swipe"));
 on("plSolo",()=>{e.opts.planner=false;e.planner.cur=null;track("planner_oferta",{si:false,despues:true});drawAcct();});
 document.querySelectorAll("#evRight [data-plprof]").forEach(x=>x.onclick=ev=>{ev.stopPropagation();plannerProfile(e.planner.cur);});
 if(!e.trk)startTracker(e);}
/* Pop-up: primera mención del event planner, ya con la pre-cotización entregada */
function plOffer(e,step){const m=$("modal");e.plAsked=true;step=step||"ask";const pool=PLANNERS.map(normPl);e.plI=(e.plI||0)%pool.length;const c=pool[e.plI],cur=e.planner.cur;
 const close=()=>{m.hidden=true;drawAcct();};
 if(step==="ask")m.innerHTML=`<div class="sheet plo"><img src="img/c_05.webp" alt="" style="width:110px"><h2>¿Quieres que un event planner organice tu fiesta?</h2><span>Ya tienes tu pre-cotización 🎉 Si prefieres no coordinar tú a ${e.interes} proveedores, un event planner de la comunidad ¡Hay que vernos! lo hace por ti, de principio a fin.</span><div class="soft" style="text-align:left"><span>💡 Su cobro lo acuerdas directo con él o ella. No lo pagas aquí ni junto con nada.</span></div><div class="yn2" style="width:100%"><button class="btn ghost" type="button" id="poNo">No, yo organizo</button><button class="btn cta" type="button" id="poYes">Sí, quiero conocerlos</button></div></div>`;
 if(step==="swipe")m.innerHTML=`<div class="sheet plo"><h2>Elige a tu event planner</h2><span class="hint">Desliza a la derecha si te gusta o a la izquierda para ver otra opción. Toca su foto para ver su perfil completo.</span>${plCardHtml(c,"",true)}<div class="yn2" style="width:100%"><button class="btn ghost" type="button" id="poNext">✕ Siguiente</button><button class="btn cta" type="button" id="poPick">💙 Lo quiero</button></div><span class="hint">${e.plI+1} de ${pool.length}</span><button class="pill sm" type="button" id="poX">Ahora no</button></div>`;
 if(step==="chosen")m.innerHTML=`<div class="sheet plo"><h2>¡Excelente elección! 💙</h2>${plCardHtml(cur)}<span>${esc(first(cur.n))} recibe tu pre-cotización completa y coordina por ti a tus ${e.interes} proveedores disponibles.</span><button class="btn cta" type="button" id="poGo" style="width:100%">Contactar a ${esc(first(cur.n))} + proveedores →</button><span class="hint">Pago único: ${money(PR.proveedoresMasPlanner)} · el cobro de ${esc(first(cur.n))} lo acuerdas directo con él o ella.</span><div class="row" style="gap:14px;justify-content:center"><button class="link" type="button" id="poOther">Ver otro planner</button><button class="link" type="button" id="poLater">Lo decido después</button></div></div>`;
 m.hidden=false;const on=(id,fn)=>{const b=$(id);if(b)b.onclick=fn;};
 on("poNo",()=>{track("planner_oferta",{si:false});close();});
 on("poYes",()=>{track("planner_oferta",{si:true});plOffer(e,"swipe");});
 on("poNext",()=>{e.plI++;plOffer(e,"swipe");});
 on("poPick",()=>{e.opts.planner=true;e.planner.cur=c;track("planner_elegido",{planner:c.n});plOffer(e,"chosen");});
 on("poX",close);on("poLater",close);on("poOther",()=>{e.plI++;plOffer(e,"swipe");});
 on("poGo",()=>{m.hidden=true;drawAcct();startPay(e);});
 m.querySelectorAll("[data-plprof]").forEach(x=>x.onclick=ev=>{ev.stopPropagation();plannerProfile(step==="chosen"?cur:c,()=>plOffer(e,step));});
 const cd=m.querySelector("#plcard");if(cd&&step==="swipe"){let x0=null;cd.onpointerdown=ev=>{if(ev.target.closest("[data-plprof]"))return;x0=ev.clientX;cd.setPointerCapture(ev.pointerId);};cd.onpointermove=ev=>{if(x0!==null)cd.style.transform=`translateX(${ev.clientX-x0}px) rotate(${(ev.clientX-x0)/20}deg)`;};
  cd.onpointerup=ev=>{const dx=ev.clientX-(x0??ev.clientX);x0=null;cd.style.transform="";if(dx>90)$("poPick").click();else if(dx<-90)$("poNext").click();};}}
''')
rep('if(!e.paid){const c=$("contact");if(c)c.onclick=()=>startPay(e);return;}', 'if(!e.paid){bindInterest(e);return;}')

# ---------- ficha: nombre resaltado + editar
rep('''<small>${esc(f.nombre||f.occ)} · ${f.guests.toLocaleString("es-MX")} invitados · ${fdate(f.date)}</small>''',
    '''<b class="fnm">${esc(f.nombre||f.occ)}</b><small>${f.guests.toLocaleString("es-MX")} invitados · ${fdate(f.date)}</small>''')
rep('''<button type="button" data-vx="${e.id}|${i}" aria-label="Borrar versión" title="Borrar">✕</button></span></div>`).join("")}</div></div>`;}''',
    '''<button type="button" data-vx="${e.id}|${i}" aria-label="Borrar versión" title="Borrar">✕</button></span></div>`).join("")}<button class="btn ghost sm" type="button" data-ved="${e.id}" style="justify-self:start">✏️ Editar esta pre-cotización</button></div></div>`;}''')
rep('''<button class="pill sm" type="button" id="evEdit">🔄 Recalcular (crea una versión nueva)</button>''',
    '''<button class="pill sm" type="button" id="evEdit">✏️ Editar esta pre-cotización</button>''')
rep(''' p.querySelectorAll("[data-vd]").forEach(''', ''' p.querySelectorAll("[data-ved]").forEach(b=>b.onclick=()=>openJourney("fiestas",true,b.dataset.ved));
 p.querySelectorAll("[data-vd]").forEach(''')
rep('''f.src=(k==="negocio"?"negocio.html":"fiestas.html")+"?"+q.toString();''',
    '''f.src=(k==="negocio"?"negocio.html":"fiestas.html")+"?"+q.toString();
 const evE=editEv&&U.events.find(x=>x.id===editEv);f.onload=evE&&evE.state?()=>{try{f.contentWindow.postMessage({hqv:"cargar",state:evE.state},"*");}catch(_){}f.onload=null;}:null;''')
func('saveFiesta', r'''
function saveFiesta(d){U.sides.fiestas=true;const old=(U.editing&&U.events.find(x=>x.id===U.editing))||U.events.find(x=>x.f.occ===d.fiesta.occ&&x.f.date===d.fiesta.date);
 const fin=(ev,isNew)=>{U.editing=null;U.tab="fiestas";U.eventId=ev.id;closeJourney();show("acct");confetti();
  inbox("fiestas",`📄 Te enviamos la pre-cotización de «${ev.f.nombre||ev.f.occ}» a tu correo, con un botón para mandártela a tu WhatsApp.`);if(isNew)onboarding(ev);else toast("✅ Pre-cotización actualizada");};
 if(old){const nv=newEvent(d.fiesta),m=$("modal");closeJourney();U.tab="fiestas";U.eventId=old.id;show("acct");
  m.innerHTML=`<div class="sheet"><img src="img/ball.webp" alt="" style="width:70px"><h2>¿Actualizamos tu pre-cotización?</h2><span>Ya tienes «${esc(old.f.nombre||old.f.occ)}». Para que siempre veas la versión más vigente, la nueva <b>reemplaza</b> a la anterior.</span><button class="btn cta" type="button" id="upY">Sí, actualizarla</button><button class="pill sm" type="button" id="upN">No, guardar las dos versiones</button></div>`;m.hidden=false;
  const upd=keep=>{m.hidden=true;const vs=keep?[{f:nv.f,t:now()},...(old.versions||[{f:old.f,t:old.t||now()}])]:[{f:nv.f,t:now()}];Object.assign(old,{f:nv.f,provs:nv.provs,interes:nv.interes,state:d.state,versions:vs,trk:false,trkStep:0});track("precotizacion_editada",{reemplazo:!keep});fin(old,false);};
  $("upY").onclick=()=>upd(false);$("upN").onclick=()=>upd(true);return;}
 const ev=newEvent(d.fiesta);ev.versions=[{f:ev.f,t:now()}];ev.cta=d.cta||"guardar";ev.state=d.state;U.events.unshift(ev);fin(ev,true);}
''')
rep('si recalculas, guardamos cada versión', 'si la editas, aquí se actualiza con la versión más vigente')

# ---------- Por celebrar: fechas populares
rep('function agendaBar(){return`', 'const POPD=[["💘","Día del amor y la amistad",2,14],["🧸","Día del niño",4,30],["💐","Día de la madre",5,10],["🍎","Día del maestro",5,15],["🏳️‍🌈","Pride",6,0],["👴","Día del abuelo",8,28],["🇲🇽","15 de septiembre",9,15],["🎃","Halloween",10,31],["🪅","Posada",12,16],["🎄","Navidad",12,24],["🎆","Año nuevo",12,31]];\nfunction popNext(mo,d){const t=new Date();for(const y of [t.getFullYear(),t.getFullYear()+1]){let dt;if(d===0){dt=new Date(y,mo,0);while(dt.getDay()!==6)dt.setDate(dt.getDate()-1);}else dt=new Date(y,mo-1,d);if(dt>t)return`${dt.getFullYear()}-${String(dt.getMonth()+1).padStart(2,"0")}-${String(dt.getDate()).padStart(2,"0")}`;}}\nfunction agendaBar(){return`')
rep('''<span class="hint" id="agMsg" aria-live="polite" style="width:100%" hidden></span></form>`;}''',
    '''<span class="hint" id="agMsg" aria-live="polite" style="width:100%" hidden></span></form><div class="popd"><span class="hint">Fechas populares · tócalas y se agendan solas:</span>${POPD.map(([e_,nm],i)=>`<button type="button" class="chip" data-pop="${i}" aria-pressed="${U.agenda.some(a=>a.w===nm)}">${e_} ${nm}</button>`).join("")}</div>`;}''')
rep('function bindAgenda(){const f=$("agF");',
    'function bindAgenda(){document.querySelectorAll("[data-pop]").forEach(b=>b.onclick=()=>{const[e_,nm,mo,d]=POPD[+b.dataset.pop],i=U.agenda.findIndex(a=>a.w===nm);if(i>=0)U.agenda.splice(i,1);else{U.agenda.push({w:nm,d:popNext(mo,d)});U.agenda.sort((a,b)=>a.d.localeCompare(b.d));track("agenda_popular",{fecha:nm});toast(`📅 ${nm} agendado. Te avisamos ${RG.diasRecordatorio} días antes.`);}drawAcct();});\n const f=$("agF");')

# ---------- Bandeja con filtros
func('drawInbox', r'''
function drawInbox(p){U.inbox.forEach(m=>m.read=true);drawTop();U.inF=U.inF||"todo";
 const promos=[{side:"todos",txt:"🎓 Curso gratis: cómo cotizar tu servicio para ganar más fiestas. Cupo limitado.",promo:true}];
 const all=[...U.inbox,...promos].filter(m=>U.inF==="todo"||m.side===U.inF);
 p.innerHTML=`<div class="box" style="max-width:760px"><h2>${em("speech_balloon")} Bandeja</h2><span class="hint">Solicitudes, respuestas, avisos y novedades de tus dos lados.</span>
 <div class="infl" role="tablist">${[["todo","Todo",""],["fiestas","🎉 Sobre mis fiestas","fs"],["negocio","💼 Sobre mi negocio","nb"]].map(([k,t,c])=>`<button type="button" role="tab" class="${c}" data-inf="${k}" aria-selected="${U.inF===k}">${t}</button>`).join("")}</div>
 <div class="list">${all.map(m=>`<div class="item"><span class="st ${m.side==="negocio"?"vis":m.side==="fiestas"?"new":"wait"}">${m.side==="negocio"?"Mi negocio":m.side==="fiestas"?"Mis fiestas":"Novedad"}</span><span class="grow">${esc(m.txt)}</span></div>`).join("")||'<div class="empty"><span class="hint">No hay mensajes aquí.</span></div>'}</div></div>`;
 p.querySelectorAll("[data-inf]").forEach(b=>b.onclick=()=>{U.inF=b.dataset.inf;drawAcct();});}
''')

# ---------- Postulaciones compactas (distintas de las solicitudes)
func('postHtml', r'''
function postHtml(x){const fin=x.fin,last=fin==="sel"?["ok","✅ Seleccionado"]:fin==="nosel"?["no","No seleccionado"]:fin==="sin"?["mute","💤 Sin comentarios"]:["","Resultado"];
 return`<div class="pst ${fin||""}"><div class="pt"><span class="pic">📨</span><span style="flex:1;min-width:0"><b>${esc(x.ev)}</b><small>${esc(x.svc)} · ${fdate(x.date)}</small></span><button class="pdel" type="button" data-pdel="${x.id}" aria-label="Borrar postulación" title="Borrar">🗑️</button></div>
  <div class="dots">${STG.map((t,i)=>`<span class="${i<=x.stage?"on":""}"><i></i>${t}</span>`).join("")}<span class="${fin?"on "+last[0]:""}"><i></i>${last[1]}</span></div>
  ${fin==="nosel"?`<div class="soft" style="font-size:13px"><b>Motivos del anfitrión</b><span>${esc((x.why||[]).join(" · "))}</span>${x.com?`<span>«${esc(x.com)}»</span>`:""}</div>`:""}
  ${fin==="sin"?`<span class="hint">Pasaron 24 h sin respuesta. Dale seguimiento por WhatsApp o bórrala.</span>`:""}
  ${fin==="sel"?`<span class="hint">🎉 ¡Quedaste! ${fdate(x.date)} quedó como fecha cerrada en tu agenda.</span>`:""}
  ${!fin?`<button class="sim" type="button" data-ps="${x.id}" style="justify-self:start">Simular siguiente paso</button>`:""}</div>`;}
''')

# ---------- demo: el demo ya eligió a su planner
rep('const pe=newEvent(past);pe.paid="prov";const fe=newEvent(f);', 'const pe=newEvent(past);pe.paid="prov";const fe=newEvent(f);fe.trk=pe.trk=true;fe.plAsked=pe.plAsked=true;')

s = s.replace('PROTOTIPO v11', 'PROTOTIPO v13')
P.write_text(s)
print('shell15 ok', len(s))
