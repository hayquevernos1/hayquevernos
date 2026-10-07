"""v6 · Nuevo selector de servicios del proveedor con el catálogo completo de Diego (catalogo_servicios.js).
Lee reg5.html (salida de patch5.py) y escribe reg6.html."""
import re
from pathlib import Path
D = Path('/home/claude/hqv/v5')


def rep(s, a, b, count=1):
    assert a in s, 'NO ENCONTRADO: ' + a[:90]
    return s.replace(a, b, count)


r = (D / 'reg5.html').read_text()

# ---------- carga del catálogo
r = rep(r, '<script src="catalogo.js"></script>', '<script src="catalogo.js"></script>\n<script src="catalogo_servicios.js"></script>\n<script src="conversiones.js"></script>')

# ---------- estilos del selector
CSS = '''
/* v6 · selector de servicios */
.cats.big{grid-template-columns:repeat(auto-fill,minmax(min(100%,150px),1fr))}
.svc-top{display:grid;gap:12px}
.qwrap{position:relative}
.qres{display:grid;gap:4px;margin-top:6px;background:var(--card);border-radius:16px;padding:6px;box-shadow:var(--hqv-clay-sm,0 6px 18px rgba(0,0,0,.08))}
.qres button{border:0;background:none;text-align:left;padding:8px 10px;border-radius:12px;font-size:13.5px;display:flex;gap:8px;align-items:center}
.qres button:hover,.qres button:focus{background:var(--grape-soft)}
.qres small{color:var(--muted)}
.qres .on{color:var(--muted)}
.sub-q{margin-bottom:6px}
.subchips .chip.hide{display:none}
.slines{display:grid;gap:10px}
.sline{background:var(--card);border-radius:16px;padding:12px;display:grid;gap:8px;box-shadow:var(--hqv-clay-sm,0 4px 12px rgba(0,0,0,.06))}
.sl-top{display:flex;justify-content:space-between;gap:8px;align-items:center}
.sl-top b{font-size:14px}
.sl-top small{font-weight:600;color:var(--muted)}
.sl-f{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;font-size:13px}
.sl-f label{display:inline-flex;gap:6px;align-items:center;flex-wrap:wrap}
.sl-f input[type=number]{width:84px;padding:8px 10px}
.sl-f .sl-p input[type=number]{width:130px}
.sl-p span{font-weight:800;color:var(--grape)}
.sl-uo{max-width:280px}
.hv{font-size:12.5px;color:var(--muted);display:block}
.hv b{color:var(--grape)}
.sl-dup{font-size:13px;justify-self:start}
.flash{background:var(--grape-soft);color:var(--grape);border-radius:12px;padding:8px 12px;font-size:13px;font-weight:600}
.vnote{background:var(--paper);border-radius:14px;padding:10px 12px;font-size:13px}
.chips.unit-chips .chip{font-size:12.5px}
'''
i = r.index('</style>')
r = r[:i] + CSS + r[i:]

