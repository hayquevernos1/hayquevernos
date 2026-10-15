/* ===== v18 · Servicios (Diego, 14 oct 2026 noche) =====
   · Cada ficha se arma como un paquete sin que se note: nombre → ¿para cuántas personas? → menú por tiempos →
     ¿Qué incluye? en 3 partes: 🧺 insumos (la unidad se predice sola), 🧩 otros servicios (categorías afines que se
     definen ahí mismo) y 🙋 staff (opción múltiple con lo indispensable ya marcado y la cantidad calculada por personas).
   · Duración en horas + aviso de llegar 1 h antes y 1 h para retirarse.
   · Tres tarifas en una sola vista: completo · sin personal · solo el personal. ±% y temporada alta pasan al final.
   · Al cerrar la ficha detectamos los servicios incluidos y recomendamos venderlos por separado (servicio unitario).
   · En catering ya no se pregunta «¿Tu equipo trabaja con los insumos del cliente?»: lo cubre la tarifa «Solo tu personal». */
const nrm=s=>String(s??"").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"");
const FOOD_FMT=["Banquete","Buffet","Cóctel","Estación de especialidad","Box lunch","Productos individuales"];
const DRINK_FMT=[...C2.bebidasServicio];
const FMT_EMO={"Banquete":"🍽️","Buffet":"🥘","Cóctel":"🍢","Estación de especialidad":"🌮","Box lunch":"🥡","Productos individuales":"🧁","Barra":"🍹","Estación":"🥤","Mesa":"🧊","Carrito":"🛒","Dispensador":"🚰","Barril":"🛢️"};
const MONTHS=[["ene","Ene"],["feb","Feb"],["mar","Mar"],["abr","Abr"],["may","May"],["jun","Jun"],["jul","Jul"],["ago","Ago"],["sep","Sep"],["oct","Oct"],["nov","Nov"],["dic","Dic"]];
const HIGH_STD=["may","jun","oct","nov","dic"];
const GASTROS=[...new Set([...Object.keys(C2.cocina.Salado),...Object.keys(C2.cocina.Dulce)])].filter(g=>g!=="Clásicos de banquete");
const U_FULL=["Por persona","Por evento","Por paquete","Por pieza","Por hora","Por caja","Por kilo","Por litro","Por mesa","Por docena (12 piezas)","Por ciento (100 piezas)","Por estación","Por día","Por menú"];
const U_STAFF=[["Por hora","por hora"],["Por turno","por turno (5 h)"],["Por evento","por evento"],["Por día","por día"]];
const U_RENT=[["Por pieza","por pieza"],["Por juego","por juego"],["Por evento","por evento"],["Por día","por día"]];
/* catálogo para predecir: especialidad → platillos, por salado / dulce / bebidas */
const ESP={},DISHES={},KIND_OF={};
["Salado","Dulce"].forEach(k=>{ESP[k]=[];DISHES[k]=[];Object.values(C2.cocina[k]).forEach(g=>Object.entries(g).forEach(([e,ps])=>{const ne=nrm(e);if(!ESP[k].some(x=>nrm(x.n)===ne))ESP[k].push({n:e,d:[]});const it=ESP[k].find(x=>nrm(x.n)===ne);ps.forEach(p=>{if(!it.d.includes(p))it.d.push(p);if(!DISHES[k].includes(p))DISHES[k].push(p);KIND_OF[nrm(p)]=KIND_OF[nrm(p)]||k;});KIND_OF[ne]=KIND_OF[ne]||k;}));});
ESP.Ambos=[...ESP.Salado,...ESP.Dulce];DISHES.Ambos=[...DISHES.Salado,...DISHES.Dulce];
["Con alcohol","Sin alcohol"].forEach(a=>{ESP[a]=C2.bebidas.filter(b=>b.alc.includes(a)).map(b=>({n:b.n,d:b.v.filter(v=>a==="Con alcohol"?true:true)}));DISHES[a]=[...new Set(ESP[a].flatMap(x=>x.d))];});
const DRINK_VARS=[...new Set(C2.bebidas.flatMap(b=>b.v))].sort((a,b)=>a.localeCompare(b,"es"));
const DISH_LIST={Salado:DISHES.Salado,Dulce:DISHES.Dulce};
const espOf=(scope,v)=>ESP[scope].find(x=>nrm(x.n)===nrm(v||"").trim());
const firstLike=(L,re,fb)=>L.find(x=>re.test(x))||fb;
const TIEMPO_N=["Primer","Segundo","Tercer","Cuarto","Quinto","Sexto","Séptimo","Octavo"];
const TIEMPO_PH=[["entradas","Carpaccio de res"],["cremas","Crema de champiñones"],["platos fuertes","Filete de res en salsa de vino tinto"],["postres tradicionales",firstLike(DISHES.Dulce,/^(flan|pastel|tiramis)/i,"Flan napolitano")]];
/* «¿Qué incluye?»: detalle sugerido según el concepto */
const DETAIL={"platos":["Loza","Desechables","Biodegradables","Base para plato"],"cubiertos":["Acero inoxidable","Desechables","Biodegradables"],"vasos y copas":["Cristal","Acrílico","Desechables"],"vasos":["Cristal","Acrílico","Desechables"],"copas":["Cristal","Acrílico"],"mantelería":["Redondos","Rectangulares","Con cubremantel","Caminos de mesa"],"manteles":["Redondos","Rectangulares","Con cubremantel"],"servilletas":["Tela","Papel","Con monograma"],"meseros":["Uniformados","Con guantes","Bilingües"],"loza":["Blanca","De color","Rústica"],"hielo":["En cubo","Frappé","Bolsa de 5 kg"],"bartender":["Uniformado","Con show de flair"]};
const INC_SUGG=["Platos","Cubiertos","Servilletas","Vasos y copas","Mantelería","Meseros","Capitán de meseros","Montaje y desmontaje","Loza","Cristalería","Chafers","Charolas","Mesa de servicio","Decoración de mesa","Cocinero","Bartender","Hielo","Popotes","Mezcladores","Barra","Limpieza","Traslado","Personal","Equipo","Hora extra","Pastel","Mesa de postres","Mesero extra","Botella extra","Coctel de autor","Bocinas","Micrófono","Luces","Pantalla","Fotos digitales","Álbum impreso"];
const UNIT_SUGG=["piezas","personas","kilos","litros","horas","cajas","juegos","charolas","mesas","porciones","paquetes","metros","por persona","por cada 10 invitados","por cada 15 invitados","por cada 25 invitados"];
const INC_PH={food:["Platos","Servilletas","Meseros"],drink:["Barra","Bartender","Hielo"],gen:["Montaje","Equipo","Personal"]};
const isCat=s=>s.cat==="Catering";
/* v18 · insumos: la unidad se predice según el concepto */
const INSUMOS={food:["Platos","Cubiertos","Servilletas","Vasos","Copas","Mantelería","Cubremanteles","Caminos de mesa","Loza","Charolas","Chafers","Desechables","Saleros y pimenteros","Servilleteros","Hielo","Carbón","Gas","Bolsas para basura"],
 drink:["Vasos","Copas","Hielo","Popotes","Mezcladores","Servilletas","Hieleras","Garrafones de agua","Refrescos","Agua mineral","Fruta para decorar","Jarras","Vitroleros"],
 gen:INC_SUGG};
const UNIT_OF=Object.fromEntries(Object.entries({"platos":"piezas","plato":"piezas","cubiertos":"juegos","servilletas":"piezas","vasos":"piezas","copas":"piezas","mantelería":"piezas","manteles":"piezas","cubremanteles":"piezas","caminos de mesa":"piezas","loza":"juegos","cristalería":"juegos","charolas":"piezas","chafers":"piezas","desechables":"juegos","saleros y pimenteros":"juegos","servilleteros":"piezas","hielo":"kilos","carbón":"kilos","gas":"tanques","bolsas para basura":"piezas","popotes":"piezas","mezcladores":"piezas","hieleras":"piezas","garrafones de agua":"garrafones","refrescos":"litros","agua mineral":"litros","fruta para decorar":"kilos","jarras":"piezas","vitroleros":"piezas","mesas":"mesas","sillas":"piezas","salas lounge":"salas","barras":"piezas","centros de mesa":"piezas","bocinas":"piezas","micrófonos":"piezas","luces":"piezas","pantallas y proyectores":"piezas","vajillas":"juegos","menaje":"juegos","utensilios":"juegos","accesorios de mesa":"juegos"}).map(([k,v])=>[nrm(k),v]));
function unitFor(c,cat){const n=nrm(c).trim();if(!n)return"";if(UNIT_OF[n])return UNIT_OF[n];const k=Object.keys(UNIT_OF).find(k=>n.startsWith(k)||(n.length>3&&k.startsWith(n)));if(k)return UNIT_OF[k];
 if(cat==="Bebidas")return"litros";const C=catOf(cat);if(C&&C.full.some(x=>nrm(x)===n))return"servicio";if(["Música","Entretenimiento y shows","Audio, iluminación, foto y video"].includes(cat))return"horas";return"piezas";}
/* v18 · staff incluido: [perfil, 1 por cada N personas (0 = uno fijo), ¿ya marcado?] */
const CREW={"Banquete":[["Capitanes de meseros",0,1],["Meseros",15,1],["Cocineros",50,1],["Ayudantes de cocina",50,1],["Garroteros",50,0],["Bartenders",75,0],["Chefs",0,0]],
 "Buffet":[["Meseros",25,1],["Cocineros",75,1],["Capitanes de meseros",0,0],["Ayudantes de cocina",75,0],["Garroteros",50,0],["Bartenders",75,0]],
 "Cóctel":[["Meseros",20,1],["Cocineros",75,1],["Capitanes de meseros",0,0],["Ayudantes de cocina",75,0],["Bartenders",75,0]],
 "Estación de especialidad":[["Cocineros",75,1],["Ayudantes de cocina",100,1],["Taqueros",75,0],["Parrilleros",75,0],["Meseros",50,0]],
 drink:[["Bartenders",50,1],["Meseros",50,0],["Mixólogos",0,0],["Baristas",0,0],["Capitanes de meseros",0,0]]};
const NO_CREW=["Box lunch","Productos individuales"];
const crewable=o=>!NO_CREW.includes(o.n);
function crewList(o,s){if(o.kind==="drink")return CREW.drink;if(CREW[o.n])return CREW[o.n];const c=catOf(s&&s.cat);return((c&&c.staff)||[]).map(n=>[n,0,0]);}
const crewQ=(ratio,pax)=>ratio?String(Math.max(1,Math.ceil((+pax||EXG)/ratio))):"1";
/* v18 · otros servicios que pueden ir dentro de la ficha (categorías afines) */
const REL={food:["Bebidas","Mobiliario y montaje","Cristalería y cubertería","Decoración y ambientación","Música","Audio, iluminación, foto y video","Sustentabilidad y limpieza","Infraestructura"],
 drink:["Cristalería y cubertería","Mobiliario y montaje","Decoración y ambientación","Música"],
 gen:["Mobiliario y montaje","Decoración y ambientación","Audio, iluminación, foto y video","Infraestructura","Transporte"]};
