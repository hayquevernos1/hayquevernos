"""v7 · Bloque 1 (cotizador): comentarios de Diego en Miro (8 oct 2026). Lee cot6.html → escribe cot7.html.
- Universo anfitrión en azul. Entrada directa (sin pantalla de bienvenida): Vernie pregunta el nombre.
- ¿Quieres un event planner? (fichas tipo Tinder) y textos adaptados.
- Botones compactos, «Otro» con campo (repetible donde aplica), requisitos del venue obligatorios u opcionales.
- Resultado: encabezado fijo con nombre de la fiesta + «Guardar y enviar», proveedores disponibles y «Contactar» por servicio."""
from pathlib import Path
D = Path('/home/claude/hqv/v5')
c = (D / 'cot6.html').read_text()


def rep(a, b, count=1):
    global c
    assert a in c, 'NO ENCONTRADO: ' + a[:110]
    c = c.replace(a, b, count)


# ---------- tema azul (después de marca.css) + estilos nuevos
CSS = '''<style>
:root{--grape:#1E69FF;--grape-soft:#E3ECFF}
@media (prefers-color-scheme:dark){:root{--grape:#6E9BFF;--grape-soft:#1A2A52}}
.tiles{grid-template-columns:repeat(auto-fill,minmax(min(100%,150px),1fr));gap:6px}
.tile{display:flex;align-items:center;gap:8px;justify-items:start;text-align:left;padding:8px 10px;font-size:13px;border-radius:14px;line-height:1.15}
.tile .emo{font-size:19px;flex:none}
.tile.more{display:none}.tiles.all .tile.more{display:flex}
.tile.hide{display:none!important}
.tip,.tip.good,.tip.warn,.tip.orange,.tip.bad,.tip.info{background:var(--grape-soft);color:var(--ink)}
.urg,.urg.u0,.urg.u1,.urg.u2,.urg.u3{background:var(--grape-soft)!important;color:var(--ink)!important}
.stages{grid-template-columns:repeat(5,1fr)}
.stages span{position:relative;margin-bottom:14px}
.stages span i{position:absolute;top:9px;left:0;right:0;font-style:normal;font-size:10.5px;font-weight:700;color:var(--muted);text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.stages span.on i{color:var(--grape)}
.othl{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.othr{display:flex;gap:4px;align-items:center}
.othr input,.oth1{max-width:240px;padding:7px 10px!important}
.reqs{display:grid;gap:6px}
.req{display:flex;justify-content:space-between;align-items:center;gap:8px;background:var(--paper);border-radius:12px;padding:6px 10px;font-size:13.5px}
.req .seg button{padding:5px 10px;font-size:12.5px}
.pdg{display:inline-flex;gap:4px;align-items:center;background:var(--hqv-vainilla,#FEEE85);color:#3A2E00;border-radius:99px;padding:2px 10px;font-size:12px;font-weight:800}
.namebox{display:grid;gap:12px;justify-items:center;text-align:center;padding:28px 18px}
.namebox input{max-width:320px;text-align:center;font-size:18px}
.plc{position:relative;border-radius:22px;background:var(--card);box-shadow:var(--hqv-clay-sm,0 6px 16px rgba(0,0,0,.08));padding:16px;display:grid;gap:8px;touch-action:pan-y;user-select:none;transition:transform .25s}
.plc .ph{font-size:46px;line-height:1}
.plc .tags{display:flex;flex-wrap:wrap;gap:6px}
.plc .tags span{background:var(--grape-soft);border-radius:99px;padding:3px 10px;font-size:12px;font-weight:700}
.plc-nav{display:flex;justify-content:space-between;gap:8px;align-items:center}
.plc-nav .btn{flex:1}
.plpick{display:flex;gap:10px;align-items:center;background:var(--grape-soft);border-radius:16px;padding:10px 12px}
.plpick .ph{font-size:30px}
.rbar{position:sticky;top:0;z-index:20;background:var(--grape);color:#fff;border-radius:22px;padding:14px 16px;display:grid;gap:10px;overflow:hidden;box-shadow:0 10px 24px rgba(20,40,120,.25)}
.rbar .meta{font-size:12px;opacity:.9}
.rbar .nums{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.rbar .pp{font-family:var(--f-display);font-size:clamp(30px,7vw,40px);font-weight:900;line-height:1}
.rbar .tt{font-size:13.5px}
.rbar .save{display:grid;grid-template-columns:1fr auto;gap:8px;align-items:end}
.rbar .save label{display:grid;gap:4px;font-size:12.5px;font-weight:800}
.rbar .save input{border:0;border-radius:14px;padding:11px 12px;font-size:15px}
.rbar .save .btn{background:#fff;color:var(--grape);white-space:nowrap}
.rbar .conf{position:absolute;inset:0;pointer-events:none;opacity:.9}
.rbar>*:not(.conf){position:relative}
@media(max-width:560px){.rbar .save{grid-template-columns:1fr}}
.break.scroll{max-height:440px;overflow-y:auto;padding-right:4px}
.avail{display:flex;gap:6px;align-items:center;justify-content:space-between;flex-wrap:wrap;width:100%;margin-top:6px;font-size:12.5px;color:var(--ink)}
.avail span{background:var(--grape-soft);border-radius:99px;padding:3px 10px}
.avail .btn{padding:6px 14px;font-size:12.5px}
.break>div{flex-wrap:wrap}
</style>'''
i = c.index('<link rel="stylesheet" href="marca.css">') + len('<link rel="stylesheet" href="marca.css">')
c = c[:i] + '\n' + CSS + c[i:]

