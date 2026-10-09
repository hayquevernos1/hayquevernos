"""v14 · Registro (Diego, 9 oct 2026 tarde). reg8.html → reg9.html
- Entregas de servicios con la lógica del Excel «Cotizador de entregas»: 9 modalidades, ¿Cobras por la entrega? Sí/No,
  ¿Cómo lo cobras? (unidad compatible con la modalidad + tarifa), hasta 3 condiciones y ejemplo en vivo.
  Compacto: cada modalidad es una tarjeta plegable; solo una abierta a la vez.
- Paquetes: «Sin límite» en ¿Para cuántas personas? y ¿Cuántas horas incluye?
- Zonas: «🇲🇽 A nivel nacional» como primera opción.
- Venue: en lugar del «Estándar ¡HQV!» de montaje, dos preguntas: tiempo de montaje (sujeto a disponibilidad)
  y tiempo de entrada/salida de asistentes (gratis o con costo)."""
from pathlib import Path
SRC = Path('/home/claude/hqv/v5/reg8.html')
DST = Path('/home/claude/hqv/v5/reg9.html')
s = SRC.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:140]
    s = s.replace(a, b, count)


CSS = '''
/* ===== v14 · entregas ===== */
.dlm-chips .chip{font-size:13px;padding:7px 12px}
.dlc{border-radius:20px;background:rgba(255,255,255,.85);box-shadow:var(--hqv-clay-sm,0 4px 12px rgba(65,20,95,.08));margin-top:8px}
.dlc.closed{padding:0}
.dlc .dlh{display:flex;align-items:center;gap:8px;width:100%;border:0;background:none;text-align:left;font:inherit;padding:11px 14px;cursor:pointer}
.dlc .dlh b{font-size:14px;white-space:nowrap}
.dlc .dlh .sm{font-size:12px;color:var(--muted);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.dlc .dlh .ed{font-size:12px;font-weight:800;color:#8205B4}
.dlc .dlh .bad{color:#c0003c}
.dlc.open{padding:4px 14px 12px;display:grid;gap:9px;outline:2px solid #BEAAFF}
.dlc.open .dlh{padding:8px 0 0}
.dlq{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-weight:800;font-size:14px}
.dlrow{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.dlrow select{flex:1 1 190px;min-width:0}
.dlrow input{flex:0 1 140px;min-width:90px}
.dlrow .u{font-size:12px;color:var(--muted);font-weight:700}
.dlz{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.dlz label{font-size:12px;color:var(--muted);font-weight:700;display:grid;gap:4px}
.dlcd{display:flex;gap:8px;align-items:center}
.dlcd select{flex:1 1 auto;min-width:0}.dlcd input{flex:0 0 110px}
.dlcd .u{font-size:12px;font-weight:800;color:var(--muted);min-width:30px}
.dl-ex{font-size:12.5px;background:#F0F0FF;border-radius:14px;padding:8px 11px;line-height:1.4}
.dl-ex b{color:#8205B4}
.dl-inc{font-size:13px;font-weight:800;color:#0a7a52;background:#E3FBF1;border-radius:12px;padding:6px 10px;justify-self:start}
.dl-ok{justify-self:end}
.sl-nolim{font-size:12px!important;padding:5px 10px!important}
.vq{display:grid;gap:6px}
.vq .row2{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.vq .row2 input{flex:0 0 110px}.vq .row2 select{flex:0 0 140px}
@media(max-width:560px){.dlz{grid-template-columns:1fr}}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# ---------- modelo de entregas ----------
JS = r'''
/* ===== v14 · entregas (lógica del Excel «Cotizador de entregas») ===== */
const DL_MODS=[["Envío a domicilio","📦"],["Entrega con instalación","🛠️"],["Entrega y recolección","🔁"],["Servicio presencial en el evento","🙋"],["Servicio en establecimiento","🏪"],["Recolección en establecimiento","🛍️"],["Entrega digital","💻"],["Servicio remoto o virtual","🎥"],["Otro","✏️"]];
/* unidad: [método, etiqueta de tarifa, cantidad del ejemplo, palabra de la cantidad] */
const DL_U={"Tarifa fija":["fijo","$ por entrega"],"Por kilómetro":["mult","$ por km",20,"km"],"Por viaje":["mult","$ por viaje",2,"viajes (ida y vuelta)"],"Por hora":["mult","$ por hora",4,"horas"],"Por día":["mult","$ por día",1,"día"],
 "Por persona del equipo":["mult","$ por persona",3,"personas del equipo"],"Por unidad":["mult","$ por pieza",10,"piezas"],"Por volumen (m³)":["mult","$ por m³",2.5,"m³"],"Por peso (kg)":["mult","$ por kg",40,"kg"],
 "Por zona geográfica":["zona"],"Por porcentaje":["pct","% del servicio"],"Por evento":["fijo","$ por evento"],"Según cotización":["cot"],"Otro":["otro"]};
