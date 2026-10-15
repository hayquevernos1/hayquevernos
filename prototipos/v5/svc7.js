/* ===== v24: cobertura por producto (zona general por defecto; paquete = zona común de sus productos); «Tu personal de <categoría>» como servicio
   cotizable que se arma solo desde «Solo tu personal» (un precio por perfil, se piden resolver precios distintos); personal compacto en celular.
   ===== v23: confeti propio (al alinear, al guardar producto o paquete) y emblema «Servicio» por cada producto terminado; «ruleta» pasa a «Arma tu servicio» en pantalla.
   ===== v22: sin saltos de pantalla al elegir; paquetes bloqueados hasta 2 productos; «Solo tu personal» compacto (filas, ± y políticas en botones).
   ===== v21 · Mis servicios con la ruleta (Diego, 15 oct 2026) =====
   v21: la entrega vive dentro de «¿Cómo lo cobras?»: Completo = entrega incluida; Sin personal = sin «¿cuántas piezas?» y con
   «¿Cómo lo entregas?» (a domicilio con su cobro, condiciones y ejemplo / recoger en mi local con la dirección del negocio);
   Solo tu personal = precio por perfil (cantidad, $, unidad, mín. horas, hora extra) + políticas del personal.
   «¿Para cuántas personas alcanza?» pasa a una tarjeta destacada con la vista del anfitrión. ----- v20 -----
   · «¿En qué tipo de eventos trabajas?» → aviso de 2 pasos (1. productos uno por uno · 2. paquetes) → buscador que alinea → ruleta de 4 rodillos.
   · Guardar la combinación abre «Dale identidad»: nombre → ¿qué incluye? (platillos, insumos, staff) → ¿cómo lo cobras? →
     ¿para cuántas personas alcanza? con «así lo verá el anfitrión» → Más opciones plegable (fotos, extras con precio, entrega,
     mínimo, promoción) → link para compartir el producto.
   · Paquetes: se eligen 2+ productos; la ficha empieza en blanco, con precio sugerido (suma) y guarda de qué productos sale.
   · El sitio muestra los productos por categoría y los paquetes primero. Base: ruleta_data.js (Excel v2). */
const RU=window.RULETA||{cats:[],rows:[],staff:{},pre:{},emo:{}};
const RU_T=new Map(),RU_U={};
RU.rows.forEach(([c,s,f,d,u,o])=>{if(!RU_T.has(c))RU_T.set(c,new Map());const A=RU_T.get(c);if(!A.has(s))A.set(s,new Map());const F=A.get(s);if(!F.has(f))F.set(f,[]);F.get(f).push(d);RU_U[[c,s,f,d].join("|")]=[u,o];});
const RU_LAB=["Categoría","Servicio o producto","Formato","Detalle"];
const ruOpts=(i,sel)=>{try{return i===0?RU.cats:i===1?[...RU_T.get(sel[0]).keys()]:i===2?[...RU_T.get(sel[0]).get(sel[1]).keys()]:RU_T.get(sel[0]).get(sel[1]).get(sel[2]);}catch(e){return[];}};
const RU_MASC={"Catering":"c_15","Música":"c_14","Entretenimiento y shows":"c_03","Infraestructura":"c_07","Mobiliario y montaje":"c_07","Cristalería y cubertería":"c_10","Audio, iluminación, foto y video":"c_13","Tecnología":"c_09","Decoración y ambientación":"c_02","Marketing y comunicación":"c_08","Transporte":"c_06","Hospedaje":"c_12","Maquillaje y estilismo":"c_01","Registro y protocolo":"c_07","Exposición y negocios":"c_09","Souvenirs y regalos":"c_11","Seguridad, salud y protección civil":"c_06","Actividades y experiencias":"c_03","Impresión y producción gráfica":"c_08","Vestuario y accesorios":"c_07","Permisos y trámites":"c_12","Sustentabilidad y limpieza":"c_06"};
const ruMasc=s=>s[1]==="Bebidas"?"c_04":/Pastel|Reposter|Postres/.test(s[1]||"")?"c_01":s[2]==="Barril"?"c_05":RU_MASC[s[0]]||"c_07";
const RU_UNITS=["Por persona","Por evento","Por pieza","Por hora","Por día","Por kilo","Por litro","Por caja","Por noche","Por viaje","Por m²","Por docena","Por ciento","Por millar","Por paquete","Por juego","Por porción","Por proyecto","Por trámite","Por sesión","Por stand","Por envío","Por mes","Por turno (5 h)"];
const RU_FIXED=["Por persona","Por evento","Por proyecto","Por trámite","Por sesión","Por mes"];
const ruNoun=u=>({"Por hora":"horas","Por pieza":"piezas","Por caja":"cajas","Por noche":"noches","Por docena":"docenas","Por porción":"porciones","Por kilo":"kilos","Por día":"días","Por juego":"juegos","Por envío":"envíos","Por litro":"litros","Por viaje":"viajes","Por m²":"m²","Por ciento":"cientos","Por millar":"millares","Por paquete":"paquetes","Por stand":"stands","Por turno (5 h)":"turnos"})[u]||u.replace(/^Por /,"");
const RU_DISHES=[...new Set(["Salado","Dulce"].flatMap(k=>Object.values(C2.cocina[k]||{}).flatMap(g=>Object.values(g).flat())))];
const RU_INS=["Platos","Cubiertos","Servilletas","Vasos","Copas","Mantelería","Cubremanteles","Charolas","Chafers","Hielo","Popotes","Mezcladores","Desechables biodegradables","Loza","Cristalería","Carbón","Gas","Bolsas para basura","Extensiones eléctricas","Cables","Montaje y desmontaje","Traslado","Iluminación básica","Bocina","Micrófono","Mesa de servicio","Toldo","Decoración de mesa"];
const ruIns=c=>{const A=RU_T.get(c);return[...new Set([...RU_INS,...(A?[...A.values()].flatMap(F=>[...F.keys()]):[]).filter(x=>x!=="Otro")])];};
const RU_EXTRAS=["Hora extra","Persona extra","Mesero extra","Bartender extra","Kilo extra","Pieza extra","Botella extra","Traslado fuera de zona","Montaje especial"];
const RU_EXU={"hora extra":"por hora","persona extra":"por persona","mesero extra":"por mesero","bartender extra":"por bartender","kilo extra":"por kilo","pieza extra":"por pieza","botella extra":"por botella","traslado fuera de zona":"por viaje","montaje especial":"por evento"};
const ruExU=c=>RU_EXU[nrm(c).trim()]||(/hora/i.test(c)?"por hora":/kilo|kg/i.test(c)?"por kilo":/persona/i.test(c)?"por persona":"por evento");
const RU_TL={full:["🎉 Completo","Con tu equipo y tu personal"],rent:["📦 Sin personal","Lo llevas o lo recogen"],labor:["🙋 Solo tu personal","Con los insumos del cliente"]};
function ruConfetti(n){if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;let c=document.getElementById("ruConf");if(!c){c=document.createElement("canvas");c.id="ruConf";c.style.cssText="position:fixed;inset:0;pointer-events:none;z-index:120";document.body.appendChild(c);}
 const x=c.getContext("2d");c.width=innerWidth;c.height=innerHeight;const cols=["#7B2FF7","#FA1ED2","#FF6905","#BEFF00","#FAFA19","#00C389"];
 const P=Array.from({length:n||120},()=>({x:innerWidth*(.25+Math.random()*.5),y:innerHeight*.35,vx:(Math.random()-.5)*14,vy:-Math.random()*13-4,s:5+Math.random()*6,c:cols[Math.random()*6|0],a:Math.random()*6}));let f=0;
 (function go(){x.clearRect(0,0,c.width,c.height);P.forEach(q=>{q.vy+=.33;q.x+=q.vx;q.y+=q.vy;q.a+=.2;x.save();x.translate(q.x,q.y);x.rotate(q.a);x.fillStyle=q.c;x.fillRect(-q.s/2,-q.s/2,q.s,q.s*.6);x.restore();});if(++f<110)requestAnimationFrame(go);else x.clearRect(0,0,c.width,c.height);})();}
/* v25 · cada perfil de personal es un producto independiente (un perfil, un precio) */
const ruStaffBy=n=>(S.rprods||[]).find(x=>x.kind==="staff"&&nrm(x.n||"")===nrm(n));
const RU_XU=["por hora","por turno (5 h)","por evento","por día"];
const ruShortU=t=>t.replace(/^por /,"").replace("turno (5 h)","turno");
/* plural del primer término: 7 meseros, 2 capitanes de meseros */
const ruPl=(n,q)=>{if(+q<=1)return n.toLowerCase();const w=n.toLowerCase().split(" ");const x=w[0];w[0]=/[aeiouáéó]$/.test(x)||/er$/.test(x)?x+"s":/[áóé]n$/.test(x)?x.replace(/án$/,"anes").replace(/ón$/,"ones").replace(/én$/,"enes"):/[lrndj]$/.test(x)?x+"es":x+"s";return w.join(" ");};
const ruXU=u=>(RU_LU.find(x=>x[0]===u)||["","por hora"])[1];
function ruLabRow(n,q){const s=ruStaffBy(n),r=s&&s.labor[0];return r?{n,q:q||"1",p:r.p,u:r.u,min:r.min,xh:r.xh,xu:r.xu||ruXU(r.u)}:{n,q:q||"1",p:"",u:"Por hora",min:"5",xh:"",xu:"por hora"};}
function ruNewStaff(r,cat){const n=r.n;return Object.assign(ruBlankMore(),{id:"st-"+slug(n),kind:"staff",n,name:n,dims:[cat,"Personal independiente","Solo talento",n],otro:"",dishes:[],ins:[],crew:[],pax:"",tw:["labor"],tar:ruBlankT("Por hora"),emb:0,labor:[{n,q:"1",p:r.p,u:r.u,min:r.min,xh:r.xh,xu:r.xu||ruXU(r.u)}]});}
function ruPropStaff(sp){const e=sp.labor[0];(S.rprods||[]).forEach(x=>{if(x.kind!=="prod")return;x.labor.forEach(r=>{if(nrm(r.n)===nrm(sp.n)){r.p=e.p;r.u=e.u;r.min=e.min;r.xh=e.xh;r.xu=e.xu;}});});}
function ruSyncStaff(p,done){const cat=p.dims[0],added=[],conf=[];
 p.labor.forEach(r=>{let sp=ruStaffBy(r.n);if(!sp){sp=ruNewStaff(r,cat);S.rprods.push(sp);added.push(r.n);return;}const e=sp.labor[0];
  if(filled(e.p)&&filled(r.p)&&+e.p!==+r.p)conf.push({n:r.n,sp,a:e.p,b:r.p,ua:e.u,ub:r.u,r});else{Object.assign(e,{p:filled(r.p)?r.p:e.p,u:r.u,min:r.min,xh:r.xh,xu:r.xu});}});
 const fin=()=>{(S.rprods||[]).filter(x=>x.kind==="staff").forEach(ruPropStaff);ruDrawLists();changed();if(added.length)ruToast(`🙋 Sumamos a «Tu personal»: ${added.join(", ")}. También se cotizan solos.`);done&&done();};
 if(!conf.length){fin();return;}
 const md=document.createElement("div");md.className="rmodal";md.innerHTML=`<div class="rsheet ru-confl"><span class="ru-embk">🙋 TU PERSONAL</span><h2>Un perfil, un precio</h2><span>Estos perfiles ya tenían otro precio. ¿Con cuál te quedas para todos tus productos?</span>
  ${conf.map((c,i)=>`<div class="ru-cf" data-i="${i}"><b>${esc(c.n)}</b><span class="row"><button type="button" class="btn sm ru-cfa">${money(c.a)} ${esc(ruXU(c.ua))}</button><button type="button" class="btn sm ghost ru-cfb">${money(c.b)} ${esc(ruXU(c.ub))}</button></span></div>`).join("")}</div>`;
 document.body.appendChild(md);let left=conf.length;
 md.querySelectorAll(".ru-cf").forEach(R=>{const c=conf[+R.dataset.i],pick=a=>{const e=c.sp.labor[0];if(a){/* se queda el de antes */}else Object.assign(e,{p:c.r.p,u:c.r.u,min:c.r.min,xh:c.r.xh,xu:c.r.xu});R.remove();if(--left===0){md.remove();fin();}};R.querySelector(".ru-cfa").onclick=()=>pick(true);R.querySelector(".ru-cfb").onclick=()=>pick(false);});}
