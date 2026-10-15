"""v27 · svc7_v26.js → svc7.js
Textos nuevos, vocabulario (servicio / producto, staff), orden de la ficha, totales grandes, saltar al primer error,
componentes en lista, aviso de cambio de precio en paquetes, animación de paquetes bloqueados, pop-up «Arma paquetes con
todo tu negocio», event planner como pieza de paquetes (tú o una persona invitada que acepta)."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'svc7_v26.js').read_text()


def rep(a, b, c=1):
    global s
    assert s.count(a) == c, ('NO/MULTI', a[:110], s.count(a))
    s = s.replace(a, b)


# ---------- vocabulario ----------
rep('const RU_TL={rent:["📦 Insumos sin personal","Lo llevas o lo recogen"],full:["🙋 Insumos con personal","Tu equipo va al evento"],labor:["🙋 Personal","Por perfil"]};',
    'const RU_TL={rent:["📦 Servicio / producto sin staff","Lo llevas o lo recogen"],full:["🙋 Servicio / producto con staff","Tu staff va al evento"],labor:["🙋 Staff","Por perfil"]};')
rep('const ruFN={rent:"📦 Insumos sin personal",full:"🙋 Insumos con personal",labor:"🙋 Personal"};',
    'const ruFN={rent:"📦 Servicio / producto sin staff",full:"🙋 Servicio / producto con staff",labor:"🙋 Staff"};')
rep('🙋 Sumamos a «Tu personal»:', '🙋 Sumamos a «Tu staff»:')
rep('m.push("precio de los insumos")', 'm.push("precio del servicio")')
rep('m.push("precio y forma de cobro de tu personal")', 'm.push("precio y forma de cobro de tu staff")')
rep('m.push("cómo entregas sin personal")', 'm.push("cómo entregas sin staff")')
rep('"🍽️ Alimentos para tu personal (fiesta de más de 5 h)"', '"🍽️ Alimentos para el staff (fiesta de más de 5 h)"')
rep('🙋 Personal</span><h4>${esc(p.name)}</h4>${ruTarsOk', '🙋 Staff</span><h4>${esc(p.name)}</h4>${ruTarsOk')
rep('$("ruStaffH").textContent=`🙋 Tu personal (${ST.length})`;', '$("ruStaffH").textContent=`🙋 Tu staff (${ST.length})`;')
rep('`Quitaste a «${p.name}» de tu personal`', '`Quitaste a «${p.name}» de tu staff`')
rep('"Elige 2 o más: formas de contratar, personal"+(ruVenueItem()?" o tu venue":"")', '"Elige 2 o más: servicios, staff"+(ruVenueItem()?", tu venue":"")+(ruPlanners().length?" o coordinación":"")')
rep('<h3 id="ruStaffH">🙋 Tu personal</h3>', '<h3 id="ruStaffH">🙋 Tu staff</h3>')
rep('<b>🙋 Personal por persona<small class="ctag">Contrátalo solo o súmalo a tu fiesta</small></b>', '<b>🙋 Staff por persona<small class="ctag">Contrátalo solo o súmalo a tu fiesta</small></b>')
rep('sub:ruFN[w]+(w==="full"?" · insumos aquí; tu personal con sus tarifas":"")', 'sub:ruFN[w]+(w==="full"?" · el servicio aquí; tu staff con sus tarifas":"")')
rep('sub:"🙋 Tu personal",price:t.p', 'sub:"🙋 Tu staff",price:t.p')
rep('Si ofreces comida, bebida, personal o algo más dentro de tu venue', 'Si ofreces comida, bebida, staff o algo más dentro de tu venue')
rep('const G=[["prod","Tus productos"],["staff","Tu personal"],["pkg","Tus paquetes"]];', 'const G=[["prod","Tus productos"],["staff","Tu staff"],["pkg","Tus paquetes"]];')
rep(' · con los precios de tu personal', ' · con los precios de tu staff')
rep('tu venue es una pieza más, junto a tus productos y tu personal.', 'tu venue es una pieza más, junto a tus productos y tu staff.')
rep('comida, bebida, personal o lo que ofrezcas en tu venue', 'comida, bebida, staff o lo que ofrezcas en tu venue')

# ---------- «Arma tu servicio» ----------
rep('<span>Desliza cada rodillo. Lo que queda en la línea verde es tu selección.</span>', '<span>Desliza y alinea en verde los factores para configurar un servicio.</span>')
rep('Guardar esta combinación ✓', 'Guardar servicio ✓')
rep('<span class="ru-unit" id="ruUnit"></span>', '<span class="ru-unit" id="ruUnit" hidden></span>')
rep('<p class="sub">Arma tu servicio alineando los rodillos. Nosotros se lo mostramos al anfitrión por persona y en total.</p>\n', '')
rep('<small>Uno por uno: alinea los rodillos, guarda y dale identidad. Cada uno te da un emblema 🏅.</small>', '<small>Enlista los bienes y servicios que provees de manera unitaria.</small>')
rep('<small>Después combinas: catering + personal + ${S.types&&S.types.venue?"tu venue":"música"}.</small>', '<small>Después combina tus productos para armar paquetes.</small>')
rep('Aún no guardas productos. Alinea los rodillos y toca «Guardar esta combinación».', 'Aún no guardas productos. Alinea los rodillos y toca «Guardar servicio».')
# sección de event planners en el armador
rep('''<div class="ru-bar" id="ruBar" hidden>''', '''<section class="ru-stsec" id="ruPlSec"><div class="ru-lh"><h3>🧭 Event planners</h3><button class="btn ghost sm" id="ruInv" type="button">＋ Invitar a un event planner</button></div><span class="hint">La coordinación del evento entra en tus paquetes como una pieza más.</span><div class="ru-grid" id="ruPl"></div></section>
 <div class="ru-bar" id="ruBar" hidden>''')

# ---------- ficha: nombre como título, orden y textos ----------
TITLE = '<input id="ruName" class="ru-title${MISS(filled(p.name))}" value="${esc(p.name)}" placeholder="${pk?"Asígnale un nombre a este paquete":"Asígnale un nombre a este servicio"}" aria-label="Nombre">'
rep('<span class="ru-pkb">🎁 Paquete</span><h3>Dale identidad a tu paquete</h3><div class="ru-crumbs ru-kits">', '<span class="ru-pkb">🎁 Paquete</span>' + TITLE + '<div class="ru-crumbs ru-kits">')
rep(':sk?`<span class="ru-stb">🙋 Tu personal</span><h3>', ':sk?`<span class="ru-stb">🙋 Tu staff</span><h3>')
rep(':`<h3>Dale identidad</h3><div class="ru-crumbs">${p.dims.map(d=>`<span>${esc(d)}</span>`).join("")}${p.otro?`<span>${esc(p.otro)}</span>`:""}</div>`;',
    ':`<div class="ru-crumbs">${p.dims.map(d=>`<span>${esc(d)}</span>`).join("")}${p.otro?`<span>${esc(p.otro)}</span>`:""}</div>' + TITLE + '`;')
rep(''' ${sk?"":`<div class="field"><label class="lbl" for="ruName">Nombre</label><input id="ruName" class="${MISS(filled(p.name))}" value="${esc(p.name)}" placeholder="${pk?"Nombre del paquete":"Nombre de tu producto"}"></div>`}
''', '')
rep('<span class="ru-sl">🧺 Insumos <span class="opt">solo el nombre; alcanzan para tus personas</span></span>', '<span class="ru-sl">🧺 Incluye</span>')
rep('🚚 ¿Cómo lo entregas y cobras?', '🚚 ¿Cómo entregas y cobras?')
rep('m.push("cómo lo entregas y cobras")', 'm.push("cómo entregas y cobras")')
rep('''  ${p.tw.includes("rent")?`<div class="ru-tg" data-w="rent"><b>${RU_TL.rent[0]}</b>${dlSecHtml(p.dlx,k+"dlx","rt","¿Cómo lo entregas?")}</div>`:""}
  ${p.tw.includes("full")?`<div class="ru-tg" data-w="full"><b>${RU_TL.full[0]}</b><span class="ru-note">🚚 La entrega y el montaje van incluidos: tu equipo va al evento.</span>${ruLaborHtml(p,staff)}</div>`:""}</div>`}''',
    '''  ${p.tw.includes("full")?`<div class="ru-stw" data-w="full">${ruLaborHtml(p,staff)}</div>`:""}
  ${p.tw.includes("rent")?`<div class="ru-tg ru-dlw" data-w="rent"><b>¿Cómo entregas?</b>${dlSecHtml(p.dlx,k+"dlx","rt","¿Cómo entregas?")}</div>`:""}</div>`}''')
rep('<b>🧺 Precio de los insumos</b><span class="hint">Es el mismo con o sin personal; tu equipo se suma aparte.</span>', '<b>💲 Precio del servicio</b><span class="hint">Es el mismo con o sin staff; el staff se cobra aparte.</span>')
rep('aria-label="Precio de los insumos"', 'aria-label="Precio del servicio"')
rep('<b>${sk?"🙋 Precio de este perfil":"🙋 Tu personal"}</b>', '<b>${sk?"🙋 Precio de este perfil":"🙋 Precio del staff"}</b>')
rep('"Cuántos mandas y cuánto cobra cada uno. Si ya lo usaste antes, lo llenamos por ti. Cada perfil se vuelve un producto que el anfitrión puede contratar solo."',
    '"Cuántos mandas y cuánto cobra cada uno. Si ya lo usaste antes, lo llenamos por ti. Con staff, la entrega y el montaje van incluidos. Cada perfil se vuelve un producto que el anfitrión puede contratar solo."')
rep('title="Precio guardado en Tu personal"', 'title="Precio guardado en Tu staff"')
rep('"🍽️ Alimentos al personal (+5 h)"', '"🍽️ Alimentos para el staff (+5 h)"')
rep('El tiempo cuenta desde que tu personal llega.', 'El tiempo cuenta desde que tu staff llega.')
rep('<b>Tu equipo en esa fiesta</b>', '<b>Tu staff en esa fiesta</b>')
# aviso: por hora sale más barato que el turno
rep('''    <button type="button" class="link ru-addt">＋ Otra forma de cobrarlo</button>''',
    '''    ${(()=>{const tu=r.tars.find(t=>t.u==="Por turno (5 h)"&&+t.p>0),th=r.tars.find(t=>t.u==="Por hora"&&+t.p>0);return tu&&th&&th.p*5<+tu.p?`<span class="ru-warn">💡 Tu tarifa por hora sale más barata que tu turno de 5 h (5 × ${money(th.p)} = ${money(th.p*5)} contra ${money(tu.p)}). ¿Es correcto?</span>`:"";})()}
    <button type="button" class="link ru-addt">＋ Otra forma de cobrarlo</button>''')
# así lo verá el anfitrión: total grande, por persona abajo
rep('''function ruHost(p){if(p.kind==="staff")return ruExHtml(p);const pax=+p.pax;if(!pax||!p.tw.length)return"";const L=p.tw.map(w=>{const r=ruTotal(p,w);return r?`<span>${RU_TL[w][0]}: <b>${ruMoney(r.pp)}</b> por persona · <b>${ruMoney(r.tot)}</b> en total</span>`:"";}).filter(Boolean);
 return L.length?`<div class="ru-host"><b>👀 Así lo verá el anfitrión</b><span class="hint">En una fiesta de ${pax} personas${p.tw.includes("full")?" (con personal: fiesta de 5 h)":""}:</span>${L.join("")}</div>`:"";}''',
    '''function ruHost(p){if(p.kind==="staff")return ruExHtml(p);const pax=+p.pax;if(!pax||!p.tw.length)return"";const L=p.tw.map(w=>{const r=ruTotal(p,w);return r?`<div class="ru-hr"><span class="ru-hl">${RU_TL[w][0]}</span><span class="ru-tot">${ruMoney(r.tot)}</span><small class="ru-ppx">total del evento · <b>${ruMoney(r.pp)}</b> por persona</small></div>`:"";}).filter(Boolean);
 return L.length?`<div class="ru-host"><b>👀 Así lo verá el anfitrión</b><span class="hint">En una fiesta de ${pax} personas${p.tw.includes("full")?" (con staff: fiesta de 5 h)":""}:</span><div class="ru-hrows">${L.join("")}</div></div>`:"";}''')

# ---------- guardar: saltar al primer error ----------
rep('''$("ruOk").onclick=()=>{const m=ruMiss(p),er=$("ruErr");if(m.length){er.hidden=false;er.textContent="Falta: "+m.join(", ")+".";if(m.some(x=>/extra|entrega|mínimo|promoción/.test(x))){p._moreOpen=true;box.querySelector("details.ru-more").open=true;}return;}''',
    '''$("ruOk").onclick=()=>{const m=ruMiss(p);if(m.length){if(m.some(x=>/extra|mínimo|promoción/.test(x)))p._moreOpen=true;showMiss=true;ruDrawIdent();const er=$("ruErr");er.hidden=false;er.textContent="Falta: "+m.join(", ")+".";
   const f=[...box.querySelectorAll(".miss")].find(x=>x.offsetParent!==null)||er;f.scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"center"});setTimeout(()=>{const i=f.matches("input,select,textarea")?f:f.querySelector("input,select,textarea");i&&i.focus({preventScroll:true});},350);return;}
  if(p.kind==="pkg")p.sugAt=ruSug(p);''')

# ---------- componentes en lista ----------
rep('function ruFormDesc(p,w){', '''function ruFormItems(p,w,site){if(w==="rent")return["Servicio / producto",...(p.dlx.dl.length?p.dlx.dl.map(d=>(DL_LABEL[d.m]||d.m)+(d.cobra?" (con costo)":DL_NOFEE.includes(d.m)?"":" (incluida)")):[])];
 const L=p.lpol;return["Servicio / producto",...p.labor.map(r=>`${r.q} ${ruPl(r.n,r.q)}`),"Entrega y montaje incluidos",...(site?["Precio para fiesta de 5 h",L.night?`Después de las 12:00 a.m. +${L.nightPct}%`:"",L.ride?"Transporte de regreso del staff a cargo del anfitrión":""]:[])].filter(Boolean);}
const ruUl=(L,c)=>`<ul class="${c||"ru-ul"}">${L.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>`;
function ruFormDesc(p,w){''')
rep('<small class="ru-fd">${esc(ruFormDesc(p,w))}</small>', '${ruUl(ruFormItems(p,w))}')
rep('''<span class="ru-meta">Para ${esc(p.pax||"—")} personas · ${esc(p.items.map(ref=>ruItemName(ref,p)).join(" + "))}</span>''',
    '''<span class="ru-meta">Para ${esc(p.pax||"—")} personas · incluye:</span>${ruUl(p.items.map(ref=>ruItemName(ref,p)))}${(()=>{const now=ruSug(p);return p.sugAt&&Math.abs(now-p.sugAt)>=1?`<div class="ru-chg">⚠️ Lo que incluye cambió de precio: ahora suma <b>${ruMoney(now)}</b> (antes ${ruMoney(p.sugAt)}).<button type="button" class="link ru-upd" data-id="${p.id}">Actualizar precio</button></div>`:"";})()}''')
rep('''return`<span class="pform"><span class="pfh"><b>${ruFN[w]}</b><span class="price"><span class="pl">${ruMoney(r.pp)} <small>por persona</small></span><span class="pl"><small>${ruMoney(r.tot)} en total</small></span>${v?`<span class="pl"><small class="pmv">± ${v}%</small></span>`:""}</span></span><small class="inc">${esc(d)}</small></span>`;}''',
    '''return`<span class="pform"><span class="pfh"><b>${ruFN[w]}</b><span class="price"><span class="pl">${ruMoney(r.pp)} <small>por persona</small></span><span class="pl"><small>${ruMoney(r.tot)} en total</small></span>${v?`<span class="pl"><small class="pmv">± ${v}%</small></span>`:""}</span></span>${ruUl(ruFormItems(p,w,true),"pul")}</span>`;}''')
rep('<small class="inc">Incluye: ${esc(P.items.map(ref=>ruItemName(ref,P)).join(" + "))}</small>', '<small class="inc">Incluye:</small>${ruUl(P.items.map(ref=>ruItemName(ref,P)),"pul")}')
rep('<small class="ru-fd">${esc(k.items.map(ref=>ruItemName(ref,k)).join(" + "))}</small>', '${ruUl(k.items.map(ref=>ruItemName(ref,k)))}')

# ---------- paquetes: aviso de cambio de precio, bloqueo animado, pop-up ----------
rep(''' root.querySelectorAll(".ru-kc").forEach(c=>{''', ''' root.querySelectorAll(".ru-upd").forEach(b=>b.onclick=()=>{const p=K.find(x=>x.id===b.dataset.id);if(!p)return;const now=ruSug(p),t=p.tar.full;if(+t.p&&p.sugAt)t.p=String(Math.round(+t.p*now/p.sugAt));p.sugAt=now;ruDrawLists();changed();ruToast(`💲 «${p.name}» ahora cuesta ${money(t.p)} ${t.u.toLowerCase()}`);});
 const ps=$("ruPkSec");if(ps)ps.onclick=e=>{if(!ps.classList.contains("locked"))return;e.preventDefault();ruLockPop(ps);};
 ruDrawPlanners();
 root.querySelectorAll(".ru-kc").forEach(c=>{''')
rep('$("ruMk").onclick=()=>ruStartPick([]);', '$("ruMk").onclick=e=>{e.stopPropagation();ruPkgGate();};const iv=$("ruInv");if(iv)iv.onclick=()=>ruInviteForm();')
# el venue entra al combinador solo si ya está configurado
rep('function ruVenueItem(){const v=S.venue;if(!S.types||!S.types.venue||!v)return null;', 'function ruVenueItem(){const v=S.venue;if(!S.types||!S.types.venue||!v||!filled(v.name)||!(+v.seated>0))return null;')
# planners como piezas de paquete
rep('const ruById=id=>{id=String(id||"").split("|")[0];return id==="venue"?ruVenueItem():(S.rprods||[]).find(x=>x.id===id);};',
    'const ruById=id=>{id=String(id||"").split("|")[0];return id==="venue"?ruVenueItem():id.startsWith("pl:")?ruPlanners().find(x=>x.id===id):(S.rprods||[]).find(x=>x.id===id);};')
rep('const L=p.items.map(ruById).filter(x=>x&&x.kind!=="venue").map(ruZones);', 'const L=p.items.map(ruById).filter(x=>x&&x.kind!=="venue"&&x.kind!=="planner").map(ruZones);')
rep('.dims[0]).filter(c=>c!=="Venue"))]:[p.dims[0]];', '.dims[0]).filter(c=>c!=="Venue"&&c!=="Event planner"))]:[p.dims[0]];')
rep(' if(x.kind==="venue")return ruVenueTot(pax);', ' if(x.kind==="venue")return ruVenueTot(pax);\n if(x.kind==="planner")return ruPlanTot(x.fees,pax,P.items.filter(r=>!String(r).startsWith("pl:")).reduce((a,r)=>a+ruItemTot(r,P),0));')
rep('return(x.kind==="venue"?"🏡 ":"")+', 'return(x.kind==="venue"?"🏡 ":x.kind==="planner"?"🧭 ":"")+')
rep('const ruRefs=()=>[...(S.rprods||[]).flatMap(p=>p.kind==="staff"?[p.id]:p.tw.map(w=>p.id+"|"+w)),...(ruVenueItem()?["venue"]:[])];',
    'const ruRefs=()=>[...(S.rprods||[]).flatMap(p=>p.kind==="staff"?[p.id]:p.tw.map(w=>p.id+"|"+w)),...(ruVenueItem()?["venue"]:[]),...ruPlanners().map(x=>x.id)];')
# paquetes del ejemplo: uno con «antes» distinto para mostrar el aviso
rep('Object.assign(P,ruBlankMore());P.tar.full.p="720";', 'Object.assign(P,ruBlankMore());P.tar.full.p="720";P._demoOld=true;')
rep(''' (S.rpkgs||[]).forEach(k=>{k.items=k.items.filter(r=>ruRefW(r)!=="labor");k.tw=["full"];});''',
    ''' (S.rpkgs||[]).forEach(k=>{k.items=k.items.filter(r=>ruRefW(r)!=="labor");k.tw=["full"];if(k.sugAt===undefined){k.sugAt=Math.round(ruSug(k)*(k._demoOld?0.94:1));delete k._demoOld;}});
 if(!S.invites)S.invites=[];if(!S.askNo)S.askNo={};''')

s += r'''
/* ===== v27 · paquetes bloqueados: animación y burbuja ===== */
function ruLockPop(sec){document.querySelectorAll(".ru-lockb").forEach(x=>x.remove());sec.classList.remove("ru-shake");void sec.offsetWidth;sec.classList.add("ru-shake");
 const b=document.createElement("div");b.className="ru-lockb";b.setAttribute("role","status");b.innerHTML=`<img src="img/c_07.webp" alt=""><span>Primero define tus productos para poder armar tus paquetes 🙌</span>`;sec.appendChild(b);setTimeout(()=>b.classList.add("out"),2300);setTimeout(()=>b.remove(),2700);}
/* ===== v27 · event planners: tú o personas invitadas que aceptan ===== */
const plFeeOk=f=>filled(f.amount)&&f.unit!=="otro";
function ruPlanners(){const out=[];const P=S.planner;if(S.types&&S.types.planner&&P&&filled(P.person)&&(P.fees||[]).some(plFeeOk))out.push({id:"pl:yo",kind:"planner",name:"Coordinación · "+P.person,who:P.person,me:true,fees:P.fees.filter(plFeeOk),dims:["Event planner","","",""],crew:[],dishes:[],ins:[],tw:["planner"],pax:"",cov:{same:true}});
 (S.invites||[]).filter(i=>i.status==="aceptada"&&(i.fees||[]).some(plFeeOk)).forEach(i=>out.push({id:"pl:"+i.id,kind:"planner",name:"Coordinación · "+i.name,who:i.name,fees:i.fees.filter(plFeeOk),dims:["Event planner","","",""],crew:[],dishes:[],ins:[],tw:["planner"],pax:"",cov:{same:true}}));return out;}
/* lo que cobra el planner: fijo, por hora, por invitado o % del total (con mínimo); el anfitrión ve la opción más conveniente */
function ruPlanTot(fees,pax,base){let best=null;(fees||[]).forEach(f=>{const a=+f.amount||0;let t=f.unit==="evento"?a:f.unit==="hora"?a*5:f.unit==="invitado"?a*(+pax||0):f.unit==="porcentaje"?Math.max(a/100*(+base||0),+f.min||0):a;if(t>0&&(best===null||t<best))best=t;});return Math.round(best||0);}
const plFeesText=fees=>(fees||[]).filter(plFeeOk).map(f=>f.unit==="porcentaje"?`${f.amount}% del total${+f.min>0?` (mínimo ${money(f.min)})`:""}`:`${money(f.amount)} ${({evento:"por evento",hora:"por hora",invitado:"por invitado"})[f.unit]||""}`).join(" o ");
function ruDrawPlanners(){const box=$("ruPl");if(!box)return;const P=S.planner,own=S.types&&S.types.planner&&P,L=[];
 if(own)L.push(`<article class="ru-pc ru-plc" data-pl="pl:yo"><span class="ru-plb">🧭 Tú</span><h4>${esc(P.person||"Tu perfil de planner")}</h4>${(P.fees||[]).some(plFeeOk)?`<span class="ru-pr">${esc(plFeesText(P.fees))}</span>`:`<span class="ru-pr hint">Falta tu tarifa en «Mi perfil de planner»</span>`}${RU_PICK&&ruPlanners().some(x=>x.id==="pl:yo")?ruPickB("pl:yo",P.person):`<span class="ru-tools"><button type="button" class="ru-pled" aria-label="Editar tu perfil de planner">✏️</button></span>`}</article>`);
 (S.invites||[]).forEach(i=>{const ok=i.status==="aceptada",ref="pl:"+i.id;L.push(`<article class="ru-pc ru-plc${ok?"":" pend"}${RU_PICK&&RU_PICKED.includes(ref)?" sel":""}" data-inv="${i.id}"><span class="ru-plb ${ok?"ok":"wait"}">${ok?"✅ Aceptó":"⏳ Invitación pendiente"}</span><h4>${esc(i.name)}</h4>${ok?`<span class="ru-pr">${esc(plFeesText(i.fees))}</span>`:`<span class="ru-meta">${esc([i.wa?waShow(i.waCC,i.wa):"",i.email].filter(Boolean).join(" · "))}</span><span class="ru-meta">No se publica nada hasta que acepte.</span><span class="row ru-plact"><button type="button" class="link ru-sim">👀 Simular que aceptó</button><button type="button" class="link ru-resend">Reenviar</button></span>`}
  ${RU_PICK&&ok?ruPickB(ref,i.name):`<span class="ru-tools"><button type="button" class="ru-inx" aria-label="Quitar a ${esc(i.name)}">✕</button></span>`}</article>`);});
 box.innerHTML=L.join("")||`<p class="ru-empty">¿Trabajas con un event planner? Invítalo: cuando acepte, lo sumas a tus paquetes.</p>`;
 box.querySelectorAll(".ru-pick").forEach(b=>b.onclick=()=>{const r=b.dataset.ref;RU_PICKED=RU_PICKED.includes(r)?RU_PICKED.filter(x=>x!==r):[...RU_PICKED,r];ruDrawLists();});
 const pe=box.querySelector(".ru-pled");if(pe)pe.onclick=()=>ruGoStep("planner");
 box.querySelectorAll("[data-inv]").forEach(c=>{const i=S.invites.find(x=>x.id===c.dataset.inv);const q=s=>c.querySelector(s);
  if(q(".ru-sim"))q(".ru-sim").onclick=()=>ruInviteeView(i);if(q(".ru-resend"))q(".ru-resend").onclick=()=>ruInviteForm(i);
  if(q(".ru-inx"))q(".ru-inx").onclick=()=>{const ix=S.invites.indexOf(i);S.invites.splice(ix,1);ruDrawLists();changed();ruToast(`Quitaste a «${i.name}»: borramos sus datos`,()=>{S.invites.splice(ix,0,i);ruDrawLists();changed();});};});}
function ruGoStep(id){const ix=stepList().findIndex(s=>s.id===id);if(ix<0)return;step=ix;render();scrollTo({top:0,behavior:"instant"});}
const ruInvMsg=i=>`¡Hola, ${i.name.split(" ")[0]}! ${S.biz.owner||"Un proveedor"} te invita a sumarte a la red de proveedores de ¡Hay que vernos! como event planner de su negocio «${S.biz.name||"su negocio"}». Crea tu cuenta aquí: https://hayquevernos.com/invita/${i.id}`;
function ruModal(html,cls){const md=document.createElement("div");md.className="rmodal";md.innerHTML=`<div class="rsheet ${cls||""}">${html}</div>`;document.body.appendChild(md);md.onclick=e=>{if(e.target===md)md.remove();};return md;}
/* invitar: solo nombre y forma de contacto; nada se publica hasta que la persona acepte */
function ruInviteForm(old){const i=old||{id:"inv"+Date.now().toString(36),name:"",wa:"",waCC:"MX",email:"",status:"pendiente",fees:[]};
 const md=ruModal(`<span class="ru-embk">🧭 INVITA A TU EVENT PLANNER</span><h2>${old?"Reenviar invitación":"¿Quién coordina tus eventos?"}</h2><span>Solo necesitamos su nombre y cómo contactarle. No publicamos nada de esta persona hasta que acepte y cree su cuenta.</span>
  <div class="ru-invf"><input type="text" id="ivN" value="${esc(i.name)}" placeholder="Nombre completo" aria-label="Nombre">${telHtml("ivW",i.waCC,i.wa,"","WhatsApp")}<input type="email" id="ivE" value="${esc(i.email)}" placeholder="Correo (opcional si pones WhatsApp)" aria-label="Correo">
  <div class="ru-invm" id="ivM"></div><span class="err" id="ivErr" hidden></span>
  <div class="row"><a class="btn cta" id="ivWa" target="_blank" rel="noopener">💬 Enviar por WhatsApp</a><a class="btn ghost" id="ivMail">✉️ Enviar por correo</a></div><button type="button" class="link" id="ivX" style="color:#fff">Cancelar</button></div>`,"ru-inv");
 const upd=()=>{i.name=$("ivN").value.trim();i.wa=$("ivW").value;i.waCC=$("ivW-cc").value;i.email=$("ivE").value.trim();$("ivM").textContent=i.name?ruInvMsg(i):"Escribe su nombre para ver el mensaje.";
  $("ivWa").href=waOk(i.waCC,i.wa)?`https://wa.me/${waIntl(i.waCC,i.wa)}?text=${encodeURIComponent(ruInvMsg(i))}`:"#";$("ivMail").href=EMAIL_OK(i.email)?`mailto:${i.email}?subject=${encodeURIComponent("Te invitan a ¡Hay que vernos!")}&body=${encodeURIComponent(ruInvMsg(i))}`:"#";};
 ["ivN","ivW","ivE"].forEach(x=>$(x).oninput=upd);$("ivW-cc").onchange=upd;upd();
 const send=(ok,e)=>{const er=$("ivErr");if(!filled(i.name)||!ok){e.preventDefault();er.hidden=false;er.textContent=!filled(i.name)?"Falta su nombre.":"Falta un WhatsApp o correo válido.";($(!filled(i.name)?"ivN":"ivW")).focus();return;}
  i.status="pendiente";if(!S.invites.includes(i))S.invites.push(i);md.remove();ruDrawLists();changed();ruToast(`📨 Invitación enviada a ${i.name}. Te avisamos cuando acepte.`);hqvTrack("planner_invitado",{});};
 $("ivWa").onclick=e=>send(waOk(i.waCC,i.wa),e);$("ivMail").onclick=e=>send(EMAIL_OK(i.email),e);$("ivX").onclick=()=>md.remove();setTimeout(()=>$("ivN").focus(),50);}
/* lo que ve la persona invitada (simulación para el prototipo) */
function ruInviteeView(i){const md=ruModal(`<span class="ru-embk">LO QUE RECIBE ${esc(i.name.split(" ")[0].toUpperCase())}</span><img src="img/logo.webp" alt="¡Hay que vernos!" class="ru-invlogo"><h2>${esc(S.biz.owner||"Un proveedor")} te invita</h2><span>a la red de proveedores de ¡Hay que vernos! como <b>event planner</b> de «${esc(S.biz.name||"su negocio")}».</span>
  <div class="ru-invf"><b>Crea tu cuenta</b><input type="text" id="iaN" value="${esc(i.name)}" aria-label="Tu nombre"><input type="text" value="${esc(i.wa?waShow(i.waCC,i.wa):"")}" aria-label="Tu WhatsApp" placeholder="Tu WhatsApp"><input type="email" value="${esc(i.email)}" aria-label="Tu correo" placeholder="Tu correo">
   <label class="ru-invck"><input type="checkbox" id="iaOk"> Acepto ser event planner de «${esc(S.biz.name||"su negocio")}» y que muestre mi coordinación en sus paquetes.</label><span class="err" id="iaErr" hidden></span>
   <button type="button" class="btn cta" id="iaGo">Crear cuenta y aceptar</button><button type="button" class="link" id="iaNo" style="color:#fff">No, gracias</button></div>`,"ru-inv");
 $("iaNo").onclick=()=>{const ix=S.invites.indexOf(i);S.invites.splice(ix,1);md.remove();ruDrawLists();changed();ruToast(`${i.name} no aceptó: borramos sus datos.`);};
 $("iaGo").onclick=()=>{if(!$("iaOk").checked){const e=$("iaErr");e.hidden=false;e.textContent="Marca la casilla para aceptar el rol.";$("iaOk").focus();return;}i.name=$("iaN").value.trim()||i.name;md.remove();ruInviteeFees(i);};}
function ruInviteeFees(i){const F=i.fees.length?i.fees:[{amount:"",unit:"evento",min:""},{amount:"",unit:"porcentaje",min:""}];
 const md=ruModal(`<span class="ru-embk">PERFIL DE EVENT PLANNER · ${esc(i.name.toUpperCase())}</span><h2>¿Cómo cobras por coordinar?</h2><span>Llena una o las dos. El anfitrión ve la que más le conviene.</span>
  <div class="ru-invf"><label class="ru-invr"><span>Precio fijo por evento</span><span class="ru-fi"><i>$</i><input type="number" min="0" id="ifA" value="${esc(F[0].amount)}" placeholder="0"></span></label>
  <label class="ru-invr"><span>Porcentaje del total del evento</span><span class="ru-fi"><input type="number" min="0" max="100" id="ifP" value="${esc((F[1]||{}).amount||"")}" placeholder="10"><i>%</i></span></label>
  <label class="ru-invr"><span>Mínimo si cobras por porcentaje <small>(opcional)</small></span><span class="ru-fi"><i>$</i><input type="number" min="0" id="ifM" value="${esc((F[1]||{}).min||"")}" placeholder="0"></span></label>
  <span class="err" id="ifErr" hidden></span><button type="button" class="btn cta" id="ifGo">Listo</button><span class="hint" style="color:rgba(255,255,255,.8)!important">En la plataforma real, aquí sigue su perfil completo de event planner: foto, bio y especialidades.</span></div>`,"ru-inv");
 $("ifGo").onclick=()=>{const a=$("ifA").value,p=$("ifP").value,m=$("ifM").value;if(!(+a>0)&&!(+p>0)){const e=$("ifErr");e.hidden=false;e.textContent="Pon al menos una forma de cobrar.";$("ifA").focus();return;}
  i.fees=[+a>0?{amount:a,unit:"evento",min:""}:null,+p>0?{amount:p,unit:"porcentaje",min:m}:null].filter(Boolean);i.status="aceptada";md.remove();ruDrawLists();changed();ruConfetti(90);ruToast(`🧭 ${i.name} aceptó: ya puedes sumarle a tus paquetes.`);};}
/* ===== v27 · pop-up «Arma paquetes con todo tu negocio» ===== */
function ruPkgGate(){const nP=(S.rprods||[]).filter(x=>x.kind==="prod").length,nS=(S.rprods||[]).filter(x=>x.kind==="staff").length,v=ruVenueItem(),pls=ruPlanners(),pend=(S.invites||[]).filter(i=>i.status==="pendiente");
 const askV=!v&&!S.askNo.venue,askP=!pls.length&&!pend.length&&!S.askNo.planner;
 if(!askV&&!askP){ruStartPick([]);return;}
 const tot=4,done=(nP?1:0)+(nS?1:0)+(v?1:0)+(pls.length?1:0),ch={v:null,p:null};
 const row=(ok,t,extra)=>`<div class="ru-gr${ok?" ok":""}"><span class="ru-gi">${ok===true?"✅":ok==="wait"?"⏳":"⬜"}</span><span class="ru-gt">${t}</span>${extra||""}</div>`;
 const md=ruModal(`<span class="ru-embk">🎁 ARMA PAQUETES CON TODO TU NEGOCIO</span><h2>Tienes ${done} de ${tot}</h2><span>Un paquete puede juntar todo lo que ofreces. ¿Te falta algo?</span>
  <div class="ru-gate">${row(nP>0,`Servicios y productos <b>(${nP})</b>`)}${row(nS>0,nS?`Staff <b>(${nS})</b>`:"Staff: aún no defines ninguno")}
  ${v?row(true,`Venue: <b>${esc(v.name)}</b>`):S.askNo.venue?"":row(false,"🏡 ¿Tienes un lugar para fiestas?",`<span class="ru-gb" data-k="v"><button type="button" class="chip" data-v="si">Sí, configurarlo</button><button type="button" class="chip" data-v="no">No tengo</button></span>`)}
  ${pls.length?row(true,`Event planner: <b>${esc(pls.map(x=>x.who).join(", "))}</b>`):pend.length?row("wait",`Event planner: <b>${esc(pend[0].name)}</b> (invitación pendiente)`):S.askNo.planner?"":row(false,"🧭 ¿Hay un event planner en tu negocio?",`<span class="ru-gb" data-k="p"><button type="button" class="chip" data-v="yo">Soy yo</button><button type="button" class="chip" data-v="otro">Es otra persona</button><button type="button" class="chip" data-v="no">No</button></span>`)}</div>
  <button type="button" class="btn cta" id="gtGo">Armar paquete con lo que tengo</button><button type="button" class="link" id="gtX" style="color:#fff">Cerrar</button>`,"ru-gates");
 const go=$("gtGo"),lbl=()=>{go.textContent=ch.v==="si"||ch.p==="yo"||ch.p==="otro"?"Continuar →":"Armar paquete con lo que tengo";};
 md.querySelectorAll(".ru-gb").forEach(g=>g.querySelectorAll("button").forEach(b=>b.onclick=()=>{ch[g.dataset.k]=b.dataset.v;g.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",x===b));lbl();}));
 $("gtX").onclick=()=>md.remove();
 go.onclick=()=>{if(ch.v==="no")S.askNo.venue=true;if(ch.p==="no")S.askNo.planner=true;md.remove();changed();const Q=[];
  if(ch.v==="si"){S.types.venue=true;Q.push("venue");}
  if(ch.p==="yo"){S.types.planner=true;ruPrefillPlanner();Q.push("planner");}
  if(ch.p==="otro"){ruInviteForm();}
  if(Q.length){S._pkgQueue=Q;ensureState();ruGoStep(Q[0]);}else if(ch.p!=="otro")ruStartPick([]);};}
/* tu perfil de planner arrastra los datos de tu perfil personal */
function ruPrefillPlanner(){const p=S.planner,b=S.biz,me=S.me||{};if(!filled(p.person))p.person=b.owner||"";if(!p.photo&&me.photo)p.photo=me.photo;
 ["instagram","tiktok","facebook"].forEach(k=>{if(!filled(p[k]||"")&&filled(me[k]||""))p[k]=me[k];});if(!(p.links||[]).length&&(me.links||[]).length)p.links=JSON.parse(JSON.stringify(me.links));p.socialFromBiz=false;
 if(!p.since&&b.founded)p.since=b.founded.slice(0,4);if(!(p.zones||[]).some(z=>z.state)&&(S.svcZones||[]).some(z=>z.state))p.zones=JSON.parse(JSON.stringify(S.svcZones));}
/* aviso arriba de «Mi venue» y «Mi perfil de planner» mientras se preparan los paquetes */
function ruQueueBannerHtml(id){const Q=S._pkgQueue;if(!Q||!Q.includes(id))return"";const nx=Q[Q.indexOf(id)+1];
 return`<div class="alert info ru-qb">🎁 <span>Estás preparando tus paquetes.${id==="planner"?" Pusimos los datos de tu perfil personal; revisa y agrega tu tarifa.":""} Cuando termines:</span><button type="button" class="btn sm" onclick="ruQueueNext('${id}')">${nx==="planner"?"Seguir a mi perfil de planner →":"Volver a armar paquetes →"}</button></div>`;}
function ruQueueNext(id){const Q=S._pkgQueue||[],nx=Q[Q.indexOf(id)+1];if(nx){ruGoStep(nx);return;}S._pkgQueue=null;S._pickStart=true;ruGoStep("svc");}
'''
# en «Mis servicios», al volver de venue/planner se abre el combinador
rep('ruBindBuilder();if(S._pickVenue){S._pickVenue=false;setTimeout(()=>ruStartPick(["venue"]),60);}',
    'ruBindBuilder();if(S._pickStart){S._pickStart=false;setTimeout(()=>ruStartPick(ruVenueItem()?["venue"]:[]),60);}if(S._pickVenue){S._pickVenue=false;setTimeout(()=>ruStartPick(["venue"]),60);}')
(V / 'svc7.js').write_text(s)
print('ok v27 svc')
