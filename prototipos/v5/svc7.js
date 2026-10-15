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
const RU_TL={rent:["📦 Servicio / producto sin staff","Lo llevas o lo recogen"],full:["🙋 Servicio / producto con staff","Tu staff va al evento"],labor:["🙋 Staff","Por perfil"]};
function ruConfetti(n){if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;let c=document.getElementById("ruConf");if(!c){c=document.createElement("canvas");c.id="ruConf";c.style.cssText="position:fixed;inset:0;pointer-events:none;z-index:120";document.body.appendChild(c);}
 const x=c.getContext("2d");c.width=innerWidth;c.height=innerHeight;const cols=["#7B2FF7","#FA1ED2","#FF6905","#BEFF00","#FAFA19","#00C389"];
 const P=Array.from({length:n||120},()=>({x:innerWidth*(.25+Math.random()*.5),y:innerHeight*.35,vx:(Math.random()-.5)*14,vy:-Math.random()*13-4,s:5+Math.random()*6,c:cols[Math.random()*6|0],a:Math.random()*6}));let f=0;
 (function go(){x.clearRect(0,0,c.width,c.height);P.forEach(q=>{q.vy+=.33;q.x+=q.vx;q.y+=q.vy;q.a+=.2;x.save();x.translate(q.x,q.y);x.rotate(q.a);x.fillStyle=q.c;x.fillRect(-q.s/2,-q.s/2,q.s,q.s*.6);x.restore();});if(++f<110)requestAnimationFrame(go);else x.clearRect(0,0,c.width,c.height);})();}
/* v25 · cada perfil de personal es un producto independiente (un perfil, un precio) */
const ruStaffBy=n=>(S.rprods||[]).find(x=>x.kind==="staff"&&nrm(x.n||"")===nrm(n));
const RU_XU=["por hora","por turno de 5 h","por evento","por día"];
const ruShortU=t=>t.replace(/^por /,"").replace("turno de 5 h","turno 5 h");
/* plural del primer término: 7 meseros, 2 capitanes de meseros */
const ruPl=(n,q)=>{if(+q<=1)return n.toLowerCase();const w=n.toLowerCase().split(" ");const x=w[0];w[0]=/[aeiouáéó]$/.test(x)||/er$/.test(x)?x+"s":/[áóé]n$/.test(x)?x.replace(/án$/,"anes").replace(/ón$/,"ones").replace(/én$/,"enes"):/[lrndj]$/.test(x)?x+"es":x+"s";return w.join(" ");};
const ruXU=u=>(RU_LU.find(x=>x[0]===u)||["","por hora"])[1];
/* v26 · cada perfil puede cobrarse de varias formas (turno de 5 h, por hora…) y tiene un solo extra */
const ruTarsOk=r=>(r.tars||[]).length>0&&r.tars.every(t=>+t.p>0&&!!t.u);
const ruTarsText=r=>(r.tars||[]).filter(t=>+t.p>0&&t.u).map(t=>`${money(t.p)} ${ruXU(t.u)}`).join(" · ");
const ruHM=h=>{h=((h%24)+24)%24;const H=Math.floor(h),M=Math.round((h-H)*60),ap=H<12?"a.m.":"p.m.",h12=H%12||12;return`${h12}:${String(M).padStart(2,"0")} ${ap}`;};
const ruHr=t=>{const [a,b]=String(t||"0:0").split(":").map(Number);return(a||0)+(b||0)/60;};
/* cómo se cotiza un perfil en una fiesta (s, e en horas; e puede pasar de 24) */
function ruProfQuote(r,pol,s,e){if(e<=s)e+=24;const H=e-s,pct=pol&&pol.night?(+pol.nightPct||0)/100:0,night=h=>h>=24;let best=null;
 (r.tars||[]).filter(t=>+t.p>0&&t.u).forEach(t=>{const p=+t.p,lines=[];let tot=0;
  if(t.u==="Por hora"){let n=0,nn=0;for(let h=s;h<e-1e-9;h++)night(h)?nn++:n++;tot=p*n+p*(1+pct)*nn;lines.push(`${n} h × ${money(p)}`+(nn?` + ${nn} h × ${money(Math.round(p*(1+pct)))} después de las 12 (+${Math.round(pct*100)}%)`:""));}
  else{const base=t.u==="Por turno (5 h)"?5:H;tot=p;lines.push(t.u==="Por turno (5 h)"?`Turno de 5 h (${ruHM(s)} a ${ruHM(s+5)}): ${money(p)}`:`${ruXU(t.u).replace(/^por /,"").replace(/^./,c=>c.toUpperCase())}: ${money(p)}`);
   const xh=Math.max(0,H-base);if(xh>0&&+r.xh>0){const xu=r.xu||"por hora";
    if(xu==="por hora"){let n=0,nn=0;for(let h=s+base;h<e-1e-9;h++)night(h)?nn++:n++;const x=+r.xh;tot+=x*n+x*(1+pct)*nn;lines.push(`${xh} h extra: `+[n?`${n} × ${money(x)}`:"",nn?`${nn} × ${money(Math.round(x*(1+pct)))} después de las 12 (+${Math.round(pct*100)}%)`:""].filter(Boolean).join(" + "));}
    else{const k=xu==="por turno de 5 h"?Math.ceil(xh/5):1;tot+=k*(+r.xh);lines.push(`${xh} h extra: ${k} × ${money(r.xh)} ${xu}`);}}
   else if(xh>0)lines.push(`${xh} h extra: sin precio de extra`);}
  if(!best||tot<best.tot)best={tot:Math.round(tot),lines,t};});return best;}
const ruProfCost=(r,pol)=>{const q=ruProfQuote(r,pol,18,23);return q?q.tot:0;};
function ruLabRow(n,q){const s=ruStaffBy(n),r=s&&s.labor[0];return r?{n,q:q||"1",tars:JSON.parse(JSON.stringify(r.tars||[{p:r.p,u:r.u}])),xh:r.xh,xu:r.xu}:{n,q:q||"1",tars:[{p:"",u:""}],xh:"",xu:""};}
const ruSyncPU=r=>{const t=(r.tars||[])[0]||{};r.p=t.p||"";r.u=t.u||"";};
function ruNewStaff(r,cat){const n=r.n,x={n,q:"1",tars:JSON.parse(JSON.stringify(r.tars||[{p:r.p,u:r.u}])),xh:r.xh,xu:r.xu};ruSyncPU(x);return Object.assign(ruBlankMore(),{id:"st-"+slug(n),kind:"staff",n,name:n,dims:[cat,"Personal independiente","Solo talento",n],otro:"",dishes:[],ins:[],crew:[],pax:"",tw:["labor"],tar:ruBlankT("Por hora"),emb:0,labor:[x]});}
function ruPropStaff(sp){const e=sp.labor[0];(S.rprods||[]).forEach(x=>{if(x.kind!=="prod")return;x.labor.forEach(r=>{if(nrm(r.n)===nrm(sp.n)){r.tars=JSON.parse(JSON.stringify(e.tars));r.xh=e.xh;r.xu=e.xu;ruSyncPU(r);}});});}
function ruSyncStaff(p,done){const cat=p.dims[0],added=[],conf=[],key=r=>JSON.stringify((r.tars||[]).map(t=>[+t.p,t.u]));
 p.labor.forEach(r=>{let sp=ruStaffBy(r.n);if(!sp){sp=ruNewStaff(r,cat);S.rprods.push(sp);added.push(r.n);return;}const e=sp.labor[0];
  if(ruTarsOk(e)&&ruTarsOk(r)&&key(e)!==key(r))conf.push({n:r.n,sp,r});else{if(ruTarsOk(r))e.tars=JSON.parse(JSON.stringify(r.tars));e.xh=r.xh;e.xu=r.xu;ruSyncPU(e);}});
 const fin=()=>{(S.rprods||[]).filter(x=>x.kind==="staff").forEach(ruPropStaff);ruDrawLists();changed();if(added.length)ruToast(`🙋 Sumamos a «Tu staff»: ${added.join(", ")}. También se cotizan solos.`);done&&done();};
 if(!conf.length){fin();return;}
 const md=document.createElement("div");md.className="rmodal";md.innerHTML=`<div class="rsheet ru-confl"><span class="ru-embk">🙋 TU PERSONAL</span><h2>Un perfil, un precio</h2><span>Estos perfiles ya tenían otras tarifas. ¿Con cuáles te quedas para todos tus productos?</span>
  ${conf.map((c,i)=>`<div class="ru-cf" data-i="${i}"><b>${esc(c.n)}</b><span class="row"><button type="button" class="btn sm ru-cfa">${esc(ruTarsText(c.sp.labor[0]))}</button><button type="button" class="btn sm ghost ru-cfb">${esc(ruTarsText(c.r))}</button></span></div>`).join("")}</div>`;
 document.body.appendChild(md);let left=conf.length;
 md.querySelectorAll(".ru-cf").forEach(R=>{const c=conf[+R.dataset.i],pick=a=>{const e=c.sp.labor[0];if(!a){e.tars=JSON.parse(JSON.stringify(c.r.tars));e.xh=c.r.xh;e.xu=c.r.xu;ruSyncPU(e);}R.remove();if(--left===0){md.remove();fin();}};R.querySelector(".ru-cfa").onclick=()=>pick(true);R.querySelector(".ru-cfb").onclick=()=>pick(false);});}
function ruEmblem(p){const n=S.remb,m=ruMasc(p.dims);const md=document.createElement("div");md.className="rmodal";
 md.innerHTML=`<div class="rsheet ru-embs"><span class="ru-embk">🏅 NUEVO EMBLEMA</span><div class="ru-emb"><img src="img/${m}.webp" alt=""><span>SERVICIO</span></div><h2>¡${esc(p.name)} ya está listo!</h2><span>Ganaste el emblema de <b>Servicio de ${esc(p.dims[0])}</b>. Llevas <b>${n}</b> ${n===1?"servicio":"servicios"} en tu sitio.</span>
  <span class="hint" style="color:rgba(255,255,255,.85)!important">${(S.rprods||[]).length>=2?"Ya puedes combinar tus productos en paquetes.":"Con un producto más desbloqueas los paquetes."}</span><button type="button" class="btn cta" id="ruEmbOk">¡Seguir! 🎉</button></div>`;
 document.body.appendChild(md);const close=()=>md.remove();md.querySelector("#ruEmbOk").onclick=close;md.onclick=e=>{if(e.target===md)close();};hqvTrack("emblema_servicio",{n});}
let RU_EDIT=null,RU_PICK=false,RU_PICKED=[],RU_BUSY=[null,null,null,null],RU_DRAG=null,RU_MOVED=false,RU_LASTM="";
const ruBlankT=u=>({i:{p:"",u,q:""},full:{p:"",u,q:""},rent:{p:"",u,q:""},labor:{p:"",u:"Por hora",q:""}});
function ruDefaults(){if(!S.rprods)S.rprods=[];if(!S.rpkgs)S.rpkgs=[];
 /* v24 → v25: «Tu personal de X» (grupo) se separa en un producto por perfil */
 if(S.rprods.some(x=>x.kind==="staff"&&!x.n)){const old=S.rprods.filter(x=>x.kind==="staff"&&!x.n);S.rprods=S.rprods.filter(x=>!old.includes(x));old.forEach(o=>o.labor.forEach(r=>{if(!ruStaffBy(r.n))S.rprods.push(ruNewStaff(r,o.dims[0]));}));}
 /* v25 → v26: tarifas por perfil, sin mínimo; «Solo personal» deja de ser forma de contratar; un solo precio de insumos */
 S.rprods.forEach(x=>{(x.labor||[]).forEach(r=>{if(!r.tars)r.tars=[{p:r.p||"",u:r.u||""}];if(r.xu==="por turno (5 h)")r.xu="por turno de 5 h";if(!r.xu)r.xu="por hora";ruSyncPU(r);});
  if(x.kind==="prod"){if(!x.tar.i){const s=+x.tar.rent.p?x.tar.rent:+x.tar.full.p?x.tar.full:x.tar.rent;x.tar.i={p:s.p,u:s.u,q:s.q||""};}
   if(x.tw.includes("labor")){x.tw=x.tw.filter(w=>w!=="labor");if(!x.tw.includes("full"))x.tw.push("full");}x.tw=["rent","full"].filter(w=>x.tw.includes(w));
   if(!x.courses)x.courses=ruTimed(x)&&x.dishes.length?x.dishes.map((d,i)=>({n:ruCourseN(i),d:[d]})):[{n:ruCourseN(0),d:ruTimed(x)?[]:[...x.dishes]}];}});
 (S.rpkgs||[]).forEach(k=>{k.items=k.items.filter(r=>ruRefW(r)!=="labor");k.tw=["full"];if(k.sugAt===undefined){k.sugAt=Math.round(ruSug(k)*(k._demoOld?0.94:1));delete k._demoOld;}});
 if(!S.invites)S.invites=[];if(!S.askNo)S.askNo={};
 if(!S.rsel||!RU_T.has(S.rsel[0]))S.rsel=["Catering","Bebidas","Barra","Sin alcohol"];}
