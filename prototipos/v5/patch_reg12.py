"""v17 · Registro (Diego, 14 oct 2026 noche). reg11.html → reg12.html — motor svc4.js (ver encabezado)."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'reg11.html').read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:140]
    s = s.replace(a, b, count)


js = (V / 'svc4.js').read_text()
a = s.index('/* ===== v16 · Servicios')
b = s.index('\n/* Venue: los servicios se eligen', a)
s = s[:a] + js + s[b:]

CSS = '''
/* ===== v17 · servicios ===== */
.dlc.closed.ofc{display:flex;align-items:center}.dlc.closed.ofc .dlh{flex:1}
.ofx{border:0;background:none;color:#c0003c;font-weight:900;font-size:16px;padding:0 14px;cursor:pointer}
.of-name{font-weight:800}
.mr{display:grid!important;grid-template-columns:1fr 1.25fr 24px!important;gap:6px;align-items:center}
.mr:has(.tn){grid-template-columns:62px 1fr 1.25fr 24px!important}
.mr .tn{font-size:11px;font-weight:900;color:#8205B4;line-height:1.1;text-transform:uppercase;letter-spacing:.03em}
.mr .ideas{grid-column:1/-1;display:none;flex-wrap:wrap;gap:5px;align-items:center;font-size:12px;color:var(--muted)}
.mr.act .ideas{display:flex}
.idea{border:1px dashed #BEAAFF;background:#fff;color:#8205B4;border-radius:99px;padding:3px 9px;font:inherit;font-size:12px;font-weight:800;cursor:pointer}
.incr .r-d{grid-column:1/-1;font-size:13px;padding:7px 10px}
.incr .r-cj{grid-column:1/-1;font-size:12.5px;color:var(--muted);font-weight:700;display:flex;gap:6px;align-items:center}.incr .r-cj input{width:70px;padding:6px 8px}
.nsr{display:flex;gap:12px;align-items:center;justify-content:space-between;background:#F7F4FF;border-radius:16px;padding:10px 12px}
.nsr b{font-size:13.5px}.nsr .hint{font-size:12px}
.inv .dlc{margin-top:8px}
.lrow{display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:#F7F4FF;border-radius:14px;padding:6px 10px}
.lrow .rn{font-size:13.5px;min-width:110px}.lrow .sl-p{display:flex;align-items:center;gap:4px;font-weight:900;color:#8205B4}.lrow .sl-p input{width:96px}
.lrow select{width:auto}.lrow .ta-al input{width:58px;padding:6px 8px}
.nightc{display:flex;gap:8px;align-items:flex-start;font-size:13px;background:#FFF7D6;border-radius:14px;padding:8px 10px}.nightc input[type=number]{width:80px;padding:4px 8px}
.dlsec{display:grid;gap:6px;margin-top:6px}
details.more{background:#FBFAFF;border-radius:14px;padding:8px 12px}details.more summary{cursor:pointer;font-size:13px;font-weight:800}
.dl-pick{display:grid;gap:6px}
.pkhint{display:block;margin:-4px 0 6px}
.plist .po.hasph{display:grid!important;grid-template-columns:132px 1fr;gap:12px;align-items:start}
.plist .phbig{width:132px;height:100px;object-fit:cover;border-radius:16px}
.plist .pob{display:grid;gap:2px;min-width:0}
.pkgsite{border:2px solid #FAB4FF}
@media(max-width:560px){.mr,.mr:has(.tn){grid-template-columns:1fr 24px!important}.mr .tn{grid-column:1/-1}.mr .m-x{grid-column:2;grid-row:1}.mr:has(.tn) .m-x{grid-row:2}.mr .m-e,.mr .m-d{grid-column:1}
.lrow{display:grid!important;grid-template-columns:1fr 1fr 24px;grid-template-areas:"n p x" "u u u" "m e e";gap:6px}.lrow .rn{grid-area:n}.lrow .sl-p{grid-area:p}.lrow .sr-rm{grid-area:x}.lrow select{grid-area:u;width:100%}.lrow .lm{grid-area:m}.lrow .lx{grid-area:e}.rt-r{grid-template-areas:"n p x" "u u u"!important}
.plist .po.hasph{grid-template-columns:1fr}.plist .phbig{width:100%;height:170px}.nsr{flex-direction:column;align-items:flex-start}}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# recoger en mi local: dirección prellenada (editable) y horario
rep('  ${d.m==="Otro"?`<input type="text" class="dl-desc',
    '''  ${d.m==="Recolección en establecimiento"?`<div class="dl-pick"><label class="hint">📍 ¿Dónde recogen? <span class="opt">Pusimos la dirección de tu negocio; cámbiala si es otra</span></label><input type="text" class="dl-pa" value="${esc(d.pa!==undefined?d.pa:addrLine(S.biz.addr,true))}" placeholder="Calle, número, colonia, alcaldía" aria-label="Dirección para recoger"><input type="text" class="dl-ph" value="${esc(d.ph||"")}" placeholder="Horario para recoger: lun a sáb de 9:00 a 18:00" aria-label="Horario para recoger"></div>`:""}
  ${d.m==="Otro"?`<input type="text" class="dl-desc''')
rep('  q(".dl-desc",x=>x.oninput=e=>{d.desc=e.target.value;changed();});',
    '  q(".dl-desc",x=>x.oninput=e=>{d.desc=e.target.value;changed();});\n  q(".dl-pa",x=>x.oninput=e=>{d.pa=e.target.value;changed();});q(".dl-ph",x=>x.oninput=e=>{d.ph=e.target.value;changed();});')

# missing()
a = s.index('  S.services.forEach((s,i)=>{svcDefaults(s);const n=catOf(s.cat)?s.cat:`Ficha ${i+1}`;')
b = s.index('  (S.svcPkgs||[]).forEach(', a)
s = s[:a] + r'''  S.services.forEach((s,i)=>{svcDefaults(s);const n=catOf(s.cat)?s.cat:`Ficha ${i+1}`;
  if(!s.cat||s.cat==="__new"){m.push(`${n}: categoría`);return;}
  if(isCat(s)){if(!s.cater.food&&!s.cater.drink)m.push(`${n}: alimentos o bebidas`);if(s.cater.food&&!s.offers.some(o=>o.kind==="food"))m.push(`${n}: formatos de alimentos`);if(s.cater.drink&&!s.offers.some(o=>o.kind==="drink"))m.push(`${n}: cómo sirves las bebidas`);}
  else if(!s.offers.length&&!s.ways.staff&&!s.ways.rent)m.push(`${n}: qué ofreces`);
  s.offers.forEach(o=>{if(!offerOk(o))m.push(`${n}: precio de ${offTitle(o)}`);});
  if(s.offers.length){if(!s.dl.length)m.push(`${n}: cómo entregas tu servicio completo`);s.dl.forEach(d=>{if(!dlOk(d))m.push(`${n}: entrega «${d.m}»`);});}
  if(s.ways.staff){if(!s.staff.length||!s.staff.every(staffOk))m.push(`${n}: perfiles y precio del staff`);}
  if(s.ways.rent){if(!s.rent.length||!s.rent.every(staffOk))m.push(`${n}: qué rentas y su precio`);if(!s.rtx.dl.length)m.push(`${n}: cómo entregas lo que rentas`);s.rtx.dl.forEach(d=>{if(!dlOk(d))m.push(`${n}: entrega de renta «${d.m}»`);});}
  if(s.subs.length&&!filled(s.desc))m.push(`${n}: descripción`);});
''' + s[b:]

# demo
a = s.index(' {const s0=x.services[0];')
b = s.index(' x.svcPkgs=', a)
s = s[:a] + r''' {const s0=x.services[0];const B=blankOffer("Buffet","food"),Q=blankOffer("Banquete","food"),R=blankOffer("Barra","drink");
  Object.assign(B,{name:"Taquiza Mexicana",sal:[{e:"Tacos",d:"Pastor"},{e:"Elotes y esquites",d:"Esquites"}],dul:[{e:"Churros",d:"Churros con chocolate"}],inc:[{c:"Platos",q:"60",u:"piezas",d:"Loza",cj:""},{c:"Servilletas",q:"2",u:"cajas",d:"Papel",cj:"100"},{c:"Meseros",q:"1",u:"por cada 25 invitados",d:"Uniformados",cj:""}],tar:[{w:"full",price:"350",u:"Por persona",uo:"",alc:""},{w:"rent",price:"260",u:"Por persona",uo:"",alc:""}],noStaff:true,ext:[{c:"Pastel de 3 pisos",q:"1",u:"piezas",d:"",cj:"",cost:"1800"}],photos:sp("🌮","#FFB3D9","#FF6DB4")});
  Object.assign(Q,{name:"Menú Oro",tiempos:[{e:"Entradas",d:"Ensalada de betabel con queso de cabra"},{e:"Cremas",d:"Crema de elote"},{e:"Platos fuertes",d:"Mole poblano con pollo"},{e:"Postres tradicionales",d:"Flan napolitano"}],inc:[{c:"Loza",q:"",u:"",d:"Blanca",cj:""},{c:"Meseros",q:"1",u:"por cada 15 invitados",d:"",cj:""}],tar:[{w:"full",price:"650",u:"Por persona",uo:"",alc:""}]});
  Object.assign(R,{con:[{e:"Coctelería",d:"Margarita"},{e:"Bebidas preparadas",d:"Carajillo frío preparado"}],sin:[{e:"Aguas, limonadas y naranjadas",d:"Agua de jamaica"}],inc:[{c:"Bartender",q:"1",u:"por cada 50 invitados",d:"Uniformado",cj:""},{c:"Hielo",q:"",u:"",d:"En cubo",cj:""}],tar:[{w:"full",price:"180",u:"Por persona",uo:"",alc:""}]});
  B.promo=s0.promo;B.min=s0.min;
  Object.assign(s0,{min:blankMin(),promo:blankPromo(),cat:"Catering",open:"",descEdited:false,cater:{food:true,drink:true,gas:["Mexicana"]},offers:[B,Q,R],askStaff:true,askRent:true,
  staff:[{n:"Meseros",price:"350",u:"Por hora",min:"5",xh:"90"},{n:"Taqueros",price:"450",u:"Por hora",min:"5",xh:"110"}],rent:[{n:"Chafers y calentadores",price:"150",u:"Por pieza",min:""}],photos:[],specs:[],
  stx:{night:true,fee:"150",dl:[Object.assign(blankDl("Servicio presencial en el evento"),{cobra:false})],dlOpen:-1,min:blankMin(),promo:blankPromo()},
  rtx:{dl:[Object.assign(blankDl("Recolección en establecimiento"),{cobra:false,ph:"Lun a sáb de 9:00 a 18:00"})],dlOpen:-1,min:blankMin(),promo:blankPromo()}});}
''' + s[b:]
rep(' x.svcPkgs=[{name:"Paquete Fiesta Mexicana",items:["o0-0","o0-2","s0-0"]', ' x.svcPkgs=[{name:"Paquete Fiesta Mexicana",items:["o0-0","o0-2","s0-0"]')

# sitio: paquetes primero
rep('${pkgSite()}${S.svcHigh&&+S.svcHigh.pct>0', '${S.svcHigh&&+S.svcHigh.pct>0')
rep('<div style="display:grid;gap:8px"><h3>🎉 Servicios</h3>', '<div style="display:grid;gap:8px"><h3>🎉 Servicios</h3>${pkgSite()}')
rep('ways:{full:false,staff:false,rent:false},cater:{food:false,drink:false,gas:[]},offers:[]', 'ways:{full:false,staff:false,rent:false},cater:{food:false,drink:false,gas:[]},askStaff:null,askRent:null,offers:[]')
(V / 'reg12.html').write_text(s)
print('ok reg12', len(s))