const DL_ALL=Object.keys(DL_U),DL_LOCAL=["Tarifa fija","Por hora","Por día","Por persona del equipo","Por unidad","Por porcentaje","Por evento","Según cotización","Otro"];
const DL_PRES=DL_ALL.filter(u=>u!=="Por volumen (m³)"&&u!=="Por peso (kg)");
const dlUnits=m=>m==="Servicio presencial en el evento"?DL_PRES:["Servicio en establecimiento","Recolección en establecimiento","Entrega digital","Servicio remoto o virtual"].includes(m)?DL_LOCAL:DL_ALL;
const DL_CONDS={"Compra mínima":"$","Entrega gratuita desde":"$","Tarifa mínima":"$","Cargo adicional":"$","Recargo (%)":"%","Distancia máxima":"km","Anticipación requerida":"días"};
const DL_CONDS_INC=["Distancia máxima","Anticipación requerida"];
const DL_OM=[["fijo","Fijo"],["mult","Multiplicar por cantidad"],["pct","Porcentaje del servicio"],["cot","Según cotización"]];
const DL_EX={serv:4000,km:20,dias:10};
const blankDl=m=>({m,desc:"",cobra:null,u:"",rate:"",z:{local:"",ext:"",fuera:""},uo:"",om:"fijo",oq:"",conds:[]});
const dlEmo=m=>(DL_MODS.find(x=>x[0]===m)||["","🚚"])[1];
const dlMeth=d=>d.u==="Otro"?d.om:(DL_U[d.u]||[])[0];
function dlCondOk(d){return d.conds.every(c=>c.c&&filled(c.v));}
function dlOk(d){if(d.m==="Otro"&&!filled(d.desc))return false;if(d.cobra===null)return false;if(!dlCondOk(d))return false;if(!d.cobra)return true;if(!d.u)return false;
 const me=dlMeth(d);if(d.u==="Otro"&&!filled(d.uo))return false;if(me==="cot")return true;if(me==="zona")return filled(d.z.local);return filled(d.rate);}
function dlCost(d,ex){const C=k=>{const c=d.conds.find(x=>x.c===k);return c&&filled(c.v)?+c.v:null;};
 if(C("Distancia máxima")!==null&&ex.km>C("Distancia máxima"))return{st:"no",why:`está a ${ex.km} km y llegas hasta ${C("Distancia máxima")} km`};
 if(C("Anticipación requerida")!==null&&ex.dias<C("Anticipación requerida"))return{st:"no",why:`pides ${C("Anticipación requerida")} días de anticipación`};
 if(!d.cobra)return{st:"ok",v:0,inc:true};
 if(C("Compra mínima")!==null&&ex.serv<C("Compra mínima"))return{st:"no",why:`la compra mínima es ${money(C("Compra mínima"))}`};
 const me=dlMeth(d),U=DL_U[d.u]||[],q=d.u==="Otro"?(+d.oq||1):(U[2]||1);if(me==="cot")return{st:"cot"};
 let b=me==="zona"?+d.z.local||0:me==="pct"?(+d.rate||0)/100*ex.serv:me==="mult"?(+d.rate||0)*q:+d.rate||0;const how=me==="mult"?`${q} ${d.u==="Otro"?esc(d.uo||"unidades"):U[3]} × ${money(+d.rate||0)}`:me==="pct"?`${d.rate||0}% de ${money(ex.serv)}`:me==="zona"?"zona local":"";
 if(C("Tarifa mínima")!==null&&C("Tarifa mínima")>b)b=C("Tarifa mínima");b+=C("Cargo adicional")||0;b*=1+(C("Recargo (%)")||0)/100;
 if(C("Entrega gratuita desde")!==null&&ex.serv>=C("Entrega gratuita desde"))return{st:"ok",v:0,free:true,how};
 return{st:"ok",v:Math.round(b*100)/100,how};}