const ruLpol=()=>({night:true,nightPct:"50",ride:false,rideFee:"",meal:true,uniform:true});
function ruBlankMore(){return{cov:{same:true,zones:[{state:"",all:false,munis:[]}]},photos:[],ext:[],dl:[],dlOpen:-1,dlx:{dl:[],dlOpen:-1},labor:[],lpol:ruLpol(),min:blankMin(),promo:blankPromo()};}
const RU_LU=[["Por turno (5 h)","por turno de 5 h"],["Por hora","por hora"],["Por evento","por evento"],["Por día","por día"]];
const ruLabTot=p=>(p.labor||[]).reduce((a,r)=>a+ruProfCost(r,p.lpol)*(+r.q||1),0);
/* tiempos: banquete o formato «por tiempos» */
const ruTimed=p=>p.dims&&p.dims[1]==="Alimentos"&&(p.dims[2]==="Banquete"||/tiempo/i.test(p.dims[3]||""));
const RU_ORD=["Primer","Segundo","Tercer","Cuarto","Quinto","Sexto","Séptimo"];
const ruCourseN=i=>(RU_ORD[i]||`${i+1}.º`)+" tiempo";
const ruDishes=p=>p.courses?p.courses.flatMap(c=>c.d):p.dishes||[];
function ruName(dims,otro){const lc=x=>x.charAt(0).toLowerCase()+x.slice(1),gen=["Alimentos","Bebidas","Otro","Personal independiente"].includes(dims[1])||nrm(dims[2]).includes(nrm(dims[1]).slice(0,5));
 const base=gen?dims[2]:`${dims[1]} ${dims[2]}`;
 return dims[1]==="Personal independiente"?dims[3]:dims[2]==="Otro"?dims[1]:dims[3]==="Otro"?(otro?`${base} ${lc(otro)}`:base):(nrm(dims[3])===nrm(dims[2])?base:`${base} ${lc(dims[3])}`);}
function ruProd(dims,otro){const [u]=RU_U[dims.join("|")]||["Por evento"],st=RU.staff[dims[0]]||[];
 return Object.assign({id:"p"+Date.now().toString(36)+Math.random().toString(36).slice(2,5),kind:"prod",dims,otro:otro||"",name:ruName(dims,otro),dishes:[],ins:[],crew:(RU.pre[dims[0]]||[]).filter(n=>st.includes(n)).map(n=>({n,q:"1"})),pax:"",tw:[],tar:ruBlankT(u),courses:[{n:ruCourseN(0),d:[]}]},ruBlankMore());}
function ruDemo(){const a=ruProd(["Catering","Alimentos","Banquete","Por tiempos"]);Object.assign(a,{name:"Menú Oro",pax:"100",dishes:["Crema de elote","Mole poblano con pollo","Flan napolitano"],courses:[{n:"Primer tiempo",d:["Crema de elote"]},{n:"Segundo tiempo",d:["Mole poblano con pollo","Arroz rojo"]},{n:"Postre",d:["Flan napolitano"]}],ins:["Platos","Cubiertos","Mantelería","Servilletas de tela"],crew:[{n:"Mesero",q:"7"},{n:"Cocinero",q:"2"},{n:"Capitán de meseros",q:"1"}],tw:["rent","full"],labor:[{n:"Mesero",q:"7",tars:[{p:"1000",u:"Por turno (5 h)"},{p:"250",u:"Por hora"}],xh:"200",xu:"por hora"},{n:"Cocinero",q:"2",tars:[{p:"1200",u:"Por turno (5 h)"}],xh:"250",xu:"por hora"},{n:"Capitán de meseros",q:"1",tars:[{p:"1400",u:"Por turno (5 h)"}],xh:"280",xu:"por hora"}],ext:[{c:"Hora extra",p:"1500",u:"por hora"}],dlx:{dlOpen:-1,dl:[Object.assign(blankDl("Recolección en establecimiento"),{cobra:false,ph:"Lun a sáb de 9:00 a 18:00"}),Object.assign(blankDl("Envío a domicilio"),{cobra:true,u:"Por kilómetro",rate:"15",conds:[{c:"Distancia máxima",v:"30"}]})]},photos:[{url:samplePic("🍽️","#FFB3D9","#7B2FF7",1200,900),name:"menu-oro.jpg",issues:[],before:812000,after:214000}]});a.tar.i={p:"480",u:"Por persona",q:""};a.lpol.ride=true;a.lpol.rideFee="150";a.id="pdemo1";
 const b=ruProd(["Catering","Bebidas","Barra","Sin alcohol"]);Object.assign(b,{pax:"100",ins:["Vasos","Hielo","Popotes"],crew:[{n:"Bartender",q:"2"}],tw:["full"],labor:[{n:"Bartender",q:"2",tars:[{p:"1500",u:"Por turno (5 h)"},{p:"350",u:"Por hora"}],xh:"320",xu:"por hora"}]});b.tar.i={p:"60",u:"Por persona",q:""};b.id="pdemo2";
 const c=ruProd(["Catering","Postres y dulces","Mesa de dulces","Temática"]);Object.assign(c,{name:"Mesa de dulces temática",pax:"50",ins:["Charolas","Bases de pastel","Mantelería","Decoración de mesa"],crew:[],tw:["rent"],dlx:{dlOpen:-1,dl:[Object.assign(blankDl("Envío a domicilio"),{cobra:true,u:"Por kilómetro",rate:"12",conds:[{c:"Entrega gratuita desde",v:"5000"}]}),Object.assign(blankDl("Recolección en establecimiento"),{cobra:false,ph:"Lun a sáb de 9:00 a 18:00"})]},promo:{has:true,what:"10% de descuento entre semana",terms:"De lunes a jueves",until:"2026-12-15"},min:{has:true,qty:"30",unit:"personas"},photos:[{url:samplePic("🍭","#D6338A","#7B2CBF",1200,900),name:"mesa.jpg",issues:[],before:640000,after:198000}]});c.tar.i={p:"3500",u:"Por evento",q:""};c.id="pdemo3";
 const P={id:"kdemo1",kind:"pkg",items:["pdemo1|full","pdemo2|full"],qty:{},name:"Paquete Boda Oro",dishes:[],ins:["Centros de mesa"],crew:[{n:"Mesero",q:"7"},{n:"Bartender",q:"2"}],pax:"100",tw:["full"],tar:ruBlankT("Por persona")};Object.assign(P,ruBlankMore());P.tar.full.p="720";P._demoOld=true;
 a.emb=1;b.emb=2;c.emb=3;
 [a,b].forEach(x=>x.labor.forEach(ruSyncPU));const st=[...a.labor,...b.labor].map(r=>ruNewStaff(r,"Catering"));
 const V={id:"kdemo2",kind:"pkg",items:["venue","pdemo3|rent","st-mesero"],qty:{"st-mesero":"4"},name:"Fiesta en la Terraza",dishes:[],ins:["Mantelería","Centros de mesa"],crew:[{n:"Mesero",q:"4"}],pax:"60",tw:["full"],tar:ruBlankT("Por persona")};Object.assign(V,ruBlankMore());V.tar.full.p="390";
 c.cov={same:false,zones:[{state:"Ciudad de México",all:true,munis:[]}]};
 return{prods:[a,b,c,...st],pkgs:[P,V],vin:{"pdemo1|full":{on:true,p:"440"},"pdemo1|rent":{on:true,p:"440"},"pdemo2|full":{on:true,p:""},"pdemo3|rent":{on:true,p:"3000"},"st-mesero":{on:true,p:""},"st-bartender":{on:false,p:""}}};}
function ruZInter(A,B){const out=[];if(A.some(z=>z.state==="__nac"))return B.map(z=>({...z,munis:[...z.munis]}));if(B.some(z=>z.state==="__nac"))return A.map(z=>({...z,munis:[...z.munis]}));
 A.forEach(z=>{const w=B.find(x=>x.state===z.state);if(!w||!z.state)return;if(z.all&&w.all)out.push({state:z.state,all:true,munis:[]});else{const m=z.all?w.munis:w.all?z.munis:z.munis.filter(x=>w.munis.includes(x));if(m.length)out.push({state:z.state,all:false,munis:[...m]});}});return out;}
function ruZones(p){if(!p.cov||p.cov.same){if(p.kind==="pkg"){const L=p.items.map(ruById).filter(x=>x&&x.kind!=="venue"&&x.kind!=="planner").map(ruZones);return L.length?L.reduce(ruZInter):S.svcZones;}return S.svcZones;}return p.cov.zones;}
const ruById=id=>{id=String(id||"").split("|")[0];return id==="venue"?ruVenueItem():id.startsWith("pl:")?ruPlanners().find(x=>x.id===id):(S.rprods||[]).find(x=>x.id===id);};
const ruRefW=r=>String(r).split("|")[1]||"";
/* v25 · el venue entra al combinador como una pieza más */
function ruVenueItem(){const v=S.venue;if(!S.types||!S.types.venue||!v||!filled(v.name)||!(+v.seated>0))return null;return{id:"venue",kind:"venue",dims:["Venue","","",""],name:v.name||"Tu venue",crew:[],dishes:[],ins:[],tw:["venue"],pax:v.seated||"",cov:{same:true}};}
function ruVenueTot(pax){const v=S.venue,r=v&&v.rent,pr=+(r&&r.price)||0;if(!pr)return 0;pax=+pax||+v.seated||0;let t=r.per==="hora"?pr*(+v.hoursIncl||5):r.per==="persona"?pr*pax:pr;if(r.per!=="persona"&&+r.upTo>0&&pax>+r.upTo)t+=(pax-r.upTo)*(+r.perExtraGuest||0);return t;}
const ruFN={rent:"📦 Servicio / producto sin staff",full:"🙋 Servicio / producto con staff",labor:"🙋 Staff"};
function ruItemName(ref,P){const x=ruById(ref),w=ruRefW(ref),q=P&&P.qty&&P.qty[ref];if(!x)return"(ya no está disponible)";return(x.kind==="venue"?"🏡 ":x.kind==="planner"?"🧭 ":"")+(x.kind==="staff"&&+q>1?q+" × ":"")+x.name+(w&&x.kind==="prod"?" · "+ruFN[w].slice(3).toLowerCase():"");}
/* precio en el venue: el proveedor lo pone aparte (no es descuento) */
const vnIn=ref=>{if(ruRefW(ref)==="labor")return null;const v=S.venue,e=v&&v.svcIn&&v.svcIn[ref];return e&&e.on!==false&&+e.p>0?e:null;};
function ruWithPrice(x,w,pr){const y=JSON.parse(JSON.stringify(x));if(x.kind==="staff"){y.labor.forEach(r=>{r.tars[0].p=pr;ruSyncPU(r);});}else if(x.kind==="pkg")y.tar.full.p=pr;else y.tar.i.p=pr;return y;}
function ruItemTot(ref,P){const x=ruById(ref);if(!x)return 0;const pax=+P.pax||+x.pax||0,vin=P.items.includes("venue")&&vnIn(ref);
 if(x.kind==="venue")return ruVenueTot(pax);
 if(x.kind==="planner")return ruPlanTot(x.fees,pax,P.items.filter(r=>!String(r).startsWith("pl:")).reduce((a,r)=>a+ruItemTot(r,P),0));
 if(x.kind==="staff"){const y=vin?ruWithPrice(x,"labor",vin.p):x;return ruProfCost(y.labor[0],y.lpol)*(+(P.qty&&P.qty[ref])||1);}
 const w=ruRefW(ref)||x.tw[0];if(!w)return 0;const y=vin?ruWithPrice(x,w,vin.p):x,r=ruTotal(Object.assign({},y,{pax:w==="labor"?y.pax:pax||y.pax}),w);return r?r.tot:0;}
const ruCats=p=>p.kind==="pkg"?[...new Set(p.items.map(id=>(ruById(id)||{dims:["Catering"]}).dims[0]).filter(c=>c!=="Venue"&&c!=="Event planner"))]:[p.dims[0]];
const ruFood=p=>p.kind==="pkg"?p.items.some(id=>(ruById(id)||{dims:[]}).dims[1]==="Alimentos"):p.dims[1]==="Alimentos";
function ruInsTot(p){const t=p.tar.i||{},pr=+t.p||0,pax=+p.pax||0;if(!pr)return 0;return t.u==="Por persona"?pr*pax:RU_FIXED.includes(t.u)?pr:pr*(+t.q||pax);}
function ruTotal(p,w){const pax=+p.pax||0;
 if(p.kind==="pkg"){const t=p.tar.full,pr=+t.p||0;if(!pr)return null;const tot=t.u==="Por persona"?pr*pax:RU_FIXED.includes(t.u)?pr:pr*(+t.q||1);return{tot,pp:pax?tot/pax:null};}
 if(p.kind==="staff"){const tot=ruProfCost(p.labor[0],p.lpol);return tot?{tot,pp:null}:null;}
 const b=ruInsTot(p);if(!b)return null;const tot=w==="full"?b+ruLabTot(p):b;return{tot,pp:pax?tot/pax:null};}
const ruInsOk=p=>{const t=p.tar.i||{};return +t.p>0&&!!t.u;};
const ruTarOk=(p,w)=>ruInsOk(p)&&(w!=="full"||(p.labor.length>0&&p.labor.every(ruTarsOk)))&&(w!=="rent"||(p.dlx.dl.length>0&&p.dlx.dl.every(dlOk)));
const ruSug=p=>p.items.reduce((a,ref)=>a+ruItemTot(ref,p),0);
const ruMoney=n=>{n=+n||0;return n>0&&n<100&&Math.round(n)!==n?"$"+n.toLocaleString("es-MX",{minimumFractionDigits:2,maximumFractionDigits:2}):money(Math.round(n));};
const ruLink=p=>`hayquevernos.com/${slug(S.biz.name)}#${p.kind==="pkg"?"paquete":"producto"}-${slug(p.name||"sin-nombre")}`;
function ruOk(p){if(!p.cov)p.cov={same:true,zones:[{state:"",all:false,munis:[]}]};const tail=p.ext.every(e=>!filled(e.c)||+e.p>0)&&(p.min.has!==true||minOk(p.min))&&(p.promo.has!==true||promoOk(p.promo))&&(p.cov.same||zonesOk(p.cov.zones));
 if(p.kind==="staff")return ruTarsOk(p.labor[0])&&tail;
 if(p.kind==="pkg")return filled(p.name)&&+p.pax>0&&+p.tar.full.p>0&&tail;
 return filled(p.name)&&+p.pax>0&&p.tw.length>0&&p.tw.every(w=>ruTarOk(p,w))&&tail;}
