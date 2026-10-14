/* ===== v15 · Servicios con el catálogo v2: servicio completo / staff / solo renta =====
   Un solo motor para todas las categorías (qué incluye · tarifa · extras) y catering con formatos,
   tiempos o variedades y bebidas. Variabilidad ± y temporada alta con calendario a nivel paso. */
const WAYS=[["full","🎁","Servicio completo","Llevo todo: equipo, insumos y personal"],["staff","🙋","Solo mi talento (staff)","Voy yo o mi equipo; el lugar o el cliente pone lo demás"],["rent","📦","Solo renta","Rento el equipo o los artículos, sin operarlos"]];
const FOOD_FMT=["Banquete","Buffet","Cóctel","Estación","Box lunch","Mesa de postres y pastel","Comida para staff y proveedores","Coffee break"];
const FMT_EMO={"Banquete":"🍽️","Buffet":"🥘","Cóctel":"🍢","Estación":"🌮","Box lunch":"🥡","Barra de bebidas":"🍹","Coffee break":"☕","Mesa de postres y pastel":"🎂","Comida para staff y proveedores":"🍱"};
const MONTHS=[["ene","Ene"],["feb","Feb"],["mar","Mar"],["abr","Abr"],["may","May"],["jun","Jun"],["jul","Jul"],["ago","Ago"],["sep","Sep"],["oct","Oct"],["nov","Nov"],["dic","Dic"]];
const HIGH_STD=["may","jun","oct","nov","dic"];
const GASTROS=[...new Set([...Object.keys(C2.cocina.Salado),...Object.keys(C2.cocina.Dulce)])];
const U_FULL=["Por persona","Por evento","Por paquete","Por pieza","Por hora","Por caja","Por kilo","Por litro","Por mesa","Por docena (12 piezas)","Por ciento (100 piezas)","Por estación","Por día","Por menú"];
const U_STAFF=[["Por hora","por hora"],["Por turno","por turno (5 h)"],["Por evento","por evento"],["Por día","por día"]];
const U_RENT=[["Por pieza","por pieza"],["Por juego","por juego"],["Por evento","por evento"],["Por día","por día"]];
const TPL={"Banquete":[["3","tiempos","de menú"],["1","mesero","por cada 15 invitados"],["","Loza, cristalería y mantelería",""]],
 "Buffet":[["4","guisados","a elegir"],["2","guarniciones",""],["1","mesero","por cada 25 invitados"]],
 "Cóctel":[["8","piezas","por persona"],["1","mesero","por cada 25 invitados"]],
 "Estación":[["1","estación","montada con cocinero"],["3","salsas y complementos",""]],
 "Box lunch":[["1","caja","por persona"],["1","bebida",""],["1","postre",""]],
 "Barra de bebidas":[["1","barra","montada"],["1","bartender","por cada 50 invitados"],["","Hielo, vasos y popotes",""]],
 "Coffee break":[["2","bebidas calientes","ilimitadas"],["3","bocadillos","por persona"]],
 "Mesa de postres y pastel":[["6","variedades","de postres"],["3","piezas","por persona"],["","Montaje y decoración de mesa",""]],
 "Comida para staff y proveedores":[["1","platillo","por persona"],["1","bebida",""]]};
const UDEF={"Estación":"Por evento","Mesa de postres y pastel":"Por paquete"};
const TIEMPOS={"Banquete":[["Entrada","Salado"],["Plato fuerte","Salado"],["Postre","Dulce"]],"Buffet":[["Variedad 1","Salado"],["Variedad 2","Salado"]],"Cóctel":[["Variedad 1","Salado"],["Variedad 2","Salado"]],
 "Estación":[["Variedad 1","Salado"]],"Box lunch":[["Variedad 1","Salado"]],"Mesa de postres y pastel":[["Variedad 1","Dulce"],["Variedad 2","Dulce"]],"Comida para staff y proveedores":[["Variedad 1","Salado"]],"Coffee break":[["Bocadillo 1","Salado"]]};
const isFood=n=>FOOD_FMT.includes(n),isDrink=n=>n==="Barra de bebidas"||n==="Coffee break";
const DISH_LIST={};["Salado","Dulce"].forEach(k=>{const s=new Set();Object.values(C2.cocina[k]).forEach(g=>Object.entries(g).forEach(([e,ps])=>{s.add(e);ps.forEach(p=>s.add(p));}));DISH_LIST[k]=[...s].sort((a,b)=>a.localeCompare(b,"es"));});
const DRINK_VARS=[...new Set(C2.bebidas.flatMap(b=>b.v))].sort((a,b)=>a.localeCompare(b,"es"));
function blankOffer(n){const t=TPL[n]||[["5","horas","de servicio"]];
 return{n,inc:t.map(([q,u,w])=>({q,u,w})),dur:/Box lunch|Mesa de postres/.test(n)?"":"5",durU:"horas",tar:[{price:"",u:UDEF[n]||(isFood(n)||n==="Barra de bebidas"?"Por persona":"Por evento"),uo:"",alc:""}],ext:[],
  gas:[],tiempos:(TIEMPOS[n]||[]).map(([nm,k])=>({n:nm,k,d:""})),dserv:n==="Barra de bebidas"?["Barra"]:[],drinks:n==="Coffee break"?["Café","Tés, tisanas e infusiones"]:[],dvar:""};}