function dlExample(d){if(d.cobra===null)return"";const r=dlCost(d,DL_EX),ctx=`una fiesta a ${DL_EX.km} km, con ${money(DL_EX.serv)} de servicio y reservada con ${DL_EX.dias} días`;
 if(r.st==="no")return`👀 Ejemplo: en ${ctx}, el anfitrión verá <b>no disponible</b> (${r.why}).`;
 if(r.st==="cot")return`👀 El anfitrión verá la entrega <b>por cotizar</b>; tú le mandas el precio.`;
 if(r.inc)return`👀 Ejemplo: en ${ctx}, el anfitrión verá <b>entrega incluida</b>.`;
 if(r.free)return`👀 Ejemplo: en ${ctx}, el anfitrión verá <b>entrega gratis</b> (alcanza tu monto de entrega gratuita).`;
 return`👀 Ejemplo: en ${ctx}, el anfitrión verá entrega de <b>${money(r.v)}</b>${r.how?` <small>(${r.how}${d.conds.length?" + condiciones":""})</small>`:""}.`;}
function dlText(d){const nm=d.m==="Otro"&&d.desc?d.desc:d.m;if(d.cobra===null)return nm;
 const C=d.conds.filter(c=>c.c&&filled(c.v)).map(c=>{const u=DL_CONDS[c.c],v=u==="$"?money(+c.v):c.v+(u==="%"?"%":" "+u);return{"Compra mínima":`compra mín. ${v}`,"Entrega gratuita desde":`gratis desde ${v}`,"Tarifa mínima":`mín. ${v}`,"Cargo adicional":`+ ${v} de cargo`,"Recargo (%)":`+ ${v} recargo`,"Distancia máxima":`hasta ${v}`,"Anticipación requerida":`${v} de anticipación`}[c.c];});
 let p;if(!d.cobra)p="incluida";else{const me=dlMeth(d),U=DL_U[d.u]||[];
  p=!d.u?"":me==="cot"?"según cotización":me==="zona"?`por zona desde ${money(+d.z.local||0)}`:me==="pct"?`${d.rate||"—"}% del servicio`:d.u==="Otro"?`${money(+d.rate||0)} ${me==="mult"?"por "+(d.uo||"unidad"):"("+(d.uo||"otro")+")"}`:`${money(+d.rate||0)} ${me==="mult"?U[1].replace("$ ",""):d.u==="Por evento"?"por evento":"fijo"}`;}
 return[nm,p,...C].filter(Boolean).join(" · ");}
