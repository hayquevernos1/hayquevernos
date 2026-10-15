/* ===== v16 · Servicios (Diego, 14 oct 2026 noche) =====
   · Todas las categorías para eventos sociales y empresariales (el tipo solo ordena).
   · «¿Cómo trabajas?» en 3 tarjetas y cada servicio cobra por separado según la modalidad.
   · Catering: Alimentos (tu cocina una sola vez + formatos como etiquetas) y Bebidas (cómo las sirves).
   · Arma tu menú: banquete por tiempos (una línea + agregar); los demás por segmentos Salado / Dulce;
     bebidas Con alcohol / Sin alcohol con switch Frío / Caliente. Escritura predictiva sin menús desplegables.
   · «¿Qué incluye?» y extras: primero el concepto, luego cantidad y unidad; atajos para agregar lo típico.
   · Fotos por ficha. Paquetes al final con precio sugerido editable. */
const WAYS=[["full","🎁","Servicio completo","Llevo todo: equipo, insumos y personal"],["staff","🙋","Solo mi talento","Voy yo o mi equipo; el equipo o los insumos los pone el cliente"],["rent","📦","Solo renta","Rento el equipo o los artículos, sin operarlos"]];
const WAY_TAR={full:"🎁 Servicio completo",staff:"🙋 Solo mi talento (con equipo o insumos del cliente)",rent:"📦 Solo renta / entrega, sin personal"};
const FOOD_FMT=["Banquete","Buffet","Cóctel","Estación de especialidad","Box lunch","Productos individuales"];
const DRINK_FMT=[...C2.bebidasServicio];
const FMT_EMO={"Banquete":"🍽️","Buffet":"🥘","Cóctel":"🍢","Estación de especialidad":"🌮","Box lunch":"🥡","Productos individuales":"🧁","Barra":"🍹","Estación":"🥤","Mesa":"🧊","Carrito":"🛒","Dispensador":"🚰","Barril":"🛢️"};
const MONTHS=[["ene","Ene"],["feb","Feb"],["mar","Mar"],["abr","Abr"],["may","May"],["jun","Jun"],["jul","Jul"],["ago","Ago"],["sep","Sep"],["oct","Oct"],["nov","Nov"],["dic","Dic"]];
const HIGH_STD=["may","jun","oct","nov","dic"];
const GASTROS=[...new Set([...Object.keys(C2.cocina.Salado),...Object.keys(C2.cocina.Dulce)])];
const U_FULL=["Por persona","Por evento","Por paquete","Por pieza","Por hora","Por caja","Por kilo","Por litro","Por mesa","Por docena (12 piezas)","Por ciento (100 piezas)","Por estación","Por día","Por menú"];
const U_STAFF=[["Por hora","por hora"],["Por turno","por turno (5 h)"],["Por evento","por evento"],["Por día","por día"]];
const U_RENT=[["Por pieza","por pieza"],["Por juego","por juego"],["Por evento","por evento"],["Por día","por día"]];
const DISH_LIST={};["Salado","Dulce"].forEach(k=>{const s=new Set();Object.values(C2.cocina[k]).forEach(g=>Object.entries(g).forEach(([e,ps])=>{s.add(e);ps.forEach(p=>s.add(p));}));DISH_LIST[k]=[...s].sort((a,b)=>a.localeCompare(b,"es"));});
const DRINK_VARS=[...new Set(C2.bebidas.flatMap(b=>b.v))].sort((a,b)=>a.localeCompare(b,"es"));
const DRINKS_BY={"Con alcohol":[],"Sin alcohol":[]};C2.bebidas.forEach(b=>b.alc.forEach(a=>{(DRINKS_BY[a]=DRINKS_BY[a]||[]).push(...b.v);}));
Object.keys(DRINKS_BY).forEach(k=>DRINKS_BY[k]=[...new Set(DRINKS_BY[k])].sort((a,b)=>a.localeCompare(b,"es")));
const QUICK={food:["Platos","Cubiertos","Servilletas","Vasos y copas","Mantelería","Meseros","Montaje y desmontaje"],drink:["Barra","Bartender","Hielo","Vasos y copas","Popotes","Mezcladores"],gen:["Montaje y desmontaje","Traslado","Personal","Equipo"]};
const QUICK_EX={food:["Hora extra de servicio","Pastel","Mesa de postres","Mesero extra","Bocadillos extra"],drink:["Hora extra de barra","Bartender extra","Botella extra","Coctel de autor"],gen:["Hora extra","Personal extra","Equipo extra"]};
const INC_SUGG=[...new Set([...QUICK.food,...QUICK.drink,...QUICK.gen,...QUICK_EX.food,...QUICK_EX.drink,...QUICK_EX.gen,"Capitán de meseros","Cocinero","Chafers","Charolas","Loza","Cristalería","Mesa de servicio","Decoración de mesa","Limpieza","Mantel","Cubremantel","Sillas","Mesas","Pantalla","Micrófono","Bocinas","Luces","Fotos digitales","Álbum impreso","Horas de servicio"])];
const UNIT_SUGG=["piezas","personas","kilos","litros","horas","cajas","juegos","charolas","mesas","porciones","paquetes","metros","por cada 10 invitados","por cada 15 invitados","por cada 25 invitados"];
const isCat=s=>s.cat==="Catering";
function newRow(c){return{c:c||"",q:"",u:""};}
function blankOffer(n,kind){return{n,kind:kind||"gen",inc:[],dur:kind==="gen"?"":"5",durU:"horas",tar:[],ext:[],photos:[],
 tiempos:n==="Banquete"?[{n:"",k:"Salado",d:""}]:[],sal:kind==="food"&&n!=="Banquete"?[{d:""}]:[],dul:kind==="food"&&n!=="Banquete"?[{d:""}]:[],con:kind==="drink"?[{d:"",t:"Frío"}]:[],sin:kind==="drink"?[{d:"",t:"Frío"}]:[]};}
function svcDefaults(s){if(!s.ways)s.ways={full:false,staff:false,rent:false};if(!s.offers)s.offers=[];if(!s.staff)s.staff=[];if(!s.rent)s.rent=[];if(s.open===undefined)s.open="";if(s.descEdited===undefined)s.descEdited=filled(s.desc);
 if(!s.cater)s.cater={food:false,drink:false,gas:[]};
 s.offers.forEach(o=>{if(!o.photos)o.photos=[];if(!o.kind)o.kind="gen";["inc","ext"].forEach(L=>{o[L]=o[L]||[];o[L].forEach(r=>{if(r.c===undefined){r.c=r.u||r.w||"";r.u=r.w&&r.u?r.w:"";delete r.w;}});});o.tar=o.tar||[];o.tar.forEach(t=>{if(!t.w)t.w="full";if(!t.u)t.u="Por persona";if(t.uo===undefined)t.uo="";if(t.alc===undefined)t.alc="";});});}