# ---------- catálogo: 19 categorías / 469 subcategorías / unidades con familia de conversión
a = r.index('const CATS=[')
b = r.index('let SPECS=')
r = r[:a] + '''const SVC=window.HQV_SVC,UF=SVC.units;
const CATS=SVC.cats.map(c=>({n:c.n,e:c.e,s:c.s.map(([n,t,u])=>({n,t,u}))}));
const EXG=50,EXH=5; /* fiesta de ejemplo para mostrar la conversión */
const COMMON_UNITS=["Por persona","Por evento","Por paquete","Por pieza","Por hora"];
''' + r[b:]
r = rep(r, 'const NEW_CATS=new Set(),NEW_SUBS=new Set(),NEW_SPECS=new Set();', 'const NEW_CATS=new Set(),NEW_SUBS=new Set(),NEW_SPECS=new Set(),NEW_UNITS=new Set();')
r = rep(r, 'const UNITS=["por evento","por persona","por hora","por pieza","por kilo","por mesa","por día","por m²","por bloque de 5 h","por niño"];\n', '''const famOf=u=>u==="__otra"?"otra":UF[u]?UF[u][0]:"",tOf=u=>UF[u]?UF[u][1]:"";
const uLabel=u=>/^Porcentaje /.test(u)?"% "+u.slice(11):u.charAt(0).toLowerCase()+u.slice(1);
const uNoun=x=>x.u==="__otra"?(x.uo||"unidad").replace(/^por\\s+/i,""):x.u.replace(/^Por /,"").replace(/ por (hora|día|noche)$/,"");
const lineLabel=x=>!x.u?"":x.u==="__otra"?(x.uo?"por "+x.uo.replace(/^por\\s+/i,""):""):uLabel(x.u);
const URANK=["Por persona","Por evento","Por paquete"];const urank=u=>{const k=URANK.indexOf(u);return k<0?9:k;};
const blankLine=n=>({n,u:"",uo:"",price:"",yieldP:"",pkgP:"",pkgH:"",unit:""});
function canonUnit(v){const t=norm(v).replace(/^por\\s+/,"").trim();return Object.keys(UF).find(u=>{const c=norm(u).replace(/^por\\s+/,"");return c===t||norm(uLabel(u))===norm(v);});}
const scopeOk=t=>{const sc=S.svcScope||{};if(!sc.S&&!sc.E)return true;return(sc.S&&t.includes("S"))||(sc.E&&t.includes("E"));};
function subOf(cat,n){const c=catOf(cat);return c&&c.s.find(x=>x.n===n);}
function priceTxt(x){if(famOf(x.u)==="porcentaje")return`${esc(x.price)}% <small>${esc(uLabel(x.u).slice(2))}</small>`;return`${money(x.price)} <small>${esc(x.unit)}${+x.pkgP>0?` · ${esc(x.pkgP)} personas`:""}</small>`;}
function hostView(x,cat){const P=+x.price;if(!x.u||!(P>0))return"";const f=famOf(x.u),t=tOf(x.u);
 if(f==="porcentaje")return`<span class="hv">👀 El anfitrión verá: ${esc(x.price)}% ${esc(uLabel(x.u).slice(2))}, calculado sobre su fiesta.</span>`;
 if(f==="extra")return`<span class="hv">👀 Solo se suma si la fiesta se alarga: ${money(P)} por hora extra.</span>`;
 const r=hqvCost({cat,sub:x.n,u:x.u,price:P,guests:EXG,hours:EXH,rinde:x.yieldP,pkgP:x.pkgP});
 if(r.pend)return`<span class="hv">👀 ${f==="otra"?"Revisamos esta unidad y te avisamos cómo se la mostramos al anfitrión.":"Dinos para cuántas personas alcanza y lo convertimos; si no, el anfitrión lo verá «por cotizar»."}</span>`;
 const def=!+x.yieldP&&(f==="cantidad"||f==="espacio")?" (con nuestro promedio; si sabes cuánto rinde, ponlo)":"";
 return`<span class="hv">👀 Así lo ve el anfitrión en una fiesta de ${EXG} personas${t==="hora"||t==="minuto"?` y ${EXH} h`:""}: <b>${money(Math.round(r.total/EXG))}</b> por persona · <b>${money(Math.round(r.total))}</b> en total${r.note?" · "+esc(r.note):""}${def}</span>`;}
let FLASH=null;const SHOWALL=new Set();
function addSubTo(cat,n){let i=S.services.findIndex(s=>s.cat===cat);
 if(i<0){i=S.services.findIndex(s=>!s.cat||s.cat==="__new");if(i<0){S.services.push(blankSvc());i=S.services.length-1;}S.services[i].cat=cat;S.services[i].subs=[];}
 const s=S.services[i];if(!s.subs.some(y=>y.n===n)){const L=blankLine(n),sub=subOf(cat,n);if(sub&&sub.u.length===1){L.u=sub.u[0];L.unit=lineLabel(L);}s.subs.push(L);}return i;}
function goBox(i,msg){if(msg)FLASH={i,msg};drawServices();changed();setTimeout(()=>{const b=document.querySelector(`#svcList .box[data-i="${i}"]`);b&&b.scrollIntoView({behavior:"smooth",block:"start"});},0);}
''')