function dlCard(s,k,d,j){const open=s.dlOpen===j,ok=dlOk(d);
 if(!open)return`<div class="dlc closed${MISS(ok)}" data-j="${j}"><button type="button" class="dlh dl-open"><b>${dlEmo(d.m)}</b><span class="sm"><b style="color:#1a1033">${esc(d.m==="Otro"&&d.desc?d.desc:d.m)}</b> · ${esc(dlText(d).split(" · ").slice(1).join(" · ")||"falta configurar")}</span><span class="ed">${ok?"✏️ Editar":"⚠️ Completar"}</span></button></div>`;
 const me=dlMeth(d),U=DL_U[d.u]||[],used=d.conds.map(c=>c.c),pool=d.cobra?Object.keys(DL_CONDS):DL_CONDS_INC;
 return`<div class="dlc open${MISS(ok)}" data-j="${j}">
  <div class="dlh"><b>${dlEmo(d.m)} ${esc(d.m)}</b><span class="sm"></span><button type="button" class="link bad dl-x" aria-label="Quitar ${esc(d.m)}">✕ Quitar</button></div>
  ${d.m==="Otro"?`<input type="text" class="dl-desc${MISS(filled(d.desc))}" value="${esc(d.desc)}" placeholder="¿Cómo entregas? Ej. Entrega en punto medio" aria-label="Describe la modalidad">`:""}
  <div class="dlq">¿Cobras por la entrega? ${ynHtml(`dly-${k}-${j}`,d.cobra)}</div>
  ${d.cobra===false?`<span class="dl-inc">✅ La entrega va incluida en tu precio</span>`:""}
  ${d.cobra?`<span class="mini-l">¿Cómo lo cobras?</span>
   <div class="dlrow"><select class="dl-u${MISS(!!d.u)}" aria-label="Unidad de cobro"><option value="">Elige la unidad…</option>${dlUnits(d.m).map(u=>`<option ${u===d.u?"selected":""}>${u}</option>`).join("")}</select>
    ${d.u&&(me==="fijo"||me==="mult"||me==="pct")&&d.u!=="Otro"?`<input type="number" min="0" step="any" class="dl-rate${MISS(filled(d.rate))}" value="${esc(d.rate)}" placeholder="${me==="pct"?"%":"$"}" aria-label="${esc(U[1])}"><span class="u">${esc(U[1])}</span>`:""}</div>
   ${me==="zona"?`<div class="dlz">${[["local","Zona local"],["ext","Zona extendida"],["fuera","Fuera de zona"]].map(([z,t])=>`<label>${t}<input type="number" min="0" class="dl-z${z==="local"?MISS(filled(d.z.local)):""}" data-z="${z}" value="${esc(d.z[z])}" placeholder="$"></label>`).join("")}</div><span class="hint">Usamos las zonas donde das servicio: local = tus municipios, extendida = colindantes, fuera = el resto.</span>`:""}
   ${d.u==="Otro"?`<div class="dlrow"><input type="text" class="dl-uo${MISS(filled(d.uo))}" value="${esc(d.uo)}" placeholder="Tu unidad: por bulto, por carga…" style="flex:1 1 180px" aria-label="Describe la unidad"><select class="dl-om" aria-label="Cómo se calcula">${DL_OM.map(([v,t])=>`<option value="${v}" ${d.om===v?"selected":""}>${t}</option>`).join("")}</select></div>
    ${d.om!=="cot"?`<div class="dlrow"><input type="number" min="0" step="any" class="dl-rate${MISS(filled(d.rate))}" value="${esc(d.rate)}" placeholder="${d.om==="pct"?"%":"$"}" aria-label="Tarifa"><span class="u">${d.om==="pct"?"% del servicio":d.om==="mult"?"$ por "+esc(d.uo||"unidad"):"$ fijo"}</span>${d.om==="mult"?`<input type="number" min="0" class="dl-oq" value="${esc(d.oq)}" placeholder="Ej. 5" aria-label="Cantidad típica"><span class="u">cantidad típica</span>`:""}</div>`:""}`:""}
   ${me==="cot"?`<span class="hint">El anfitrión verá la entrega «por cotizar» y tú le mandas el precio.</span>`:""}`:""}
  ${d.cobra!==null?`<span class="mini-l">Condiciones <span class="opt">(opcional · hasta 3)</span></span>
   ${d.conds.map((c,ci)=>`<div class="dlcd" data-ci="${ci}"><select class="dc-c" aria-label="Condición">${pool.filter(x=>x===c.c||!used.includes(x)).map(x=>`<option ${x===c.c?"selected":""}>${x}</option>`).join("")}</select><input type="number" min="0" step="any" class="dc-v${MISS(filled(c.v))}" value="${esc(c.v)}" aria-label="Valor"><span class="u">${DL_CONDS[c.c]}</span><button type="button" class="link bad dc-x" aria-label="Quitar condición">✕</button></div>`).join("")}
   ${d.conds.length<3&&pool.some(x=>!used.includes(x))?`<button type="button" class="link dc-add" style="justify-self:start">+ Agregar condición${d.cobra?" (compra mínima, entrega gratis desde, distancia máxima…)":" (distancia máxima, anticipación)"}</button>`:""}`:""}
  <div class="dl-ex">${dlExample(d)}</div>
  ${ok?`<button type="button" class="btn cta sm dl-ok">Listo ✓</button>`:""}</div>`;}