function waysOn(s){return WAYS.map(w=>w[0]).filter(w=>s.ways[w]);}
function tarUnitLabel(t){return t.u==="__otra"?(t.uo?"por "+t.uo.replace(/^por\s+/i,""):"otra unidad"):uLabel(t.u);}
function syncSubs(s){svcDefaults(s);const L=[];
 s.offers.forEach(o=>o.tar.forEach(t=>{if(t.u&&s.ways[t.w])L.push({n:o.n,u:t.u,uo:t.uo||"",price:t.price,yieldP:t.alc||"",pkgP:t.alc||"",pkgH:o.dur||"",unit:tarUnitLabel(t),modo:t.w});}));
 if(s.ways.staff)s.staff.forEach(r=>L.push({n:r.n,u:r.u,uo:"",price:r.price,yieldP:"",pkgP:"",pkgH:r.min||"",unit:uLabel(r.u),modo:"staff"}));
 if(s.ways.rent)s.rent.forEach(r=>L.push({n:r.n,u:r.u,uo:"",price:r.price,yieldP:"",pkgP:"",pkgH:"",unit:uLabel(r.u),modo:"rent"}));
 s.subs=L;if(!s.descEdited)s.desc=autoDesc(s);}
function joinY(a){a=a.filter(Boolean);return a.length<2?a.join(""):a.slice(0,-1).join(", ")+" y "+a[a.length-1];}
function autoDesc(s){const p=[];if(s.offers.length)p.push(joinY(s.offers.map(o=>o.kind==="drink"?"bebidas en "+o.n.toLowerCase():o.n.toLowerCase())));if(s.ways.staff&&s.staff.length)p.push(joinY(s.staff.map(r=>r.n.toLowerCase())));if(s.ways.rent&&s.rent.length)p.push("renta de "+joinY(s.rent.map(r=>r.n.toLowerCase())));
 if(!p.length)return"";const g=isCat(s)&&s.cater.gas.length?` de cocina ${joinY(s.cater.gas.map(x=>x.toLowerCase()))}`:"";const t=joinY(p);return t.charAt(0).toUpperCase()+t.slice(1)+g+" para tu fiesta.";}
function rowsText(L){return L.filter(r=>filled(r.c)).map(r=>[r.c,filled(r.q)?r.q+(filled(r.u)?" "+r.u:""):""].filter(Boolean).join(" ")).join(" · ");}
function menuText(o){if(o.n==="Banquete")return o.tiempos.filter(t=>filled(t.d)).map((t,i)=>(t.n||`Tiempo ${i+1}`)+": "+t.d).join(" · ");
 if(o.kind==="drink")return[...o.con,...o.sin].filter(x=>filled(x.d)).map(x=>x.d).join(", ");
 return[...o.sal,...o.dul].filter(x=>filled(x.d)).map(x=>x.d).join(", ");}
const VAR=()=>+S.svcVar||0,HIGH=()=>S.svcHigh&&+S.svcHigh.pct>0?+S.svcHigh.pct:0;
function costAt(o,t,cat,g){const r=hqvCost({cat,sub:o.n,u:t.u,price:+t.price,guests:g,hours:+o.dur||EXH,rinde:t.alc,pkgP:t.alc});return r;}
function offerHost(o,t,cat){if(!(+t.price>0))return"";
 if(t.u==="__otra")return`<span class="hv">👀 Unidad nueva: el anfitrión la verá tal cual y tú le confirmas el total.</span>`;
 const r=costAt(o,t,cat,EXG);if(r.pend)return`<span class="hv">👀 Dinos para cuántas personas alcanza y lo convertimos; si no, el anfitrión lo verá «por cotizar».</span>`;
 const pp=Math.round(r.total/EXG),v=VAR(),h=HIGH();
 return`<span class="hv">👀 En una fiesta de ${EXG} personas: <b>${money(pp)}</b> por persona · <b>${money(Math.round(r.total))}</b> en total${v?` <span class="pm">± ${v}%</span>`:""}${h?` · temporada alta ${money(Math.round(r.total*(1+h/100)))}`:""}</span>`;}
function offerOk(o,s){const T=o.tar.filter(t=>s.ways[t.w]);return T.some(t=>filled(t.price))&&T.every(t=>!filled(t.price)||(t.u&&(t.u!=="__otra"||filled(t.uo))))&&o.ext.every(e=>!filled(e.c)||filled(e.cost));}
function staffOk(r){return filled(r.price)&&!!r.u;}
function offerSummary(o,s){const t=o.tar.find(x=>filled(x.price)&&s.ways[x.w]);return[menuText(o)||rowsText(o.inc),t?`${money(t.price)} ${tarUnitLabel(t)}`:""].filter(Boolean).join(" · ");}
/* filas de concepto → cantidad → unidad (incluye y extras) */
function rowsHtml(o,cost){const L=cost?o.ext:o.inc,cls=cost?"ex":"in",kind=o.kind,used=L.map(r=>r.c);
 const quick=((cost?QUICK_EX:QUICK)[kind]||(cost?QUICK_EX:QUICK).gen).filter(x=>!used.includes(x));
 return`${quick.length?`<div class="qk">${quick.map(x=>`<button type="button" class="qkb" data-l="${cls}" data-c="${esc(x)}">＋ ${esc(x)}</button>`).join("")}</div>`:""}
 ${L.map((r,ri)=>`<div class="incr ${cls}" data-ri="${ri}"><input type="text" class="r-c" data-sg="inc" value="${esc(r.c)}" placeholder="${cost?"¿Qué extra? Ej. pastel, hora extra":"¿Qué incluye? Ej. servilletas"}" aria-label="Concepto" autocomplete="off"><input type="number" inputmode="decimal" class="r-q" value="${esc(r.q)}" placeholder="#" aria-label="Cantidad"><input type="text" class="r-u" data-sg="u" value="${esc(r.u)}" placeholder="unidad" aria-label="Unidad" autocomplete="off">${cost?`<label class="r-m"><span>$</span><input type="number" min="0" class="r-cost${MISS(!filled(r.c)||filled(r.cost))}" value="${esc(r.cost)}" aria-label="Costo del extra"></label>`:""}<button type="button" class="link bad r-x" aria-label="Quitar renglón">✕</button></div>`).join("")}
 <button type="button" class="link r-add" data-l="${cls}" style="justify-self:start">+ ${cost?"Agregar extra":"Agregar otro"}</button>`;}
function menuHtml(o){
 if(o.n==="Banquete")return`<span class="mini-l">🍴 Arma tu menú por tiempos <span class="opt">(opcional)</span></span>
  ${o.tiempos.map((t,ti)=>`<div class="tmr" data-ti="${ti}"><input type="text" class="t-n" value="${esc(t.n)}" placeholder="${["Entrada","Plato fuerte","Postre"][ti]||`Tiempo ${ti+1}`}" aria-label="Nombre del tiempo"><div class="sw sd" role="group"><button type="button" data-k="Salado" aria-pressed="${t.k==="Salado"}">Salado</button><button type="button" data-k="Dulce" aria-pressed="${t.k==="Dulce"}">Dulce</button></div><input type="text" class="t-d" data-sg="${t.k}" value="${esc(t.d)}" placeholder="¿Qué sirves?" aria-label="Platillo" autocomplete="off"><button type="button" class="link bad t-x" aria-label="Quitar tiempo">✕</button></div>`).join("")}
  <button type="button" class="link t-add" style="justify-self:start">+ Agregar tiempo</button>`;
 const seg=(key,tit,sg)=>`<div class="seg2"><b>${tit}</b>${o[key].map((x,xi)=>`<div class="mr" data-k="${key}" data-xi="${xi}">${o.kind==="drink"?`<div class="sw" role="group"><button type="button" data-t="Frío" aria-pressed="${x.t==="Frío"}">Frío</button><button type="button" data-t="Caliente" aria-pressed="${x.t==="Caliente"}">Caliente</button></div>`:""}<input type="text" class="m-d" data-sg="${sg}" value="${esc(x.d)}" placeholder="¿Qué sirves?" aria-label="Qué sirves" autocomplete="off"><button type="button" class="link bad m-x" aria-label="Quitar">✕</button></div>`).join("")}<button type="button" class="link m-add" data-k="${key}" style="justify-self:start">+ Agregar</button></div>`;
 if(o.kind==="drink")return`<span class="mini-l">🍹 Arma tu menú de bebidas <span class="opt">(opcional)</span></span>${seg("con","🍸 Con alcohol","Con alcohol")}${seg("sin","🧃 Sin alcohol","Sin alcohol")}`;
 if(o.kind==="food")return`<span class="mini-l">🍴 Arma tu menú <span class="opt">(opcional)</span></span>${seg("sal","🧂 Salado","Salado")}${seg("dul","🍰 Dulce","Dulce")}`;
 return"";}