const relEmo=c=>c==="Bebidas"?"🍹":((catOf(c)||{}).e||"✨");
function relList(o,s){return REL[o.kind].filter(c=>c!==s.cat&&(c==="Bebidas"||catOf(c)));}
function relSugg(c){if(c==="Bebidas")return[...DRINK_VARS];const C=catOf(c);return C?[...C.full,...C.rent]:[];}
function newRow(c){return{c:c||"",q:"",u:"",d:"",cj:""};}
function menuRows(n,kind){if(n==="Banquete")return[0,1,2,3].map(()=>({e:"",d:""}));return[{e:"",d:""}];}
function blankOffer(n,kind){kind=kind||"gen";const o={n,kind,name:"",pax:"",inc:[newRow()],svcs:[],crew:[],dur:kind==="gen"?"":"5",durU:"horas",tar:[{w:"full",price:"",u:kind==="gen"?"Por evento":"Por persona",uo:"",alc:""}],noStaff:false,ext:[],photos:[],min:blankMin(),promo:blankPromo(),
 tiempos:n==="Banquete"?menuRows(n):[],sal:kind==="food"&&n!=="Banquete"?menuRows():[],dul:kind==="food"&&n!=="Banquete"?menuRows():[],con:kind==="drink"?menuRows():[],sin:kind==="drink"?menuRows():[]};
 if(kind!=="gen"&&crewable(o))o.crew=crewList(o).filter(x=>x[2]).map(([c,r])=>({n:c,q:crewQ(r,o.pax),auto:true}));return o;}
const blankDlList=m=>m?[Object.assign(blankDl(m),{cobra:false})]:[];
function svcDefaults(s){if(!s.offers)s.offers=[];if(!s.staff)s.staff=[];if(!s.rent)s.rent=[];if(s.open===undefined)s.open="";if(s.descEdited===undefined)s.descEdited=filled(s.desc);
 if(!s.cater)s.cater={food:false,drink:false,gas:[]};if(s.askStaff===undefined)s.askStaff=s.staff.length?true:null;if(s.askRent===undefined)s.askRent=s.rent.length?true:null;
 if(!s.stx)s.stx={night:false,fee:"",dl:blankDlList("Servicio presencial en el evento"),dlOpen:-1,min:blankMin(),promo:blankPromo()};
 if(!s.rtx)s.rtx={dl:[],dlOpen:-1,min:blankMin(),promo:blankPromo()};if(!s.dl)s.dl=[];if(s.dlOpen===undefined)s.dlOpen=-1;
 s.ways={full:s.offers.length>0,staff:s.askStaff===true,rent:s.askRent===true};
 s.offers.forEach(o=>{if(!o.photos)o.photos=[];if(!o.kind)o.kind="gen";if(o.name===undefined)o.name="";if(!o.min)o.min=blankMin();if(!o.promo)o.promo=blankPromo();
  ["inc","ext"].forEach(L=>{o[L]=o[L]||[];o[L].forEach(r=>{if(r.c===undefined){r.c=r.u||r.w||"";r.u="";}if(r.d===undefined)r.d="";if(r.cj===undefined)r.cj="";});});
  o.tar=o.tar||[];o.tar.forEach(t=>{if(!t.w||t.w==="staff")t.w="full";if(!t.u)t.u="Por persona";if(t.uo===undefined)t.uo="";if(t.alc===undefined)t.alc="";});if(!o.tar.some(t=>t.w==="full"))o.tar.unshift({w:"full",price:"",u:"Por persona",uo:"",alc:""});
  if(o.pax===undefined)o.pax="";if(!o.svcs)o.svcs=[];if(!o.crew)o.crew=[];o.svcs.forEach(v=>{if(!v.rows||!v.rows.length)v.rows=[newRow()];});
  if(crewable(o))["rent","labor"].forEach(w=>{if(!o.tar.some(t=>t.w===w))o.tar.push({w,price:"",u:w==="labor"&&o.kind==="gen"?"Por evento":o.tar[0].u,uo:"",alc:""});});
  else o.tar=o.tar.filter(t=>t.w==="full");
  o.noStaff=o.tar.some(t=>t.w==="rent"&&filled(t.price));
  ["tiempos","sal","dul","con","sin"].forEach(L=>{o[L]=(o[L]||[]).map(r=>r.e!==undefined?r:{e:"",d:r.d||""});});});}
function tarUnitLabel(t){return t.u==="__otra"?(t.uo?"por "+t.uo.replace(/^por\s+/i,""):"otra unidad"):uLabel(t.u);}
const offTitle=o=>(o.kind==="drink"?"Bebidas · ":"")+o.n+(filled(o.name)?" · "+o.name:"");
const activeTar=o=>o.tar.filter(t=>t.w==="full"||filled(t.price));
const TAR_MODO={full:"completo",rent:"sin personal",labor:"solo personal"};
function tarLabels(o){const f=o.kind==="food"?"la comida":o.kind==="drink"?"las bebidas":"tu servicio";
 return{full:["🎉 Completo",`${f.charAt(0).toUpperCase()+f.slice(1)} + tu equipo y tu personal`],rent:["📦 Sin personal",o.kind==="gen"?"Solo el equipo; tu cliente lo opera":`Solo ${f}; lo llevas o lo recogen y tu cliente lo sirve`],labor:["🙋 Solo tu personal",o.kind==="gen"?"Tu gente trabaja con el equipo del cliente":"Tu equipo trabaja con los insumos del cliente"]};}
const ONE={"Capitanes de meseros":"Capitán de meseros","Meseros":"Mesero","Cocineros":"Cocinero","Ayudantes de cocina":"Ayudante de cocina","Bartenders":"Bartender","Garroteros":"Garrotero","Chefs":"Chef","Taqueros":"Taquero","Parrilleros":"Parrillero","Mixólogos":"Mixólogo","Baristas":"Barista","Reposteros":"Repostero","Sommeliers":"Sommelier"};
const crewText=o=>o.crew.filter(r=>filled(r.n)).map(r=>`${filled(r.q)?r.q+" ":""}${(r.q==="1"&&ONE[r.n]||r.n).toLowerCase()}`).join(", ");
const svcsText=o=>o.svcs.map(v=>{const t=rowsText(v.rows);return t?`${v.cat}: ${t}`:"";}).filter(Boolean).join(" · ");
function syncSubs(s){svcDefaults(s);const L=[];
 s.offers.forEach(o=>activeTar(o).forEach(t=>{if(t.u)L.push({n:offTitle(o),u:t.u,uo:t.uo||"",price:t.price,yieldP:t.alc||"",pkgP:t.alc||o.pax||"",pkgH:o.dur||"",unit:tarUnitLabel(t),modo:TAR_MODO[t.w]});}));
 if(s.ways.staff)s.staff.forEach(r=>L.push({n:r.n,u:r.u,uo:"",price:r.price,yieldP:"",pkgP:"",pkgH:r.min||"",unit:uLabel(r.u),modo:"staff"}));
 if(s.ways.rent)s.rent.forEach(r=>L.push({n:r.n,u:r.u,uo:"",price:r.price,yieldP:"",pkgP:"",pkgH:"",unit:uLabel(r.u),modo:"renta"}));
 s.subs=L;if(!s.descEdited)s.desc=autoDesc(s);}
function joinY(a){a=a.filter(Boolean);return a.length<2?a.join(""):a.slice(0,-1).join(", ")+" y "+a[a.length-1];}
function autoDesc(s){const p=[];const ns=[...new Set(s.offers.map(o=>o.kind==="drink"?"bebidas en "+o.n.toLowerCase():o.n.toLowerCase()))];if(ns.length)p.push(joinY(ns));if(s.ways.staff&&s.staff.length)p.push(joinY(s.staff.map(r=>r.n.toLowerCase())));if(s.ways.rent&&s.rent.length)p.push("renta de "+joinY(s.rent.map(r=>r.n.toLowerCase())));
 if(!p.length)return"";const g=isCat(s)&&s.cater.gas.length?` de cocina ${joinY(s.cater.gas.map(x=>x.toLowerCase()))}`:"";const t=joinY(p);return t.charAt(0).toUpperCase()+t.slice(1)+g+" para tu fiesta.";}
function rowsText(L){return L.filter(r=>filled(r.c)).map(r=>[filled(r.q)&&nrm(r.u)===nrm(r.c)?"":r.c,filled(r.q)?r.q+(filled(r.u)?" "+r.u:""):"",filled(r.cj)?`de ${r.cj} piezas`:"",filled(r.d)?`(${r.d.toLowerCase()})`:""].filter(Boolean).join(" ")).join(" · ");}
const rowTxt=r=>[r.e,r.d].filter(filled).join(": ");
function menuText(o){if(o.n==="Banquete")return o.tiempos.filter(t=>filled(t.d)||filled(t.e)).map((t,i)=>`${TIEMPO_N[i]||i+1} tiempo: ${t.d||t.e}`).join(" · ");
 const L=o.kind==="drink"?[...o.con,...o.sin]:[...o.sal,...o.dul];return L.filter(x=>filled(x.d)||filled(x.e)).map(x=>x.d||x.e).join(", ");}
const VAR=()=>+S.svcVar||0,HIGH=()=>S.svcHigh&&+S.svcHigh.pct>0?+S.svcHigh.pct:0;
function costAt(o,t,cat,g){return hqvCost({cat,sub:o.n,u:t.u,price:+t.price,guests:g,hours:+o.dur||EXH,rinde:t.alc,pkgP:t.alc});}
function offerHost(o,t,cat){if(!(+t.price>0))return"";
 if(t.u==="__otra")return`<span class="hv">👀 Unidad nueva: el anfitrión la verá tal cual y tú le confirmas el total.</span>`;
 const g=+o.pax||EXG,r=costAt(o,t,cat,g);if(r.pend)return`<span class="hv">👀 Dinos para cuántas personas alcanza y lo convertimos; si no, el anfitrión lo verá «por cotizar».</span>`;
 const pp=Math.round(r.total/g);
 return`<span class="hv">👀 En una fiesta de ${g} personas: <b>${money(pp)}</b> por persona · <b>${money(Math.round(r.total))}</b> en total</span>`;}
function offerOk(o){const F=o.tar.filter(t=>t.w==="full"),R=o.tar.filter(t=>t.w!=="full");const good=t=>!filled(t.price)||(t.u&&(t.u!=="__otra"||filled(t.uo)));
 return F.some(t=>filled(t.price))&&F.every(good)&&R.every(good)&&o.ext.every(e=>!filled(e.c)||filled(e.cost))&&(o.min.has!==true||minOk(o.min))&&(o.promo.has!==true||promoOk(o.promo));}