function svcDefaults(s){if(!s.ways)s.ways={full:false,staff:false,rent:false};if(!s.offers)s.offers=[];if(!s.staff)s.staff=[];if(!s.rent)s.rent=[];if(s.open===undefined)s.open="";if(s.descEdited===undefined)s.descEdited=filled(s.desc);}
function tarUnitLabel(t){return t.u==="__otra"?(t.uo?"por "+t.uo.replace(/^por\s+/i,""):"otra unidad"):uLabel(t.u);}
function syncSubs(s){svcDefaults(s);const L=[];
 if(s.ways.full)s.offers.forEach(o=>o.tar.forEach(t=>{if(t.u)L.push({n:o.n,u:t.u,uo:t.uo||"",price:t.price,yieldP:t.alc||"",pkgP:t.alc||"",pkgH:o.dur||"",unit:tarUnitLabel(t)});}));
 if(s.ways.staff)s.staff.forEach(r=>L.push({n:r.n,u:r.u,uo:"",price:r.price,yieldP:"",pkgP:"",pkgH:r.min||"",unit:uLabel(r.u)}));
 if(s.ways.rent)s.rent.forEach(r=>L.push({n:r.n,u:r.u,uo:"",price:r.price,yieldP:"",pkgP:"",pkgH:"",unit:uLabel(r.u)}));
 s.subs=L;if(!s.descEdited)s.desc=autoDesc(s);}
function joinY(a){a=a.filter(Boolean);return a.length<2?a.join(""):a.slice(0,-1).join(", ")+" y "+a[a.length-1];}
function autoDesc(s){const p=[];if(s.ways.full&&s.offers.length)p.push(joinY(s.offers.map(o=>o.n.toLowerCase())));if(s.ways.staff&&s.staff.length)p.push(joinY(s.staff.map(r=>r.n.toLowerCase())));if(s.ways.rent&&s.rent.length)p.push("renta de "+joinY(s.rent.map(r=>r.n.toLowerCase())));
 if(!p.length)return"";const t=joinY(p);return t.charAt(0).toUpperCase()+t.slice(1)+" para tu fiesta.";}
function incText(o){return o.inc.filter(r=>filled(r.u)||filled(r.w)).map(r=>[r.q,r.u,r.w].filter(filled).join(" ")).join(" · ");}
const VAR=()=>+S.svcVar||0,HIGH=()=>S.svcHigh&&+S.svcHigh.pct>0?+S.svcHigh.pct:0;
function offerHost(o,t,cat){if(!(+t.price>0))return"";const x={n:o.n,u:t.u,uo:t.uo,price:t.price,yieldP:t.alc,pkgP:t.alc};
 if(t.u==="__otra")return`<span class="hv">👀 Unidad nueva: el anfitrión la verá tal cual y tú le confirmas el total.</span>`;
 const r=hqvCost({cat,sub:o.n,u:t.u,price:+t.price,guests:EXG,hours:+o.dur||EXH,rinde:t.alc,pkgP:t.alc});
 if(r.pend)return`<span class="hv">👀 Dinos para cuántas personas alcanza y lo convertimos; si no, el anfitrión lo verá «por cotizar».</span>`;
 const pp=Math.round(r.total/EXG),v=VAR(),h=HIGH();
 return`<span class="hv">👀 En una fiesta de ${EXG} personas el anfitrión ve <b>${money(pp)}</b> por persona · <b>${money(Math.round(r.total))}</b> en total${v?` <span class="pm">± ${v}%</span>`:""}${h?` · temporada alta ${money(Math.round(r.total*(1+h/100)))}`:""}${r.note?" · "+esc(r.note):""}</span>`;}
function offerOk(o){return o.tar.length&&o.tar.every(t=>filled(t.price)&&t.u&&(t.u!=="__otra"||filled(t.uo)))&&o.ext.every(e=>filled(e.w||e.u)&&filled(e.cost));}
function staffOk(r){return filled(r.price)&&!!r.u;}
function offerSummary(o){const t=o.tar.find(x=>filled(x.price));return[incText(o),t?`${money(t.price)} ${tarUnitLabel(t)}`:""].filter(Boolean).join(" · ");}
function rowsInc(o,j,k,cost){const list=cost?o.ext:o.inc,cls=cost?"ex":"in";
 return list.map((r,ri)=>`<div class="incr ${cls}" data-ri="${ri}"><input type="text" inputmode="decimal" class="r-q" value="${esc(r.q)}" placeholder="#" aria-label="Cantidad"><input type="text" class="r-u" list="dlIncU" value="${esc(r.u)}" placeholder="${cost?"pastel, hora extra…":"piezas, meseros, horas…"}" aria-label="Unidad"><input type="text" class="r-w" value="${esc(r.w)}" placeholder="${cost?"detalle (opcional)":"detalle: de menú, por persona…"}" aria-label="Detalle">${cost?`<label class="r-c"><span>$</span><input type="number" min="0" class="r-cost${MISS(filled(r.cost))}" value="${esc(r.cost)}" aria-label="Costo del extra"></label>`:""}<button type="button" class="link bad r-x" aria-label="Quitar renglón">✕</button></div>`).join("")+
  `<button type="button" class="link r-add" data-l="${cls}" style="justify-self:start">+ ${cost?"Agregar extra":"Agregar otro"}</button>`;}