function offerCard(s,k,o,j,cat){const open=s.open==="f"+j,ok=offerOk(o,s),emo=FMT_EMO[o.n]||(o.kind==="drink"?"🍹":"✨"),kj=`${k}o${j}`;
 if(!open)return`<div class="dlc closed ofc${MISS(ok)}" data-j="${j}"><button type="button" class="dlh of-open"><b>${emo}</b><span class="sm"><b style="color:#1a1033">${esc(o.kind==="drink"?"Bebidas · "+o.n:o.n)}</b> · ${esc(offerSummary(o,s)||"falta tu precio")}</span><span class="ed">${ok?"✏️ Editar":"⚠️ Completar"}</span></button></div>`;
 const hasPrice=o.tar.some(t=>filled(t.price));
 return`<div class="dlc open ofc${MISS(ok)}" data-j="${j}">
  <div class="dlh"><b>${emo} ${esc(o.kind==="drink"?"Bebidas · "+o.n:o.n)}</b><span class="sm"></span><button type="button" class="link bad of-x" aria-label="Quitar ${esc(o.n)}">✕ Quitar</button></div>
  ${menuHtml(o)}
  <span class="mini-l">✅ ¿Qué incluye? <span class="opt">Ya va dentro de tu precio · toca para agregar</span></span>
  ${rowsHtml(o,false)}
  <div class="durr"><span class="mini-l" style="margin:0">⏱️ Duración del servicio</span><input type="number" min="0" step="any" class="of-dur" value="${esc(o.dur)}" placeholder="—" aria-label="Duración"><select class="of-duru" aria-label="Unidad de duración">${["minutos","horas","días"].map(u=>`<option ${o.durU===u?"selected":""}>${u}</option>`).join("")}</select></div>
  <span class="mini-l">💲 Tarifa <span class="opt">${waysOn(s).length>1?"una por cada forma en que trabajas":"¿cobras de varias formas? agrega otra"}</span></span>
  ${waysOn(s).map(w=>{const T=o.tar.map((t,ti)=>[t,ti]).filter(([t])=>t.w===w);return`<div class="tgrp"><b class="tw">${WAY_TAR[w]}</b>
   ${T.map(([t,ti])=>`<div class="tarr" data-ti="${ti}"><label class="sl-p"><span>$</span><input type="number" min="0" step="any" class="ta-p" value="${esc(t.price)}" placeholder="precio" aria-label="Precio"></label>
    <select class="ta-u" aria-label="Cómo lo cobras">${U_FULL.map(u=>`<option value="${esc(u)}" ${t.u===u?"selected":""}>${esc(uLabel(u))}</option>`).join("")}<option value="__otra" ${t.u==="__otra"?"selected":""}>✏️ otra unidad…</option></select>
    ${t.u==="__otra"?`<input type="text" class="ta-uo${MISS(filled(t.uo))}" data-sg="u" value="${esc(t.uo)}" placeholder="por charola, por metro…" aria-label="Otra unidad" autocomplete="off">`:""}
    ${t.u!=="Por persona"?`<label class="ta-al">alcanza para <input type="number" min="0" class="ta-a" value="${esc(t.alc)}" placeholder="#" aria-label="Alcanza para cuántas personas"> personas</label>`:""}
    ${T.length>1?`<button type="button" class="link bad ta-x" aria-label="Quitar tarifa">✕</button>`:""}<div class="ta-hv">${offerHost(o,t,s.cat)}</div></div>`).join("")}
   <button type="button" class="link ta-add" data-w="${w}" style="justify-self:start">+ Otra tarifa</button></div>`;}).join("")}
  ${hasPrice?`<span class="mini-l">➕ Extras <span class="opt">(opcional · lo que el anfitrión puede sumar con costo)</span></span>${rowsHtml(o,true)}
  <span class="mini-l">📷 Fotos de ${esc(o.n.toLowerCase())} <span class="opt">(opcional)</span></span>${uploaderHtml(kj,"photo",o.photos,true)}`:`<span class="hint">Pon al menos un precio y te mostramos extras y fotos.</span>`}
  ${ok?`<button type="button" class="btn cta sm dl-ok of-ok">Listo ✓</button>`:""}</div>`;}
function listCard(s,k,cat,list){const st=list==="staff",open=s.open===(st?"st":"rt"),L=s[list],ok=L.length&&L.every(staffOk);
 const head=st?"🙋 Staff":"📦 Renta";
 if(!open)return`<div class="dlc closed ofc${MISS(ok)}"><button type="button" class="dlh ${st?"st":"rt"}-open"><b>${st?"🙋":"📦"}</b><span class="sm"><b style="color:#1a1033">${st?"Staff":"Renta"}</b> · ${esc(L.map(r=>r.n+(filled(r.price)?` ${money(r.price)} ${uLabel(r.u)}`:"")).join(" · ")||(st?"elige tus perfiles":"elige lo que rentas"))}</span><span class="ed">${ok?"✏️ Editar":"⚠️ Completar"}</span></button></div>`;
 const names=[...new Set([...(cat?cat[list]:[]),...L.map(r=>r.n)])],U=st?U_STAFF:U_RENT;
 return`<div class="dlc open ofc${MISS(ok)}"><div class="dlh"><b>${st?"🙋 Staff que ofreces":"📦 ¿Qué rentas?"}</b><span class="sm"></span></div>
  <span class="hint">${st?"Personal que va a trabajar con el equipo o los insumos del cliente.":"Artículos o equipo que rentas, sin operarlos."}</span>
  <div class="chips cmini">${names.map(n=>`<button type="button" class="chip ${st?"st":"rt"}-c" data-n="${esc(n)}" aria-pressed="${L.some(r=>r.n===n)}">${TICK}${esc(n)}</button>`).join("")}<button type="button" class="chip new ${st?"st":"rt"}-new">✏️ Otro</button></div>
  <div class="newrow" hidden><input type="text" class="${st?"st":"rt"}-in" data-sg="${st?"staff":"full"}" placeholder="${st?"Ej. Taquero, Bartender…":"Ej. Pista de baile iluminada"}" aria-label="Otro" autocomplete="off"><button type="button" class="btn sm ${st?"st":"rt"}-addb">Agregar</button></div>
  ${L.map((r,ri)=>`<div class="tarr ${st?"st":"rt"}-r" data-ri="${ri}"><b class="rn">${esc(r.n)}</b><label class="sl-p"><span>$</span><input type="number" min="0" class="sr-p${MISS(filled(r.price))}" value="${esc(r.price)}" placeholder="precio" aria-label="Precio de ${esc(r.n)}"></label><select class="sr-u" aria-label="Cómo lo cobras">${U.map(([u,t])=>`<option value="${u}" ${r.u===u?"selected":""}>${t}${st?" c/u":""}</option>`).join("")}</select>${st&&r.u==="Por hora"?`<label class="ta-al">mínimo <input type="number" min="0" class="sr-m" value="${esc(r.min)}" placeholder="#" aria-label="Horas mínimas"> h</label>`:""}${!st?`<label class="ta-al">tengo <input type="number" min="0" class="sr-m" value="${esc(r.min)}" placeholder="#" aria-label="Cantidad disponible"> disponibles</label>`:""}</div>`).join("")}
  ${ok?`<button type="button" class="btn cta sm dl-ok of-ok">Listo ✓</button>`:""}</div>`;}
