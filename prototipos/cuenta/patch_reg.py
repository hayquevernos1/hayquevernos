import re,sys
s=open('src3.html').read()
def R(a,b,n=1):
    global s
    c=s.count(a);assert c==n,(a[:70],c);s=s.replace(a,b)
# catálogo compartido
R('<script>\n','<script src="catalogo.js"></script>\n<script>\n')
a=s.index('const VENUE_TYPES=[');b=s.index('const DOCS=[')
s=s[:a]+'const VENUE_TYPES=HQV.VENUE_TYPES,FEATURES=HQV.VENUE_FEATS,POLICY_SVCS=HQV.POLICY_CATS;\n'+s[b:]
# estado de ejemplo
a=s.index('  type:"Terraza",seated:"60"');b=s.index(' planner:{person:"Lupita')
s=s[:a]+'''  type:"Terraza",seated:"60",standing:"90",area:"51 a 60 m²",features:["techado","aire","fumar","luz","agua","refri","calle","ninos"],baths:{m:"1",w:"1",g:"1"},
  days:["jue","vie","sab","dom"],open:"12:00",limit:"23:00",hoursIncl:"5",extraHour:"1800",
  mode:"renta",rent:{price:"9000",per:"evento",upTo:"60",perExtraGuest:"150"},packages:[],adj:{day:{sab:"10"},daytime:"-10"},spaces:[{name:"Salón interior",price:"2500"}],negotiable:true,
  policy:{"Comida":{offer:"no",price:"",per:"evento",own:"si",fee:""},"Con alcohol":{offer:"no",price:"",per:"evento",own:"cuota",fee:"1500"},"Sin alcohol":{offer:"no",price:"",per:"evento",own:"si",fee:""},"Postres":{offer:"no",price:"",per:"evento",own:"si",fee:""},"Música":{offer:"costo",price:"3500",per:"evento",own:"no",fee:""},"Luz y show":{offer:"no",price:"",per:"evento",own:"si",fee:""},"Mobiliario":{offer:"inc",price:"",per:"evento",own:"si",fee:""},"Decoración":{offer:"no",price:"",per:"evento",own:"si",fee:""},"Staff":{offer:"no",price:"",per:"evento",own:"si",fee:""}},
  deposit:"50%",advance:"15",guarantee:"2000",cancel:"Reembolso del anticipo con 30 días de aviso",corkage:"$150 por botella",docs:["INE","Contrato firmado"],docsOther:"",docsNone:false,rulesText:"Volumen moderado después de las 22:00. Sin confeti.",rulesFile:null,promo:{has:false,what:"",terms:"",until:""},photos:[...sp("🌇","#FFC83D","#D6338A"),...sp("🌙","#2E1F4A","#7B2CBF")]},
'''+s[b:]
R('type:"",seated:"",standing:"",area:"",price:"",unit:"por bloque de 5 h",extra:"",hours:"",min:blankMin(),features:[],baths:{m:"",w:"",g:""},\n  policy:Object.fromEntries(POLICY_SVCS.map(([s])=>[s,{inc:false,ext:""}])),',
  'type:"",seated:"",standing:"",area:"",features:[],baths:{m:"",w:"",g:""},\n  days:[],open:"",limit:"",hoursIncl:"5",extraHour:"",mode:"",rent:{price:"",per:"evento",upTo:"",perExtraGuest:""},packages:[],adj:{day:{},daytime:""},spaces:[],negotiable:null,\n  policy:Object.fromEntries(POLICY_SVCS.map(([s])=>[s,{offer:"",price:"",per:"evento",own:"",fee:""}])),')
# validación
R('if(!v.area)m.push("Tamaño");if(!filled(v.price))m.push("Precio de renta");if(!filled(v.hours))m.push("Horario");if(!minOk(v.min))m.push("Mínimo de compra");',
  'if(!v.area)m.push("Tamaño");if(!v.days.length)m.push("Días que rentas");if(!filled(v.open)||!filled(v.limit))m.push("Horario");if(!(+v.hoursIncl>0))m.push("Horas incluidas");if(!filled(v.extraHour))m.push("Costo de hora extra");\n  if(!v.mode)m.push("Cómo cobras");if((v.mode==="renta"||v.mode==="ambos")&&!filled(v.rent.price))m.push("Precio de renta");if((v.mode==="paquetes"||v.mode==="ambos")&&!(v.packages.length&&v.packages.every(pkgOk)))m.push("Nombre y precio de cada paquete");if(v.negotiable===null)m.push("¿Precio negociable?");')
R('if(POLICY_SVCS.some(([s])=>!v.policy[s].ext))m.push("Si pueden traer de fuera (en cada servicio)");',
  'POLICY_SVCS.forEach(([sv])=>{if(!polOk(v.policy[sv]))m.push(`${sv}: si lo ofreces y si pueden traerlo`);});')
# nuevo drawVenue
a=s.index('function drawVenue(){');b=s.index('function drawPlanner(){')
s=s[:a]+open('v4/venue_draw.js').read()+'\n'+s[b:]
# vista del micrositio
R('''   <div class="ms-item-top"><b>Renta del espacio</b><span class="price">${filled(v.price)?`${money(v.price)} <small>${esc(v.unit)}</small>`:'<small>Por cotizar</small>'}</span></div>''',
  '''   ${venuePriceHtml(v)}''')