function ruEmblem(p){const n=S.remb,m=ruMasc(p.dims);const md=document.createElement("div");md.className="rmodal";
 md.innerHTML=`<div class="rsheet ru-embs"><span class="ru-embk">🏅 NUEVO EMBLEMA</span><div class="ru-emb"><img src="img/${m}.webp" alt=""><span>SERVICIO</span></div><h2>¡${esc(p.name)} ya está listo!</h2><span>Ganaste el emblema de <b>Servicio de ${esc(p.dims[0])}</b>. Llevas <b>${n}</b> ${n===1?"servicio":"servicios"} en tu sitio.</span>
  <span class="hint" style="color:rgba(255,255,255,.85)!important">${(S.rprods||[]).length>=2?"Ya puedes combinar tus productos en paquetes.":"Con un producto más desbloqueas los paquetes."}</span><button type="button" class="btn cta" id="ruEmbOk">¡Seguir! 🎉</button></div>`;
 document.body.appendChild(md);const close=()=>md.remove();md.querySelector("#ruEmbOk").onclick=close;md.onclick=e=>{if(e.target===md)close();};hqvTrack("emblema_servicio",{n});}
let RU_EDIT=null,RU_PICK=false,RU_PICKED=[],RU_BUSY=[null,null,null,null],RU_DRAG=null,RU_MOVED=false,RU_LASTM="";
const ruBlankT=u=>({full:{p:"",u,q:""},rent:{p:"",u,q:""},labor:{p:"",u:"Por hora",q:""}});
function ruDefaults(){if(!S.rprods)S.rprods=[];if(!S.rpkgs)S.rpkgs=[];
 /* v24 → v25: «Tu personal de X» (grupo) se separa en un producto por perfil */
 if(S.rprods.some(x=>x.kind==="staff"&&!x.n)){const old=S.rprods.filter(x=>x.kind==="staff"&&!x.n);S.rprods=S.rprods.filter(x=>!old.includes(x));old.forEach(o=>o.labor.forEach(r=>{if(!ruStaffBy(r.n))S.rprods.push(ruNewStaff(r,o.dims[0]));}));}
 S.rprods.forEach(x=>(x.labor||[]).forEach(r=>{if(!r.xu)r.xu=ruXU(r.u);}));if(!S.rsel||!RU_T.has(S.rsel[0]))S.rsel=["Catering","Bebidas","Barra","Sin alcohol"];}
const ruLpol=()=>({night:true,nightPct:"50",ride:false,rideFee:"",meal:true,uniform:true});
function ruBlankMore(){return{cov:{same:true,zones:[{state:"",all:false,munis:[]}]},photos:[],ext:[],dl:[],dlOpen:-1,dlx:{dl:[],dlOpen:-1},labor:[],lpol:ruLpol(),min:blankMin(),promo:blankPromo()};}
const RU_LU=[["Por hora","por hora"],["Por turno (5 h)","por turno (5 h)"],["Por evento","por evento"],["Por día","por día"]];
const ruLabTot=p=>(p.labor||[]).reduce((a,r)=>a+(+r.p||0)*(+r.q||1)*(r.u==="Por hora"?(+r.min||5):1),0);
function ruName(dims,otro){const lc=x=>x.charAt(0).toLowerCase()+x.slice(1),gen=["Alimentos","Bebidas","Otro","Personal independiente"].includes(dims[1])||nrm(dims[2]).includes(nrm(dims[1]).slice(0,5));
 const base=gen?dims[2]:`${dims[1]} ${dims[2]}`;
 return dims[1]==="Personal independiente"?dims[3]:dims[2]==="Otro"?dims[1]:dims[3]==="Otro"?(otro?`${base} ${lc(otro)}`:base):(nrm(dims[3])===nrm(dims[2])?base:`${base} ${lc(dims[3])}`);}
function ruProd(dims,otro){const [u]=RU_U[dims.join("|")]||["Por evento"],st=RU.staff[dims[0]]||[];
 return Object.assign({id:"p"+Date.now().toString(36)+Math.random().toString(36).slice(2,5),kind:"prod",dims,otro:otro||"",name:ruName(dims,otro),dishes:[],ins:[],crew:(RU.pre[dims[0]]||[]).filter(n=>st.includes(n)).map(n=>({n,q:"1"})),pax:"",tw:[],tar:ruBlankT(u)},ruBlankMore());}
function ruDemo(){const a=ruProd(["Catering","Alimentos","Banquete","Por tiempos"]);Object.assign(a,{name:"Menú Oro",pax:"100",dishes:["Crema de elote","Mole poblano con pollo","Flan napolitano"],ins:["Platos","Cubiertos","Mantelería","Servilletas de tela"],crew:[{n:"Mesero",q:"7"},{n:"Cocinero",q:"2"},{n:"Capitán de meseros",q:"1"}],tw:["full","rent","labor"],labor:[{n:"Mesero",q:"7",p:"90",u:"Por hora",min:"5",xh:"110",xu:"por hora"},{n:"Cocinero",q:"2",p:"700",u:"Por turno (5 h)",min:"5",xh:"150",xu:"por hora"},{n:"Capitán de meseros",q:"1",p:"130",u:"Por hora",min:"5",xh:"160",xu:"por hora"}],ext:[{c:"Hora extra",p:"1500",u:"por hora"}],dlx:{dlOpen:-1,dl:[Object.assign(blankDl("Recolección en establecimiento"),{cobra:false,ph:"Lun a sáb de 9:00 a 18:00"}),Object.assign(blankDl("Envío a domicilio"),{cobra:true,u:"Por kilómetro",rate:"15",conds:[{c:"Distancia máxima",v:"30"}]})]},photos:[{url:samplePic("🍽️","#FFB3D9","#7B2FF7",1200,900),name:"menu-oro.jpg",issues:[],before:812000,after:214000}]});a.tar.full.p="650";a.tar.rent.p="480";a.id="pdemo1";
 const b=ruProd(["Catering","Bebidas","Barra","Sin alcohol"]);Object.assign(b,{pax:"100",ins:["Vasos","Hielo","Popotes"],crew:[{n:"Bartender",q:"2"}],tw:["full","labor"],labor:[{n:"Bartender",q:"2",p:"280",u:"Por hora",min:"5",xh:"320",xu:"por hora"}]});b.tar.full.p="95";b.id="pdemo2";
 const c=ruProd(["Catering","Postres y dulces","Mesa de dulces","Temática"]);Object.assign(c,{name:"Mesa de dulces temática",pax:"50",ins:["Charolas","Bases de pastel","Mantelería","Decoración de mesa"],crew:[],tw:["rent"],dlx:{dlOpen:-1,dl:[Object.assign(blankDl("Envío a domicilio"),{cobra:true,u:"Por kilómetro",rate:"12",conds:[{c:"Entrega gratuita desde",v:"5000"}]}),Object.assign(blankDl("Recolección en establecimiento"),{cobra:false,ph:"Lun a sáb de 9:00 a 18:00"})]},promo:{has:true,what:"10% de descuento entre semana",terms:"De lunes a jueves",until:"2026-12-15"},min:{has:true,qty:"30",unit:"personas"},photos:[{url:samplePic("🍭","#D6338A","#7B2CBF",1200,900),name:"mesa.jpg",issues:[],before:640000,after:198000}]});c.tar.rent.p="3500";c.tar.rent.u="Por evento";c.id="pdemo3";
 const P={id:"kdemo1",kind:"pkg",items:["pdemo1|full","pdemo2|full"],qty:{},name:"Paquete Boda Oro",dishes:[],ins:["Centros de mesa"],crew:[{n:"Mesero",q:"7"},{n:"Bartender",q:"2"}],pax:"100",tw:["full"],tar:ruBlankT("Por persona")};Object.assign(P,ruBlankMore());P.tar.full.p="720";
 a.emb=1;b.emb=2;c.emb=3;
 const st=[...a.labor,...b.labor].map(r=>ruNewStaff(r,"Catering"));
 const V={id:"kdemo2",kind:"pkg",items:["venue","pdemo3|rent","st-mesero"],qty:{"st-mesero":"4"},name:"Fiesta en la Terraza",dishes:[],ins:["Mantelería","Centros de mesa"],crew:[{n:"Mesero",q:"4"}],pax:"60",tw:["full"],tar:ruBlankT("Por persona")};Object.assign(V,ruBlankMore());V.tar.full.p="390";
 c.cov={same:false,zones:[{state:"Ciudad de México",all:true,munis:[]}]};
 return{prods:[a,b,c,...st],pkgs:[P,V],vin:{"pdemo1|full":{on:true,p:"590"},"pdemo1|rent":{on:true,p:""},"pdemo2|full":{on:true,p:""},"pdemo3|rent":{on:true,p:"3000"},"st-mesero":{on:true,p:""},"st-bartender":{on:false,p:""}}};}
function ruZInter(A,B){const out=[];if(A.some(z=>z.state==="__nac"))return B.map(z=>({...z,munis:[...z.munis]}));if(B.some(z=>z.state==="__nac"))return A.map(z=>({...z,munis:[...z.munis]}));
 A.forEach(z=>{const w=B.find(x=>x.state===z.state);if(!w||!z.state)return;if(z.all&&w.all)out.push({state:z.state,all:true,munis:[]});else{const m=z.all?w.munis:w.all?z.munis:z.munis.filter(x=>w.munis.includes(x));if(m.length)out.push({state:z.state,all:false,munis:[...m]});}});return out;}
function ruZones(p){if(!p.cov||p.cov.same){if(p.kind==="pkg"){const L=p.items.map(ruById).filter(x=>x&&x.kind!=="venue").map(ruZones);return L.length?L.reduce(ruZInter):S.svcZones;}return S.svcZones;}return p.cov.zones;}
const ruById=id=>{id=String(id||"").split("|")[0];return id==="venue"?ruVenueItem():(S.rprods||[]).find(x=>x.id===id);};
const ruRefW=r=>String(r).split("|")[1]||"";
/* v25 · el venue entra al combinador como una pieza más */
function ruVenueItem(){const v=S.venue;if(!S.types||!S.types.venue||!v)return null;return{id:"venue",kind:"venue",dims:["Venue","","",""],name:v.name||"Tu venue",crew:[],dishes:[],ins:[],tw:["venue"],pax:v.seated||"",cov:{same:true}};}
function ruVenueTot(pax){const v=S.venue,r=v&&v.rent,pr=+(r&&r.price)||0;if(!pr)return 0;pax=+pax||+v.seated||0;let t=r.per==="hora"?pr*(+v.hoursIncl||5):r.per==="persona"?pr*pax:pr;if(r.per!=="persona"&&+r.upTo>0&&pax>+r.upTo)t+=(pax-r.upTo)*(+r.perExtraGuest||0);return t;}
const ruFN={full:"🎉 Servicio completo",rent:"📦 Sin personal",labor:"🙋 Solo personal"};
function ruItemName(ref,P){const x=ruById(ref),w=ruRefW(ref),q=P&&P.qty&&P.qty[ref];if(!x)return"(ya no está disponible)";return(x.kind==="venue"?"🏡 ":"")+(x.kind==="staff"&&+q>1?q+" × ":"")+x.name+(w&&x.kind==="prod"?" · "+ruFN[w].slice(3).toLowerCase():"");}
/* precio en el venue: el proveedor lo pone aparte (no es descuento) */
const vnIn=ref=>{if(ruRefW(ref)==="labor")return null;const v=S.venue,e=v&&v.svcIn&&v.svcIn[ref];return e&&e.on!==false&&+e.p>0?e:null;};
function ruWithPrice(x,w,pr){const y=JSON.parse(JSON.stringify(x));if(w==="labor"||x.kind==="staff")y.labor.forEach(r=>{r.p=pr;});else y.tar[w].p=pr;return y;}
function ruItemTot(ref,P){const x=ruById(ref);if(!x)return 0;const pax=+P.pax||+x.pax||0,vin=P.items.includes("venue")&&vnIn(ref);
 if(x.kind==="venue")return ruVenueTot(pax);
 if(x.kind==="staff"){const y=vin?ruWithPrice(x,"labor",vin.p):x,r=y.labor[0];return(+r.p||0)*(r.u==="Por hora"?(+r.min||5):1)*(+(P.qty&&P.qty[ref])||1);}
 const w=ruRefW(ref)||x.tw[0];if(!w)return 0;const y=vin?ruWithPrice(x,w,vin.p):x,r=ruTotal(Object.assign({},y,{pax:w==="labor"?y.pax:pax||y.pax}),w);return r?r.tot:0;}