# ---------- estado
rep('''hasPlace:null,place:{type:"",addr:blankAddr(),floor:"",up:"",cover:"",parking:"",feats:[],baths:{m:"",w:"",g:""},photos:[]},
 need:{state:"Ciudad de México",all:false,munis:[],types:[],feats:[],format:""},''',
    '''hasPlace:null,place:{type:"",owner:"",addr:blankAddr(),floor:"",floorOther:"",up:"",upOther:"",cover:"",coverOther:"",parking:"",parkingOther:"",feats:[],featsOther:[],baths:{m:"",w:"",g:""},photos:[]},
 need:{state:"Ciudad de México",all:false,munis:[],types:[],feats:[],featsOther:[],req:{},format:""},nameOk:false,plannerPick:null,plIdx:0,partyName:"",''')
rep('''fact:{docs:[],days:"",terms:"",method:[],biz:""}''', '''fact:{docs:[],docsOther:[],days:"",reqDate:"",terms:"",method:[],methodOther:[],biz:""}''')
rep('''let screen="intro",''', '''let screen="fiesta",''')

# ---------- helpers: «Otro» y planner
rep('''const say=m=>''', '''const PLN=()=>S.wantPlanner&&S.plannerPick!=null?PLANNERS[S.plannerPick]:null;
const OTH={pf:()=>S.place.featsOther,nf:()=>S.need.featsOther,fd:()=>S.fact.docsOther,fm:()=>S.fact.methodOther};
const othList=(k,ph)=>{const a=OTH[k]();return`<div class="othl">${a.map((v,i)=>`<span class="othr"><input type="text" class="othi" data-k="${k}" data-i="${i}" value="${esc(v)}" placeholder="${esc(ph)}" aria-label="${esc(ph)}"><button type="button" class="link-btn othx" data-k="${k}" data-i="${i}" aria-label="Quitar">✕</button></span>`).join("")}<button type="button" class="chip othadd" data-k="${k}">✏️ ${a.length?"Agregar otro":"Otro"}</button></div>`;};
const oth1=(o,k,ph)=>`<input type="text" class="oth1" data-o="${o}" data-k="${k}" value="${esc((o==="p"?S.place:S.need)[k]||"")}" placeholder="${esc(ph)}" aria-label="${esc(ph)}">`;
function bindOth(el,st){el.querySelectorAll(".othadd").forEach(b=>b.onclick=()=>{OTH[b.dataset.k]().push("");const y=scrollY;render();scrollTo({top:y});const ins=el.querySelectorAll(`.othi[data-k="${b.dataset.k}"]`);const last=document.querySelectorAll(`.othi[data-k="${b.dataset.k}"]`);last.length&&last[last.length-1].focus();});
 el.querySelectorAll(".othx").forEach(b=>b.onclick=()=>{OTH[b.dataset.k]().splice(+b.dataset.i,1);const y=scrollY;render();scrollTo({top:y});});
 el.querySelectorAll(".othi").forEach(i=>i.oninput=()=>{OTH[i.dataset.k]()[+i.dataset.i]=i.value;});
 el.querySelectorAll(".oth1").forEach(i=>i.oninput=()=>{(i.dataset.o==="p"?S.place:S.need)[i.dataset.k]=i.value;refresh(st);});}
const say=m=>''')

# ---------- validación
rep('''if(st==="fiesta"){if(!S.kind)''', '''if(st==="fiesta"){if(!S.nameOk)m.push("Tu nombre");if(S.wantPlanner===null)m.push("¿Quieres un event planner?");if(S.wantPlanner&&S.plannerPick==null)m.push("Elige a tu event planner");if(!S.kind)''')
rep('''if(S.hasPlace===true){const p=S.place;if(!p.type)m.push("Tipo de espacio");''', '''if(S.hasPlace===true){const p=S.place;if(!p.owner)m.push("¿De quién es el lugar?");if(!p.type)m.push("Tipo de espacio");''')
rep('''if(!filled(f.days))m.push("Días para dar de alta");''', '''if(!f.reqDate)m.push("Fecha en que necesitas los requisitos");''')