function staffOk(r){return filled(r.price)&&!!r.u;}
function offerSummary(o){const t=o.tar.find(x=>x.w==="full"&&filled(x.price));return[menuText(o)||rowsText(o.inc),t?`${money(t.price)} ${tarUnitLabel(t)}`:""].filter(Boolean).join(" · ");}
/* ---------- partes de la ficha ---------- */
const INS_PH={food:["platos","servilletas","mantelería"],drink:["vasos","hielo","popotes"],gen:["montaje","equipo","cables"]};
function rowsHtml(o,cost,sv){const L=sv?sv.rows:cost?o.ext:o.inc,cls=cost?"ex":"in",ph=sv?relSugg(sv.cat).slice(0,3).map(x=>x.toLowerCase()):INS_PH[o.kind]||INS_PH.gen,sg=sv?`rel:${sv.cat}`:cost?"inc":`ins:${o.kind}`,lbl=sv?"":"Insumo: ";
 return`<div class="rws" data-l="${sv?"sv:"+sv.cat:cls}">${L.map((r,ri)=>{const det=DETAIL[nrm(r.c||"").trim()];return`<div class="incr ${cls}" data-ri="${ri}"><input type="text" class="r-c" data-sg="${esc(sg)}" value="${esc(r.c)}" placeholder="${cost?"Extra: hora extra, pastel…":(sv?"Ej. ":lbl)+(ph[ri%Math.max(1,ph.length)]||"")}" aria-label="Concepto" autocomplete="off"><input type="number" inputmode="decimal" class="r-q" value="${esc(r.q)}" placeholder="#" aria-label="Cantidad"><input type="text" class="r-u" data-sg="u" value="${esc(r.u)}" placeholder="unidad" aria-label="Unidad" autocomplete="off">${cost?`<label class="r-m"><span>$</span><input type="number" min="0" class="r-cost${MISS(!filled(r.c)||filled(r.cost))}" value="${esc(r.cost)}" aria-label="Costo del extra"></label>`:""}<button type="button" class="link bad r-x" aria-label="Quitar renglón">✕</button>
  ${/caja/i.test(r.u||"")?`<label class="r-cj">cada caja de <input type="number" min="0" class="r-cjn" value="${esc(r.cj)}" placeholder="#" aria-label="Piezas por caja"> piezas</label>`:""}
  ${filled(r.c)?`<input type="text" class="r-d" data-sg="det:${esc(nrm(r.c).trim())}" value="${esc(r.d)}" placeholder="${det?"¿De qué tipo? "+det.slice(0,3).join(", ").toLowerCase()+"…":"¿De qué tipo? (opcional)"}" aria-label="Detalle" autocomplete="off">`:""}</div>`;}).join("")}
 <button type="button" class="link r-add" style="justify-self:start">+ ${cost?"Agregar extra":"Agregar otro"}</button></div>`;}
/* v18 · 🧩 otros servicios incluidos y 🙋 staff incluido */
function svcsHtml(o,s){const R=relList(o,s);if(!R.length)return"";
 return`<div class="incsec"><span class="mini-l">🧩 ¿Qué otros servicios incluye? <span class="opt">(opcional · elige y defínelos aquí mismo)</span></span>
  <div class="chips cmini">${R.map(c=>`<button type="button" class="chip rel-c" data-c="${esc(c)}" aria-pressed="${o.svcs.some(v=>v.cat===c)}">${TICK}${relEmo(c)} ${esc(c)}</button>`).join("")}</div>
  ${o.svcs.map(v=>`<div class="relbox" data-c="${esc(v.cat)}"><b class="relh">${relEmo(v.cat)} ${esc(v.cat)} <span class="opt">incluido en tu precio</span></b>${rowsHtml(o,false,v)}</div>`).join("")}</div>`;}
function crewHtml(o,s){if(!crewable(o))return"";const P=crewList(o,s),names=[...new Set([...P.map(x=>x[0]),...o.crew.map(r=>r.n)])];
 return`<div class="incsec"><span class="mini-l">🙋 ¿Qué staff incluye? <span class="opt">Ya marcamos lo indispensable · ya va dentro de tu precio</span></span>
  <div class="chips cmini">${names.map(n=>`<button type="button" class="chip crew-c" data-n="${esc(n)}" aria-pressed="${o.crew.some(r=>r.n===n)}">${TICK}${esc(n)}</button>`).join("")}<button type="button" class="chip new crew-new">✏️ Otro</button></div>
  <div class="newrow" hidden><input type="text" class="crew-in" data-sg="staff" placeholder="Ej. Sommelier, Parrillero…" aria-label="Otro perfil" autocomplete="off"><button type="button" class="btn sm crew-addb">Agregar</button></div>
  ${o.crew.length?`<div class="crewl">${o.crew.map((r,ri)=>`<label class="crewr" data-ri="${ri}"><span>${esc(r.n)}</span><input type="number" min="0" class="cr-q" value="${esc(r.q)}" placeholder="#" aria-label="¿Cuántos ${esc(r.n.toLowerCase())}?"></label>`).join("")}</div>
  <span class="hint">${o.kind!=="gen"?`Calculamos cuántos para ${+o.pax||EXG} personas; cámbialo si llevas otra cantidad.`:"¿Cuántas personas de cada perfil van?"}</span>`:""}</div>`;}
function tarGridHtml(o,s){const T=tarLabels(o),W=crewable(o)?["full","rent","labor"]:["full"];
 return`<span class="mini-l">💲 Tus tarifas <span class="opt">${W.length>1?"La primera es obligatoria; las otras, solo si también las ofreces":"Con todo lo que incluye"}</span></span>
  <div class="tgrid${W.length>1?"":" one"}">${W.map(w=>`<div class="tgrp tw-${w}"><b class="tw">${T[w][0]}${w==="full"?"":` <span class="opt">(opcional)</span>`}</b><span class="hint">${T[w][1]}</span>${tarRowsHtml(o,w,s)}</div>`).join("")}</div>`;}
function rowIdeas(scope,r){const e=espOf(scope,r.e);if(!e)return"";const used=new Set();return`<div class="ideas"><span>💡 Más ideas de ${esc(e.n.toLowerCase())}:</span>${e.d.filter(x=>nrm(x)!==nrm(r.d||"")).slice(0,6).map(x=>`<button type="button" class="idea" data-d="${esc(x)}">＋ ${esc(x)}</button>`).join("")}</div>`;}
function menuRowHtml(o,key,xi,r,scope,lead){const drink=o.kind==="drink";
 const phE=key==="tiempos"?`Especialidad: ${(TIEMPO_PH[xi]||["otro tiempo"])[0]}`:drink?(key==="con"?"Tipo: coctelería":"Tipo: aguas frescas"):(key==="dul"?"Especialidad: postres":"Especialidad: tacos");
 const phD=key==="tiempos"?`Platillo: ${(TIEMPO_PH[xi]||["",""])[1]||"tu platillo"}`:drink?(key==="con"?"Bebida: margarita":"Bebida: agua de jamaica"):(key==="dul"?"Platillo: churros":"Platillo: al pastor");
 return`<div class="mr" data-k="${key}" data-xi="${xi}">${lead?`<span class="tn">${lead}</span>`:""}<input type="text" class="m-e" data-sg="esp:${scope}" value="${esc(r.e)}" placeholder="${esc(phE)}" aria-label="Especialidad" autocomplete="off"><input type="text" class="m-d" data-sg="dish:${scope}" value="${esc(r.d)}" placeholder="${esc(phD)}" aria-label="Platillo" autocomplete="off"><button type="button" class="link bad m-x" aria-label="Quitar">✕</button>${rowIdeas(scope,r)}</div>`;}
function menuHtml(o){
 if(o.n==="Banquete")return`<span class="mini-l">🍴 Arma tu menú por tiempos <span class="opt">(opcional · escribe y te sugerimos)</span></span>
  ${o.tiempos.map((t,ti)=>menuRowHtml(o,"tiempos",ti,t,"Ambos",`${TIEMPO_N[ti]||ti+1}<br>tiempo`)).join("")}<button type="button" class="link m-add" data-k="tiempos" style="justify-self:start">+ Agregar tiempo</button>`;
 const seg=(key,tit,scope)=>`<div class="seg2"><b>${tit}</b>${o[key].map((x,xi)=>menuRowHtml(o,key,xi,x,scope,"")).join("")}<button type="button" class="link m-add" data-k="${key}" style="justify-self:start">+ Agregar</button></div>`;
 if(o.kind==="drink")return`<span class="mini-l">🍹 Arma tu menú de bebidas <span class="opt">(opcional · escribe y te sugerimos)</span></span>${seg("con","🍸 Con alcohol","Con alcohol")}${seg("sin","🧃 Sin alcohol","Sin alcohol")}`;
 if(o.kind==="food")return`<span class="mini-l">🍴 Arma tu menú <span class="opt">(opcional · escribe y te sugerimos)</span></span>${seg("sal","🧂 Salado","Salado")}${seg("dul","🍰 Dulce","Dulce")}`;
 return"";}
function tarRowsHtml(o,w,s){const T=o.tar.map((t,ti)=>[t,ti]).filter(([t])=>t.w===w);
 return`${T.map(([t,ti])=>`<div class="tarr" data-ti="${ti}"><label class="sl-p"><span>$</span><input type="number" min="0" step="any" class="ta-p${w==="full"?MISS(T.some(([x])=>filled(x.price))):""}" value="${esc(t.price)}" placeholder="precio" aria-label="Precio"></label>
  <select class="ta-u" aria-label="Cómo lo cobras">${U_FULL.map(u=>`<option value="${esc(u)}" ${t.u===u?"selected":""}>${esc(uLabel(u))}</option>`).join("")}<option value="__otra" ${t.u==="__otra"?"selected":""}>✏️ otra unidad…</option></select>
  ${t.u==="__otra"?`<input type="text" class="ta-uo${MISS(filled(t.uo))}" data-sg="u" value="${esc(t.uo)}" placeholder="por charola, por metro…" aria-label="Otra unidad" autocomplete="off">`:""}
  ${t.u!=="Por persona"?`<label class="ta-al">alcanza para <input type="number" min="0" class="ta-a" value="${esc(t.alc)}" placeholder="#" aria-label="Alcanza para cuántas personas"> personas</label>`:""}
  ${T.length>1?`<button type="button" class="link bad ta-x" aria-label="Quitar tarifa">✕</button>`:""}<div class="ta-hv">${offerHost(o,t,s.cat)}</div></div>`).join("")}
 ${w==="full"?`<button type="button" class="link ta-add" data-w="${w}" style="justify-self:start">+ Otra tarifa</button>`:""}`;}