const ruCats=p=>p.kind==="pkg"?[...new Set(p.items.map(id=>(ruById(id)||{dims:["Catering"]}).dims[0]).filter(c=>c!=="Venue"))]:[p.dims[0]];
const ruFood=p=>p.kind==="pkg"?p.items.some(id=>(ruById(id)||{dims:[]}).dims[1]==="Alimentos"):p.dims[1]==="Alimentos";
function ruTotal(p,w){const pax=+p.pax||0;if(w==="labor"){const tot=ruLabTot(p);return tot?{tot,pp:pax?tot/pax:null}:null;}
 const t=p.tar[w],pr=+t.p||0;if(!pr)return null;const tot=t.u==="Por persona"?pr*pax:RU_FIXED.includes(t.u)?pr:w==="rent"?pr*pax:pr*(+t.q||1);return{tot,pp:pax?tot/pax:null};}
const ruTarOk=(p,w)=>w==="labor"?p.labor.length>0&&p.labor.every(r=>+r.p>0):+p.tar[w].p>0&&(w==="rent"||RU_FIXED.includes(p.tar[w].u)||+p.tar[w].q>0);
const ruSug=p=>p.items.reduce((a,ref)=>a+ruItemTot(ref,p),0);
const ruMoney=n=>{n=+n||0;return n>0&&n<100&&Math.round(n)!==n?"$"+n.toLocaleString("es-MX",{minimumFractionDigits:2,maximumFractionDigits:2}):money(Math.round(n));};
const ruLink=p=>`hayquevernos.com/${slug(S.biz.name)}#${p.kind==="pkg"?"paquete":"producto"}-${slug(p.name||"sin-nombre")}`;
function ruOk(p){if(!p.cov)p.cov={same:true,zones:[{state:"",all:false,munis:[]}]};if(p.kind==="staff")return(p.cov.same||zonesOk(p.cov.zones))&&+p.labor[0].p>0&&p.ext.every(e=>!filled(e.c)||+e.p>0)&&(p.min.has!==true||minOk(p.min))&&(p.promo.has!==true||promoOk(p.promo));return(p.cov.same||zonesOk(p.cov.zones))&&filled(p.name)&&+p.pax>0&&p.tw.length>0&&p.tw.every(w=>ruTarOk(p,w))&&(!p.tw.includes("rent")||(p.dlx.dl.length>0&&p.dlx.dl.every(dlOk)))&&p.ext.every(e=>!filled(e.c)||+e.p>0)&&(p.min.has!==true||minOk(p.min))&&(p.promo.has!==true||promoOk(p.promo));}
function ruMiss(p){const m=[];if(p.kind==="staff"){if(!(+p.labor[0].p>0))m.push("precio");if(p.cov&&!p.cov.same&&!zonesOk(p.cov.zones))m.push("zona");if(!p.ext.every(e=>!filled(e.c)||+e.p>0))m.push("precio de cada extra");if(p.min.has===true&&!minOk(p.min))m.push("mínimo de compra");if(p.promo.has===true&&!promoOk(p.promo))m.push("promoción");return m;}if(!filled(p.name))m.push("nombre");if(p.cov&&!p.cov.same&&!zonesOk(p.cov.zones))m.push("zona de este servicio");if(!p.tw.length)m.push("cómo lo cobras");else{if(p.tw.some(w=>w!=="labor"&&!(+p.tar[w].p>0)))m.push("precio");if(p.tw.includes("full")&&+p.tar.full.p>0&&!RU_FIXED.includes(p.tar.full.u)&&!(+p.tar.full.q>0))m.push("cuántas unidades incluye");if(p.tw.includes("labor")&&!(p.labor.length&&p.labor.every(r=>+r.p>0)))m.push("precio de cada perfil de tu personal");if(p.tw.includes("rent")&&!p.dlx.dl.length)m.push("cómo entregas sin personal");else if(p.tw.includes("rent")&&!p.dlx.dl.every(dlOk))m.push("entrega por completar");}if(!(+p.pax>0))m.push("para cuántas personas alcanza");
 if(!p.ext.every(e=>!filled(e.c)||+e.p>0))m.push("precio de cada extra");if(p.min.has===true&&!minOk(p.min))m.push("mínimo de compra");if(p.promo.has===true&&!promoOk(p.promo))m.push("promoción");return m;}
/* ---------- ruleta ---------- */
function ruMachineHtml(){return`<section class="ru-m" aria-label="Arma tu servicio">
 <div class="ru-mh"><img class="ru-masc" id="ruMasc" alt=""><div class="ru-mt"><b id="ruTit">Arma tu servicio</b><span>Desliza cada rodillo. Lo que queda en la línea verde es tu selección.</span></div></div>
 <div class="ru-reels" id="ruReels">${RU_LAB.map((l,i)=>`<div class="ru-row"><div class="ru-lab">${i+1} · ${l}<span id="ruCnt${i}"></span></div><div class="ru-wrap"><button class="ru-ar l" type="button" data-i="${i}" data-d="-1" aria-label="Anterior">‹</button><div class="ru-reel" id="ruReel${i}" tabindex="0" role="listbox" aria-label="${l}"></div><button class="ru-ar r" type="button" data-i="${i}" data-d="1" aria-label="Siguiente">›</button></div></div>`).join("")}</div>
 <div class="ru-combo"><span class="ru-unit" id="ruUnit"></span><div id="ruOtro" hidden><input id="ruOtroIn" type="text" placeholder="Escribe cuál es (ej. barra de mezcal)" aria-label="Escribe cuál es"></div>
 <button class="btn cta ru-save" id="ruSave" type="button">Guardar esta combinación ✓</button></div></section>`;}
const ruReel=i=>$("ruReel"+i);
function ruFill(i){const el=ruReel(i);if(!el)return;const L=ruOpts(i,S.rsel);el.innerHTML=L.map(v=>`<button type="button" class="ru-it" role="option" data-v="${esc(v)}">${i===0&&RU.emo[v]?`<span class="e">${RU.emo[v]}</span>`:""}${esc(v)}</button>`).join("");$("ruCnt"+i).textContent=L.length+" opciones";}
const ruIdx=(i,v)=>[...ruReel(i).children].findIndex(b=>b.dataset.v===v);
const RU_RM=matchMedia("(prefers-reduced-motion: reduce)").matches;
function ruCenter(i,ix,smooth){const el=ruReel(i),b=el&&el.children[ix];if(!b)return;el.scrollTo({left:b.offsetLeft+b.offsetWidth/2-el.clientWidth/2,behavior:smooth&&!RU_RM?"smooth":"auto"});}
function ruNear(i){const el=ruReel(i);if(!el)return null;const c=el.scrollLeft+el.clientWidth/2;let best=null,bd=1e9;for(const b of el.children){const d=Math.abs(b.offsetLeft+b.offsetWidth/2-c);if(d<bd){bd=d;best=b;}}return best;}
function ruPaint(i){const el=ruReel(i);if(!el)return;const c=el.scrollLeft+el.clientWidth/2,w=el.clientWidth/2||1,nb=ruNear(i);for(const b of el.children){const d=Math.min(1,Math.abs(b.offsetLeft+b.offsetWidth/2-c)/w);b.style.setProperty("--d",d.toFixed(3));b.classList.toggle("on",b===nb);b.setAttribute("aria-selected",b===nb);}}
function ruRebuild(i,target,spin){if(i>3||!ruReel(i))return;const L=ruOpts(i,S.rsel);S.rsel[i]=target&&L.includes(target)?target:L[0];ruFill(i);const ix=ruIdx(i,S.rsel[i]);RU_BUSY[i]=ix;
 if(spin&&!RU_RM){ruReel(i).scrollLeft=ruReel(i).scrollWidth;ruPaint(i);requestAnimationFrame(()=>ruCenter(i,ix,true));}else{ruCenter(i,ix,false);ruPaint(i);RU_BUSY[i]=null;}
 setTimeout(()=>{if(RU_BUSY[i]===ix&&ruReel(i)){RU_BUSY[i]=null;ruCenter(i,ix,false);ruPaint(i);}},900);}
function ruCascade(from,targets){for(let j=from;j<4;j++){const t=targets?targets[j]:null;setTimeout(()=>{ruRebuild(j,t,true);if(j===3)setTimeout(ruUpdate,80);},(j-from)*(RU_RM?0:170));}if(from>3)ruUpdate();}
function ruSettle(i){if(RU_DRAG&&RU_DRAG.i===i)return;const b=ruNear(i);if(!b)return;const ix=[...ruReel(i).children].indexOf(b);
 if(RU_BUSY[i]!==null){if(RU_BUSY[i]!==ix)return;RU_BUSY[i]=null;}const v=b.dataset.v;if(v!==S.rsel[i]){S.rsel[i]=v;ruCascade(i+1);}else ruUpdate();}
function ruStep(i,d){if(!ruReel(i))return;const b=ruNear(i),ix=[...ruReel(i).children].indexOf(b)+d;if(ix>=0&&ix<ruReel(i).children.length)ruCenter(i,ix,true);}
function ruUpdate(){if(!$("ruUnit"))return;const [u,o]=RU_U[S.rsel.join("|")]||["Por evento",""];
 $("ruUnit").innerHTML=`💲 Se suele cobrar <b>${esc(u.toLowerCase())}</b>${o?` · también ${esc(o.toLowerCase())}`:""}`;$("ruOtro").hidden=S.rsel[3]!=="Otro";$("ruTit").textContent="Arma tu servicio · "+(RU.emo[S.rsel[0]]?RU.emo[S.rsel[0]]+" ":"")+S.rsel[0];
 const m=ruMasc(S.rsel),im=$("ruMasc");if(m!==RU_LASTM||!im.src){RU_LASTM=m;im.src=`img/${m}.webp`;im.classList.remove("pop");void im.offsetWidth;im.classList.add("pop");}
 const R=$("ruReels");R.classList.remove("aligned");void R.offsetWidth;R.classList.add("aligned");}
function ruSetPath(p){S.rsel[0]=p[0];ruRebuild(0,p[0],true);ruCascade(1,p);}
function ruBindMachine(){for(let i=0;i<4;i++){const el=ruReel(i);let t;ruFill(i);
 el.addEventListener("scroll",()=>{ruPaint(i);clearTimeout(t);t=setTimeout(()=>ruSettle(i),120);},{passive:true});
 el.addEventListener("keydown",e=>{if(e.key==="ArrowRight"||e.key==="ArrowLeft"){e.preventDefault();ruStep(i,e.key==="ArrowRight"?1:-1);}});
 el.addEventListener("click",e=>{const b=e.target.closest(".ru-it");if(!b||RU_MOVED)return;ruCenter(i,[...el.children].indexOf(b),true);});
 el.addEventListener("pointerdown",e=>{if(e.pointerType!=="mouse")return;RU_DRAG={i,x:e.clientX,s:el.scrollLeft};RU_MOVED=false;});}
 document.querySelectorAll(".ru-ar").forEach(a=>a.onclick=()=>ruStep(+a.dataset.i,+a.dataset.d));
 requestAnimationFrame(()=>{for(let i=0;i<4;i++){ruCenter(i,Math.max(0,ruIdx(i,S.rsel[i])),false);ruPaint(i);}RU_LASTM="";ruUpdate();});
 $("ruSave").onclick=()=>{const o=$("ruOtroIn");if(S.rsel[3]==="Otro"&&!o.value.trim()){o.focus();o.placeholder="Escribe cuál es para guardarlo";return;}
  RU_EDIT=ruProd([...S.rsel],o.value.trim());o.value="";ruConfetti(70);hqvTrack("ruleta_combinacion",{dims:S.rsel.join(" › ")});ruDrawIdent(true);};}
