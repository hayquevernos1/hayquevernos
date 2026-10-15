"""v26 · Registro (Diego, 15 oct 2026). reg17.html → reg18.html
- Recoger en mi negocio / servicio en mi negocio: no se cobra la entrega; solo confirmar dirección y horario (prellenado con el horario de atención).
- Horario de atención por día (validación).
- CSS: filas de personal sin títulos, tiempos de platillos, simulación del anfitrión, alineación teléfono/correo."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'reg17.html').read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:140]
    s = s.replace(a, b, count)


rep('if(!b.hDays.length||!filled(b.hOpen)||!filled(b.hClose))m.push("Horario de atención");', 'if(!bzHoursOk(b))m.push("Horario de atención");')
rep('const blankDl=m=>({m,desc:"",cobra:null,', 'const DL_NOFEE=["Recolección en establecimiento","Servicio en establecimiento"];\nconst blankDl=m=>({m,desc:"",cobra:DL_NOFEE.includes(m)?false:null,')
rep('<div class="dlq">¿Cobras por la entrega? ${ynHtml(`dly-${k}-${j}`,d.cobra)}</div>',
    '${DL_NOFEE.includes(d.m)?((d.cobra=false),""):`<div class="dlq">¿Cobras por la entrega? ${ynHtml(`dly-${k}-${j}`,d.cobra)}</div>`}')
rep('${d.cobra===false?`<span class="dl-inc">✅ La entrega va incluida en tu precio</span>`:""}',
    '${d.cobra===false&&!DL_NOFEE.includes(d.m)?`<span class="dl-inc">✅ La entrega va incluida en tu precio</span>`:""}')
rep('class="dl-ph" value="${esc(d.ph||"', 'class="dl-ph" value="${esc((d.ph||(d.ph=bzHours(S.biz)))||"')

CSS = '''
/* ===== v26 ===== */
.bz-row{align-items:flex-start}
.ru-line{display:grid;grid-template-columns:62px minmax(0,1fr) minmax(0,1.25fr) 22px;gap:6px;align-items:center}
.ru-line.ru-l2{grid-template-columns:minmax(0,1fr) minmax(0,1.25fr) 52px}
.ru-line.ru-lx{grid-template-columns:62px minmax(0,1fr) minmax(0,1.25fr) 22px}
.ru-lbody{display:grid;gap:6px;min-width:0}
.ru-lr{display:grid;gap:6px;grid-template-columns:1fr}
.ru-lr .ru-f{padding:0 10px;height:42px;flex-direction:row;align-items:center}
.ru-or,.ru-xt{font-size:12.5px;font-weight:900;color:var(--muted);text-align:center}
.ru-xt{color:#8205B4;text-align:left}
.ru-addt{justify-self:start;font-size:13px}
.ru-f .ru-fi select.ph,.ru-f .ru-fi select:invalid{color:var(--help,#9A92AE)!important;font-weight:700}
.ru-f .ru-fi input::placeholder{color:var(--help,#9A92AE);font-weight:700}
.ru-l3{grid-template-columns:minmax(0,1fr) minmax(0,1.3fr) minmax(0,1fr)}
.ru-l3 .ru-f{padding:0 10px;height:44px;flex-direction:row;align-items:center}
.ru-l3 .ru-fi i:last-child{font-size:12px;color:var(--muted);font-weight:800;margin-left:4px}
@container (min-width:640px){.ru-labr .ru-lr{grid-template-columns:minmax(150px,200px) minmax(0,1fr);align-items:start}.ru-labr .ru-lnr{grid-column:auto;padding-top:10px}.ru-labr .ru-lbody{max-width:520px}}
.ru-tsel2{grid-template-columns:repeat(2,minmax(0,1fr))}
.ru-course{display:grid;gap:6px;background:var(--paper);border-radius:14px;padding:8px 10px}
.ru-ch{display:flex;align-items:center;gap:6px}.ru-ch input.ru-cn[type]{font-weight:900;font-size:14px;border:0!important;background:none!important;box-shadow:none!important;padding:2px 0!important;flex:1;min-width:0}
.ru-cadd{font-size:13.5px}.ru-comma{margin-top:-4px}
.ru-exh{display:grid;gap:6px}
.ru-exq{display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:13px;font-weight:700}.ru-exq input{width:118px;padding:6px 8px!important}
.ru-exr{display:grid;gap:1px;background:rgba(255,255,255,.55);border-radius:12px;padding:7px 10px;font-size:12.5px}.ru-exr b{font-size:13.5px}
.ru-ext{font-weight:900;color:#8205B4;font-size:14px}
.ru-exsum{display:flex;justify-content:space-between;align-items:center}
.ru-exn{font-size:12.5px;font-weight:700}
.ru-tg .ru-labr{padding:0;background:none;border:0;box-shadow:none}
.ru-labr .ru-lr{padding:8px}
.ru-line{grid-template-columns:40px minmax(0,.9fr) minmax(0,1.35fr) 18px;gap:5px}
.ru-line.ru-lx{grid-template-columns:40px minmax(0,.9fr) minmax(0,1.35fr) 18px}
.ru-lr .ru-f .ru-fi select{font-size:13px}
.ru-lr .ru-f{padding:0 7px}
.ru-lr .ru-fq input{text-align:center}
.ru-f .ru-fi select{text-align:left;text-align-last:left}
.ru-lbody{max-width:440px}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]
(V / 'reg18.html').write_text(s)
print('ok reg18', len(s))
