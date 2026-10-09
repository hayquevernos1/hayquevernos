"""v8 · Cotizador (comentarios de Diego en Miro, 8 oct 2026 noche). cot7.html → cot8.html
- Animación en la tarjeta del planner: a la derecha se acepta, a la izquierda se descarta.
- Precio por persona como protagonista y el total abajo, más chico: «por el total de invitados». Precios promedio del mercado.
- Sin «Solo lo que aplica a…», sin la línea de ahorro por anticipación en el resultado.
- Amarillo legible; texto oscuro sobre fondo claro en el nombre de la fiesta.
- «Guardar y enviar» en verde debajo del nombre (como en celular) + línea «Guarda esta pre-cotización y auto envíatela por correo.»
- Todos los «Contactar» en verde. Botones de conversión = verde (--cta)."""
from pathlib import Path
SRC = Path('/home/claude/hqv/v5/cot7.html')
DST = Path('/home/claude/hqv/v5/cot8.html')
s = SRC.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:110]
    s = s.replace(a, b, count)


CSS = '''
/* ===== v8 ===== */
:root{--cta:#0E8F45;--cta-d:#0B7639}
.btn.cta,.rbar .save .btn.cta{background:var(--cta)!important;color:#fff!important;box-shadow:0 8px 18px rgba(14,143,69,.28)}
.btn.cta:hover{background:var(--cta-d)!important}
.lvl.mid{color:#8A6500!important}
.rbar .save{grid-template-columns:1fr!important}
.rbar .save input{background:#fff;color:#1a1033!important}
.rbar .save input::placeholder{color:#7a7394}
.rbar .save .btn{justify-self:stretch;font-size:17px;padding:14px 18px}
.rbar .save .sv-note{font-size:12.5px;opacity:.95;text-align:center}
.pp2{display:grid;justify-items:end;line-height:1.15}
.pp2 b{font-size:15px}
.pp2 small{font-size:60%;color:var(--muted);font-weight:600}
.break .pp2 small{font-size:11px}
.mkt{font-size:12px;color:var(--muted)}
@keyframes plcHint{0%,100%{transform:none}15%{transform:translateX(26px) rotate(3deg)}30%{transform:none}45%{transform:translateX(-26px) rotate(-3deg)}60%{transform:none}}
.plc.hint-anim{animation:plcHint 2.4s ease-in-out 2 .6s}
.plc{position:relative}
.plc .sw-l,.plc .sw-r{position:absolute;top:12px;font-weight:900;font-size:12px;border-radius:99px;padding:4px 10px;opacity:.9}
.plc .sw-l{left:12px;background:#fff;color:#1a1033;box-shadow:var(--hqv-clay-sm)}
.plc .sw-r{right:12px;background:var(--cta);color:#fff}
@media (prefers-reduced-motion:reduce){.plc.hint-anim{animation:none}}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# ---------- planner: animación + etiquetas de deslizar; «Lo quiero» en verde
rep('''return`<div class="plc" id="plc"><div style="display:flex;gap:12px;align-items:center">''',
    '''return`<div class="plc hint-anim" id="plc"><span class="sw-l">← Siguiente</span><span class="sw-r">Lo quiero →</span><div style="display:flex;gap:12px;align-items:center;margin-top:28px">''')
rep('''<button class="btn" type="button" id="plYes">💙 Lo quiero</button>''', '''<button class="btn cta" type="button" id="plYes">💙 Lo quiero</button>''')

# ---------- precios: por persona protagonista + total abajo
rep('''return x.pend?'<span class="pc">Por cotizar</span>':`~${money(x.total/S.guests)} c/u · ${money(x.total)}`;};''',
    '''return x.pend?'<span class="pc">Por cotizar</span>':`<span class="pp2"><b>~${money(x.total/S.guests)} por persona</b><small>${money(x.total)} por el total de invitados</small></span>`;};''')
rep('''<span class="lbl">📂 Explora por categoría <span class="opt">Solo lo que aplica a ${esc(S.occ.toLowerCase())}</span></span>''',
    '''<span class="lbl">📂 Explora por categoría</span><span class="mkt">💡 Los precios son el promedio del mercado en tu zona.</span>''')
rep('''${r.pendOnly?"Por cotizar":`${money(r.amt/S.guests)} c/u<br><span class="sub">${money(r.amt)}${r.pend&&r.pend.length?" + por cotizar":""}</span>`}''',
    '''${r.pendOnly?"Por cotizar":`<span class="pp2"><b>${money(r.amt/S.guests)} por persona</b><small>${money(r.amt)} por el total de invitados${r.pend&&r.pend.length?" + por cotizar":""}</small></span>`}''')
rep('''<span>${money(x.q.total*ef*f/S.guests)} c/u<br><span class="sub">${money(x.q.total*ef*f)}</span></span>''',
    '''<span class="pp2"><b>${money(x.q.total*ef*f/S.guests)} por persona</b><small>${money(x.q.total*ef*f)} por el total de invitados</small></span>''')
rep('''$("pp").innerHTML=t?`${money(pp)} <em>c/u</em>`:"$0";''', '''$("pp").innerHTML=t?`${money(pp)} <em>por persona</em>`:"$0";''')
s = s.replace('· ~${money(p.price/S.guests)} c/u</small>', '· ~${money(p.price/S.guests)} por persona</small>')

# ---------- resultado
rep('''${earlyPct()?`<span class="meta">🎁 Gracias a tu anticipación, estás ahorrando ${earlyPct()}% (en promedio) respecto a otros anfitriones con la misma fiesta pero con menos anticipación.</span>`:''}''', '')
rep('''<button class="btn" type="button" id="send">Guardar y enviar →</button></div>''',
    '''<button class="btn cta" type="button" id="send">Guardar y enviar →</button><span class="sv-note">Guarda esta pre-cotización y auto envíatela por correo.</span></div>''')
rep('''<button class="btn sm" type="button" data-ct="${esc(r.k)}">Contactar</button>''', '''<button class="btn cta sm" type="button" data-ct="${esc(r.k)}">Contactar</button>''')
rep('<span class="mkt-dummy"></span>', '') if '<span class="mkt-dummy"></span>' in s else None

DST.write_text(s)
print('cot8 ok', len(s))