addEventListener("pointermove",e=>{if(!RU_DRAG)return;const el=ruReel(RU_DRAG.i);if(!el){RU_DRAG=null;return;}const dx=e.clientX-RU_DRAG.x;if(Math.abs(dx)>4){RU_MOVED=true;el.classList.add("drag");}if(RU_MOVED)el.scrollLeft=RU_DRAG.s-dx;});
addEventListener("pointerup",()=>{if(!RU_DRAG)return;const i=RU_DRAG.i,el=ruReel(i);RU_DRAG=null;if(!el)return;el.classList.remove("drag");if(RU_MOVED){const b=ruNear(i);ruCenter(i,[...el.children].indexOf(b),true);setTimeout(()=>{RU_MOVED=false;},50);}});
addEventListener("resize",()=>{if(!ruReel(0))return;for(let i=0;i<4;i++){ruCenter(i,Math.max(0,ruIdx(i,S.rsel[i])),false);ruPaint(i);}});
/* buscador que alinea los rodillos */
const RU_IDX=RU.rows.map(r=>({r,h:nrm(r.slice(0,4).join(" "))}));
function ruBindSearch(){const q=$("ruQ"),qr=$("ruQr");let res=[];if(!q)return;
 q.oninput=()=>{const v=nrm(q.value).trim();if(v.length<2){qr.hidden=true;return;}const toks=v.split(/\s+/),seen=new Set();res=[];
  for(const x of RU_IDX){if(!toks.every(t=>x.h.includes(t)))continue;res.push([(nrm(x.r[2]).startsWith(toks[0])?0:nrm(x.r[1]).startsWith(toks[0])?1:2)+(x.r[3]==="Otro"?3:0),x.r]);}
  res=res.sort((a,b)=>a[0]-b[0]).map(x=>x[1]).filter(r=>{const k=r.slice(0,4).join("|");if(seen.has(k))return false;seen.add(k);return true;}).slice(0,8);
  qr.innerHTML=res.map((r,ix)=>`<button type="button" data-ix="${ix}" class="${ix?"":"on"}"><b>${esc(r[2])} · ${esc(r[3])}</b><small>${esc(r[0])} › ${esc(r[1])}</small></button>`).join("")||`<span class="hint" style="padding:10px">No lo encontramos. Mueve los rodillos y usa «Otro».</span>`;
  qr.hidden=false;qr.querySelectorAll("button").forEach(b=>b.onclick=()=>pick(+b.dataset.ix));};
 const pick=ix=>{const r=res[ix];if(!r)return;qr.hidden=true;q.value="";q.blur();ruSetPath(r.slice(0,4));hqvTrack("ruleta_buscador",{q:r.slice(0,4).join(" › ")});const m=document.querySelector(".ru-m");m&&m.scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"center"});};
 q.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();pick(0);}if(e.key==="Escape")qr.hidden=true;};
 document.addEventListener("click",e=>{if(!e.target.closest(".ru-search")&&qr)qr.hidden=true;});}
/* ---------- etiquetas predictivas ---------- */
function ruTags(id,L,ph){return`<div class="ru-tags" data-t="${id}">${L.map((t,ix)=>`<span class="ru-tag">${esc(t)}<button type="button" data-x="${ix}" aria-label="Quitar ${esc(t)}">✕</button></span>`).join("")}<input type="text" autocomplete="off" placeholder="${esc(ph)}" aria-label="${esc(ph)}"><div class="ru-sg" hidden></div></div>`;}
function ruBindTags(root,id,L,src,onAdd,redraw){const w=root.querySelector(`.ru-tags[data-t="${id}"]`);if(!w)return;const inp=w.querySelector("input"),sg=w.querySelector(".ru-sg");let res=[],on=0;
 const add=v=>{v=(v||"").trim().replace(/,$/,"");if(!v)return;if(onAdd)onAdd(v);else{if(L.some(x=>nrm(x)===nrm(v)))return;L.push(v);}redraw(id);};
 w.querySelectorAll("[data-x]").forEach(b=>b.onclick=()=>{L.splice(+b.dataset.x,1);redraw(id);});
 const show=()=>{const v=nrm(inp.value).trim();if(!v){sg.hidden=true;return;}res=src().filter(x=>nrm(x).includes(v)&&!L.includes(x)).sort((a,b)=>(nrm(a).startsWith(v)?0:1)-(nrm(b).startsWith(v)?0:1)).slice(0,6);on=0;
  sg.innerHTML=res.map((x,ix)=>`<button type="button" class="${ix?"":"on"}">${esc(x)}</button>`).join("");sg.hidden=!res.length;sg.querySelectorAll("button").forEach((b,ix)=>b.onmousedown=e=>{e.preventDefault();add(res[ix]);});};
 inp.oninput=show;inp.onblur=()=>setTimeout(()=>{sg.hidden=true;},120);
 inp.onkeydown=e=>{if((e.key==="ArrowDown"||e.key==="ArrowUp")&&res.length){e.preventDefault();on=(on+(e.key==="ArrowDown"?1:-1)+res.length)%res.length;sg.querySelectorAll("button").forEach((b,ix)=>b.classList.toggle("on",ix===on));}
  if(e.key==="Enter"||e.key===","){e.preventDefault();add(!sg.hidden&&res[on]?res[on]:inp.value);}if(e.key==="Backspace"&&!inp.value&&L.length&&!onAdd){L.pop();redraw(id);}};}
/* ---------- ficha de identidad ---------- */
function ruHost(p){if(p.kind==="staff"){const r=p.labor[0];if(!(+r.p>0))return"";const ev=(+r.p)*(r.u==="Por hora"?(+r.min||5):1);return`<div class="ru-host ru-hosts"><b>👀 Así lo verá el anfitrión</b><span>${esc(p.name)}: <b>${money(r.p)}</b> ${esc(ruXU(r.u))}${r.u==="Por hora"?` · mínimo ${esc(r.min||5)} h`:""} → <b>${money(ev)}</b> por persona del equipo${+r.xh>0?` · extra ${money(r.xh)} ${esc(r.xu||ruXU(r.u))}`:""}</span></div>`;}const pax=+p.pax;if(!pax||!p.tw.length)return"";const L=p.tw.map(w=>{const r=ruTotal(p,w);return r?`<span>${RU_TL[w][0]}: <b>${ruMoney(r.pp)}</b> por persona · <b>${ruMoney(r.tot)}</b> en total</span>`:"";}).filter(Boolean);
 return L.length?`<div class="ru-host"><b>👀 Así lo verá el anfitrión</b><span class="hint">En una fiesta de ${pax} personas:</span>${L.join("")}</div>`:"";}
function ruTarHtml(p,w,k){const t=p.tar[w],cnt=w==="full"&&!RU_FIXED.includes(t.u);
 return`<div class="ru-tg" data-w="${w}"><b>${RU_TL[w][0]}</b><div class="row"><label class="ru-money">$<input type="number" min="0" inputmode="decimal" data-tp="${w}" class="${MISS(+t.p>0)}" value="${esc(t.p)}" placeholder="precio" aria-label="Precio ${RU_TL[w][0]}"></label>
  <select data-tu="${w}" aria-label="Unidad">${RU_UNITS.map(u=>`<option ${t.u===u?"selected":""}>${u}</option>`).join("")}</select>
  ${cnt?`<label class="ru-q">¿Cuántas ${esc(ruNoun(t.u))}? <input type="number" min="1" data-tq="${w}" class="${MISS(+t.q>0)}" value="${esc(t.q)}" placeholder="#"></label>`:""}</div>
  ${w==="full"?`<span class="ru-note">🚚 La entrega, el montaje y tu personal van incluidos en este precio.</span>`:`${!RU_FIXED.includes(t.u)?`<span class="hint">Para el cotizador calculamos 1 ${esc(ruNoun(t.u).replace(/s$/,""))} por persona.</span>`:""}
   ${dlSecHtml(p.dlx,k+"dlx","rt","¿Cómo lo entregas?")}`}</div>`;}
function ruLaborHtml(p,staff){const sk=p.kind==="staff",rest=sk?[]:[...new Set(staff)].filter(n=>!p.labor.some(r=>r.n===n)),L=p.lpol;
 const pill=(k,on,txt,extra)=>`<span class="ru-pill" aria-pressed="${on}"><button type="button" class="ru-pt" data-k="${k}" aria-pressed="${on}">${on?"✓ ":""}${txt}</button>${on&&extra?extra:""}</span>`;
 const F=(lb,inner,c)=>`<label class="ru-f${c?" "+c:""}"><small>${lb}</small><span class="ru-fi">${inner}</span></label>`;
 return`<div class="ru-tg ru-labr" data-w="labor"><b>${sk?"🙋 Precio de este perfil":RU_TL.labor[0]}</b><span class="hint">${sk?"Lo que cobra una persona. Si lo cambias, se actualiza en todos tus productos.":"Precio de cada perfil que mandas. Si ya lo usaste antes, lo llenamos por ti."}</span>
  <div class="ru-lt">${p.labor.map((r,ix)=>{const hr=r.u==="Por hora",known=!sk&&ruStaffBy(r.n)&&filled(ruStaffBy(r.n).labor[0].p);return`<div class="ru-lr${sk?" one":""}" data-ix="${ix}"><div class="ru-lnr"><b class="ru-ln">${esc(r.n)}</b>${known?`<span class="ru-known" title="Precio guardado en Tu personal">🔁<span> guardado</span></span>`:""}${sk?"":`<button type="button" class="link bad ru-lrm" aria-label="Quitar ${esc(r.n)}">✕</button>`}</div>
   ${sk?"":`<span class="ru-f ru-fq"><small>cant.</small><span class="ru-fi ru-stp"><button type="button" class="ru-sm" aria-label="Uno menos">−</button><input type="number" min="1" inputmode="numeric" class="ru-lq" value="${esc(r.q)}" aria-label="¿Cuántos ${esc(r.n)}?"><button type="button" class="ru-sp" aria-label="Uno más">+</button></span></span>`}
   ${F("precio",`<i>$</i><input type="number" min="0" inputmode="decimal" class="ru-lp${MISS(+r.p>0)}" value="${esc(r.p)}" placeholder="0" aria-label="Precio de ${esc(r.n)}">`,"ru-fp")}
   ${F("cobro",`<select class="ru-lu" aria-label="Cómo cobras ${esc(r.n)}">${RU_LU.map(([u,t])=>`<option value="${u}" ${r.u===u?"selected":""}>${ruShortU(t)}</option>`).join("")}</select>`,"ru-fu")}
   ${hr?F("mínimo",`<input type="number" min="1" inputmode="numeric" class="ru-lm" value="${esc(r.min)}" aria-label="Horas mínimas de ${esc(r.n)}"><i>h</i>`,"ru-fm"):`<span class="ru-f ru-fm ru-na"><small>mínimo</small><span class="ru-fi">—</span></span>`}
   ${F("extra",`<i>$</i><input type="number" min="0" inputmode="decimal" class="ru-lx" value="${esc(r.xh)}" placeholder="0" aria-label="Precio extra de ${esc(r.n)}">`,"ru-fx")}
   ${F("cobro",`<select class="ru-lxu" aria-label="Cómo cobras el extra de ${esc(r.n)}">${RU_XU.map(t=>`<option value="${t}" ${(r.xu||ruXU(r.u))===t?"selected":""}>${ruShortU(t)}</option>`).join("")}</select>`,"ru-fxu")}</div>`;}).join("")||`<span class="hint">Agrega al menos un perfil.</span>`}</div>
  ${sk?"":`<div class="ru-add"><span class="ru-sl">＋ Sumar perfil</span><div class="ru-addc">${rest.map(n=>`<button type="button" class="chip ru-lab-c" data-n="${esc(n)}">＋ ${esc(n)}${ruStaffBy(n)&&+ruStaffBy(n).labor[0].p>0?` <small>${money(ruStaffBy(n).labor[0].p)}</small>`:""}</button>`).join("")}<button type="button" class="chip new ru-lab-o">✏️ Otro</button></div><div class="ru-labnew" hidden>${ruTags("labNew",[],"Otro perfil: escribe y Enter")}</div></div>`}
  <div class="ru-pols"><span class="ru-sl">📋 Tus políticas</span><div class="ru-pils">
   ${pill("night",L.night,"🌙 Recargo después de 12 a.m.",`<label class="ru-pin">+<input type="number" min="0" class="ru-p-pct" value="${esc(L.nightPct)}" aria-label="Recargo nocturno">%</label>`)}
   ${pill("ride",L.ride,"🚕 Transporte de regreso lo cubre el anfitrión",`<label class="ru-pin">$<input type="number" min="0" class="ru-p-fee" value="${esc(L.rideFee)}" placeholder="0" aria-label="Transporte por persona">c/u</label>`)}
   ${pill("meal",L.meal,"🍽️ Alimentos al personal (+5 h)")}
   ${pill("uniform",L.uniform,"👔 Uniforme incluido")}</div>
   <span class="hint">El tiempo cuenta desde que tu personal llega. Viáticos fuera de zona se acuerdan.</span></div></div>`;}
