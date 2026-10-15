/* ===== v22: sin saltos de pantalla al elegir; paquetes bloqueados hasta 2 productos; «Solo tu personal» compacto (filas, ± y políticas en botones).
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
let RU_EDIT=null,RU_PICK=false,RU_PICKED=[],RU_BUSY=[null,null,null,null],RU_DRAG=null,RU_MOVED=false,RU_LASTM="";
const ruBlankT=u=>({full:{p:"",u,q:""},rent:{p:"",u,q:""},labor:{p:"",u:"Por hora",q:""}});
function ruDefaults(){if(!S.rprods)S.rprods=[];if(!S.rpkgs)S.rpkgs=[];if(!S.rsel||!RU_T.has(S.rsel[0]))S.rsel=["Catering","Bebidas","Barra","Sin alcohol"];}
const ruLpol=()=>({night:true,nightPct:"50",ride:false,rideFee:"",meal:true,uniform:true});
function ruBlankMore(){return{photos:[],ext:[],dl:[],dlOpen:-1,dlx:{dl:[],dlOpen:-1},labor:[],lpol:ruLpol(),min:blankMin(),promo:blankPromo()};}
const RU_LU=[["Por hora","por hora"],["Por turno (5 h)","por turno (5 h)"],["Por evento","por evento"],["Por día","por día"]];
const ruLabTot=p=>p.labor.reduce((a,r)=>a+(+r.p||0)*(+r.q||1)*(r.u==="Por hora"?(+r.min||5):1),0);
function ruName(dims,otro){const lc=x=>x.charAt(0).toLowerCase()+x.slice(1),gen=["Alimentos","Bebidas","Otro","Personal independiente"].includes(dims[1])||nrm(dims[2]).includes(nrm(dims[1]).slice(0,5));
 const base=gen?dims[2]:`${dims[1]} ${dims[2]}`;
 return dims[1]==="Personal independiente"?dims[3]:dims[2]==="Otro"?dims[1]:dims[3]==="Otro"?(otro?`${base} ${lc(otro)}`:base):(nrm(dims[3])===nrm(dims[2])?base:`${base} ${lc(dims[3])}`);}
function ruProd(dims,otro){const [u]=RU_U[dims.join("|")]||["Por evento"],st=RU.staff[dims[0]]||[];
 return Object.assign({id:"p"+Date.now().toString(36)+Math.random().toString(36).slice(2,5),kind:"prod",dims,otro:otro||"",name:ruName(dims,otro),dishes:[],ins:[],crew:(RU.pre[dims[0]]||[]).filter(n=>st.includes(n)).map(n=>({n,q:"1"})),pax:"",tw:[],tar:ruBlankT(u)},ruBlankMore());}
function ruDemo(){const a=ruProd(["Catering","Alimentos","Banquete","Por tiempos"]);Object.assign(a,{name:"Menú Oro",pax:"100",dishes:["Crema de elote","Mole poblano con pollo","Flan napolitano"],ins:["Platos","Cubiertos","Mantelería","Servilletas de tela"],crew:[{n:"Mesero",q:"7"},{n:"Cocinero",q:"2"},{n:"Capitán de meseros",q:"1"}],tw:["full","rent"],ext:[{c:"Hora extra",p:"1500",u:"por hora"}],dlx:{dlOpen:-1,dl:[Object.assign(blankDl("Recolección en establecimiento"),{cobra:false,ph:"Lun a sáb de 9:00 a 18:00"}),Object.assign(blankDl("Envío a domicilio"),{cobra:true,u:"Por kilómetro",rate:"15",conds:[{c:"Distancia máxima",v:"30"}]})]},photos:[{url:samplePic("🍽️","#FFB3D9","#7B2FF7",1200,900),name:"menu-oro.jpg"}]});a.tar.full.p="650";a.tar.rent.p="480";a.id="pdemo1";
 const b=ruProd(["Catering","Bebidas","Barra","Sin alcohol"]);Object.assign(b,{pax:"100",ins:["Vasos","Hielo","Popotes"],crew:[{n:"Bartender",q:"2"}],tw:["full","labor"],labor:[{n:"Bartender",q:"2",p:"280",u:"Por hora",min:"5",xh:"320"}]});b.tar.full.p="95";b.id="pdemo2";
 const c=ruProd(["Catering","Postres y dulces","Mesa de dulces","Temática"]);Object.assign(c,{name:"Mesa de dulces temática",pax:"50",ins:["Charolas","Bases de pastel","Mantelería","Decoración de mesa"],crew:[],tw:["rent"],dlx:{dlOpen:-1,dl:[Object.assign(blankDl("Envío a domicilio"),{cobra:true,u:"Por kilómetro",rate:"12",conds:[{c:"Entrega gratuita desde",v:"5000"}]}),Object.assign(blankDl("Recolección en establecimiento"),{cobra:false,ph:"Lun a sáb de 9:00 a 18:00"})]},promo:{has:true,what:"10% de descuento entre semana",terms:"De lunes a jueves",until:"2026-12-15"},min:{has:true,qty:"30",unit:"personas"},photos:[{url:samplePic("🍭","#D6338A","#7B2CBF",1200,900),name:"mesa.jpg"}]});c.tar.rent.p="3500";c.tar.rent.u="Por evento";c.id="pdemo3";
 const P={id:"kdemo1",kind:"pkg",items:["pdemo1","pdemo2"],name:"Paquete Boda Oro",dishes:[],ins:["Centros de mesa"],crew:[{n:"Mesero",q:"7"},{n:"Bartender",q:"2"}],pax:"100",tw:["full"],tar:ruBlankT("Por persona")};Object.assign(P,ruBlankMore());P.tar.full.p="720";
 return{prods:[a,b,c],pkgs:[P]};}
const ruById=id=>(S.rprods||[]).find(x=>x.id===id);
const ruCats=p=>p.kind==="pkg"?[...new Set(p.items.map(id=>(ruById(id)||{dims:["Catering"]}).dims[0]))]:[p.dims[0]];
const ruFood=p=>p.kind==="pkg"?p.items.some(id=>(ruById(id)||{dims:[]}).dims[1]==="Alimentos"):p.dims[1]==="Alimentos";
function ruTotal(p,w){const pax=+p.pax||0;if(w==="labor"){const tot=ruLabTot(p);return tot?{tot,pp:pax?tot/pax:null}:null;}
 const t=p.tar[w],pr=+t.p||0;if(!pr)return null;const tot=t.u==="Por persona"?pr*pax:RU_FIXED.includes(t.u)?pr:w==="rent"?pr*pax:pr*(+t.q||1);return{tot,pp:pax?tot/pax:null};}
const ruTarOk=(p,w)=>w==="labor"?p.labor.length>0&&p.labor.every(r=>+r.p>0):+p.tar[w].p>0&&(w==="rent"||RU_FIXED.includes(p.tar[w].u)||+p.tar[w].q>0);
const ruSug=p=>p.items.reduce((a,id)=>{const x=ruById(id),w=x&&x.tw[0],r=w&&ruTotal(x,w);return a+(r?r.tot:0);},0);
const ruMoney=n=>{n=+n||0;return n>0&&n<100&&Math.round(n)!==n?"$"+n.toLocaleString("es-MX",{minimumFractionDigits:2,maximumFractionDigits:2}):money(Math.round(n));};
const ruLink=p=>`hayquevernos.com/${slug(S.biz.name)}#${p.kind==="pkg"?"paquete":"producto"}-${slug(p.name||"sin-nombre")}`;
function ruOk(p){return filled(p.name)&&+p.pax>0&&p.tw.length>0&&p.tw.every(w=>ruTarOk(p,w))&&(!p.tw.includes("rent")||(p.dlx.dl.length>0&&p.dlx.dl.every(dlOk)))&&p.ext.every(e=>!filled(e.c)||+e.p>0)&&(p.min.has!==true||minOk(p.min))&&(p.promo.has!==true||promoOk(p.promo));}
function ruMiss(p){const m=[];if(!filled(p.name))m.push("nombre");if(!p.tw.length)m.push("cómo lo cobras");else{if(p.tw.some(w=>w!=="labor"&&!(+p.tar[w].p>0)))m.push("precio");if(p.tw.includes("full")&&+p.tar.full.p>0&&!RU_FIXED.includes(p.tar.full.u)&&!(+p.tar.full.q>0))m.push("cuántas unidades incluye");if(p.tw.includes("labor")&&!(p.labor.length&&p.labor.every(r=>+r.p>0)))m.push("precio de cada perfil de tu personal");if(p.tw.includes("rent")&&!p.dlx.dl.length)m.push("cómo entregas sin personal");else if(p.tw.includes("rent")&&!p.dlx.dl.every(dlOk))m.push("entrega por completar");}if(!(+p.pax>0))m.push("para cuántas personas alcanza");
 if(!p.ext.every(e=>!filled(e.c)||+e.p>0))m.push("precio de cada extra");if(p.min.has===true&&!minOk(p.min))m.push("mínimo de compra");if(p.promo.has===true&&!promoOk(p.promo))m.push("promoción");return m;}
/* ---------- ruleta ---------- */
function ruMachineHtml(){return`<section class="ru-m" aria-label="Ruleta de servicios">
 <div class="ru-mh"><img class="ru-masc" id="ruMasc" alt=""><div class="ru-mt"><b id="ruTit">Gira y alinea</b><span>Desliza cada rodillo. Lo que queda en la línea verde es tu selección.</span></div></div>
 <div class="ru-reels" id="ruReels">${RU_LAB.map((l,i)=>`<div class="ru-row"><div class="ru-lab">${i+1} · ${l}<span id="ruCnt${i}"></span></div><div class="ru-wrap"><button class="ru-ar l" type="button" data-i="${i}" data-d="-1" aria-label="Anterior">‹</button><div class="ru-reel" id="ruReel${i}" tabindex="0" role="listbox" aria-label="${l}"></div><button class="ru-ar r" type="button" data-i="${i}" data-d="1" aria-label="Siguiente">›</button></div></div>`).join("")}</div>
 <div class="ru-combo"><span class="ru-unit" id="ruUnit"></span><div id="ruOtro" hidden><input id="ruOtroIn" type="text" placeholder="Escribe cuál es (ej. barra de mezcal)" aria-label="Escribe cuál es"></div>
 <button class="btn cta ru-save" id="ruSave" type="button">Guardar esta combinación ✓</button></div></section>`;}
