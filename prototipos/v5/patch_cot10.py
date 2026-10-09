"""v14 · Cotizador (Diego, 9 oct 2026 tarde). cot9.html → cot10.html
- Anticipos y liquidaciones: monto con selector % / $ + tiempo con selector horas/días/semanas/meses + «antes del evento».
- Resultado «Así se reparte»: disclaimer de la comunidad en cada línea."""
from pathlib import Path
SRC = Path('/home/claude/hqv/v5/cot9.html')
DST = Path('/home/claude/hqv/v5/cot10.html')
s = SRC.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:120]
    s = s.replace(a, b, count)


CSS = '''
/* ===== v14 · cotizador ===== */
.payrow input{flex:0 0 84px!important;width:84px!important}.payrow select{flex:0 0 auto!important;width:auto!important;min-width:0}
.payrow .ab{font-size:12px;font-weight:800;color:var(--muted)}
.payrow .pg{display:flex;gap:6px;align-items:center;flex-wrap:nowrap}
.payrow{gap:8px 14px!important}
.break .rdisc{flex-basis:100%;margin:0;font-weight:400;white-space:normal;text-align:left}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

rep('pay:{mode:"",ant:[{n:"",u:"porcentaje"}],liq:[{n:"",u:"porcentaje"}],how:[],howOther:""}',
    'pay:{mode:"",ant:[{n:"",u:"%",t:"",tu:"días"}],liq:[{n:"",u:"%",t:"",tu:"días"}],how:[],howOther:""}')
rep('const PAY_UNITS=["porcentaje","horas","días","semanas","meses"];',
    'const PAY_UNITS=["%","$"],PAY_TIME=["horas","días","semanas","meses"];')
i = s.index('function payRows(k,lab)')
j = s.index('\n', i)
s = s[:i] + r'''function payRows(k,lab){return S.pay[k].map((x,i)=>{if(!PAY_UNITS.includes(x.u))x.u="%";if(!x.tu)x.tu="días";return`<div class="payrow"><b>${lab} ${i+1}</b><span class="pg"><input type="number" min="0" data-pn="${k}|${i}" value="${esc(x.n)}" placeholder="Monto" aria-label="${lab} ${i+1}"><select data-pu="${k}|${i}" aria-label="Porcentaje o dinero">${PAY_UNITS.map(u=>`<option value="${u}" ${x.u===u?"selected":""}>${u==="%"?"% porcentaje":"$ pesos"}</option>`).join("")}</select></span><span class="pg"><input type="number" min="0" data-pt="${k}|${i}" value="${esc(x.t)}" placeholder="Tiempo" aria-label="Tiempo antes del evento"><select data-ptu="${k}|${i}" aria-label="Unidad de tiempo">${PAY_TIME.map(u=>`<option ${x.tu===u?"selected":""}>${u}</option>`).join("")}</select><span class="ab">antes del evento</span></span>${S.pay[k].length>1?`<button type="button" class="link-btn" data-px="${k}|${i}">✕</button>`:""}</div>`;}).join("")+`<button type="button" class="link-btn" data-padd="${k}" style="justify-self:start">＋ Agregar ${k==="liq"?"otra":"otro"} ${lab.toLowerCase()}</button>`;}''' + s[j:]
rep('''el.querySelectorAll("[data-pu]").forEach(x=>x.onchange=()=>{const[k,i]=x.dataset.pu.split("|");P[k][+i].u=x.value;});''',
    '''el.querySelectorAll("[data-pu]").forEach(x=>x.onchange=()=>{const[k,i]=x.dataset.pu.split("|");P[k][+i].u=x.value;});
 el.querySelectorAll("[data-pt]").forEach(x=>x.oninput=()=>{const[k,i]=x.dataset.pt.split("|");P[k][+i].t=x.value;});
 el.querySelectorAll("[data-ptu]").forEach(x=>x.onchange=()=>{const[k,i]=x.dataset.ptu.split("|");P[k][+i].tu=x.value;});''')
rep('P[x.dataset.padd].push({n:"",u:"porcentaje"})', 'P[x.dataset.padd].push({n:"",u:"%",t:"",tu:"días"})')
rep('map((x,i)=>`${l} ${i+1}: ${x.n} ${x.u}`)',
    'map((x,i)=>`${l} ${i+1}: ${x.u==="$"?money(+x.n):x.n+"%"}${filled(x.t)?` ${x.t} ${x.tu} antes del evento`:""}`)')

# disclaimer en cada línea del resultado
rep('''<button class="btn cta sm" type="button" data-ct="${esc(r.k)}">Contactar</button></div>`:''}</div>`).join("")}''',
    '''<button class="btn cta sm" type="button" data-ct="${esc(r.k)}">Contactar</button></div>`:''}<p class="disc rdisc">Cálculo basado en el promedio del histórico de precios publicados/pagados por los proveedores/anfitriones de la comunidad ¡Hay que vernos!.</p></div>`).join("")}''')

DST.write_text(s)
print('ok cot10', len(s))