# ---------- barra superior: nombre de cada etapa
rep('''$("stages").innerHTML=STAGES.map((s,j)=>`<span class="${screen==="result"||j<i?'done':j===i?'on':''}"></span>`).join("");''',
    '''$("stages").innerHTML=STAGES.map((s,j)=>`<span class="${screen==="result"||j<i?'done':j===i?'on':''}"><i>${["Tu fiesta","Lugar","Servicios","Presupuesto","Detalles"][j]}</i></span>`).join("");''')
rep('''const show=i>0||screen==="result"||(i===0&&S.occ);$("top").hidden=!show;''', '''const show=(i>0||(i===0&&S.occ))&&screen!=="result";$("top").hidden=!show;''')

# ---------- pantalla «Tu fiesta»
a = c.index(''' if(screen==="fiesta"){el.innerHTML=''')
b = c.index(''' if(screen==="lugar"){''')
FIESTA = r''' if(screen==="fiesta"){
  if(!S.nameOk){el.innerHTML=`<div class="card namebox"><img src="${BALL}" alt="" style="width:96px;animation:bob 3s ease-in-out infinite"><h2 style="font-size:24px;margin:0">¡Hola! Soy Vernie 🪩<br>¿Cómo te llamas?</h2>
   <input type="text" id="nm0" autocomplete="given-name" maxlength="40" value="${esc(S.name)}" placeholder="Tu nombre" aria-label="Tu nombre"><button class="btn big" type="button" id="nmOk">Guardar</button></div>`;
   const ok=()=>{const v=$("nm0").value.trim();if(v.length<2){$("nm0").classList.add("miss");$("nm0").focus();return;}S.name=v;S.nameOk=true;hqvTrack("cotizador_inicio",{con_nombre:true});try{if(parent!==window)parent.postMessage({hqv:"invitado",nombre:S.name},"*");}catch(_){}render();};
   $("nmOk").onclick=ok;$("nm0").onkeydown=e=>{if(e.key==="Enter")ok();};setTimeout(()=>$("nm0").focus(),50);return;}
  const pl=PLN(),first=esc(S.name.split(" ")[0]);
  const card=i=>{const p=PLANNERS[i];return`<div class="plc" id="plc"><div style="display:flex;gap:12px;align-items:center"><span class="ph">${p.e}</span><div><b style="font-size:18px">${esc(p.n)}</b><br><small>⭐ ${p.r} · ${p.y} años de experiencia · ${esc(p.z)}</small></div></div>
   <span>${esc(p.b)}</span><div class="tags">${p.sp.map(x=>`<span>${esc(x)}</span>`).join("")}</div><b>Desde ${money(p.f)}</b><small class="hint">${i+1} de ${PLANNERS.length} · desliza o usa los botones</small></div>`;};
  el.innerHTML=`<div class="card">${say(`¡Mucho gusto, <b>${first}</b>! Cuéntame de tu fiesta.`)}
  <div class="field"><span class="lbl">📋 ¿Quieres la ayuda de un event planner?</span><div class="seg${MISS(S.wantPlanner!==null)}" id="wpl"><button type="button" data-v="0" aria-pressed="${S.wantPlanner===false}">No. Yo organizo</button><button type="button" data-v="1" aria-pressed="${S.wantPlanner===true}">Sí, que me ayude</button></div>
   ${S.wantPlanner===true&&S.plannerPick==null?`${card(S.plIdx)}<div class="plc-nav"><button class="btn ghost" type="button" id="plNo">✕ Siguiente</button><button class="btn" type="button" id="plYes">💙 Lo quiero</button></div>`:''}
   ${pl?`<div class="plpick"><span class="ph">${pl.e}</span><span style="flex:1"><b>Tu event planner: ${esc(pl.n)}</b><br><small>⭐ ${pl.r} · desde ${money(pl.f)}</small></span><button class="link-btn" type="button" id="plCh">Cambiar</button></div>`:''}</div>
  ${S.wantPlanner===false?`<div class="note">✅ <span><b>De acuerdo. Eres tu propio event planner.</b> Ahora comienza a configurar tu fiesta para conseguir tu pre-cotización. (Si aún no tienes decisiones definitivas, no te preocupes. Puedes editar todo lo que necesites en el momento que quieras).</span></div>`:''}
  ${pl?`<div class="note">💙 <span><b>¡Perfecto! Te apoyarás en un event planner.</b> Ahora comienza a configurar tu fiesta para conseguir tu pre-cotización y explicarle a tu eventual planner lo que quieres. (Si aún no tienes decisiones definitivas, no te preocupes. Tu event planner te ayudará a editar todo lo necesario hasta conseguir tu fiesta ideal).</span></div>`:''}
  ${S.wantPlanner===false||pl?`
  <div class="field"><span class="lbl">Tu evento es…</span><div class="seg${MISS(!!S.kind)}" id="kind"><button type="button" data-v="social" aria-pressed="${S.kind==="social"}">🎉 Social</button><button type="button" data-v="empresa" aria-pressed="${S.kind==="empresa"}">🏢 De empresa</button></div></div>
  ${S.kind?`<div class="field"><span class="lbl">${S.kind==="empresa"?"¿Qué tipo de evento es?":"¿Qué celebras?"}</span><input type="search" class="evq" id="evq" placeholder="🔎 Busca: boda, congreso, posada…" aria-label="Buscar tipo de evento"><div class="tiles${MISS(!!S.occ)}" id="evTiles">${OCC[S.kind].map(([o,e],i)=>`<button type="button" class="tile occ${i>=11&&S.occ!==o&&o!=="Otro"?" more":""}" data-o="${esc(o)}" aria-pressed="${S.occ===o}"><span class="emo">${e}</span>${esc(o)}</button>`).join("")}</div><button type="button" class="link-btn" id="evAll" style="justify-self:start">Ver los ${OCC[S.kind].length} tipos de evento</button></div>`:''}
  <div class="field"><span class="lbl">👥 ¿Cuántos invitados?</span><div class="counter"><button type="button" class="pm" id="gm" aria-label="Menos">−</button><input type="number" id="g" min="2" value="${S.guests}" aria-label="Invitados"><button type="button" class="pm" id="gp" aria-label="Más">+</button>
</div><input type="range" id="gr" min="0" max="1000" step="1" value="${g2s(S.guests)}" aria-label="Invitados"><div class="zones"><span>2</span><span>5,000+</span></div></div>
  <div class="row"><div class="field"><label class="lbl" for="d">📅 Fecha</label><input type="date" id="d" min="${addDays(0)}" value="${esc(S.date)}"></div>
   <div class="field"><label class="lbl" for="s">🕖 Empieza</label><input type="time" id="s" value="${esc(S.start)}"></div>
   <div class="field"><label class="lbl" for="e">🕚 Termina</label><input type="time" id="e" value="${esc(S.end)}"></div></div>
  <div id="tipsBox">${tipHtml(tips(""))}</div>`:''}
  ${navHtml("fiesta")}</div>`;
  el.querySelectorAll("#wpl button").forEach(b=>b.onclick=()=>{S.wantPlanner=b.dataset.v==="1";if(!S.wantPlanner)S.plannerPick=null;hqvTrack("quiere_planner",{si:S.wantPlanner});render();});
  const nextCard=()=>{S.plIdx=(S.plIdx+1)%PLANNERS.length;render();};
  const pick=()=>{S.plannerPick=S.plIdx;hqvTrack("planner_elegido",{planner:PLANNERS[S.plIdx].n});render();};
  if($("plNo")){$("plNo").onclick=nextCard;$("plYes").onclick=pick;const cd=$("plc");let x0=null;
   cd.onpointerdown=e=>{x0=e.clientX;cd.setPointerCapture(e.pointerId);};cd.onpointermove=e=>{if(x0!==null)cd.style.transform=`translateX(${e.clientX-x0}px) rotate(${(e.clientX-x0)/20}deg)`;};
   cd.onpointerup=e=>{const dx=e.clientX-(x0??e.clientX);x0=null;cd.style.transform="";if(dx>90)pick();else if(dx<-90)nextCard();};}
  if($("plCh"))$("plCh").onclick=()=>{S.plannerPick=null;render();};
  if(!(S.wantPlanner===false||pl)){bindNav("fiesta","fiesta","lugar");$("back").hidden=true;return;}
  el.querySelectorAll("#kind button").forEach(b=>b.onclick=()=>{if(S.kind!==b.dataset.v){S.kind=b.dataset.v;S.occ="";}render();});
  const evq=$("evq"),evT=$("evTiles");if(evq)evq.oninput=()=>{const v=evq.value.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"").trim();evT.classList.toggle("all",!!v);el.querySelectorAll(".occ").forEach(b=>b.classList.toggle("hide",!!v&&!b.dataset.o.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"").includes(v)&&b.dataset.o!=="Otro"));};
  if($("evAll"))$("evAll").onclick=()=>{evT.classList.add("all");$("evAll").remove();};
  el.querySelectorAll(".occ").forEach(b=>b.onclick=()=>{S.occ=b.dataset.o;el.querySelectorAll(".occ").forEach(x=>x.setAttribute("aria-pressed",x===b));applySuggestions();refresh("fiesta");});
  const setG=v=>{S.guests=Math.max(2,Math.round(+v||2));$("g").value=S.guests;$("gr").value=g2s(S.guests);syncBasics();refresh("fiesta");};
  $("gm").onclick=()=>setG(S.guests-1);$("gp").onclick=()=>setG(S.guests+1);$("g").oninput=e=>{if(+e.target.value>=2){S.guests=Math.round(+e.target.value);$("gr").value=g2s(S.guests);syncBasics();refresh("fiesta");}};$("g").onchange=e=>setG(e.target.value);
  $("gr").oninput=e=>{S.guests=s2g(+e.target.value);$("g").value=S.guests;syncBasics();refresh("fiesta");};
  const upd=()=>{syncBasics();$("tipsBox").innerHTML=tipHtml(tips(""));refresh("fiesta");};
  $("d").oninput=$("d").onchange=e=>{S.date=e.target.value;upd();};$("s").oninput=e=>{S.start=e.target.value;upd();};$("e").oninput=e=>{S.end=e.target.value;upd();};
  bindNav("fiesta","fiesta","lugar");$("back").hidden=true;return;}

'''
c = c[:a] + FIESTA + c[b:]

