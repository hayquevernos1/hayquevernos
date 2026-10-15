"""v16 · Registro (Diego, 14 oct 2026 noche). reg10.html → reg11.html — motor de servicios svc3.js.
Ver encabezado de svc3.js para el detalle de cambios."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'reg10.html').read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:140]
    s = s.replace(a, b, count)


js = (V / 'svc3.js').read_text()
a = s.index('/* ===== v15 · Servicios con el catálogo v2')
b = s.index('\n/* Venue: los servicios se eligen', a)
s = s[:a] + js + s[b:]

CSS = '''
/* ===== v16 · servicios ===== */
input[type=number]::-webkit-inner-spin-button,input[type=number]::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}
input[type=number]{-moz-appearance:textfield;appearance:textfield}
.ways{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:8px!important}
.ways.two{grid-template-columns:repeat(2,minmax(0,1fr))!important;max-width:420px}
.way{flex-direction:column!important;align-items:center!important;text-align:center!important;gap:4px!important;padding:12px 8px!important}
.way .emo{font-size:30px!important}.way b{font-size:13.5px!important;line-height:1.15}.way small{font-size:11px!important}
.fullx{margin-top:8px;font-size:12.5px;background:#F7F4FF;border-radius:14px;padding:8px 11px;line-height:1.4}
.sub2{border-left:4px solid #BEAAFF;padding-left:12px}
.incr input.r-c{color:inherit!important;font-weight:600!important;display:block!important}
.qk{display:flex;flex-wrap:wrap;gap:6px}
.qkb{border:1px dashed #BEAAFF;background:#fff;color:#8205B4;border-radius:99px;padding:5px 10px;font:inherit;font-size:12.5px;font-weight:800;cursor:pointer}
.incr{grid-template-columns:1.4fr 64px 1fr auto!important}.incr.ex{grid-template-columns:1.3fr 56px .9fr 104px auto!important}
.incr .r-m{display:flex;align-items:center;gap:4px;font-weight:900;color:#8205B4}
.tgrp{display:grid;gap:6px;background:#FBFAFF;border-radius:16px;padding:8px}.tgrp .tw{font-size:12.5px}
.tmr{grid-template-columns:130px auto 1fr auto!important}
.seg2{display:grid;gap:6px}.seg2>b{font-size:13px}
.mr{display:grid;grid-template-columns:1fr auto;gap:6px;align-items:center}.mr:has(.sw){grid-template-columns:auto 1fr auto}
.mr input{min-width:0;padding:9px 10px;font-size:14px}
.sw{display:inline-flex;background:#EFE9FF;border-radius:99px;padding:3px}.sw button{border:0;background:none;border-radius:99px;padding:5px 10px;font:inherit;font-size:12px;font-weight:800;color:#5b4b80;cursor:pointer}
.sw button[aria-pressed="true"]{background:linear-gradient(160deg,#9146FF,#FA1ED2);color:#fff}
.sgf{position:absolute;z-index:80;background:#fff;border-radius:14px;box-shadow:0 10px 30px rgba(65,20,95,.22);padding:4px;display:grid;max-width:340px}
.sgf button{border:0;background:none;text-align:left;font:inherit;font-size:13.5px;padding:7px 10px;border-radius:10px;cursor:pointer}.sgf button:hover{background:#F3EEFF}
.pkgc{display:grid;gap:8px;background:#fff;border-radius:20px;padding:12px;box-shadow:var(--hqv-clay-sm,0 4px 12px rgba(65,20,95,.08))}
.pkgc .row{display:flex;gap:8px;align-items:center}.pkgc .pk-n{flex:1}.pkgc .pk-al{width:64px}
.plist .price{white-space:normal!important;text-align:right}
.plist .pph{display:flex;gap:6px;margin-top:4px}.plist .pph img{width:64px;height:48px;object-fit:cover;border-radius:10px}
@media(max-width:560px){.incr,.incr.ex{grid-template-columns:1fr 56px 24px!important;grid-template-areas:"c q x" "u u u" "m m m"!important}.incr .r-c{grid-area:c}.incr .r-q{grid-area:q}.incr .r-u{grid-area:u}.incr .r-x{grid-area:x}.incr .r-m{grid-area:m}
.tmr{grid-template-columns:1fr auto 24px!important}.way small{display:none}
.mr:has(.sw){grid-template-columns:1fr 24px;grid-template-areas:"s x" "d d"}.mr:has(.sw) .sw{grid-area:s;justify-self:start}.mr:has(.sw) .m-x{grid-area:x}.mr:has(.sw) .m-d{grid-area:d}}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# missing(): servicios v16
a = s.index('  S.services.forEach((s,i)=>{svcDefaults(s);const n=catOf(s.cat)?s.cat:`Ficha ${i+1}`;')
b = s.index('  if(!filled(S.svcVar))', a)
s = s[:a] + r'''  S.services.forEach((s,i)=>{svcDefaults(s);const n=catOf(s.cat)?s.cat:`Ficha ${i+1}`;
  if(!s.cat||s.cat==="__new"){m.push(`${n}: categoría`);return;}
  if(!waysOn(s).length){m.push(`${n}: cómo trabajas`);return;}
  if(isCat(s)){if(!s.cater.food&&!s.cater.drink)m.push(`${n}: alimentos o bebidas`);if(s.cater.food&&!s.offers.some(o=>o.kind==="food"))m.push(`${n}: formatos de alimentos`);if(s.cater.drink&&!s.offers.some(o=>o.kind==="drink"))m.push(`${n}: cómo sirves las bebidas`);}
  else if(!s.offers.length&&!(s.ways.staff&&s.staff.length)&&!(s.ways.rent&&s.rent.length))m.push(`${n}: qué ofreces`);
  s.offers.forEach(o=>{if(!offerOk(o,s))m.push(`${n}: precio de ${o.n}`);});
  if(s.ways.staff&&s.staff.length&&!s.staff.every(staffOk))m.push(`${n}: precio del staff`);
  if(s.ways.rent&&s.rent.length&&!s.rent.every(staffOk))m.push(`${n}: precio de renta`);
  if(s.subs.length){if(!filled(s.desc))m.push(`${n}: descripción`);if(!(s.dl||[]).length)m.push(`${n}: cómo lo entregas`);(s.dl||[]).forEach(d=>{if(!dlOk(d))m.push(`${n}: entrega «${d.m}»`);});
  if(!minOk(s.min))m.push(`${n}: mínimo de compra`);if(!promoOk(s.promo))m.push(`${n}: promoción`);}});
  (S.svcPkgs||[]).forEach((P,pi)=>{if(!filled(P.name)||!filled(P.price))m.push(`Paquete ${pi+1}: nombre y precio`);});
''' + s[b:]
rep('if(S.svcVar===undefined)S.svcVar="20";', 'if(S.svcVar===undefined)S.svcVar="20";if(!S.svcPkgs)S.svcPkgs=[];')
rep('ways:{full:false,staff:false,rent:false},offers:[],staff:[],rent:[],open:"",descEdited:false,min:blankMin()',
    'ways:{full:false,staff:false,rent:false},cater:{food:false,drink:false,gas:[]},offers:[],staff:[],rent:[],open:"",descEdited:false,min:blankMin()')
# demo
a = s.index(' {const s0=x.services[0];')
b = s.index('rent:[]});}\n', a) + len('rent:[]});}\n')
s = s[:a] + r''' {const s0=x.services[0];Object.assign(s0,{cat:"Catering",ways:{full:true,staff:true,rent:true},open:"",descEdited:false,cater:{food:true,drink:true,gas:["Mexicana"]},
  offers:[Object.assign(blankOffer("Buffet","food"),{sal:[{d:"Tacos al pastor"},{d:"Esquites"}],dul:[{d:"Churros con chocolate"}],inc:[{c:"Platos",q:"1",u:"por persona"},{c:"Cubiertos",q:"1",u:"juego por persona"},{c:"Servilletas",q:"2",u:"por persona"},{c:"Meseros",q:"1",u:"por cada 25 invitados"}],tar:[{w:"full",price:"350",u:"Por persona",uo:"",alc:""},{w:"staff",price:"180",u:"Por persona",uo:"",alc:""},{w:"rent",price:"260",u:"Por persona",uo:"",alc:""}],ext:[{c:"Pastel de 3 pisos",q:"1",u:"piezas",cost:"1800"}],photos:sp("🌮","#FFB3D9","#FF6DB4")}),
   Object.assign(blankOffer("Banquete","food"),{tiempos:[{n:"Entrada",k:"Salado",d:"Crema de elote"},{n:"Plato fuerte",k:"Salado",d:"Mole poblano"},{n:"Postre",k:"Dulce",d:"Flan napolitano"}],inc:[{c:"Loza y cristalería",q:"",u:""},{c:"Meseros",q:"1",u:"por cada 15 invitados"}],tar:[{w:"full",price:"650",u:"Por persona",uo:"",alc:""},{w:"staff",price:"",u:"Por persona",uo:"",alc:""},{w:"rent",price:"",u:"Por persona",uo:"",alc:""}]}),
   Object.assign(blankOffer("Barra","drink"),{con:[{d:"Margarita",t:"Frío"},{d:"Carajillo",t:"Frío"}],sin:[{d:"Agua de jamaica",t:"Frío"},{d:"Café de olla",t:"Caliente"}],inc:[{c:"Bartender",q:"1",u:"por cada 50 invitados"},{c:"Hielo",q:"",u:""}],tar:[{w:"full",price:"180",u:"Por persona",uo:"",alc:""},{w:"staff",price:"",u:"Por persona",uo:"",alc:""},{w:"rent",price:"",u:"Por persona",uo:"",alc:""}]})],
  staff:[{n:"Meseros",price:"350",u:"Por hora",min:"5"}],rent:[{n:"Chafers y calentadores",price:"150",u:"Por pieza",min:"12"}],photos:[],specs:[]});}
 x.svcPkgs=[{name:"Paquete Fiesta Mexicana",items:["o0-0","o0-2","s0-0"],alc:"50",price:"24000",per:"evento",photos:[]}];
''' + s[b:]
rep('${S.svcHigh&&+S.svcHigh.pct>0&&S.svcHigh.months.length?', '${pkgSite()}${S.svcHigh&&+S.svcHigh.pct>0&&S.svcHigh.months.length?')
rep('variabilidad:S.svcVar,', 'variabilidad:S.svcVar,paquetes:S.svcPkgs,')
rep('modos:s.ways,ofertas:s.offers,', 'modos:s.ways,catering:s.cater,ofertas:s.offers,')

(V / 'reg11.html').write_text(s)
print('ok reg11', len(s))