function addOffer(s,n,kind){svcDefaults(s);let j=s.offers.findIndex(o=>o.n===n&&o.kind===(kind||"gen"));if(j<0){const o=blankOffer(n,kind||"gen");waysOn(s).forEach(w=>{if(w!=="staff"||!isCat(s)||true)o.tar.push({w,price:"",u:kind==="food"||kind==="drink"?"Por persona":"Por evento",uo:"",alc:""});});if(!o.tar.length)o.tar.push({w:"full",price:"",u:"Por persona",uo:"",alc:""});s.offers.push(o);j=s.offers.length-1;}s.open="f"+j;}
function addPerson(s,list,n,u){svcDefaults(s);if(!s[list].some(r=>r.n===n))s[list].push({n,price:"",u,min:""});s.ways[list]=true;s.open=list==="staff"?"st":"rt";}
function boxFor(cat){let i=S.services.findIndex(s=>s.cat===cat);if(i<0){i=S.services.findIndex(s=>!s.cat);if(i<0){S.services.push(blankSvc());i=S.services.length-1;}S.services[i].cat=cat;}svcDefaults(S.services[i]);return i;}
function ensureTar(s){s.offers.forEach(o=>waysOn(s).forEach(w=>{if(!o.tar.some(t=>t.w===w))o.tar.push({w,price:"",u:o.tar[0]?o.tar[0].u:"Por persona",uo:"",alc:""});}));}
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
/* ---------- paquetes ---------- */
function pkgItems(){const out=[];S.services.forEach((s,i)=>{svcDefaults(s);if(!catOf(s.cat))return;s.offers.forEach((o,j)=>out.push({key:`o${i}-${j}`,n:(o.kind==="drink"?"Bebidas · ":"")+o.n,s,o}));if(s.ways.staff)s.staff.forEach((r,j)=>out.push({key:`s${i}-${j}`,n:r.n,s,r,st:true}));if(s.ways.rent)s.rent.forEach((r,j)=>out.push({key:`r${i}-${j}`,n:r.n,s,r}));});return out;}
function itemCost(it,g){if(it.o){const t=it.o.tar.find(x=>filled(x.price)&&it.s.ways[x.w]&&x.w==="full")||it.o.tar.find(x=>filled(x.price)&&it.s.ways[x.w]);if(!t)return 0;const r=costAt(it.o,t,it.s.cat,g);return r.pend?0:r.total;}
 const p=+it.r.price||0;return it.st?p*(it.r.u==="Por hora"?(+it.r.min||5):1):p;}
function pkgSuggest(P){const g=+P.alc||EXG,items=pkgItems().filter(it=>P.items.includes(it.key));const tot=items.reduce((a,it)=>a+itemCost(it,g),0);return P.per==="persona"?Math.round(tot/g):Math.round(tot);}
function pkgHtml(){const L=S.svcPkgs,items=pkgItems();if(!items.length)return"";
 return`<div class="field"><span class="lbl">🎁 Arma tus paquetes <span class="opt">(opcional · combina tus servicios con un precio especial)</span></span>
  ${L.map((P,pi)=>{const sug=pkgSuggest(P);return`<div class="pkgc" data-pi="${pi}"><div class="row"><input type="text" class="pk-n${MISS(filled(P.name))}" value="${esc(P.name)}" placeholder="Nombre: Paquete Fiesta Mexicana" aria-label="Nombre del paquete"><button type="button" class="link bad pk-x">✕ Quitar</button></div>
   <span class="mini-l">¿Qué incluye este paquete?</span><div class="chips cmini">${items.map(it=>`<button type="button" class="chip pk-it" data-k="${it.key}" aria-pressed="${P.items.includes(it.key)}">${TICK}${esc(it.n)}</button>`).join("")}</div>
   <div class="tarr"><span class="ta-al">para</span><label class="ta-al"><input type="number" min="1" class="pk-al" value="${esc(P.alc)}" aria-label="Personas"> personas</label><label class="sl-p"><span>$</span><input type="number" min="0" class="pk-p${MISS(filled(P.price))}" value="${esc(P.price)}" placeholder="${sug||"precio"}" aria-label="Precio del paquete"></label><select class="pk-per" aria-label="Cómo se cobra"><option value="evento" ${P.per==="evento"?"selected":""}>por evento</option><option value="persona" ${P.per==="persona"?"selected":""}>por persona</option></select>
    <div class="ta-hv"><span class="hv">💡 Precio sugerido con tus tarifas: <b>${money(sug)}</b> ${P.per==="persona"?"por persona":"por evento"}${filled(P.price)&&+P.price<sug?` · ahorro para tu cliente <b>${money(sug-+P.price)}</b>`:""} <button type="button" class="link pk-use">Usar sugerido</button></span></div></div>
   <span class="mini-l">📷 Fotos del paquete <span class="opt">(opcional)</span></span>${uploaderHtml("pk"+pi,"photo",P.photos,true)}</div>`;}).join("")}
  <button type="button" class="btn ghost sm" id="pkAdd" style="width:fit-content">+ Armar un paquete</button></div>`;}
function bindPkgs(redraw){const a=$("pkAdd");if(a)a.onclick=()=>{S.svcPkgs.push({name:"",items:pkgItems().slice(0,3).map(x=>x.key),alc:"50",price:"",per:"evento",photos:[]});redraw();changed();};
 document.querySelectorAll(".pkgc").forEach(C=>{const P=S.svcPkgs[+C.dataset.pi],q=x=>C.querySelector(x);
  q(".pk-n").oninput=e=>{P.name=e.target.value;changed();};q(".pk-x").onclick=()=>{S.svcPkgs.splice(+C.dataset.pi,1);redraw();changed();};
  C.querySelectorAll(".pk-it").forEach(b=>b.onclick=()=>{const k=b.dataset.k;P.items=P.items.includes(k)?P.items.filter(x=>x!==k):[...P.items,k];redraw();changed();});
  q(".pk-al").onchange=e=>{P.alc=e.target.value;redraw();changed();};q(".pk-p").oninput=e=>{P.price=e.target.value;changed();};q(".pk-per").onchange=e=>{P.per=e.target.value;redraw();changed();};
  q(".pk-use").onclick=()=>{P.price=String(pkgSuggest(P));redraw();changed();};
  bindUploader("pk"+C.dataset.pi,"photo",P.photos,redraw);});}
