"""v24 · Registro (Diego, 15 oct 2026). reg15.html → reg16.html — «Mi negocio» en 4 bloques (biz2.js)."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'reg15.html').read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:140]
    s = s.replace(a, b, count)


js = (V / 'biz2.js').read_text()
rep('\nfunction drawSvcStepOld(){', '\n' + js + '\nfunction drawSvcStepOld(){')
rep('if(b.visits===null||b.visits===undefined)m.push("¿Recibes clientes en tu negocio?");',
    'bzDefaults();if(b.attends===null)m.push("¿Atiendes clientes en tu negocio?");if(b.attends){if(!b.modes.length)m.push("Para qué atiendes clientes en tu negocio");if(!b.hDays.length||!filled(b.hOpen)||!filled(b.hClose))m.push("Horario de atención");}')
rep('exampleState=function(){const x=__exampleState();x.biz.links=[{t:"Sitio web",u:"lupitadulces.mx"}];x.biz.visits=true;',
    'exampleState=function(){const x=__exampleState();x.biz.links=[{t:"Sitio web",u:"lupitadulces.mx"}];x.biz.visits=true;x.biz.attends=true;x.biz.modes=["retiro","cita"];x.biz.hDays=["lun","mar","mie","jue","vie","sab"];x.biz.hOpen="09:00";x.biz.hClose="18:00";x.me={photo:samplePic("🙂","#FFD25E","#FF6905",600,600),instagram:"@lupi.ramirez",tiktok:"",facebook:"",links:[],whatsapp:"55 8765 4321",email:"lupita.ramirez@gmail.com",gender:"Mujer",genderOther:"",birthday:"1990-05-12",pub:{social:false}};')
rep("${b.visits?'<span>🏪 Recibe clientes en su local</span>':\"\"}",
    "${b.attends&&(b.modes||[]).length?(b.modes||[]).map(m=>`<span>${(BZ_MODES.find(x=>x[0]===m)||[\"\",\"\"])[1]}</span>`).join(\"\"):\"\"}${bzHours(b)?`<span>🕒 ${esc(bzHours(b))}</span>`:\"\"}")
rep('<div class="ms-name">${esc(b.name||"Tu negocio")}</div>',
    '<div class="ms-name">${esc(b.name||"Tu negocio")}</div>${b.owner?`<div class="ms-own">${S.me&&S.me.photo?`<img src="${S.me.photo}" alt="">`:""}<span>Te atiende <b>${esc(b.owner)}</b></span></div>`:""}')
rep('negocio:S.biz.name,', 'negocio:S.biz.name,atencion:{atiende:S.biz.attends,modos:S.biz.modes,dias:S.biz.hDays,abre:S.biz.hOpen,cierra:S.biz.hClose},perfilPersonal:S.me?{whatsapp:S.me.whatsapp,correo:S.me.email,genero:S.me.gender==="Otro"?(S.me.genderOther||"Otro"):S.me.gender,cumpleanos:S.me.birthday,redes:{instagram:S.me.instagram,tiktok:S.me.tiktok,facebook:S.me.facebook}}:null,')
CSS = '''
/* ===== v24 · Mi negocio en 4 bloques ===== */
.bz-sec{display:grid;gap:16px;border:1.5px solid var(--line);border-radius:22px;padding:16px;background:var(--card)}
.bz-h{display:flex;gap:10px;align-items:flex-start}.bz-h>b{flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(135deg,#9146FF,#FA1ED2);color:#fff;font-weight:900}
.bz-h span{display:grid;gap:1px}.bz-h strong{font-size:17px}.bz-h small{font-size:12.5px;color:var(--help,#9A92AE)}
.bz-att{display:grid;gap:10px}.bz-hr .field{gap:2px}.bz-hr input{width:140px}
.bz-priv{margin:0;background:var(--paper);border-radius:14px;padding:10px 12px;font-size:12.5px;line-height:1.45;color:var(--muted)}
.ms-own{display:flex;align-items:center;gap:8px;font-size:13px;margin-top:4px}.ms-own img{width:28px;height:28px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,.7)}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]
(V / 'reg16.html').write_text(s)
print('ok reg16', len(s))