function moreHtml(min,promo,k2,anchor,open){return`<details class="more"${open?" open":""}><summary>⚙️ Más opciones <span class="opt">(mínimo de compra y promoción)</span>${min.has===true?" · 🧾":""}${promo.has===true?" · 🏷️":""}</summary>${minHtml(min,k2)}${promoHtml(promo,k2,anchor)}</details>`;}
function offerCard(s,k,o,j){const open=s.open==="f"+j,ok=offerOk(o),emo=FMT_EMO[o.n]||(o.kind==="drink"?"🍹":"✨"),kj=`${k}o${j}`;
 if(!open)return`<div class="dlc closed ofc${MISS(ok)}" data-j="${j}"><button type="button" class="dlh of-open"><b>${emo}</b><span class="sm"><b style="color:#1a1033">${esc(offTitle(o))}</b> · ${esc(offerSummary(o)||"falta tu precio")}</span><span class="ed">${ok?"✏️ Editar":"⚠️ Completar"}</span></button><button type="button" class="ofx of-x" aria-label="Quitar ${esc(o.n)}">✕</button></div>`;
 const hasPrice=o.tar.some(t=>t.w==="full"&&filled(t.price)),multi=o.kind!=="gen";
 return`<div class="dlc open ofc${MISS(ok)}" data-j="${j}">
  <div class="dlh"><b>${emo} ${esc(o.kind==="drink"?"Bebidas · "+o.n:o.n)}</b><span class="sm"></span><button type="button" class="link bad of-x" aria-label="Quitar ${esc(o.n)}">✕ Quitar</button></div>
  ${multi?`<input type="text" class="of-name" value="${esc(o.name)}" placeholder="Nombre de este menú (opcional): ${o.n==="Banquete"?"Menú Plata, Menú Oro…":"Menú Clásico, Menú Premium…"}" aria-label="Nombre del menú">
  <label class="paxr"><span>👥 ¿Para cuántas personas está pensado?</span><input type="number" min="1" class="of-pax" value="${esc(o.pax)}" placeholder="Ej. 100" aria-label="Personas"> <span>personas</span></label>`:""}
  ${menuHtml(o)}
  <div class="incwrap"><span class="mini-l inct">✅ ¿Qué incluye tu ${esc(o.kind==="drink"?"servicio de bebidas":o.n.toLowerCase())}? <span class="opt">Todo esto ya va dentro de tu precio</span></span>
  <div class="incsec"><span class="mini-l">🧺 ¿Qué insumos incluye? <span class="opt">Escribe el insumo y la cantidad; la unidad te la ponemos</span></span>${rowsHtml(o,false)}</div>
  ${svcsHtml(o,s)}
  ${crewHtml(o,s)}</div>
  ${crewable(o)?`<div class="durr"><span class="mini-l" style="margin:0">⏱️ Duración del servicio</span><input type="number" min="0" step="any" class="of-dur" value="${esc(o.dur)}" placeholder="—" aria-label="Duración en horas"><span class="durh">horas</span></div>
  <span class="hint arrive">⏰ Como proveedor, entiendo que llego <b>1 hora antes</b> para montar y tengo <b>1 hora al terminar</b> para retirarme${+o.dur>0?`: con ${esc(o.dur)} h de servicio estaré <b>${+o.dur+2} h</b> en el evento`:""}.</span>`:""}
  ${tarGridHtml(o,s)}
  ${hasPrice?`<span class="mini-l">➕ Extras <span class="opt">(opcional · lo que el anfitrión puede sumar con costo)</span></span>${o.ext.length?rowsHtml(o,true):`<button type="button" class="link r-add" data-l="ex" style="justify-self:start">+ Agregar extra</button>`}
  <span class="mini-l">📷 Fotos de ${esc(o.n.toLowerCase())} <span class="opt">(opcional · salen grandes en tu sitio)</span></span>${uploaderHtml(kj,"photo",o.photos,true)}
  ${moreHtml(o.min,o.promo,kj,`s${k.slice(1)}-${j}`,o.min.has===true||o.promo.has===true)}`:`<span class="hint">Pon tu precio y te mostramos extras, fotos y más opciones.</span>`}
  ${multi?`<button type="button" class="link of-dup" style="justify-self:start">+ Otro menú de ${esc(o.kind==="drink"?"bebidas en "+o.n.toLowerCase():o.n.toLowerCase())}</button>`:""}
  ${ok?`<button type="button" class="btn cta sm dl-ok of-ok">Listo ✓</button>`:""}</div>`;}
/* entrega por sección: A domicilio / Recoger en mi local primero */
const DL_MAIN={full:["Envío a domicilio","Recolección en establecimiento","Servicio presencial en el evento"],st:["Servicio presencial en el evento"],rt:["Envío a domicilio","Recolección en establecimiento"]};
const DL_LABEL={"Envío a domicilio":"A domicilio","Recolección en establecimiento":"Recoger en mi local","Servicio presencial en el evento":"Lo sirvo en el evento"};
function dlSecHtml(sx,k2,sec,title){const main=DL_MAIN[sec],L=sx.dl,more=sx._more||L.some(d=>!main.includes(d.m));
 const mods=DL_MODS.filter(([m])=>main.includes(m)||more);
 return`<div class="dlsec" data-sec="${sec}"><span class="mini-l">🚚 ${title}</span>
  <div class="chips dlm-chips${MISS(L.length>0)}" style="border-radius:14px">${mods.map(([m,e])=>`<button type="button" class="chip dlm" data-m="${esc(m)}" aria-pressed="${L.some(d=>d.m===m)}">${TICK}${e} ${esc(DL_LABEL[m]||m)}</button>`).join("")}${more?"":`<button type="button" class="chip new dl-more">Más formas ▾</button>`}</div>
  ${L.map((d,j)=>dlCard(sx,k2,d,j)).join("")}</div>`;}
function bindDlSec(box,sec,sx,k2,redraw){const el=box.querySelector(`.dlsec[data-sec="${sec}"]`);if(!el)return;bindDl(sx,k2,el,redraw);const m=el.querySelector(".dl-more");if(m)m.onclick=()=>{sx._more=true;redraw();};}
function listSecHtml(s,k,cat,list){const st=list==="staff",X=st?s.stx:s.rtx,ask=st?s.askStaff:s.askRent,L=s[list],open=s.open===(st?"st":"rt"),ok=L.length&&L.every(staffOk);
 const q=st?`<b>🙋 ¿Tu equipo también trabaja con los insumos del cliente?</b><span class="hint" style="display:block">Aquí cobras solo su trabajo: cocinar, servir, preparar bebidas. Los ingredientes y el equipo los pone el cliente.</span>`
  :`<b>📦 ¿También rentas artículos o equipo sin operarlos?</b><span class="hint" style="display:block">Chafers, vitroleros, equipo de cocina… lo entregas o lo recogen, sin tu personal.</span>`;
 const head=`<div class="nsr">${`<span>${q}</span>`}${ynHtml(`${st?"ask-st":"ask-rt"}-${k}`,ask)}</div>`;
 if(ask!==true)return`<div class="field inv">${head}</div>`;
 if(!open&&L.length)return`<div class="field inv">${head}<div class="dlc closed ofc${MISS(ok)}"><button type="button" class="dlh ${st?"st":"rt"}-open"><b>${st?"🙋":"📦"}</b><span class="sm"><b style="color:#1a1033">${st?"Staff":"Renta"}</b> · ${esc(L.map(r=>r.n+(filled(r.price)?` ${money(r.price)} ${uLabel(r.u)}`:"")).join(" · "))}</span><span class="ed">${ok?"✏️ Editar":"⚠️ Completar"}</span></button></div></div>`;
 const names=[...new Set([...(cat?cat[list]:[]),...L.map(r=>r.n)])],U=st?U_STAFF:U_RENT,sec=st?"st":"rt";
 return`<div class="field inv">${head}<div class="dlc open ofc${MISS(ok)}">
  <div class="chips cmini">${names.map(n=>`<button type="button" class="chip ${sec}-c" data-n="${esc(n)}" aria-pressed="${L.some(r=>r.n===n)}">${TICK}${esc(n)}</button>`).join("")}<button type="button" class="chip new ${sec}-new">✏️ Otro</button></div>
  <div class="newrow" hidden><input type="text" class="${sec}-in" data-sg="${st?"staff":"full"}" placeholder="${st?"Ej. Taquero, Bartender…":"Ej. Pista de baile iluminada"}" aria-label="Otro" autocomplete="off"><button type="button" class="btn sm ${sec}-addb">Agregar</button></div>
  ${L.map((r,ri)=>`<div class="lrow ${sec}-r" data-ri="${ri}"><b class="rn">${esc(r.n)}</b><label class="sl-p"><span>$</span><input type="number" min="0" class="sr-p${MISS(filled(r.price))}" value="${esc(r.price)}" placeholder="precio" aria-label="Precio de ${esc(r.n)}"></label><select class="sr-u" aria-label="Cómo lo cobras">${U.map(([u,t])=>`<option value="${u}" ${r.u===u?"selected":""}>${t}</option>`).join("")}</select>${st?`<label class="ta-al lm">mín. <input type="number" min="0" class="sr-m" value="${esc(r.min)}" placeholder="#" aria-label="Horas mínimas"> h</label><label class="ta-al lx">extra $<input type="number" min="0" class="sr-x" value="${esc(r.xh)}" placeholder="#" aria-label="Costo de hora extra"></label>`:""}<button type="button" class="link bad sr-rm" aria-label="Quitar">✕</button></div>`).join("")}
  ${st?`<label class="nightc"><input type="checkbox" class="st-night" ${X.night?"checked":""}> <span>🌙 Si la jornada de mi personal termina después de las 12:00 a.m., el anfitrión cubre su transporte${X.night?`: <input type="number" min="0" class="st-fee" value="${esc(X.fee)}" placeholder="$" aria-label="Monto por persona"> por persona`:""}.</span></label>`:""}
  ${dlSecHtml(X,k+sec,sec,st?"¿Cómo llega tu personal?":"¿Cómo entregas lo que rentas?")}
  ${moreHtml(X.min,X.promo,k+sec,`s${k.slice(1)}-${sec}`,X.min.has===true||X.promo.has===true)}
  ${ok?`<button type="button" class="btn cta sm dl-ok of-ok">Listo ✓</button>`:""}</div></div>`;}