/* ---------- escritura predictiva (sin menús desplegables) ---------- */
function sgList(k){return k==="Salado"||k==="Dulce"?DISH_LIST[k]:k==="Con alcohol"||k==="Sin alcohol"?DRINKS_BY[k]:k==="inc"?INC_SUGG:k==="u"?UNIT_SUGG:k==="staff"?[...new Set(CAT2.flatMap(c=>c.staff))]:k==="full"?[...new Set(CAT2.flatMap(c=>[...c.full,...c.rent]))]:[];}
(function(){let box=null,cur=null;const hide=()=>{if(box)box.hidden=true;};
 const show=inp=>{const v=norm(inp.value).trim();if(v.length<2){hide();return;}const L=sgList(inp.dataset.sg),res=[];
  for(const x of L){const n=norm(x);if(n.startsWith(v))res.push([0,x]);else if(n.includes(v))res.push([1,x]);if(res.length>40)break;}
  res.sort((a,b)=>a[0]-b[0]);const top=res.slice(0,6).map(r=>r[1]).filter(x=>norm(x)!==v);if(!top.length){hide();return;}
  if(!box){box=document.createElement("div");box.className="sgf";document.body.appendChild(box);}
  box.innerHTML=top.map(x=>`<button type="button">${esc(x)}</button>`).join("");const r=inp.getBoundingClientRect();box.style.left=(r.left+scrollX)+"px";box.style.top=(r.bottom+scrollY+4)+"px";box.style.minWidth=Math.max(180,r.width)+"px";box.hidden=false;cur=inp;
  box.querySelectorAll("button").forEach(b=>b.onmousedown=e=>{e.preventDefault();cur.value=b.textContent;cur.dispatchEvent(new Event("input",{bubbles:true}));cur.dispatchEvent(new Event("change",{bubbles:true}));hide();});};
 document.addEventListener("input",e=>{if(e.target.dataset&&e.target.dataset.sg)show(e.target);});
 document.addEventListener("focusout",e=>{if(e.target.dataset&&e.target.dataset.sg)setTimeout(hide,120);});
 addEventListener("scroll",hide,{passive:true});})();
/* ---------- sitio público ---------- */
function svcPlist(s){svcDefaults(s);const v=+S.svcVar||0,out=[];
 s.offers.forEach(o=>{const t=o.tar.filter(x=>filled(x.price)&&s.ways[x.w]);const multi=new Set(t.map(x=>x.w)).size>1;const m=menuText(o),inc=rowsText(o.inc);
  out.push(`<span class="po"><span class="poh"><b>${FMT_EMO[o.n]||"✨"} ${esc(o.kind==="drink"?"Bebidas · "+o.n:o.n)}</b> <span class="price">${t.length?t.map(x=>`${multi?`<small>${esc(WAY_TAR[x.w].split(" (")[0].replace(/^\S+ /,""))}:</small> `:""}${money(x.price)} <small>${esc(tarUnitLabel(x))}${+x.alc>0?` · ${esc(x.alc)} personas`:""}</small>`).join(" · "):"<small>Por cotizar</small>"}${v&&t.length?` <small class="pmv">± ${v}%</small>`:""}</span></span>${m?`<small class="inc">Menú: ${esc(m)}</small>`:""}${inc?`<small class="inc">Incluye: ${esc(inc)}</small>`:""}${o.ext.some(e=>filled(e.c))?`<small class="inc">Extras: ${esc(o.ext.filter(e=>filled(e.c)).map(e=>rowsText([e])+(filled(e.cost)?" "+money(e.cost):"")).join(" · "))}</small>`:""}${o.photos.length?`<span class="pph">${o.photos.slice(0,4).map(p=>`<img src="${p.url||p}" alt="">`).join("")}</span>`:""}</span>`);});
 if(s.ways.staff&&s.staff.length)out.push(`<span class="po"><span class="poh"><b>🙋 Staff</b> <span class="price">${s.staff.map(r=>`${esc(r.n)} ${filled(r.price)?money(r.price):""} <small>${esc(uLabel(r.u))}</small>`).join(" · ")}</span></span></span>`);
 if(s.ways.rent&&s.rent.length)out.push(`<span class="po"><span class="poh"><b>📦 Renta</b> <span class="price">${s.rent.map(r=>`${esc(r.n)} ${filled(r.price)?money(r.price):""} <small>${esc(uLabel(r.u))}</small>`).join(" · ")}</span></span></span>`);
 return out.join("");}
function pkgSite(){const L=(S.svcPkgs||[]).filter(P=>filled(P.name)&&filled(P.price));if(!L.length)return"";const I=pkgItems();
 return`<div class="ms-item"><div class="ms-item-top"><b>🎁 Paquetes</b></div><div class="plist">${L.map(P=>`<span class="po"><span class="poh"><b>${esc(P.name)}</b><span class="price">${money(P.price)} <small>${P.per==="persona"?"por persona":"por evento"} · ${esc(P.alc)} personas</small></span></span><small class="inc">Incluye: ${esc(I.filter(it=>P.items.includes(it.key)).map(it=>it.n).join(" · "))}</small>${P.photos.length?`<span class="pph">${P.photos.slice(0,4).map(p=>`<img src="${p.url||p}" alt="">`).join("")}</span>`:""}</span>`).join("")}</div></div>`;}