function ruMiss(p){const m=[];
 if(p.kind==="staff"){if(!ruTarsOk(p.labor[0]))m.push("precio y forma de cobro");}
 else{if(!filled(p.name))m.push("nombre");
  if(p.kind==="pkg"){if(!(+p.tar.full.p>0))m.push("precio del paquete");}
  else{if(!p.tw.length)m.push("cómo entregas y cobras");else{if(!ruInsOk(p))m.push("precio del servicio");if(p.tw.includes("full")&&!(p.labor.length&&p.labor.every(ruTarsOk)))m.push("precio y forma de cobro de tu staff");if(p.tw.includes("rent")&&!p.dlx.dl.length)m.push("cómo entregas sin staff");else if(p.tw.includes("rent")&&!p.dlx.dl.every(dlOk))m.push("entrega por completar");}}
  if(!(+p.pax>0))m.push("para cuántas personas alcanza");}
 if(p.cov&&!p.cov.same&&!zonesOk(p.cov.zones))m.push("zona");
 if(!p.ext.every(e=>!filled(e.c)||+e.p>0))m.push("precio de cada extra");if(p.min.has===true&&!minOk(p.min))m.push("mínimo de compra");if(p.promo.has===true&&!promoOk(p.promo))m.push("promoción");return m;}
/* ---------- ruleta ---------- */
function ruMachineHtml(){return`<section class="ru-m" aria-label="Arma tu servicio">
 <div class="ru-mh"><img class="ru-masc" id="ruMasc" alt=""><div class="ru-mt"><b id="ruTit">Arma tu servicio</b><span>Desliza y alinea en verde los factores para configurar un servicio.</span></div></div>
 <div class="ru-reels" id="ruReels">${RU_LAB.map((l,i)=>`<div class="ru-row"><div class="ru-lab">${i+1} · ${l}<span id="ruCnt${i}"></span></div><div class="ru-wrap"><button class="ru-ar l" type="button" data-i="${i}" data-d="-1" aria-label="Anterior">‹</button><div class="ru-reel" id="ruReel${i}" tabindex="0" role="listbox" aria-label="${l}"></div><button class="ru-ar r" type="button" data-i="${i}" data-d="1" aria-label="Siguiente">›</button></div></div>`).join("")}</div>
 <div class="ru-combo"><span class="ru-unit" id="ruUnit" hidden></span><div id="ruOtro" hidden><input id="ruOtroIn" type="text" placeholder="Escribe cuál es (ej. barra de mezcal)" aria-label="Escribe cuál es"></div>
 <button class="btn cta ru-save" id="ruSave" type="button">Guardar servicio ✓</button></div></section>`;}
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
 const add=v=>{const P=String(v||"").split(",").map(x=>x.trim()).filter(Boolean);if(!P.length)return;P.forEach(v=>{if(onAdd)onAdd(v);else if(!L.some(x=>nrm(x)===nrm(v)))L.push(v);});redraw(id);};
 w.querySelectorAll("[data-x]").forEach(b=>b.onclick=()=>{L.splice(+b.dataset.x,1);redraw(id);});
 const show=()=>{const v=nrm(inp.value).trim();if(!v){sg.hidden=true;return;}res=src().filter(x=>nrm(x).includes(v)&&!L.includes(x)).sort((a,b)=>(nrm(a).startsWith(v)?0:1)-(nrm(b).startsWith(v)?0:1)).slice(0,6);on=0;
  sg.innerHTML=res.map((x,ix)=>`<button type="button" class="${ix?"":"on"}">${esc(x)}</button>`).join("");sg.hidden=!res.length;sg.querySelectorAll("button").forEach((b,ix)=>b.onmousedown=e=>{e.preventDefault();add(res[ix]);});};
 inp.oninput=show;inp.onblur=()=>setTimeout(()=>{sg.hidden=true;},120);
 inp.onkeydown=e=>{if((e.key==="ArrowDown"||e.key==="ArrowUp")&&res.length){e.preventDefault();on=(on+(e.key==="ArrowDown"?1:-1)+res.length)%res.length;sg.querySelectorAll("button").forEach((b,ix)=>b.classList.toggle("on",ix===on));}
  if(e.key==="Enter"||e.key===","){e.preventDefault();add(!sg.hidden&&res[on]?res[on]:inp.value);}if(e.key==="Backspace"&&!inp.value&&L.length&&!onAdd){L.pop();redraw(id);}};}
/* ---------- ficha de identidad ---------- */
let RU_EX={s:"18:00",e:"02:00"};
function ruExHtml(p){const s=ruHr(RU_EX.s),e=ruHr(RU_EX.e),H=(e<=s?e+24:e)-s,pol=p.lpol,rows=p.labor.filter(ruTarsOk);if(!rows.length)return"";let sum=0;
 const L=rows.map(r=>{const q=ruProfQuote(r,pol,s,e),n=p.kind==="staff"?1:(+r.q||1);sum+=q.tot*n;return`<div class="ru-exr"><b>${n>1?n+" × ":""}${esc(r.n)}</b>${q.lines.map(l=>`<span>${esc(l)}</span>`).join("")}<span class="ru-ext">${money(q.tot)}${n>1?` c/u · ${money(q.tot*n)}`:""}</span></div>`;}).join("");
 const notes=[pol.ride&&e<=s?`🚕 El transporte de regreso lo cubre el anfitrión${+pol.rideFee>0?` (${money(pol.rideFee)} por persona)`:""}`:"",pol.meal&&H>5?"🍽️ Alimentos para el staff (fiesta de más de 5 h)":"",pol.uniform?"👔 Uniforme incluido":""].filter(Boolean);
 return`<div class="ru-host ru-exh"><b>👀 Así lo verá el anfitrión</b><div class="ru-exq"><span>Si su fiesta es de</span><input type="time" id="ruExS" value="${RU_EX.s}" aria-label="Empieza"><span>a</span><input type="time" id="ruExE" value="${RU_EX.e}" aria-label="Termina"><span>(${H} h)</span></div>${L}${p.kind==="staff"?"":`<div class="ru-exr ru-exsum"><b>Tu staff en esa fiesta</b><span class="ru-ext">${money(sum)}</span></div>`}${notes.map(n=>`<span class="ru-exn">${esc(n)}</span>`).join("")}<span class="hint">Usamos la tarifa que más le conviene al anfitrión.</span></div>`;}
function ruHost(p){if(p.kind==="staff")return ruExHtml(p);const pax=+p.pax;if(!pax||!p.tw.length)return"";const L=p.tw.map(w=>{const r=ruTotal(p,w);return r?`<div class="ru-hr"><span class="ru-hl">${RU_TL[w][0]}</span><span class="ru-tot">${ruMoney(r.tot)}</span><small class="ru-ppx">total del evento · <b>${ruMoney(r.pp)}</b> por persona</small></div>`:"";}).filter(Boolean);
 return L.length?`<div class="ru-host"><b>👀 Así lo verá el anfitrión</b><span class="hint">En una fiesta de ${pax} personas${p.tw.includes("full")?" (con staff: fiesta de 5 h)":""}:</span><div class="ru-hrows">${L.join("")}</div></div>`:"";}