function ruIdentHtml(p){const sk=p.kind==="staff",pk=p.kind==="pkg",staff=[...new Set(ruCats(p).flatMap(c=>RU.staff[c]||[]))],names=[...new Set([...staff,...p.crew.map(r=>r.n)])],k="ru"+(pk?"k":"p"),sug=pk?ruSug(p):0;
 if(pk&&!p.qty)p.qty={};const head=pk?`<span class="ru-pkb">🎁 Paquete</span><h3>Dale identidad a tu paquete</h3><div class="ru-crumbs ru-kits">${p.items.map(ref=>{const x=ruById(ref);return x&&x.kind==="staff"?`<label class="ru-kq"><input type="number" min="1" inputmode="numeric" data-kq="${esc(ref)}" value="${esc(p.qty[ref]||"1")}" aria-label="¿Cuántos ${esc(x.name)}?"> × ${esc(x.name)}</label>`:`<span>${esc(ruItemName(ref,p))}</span>`;}).join("")}</div><span class="hint">Empieza en blanco: el paquete lleva su propio nombre, detalles y precio. Guardamos de qué productos sale.</span>`
  :sk?`<span class="ru-stb">🙋 Tu personal</span><h3>${esc(p.name)}</h3><span class="hint">Es un producto independiente: el anfitrión lo puede contratar solo y tú lo sumas a tus paquetes las veces que quieras.</span>`
  :`<h3>Dale identidad</h3><div class="ru-crumbs">${p.dims.map(d=>`<span>${esc(d)}</span>`).join("")}${p.otro?`<span>${esc(p.otro)}</span>`:""}</div>`;
 return`${head}
 ${sk?"":`<div class="field"><label class="lbl" for="ruName">Nombre</label><input id="ruName" class="${MISS(filled(p.name))}" value="${esc(p.name)}" placeholder="${pk?"Nombre del paquete":"Nombre de tu producto"}"></div>`}
 ${sk?ruLaborHtml(p,staff):`<div class="field ru-inc"><span class="lbl">¿Qué incluye?</span>
  ${ruFood(p)?`<span class="ru-sl">🍴 Platillos <span class="opt">escribe y te sugerimos</span></span>${ruTags("dishes",p.dishes,"Ej. crema de elote")}`:""}
  <span class="ru-sl">🧺 Insumos <span class="opt">solo el nombre; alcanzan para tus personas</span></span>${ruTags("ins",p.ins,"Ej. platos, hielo, mantelería")}
  <span class="ru-sl">🙋 Staff <span class="opt">ya marcamos lo más común</span></span>
  <div class="chips cmini">${names.map(n=>`<button type="button" class="chip ru-crew" data-n="${esc(n)}" aria-pressed="${p.crew.some(r=>r.n===n)}">${TICK}${esc(n)}</button>`).join("")}</div>
  ${ruTags("crewNew",[],"Otro perfil: escribe y Enter")}
  ${p.crew.length?`<div class="ru-crewq">${p.crew.map((r,ix)=>`<label>${esc(r.n)}<input type="number" min="0" inputmode="numeric" data-cq="${ix}" value="${esc(r.q)}" aria-label="¿Cuántos ${esc(r.n)}?"></label>`).join("")}</div>`:""}</div>
 <div class="field"><span class="lbl">💲 ¿Cómo lo cobras? <span class="opt">elige una o varias</span></span>
  <div class="ru-tsel${MISS(p.tw.length>0)}">${["full","rent","labor"].map(w=>`<button type="button" class="ru-tsb" data-w="${w}" aria-pressed="${p.tw.includes(w)}"><b>${RU_TL[w][0]}</b><small>${RU_TL[w][1]}</small></button>`).join("")}</div>
  ${pk&&sug?`<div class="ru-sug">💡 Tus productos suman <b>${ruMoney(sug)}</b>${+p.pax?` · ${ruMoney(sug/ +p.pax)} por persona`:""}<button type="button" class="link" id="ruUseSug">Usar como precio</button></div>`:""}
  ${p.tw.map(w=>w==="labor"?ruLaborHtml(p,staff):ruTarHtml(p,w,k)).join("")}</div>`}
 ${sk?`<div id="ruHost">${ruHost(p)}</div>`:`<div class="ru-paxc"><img src="img/c_07.webp" alt="" class="ru-paxm"><div class="ru-paxq"><label class="ru-paxl" for="ruPax">¿Para cuántas personas alcanza todo esto?</label><span class="ru-paxh">Es el dato más importante: con él te mostramos en el cotizador del anfitrión.</span>
  <div class="ru-paxi"><input id="ruPax" class="${MISS(+p.pax>0)}" type="number" min="1" inputmode="numeric" value="${esc(p.pax)}" placeholder="#" aria-label="Personas"><b>personas</b></div></div>
  <div id="ruHost">${ruHost(p)}</div></div>`}
 <div class="field ru-cov"><span class="lbl">📍 ¿Hasta dónde llevas ${pk?"este paquete":"este servicio"}?</span>
  <div class="chips"><button type="button" class="chip ru-covb" data-v="1" aria-pressed="${p.cov.same}">${TICK}${pk?"Donde llegan todos sus productos":"Igual que mi zona general"}</button><button type="button" class="chip ru-covb" data-v="0" aria-pressed="${!p.cov.same}">${TICK}Otra zona</button></div>
  ${p.cov.same?`<span class="hint">📍 ${esc(zonesText(ruZones(p))||"Aún no defines tu zona general (abajo, en este mismo paso).")}</span>`:zonesHtml(p.cov.zones,k+"cv","Zona de "+(pk?"este paquete":"este servicio"))}</div>
 <details class="more ru-more"${p._moreOpen?" open":""}><summary>⚙️ Más opciones <span class="opt">fotos, extras, mínimo y promoción</span></summary>
  <div class="ru-mo">
  <div class="field"><span class="ru-sl">📷 Fotos</span>${uploaderHtml(k+"ph","photo",p.photos,true)}</div>
  <div class="field"><span class="ru-sl">➕ Extras con costo <span class="opt">escribe el extra y su precio</span></span>
   ${p.ext.length?`<div class="ru-exl">${p.ext.map((e,ix)=>`<div class="ru-ex" data-ix="${ix}"><input type="text" class="ru-exc" value="${esc(e.c)}" aria-label="Extra"><label class="ru-money">$<input type="number" min="0" class="ru-exp${MISS(+e.p>0)}" value="${esc(e.p)}" placeholder="precio" aria-label="Precio de ${esc(e.c)}"></label><input type="text" class="ru-exu" value="${esc(e.u)}" placeholder="por hora" aria-label="Unidad"><button type="button" class="link bad ru-exx" aria-label="Quitar ${esc(e.c)}">✕</button></div>`).join("")}</div>`:""}
   ${ruTags("ext",[],"Ej. hora extra, kilo extra…")}</div>
  ${minHtml(p.min,k+"mn")}
  ${promoHtml(p.promo,k+"pr",(pk?"paquete-":"producto-")+slug(p.name||"x"))}
  </div></details>
 <div class="ru-share"><span>🔗 Comparte ${pk?"este paquete":"este producto"} por WhatsApp o redes</span><code id="ruLk">${esc(ruLink(p))}</code><span class="row"><button type="button" class="btn sm" id="ruCopy">Copiar link</button><button type="button" class="btn sm ghost" id="ruImg">⬇️ Imagen para redes</button></span><span class="hint" id="ruLkMsg" aria-live="polite">Lleva directo a ${pk?"este paquete":"este producto"} en tu sitio.</span></div>
 <span class="err ru-err" id="ruErr" hidden></span>
 <div class="row"><button class="btn cta" type="button" id="ruOk">${pk?"Guardar paquete ✓":"Guardar producto ✓"}</button><button class="btn ghost" type="button" id="ruCancel">Cancelar</button></div>`;}
