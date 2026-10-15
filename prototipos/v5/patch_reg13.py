"""v18 · Registro (Diego, 14 oct 2026 noche). reg12.html → reg13.html — motor svc5.js (ver encabezado) + micrositio.
- Micrositio: las verticales (servicios · venue · planner) en una sola línea fija arriba al hacer scroll;
  sin el título repetido dentro de cada vertical; paquetes primero y luego «Servicios por separado»."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'reg12.html').read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:140]
    s = s.replace(a, b, count)


js = (V / 'svc5.js').read_text()
a = s.index('/* ===== v17 · Servicios')
b = s.index('\n/* Venue: los servicios se eligen', a)
s = s[:a] + js + s[b:]

CSS = '''
/* ===== v18 · ficha como paquete ===== */
.paxr{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:13.5px;font-weight:800}.paxr input{width:96px}
.incwrap{display:grid;gap:12px;border:1.5px dashed var(--line);border-radius:18px;padding:12px}
.incwrap .inct{font-size:14.5px}
.incsec{display:grid;gap:8px}
.rws{display:grid;gap:8px}
.relbox{display:grid;gap:6px;border-left:4px solid #BEAAFF;padding-left:10px}.relh{font-size:13.5px}
.crewl{display:flex;flex-wrap:wrap;gap:8px}
.crewr{display:flex;align-items:center;gap:6px;background:var(--paper);border:1.5px solid var(--line);border-radius:14px;padding:5px 6px 5px 12px;font-size:13.5px;font-weight:700}
.crewr input{width:62px;padding:6px 8px}
.durh{font-weight:800;font-size:13.5px}
.arrive{display:block;background:var(--paper);border-radius:14px;padding:8px 11px;line-height:1.4}
.tgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.tgrid.one{grid-template-columns:minmax(0,1fr);max-width:520px}
.tgrid .tgrp{align-content:start}.tgrid .tgrp>.hint{font-size:12px;line-height:1.3}
.tgrid .tarr{grid-template-columns:1fr!important;display:grid!important;gap:6px}
.tgrid .tw-full{border:2px solid #BEAAFF}
.reco{display:grid;gap:8px;border-radius:20px;padding:14px;background:linear-gradient(160deg,#41145F,#8205B4);color:#fff}
.reco .mk{font-size:11px;font-weight:900;letter-spacing:.12em;color:#BEFF00}.reco .hint{color:rgba(255,255,255,.88)!important}
.recor{display:flex;gap:10px;align-items:center;justify-content:space-between;background:rgba(255,255,255,.12);border-radius:14px;padding:8px 10px}
.recor span{display:grid}.recor small{opacity:.85;font-size:12px}.recob{display:flex!important;gap:8px;align-items:center;flex:none}.reco .link{color:#fff}
.ctag{display:block;font-weight:600;font-size:11.5px;color:var(--muted)}
.mssub{margin:6px 0 0;font-size:15px}
@media(max-width:760px){.tgrid{grid-template-columns:minmax(0,1fr)}}
@media(max-width:560px){.recor{flex-direction:column;align-items:flex-start}}
/* ===== v18 · micrositio: verticales en una línea y fijas ===== */
.site .net,.public-site .net{position:relative!important}
.vtabs{flex-wrap:nowrap!important;position:sticky!important;top:0;z-index:5!important;background:var(--card)!important;padding:8px 0!important;box-shadow:-24px 0 0 var(--card),24px 0 0 var(--card),0 10px 12px -10px rgba(35,23,58,.45)}
.price .pl{display:block;white-space:nowrap}
@media(max-width:920px){.editor.show-preview .phone{overflow:clip}.editor.show-preview .site{overflow:visible}.editor.show-preview .site .vtabs{top:var(--tgh,58px)}}
.vtabs button{flex:1 1 0;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:9px 6px!important;font-size:13px!important}
@media(max-width:420px){.vtabs button{font-size:12px!important}}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# demo: banquete como paquete; catering ya sin «staff con insumos del cliente»
a = s.index(' {const s0=x.services[0];')
b = s.index(' x.svcPkgs=', a)
s = s[:a] + r''' {const s0=x.services[0];const B=blankOffer("Buffet","food"),Q=blankOffer("Banquete","food"),R=blankOffer("Barra","drink");
  Object.assign(B,{name:"Taquiza Mexicana",pax:"60",sal:[{e:"Tacos",d:"Pastor"},{e:"Elotes y esquites",d:"Esquites"}],dul:[{e:"Churros",d:"Churros con chocolate"}],inc:[{c:"Platos",q:"60",u:"piezas",d:"Loza",cj:""},{c:"Servilletas",q:"2",u:"cajas",d:"Papel",cj:"100"}],crew:[{n:"Meseros",q:"3",auto:true},{n:"Cocineros",q:"1",auto:true},{n:"Taqueros",q:"2",auto:false}],tar:[{w:"full",price:"350",u:"Por persona",uo:"",alc:""},{w:"rent",price:"260",u:"Por persona",uo:"",alc:""},{w:"labor",price:"",u:"Por persona",uo:"",alc:""}],ext:[{c:"Pastel de 3 pisos",q:"1",u:"piezas",d:"",cj:"",cost:"1800"}],photos:sp("🌮","#FFB3D9","#FF6DB4")});
  Object.assign(Q,{name:"Menú Oro",pax:"100",tiempos:[{e:"Entradas",d:"Ensalada de betabel con queso de cabra"},{e:"Cremas",d:"Crema de elote"},{e:"Platos fuertes",d:"Mole poblano con pollo"},{e:"Postres tradicionales",d:"Flan napolitano"}],
   inc:[{c:"Platos",q:"100",u:"piezas",d:"Loza",cj:""},{c:"Mantelería",q:"10",u:"piezas",d:"Redondos",cj:""},{c:"Servilletas",q:"100",u:"piezas",d:"Tela",cj:""}],
   svcs:[{cat:"Mobiliario y montaje",rows:[{c:"Sillas",q:"100",u:"piezas",d:"Tiffany",cj:""},{c:"Mesas",q:"10",u:"mesas",d:"Redondas",cj:""}]},{cat:"Cristalería y cubertería",rows:[{c:"Cristalería",q:"100",u:"juegos",d:"",cj:""}]}],
   crew:[{n:"Capitanes de meseros",q:"1",auto:true},{n:"Meseros",q:"7",auto:true},{n:"Cocineros",q:"2",auto:true},{n:"Ayudantes de cocina",q:"2",auto:true}],
   tar:[{w:"full",price:"650",u:"Por persona",uo:"",alc:""},{w:"rent",price:"480",u:"Por persona",uo:"",alc:""},{w:"labor",price:"180",u:"Por persona",uo:"",alc:""}]});
  Object.assign(R,{pax:"50",con:[{e:"Coctelería",d:"Margarita"},{e:"Bebidas preparadas",d:"Carajillo frío preparado"}],sin:[{e:"Aguas, limonadas y naranjadas",d:"Agua de jamaica"}],inc:[{c:"Hielo",q:"20",u:"kilos",d:"En cubo",cj:""},{c:"Vasos",q:"150",u:"piezas",d:"Acrílico",cj:""}],crew:[{n:"Bartenders",q:"1",auto:true}],tar:[{w:"full",price:"180",u:"Por persona",uo:"",alc:""}]});
  B.promo=s0.promo;B.min=s0.min;
  Object.assign(s0,{min:blankMin(),promo:blankPromo(),cat:"Catering",open:"",descEdited:false,cater:{food:true,drink:true,gas:["Mexicana"]},offers:[B,Q,R],askStaff:null,askRent:true,
  staff:[],rent:[{n:"Chafers y calentadores",price:"150",u:"Por pieza",min:""}],photos:[],specs:[],
  rtx:{dl:[Object.assign(blankDl("Recolección en establecimiento"),{cobra:false,ph:"Lun a sáb de 9:00 a 18:00"})],dlOpen:-1,min:blankMin(),promo:blankPromo()}});}
''' + s[b:]
rep(' x.svcPkgs=[{name:"Paquete Fiesta Mexicana",items:["o0-0","o0-2","s0-0"]', ' x.svcPkgs=[{name:"Paquete Fiesta Mexicana",items:["o0-0","o0-2","r0-0"]')

# micrositio: sin título repetido cuando hay pestañas; paquetes primero y luego servicios por separado
rep('<div style="display:grid;gap:8px"><h3>🎉 Servicios</h3>${pkgSite()}${sv.length?',
    '<div style="display:grid;gap:8px">${VT.length>1?"":"<h3>🎉 Servicios</h3>"}${pkgSite()}${pkgSite()&&sv.length?`<h3 class="mssub">🧩 Servicios por separado</h3>`:""}${sv.length?')
rep('<div style="display:grid;gap:8px"><h3>🏡 Venue</h3>', '<div style="display:grid;gap:8px">${VT.length>1?"":"<h3>🏡 Venue</h3>"}')
rep('<div style="display:grid;gap:8px"><h3>📋 Event planner</h3>', '<div style="display:grid;gap:8px">${VT.length>1?"":"<h3>📋 Event planner</h3>"}')
rep('const VT=[S.types.services&&["svc","🎉 Mis servicios"],S.types.venue&&["venue","🏡 Mi venue"],S.types.planner&&["planner","📋 Event planner"]]',
    'const VT=[S.types.services&&["svc","🎉 Servicios"],S.types.venue&&["venue","🏡 Venue"],S.types.planner&&["planner","📋 Planner"]]')
rep('root.querySelectorAll("[data-vp]").forEach(x=>x.hidden=x.dataset.vp!==t.dataset.vt);',
    'root.querySelectorAll("[data-vp]").forEach(x=>x.hidden=x.dataset.vp!==t.dataset.vt);const tb=t.closest(".vtabs");if(tb&&tb.getBoundingClientRect().top<=8)tb.scrollIntoView({block:"start"});')
rep('variabilidad:S.svcVar,paquetes:S.svcPkgs,', 'variabilidad:S.svcVar,paquetes:S.svcPkgs,recomendacionesRechazadas:S.svcRecoNo||[],')
(V / 'reg13.html').write_text(s)
print('ok reg13', len(s))