/* precio de los insumos: uno solo para «con» y «sin» personal */
function ruInsHtml(p){const t=p.tar.i,cnt=t.u&&!RU_FIXED.includes(t.u);
 return`<div class="ru-tg" data-w="ins"><b>💲 Precio del servicio</b><span class="hint">Es el mismo con o sin staff; el staff se cobra aparte.</span><div class="ru-line ru-l3"><label class="ru-f"><span class="ru-fi"><i>$</i><input type="number" min="0" inputmode="decimal" id="ruIp" class="${MISS(+t.p>0)}" value="${esc(t.p)}" placeholder="0" aria-label="Precio del servicio"></span></label>
  <label class="ru-f ru-fsel"><span class="ru-fi"><select id="ruIu" class="${t.u?"":"ph"}${MISS(!!t.u)}" aria-label="Unidad de medida"><option value="" disabled ${t.u?"":"selected"} hidden>por persona</option>${RU_UNITS.map(u=>`<option ${t.u===u?"selected":""}>${u}</option>`).join("")}</select></span></label>
  ${cnt?`<label class="ru-f"><span class="ru-fi"><input type="number" min="1" inputmode="numeric" id="ruIq" value="${esc(t.q)}" placeholder="${esc(p.pax||"#")}" aria-label="¿Cuántas ${esc(ruNoun(t.u))}?"><i>${esc(ruNoun(t.u))}</i></span></label>`:"<span></span>"}</div></div>`;}
function ruPkgPriceHtml(p){const t=p.tar.full,cnt=!RU_FIXED.includes(t.u);
 return`<div class="ru-tg" data-w="full"><b>💲 Precio del paquete</b><div class="row"><label class="ru-money">$<input type="number" min="0" inputmode="decimal" data-tp="full" class="${MISS(+t.p>0)}" value="${esc(t.p)}" placeholder="precio" aria-label="Precio del paquete"></label>
  <select data-tu="full" aria-label="Unidad">${RU_UNITS.map(u=>`<option ${t.u===u?"selected":""}>${u}</option>`).join("")}</select>
  ${cnt?`<label class="ru-q">¿Cuántas ${esc(ruNoun(t.u))}? <input type="number" min="1" data-tq="full" class="${MISS(+t.q>0)}" value="${esc(t.q)}" placeholder="#"></label>`:""}</div></div>`;}
function ruLaborHtml(p,staff){const sk=p.kind==="staff",rest=sk?[]:[...new Set(staff)].filter(n=>!p.labor.some(r=>r.n===n)),L=p.lpol;
 const pill=(k,on,txt,extra)=>`<span class="ru-pill" aria-pressed="${on}"><button type="button" class="ru-pt" data-k="${k}" aria-pressed="${on}">${on?"✓ ":""}${txt}</button>${on&&extra?extra:""}</span>`;
 const sel=(cls,val,opts,ph,lab)=>`<label class="ru-f ru-fsel"><span class="ru-fi"><select class="${cls}${val?"":" ph"}" aria-label="${esc(lab)}"><option value="" disabled ${val?"":"selected"} hidden>${ph}</option>${opts.map(([v,t])=>`<option value="${v}" ${val===v?"selected":""}>${t}</option>`).join("")}</select></span></label>`;
 const LU=RU_LU.map(([u,t])=>[u,ruShortU(t)]),XU=RU_XU.map(t=>[t,ruShortU(t)]);
 return`<div class="ru-tg ru-labr" data-w="labor"><b>${sk?"🙋 Precio de este perfil":"🙋 Precio del staff"}</b><span class="hint">${sk?"Lo que cobra una persona. Puedes darle varias formas de cobro; si lo cambias, se actualiza en todos tus productos.":"Cuántos mandas y cuánto cobra cada uno. Si ya lo usaste antes, lo llenamos por ti. Con staff, la entrega y el montaje van incluidos. Cada perfil se vuelve un producto que el anfitrión puede contratar solo."}</span>
  <div class="ru-lt">${p.labor.map((r,ix)=>{const known=!sk&&ruStaffBy(r.n)&&ruTarsOk(ruStaffBy(r.n).labor[0]);return`<div class="ru-lr${sk?" one":""}" data-ix="${ix}"><div class="ru-lnr"><b class="ru-ln">${esc(r.n)}</b>${known?`<span class="ru-known" title="Precio guardado en Tu staff">🔁<span> guardado</span></span>`:""}${sk?"":`<button type="button" class="link bad ru-lrm" aria-label="Quitar ${esc(r.n)}">✕</button>`}</div>
   <div class="ru-lbody">${r.tars.map((t,j)=>`<div class="ru-line${sk?" ru-l2":""}" data-j="${j}">${sk?"":j===0?`<label class="ru-f ru-fq"><span class="ru-fi"><input type="number" min="1" inputmode="numeric" class="ru-lq" value="${esc(r.q)}" placeholder="1" aria-label="¿Cuántos ${esc(r.n)}?"></span></label>`:`<span class="ru-or">o</span>`}
     <label class="ru-f"><span class="ru-fi"><i>$</i><input type="number" min="0" inputmode="decimal" class="ru-tp${MISS(+t.p>0)}" value="${esc(t.p)}" placeholder="0" aria-label="Precio de ${esc(r.n)}"></span></label>
     ${sel("ru-tu"+MISS(!!t.u),t.u,LU,"turno 5 h","Unidad de medida de "+r.n)}${j>0?`<button type="button" class="link bad ru-trm" aria-label="Quitar esta forma de cobro">✕</button>`:""}</div>`).join("")}
    ${(()=>{const tu=r.tars.find(t=>t.u==="Por turno (5 h)"&&+t.p>0),th=r.tars.find(t=>t.u==="Por hora"&&+t.p>0);return tu&&th&&th.p*5<+tu.p?`<span class="ru-warn">💡 Tu tarifa por hora sale más barata que tu turno de 5 h (5 × ${money(th.p)} = ${money(th.p*5)} contra ${money(tu.p)}). ¿Es correcto?</span>`:"";})()}
    <button type="button" class="link ru-addt">＋ Otra forma de cobrarlo</button>
    <div class="ru-line ru-lx${sk?" ru-l2":""}">${sk?"":`<span class="ru-xt">Extra</span>`}<label class="ru-f"><span class="ru-fi"><i>$</i><input type="number" min="0" inputmode="decimal" class="ru-lx" value="${esc(r.xh)}" placeholder="0" aria-label="Precio extra de ${esc(r.n)}"></span></label>${sel("ru-lxu",r.xu,XU,"hora","Unidad del extra de "+r.n)}${sk?`<span class="ru-xt">Extra</span>`:""}</div></div></div>`;}).join("")||`<span class="hint">Agrega al menos un perfil.</span>`}</div>
  ${sk?"":`<div class="ru-add"><span class="ru-sl">＋ Sumar perfil</span><div class="ru-addc">${rest.map(n=>`<button type="button" class="chip ru-lab-c" data-n="${esc(n)}">＋ ${esc(n)}${ruStaffBy(n)&&ruTarsOk(ruStaffBy(n).labor[0])?` <small>${money(ruStaffBy(n).labor[0].tars[0].p)}</small>`:""}</button>`).join("")}<button type="button" class="chip new ru-lab-o">✏️ Otro</button></div><div class="ru-labnew" hidden>${ruTags("labNew",[],"Otro perfil: escribe y Enter")}</div></div>`}
  <div class="ru-pols"><span class="ru-sl">📋 Tus políticas</span><div class="ru-pils">
   ${pill("night",L.night,"🌙 Recargo después de las 12 a.m.",`<label class="ru-pin">+<input type="number" min="0" class="ru-p-pct" value="${esc(L.nightPct)}" aria-label="Recargo nocturno">%</label>`)}
   ${pill("ride",L.ride,"🚕 Transporte de regreso lo cubre el anfitrión",`<label class="ru-pin">$<input type="number" min="0" class="ru-p-fee" value="${esc(L.rideFee)}" placeholder="0" aria-label="Transporte por persona">c/u</label>`)}
   ${pill("meal",L.meal,"🍽️ Alimentos para el staff (+5 h)")}
   ${pill("uniform",L.uniform,"👔 Uniforme incluido")}</div>
   <span class="hint">El tiempo cuenta desde que tu staff llega. Viáticos fuera de zona se acuerdan.</span></div>
  ${sk?"":`<div id="ruExBox">${ruExHtml(p)}</div>`}</div>`;}
function ruIdentHtml(p){const sk=p.kind==="staff",pk=p.kind==="pkg",staff=[...new Set(ruCats(p).flatMap(c=>RU.staff[c]||[]))],names=[...new Set([...staff,...p.crew.map(r=>r.n)])],k="ru"+(pk?"k":"p"),sug=pk?ruSug(p):0;
 if(pk&&!p.qty)p.qty={};const head=pk?`<span class="ru-pkb">🎁 Paquete</span><input id="ruName" class="ru-title${MISS(filled(p.name))}" value="${esc(p.name)}" placeholder="${pk?"Asígnale un nombre a este paquete":"Asígnale un nombre a este servicio"}" aria-label="Nombre"><div class="ru-crumbs ru-kits">${p.items.map(ref=>{const x=ruById(ref);return x&&x.kind==="staff"?`<label class="ru-kq"><input type="number" min="1" inputmode="numeric" data-kq="${esc(ref)}" value="${esc(p.qty[ref]||"1")}" aria-label="¿Cuántos ${esc(x.name)}?"> × ${esc(x.name)}</label>`:`<span>${esc(ruItemName(ref,p))}</span>`;}).join("")}</div><span class="hint">Empieza en blanco: el paquete lleva su propio nombre, detalles y precio. Guardamos de qué productos sale.</span>`
  :sk?`<span class="ru-stb">🙋 Tu staff</span><h3>${esc(p.name)}</h3><span class="hint">Es un producto independiente: el anfitrión lo puede contratar solo y tú lo sumas a tus paquetes las veces que quieras.</span>`
  :`<div class="ru-crumbs">${p.dims.map(d=>`<span>${esc(d)}</span>`).join("")}${p.otro?`<span>${esc(p.otro)}</span>`:""}</div><input id="ruName" class="ru-title${MISS(filled(p.name))}" value="${esc(p.name)}" placeholder="${pk?"Asígnale un nombre a este paquete":"Asígnale un nombre a este servicio"}" aria-label="Nombre">`;
 return`${head}
 ${sk?ruLaborHtml(p,staff):pk?`<div class="field ru-inc"><span class="lbl">¿Qué incluye?</span><span class="ru-sl">🧺 Además incluye <span class="opt">opcional</span></span>${ruTags("ins",p.ins,"Ej. centros de mesa, mantelería")}</div>
 <div class="field">${sug?`<div class="ru-sug">💡 Tus productos suman <b>${ruMoney(sug)}</b>${+p.pax?` · ${ruMoney(sug/ +p.pax)} por persona`:""}<button type="button" class="link" id="ruUseSug">Usar como precio</button></div>`:""}${ruPkgPriceHtml(p)}</div>`
 :`<div class="field ru-inc"><span class="lbl">¿Qué incluye?</span>
  ${ruFood(p)?(ruTimed(p)?`<span class="ru-sl">🍴 Platillos por tiempo <span class="opt">escribe y te sugerimos</span></span>
   ${p.courses.map((c,i)=>`<div class="ru-course" data-i="${i}"><div class="ru-ch"><input type="text" class="ru-cn" value="${esc(c.n)}" aria-label="Nombre del tiempo">${p.courses.length>1?`<button type="button" class="link bad ru-crm" aria-label="Quitar ${esc(c.n)}">✕</button>`:""}</div>${ruTags("course"+i,c.d,i===0?"Ej. crema de elote, sopa de fideo":"Escribe y te sugerimos")}</div>`).join("")}
   <span class="hint ru-comma">Separa los platillos con coma o Enter.</span><button type="button" class="link ru-cadd" style="justify-self:start">＋ Agregar tiempo</button>`
   :`<span class="ru-sl">🍴 Platillos <span class="opt">escribe y te sugerimos</span></span>${ruTags("course0",p.courses[0].d,"Ej. tacos al pastor, quesadillas")}<span class="hint ru-comma">Separa los platillos con coma o Enter.</span>`):""}
  <span class="ru-sl">🧺 Incluye</span>${ruTags("ins",p.ins,"Ej. platos, hielo, mantelería")}<span class="hint ru-comma">Sepáralos con coma o Enter.</span></div>
 <div class="field"><span class="lbl">🚚 ¿Cómo entregas y cobras? <span class="opt">elige una o las dos</span></span>
  <div class="ru-tsel ru-tsel2${MISS(p.tw.length>0)}">${["rent","full"].map(w=>`<button type="button" class="ru-tsb" data-w="${w}" aria-pressed="${p.tw.includes(w)}"><b>${RU_TL[w][0]}</b><small>${RU_TL[w][1]}</small></button>`).join("")}</div>
  ${p.tw.length?ruInsHtml(p):""}
  ${p.tw.includes("full")?`<div class="ru-stw" data-w="full">${ruLaborHtml(p,staff)}</div>`:""}
  ${p.tw.includes("rent")?`<div class="ru-tg ru-dlw" data-w="rent"><b>¿Cómo entregas?</b>${dlSecHtml(p.dlx,k+"dlx","rt","¿Cómo entregas?")}</div>`:""}</div>`}
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
 (p.courses||[]).forEach((c,i)=>ruBindTags(box,"course"+i,c.d,()=>RU_DISHES,null,rd));
 box.querySelectorAll(".ru-course").forEach(C=>{const c=p.courses[+C.dataset.i];C.querySelector(".ru-cn").oninput=e=>{c.n=e.target.value;};const x=C.querySelector(".ru-crm");if(x)x.onclick=()=>{p.courses.splice(+C.dataset.i,1);ruDrawIdent();};});
 const ca=box.querySelector(".ru-cadd");if(ca)ca.onclick=()=>{p.courses.push({n:ruCourseN(p.courses.length),d:[]});ruDrawIdent(false,"course"+(p.courses.length-1));};
 const ip=$("ruIp"),iu=$("ruIu"),iq=$("ruIq");if(ip)ip.oninput=e=>{p.tar.i.p=e.target.value;live();};if(iu)iu.onchange=e=>{p.tar.i.u=e.target.value;ruDrawIdent();};if(iq)iq.oninput=e=>{p.tar.i.q=e.target.value;live();};ruBindTags(box,"ins",p.ins,()=>ruIns(ruCats(p)[0]),null,rd);
 ruBindTags(box,"crewNew",[],()=>[...new Set(Object.values(RU.staff).flat())],v=>{if(!p.crew.some(r=>nrm(r.n)===nrm(v)))p.crew.push({n:v,q:"1"});},rd);
 ruBindTags(box,"ext",[],()=>RU_EXTRAS.filter(x=>!p.ext.some(e=>e.c===x)),v=>{if(!p.ext.some(e=>nrm(e.c)===nrm(v)))p.ext.push({c:v,p:"",u:ruExU(v)});setTimeout(()=>{const l=[...box.querySelectorAll(".ru-exp")].pop();l&&l.focus({preventScroll:true});},0);},rd);
 
 box.querySelectorAll("[data-cq]").forEach(x=>x.oninput=e=>{p.crew[+x.dataset.cq].q=e.target.value;});
 box.querySelectorAll(".ru-tsb").forEach(b=>b.onclick=()=>{const w=b.dataset.w;p.tw=p.tw.includes(w)?p.tw.filter(x=>x!==w):["rent","full"].filter(x=>x===w||p.tw.includes(x));
  if(w==="full"&&p.tw.includes("full")&&!p.labor.length)p.labor=p.crew.map(r=>ruLabRow(r.n,r.q));if(!p.tar.i.u)p.tar.i.u=(RU_U[p.dims.join("|")]||["Por persona"])[0];ruDrawIdent();});
 const bindEx=()=>{const s=$("ruExS"),e=$("ruExE");if(s)s.onchange=x=>{RU_EX.s=x.target.value||"18:00";live();};if(e)e.onchange=x=>{RU_EX.e=x.target.value||"02:00";live();};};
 const live=()=>{const h=$("ruHost");if(h)h.innerHTML=ruHost(p);const x=$("ruExBox");if(x)x.innerHTML=ruExHtml(p);bindEx();};bindEx();
 box.querySelectorAll("[data-tp]").forEach(x=>x.oninput=e=>{p.tar[x.dataset.tp].p=e.target.value;live();});
 box.querySelectorAll("[data-tq]").forEach(x=>x.oninput=e=>{p.tar[x.dataset.tq].q=e.target.value;live();});
 box.querySelectorAll("[data-tu]").forEach(x=>x.onchange=e=>{p.tar[x.dataset.tu].u=e.target.value;ruDrawIdent();});
 const us=$("ruUseSug");if(us)us.onclick=()=>{const s=ruSug(p);p.tw=["full"];if(+p.pax){p.tar.full.u="Por persona";p.tar.full.p=String(Math.round(s/ +p.pax));}else{p.tar.full.u="Por evento";p.tar.full.p=String(Math.round(s));}ruDrawIdent();};
 box.querySelectorAll(".ru-ex").forEach(R=>{const e=p.ext[+R.dataset.ix];R.querySelector(".ru-exc").oninput=x=>{e.c=x.target.value;};R.querySelector(".ru-exp").oninput=x=>{e.p=x.target.value;};R.querySelector(".ru-exu").oninput=x=>{e.u=x.target.value;};R.querySelector(".ru-exx").onclick=()=>{p.ext.splice(+R.dataset.ix,1);ruDrawIdent();};});
 const red=()=>ruDrawIdent();
 bindUploader(k+"ph","photo",p.photos,red);bindMin(p.min,k+"mn",red);bindPromo(p.promo,k+"pr",red);
 box.querySelectorAll(".ru-covb").forEach(b=>b.onclick=()=>{p.cov.same=b.dataset.v==="1";if(!p.cov.same&&!zonesOk(p.cov.zones))p.cov.zones=JSON.parse(JSON.stringify(ruZones(Object.assign({},p,{cov:{same:true}}))||[{state:"",all:false,munis:[]}]));if(!p.cov.zones.length)p.cov.zones=[{state:"",all:false,munis:[]}];ruDrawIdent();});
 if(!p.cov.same)bindZones(p.cov.zones,k+"cv",red);bindDlSec(box,"rt",p.dlx,k+"dlx",red);
 box.querySelectorAll(".ru-lab-c").forEach(b=>b.onclick=()=>{const n=b.dataset.n;if(!p.labor.some(r=>r.n===n)){const c=p.crew.find(r=>r.n===n);p.labor.push(ruLabRow(n,c?c.q:"1"));}ruDrawIdent();});
 const lo=box.querySelector(".ru-lab-o");if(lo)lo.onclick=()=>{const w=box.querySelector(".ru-labnew");w.hidden=false;w.querySelector("input").focus({preventScroll:true});};
 ruBindTags(box,"labNew",[],()=>[...new Set(Object.values(RU.staff).flat())],v=>{if(!p.labor.some(r=>nrm(r.n)===nrm(v)))p.labor.push(ruLabRow(v,"1"));},()=>ruDrawIdent());
 box.querySelectorAll(".ru-lr").forEach(R=>{const r=p.labor[+R.dataset.ix],up=()=>{ruSyncPU(r);live();};
  const q=R.querySelector(".ru-lq");if(q)q.oninput=e=>{r.q=e.target.value;live();};
  R.querySelectorAll(".ru-line[data-j]").forEach(T=>{const t=r.tars[+T.dataset.j];T.querySelector(".ru-tp").oninput=e=>{t.p=e.target.value;up();};T.querySelector(".ru-tu").onchange=e=>{t.u=e.target.value;e.target.classList.remove("ph");if(!r.xu)r.xu=t.u==="Por hora"?"por hora":"por hora";up();};const x=T.querySelector(".ru-trm");if(x)x.onclick=()=>{r.tars.splice(+T.dataset.j,1);ruSyncPU(r);ruDrawIdent();};});
  R.querySelector(".ru-addt").onclick=()=>{const used=r.tars.map(t=>t.u);r.tars.push({p:"",u:(RU_LU.find(([u])=>!used.includes(u))||[""])[0]});ruDrawIdent();setTimeout(()=>{const l=[...document.querySelectorAll(`#ruIdent .ru-lr[data-ix="${R.dataset.ix}"] .ru-tp`)].pop();l&&l.focus({preventScroll:true});},0);};
  R.querySelector(".ru-lx").oninput=e=>{r.xh=e.target.value;live();};R.querySelector(".ru-lxu").onchange=e=>{r.xu=e.target.value;e.target.classList.remove("ph");live();};
  const rm=R.querySelector(".ru-lrm");if(rm)rm.onclick=()=>{p.labor.splice(+R.dataset.ix,1);ruDrawIdent();};});
 box.querySelectorAll(".ru-pt").forEach(b=>b.onclick=()=>{const k=b.dataset.k,m={night:"night",ride:"ride",meal:"meal",uniform:"uniform"}[k];p.lpol[m]=!p.lpol[m];ruDrawIdent();});
 const pq=(c,f)=>{const x=box.querySelector(c);if(x)f(x);};pq(".ru-p-pct",x=>x.oninput=e=>{p.lpol.nightPct=e.target.value;});pq(".ru-p-fee",x=>x.oninput=e=>{p.lpol.rideFee=e.target.value;});
 $("ruCopy").onclick=()=>copyText("https://"+$("ruLk").textContent,$("ruLkMsg"));
 $("ruImg").onclick=async()=>{const w=p.tw[0],r=w&&ruTotal(p,w);const url=await hqvShareImage({logo:"img/logo.webp",kicker:S.biz.name||"Mi negocio",title:p.name||"Mi producto",sub:[r&&+p.pax?`${ruMoney(r.pp)} por persona · para ${p.pax} personas`:"",[...ruDishes(p),...p.ins].slice(0,4).join(", ")].filter(Boolean).join(" · "),url:ruLink(p),foot:"Escanea y cotiza por WhatsApp"});hqvDownload(url,(p.kind==="pkg"?"paquete-":"producto-")+slug(p.name)+".png");hqvTrack("imagen_producto_descargada");};
 $("ruCancel").onclick=()=>{RU_EDIT=null;ruDrawIdent();};
 $("ruOk").onclick=()=>{const m=ruMiss(p);if(m.length){if(m.some(x=>/extra|mínimo|promoción/.test(x)))p._moreOpen=true;showMiss=true;ruDrawIdent();const er=$("ruErr");er.hidden=false;er.textContent="Falta: "+m.join(", ")+".";
   const f=[...box.querySelectorAll(".miss")].find(x=>x.offsetParent!==null)||er;f.scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"center"});setTimeout(()=>{const i=f.matches("input,select,textarea")?f:f.querySelector("input,select,textarea");i&&i.focus({preventScroll:true});},350);return;}
  if(p.kind==="pkg")p.sugAt=ruSug(p);
  const L=p.kind==="pkg"?S.rpkgs:S.rprods,ix=L.findIndex(x=>x.id===p.id);delete p._moreOpen;const isNew=ix<0;if(isNew&&p.kind==='prod'){S.remb=(S.remb||0)+1;p.emb=S.remb;}if(ix>=0)L[ix]=p;else L.push(p);RU_EDIT=null;ruDrawIdent();ruDrawLists();changed();ruConfetti(140);const after=()=>{if(isNew&&p.kind==='prod')setTimeout(()=>ruEmblem(p),350);else ruToast(p.kind==='pkg'?'🎁 Paquete guardado':'✓ Cambios guardados');};if(p.kind==='prod'&&p.tw.includes('full'))ruSyncStaff(p,after);else if(p.kind==='staff'){ruPropStaff(p);ruDrawLists();after();}else after();
  hqvTrack(p.kind==="pkg"?"ruleta_paquete_guardado":"ruleta_producto_guardado",{n:L.length});const t=$(p.kind==="pkg"?"ruPkgs":"ruProds");t&&t.scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"center"});};
 if(scroll)box.scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"start"});
 if(focusTag){const i=box.querySelector(`.ru-tags[data-t="${focusTag}"] input`);i&&i.focus({preventScroll:true});}}
