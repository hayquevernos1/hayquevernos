"""v27 · Registro (Diego, 15 oct 2026). reg18.html → reg19.html
- Fecha de fundación (en vez del año).
- Aviso «Estás preparando tus paquetes» arriba de Mi venue y Mi perfil de planner.
- Tarifa del planner por porcentaje con mínimo opcional.
- CSS v27."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'reg18.html').read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:140]
    s = s.replace(a, b, count)


rep('if(!b.since)m.push("Año en que empezaste")', 'if(!b.founded)m.push("Fecha de fundación")')
rep('x.biz.attends=true;', 'x.biz.attends=true;x.biz.founded="2019-03-14";x.biz.since="2019";')
rep('<h2>Mi venue 🏡</h2>', '<h2>Mi venue 🏡</h2>${ruQueueBannerHtml("venue")}')
rep('<h2>Mi perfil de planner 📋</h2>', '<h2>Mi perfil de planner 📋</h2>${ruQueueBannerHtml("planner")}')
rep('<input type="text" class="fe-n"', '${f.unit==="porcentaje"?`<input type="number" min="0" class="fe-min" value="${esc(f.min||"")}" placeholder="Mínimo $ (opcional)" aria-label="Mínimo si cobras por porcentaje">`:""}<input type="text" class="fe-n"')
rep('r.querySelector(".fe-n").oninput=e=>{f.note=e.target.value;changed();};', 'r.querySelector(".fe-n").oninput=e=>{f.note=e.target.value;changed();};const mi=r.querySelector(".fe-min");if(mi)mi.oninput=e=>{f.min=e.target.value;changed();};')

CSS = '''
/* ===== v27 ===== */
.ru-title[id]{font-size:20px;font-weight:900;padding:10px 14px!important}
.ru-l3{grid-template-columns:minmax(120px,1.1fr) minmax(0,1.3fr) minmax(0,1fr)}
.ru-l3 .ru-fi input{font-size:17px}
.ru-stw{display:grid;gap:8px}
.ru-dlw .dlsec>.mini-l{display:none}
.ru-warn{font-size:12.5px;font-weight:700;background:var(--warn-soft,#FFF4D6);border-radius:10px;padding:6px 9px}
.ru-hrows{display:grid;gap:6px}.ru-hr{display:grid;gap:0;background:rgba(255,255,255,.6);border-radius:12px;padding:8px 10px}.ru-hl{font-size:13px;font-weight:800}
.ru-ul{margin:4px 0 0;padding-left:18px;display:grid;gap:1px;font-size:12.5px;color:var(--muted)}
.pul{margin:4px 0 0;padding-left:18px;display:grid;gap:1px;font-size:12.5px;color:var(--muted)}
.ru-chg{font-size:12.5px;font-weight:700;background:var(--warn-soft,#FFF4D6);border-radius:12px;padding:7px 10px;display:grid;gap:2px;position:relative;z-index:2}.ru-chg .link{justify-self:start;font-size:13px}
.ru-pksec{position:relative}.ru-pksec.locked{cursor:pointer}
.ru-shake{animation:ruShake .5s cubic-bezier(.36,.07,.19,.97)}
@keyframes ruShake{10%,90%{transform:translateX(-2px)}20%,80%{transform:translateX(4px)}30%,50%,70%{transform:translateX(-6px)}40%,60%{transform:translateX(6px)}}
.ru-lockb{position:absolute;left:50%;top:40%;transform:translate(-50%,-50%) scale(.6);opacity:0;display:flex;align-items:center;gap:10px;background:#1A2600;color:#BEFF00;font-weight:900;font-size:14px;border-radius:20px;padding:10px 16px 10px 10px;box-shadow:0 12px 30px rgba(0,0,0,.3);width:max-content;max-width:calc(100% - 20px);animation:ruPop .45s cubic-bezier(.3,1.6,.5,1) forwards;z-index:5}
.ru-lockb img{width:46px;height:46px;object-fit:contain;animation:ruHop .6s ease-in-out 2}
.ru-lockb.out{transition:opacity .35s,transform .35s;opacity:0!important;transform:translate(-50%,-60%) scale(.9)!important}
@keyframes ruPop{to{opacity:1;transform:translate(-50%,-50%) scale(1)}}@keyframes ruHop{50%{transform:translateY(-8px) rotate(-8deg)}}
@media (prefers-reduced-motion:reduce){.ru-shake,.ru-lockb,.ru-lockb img{animation:none!important;opacity:1;transform:translate(-50%,-50%)}}
.ru-plb{border-radius:99px;padding:2px 9px;font-size:11px;font-weight:900;width:fit-content;background:linear-gradient(135deg,#8205B4,#FA1ED2);color:#fff}.ru-plb.ok{background:linear-gradient(135deg,#00C389,#BEFF00);color:#0B2A1F}.ru-plb.wait{background:var(--warn-soft,#FFF4D6);color:#5A3A00}
.ru-plc.pend{border-style:dashed}.ru-plact{gap:12px}.ru-plact .link{font-size:13px}
.ru-gates{gap:12px;text-align:left;justify-items:stretch}.ru-gates h2,.ru-gates>span{text-align:center}
.ru-gate{display:grid;gap:8px}.ru-gr{display:grid;grid-template-columns:28px 1fr;gap:4px 8px;align-items:center;background:rgba(255,255,255,.12);border-radius:14px;padding:9px 12px}.ru-gr.ok{background:rgba(190,255,0,.16)}
.ru-gi{font-size:18px}.ru-gt{font-size:14px}.ru-gb{grid-column:2;display:flex;flex-wrap:wrap;gap:6px}.ru-gb .chip{background:rgba(255,255,255,.14);color:#fff;border-color:rgba(255,255,255,.35)}.ru-gb .chip[aria-pressed="true"]{background:#BEFF00;color:#1A2600;border-color:#BEFF00}
.ru-gates .btn.cta{justify-self:center}
.ru-inv{gap:10px}.ru-invf{display:grid;gap:8px;width:100%;text-align:left}.ru-invf input[type=text],.ru-invf input[type=email],.ru-invf input[type=tel]{width:100%}
.ru-invm{background:rgba(255,255,255,.12);border-radius:12px;padding:10px 12px;font-size:13px;line-height:1.45}
.ru-invf .row{gap:8px;flex-wrap:wrap}.ru-invf .btn{text-decoration:none}
.ru-invck{display:flex;gap:8px;align-items:flex-start;font-size:13px}.ru-invck input{margin-top:3px;width:18px;height:18px;flex:none}
.ru-invlogo{width:120px;height:auto}
.ru-invr{display:grid;gap:4px;font-size:13.5px;font-weight:800}.ru-invr .ru-fi{background:#fff;border-radius:12px;padding:0 10px;color:#1A1033}.ru-invr .ru-fi input[type]{border:0!important;box-shadow:none!important;background:none!important;color:#1A1033}.ru-invr small{font-weight:600;opacity:.8}
.ru-qb{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.ru-invf input[type=text],.ru-invf input[type=email],.ru-invf input[type=tel],.ru-invf select{color:#1A1033!important;background:#fff!important}
.ru-l3{grid-template-columns:minmax(110px,1fr) minmax(0,1.6fr) auto}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]
(V / 'reg19.html').write_text(s)
print('ok reg19', len(s))