function addOffer(s,n,kind){svcDefaults(s);let j=s.offers.findIndex(o=>o.n===n&&o.kind===(kind||"gen"));if(j<0){s.offers.push(blankOffer(n,kind));j=s.offers.length-1;}s.open="f"+j;}
function addPerson(s,list,n,u){svcDefaults(s);if(!s[list].some(r=>r.n===n))s[list].push({n,price:"",u,min:list==="staff"?"5":"",xh:""});if(list==="staff")s.askStaff=true;else s.askRent=true;s.open=list==="staff"?"st":"rt";}
function boxFor(cat){let i=S.services.findIndex(s=>s.cat===cat);if(i<0){i=S.services.findIndex(s=>!s.cat);if(i<0){S.services.push(blankSvc());i=S.services.length-1;}S.services[i].cat=cat;}svcDefaults(S.services[i]);return i;}
function priceBoxHtml(){const h=S.svcHigh;return`<div class="field pricebox"><span class="lbl">💸 Ajustes para todos tus precios <span class="opt">Aplican a todo tu catálogo</span></span>
  <div class="sub-box" style="display:grid;gap:10px">
   <div class="varr"><span><b>¿Cuánto puede variar tu precio al negociar?</b><span class="hint" style="display:block">El anfitrión ve precios estandarizados de la comunidad. Lo que pongas aquí es tu margen al platicar y queda bajo tu responsabilidad. Recomendamos <b>±20%</b>.</span></span><label class="pmf"><span>±</span><input type="number" min="0" max="100" id="svcVar" class="${MISS(filled(S.svcVar))}" value="${esc(S.svcVar)}" aria-label="Variabilidad en porcentaje"><span>%</span></label></div>
   <div class="varr"><span><b>🔥 En temporada alta cobro</b><span class="hint" style="display:block">Calendario estándar ¡Hay que vernos! (bodas, XV y posadas). Edítalo si tu temporada es otra. Pon 0 si cobras igual todo el año.</span></span><label class="pmf"><span>+</span><input type="number" min="0" max="100" id="svcHigh" value="${esc(h.pct)}" aria-label="Aumento en temporada alta"><span>%</span></label></div>
   ${+h.pct>0?`<div class="chips cmini months">${MONTHS.map(([m,t])=>`<button type="button" class="chip mo" data-m="${m}" aria-pressed="${h.months.includes(m)}">${TICK}${t}</button>`).join("")}</div>`:""}
  </div></div>`;}
function bindPriceBox(redraw){const v=$("svcVar");if(v)v.oninput=e=>{S.svcVar=e.target.value;document.querySelectorAll(".pm").forEach(x=>x.textContent="± "+(+S.svcVar||0)+"%");changed();};
 const h=$("svcHigh");if(h){h.oninput=e=>{S.svcHigh.pct=e.target.value;changed();};h.onchange=()=>redraw();}
 document.querySelectorAll(".mo").forEach(c=>c.onclick=()=>{const m=c.dataset.m,M=S.svcHigh.months;S.svcHigh.months=M.includes(m)?M.filter(x=>x!==m):MONTHS.map(x=>x[0]).filter(x=>x===m||M.includes(x));c.setAttribute("aria-pressed",S.svcHigh.months.includes(m));changed();});}
const VIATICOS=`<span class="hint viat">🚗 Si hay viáticos o costos adicionales por traslado fuera de tu zona, se acuerdan en la conversación directa con el anfitrión.</span>`;
/* ---------- paquetes ---------- */
function pkgItems(){const out=[];S.services.forEach((s,i)=>{svcDefaults(s);if(!catOf(s.cat))return;s.offers.forEach((o,j)=>out.push({key:`o${i}-${j}`,n:offTitle(o),s,o}));if(s.ways.staff)s.staff.forEach((r,j)=>out.push({key:`s${i}-${j}`,n:r.n,s,r,st:true}));if(s.ways.rent)s.rent.forEach((r,j)=>out.push({key:`r${i}-${j}`,n:r.n,s,r}));});return out;}
function itemCost(it,g){if(it.o){const t=it.o.tar.find(x=>x.w==="full"&&filled(x.price));if(!t)return 0;const r=costAt(it.o,t,it.s.cat,g);return r.pend?0:r.total;}
 const p=+it.r.price||0;return it.st?p*(it.r.u==="Por hora"?(+it.r.min||5):1):p;}
function pkgSuggest(P){const g=+P.alc||EXG,items=pkgItems().filter(it=>P.items.includes(it.key));const tot=items.reduce((a,it)=>a+itemCost(it,g),0);return P.per==="persona"?Math.round(tot/g):Math.round(tot);}
function pkgHtml(){const L=S.svcPkgs,items=pkgItems();if(!items.length)return"";
 return`<div class="field"><span class="lbl">🎁 Arma tus paquetes <span class="opt">(opcional · salen primero en tu sitio)</span></span>
  ${L.map((P,pi)=>{const sug=pkgSuggest(P);return`<div class="pkgc" data-pi="${pi}"><div class="row"><input type="text" class="pk-n${MISS(filled(P.name))}" value="${esc(P.name)}" placeholder="Nombre: Paquete Fiesta Mexicana" aria-label="Nombre del paquete"><button type="button" class="link bad pk-x">✕ Quitar</button></div>
   <span class="mini-l">¿Qué incluye este paquete?</span><div class="chips cmini">${items.map(it=>`<button type="button" class="chip pk-it" data-k="${it.key}" aria-pressed="${P.items.includes(it.key)}">${TICK}${esc(it.n)}</button>`).join("")}</div>
   <div class="tarr"><span class="ta-al">para</span><label class="ta-al"><input type="number" min="1" class="pk-al" value="${esc(P.alc)}" aria-label="Personas"> personas</label><label class="sl-p"><span>$</span><input type="number" min="0" class="pk-p${MISS(filled(P.price))}" value="${esc(P.price)}" placeholder="${sug||"precio"}" aria-label="Precio del paquete"></label><select class="pk-per" aria-label="Cómo se cobra"><option value="evento" ${P.per==="evento"?"selected":""}>por evento</option><option value="persona" ${P.per==="persona"?"selected":""}>por persona</option></select>
    <div class="ta-hv"><span class="hv">💡 Precio sugerido con tus tarifas: <b>${money(sug)}</b> ${P.per==="persona"?"por persona":"por evento"}${filled(P.price)&&+P.price<sug?` · ahorro para tu cliente <b>${money(sug-+P.price)}</b>`:""} <button type="button" class="link pk-use">Usar sugerido</button></span></div></div>
   <span class="mini-l">📷 Fotos del paquete <span class="opt">(opcional)</span></span>${uploaderHtml("pk"+pi,"photo",P.photos,true)}</div>`;}).join("")}
  <button type="button" class="btn ghost sm" id="pkAdd" style="width:fit-content">+ Armar un paquete</button></div>`;}
function bindPkgs(redraw){const a=$("pkAdd");if(a)a.onclick=()=>{S.svcPkgs.push({name:"",items:pkgItems().slice(0,3).map(x=>x.key),alc:"50",price:"",per:"evento",photos:[]});redraw();changed();};
 document.querySelectorAll(".pkgc").forEach(C=>{const P=S.svcPkgs[+C.dataset.pi],q=x=>C.querySelector(x);
  q(".pk-n").oninput=e=>{P.name=e.target.value;changed();};q(".pk-x").onclick=()=>{S.svcPkgs.splice(+C.dataset.pi,1);redraw();changed();};
  C.querySelectorAll(".pk-it").forEach(b=>b.onclick=()=>{const k=b.dataset.k;P.items=P.items.includes(k)?P.items.filter(x=>x!==k):[...P.items,k];redraw();changed();});
  q(".pk-al").onchange=e=>{P.alc=e.target.value;redraw();changed();};q(".pk-p").oninput=e=>{P.price=e.target.value;changed();};q(".pk-per").onchange=e=>{P.per=e.target.value;redraw();changed();};
  q(".pk-use").onclick=()=>{P.price=String(pkgSuggest(P));redraw();changed();};
  bindUploader("pk"+C.dataset.pi,"photo",P.photos,redraw);});}
/* ---------- escritura predictiva ---------- */
function sgList(inp){const k=inp.dataset.sg;
 if(k.startsWith("esp:"))return ESP[k.slice(4)].map(x=>x.n);
 if(k.startsWith("dish:")){const sc=k.slice(5),row=inp.closest(".mr"),e=row&&espOf(sc,row.querySelector(".m-e").value);return e?[...e.d,...DISHES[sc]]:DISHES[sc];}
 if(k.startsWith("det:"))return DETAIL[k.slice(4)]||[];
 if(k.startsWith("ins:"))return[...INSUMOS[k.slice(4)]||INC_SUGG,...INC_SUGG];
 if(k.startsWith("rel:"))return relSugg(k.slice(4));
 return k==="inc"?INC_SUGG:k==="u"?UNIT_SUGG:k==="staff"?[...new Set(CAT2.flatMap(c=>c.staff))]:k==="full"?[...new Set(CAT2.flatMap(c=>[...c.full,...c.rent]))]:[];}
(function(){let box=null,cur=null;const hide=()=>{if(box)box.hidden=true;};
 const show=inp=>{const v=nrm(inp.value).trim(),L=sgList(inp),res=[],seen=new Set();
  const spec=inp.dataset.sg.startsWith("dish:")||inp.dataset.sg.startsWith("det:");if(v.length<2&&!(spec&&!v)){hide();return;}
  for(const x of L){const n=nrm(x);if(seen.has(n))continue;seen.add(n);if(!v)res.push([0,x]);else if(n.startsWith(v))res.push([0,x]);else if(n.includes(v))res.push([1,x]);if(res.length>60)break;}
  res.sort((a,b)=>a[0]-b[0]);const top=res.slice(0,6).map(r=>r[1]).filter(x=>nrm(x)!==v);if(!top.length||(!v&&!(inp.dataset.sg.startsWith("det:")||(inp.closest(".mr")&&espOf(inp.dataset.sg.slice(5),inp.closest(".mr").querySelector(".m-e").value))))){hide();return;}
  if(!box){box=document.createElement("div");box.className="sgf";document.body.appendChild(box);}
  box.innerHTML=top.map(x=>`<button type="button">${esc(x)}</button>`).join("");const r=inp.getBoundingClientRect();box.style.left=(r.left+scrollX)+"px";box.style.top=(r.bottom+scrollY+4)+"px";box.style.minWidth=Math.max(180,r.width)+"px";box.hidden=false;cur=inp;
  box.querySelectorAll("button").forEach(b=>b.onmousedown=e=>{e.preventDefault();cur.value=b.textContent;cur.dispatchEvent(new Event("input",{bubbles:true}));cur.dispatchEvent(new Event("change",{bubbles:true}));hide();});};
 document.addEventListener("input",e=>{if(e.target.dataset&&e.target.dataset.sg)show(e.target);});
 document.addEventListener("focusin",e=>{const t=e.target;if(t.dataset&&t.dataset.sg&&(t.dataset.sg.startsWith("dish:")||t.dataset.sg.startsWith("det:")))show(t);const r=t.closest&&t.closest(".mr");document.querySelectorAll(".mr.act").forEach(x=>{if(x!==r)x.classList.remove("act");});if(r)r.classList.add("act");});
 document.addEventListener("focusout",e=>{if(e.target.dataset&&e.target.dataset.sg)setTimeout(hide,120);});
 addEventListener("scroll",hide,{passive:true});})();
