"""v13 · Cotizador (Diego, 9 oct 2026). cot8.html → cot9.html
- El event planner ya NO se pregunta al inicio: se ofrece en la cuenta, después de entregar la pre-cotización.
- Navegación: etapas de arriba clicables + «← Atrás» y «Adelante →» arriba. Botón principal lima.
- Lugar (ya tengo): sin «Techado» ni «Área al aire libre» en ¿Con qué cuenta? (ya se preguntó en «El espacio es…»).
- Servicios: «Lo pongo yo y/o proveedor externo». Precios = promedio de la comunidad ¡Hay que vernos!.
- Presupuesto: «¡Felicitaciones!», solo «Promedio de la comunidad», disclaimer discreto en cada servicio.
- Detalles (para todos): proceso de pago (sigo a los proveedores / defino anticipos y liquidaciones) + cómo pagar + leyenda.
- Nueva última pantalla «¿Quieres agregar algo? Explícame aquí.» (máx. 500 caracteres).
- Carga de una pre-cotización guardada para editarla (mensaje «cargar» desde la cuenta) y envío del estado completo."""
from pathlib import Path
SRC = Path('/home/claude/hqv/v5/cot8.html')
DST = Path('/home/claude/hqv/v5/cot9.html')
s = SRC.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:120]
    s = s.replace(a, b, count)


