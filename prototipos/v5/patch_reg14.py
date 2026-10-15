"""v19 · Registro (Diego, 14 oct 2026 noche). reg13.html → reg14.html — motor svc6.js (ver encabezado)."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'reg13.html').read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:140]
    s = s.replace(a, b, count)


js = (V / 'svc6.js').read_text()
a = s.index('/* ===== v18 · Servicios')
b = s.index('\n/* Venue: los servicios se eligen', a)
s = s[:a] + js + s[b:]

CSS = '''
/* ===== v19 · servicios ===== */
.carr{display:flex;align-items:center;gap:6px;min-width:0}
.carr-in{display:flex;flex-wrap:wrap;gap:6px;min-width:0}
.carr.many .carr-in{flex-wrap:nowrap;display:grid;grid-auto-flow:column;grid-template-rows:repeat(2,auto);grid-auto-columns:max-content;overflow-x:auto;scroll-snap-type:x proximity;scrollbar-width:none;padding:2px;flex:1;-webkit-mask-image:linear-gradient(90deg,#000 88%,transparent);mask-image:linear-gradient(90deg,#000 88%,transparent)}
.carr.many .carr-in::-webkit-scrollbar{display:none}
.carr-in .chip{scroll-snap-align:start;white-space:nowrap}
.carr-a{flex:none;width:30px;height:30px;border-radius:50%;border:1.5px solid var(--line);background:var(--card);font-weight:900;font-size:17px;line-height:1;color:var(--ink);cursor:pointer}
@media(max-width:560px){.carr-a{display:none}}
.pkrs{display:grid;gap:6px}
.pkr{display:grid;grid-template-columns:minmax(0,1.3fr) 76px minmax(0,1fr) 24px;gap:6px;align-items:center;background:var(--paper);border-radius:14px;padding:6px 8px}
.pkr .pkn{font-size:13.5px;overflow:hidden;text-overflow:ellipsis}
.pkr input{padding:7px 9px;min-width:0}
.pkr .sl-p{display:flex;align-items:center;gap:4px;font-weight:900;color:#8205B4}
.pkbox[data-l="ex"] .pkr{grid-template-columns:minmax(0,1.3fr) 110px minmax(0,1fr) 24px}
.relbox{gap:8px!important}
.tsel{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;border-radius:16px}
.tsb{position:relative;display:grid;gap:2px;align-content:start;text-align:left;border:1.5px solid var(--line);background:var(--paper);border-radius:16px;padding:10px 40px 10px 12px;cursor:pointer;font:inherit;color:var(--ink)}
.tsb b{font-size:14px}.tsb small{font-size:12px;color:var(--help,#9A92AE);line-height:1.3}
.tsb .tick{top:12px;transform:none}
.tsb[aria-pressed="true"]{border-color:#9146FF;box-shadow:0 0 0 2px rgba(145,70,255,.25)}
.tsb[aria-pressed="true"] .tick{background:var(--grape);border-color:var(--grape)}.tsb[aria-pressed="true"] .tick svg{opacity:1}
.tgrp.tw-full,.tgrp.tw-rent,.tgrp.tw-labor{border:0}
.tgrp .tarr{display:flex!important;flex-wrap:wrap;gap:8px;align-items:center}
.tgrp .tarr .sl-p input{width:110px}.tgrp .tarr select{width:auto}.tgrp .ta-hv{flex-basis:100%}
.pkbadge{background:linear-gradient(135deg,#BEFF00,#FAFA19);color:#1a1033;border-radius:99px;padding:2px 10px;font-size:11.5px;font-weight:900}
.ofn{color:var(--ink)}
.rmodal{position:fixed;inset:0;z-index:90;background:rgba(18,11,30,.5);display:grid;place-items:center;padding:16px}
.rsheet{max-width:500px;width:100%;max-height:calc(100% - 16px);overflow:auto;display:grid;gap:10px;justify-items:center;text-align:center;border-radius:28px;padding:20px;background:linear-gradient(165deg,#41145F 0%,#8205B4 60%,#FA1ED2 130%);color:#fff;box-shadow:0 0 0 3px rgba(190,255,0,.35),0 24px 60px rgba(0,0,0,.45)}
.rsheet h2{color:#fff;font-size:22px;margin:0}.rsheet .big{font-size:48px;line-height:1}
.rsheet .reco{background:none;padding:0;text-align:left}.rsheet .link{color:#fff}
@media(max-width:560px){.tsel{grid-template-columns:minmax(0,1fr)}.pkr,.pkbox[data-l="ex"] .pkr{grid-template-columns:minmax(0,1fr) 76px 24px;grid-template-areas:"n q x" "u u u"}.pkr .pkn{grid-area:n}.pkr .pr-q,.pkr .sl-p{grid-area:q}.pkr .pr-u{grid-area:u}.pkr .pr-x{grid-area:x}.pkbox[data-l="ex"] .pkr .sl-p input{width:100%}}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

rep('ext:[{c:"Pastel de 3 pisos",q:"1",u:"piezas",d:"",cj:"",cost:"1800"}]', 'ext:[{c:"Pastel",q:"",u:"por pieza",d:"",cj:"",cost:"1800"},{c:"Hora extra",q:"",u:"por hora",d:"",cj:"",cost:"1500"}]')
(V / 'reg14.html').write_text(s)
print('ok reg14', len(s))