/* ---------- sitio público ---------- */
function svcPlist(s){svcDefaults(s);const v=+S.svcVar||0,out=[];
 s.offers.forEach(o=>{const t=activeTar(o).filter(x=>filled(x.price));const m=menuText(o),inc=rowsText(o.inc),sv=svcsText(o),cr=crewText(o),TL={full:"Completo",rent:"Sin personal",labor:"Solo personal"};
  out.push(`<span class="po${o.photos.length?" hasph":""}">${o.photos.length?`<img class="phbig" src="${o.photos[0].url||o.photos[0]}" alt="">`:""}<span class="pob"><span class="poh"><b>${FMT_EMO[o.n]||"✨"} ${esc(o.kind!=="gen"&&filled(o.name)?o.name:o.n)}<small class="ctag">${esc(o.kind==="drink"?"Bebidas · "+o.n:o.n)}${filled(o.pax)?` · para ${esc(o.pax)} personas`:""}${crewable(o)&&+o.dur>0?` · ${esc(o.dur)} h`:""}</small></b> <span class="price">${t.length?t.map(x=>`<span class="pl">${t.length>1?`<small>${TL[x.w]}:</small> `:""}${money(x.price)} <small>${esc(tarUnitLabel(x))}${+x.alc>0?` · ${esc(x.alc)} personas`:""}</small></span>`).join(""):"<small>Por cotizar</small>"}${v&&t.length?`<span class="pl"><small class="pmv">± ${v}%</small></span>`:""}</span></span>${m?`<small class="inc">🍴 Menú: ${esc(m)}</small>`:""}${inc?`<small class="inc">🧺 Incluye: ${esc(inc)}</small>`:""}${sv?`<small class="inc">🧩 ${esc(sv)}</small>`:""}${cr?`<small class="inc">🙋 Staff: ${esc(cr)}</small>`:""}${o.ext.some(e=>filled(e.c))?`<small class="inc">Extras: ${esc(o.ext.filter(e=>filled(e.c)).map(e=>rowsText([e])+(filled(e.cost)?" "+money(e.cost):"")).join(" · "))}</small>`:""}${o.min.has===true&&minText(o.min)?`<small class="inc">🧾 ${esc(minText(o.min))}</small>`:""}${o.promo.has===true&&o.promo.what?`<small class="inc">🏷️ ${esc(o.promo.what)}</small>`:""}${o.photos.length>1?`<span class="pph">${o.photos.slice(1,5).map(p=>`<img src="${p.url||p}" alt="">`).join("")}</span>`:""}</span></span>`);});
 if(s.ways.staff&&s.staff.length)out.push(`<span class="po"><span class="pob"><span class="poh"><b>🙋 Staff</b> <span class="price">${s.staff.map(r=>`${esc(r.n)} ${filled(r.price)?money(r.price):""} <small>${esc(uLabel(r.u))}${filled(r.xh)?` · hora extra ${money(r.xh)}`:""}</small>`).join(" · ")}</span></span>${s.stx.night?`<small class="inc">🌙 Si la jornada termina después de las 12:00 a.m., el anfitrión cubre el transporte del personal${filled(s.stx.fee)?` (${money(s.stx.fee)} por persona)`:""}.</small>`:""}</span></span>`);
 if(s.ways.rent&&s.rent.length)out.push(`<span class="po"><span class="pob"><span class="poh"><b>📦 Renta</b> <span class="price">${s.rent.map(r=>`${esc(r.n)} ${filled(r.price)?money(r.price):""} <small>${esc(uLabel(r.u))}</small>`).join(" · ")}</span></span>${s.rtx.dl.length?`<small class="inc">${esc(s.rtx.dl.map(d=>dlText(d)).join(" · "))}</small>`:""}</span></span>`);
 return out.join("");}
function pkgSite(){const L=(S.svcPkgs||[]).filter(P=>filled(P.name)&&filled(P.price));if(!L.length)return"";const I=pkgItems();
 return`<div class="ms-item pkgsite"><div class="ms-item-top"><b>🎁 Paquetes</b></div><div class="plist">${L.map(P=>`<span class="po${P.photos.length?" hasph":""}">${P.photos.length?`<img class="phbig" src="${P.photos[0].url||P.photos[0]}" alt="">`:""}<span class="pob"><span class="poh"><b>${esc(P.name)}</b><span class="price">${money(P.price)} <small>${P.per==="persona"?"por persona":"por evento"} · ${esc(P.alc)} personas</small></span></span><small class="inc">Incluye: ${esc(I.filter(it=>P.items.includes(it.key)).map(it=>it.n).join(" · "))}</small></span></span>`).join("")}</div></div>`;}