function offerCard(s,k,o,j,cat){const open=s.open==="f"+j,ok=offerOk(o),emo=FMT_EMO[o.n]||"✨";
 if(!open)return`<div class="dlc closed ofc${MISS(ok)}" data-j="${j}"><button type="button" class="dlh of-open"><b>${emo}</b><span class="sm"><b style="color:#1a1033">${esc(o.n)}</b> · ${esc(offerSummary(o)||"falta tu precio")}</span><span class="ed">${ok?"✏️ Editar":"⚠️ Completar"}</span></button></div>`;
 const food=isFood(o.n)&&o.n!=="Coffee break",drink=isDrink(o.n),tl=o.n==="Banquete"?"tiempo":o.n==="Coffee break"?"bocadillo":"variedad";
 return`<div class="dlc open ofc${MISS(ok)}" data-j="${j}">
  <div class="dlh"><b>${emo} ${esc(o.n)}</b><span class="sm"></span><button type="button" class="link bad of-x" aria-label="Quitar ${esc(o.n)}">✕ Quitar</button></div>
  ${food?`<span class="mini-l">🌎 ¿Qué cocina? <span class="opt">(opcional)</span></span><div class="chips cmini">${GASTROS.map(g=>`<button type="button" class="chip of-g" data-g="${esc(g)}" aria-pressed="${o.gas.includes(g)}">${TICK}${esc(g)}</button>`).join("")}</div>`:""}
  ${drink?`<span class="mini-l">🍹 ¿Cómo lo sirves?</span><div class="chips cmini">${C2.bebidasServicio.map(g=>`<button type="button" class="chip of-ds" data-v="${esc(g)}" aria-pressed="${o.dserv.includes(g)}">${TICK}${esc(g)}</button>`).join("")}</div>
   <span class="mini-l">¿Qué bebidas? <span class="opt">Toca todas las que sirvas</span></span><div class="chips cmini">${C2.bebidas.map(b=>`<button type="button" class="chip of-dr" data-v="${esc(b.n)}" aria-pressed="${o.drinks.includes(b.n)}">${TICK}${b.alc.includes("Con alcohol")&&!b.alc.includes("Sin alcohol")?"🍸 ":b.alc.includes("Con alcohol")?"":"🧃 "}${esc(b.n)}</button>`).join("")}</div>
   <input type="text" class="of-dv" list="dlDrinks" value="${esc(o.dvar)}" placeholder="Variedades (opcional): margarita, carajillo, agua de jamaica…" aria-label="Variedades de bebidas">`:""}
  ${o.tiempos.length||food?`<span class="mini-l">🍴 ${o.n==="Banquete"?"Tiempos":o.n==="Coffee break"?"Bocadillos":"Variedades"} <span class="opt">(opcional · si no los defines, el anfitrión ve lo que incluye)</span></span>
   ${o.tiempos.map((t,ti)=>`<div class="tmr" data-ti="${ti}"><input type="text" class="t-n" value="${esc(t.n)}" aria-label="Nombre del ${tl}"><div class="yn sd" role="group"><button type="button" data-k="Salado" aria-pressed="${t.k==="Salado"}">Salado</button><button type="button" data-k="Dulce" aria-pressed="${t.k==="Dulce"}">Dulce</button></div><input type="text" class="t-d" list="dl${t.k}" value="${esc(t.d)}" placeholder="¿Qué sirves? Escribe y elige: tacos, crema de elote, tiramisú…" aria-label="Platillo"><button type="button" class="link bad t-x" aria-label="Quitar ${tl}">✕</button></div>`).join("")}
   <button type="button" class="link t-add" style="justify-self:start">+ Agregar ${tl}</button>`:""}
  <span class="mini-l">✅ ¿Qué incluye? <span class="opt">Ya va dentro de tu precio · edita o borra lo que no aplique</span></span>
  ${rowsInc(o,j,k,false)}
  <div class="durr"><span class="mini-l" style="margin:0">⏱️ Duración del servicio</span><input type="number" min="0" step="any" class="of-dur" value="${esc(o.dur)}" placeholder="—" aria-label="Duración"><select class="of-duru" aria-label="Unidad de duración">${["minutos","horas","días"].map(u=>`<option ${o.durU===u?"selected":""}>${u}</option>`).join("")}</select></div>
  <span class="mini-l">💲 Tarifa <span class="opt">¿Cobras de varias formas? Agrega otra tarifa</span></span>
  ${o.tar.map((t,ti)=>`<div class="tarr" data-ti="${ti}"><label class="sl-p"><span>$</span><input type="number" min="0" step="any" class="ta-p${MISS(filled(t.price))}" value="${esc(t.price)}" placeholder="precio" aria-label="Precio"></label>
   <select class="ta-u" aria-label="Cómo lo cobras">${U_FULL.map(u=>`<option value="${esc(u)}" ${t.u===u?"selected":""}>${esc(uLabel(u))}</option>`).join("")}<option value="__otra" ${t.u==="__otra"?"selected":""}>✏️ otra unidad…</option></select>
   ${t.u==="__otra"?`<input type="text" class="ta-uo${MISS(filled(t.uo))}" list="dlUnits" value="${esc(t.uo)}" placeholder="por charola, por metro…" aria-label="Otra unidad">`:""}
   ${t.u!=="Por persona"?`<label class="ta-al">alcanza para <input type="number" min="0" class="ta-a" value="${esc(t.alc)}" placeholder="#" aria-label="Alcanza para cuántas personas"> personas</label>`:""}
   ${o.tar.length>1?`<button type="button" class="link bad ta-x" aria-label="Quitar tarifa">✕</button>`:""}<div class="ta-hv">${offerHost(o,t,s.cat)}</div></div>`).join("")}
  <button type="button" class="link ta-add" style="justify-self:start">+ Otra tarifa</button>
  <span class="mini-l">➕ Extras <span class="opt">(opcional · lo que el anfitrión puede sumar con costo)</span></span>
  ${rowsInc(o,j,k,true)}
  ${ok?`<button type="button" class="btn cta sm dl-ok of-ok">Listo ✓</button>`:""}</div>`;}