CSS = '''
/* ===== v13 · cotizador ===== */
.stages{grid-template-columns:repeat(6,1fr)!important}
.stages span.go{cursor:pointer}
.stages span.go:hover i{text-decoration:underline}
.tnav{display:flex;justify-content:space-between;gap:8px;margin-top:6px}
.tnav button{border:0;background:rgba(255,255,255,.75);border-radius:99px;padding:6px 12px;font-weight:900;font-size:13px;color:#1a1033;box-shadow:var(--hqv-clay-sm)}
.tnav button[disabled]{opacity:.35}
.disc{font-size:11px;color:var(--muted);line-height:1.35}
.payrow{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.payrow input{flex:0 0 96px}.payrow select{flex:0 0 150px}
.payrow b{font-size:13px;min-width:92px}
.paylegend{background:#FFF7D6;border-radius:16px;padding:10px 12px;font-size:13px;font-weight:700}
.xtra textarea{width:100%;min-height:150px;border-radius:18px;border:1.5px solid var(--line);padding:12px;font:inherit;resize:vertical}
.xtra .cnt{justify-self:end;font-size:12px;color:var(--muted)}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# ---------- estado: sin pregunta de planner; nuevos campos
rep('fact:{docs:[],docsOther:[],days:"",reqDate:"",terms:"",method:[],methodOther:[],biz:""},wantPlanner:null,planners:[],',
    'fact:{docs:[],docsOther:[],days:"",reqDate:"",terms:"",method:[],methodOther:[],biz:""},wantPlanner:false,planners:[],\n pay:{mode:"",ant:[{n:"",u:"porcentaje"}],liq:[{n:"",u:"porcentaje"}],how:[],howOther:""},extra:"",maxStage:0,')
rep('const STAGES=["fiesta","lugar","servicios","presupuesto","detalles"];',
    'const STAGES=["fiesta","lugar","servicios","presupuesto","detalles","extra"];')

# ---------- Tu fiesta: se quita el bloque del event planner
a = s.index('<div class="field"><span class="lbl">📋 ¿Quieres la ayuda de un event planner?</span>')
b = s.index('${S.wantPlanner===false||pl?`')
s = s[:a] + s[b:]

# ---------- etapas clicables + atrás / adelante arriba
rep('''$("stages").innerHTML=STAGES.map((s,j)=>`<span class="${screen==="result"||j<i?'done':j===i?'on':''}"><i>${["Tu fiesta","Lugar","Servicios","Presupuesto","Detalles"][j]}</i></span>`).join("");''',
    '''if(i>S.maxStage)S.maxStage=i;
 $("stages").innerHTML=STAGES.map((s,j)=>`<span class="${screen==="result"||j<i?'done':j===i?'on':''}${j!==i&&j<=S.maxStage?' go':''}" ${j!==i&&j<=S.maxStage?`data-st="${s}" role="button" tabindex="0"`:''}><i>${["Tu fiesta","Lugar","Servicios","Presupuesto","Detalles","Algo más"][j]}</i></span>`).join("");$("tnav").innerHTML=screen==="result"||i<0?"":`<button type="button" id="tBack" ${i<=0?"disabled":""}>← Atrás</button><button type="button" id="tFwd" ${i>=S.maxStage?"disabled":""}>Adelante →</button>`;
 $("stages").querySelectorAll("[data-st]").forEach(x=>x.onclick=()=>{showMiss=false;go(x.dataset.st);});
 const tb=$("tBack"),tf=$("tFwd");if(tb)tb.onclick=()=>{showMiss=false;go(STAGES[Math.max(0,i-1)]);};if(tf)tf.onclick=()=>{showMiss=false;go(STAGES[Math.min(S.maxStage,i+1)]);};''')
rep('<div class="stages" id="stages" aria-hidden="true"></div>', '<div class="stages" id="stages"></div><div class="tnav" id="tnav"></div>')
# botón principal lima
rep('''<button class="btn ${n?'off':''}" type="button" id="next"''', '''<button class="btn cta ${n?'off':''}" type="button" id="next"''')

# ---------- Lugar: quitar Techado / Área al aire libre de «¿Con qué cuenta?»
rep('''${FEATURES.map(([id,e,t])=>`<button type="button" class="chip pf"''',
    '''${FEATURES.filter(x=>!["techado","aire"].includes(x[0])).map(([id,e,t])=>`<button type="button" class="chip pf"''')

# ---------- Servicios
rep('🙋 Lo llevo yo</button>', '🙋 Lo pongo yo y/o proveedor externo</button>')
rep('<span class="mkt">💡 Los precios son el promedio del mercado en tu zona.</span>',
    '<span class="mkt">💡 Precios promedio de la comunidad de proveedores de ¡Hay que vernos! en tu zona.</span>')

# ---------- Presupuesto
rep('<b>Premio por anticipación:</b> como estás reservando con ${daysTo()} días de anticipación, tu promedio es ${pct}% más bajo que el del mercado. ¡Así se planea una fiesta!',
    '<b>¡Felicitaciones!</b> Como estás organizando con ${daysTo()} días de anticipación, tu promedio es ${pct}% más bajo. ¡Así se planea una fiesta!')
rep('''$("av-"+r.k).innerHTML=pct?`Promedio del mercado <s>${money(r.mkt/S.guests)}</s> · <b>tu promedio ${money(r.avg/S.guests)}</b> por persona`:`Promedio del mercado: ${money(r.avg/S.guests)} por persona`;''',
    '''$("av-"+r.k).innerHTML=`Promedio de la comunidad ¡Hay que vernos!: <b>${money(r.avg/S.guests)}</b> por persona`;''')
rep('["mid","⭐ En el promedio del mercado"]', '["mid","⭐ En el promedio de la comunidad"]')
rep('''<div class="lvl-row"><span class="lvl" id="l-${esc(r.k)}"></span>${r.set?'':`<button type="button" class="link-btn useavg" data-k="${esc(r.k)}">Usar el promedio</button>`}</div></div>`).join("")}</div>''',
    '''<div class="lvl-row"><span class="lvl" id="l-${esc(r.k)}"></span>${r.set?'':`<button type="button" class="link-btn useavg" data-k="${esc(r.k)}">Usar el promedio</button>`}</div><span class="disc">Cálculo basado en el promedio del histórico de precios publicados/pagados por los proveedores/anfitriones de la comunidad ¡Hay que vernos!.</span></div>`).join("")}</div>''')
rep('''${navHtml("presupuesto",needInvoice()?"Siguiente →":"Ver mi fiesta 🎉")}</div>`;''', '''${navHtml("presupuesto")}</div>`;''')
rep('''drawBudgetAmounts();bindNav("presupuesto","servicios",needInvoice()?"detalles":"result");return;}''',
    '''drawBudgetAmounts();bindNav("presupuesto","servicios","detalles");return;}''')

# ---------- Detalles: condiciones de pago para todos
rep('''   <span class="mini-l">¿Cómo y cuándo pagas?</span><div class="chips${MISS(!!S.fact.terms)}">${["Anticipo y liquidación el día del evento","Pago a 15 días","Pago a 30 días","Pago a 60 días"].map(t=>`<button type="button" class="chip ft2" aria-pressed="${S.fact.terms===t}">${esc(t)}</button>`).join("")}</div>
   <div class="chips${MISS(S.fact.method.length>0)}">${["Transferencia","Tarjeta corporativa","Cheque"].map(t=>`<button type="button" class="chip fm" aria-pressed="${S.fact.method.includes(t)}">${esc(t)}</button>`).join("")}</div>${othList("fm","Otra forma de pago")}</div>`:''}
  ${navHtml("detalles","Ver mi fiesta 🎉")}</div>`;''',
    '''   </div>`:''}
  ${payHtml()}
  ${navHtml("detalles")}</div>`;
  bindPay(el);''')
rep('''if(!f.terms)m.push("Condiciones de pago");if(!f.method.length&&!f.methodOther.some(filled))m.push("Forma de pago");}''',
    '''}const P=S.pay;if(!P.mode)m.push("Proceso de pago");if(P.mode==="mine"&&!P.ant.concat(P.liq).some(x=>filled(x.n)))m.push("Tus anticipos o liquidaciones");if(!P.how.length)m.push("¿Cómo te gustaría pagar?");if(P.how.includes("Otro")&&!filled(P.howOther))m.push("Otra forma de pago");''')
rep('''bindNav("detalles","presupuesto","result");return;}''',
    '''bindNav("detalles","presupuesto","extra");return;}
 if(screen==="extra"){el.innerHTML=`<div class="card xtra">${say("¿Quieres agregar algo? Explícame aquí. ✍️")}
  <span class="hint">Lo que no te preguntamos y quieres que sepan tus proveedores: ideas, temática, restricciones, sorpresas… (opcional)</span>
  <textarea id="xt" maxlength="500" placeholder="Ej. Es sorpresa para mi mamá: que nadie le escriba directo. Queremos temática años 80.">${esc(S.extra)}</textarea><span class="cnt" id="xc">${S.extra.length}/500</span>
  ${navHtml("extra","Ver mi fiesta 🎉")}</div>`;
  $("xt").oninput=e=>{S.extra=e.target.value.slice(0,500);$("xc").textContent=S.extra.length+"/500";};
  bindNav("extra","detalles","result");return;}''')

# ---------- funciones de pago
PAY = r'''
/* v13 · condiciones y formas de pago */
const PAY_UNITS=["porcentaje","horas","días","semanas","meses"];
function payRows(k,lab){return S.pay[k].map((x,i)=>`<div class="payrow"><b>${lab} ${i+1}</b><input type="number" min="0" data-pn="${k}|${i}" value="${esc(x.n)}" placeholder="Número" aria-label="${lab} ${i+1}"><select data-pu="${k}|${i}" aria-label="Unidad">${PAY_UNITS.map(u=>`<option ${x.u===u?"selected":""}>${u}</option>`).join("")}</select>${S.pay[k].length>1?`<button type="button" class="link-btn" data-px="${k}|${i}">✕</button>`:""}</div>`).join("")+`<button type="button" class="link-btn" data-padd="${k}" style="justify-self:start">＋ Agregar otro ${lab.toLowerCase()}</button>`;}
function payHtml(){const P=S.pay,done=P.mode&&P.how.length;
 return`<div class="field"><span class="lbl">💳 ¿Cuál es el proceso de pago que te gustaría implementar?</span>
  <div class="chips${MISS(!!P.mode)}">${[["prov","Sigo las indicaciones de los proveedores"],["mine","Yo defino anticipos y liquidaciones"]].map(([v,t])=>`<button type="button" class="chip pm2" data-v="${v}" aria-pressed="${P.mode===v}">${t}</button>`).join("")}</div>
  ${P.mode==="mine"?`<span class="hint">Útil sobre todo en eventos de empresa, donde el cliente define cómo paga.</span><div style="display:grid;gap:8px">${payRows("ant","Anticipo")}</div><div style="display:grid;gap:8px">${payRows("liq","Liquidación")}</div>`:""}</div>
 <div class="field"><span class="lbl">💵 ¿Cómo te gustaría pagar?</span><div class="chips${MISS(P.how.length>0)}">${["Pago con tarjeta","Transferencia SPEI","Efectivo","Otro"].map(t=>`<button type="button" class="chip ph2" aria-pressed="${P.how.includes(t)}">${t}</button>`).join("")}</div>
  ${P.how.includes("Otro")?`<input type="text" id="phO" value="${esc(P.howOther)}" placeholder="¿Cuál?" class="${MISS(filled(P.howOther))}">`:""}</div>
 ${done?`<div class="paylegend">📝 Estas condiciones de pago serán expresadas a los proveedores de la comunidad ¡Hay que vernos! y estarán sujetas a su aprobación, previa negociación directa entre ustedes como particulares.</div>`:""}`;}