# ---------- «Lugar»
rep('''${say("¿Dónde será la fiesta? 📍")}''', '''${say(PLN()?`Cuéntale a <b>${esc(PLN().n)}</b> dónde será la fiesta 📍`:"¿Dónde será la fiesta? 📍")}''')
rep('''  ${S.hasPlace===true?`
   <div class="field"><span class="lbl">¿Qué tipo de espacio es?</span>''', '''  ${S.hasPlace===true?`
   <div class="field"><span class="lbl">🔑 ¿De quién es?</span><div class="seg${MISS(!!p.owner)}" id="own">${[["mio","Mío"],["rentado","Rentado"],["prestado","Prestado"]].map(([v,t])=>`<button type="button" data-v="${v}" aria-pressed="${p.owner===v}">${t}</button>`).join("")}</div>${p.owner&&p.owner!=="mio"?`<span class="hint">Útil para tus proveedores y tu planner: a veces hay que coordinarse con el dueño del lugar.</span>`:''}</div>
   <div class="field"><span class="lbl">¿Qué tipo de espacio es?</span>''')
rep('''[["pb","Planta baja"],["1","Piso 1"],["2","Piso 2"],["3","Piso 3"],["4+","Piso 4 o más"],["azotea","Azotea"]].map(([v,t])=>`<button type="button" class="chip fl" data-v="${v}" aria-pressed="${p.floor===v}">${t}</button>`).join("")}</div>''',
    '''[["pb","Planta baja"],["1","Piso 1"],["2","Piso 2"],["3","Piso 3"],["4+","Piso 4 o más"],["azotea","Azotea"],["otro","✏️ Otro"]].map(([v,t])=>`<button type="button" class="chip fl" data-v="${v}" aria-pressed="${p.floor===v}">${t}</button>`).join("")}</div>${p.floor==="otro"?oth1("p","floorOther","¿Dónde está? Ej. sótano, mezzanine…"):''}''')
