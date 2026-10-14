"""v15 · Registro (Diego, 14 oct 2026). reg9.html → reg10.html
- Catálogo v2 (catalogo_v2.js): 22 categorías homologadas; cada una con Servicio completo / Solo mi talento (staff) / Solo renta.
- Un solo motor por oferta: qué incluye (prellenado) · duración · tarifa duplicable con «alcanza para» · extras opcionales con costo.
- Catering: formatos (banquete, buffet, cóctel, estación, box lunch, barra de bebidas, coffee break, mesa de postres),
  tiempos/variedades opcionales con platillos predictivos, bebidas por tipo y forma de servir.
- Variabilidad ± (un campo, 20% recomendado) reemplaza «¿es negociable?» en servicios, venue y planner.
- Temporada alta: +% con calendario estándar editable.
- Pendientes: dirección del venue prellenada con la del negocio; «tiempo previo» para montajes; entrada y salida separadas
  (el costo es por el total); orden de Horario y precios; servicios del venue eligiendo categorías; anticipo del planner en
  horizontal; disclaimer de viáticos en la cobertura."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'reg9.html').read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:140]
    s = s.replace(a, b, count)


CSS = '''
/* ===== v15 · catálogo v2 ===== */
.dlc,.dlc .dlh,.dlc .dlh .sm,#svcList .box,#svcList .field,#svcList .field>*,.ofc{min-width:0}
.dlc.closed .dlh{overflow:hidden}.ofc .dlh .of-x{flex:0 0 auto}
.dlc .dlh .sm{flex:1 1 0}
.ways{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;border-radius:18px}
.way{display:flex;gap:10px;align-items:center;text-align:left;border:0;border-radius:20px;padding:12px 14px;background:#fff;box-shadow:var(--hqv-clay-sm,0 4px 12px rgba(65,20,95,.08));font:inherit;cursor:pointer;color:#1a1033}
.way .emo{font-size:26px}.way b{display:block;font-size:14.5px}.way small{display:block;font-size:12px;color:var(--muted);line-height:1.3}
.way[aria-pressed="true"]{background:linear-gradient(160deg,#9146FF,#FA1ED2);color:#fff}.way[aria-pressed="true"] small{color:rgba(255,255,255,.88)}
.chips.cmini .chip{font-size:12.5px;padding:6px 11px}
.ofc .mini-l{margin-top:4px}
.incr{display:grid;grid-template-columns:56px 1fr 1.3fr auto;gap:6px;align-items:center}
.incr.ex{grid-template-columns:56px 1fr 1.1fr 112px auto}
.incr input{min-width:0;padding:9px 10px;font-size:14px}
.incr .r-c{display:flex;align-items:center;gap:4px;font-weight:900;color:#8205B4}
.tmr{display:grid;grid-template-columns:120px auto 1fr auto;gap:6px;align-items:center}
.tmr input{min-width:0;padding:9px 10px;font-size:14px}
.tmr .yn button{padding:6px 10px;font-size:12px}
.durr{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.durr input{width:80px}.durr select{width:auto}
.tarr{display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:#F7F4FF;border-radius:16px;padding:8px 10px}
.tarr .sl-p{display:flex;align-items:center;gap:4px;font-weight:900;color:#8205B4}.tarr .sl-p input{width:110px}
.tarr select{width:auto;min-width:0;flex:0 1 auto}
.tarr .ta-uo{flex:1 1 140px}
.tarr .ta-al{font-size:12.5px;color:var(--muted);font-weight:700;display:flex;align-items:center;gap:4px}.tarr .ta-al input{width:64px;padding:6px 8px}
.tarr .ta-hv{flex-basis:100%}.tarr .rn{font-size:13.5px;min-width:120px}
.hv .pm,.pmv{background:#E6FFF4;color:#00684A;border-radius:99px;padding:1px 7px;font-weight:900;font-size:11.5px}
.newrow{display:flex;gap:8px}
.varr{display:flex;gap:12px;align-items:center;justify-content:space-between}
.varr .hint{font-size:12px}
.pmf{display:flex;align-items:center;gap:4px;font-weight:900;font-size:20px;color:#8205B4;flex:0 0 auto}.pmf input{width:76px;font-size:17px;font-weight:900;text-align:center}
.viat{display:block;margin:-6px 0 10px;background:#FFF7D6;border-radius:12px;padding:8px 11px;font-size:12.5px;color:#3A2E00}
.hrow{display:flex;gap:8px;align-items:center}.hrow input{flex:1 1 auto;min-width:0}.hrow select{flex:0 0 auto;width:auto}
.vq .row2 .lab{font-size:13px;font-weight:800;min-width:62px}
.plist .po{display:grid!important;gap:2px;justify-content:stretch!important}.plist .poh{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:baseline}
.plist .inc{display:block;font-size:11.5px;color:var(--muted);font-weight:600;margin-top:2px}
@media(max-width:560px){.incr,.incr.ex{grid-template-columns:48px 1fr 24px;grid-template-areas:"q u x" "w w w" "c c c"}.incr .r-q{grid-area:q}.incr .r-u{grid-area:u}.incr .r-x{grid-area:x}.incr .r-w{grid-area:w}.incr .r-c{grid-area:c}
.tmr{grid-template-columns:1fr auto 24px;grid-template-areas:"n s x" "d d d"}.tmr .t-n{grid-area:n}.tmr .sd{grid-area:s}.tmr .t-x{grid-area:x}.tmr .t-d{grid-area:d}
.ofc .dlh .of-x{white-space:nowrap}.varr{flex-direction:column;align-items:flex-start}}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

rep('<script src="catalogo_servicios.js"></script>', '<script src="catalogo_servicios.js"></script>\n<script src="catalogo_v2.js"></script>')
rep('const CATS=SVC.cats.map(c=>({n:c.n,e:c.e,s:c.s.map(([n,t,u])=>({n,t,u}))}));',
    'const CATS=SVC.cats.map(c=>({n:c.n,e:c.e,s:c.s.map(([n,t,u])=>({n,t,u}))}));\nconst C2=window.HQV_CAT2,CAT2=C2.cats;')
rep('const catOf=n=>CATS.find(c=>c.n===n);', 'const catOf=n=>CAT2.find(c=>c.n===n)||CATS.find(c=>c.n===n);')
rep('shipFreeFrom:"",dl:[],dlOpen:-1,min:blankMin()', 'shipFreeFrom:"",dl:[],dlOpen:-1,ways:{full:false,staff:false,rent:false},offers:[],staff:[],rent:[],open:"",descEdited:false,min:blankMin()')

# motor nuevo (antes de renderStep, después de todas las definiciones viejas: las funciones con el mismo nombre ganan)
js = (V / 'svc2.js').read_text()
POL_JS = r'''
/* Venue: los servicios se eligen por categoría (igual que el anfitrión) y luego se pregunta lo demás */
const POL_LABEL={"Comida":"Alimentos (catering)","Con alcohol":"Bebidas con alcohol","Sin alcohol":"Bebidas sin alcohol","Postres":"Postres y pastel","Música":"Música","Luz y show":"Audio, iluminación y show","Mobiliario":"Mobiliario y cristalería","Decoración":"Decoración y ambientación","Staff":"Staff (meseros, bartenders…)"};
function polSubs(x){const cat=n=>(CAT2.find(c=>c.n===n)||{});const drinks=a=>C2.bebidas.filter(b=>b.alc.includes(a)).map(b=>b.n);
 return({"Comida":["Banquete","Buffet","Cóctel","Estación","Box lunch"],"Con alcohol":drinks("Con alcohol"),"Sin alcohol":drinks("Sin alcohol"),"Postres":["Mesa de postres","Pastel","Mesa de dulces"],
  "Música":cat("Música").full,"Luz y show":cat("Audio, iluminación, foto y video").full,"Mobiliario":[...(cat("Mobiliario y montaje").rent||[]),...(cat("Cristalería y cubertería").rent||[])],"Decoración":cat("Decoración y ambientación").full,"Staff":cat("Catering").staff}[x]||[]).slice(0,14);}
function polCard(s,e,p,k){const subs=polSubs(s);const inc=p.incl&&p.incl!=="noinc";
 return`<div class="polc${MISS(polOk(p))}" data-s="${esc(s)}"><b>${e} ${esc(POL_LABEL[s]||s)}</b>
  <span class="q">¿Cómo lo ofreces?</span><div class="chips">${[["inc","✅ Incluido en tu renta o paquetes"],["parte","🟡 Incluido en parte"],["costo","💲 Con costo extra"]].map(([v,t])=>`<button type="button" class="chip p-in" data-v="${v}" aria-pressed="${p.incl===v}">${TICK}${t}</button>`).join("")}</div>
  ${p.incl==="parte"?`<input type="text" class="p-det" value="${esc(p.detail)}" placeholder="¿Qué parte incluye? Ej. 60 sillas y 6 mesas" aria-label="Detalle de lo incluido">`:""}
  ${p.incl==="costo"?`<div class="row"><input type="number" min="0" class="ppr" value="${esc(p.price)}" placeholder="$ precio" aria-label="Precio"><select class="pper" aria-label="Cómo lo cobras">${[["evento","por evento"],["persona","por persona"],["hora","por hora"]].map(([v,t])=>`<option value="${v}" ${p.per===v?"selected":""}>${t}</option>`).join("")}</select></div>`:""}
  ${p.incl&&subs.length?`<span class="q">¿Qué incluye? <span class="opt">(opcional)</span></span><div class="chips cmini">${subs.map(n=>`<button type="button" class="chip p-sub" data-n="${esc(n)}" aria-pressed="${(p.subs||[]).includes(n)}">${TICK}${esc(n)}</button>`).join("")}</div>`:""}
  ${p.incl?`<span class="q">¿El cliente puede traer su propio proveedor de esto?</span><div class="chips">${[["si","Sí"],["no","No"],["parcial","Parcial"],["otro","Otro"]].map(([v,t])=>`<button type="button" class="chip p-sb" data-v="${v}" aria-pressed="${p.subst===v}">${TICK}${t}</button>`).join("")}</div>
   ${p.subst==="otro"||p.subst==="parcial"?`<input type="text" class="p-sbo" value="${esc(p.substOther)}" placeholder="${p.subst==="parcial"?"¿Qué sí puede traer?":"Explícalo"}" aria-label="Detalle de sustitución">`:""}
   ${p.subst==="si"||p.subst==="parcial"?`<div class="chips">${[["libre","🆓 Libre"],["cuota","🎟️ Con cuota"],["otro","Otro"]].map(([v,t])=>`<button type="button" class="chip p-sm" data-v="${v}" aria-pressed="${p.substMode===v}">${TICK}${t}</button>`).join("")}</div>
    ${p.substMode==="cuota"?`<div class="row"><input type="number" min="0" class="pfee" value="${esc(p.fee)}" placeholder="$ cuota" aria-label="Cuota"><select class="pfu" aria-label="Unidad de la cuota">${["evento","persona","botella","hora"].map(u=>`<option value="${u}" ${p.feeUnit===u?"selected":""}>por ${u}</option>`).join("")}</select></div><input type="text" class="pfn" value="${esc(p.feeNote)}" placeholder="Nota: descorche, derecho de piso… (opcional)" aria-label="Nota de la cuota">`:""}
    ${p.substMode==="otro"?`<input type="text" class="pmo" value="${esc(p.modeOther)}" placeholder="Explícalo" aria-label="Otra condición">`:""}`:""}`:""}
  ${inc||p.incl===""?"":""}</div>`;}
'''
rep('function drawServices(){const list=$("svcList");if(!list)return;\n list.innerHTML=S.services.map((s,i)=>{const cat=catOf(s.cat),k="s"+i', 'function drawServicesOld(){const list=$("svcList");if(!list)return;\n list.innerHTML=S.services.map((s,i)=>{const cat=catOf(s.cat),k="s"+i')
rep('function drawSvcStep(){const sc=S.svcScope=S.svcScope||{S:false,E:false};\n $("stepBody").innerHTML=`<div class="panel"><span class="crumb">Mi negocio › Servicios</span><h2>Mis servicios 🎉</h2><p class="sub">Pon el precio como tú lo cobras. Nosotros se lo mostramos al anfitrión por persona y en total.</p>\n <div class="svc-top">\n  <div class="field"><span class="lbl">¿Para qué tipo de eventos? <span class="opt">Puedes elegir los dos</span></span><div class="chips${MISS(sc.S||sc.E)}" style="width:fit-content;border-radius:99px"><button type="button" class="chip scp" data-v="S" aria-pressed="${!!sc.S}">${TICK}🎉 Sociales</button><button type="button" class="chip scp" data-v="E" aria-pressed="${!!sc.E}">${TICK}💼 Empresariales</button></div></div>\n  <div class="field qwrap"><label class="lbl" for="svcQ">🔎 Busca lo que ofreces <span class="opt">o elige abajo por categoría</span></label><input type="search" id="svcQ" autocomplete="off" placeholder="Ej. taquiza', 'function drawSvcStepOld(){const sc=S.svcScope=S.svcScope||{S:false,E:false};\n $("stepBody").innerHTML=`<div class="panel"><span class="crumb">Mi negocio › Servicios</span><h2>Mis servicios 🎉</h2><p class="sub">Pon el precio como tú lo cobras. Nosotros se lo mostramos al anfitrión por persona y en total.</p>\n <div class="svc-top">\n  <div class="field"><span class="lbl">¿Para qué tipo de eventos? <span class="opt">Puedes elegir los dos</span></span><div class="chips${MISS(sc.S||sc.E)}" style="width:fit-content;border-radius:99px"><button type="button" class="chip scp" data-v="S" aria-pressed="${!!sc.S}">${TICK}🎉 Sociales</button><button type="button" class="chip scp" data-v="E" aria-pressed="${!!sc.E}">${TICK}💼 Empresariales</button></div></div>\n  <div class="field qwrap"><label class="lbl" for="svcQ">🔎 Busca lo que ofreces <span class="opt">o elige abajo por categoría</span></label><input type="search" id="svcQ" autocomplete="off" placeholder="Ej. taquiza')
rep('function polCard(s,e,p,k){const cat=POL_MAP[s]', 'function polCardOld(s,e,p,k){const cat=POL_MAP[s]')
rep('const C2=window.HQV_CAT2,CAT2=C2.cats;', 'const C2=window.HQV_CAT2,CAT2=C2.cats;\n' + js + '\n' + POL_JS)

# ---------- missing(): servicios con el motor nuevo; venue y planner con variabilidad
a = s.index('  S.services.forEach((s,i)=>{const n=catOf(s.cat)?s.cat:`Ficha ${i+1}`;')
b = s.index('  if(!zonesOk(S.svcZones))', a)
s = s[:a] + r'''  S.services.forEach((s,i)=>{svcDefaults(s);const n=catOf(s.cat)?s.cat:`Ficha ${i+1}`;
  if(!s.cat||s.cat==="__new"){m.push(`${n}: categoría`);return;}
  if(!s.ways.full&&!s.ways.staff&&!s.ways.rent)m.push(`${n}: cómo trabajas`);
  if(s.ways.full){if(!s.offers.length)m.push(`${n}: qué ofreces`);s.offers.forEach(o=>{if(!offerOk(o))m.push(`${n}: tarifa de ${o.n}`);});}
  if(s.ways.staff){if(!s.staff.length)m.push(`${n}: perfiles de staff`);else if(!s.staff.every(staffOk))m.push(`${n}: precio del staff`);}
  if(s.ways.rent){if(!s.rent.length)m.push(`${n}: qué rentas`);else if(!s.rent.every(staffOk))m.push(`${n}: precio de renta`);}
  if(s.subs.length){if(!filled(s.desc))m.push(`${n}: descripción`);if(!(s.dl||[]).length)m.push(`${n}: cómo lo entregas`);(s.dl||[]).forEach(d=>{if(!dlOk(d))m.push(`${n}: entrega «${d.m}»`);});
  if(!minOk(s.min))m.push(`${n}: mínimo de compra`);if(!promoOk(s.promo))m.push(`${n}: promoción`);}});
  if(!filled(S.svcVar))m.push("Cuánto puede variar tu precio");
''' + s[b:]
rep('if(v.negotiable===null)m.push("¿Precio negociable?");', 'if(!filled(v.var))m.push("Cuánto puede variar tu precio");')
rep('if(p.negotiable===null||p.negotiable===undefined)m.push("¿Costos negociables?");', 'if(!filled(p.var))m.push("Cuánto pueden variar tus costos");')

# ---------- ensureState: valores nuevos, variabilidad → negociable, servicios del venue elegidos
rep(' p.fee=p.fees[0]?p.fees[0].amount:"";v.deposit=', ''' if(v.var===undefined)v.var=v.negotiable===false?"0":"20";v.negotiable=+v.var>0;if(p.var===undefined)p.var=p.negotiable===false?"0":"20";p.negotiable=+p.var>0;
 if(v.inN===undefined){v.inN=v.ioN||"";v.inU=v.ioU||"Minutos";v.outN=v.ioN||"";v.outU=v.ioU||"Minutos";}
 if(!v.polSel)v.polSel=POLICY_SVCS.map(([x])=>x).filter(x=>v.policy[x].incl&&v.policy[x].incl!=="noinc");
 POLICY_SVCS.forEach(([x])=>{if(!v.polSel.includes(x)){v.policy[x].incl="noinc";syncPol(v.policy[x],v.extAll);}});
 if(S.svcVar===undefined)S.svcVar="20";if(!S.svcHigh)S.svcHigh={pct:"15",months:HIGH_STD.slice()};
 S.services.forEach(x=>{svcDefaults(x);syncSubs(x);});
 p.fee=p.fees[0]?p.fees[0].amount:"";v.deposit=''')

# ---------- demo
rep(' return x;};\n\nfunction emptyState(){', r''' {const s0=x.services[0];Object.assign(s0,{cat:"Catering",ways:{full:true,staff:true,rent:false},open:"",descEdited:true,
  offers:[Object.assign(blankOffer("Mesa de postres y pastel"),{gas:["Mexicana"],tiempos:[{n:"Variedad 1",k:"Dulce",d:"Galletas decoradas"},{n:"Variedad 2",k:"Dulce",d:"Cupcakes"},{n:"Variedad 3",k:"Dulce",d:"Gelatinas artísticas"}],tar:[{price:"3500",u:"Por paquete",uo:"",alc:"50"},{price:"75",u:"Por persona",uo:"",alc:""}],ext:[{q:"1",u:"pastel",w:"de 3 pisos",cost:"1800"}]}),
   Object.assign(blankOffer("Estación"),{gas:["Mexicana"],tiempos:[{n:"Variedad 1",k:"Salado",d:"Tacos al pastor"},{n:"Variedad 2",k:"Salado",d:"Esquites"}],tar:[{price:"1200",u:"Por hora",uo:"",alc:""}]})],
  staff:[{n:"Meseros",price:"350",u:"Por hora",min:"5"}],rent:[]});}
 x.svcVar="20";x.svcHigh={pct:"15",months:["may","jun","oct","nov","dic"]};
 v.inN="45";v.inU="Minutos";v.outN="30";v.outU="Minutos";v.ioPaid=true;v.ioCost="800";v.var="15";p.var="10";
 return x;};

function emptyState(){''')

# ---------- servicios en el sitio público
rep('''<div class="plist">${s.subs.map(x=>`<span>${esc(x.n)} <span class="price">${filled(x.price)&&x.u?priceTxt(x):'<small>Por cotizar</small>'}</span></span>`).join("")}</div>''',
    '''<div class="plist">${svcPlist(s)}</div>''')
rep('''${zonesText(S.svcZones)?`<small style="color:var(--muted);font-size:12px">🗺️ Servicio en: ${esc(zonesText(S.svcZones))}</small>`:''}''',
    '''${zonesText(S.svcZones)?`<small style="color:var(--muted);font-size:12px">🗺️ Servicio en: ${esc(zonesText(S.svcZones))}</small>`:''}${S.svcHigh&&+S.svcHigh.pct>0&&S.svcHigh.months.length?`<small style="color:var(--muted);font-size:12px">🔥 Temporada alta (${esc(S.svcHigh.months.map(m=>MONTHS.find(x=>x[0]===m)[1]).join(", "))}): +${esc(S.svcHigh.pct)}%</small>`:""}''')
rep("""${p.negotiable?'<span>🤝 Precios negociables</span>':""}""", """${+p.var>0?`<span>🤝 Negociable ± ${esc(p.var)}%</span>`:""}""")
rep("""${v.negotiable?'<span>🤝 Precio negociable</span>':''}""", """${+v.var>0?`<span>🤝 Negociable ± ${esc(v.var)}%</span>`:''}""")
rep('''${v.ioN?`<span>🚪 Entrada y salida: ${esc(v.ioN)} ${esc((v.ioU||"Minutos").toLowerCase())} · ${v.ioPaid?money(v.ioCost||0):"gratis"}</span>`:''}''',
    '''${v.inN||v.outN?`<span>🚪 Entrada ${esc(v.inN||"0")} ${esc((v.inU||"Minutos").toLowerCase())} · salida ${esc(v.outN||"0")} ${esc((v.outU||"Minutos").toLowerCase())} · ${v.ioPaid?money(v.ioCost||0)+" por el total":"gratis"}</span>`:''}''')
rep('${v.setupN?`<span>🛠️ Montaje: ${esc(v.setupN)}', '${v.setupN?`<span>🛠️ Montaje previo: ${esc(v.setupN)}')
rep('${v.hoursIncl?`<span>⏱️ ${esc(v.hoursIncl)} h de fiesta + ½ h montaje + ½ h desmontaje</span>`:\'\'}', '${v.hoursIncl?`<span>⏱️ ${esc(v.hoursIncl)} h de fiesta</span>`:\'\'}')
# payload
rep('entregas:(s.dl||[]).map(', 'modos:s.ways,ofertas:s.offers,staff:s.staff,renta:s.rent,entregas:(s.dl||[]).map(')
rep('servicios:S.services.map(', 'variabilidad:S.svcVar,temporadaAlta:S.svcHigh,servicios:S.services.map(')
# datalists predictivos
rep('<datalist id="dlCats">', '''<datalist id="dlFull">${[...new Set(CAT2.flatMap(c=>c.full))].sort().map(n=>`<option value="${esc(n)}">`).join("")}</datalist>
<datalist id="dlStaff">${[...new Set(CAT2.flatMap(c=>c.staff))].sort().map(n=>`<option value="${esc(n)}">`).join("")}</datalist>
<datalist id="dlSalado">${DISH_LIST.Salado.map(n=>`<option value="${esc(n)}">`).join("")}</datalist>
<datalist id="dlDulce">${DISH_LIST.Dulce.map(n=>`<option value="${esc(n)}">`).join("")}</datalist>
<datalist id="dlDrinks">${DRINK_VARS.map(n=>`<option value="${esc(n)}">`).join("")}</datalist>
<datalist id="dlIncU">${["tiempos","piezas","platillos","guisados","guarniciones","meseros","bartenders","horas","litros","kilos","cajas","bebidas","variedades","personas","mesas","sillas","bocadillos","estaciones","canciones","fotos","invitaciones"].map(n=>`<option value="${n}">`).join("")}</datalist>
<datalist id="dlCats">''')

# ---------- venue
rep('function drawVenue(){const v=S.venue,k="v",b=S.biz;',
    'function drawVenue(){const v=S.venue,k="v",b=S.biz;if(!v.addrTouched&&!addrOk(v.addr)&&addrOk(b.addr)){v.addr=JSON.parse(JSON.stringify(b.addr));v.addrFromBiz=true;}')
rep('${addrHtml(v.addr,"v","Dirección del lugar")}',
    '${v.addrFromBiz?`<div class="alert info" style="margin-bottom:-6px">📍 <span>Pusimos la dirección de tu negocio. Si tu venue está en otro lugar, cámbiala aquí.</span></div>`:""}${addrHtml(v.addr,"v","Dirección del lugar")}')
rep('bindAddr(v.addr,"v",redraw);', 'bindAddr(v.addr,"v",redraw);document.querySelectorAll("#stepBody input,#stepBody select").forEach(x=>{if(/^a[a-z]{1,3}-v$/.test(x.id||""))x.addEventListener("input",()=>{v.addrTouched=true;});});')
a = s.index('  <div class="vq"><span class="lbl" style="font-size:14px">🛠️')
bb = s.index('  <span class="lbl" style="font-size:14px">💲 ¿Cómo cobras?', a)
c = s.index('  <span class="hint">¿Tu precio es negociable?', bb)
d = s.index('\n', c) + 1
cobras = s[bb:c]
newvq = r'''  <div class="vq"><span class="lbl" style="font-size:14px">🛠️ ¿Cuánto tiempo previo tiene tu cliente para hacer montajes?</span>
   <div class="row2"><input type="number" min="0" step="any" id="v-setn" value="${esc(v.setupN||"")}" placeholder="Ej. 2" aria-label="Tiempo previo de montaje"><select id="v-setu" aria-label="Unidad del tiempo de montaje">${["Horas","Días","Semanas","Meses"].map(u=>`<option ${(v.setupU||"Horas")===u?"selected":""}>${u}</option>`).join("")}</select></div>
   <span class="hint">Sujeto a disponibilidad.</span></div>
  <div class="vq"><span class="lbl" style="font-size:14px">🚪 ¿Cuánto tiempo ofreces para entrada y salida de asistentes?</span>
   <div class="row2"><span class="lab">Entrada</span><input type="number" min="0" step="any" id="v-inn" value="${esc(v.inN||"")}" placeholder="Ej. 45" aria-label="Tiempo de entrada"><select id="v-inu" aria-label="Unidad del tiempo de entrada">${["Minutos","Horas"].map(u=>`<option ${(v.inU||"Minutos")===u?"selected":""}>${u}</option>`).join("")}</select></div>
   <div class="row2"><span class="lab">Salida</span><input type="number" min="0" step="any" id="v-outn" value="${esc(v.outN||"")}" placeholder="Ej. 30" aria-label="Tiempo de salida"><select id="v-outu" aria-label="Unidad del tiempo de salida">${["Minutos","Horas"].map(u=>`<option ${(v.outU||"Minutos")===u?"selected":""}>${u}</option>`).join("")}</select></div>
   <div class="row2"><div class="chips" style="width:fit-content;border-radius:99px">${[[0,"🎁 Gratis"],[1,"💲 Con costo"]].map(([val,t])=>`<button type="button" class="chip vio" data-v="${val}" aria-pressed="${!!v.ioPaid===!!val}">${TICK}${t}</button>`).join("")}</div>
    ${v.ioPaid?`<input type="number" min="0" id="v-ioc" class="${MISS(filled(v.ioCost))}" value="${esc(v.ioCost||"")}" placeholder="$ ¿de cuánto?" aria-label="Costo de entrada y salida">`:""}</div>
   ${v.ioPaid?`<span class="hint">El costo es por el total del tiempo de entrada y salida juntos.</span>`:""}</div>
  <div class="varr"><span><b>¿Cuánto puede variar tu precio al negociar?</b><span class="hint" style="display:block">El anfitrión ve precios estandarizados. Este margen es tu responsabilidad. Recomendamos <b>±20%</b>.</span></span><label class="pmf"><span>±</span><input type="number" min="0" max="100" id="v-var" class="${MISS(filled(v.var))}" value="${esc(v.var)}" aria-label="Variabilidad del precio"><span>%</span></label></div>
'''
s = s[:a] + cobras + newvq + s[d:]
rep('["v-ion","ioN"],["v-iou","ioU"],', '["v-inn","inN"],["v-inu","inU"],["v-outn","outN"],["v-outu","outU"],')
rep('["v-extn","extAllNote"]].forEach(([i,f])=>{const el=$(i);if(el)', '["v-extn","extAllNote"]].forEach(([i,f])=>{const el=$(i);if(el)')
rep(' $("v-guar").onchange=()=>redraw();', ' const vv=$("v-var");if(vv)vv.oninput=e=>{v.var=e.target.value;v.negotiable=+v.var>0;ch();};\n $("v-guar").onchange=()=>redraw();')
# servicios del venue: primero se eligen
rep(' const pol=POLICY_SVCS.map(([x,e])=>polCard(x,e,v.policy[x],k)).join("");',
    ' const pol=POLICY_SVCS.filter(([x])=>(v.polSel||[]).includes(x)).map(([x,e])=>polCard(x,e,v.policy[x],k)).join("");')
rep('''<span class="hint">Para cada servicio dinos si está incluido y si el cliente puede traer a su propio proveedor. Así solo te llegan fiestas que sí puedes atender.</span><div style="display:grid;gap:10px">${pol}</div>''',
    '''<span class="hint">Toca solo los servicios que ofreces en tu venue (incluidos o con costo). Luego te preguntamos los detalles. Así solo te llegan fiestas que sí puedes atender.</span>
  <div class="chips" style="border-radius:14px">${POLICY_SVCS.map(([x,e])=>`<button type="button" class="chip vps" data-s="${esc(x)}" aria-pressed="${(v.polSel||[]).includes(x)}">${TICK}${e} ${esc(POL_LABEL[x]||x)}</button>`).join("")}</div>
  <div style="display:grid;gap:10px">${pol}</div>''')
rep('<b>🚪 ¿Todos los servicios que no incluyes los puede traer el cliente con proveedores externos?</b>',
    '<b>🚪 ¿Los servicios que no ofreces los puede traer el cliente con proveedores externos?</b>')
rep(' document.querySelectorAll(".p-ext").forEach(', ''' document.querySelectorAll(".vps").forEach(c=>c.onclick=()=>{const x=c.dataset.s,P=v.policy[x];v.polSel=v.polSel.includes(x)?v.polSel.filter(y=>y!==x):[...v.polSel,x];if(v.polSel.includes(x)){if(P.incl==="noinc")P.incl="";}else P.incl="noinc";syncPol(P,v.extAll);redraw();changed();});
 document.querySelectorAll(".p-ext").forEach(''')

# ---------- planner: anticipo en horizontal, variabilidad abajo, viáticos
a = s.index('<div class="row"><div class="field"><span class="lbl">💳 Anticipo para apartar</span><div class="row"><input type="number" min="0" id="pl-depn"')
b = s.index('\n <div class="field"><span class="lbl">⭐ Me especializo en</span>', a)
s = s[:a] + r'''<div class="field"><span class="lbl">💳 Anticipo para apartar</span><div class="hrow"><input type="number" min="0" id="pl-depn" class="${MISS(filled(p.depositN))}" value="${esc(p.depositN)}" placeholder="Ej. 30" aria-label="Anticipo"><select id="pl-depu" aria-label="Unidad del anticipo"><option value="%" ${p.depositU==="%"?"selected":""}>% del total</option><option value="$" ${p.depositU==="$"?"selected":""}>pesos ($)</option></select></div></div>
 <div class="field"><div class="varr"><span><b>🤝 ¿Cuánto pueden variar tus costos al negociar?</b><span class="hint" style="display:block">Pon 0 si es precio fijo. Recomendamos <b>±20%</b>; el margen es tu responsabilidad.</span></span><label class="pmf"><span>±</span><input type="number" min="0" max="100" id="pl-var" class="${MISS(filled(p.var))}" value="${esc(p.var)}" aria-label="Variabilidad de tus costos"><span>%</span></label></div></div>''' + s[b:]
rep('[["pl-name","person"],["pl-since","since"],["pl-bio","bio"],["pl-depn","depositN"],["pl-depu","depositU"]].forEach(([i,f])=>{$(i).oninput=$(i).onchange=e=>{p[f]=e.target.value;changed();};});',
    '[["pl-name","person"],["pl-since","since"],["pl-bio","bio"],["pl-depn","depositN"],["pl-depu","depositU"],["pl-var","var"]].forEach(([i,f])=>{$(i).oninput=$(i).onchange=e=>{p[f]=e.target.value;p.negotiable=+p.var>0;changed();};});')
rep('${zonesHtml(p.zones,"pl","¿Dónde trabajas como planner?")}', '${zonesHtml(p.zones,"pl","¿Dónde trabajas como planner?")}${VIATICOS}')

(V / 'reg10.html').write_text(s)
print('ok reg10', len(s))