R('''${v.area?`<span>📐 ${esc(v.area)}</span>`:''}${v.hours?`<span>🕒 ${esc(v.hours)}</span>`:''}${v.extra?`<span>⏰ Hora extra ${money(v.extra)}</span>`:''}${minText(v.min)?`<span>🧾 ${esc(minText(v.min))}</span>`:''}''',
  '''${v.area?`<span>📐 ${esc(v.area)}</span>`:''}${v.days.length?`<span>🗓️ ${esc(v.days.map(d=>HQV.DAYS.find(x=>x[0]===d)[1]).join(" "))}</span>`:''}${v.limit?`<span>🕒 ${esc(v.open||"")}${v.open?" a ":"Hasta las "}${esc(v.limit)}</span>`:''}${v.hoursIncl?`<span>⏱️ ${esc(v.hoursIncl)} h de fiesta + ½ h montaje + ½ h desmontaje</span>`:''}${filled(v.extraHour)?`<span>⏰ Hora extra ${money(v.extraHour)}</span>`:''}${v.negotiable?'<span>🤝 Precio negociable</span>':''}''')
R('''<div class="ms-pol">${POLICY_SVCS.map(([s,e])=>{const p=v.policy[s];if(!p.inc&&!p.ext)return"";return`<span>${e} ${esc(s)} <span style="display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end">${p.inc?'<em class="st inc">Incluido</em>':''}${p.ext==="si"?'<em class="st ext">Puedes traerlo</em>':p.ext==="no"?'<em class="st no">No de fuera</em>':''}</span></span>`;}).join("")}</div>''',
  '''<div class="ms-pol">${POLICY_SVCS.map(([s,e])=>{const p=v.policy[s];if(!p.offer&&!p.own)return"";return`<span>${e} ${esc(s)} <span style="display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end">${p.offer==="inc"?'<em class="st inc">Incluido</em>':p.offer==="costo"?`<em class="st ext">Lo ofrece ${filled(p.price)?money(p.price)+(p.per==="persona"?" c/u":""):""}</em>`:''}${p.own==="si"?'<em class="st inc">Puedes traerlo</em>':p.own==="cuota"?`<em class="st ext">Traerlo: cuota ${money(p.fee)}</em>`:p.own==="no"?'<em class="st no">Solo con su gente</em>':''}</span></span>`;}).join("")}</div>''')
# helper de precio en el micrositio
R('function siteHtml(){','''function venuePriceHtml(v){const out=[];const isR=v.mode==="renta"||v.mode==="ambos",isP=v.mode==="paquetes"||v.mode==="ambos";
 if(isR)out.push(`<div class="ms-item-top"><b>Renta del espacio</b><span class="price">${filled(v.rent.price)?`${money(v.rent.price)} <small>${v.rent.per==="hora"?"por hora":v.rent.per==="persona"?"por persona":`por evento de ${esc(v.hoursIncl||5)} h`}</small>`:'<small>Por cotizar</small>'}</span></div>${filled(v.rent.upTo)?`<small style="color:var(--muted)">Incluye hasta ${esc(v.rent.upTo)} invitados${filled(v.rent.perExtraGuest)?` · invitado extra ${money(v.rent.perExtraGuest)}`:''}</small>`:''}`);
 if(isP)v.packages.filter(pkgOk).forEach(x=>out.push(`<div class="ms-item-top"><b>📦 ${esc(x.name)}</b><span class="price">${money(x.price)} <small>${x.per==="persona"?"por persona":"total"}</small></span></div><small style="color:var(--muted)">${filled(x.min)?`Desde ${esc(x.min)} invitados · `:''}${x.inc.length?"Incluye: "+esc(x.inc.join(", ")):""}</small>`));
 v.spaces.filter(x=>filled(x.name)).forEach(x=>out.push(`<div class="ms-item-top"><span>➕ ${esc(x.name)}</span><span class="price">${filled(x.price)?money(x.price):''}</span></div>`));
 return out.join("")||'<div class="ms-item-top"><b>Renta del espacio</b><span class="price"><small>Por cotizar</small></span></div>';}
function siteHtml(){''')
# CSS nuevo
R('.pol{display:grid;gap:6px}','''.pol{display:grid;gap:8px}
.pol2{border:1.5px solid var(--line);border-radius:12px;padding:10px;background:var(--paper);display:grid;gap:6px}
.pol2>b{font-size:14px}
.mini-l{font-size:12px;font-weight:700;color:var(--muted)}
.pkg{border:1.5px solid var(--line);border-radius:12px;padding:10px;background:var(--card);display:grid;gap:8px}
.dayadj{display:grid;grid-template-columns:repeat(auto-fill,minmax(78px,1fr));gap:6px}
.dayadj label{display:grid;gap:2px;font-size:12px;font-weight:700;color:var(--muted)}
.sp-row{grid-template-columns:minmax(0,1fr) 120px auto!important;align-items:center}
.stdbox{border:2px dashed var(--grape);border-radius:16px;padding:12px 14px;display:grid;gap:6px;background:var(--grape-soft)}
.stdrows{display:grid;gap:4px;font-size:13.5px}.stdrows>div{display:flex;justify-content:space-between;gap:8px}
.stdrows small{color:var(--muted)}''')
open('v4/reg_src.html','w').write(s)
print("ok")