function staffCard(s,k,cat){const open=s.open==="st",ok=s.staff.length&&s.staff.every(staffOk);
 if(!open)return`<div class="dlc closed ofc${MISS(ok)}"><button type="button" class="dlh st-open"><b>🙋</b><span class="sm"><b style="color:#1a1033">Staff</b> · ${esc(s.staff.map(r=>r.n+(filled(r.price)?` ${money(r.price)} ${uLabel(r.u)}`:"")).join(" · ")||"elige tus perfiles")}</span><span class="ed">${ok?"✏️ Editar":"⚠️ Completar"}</span></button></div>`;
 const names=[...new Set([...(cat?cat.staff:[]),...s.staff.map(r=>r.n)])];
 return`<div class="dlc open ofc${MISS(ok)}"><div class="dlh"><b>🙋 Solo mi talento (staff)</b><span class="sm"></span></div>
  <span class="mini-l">¿Qué perfiles ofreces? <span class="opt">Tú pones el talento; el lugar o el cliente pone el equipo</span></span>
  <div class="chips cmini">${names.map(n=>`<button type="button" class="chip st-c" data-n="${esc(n)}" aria-pressed="${s.staff.some(r=>r.n===n)}">${TICK}${esc(n)}</button>`).join("")}<button type="button" class="chip new st-new">✏️ Otro</button></div>
  <div class="newrow" hidden><input type="text" class="st-in" list="dlStaff" placeholder="Ej. Taquero, Bartender…" aria-label="Otro perfil"><button type="button" class="btn sm st-addb">Agregar</button></div>
  ${s.staff.map((r,ri)=>`<div class="tarr st-r" data-ri="${ri}"><b class="rn">${esc(r.n)}</b><label class="sl-p"><span>$</span><input type="number" min="0" class="sr-p${MISS(filled(r.price))}" value="${esc(r.price)}" placeholder="precio" aria-label="Precio de ${esc(r.n)}"></label><select class="sr-u" aria-label="Cómo lo cobras">${U_STAFF.map(([u,t])=>`<option value="${u}" ${r.u===u?"selected":""}>${t} c/u</option>`).join("")}</select>${r.u==="Por hora"?`<label class="ta-al">mínimo <input type="number" min="0" class="sr-m" value="${esc(r.min)}" placeholder="#" aria-label="Horas mínimas"> h</label>`:""}<div class="ta-hv">${filled(r.price)?`<span class="hv">👀 El anfitrión ve: 1 ${esc(r.n.toLowerCase().replace(/(es|s)$/,""))} por ${r.u==="Por hora"?(+r.min||5)+" h":uLabel(r.u).replace("por ","")} = <b>${money((+r.price||0)*(r.u==="Por hora"?(+r.min||5):1))}</b>${VAR()?` <span class="pm">± ${VAR()}%</span>`:""}</span>`:""}</div></div>`).join("")}
  ${ok?`<button type="button" class="btn cta sm dl-ok of-ok">Listo ✓</button>`:""}</div>`;}
function rentCard(s,k,cat){const open=s.open==="rt",ok=s.rent.length&&s.rent.every(staffOk);
 if(!open)return`<div class="dlc closed ofc${MISS(ok)}"><button type="button" class="dlh rt-open"><b>📦</b><span class="sm"><b style="color:#1a1033">Renta</b> · ${esc(s.rent.map(r=>r.n+(filled(r.price)?` ${money(r.price)} ${uLabel(r.u)}`:"")).join(" · ")||"elige lo que rentas")}</span><span class="ed">${ok?"✏️ Editar":"⚠️ Completar"}</span></button></div>`;
 const names=[...new Set([...(cat?cat.rent:[]),...s.rent.map(r=>r.n)])];
 return`<div class="dlc open ofc${MISS(ok)}"><div class="dlh"><b>📦 Solo renta</b><span class="sm"></span></div>
  <span class="mini-l">¿Qué rentas?</span><div class="chips cmini">${names.map(n=>`<button type="button" class="chip rt-c" data-n="${esc(n)}" aria-pressed="${s.rent.some(r=>r.n===n)}">${TICK}${esc(n)}</button>`).join("")}<button type="button" class="chip new rt-new">✏️ Otro</button></div>
  <div class="newrow" hidden><input type="text" class="rt-in" placeholder="Ej. Pista de baile iluminada" aria-label="Otro artículo"><button type="button" class="btn sm rt-addb">Agregar</button></div>
  ${s.rent.map((r,ri)=>`<div class="tarr rt-r" data-ri="${ri}"><b class="rn">${esc(r.n)}</b><label class="sl-p"><span>$</span><input type="number" min="0" class="sr-p${MISS(filled(r.price))}" value="${esc(r.price)}" placeholder="precio" aria-label="Precio de ${esc(r.n)}"></label><select class="sr-u" aria-label="Cómo lo cobras">${U_RENT.map(([u,t])=>`<option value="${u}" ${r.u===u?"selected":""}>${t}</option>`).join("")}</select><label class="ta-al">tengo <input type="number" min="0" class="sr-m" value="${esc(r.min)}" placeholder="#" aria-label="Cantidad disponible"> disponibles <span class="opt">(opcional)</span></label></div>`).join("")}
  ${ok?`<button type="button" class="btn cta sm dl-ok of-ok">Listo ✓</button>`:""}</div>`;}