const ruReel=i=>$("ruReel"+i);
function ruFill(i){const el=ruReel(i);if(!el)return;const L=ruOpts(i,S.rsel);el.innerHTML=L.map(v=>`<button type="button" class="ru-it" role="option" data-v="${esc(v)}">${i===0&&RU.emo[v]?`<span class="e">${RU.emo[v]}</span>`:""}${esc(v)}</button>`).join("");$("ruCnt"+i).textContent=L.length+" opciones";}
const ruIdx=(i,v)=>[...ruReel(i).children].findIndex(b=>b.dataset.v===v);
const RU_RM=matchMedia("(prefers-reduced-motion: reduce)").matches;
function ruCenter(i,ix,smooth){const el=ruReel(i),b=el&&el.children[ix];if(!b)return;el.scrollTo({left:b.offsetLeft+b.offsetWidth/2-el.clientWidth/2,behavior:smooth&&!RU_RM?"smooth":"auto"});}
function ruNear(i){const el=ruReel(i),c=el.scrollLeft+el.clientWidth/2;let best=null,bd=1e9;for(const b of el.children){const d=Math.abs(b.offsetLeft+b.offsetWidth/2-c);if(d<bd){bd=d;best=b;}}return best;}
function ruPaint(i){const el=ruReel(i);if(!el)return;const c=el.scrollLeft+el.clientWidth/2,w=el.clientWidth/2||1,nb=ruNear(i);for(const b of el.children){const d=Math.min(1,Math.abs(b.offsetLeft+b.offsetWidth/2-c)/w);b.style.setProperty("--d",d.toFixed(3));b.classList.toggle("on",b===nb);b.setAttribute("aria-selected",b===nb);}}
function ruRebuild(i,target,spin){if(i>3||!ruReel(i))return;const L=ruOpts(i,S.rsel);S.rsel[i]=target&&L.includes(target)?target:L[0];ruFill(i);const ix=ruIdx(i,S.rsel[i]);RU_BUSY[i]=ix;
 if(spin&&!RU_RM){ruReel(i).scrollLeft=ruReel(i).scrollWidth;ruPaint(i);requestAnimationFrame(()=>ruCenter(i,ix,true));}else{ruCenter(i,ix,false);ruPaint(i);RU_BUSY[i]=null;}
 setTimeout(()=>{if(RU_BUSY[i]===ix&&ruReel(i)){RU_BUSY[i]=null;ruCenter(i,ix,false);ruPaint(i);}},900);}