# ---------- estados
r = rep(r, ''' services:[{cat:"Postres",catNew:"",subs:[{n:"Mesa de dulces",price:"3500",unit:"por evento"},{n:"Carrito de antojo",price:"1200",unit:"por hora"}],''',
        ''' svcScope:{S:true,E:false},
 services:[{cat:"Alimentos",catNew:"",subs:[{n:"Mesas de dulces",u:"Por paquete",uo:"",price:"3500",yieldP:"",pkgP:"50",pkgH:"5",unit:"por paquete"},{n:"Mesas de dulces",u:"Por persona",uo:"",price:"75",yieldP:"",pkgP:"",pkgH:"",unit:"por persona"},{n:"Galletas decoradas",u:"Por docena (12 piezas)",uo:"",price:"280",yieldP:"6",pkgP:"",pkgH:"",unit:"por docena (12 piezas)"},{n:"Carritos de alimentos",u:"Por hora",uo:"",price:"1200",yieldP:"",pkgP:"",pkgH:"",unit:"por hora"}],''')
r = rep(r, ''' services:[blankSvc()],svcZones:[blankZone()],''', ''' svcScope:{S:false,E:false},services:[blankSvc()],svcZones:[blankZone()],''')

# ---------- validación
r = rep(r, ''' if(id==="svc"){S.services.forEach((s,i)=>{const n=`Ficha ${i+1}`;
  if(!s.cat||s.cat==="__new")m.push(`${n}: categoría`);if(!s.subs.length)m.push(`${n}: qué ofreces`);
  s.subs.forEach(x=>{if(!filled(x.price))m.push(`${n}: precio de ${x.n}`);});''',
        ''' if(id==="svc"){const sc=S.svcScope||{};if(!sc.S&&!sc.E)m.push("Tipo de eventos: sociales, empresariales o ambos");
  S.services.forEach((s,i)=>{const n=catOf(s.cat)?s.cat:`Ficha ${i+1}`;
  if(!s.cat||s.cat==="__new")m.push(`${n}: categoría`);if(!s.subs.length)m.push(`${n}: qué ofreces`);
  s.subs.forEach(x=>{if(!x.u||(x.u==="__otra"&&!filled(x.uo)))m.push(`${n}: cómo cobras ${x.n}`);else{if(!filled(x.price))m.push(`${n}: precio de ${x.n}`);if(famOf(x.u)==="paquete"&&!(+x.pkgP>0))m.push(`${n}: personas del paquete de ${x.n}`);}});''')