function ruDrawIdent(scroll,focusTag){const box=$("ruIdent");if(!box)return;const p=RU_EDIT;if(!p){box.hidden=true;box.innerHTML="";return;}
 const mo=box.querySelector("details.ru-more");if(mo)p._moreOpen=mo.open;const y0=scrollY;box.hidden=false;box.innerHTML=ruIdentHtml(p);if(!scroll)scrollTo({top:y0,behavior:"instant"});
 const rd=id=>ruDrawIdent(false,id),k="ru"+(p.kind==="pkg"?"k":"p");
 box.querySelector("details.ru-more").ontoggle=e=>{p._moreOpen=e.target.open;};
 const rn=$("ruName");if(rn)rn.oninput=e=>{p.name=e.target.value;$("ruLk").textContent=ruLink(p);};
 const rx=$("ruPax");if(rx)rx.oninput=e=>{p.pax=e.target.value;$("ruHost").innerHTML=ruHost(p);};
 box.querySelectorAll("[data-kq]").forEach(x=>x.oninput=e=>{p.qty[x.dataset.kq]=e.target.value;});
 ruBindTags(box,"dishes",p.dishes,()=>RU_DISHES,null,rd);ruBindTags(box,"ins",p.ins,()=>ruIns(ruCats(p)[0]),null,rd);
 ruBindTags(box,"crewNew",[],()=>[...new Set(Object.values(RU.staff).flat())],v=>{if(!p.crew.some(r=>nrm(r.n)===nrm(v)))p.crew.push({n:v,q:"1"});},rd);
 ruBindTags(box,"ext",[],()=>RU_EXTRAS.filter(x=>!p.ext.some(e=>e.c===x)),v=>{if(!p.ext.some(e=>nrm(e.c)===nrm(v)))p.ext.push({c:v,p:"",u:ruExU(v)});setTimeout(()=>{const l=[...box.querySelectorAll(".ru-exp")].pop();l&&l.focus({preventScroll:true});},0);},rd);
 box.querySelectorAll(".ru-crew").forEach(b=>b.onclick=()=>{const n=b.dataset.n,ix=p.crew.findIndex(r=>r.n===n);if(ix>=0)p.crew.splice(ix,1);else p.crew.push({n,q:"1"});ruDrawIdent();});
 box.querySelectorAll("[data-cq]").forEach(x=>x.oninput=e=>{p.crew[+x.dataset.cq].q=e.target.value;});
 box.querySelectorAll(".ru-tsb").forEach(b=>b.onclick=()=>{const w=b.dataset.w;p.tw=p.tw.includes(w)?p.tw.filter(x=>x!==w):["full","rent","labor"].filter(x=>x===w||p.tw.includes(x));
  if(w==="labor"&&p.tw.includes("labor")&&!p.labor.length)p.labor=p.crew.map(r=>ruLabRow(r.n,r.q));ruDrawIdent();});
 const live=()=>{$("ruHost").innerHTML=ruHost(p);};
 box.querySelectorAll("[data-tp]").forEach(x=>x.oninput=e=>{p.tar[x.dataset.tp].p=e.target.value;live();});
 box.querySelectorAll("[data-tq]").forEach(x=>x.oninput=e=>{p.tar[x.dataset.tq].q=e.target.value;live();});
 box.querySelectorAll("[data-tu]").forEach(x=>x.onchange=e=>{p.tar[x.dataset.tu].u=e.target.value;ruDrawIdent();});
 const us=$("ruUseSug");if(us)us.onclick=()=>{const s=ruSug(p);if(!p.tw.includes("full"))p.tw.unshift("full");if(+p.pax){p.tar.full.u="Por persona";p.tar.full.p=String(Math.round(s/ +p.pax));}else{p.tar.full.u="Por evento";p.tar.full.p=String(Math.round(s));}ruDrawIdent();};
 box.querySelectorAll(".ru-ex").forEach(R=>{const e=p.ext[+R.dataset.ix];R.querySelector(".ru-exc").oninput=x=>{e.c=x.target.value;};R.querySelector(".ru-exp").oninput=x=>{e.p=x.target.value;};R.querySelector(".ru-exu").oninput=x=>{e.u=x.target.value;};R.querySelector(".ru-exx").onclick=()=>{p.ext.splice(+R.dataset.ix,1);ruDrawIdent();};});
 const red=()=>ruDrawIdent();
 bindUploader(k+"ph","photo",p.photos,red);bindMin(p.min,k+"mn",red);bindPromo(p.promo,k+"pr",red);
 box.querySelectorAll(".ru-covb").forEach(b=>b.onclick=()=>{p.cov.same=b.dataset.v==="1";if(!p.cov.same&&!zonesOk(p.cov.zones))p.cov.zones=JSON.parse(JSON.stringify(ruZones(Object.assign({},p,{cov:{same:true}}))||[{state:"",all:false,munis:[]}]));if(!p.cov.zones.length)p.cov.zones=[{state:"",all:false,munis:[]}];ruDrawIdent();});
 if(!p.cov.same)bindZones(p.cov.zones,k+"cv",red);bindDlSec(box,"rt",p.dlx,k+"dlx",red);
 box.querySelectorAll(".ru-lab-c").forEach(b=>b.onclick=()=>{const n=b.dataset.n;if(!p.labor.some(r=>r.n===n)){const c=p.crew.find(r=>r.n===n);p.labor.push(ruLabRow(n,c?c.q:"1"));}ruDrawIdent();});
 const lo=box.querySelector(".ru-lab-o");if(lo)lo.onclick=()=>{const w=box.querySelector(".ru-labnew");w.hidden=false;w.querySelector("input").focus({preventScroll:true});};
 ruBindTags(box,"labNew",[],()=>[...new Set(Object.values(RU.staff).flat())],v=>{if(!p.labor.some(r=>nrm(r.n)===nrm(v)))p.labor.push(ruLabRow(v,"1"));},()=>ruDrawIdent());
 box.querySelectorAll(".ru-lr").forEach(R=>{const r=p.labor[+R.dataset.ix];[["ru-lq","q"],["ru-lp","p"],["ru-lm","min"],["ru-lx","xh"]].forEach(([c,f])=>{const x=R.querySelector("."+c);if(x)x.oninput=e=>{r[f]=e.target.value;live();};});
  const q=R.querySelector(".ru-lq");if(q){R.querySelector(".ru-sm").onclick=()=>{r.q=String(Math.max(1,(+r.q||1)-1));q.value=r.q;live();};R.querySelector(".ru-sp").onclick=()=>{r.q=String((+r.q||0)+1);q.value=r.q;live();};}
  R.querySelector(".ru-lu").onchange=e=>{const was=ruXU(r.u);r.u=e.target.value;if(!r.xu||r.xu===was)r.xu=ruXU(r.u);ruDrawIdent();};R.querySelector(".ru-lxu").onchange=e=>{r.xu=e.target.value;};const rm=R.querySelector(".ru-lrm");if(rm)rm.onclick=()=>{p.labor.splice(+R.dataset.ix,1);ruDrawIdent();};});
 box.querySelectorAll(".ru-pt").forEach(b=>b.onclick=()=>{const k=b.dataset.k,m={night:"night",ride:"ride",meal:"meal",uniform:"uniform"}[k];p.lpol[m]=!p.lpol[m];ruDrawIdent();});
 const pq=(c,f)=>{const x=box.querySelector(c);if(x)f(x);};pq(".ru-p-pct",x=>x.oninput=e=>{p.lpol.nightPct=e.target.value;});pq(".ru-p-fee",x=>x.oninput=e=>{p.lpol.rideFee=e.target.value;});
 $("ruCopy").onclick=()=>copyText("https://"+$("ruLk").textContent,$("ruLkMsg"));
 $("ruImg").onclick=async()=>{const w=p.tw[0],r=w&&ruTotal(p,w);const url=await hqvShareImage({logo:"img/logo.webp",kicker:S.biz.name||"Mi negocio",title:p.name||"Mi producto",sub:[r&&+p.pax?`${ruMoney(r.pp)} por persona · para ${p.pax} personas`:"",[...p.dishes,...p.ins].slice(0,4).join(", ")].filter(Boolean).join(" · "),url:ruLink(p),foot:"Escanea y cotiza por WhatsApp"});hqvDownload(url,(p.kind==="pkg"?"paquete-":"producto-")+slug(p.name)+".png");hqvTrack("imagen_producto_descargada");};
 $("ruCancel").onclick=()=>{RU_EDIT=null;ruDrawIdent();};
 $("ruOk").onclick=()=>{const m=ruMiss(p),er=$("ruErr");if(m.length){er.hidden=false;er.textContent="Falta: "+m.join(", ")+".";if(m.some(x=>/extra|entrega|mínimo|promoción/.test(x))){p._moreOpen=true;box.querySelector("details.ru-more").open=true;}return;}
  const L=p.kind==="pkg"?S.rpkgs:S.rprods,ix=L.findIndex(x=>x.id===p.id);delete p._moreOpen;const isNew=ix<0;if(isNew&&p.kind==='prod'){S.remb=(S.remb||0)+1;p.emb=S.remb;}if(ix>=0)L[ix]=p;else L.push(p);RU_EDIT=null;ruDrawIdent();ruDrawLists();changed();ruConfetti(140);const after=()=>{if(isNew&&p.kind==='prod')setTimeout(()=>ruEmblem(p),350);else ruToast(p.kind==='pkg'?'🎁 Paquete guardado':'✓ Cambios guardados');};if(p.kind==='prod'&&p.tw.includes('labor'))ruSyncStaff(p,after);else if(p.kind==='staff'){ruPropStaff(p);ruDrawLists();after();}else after();
  hqvTrack(p.kind==="pkg"?"ruleta_paquete_guardado":"ruleta_producto_guardado",{n:L.length});const t=$(p.kind==="pkg"?"ruPkgs":"ruProds");t&&t.scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"center"});};
 if(scroll)box.scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"start"});
 if(focusTag){const i=box.querySelector(`.ru-tags[data-t="${focusTag}"] input`);i&&i.focus({preventScroll:true});}}
/* ---------- productos y paquetes ---------- */
/* v25 · el proveedor ve primero el total del evento y después el precio por persona */
function ruPrice(p){const w=p.tw[0],r=w&&ruTotal(p,w);return r?`<span class="ru-pr"><b>${ruMoney(r.tot)}</b> total${r.pp!==null?` · ${ruMoney(r.pp)} por persona`:""}</span>`:`<span class="ru-pr hint">Falta el precio</span>`;}
function ruFormDesc(p,w){if(w==="full")return"Con insumos, tu personal, entrega y montaje";if(w==="rent")return p.dlx.dl.length?p.dlx.dl.map(d=>(DL_LABEL[d.m]||d.m)+(d.cobra?" (con costo)":"")).join(" · "):"Solo insumos";return p.labor.map(r=>`${r.q} ${ruPl(r.n,r.q)}`).join(" + ")||"Agrega tu personal";}
const ruTools=(nm,x)=>`<span class="ru-tools"${x||""}><button type="button" data-ed aria-label="Editar ${esc(nm)}">✏️</button><button type="button" data-rm aria-label="Quitar ${esc(nm)}">✕</button></span>`;
const ruPickB=(ref,nm)=>{const on=RU_PICKED.includes(ref);return`<button class="ru-pick" type="button" data-ref="${esc(ref)}" aria-pressed="${on}" aria-label="Elegir ${esc(nm)}"></button><span class="ru-ck">✓</span>`;};
function ruFormCard(p,w){const r=ruTotal(p,w),ref=p.id+"|"+w,sel=RU_PICK&&RU_PICKED.includes(ref);
 return`<article class="ru-fc${sel?" sel":""}" data-id="${p.id}" data-w="${w}"><b class="ru-fl">${ruFN[w]}</b>${r?`<span class="ru-tot">${ruMoney(r.tot)}</span><small class="ru-ppx">total del evento${r.pp!==null?` · <b>${ruMoney(r.pp)}</b> por persona`:""}</small>`:`<span class="ru-pr hint">Falta el precio</span>`}<small class="ru-fd">${esc(ruFormDesc(p,w))}</small>
  ${RU_PICK?ruPickB(ref,p.name+" "+ruFN[w]):ruTools(ruFN[w].slice(3)+" de "+p.name)}</article>`;}
function ruGroup(p){const ok=ruOk(p);
 return`<section class="ru-grp${ok?"":" warn"}" data-id="${p.id}"><header class="ru-gh"><div><div class="ru-crumbs">${p.dims.slice(0,3).map(d=>`<span>${esc(d)}</span>`).join("")}</div>
  <h4>${p.emb?`<span class="ru-embmini" title="Emblema de servicio">🏅</span>`:""}${esc(p.name)}</h4><span class="ru-meta">Para ${esc(p.pax||"—")} personas · ${p.tw.length} ${p.tw.length===1?"forma":"formas"} de contratarlo</span>${ok?"":`<span class="ru-meta" style="color:var(--bad)">⚠️ ${esc(ruMiss(p).join(", "))}</span>`}</div>
  ${RU_PICK?"":ruTools(p.name)}</header><div class="ru-forms">${p.tw.map(w=>ruFormCard(p,w)).join("")||`<span class="hint">Aún no eliges cómo lo cobras.</span>`}</div></section>`;}
function ruStaffCard(p){const r=p.labor[0],ok=ruOk(p),sel=RU_PICK&&RU_PICKED.includes(p.id),ev=(+r.p||0)*(r.u==="Por hora"?(+r.min||5):1);
 return`<article class="ru-pc ru-sc${sel?" sel":""}${ok?"":" warn"}" data-id="${p.id}"><span class="ru-stb">🙋 Personal</span><h4>${esc(p.name)}</h4>${+r.p>0?`<span class="ru-pr"><b>${money(r.p)}</b> ${esc(ruXU(r.u))}</span><span class="ru-meta">${r.u==="Por hora"?`Mínimo ${esc(r.min||5)} h · `:""}${money(ev)} por evento${+r.xh>0?` · extra ${money(r.xh)} ${esc(r.xu||ruXU(r.u))}`:""}</span>`:`<span class="ru-pr hint">Falta el precio</span>`}
  ${RU_PICK?ruPickB(p.id,p.name):ruTools(p.name)}</article>`;}
function ruVenueCard(){const x=ruVenueItem();if(!x)return"";const t=ruVenueTot(),sel=RU_PICKED.includes("venue");
 return`<article class="ru-pc ru-vc${sel?" sel":""}" data-id="venue"><span class="ru-vb">🏡 Tu venue</span><h4>${esc(x.name)}</h4><span class="ru-pr">${t?`<b>${ruMoney(t)}</b> renta`:"Pon tu precio de renta en «Mi venue»"}</span><span class="ru-meta">${esc(S.venue.seated||"—")} personas sentadas</span>${RU_PICK?ruPickB("venue",x.name):""}</article>`;}
function ruCard(p){const ok=ruOk(p),r=ruTotal(p,p.tw[0]);
 return`<article class="ru-pc ru-kc${ok?"":" warn"}" data-id="${p.id}"><span class="ru-pkb">🎁 Paquete</span><h4>${esc(p.name)}</h4>${r?`<span class="ru-tot">${ruMoney(r.tot)}</span><small class="ru-ppx">total del evento${r.pp!==null?` · <b>${ruMoney(r.pp)}</b> por persona`:""}</small>`:`<span class="ru-pr hint">Falta el precio</span>`}
  <span class="ru-meta">Para ${esc(p.pax||"—")} personas · ${esc(p.items.map(ref=>ruItemName(ref,p)).join(" + "))}</span>${ok?"":`<span class="ru-meta" style="color:var(--bad)">⚠️ ${esc(ruMiss(p).join(", "))}</span>`}${RU_PICK?"":ruTools(p.name)}</article>`;}