rep('''[["elevador","🛗 Elevador"],["elevadorc","📦 Elevador de carga"],["escaleras","🪜 Solo escaleras"]].map(([v,t])=>`<button type="button" class="chip upb" data-v="${v}" aria-pressed="${p.up===v}">${t}</button>`).join("")}</div>''',
    '''[["elevador","🛗 Elevador"],["elevadorc","📦 Elevador de carga"],["escaleras","🪜 Solo escaleras"],["otro","✏️ Otro"]].map(([v,t])=>`<button type="button" class="chip upb" data-v="${v}" aria-pressed="${p.up===v}">${t}</button>`).join("")}</div>${p.up==="otro"?oth1("p","upOther","¿Cómo se sube?"):''}''')
rep('''[["techado","☂️ Techado"],["aire","🌤️ Al aire libre"],["mixto","⛅ Mixto"]].map(([v,t])=>`<button type="button" class="chip cv" data-v="${v}" aria-pressed="${p.cover===v}">${t}</button>`).join("")}</div>''',
    '''[["techado","☂️ Techado"],["aire","🌤️ Al aire libre"],["mixto","⛅ Mixto"],["otro","✏️ Otro"]].map(([v,t])=>`<button type="button" class="chip cv" data-v="${v}" aria-pressed="${p.cover===v}">${t}</button>`).join("")}</div>${p.cover==="otro"?oth1("p","coverOther","Cuéntanos cómo es"):''}''')