# ---------- paso de servicios (nuevo)
a = r.index('function drawSvcStep(){')
b = r.index('function drawVenue(){')
NEW = r'''function drawSvcStep(){const sc=S.svcScope=S.svcScope||{S:false,E:false};
 $("stepBody").innerHTML=`<div class="panel"><span class="crumb">Mi negocio › Servicios</span><h2>Mis servicios 🎉</h2><p class="sub">Pon el precio como tú lo cobras. Nosotros se lo mostramos al anfitrión por persona y en total.</p>
 <div class="svc-top">
  <div class="field"><span class="lbl">¿Para qué tipo de eventos? <span class="opt">Puedes elegir los dos</span></span><div class="chips${MISS(sc.S||sc.E)}" style="width:fit-content;border-radius:99px"><button type="button" class="chip scp" data-v="S" aria-pressed="${!!sc.S}">${TICK}🎉 Sociales</button><button type="button" class="chip scp" data-v="E" aria-pressed="${!!sc.E}">${TICK}💼 Empresariales</button></div></div>
  <div class="field qwrap"><label class="lbl" for="svcQ">🔎 Busca lo que ofreces <span class="opt">o elige abajo por categoría</span></label><input type="search" id="svcQ" autocomplete="off" placeholder="Ej. taquiza, DJ, carpa, meseros, galletas…"><div id="svcQr" class="qres" hidden></div></div>
 </div>
 <div id="svcList" style="display:grid;gap:14px"></div><button type="button" class="btn ghost" id="addSvc">+ Agregar otra categoría</button>
 ${zonesHtml(S.svcZones,"svc","¿Dónde das estos servicios?")}${navHtml()}</div>`;
 document.querySelectorAll(".scp").forEach(c=>c.onclick=()=>{sc[c.dataset.v]=!sc[c.dataset.v];drawSvcStep();changed();});
 const q=$("svcQ"),qr=$("svcQr");
 const search=()=>{const v=norm(q.value).trim();if(v.length<2){qr.hidden=true;return;}const toks=v.split(/\s+/);const res=[];
  CATS.forEach(c=>c.s.forEach(x=>{if(!scopeOk(x.t))return;const h=norm(x.n+" "+c.n);if(toks.every(t=>h.includes(t)))res.push([c,x,norm(x.n).startsWith(v)?0:norm(x.n).includes(v)?1:2]);}));
  res.sort((p,q2)=>p[2]-q2[2]);
  qr.innerHTML=res.slice(0,8).map(([c,x])=>{const on=S.services.some(s=>s.cat===c.n&&s.subs.some(y=>y.n===x.n));return`<button type="button" data-c="${esc(c.n)}" data-s="${esc(x.n)}"${on?' class="on"':''}><span>${c.e}</span><span><b>${esc(x.n)}</b> <small>· ${esc(c.n)}${on?" · ya lo tienes":""}</small></span></button>`;}).join("")
   ||`<span class="hint" style="padding:8px">No lo encontramos. Elige la categoría más cercana y usa <b>✏️ Otro</b> para escribirlo; lo revisamos para sumarlo al catálogo.</span>`;
  qr.hidden=false;qr.querySelectorAll("button").forEach(btn=>btn.onclick=()=>{const i=addSubTo(btn.dataset.c,btn.dataset.s);q.value="";qr.hidden=true;hqvTrack("servicio_buscado",{sub:btn.dataset.s});goBox(i);});};
 q.oninput=search;q.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();const f=qr.querySelector("button");f&&f.click();}if(e.key==="Escape"){qr.hidden=true;}};
 drawServices();$("addSvc").onclick=()=>{S.services.push(blankSvc());drawServices();changed();const l=$("svcList").lastElementChild;l&&l.scrollIntoView({behavior:"smooth",block:"start"});};
 bindZones(S.svcZones,"svc",drawSvcStep);bindNav();}

function lineHtml(s,k,x,j){const sub=subOf(s.cat,x.n),allowed=(sub&&sub.u.length?sub.u:COMMON_UNITS).slice().sort((p,q)=>urank(p)-urank(q)),f=famOf(x.u);if(x.u&&x.u!=="__otra"&&!allowed.includes(x.u))allowed.push(x.u);
 const same=s.subs.filter(y=>y.n===x.n),nth=same.indexOf(x)+1;
 return`<div class="sline" data-j="${j}">
  <div class="sl-top"><b>${esc(x.n)}${same.length>1?` <small>· forma ${nth}</small>`:''}${NEW_SUBS.has(x.n)?' <small>· nuevo</small>':''}</b><button type="button" class="link bad sl-rm" aria-label="Quitar ${esc(x.n)}">✕ Quitar</button></div>
  <span class="mini-l">¿Cómo lo cobras?</span>
  <div class="chips unit-chips${MISS(!!x.u&&(x.u!=="__otra"||filled(x.uo)))}">${allowed.map(u=>`<button type="button" class="chip sl-u" data-u="${esc(u)}" aria-pressed="${x.u===u}">${esc(uLabel(u))}</button>`).join("")}<button type="button" class="chip new sl-u" data-u="__otra" aria-pressed="${x.u==="__otra"}">✏️ Otra</button></div>
  ${x.u==="__otra"?`<input type="text" class="sl-uo${MISS(filled(x.uo))}" list="dlUnits" value="${esc(x.uo)}" placeholder="Escribe tu unidad: por charola, por metro…" aria-label="Otra unidad para ${esc(x.n)}">`:''}
  ${x.u?`<div class="sl-f">
   <label class="sl-p"><span>${f==="porcentaje"?"%":"$"}</span><input type="number" min="0" step="any" class="sl-price${MISS(filled(x.price))}" value="${esc(x.price)}" placeholder="${f==="porcentaje"?"porcentaje":"precio"}" aria-label="Precio de ${esc(x.n)} ${esc(lineLabel(x))}"> <small class="opt">${esc(f==="porcentaje"?uLabel(x.u).slice(2):lineLabel(x))}</small></label>
   ${f==="paquete"?`<label>¿Para cuántas personas? <input type="number" min="1" class="sl-pkgP${MISS(+x.pkgP>0)}" value="${esc(x.pkgP)}"></label><label>¿Cuántas horas incluye? <input type="number" min="0" step="any" class="sl-pkgH" value="${esc(x.pkgH)}"> <span class="opt">(opcional)</span></label>`:''}
   ${f==="cantidad"||f==="espacio"||f==="otra"?`<label>Cada ${esc(uNoun(x))} alcanza para <input type="number" min="0" step="any" class="sl-yield" value="${esc(x.yieldP)}"> personas <span class="opt">(opcional)</span></label>`:''}
  </div><div class="sl-hv">${hostView(x,s.cat)}</div>`:''}
  <button type="button" class="link sl-dup">+ Otra forma de cobrar ${esc(x.n.toLowerCase())}</button>
 </div>`;}

function drawServices(){const list=$("svcList");if(!list)return;
 list.innerHTML=S.services.map((s,i)=>{const cat=catOf(s.cat),k="s"+i,anchor="s"+(i+1),fl=FLASH&&FLASH.i===i?FLASH.msg:"";
 const subs=cat?cat.s.filter(x=>scopeOk(x.t)||s.subs.some(y=>y.n===x.n)):[],hid=cat?cat.s.length-subs.length:0;
 return`<div class="box" data-i="${i}"><div class="box-head"><h3>${cat?cat.e+" "+esc(cat.n):"Ficha "+(i+1)}</h3><span style="display:flex;gap:14px">${cat?`<button type="button" class="link ch-cat">Cambiar categoría</button>`:''}${S.services.length>1?`<button type="button" class="link bad rm-svc">Quitar</button>`:''}</span></div>
 ${fl?`<div class="flash">${esc(fl)}</div>`:''}
 ${!cat?`<div class="field"><span class="lbl">1. Categoría</span><div class="cats big${MISS(!!cat)}">${CATS.map(c=>{const used=S.services.some((y,ii)=>ii!==i&&y.cat===c.n);return`<button type="button" class="cat" data-c="${esc(c.n)}" aria-pressed="${s.cat===c.n}"><span class="emo">${c.e}</span><span>${esc(c.n)}${NEW_CATS.has(c.n)?' <small>· nueva</small>':''}${used?' <small>· ya la tienes</small>':''}</span></button>`;}).join("")}<button type="button" class="cat" data-c="__new" aria-pressed="${s.cat==="__new"}"><span class="emo">✏️</span><span>Otra</span></button></div>
  ${s.cat==="__new"?`<div style="display:flex;gap:8px"><input type="text" id="cn-${k}" list="dlCats" value="${esc(s.catNew)}" placeholder="Escribe tu categoría"><button type="button" class="btn sm" id="cnb-${k}">Agregar</button></div><span class="hint">Si ya existe te la sugerimos; si no, la revisamos para sumarla al catálogo.</span>`:''}</div>`:''}
 ${cat?`<div class="field"><span class="lbl">¿Qué ofreces de ${esc(cat.n.toLowerCase())}? <span class="opt">Elige todos los que hagas</span></span>
  ${subs.length>10?`<input type="search" class="sub-q" placeholder="🔎 Filtrar ${subs.length} opciones…" aria-label="Filtrar subcategorías">`:''}
  <div class="chips subchips${MISS(s.subs.length>0)}" style="border-radius:14px">${subs.map((x,xi)=>`<button type="button" class="chip sub${xi>=12&&!s.subs.some(y=>y.n===x.n)&&!SHOWALL.has(i)?" more hide":""}" data-s="${esc(x.n)}" aria-pressed="${s.subs.some(y=>y.n===x.n)}">${TICK}${esc(x.n)}${NEW_SUBS.has(x.n)?' <small>· nuevo</small>':''}</button>`).join("")}${subs.length>12&&!SHOWALL.has(i)?`<button type="button" class="chip new sh-all">Ver las ${subs.length} opciones</button>`:''}<button type="button" class="chip new" id="sbn-${k}">✏️ Otro</button></div>
  ${hid?`<span class="hint">Ocultamos ${hid} que no son para el tipo de eventos que elegiste.</span>`:''}
  <div style="display:flex;gap:8px" id="snw-${k}" hidden><input type="text" id="sn-${k}" list="dlSubs" placeholder="¿Cómo se llama tu servicio?"><button type="button" class="btn sm" id="snb-${k}">Agregar</button></div>
  ${cat.n==="Espacios y hospedaje"?`<div class="vnote">🏡 ¿Rentas un salón, terraza, jardín o casa para fiestas? ${S.types.venue?"Tu venue tiene su propia sección con capacidad, horarios y paquetes.":`<button type="button" class="link" id="tv-${k}">Activa la ficha de venue</button> para registrar capacidad, horarios y paquetes.`}</div>`:''}</div>`:''}
 ${s.subs.length?`<div class="field"><span class="lbl">💲 ¿Cómo lo cobras?</span><span class="hint">¿Cobras de dos formas? Usa <b>+ Otra forma de cobrar</b>.</span><div class="slines">${s.subs.map((x,j)=>lineHtml(s,k,x,j)).join("")}</div></div>
 <div class="field"><label class="lbl" for="d-${k}">💬 Descríbelo en una frase</label><input type="text" id="d-${k}" class="${MISS(filled(s.desc))}" value="${esc(s.desc)}" placeholder="Qué incluye y para cuántas personas"></div>
 <div class="field"><span class="lbl">🚚 ¿Cómo entregas este servicio? <span class="opt">Puedes elegir los dos</span></span><div class="chips${MISS(s.person||s.ship)}" style="width:fit-content;border-radius:99px"><button type="button" class="chip" id="dp-${k}" aria-pressed="${s.person}">${TICK}🙋 En persona</button><button type="button" class="chip" id="ds-${k}" aria-pressed="${s.ship}">${TICK}📦 Por envío a domicilio</button></div>
  ${s.ship?`<div class="sub-box${MISS(shipOk(s))}"><span class="lbl">¿Cuánto cobras de envío?</span><div class="chips">${[["gratis","🎁 Gratis"],["fijo","💵 Costo fijo"],["distancia","📍 Según la distancia"]].map(([v,t])=>`<button type="button" class="chip shm" data-v="${v}" aria-pressed="${s.shipMode===v}">${TICK}${t}</button>`).join("")}</div>
   ${s.shipMode==="fijo"?`<input type="number" min="0" id="sf-${k}" value="${esc(s.shipFixed)}" placeholder="$ costo del envío" aria-label="Costo fijo de envío">`:''}
   ${s.shipMode==="distancia"?`<div class="row"><div class="field"><label class="hint" for="sb-${k}">Cobro base $</label><input type="number" min="0" id="sb-${k}" value="${esc(s.shipBase)}"></div><div class="field"><label class="hint" for="sk-${k}">Incluye hasta (km)</label><input type="number" min="0" id="sk-${k}" value="${esc(s.shipBaseKm)}"></div><div class="field"><label class="hint" for="sq-${k}">$ por km extra</label><input type="number" min="0" id="sq-${k}" value="${esc(s.shipPerKm)}"></div><div class="field"><label class="hint" for="sm-${k}">Llego hasta (km)</label><input type="number" min="0" id="sm-${k}" value="${esc(s.shipMaxKm)}"></div></div>
    <div class="calc" id="calc-${k}"></div><span class="hint">Cuando un anfitrión cotice, calculamos la distancia entre tu negocio y su fiesta y le mostramos el envío exacto.</span>`:''}
   ${s.shipMode&&s.shipMode!=="gratis"?`<div class="field"><label class="hint" for="sfr-${k}">Envío gratis en compras desde $ <span class="opt">(opcional)</span></label><input type="number" min="0" id="sfr-${k}" value="${esc(s.shipFreeFrom)}"></div>`:''}</div>`:''}</div>
 ${minHtml(s.min,k)}
 ${specsHtml(s.specs,k)}
 ${promoHtml(s.promo,k,anchor)}
 <div class="field"><span class="lbl">📷 Fotos de este servicio</span>${uploaderHtml(k,"photo",s.photos,s.photos.length>0)}</div>`:''}
 </div>`;}).join("");
 FLASH=null;
 list.querySelectorAll(".box").forEach(el=>{const i=+el.dataset.i,s=S.services[i],k="s"+i,redraw=()=>drawServices();
  el.querySelectorAll(".cat").forEach(t=>t.onclick=()=>{const c=t.dataset.c;
   const o=S.services.findIndex((y,ii)=>ii!==i&&y.cat===c&&c!=="__new");
   if(o>=0){if(!s.subs.length){S.services.splice(i,1);goBox(o>i?o-1:o,"Ya tenías esta categoría; aquí está.");}else goBox(o,"Ya tenías esta categoría; aquí está.");return;}
   if(s.cat!==c){s.cat=c;s.subs=[];}redraw();changed();});
  const chc=el.querySelector(".ch-cat");if(chc)chc.onclick=()=>{s.cat="";s.subs=[];redraw();changed();};
  const tv=$("tv-"+k);if(tv)tv.onclick=()=>{S.types.venue=true;hqvTrack("venue_desde_servicios");render();};
  const sq=el.querySelector(".sub-q");if(sq)sq.oninput=()=>{const v=norm(sq.value).trim();el.querySelectorAll(".subchips .chip.sub").forEach(c=>c.classList.toggle("hide",v?!norm(c.dataset.s).includes(v)&&c.getAttribute("aria-pressed")!=="true":c.classList.contains("more")));};
  const sa=el.querySelector(".sh-all");if(sa)sa.onclick=()=>{SHOWALL.add(i);redraw();};
  el.querySelectorAll(".sub").forEach(t=>t.onclick=()=>{const n=t.dataset.s;if(s.subs.some(y=>y.n===n))s.subs=s.subs.filter(y=>y.n!==n);else addSubTo(s.cat,n);redraw();changed();});
  const addCat=()=>{const v=($("cn-"+k).value||"").trim();if(!v)return;let c=CATS.find(x=>norm(x.n)===norm(v));if(!c){c={n:v,e:"✨",s:[]};CATS.push(c);NEW_CATS.add(v);}
   const o=S.services.findIndex((y,ii)=>ii!==i&&y.cat===c.n);if(o>=0){S.services.splice(i,1);goBox(o>i?o-1:o,"Ya tenías esta categoría; aquí está.");return;}
   s.cat=c.n;s.catNew="";redraw();changed();if(!c.s.length)setTimeout(()=>{const b=$("sbn-"+k);b&&b.click();},0);};
  if($("cn-"+k)){$("cnb-"+k).onclick=addCat;$("cn-"+k).onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();addCat();}};$("cn-"+k).oninput=e=>{s.catNew=e.target.value;};}
  const addSub=()=>{const v=($("sn-"+k).value||"").trim();if(!v)return;const c=catOf(s.cat);const ex=c.s.find(x=>norm(x.n)===norm(v));
   if(ex){addSubTo(c.n,ex.n);redraw();changed();return;}
   for(const cc of CATS){const e2=cc.s.find(x=>norm(x.n)===norm(v));if(e2){const ii=addSubTo(cc.n,e2.n);goBox(ii,`“${e2.n}” ya existe en ${cc.n}; lo agregamos ahí.`);return;}}
   c.s.push({n:v,t:"SE",u:[]});NEW_SUBS.add(v);s.subs.push(blankLine(v));hqvTrack("catalogo_propuesta",{tipo:"subcategoria",cat:c.n,valor:v});redraw();changed();};
  if($("sbn-"+k)){$("sbn-"+k).onclick=()=>{$("snw-"+k).hidden=false;$("sn-"+k).focus();};$("snb-"+k).onclick=addSub;$("sn-"+k).onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();addSub();}};}
  el.querySelectorAll(".sline").forEach(L=>{const j=+L.dataset.j,x=s.subs[j],hv=()=>{const h=L.querySelector(".sl-hv");if(h)h.innerHTML=hostView(x,s.cat);};
   L.querySelectorAll(".sl-u").forEach(c=>c.onclick=()=>{x.u=c.dataset.u;x.unit=lineLabel(x);redraw();changed();if(x.u==="__otra")setTimeout(()=>{const b=document.querySelector(`#svcList .box[data-i="${i}"] .sline[data-j="${j}"] .sl-uo`);b&&b.focus();},0);});
   const uo=L.querySelector(".sl-uo");if(uo){uo.oninput=e=>{x.uo=e.target.value;x.unit=lineLabel(x);changed();};
    uo.onchange=()=>{const v=x.uo.trim();if(!v)return;const cu=canonUnit(v);if(cu){x.u=cu;x.uo="";}else{NEW_UNITS.add(v);hqvTrack("catalogo_propuesta",{tipo:"unidad",sub:x.n,valor:v});}x.unit=lineLabel(x);redraw();changed();};}
   [["sl-price","price"],["sl-pkgP","pkgP"],["sl-pkgH","pkgH"],["sl-yield","yieldP"]].forEach(([c,f])=>{const n=L.querySelector("."+c);if(n)n.oninput=e=>{x[f]=e.target.value;hv();changed();};});
   L.querySelector(".sl-rm").onclick=()=>{s.subs.splice(j,1);redraw();changed();};
   L.querySelector(".sl-dup").onclick=()=>{let e=j;while(e+1<s.subs.length&&s.subs[e+1].n===x.n)e++;s.subs.splice(e+1,0,blankLine(x.n));redraw();changed();};});
  const calc=()=>{const c=$("calc-"+k);if(c)c.innerHTML="Así se vería: "+[3,10,20,35].map(km=>{const v=shipCost(s,km);return`<span>${km} km: ${v===null?"fuera de zona":money(Math.round(v))}</span>`;}).join("");};
  [["d-","desc"],["sf-","shipFixed"],["sb-","shipBase"],["sk-","shipBaseKm"],["sq-","shipPerKm"],["sm-","shipMaxKm"],["sfr-","shipFreeFrom"]].forEach(([p,f])=>{const x=$(p+k);if(x)x.oninput=e=>{s[f]=e.target.value;calc();changed();};});calc();
  const dp=$("dp-"+k),ds=$("ds-"+k);if(dp)dp.onclick=()=>{s.person=!s.person;redraw();changed();};if(ds)ds.onclick=()=>{s.ship=!s.ship;redraw();changed();};
  el.querySelectorAll(".shm").forEach(c=>c.onclick=()=>{s.shipMode=c.dataset.v;redraw();changed();});
  if(s.subs.length){bindMin(s.min,k,redraw);bindSpecs(s.specs,k,redraw);bindPromo(s.promo,k,redraw);bindUploader(k,"photo",s.photos,redraw);}
  const rm=el.querySelector(".rm-svc");if(rm)rm.onclick=()=>{S.services.splice(i,1);redraw();changed();};});}

'''
r = r[:a] + NEW + r[b:]

