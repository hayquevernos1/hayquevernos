"""v25 · Registro (Diego, 15 oct 2026). reg16.html → reg17.html
- WhatsApp con clave de país (validación, sitio y publicación).
- «Recoger en mi negocio»; si cobra la entrega al recoger, solo tarifa fija.
- Mi venue: tus servicios reflejados con precio aparte, paquetes con tu venue desde el combinador,
  «Arma tu servicio» dentro del venue si no tienes «Servicios». Se quita «Servicios en tu venue» (políticas viejas).
- Sitio del venue: «Servicios en este venue».
- CSS: filas compactas de personal, tarjetas agrupadas por formas de contratarlo, venue."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'reg16.html').read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:140]
    s = s.replace(a, b, count)


# ---------- WhatsApp con lada ----------
rep('if(b.whatsapp.replace(/\\D/g,"").length!==10)m.push("WhatsApp de 10 dígitos")',
    'if(!waOk(b.waCC,b.whatsapp))m.push((b.waCC||"MX")==="MX"?"WhatsApp de 10 dígitos":"WhatsApp completo")')
rep('https://wa.me/52${wa}', 'https://wa.me/${waIntl(b.waCC,b.whatsapp)}')
rep('${wa?`<span class="hint" style="text-align:center">${esc(b.whatsapp)}</span>`',
    '${wa?`<span class="hint" style="text-align:center">${esc(waShow(b.waCC,b.whatsapp))}</span>`')
rep('<span>📱 ${esc(b.whatsapp||"—")}</span>', '<span>📱 ${esc(waShow(b.waCC,b.whatsapp)||"—")}</span>')
rep('wa:S.biz.whatsapp.replace(/\\D/g,"").slice(-10),',
    'wa:S.biz.whatsapp.replace(/\\D/g,""),waLada:ccDial(S.biz.waCC),waInternacional:waIntl(S.biz.waCC,S.biz.whatsapp),')
rep('perfilPersonal:S.me?{whatsapp:S.me.whatsapp,', 'perfilPersonal:S.me?{whatsapp:S.me.whatsapp?waShow(S.me.waCC,S.me.whatsapp):"",')

# ---------- Recoger en mi negocio ----------
s = s.replace('Recoger en mi local', 'Recoger en mi negocio')
rep('${d.cobra?`<span class="mini-l">¿Cómo lo cobras?</span>',
    '${d.cobra&&d.m==="Recolección en establecimiento"?((d.u="Tarifa fija"),`<span class="mini-l">Tarifa fija por la entrega</span><div class="dlrow"><input type="number" min="0" step="any" class="dl-rate${MISS(filled(d.rate))}" value="${esc(d.rate)}" placeholder="$" aria-label="Tarifa fija por la entrega"><span class="u">$ por entrega</span></div>`)'
    ':d.cobra?`<span class="mini-l">¿Cómo lo cobras?</span>')

# ---------- Mi venue ----------
a = s.index('\n <div class="field"><span class="lbl">🔄 Servicios en tu venue</span>')
b = s.index('\n\n <div class="field"><span class="lbl">📝 Condiciones para rentarlo</span>')
s = s[:a] + s[b:]
rep('\n\n <div class="field"><span class="lbl">🕒 Horario y precios</span>',
    '\n ${vnSvcHtml(v)}\n\n <div class="field"><span class="lbl">🕒 Horario y precios</span>')
rep("${isP?`<b style=\"font-size:14px\">📦 Mis paquetes</b>${pk||''}${v.packages.length<4?`<button type=\"button\" class=\"btn ghost sm\" id=\"pk-add\">+ Agregar paquete</button>`:''}`:''}",
    "${isP?`<span class=\"hint\">📦 Tus paquetes con venue se arman arriba, en «Paquetes con tu venue», junto con tus productos y tu personal.</span>`:''}")
rep('bindUploader(k,"photo",v.photos,redraw);bindNav();}', 'bindUploader(k,"photo",v.photos,redraw);vnBind(v);bindNav();}')
rep('if((v.mode==="paquetes"||v.mode==="ambos")&&!(v.packages.length&&v.packages.every(pkgOk)))m.push("Nombre y precio de cada paquete");',
    'if((v.mode==="paquetes"||v.mode==="ambos")&&!vnPkgs().length)m.push("Arma al menos un paquete con tu venue");')
# sitio del venue: lista nueva en lugar de las políticas viejas
a = s.index('<div class="ms-pol">${POLICY_SVCS.map(([s,e])=>{const p=v.policy[s];')
b = s.index('<div class="prompt" style="font-size:12px;display:grid;gap:2px"><small>Condiciones</small>', a)
s = s[:a] + '${vnSiteHtml(v)}\n   ' + s[b:]
# ejemplo: precios en el venue
rep('x.remb=3;', 'x.remb=3;x.venue.svcIn=D.vin;')
rep('whatsapp:"55 8765 4321",email:"lupita.ramirez@gmail.com"', 'whatsapp:"",email:"lupita.ramirez@gmail.com"')

CSS = '''
/* ===== v25 · personal compacto (texto de ayuda dentro del campo) ===== */
.ru-lt{display:grid;gap:8px}
.ru-lr{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;background:var(--card);border-radius:16px;padding:8px 10px;align-items:stretch}
.ru-lnr{grid-column:1/-1;display:flex;align-items:center;gap:8px;min-width:0}
.ru-ln{font-size:15px;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ru-known{font-size:11px;font-weight:800;color:#00A374;white-space:nowrap}
.ru-lnr .ru-lrm{font-size:15px;padding:2px 6px}
.ru-f{display:flex;flex-direction:column;justify-content:center;min-width:0;border:1.5px solid var(--line);border-radius:12px;background:var(--paper);padding:3px 8px 4px;cursor:text;margin:0}
.ru-f small{font-size:10px;font-weight:900;letter-spacing:.05em;text-transform:uppercase;color:var(--help,#9A92AE);line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ru-fi{display:flex;align-items:center;gap:2px;min-width:0}
.ru-fi i{font-style:normal;font-weight:900;color:#8205B4;font-size:14px;flex:none}
.ru-f .ru-fi input[type],.ru-f .ru-fi select{border:0!important;background:none!important;box-shadow:none!important;padding:1px 0!important;min-width:0;width:100%;font-size:15px;font-weight:800;color:var(--ink);height:auto;min-height:0;border-radius:0!important;outline:none}
.ru-f .ru-fi select{font-size:13.5px;cursor:pointer;padding-right:14px!important;background:url("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2710%27 height=%276%27%3E%3Cpath d=%27M1 1l4 4 4-4%27 fill=%27none%27 stroke=%27%238205B4%27 stroke-width=%272%27/%3E%3C/svg%3E") right 2px center/10px 6px no-repeat!important;-webkit-appearance:none;appearance:none}
.ru-f input[type=number]{-moz-appearance:textfield;appearance:textfield}.ru-f input::-webkit-inner-spin-button,.ru-f input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}
.ru-f:focus-within{border-color:#9146FF;box-shadow:0 0 0 3px rgba(145,70,255,.18)}
.ru-f:has(.miss){border-color:var(--bad)}
.ru-f.ru-na .ru-fi{color:var(--help,#9A92AE);font-weight:800}
.ru-fq .ru-stp{border:0;background:none;border-radius:0;overflow:visible}
.ru-fq .ru-stp button{width:22px;height:24px;font-size:16px;flex:none;padding:0;border:0;background:none;color:#8205B4;font-weight:900;cursor:pointer}
.ru-fq .ru-stp input{text-align:center}
@container (min-width:640px){.ru-labr .ru-lr{grid-template-columns:minmax(150px,1.6fr) minmax(100px,1.1fr) repeat(5,minmax(0,1fr));align-items:center}.ru-labr .ru-lnr{grid-column:auto}.ru-labr .ru-lr.one{grid-template-columns:minmax(170px,1.7fr) repeat(5,minmax(0,1fr))}.ru-known span{display:none}}
.ru-pill .ru-pin input[type]{background:var(--card)!important;color:var(--ink)!important}
@container (max-width:720px){.ru-pill{max-width:100%;flex-wrap:wrap}.ru-pt{white-space:normal;text-align:left}}
.ru-addc .chip small{font-weight:800;color:#00A374;margin-left:2px}
/* ===== v25 · productos agrupados por formas de contratarlo ===== */
.ru-glist{display:grid;gap:12px}
.ru-grp{position:relative;background:var(--card);border:2px solid var(--line);border-radius:22px;padding:12px;display:grid;gap:10px}.ru-grp.warn{border-color:#FFB3C7}
.ru-gh{position:relative}.ru-gh>div{padding-right:62px;display:grid;gap:3px}.ru-gh h4{font-size:17px;font-weight:900;margin:2px 0 0}.ru-gh .ru-tools{top:-2px;right:-2px}
.ru-forms{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:8px}
.ru-fc{position:relative;background:var(--paper);border:1.5px solid var(--line);border-radius:16px;padding:10px 12px;display:grid;gap:2px;align-content:start}
.ru-fc.sel{border-color:#9146FF;box-shadow:0 0 0 3px rgba(145,70,255,.2)}.ru-fc.sel .ru-ck{background:#9146FF;border-color:#9146FF}
.ru-fc .ru-pick{border-radius:16px}.ru-fc .ru-tools{top:4px;right:4px}
.ru-fl{font-size:13px;padding-right:58px}
.ru-tot{font-size:22px;font-weight:900;font-variant-numeric:tabular-nums;color:#8205B4;line-height:1.15}
.ru-ppx{font-size:12.5px;color:var(--muted)}.ru-ppx b{color:var(--ink)}
.ru-fd{font-size:12px;color:var(--muted)}
.ru-stsec{display:grid;gap:8px}.ru-stsec[hidden]{display:none}
.ru-vb{background:linear-gradient(135deg,#FF6905,#FAFA19);color:#3A1A00;border-radius:99px;padding:2px 9px;font-size:11px;font-weight:900;width:fit-content}
.ru-vc{border-style:dashed}
.ru-kits{align-items:center}.ru-kq{display:inline-flex;align-items:center;gap:4px;background:var(--paper);border-radius:99px;padding:2px 10px 2px 4px;font-size:12.5px;font-weight:800}.ru-kq input{width:48px;padding:3px 6px!important;text-align:center}
.ru-hosts{margin-top:2px}
/* sitio: formas de contratarlo y personal */
.pforms{display:grid;gap:6px;margin:4px 0}
.pform{display:grid;gap:2px;background:var(--paper);border-radius:12px;padding:8px 10px}
.pfh{display:flex;justify-content:space-between;gap:8px;align-items:flex-start;flex-wrap:wrap}.pfh>b{font-size:13.5px}
.pstaff .pst-r{display:flex;justify-content:space-between;gap:10px;font-size:13px;padding:6px 0;border-top:1px dashed var(--line);flex-wrap:wrap}.pstaff .pst-r>span:first-child{font-weight:800}
/* WhatsApp con clave de país */
.tel{display:flex;gap:6px;min-width:0}.tel select{flex:none;width:auto;max-width:112px;padding-left:8px;padding-right:4px}.tel input{flex:1;min-width:0}
.tel.miss input{border-color:var(--bad)}
.bz-same{font-size:12px;font-weight:700;color:#00A374}.bz-reuse{font-size:12.5px;justify-self:start;width:fit-content}
/* Mi venue · servicios y paquetes */
.vn-svc{display:grid;gap:10px}.vn-rows{display:grid;gap:6px}
.vn-r{display:grid;grid-template-columns:30px minmax(0,1fr) minmax(96px,130px);gap:8px;align-items:center;background:var(--card);border:1.5px solid var(--line);border-radius:14px;padding:6px 8px}
.vn-r.off{opacity:.7}.vn-r.off .vn-n b{text-decoration:line-through;text-decoration-thickness:1px}
.vn-on{width:28px;height:28px;border-radius:9px;border:2px solid var(--line);background:var(--card);font-weight:900;color:#fff;cursor:pointer;display:grid;place-items:center;padding:0}
.vn-on[aria-pressed="true"]{background:#8A3FFC;border-color:#8A3FFC}
.vn-n{display:grid;min-width:0}.vn-n b{font-size:14px;overflow-wrap:anywhere}.vn-n small{font-size:12px;color:var(--muted)}
.vn-no{font-size:12px;color:var(--muted);font-weight:700;text-align:right}
.vn-build{border-radius:18px}.vn-bw{display:grid;gap:14px;margin-top:12px;min-width:0}
.vn-pk{display:grid;gap:8px}.vn-kl{display:grid;gap:8px}
.vn-kc{display:grid;gap:2px;background:var(--card);border:1.5px solid var(--line);border-radius:16px;padding:10px 12px}.vn-kc .link{justify-self:start;margin-top:4px}
.vn-site{display:grid;gap:4px;background:var(--paper);border-radius:14px;padding:10px 12px;font-size:13px}
.vn-sr{display:flex;justify-content:space-between;gap:10px;padding:6px 0;border-top:1px dashed var(--line);flex-wrap:wrap}.vn-sr>span{display:grid}.vn-sr>span:last-child{text-align:right}.vn-sr small{color:var(--muted);font-size:11.5px}
@media (max-width:420px){.vn-r{grid-template-columns:30px minmax(0,1fr);}.vn-r .vn-p,.vn-r .vn-no{grid-column:2}}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]
(V / 'reg17.html').write_text(s)
print('ok reg17', len(s))