function addOffer(s,n){svcDefaults(s);s.ways.full=true;let j=s.offers.findIndex(o=>o.n===n);if(j<0){s.offers.push(blankOffer(n));j=s.offers.length-1;}s.open="f"+j;}
function addPerson(s,list,n,u){svcDefaults(s);if(!s[list].some(r=>r.n===n))s[list].push({n,price:"",u,min:""});s.ways[list==="staff"?"staff":"rent"]=true;s.open=list==="staff"?"st":"rt";}
function boxFor(cat){let i=S.services.findIndex(s=>s.cat===cat);if(i<0){i=S.services.findIndex(s=>!s.cat);if(i<0){S.services.push(blankSvc());i=S.services.length-1;}S.services[i].cat=cat;}svcDefaults(S.services[i]);return i;}
function priceBoxHtml(){const h=S.svcHigh;return`<div class="field pricebox"><span class="lbl">💸 Tus precios</span>
  <div class="sub-box" style="display:grid;gap:10px">
   <div class="varr"><span><b>¿Cuánto puede variar tu precio al negociar?</b><span class="hint" style="display:block">El anfitrión ve precios estandarizados de la comunidad. Lo que pongas aquí es tu margen al platicar y queda bajo tu responsabilidad. Recomendamos <b>±20%</b>.</span></span><label class="pmf"><span>±</span><input type="number" min="0" max="100" id="svcVar" class="${MISS(filled(S.svcVar))}" value="${esc(S.svcVar)}" aria-label="Variabilidad en porcentaje"><span>%</span></label></div>
   <div class="varr"><span><b>🔥 En temporada alta cobro</b><span class="hint" style="display:block">Calendario estándar ¡Hay que vernos! (bodas, XV y posadas). Edítalo si tu temporada es otra. Pon 0 si cobras igual todo el año.</span></span><label class="pmf"><span>+</span><input type="number" min="0" max="100" id="svcHigh" value="${esc(h.pct)}" aria-label="Aumento en temporada alta"><span>%</span></label></div>
   ${+h.pct>0?`<div class="chips cmini months">${MONTHS.map(([m,t])=>`<button type="button" class="chip mo" data-m="${m}" aria-pressed="${h.months.includes(m)}">${TICK}${t}</button>`).join("")}</div>`:""}
  </div></div>`;}
function bindPriceBox(redraw){const v=$("svcVar");if(v)v.oninput=e=>{S.svcVar=e.target.value;document.querySelectorAll(".pm").forEach(x=>x.textContent="± "+(+S.svcVar||0)+"%");changed();};
 const h=$("svcHigh");if(h){h.oninput=e=>{S.svcHigh.pct=e.target.value;changed();};h.onchange=()=>redraw();}
 document.querySelectorAll(".mo").forEach(c=>c.onclick=()=>{const m=c.dataset.m,M=S.svcHigh.months;S.svcHigh.months=M.includes(m)?M.filter(x=>x!==m):MONTHS.map(x=>x[0]).filter(x=>x===m||M.includes(x));c.setAttribute("aria-pressed",S.svcHigh.months.includes(m));changed();});}
const VIATICOS=`<span class="hint viat">🚗 Si hay viáticos o costos adicionales por traslado fuera de tu zona, se acuerdan en la conversación directa con el anfitrión.</span>`;
function svcPlist(s){svcDefaults(s);const v=+S.svcVar||0,out=[];
 if(s.ways.full)s.offers.forEach(o=>{const t=o.tar.filter(x=>filled(x.price));out.push(`<span class="po"><span class="poh"><b>${FMT_EMO[o.n]||"✨"} ${esc(o.n)}</b> <span class="price">${t.length?t.map(x=>`${money(x.price)} <small>${esc(tarUnitLabel(x))}${+x.alc>0?` · ${esc(x.alc)} personas`:""}</small>`).join(" · "):"<small>Por cotizar</small>"}${v&&t.length?` <small class="pmv">± ${v}%</small>`:""}</span></span>${incText(o)?`<small class="inc">Incluye: ${esc(incText(o))}${o.tiempos.some(x=>filled(x.d))?` · ${esc(o.tiempos.filter(x=>filled(x.d)).map(x=>x.n+": "+x.d).join(" · "))}`:""}</small>`:""}${o.ext.length?`<small class="inc">Extras: ${esc(o.ext.map(e=>[e.q,e.u,e.w].filter(filled).join(" ")+(filled(e.cost)?" "+money(e.cost):"")).join(" · "))}</small>`:""}</span>`);});
 if(s.ways.staff&&s.staff.length)out.push(`<span class="po"><span class="poh"><b>🙋 Staff</b> <span class="price">${s.staff.map(r=>`${esc(r.n)} ${filled(r.price)?money(r.price):""} <small>${esc(uLabel(r.u))}</small>`).join(" · ")}</span></span></span>`);
 if(s.ways.rent&&s.rent.length)out.push(`<span class="po"><span class="poh"><b>📦 Renta</b> <span class="price">${s.rent.map(r=>`${esc(r.n)} ${filled(r.price)?money(r.price):""} <small>${esc(uLabel(r.u))}</small>`).join(" · ")}</span></span></span>`);
 return out.join("");}