/* ---------- paso de servicios ---------- */
function drawServices(){const list=$("svcList");if(!list)return;const ae=document.activeElement;if(ae&&list.contains(ae))ae.blur();const sc=S.svcScope||{};
 list.innerHTML=S.services.map((s,i)=>{svcDefaults(s);const cat=catOf(s.cat),k="s"+i,fl=FLASH&&FLASH.i===i?FLASH.msg:"";
 const EMP=["Tecnología","Marketing y comunicación","Exposición y negocios","Registro y protocolo","Permisos y trámites"];
 const order=CAT2.slice().sort((a,b)=>sc.E&&!sc.S?(EMP.includes(b.n)?1:0)-(EMP.includes(a.n)?1:0):0);
 const cater=isCat(s),fulls=cat&&!cater?[...new Set([...(cat.full||[]),...s.offers.map(o=>o.n)])]:[];
 const priced=s.offers.some(o=>o.tar.some(t=>filled(t.price)));
 const sec=kind=>s.offers.map((o,j)=>[o,j]).filter(([o])=>o.kind===kind);
 const chips=(kind,list)=>`<div class="chips${MISS(sec(kind).length>0)}" style="border-radius:14px">${list.map(n=>`<button type="button" class="chip fmt" data-k="${kind}" data-n="${esc(n)}" aria-pressed="${s.offers.some(o=>o.kind===kind&&o.n===n)}">${TICK}${FMT_EMO[n]?FMT_EMO[n]+" ":""}${esc(n)}</button>`).join("")}<button type="button" class="chip new of-new">✏️ Otro</button></div>
   <div class="newrow" hidden><input type="text" class="of-in" data-k="${kind}" ${kind==="gen"?'data-sg="full"':""} placeholder="¿Cómo se llama?" aria-label="Otro" autocomplete="off"><button type="button" class="btn sm of-addb">Agregar</button></div>
   ${sec(kind).map(([o,j])=>offerCard(s,k,o,j)).join("")}`;
 return`<div class="box" data-i="${i}"><div class="box-head"><h3>${cat?cat.e+" "+esc(cat.n):"Ficha "+(i+1)}</h3><span style="display:flex;gap:14px">${cat?`<button type="button" class="link ch-cat">Cambiar categoría</button>`:''}${S.services.length>1?`<button type="button" class="link bad rm-svc">Quitar</button>`:''}</span></div>
 ${fl?`<div class="flash">${esc(fl)}</div>`:''}
 ${!cat?`<div class="field"><span class="lbl">1. Elige tu categoría</span><div class="cats big${MISS(!!cat)}">${order.map(c=>{const used=S.services.some((y,ii)=>ii!==i&&y.cat===c.n);return`<button type="button" class="cat" data-c="${esc(c.n)}" aria-pressed="${s.cat===c.n}"><span class="emo">${c.e}</span><span>${esc(c.n)}${used?' <small>· ya la tienes</small>':''}</span></button>`;}).join("")}</div></div>`:''}
 ${cat&&cater?`<div class="field"><span class="lbl">¿Qué sirves?</span><div class="ways two${MISS(s.cater.food||s.cater.drink)}">${[["food","🍽️","Alimentos"],["drink","🍹","Bebidas"]].map(([x,e,t])=>`<button type="button" class="way ct" data-x="${x}" aria-pressed="${!!s.cater[x]}"><span class="emo">${e}</span><b>${t}</b></button>`).join("")}</div></div>
   ${s.cater.food?`<div class="field sub2"><span class="lbl">🍽️ Alimentos</span>
    <span class="mini-l">🌎 Tu cocina <span class="opt">Aplica a todos tus formatos</span></span><div class="chips cmini">${GASTROS.map(g=>`<button type="button" class="chip gas" data-g="${esc(g)}" aria-pressed="${s.cater.gas.includes(g)}">${TICK}${esc(g)}</button>`).join("")}</div>
    <span class="mini-l">¿En qué formatos lo sirves? <span class="opt">Cada uno se arma con servicio completo</span></span>${chips("food",FOOD_FMT)}</div>`:""}
   ${s.cater.drink?`<div class="field sub2"><span class="lbl">🍹 Bebidas</span><span class="mini-l">¿Cómo las sirves?</span>${chips("drink",DRINK_FMT)}</div>`:""}`:""}
 ${cat&&!cater?`<div class="field"><span class="lbl">¿Qué ofreces? <span class="opt">Servicio completo: tu servicio, tu equipo y tu personal</span></span>${chips("gen",fulls)}</div>`:""}
 ${cat&&s.offers.length?dlSecHtml(s,k,"full","¿Cómo entregas tu servicio completo?"):""}
 ${cat&&!cater&&(cat.staff||[]).length&&(s.offers.length||s.askStaff!==null)?listSecHtml(s,k,cat,"staff"):""}
 ${cat&&(cat.rent||[]).length&&(s.offers.length||s.askRent!==null)?listSecHtml(s,k,cat,"rent"):""}
 ${priced?`<div class="field"><label class="lbl" for="d-${k}">💬 Descríbelo en una frase <span class="opt">${s.descEdited?"":"✨ te la escribimos; cámbiala si quieres"}</span></label><input type="text" id="d-${k}" class="${MISS(filled(s.desc))}" value="${esc(s.desc)}" placeholder="Qué incluye y para cuántas personas"></div>`:""}
 </div>`;}).join("");
 FLASH=null;
 list.querySelectorAll(".box").forEach(el=>{const i=+el.dataset.i,s=S.services[i],k="s"+i,redraw=()=>{syncSubs(s);const y=scrollY;drawServices();scrollTo({top:y});},cat=catOf(s.cat);
  const on=(sel,f)=>el.querySelectorAll(sel).forEach(x=>x.onclick=ev=>{f(x,ev);redraw();changed();});
  el.querySelectorAll(".cat").forEach(t=>t.onclick=()=>{const c=t.dataset.c;const o=S.services.findIndex((y,ii)=>ii!==i&&y.cat===c);
   if(o>=0){S.services.splice(i,1);goBox(o>i?o-1:o,"Ya tenías esta categoría; aquí está.");return;}
   s.cat=c;s.offers=[];s.staff=[];s.rent=[];s.askStaff=null;s.askRent=null;s.cater={food:false,drink:false,gas:[]};redraw();changed();});
  const chc=el.querySelector(".ch-cat");if(chc)chc.onclick=()=>{s.cat="";redraw();changed();};
  on(".ct",x=>{const c=x.dataset.x;s.cater[c]=!s.cater[c];if(!s.cater[c])s.offers=s.offers.filter(o=>o.kind!==c);});
  el.querySelectorAll(".gas").forEach(b=>b.onclick=()=>{const g=b.dataset.g;s.cater.gas=s.cater.gas.includes(g)?s.cater.gas.filter(x=>x!==g):[...s.cater.gas,g];b.setAttribute("aria-pressed",s.cater.gas.includes(g));if(!s.descEdited){s.desc=autoDesc(s);const d=$("d-"+k);if(d)d.value=s.desc;}changed();});
  on(".fmt",x=>{const n=x.dataset.n,kd=x.dataset.k;if(s.offers.some(o=>o.n===n&&o.kind===kd)){s.offers=s.offers.filter(o=>!(o.n===n&&o.kind===kd));s.open="";}else addOffer(s,n,kd);});
  el.querySelectorAll(".of-new,.st-new,.rt-new").forEach(b=>b.onclick=()=>{const r=b.closest(".field,.dlc").querySelector(".newrow");r.hidden=false;r.querySelector("input").focus();});
  const addNew=(inp,f)=>{const v=(inp.value||"").trim();if(!v)return;NEW_SUBS.add(v);hqvTrack("catalogo_propuesta",{tipo:"servicio",cat:s.cat,valor:v});f(v);redraw();changed();};
  el.querySelectorAll(".of-in").forEach(inp=>{const b=inp.nextElementSibling,f=v=>addOffer(s,v,inp.dataset.k);b.onclick=()=>addNew(inp,f);inp.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();addNew(inp,f);}};});
  [[".st-in",".st-addb",v=>addPerson(s,"staff",v,"Por hora")],[".rt-in",".rt-addb",v=>addPerson(s,"rent",v,"Por pieza")]].forEach(([iq,bq,f])=>{const inp=el.querySelector(iq),b=el.querySelector(bq);if(!inp)return;b.onclick=()=>addNew(inp,f);inp.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();addNew(inp,f);}};});
  on(".of-open",x=>{s.open="f"+x.closest(".ofc").dataset.j;});on(".st-open",()=>{s.open="st";});on(".rt-open",()=>{s.open="rt";});on(".of-ok",()=>{s.open="";});
  el.querySelectorAll(".ofc.closed .ofx").forEach(b=>b.onclick=()=>{const j=+b.closest(".ofc").dataset.j;confirmX(`¿Quitar ${offTitle(s.offers[j])}?`,()=>{s.offers.splice(j,1);s.open="";redraw();changed();});});
  bindYN(`ask-st-${k}`,v=>{s.askStaff=v;s.open=v?"st":"";redraw();changed();});bindYN(`ask-rt-${k}`,v=>{s.askRent=v;s.open=v?"rt":"";redraw();changed();});
  on(".st-c",x=>{const n=x.dataset.n,j=s.staff.findIndex(r=>r.n===n);if(j>=0)s.staff.splice(j,1);else s.staff.push({n,price:"",u:"Por hora",min:"5",xh:""});});
  on(".rt-c",x=>{const n=x.dataset.n,j=s.rent.findIndex(r=>r.n===n);if(j>=0)s.rent.splice(j,1);else s.rent.push({n,price:"",u:"Por pieza",min:""});});
  el.querySelectorAll(".st-r,.rt-r").forEach(R=>{const st=R.classList.contains("st-r"),L=st?s.staff:s.rent,r=L[+R.dataset.ri];R.querySelector(".sr-p").oninput=e=>{r.price=e.target.value;syncSubs(s);changed();};R.querySelector(".sr-u").onchange=e=>{r.u=e.target.value;redraw();changed();};
   const m=R.querySelector(".sr-m");if(m)m.oninput=e=>{r.min=e.target.value;changed();};const x=R.querySelector(".sr-x");if(x)x.oninput=e=>{r.xh=e.target.value;changed();};R.querySelector(".sr-rm").onclick=()=>{L.splice(+R.dataset.ri,1);redraw();changed();};});
  const ng=el.querySelector(".st-night");if(ng)ng.onchange=e=>{s.stx.night=e.target.checked;redraw();changed();};const nf=el.querySelector(".st-fee");if(nf)nf.oninput=e=>{s.stx.fee=e.target.value;changed();};
  el.querySelectorAll(".ofc.open[data-j]").forEach(C=>{const j=+C.dataset.j,o=s.offers[j];if(!o)return;const q=(sel,f)=>C.querySelectorAll(sel).forEach(f),kj=`${k}o${j}`;
   q(".of-x",b=>b.onclick=()=>{s.offers.splice(j,1);s.open="";redraw();changed();});
   q(".of-name",x=>x.oninput=e=>{o.name=e.target.value;changed();});
   q(".of-dup",b=>b.onclick=()=>{const n=blankOffer(o.n,o.kind);n.tar=[{w:"full",price:"",u:o.tar[0].u,uo:"",alc:""}];s.offers.splice(j+1,0,n);s.open="f"+(j+1);redraw();changed();});
   q(".mr",R=>{const L=o[R.dataset.k],x=L[+R.dataset.xi];R.querySelector(".m-e").oninput=e=>{x.e=e.target.value;changed();};R.querySelector(".m-e").onchange=()=>{const sc=(R.querySelector(".m-e").dataset.sg||"").slice(4);if(!espOf(sc,x.e))return;const key=R.dataset.k,xi=R.dataset.xi;redraw();setTimeout(()=>{const n=document.querySelector(`.box[data-i="${i}"] .ofc.open .mr[data-k="${key}"][data-xi="${xi}"] .m-d`);n&&n.focus();},0);};R.querySelector(".m-d").oninput=e=>{x.d=e.target.value;changed();};
    R.querySelector(".m-x").onclick=()=>{L.splice(+R.dataset.xi,1);redraw();changed();};
    R.querySelectorAll(".idea").forEach(b=>b.onmousedown=e=>{e.preventDefault();L.splice(+R.dataset.xi+1,0,{e:x.e,d:b.dataset.d});redraw();changed();});});
   q(".m-add",b=>b.onclick=()=>{o[b.dataset.k].push({e:"",d:""});redraw();setTimeout(()=>{const l=[...document.querySelectorAll(`.box[data-i="${i}"] .ofc.open .mr[data-k="${b.dataset.k}"] .m-e`)].pop();l&&l.focus();},0);});
   const listOf=l=>l==="ex"?o.ext:l==="in"?o.inc:(o.svcs.find(v=>"sv:"+v.cat===l)||{rows:[]}).rows,relCat=l=>l.startsWith("sv:")?l.slice(3):"";
   q(".incr",R=>{const l=R.closest(".rws").dataset.l,L=listOf(l),r=L[+R.dataset.ri];[["r-c","c"],["r-q","q"],["r-cost","cost"],["r-d","d"],["r-cjn","cj"]].forEach(([c,f])=>{const x=R.querySelector("."+c);if(x)x.oninput=e=>{r[f]=e.target.value;syncSubs(s);changed();};});
    const c=R.querySelector(".r-c");c.onchange=()=>{if(l!=="ex"&&filled(r.c)&&(!filled(r.u)||r.uAuto)){r.u=unitFor(r.c,relCat(l));r.uAuto=true;}if(filled(r.c)){redraw();setTimeout(()=>{const n=document.querySelector(`.box[data-i="${i}"] .ofc.open .rws[data-l="${CSS.escape(l)}"] .incr[data-ri="${R.dataset.ri}"] .r-q`);n&&!filled(r.q)&&n.focus();},0);}changed();};
    const u=R.querySelector(".r-u");u.oninput=e=>{r.u=e.target.value;r.uAuto=false;changed();};u.onchange=()=>{if(/caja/i.test(r.u)!==!!R.querySelector(".r-cj"))redraw();};
    R.querySelector(".r-x").onclick=()=>{L.splice(+R.dataset.ri,1);if(!L.length&&l!=="ex")L.push(newRow());redraw();changed();};});
   q(".r-add",b=>b.onclick=()=>{const l=b.closest(".rws").dataset.l;listOf(l).push(l==="ex"?{c:"",q:"",u:"",d:"",cj:"",cost:""}:newRow());redraw();setTimeout(()=>{const x=[...document.querySelectorAll(`.box[data-i="${i}"] .ofc.open .rws[data-l="${CSS.escape(l)}"] .r-c`)].pop();x&&x.focus();},0);});
   q(".rel-c",b=>b.onclick=()=>{const c=b.dataset.c,ix=o.svcs.findIndex(v=>v.cat===c);if(ix>=0)o.svcs.splice(ix,1);else o.svcs.push({cat:c,rows:[newRow()]});redraw();changed();if(ix<0)setTimeout(()=>{const x=document.querySelector(`.box[data-i="${i}"] .ofc.open .rws[data-l="${CSS.escape("sv:"+c)}"] .r-c`);x&&x.focus();},0);});
   q(".of-pax",x=>{x.oninput=e=>{o.pax=e.target.value;changed();};x.onchange=()=>{const P=crewList(o,s);o.crew.forEach(r=>{if(r.auto){const p=P.find(z=>z[0]===r.n);if(p)r.q=crewQ(p[1],o.pax);}});syncSubs(s);redraw();};});
   q(".crew-c",b=>b.onclick=()=>{const n=b.dataset.n,ix=o.crew.findIndex(r=>r.n===n);if(ix>=0)o.crew.splice(ix,1);else{const p=crewList(o,s).find(z=>z[0]===n);o.crew.push({n,q:o.kind==="gen"?"":crewQ(p?p[1]:0,o.pax),auto:o.kind!=="gen"});}redraw();changed();});
   q(".crew-new",b=>b.onclick=()=>{const r=C.querySelector(".crew-in").closest(".newrow");r.hidden=false;r.querySelector("input").focus();});
   q(".crew-in",inp=>{const add=()=>{const v=(inp.value||"").trim();if(!v)return;if(!o.crew.some(r=>nrm(r.n)===nrm(v)))o.crew.push({n:v,q:"1",auto:false});NEW_SUBS.add(v);redraw();changed();};inp.nextElementSibling.onclick=add;inp.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();add();}};});
   q(".crewr",R=>{const r=o.crew[+R.dataset.ri];R.querySelector(".cr-q").oninput=e=>{r.q=e.target.value;r.auto=false;changed();};});
   q(".of-dur",x=>{x.oninput=e=>{o.dur=e.target.value;o.durU="horas";changed();};x.onchange=()=>redraw();});
   q(".tarr[data-ti]",R=>{const t=o.tar[+R.dataset.ti],hv=()=>{const h=R.querySelector(".ta-hv");if(h)h.innerHTML=offerHost(o,t,s.cat);};
    R.querySelector(".ta-p").oninput=e=>{t.price=e.target.value;hv();syncSubs(s);changed();};R.querySelector(".ta-p").onchange=()=>{if(!C.querySelector(".more"))redraw();};R.querySelector(".ta-u").onchange=e=>{t.u=e.target.value;redraw();changed();};
    const uo=R.querySelector(".ta-uo");if(uo){uo.oninput=e=>{t.uo=e.target.value;changed();};uo.onchange=()=>{const cu=canonUnit(t.uo);if(cu){t.u=cu;t.uo="";if(!U_FULL.includes(cu))U_FULL.push(cu);redraw();}else NEW_UNITS.add(t.uo);};}
    const a=R.querySelector(".ta-a");if(a)a.oninput=e=>{t.alc=e.target.value;hv();syncSubs(s);changed();};const x=R.querySelector(".ta-x");if(x)x.onclick=()=>{o.tar.splice(+R.dataset.ti,1);redraw();changed();};});
   q(".ta-add",b=>b.onclick=()=>{o.tar.push({w:b.dataset.w,price:"",u:"Por evento",uo:"",alc:""});redraw();});
   if(o.tar.some(t=>t.w==="full"&&filled(t.price))){bindUploader(kj,"photo",o.photos,redraw);if($("mn-"+kj)){bindMin(o.min,kj,redraw);bindPromo(o.promo,kj,redraw);}}});
  bindDlSec(el,"full",s,k,redraw);bindDlSec(el,"st",s.stx,k+"st",redraw);bindDlSec(el,"rt",s.rtx,k+"rt",redraw);
  ["st","rt"].forEach(sx=>{const X=sx==="st"?s.stx:s.rtx;if($("mn-"+k+sx)){bindMin(X.min,k+sx,redraw);bindPromo(X.promo,k+sx,redraw);}});
  const d=$("d-"+k);if(d)d.oninput=e=>{s.desc=e.target.value;s.descEdited=true;changed();};
  const rm=el.querySelector(".rm-svc");if(rm)rm.onclick=()=>{S.services.splice(i,1);drawServices();changed();};});
 const rb=$("recoBox");if(rb){rb.innerHTML=recoHtml();bindReco(()=>{const y=scrollY;drawServices();scrollTo({top:y});});}
 const pb=$("pkgBox");if(pb){pb.innerHTML=pkgHtml();bindPkgs(()=>{const y=scrollY;drawServices();scrollTo({top:y});});}}