function bindPay(el){const P=S.pay,keep=()=>{const y=scrollY;render();scrollTo({top:y});};
 el.querySelectorAll(".pm2").forEach(b=>b.onclick=()=>{P.mode=b.dataset.v;keep();});
 el.querySelectorAll(".ph2").forEach(b=>b.onclick=()=>{const t=b.textContent.replace("✓","").trim();P.how=P.how.includes(t)?P.how.filter(x=>x!==t):[...P.how,t];keep();});
 const o=$("phO");if(o)o.oninput=e=>{P.howOther=e.target.value;refresh("detalles");};
 el.querySelectorAll("[data-pn]").forEach(x=>x.oninput=()=>{const[k,i]=x.dataset.pn.split("|");P[k][+i].n=x.value;refresh("detalles");});
 el.querySelectorAll("[data-pu]").forEach(x=>x.onchange=()=>{const[k,i]=x.dataset.pu.split("|");P[k][+i].u=x.value;});
 el.querySelectorAll("[data-padd]").forEach(x=>x.onclick=()=>{P[x.dataset.padd].push({n:"",u:"porcentaje"});keep();});
 el.querySelectorAll("[data-px]").forEach(x=>x.onclick=()=>{const[k,i]=x.dataset.px.split("|");P[k].splice(+i,1);keep();});}