function drawServices(){const list=$("svcList");if(!list)return;
 list.innerHTML=S.services.map((s,i)=>{svcDefaults(s);const cat=catOf(s.cat),k="s"+i,anchor="s"+(i+1),fl=FLASH&&FLASH.i===i?FLASH.msg:"";
 const shown=CAT2.filter(c=>scopeOk(c.t)||S.services.some(y=>y.cat===c.n)),hid=CAT2.length-shown.length;
 const fulls=cat?[...new Set([...(cat.full||[]),...s.offers.map(o=>o.n)])]:[];
 const any=(s.ways.full&&s.offers.length)||(s.ways.staff&&s.staff.length)||(s.ways.rent&&s.rent.length);
 return`<div class="box" data-i="${i}"><div class="box-head"><h3>${cat?cat.e+" "+esc(cat.n):"Ficha "+(i+1)}</h3><span style="display:flex;gap:14px">${cat?`<button type="button" class="link ch-cat">Cambiar categoría</button>`:''}${S.services.length>1?`<button type="button" class="link bad rm-svc">Quitar</button>`:''}</span></div>
 ${fl?`<div class="flash">${esc(fl)}</div>`:''}
 ${!cat?`<div class="field"><span class="lbl">1. Elige tu categoría</span><div class="cats big${MISS(!!cat)}">${shown.map(c=>{const used=S.services.some((y,ii)=>ii!==i&&y.cat===c.n);return`<button type="button" class="cat" data-c="${esc(c.n)}" aria-pressed="${s.cat===c.n}"><span class="emo">${c.e}</span><span>${esc(c.n)}${used?' <small>· ya la tienes</small>':''}</span></button>`;}).join("")}</div>${hid?`<span class="hint">Ocultamos ${hid} categorías que son para otro tipo de eventos.</span>`:""}</div>`:''}
 ${cat?`<div class="field"><span class="lbl">¿Cómo trabajas? <span class="opt">Puedes elegir varias</span></span><div class="ways${MISS(s.ways.full||s.ways.staff||s.ways.rent)}">${WAYS.filter(w=>w[0]!=="rent"||(cat.rent||[]).length||s.ways.rent).filter(w=>w[0]!=="staff"||(cat.staff||[]).length).map(([w,e,t,d])=>`<button type="button" class="way" data-w="${w}" aria-pressed="${!!s.ways[w]}"><span class="emo">${e}</span><span><b>${t}</b><small>${d}</small></span></button>`).join("")}</div></div>
  ${s.ways.full?`<div class="field"><span class="lbl">🎁 ¿Qué ofreces como servicio completo? <span class="opt">Cada uno se configura en su ficha</span></span><div class="chips${MISS(s.offers.length>0)}" style="border-radius:14px">${fulls.map(n=>`<button type="button" class="chip of-c" data-n="${esc(n)}" aria-pressed="${s.offers.some(o=>o.n===n)}">${TICK}${FMT_EMO[n]?FMT_EMO[n]+" ":""}${esc(n)}</button>`).join("")}<button type="button" class="chip new of-new">✏️ Otro</button></div>
   <div class="newrow" hidden><input type="text" class="of-in" list="dlFull" placeholder="¿Cómo se llama tu servicio?" aria-label="Otro servicio"><button type="button" class="btn sm of-addb">Agregar</button></div>
   ${s.offers.map((o,j)=>offerCard(s,k,o,j,cat)).join("")}</div>`:""}
  ${s.ways.staff?`<div class="field">${staffCard(s,k,cat)}</div>`:""}
  ${s.ways.rent?`<div class="field">${rentCard(s,k,cat)}</div>`:""}`:''}
 ${any?`<div class="field"><label class="lbl" for="d-${k}">💬 Descríbelo en una frase <span class="opt">${s.descEdited?"":"✨ te la escribimos; cámbiala si quieres"}</span></label><input type="text" id="d-${k}" class="${MISS(filled(s.desc))}" value="${esc(s.desc)}" placeholder="Qué incluye y para cuántas personas"></div>
 <div class="field"><span class="lbl">🚚 ¿Cómo entregas este servicio? <span class="opt">Elige todas las que hagas</span></span>
  <div class="chips dlm-chips${MISS((s.dl||[]).length>0)}" style="border-radius:14px">${DL_MODS.map(([m,e])=>`<button type="button" class="chip dlm" data-m="${esc(m)}" aria-pressed="${(s.dl||[]).some(d=>d.m===m)}">${TICK}${e} ${esc(m)}</button>`).join("")}</div>
  ${(s.dl||[]).map((d,j)=>dlCard(s,k,d,j)).join("")}</div>
 ${minHtml(s.min,k)}
 ${promoHtml(s.promo,k,anchor)}
 <div class="field"><span class="lbl">📷 Fotos de este servicio</span>${uploaderHtml(k,"photo",s.photos,s.photos.length>0)}</div>`:''}
 </div>`;}).join("");
 FLASH=null;
 list.querySelectorAll(".box").forEach(el=>{const i=+el.dataset.i,s=S.services[i],k="s"+i,redraw=()=>{syncSubs(s);const y=scrollY;drawServices();scrollTo({top:y});},cat=catOf(s.cat);
  const on=(sel,f)=>el.querySelectorAll(sel).forEach(x=>x.onclick=ev=>{f(x,ev);redraw();changed();});
  el.querySelectorAll(".cat").forEach(t=>t.onclick=()=>{const c=t.dataset.c;const o=S.services.findIndex((y,ii)=>ii!==i&&y.cat===c);
   if(o>=0){S.services.splice(i,1);goBox(o>i?o-1:o,"Ya tenías esta categoría; aquí está.");return;}
   s.cat=c;s.ways={full:false,staff:false,rent:false};s.offers=[];s.staff=[];s.rent=[];const cc=catOf(c);if(cc&&!(cc.staff||[]).length&&!(cc.rent||[]).length)s.ways.full=true;redraw();changed();});
  const chc=el.querySelector(".ch-cat");if(chc)chc.onclick=()=>{s.cat="";redraw();changed();};
  on(".way",x=>{const w=x.dataset.w;s.ways[w]=!s.ways[w];if(s.ways[w])s.open=w==="full"?(s.offers.length?"f0":""):w==="staff"?"st":"rt";});
  on(".of-c",x=>{const n=x.dataset.n,j=s.offers.findIndex(o=>o.n===n);if(j>=0){s.offers.splice(j,1);s.open="";}else addOffer(s,n);});
  el.querySelectorAll(".of-new,.st-new,.rt-new").forEach(b=>b.onclick=()=>{const r=b.closest(".field,.dlc").querySelector(".newrow");r.hidden=false;r.querySelector("input").focus();});
  const addNew=(inp,f)=>{const v=(inp.value||"").trim();if(!v)return;NEW_SUBS.add(v);hqvTrack("catalogo_propuesta",{tipo:"servicio",cat:s.cat,valor:v});f(v);redraw();changed();};
  [[".of-in",".of-addb",v=>addOffer(s,v)],[".st-in",".st-addb",v=>addPerson(s,"staff",v,"Por hora")],[".rt-in",".rt-addb",v=>addPerson(s,"rent",v,"Por pieza")]].forEach(([iq,bq,f])=>{const inp=el.querySelector(iq),b=el.querySelector(bq);if(!inp)return;b.onclick=()=>addNew(inp,f);inp.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();addNew(inp,f);}};});
  on(".of-open",x=>{s.open="f"+x.closest(".ofc").dataset.j;});on(".st-open",()=>{s.open="st";});on(".rt-open",()=>{s.open="rt";});on(".of-ok",()=>{s.open="";});
  on(".st-c",x=>{const n=x.dataset.n,j=s.staff.findIndex(r=>r.n===n);if(j>=0)s.staff.splice(j,1);else s.staff.push({n,price:"",u:"Por hora",min:"5"});});
  on(".rt-c",x=>{const n=x.dataset.n,j=s.rent.findIndex(r=>r.n===n);if(j>=0)s.rent.splice(j,1);else s.rent.push({n,price:"",u:"Por pieza",min:""});});
  el.querySelectorAll(".st-r,.rt-r").forEach(R=>{const r=(R.classList.contains("st-r")?s.staff:s.rent)[+R.dataset.ri];R.querySelector(".sr-p").oninput=e=>{r.price=e.target.value;syncSubs(s);changed();};R.querySelector(".sr-u").onchange=e=>{r.u=e.target.value;redraw();changed();};const m=R.querySelector(".sr-m");if(m)m.oninput=e=>{r.min=e.target.value;changed();};});
  el.querySelectorAll(".ofc.open[data-j]").forEach(C=>{const o=s.offers[+C.dataset.j];if(!o)return;const q=(sel,f)=>C.querySelectorAll(sel).forEach(f);
   q(".of-x",b=>b.onclick=()=>{s.offers.splice(+C.dataset.j,1);s.open="";redraw();changed();});
   q(".of-g",b=>b.onclick=()=>{const g=b.dataset.g;o.gas=o.gas.includes(g)?o.gas.filter(x=>x!==g):[...o.gas,g];b.setAttribute("aria-pressed",o.gas.includes(g));changed();});
   q(".of-ds",b=>b.onclick=()=>{const g=b.dataset.v;o.dserv=o.dserv.includes(g)?o.dserv.filter(x=>x!==g):[...o.dserv,g];b.setAttribute("aria-pressed",o.dserv.includes(g));changed();});
   q(".of-dr",b=>b.onclick=()=>{const g=b.dataset.v;o.drinks=o.drinks.includes(g)?o.drinks.filter(x=>x!==g):[...o.drinks,g];b.setAttribute("aria-pressed",o.drinks.includes(g));changed();});
   q(".of-dv",x=>x.oninput=e=>{o.dvar=e.target.value;changed();});
   q(".tmr",R=>{const t=o.tiempos[+R.dataset.ti];R.querySelector(".t-n").oninput=e=>{t.n=e.target.value;changed();};R.querySelector(".t-d").oninput=e=>{t.d=e.target.value;changed();};
    R.querySelectorAll(".sd button").forEach(b=>b.onclick=()=>{t.k=b.dataset.k;redraw();});R.querySelector(".t-x").onclick=()=>{o.tiempos.splice(+R.dataset.ti,1);redraw();changed();};});
   q(".t-add",b=>b.onclick=()=>{const n=o.tiempos.length+1;o.tiempos.push({n:o.n==="Banquete"?`Tiempo ${n}`:o.n==="Coffee break"?`Bocadillo ${n}`:`Variedad ${n}`,k:o.n==="Mesa de postres y pastel"?"Dulce":"Salado",d:""});redraw();});
   q(".incr",R=>{const L=R.classList.contains("ex")?o.ext:o.inc,r=L[+R.dataset.ri];[["r-q","q"],["r-u","u"],["r-w","w"],["r-cost","cost"]].forEach(([c,f])=>{const x=R.querySelector("."+c);if(x)x.oninput=e=>{r[f]=e.target.value;syncSubs(s);changed();};});R.querySelector(".r-x").onclick=()=>{L.splice(+R.dataset.ri,1);redraw();changed();};});
   q(".r-add",b=>b.onclick=()=>{(b.dataset.l==="ex"?o.ext:o.inc).push(b.dataset.l==="ex"?{q:"1",u:"",w:"",cost:""}:{q:"",u:"",w:""});redraw();setTimeout(()=>{const l=[...document.querySelectorAll(`.box[data-i="${i}"] .ofc.open .incr.${b.dataset.l} .r-u`)].pop();l&&l.focus();},0);});
   q(".of-dur",x=>x.oninput=e=>{o.dur=e.target.value;changed();});q(".of-duru",x=>x.onchange=e=>{o.durU=e.target.value;changed();});
   q(".tarr",R=>{const t=o.tar[+R.dataset.ti],hv=()=>{const h=R.querySelector(".ta-hv");if(h)h.innerHTML=offerHost(o,t,s.cat);};
    R.querySelector(".ta-p").oninput=e=>{t.price=e.target.value;hv();syncSubs(s);changed();};R.querySelector(".ta-u").onchange=e=>{t.u=e.target.value;redraw();changed();};
    const uo=R.querySelector(".ta-uo");if(uo){uo.oninput=e=>{t.uo=e.target.value;changed();};uo.onchange=()=>{const cu=canonUnit(t.uo);if(cu){t.u=cu;t.uo="";if(!U_FULL.includes(cu))U_FULL.push(cu);redraw();}else NEW_UNITS.add(t.uo);};}
    const a=R.querySelector(".ta-a");if(a)a.oninput=e=>{t.alc=e.target.value;hv();syncSubs(s);changed();};const x=R.querySelector(".ta-x");if(x)x.onclick=()=>{o.tar.splice(+R.dataset.ti,1);redraw();changed();};});
   q(".ta-add",b=>b.onclick=()=>{o.tar.push({price:"",u:"Por evento",uo:"",alc:""});redraw();});});
  const d=$("d-"+k);if(d)d.oninput=e=>{s.desc=e.target.value;s.descEdited=true;changed();};
  bindDl(s,k,el,redraw);
  if(cat&&((s.ways.full&&s.offers.length)||(s.ways.staff&&s.staff.length)||(s.ways.rent&&s.rent.length))){bindMin(s.min,k,redraw);bindPromo(s.promo,k,redraw);bindUploader(k,"photo",s.photos,redraw);}
  const rm=el.querySelector(".rm-svc");if(rm)rm.onclick=()=>{S.services.splice(i,1);drawServices();changed();};});}