/* ---------- productos y paquetes ---------- */
/* v25 · el proveedor ve primero el total del evento y después el precio por persona */
function ruPrice(p){const w=p.tw[0],r=w&&ruTotal(p,w);return r?`<span class="ru-pr"><b>${ruMoney(r.tot)}</b> total${r.pp!==null?` · ${ruMoney(r.pp)} por persona`:""}</span>`:`<span class="ru-pr hint">Falta el precio</span>`;}
function ruFormItems(p,w,site){if(w==="rent")return["Servicio / producto",...(p.dlx.dl.length?p.dlx.dl.map(d=>(DL_LABEL[d.m]||d.m)+(d.cobra?" (con costo)":DL_NOFEE.includes(d.m)?"":" (incluida)")):[])];
 const L=p.lpol;return["Servicio / producto",...p.labor.map(r=>`${r.q} ${ruPl(r.n,r.q)}`),"Entrega y montaje incluidos",...(site?["Precio para fiesta de 5 h",L.night?`Después de las 12:00 a.m. +${L.nightPct}%`:"",L.ride?"Transporte de regreso del staff a cargo del anfitrión":""]:[])].filter(Boolean);}
const ruUl=(L,c)=>`<ul class="${c||"ru-ul"}">${L.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>`;
function ruFormDesc(p,w){if(w==="rent")return p.dlx.dl.length?p.dlx.dl.map(d=>(DL_LABEL[d.m]||d.m)+(d.cobra?" (con costo)":"")).join(" · "):"Solo insumos";return"Insumos + "+(p.labor.map(r=>`${r.q} ${ruPl(r.n,r.q)}`).join(" + ")||"tu personal")+" · entrega y montaje incluidos";}
const ruTools=(nm,x)=>`<span class="ru-tools"${x||""}><button type="button" data-ed aria-label="Editar ${esc(nm)}">✏️</button><button type="button" data-rm aria-label="Quitar ${esc(nm)}">✕</button></span>`;
const ruPickB=(ref,nm)=>{const on=RU_PICKED.includes(ref);return`<button class="ru-pick" type="button" data-ref="${esc(ref)}" aria-pressed="${on}" aria-label="Elegir ${esc(nm)}"></button><span class="ru-ck">✓</span>`;};
function ruFormCard(p,w){const r=ruTotal(p,w),ref=p.id+"|"+w,sel=RU_PICK&&RU_PICKED.includes(ref);
 return`<article class="ru-fc${sel?" sel":""}" data-id="${p.id}" data-w="${w}"><b class="ru-fl">${ruFN[w]}</b>${r?`<span class="ru-tot">${ruMoney(r.tot)}</span><small class="ru-ppx">total del evento${r.pp!==null?` · <b>${ruMoney(r.pp)}</b> por persona`:""}</small>`:`<span class="ru-pr hint">Falta el precio</span>`}${ruUl(ruFormItems(p,w))}
  ${RU_PICK?ruPickB(ref,p.name+" "+ruFN[w]):ruTools(ruFN[w].slice(3)+" de "+p.name)}</article>`;}
function ruGroup(p){const ok=ruOk(p);
 return`<section class="ru-grp${ok?"":" warn"}" data-id="${p.id}"><header class="ru-gh"><div><div class="ru-crumbs">${p.dims.slice(0,3).map(d=>`<span>${esc(d)}</span>`).join("")}</div>
  <h4>${p.emb?`<span class="ru-embmini" title="Emblema de servicio">🏅</span>`:""}${esc(p.name)}</h4><span class="ru-meta">Para ${esc(p.pax||"—")} personas · ${p.tw.length} ${p.tw.length===1?"forma":"formas"} de contratarlo</span>${ok?"":`<span class="ru-meta" style="color:var(--bad)">⚠️ ${esc(ruMiss(p).join(", "))}</span>`}</div>
  ${RU_PICK?"":ruTools(p.name)}</header><div class="ru-forms">${p.tw.map(w=>ruFormCard(p,w)).join("")||`<span class="hint">Aún no eliges cómo lo cobras.</span>`}</div></section>`;}
function ruStaffCard(p){const r=p.labor[0],ok=ruOk(p),sel=RU_PICK&&RU_PICKED.includes(p.id);
 return`<article class="ru-pc ru-sc${sel?" sel":""}${ok?"":" warn"}" data-id="${p.id}"><span class="ru-stb">🙋 Staff</span><h4>${esc(p.name)}</h4>${ruTarsOk(r)?r.tars.map((t,j)=>`<span class="ru-pr">${j?"o ":""}<b>${money(t.p)}</b> ${esc(ruXU(t.u))}</span>`).join("")+`<span class="ru-meta">${+r.xh>0?`Extra ${money(r.xh)} ${esc(r.xu||"por hora")}`:"Sin precio de extra"}</span>`:`<span class="ru-pr hint">Falta el precio</span>`}
  ${RU_PICK?ruPickB(p.id,p.name):ruTools(p.name)}</article>`;}
function ruVenueCard(){const x=ruVenueItem();if(!x)return"";const t=ruVenueTot(),sel=RU_PICKED.includes("venue");
 return`<article class="ru-pc ru-vc${sel?" sel":""}" data-id="venue"><span class="ru-vb">🏡 Tu venue</span><h4>${esc(x.name)}</h4><span class="ru-pr">${t?`<b>${ruMoney(t)}</b> renta`:"Pon tu precio de renta en «Mi venue»"}</span><span class="ru-meta">${esc(S.venue.seated||"—")} personas sentadas</span>${RU_PICK?ruPickB("venue",x.name):""}</article>`;}
function ruCard(p){const ok=ruOk(p),r=ruTotal(p,p.tw[0]);
 return`<article class="ru-pc ru-kc${ok?"":" warn"}" data-id="${p.id}"><span class="ru-pkb">🎁 Paquete</span><h4>${esc(p.name)}</h4>${r?`<span class="ru-tot">${ruMoney(r.tot)}</span><small class="ru-ppx">total del evento${r.pp!==null?` · <b>${ruMoney(r.pp)}</b> por persona`:""}</small>`:`<span class="ru-pr hint">Falta el precio</span>`}
  <span class="ru-meta">Para ${esc(p.pax||"—")} personas · incluye:</span>${ruUl(p.items.map(ref=>ruItemName(ref,p)))}${(()=>{const now=ruSug(p);return p.sugAt&&Math.abs(now-p.sugAt)>=1?`<div class="ru-chg">⚠️ Lo que incluye cambió de precio: ahora suma <b>${ruMoney(now)}</b> (antes ${ruMoney(p.sugAt)}).<button type="button" class="link ru-upd" data-id="${p.id}">Actualizar precio</button></div>`:"";})()}${ok?"":`<span class="ru-meta" style="color:var(--bad)">⚠️ ${esc(ruMiss(p).join(", "))}</span>`}${RU_PICK?"":ruTools(p.name)}</article>`;}