function dlSync(s){s.person=s.dl.some(d=>/presencial|establecimiento|remoto/.test(d.m));s.ship=s.dl.some(d=>/Envío|Entrega/.test(d.m));}
function bindDl(s,k,el,redraw){s.dl=s.dl||[];
 el.querySelectorAll(".dlm").forEach(c=>c.onclick=()=>{const m=c.dataset.m,j=s.dl.findIndex(d=>d.m===m);if(j>=0){s.dl.splice(j,1);s.dlOpen=-1;}else{s.dl.push(blankDl(m));s.dlOpen=s.dl.length-1;}dlSync(s);redraw();changed();});
 el.querySelectorAll(".dlc").forEach(C=>{const j=+C.dataset.j,d=s.dl[j];if(!d)return;const ex=()=>{const e=C.querySelector(".dl-ex");if(e)e.innerHTML=dlExample(d);};
  const q=(c,f)=>C.querySelectorAll(c).forEach(f);
  q(".dl-open",b=>b.onclick=()=>{s.dlOpen=j;redraw();});
  q(".dl-ok",b=>b.onclick=()=>{s.dlOpen=-1;redraw();changed();});
  q(".dl-x",b=>b.onclick=()=>{s.dl.splice(j,1);s.dlOpen=-1;dlSync(s);redraw();changed();});
  bindYN(`dly-${k}-${j}`,v=>{d.cobra=v;if(!v){d.conds=d.conds.filter(c=>DL_CONDS_INC.includes(c.c));}redraw();changed();});
  q(".dl-desc",x=>x.oninput=e=>{d.desc=e.target.value;changed();});
  q(".dl-u",x=>x.onchange=e=>{d.u=e.target.value;d.rate="";redraw();changed();});
  q(".dl-rate",x=>x.oninput=e=>{d.rate=e.target.value;ex();changed();});
  q(".dl-z",x=>x.oninput=e=>{d.z[x.dataset.z]=e.target.value;ex();changed();});
  q(".dl-uo",x=>x.oninput=e=>{d.uo=e.target.value;ex();changed();});
  q(".dl-om",x=>x.onchange=e=>{d.om=e.target.value;redraw();changed();});
  q(".dl-oq",x=>x.oninput=e=>{d.oq=e.target.value;ex();changed();});
  q(".dlcd",R=>{const c=d.conds[+R.dataset.ci];R.querySelector(".dc-c").onchange=e=>{c.c=e.target.value;redraw();changed();};R.querySelector(".dc-v").oninput=e=>{c.v=e.target.value;ex();changed();};R.querySelector(".dc-x").onclick=()=>{d.conds.splice(+R.dataset.ci,1);redraw();changed();};});
  q(".dc-add",b=>b.onclick=()=>{const pool=d.cobra?Object.keys(DL_CONDS):DL_CONDS_INC,used=d.conds.map(c=>c.c),nx=pool.find(x=>!used.includes(x));if(nx)d.conds.push({c:nx,v:""});redraw();});});}
'''
rep('function shipCost(s,km){', JS + '\nfunction shipCost(s,km){')

# blankSvc + demo
rep('shipFreeFrom:"",min:blankMin()', 'shipFreeFrom:"",dl:[],dlOpen:-1,min:blankMin()')
rep('shipMaxKm:"30",shipFreeFrom:"5000",',
    'shipMaxKm:"30",shipFreeFrom:"5000",dlOpen:-1,dl:[{m:"Envío a domicilio",desc:"",cobra:true,u:"Por kilómetro",rate:"12",z:{local:"",ext:"",fuera:""},uo:"",om:"fijo",oq:"",conds:[{c:"Tarifa mínima",v:"80"},{c:"Distancia máxima",v:"30"},{c:"Entrega gratuita desde",v:"5000"}]},{m:"Servicio presencial en el evento",desc:"",cobra:false,u:"",rate:"",z:{local:"",ext:"",fuera:""},uo:"",om:"fijo",oq:"",conds:[{c:"Anticipación requerida",v:"7"}]}],')

# UI: reemplaza «¿Cómo entregas este servicio?» + envío
i = s.index(' <div class="field"><span class="lbl">🚚 ¿Cómo entregas este servicio?')
j = s.index(' ${minHtml(s.min,k)}', i)
s = s[:i] + r''' <div class="field"><span class="lbl">🚚 ¿Cómo entregas este servicio? <span class="opt">Elige todas las que hagas</span></span>
  <div class="chips dlm-chips${MISS((s.dl||[]).length>0)}" style="border-radius:14px">${DL_MODS.map(([m,e])=>`<button type="button" class="chip dlm" data-m="${esc(m)}" aria-pressed="${(s.dl||[]).some(d=>d.m===m)}">${TICK}${e} ${esc(m)}</button>`).join("")}</div>
  ${(s.dl||[]).map((d,j)=>dlCard(s,k,d,j)).join("")}</div>