function drawSvcStep(){const sc=S.svcScope=S.svcScope||{S:false,E:false};
 $("stepBody").innerHTML=`<div class="panel"><span class="crumb">Mi negocio › Servicios</span><h2>Mis servicios 🎉</h2><p class="sub">Pon el precio como tú lo cobras. Nosotros se lo mostramos al anfitrión por persona y en total.</p>
 <div class="svc-top">
  <div class="field"><span class="lbl">¿Para qué tipo de eventos? <span class="opt">Puedes elegir los dos</span></span><div class="chips${MISS(sc.S||sc.E)}" style="width:fit-content;border-radius:99px"><button type="button" class="chip scp" data-v="S" aria-pressed="${!!sc.S}">${TICK}🎉 Sociales</button><button type="button" class="chip scp" data-v="E" aria-pressed="${!!sc.E}">${TICK}💼 Empresariales</button></div></div>
  <div class="field qwrap"><label class="lbl" for="svcQ">🔎 Busca lo que ofreces <span class="opt">o elige abajo por categoría</span></label><input type="search" id="svcQ" autocomplete="off" placeholder="Ej. banquete, tacos al pastor, DJ, meseros, sillas…"><div id="svcQr" class="qres" hidden></div></div>
 </div>
 <div id="svcList" style="display:grid;gap:14px"></div><button type="button" class="btn ghost" id="addSvc">+ Agregar otra categoría</button>
 ${priceBoxHtml()}
 ${zonesHtml(S.svcZones,"svc","¿Dónde das estos servicios?")}${VIATICOS}${navHtml()}</div>`;
 document.querySelectorAll(".scp").forEach(c=>c.onclick=()=>{sc[c.dataset.v]=!sc[c.dataset.v];drawSvcStep();changed();});
 const q=$("svcQ"),qr=$("svcQr"),WE={full:"🎁",staff:"🙋",rent:"📦"},WT={full:"servicio completo",staff:"staff",rent:"renta"};
 const search=()=>{const v=norm(q.value).trim();if(v.length<2){qr.hidden=true;return;}const toks=v.split(/\s+/),res=[];
  CAT2.forEach(c=>{if(!scopeOk(c.t))return;[["full",c.full],["staff",c.staff],["rent",c.rent]].forEach(([w,l])=>l.forEach(n=>{const h=norm(n+" "+c.n);if(toks.every(t=>h.includes(t)))res.push({c,n,w,r:norm(n).startsWith(v)?0:1});}));});
  if(res.length<6)["Salado","Dulce"].forEach(kd=>DISH_LIST[kd].forEach(d=>{if(res.length<8&&toks.every(t=>norm(d).includes(t)))res.push({c:CAT2[0],n:kd==="Dulce"?"Mesa de postres y pastel":"Estación",w:"full",r:2,dish:d});}));
  res.sort((a,b)=>a.r-b.r);
  qr.innerHTML=res.slice(0,8).map((x,ix)=>`<button type="button" data-ix="${ix}"><span>${x.c.e}</span><span><b>${esc(x.dish||x.n)}</b> <small>· ${esc(x.c.n)} · ${WE[x.w]} ${x.dish?esc(x.n.toLowerCase()):WT[x.w]}</small></span></button>`).join("")
   ||`<span class="hint" style="padding:8px">No lo encontramos. Elige la categoría más cercana y usa <b>✏️ Otro</b>: lo sumamos solito al catálogo.</span>`;
  qr.hidden=false;qr.querySelectorAll("button").forEach(btn=>btn.onclick=()=>{const x=res[+btn.dataset.ix],i=boxFor(x.c.n),s=S.services[i];
   if(x.w==="full"){addOffer(s,x.n);if(x.dish){const o=s.offers[+s.open.slice(1)],t=o.tiempos.find(t=>!filled(t.d));if(t)t.d=x.dish;else o.tiempos.push({n:`Variedad ${o.tiempos.length+1}`,k:"Salado",d:x.dish});}}
   else addPerson(s,x.w==="staff"?"staff":"rent",x.n,x.w==="staff"?"Por hora":"Por pieza");
   syncSubs(s);q.value="";qr.hidden=true;hqvTrack("servicio_buscado",{sub:x.n});goBox(i);});};
 q.oninput=search;q.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();const f=qr.querySelector("button");f&&f.click();}if(e.key==="Escape"){qr.hidden=true;}};
 drawServices();$("addSvc").onclick=()=>{S.services.push(blankSvc());drawServices();changed();const l=$("svcList").lastElementChild;l&&l.scrollIntoView({behavior:"smooth",block:"start"});};
 bindPriceBox(drawSvcStep);bindZones(S.svcZones,"svc",drawSvcStep);bindNav();}