const ruRefs=()=>[...(S.rprods||[]).flatMap(p=>p.kind==="staff"?[p.id]:p.tw.map(w=>p.id+"|"+w)),...(ruVenueItem()?["venue"]:[]),...ruPlanners().map(x=>x.id)];
function ruDrawLists(){if(!$("ruProds"))return;ruDefaults();const P=S.rprods.filter(x=>x.kind==="prod"),ST=S.rprods.filter(x=>x.kind==="staff"),K=S.rpkgs,nRef=ruRefs().length;
 $("ruProdH").textContent=`Tus productos (${P.length})`;
 $("ruProds").innerHTML=(RU_PICK&&ruVenueItem()?ruVenueCard():"")+(P.map(ruGroup).join("")||`<p class="ru-empty">Aún no guardas productos. Alinea los rodillos y toca «Guardar servicio».</p>`);
 const sw=$("ruStaffSec");if(sw){sw.hidden=!ST.length;$("ruStaffH").textContent=`🙋 Tu staff (${ST.length})`;$("ruStaff").innerHTML=ST.map(ruStaffCard).join("");}
 const lock=nRef<2;$("ruPkSec").classList.toggle("locked",lock);$("ruPkgH").textContent=lock?"🔒 Tus paquetes":`Tus paquetes (${K.length})`;
 $("ruPkgs").innerHTML=lock?`<p class="ru-lock">🔒 Se desbloquea cuando tengas 2 productos. ${nRef?"Te falta 1.":"Te faltan 2."} Después combinas tus productos en paquetes.</p>`:K.map(ruCard).join("")||`<p class="ru-empty">Toca «🎁 Armar un paquete» y elige qué combinar.</p>`;
 $("ruMk").disabled=lock;$("ruBar").hidden=!RU_PICK;$("ruBarT").textContent=RU_PICKED.length<2?"Elige 2 o más: servicios, staff"+(ruVenueItem()?", tu venue":"")+(ruPlanners().length?" o coordinación":""):`${RU_PICKED.length} elegidos`;$("ruGo").disabled=RU_PICKED.length<2;
 document.querySelectorAll(".ru-step2").forEach(x=>x.classList.toggle("on",!lock));
 const root=$("ruProds").closest(".panel")||document;
 root.querySelectorAll(".ru-pick").forEach(b=>b.onclick=()=>{const r=b.dataset.ref;RU_PICKED=RU_PICKED.includes(r)?RU_PICKED.filter(x=>x!==r):[...RU_PICKED,r];ruDrawLists();});
 const edit=(p,w)=>{RU_EDIT=JSON.parse(JSON.stringify(p));ruDrawIdent(!w);if(w)setTimeout(()=>{const t=document.querySelector(`#ruIdent .ru-tg[data-w="${w}"]`);(t||$("ruIdent")).scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"start"});},30);};
 const undoRm=(L,p,ix,msg)=>{L.splice(ix,1);ruDrawLists();changed();ruToast(msg,()=>{L.splice(ix,0,p);ruDrawLists();changed();});};
 root.querySelectorAll(".ru-grp").forEach(g=>{const p=S.rprods.find(x=>x.id===g.dataset.id);if(!p)return;const T=g.querySelector(".ru-gh .ru-tools");
  if(T){T.querySelector("[data-ed]").onclick=()=>edit(p);T.querySelector("[data-rm]").onclick=()=>undoRm(S.rprods,p,S.rprods.indexOf(p),`Quitaste «${p.name}»`);}
  g.querySelectorAll(".ru-fc").forEach(c=>{const w=c.dataset.w,t=c.querySelector(".ru-tools");if(!t)return;t.querySelector("[data-ed]").onclick=()=>edit(p,w);
   t.querySelector("[data-rm]").onclick=()=>{if(p.tw.length===1){undoRm(S.rprods,p,S.rprods.indexOf(p),`Quitaste «${p.name}»`);return;}const old=[...p.tw];p.tw=p.tw.filter(x=>x!==w);ruDrawLists();changed();ruToast(`Quitaste «${ruFN[w].slice(3)}» de ${p.name}`,()=>{p.tw=old;ruDrawLists();changed();});};});});
 root.querySelectorAll(".ru-sc").forEach(c=>{const p=S.rprods.find(x=>x.id===c.dataset.id),t=c.querySelector(".ru-tools");if(!p||!t)return;t.querySelector("[data-ed]").onclick=()=>edit(p);t.querySelector("[data-rm]").onclick=()=>undoRm(S.rprods,p,S.rprods.indexOf(p),`Quitaste a «${p.name}» de tu staff`);});
 root.querySelectorAll(".ru-upd").forEach(b=>b.onclick=()=>{const p=K.find(x=>x.id===b.dataset.id);if(!p)return;const now=ruSug(p),t=p.tar.full;if(+t.p&&p.sugAt)t.p=String(Math.round(+t.p*now/p.sugAt));p.sugAt=now;ruDrawLists();changed();ruToast(`💲 «${p.name}» ahora cuesta ${money(t.p)} ${t.u.toLowerCase()}`);});
 const ps=$("ruPkSec");if(ps)ps.onclick=e=>{if(!ps.classList.contains("locked"))return;e.preventDefault();ruLockPop(ps);};
 ruDrawPlanners();
 root.querySelectorAll(".ru-kc").forEach(c=>{const p=K.find(x=>x.id===c.dataset.id),t=c.querySelector(".ru-tools");if(!p||!t)return;t.querySelector("[data-ed]").onclick=()=>edit(p);t.querySelector("[data-rm]").onclick=()=>undoRm(K,p,K.indexOf(p),`Quitaste «${p.name}»`);});
 if(typeof vnRefresh==="function")vnRefresh();}
function ruToast(msg,undo){document.querySelectorAll(".ru-toast").forEach(x=>x.remove());const t=document.createElement("div");t.className="ru-toast";t.innerHTML=`<span>${esc(msg)}</span>${undo?`<button class="link" type="button">Deshacer</button>`:""}`;document.body.appendChild(t);if(undo)t.querySelector("button").onclick=()=>{undo();t.remove();};setTimeout(()=>t.remove(),4200);}
/* ---------- «Arma tu servicio» (se usa en Mis servicios y, si solo tienes venue, en Mi venue) ---------- */
function ruBuilderHtml(){return`<div class="ru-steps" role="list"><div class="ru-st on" role="listitem"><b>1</b><span><strong>Tus productos</strong><small>Enlista los bienes y servicios que provees de manera unitaria.</small></span></div><div class="ru-st ru-step2" role="listitem"><b>2</b><span><strong>Tus paquetes</strong><small>Después combina tus productos para armar paquetes.</small></span></div></div>
 <div class="ru-search"><input id="ruQ" type="search" autocomplete="off" placeholder="Busca lo que ofreces: barra de café, DJ, sillas Tiffany…" aria-label="Busca lo que ofreces"><div id="ruQr" class="ru-qr" hidden></div></div>
 ${ruMachineHtml()}
 <section class="ru-ident" id="ruIdent" hidden></section>
 <div class="ru-lh"><h3 id="ruProdH">Tus productos</h3></div>
 <div class="ru-glist" id="ruProds"></div>
 <section class="ru-stsec" id="ruStaffSec" hidden><div class="ru-lh"><h3 id="ruStaffH">🙋 Tu staff</h3></div><span class="hint">Cada perfil es un producto: se cotiza solo y lo sumas a tus paquetes por persona.</span><div class="ru-grid" id="ruStaff"></div></section>
 <section class="ru-stsec" id="ruPlSec"><div class="ru-lh"><h3>🧭 Event planners</h3><button class="btn ghost sm" id="ruInv" type="button">＋ Invitar a un event planner</button></div><span class="hint">La coordinación del evento entra en tus paquetes como una pieza más.</span><div class="ru-grid" id="ruPl"></div></section>
 <div class="ru-bar" id="ruBar" hidden><span id="ruBarT"></span><span class="row"><button class="link" id="ruNo" type="button">Cancelar</button><button class="btn cta sm" id="ruGo" type="button">Combinar</button></span></div>
 <section class="ru-pksec" id="ruPkSec"><div class="ru-lh"><h3 id="ruPkgH">Tus paquetes</h3><button class="btn ghost sm" id="ruMk" type="button">🎁 Armar un paquete</button></div>
 <div class="ru-grid" id="ruPkgs"></div></section>`;}
function ruStartPick(pre){RU_PICK=true;RU_PICKED=pre||[];ruDrawLists();const t=$("ruProds");t&&t.scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"start"});}
function ruBindBuilder(){ruBindMachine();ruBindSearch();ruDrawLists();ruDrawIdent();
 $("ruMk").onclick=e=>{e.stopPropagation();ruPkgGate();};const iv=$("ruInv");if(iv)iv.onclick=()=>ruInviteForm();
 $("ruNo").onclick=()=>{RU_PICK=false;RU_PICKED=[];ruDrawLists();};
 $("ruGo").onclick=()=>{const items=[...RU_PICKED];RU_PICK=false;RU_PICKED=[];const qty={};items.forEach(r=>{const x=ruById(r);if(x&&x.kind==="staff")qty[r]="1";});
  const cr=[...new Set(items.flatMap(r=>{const x=ruById(r);return!x?[]:x.kind==="staff"?[x.n]:ruRefW(r)==="full"?(x.labor||[]).map(c=>c.n):[];}))];const vn=items.includes("venue");
  RU_EDIT=Object.assign({id:"k"+Date.now().toString(36),kind:"pkg",items,qty,name:"",dishes:[],ins:[],crew:cr.map(n=>({n,q:"1"})),pax:vn?String(S.venue.seated||""):"",tw:[],tar:ruBlankT("Por persona")},ruBlankMore());ruDrawLists();ruDrawIdent(true);hqvTrack("ruleta_paquete_iniciado",{n:items.length,venue:vn});};}
/* ---------- paso «Mis servicios» ---------- */
function drawSvcStep(){const sc=S.svcScope=S.svcScope||{S:false,E:false};ruDefaults();
 $("stepBody").innerHTML=`<div class="panel"><span class="crumb">Mi negocio › Servicios</span><h2>Mis servicios 🎉</h2> <div class="field"><span class="lbl">¿En qué tipo de eventos trabajas? <span class="opt">Puedes elegir los dos</span></span><div class="chips${MISS(sc.S||sc.E)}" style="width:fit-content;border-radius:99px"><button type="button" class="chip scp" data-v="S" aria-pressed="${!!sc.S}">${TICK}🎉 Sociales</button><button type="button" class="chip scp" data-v="E" aria-pressed="${!!sc.E}">${TICK}💼 Empresariales</button></div></div>
 ${ruBuilderHtml()}
 ${priceBoxHtml()}
 ${zonesHtml(S.svcZones,"svc","📍 Tu zona general: ¿hasta dónde llevas tus servicios?")}<span class="hint" style="margin-top:-10px">Cada producto la usa por defecto. Si alguno llega más lejos o más cerca, lo cambias en su ficha.</span>${VIATICOS}${navHtml()}</div>`;
 document.querySelectorAll(".scp").forEach(c=>c.onclick=()=>{sc[c.dataset.v]=!sc[c.dataset.v];c.setAttribute("aria-pressed",!!sc[c.dataset.v]);changed();});
 ruBindBuilder();if(S._pickStart){S._pickStart=false;setTimeout(()=>ruStartPick(ruVenueItem()?["venue"]:[]),60);}if(S._pickVenue){S._pickVenue=false;setTimeout(()=>ruStartPick(["venue"]),60);}if(S._editPkg){const k=S.rpkgs.find(x=>x.id===S._editPkg);S._editPkg=null;if(k){RU_EDIT=JSON.parse(JSON.stringify(k));setTimeout(()=>ruDrawIdent(true),60);}}
 bindPriceBox(drawSvcStep);bindZones(S.svcZones,"svc",drawSvcStep);bindNav();}
function ruMissStep(m){ruDefaults();if(!S.rprods.some(x=>x.kind==="prod"))m.push("Guarda al menos un producto en «Arma tu servicio»");
 S.rprods.forEach(p=>{const x=ruMiss(p);if(x.length)m.push(`${p.name||"Producto"}: ${x.join(", ")}`);});S.rpkgs.forEach(p=>{const x=ruMiss(p);if(x.length)m.push(`${p.name||"Paquete"}: ${x.join(", ")}`);});}
/* ---------- sitio público ---------- */
function ruSyncServices(){if(!S.rprods)return;const cats=[...new Set(S.rprods.map(p=>p.dims[0]))];
 S.services=cats.map(c=>{const ex=(S.services||[]).find(s=>s.cat===c&&s._ru);return Object.assign(ex||{_ru:true,cat:c,desc:"",dl:[],specs:[],photos:[],min:blankMin(),promo:blankPromo(),offers:[],staff:[],rent:[],askStaff:null,askRent:null,cater:{food:false,drink:false,gas:[]}},{subs:S.rprods.filter(p=>p.dims[0]===c).map(p=>({n:p.name}))});});}
/* v25 · en el sitio: cada producto con sus formas de contratarlo y, aparte, tu personal por perfil */
function ruSiteForm(p,w){const r=ruTotal(p,w);if(!r||r.pp===null)return"";const v=+S.svcVar||0;
 const d=w==="rent"?(p.dlx.dl.length?p.dlx.dl.map(dlText).join(" · "):"Solo insumos"):"Insumos + "+p.labor.map(x=>`${x.q} ${ruPl(x.n,x.q)}`).join(" + ")+" · entrega y montaje incluidos · fiesta de 5 h"+(p.lpol.night?` · después de las 12:00 a.m. +${p.lpol.nightPct}%`:"");
 return`<span class="pform"><span class="pfh"><b>${ruFN[w]}</b><span class="price"><span class="pl">${ruMoney(r.pp)} <small>por persona</small></span><span class="pl"><small>${ruMoney(r.tot)} en total</small></span>${v?`<span class="pl"><small class="pmv">± ${v}%</small></span>`:""}</span></span>${ruUl(ruFormItems(p,w,true),"pul")}</span>`;}
function ruSiteStaff(L){return L.length?`<span class="po pstaff"><span class="pob"><span class="poh"><b>🙋 Staff por persona<small class="ctag">Contrátalo solo o súmalo a tu fiesta</small></b></span>
 ${L.map(x=>{const r=x.labor[0];return`<span class="pst-r"><span>${esc(x.name)}</span><span>${esc(ruTarsText(r))}${+r.xh>0?` · extra ${money(r.xh)} ${esc(r.xu||"por hora")}`:""}</span></span>`;}).join("")}</span></span>`:"";}
