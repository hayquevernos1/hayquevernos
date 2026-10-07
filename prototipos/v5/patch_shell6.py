"""v6 en la cuenta (shell.html, en su lugar; respaldo en shell5_backup.html):
servicios «por cotizar», nombres del catálogo maestro, encuesta post-fiesta del anfitrión y cierre de trato del proveedor."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = Path('/home/claude/hqv/v5/shell5_backup.html').read_text()


def rep(a, b):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:100]
    s = s.replace(a, b, 1)


rep('''.sim{border:2px dashed''', '''.stars{display:flex;gap:4px}.stars button{border:0;background:none;font-size:28px;line-height:1;padding:2px;filter:grayscale(1);opacity:.45}.stars button[aria-pressed="true"]{filter:none;opacity:1}
.svq{display:grid;gap:6px;padding:10px 0;border-bottom:1px dashed var(--line)}.svq:last-of-type{border-bottom:0}
.sim{border:2px dashed''')

# nombres de ejemplo con las categorías del catálogo maestro
rep('''const POOL={"Música":''', '''const POOL={"Música y espectáculos":["DJ Rafa Beats","DJ Sonido Lunar","Mariachi Los Reyes","Grupo Versátil Fiesta","DJ Kenia","Banda La Chida","Trío Bohemio","DJ Mixer Max"],
 "Alimentos":["Taquizas Don Beto","Sabores de Coyoacán","Paella Mar y Tierra","Banquetes Lupe","Pastelería Canela","Mesa Dulce Lupita","Parrilladas El Norte","Catering Verde"],
 "Decoración y flores":["Globos Mágicos","Deco Fiesta Total","Flores y Listones","Arcos de Ensueño","Ambienta MX","Neón Party"],
 "Bebidas y barra":["Barra La Catrina","Mixología Agave","Aguas La Güera","Café Nómada","Cervecería Móvil"],
 "Música":''')
# filas «por cotizar»
rep('''function providersFor(row,base){const n=6+Math.floor(rnd()*9);''', '''function providersFor(row,base){const n=6+Math.floor(rnd()*9);if(!row.amt){const o=[];const names=POOL[row.k]||[];for(let i=0;i<n;i++){const km=Math.round((1+rnd()*24)*10)/10,rate=Math.round((3.9+rnd()*1.1)*10)/10,rev=Math.floor(rnd()*80),resp=[5,10,15,30,45,60,120,240][Math.floor(rnd()*8)];o.push({nm:names[i]||`${GEN[Math.floor(rnd()*GEN.length)]} ${SUR[Math.floor(rnd()*SUR.length)]}`,km,rate,rev,resp,price:null,badges:resp<=60?["responde_ya"]:[],nuevo:rev<3,fit:.5,score:.4*(1-km/25)+.3*((rate-3.5)/1.5)+.3*(1-resp/240),emo:row.e});}return o.sort((a,b)=>b.score-a.score);}''')
rep('''const rows=(f.rows||[]).filter(r=>r.k!=="Planner"&&r.amt>0);''', '''const rows=(f.rows||[]).filter(r=>r.k!=="Planner"&&(r.amt>0||r.pend));''')
rep('''<b class="${blur?"blur":""}">${esc(x.nm)}</b></span><b>${money(x.price)}</b></div>''', '''<b class="${blur?"blur":""}">${esc(x.nm)}</b></span><b>${x.price==null?"Por cotizar":money(x.price)}</b></div>''')
rep('''<div class="brk">${f.rows.map(r=>`<div><span>${r.e} ${esc(r.label)}</span><span>${money(r.amt)}</span></div>`).join("")}</div>''',
    '''<div class="brk">${f.rows.map(r=>`<div><span>${r.e} ${esc(r.label)}</span><span>${r.pend?"Por cotizar":money(r.amt)}</span></div>`).join("")}</div>''')

# ---------- encuesta post-fiesta (anfitrión)
rep('''function drawEvent(p){const e=getEv(),f=e.f;''', '''/* Encuesta post-fiesta: valida los promedios con lo que pasó de verdad (1 minuto) */
const FIT=[["falto","😬 Faltó"],["justo","👌 Justo"],["sobro","🤷 Sobró"]];
function surveyBox(e){const f=e.f,v=e.sv||(e.sv={total:f.total,fit:{},stars:0,note:""});const rows=f.rows.filter(r=>r.k!=="Venue").slice(0,3);
 return`<div class="box" id="svBox" style="background:var(--hqv-vainilla)"><h2>${em("party_popper")} ¿Cómo te fue en tu fiesta?</h2><span class="hint">1 minuto. Con tu respuesta calculamos mejor la próxima fiesta de alguien más 💜</span>
  <div class="svq"><b>💸 ¿Cuánto pagaste en total?</b><span class="hint">Ya pusimos nuestro cálculo. Si fue distinto, corrígelo.</span><input type="number" min="0" id="svTot" value="${esc(v.total)}" aria-label="Total pagado" style="max-width:220px"></div>
  ${rows.map(r=>`<div class="svq"><b>${r.e} ¿Alcanzó ${esc(r.label.toLowerCase())}?</b><div class="seg" data-fit="${esc(r.k)}">${FIT.map(([k,t])=>`<button type="button" data-v="${k}" aria-pressed="${v.fit[r.k]===k}">${t}</button>`).join("")}</div></div>`).join("")}
  <div class="svq"><b>⭐ ¿Cómo calificas a tus proveedores?</b><div class="stars">${[1,2,3,4,5].map(n=>`<button type="button" data-st="${n}" aria-pressed="${v.stars>=n}" aria-label="${n} estrellas">⭐</button>`).join("")}</div>
   <input type="text" id="svNote" value="${esc(v.note)}" placeholder="¿Algo que debamos saber? (opcional)"></div>
  <button class="btn host" type="button" id="svSend">Enviar y ganar mi insignia</button><span class="hint">Te regalamos la insignia <b>Anfitrión experto</b> y 10% en tu próxima cotización.</span></div>`;}
function bindSurvey(e){const v=e.sv,b=$("svBox");if(!b)return;
 $("svTot").oninput=x=>{v.total=+x.target.value||0;};$("svNote").oninput=x=>{v.note=x.target.value;};
 b.querySelectorAll("[data-fit]").forEach(g=>g.querySelectorAll("button").forEach(x=>x.onclick=()=>{v.fit[g.dataset.fit]=x.dataset.v;g.querySelectorAll("button").forEach(y=>y.setAttribute("aria-pressed",y===x));}));
 b.querySelectorAll("[data-st]").forEach(x=>x.onclick=()=>{v.stars=+x.dataset.st;b.querySelectorAll("[data-st]").forEach(y=>y.setAttribute("aria-pressed",+y.dataset.st<=v.stars));});
 $("svSend").onclick=()=>{if(!v.stars){toast("⭐ Califica a tus proveedores para enviar");return;}e.surveyDone=true;
  const dif=e.f.total?Math.round((v.total-e.f.total)/e.f.total*100):0;
  track("encuesta_post_fiesta",{occ:e.f.occ,invitados:e.f.guests,estimado:e.f.total,real:v.total,diferencia_pct:dif,alcanzo:v.fit,estrellas:v.stars,servicios:e.f.servicios||null});
  U.hostBadge=true;inbox("fiestas","🏅 Ganaste la insignia Anfitrión experto y 10% en tu próxima cotización.");confetti();drawAcct();};}
function drawEvent(p){const e=getEv(),f=e.f;const past=daysTo(f.date)<0;''')
rep('''   ${!e.paid||e.paid==="prov"?checklistBox(e):""}
  </div>''', '''   ${!e.paid||e.paid==="prov"?checklistBox(e):""}
   ${past?"":`<button class="sim" type="button" id="evPast" style="justify-self:start">Simular: ya pasó mi fiesta</button>`}
  </div>''')
rep('''$("evBack").onclick=()=>{U.eventId=null;drawAcct();};$("evEdit").onclick=()=>openJourney("fiestas",true,e.id);''',
    '''$("evBack").onclick=()=>{U.eventId=null;drawAcct();};$("evEdit").onclick=()=>openJourney("fiestas",true,e.id);
 const ep=$("evPast");if(ep)ep.onclick=()=>{f.date=new Date(now()-864e5).toISOString().slice(0,10);inbox("fiestas",`🎉 ¿Cómo te fue en tu ${f.occ.toLowerCase()}? Cuéntanos en 1 minuto.`);drawAcct();};
 if(past){const R0=$("evRight");R0.innerHTML=e.surveyDone?`<div class="box" style="background:var(--hqv-menta)"><h2>${em("glowing_star")} ¡Gracias por contarnos!</h2><span>Con tu respuesta ajustamos los cálculos para las próximas fiestas. Ya tienes tu insignia <b>Anfitrión experto</b> y 10% en tu próxima cotización.</span></div>`:surveyBox(e);bindSurvey(e);return;}''')
rep('''function evState(e){if(!e.paid)''', '''function evState(e){if(daysTo(e.f.date)<0)return e.surveyDone?'<span class="st go">Celebrada ✓</span>':'<span class="st wait">Cuéntanos cómo te fue</span>';if(!e.paid)''')

# ---------- cierre de trato (proveedor)
rep('''U.solicitudes.unshift({kind:"svc",occ:["Cumpleaños","Boda","XV años","Baby shower"][U.solicitudes.length%4],guests:[40,120,150,30][U.solicitudes.length%4],''',
    '''U.solicitudes.unshift({kind:"svc",occ:["Cumpleaños","Boda","15 años","Congreso"][U.solicitudes.length%4],guests:[40,120,150,300][U.solicitudes.length%4],svc:["Taquizas · por persona","Mesas de dulces · por paquete","DJ · por hora","Coffee break · por persona"][U.solicitudes.length%4],est:[8400,10500,7500,36000][U.solicitudes.length%4],''')
rep('''if(a==="no"){r.st="rechazada";}''', '''if(a==="no"){r.st="rechazada";}
  if(a==="close"){r.closing=true;r.cq=r.cq||"";}
  if(a==="cq"){r.cq=b.dataset.v;const inp=document.getElementById("cm-"+b.dataset.sol);if(inp)r.draft=inp.value;}
  if(a==="lost"){r.st="perdida";r.closing=false;}
  if(a==="why"){r.lostWhy=b.dataset.v;track("trato_perdido",{occ:r.occ,motivo:r.lostWhy});toast("👌 Gracias, nos ayuda a mejorar tus solicitudes.");}
  if(a==="cfin"){const v=+(document.getElementById("cm-"+b.dataset.sol)||{}).value||r.est;if(!r.cq){toast("Dinos si nuestro cálculo fue corto, bien o sobrado");return;}
   r.st="cerrada";r.closing=false;r.final=v;const po=U.postul.find(x=>x.st!=="Elegido");if(po)po.st="Elegido";
   track("cierre_trato",{occ:r.occ,invitados:r.guests,servicio:r.svc,estimado:r.est,final:v,diferencia_pct:Math.round((v-r.est)/r.est*100),calculo:r.cq});
   toast("🤝 ¡Felicidades por el cierre! Ya cuenta para tu insignia de 50 fiestas.");}''')
rep('''if(pl&&r.st==="aceptada")return''', '''if(!pl&&r.st==="aceptada"&&r.closing)return`<div class="item" style="flex-wrap:wrap">${head}<div class="soft" style="width:100%"><b>🤝 ¡Bien! Cuéntanos en 10 segundos</b>
   <label class="hint" for="cm-${i}">Monto final que cobraste</label><input type="number" min="0" id="cm-${i}" value="${r.draft||r.est||""}" style="max-width:200px">
   <span class="hint">Nuestro cálculo de cantidad para este evento fue…</span><div class="seg">${[["corto","Corto"],["bien","Bien"],["sobrado","Sobrado"]].map(([k,t])=>`<button type="button" data-sol="${i}" data-a="cq" data-v="${k}" aria-pressed="${r.cq===k}">${t}</button>`).join("")}</div>
   <button class="btn sm" type="button" data-sol="${i}" data-a="cfin" style="justify-self:start">Guardar</button></div></div>`;
 if(!pl&&r.st==="aceptada")return`<div class="item" style="flex-wrap:wrap">${head}${r.est?`<span class="hint" style="width:100%">Cálculo ¡HQV!: ~${money(r.est)} · ${esc(r.svc||"")}</span>`:""}<div class="row"><button class="btn sm" type="button" data-sol="${i}" data-a="close">🤝 Se cerró</button><button class="btn ghost sm" type="button" data-sol="${i}" data-a="lost">No se cerró</button></div></div>`;
 if(r.st==="perdida")return`<div class="item" style="flex-wrap:wrap">${head}<span class="st no">No se cerró</span>${r.lostWhy?"":`<span class="hint" style="width:100%">¿Por qué? (opcional)</span><div class="row">${["Precio","Fecha","Eligió a otro","No respondió"].map(t=>`<button class="pill sm" type="button" data-sol="${i}" data-a="why" data-v="${t}">${t}</button>`).join("")}</div>`}</div>`;
 if(r.st==="cerrada")return`<div class="item">${head}<span class="st go">Cerrada · ${money(r.final)}</span></div>`;
 if(pl&&r.st==="aceptada")return''')
rep('''if(r.st==="nueva")return`<div class="item" style="flex-wrap:wrap">${head}<span class="hint" style="width:100%">Anfitrión: Mariana G. · 55 8765 4321</span>''',
    '''if(r.st==="nueva")return`<div class="item" style="flex-wrap:wrap">${head}<span class="hint" style="width:100%">Anfitrión: Mariana G. · 55 8765 4321${r.svc?` · Busca: ${esc(r.svc)} · cálculo ¡HQV! ~${money(r.est)}`:""}</span>''')

# ---------- demo con el catálogo maestro + una fiesta que ya pasó
rep('''rows:[{k:"Venue",e:"🏛️",label:"Venue (renta del espacio)",amt:26000},{k:"Comida",e:"🌮",label:"Comida: taquiza",amt:24000},{k:"Música",e:"🎧",label:"Música: DJ",amt:9000},{k:"Postres",e:"🎂",label:"Postres: pastel",amt:4600},{k:"Decoración",e:"🎈",label:"Decoración: globos",amt:6000},{k:"Con alcohol",e:"🍸",label:"Barra libre",amt:15000}]};
 U.events=[newEvent(f)];''', '''rows:[{k:"Venue",e:"🏛️",label:"Venue (renta del espacio)",amt:26000},{k:"Alimentos",e:"🍽️",label:"Alimentos",subs:["Taquizas","Pasteles de celebración"],amt:15300},{k:"Música y espectáculos",e:"🎧",label:"Música y espectáculos",subs:["DJ"],amt:7500},{k:"Decoración y flores",e:"💐",label:"Decoración y flores",subs:["Decoración con globos"],amt:2800},{k:"Bebidas y barra",e:"🍹",label:"Bebidas y barra",subs:["Barra libre"],amt:19200}]};
 const past={occ:"Baby shower",kind:"social",guests:35,date:new Date(now()-3*864e5).toISOString().slice(0,10),hours:4,total:21400,pp:611,zona:"Coyoacán",
  rows:[{k:"Alimentos",e:"🍽️",label:"Alimentos",subs:["Catering de cóctel y canapés","Mesas de postres"],amt:10325},{k:"Bebidas y barra",e:"🍹",label:"Bebidas y barra",subs:["Coctelería sin alcohol"],amt:3850},{k:"Decoración y flores",e:"💐",label:"Decoración y flores",subs:["Decoración con globos"],amt:2800},{k:"Experiencias y actividades",e:"🎡",label:"Experiencias y actividades",subs:["Glitter bar"],amt:2500}]};
 const pe=newEvent(past);pe.paid="prov";U.events=[newEvent(f),pe];''')
rep('''U.site={nombre:"Diego Juárez",negocio:"DJ Diego Fiestas",url:"hayquevernos.com/dj-diego-fiestas",tipos:["services","planner"],servicios:[{cat:"Música"}],completo:85};''',
    '''U.site={nombre:"Diego Juárez",negocio:"DJ Diego Fiestas",url:"hayquevernos.com/dj-diego-fiestas",tipos:["services","planner"],servicios:[{cat:"Música y espectáculos"}],completo:85};''')
rep('''U.postul=[{ev:"Boda · 120 invitados",svc:"Música",pos:1,of:7,st:"Elegido"},{ev:"XV años · 150 invitados",svc:"Música",pos:4,of:9,st:"No elegido esta vez"},{ev:"Baby shower · 30 invitados",svc:"Música",pos:2,of:5,st:"Vista"}];''',
    '''U.postul=[{ev:"Boda · 120 invitados",svc:"DJ",pos:1,of:7,st:"Elegido"},{ev:"15 años · 150 invitados",svc:"DJ",pos:4,of:9,st:"No elegido esta vez"},{ev:"Baby shower · 30 invitados",svc:"DJ",pos:2,of:5,st:"Vista"}];
 inbox("fiestas","🎉 ¿Cómo te fue en tu baby shower? Cuéntanos en 1 minuto.");''')
s = s.replace('PROTOTIPO v5', 'PROTOTIPO v6')
P.write_text(s)
print('shell ok', len(s))