''' + s[j:]
rep('''  const dp=$("dp-"+k),ds=$("ds-"+k);''', '''  bindDl(s,k,el,redraw);
  const dp=$("dp-"+k),ds=$("ds-"+k);''')

# missing()
rep('if(!s.person&&!s.ship)m.push(`${n}: cómo lo entregas`);if(!shipOk(s))m.push(`${n}: costo de envío`);',
    'if(!(s.dl||[]).length)m.push(`${n}: cómo lo entregas`);(s.dl||[]).forEach(d=>{if(!dlOk(d))m.push(`${n}: entrega «${d.m}»`);});')
rep('if(famOf(x.u)==="paquete"&&!(+x.pkgP>0))', 'if(famOf(x.u)==="paquete"&&!(+x.pkgP>0)&&x.pkgP!=="sin")')

# sitio público
rep('''<div class="feat">${s.person?'<span>🙋 En persona</span>':''}${s.ship?`<span>${esc(shipText(s))}</span>`:''}''',
    '''<div class="feat">${(s.dl||[]).map(d=>`<span>${dlEmo(d.m)} ${esc(dlText(d))}</span>`).join("")}''')
# payload
rep('paqueteHoras:x.pkgH||null}))}))', 'paqueteHoras:x.pkgH||null})),entregas:(s.dl||[]).map(d=>({modalidad:d.m,descripcion:d.desc||null,cobra:d.cobra,unidad:d.u||null,tarifa:d.rate||null,zonas:dlMeth(d)==="zona"?d.z:null,unidadOtra:d.uo||null,metodoOtra:d.u==="Otro"?d.om:null,condiciones:d.conds}))}))')

# ---------- paquetes: sin límite ----------
rep('''<label>¿Para cuántas personas? <input type="number" min="1" class="sl-pkgP${MISS(+x.pkgP>0)}" value="${esc(x.pkgP)}"></label><label>¿Cuántas horas incluye? <input type="number" min="0" step="any" class="sl-pkgH" value="${esc(x.pkgH)}"> <span class="opt">(opcional)</span></label>''',
    '''<label>¿Para cuántas personas? <input type="number" min="1" class="sl-pkgP${MISS(+x.pkgP>0||x.pkgP==="sin")}" value="${x.pkgP==="sin"?"":esc(x.pkgP)}" ${x.pkgP==="sin"?"disabled placeholder=\'∞\'":""}><button type="button" class="chip sl-nolim" data-f="pkgP" aria-pressed="${x.pkgP==="sin"}">${TICK}Sin límite</button></label><label>¿Cuántas horas incluye? <input type="number" min="0" step="any" class="sl-pkgH" value="${x.pkgH==="sin"?"":esc(x.pkgH)}" ${x.pkgH==="sin"?"disabled placeholder=\'∞\'":""}><button type="button" class="chip sl-nolim" data-f="pkgH" aria-pressed="${x.pkgH==="sin"}">${TICK}Sin límite</button> <span class="opt">(opcional)</span></label>''')
rep('''   L.querySelector(".sl-rm").onclick=''', '''   L.querySelectorAll(".sl-nolim").forEach(b=>b.onclick=e=>{e.preventDefault();const f=b.dataset.f;x[f]=x[f]==="sin"?"":"sin";redraw();changed();});
   L.querySelector(".sl-rm").onclick=''')
rep('rinde:x.yieldP,pkgP:x.pkgP});', 'rinde:x.yieldP,pkgP:x.pkgP==="sin"?1e9:x.pkgP});')
rep('${+x.pkgP>0?` · ${esc(x.pkgP)} personas`:""}', '${+x.pkgP>0?` · ${esc(x.pkgP)} personas`:x.pkgP==="sin"?" · sin límite de personas":""}${x.pkgH==="sin"?" · horas ilimitadas":+x.pkgH>0?` · ${esc(x.pkgH)} h`:""}')

# ---------- zonas: a nivel nacional ----------
rep('''<option value="">Elige un estado…</option>${Object.keys(MX)''', '''<option value="">Elige un estado…</option><option value="__nac" ${z.state==="__nac"?"selected":""}>🇲🇽 A nivel nacional (toda la República)</option>${Object.keys(MX)''')
rep('''  ${z.state?`<div class="chips"><button type="button" class="chip" id="za-''', '''  ${z.state==="__nac"?`<span class="hint">✅ Atiendes en los 32 estados. No tienes que elegir municipios.</span>`:''}
  ${z.state&&z.state!=="__nac"?`<div class="chips"><button type="button" class="chip" id="za-''')
rep('const zonesOk=zs=>zs.some(z=>z.state&&(z.all||z.munis.length));', 'const zonesOk=zs=>zs.some(z=>z.state==="__nac"||(z.state&&(z.all||z.munis.length)));')
rep('const zonesText=zs=>zs.filter(z=>z.state).map(z=>z.all?', 'const zonesText=zs=>zs.some(z=>z.state==="__nac")?"Todo México 🇲🇽":zs.filter(z=>z.state).map(z=>z.all?')

rep('''<button type="button" class="link" id="zadd-${k}">+ Agregar otro estado</button>''','''<button type="button" class="link" id="zadd-${k}" ${zs.some(z=>z.state==="__nac")?"hidden":""}>+ Agregar otro estado</button>''')

# ---------- venue: montaje y entrada/salida ----------
rep('''  <span class="hint">📏 Estándar ¡HQV!: además de las horas de fiesta, ½ hora para montar y ½ hora para desmontar sin costo.</span>''',
    '''  <div class="vq"><span class="lbl" style="font-size:14px">🛠️ ¿Cuánto tiempo tiene tu cliente para hacer montajes?</span>
   <div class="row2"><input type="number" min="0" step="any" id="v-setn" value="${esc(v.setupN||"")}" placeholder="Ej. 2" aria-label="Tiempo de montaje"><select id="v-setu" aria-label="Unidad del tiempo de montaje">${["Horas","Días","Semanas","Meses"].map(u=>`<option ${(v.setupU||"Horas")===u?"selected":""}>${u}</option>`).join("")}</select></div>
   <span class="hint">Sujeto a disponibilidad.</span></div>
  <div class="vq"><span class="lbl" style="font-size:14px">🚪 ¿Cuánto tiempo ofreces para entrada y salida de asistentes?</span>
   <div class="row2"><input type="number" min="0" step="any" id="v-ion" value="${esc(v.ioN||"")}" placeholder="Ej. 30" aria-label="Tiempo de entrada y salida"><select id="v-iou" aria-label="Unidad del tiempo de entrada y salida">${["Minutos","Horas"].map(u=>`<option ${(v.ioU||"Minutos")===u?"selected":""}>${u}</option>`).join("")}</select>
    <div class="chips" style="width:fit-content;border-radius:99px">${[[0,"🎁 Gratis"],[1,"💲 Costo"]].map(([val,t])=>`<button type="button" class="chip vio" data-v="${val}" aria-pressed="${!!v.ioPaid===!!val}">${TICK}${t}</button>`).join("")}</div>
    ${v.ioPaid?`<input type="number" min="0" id="v-ioc" class="${MISS(filled(v.ioCost))}" value="${esc(v.ioCost||"")}" placeholder="$ ¿de cuánto?" aria-label="Costo de entrada y salida">`:""}</div></div>''')
rep('["v-tother","typeOther"],', '["v-tother","typeOther"],["v-setn","setupN"],["v-setu","setupU"],["v-ion","ioN"],["v-iou","ioU"],["v-ioc","ioCost"],')
rep(' document.querySelectorAll(".vm").forEach(', ' document.querySelectorAll(".vio").forEach(c=>c.onclick=()=>{v.ioPaid=c.dataset.v==="1";redraw();changed();});\n document.querySelectorAll(".vm").forEach(')
rep('hoursIncl:"5",extraHour:"1800",', 'hoursIncl:"5",extraHour:"1800",setupN:"2",setupU:"Horas",ioN:"30",ioU:"Minutos",ioPaid:false,ioCost:"",')
rep('hoursIncl:"5",extraHour:"",', 'hoursIncl:"5",extraHour:"",setupN:"",setupU:"Horas",ioN:"",ioU:"Minutos",ioPaid:false,ioCost:"",')
rep('${v.area?`<span>📐 ${esc(v.area)}</span>`:\'\'}', '${v.area?`<span>📐 ${esc(v.area)}</span>`:\'\'}${v.setupN?`<span>🛠️ Montaje: ${esc(v.setupN)} ${esc((v.setupU||"Horas").toLowerCase())} (sujeto a disponibilidad)</span>`:\'\'}${v.ioN?`<span>🚪 Entrada y salida: ${esc(v.ioN)} ${esc((v.ioU||"Minutos").toLowerCase())} · ${v.ioPaid?money(v.ioCost||0):"gratis"}</span>`:\'\'}')

DST.write_text(s)
print('ok reg9', len(s))