rep('''[["si","🚗 Sí, dentro"],["calle","🅿️ En la calle"],["no","🚫 No hay"]].map(([v,t])=>`<button type="button" class="chip pk" data-v="${v}" aria-pressed="${p.parking===v}">${t}</button>`).join("")}</div></div>''',
    '''[["si","🚗 Sí, dentro"],["calle","🅿️ En la calle"],["otro","✏️ Otro"]].map(([v,t])=>`<button type="button" class="chip pk" data-v="${v}" aria-pressed="${p.parking===v}">${t}</button>`).join("")}</div>${p.parking==="otro"?oth1("p","parkingOther","Ej. estacionamiento público a 1 cuadra"):''}</div>''')
rep('''${FEATURES.map(([id,e,t])=>`<button type="button" class="chip pf" data-f="${id}" aria-pressed="${p.feats.includes(id)}">${e} ${esc(t)}</button>`).join("")}</div>''',
    '''${FEATURES.map(([id,e,t])=>`<button type="button" class="chip pf" data-f="${id}" aria-pressed="${p.feats.includes(id)}">${e} ${esc(t)}</button>`).join("")}</div>${othList("pf","¿Con qué más cuenta?")}''')
rep('''<div class="field"><span class="lbl">📷 Fotos del espacio <span class="opt">(opcional)</span></span><span class="hint">Así los proveedores saben qué llevar y cómo montarlo.</span>
    ${p.photos.length?'':`<div class="tip warn"><span class="emo">📷</span><span>Las fotos son opcionales, pero sin ellas será más difícil que los proveedores coticen con precisión y acepten tu evento.</span></div>`}''',
    '''<div class="field"><span class="lbl">📷 Fotos del espacio ${p.photos.length?'':'<span class="pdg">⏳ Pendiente</span>'}</span><span class="hint">Opcional. Puedes subirlas después desde tu cuenta; con fotos los proveedores cotizan con más precisión.</span>''')
rep('''one("fl","floor",true);one("upb","up");one("cv","cover");one("pk","parking");''', '''one("fl","floor",true);one("upb","up",true);one("cv","cover",true);one("pk","parking",true);
   el.querySelectorAll("#own button").forEach(b=>b.onclick=()=>{p.owner=b.dataset.v;render();});''')
# venue: requisitos obligatorios u opcionales + «Otro»
rep('''<div class="field"><span class="lbl">✅ ¿Qué debe tener?</span><div class="chips${MISS(n.feats.length>0)}">${NEED_FEATS.map(([id,e,t])=>`<button type="button" class="chip nf" data-f="${id}" aria-pressed="${n.feats.includes(id)}">${e} ${esc(t)}</button>`).join("")}</div></div>
   <div id="vlive"></div>
   <div class="tip info"><span class="emo">💡</span><span>En el siguiente paso eliges qué servicios quieres que ponga el venue y cuáles llevas tú.</span></div>`:''}''',
    '''<div class="field"><span class="lbl">✅ ¿Qué debe tener?</span><div class="chips${MISS(n.feats.length>0)}">${NEED_FEATS.map(([id,e,t])=>`<button type="button" class="chip nf" data-f="${id}" aria-pressed="${n.feats.includes(id)}">${e} ${esc(t)}</button>`).join("")}</div>${othList("nf","¿Qué más necesitas?")}
    ${n.feats.filter(f=>f!=="nada").length?`<span class="mini-l">¿Es indispensable o negociable?</span><div class="reqs">${n.feats.filter(f=>f!=="nada").map(f=>{const x=NEED_FEATS.find(y=>y[0]===f)||[f,"",f];const r=n.req[f]||"must";return`<div class="req"><span>${x[1]} ${esc(x[2])}</span><div class="seg" data-req="${f}"><button type="button" data-v="must" aria-pressed="${r==="must"}">Obligatorio</button><button type="button" data-v="opt" aria-pressed="${r==="opt"}">Opcional</button></div></div>`;}).join("")}</div><span class="hint">Los opcionales no descartan venues; solo los usamos para ordenar.</span>`:''}</div>
   <div id="vlive"></div>`:''}''')
rep('''el.querySelectorAll(".nf").forEach(b=>b.onclick=()=>{const f=b.dataset.f;''', '''el.querySelectorAll("[data-req]").forEach(g=>g.querySelectorAll("button").forEach(b=>b.onclick=()=>{n.req[g.dataset.req]=b.dataset.v;g.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",x===b));drawVenueLive();}));
   el.querySelectorAll(".nf").forEach(b=>b.onclick=()=>{const f=b.dataset.f;''')
