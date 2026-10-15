"""v28 · Registro (Diego, 15 oct 2026). reg19.html → reg20.html
- Datos de publicación con el modelo actual (ruPayload): servicio y staff separados, tarifas, tiempos, venue, planners, oferta cotizable.
- Mi perfil de planner: fecha de fundación y bio ligadas a Mi negocio.
- Sitio del venue: proveedores no permitidos.
- CSS v28."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'reg19.html').read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:140]
    s = s.replace(a, b, count)


a = s.index('variabilidad:S.svcVar,productos:')
b = s.index('minimo:p.min,promo:p.promo})),paquetes:S.svcPkgs,', a) + len('minimo:p.min,promo:p.promo})),')
s = s[:a] + 'variabilidad:S.svcVar,...ruPayload(),' + s[b:]
rep('function drawPlanner(){const p=S.planner,', 'function drawPlanner(){plSync();const p=S.planner,')
rep('''<div class="field"><label class="lbl" for="pl-since">Organizo eventos desde</label><select id="pl-since" class="${MISS(!!p.since)}"><option value="">Año</option>${yrs.map(y=>`<option ${String(y)===String(p.since)?'selected':''}>${y}</option>`).join("")}</select></div></div>''',
    '''<div class="field"><label class="lbl" for="pl-since">Fecha de fundación de tu negocio</label><input type="date" id="pl-since" class="${MISS(!!p.since)}" value="${esc(S.biz.founded||"")}" max="${new Date().toISOString().slice(0,10)}"><span class="bz-same">🔗 La misma de Mi negocio</span></div></div>''')
rep('[["pl-name","person"],["pl-since","since"],["pl-bio","bio"],', '[["pl-name","person"],')
rep('rows="5" placeholder="Cuéntales quién eres y cómo trabajas">${esc(p.bio)}</textarea></div>',
    '''rows="5" placeholder="Cuéntales quién eres y cómo trabajas">${esc(p.bio)}</textarea>${p.bioLink!==false?`<span class="bz-same">🔗 Es la misma bio de tu negocio: si la cambias aquí, también cambia allá.</span><button type="button" class="link" id="pl-bsep" style="justify-self:start;font-size:12.5px">Usar una bio distinta</button>`:`<button type="button" class="link bz-reuse" id="pl-blink">↺ Usar la bio de tu negocio</button>`}</div>''')
rep('p.bio=t.value;', 'p.bio=t.value;if(p.bioLink!==false)S.biz.about=p.bio;')
rep('const redraw=()=>{const y=scrollY;drawPlanner();scrollTo({top:y});};',
    '''const redraw=()=>{const y=scrollY;drawPlanner();scrollTo({top:y});};
 $("pl-since").oninput=$("pl-since").onchange=e=>{S.biz.founded=e.target.value;S.biz.since=S.biz.founded.slice(0,4);plSync();changed();};
 $("pl-bio").oninput=e=>{p.bio=e.target.value;if(p.bioLink!==false)S.biz.about=p.bio;changed();};
 const bs=$("pl-bsep");if(bs)bs.onclick=()=>{p.bioLink=false;redraw();changed();};const bl=$("pl-blink");if(bl)bl.onclick=()=>{p.bioLink=true;p.bio=S.biz.about||p.bio;redraw();changed();};''')
rep('v.extAll==="no"?"no":esc(v.extAllNote||"solo algunos")', 'v.extAll==="no"?"no":esc((v.extNo||[]).length?"sí, excepto "+v.extNo.join(", ").toLowerCase():"solo algunos")')

CSS = '''
/* ===== v28 ===== */
.ru-st.ru-step2{position:relative;cursor:pointer}.ru-st.ru-step2.locked{opacity:.85}
.ru-st .ru-lockb{top:50%}
.ru-hr .ru-tot small{font-size:13px;font-weight:700;color:var(--muted)}
.ru-invp{display:flex;gap:10px;align-items:center;background:rgba(255,255,255,.12);border-radius:14px;padding:8px 10px}.ru-invp>span:last-child{display:grid}.ru-invp small{opacity:.85;font-size:12px}
.ru-invav{width:44px;height:44px;border-radius:50%;background:#fff;display:grid;place-items:center;font-size:24px;flex:none}
.ru-invf textarea{color:#1A1033!important;background:#fff!important;width:100%}
.ru-invf .btn.ghost{color:#fff;border-color:rgba(255,255,255,.5);background:rgba(255,255,255,.1)}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]
(V / 'reg20.html').write_text(s)
print('ok reg20', len(s))