function svcPlist(s){const all=(S.rprods||[]).filter(p=>p.dims[0]===s.cat&&ruOk(p));
 return all.filter(p=>p.kind==="prod").map(p=>{const ph=p.photos[0];
 return`<span class="po${ph?" hasph":""}" id="producto-${slug(p.name)}">${ph?`<img class="phbig" src="${ph.url||ph}" alt="">`:""}<span class="pob"><span class="poh"><b>${esc(p.name)}<small class="ctag">${esc(p.dims.slice(1,3).filter(x=>x!=="Otro").join(" · "))} · para ${esc(p.pax)} personas · ${p.tw.length} ${p.tw.length===1?"forma":"formas"} de contratarlo</small></b></span>
  <span class="pforms">${p.tw.map(w=>ruSiteForm(p,w)).join("")}</span>
  ${ruDishes(p).length?(ruTimed(p)?p.courses.filter(c=>c.d.length).map(c=>`<small class="inc">🍴 <b>${esc(c.n)}:</b> ${esc(c.d.join(", "))}</small>`).join(""):`<small class="inc">🍴 ${esc(ruDishes(p).join(", "))}</small>`):""}${p.ins.length?`<small class="inc">🧺 Incluye: ${esc(p.ins.join(", "))}</small>`:""}
  ${p.ext.filter(e=>filled(e.c)).length?`<small class="inc">➕ Extras: ${esc(p.ext.filter(e=>filled(e.c)).map(e=>`${e.c} ${money(e.p)} ${e.u}`).join(" · "))}</small>`:""}${p.min.has===true&&minText(p.min)?`<small class="inc">🧾 ${esc(minText(p.min))}</small>`:""}${p.promo.has===true&&p.promo.what?`<small class="inc">🏷️ ${esc(p.promo.what)}</small>`:""}${p.cov&&!p.cov.same?`<small class="inc">📍 Llega a: ${esc(zonesText(p.cov.zones))}</small>`:""}
  ${p.photos.length>1?`<span class="pph">${p.photos.slice(1,5).map(x=>`<img src="${x.url||x}" alt="">`).join("")}</span>`:""}</span></span>`;}).join("")+ruSiteStaff(all.filter(p=>p.kind==="staff"));}
function pkgSite(){const L=(S.rpkgs||[]).filter(ruOk);if(!L.length)return"";
 return`<div class="ms-item pkgsite"><div class="ms-item-top"><b>🎁 Paquetes</b></div><div class="plist">${L.map(P=>{const w=P.tw[0],r=ruTotal(P,w),ph=P.photos[0];return`<span class="po${ph?" hasph":""}" id="paquete-${slug(P.name)}">${ph?`<img class="phbig" src="${ph.url||ph}" alt="">`:""}<span class="pob"><span class="poh"><b>${esc(P.name)}<small class="ctag">Para ${esc(P.pax)} personas</small></b><span class="price"><span class="pl">${ruMoney(r.pp)} <small>por persona</small></span><span class="pl"><small>${ruMoney(r.tot)} en total</small></span></span></span>
  <small class="inc">Incluye:</small>${ruUl(P.items.map(ref=>ruItemName(ref,P)),"pul")}${P.ins.length?`<small class="inc">🧺 ${esc(P.ins.join(", "))}</small>`:""}${P.promo.has===true&&P.promo.what?`<small class="inc">🏷️ ${esc(P.promo.what)}</small>`:""}</span></span>`;}).join("")}</div></div>`;}
/* ===== v25 · Integración del venue =====
   - Tus productos, tu personal y tus paquetes se reflejan en «Mi venue» con «¿Lo ofreces en tu venue?» y un precio aparte (no descuento).
   - El venue entra al combinador como una pieza más: «venue + productos + personal», sin volver a llenar sus datos.
   - Si solo tienes venue, «Arma tu servicio» vive dentro de «Mi venue». */
function vnItems(){const out=[];(S.rprods||[]).filter(p=>p.kind==="prod"&&ruOk(p)).forEach(p=>p.tw.forEach(w=>{const t=p.tar.i;out.push({g:"prod",ref:p.id+"|"+w,name:p.name,sub:ruFN[w]+(w==="full"?" · el servicio aquí; tu staff con sus tarifas":""),price:t.p,unit:(t.u||"").toLowerCase()});}));
 (S.rprods||[]).filter(p=>p.kind==="staff"&&ruOk(p)).forEach(p=>{const r=p.labor[0],t=r.tars[0];out.push({g:"staff",ref:p.id,name:p.name,sub:"🙋 Tu staff",price:t.p,unit:ruXU(t.u)});});
 (S.rpkgs||[]).filter(k=>!k.items.includes("venue")&&ruOk(k)).forEach(k=>{const t=k.tar.full;out.push({g:"pkg",ref:"pkg:"+k.id,name:k.name,sub:"🎁 Paquete",price:t&&t.p,unit:t&&t.u.toLowerCase()});});return out;}
const vnE=(v,ref)=>(v.svcIn=v.svcIn||{})[ref]||(v.svcIn[ref]={on:true,p:""});
function vnRowsHtml(v){const L=vnItems();if(!L.length)return`<p class="ru-empty">${S.types.services?"Cuando guardes productos en «Mis servicios», aparecen aquí para que decidas cuáles ofreces en tu venue y a qué precio.":"Si ofreces comida, bebida, staff o algo más dentro de tu venue, ármalo aquí abajo y aparecerá en esta lista."}</p>`;
 const G=[["prod","Tus productos"],["staff","Tu staff"],["pkg","Tus paquetes"]];
 return G.filter(([g])=>L.some(x=>x.g===g)).map(([g,t])=>`<span class="ru-sl">${t}</span>${L.filter(x=>x.g===g).map(x=>{const e=vnE(v,x.ref),on=e.on!==false;return`<div class="vn-r${on?"":" off"}" data-ref="${esc(x.ref)}"><button type="button" class="vn-on" aria-pressed="${on}" aria-label="¿Ofreces ${esc(x.name)} en tu venue?">${on?"✓":""}</button>
  <span class="vn-n"><b>${esc(x.name)}</b><small>${esc(x.sub)}${x.fixed?" · con los precios de tu staff":+x.price>0?` · precio normal ${money(x.price)} ${esc(x.unit)}`:""}</small></span>
  ${on&&!x.fixed?`<label class="ru-f vn-p"><small>en tu venue</small><span class="ru-fi"><i>$</i><input type="number" min="0" inputmode="decimal" class="vn-pi" value="${esc(e.p)}" placeholder="${esc(x.price||"0")}" aria-label="Precio de ${esc(x.name)} en tu venue"></span></label>`:on?"":`<span class="vn-no">No en tu venue</span>`}</div>`;}).join("")}`).join("");}
function vnPkgInner(){const L=(S.rpkgs||[]).filter(k=>k.items.includes("venue"));
 return`${L.map(k=>{const r=ruTotal(k,k.tw[0]);return`<div class="vn-kc"><span class="ru-pkb">🎁 Paquete</span><b>${esc(k.name||"Sin nombre")}</b>${r?`<span class="ru-tot">${ruMoney(r.tot)}</span><small class="ru-ppx">total del evento${r.pp!==null?` · <b>${ruMoney(r.pp)}</b> por persona`:""}</small>`:`<span class="hint">Falta el precio</span>`}${ruUl(k.items.map(ref=>ruItemName(ref,k)))}<button type="button" class="link vn-ked" data-id="${k.id}">✏️ Editar</button></div>`;}).join("")}
 <button type="button" class="btn ghost sm" id="vnMkPk">🎁 Armar paquete con tu venue</button>`;}