rep('''drawVenueLive();bindNav("lugar","fiesta","servicios");return;}''', '''bindOth(el,"lugar");drawVenueLive();bindNav("lugar","fiesta","servicios");return;}''')
rep('''const req={guests:g,date:S.date,start:S.start,end:S.end,format:n.format||"sentados",types:n.types,feats:n.feats,''', '''const req={guests:g,date:S.date,start:S.start,end:S.end,format:n.format||"sentados",types:n.types,feats:n.feats.filter(f=>(n.req||{})[f]!=="opt"),''')

# ---------- servicios: texto adaptado al planner
rep('''say(`Te dejé marcado lo más común para <b>${esc(S.occ.toLowerCase())}</b> ✨ Busca lo que necesites o explóralo por categoría.`)''',
    '''say(PLN()?`Te dejé marcado lo más común para <b>${esc(S.occ.toLowerCase())}</b> ✨ Elige lo que quieres que <b>${esc(PLN().n)}</b> consiga para tu fiesta.`:`Te dejé marcado lo más común para <b>${esc(S.occ.toLowerCase())}</b> ✨ Busca lo que necesites o explóralo por categoría.`)''')

# ---------- detalles (factura): «Otro» + fecha
rep('''${FACT_DOCS.map(d=>`<button type="button" class="chip fd" aria-pressed="${S.fact.docs.includes(d)}">${esc(d)}</button>`).join("")}</div>''',
    '''${FACT_DOCS.map(d=>`<button type="button" class="chip fd" aria-pressed="${S.fact.docs.includes(d)}">${esc(d)}</button>`).join("")}</div>${othList("fd","Otro documento")}''')
rep('''<div class="field"><label class="mini-l" for="fdays">Días que tarda el alta</label><input type="number" min="0" id="fdays" value="${esc(S.fact.days)}" class="${MISS(filled(S.fact.days))}" placeholder="Ej. 10"></div>''',
    '''<div class="field"><label class="mini-l" for="fdate">📅 ¿En qué fecha necesitas estos requisitos?</label><input type="date" id="fdate" min="${addDays(0)}" value="${esc(S.fact.reqDate)}" class="${MISS(!!S.fact.reqDate)}"></div>''')
rep('''${["Transferencia","Tarjeta corporativa","Cheque"].map(t=>`<button type="button" class="chip fm" aria-pressed="${S.fact.method.includes(t)}">${esc(t)}</button>`).join("")}</div></div>`:''}''',
    '''${["Transferencia","Tarjeta corporativa","Cheque"].map(t=>`<button type="button" class="chip fm" aria-pressed="${S.fact.method.includes(t)}">${esc(t)}</button>`).join("")}</div>${othList("fm","Otra forma de pago")}</div>`:''}''')
rep('''const fd=$("fdays");if(fd){fd.oninput=e=>{S.fact.days=e.target.value;refresh("detalles");};''', '''bindOth(el,"detalles");const fd=$("fdate");if(fd){fd.oninput=fd.onchange=e=>{S.fact.reqDate=e.target.value;refresh("detalles");};''')
rep('''if(!f.method.length)m.push("Forma de pago");''', '''if(!f.method.length&&!f.methodOther.some(filled))m.push("Forma de pago");''')
rep('''if(!f.docs.length)m.push("Documentos que pedirás");''', '''if(!f.docs.length&&!f.docsOther.some(filled))m.push("Documentos que pedirás");''')