/* v18 · detectamos servicios incluidos y recomendamos venderlos por separado */
function soldApart(c){return c==="Bebidas"?S.services.some(x=>isCat(x)&&x.offers.some(o=>o.kind==="drink")):S.services.some(x=>x.cat===c&&(x.offers.length||x.ways.rent));}
function recoList(){const M=new Map(),no=S.svcRecoNo||[];
 S.services.forEach(s=>{svcDefaults(s);s.offers.forEach((o,j)=>{if(s.open==="f"+j)return;o.svcs.forEach(v=>{const rows=v.rows.filter(r=>filled(r.c));if(!rows.length||no.includes(v.cat)||soldApart(v.cat))return;
  if(!M.has(v.cat))M.set(v.cat,{cat:v.cat,rows:[],from:[]});const m=M.get(v.cat);rows.forEach(r=>{if(!m.rows.some(x=>nrm(x.c)===nrm(r.c)))m.rows.push(r);});m.from.push(offTitle(o));});});});
 return[...M.values()];}
function recoHtml(){const L=recoList();if(!L.length)return"";
 return`<div class="reco"><span class="mk">🔎 DETECTAMOS MÁS SERVICIOS</span><b>Dentro de tus menús también ofreces ${esc(joinY(L.map(x=>x.cat.toLowerCase())))}.</b>
  <span class="hint">Te recomendamos venderlos también por separado: así te encuentran los anfitriones que solo buscan eso. Solo les pones precio.</span>
  ${L.map(x=>`<div class="recor" data-c="${esc(x.cat)}"><span><b>${relEmo(x.cat)} ${esc(x.cat)}</b><small>${esc(x.rows.map(r=>r.c).join(", "))} · en ${esc(joinY([...new Set(x.from)]))}</small></span><span class="recob"><button type="button" class="btn cta sm reco-y">Sí, venderlo aparte</button><button type="button" class="link reco-n">Ahora no</button></span></div>`).join("")}</div>`;}
function addUnitSvc(x){if(x.cat==="Bebidas"){const i=boxFor("Catering"),s=S.services[i];s.cater.drink=true;addOffer(s,"Barra","drink");const o=s.offers[+s.open.slice(1)];
  x.rows.forEach(r=>{const alc=DISHES["Con alcohol"].some(d=>nrm(d)===nrm(r.c))&&!DISHES["Sin alcohol"].some(d=>nrm(d)===nrm(r.c));const L=o[alc?"con":"sin"],e=L.find(z=>!filled(z.d));if(e)e.d=r.c;else L.push({e:"",d:r.c});});s.open="";syncSubs(s);return i;}
 const i=boxFor(x.cat),s=S.services[i],C=catOf(x.cat);
 x.rows.forEach(r=>{const full=C&&C.full.find(f=>nrm(f)===nrm(r.c));addOffer(s,full||r.c,"gen");const o=s.offers[+s.open.slice(1)];if(!full)o.inc=[{c:r.c,q:r.q,u:r.u,d:r.d,cj:""}];});
 s.open="";syncSubs(s);return i;}
function bindReco(redraw){document.querySelectorAll(".recor").forEach(R=>{const c=R.dataset.c,x=recoList().find(z=>z.cat===c);
 R.querySelector(".reco-y").onclick=()=>{const i=addUnitSvc(x);hqvTrack("recomendacion_unitario",{cat:c,acepta:true});changed();goBox(i,`✨ Agregamos ${c} como servicio por separado. Ponle su precio en «⚠️ Completar».`);};
 R.querySelector(".reco-n").onclick=()=>{S.svcRecoNo=[...(S.svcRecoNo||[]),c];hqvTrack("recomendacion_unitario",{cat:c,acepta:false});redraw();changed();};});}
function confirmX(msg,yes){yes();}
function drawSvcStep(){const sc=S.svcScope=S.svcScope||{S:false,E:false};
 $("stepBody").innerHTML=`<div class="panel"><span class="crumb">Mi negocio › Servicios</span><h2>Mis servicios 🎉</h2><p class="sub">Pon el precio como tú lo cobras. Nosotros se lo mostramos al anfitrión por persona y en total.</p>
 <div class="svc-top">
  <div class="field"><span class="lbl">¿Para qué tipo de eventos? <span class="opt">Puedes elegir los dos</span></span><div class="chips${MISS(sc.S||sc.E)}" style="width:fit-content;border-radius:99px"><button type="button" class="chip scp" data-v="S" aria-pressed="${!!sc.S}">${TICK}🎉 Sociales</button><button type="button" class="chip scp" data-v="E" aria-pressed="${!!sc.E}">${TICK}💼 Empresariales</button></div></div>
  <div class="field qwrap"><label class="lbl" for="svcQ">🔎 Busca lo que ofreces <span class="opt">o elige abajo por categoría</span></label><input type="search" id="svcQ" autocomplete="off" placeholder="Ej. banquete, tacos al pastor, DJ, meseros, sillas…"><div id="svcQr" class="qres" hidden></div></div>
 </div>
 <span class="hint pkhint">🎁 ¿Vendes por paquete? Configura tus servicios y al final armas tus paquetes con un precio sugerido.</span>
 <div id="svcList" style="display:grid;gap:14px"></div><button type="button" class="btn ghost" id="addSvc">+ Agregar otra categoría</button>
 <div id="recoBox"></div>
 <div id="pkgBox"></div>
 ${priceBoxHtml()}
 ${zonesHtml(S.svcZones,"svc","¿Dónde das estos servicios?")}${VIATICOS}${navHtml()}</div>`;
 document.querySelectorAll(".scp").forEach(c=>c.onclick=()=>{sc[c.dataset.v]=!sc[c.dataset.v];drawSvcStep();changed();});
 const q=$("svcQ"),qr=$("svcQr"),WE={full:"🎁",staff:"🙋",rent:"📦"},WT={full:"servicio",staff:"staff",rent:"renta"};
 const search=()=>{const v=nrm(q.value).trim();if(v.length<2){qr.hidden=true;return;}const toks=v.split(/\s+/),res=[];
  CAT2.forEach(c=>{[["full",c.full],["staff",c.staff],["rent",c.rent]].forEach(([w,l])=>l.forEach(n=>{const h=nrm(n+" "+c.n);if(toks.every(t=>h.includes(t)))res.push({c,n,w,r:nrm(n).startsWith(v)?0:1});}));});
  if(res.length<6)["Salado","Dulce"].forEach(kd=>DISHES[kd].forEach(d=>{if(res.length<8&&toks.every(t=>nrm(d).includes(t)))res.push({c:CAT2[0],n:"Buffet",w:"full",r:2,dish:d,kd});}));
  res.sort((a,b)=>a.r-b.r);
  qr.innerHTML=res.slice(0,8).map((x,ix)=>`<button type="button" data-ix="${ix}"><span>${x.c.e}</span><span><b>${esc(x.dish||x.n)}</b> <small>· ${esc(x.c.n)} · ${WE[x.w]} ${x.dish?"menú de buffet":WT[x.w]}</small></span></button>`).join("")
   ||`<span class="hint" style="padding:8px">No lo encontramos. Elige la categoría más cercana y usa <b>✏️ Otro</b>: lo sumamos al catálogo.</span>`;
  qr.hidden=false;qr.querySelectorAll("button").forEach(btn=>btn.onclick=()=>{const x=res[+btn.dataset.ix],i=boxFor(x.c.n),s=S.services[i];
   if(x.w==="full"){const food=s.cat==="Catering"&&FOOD_FMT.includes(x.n),drink=s.cat==="Catering"&&!food;if(s.cat==="Catering")s.cater[food?"food":"drink"]=true;
    addOffer(s,drink?x.n.replace(/ de bebidas$/,"").replace(/^(\w)/,m=>m.toUpperCase()):x.n,s.cat==="Catering"?(food?"food":"drink"):"gen");
    if(x.dish){const o=s.offers[+s.open.slice(1)],L=o[x.kd==="Dulce"?"dul":"sal"],e=L.find(r=>!filled(r.d));if(e)e.d=x.dish;else L.push({e:"",d:x.dish});}}
   else addPerson(s,x.w==="staff"?"staff":"rent",x.n,x.w==="staff"?"Por hora":"Por pieza");
   syncSubs(s);q.value="";qr.hidden=true;hqvTrack("servicio_buscado",{sub:x.n});goBox(i);});};
 q.oninput=search;q.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();const f=qr.querySelector("button");f&&f.click();}if(e.key==="Escape"){qr.hidden=true;}};
 drawServices();$("addSvc").onclick=()=>{S.services.push(blankSvc());drawServices();changed();const l=$("svcList").lastElementChild;l&&l.scrollIntoView({behavior:"smooth",block:"start"});};
 bindPriceBox(drawSvcStep);bindZones(S.svcZones,"svc",drawSvcStep);bindNav();}