function payText(){const P=S.pay;const r=(l,k)=>P[k].filter(x=>filled(x.n)).map((x,i)=>`${l} ${i+1}: ${x.n} ${x.u}`).join(" · ");
 return{proceso:P.mode==="prov"?"Sigo las indicaciones de los proveedores":[r("Anticipo","ant"),r("Liquidación","liq")].filter(Boolean).join(" · "),formas:P.how.map(x=>x==="Otro"?(P.howOther||"Otro"):x)};}
/* cargar una pre-cotización guardada para editarla */
addEventListener("message",e=>{const d=e.data||{};if(d.hqv!=="cargar"||!d.state)return;try{const st=JSON.parse(JSON.stringify(d.state));Object.keys(st).forEach(k=>{S[k]=st[k];});S.maxStage=STAGES.length-1;S.nameOk=true;go("fiesta");}catch(_){}});
'''
i = s.index('function render(){')
s = s[:i] + PAY + s[i:]

# ---------- resultado: manda condiciones, nota y el estado completo
rep('''servicios:Object.keys(S.sel).map(c=>({cat:c,subs:''', '''pago:payText(),nota:S.extra||"",
    servicios:Object.keys(S.sel).map(c=>({cat:c,subs:''')
rep('''parent.postMessage({hqv:"fiesta-lista",fiesta,nombre:S.name,cta},"*");''',
    '''parent.postMessage({hqv:"fiesta-lista",fiesta,nombre:S.name,cta,state:JSON.parse(JSON.stringify(S))},"*");''')
rep('''${S.more?`<div><span>✏️ Pedido especial<br><span class="sub">${esc(S.more)}</span></span><span>Por cotizar</span></div>`:''}</div>''',
    '''${S.more?`<div><span>✏️ Pedido especial<br><span class="sub">${esc(S.more)}</span></span><span>Por cotizar</span></div>`:''}${S.extra?`<div><span>📝 Lo que agregaste<br><span class="sub">${esc(S.extra)}</span></span><span></span></div>`:''}</div>''')

DST.write_text(s)
print('cot9 ok', len(s))