function vnPkgHtml(v){return`<div class="vn-pk"><b style="font-size:14px">📦 Paquetes con tu venue</b><span class="hint">Se arman en el combinador: tu venue es una pieza más, junto a tus productos y tu staff. Los datos del venue no se vuelven a llenar.</span><div class="vn-kl" id="vnPk">${vnPkgInner()}</div></div>`;}
function vnSvcHtml(v){const solo=!S.types.services,open=solo&&((S.rprods||[]).length>0||v._build);
 return`<div class="field vn-svc" id="vnSvc"><span class="lbl">🍽️ Tus servicios en tu venue</span><span class="hint">Marca lo que ofreces dentro de tu venue. El precio en tu venue es un precio aparte, no un descuento: si lo dejas vacío, usamos tu precio normal. Si quieres, después le sumas una promoción.</span>
  <div class="vn-rows" id="vnRows">${vnRowsHtml(v)}</div>
  ${solo?`<details class="more vn-build"${open?" open":""}><summary>🧩 Arma tu servicio <span class="opt">comida, bebida, staff o lo que ofrezcas en tu venue</span></summary><div class="vn-bw">${ruBuilderHtml()}</div></details>`:`<button type="button" class="link" id="vnGoSvc" style="justify-self:start">＋ Agregar o cambiar productos en «Mis servicios»</button>`}
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

/* ===== v27 · paquetes bloqueados: animación y burbuja ===== */
function ruLockPop(sec){document.querySelectorAll(".ru-lockb").forEach(x=>x.remove());sec.classList.remove("ru-shake");void sec.offsetWidth;sec.classList.add("ru-shake");
 const b=document.createElement("div");b.className="ru-lockb";b.setAttribute("role","status");b.innerHTML=`<img src="img/c_07.webp" alt=""><span>Primero define tus productos para poder armar tus paquetes 🙌</span>`;sec.appendChild(b);setTimeout(()=>b.classList.add("out"),2300);setTimeout(()=>b.remove(),2700);}
/* ===== v27 · event planners: tú o personas invitadas que aceptan ===== */
const plFeeOk=f=>filled(f.amount)&&f.unit!=="otro";
function ruPlanners(){const out=[];const P=S.planner;if(S.types&&S.types.planner&&P&&filled(P.person)&&(P.fees||[]).some(plFeeOk))out.push({id:"pl:yo",kind:"planner",name:"Coordinación · "+P.person,who:P.person,me:true,fees:P.fees.filter(plFeeOk),dims:["Event planner","","",""],crew:[],dishes:[],ins:[],tw:["planner"],pax:"",cov:{same:true}});
 (S.invites||[]).filter(i=>i.status==="aceptada"&&(i.fees||[]).some(plFeeOk)).forEach(i=>out.push({id:"pl:"+i.id,kind:"planner",name:"Coordinación · "+i.name,who:i.name,fees:i.fees.filter(plFeeOk),dims:["Event planner","","",""],crew:[],dishes:[],ins:[],tw:["planner"],pax:"",cov:{same:true}}));return out;}
/* lo que cobra el planner: fijo, por hora, por invitado o % del total (con mínimo); el anfitrión ve la opción más conveniente */
function ruPlanTot(fees,pax,base){let best=null;(fees||[]).forEach(f=>{const a=+f.amount||0;let t=f.unit==="evento"?a:f.unit==="hora"?a*5:f.unit==="invitado"?a*(+pax||0):f.unit==="porcentaje"?Math.max(a/100*(+base||0),+f.min||0):a;if(t>0&&(best===null||t<best))best=t;});return Math.round(best||0);}
const plFeesText=fees=>(fees||[]).filter(plFeeOk).map(f=>f.unit==="porcentaje"?`${f.amount}% del total${+f.min>0?` (mínimo ${money(f.min)})`:""}`:`${money(f.amount)} ${({evento:"por evento",hora:"por hora",invitado:"por invitado"})[f.unit]||""}`).join(" o ");
function ruDrawPlanners(){const box=$("ruPl");if(!box)return;const P=S.planner,own=S.types&&S.types.planner&&P,L=[];
 if(own)L.push(`<article class="ru-pc ru-plc" data-pl="pl:yo"><span class="ru-plb">🧭 Tú</span><h4>${esc(P.person||"Tu perfil de planner")}</h4>${(P.fees||[]).some(plFeeOk)?`<span class="ru-pr">${esc(plFeesText(P.fees))}</span>`:`<span class="ru-pr hint">Falta tu tarifa en «Mi perfil de planner»</span>`}${RU_PICK&&ruPlanners().some(x=>x.id==="pl:yo")?ruPickB("pl:yo",P.person):`<span class="ru-tools"><button type="button" class="ru-pled" aria-label="Editar tu perfil de planner">✏️</button></span>`}</article>`);
 (S.invites||[]).forEach(i=>{const ok=i.status==="aceptada",ref="pl:"+i.id;L.push(`<article class="ru-pc ru-plc${ok?"":" pend"}${RU_PICK&&RU_PICKED.includes(ref)?" sel":""}" data-inv="${i.id}"><span class="ru-plb ${ok?"ok":"wait"}">${ok?"✅ Aceptó":"⏳ Invitación pendiente"}</span><h4>${esc(i.name)}</h4>${ok?`<span class="ru-pr">${esc(plFeesText(i.fees))}</span>`:`<span class="ru-meta">${esc([i.wa?waShow(i.waCC,i.wa):"",i.email].filter(Boolean).join(" · "))}</span><span class="ru-meta">No se publica nada hasta que acepte.</span><span class="row ru-plact"><button type="button" class="link ru-sim">👀 Simular que aceptó</button><button type="button" class="link ru-resend">Reenviar</button></span>`}
  ${RU_PICK&&ok?ruPickB(ref,i.name):`<span class="ru-tools"><button type="button" class="ru-inx" aria-label="Quitar a ${esc(i.name)}">✕</button></span>`}</article>`);});
 box.innerHTML=L.join("")||`<p class="ru-empty">¿Trabajas con un event planner? Invítalo: cuando acepte, lo sumas a tus paquetes.</p>`;
 box.querySelectorAll(".ru-pick").forEach(b=>b.onclick=()=>{const r=b.dataset.ref;RU_PICKED=RU_PICKED.includes(r)?RU_PICKED.filter(x=>x!==r):[...RU_PICKED,r];ruDrawLists();});
 const pe=box.querySelector(".ru-pled");if(pe)pe.onclick=()=>ruGoStep("planner");
 box.querySelectorAll("[data-inv]").forEach(c=>{const i=S.invites.find(x=>x.id===c.dataset.inv);const q=s=>c.querySelector(s);
  if(q(".ru-sim"))q(".ru-sim").onclick=()=>ruInviteeView(i);if(q(".ru-resend"))q(".ru-resend").onclick=()=>ruInviteForm(i);
  if(q(".ru-inx"))q(".ru-inx").onclick=()=>{const ix=S.invites.indexOf(i);S.invites.splice(ix,1);ruDrawLists();changed();ruToast(`Quitaste a «${i.name}»: borramos sus datos`,()=>{S.invites.splice(ix,0,i);ruDrawLists();changed();});};});}
function ruGoStep(id){const ix=stepList().findIndex(s=>s.id===id);if(ix<0)return;step=ix;render();scrollTo({top:0,behavior:"instant"});}
const ruInvMsg=i=>`¡Hola, ${i.name.split(" ")[0]}! ${S.biz.owner||"Un proveedor"} te invita a sumarte a la red de proveedores de ¡Hay que vernos! como event planner de su negocio «${S.biz.name||"su negocio"}». Crea tu cuenta aquí: https://hayquevernos.com/invita/${i.id}`;
function ruModal(html,cls){const md=document.createElement("div");md.className="rmodal";md.innerHTML=`<div class="rsheet ${cls||""}">${html}</div>`;document.body.appendChild(md);md.onclick=e=>{if(e.target===md)md.remove();};return md;}
/* invitar: solo nombre y forma de contacto; nada se publica hasta que la persona acepte */
function ruInviteForm(old){const i=old||{id:"inv"+Date.now().toString(36),name:"",wa:"",waCC:"MX",email:"",status:"pendiente",fees:[]};
 const md=ruModal(`<span class="ru-embk">🧭 INVITA A TU EVENT PLANNER</span><h2>${old?"Reenviar invitación":"¿Quién coordina tus eventos?"}</h2><span>Solo necesitamos su nombre y cómo contactarle. No publicamos nada de esta persona hasta que acepte y cree su cuenta.</span>
  <div class="ru-invf"><input type="text" id="ivN" value="${esc(i.name)}" placeholder="Nombre completo" aria-label="Nombre">${telHtml("ivW",i.waCC,i.wa,"","WhatsApp")}<input type="email" id="ivE" value="${esc(i.email)}" placeholder="Correo (opcional si pones WhatsApp)" aria-label="Correo">
  <div class="ru-invm" id="ivM"></div><span class="err" id="ivErr" hidden></span>
  <div class="row"><a class="btn cta" id="ivWa" target="_blank" rel="noopener">💬 Enviar por WhatsApp</a><a class="btn ghost" id="ivMail">✉️ Enviar por correo</a></div><button type="button" class="link" id="ivX" style="color:#fff">Cancelar</button></div>`,"ru-inv");
 const upd=()=>{i.name=$("ivN").value.trim();i.wa=$("ivW").value;i.waCC=$("ivW-cc").value;i.email=$("ivE").value.trim();$("ivM").textContent=i.name?ruInvMsg(i):"Escribe su nombre para ver el mensaje.";
  $("ivWa").href=waOk(i.waCC,i.wa)?`https://wa.me/${waIntl(i.waCC,i.wa)}?text=${encodeURIComponent(ruInvMsg(i))}`:"#";$("ivMail").href=EMAIL_OK(i.email)?`mailto:${i.email}?subject=${encodeURIComponent("Te invitan a ¡Hay que vernos!")}&body=${encodeURIComponent(ruInvMsg(i))}`:"#";};
 ["ivN","ivW","ivE"].forEach(x=>$(x).oninput=upd);$("ivW-cc").onchange=upd;upd();
 const send=(ok,e)=>{const er=$("ivErr");if(!filled(i.name)||!ok){e.preventDefault();er.hidden=false;er.textContent=!filled(i.name)?"Falta su nombre.":"Falta un WhatsApp o correo válido.";($(!filled(i.name)?"ivN":"ivW")).focus();return;}
  i.status="pendiente";if(!S.invites.includes(i))S.invites.push(i);md.remove();ruDrawLists();changed();ruToast(`📨 Invitación enviada a ${i.name}. Te avisamos cuando acepte.`);hqvTrack("planner_invitado",{});};
 $("ivWa").onclick=e=>send(waOk(i.waCC,i.wa),e);$("ivMail").onclick=e=>send(EMAIL_OK(i.email),e);$("ivX").onclick=()=>md.remove();setTimeout(()=>$("ivN").focus(),50);}
/* lo que ve la persona invitada (simulación para el prototipo) */
function ruInviteeView(i){const md=ruModal(`<span class="ru-embk">LO QUE RECIBE ${esc(i.name.split(" ")[0].toUpperCase())}</span><img src="img/logo.webp" alt="¡Hay que vernos!" class="ru-invlogo"><h2>${esc(S.biz.owner||"Un proveedor")} te invita</h2><span>a la red de proveedores de ¡Hay que vernos! como <b>event planner</b> de «${esc(S.biz.name||"su negocio")}».</span>
  <div class="ru-invf"><b>Crea tu cuenta</b><input type="text" id="iaN" value="${esc(i.name)}" aria-label="Tu nombre"><input type="text" value="${esc(i.wa?waShow(i.waCC,i.wa):"")}" aria-label="Tu WhatsApp" placeholder="Tu WhatsApp"><input type="email" value="${esc(i.email)}" aria-label="Tu correo" placeholder="Tu correo">
   <label class="ru-invck"><input type="checkbox" id="iaOk"> Acepto ser event planner de «${esc(S.biz.name||"su negocio")}» y que muestre mi coordinación en sus paquetes.</label><span class="err" id="iaErr" hidden></span>
   <button type="button" class="btn cta" id="iaGo">Crear cuenta y aceptar</button><button type="button" class="link" id="iaNo" style="color:#fff">No, gracias</button></div>`,"ru-inv");
 $("iaNo").onclick=()=>{const ix=S.invites.indexOf(i);S.invites.splice(ix,1);md.remove();ruDrawLists();changed();ruToast(`${i.name} no aceptó: borramos sus datos.`);};
 $("iaGo").onclick=()=>{if(!$("iaOk").checked){const e=$("iaErr");e.hidden=false;e.textContent="Marca la casilla para aceptar el rol.";$("iaOk").focus();return;}i.name=$("iaN").value.trim()||i.name;md.remove();ruInviteeFees(i);};}
function ruInviteeFees(i){const F=i.fees.length?i.fees:[{amount:"",unit:"evento",min:""},{amount:"",unit:"porcentaje",min:""}];
 const md=ruModal(`<span class="ru-embk">PERFIL DE EVENT PLANNER · ${esc(i.name.toUpperCase())}</span><h2>¿Cómo cobras por coordinar?</h2><span>Llena una o las dos. El anfitrión ve la que más le conviene.</span>
  <div class="ru-invf"><label class="ru-invr"><span>Precio fijo por evento</span><span class="ru-fi"><i>$</i><input type="number" min="0" id="ifA" value="${esc(F[0].amount)}" placeholder="0"></span></label>
  <label class="ru-invr"><span>Porcentaje del total del evento</span><span class="ru-fi"><input type="number" min="0" max="100" id="ifP" value="${esc((F[1]||{}).amount||"")}" placeholder="10"><i>%</i></span></label>
  <label class="ru-invr"><span>Mínimo si cobras por porcentaje <small>(opcional)</small></span><span class="ru-fi"><i>$</i><input type="number" min="0" id="ifM" value="${esc((F[1]||{}).min||"")}" placeholder="0"></span></label>
  <span class="err" id="ifErr" hidden></span><button type="button" class="btn cta" id="ifGo">Listo</button><span class="hint" style="color:rgba(255,255,255,.8)!important">En la plataforma real, aquí sigue su perfil completo de event planner: foto, bio y especialidades.</span></div>`,"ru-inv");
 $("ifGo").onclick=()=>{const a=$("ifA").value,p=$("ifP").value,m=$("ifM").value;if(!(+a>0)&&!(+p>0)){const e=$("ifErr");e.hidden=false;e.textContent="Pon al menos una forma de cobrar.";$("ifA").focus();return;}
  i.fees=[+a>0?{amount:a,unit:"evento",min:""}:null,+p>0?{amount:p,unit:"porcentaje",min:m}:null].filter(Boolean);i.status="aceptada";md.remove();ruDrawLists();changed();ruConfetti(90);ruToast(`🧭 ${i.name} aceptó: ya puedes sumarle a tus paquetes.`);};}
/* ===== v27 · pop-up «Arma paquetes con todo tu negocio» ===== */
function ruPkgGate(){const nP=(S.rprods||[]).filter(x=>x.kind==="prod").length,nS=(S.rprods||[]).filter(x=>x.kind==="staff").length,v=ruVenueItem(),pls=ruPlanners(),pend=(S.invites||[]).filter(i=>i.status==="pendiente");
 const askV=!v&&!S.askNo.venue,askP=!pls.length&&!pend.length&&!S.askNo.planner;
 if(!askV&&!askP){ruStartPick([]);return;}
 const tot=4,done=(nP?1:0)+(nS?1:0)+(v?1:0)+(pls.length?1:0),ch={v:null,p:null};
 const row=(ok,t,extra)=>`<div class="ru-gr${ok?" ok":""}"><span class="ru-gi">${ok===true?"✅":ok==="wait"?"⏳":"⬜"}</span><span class="ru-gt">${t}</span>${extra||""}</div>`;
 const md=ruModal(`<span class="ru-embk">🎁 ARMA PAQUETES CON TODO TU NEGOCIO</span><h2>Tienes ${done} de ${tot}</h2><span>Un paquete puede juntar todo lo que ofreces. ¿Te falta algo?</span>
  <div class="ru-gate">${row(nP>0,`Servicios y productos <b>(${nP})</b>`)}${row(nS>0,nS?`Staff <b>(${nS})</b>`:"Staff: aún no defines ninguno")}
  ${v?row(true,`Venue: <b>${esc(v.name)}</b>`):S.askNo.venue?"":row(false,"🏡 ¿Tienes un lugar para fiestas?",`<span class="ru-gb" data-k="v"><button type="button" class="chip" data-v="si">Sí, configurarlo</button><button type="button" class="chip" data-v="no">No tengo</button></span>`)}
  ${pls.length?row(true,`Event planner: <b>${esc(pls.map(x=>x.who).join(", "))}</b>`):pend.length?row("wait",`Event planner: <b>${esc(pend[0].name)}</b> (invitación pendiente)`):S.askNo.planner?"":row(false,"🧭 ¿Hay un event planner en tu negocio?",`<span class="ru-gb" data-k="p"><button type="button" class="chip" data-v="yo">Soy yo</button><button type="button" class="chip" data-v="otro">Es otra persona</button><button type="button" class="chip" data-v="no">No</button></span>`)}</div>
  <button type="button" class="btn cta" id="gtGo">Armar paquete con lo que tengo</button><button type="button" class="link" id="gtX" style="color:#fff">Cerrar</button>`,"ru-gates");
 const go=$("gtGo"),lbl=()=>{go.textContent=ch.v==="si"||ch.p==="yo"||ch.p==="otro"?"Continuar →":"Armar paquete con lo que tengo";};
 md.querySelectorAll(".ru-gb").forEach(g=>g.querySelectorAll("button").forEach(b=>b.onclick=()=>{ch[g.dataset.k]=b.dataset.v;g.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",x===b));lbl();}));
 $("gtX").onclick=()=>md.remove();
 go.onclick=()=>{if(ch.v==="no")S.askNo.venue=true;if(ch.p==="no")S.askNo.planner=true;md.remove();changed();const Q=[];
  if(ch.v==="si"){S.types.venue=true;Q.push("venue");}
  if(ch.p==="yo"){S.types.planner=true;ruPrefillPlanner();Q.push("planner");}
  if(ch.p==="otro"){ruInviteForm();}
  if(Q.length){S._pkgQueue=Q;ensureState();ruGoStep(Q[0]);}else if(ch.p!=="otro")ruStartPick([]);};}
/* tu perfil de planner arrastra los datos de tu perfil personal */
function ruPrefillPlanner(){const p=S.planner,b=S.biz,me=S.me||{};if(!filled(p.person))p.person=b.owner||"";if(!p.photo&&me.photo)p.photo=me.photo;
 ["instagram","tiktok","facebook"].forEach(k=>{if(!filled(p[k]||"")&&filled(me[k]||""))p[k]=me[k];});if(!(p.links||[]).length&&(me.links||[]).length)p.links=JSON.parse(JSON.stringify(me.links));p.socialFromBiz=false;
 if(!p.since&&b.founded)p.since=b.founded.slice(0,4);if(!(p.zones||[]).some(z=>z.state)&&(S.svcZones||[]).some(z=>z.state))p.zones=JSON.parse(JSON.stringify(S.svcZones));}
/* aviso arriba de «Mi venue» y «Mi perfil de planner» mientras se preparan los paquetes */
function ruQueueBannerHtml(id){const Q=S._pkgQueue;if(!Q||!Q.includes(id))return"";const nx=Q[Q.indexOf(id)+1];
 return`<div class="alert info ru-qb">🎁 <span>Estás preparando tus paquetes.${id==="planner"?" Pusimos los datos de tu perfil personal; revisa y agrega tu tarifa.":""} Cuando termines:</span><button type="button" class="btn sm" onclick="ruQueueNext('${id}')">${nx==="planner"?"Seguir a mi perfil de planner →":"Volver a armar paquetes →"}</button></div>`;}
function ruQueueNext(id){const Q=S._pkgQueue||[],nx=Q[Q.indexOf(id)+1];if(nx){ruGoStep(nx);return;}S._pkgQueue=null;S._pickStart=true;ruGoStep("svc");}