function ruCascade(from,targets){for(let j=from;j<4;j++){const t=targets?targets[j]:null;setTimeout(()=>{ruRebuild(j,t,true);if(j===3)setTimeout(ruUpdate,80);},(j-from)*(RU_RM?0:170));}if(from>3)ruUpdate();}
function ruSettle(i){if(RU_DRAG&&RU_DRAG.i===i)return;const b=ruNear(i);if(!b)return;const ix=[...ruReel(i).children].indexOf(b);
 if(RU_BUSY[i]!==null){if(RU_BUSY[i]!==ix)return;RU_BUSY[i]=null;}const v=b.dataset.v;if(v!==S.rsel[i]){S.rsel[i]=v;ruCascade(i+1);}else ruUpdate();}
function ruStep(i,d){const b=ruNear(i),ix=[...ruReel(i).children].indexOf(b)+d;if(ix>=0&&ix<ruReel(i).children.length)ruCenter(i,ix,true);}
function ruUpdate(){if(!$("ruUnit"))return;const [u,o]=RU_U[S.rsel.join("|")]||["Por evento",""];
 $("ruUnit").innerHTML=`💲 Se suele cobrar <b>${esc(u.toLowerCase())}</b>${o?` · también ${esc(o.toLowerCase())}`:""}`;$("ruOtro").hidden=S.rsel[3]!=="Otro";$("ruTit").textContent=(RU.emo[S.rsel[0]]?RU.emo[S.rsel[0]]+" ":"")+S.rsel[0];
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
  RU_EDIT=ruProd([...S.rsel],o.value.trim());o.value="";try{confetti();}catch(_){}hqvTrack("ruleta_combinacion",{dims:S.rsel.join(" › ")});ruDrawIdent(true);};}
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
function ruHost(p){const pax=+p.pax;if(!pax||!p.tw.length)return"";const L=p.tw.map(w=>{const r=ruTotal(p,w);return r?`<span>${RU_TL[w][0]}: <b>${ruMoney(r.pp)}</b> por persona · <b>${ruMoney(r.tot)}</b> en total</span>`:"";}).filter(Boolean);
 return L.length?`<div class="ru-host"><b>👀 Así lo verá el anfitrión</b><span class="hint">En una fiesta de ${pax} personas:</span>${L.join("")}</div>`:"";}
function ruTarHtml(p,w,k){const t=p.tar[w],cnt=w==="full"&&!RU_FIXED.includes(t.u);
 return`<div class="ru-tg"><b>${RU_TL[w][0]}</b><div class="row"><label class="ru-money">$<input type="number" min="0" inputmode="decimal" data-tp="${w}" class="${MISS(+t.p>0)}" value="${esc(t.p)}" placeholder="precio" aria-label="Precio ${RU_TL[w][0]}"></label>
  <select data-tu="${w}" aria-label="Unidad">${RU_UNITS.map(u=>`<option ${t.u===u?"selected":""}>${u}</option>`).join("")}</select>
  ${cnt?`<label class="ru-q">¿Cuántas ${esc(ruNoun(t.u))}? <input type="number" min="1" data-tq="${w}" class="${MISS(+t.q>0)}" value="${esc(t.q)}" placeholder="#"></label>`:""}</div>
  ${w==="full"?`<span class="ru-note">🚚 La entrega, el montaje y tu personal van incluidos en este precio.</span>`:`${!RU_FIXED.includes(t.u)?`<span class="hint">Para el cotizador calculamos 1 ${esc(ruNoun(t.u).replace(/s$/,""))} por persona.</span>`:""}
   ${dlSecHtml(p.dlx,k+"dlx","rt","¿Cómo lo entregas?")}`}</div>`;}