# ---------- sitio público: precio con unidad / % / personas del paquete
r = rep(r, '''${filled(x.price)?`${money(x.price)} <small>${esc(x.unit)}</small>`:'<small>Por cotizar</small>'}''',
        '''${filled(x.price)&&x.u?priceTxt(x):'<small>Por cotizar</small>'}''')

# ---------- lo que se publica (para Supabase): unidad canónica, rendimiento, paquete, propuestas al catálogo
r = rep(r, '''servicios:S.services.map(s=>({cat:s.cat,subs:s.subs.map(x=>({n:x.n,precio:x.price}))})).filter(s=>s.cat),''',
        '''ambito:{social:!!(S.svcScope||{}).S,empresarial:!!(S.svcScope||{}).E},
  servicios:S.services.map(s=>({cat:s.cat,subs:s.subs.map(x=>({n:x.n,precio:x.price,unidad:x.u==="__otra"?null:x.u,unidadOtra:x.u==="__otra"?x.uo:null,familia:famOf(x.u),rinde:x.yieldP||null,paquetePersonas:x.pkgP||null,paqueteHoras:x.pkgH||null}))})).filter(s=>s.cat),
  propuestas:{categorias:[...NEW_CATS],subcategorias:[...NEW_SUBS],unidades:[...NEW_UNITS]},''')

# ---------- datalists para autocompletar sin duplicados
r = rep(r, '''document.body.insertAdjacentHTML("beforeend",`<datalist id="minUnits">${MIN_UNITS.map(u=>`<option value="${u}">`).join("")}</datalist>`);''',
        '''document.body.insertAdjacentHTML("beforeend",`<datalist id="minUnits">${MIN_UNITS.map(u=>`<option value="${u}">`).join("")}</datalist>
<datalist id="dlUnits">${Object.keys(UF).map(u=>`<option value="${esc(uLabel(u))}">`).join("")}</datalist>
<datalist id="dlCats">${CATS.map(c=>`<option value="${esc(c.n)}">`).join("")}</datalist>
<datalist id="dlSubs">${[...new Set(CATS.flatMap(c=>c.s.map(x=>x.n)))].sort().map(n=>`<option value="${esc(n)}">`).join("")}</datalist>`);''')

assert 'UNITS.map' not in r.replace('MIN_UNITS.map', ''), 'quedó una referencia a UNITS'
(D / 'reg6.html').write_text(r)
print('reg6.html', len(r))
