"""v12 · Degradados de marca (Diego, 9 oct 2026). Correr DESPUÉS de build5.py (inyecta CSS en out/*.html).
- Proveedor: Morado → Magenta (#9146FF → #FA1ED2). Sólido de texto: morado.
- Anfitrión: Magenta → Naranja (#FA1ED2 → #FF6905). Sólido de texto/contornos: frambuesa #BE0078 (se lee bien sobre claro).
- Botón principal (uno por pantalla): Lima → Amarillo (#BEFF00 → #FAFA19) con texto oscuro. Nunca blanco.
- WhatsApp: siempre su verde #25D366 con texto blanco.
- Fondos de la app: pastel «nube» (lila · chicle · cielo sobre hielo). Éxito: menta/turquesa."""
from pathlib import Path
OUT = Path('/home/claude/hqv/v5/out')

COMMON = '''
/* ===== v12 · degradados de marca ===== */
:root{--g-prov:linear-gradient(160deg,#9146FF 0%,#FA1ED2 100%);--g-host:linear-gradient(160deg,#FA1ED2 0%,#FF6905 100%);
 --g-cta:linear-gradient(135deg,#BEFF00 0%,#FAFA19 100%);--cta-ink:#1a1033;--wa:#25D366;--ok-solid:#00A884}
@media not (prefers-color-scheme:dark){
 body{background:radial-gradient(1100px 700px at 0% 0%,#E6DCFF 0,rgba(230,220,255,0) 62%),radial-gradient(900px 600px at 100% 8%,#FDE0F6 0,rgba(253,224,246,0) 58%),radial-gradient(1200px 800px at 50% 105%,#DDF3FF 0,rgba(221,243,255,0) 62%),#F0F0FF!important;background-attachment:fixed!important}
}
.btn.cta,.rbar .save .btn.cta{background:var(--g-cta)!important;color:var(--cta-ink)!important;box-shadow:inset 3px 3px 6px rgba(255,255,255,.55),inset -3px -4px 8px rgba(70,80,0,.18),0 8px 18px rgba(120,140,0,.28)!important}
.btn.cta:hover{filter:brightness(1.04)}
.btn.big{background:var(--g-cta)!important;color:var(--cta-ink)!important;box-shadow:inset 3px 3px 6px rgba(255,255,255,.55),inset -3px -4px 8px rgba(70,80,0,.18),0 8px 18px rgba(120,140,0,.28)!important}
.btn.wa,a.wa,.wa.btn{background:#25D366!important;color:#fff!important}
.cta-g,#goProv,.door .go,.plc .sw-r{background:var(--g-cta)!important;color:var(--cta-ink)!important;box-shadow:inset 3px 3px 6px rgba(255,255,255,.55),inset -3px -4px 8px rgba(70,80,0,.18),0 8px 18px rgba(120,140,0,.28)!important}
#goProv[disabled],#goProv:disabled{filter:grayscale(.6);opacity:.55}
'''

SHELL = COMMON + '''
:root{--host:#BE0078}
.btn.host,.pill.host{background:var(--g-host)!important;color:#fff!important}
.badge{background:#FA1ED2}
.door.pv .band{background:var(--g-prov)!important}
.door.hs .band{background:var(--g-host)!important}
.door.pv .emph{border-left-color:#9146FF!important;background:#EFE6FF!important}
.home .door.hs .emph{background:#FFE6F3!important;border-left-color:#FA1ED2!important}
.tab[aria-selected="true"].fs{background:var(--g-host)!important}
.tab[aria-selected="true"].nb{background:var(--g-prov)!important}
.subtabs button[aria-selected="true"]{background:var(--g-host)!important;color:#fff!important}
.nb-sub button[aria-selected="true"]{background:var(--g-prov)!important}
.hero{background:var(--g-host)!important}
.fch .fh{background:var(--g-host)!important}
.fch.on{outline-color:#FA1ED2}
.solc .sh{background:var(--g-prov)!important}
.inv.fs{background:var(--g-host)!important}
.inv.nb{background:var(--g-prov)!important}
[style*="background:var(--prov)"]{background:var(--g-prov)!important}
[style*="background:var(--host)"]{background:var(--g-host)!important}
.steps li.now i,.nsteps li::before{background:var(--g-host)!important}
.trk span.ok i{background:var(--ok-solid)!important}
.plan .pro{background:var(--g-prov)!important}
.doc .pp{color:#BE0078}
'''

# Cotizador = lado anfitrión
COT = COMMON + '''
@media not (prefers-color-scheme:dark){:root{--grape:#BE0078!important;--grape-soft:#FFE3F3!important}}
.btn:not(.cta):not(.ghost):not(.white):not(.wa):not(.sm.ghost){background:var(--g-host)}
.rbar{background:var(--g-host)!important;box-shadow:0 10px 24px rgba(190,0,120,.28)!important}
'''

# Registro de negocio = lado proveedor
REG = COMMON + '''
@media not (prefers-color-scheme:dark){:root{--grape:#9146FF!important;--grape-soft:#EFE6FF!important}}
.btn:not(.cta):not(.ghost):not(.white):not(.wa):not(.secondary){background:var(--g-prov)}
'''


def inject(name, css):
    p = OUT / name
    s = p.read_text()
    if '/* ===== v12 · degradados de marca ===== */' in s:
        print('ya tenía v12:', name)
        return
    i = s.rindex('</style>')
    s = s[:i] + css + s[i:]
    s = s.replace('PROTOTIPO v11', 'PROTOTIPO v12')
    p.write_text(s)
    print('v12 ok', name)


inject('index.html', SHELL)
inject('fiestas.html', COT)
inject('negocio.html', REG)