function ruLaborHtml(p,staff){const rest=[...new Set(staff)].filter(n=>!p.labor.some(r=>r.n===n)),L=p.lpol;
 const pill=(k,on,txt,extra)=>`<span class="ru-pill" aria-pressed="${on}"><button type="button" class="ru-pt" data-k="${k}" aria-pressed="${on}">${on?"✓ ":""}${txt}</button>${on&&extra?extra:""}</span>`;
 return`<div class="ru-tg ru-labr"><b>${RU_TL.labor[0]}</b><span class="hint">Precio de cada perfil que mandas.</span>
  <div class="ru-lt"><div class="ru-lhd" aria-hidden="true"><span>Perfil</span><span>¿Cuántos?</span><span>Precio</span><span>Cobro</span><span>Mín.</span><span>Hora extra</span><span></span></div>
  ${p.labor.map((r,ix)=>`<div class="ru-lr" data-ix="${ix}"><b class="ru-ln">${esc(r.n)}</b>
   <span class="ru-stp"><button type="button" class="ru-sm" aria-label="Uno menos">−</button><input type="number" min="1" class="ru-lq" value="${esc(r.q)}" aria-label="¿Cuántos ${esc(r.n)}?"><button type="button" class="ru-sp" aria-label="Uno más">+</button></span>
   <label class="ru-money">$<input type="number" min="0" class="ru-lp${MISS(+r.p>0)}" value="${esc(r.p)}" placeholder="0" aria-label="Precio de ${esc(r.n)}"></label>
   <select class="ru-lu" aria-label="Cobro de ${esc(r.n)}">${RU_LU.map(([u,t])=>`<option value="${u}" ${r.u===u?"selected":""}>${t}</option>`).join("")}</select>
   ${r.u==="Por hora"?`<label class="ru-mn"><input type="number" min="1" class="ru-lm" value="${esc(r.min)}" aria-label="Horas mínimas de ${esc(r.n)}"> h</label>`:`<span class="ru-mn ru-na">—</span>`}
   <label class="ru-xh">$<input type="number" min="0" class="ru-lx" value="${esc(r.xh)}" placeholder="0" aria-label="Hora extra de ${esc(r.n)}"></label>
   <button type="button" class="link bad ru-lrm" aria-label="Quitar ${esc(r.n)}">✕</button></div>`).join("")||`<span class="hint">Agrega al menos un perfil.</span>`}</div>
  <div class="ru-add"><span class="ru-sl">＋ Sumar perfil</span><div class="ru-addc">${rest.map(n=>`<button type="button" class="chip ru-lab-c" data-n="${esc(n)}">＋ ${esc(n)}</button>`).join("")}<button type="button" class="chip new ru-lab-o">✏️ Otro</button></div><div class="ru-labnew" hidden>${ruTags("labNew",[],"Otro perfil: escribe y Enter")}</div></div>
  <div class="ru-pols"><span class="ru-sl">📋 Tus políticas</span><div class="ru-pils">
   ${pill("night",L.night,"🌙 Recargo después de 12 a.m.",`<label class="ru-pin">+<input type="number" min="0" class="ru-p-pct" value="${esc(L.nightPct)}" aria-label="Recargo nocturno">%</label>`)}
   ${pill("ride",L.ride,"🚕 Transporte de regreso lo cubre el anfitrión",`<label class="ru-pin">$<input type="number" min="0" class="ru-p-fee" value="${esc(L.rideFee)}" placeholder="0" aria-label="Transporte por persona">c/u</label>`)}
   ${pill("meal",L.meal,"🍽️ Alimentos al personal (+5 h)")}
   ${pill("uniform",L.uniform,"👔 Uniforme incluido")}</div>
   <span class="hint">El tiempo cuenta desde que tu personal llega. Viáticos fuera de zona se acuerdan.</span></div></div>`;}