# ---------- resultado
a = c.index(''' if(screen==="result"){const rs=rows(),t=total();''')
b = c.index(''' if(screen==="signup"){''')
RESULT = r''' if(screen==="result"){const rs=rows(),t=total(),pl=PLN();
  const nAv=k=>3+((k.length*7+S.guests)%6);
  const fecha=S.date?new Date(S.date+"T12:00").toLocaleDateString("es-MX",{day:"numeric",month:"long"}):"";
  const conf=`<svg class="conf" viewBox="0 0 400 140" preserveAspectRatio="none" aria-hidden="true"><circle cx="30" cy="20" r="6" fill="#FAFA19"/><rect x="340" y="14" width="14" height="6" rx="3" fill="#BEFF00" transform="rotate(25 347 17)"/><circle cx="370" cy="110" r="5" fill="#FAB4FF"/><rect x="70" y="112" width="16" height="6" rx="3" fill="#69FFC3" transform="rotate(-20 78 115)"/><circle cx="250" cy="12" r="4" fill="#FF6905"/><rect x="190" y="124" width="12" height="5" rx="2" fill="#FAFA19" transform="rotate(30 196 126)"/></svg>`;
  el.innerHTML=`<div class="rbar" id="rbar">${conf}
   <span class="meta">${esc(S.occ)} · ${S.guests.toLocaleString("es-MX")} invitados · ${fecha} · ${hours()} h${pl?` · con ${esc(pl.n)}`:""}</span>
   <div class="nums"><span class="pp">${money(t/S.guests)}</span><span>por persona</span><span class="tt">· Total aproximado <b>${money(t)}</b>${rs.some(r=>r.pend&&r.pend.length)?` + ${rs.reduce((a,r)=>a+(r.pend?r.pend.length:0),0)} por cotizar`:""}</span></div>
   ${earlyPct()?`<span class="meta">🎁 Gracias a tu anticipación, estás ahorrando ${earlyPct()}% (en promedio) respecto a otros anfitriones con la misma fiesta pero con menos anticipación.</span>`:''}
   <div class="save"><label for="pname">¿Cuál es el nombre de esta fiesta?<input type="text" id="pname" maxlength="60" value="${esc(S.partyName)}" placeholder="Ej. La boda de Mariana y Leo"></label><button class="btn" type="button" id="send">Guardar y enviar →</button></div></div>
  ${S.hasPlace===false?venueResultHtml():''}
  <div class="card"><h3 style="font-size:19px">Así se reparte 👇</h3>
   <div class="break scroll">${rs.map(r=>`<div><span>${r.e} ${esc(r.label)}${r.subs?`<br><span class="sub">${r.subs.map(esc).join(" · ")}</span>`:''}</span><span>${r.pendOnly?"Por cotizar":`${money(r.amt/S.guests)} c/u<br><span class="sub">${money(r.amt)}${r.pend&&r.pend.length?" + por cotizar":""}</span>`}</span>
    ${r.k!=="Planner"?`<div class="avail"><span>🔔 ${nAv(r.k)} proveedores que cumplen con lo que pides <b>están disponibles</b></span><button class="btn sm" type="button" data-ct="${esc(r.k)}">Contactar</button></div>`:''}</div>`).join("")}
   ${S.more?`<div><span>✏️ Pedido especial<br><span class="sub">${esc(S.more)}</span></span><span>Por cotizar</span></div>`:''}</div>
   <h3 style="font-size:19px">Consejos de Vernie 🪩</h3><div id="tipsBox">${tipHtml(tips("result"))}</div></div>`;
  hqvTrack("calculo_visto",{occ:S.occ,invitados:S.guests,total:Math.round(t)});
  $("pname").oninput=e=>{S.partyName=e.target.value;};
  const send=cta=>{const fiesta={nombre:(S.partyName||"").trim()||`${S.occ} de ${S.name.split(" ")[0]}`,occ:S.occ,kind:S.kind,guests:S.guests,date:S.date,start:S.start,end:S.end,hours:hours(),total:Math.round(t),pp:Math.round(t/S.guests),
    zona:S.hasPlace?((S.place.addr&&(S.place.addr.muni||S.place.addr.state))||""):(S.need.all?S.need.state:S.need.munis.join(", ")),venue:S.hasPlace===false,lugarDe:S.hasPlace?S.place.owner:null,
    planner:pl?{n:pl.n,e:pl.e,z:pl.z,y:pl.y,r:pl.r,f:pl.f,sp:pl.sp,b:pl.b}:null,
    rows:rs.map(r=>({k:r.k,e:r.e,label:r.label,subs:r.subs||[],amt:Math.round(r.amt),pend:!!r.pendOnly,disp:nAv(r.k)})),early:earlyPct(),
    servicios:Object.keys(S.sel).map(c=>({cat:c,subs:S.sel[c].map(s=>{const x=lineCalc(c,s,S.guests),r=REF[c+"|"+s];return{n:s,unidad:r?r[0]:null,estimado:Math.round(x.total||0),cantidad:x.qty||null};})}))};
   hqvTrack("guardar_y_enviar",{occ:S.occ,cta});
   if(parent!==window){try{parent.postMessage({hqv:"fiesta-lista",fiesta,nombre:S.name,cta},"*");}catch(_){}}
   else alert("En el sitio real aquí se abre «Crea tu cuenta» y luego tu cuenta.");};
  $("send").onclick=()=>send("guardar");el.querySelectorAll("[data-ct]").forEach(b=>b.onclick=()=>send("contactar:"+b.dataset.ct));confetti();return;}

'''
c = c[:a] + RESULT + c[b:]

(D / 'cot7.html').write_text(c)
print('cot7 ok', len(c))
