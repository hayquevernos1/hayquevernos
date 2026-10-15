"""v18 · Modo noche: corrige superficies claras con texto claro y rellenos morados claros con texto blanco.
Se corre DESPUÉS de post_brand.py. Inserta un <style id="dark-fix"> al final del <head> de cada página."""
from pathlib import Path
O = Path('/home/claude/hqv/v5/out')
RULES = r'''
/* superficies que estaban fijas en blanco o lila claro */
.dlc,.nsr,.lrow,.tgrp,.pkgc,.polc,.fee,.pst,.arrive,.emph,.trkm,.rec,.fullx,.relbox,.incwrap,.sub-box{background:var(--paper)!important}
.tarr,details.more,.crewr,.sugg .bs,.tab.sh,.infl button,.pt .pic,.idea,.qkb,.btn.white,.tnav button,.pricebar.empty,.vtabs button,.sgf,.ta-hv .hv,.rec>div{background:#2C2245!important;color:var(--ink)!important}
.sgf button{color:var(--ink)!important}.sgf button:hover{background:#3A2E58!important}
.vtabs{background:var(--card)!important}
.vtabs button[aria-selected="true"]{background:#8A3FFC!important;color:#fff!important}
.dlc .dlh b[style*="1a1033"],.dlc b[style*="1a1033"]{color:var(--ink)!important}
.pmv{background:var(--mint-soft)!important;color:var(--mint)!important}
.hint.viat,.nightc{background:var(--warn-soft)!important;color:var(--ink)!important}
/* textos morados oscuros fijos */
.sl-p,.sl-p input,.pkr .sl-p,.pmf,.pmf input,.r-m,.r-m input,.mr .tn,.idea,.qkb,.ta-p,.pk-p,.sr-p,.r-cost,.ben-lead,.ben-lead b,.emph strong,.dlh .ed,.incr .r-m span{color:#D6BEFF!important}
button.link{color:#FF8FD2}
.link.bad,.bad{color:#FF8FA6!important}
/* rellenos morados: el lila de noche es muy claro para texto blanco */
.chip[aria-pressed="true"],.cat[aria-pressed="true"],.yn button[aria-pressed="true"],.seg button[aria-pressed="true"],.timeline li.now .dot,.avatar,.pill.primary,.plan .pro,.ag2.on .dt,.prov-top .av,.venue-head .ms-logo,.rbar,
.btn:not(.ghost):not(.white):not(.cta):not(.wa){background:#8A3FFC!important;color:#fff!important}
.steps-list li::before{background:#8A3FFC!important}
.timeline li.done .dot{color:#0B2A1F!important}
.ms-hero{background:linear-gradient(160deg,#5A1E9E,#9A1477)!important}
.level,.ms-tags span{background:rgba(255,255,255,.14)!important}
.ms-cta .wa,a.wa{color:#0B2A14!important}
.tick{background:var(--card)}
.dots .on{color:var(--ink)!important}
.ru-money,.ru-money input{color:#D6BEFF!important}
.ru-paxc .ru-paxi input{background:#FFFFFF!important;color:#1A2600!important;border-color:#1A2600!important}
.ru-paxc,.ru-paxc .ru-paxl,.ru-paxc .ru-paxi b{color:#1A2600!important}
.ru-paxc .ru-host{background:rgba(255,255,255,.8)!important;color:#1A2600!important}
.ru-tg .dlc{background:#2C2245!important}
.ru-tot,.ru-fi i,.ru-fq .ru-stp button{color:#D6BEFF!important}
.ru-f{background:#2C2245!important}
.ru-ext,.ru-xt{color:#D6BEFF!important}
.ru-exr{background:rgba(255,255,255,.08)!important}
.ru-course{background:#2C2245!important}
.vn-on[aria-pressed="true"]{background:#8A3FFC!important}
'''
def scoped(prefix):
    out = []
    for block in RULES.strip().split('}'):
        if '{' not in block:
            continue
        sel, body = block.split('{', 1)
        sel = sel.strip()
        if sel.startswith('/*'):
            sel = sel.split('*/', 1)[1].strip()
        sels = ','.join(prefix + ' ' + x.strip() for x in sel.split(',') if x.strip())
        out.append(sels + '{' + body + '}')
    return '\n'.join(out)


HELP = ('/* v19 · textos de ayuda más claros (todo el sitio) */\n:root{--help:#9A92AE}\n'
        '@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--help:#8F86A8}}\n:root[data-theme="dark"]{--help:#8F86A8}\n'
        '.hint,.opt,.mini-l .opt,.lbl .opt,small.hint,.field .hint{color:var(--help)!important}\n'
        'input::placeholder,textarea::placeholder{color:var(--help)!important;opacity:1}\n')
STYLE = ('<style id="dark-fix">\n' + HELP + '@media (prefers-color-scheme: dark){\n' + scoped(':root:not([data-theme="light"])') + '\n}\n'
         + scoped(':root[data-theme="dark"]') + '\n</style>\n')
for f in ['negocio.html', 'fiestas.html', 'index.html']:
    p = O / f
    s = p.read_text()
    if 'id="dark-fix"' in s:
        a = s.index('<style id="dark-fix">')
        b = s.index('</style>', a) + len('</style>\n')
        s = s[:a] + s[b:]
    i = s.rfind('</style>') + len('</style>\n')
    s = s[:i] + STYLE + s[i:]
    p.write_text(s)
    print('dark-fix ok', f)