function ruIdentHtml(p){const pk=p.kind==="pkg",staff=[...new Set(ruCats(p).flatMap(c=>RU.staff[c]||[]))],names=[...new Set([...staff,...p.crew.map(r=>r.n)])],k="ru"+(pk?"k":"p"),sug=pk?ruSug(p):0;
 const head=pk?`<span class="ru-pkb">🎁 Paquete</span><h3>Dale identidad a tu paquete</h3><div class="ru-crumbs">${p.items.map(id=>`<span>${esc((ruById(id)||{}).name||"—")}</span>`).join("")}</div><span class="hint">Empieza en blanco: el paquete lleva su propio nombre, detalles y precio. Guardamos de qué productos sale.</span>`
  :`<h3>Dale identidad</h3><div class="ru-crumbs">${p.dims.map(d=>`<span>${esc(d)}</span>`).join("")}${p.otro?`<span>${esc(p.otro)}</span>`:""}</div>`;
 return`${head}
 <div class="field"><label class="lbl" for="ruName">Nombre</label><input id="ruName" class="${MISS(filled(p.name))}" value="${esc(p.name)}" placeholder="${pk?"Nombre del paquete":"Nombre de tu producto"}"></div>
 <div class="field ru-inc"><span class="lbl">¿Qué incluye?</span>
  ${ruFood(p)?`<span class="ru-sl">🍴 Platillos <span class="opt">escribe y te sugerimos</span></span>${ruTags("dishes",p.dishes,"Ej. crema de elote")}`:""}
  <span class="ru-sl">🧺 Insumos <span class="opt">solo el nombre; alcanzan para tus personas</span></span>${ruTags("ins",p.ins,"Ej. platos, hielo, mantelería")}
  <span class="ru-sl">🙋 Staff <span class="opt">ya marcamos lo más común</span></span>
  <div class="chips cmini">${names.map(n=>`<button type="button" class="chip ru-crew" data-n="${esc(n)}" aria-pressed="${p.crew.some(r=>r.n===n)}">${TICK}${esc(n)}</button>`).join("")}</div>
  ${ruTags("crewNew",[],"Otro perfil: escribe y Enter")}
  ${p.crew.length?`<div class="ru-crewq">${p.crew.map((r,ix)=>`<label>${esc(r.n)}<input type="number" min="0" inputmode="numeric" data-cq="${ix}" value="${esc(r.q)}" aria-label="¿Cuántos ${esc(r.n)}?"></label>`).join("")}</div>`:""}</div>
 <div class="field"><span class="lbl">💲 ¿Cómo lo cobras? <span class="opt">elige una o varias</span></span>
  <div class="ru-tsel${MISS(p.tw.length>0)}">${["full","rent","labor"].map(w=>`<button type="button" class="ru-tsb" data-w="${w}" aria-pressed="${p.tw.includes(w)}"><b>${RU_TL[w][0]}</b><small>${RU_TL[w][1]}</small></button>`).join("")}</div>
  ${pk&&sug?`<div class="ru-sug">💡 Tus productos suman <b>${ruMoney(sug)}</b>${+p.pax?` · ${ruMoney(sug/ +p.pax)} por persona`:""}<button type="button" class="link" id="ruUseSug">Usar como precio</button></div>`:""}
  ${p.tw.map(w=>w==="labor"?ruLaborHtml(p,staff):ruTarHtml(p,w,k)).join("")}</div>
 <div class="ru-paxc"><img src="img/c_07.webp" alt="" class="ru-paxm"><div class="ru-paxq"><label class="ru-paxl" for="ruPax">¿Para cuántas personas alcanza todo esto?</label><span class="ru-paxh">Es el dato más importante: con él te mostramos en el cotizador del anfitrión.</span>
  <div class="ru-paxi"><input id="ruPax" class="${MISS(+p.pax>0)}" type="number" min="1" inputmode="numeric" value="${esc(p.pax)}" placeholder="#" aria-label="Personas"><b>personas</b></div></div>
  <div id="ruHost">${ruHost(p)}</div></div>
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
 $("ruName").oninput=e=>{p.name=e.target.value;$("ruLk").textContent=ruLink(p);};
 $("ruPax").oninput=e=>{p.pax=e.target.value;$("ruHost").innerHTML=ruHost(p);};
 ruBindTags(box,"dishes",p.dishes,()=>RU_DISHES,null,rd);ruBindTags(box,"ins",p.ins,()=>ruIns(ruCats(p)[0]),null,rd);
 ruBindTags(box,"crewNew",[],()=>[...new Set(Object.values(RU.staff).flat())],v=>{if(!p.crew.some(r=>nrm(r.n)===nrm(v)))p.crew.push({n:v,q:"1"});},rd);
 ruBindTags(box,"ext",[],()=>RU_EXTRAS.filter(x=>!p.ext.some(e=>e.c===x)),v=>{if(!p.ext.some(e=>nrm(e.c)===nrm(v)))p.ext.push({c:v,p:"",u:ruExU(v)});setTimeout(()=>{const l=[...box.querySelectorAll(".ru-exp")].pop();l&&l.focus({preventScroll:true});},0);},rd);
 box.querySelectorAll(".ru-crew").forEach(b=>b.onclick=()=>{const n=b.dataset.n,ix=p.crew.findIndex(r=>r.n===n);if(ix>=0)p.crew.splice(ix,1);else p.crew.push({n,q:"1"});ruDrawIdent();});
 box.querySelectorAll("[data-cq]").forEach(x=>x.oninput=e=>{p.crew[+x.dataset.cq].q=e.target.value;});
 box.querySelectorAll(".ru-tsb").forEach(b=>b.onclick=()=>{const w=b.dataset.w;p.tw=p.tw.includes(w)?p.tw.filter(x=>x!==w):["full","rent","labor"].filter(x=>x===w||p.tw.includes(x));
  if(w==="labor"&&p.tw.includes("labor")&&!p.labor.length)p.labor=p.crew.map(r=>({n:r.n,q:r.q||"1",p:"",u:"Por hora",min:"5",xh:""}));ruDrawIdent();});
 const live=()=>{$("ruHost").innerHTML=ruHost(p);};
 box.querySelectorAll("[data-tp]").forEach(x=>x.oninput=e=>{p.tar[x.dataset.tp].p=e.target.value;live();});
 box.querySelectorAll("[data-tq]").forEach(x=>x.oninput=e=>{p.tar[x.dataset.tq].q=e.target.value;live();});
 box.querySelectorAll("[data-tu]").forEach(x=>x.onchange=e=>{p.tar[x.dataset.tu].u=e.target.value;ruDrawIdent();});
 const us=$("ruUseSug");if(us)us.onclick=()=>{const s=ruSug(p);if(!p.tw.includes("full"))p.tw.unshift("full");if(+p.pax){p.tar.full.u="Por persona";p.tar.full.p=String(Math.round(s/ +p.pax));}else{p.tar.full.u="Por evento";p.tar.full.p=String(Math.round(s));}ruDrawIdent();};
 box.querySelectorAll(".ru-ex").forEach(R=>{const e=p.ext[+R.dataset.ix];R.querySelector(".ru-exc").oninput=x=>{e.c=x.target.value;};R.querySelector(".ru-exp").oninput=x=>{e.p=x.target.value;};R.querySelector(".ru-exu").oninput=x=>{e.u=x.target.value;};R.querySelector(".ru-exx").onclick=()=>{p.ext.splice(+R.dataset.ix,1);ruDrawIdent();};});
 const red=()=>ruDrawIdent();
 bindUploader(k+"ph","photo",p.photos,red);bindDlSec(box,"rt",p.dlx,k+"dlx",red);
 box.querySelectorAll(".ru-lab-c").forEach(b=>b.onclick=()=>{const n=b.dataset.n;if(!p.labor.some(r=>r.n===n)){const c=p.crew.find(r=>r.n===n);p.labor.push({n,q:c?c.q:"1",p:"",u:"Por hora",min:"5",xh:""});}ruDrawIdent();});
 const lo=box.querySelector(".ru-lab-o");if(lo)lo.onclick=()=>{const w=box.querySelector(".ru-labnew");w.hidden=false;w.querySelector("input").focus({preventScroll:true});};
 ruBindTags(box,"labNew",[],()=>[...new Set(Object.values(RU.staff).flat())],v=>{if(!p.labor.some(r=>nrm(r.n)===nrm(v)))p.labor.push({n:v,q:"1",p:"",u:"Por hora",min:"5",xh:""});},()=>ruDrawIdent());
 box.querySelectorAll(".ru-lr").forEach(R=>{const r=p.labor[+R.dataset.ix];[["ru-lq","q"],["ru-lp","p"],["ru-lm","min"],["ru-lx","xh"]].forEach(([c,f])=>{const x=R.querySelector("."+c);if(x)x.oninput=e=>{r[f]=e.target.value;live();};});
  const q=R.querySelector(".ru-lq");R.querySelector(".ru-sm").onclick=()=>{r.q=String(Math.max(1,(+r.q||1)-1));q.value=r.q;live();};R.querySelector(".ru-sp").onclick=()=>{r.q=String((+r.q||0)+1);q.value=r.q;live();};
  R.querySelector(".ru-lu").onchange=e=>{r.u=e.target.value;ruDrawIdent();};R.querySelector(".ru-lrm").onclick=()=>{p.labor.splice(+R.dataset.ix,1);ruDrawIdent();};});
 box.querySelectorAll(".ru-pt").forEach(b=>b.onclick=()=>{const k=b.dataset.k,m={night:"night",ride:"ride",meal:"meal",uniform:"uniform"}[k];p.lpol[m]=!p.lpol[m];ruDrawIdent();});
 const pq=(c,f)=>{const x=box.querySelector(c);if(x)f(x);};pq(".ru-p-pct",x=>x.oninput=e=>{p.lpol.nightPct=e.target.value;});pq(".ru-p-fee",x=>x.oninput=e=>{p.lpol.rideFee=e.target.value;});
 $("ruCopy").onclick=()=>copyText("https://"+$("ruLk").textContent,$("ruLkMsg"));
 $("ruImg").onclick=async()=>{const w=p.tw[0],r=w&&ruTotal(p,w);const url=await hqvShareImage({logo:"img/logo.webp",kicker:S.biz.name||"Mi negocio",title:p.name||"Mi producto",sub:[r&&+p.pax?`${ruMoney(r.pp)} por persona · para ${p.pax} personas`:"",[...p.dishes,...p.ins].slice(0,4).join(", ")].filter(Boolean).join(" · "),url:ruLink(p),foot:"Escanea y cotiza por WhatsApp"});hqvDownload(url,(p.kind==="pkg"?"paquete-":"producto-")+slug(p.name)+".png");hqvTrack("imagen_producto_descargada");};
 $("ruCancel").onclick=()=>{RU_EDIT=null;ruDrawIdent();};
 $("ruOk").onclick=()=>{const m=ruMiss(p),er=$("ruErr");if(m.length){er.hidden=false;er.textContent="Falta: "+m.join(", ")+".";if(m.some(x=>/extra|entrega|mínimo|promoción/.test(x))){p._moreOpen=true;box.querySelector("details.ru-more").open=true;}return;}
  const L=p.kind==="pkg"?S.rpkgs:S.rprods,ix=L.findIndex(x=>x.id===p.id);delete p._moreOpen;if(ix>=0)L[ix]=p;else L.push(p);RU_EDIT=null;ruDrawIdent();ruDrawLists();changed();try{confetti();}catch(_){}
  hqvTrack(p.kind==="pkg"?"ruleta_paquete_guardado":"ruleta_producto_guardado",{n:L.length});const t=$(p.kind==="pkg"?"ruPkgs":"ruProds");t&&t.scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"center"});};
 if(scroll)box.scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"start"});
 if(focusTag){const i=box.querySelector(`.ru-tags[data-t="${focusTag}"] input`);i&&i.focus({preventScroll:true});}}
/* ---------- productos y paquetes ---------- */
function ruPrice(p){const w=p.tw[0],r=w&&ruTotal(p,w);return r&&r.pp!==null?`<span class="ru-pr"><b>${ruMoney(r.pp)}</b> por persona · ${ruMoney(r.tot)} total</span>`:`<span class="ru-pr hint">Falta el precio</span>`;}
function ruCard(p){const pk=p.kind==="pkg",sel=RU_PICK&&!pk&&RU_PICKED.includes(p.id),ok=ruOk(p);
 return`<article class="ru-pc${sel?" sel":""}${ok?"":" warn"}" data-id="${p.id}">${pk?`<span class="ru-pkb">🎁 Paquete</span>`:`<div class="ru-crumbs">${p.dims.slice(0,3).map(d=>`<span>${esc(d)}</span>`).join("")}</div>`}
  <h4>${esc(p.name)}</h4>${ruPrice(p)}<span class="ru-meta">Para ${esc(p.pax||"—")} personas${p.tw.length>1?` · ${p.tw.length} formas de cobro`:""}</span>
  <span class="ru-meta">${esc(pk?"Incluye: "+p.items.map(id=>(ruById(id)||{}).name||"—").join(" + "):[...p.dishes,...p.ins].slice(0,4).join(", "))}</span>${ok?"":`<span class="ru-meta" style="color:var(--bad)">⚠️ ${esc(ruMiss(p).join(", "))}</span>`}
  ${RU_PICK&&!pk?`<button class="ru-pick" type="button" aria-label="Elegir ${esc(p.name)}"></button><span class="ru-ck">✓</span>`:`<span class="ru-tools"><button type="button" data-ed aria-label="Editar ${esc(p.name)}">✏️</button><button type="button" data-rm aria-label="Quitar ${esc(p.name)}">✕</button></span>`}</article>`;}
function ruDrawLists(){if(!$("ruProds"))return;ruDefaults();const P=S.rprods,K=S.rpkgs;
 $("ruProdH").textContent=`Tus productos (${P.length})`;
 $("ruProds").innerHTML=P.map(ruCard).join("")||`<p class="ru-empty">Aún no guardas productos. Alinea los rodillos y toca «Guardar esta combinación».</p>`;
 const lock=P.length<2;$("ruPkSec").classList.toggle("locked",lock);$("ruPkgH").textContent=lock?"🔒 Tus paquetes":`Tus paquetes (${K.length})`;
 $("ruPkgs").innerHTML=lock?`<p class="ru-lock">🔒 Se desbloquea cuando tengas 2 productos. ${P.length?"Te falta 1.":"Te faltan 2."} Después combinas tus productos en paquetes.</p>`:K.map(ruCard).join("")||`<p class="ru-empty">Toca «🎁 Armar un paquete» y elige qué productos combinar.</p>`;
 $("ruMk").disabled=P.length<2;$("ruBar").hidden=!RU_PICK;$("ruBarT").textContent=RU_PICKED.length<2?"Elige 2 o más productos":`${RU_PICKED.length} productos elegidos`;$("ruGo").disabled=RU_PICKED.length<2;
 document.querySelectorAll(".ru-step2").forEach(x=>x.classList.toggle("on",P.length>=2));
 document.querySelectorAll(".ru-pc").forEach(c=>{const id=c.dataset.id,L=P.some(x=>x.id===id)?P:K,p=L.find(x=>x.id===id);
  const pk=c.querySelector(".ru-pick");if(pk)pk.onclick=()=>{RU_PICKED=RU_PICKED.includes(id)?RU_PICKED.filter(x=>x!==id):[...RU_PICKED,id];ruDrawLists();};
  const ed=c.querySelector("[data-ed]");if(ed)ed.onclick=()=>{RU_EDIT=JSON.parse(JSON.stringify(p));ruDrawIdent(true);};
  const rm=c.querySelector("[data-rm]");if(rm)rm.onclick=()=>{const ix=L.indexOf(p);L.splice(ix,1);ruDrawLists();changed();ruToast(`Quitaste «${p.name}»`,()=>{L.splice(ix,0,p);ruDrawLists();changed();});};});}
function ruToast(msg,undo){document.querySelectorAll(".ru-toast").forEach(x=>x.remove());const t=document.createElement("div");t.className="ru-toast";t.innerHTML=`<span>${esc(msg)}</span>${undo?`<button class="link" type="button">Deshacer</button>`:""}`;document.body.appendChild(t);if(undo)t.querySelector("button").onclick=()=>{undo();t.remove();};setTimeout(()=>t.remove(),4200);}
/* ---------- paso «Mis servicios» ---------- */
function drawSvcStep(){const sc=S.svcScope=S.svcScope||{S:false,E:false};ruDefaults();
 $("stepBody").innerHTML=`<div class="panel"><span class="crumb">Mi negocio › Servicios</span><h2>Mis servicios 🎉</h2><p class="sub">Arma lo que vendes jugando con la ruleta. Nosotros se lo mostramos al anfitrión por persona y en total.</p>
 <div class="field"><span class="lbl">¿En qué tipo de eventos trabajas? <span class="opt">Puedes elegir los dos</span></span><div class="chips${MISS(sc.S||sc.E)}" style="width:fit-content;border-radius:99px"><button type="button" class="chip scp" data-v="S" aria-pressed="${!!sc.S}">${TICK}🎉 Sociales</button><button type="button" class="chip scp" data-v="E" aria-pressed="${!!sc.E}">${TICK}💼 Empresariales</button></div></div>
 <div class="ru-steps" role="list"><div class="ru-st on" role="listitem"><b>1</b><span><strong>Tus productos</strong><small>Uno por uno: alinea la ruleta, guarda y dale identidad.</small></span></div><div class="ru-st ru-step2" role="listitem"><b>2</b><span><strong>Tus paquetes</strong><small>Después combinas tus productos: catering + música + mesas.</small></span></div></div>
 <div class="ru-search"><input id="ruQ" type="search" autocomplete="off" placeholder="Busca lo que ofreces: barra de café, DJ, sillas Tiffany…" aria-label="Busca lo que ofreces"><div id="ruQr" class="ru-qr" hidden></div></div>
 ${ruMachineHtml()}
 <section class="ru-ident" id="ruIdent" hidden></section>
 <div class="ru-lh"><h3 id="ruProdH">Tus productos</h3></div>
 <div class="ru-grid" id="ruProds"></div>
 <div class="ru-bar" id="ruBar" hidden><span id="ruBarT"></span><span class="row"><button class="link" id="ruNo" type="button">Cancelar</button><button class="btn cta sm" id="ruGo" type="button">Combinar</button></span></div>
 <section class="ru-pksec" id="ruPkSec"><div class="ru-lh"><h3 id="ruPkgH">Tus paquetes</h3><button class="btn ghost sm" id="ruMk" type="button">🎁 Armar un paquete</button></div>
 <div class="ru-grid" id="ruPkgs"></div></section>
 ${priceBoxHtml()}
 ${zonesHtml(S.svcZones,"svc","¿Dónde das estos servicios?")}${VIATICOS}${navHtml()}</div>`;
 document.querySelectorAll(".scp").forEach(c=>c.onclick=()=>{sc[c.dataset.v]=!sc[c.dataset.v];c.setAttribute("aria-pressed",!!sc[c.dataset.v]);changed();});
 ruBindMachine();ruBindSearch();ruDrawLists();ruDrawIdent();
 $("ruMk").onclick=()=>{RU_PICK=true;RU_PICKED=[];ruDrawLists();$("ruProds").scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"start"});};
 $("ruNo").onclick=()=>{RU_PICK=false;RU_PICKED=[];ruDrawLists();};
 $("ruGo").onclick=()=>{const items=[...RU_PICKED];RU_PICK=false;RU_PICKED=[];const cr=[...new Set(items.flatMap(id=>(ruById(id)||{crew:[]}).crew.map(r=>r.n)))];
  RU_EDIT=Object.assign({id:"k"+Date.now().toString(36),kind:"pkg",items,name:"",dishes:[],ins:[],crew:cr.map(n=>({n,q:"1"})),pax:"",tw:[],tar:ruBlankT("Por persona")},ruBlankMore());ruDrawLists();ruDrawIdent(true);hqvTrack("ruleta_paquete_iniciado",{n:items.length});};
 bindPriceBox(drawSvcStep);bindZones(S.svcZones,"svc",drawSvcStep);bindNav();}
function ruMissStep(m){ruDefaults();if(!S.rprods.length)m.push("Guarda al menos un producto con la ruleta");
 S.rprods.forEach(p=>{const x=ruMiss(p);if(x.length)m.push(`${p.name||"Producto"}: ${x.join(", ")}`);});S.rpkgs.forEach(p=>{const x=ruMiss(p);if(x.length)m.push(`${p.name||"Paquete"}: ${x.join(", ")}`);});}
/* ---------- sitio público ---------- */
function ruSyncServices(){if(!S.rprods)return;const cats=[...new Set(S.rprods.map(p=>p.dims[0]))];
 S.services=cats.map(c=>{const ex=(S.services||[]).find(s=>s.cat===c&&s._ru);return Object.assign(ex||{_ru:true,cat:c,desc:"",dl:[],specs:[],photos:[],min:blankMin(),promo:blankPromo(),offers:[],staff:[],rent:[],askStaff:null,askRent:null,cater:{food:false,drink:false,gas:[]}},{subs:S.rprods.filter(p=>p.dims[0]===c).map(p=>({n:p.name}))});});}
function svcPlist(s){const v=+S.svcVar||0;return(S.rprods||[]).filter(p=>p.dims[0]===s.cat&&ruOk(p)).map(p=>{const ph=p.photos[0];
 return`<span class="po${ph?" hasph":""}" id="producto-${slug(p.name)}">${ph?`<img class="phbig" src="${ph.url||ph}" alt="">`:""}<span class="pob"><span class="poh"><b>${esc(p.name)}<small class="ctag">${esc(p.dims.slice(1,3).filter(x=>x!=="Otro").join(" · "))} · para ${esc(p.pax)} personas</small></b>
  <span class="price">${p.tw.map(w=>{const r=ruTotal(p,w);return r&&r.pp!==null?`<span class="pl">${p.tw.length>1?`<small>${RU_TL[w][0].slice(3)}:</small> `:""}${ruMoney(r.pp)} <small>por persona</small></span>`:"";}).join("")}${v?`<span class="pl"><small class="pmv">± ${v}%</small></span>`:""}</span></span>
  ${p.dishes.length?`<small class="inc">🍴 ${esc(p.dishes.join(", "))}</small>`:""}${p.ins.length?`<small class="inc">🧺 Incluye: ${esc(p.ins.join(", "))}</small>`:""}${p.crew.length?`<small class="inc">🙋 Staff: ${esc(p.crew.map(r=>`${r.q} ${r.n.toLowerCase()}`).join(", "))}</small>`:""}
  ${p.ext.filter(e=>filled(e.c)).length?`<small class="inc">➕ Extras: ${esc(p.ext.filter(e=>filled(e.c)).map(e=>`${e.c} ${money(e.p)} ${e.u}`).join(" · "))}</small>`:""}${p.tw.includes("full")?`<small class="inc">🚚 Servicio completo: entrega y montaje incluidos</small>`:""}${p.tw.includes("rent")&&p.dlx.dl.length?`<small class="inc">📦 Sin personal: ${esc(p.dlx.dl.map(dlText).join(" · "))}</small>`:""}${p.tw.includes("labor")&&p.labor.length?`<small class="inc">🙋 Solo personal: ${esc(p.labor.map(r=>`${r.n} ${money(r.p)} ${RU_LU.find(x=>x[0]===r.u)[1]}${filled(r.xh)?` (hora extra ${money(r.xh)})`:""}`).join(" · "))}${p.lpol.night?` · después de las 12:00 a.m. +${esc(p.lpol.nightPct)}%`:""}</small>`:""}${p.min.has===true&&minText(p.min)?`<small class="inc">🧾 ${esc(minText(p.min))}</small>`:""}${p.promo.has===true&&p.promo.what?`<small class="inc">🏷️ ${esc(p.promo.what)}</small>`:""}
  ${p.photos.length>1?`<span class="pph">${p.photos.slice(1,5).map(x=>`<img src="${x.url||x}" alt="">`).join("")}</span>`:""}</span></span>`;}).join("");}
function pkgSite(){const L=(S.rpkgs||[]).filter(ruOk);if(!L.length)return"";
 return`<div class="ms-item pkgsite"><div class="ms-item-top"><b>🎁 Paquetes</b></div><div class="plist">${L.map(P=>{const w=P.tw[0],r=ruTotal(P,w),ph=P.photos[0];return`<span class="po${ph?" hasph":""}" id="paquete-${slug(P.name)}">${ph?`<img class="phbig" src="${ph.url||ph}" alt="">`:""}<span class="pob"><span class="poh"><b>${esc(P.name)}<small class="ctag">Para ${esc(P.pax)} personas</small></b><span class="price"><span class="pl">${ruMoney(r.pp)} <small>por persona</small></span><span class="pl"><small>${ruMoney(r.tot)} en total</small></span></span></span>
  <small class="inc">Incluye: ${esc(P.items.map(id=>(ruById(id)||{}).name||"—").join(" + "))}</small>${P.ins.length?`<small class="inc">🧺 ${esc(P.ins.join(", "))}</small>`:""}${P.crew.length?`<small class="inc">🙋 Staff: ${esc(P.crew.map(x=>`${x.q} ${x.n.toLowerCase()}`).join(", "))}</small>`:""}${P.promo.has===true&&P.promo.what?`<small class="inc">🏷️ ${esc(P.promo.what)}</small>`:""}</span></span>`;}).join("")}</div></div>`;}