/* ---------- paso de servicios ---------- */
function drawServices(){const list=$("svcList");if(!list)return;const sc=S.svcScope||{};
 list.innerHTML=S.services.map((s,i)=>{svcDefaults(s);const cat=catOf(s.cat),k="s"+i,anchor="s"+(i+1),fl=FLASH&&FLASH.i===i?FLASH.msg:"";
 const order=CAT2.slice().sort((a,b)=>(sc.E&&!sc.S?(["Tecnología","Marketing y comunicación","Exposición y negocios","Registro y protocolo","Permisos y trámites"].includes(a.n)?-1:0)-(["Tecnología","Marketing y comunicación","Exposición y negocios","Registro y protocolo","Permisos y trámites"].includes(b.n)?-1:0):0));
 const ways=s.ways.full||s.ways.staff||s.ways.rent,cater=isCat(s);
 const fulls=cat&&!cater?[...new Set([...(cat.full||[]),...s.offers.map(o=>o.n)])]:[];
 const any=s.offers.length||(s.ways.staff&&s.staff.length)||(s.ways.rent&&s.rent.length);
 const priced=s.offers.some(o=>o.tar.some(t=>filled(t.price)))||(s.ways.staff&&s.staff.some(r=>filled(r.price)))||(s.ways.rent&&s.rent.some(r=>filled(r.price)));
 const foods=s.offers.map((o,j)=>[o,j]).filter(([o])=>o.kind==="food"),drinks=s.offers.map((o,j)=>[o,j]).filter(([o])=>o.kind==="drink"),gens=s.offers.map((o,j)=>[o,j]).filter(([o])=>o.kind==="gen");
 return`<div class="box" data-i="${i}"><div class="box-head"><h3>${cat?cat.e+" "+esc(cat.n):"Ficha "+(i+1)}</h3><span style="display:flex;gap:14px">${cat?`<button type="button" class="link ch-cat">Cambiar categoría</button>`:''}${S.services.length>1?`<button type="button" class="link bad rm-svc">Quitar</button>`:''}</span></div>
 ${fl?`<div class="flash">${esc(fl)}</div>`:''}
 ${!cat?`<div class="field"><span class="lbl">1. Elige tu categoría</span><div class="cats big${MISS(!!cat)}">${order.map(c=>{const used=S.services.some((y,ii)=>ii!==i&&y.cat===c.n);return`<button type="button" class="cat" data-c="${esc(c.n)}" aria-pressed="${s.cat===c.n}"><span class="emo">${c.e}</span><span>${esc(c.n)}${used?' <small>· ya la tienes</small>':''}</span></button>`;}).join("")}</div></div>`:''}
 ${cat?`<div class="field"><span class="lbl">¿Cómo trabajas? <span class="opt">Elige todas las que hagas · cada una tiene su precio</span></span><div class="ways${MISS(ways)}">${WAYS.filter(w=>w[0]==="full"||(cat[w[0]]||[]).length||s.ways[w[0]]).map(([w,e,t,d])=>`<button type="button" class="way" data-w="${w}" aria-pressed="${!!s.ways[w]}"><span class="emo">${e}</span><b>${t}</b><small>${d}</small></button>`).join("")}</div>
  ${s.ways.full?`<div class="fullx">🎁 <b>Servicio completo</b> = ${cater?"🍲 lo que preparas + 🍴 lo que lo acompaña (platos, cubiertos, servilletas…) + 🙋 quien lo sirve":"🛠️ el servicio + 🎛️ tu equipo + 🙋 tu personal"}</div>`:""}</div>
  ${ways&&cater?`<div class="field"><span class="lbl">¿Qué sirves?</span><div class="ways two${MISS(s.cater.food||s.cater.drink)}">${[["food","🍽️","Alimentos"],["drink","🍹","Bebidas"]].map(([x,e,t])=>`<button type="button" class="way ct" data-x="${x}" aria-pressed="${!!s.cater[x]}"><span class="emo">${e}</span><b>${t}</b></button>`).join("")}</div></div>
   ${s.cater.food?`<div class="field sub2"><span class="lbl">🍽️ Alimentos</span>
    <span class="mini-l">🌎 Tu cocina <span class="opt">Aplica a todos tus formatos</span></span><div class="chips cmini">${GASTROS.map(g=>`<button type="button" class="chip gas" data-g="${esc(g)}" aria-pressed="${s.cater.gas.includes(g)}">${TICK}${esc(g)}</button>`).join("")}</div>
    <span class="mini-l">¿En qué formatos lo sirves?</span><div class="chips${MISS(foods.length>0)}" style="border-radius:14px">${FOOD_FMT.map(n=>`<button type="button" class="chip fmt" data-k="food" data-n="${esc(n)}" aria-pressed="${s.offers.some(o=>o.kind==="food"&&o.n===n)}">${TICK}${FMT_EMO[n]} ${esc(n)}</button>`).join("")}<button type="button" class="chip new of-new" data-k="food">✏️ Otro</button></div>
    <div class="newrow" hidden><input type="text" class="of-in" data-k="food" placeholder="¿Cómo se llama tu formato?" aria-label="Otro formato"><button type="button" class="btn sm of-addb">Agregar</button></div>
    ${foods.map(([o,j])=>offerCard(s,k,o,j,cat)).join("")}</div>`:""}
   ${s.cater.drink?`<div class="field sub2"><span class="lbl">🍹 Bebidas</span>
    <span class="mini-l">¿Cómo las sirves?</span><div class="chips${MISS(drinks.length>0)}" style="border-radius:14px">${DRINK_FMT.map(n=>`<button type="button" class="chip fmt" data-k="drink" data-n="${esc(n)}" aria-pressed="${s.offers.some(o=>o.kind==="drink"&&o.n===n)}">${TICK}${FMT_EMO[n]||"🍹"} ${esc(n)}</button>`).join("")}<button type="button" class="chip new of-new" data-k="drink">✏️ Otro</button></div>
    <div class="newrow" hidden><input type="text" class="of-in" data-k="drink" placeholder="¿Cómo las sirves?" aria-label="Otra forma de servir"><button type="button" class="btn sm of-addb">Agregar</button></div>
    ${drinks.map(([o,j])=>offerCard(s,k,o,j,cat)).join("")}</div>`:""}`:""}
  ${ways&&!cater?`<div class="field"><span class="lbl">¿Qué ofreces?</span><div class="chips${MISS(s.offers.length>0||(s.ways.staff&&s.staff.length)||(s.ways.rent&&s.rent.length))}" style="border-radius:14px">${fulls.map(n=>`<button type="button" class="chip fmt" data-k="gen" data-n="${esc(n)}" aria-pressed="${s.offers.some(o=>o.n===n)}">${TICK}${esc(n)}</button>`).join("")}<button type="button" class="chip new of-new" data-k="gen">✏️ Otro</button></div>
   <div class="newrow" hidden><input type="text" class="of-in" data-k="gen" data-sg="full" placeholder="¿Cómo se llama tu servicio?" aria-label="Otro servicio" autocomplete="off"><button type="button" class="btn sm of-addb">Agregar</button></div>
   ${gens.map(([o,j])=>offerCard(s,k,o,j,cat)).join("")}</div>`:""}
  ${s.ways.staff&&(cat.staff||[]).length?`<div class="field">${listCard(s,k,cat,"staff")}</div>`:""}
  ${s.ways.rent&&(cat.rent||[]).length?`<div class="field">${listCard(s,k,cat,"rent")}</div>`:""}`:''}
 ${any&&priced?`<div class="field"><label class="lbl" for="d-${k}">💬 Descríbelo en una frase <span class="opt">${s.descEdited?"":"✨ te la escribimos; cámbiala si quieres"}</span></label><input type="text" id="d-${k}" class="${MISS(filled(s.desc))}" value="${esc(s.desc)}" placeholder="Qué incluye y para cuántas personas"></div>
 <div class="field"><span class="lbl">🚚 ¿Cómo entregas este servicio? <span class="opt">Elige todas las que hagas</span></span>
  <div class="chips dlm-chips${MISS((s.dl||[]).length>0)}" style="border-radius:14px">${DL_MODS.map(([m,e])=>`<button type="button" class="chip dlm" data-m="${esc(m)}" aria-pressed="${(s.dl||[]).some(d=>d.m===m)}">${TICK}${e} ${esc(m)}</button>`).join("")}</div>
  ${(s.dl||[]).map((d,j)=>dlCard(s,k,d,j)).join("")}</div>
 ${minHtml(s.min,k)}
 ${promoHtml(s.promo,k,anchor)}`:any?`<span class="hint">Cuando pongas tus precios te preguntamos cómo lo entregas y lo demás.</span>`:''}
 </div>`;}).join("");
 FLASH=null;
 list.querySelectorAll(".box").forEach(el=>{const i=+el.dataset.i,s=S.services[i],k="s"+i,redraw=()=>{syncSubs(s);const y=scrollY;drawServices();scrollTo({top:y});},cat=catOf(s.cat);
  const on=(sel,f)=>el.querySelectorAll(sel).forEach(x=>x.onclick=ev=>{f(x,ev);redraw();changed();});
  el.querySelectorAll(".cat").forEach(t=>t.onclick=()=>{const c=t.dataset.c;const o=S.services.findIndex((y,ii)=>ii!==i&&y.cat===c);
   if(o>=0){S.services.splice(i,1);goBox(o>i?o-1:o,"Ya tenías esta categoría; aquí está.");return;}
   s.cat=c;s.ways={full:false,staff:false,rent:false};s.offers=[];s.staff=[];s.rent=[];s.cater={food:false,drink:false,gas:[]};redraw();changed();});
  const chc=el.querySelector(".ch-cat");if(chc)chc.onclick=()=>{s.cat="";redraw();changed();};
  on(".way[data-w]",x=>{const w=x.dataset.w;s.ways[w]=!s.ways[w];ensureTar(s);if(s.ways[w]&&w!=="full"&&(cat[w]||[]).length&&!s[w].length)s.open=w==="staff"?"st":"rt";});
  on(".ct",x=>{const c=x.dataset.x;s.cater[c]=!s.cater[c];if(!s.cater[c])s.offers=s.offers.filter(o=>o.kind!==c);});
  el.querySelectorAll(".gas").forEach(b=>b.onclick=()=>{const g=b.dataset.g;s.cater.gas=s.cater.gas.includes(g)?s.cater.gas.filter(x=>x!==g):[...s.cater.gas,g];b.setAttribute("aria-pressed",s.cater.gas.includes(g));if(!s.descEdited){s.desc=autoDesc(s);const d=$("d-"+k);if(d)d.value=s.desc;}changed();});
  on(".fmt",x=>{const n=x.dataset.n,kd=x.dataset.k,j=s.offers.findIndex(o=>o.n===n&&o.kind===kd);if(j>=0){s.offers.splice(j,1);s.open="";}else addOffer(s,n,kd);});
  el.querySelectorAll(".of-new,.st-new,.rt-new").forEach(b=>b.onclick=()=>{const r=b.closest(".field,.dlc").querySelector(".newrow");r.hidden=false;r.querySelector("input").focus();});
  const addNew=(inp,f)=>{const v=(inp.value||"").trim();if(!v)return;NEW_SUBS.add(v);hqvTrack("catalogo_propuesta",{tipo:"servicio",cat:s.cat,valor:v});f(v);redraw();changed();};
  el.querySelectorAll(".of-in").forEach(inp=>{const b=inp.nextElementSibling,f=v=>addOffer(s,v,inp.dataset.k);b.onclick=()=>addNew(inp,f);inp.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();addNew(inp,f);}};});
  [[".st-in",".st-addb",v=>addPerson(s,"staff",v,"Por hora")],[".rt-in",".rt-addb",v=>addPerson(s,"rent",v,"Por pieza")]].forEach(([iq,bq,f])=>{const inp=el.querySelector(iq),b=el.querySelector(bq);if(!inp)return;b.onclick=()=>addNew(inp,f);inp.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();addNew(inp,f);}};});
  on(".of-open",x=>{s.open="f"+x.closest(".ofc").dataset.j;});on(".st-open",()=>{s.open="st";});on(".rt-open",()=>{s.open="rt";});on(".of-ok",()=>{s.open="";});
  on(".st-c",x=>{const n=x.dataset.n,j=s.staff.findIndex(r=>r.n===n);if(j>=0)s.staff.splice(j,1);else s.staff.push({n,price:"",u:"Por hora",min:"5"});});
  on(".rt-c",x=>{const n=x.dataset.n,j=s.rent.findIndex(r=>r.n===n);if(j>=0)s.rent.splice(j,1);else s.rent.push({n,price:"",u:"Por pieza",min:""});});
  el.querySelectorAll(".st-r,.rt-r").forEach(R=>{const r=(R.classList.contains("st-r")?s.staff:s.rent)[+R.dataset.ri];R.querySelector(".sr-p").oninput=e=>{r.price=e.target.value;syncSubs(s);changed();};R.querySelector(".sr-p").onchange=()=>redraw();R.querySelector(".sr-u").onchange=e=>{r.u=e.target.value;redraw();changed();};const m=R.querySelector(".sr-m");if(m)m.oninput=e=>{r.min=e.target.value;changed();};});
  el.querySelectorAll(".ofc.open[data-j]").forEach(C=>{const j=+C.dataset.j,o=s.offers[j];if(!o)return;const q=(sel,f)=>C.querySelectorAll(sel).forEach(f);
   q(".of-x",b=>b.onclick=()=>{s.offers.splice(j,1);s.open="";redraw();changed();});
   q(".tmr",R=>{const t=o.tiempos[+R.dataset.ti];R.querySelector(".t-n").oninput=e=>{t.n=e.target.value;changed();};R.querySelector(".t-d").oninput=e=>{t.d=e.target.value;changed();};
    R.querySelectorAll(".sd button").forEach(b=>b.onclick=()=>{t.k=b.dataset.k;redraw();});R.querySelector(".t-x").onclick=()=>{o.tiempos.splice(+R.dataset.ti,1);redraw();changed();};});
   q(".t-add",b=>b.onclick=()=>{o.tiempos.push({n:"",k:"Salado",d:""});redraw();});
   q(".mr",R=>{const L=o[R.dataset.k],x=L[+R.dataset.xi];R.querySelector(".m-d").oninput=e=>{x.d=e.target.value;changed();};R.querySelectorAll(".sw button").forEach(b=>b.onclick=()=>{x.t=b.dataset.t;redraw();});R.querySelector(".m-x").onclick=()=>{L.splice(+R.dataset.xi,1);redraw();changed();};});
   q(".m-add",b=>b.onclick=()=>{o[b.dataset.k].push(o.kind==="drink"?{d:"",t:"Frío"}:{d:""});redraw();setTimeout(()=>{const l=[...document.querySelectorAll(`.box[data-i="${i}"] .ofc.open .mr[data-k="${b.dataset.k}"] .m-d`)].pop();l&&l.focus();},0);});
   q(".qkb",b=>b.onclick=()=>{(b.dataset.l==="ex"?o.ext:o.inc).push(b.dataset.l==="ex"?{c:b.dataset.c,q:"",u:"",cost:""}:newRow(b.dataset.c));redraw();setTimeout(()=>{const l=[...document.querySelectorAll(`.box[data-i="${i}"] .ofc.open .incr.${b.dataset.l} .r-q`)].pop();l&&l.focus();},0);});
   q(".incr",R=>{const L=R.classList.contains("ex")?o.ext:o.inc,r=L[+R.dataset.ri];[["r-c","c"],["r-q","q"],["r-u","u"],["r-cost","cost"]].forEach(([c,f])=>{const x=R.querySelector("."+c);if(x)x.oninput=e=>{r[f]=e.target.value;syncSubs(s);changed();};});R.querySelector(".r-x").onclick=()=>{L.splice(+R.dataset.ri,1);redraw();changed();};});
   q(".r-add",b=>b.onclick=()=>{(b.dataset.l==="ex"?o.ext:o.inc).push(b.dataset.l==="ex"?{c:"",q:"",u:"",cost:""}:newRow());redraw();setTimeout(()=>{const l=[...document.querySelectorAll(`.box[data-i="${i}"] .ofc.open .incr.${b.dataset.l} .r-c`)].pop();l&&l.focus();},0);});
   q(".of-dur",x=>x.oninput=e=>{o.dur=e.target.value;changed();});q(".of-duru",x=>x.onchange=e=>{o.durU=e.target.value;changed();});
   q(".tarr[data-ti]",R=>{const t=o.tar[+R.dataset.ti],hv=()=>{const h=R.querySelector(".ta-hv");if(h)h.innerHTML=offerHost(o,t,s.cat);};
    R.querySelector(".ta-p").oninput=e=>{t.price=e.target.value;hv();syncSubs(s);changed();};R.querySelector(".ta-p").onchange=()=>{if(!C.querySelector('.r-add[data-l="ex"]'))redraw();};R.querySelector(".ta-u").onchange=e=>{t.u=e.target.value;redraw();changed();};
    const uo=R.querySelector(".ta-uo");if(uo){uo.oninput=e=>{t.uo=e.target.value;changed();};uo.onchange=()=>{const cu=canonUnit(t.uo);if(cu){t.u=cu;t.uo="";if(!U_FULL.includes(cu))U_FULL.push(cu);redraw();}else NEW_UNITS.add(t.uo);};}
    const a=R.querySelector(".ta-a");if(a)a.oninput=e=>{t.alc=e.target.value;hv();syncSubs(s);changed();};const x=R.querySelector(".ta-x");if(x)x.onclick=()=>{o.tar.splice(+R.dataset.ti,1);redraw();changed();};});
   q(".ta-add",b=>b.onclick=()=>{o.tar.push({w:b.dataset.w,price:"",u:"Por evento",uo:"",alc:""});redraw();});
   if(o.tar.some(t=>filled(t.price)))bindUploader(`${k}o${j}`,"photo",o.photos,redraw);});
  const d=$("d-"+k);if(d)d.oninput=e=>{s.desc=e.target.value;s.descEdited=true;changed();};
  bindDl(s,k,el,redraw);
  if($("mn-"+k)){bindMin(s.min,k,redraw);bindPromo(s.promo,k,redraw);}
  const rm=el.querySelector(".rm-svc");if(rm)rm.onclick=()=>{S.services.splice(i,1);drawServices();changed();};});
 const pb=$("pkgBox");if(pb){pb.innerHTML=pkgHtml();bindPkgs(()=>{const y=scrollY;drawServices();scrollTo({top:y});});}}