const ruRefs=()=>[...(S.rprods||[]).flatMap(p=>p.kind==="staff"?[p.id]:p.tw.map(w=>p.id+"|"+w)),...(ruVenueItem()?["venue"]:[])];
function ruDrawLists(){if(!$("ruProds"))return;ruDefaults();const P=S.rprods.filter(x=>x.kind==="prod"),ST=S.rprods.filter(x=>x.kind==="staff"),K=S.rpkgs,nRef=ruRefs().length;
 $("ruProdH").textContent=`Tus productos (${P.length})`;
 $("ruProds").innerHTML=(RU_PICK&&ruVenueItem()?ruVenueCard():"")+(P.map(ruGroup).join("")||`<p class="ru-empty">Aún no guardas productos. Alinea los rodillos y toca «Guardar esta combinación».</p>`);
 const sw=$("ruStaffSec");if(sw){sw.hidden=!ST.length;$("ruStaffH").textContent=`🙋 Tu personal (${ST.length})`;$("ruStaff").innerHTML=ST.map(ruStaffCard).join("");}
 const lock=nRef<2;$("ruPkSec").classList.toggle("locked",lock);$("ruPkgH").textContent=lock?"🔒 Tus paquetes":`Tus paquetes (${K.length})`;
 $("ruPkgs").innerHTML=lock?`<p class="ru-lock">🔒 Se desbloquea cuando tengas 2 productos. ${nRef?"Te falta 1.":"Te faltan 2."} Después combinas tus productos en paquetes.</p>`:K.map(ruCard).join("")||`<p class="ru-empty">Toca «🎁 Armar un paquete» y elige qué combinar.</p>`;
 $("ruMk").disabled=lock;$("ruBar").hidden=!RU_PICK;$("ruBarT").textContent=RU_PICKED.length<2?"Elige 2 o más: formas de contratar, personal"+(ruVenueItem()?" o tu venue":""):`${RU_PICKED.length} elegidos`;$("ruGo").disabled=RU_PICKED.length<2;
 document.querySelectorAll(".ru-step2").forEach(x=>x.classList.toggle("on",!lock));
 const root=$("ruProds").closest(".panel")||document;
 root.querySelectorAll(".ru-pick").forEach(b=>b.onclick=()=>{const r=b.dataset.ref;RU_PICKED=RU_PICKED.includes(r)?RU_PICKED.filter(x=>x!==r):[...RU_PICKED,r];ruDrawLists();});
 const edit=(p,w)=>{RU_EDIT=JSON.parse(JSON.stringify(p));ruDrawIdent(!w);if(w)setTimeout(()=>{const t=document.querySelector(`#ruIdent .ru-tg[data-w="${w}"]`);(t||$("ruIdent")).scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"start"});},30);};
 const undoRm=(L,p,ix,msg)=>{L.splice(ix,1);ruDrawLists();changed();ruToast(msg,()=>{L.splice(ix,0,p);ruDrawLists();changed();});};
 root.querySelectorAll(".ru-grp").forEach(g=>{const p=S.rprods.find(x=>x.id===g.dataset.id);if(!p)return;const T=g.querySelector(".ru-gh .ru-tools");
  if(T){T.querySelector("[data-ed]").onclick=()=>edit(p);T.querySelector("[data-rm]").onclick=()=>undoRm(S.rprods,p,S.rprods.indexOf(p),`Quitaste «${p.name}»`);}
  g.querySelectorAll(".ru-fc").forEach(c=>{const w=c.dataset.w,t=c.querySelector(".ru-tools");if(!t)return;t.querySelector("[data-ed]").onclick=()=>edit(p,w);
   t.querySelector("[data-rm]").onclick=()=>{if(p.tw.length===1){undoRm(S.rprods,p,S.rprods.indexOf(p),`Quitaste «${p.name}»`);return;}const old=[...p.tw];p.tw=p.tw.filter(x=>x!==w);ruDrawLists();changed();ruToast(`Quitaste «${ruFN[w].slice(3)}» de ${p.name}`,()=>{p.tw=old;ruDrawLists();changed();});};});});
 root.querySelectorAll(".ru-sc").forEach(c=>{const p=S.rprods.find(x=>x.id===c.dataset.id),t=c.querySelector(".ru-tools");if(!p||!t)return;t.querySelector("[data-ed]").onclick=()=>edit(p);t.querySelector("[data-rm]").onclick=()=>undoRm(S.rprods,p,S.rprods.indexOf(p),`Quitaste a «${p.name}» de tu personal`);});
 root.querySelectorAll(".ru-kc").forEach(c=>{const p=K.find(x=>x.id===c.dataset.id),t=c.querySelector(".ru-tools");if(!p||!t)return;t.querySelector("[data-ed]").onclick=()=>edit(p);t.querySelector("[data-rm]").onclick=()=>undoRm(K,p,K.indexOf(p),`Quitaste «${p.name}»`);});
 if(typeof vnRefresh==="function")vnRefresh();}
function ruToast(msg,undo){document.querySelectorAll(".ru-toast").forEach(x=>x.remove());const t=document.createElement("div");t.className="ru-toast";t.innerHTML=`<span>${esc(msg)}</span>${undo?`<button class="link" type="button">Deshacer</button>`:""}`;document.body.appendChild(t);if(undo)t.querySelector("button").onclick=()=>{undo();t.remove();};setTimeout(()=>t.remove(),4200);}
/* ---------- «Arma tu servicio» (se usa en Mis servicios y, si solo tienes venue, en Mi venue) ---------- */
function ruBuilderHtml(){return`<div class="ru-steps" role="list"><div class="ru-st on" role="listitem"><b>1</b><span><strong>Tus productos</strong><small>Uno por uno: alinea los rodillos, guarda y dale identidad. Cada uno te da un emblema 🏅.</small></span></div><div class="ru-st ru-step2" role="listitem"><b>2</b><span><strong>Tus paquetes</strong><small>Después combinas: catering + personal + ${S.types&&S.types.venue?"tu venue":"música"}.</small></span></div></div>
 <div class="ru-search"><input id="ruQ" type="search" autocomplete="off" placeholder="Busca lo que ofreces: barra de café, DJ, sillas Tiffany…" aria-label="Busca lo que ofreces"><div id="ruQr" class="ru-qr" hidden></div></div>
 ${ruMachineHtml()}
 <section class="ru-ident" id="ruIdent" hidden></section>
 <div class="ru-lh"><h3 id="ruProdH">Tus productos</h3></div>
 <div class="ru-glist" id="ruProds"></div>
 <section class="ru-stsec" id="ruStaffSec" hidden><div class="ru-lh"><h3 id="ruStaffH">🙋 Tu personal</h3></div><span class="hint">Cada perfil es un producto: se cotiza solo y lo sumas a tus paquetes por persona.</span><div class="ru-grid" id="ruStaff"></div></section>
 <div class="ru-bar" id="ruBar" hidden><span id="ruBarT"></span><span class="row"><button class="link" id="ruNo" type="button">Cancelar</button><button class="btn cta sm" id="ruGo" type="button">Combinar</button></span></div>
 <section class="ru-pksec" id="ruPkSec"><div class="ru-lh"><h3 id="ruPkgH">Tus paquetes</h3><button class="btn ghost sm" id="ruMk" type="button">🎁 Armar un paquete</button></div>
 <div class="ru-grid" id="ruPkgs"></div></section>`;}
function ruStartPick(pre){RU_PICK=true;RU_PICKED=pre||[];ruDrawLists();const t=$("ruProds");t&&t.scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"start"});}
function ruBindBuilder(){ruBindMachine();ruBindSearch();ruDrawLists();ruDrawIdent();
 $("ruMk").onclick=()=>ruStartPick([]);
 $("ruNo").onclick=()=>{RU_PICK=false;RU_PICKED=[];ruDrawLists();};
 $("ruGo").onclick=()=>{const items=[...RU_PICKED];RU_PICK=false;RU_PICKED=[];const qty={};items.forEach(r=>{const x=ruById(r);if(x&&x.kind==="staff")qty[r]="1";});
  const cr=[...new Set(items.flatMap(r=>{const x=ruById(r);return!x?[]:x.kind==="staff"?[x.n]:x.crew.map(c=>c.n);}))];const vn=items.includes("venue");
  RU_EDIT=Object.assign({id:"k"+Date.now().toString(36),kind:"pkg",items,qty,name:"",dishes:[],ins:[],crew:cr.map(n=>({n,q:"1"})),pax:vn?String(S.venue.seated||""):"",tw:[],tar:ruBlankT("Por persona")},ruBlankMore());ruDrawLists();ruDrawIdent(true);hqvTrack("ruleta_paquete_iniciado",{n:items.length,venue:vn});};}
/* ---------- paso «Mis servicios» ---------- */
function drawSvcStep(){const sc=S.svcScope=S.svcScope||{S:false,E:false};ruDefaults();
 $("stepBody").innerHTML=`<div class="panel"><span class="crumb">Mi negocio › Servicios</span><h2>Mis servicios 🎉</h2><p class="sub">Arma tu servicio alineando los rodillos. Nosotros se lo mostramos al anfitrión por persona y en total.</p>
 <div class="field"><span class="lbl">¿En qué tipo de eventos trabajas? <span class="opt">Puedes elegir los dos</span></span><div class="chips${MISS(sc.S||sc.E)}" style="width:fit-content;border-radius:99px"><button type="button" class="chip scp" data-v="S" aria-pressed="${!!sc.S}">${TICK}🎉 Sociales</button><button type="button" class="chip scp" data-v="E" aria-pressed="${!!sc.E}">${TICK}💼 Empresariales</button></div></div>
 ${ruBuilderHtml()}
 ${priceBoxHtml()}
 ${zonesHtml(S.svcZones,"svc","📍 Tu zona general: ¿hasta dónde llevas tus servicios?")}<span class="hint" style="margin-top:-10px">Cada producto la usa por defecto. Si alguno llega más lejos o más cerca, lo cambias en su ficha.</span>${VIATICOS}${navHtml()}</div>`;
 document.querySelectorAll(".scp").forEach(c=>c.onclick=()=>{sc[c.dataset.v]=!sc[c.dataset.v];c.setAttribute("aria-pressed",!!sc[c.dataset.v]);changed();});
 ruBindBuilder();if(S._pickVenue){S._pickVenue=false;setTimeout(()=>ruStartPick(["venue"]),60);}if(S._editPkg){const k=S.rpkgs.find(x=>x.id===S._editPkg);S._editPkg=null;if(k){RU_EDIT=JSON.parse(JSON.stringify(k));setTimeout(()=>ruDrawIdent(true),60);}}
 bindPriceBox(drawSvcStep);bindZones(S.svcZones,"svc",drawSvcStep);bindNav();}
function ruMissStep(m){ruDefaults();if(!S.rprods.some(x=>x.kind==="prod"))m.push("Guarda al menos un producto en «Arma tu servicio»");
 S.rprods.forEach(p=>{const x=ruMiss(p);if(x.length)m.push(`${p.name||"Producto"}: ${x.join(", ")}`);});S.rpkgs.forEach(p=>{const x=ruMiss(p);if(x.length)m.push(`${p.name||"Paquete"}: ${x.join(", ")}`);});}
/* ---------- sitio público ---------- */
function ruSyncServices(){if(!S.rprods)return;const cats=[...new Set(S.rprods.map(p=>p.dims[0]))];
 S.services=cats.map(c=>{const ex=(S.services||[]).find(s=>s.cat===c&&s._ru);return Object.assign(ex||{_ru:true,cat:c,desc:"",dl:[],specs:[],photos:[],min:blankMin(),promo:blankPromo(),offers:[],staff:[],rent:[],askStaff:null,askRent:null,cater:{food:false,drink:false,gas:[]}},{subs:S.rprods.filter(p=>p.dims[0]===c).map(p=>({n:p.name}))});});}
/* v25 · en el sitio: cada producto con sus formas de contratarlo y, aparte, tu personal por perfil */
function ruSiteForm(p,w){const r=ruTotal(p,w);if(!r||r.pp===null)return"";const v=+S.svcVar||0;
 const d=w==="full"?"Incluye insumos, personal, entrega y montaje":w==="rent"?(p.dlx.dl.length?p.dlx.dl.map(dlText).join(" · "):"Solo insumos"):p.labor.map(x=>`${x.q} ${ruPl(x.n,x.q)}`).join(" + ")+(p.lpol.night?` · después de las 12:00 a.m. +${p.lpol.nightPct}%`:"");
 return`<span class="pform"><span class="pfh"><b>${ruFN[w]}</b><span class="price"><span class="pl">${ruMoney(r.pp)} <small>por persona</small></span><span class="pl"><small>${ruMoney(r.tot)} en total</small></span>${v?`<span class="pl"><small class="pmv">± ${v}%</small></span>`:""}</span></span><small class="inc">${esc(d)}</small></span>`;}
function ruSiteStaff(L){return L.length?`<span class="po pstaff"><span class="pob"><span class="poh"><b>🙋 Personal por persona<small class="ctag">Contrátalo solo o súmalo a tu fiesta</small></b></span>
 ${L.map(x=>{const r=x.labor[0];return`<span class="pst-r"><span>${esc(x.name)}</span><span><b>${money(r.p)}</b> ${esc(ruXU(r.u))}${r.u==="Por hora"?` · mín. ${esc(r.min||5)} h`:""}${+r.xh>0?` · extra ${money(r.xh)} ${esc(r.xu||ruXU(r.u))}`:""}</span></span>`;}).join("")}</span></span>`:"";}