function drawSvcStep(){const sc=S.svcScope=S.svcScope||{S:false,E:false};
 $("stepBody").innerHTML=`<div class="panel"><span class="crumb">Mi negocio › Servicios</span><h2>Mis servicios 🎉</h2><p class="sub">Pon el precio como tú lo cobras. Nosotros se lo mostramos al anfitrión por persona y en total.</p>
 <div class="svc-top">
  <div class="field"><span class="lbl">¿Para qué tipo de eventos? <span class="opt">Puedes elegir los dos</span></span><div class="chips${MISS(sc.S||sc.E)}" style="width:fit-content;border-radius:99px"><button type="button" class="chip scp" data-v="S" aria-pressed="${!!sc.S}">${TICK}🎉 Sociales</button><button type="button" class="chip scp" data-v="E" aria-pressed="${!!sc.E}">${TICK}💼 Empresariales</button></div></div>
  <div class="field qwrap"><label class="lbl" for="svcQ">🔎 Busca lo que ofreces <span class="opt">o elige abajo por categoría</span></label><input type="search" id="svcQ" autocomplete="off" placeholder="Ej. banquete, tacos al pastor, DJ, meseros, sillas…"><div id="svcQr" class="qres" hidden></div></div>
 </div>
 <div id="svcList" style="display:grid;gap:14px"></div><button type="button" class="btn ghost" id="addSvc">+ Agregar otra categoría</button>
 <div id="pkgBox"></div>
 ${priceBoxHtml()}
 ${zonesHtml(S.svcZones,"svc","¿Dónde das estos servicios?")}${VIATICOS}${navHtml()}</div>`;
 document.querySelectorAll(".scp").forEach(c=>c.onclick=()=>{sc[c.dataset.v]=!sc[c.dataset.v];drawSvcStep();changed();});
 const q=$("svcQ"),qr=$("svcQr"),WE={full:"🎁",staff:"🙋",rent:"📦"},WT={full:"servicio",staff:"staff",rent:"renta"};
 const search=()=>{const v=norm(q.value).trim();if(v.length<2){qr.hidden=true;return;}const toks=v.split(/\s+/),res=[];
  CAT2.forEach(c=>{[["full",c.full],["staff",c.staff],["rent",c.rent]].forEach(([w,l])=>l.forEach(n=>{const h=norm(n+" "+c.n);if(toks.every(t=>h.includes(t)))res.push({c,n,w,r:norm(n).startsWith(v)?0:1});}));});
  if(res.length<6)["Salado","Dulce"].forEach(kd=>DISH_LIST[kd].forEach(d=>{if(res.length<8&&toks.every(t=>norm(d).includes(t)))res.push({c:CAT2[0],n:"Buffet",w:"full",r:2,dish:d,kd});}));
  res.sort((a,b)=>a.r-b.r);
  qr.innerHTML=res.slice(0,8).map((x,ix)=>`<button type="button" data-ix="${ix}"><span>${x.c.e}</span><span><b>${esc(x.dish||x.n)}</b> <small>· ${esc(x.c.n)} · ${WE[x.w]} ${x.dish?"menú de buffet":WT[x.w]}</small></span></button>`).join("")
   ||`<span class="hint" style="padding:8px">No lo encontramos. Elige la categoría más cercana y usa <b>✏️ Otro</b>: lo sumamos al catálogo.</span>`;
  qr.hidden=false;qr.querySelectorAll("button").forEach(btn=>btn.onclick=()=>{const x=res[+btn.dataset.ix],i=boxFor(x.c.n),s=S.services[i];
   if(x.w==="full"){s.ways.full=true;const food=s.cat==="Catering"&&FOOD_FMT.includes(x.n),drink=s.cat==="Catering"&&!food;if(s.cat==="Catering")s.cater[food?"food":"drink"]=true;
    addOffer(s,drink?x.n.replace(/ de bebidas$/,"").replace(/^(\w)/,m=>m.toUpperCase()):x.n,s.cat==="Catering"?(food?"food":"drink"):"gen");
    if(x.dish){const o=s.offers[+s.open.slice(1)],L=o[x.kd==="Dulce"?"dul":"sal"],e=L.find(r=>!filled(r.d));if(e)e.d=x.dish;else L.push({d:x.dish});}}
   else addPerson(s,x.w==="staff"?"staff":"rent",x.n,x.w==="staff"?"Por hora":"Por pieza");
   syncSubs(s);q.value="";qr.hidden=true;hqvTrack("servicio_buscado",{sub:x.n});goBox(i);});};
 q.oninput=search;q.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();const f=qr.querySelector("button");f&&f.click();}if(e.key==="Escape"){qr.hidden=true;}};
 drawServices();$("addSvc").onclick=()=>{S.services.push(blankSvc());drawServices();changed();const l=$("svcList").lastElementChild;l&&l.scrollIntoView({behavior:"smooth",block:"start"});};
 bindPriceBox(drawSvcStep);bindZones(S.svcZones,"svc",drawSvcStep);bindNav();}