function svcPlist(s){const all=(S.rprods||[]).filter(p=>p.dims[0]===s.cat&&ruOk(p));
 return all.filter(p=>p.kind==="prod").map(p=>{const ph=p.photos[0];
 return`<span class="po${ph?" hasph":""}" id="producto-${slug(p.name)}">${ph?`<img class="phbig" src="${ph.url||ph}" alt="">`:""}<span class="pob"><span class="poh"><b>${esc(p.name)}<small class="ctag">${esc(p.dims.slice(1,3).filter(x=>x!=="Otro").join(" · "))} · para ${esc(p.pax)} personas · ${p.tw.length} ${p.tw.length===1?"forma":"formas"} de contratarlo</small></b></span>
  <span class="pforms">${p.tw.map(w=>ruSiteForm(p,w)).join("")}</span>
  ${p.dishes.length?`<small class="inc">🍴 ${esc(p.dishes.join(", "))}</small>`:""}${p.ins.length?`<small class="inc">🧺 Incluye: ${esc(p.ins.join(", "))}</small>`:""}
  ${p.ext.filter(e=>filled(e.c)).length?`<small class="inc">➕ Extras: ${esc(p.ext.filter(e=>filled(e.c)).map(e=>`${e.c} ${money(e.p)} ${e.u}`).join(" · "))}</small>`:""}${p.min.has===true&&minText(p.min)?`<small class="inc">🧾 ${esc(minText(p.min))}</small>`:""}${p.promo.has===true&&p.promo.what?`<small class="inc">🏷️ ${esc(p.promo.what)}</small>`:""}${p.cov&&!p.cov.same?`<small class="inc">📍 Llega a: ${esc(zonesText(p.cov.zones))}</small>`:""}
  ${p.photos.length>1?`<span class="pph">${p.photos.slice(1,5).map(x=>`<img src="${x.url||x}" alt="">`).join("")}</span>`:""}</span></span>`;}).join("")+ruSiteStaff(all.filter(p=>p.kind==="staff"));}
function pkgSite(){const L=(S.rpkgs||[]).filter(ruOk);if(!L.length)return"";
 return`<div class="ms-item pkgsite"><div class="ms-item-top"><b>🎁 Paquetes</b></div><div class="plist">${L.map(P=>{const w=P.tw[0],r=ruTotal(P,w),ph=P.photos[0];return`<span class="po${ph?" hasph":""}" id="paquete-${slug(P.name)}">${ph?`<img class="phbig" src="${ph.url||ph}" alt="">`:""}<span class="pob"><span class="poh"><b>${esc(P.name)}<small class="ctag">Para ${esc(P.pax)} personas</small></b><span class="price"><span class="pl">${ruMoney(r.pp)} <small>por persona</small></span><span class="pl"><small>${ruMoney(r.tot)} en total</small></span></span></span>
  <small class="inc">Incluye: ${esc(P.items.map(ref=>ruItemName(ref,P)).join(" + "))}</small>${P.ins.length?`<small class="inc">🧺 ${esc(P.ins.join(", "))}</small>`:""}${P.promo.has===true&&P.promo.what?`<small class="inc">🏷️ ${esc(P.promo.what)}</small>`:""}</span></span>`;}).join("")}</div></div>`;}
/* ===== v25 · Integración del venue =====
   - Tus productos, tu personal y tus paquetes se reflejan en «Mi venue» con «¿Lo ofreces en tu venue?» y un precio aparte (no descuento).
   - El venue entra al combinador como una pieza más: «venue + productos + personal», sin volver a llenar sus datos.
   - Si solo tienes venue, «Arma tu servicio» vive dentro de «Mi venue». */
function vnItems(){const out=[];(S.rprods||[]).filter(p=>p.kind==="prod"&&ruOk(p)).forEach(p=>p.tw.forEach(w=>{const t=w==="labor"?null:p.tar[w];out.push({g:"prod",ref:p.id+"|"+w,name:p.name,sub:ruFN[w],price:t&&t.p,unit:t&&t.u.toLowerCase(),fixed:!t});}));
 (S.rprods||[]).filter(p=>p.kind==="staff"&&ruOk(p)).forEach(p=>{const r=p.labor[0];out.push({g:"staff",ref:p.id,name:p.name,sub:"🙋 Tu personal",price:r.p,unit:ruXU(r.u)});});
 (S.rpkgs||[]).filter(k=>!k.items.includes("venue")&&ruOk(k)).forEach(k=>{const w=k.tw[0],t=k.tar[w];out.push({g:"pkg",ref:"pkg:"+k.id,name:k.name,sub:"🎁 Paquete",price:t&&t.p,unit:t&&t.u.toLowerCase(),fixed:w==="labor"});});return out;}
const vnE=(v,ref)=>(v.svcIn=v.svcIn||{})[ref]||(v.svcIn[ref]={on:true,p:""});
function vnRowsHtml(v){const L=vnItems();if(!L.length)return`<p class="ru-empty">${S.types.services?"Cuando guardes productos en «Mis servicios», aparecen aquí para que decidas cuáles ofreces en tu venue y a qué precio.":"Si ofreces comida, bebida, personal o algo más dentro de tu venue, ármalo aquí abajo y aparecerá en esta lista."}</p>`;
 const G=[["prod","Tus productos"],["staff","Tu personal"],["pkg","Tus paquetes"]];
 return G.filter(([g])=>L.some(x=>x.g===g)).map(([g,t])=>`<span class="ru-sl">${t}</span>${L.filter(x=>x.g===g).map(x=>{const e=vnE(v,x.ref),on=e.on!==false;return`<div class="vn-r${on?"":" off"}" data-ref="${esc(x.ref)}"><button type="button" class="vn-on" aria-pressed="${on}" aria-label="¿Ofreces ${esc(x.name)} en tu venue?">${on?"✓":""}</button>
  <span class="vn-n"><b>${esc(x.name)}</b><small>${esc(x.sub)}${x.fixed?" · con los precios de tu personal":+x.price>0?` · precio normal ${money(x.price)} ${esc(x.unit)}`:""}</small></span>
  ${on&&!x.fixed?`<label class="ru-f vn-p"><small>en tu venue</small><span class="ru-fi"><i>$</i><input type="number" min="0" inputmode="decimal" class="vn-pi" value="${esc(e.p)}" placeholder="${esc(x.price||"0")}" aria-label="Precio de ${esc(x.name)} en tu venue"></span></label>`:on?"":`<span class="vn-no">No en tu venue</span>`}</div>`;}).join("")}`).join("");}
function vnPkgInner(){const L=(S.rpkgs||[]).filter(k=>k.items.includes("venue"));
 return`${L.map(k=>{const r=ruTotal(k,k.tw[0]);return`<div class="vn-kc"><span class="ru-pkb">🎁 Paquete</span><b>${esc(k.name||"Sin nombre")}</b>${r?`<span class="ru-tot">${ruMoney(r.tot)}</span><small class="ru-ppx">total del evento${r.pp!==null?` · <b>${ruMoney(r.pp)}</b> por persona`:""}</small>`:`<span class="hint">Falta el precio</span>`}<small class="ru-fd">${esc(k.items.map(ref=>ruItemName(ref,k)).join(" + "))}</small><button type="button" class="link vn-ked" data-id="${k.id}">✏️ Editar</button></div>`;}).join("")}
 <button type="button" class="btn ghost sm" id="vnMkPk">🎁 Armar paquete con tu venue</button>`;}
function vnPkgHtml(v){return`<div class="vn-pk"><b style="font-size:14px">📦 Paquetes con tu venue</b><span class="hint">Se arman en el combinador: tu venue es una pieza más, junto a tus productos y tu personal. Los datos del venue no se vuelven a llenar.</span><div class="vn-kl" id="vnPk">${vnPkgInner()}</div></div>`;}
function vnSvcHtml(v){const solo=!S.types.services,open=solo&&((S.rprods||[]).length>0||v._build);
 return`<div class="field vn-svc" id="vnSvc"><span class="lbl">🍽️ Tus servicios en tu venue</span><span class="hint">Marca lo que ofreces dentro de tu venue. El precio en tu venue es un precio aparte, no un descuento: si lo dejas vacío, usamos tu precio normal. Si quieres, después le sumas una promoción.</span>
  <div class="vn-rows" id="vnRows">${vnRowsHtml(v)}</div>
  ${solo?`<details class="more vn-build"${open?" open":""}><summary>🧩 Arma tu servicio <span class="opt">comida, bebida, personal o lo que ofrezcas en tu venue</span></summary><div class="vn-bw">${ruBuilderHtml()}</div></details>`:`<button type="button" class="link" id="vnGoSvc" style="justify-self:start">＋ Agregar o cambiar productos en «Mis servicios»</button>`}
  <div class="polc${MISS(!!v.extAll)}"><b>🚪 ¿Pueden traer sus propios proveedores?</b><span class="hint">Para lo que no ofreces tú.</span><div class="chips">${[["si","Sí, todos"],["algunos","Solo algunos"],["no","No"]].map(([x,t])=>`<button type="button" class="chip p-ext" data-v="${x}" aria-pressed="${v.extAll===x}">${TICK}${t}</button>`).join("")}</div>
   ${v.extAll==="algunos"?`<input type="text" id="v-extn" value="${esc(v.extAllNote)}" placeholder="¿Cuáles sí y cuáles no?" aria-label="Cuáles servicios externos">`:""}</div>
  ${vnPkgHtml(v)}</div>`;}
function vnGoSvc(){step=stepList().findIndex(s=>s.id==="svc");render();scrollTo({top:0,behavior:"instant"});}
function vnBindRows(v){const box=$("vnRows");if(!box)return;box.querySelectorAll(".vn-r").forEach(R=>{const e=vnE(v,R.dataset.ref);R.querySelector(".vn-on").onclick=()=>{e.on=e.on===false;box.innerHTML=vnRowsHtml(v);vnBindRows(v);changed();};const i=R.querySelector(".vn-pi");if(i)i.oninput=x=>{e.p=x.target.value;changed();};});}
function vnBindPk(v){const mk=$("vnMkPk");if(mk)mk.onclick=()=>{if($("ruProds")){const d=document.querySelector(".vn-build");if(d)d.open=true;ruStartPick(["venue"]);}else{S._pickVenue=true;vnGoSvc();}};
 document.querySelectorAll(".vn-ked").forEach(b=>b.onclick=()=>{const k=S.rpkgs.find(x=>x.id===b.dataset.id);if(!k)return;if($("ruIdent")){const d=document.querySelector(".vn-build");if(d)d.open=true;RU_EDIT=JSON.parse(JSON.stringify(k));ruDrawIdent(true);}else{S._editPkg=k.id;vnGoSvc();}});}
function vnRefresh(){const v=S.venue;if(!v||!$("vnSvc"))return;const r=$("vnRows");if(r){r.innerHTML=vnRowsHtml(v);vnBindRows(v);}const k=$("vnPk");if(k){k.innerHTML=vnPkgInner();vnBindPk(v);}}
function vnBind(v){vnBindRows(v);vnBindPk(v);const g=$("vnGoSvc");if(g)g.onclick=vnGoSvc;
 const d=document.querySelector(".vn-build");if(d){ruBindBuilder();d.ontoggle=()=>{v._build=d.open;if(d.open)requestAnimationFrame(()=>{for(let i=0;i<4;i++){ruCenter(i,Math.max(0,ruIdx(i,S.rsel[i])),false);ruPaint(i);}ruUpdate();});};}}
const vnPkgs=()=>(S.rpkgs||[]).filter(k=>k.items.includes("venue"));
/* en el sitio del venue */
function vnSiteHtml(v){const L=vnItems().filter(x=>vnE(v,x.ref).on!==false),K=vnPkgs().filter(ruOk);if(!L.length&&!K.length)return"";
 return`<div class="vn-site"><b>🍽️ Servicios en este venue</b>${K.map(k=>{const r=ruTotal(k,k.tw[0]);return r?`<span class="vn-sr pk"><span>🎁 ${esc(k.name)}<small>${esc(k.items.map(ref=>ruItemName(ref,k)).join(" + "))}</small></span><span><b>${ruMoney(r.pp)}</b> por persona<small>${ruMoney(r.tot)} en total · ${esc(k.pax)} personas</small></span></span>`:"";}).join("")}
  ${L.map(x=>{const e=vnE(v,x.ref),pr=+e.p>0?e.p:x.price;return`<span class="vn-sr"><span>${esc(x.name)}<small>${esc(x.sub.slice(2).trim())}</small></span><span>${x.fixed?"Precio por perfil":`<b>${money(pr)}</b> ${esc(x.unit)}`}</span></span>`;}).join("")}</div>`;}
