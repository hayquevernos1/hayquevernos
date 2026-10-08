/* ¡Hay que vernos! · Catálogo compartido entre "Mi negocio" (proveedores) y "Mis fiestas" (anfitriones).
   Una sola lista de tipos de venue, características y servicios para que los dos lados hablen el mismo idioma,
   y el motor del "precio estándar ¡HQV!": convierte cualquier forma de cobro de un venue a un precio comparable. */
const HQV=(()=>{
const VENUE_TYPES=[["Terraza","🌇"],["Jardín","🌳"],["Salón","🏛️"],["Roof garden","🏙️"],["Casa o depa","🏠"],["Patio","🪴"],["Restaurante o bar","🍸"],["Club o centro social","🎾"],["Foro o bodega","🏭"],["Oficina o coworking","🏢"],["Locación","📍"]];
// Lo que el venue TIENE (proveedor) y lo que el anfitrión NECESITA salen de esta misma lista
const VENUE_FEATS=[["techado","☂️","Techado"],["aire","🌤️","Área al aire libre"],["estac","🚗","Estacionamiento"],["cocina","🍳","Cocina equipada"],["accesible","♿","Accesible"],["ninos","🧸","Zona para niños"],["pet","🐶","Pet friendly"],["fumar","🚬","Área para fumar"],["sonido","🔊","Sonido instalado"],["luz","💡","Luz y contactos"],["agua","🚰","Agua corriente"],["refri","❄️","Refrigerador"],["almacen","📦","Almacenamiento"],["calle","🚪","Acceso directo a la calle"],["elevador","🛗","Elevador"],["wifi","📶","Wifi"]];
const NEED_KEYS=["techado","aire","estac","cocina","accesible","ninos","pet","fumar","sonido"];
// Servicios que un venue puede ofrecer o restringir (mismos nombres que las categorías del cotizador)
const POLICY_CATS=[["Comida","🍽️"],["Con alcohol","🍹"],["Sin alcohol","🧃"],["Postres","🎂"],["Música","🎧"],["Luz y show","💡"],["Mobiliario","🪑"],["Decoración","🎈"],["Staff","🤵"]];
const DAYS=[["lun","Lun"],["mar","Mar"],["mie","Mié"],["jue","Jue"],["vie","Vie"],["sab","Sáb"],["dom","Dom"]];
const DAY_NAMES={lun:"lunes",mar:"martes",mie:"miércoles",jue:"jueves",vie:"viernes",sab:"sábado",dom:"domingo"};
const STD={hours:5,setup:.5,teardown:.5};
const num=v=>{const n=parseFloat(String(v??"").replace(/[^0-9.\-]/g,""));return isFinite(n)?n:0;};
const t2h=t=>{if(!t)return null;const[h,m]=t.split(":").map(Number);return h+(m||0)/60;};
const fmtH=h=>{h=((h%24)+24)%24;const hh=Math.floor(h),mm=Math.round((h-hh)*60);return`${String(hh).padStart(2,"0")}:${String(mm).padStart(2,"0")}`;};
const dayKey=iso=>["dom","lun","mar","mie","jue","vie","sab"][new Date(iso+"T12:00").getDay()];
const capFor=(v,format)=>{const s=num(v.seated),p=num(v.standing);return format==="pie"?p:format==="mixto"?Math.round((s+p)/2):s;};
function eventHours(start,end){const a=t2h(start),b=t2h(end);if(a==null||b==null)return STD.hours;let d=b-a;if(d<=0)d+=24;return Math.round(d*10)/10;}
// ¿La hora de fin del evento cabe antes de la hora límite del venue? (las horas después de medianoche cuentan como +24)
function endsBeforeLimit(v,start,end){const lim=t2h(v.limit),a=t2h(start),b=t2h(end);if(lim==null||a==null||b==null)return true;
 const L=lim<8?lim+24:lim;let E=b<=a?b+24:b;if(E<8)E+=24;return E+STD.teardown<=L+1e-9;}

/** Cotiza un venue para una solicitud. Devuelve {ok, reasons[], total, option, lines[], negotiable, cond}.
 req = {guests, date, start, end, format, types[], feats[], munis[], allZone, fromVenue[] (servicios que pone el venue), own[] (servicios que lleva el anfitrión), ownCost{cat:monto}} */
function venueQuote(v,req){const reasons=[],g=Math.max(1,num(req.guests));
 if(req.types&&req.types.length&&!req.types.includes("Me da igual")&&!req.types.includes(v.type))reasons.push("tipo");
 if(!req.allZone&&req.munis&&req.munis.length&&!req.munis.includes(v.addr.muni))reasons.push("zona");
 const lacking=(req.feats||[]).filter(f=>NEED_KEYS.includes(f)&&!v.features.includes(f));if(lacking.length)reasons.push("caracteristicas");
 if(req.date&&v.days&&v.days.length&&!v.days.includes(dayKey(req.date)))reasons.push("dia");
 if(!endsBeforeLimit(v,req.start,req.end))reasons.push("hora");
 if(capFor(v,req.format||"sentados")<g)reasons.push("capacidad");
 const H=eventHours(req.start,req.end),incl=num(v.hoursIncl)||STD.hours,extraH=Math.max(0,Math.ceil(H-incl)),extraCost=extraH*num(v.extraHour);
 const dk=req.date?dayKey(req.date):"sab",dayAdj=num((v.adj&&v.adj.day||{})[dk])/100;
 const endH=t2h(req.end),isDay=endH!=null&&endH>8&&endH<=19,dayTimeAdj=isDay?num(v.adj&&v.adj.daytime)/100:0;
 const adjust=x=>x*(1+dayAdj)*(1+dayTimeAdj);
 const opts=[];
 const svcCost=(inc)=>{let c=0,lines=[],bad=null;
  (req.fromVenue||[]).forEach(cat=>{const p=(v.policy||{})[cat];if(inc&&inc.includes(cat)){lines.push([cat,"incluido en el paquete",0]);return;}
   if(!p||p.offer==="no"){bad=bad||("noofrece:"+cat);return;}
   if(p.offer==="inc"){lines.push([cat,"incluido",0]);return;}
   const m=num(p.price)*(p.per==="persona"?g:1);c+=m;lines.push([cat,"con costo",m]);});
  (req.own||[]).forEach(cat=>{const p=(v.policy||{})[cat];if(!p)return;
   if(p.own==="no"){bad=bad||("exclusivo:"+cat);return;}
   if(p.own==="cuota"){const m=num(p.fee);c+=m;lines.push([cat,"cuota por traerlo",m]);}});
  return{c,lines,bad};};
 if(v.mode==="renta"||v.mode==="ambos"){const r=v.rent||{};const per=r.per||"evento";let base=per==="hora"?num(r.price)*Math.max(H,incl):per==="persona"?num(r.price)*g:num(r.price);
  if(num(r.upTo)>0&&g>num(r.upTo))base+=(g-num(r.upTo))*num(r.perExtraGuest);
  const s=svcCost(null);if(!s.bad)opts.push({label:"Renta del espacio",total:adjust(base)+(per==="hora"?0:extraCost)+s.c,lines:[["Renta del espacio",per==="hora"?`${Math.max(H,incl)} h`:"",adjust(base)],...(per!=="hora"&&extraCost?[["Horas extra",`${extraH} h`,extraCost]]:[]),...s.lines]});else opts.bad=s.bad;}
 if(v.mode==="paquetes"||v.mode==="ambos"){(v.packages||[]).forEach(pk=>{const gg=Math.max(g,num(pk.min));const base=pk.per==="persona"?num(pk.price)*gg:num(pk.price);
  const s=svcCost(pk.inc||[]);if(!s.bad)opts.push({label:pk.name||"Paquete",total:adjust(base)+extraCost+s.c,lines:[[pk.name||"Paquete",pk.per==="persona"?`${gg} personas`:"",adjust(base)],...(extraCost?[["Horas extra",`${extraH} h`,extraCost]]:[]),...s.lines]});else opts.bad=opts.bad||s.bad;});}
 if(!opts.length)reasons.push(opts.bad||"sinprecio");
 const best=opts.sort((a,b)=>a.total-b.total)[0]||null;
 return{ok:!reasons.length&&!!best,reasons,total:best?Math.round(best.total):0,option:best?best.label:"",lines:best?best.lines:[],options:opts,hours:H,extraH,negotiable:!!v.negotiable,
  cond:{deposit:v.deposit,advance:v.advance,guarantee:v.guarantee,corkage:v.corkage,cancel:v.cancel,docs:v.docsNone?[]:[...(v.docs||[]),v.docsOther].filter(Boolean)}};}

function reasonText(r){if(r.startsWith("noofrece:"))return`No ofrece ${r.slice(9).toLowerCase()}`;if(r.startsWith("exclusivo:"))return`${r.slice(10)}: solo con su gente`;
 return{tipo:"Otro tipo de lugar",zona:"Fuera de tu zona",caracteristicas:"Le falta algo que pediste",dia:"No renta ese día",hora:"Cierra antes de que termine tu fiesta",capacidad:"No caben tus invitados",sinprecio:"Sin precio publicado"}[r]||r;}

/** Precio estándar ¡HQV!: misma regla para todos (5 h, sábado en la noche, sin servicios extra). */
function standardPrice(v,guests){const sat=(()=>{const d=new Date();d.setDate(d.getDate()+((6-d.getDay()+7)%7||7));return`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")}`;})();
 const start=v.limit&&t2h(v.limit)<20&&t2h(v.limit)>=8?fmtH(t2h(v.limit)-STD.hours-STD.teardown):"18:00";
 const q=venueQuote(v,{guests,date:sat,start,end:fmtH(t2h(start)+STD.hours),format:"sentados",fromVenue:[],own:[]});
 return q.options&&q.options.length?Math.round(q.options.sort((a,b)=>a.total-b.total)[0].total):0;}

/* Venues de ejemplo de la red (simulación): distintas formas de cobro reales */
const P=(offer,own,price,per,fee)=>({offer,own,price:price||"",per:per||"evento",fee:fee||""});
const SAMPLE_VENUES=[
 {name:"Terraza Lupita",type:"Terraza",addr:{muni:"Álvaro Obregón"},seated:60,standing:90,features:["techado","aire","fumar","luz","agua","refri","calle","ninos"],days:["jue","vie","sab","dom"],open:"12:00",limit:"23:00",hoursIncl:5,extraHour:1800,
  mode:"renta",rent:{price:9000,per:"evento",upTo:60,perExtraGuest:150},adj:{day:{sab:10},daytime:-10},negotiable:true,
  policy:{"Comida":P("no","si"),"Con alcohol":P("no","cuota","","",1500),"Sin alcohol":P("no","si"),"Postres":P("no","si"),"Música":P("costo","no",3500),"Luz y show":P("no","si"),"Mobiliario":P("inc","si"),"Decoración":P("no","si"),"Staff":P("no","si")},
  deposit:"50%",advance:15,guarantee:2000,corkage:"$150 por botella",cancel:"Reembolso del anticipo con 30 días de aviso",docs:["INE","Contrato firmado"]},
 {name:"Salón Fiesta Real",type:"Salón",addr:{muni:"Coyoacán"},seated:220,standing:330,features:["techado","estac","cocina","accesible","sonido","luz","agua","refri","almacen","calle","ninos"],days:["lun","mar","mie","jue","vie","sab","dom"],open:"10:00",limit:"02:00",hoursIncl:5,extraHour:4500,
  mode:"paquetes",packages:[{name:"Paquete 1",price:450,per:"persona",min:80,inc:["Comida","Mobiliario","Staff","Música"]},{name:"Paquete 2",price:650,per:"persona",min:80,inc:["Comida","Mobiliario","Staff","Música","Sin alcohol","Decoración","Luz y show"]},{name:"Paquete 3",price:890,per:"persona",min:80,inc:["Comida","Mobiliario","Staff","Música","Sin alcohol","Decoración","Luz y show","Con alcohol"]}],
  adj:{day:{lun:-15,mar:-15,mie:-15,jue:-10,sab:15}},negotiable:true,
  policy:{"Comida":P("costo","no",380,"persona"),"Con alcohol":P("costo","cuota",220,"persona",4000),"Sin alcohol":P("costo","si",60,"persona"),"Postres":P("costo","si",45,"persona"),"Música":P("costo","no",6000),"Luz y show":P("costo","no",5000),"Mobiliario":P("inc","no"),"Decoración":P("costo","cuota",8000,"evento",1500),"Staff":P("costo","no",900,"evento")},
  deposit:"30%",advance:60,guarantee:5000,corkage:"$4,000 por evento",cancel:"El anticipo no es reembolsable",docs:["INE","Comprobante de domicilio","Contrato firmado"]},
 {name:"Jardín Las Flores",type:"Jardín",addr:{muni:"Tlalpan"},seated:180,standing:260,features:["aire","estac","ninos","pet","accesible","luz","agua","almacen"],days:["vie","sab","dom"],open:"09:00",limit:"01:00",hoursIncl:6,extraHour:3000,
  mode:"renta",rent:{price:18000,per:"evento",upTo:150,perExtraGuest:120},adj:{day:{sab:15,dom:-10},daytime:-15},negotiable:false,
  policy:{"Comida":P("no","si"),"Con alcohol":P("no","si"),"Sin alcohol":P("no","si"),"Postres":P("no","si"),"Música":P("no","cuota","","",1000),"Luz y show":P("no","si"),"Mobiliario":P("costo","si",45,"persona"),"Decoración":P("no","si"),"Staff":P("no","si")},
  deposit:"50%",advance:30,guarantee:3000,corkage:"",cancel:"Reembolso del 50% con 45 días de aviso",docs:["INE","Contrato firmado","Carta responsiva"]},
 {name:"Foro La Bodega",type:"Foro o bodega",addr:{muni:"Cuauhtémoc"},seated:200,standing:400,features:["techado","sonido","luz","agua","calle","almacen","accesible"],days:["jue","vie","sab"],open:"14:00",limit:"04:00",hoursIncl:5,extraHour:2500,
  mode:"renta",rent:{price:2500,per:"hora"},adj:{day:{sab:20}},negotiable:true,
  policy:Object.fromEntries(POLICY_CATS.map(([c])=>[c,P("no","si")])),
  deposit:"50%",advance:10,guarantee:8000,corkage:"",cancel:"Sin reembolso",docs:["INE","Póliza de seguro"]},
 {name:"Roof Polanco",type:"Roof garden",addr:{muni:"Miguel Hidalgo"},seated:70,standing:120,features:["aire","techado","elevador","accesible","sonido","fumar","luz","agua","refri","wifi"],days:["jue","vie","sab"],open:"13:00",limit:"01:00",hoursIncl:5,extraHour:5000,
  mode:"ambos",rent:{price:25000,per:"evento",upTo:80,perExtraGuest:250},packages:[{name:"Paquete cóctel",price:1100,per:"persona",min:40,inc:["Comida","Con alcohol","Sin alcohol","Staff","Música"]}],adj:{day:{sab:20}},negotiable:false,
  policy:{"Comida":P("costo","no",520,"persona"),"Con alcohol":P("costo","cuota",450,"persona",3000),"Sin alcohol":P("costo","no",90,"persona"),"Postres":P("no","si"),"Música":P("costo","no",7000),"Luz y show":P("no","si"),"Mobiliario":P("inc","no"),"Decoración":P("no","cuota","","",2000),"Staff":P("costo","no",1500)},
  deposit:"50%",advance:30,guarantee:10000,corkage:"$3,000 por evento",cancel:"Reembolso del 50% con 30 días de aviso",docs:["INE","Contrato firmado"]},
 {name:"Casa Coyoacán",type:"Casa o depa",addr:{muni:"Coyoacán"},seated:35,standing:55,features:["aire","cocina","ninos","pet","luz","agua","refri","calle"],days:["lun","mar","mie","jue","vie","sab","dom"],open:"10:00",limit:"22:00",hoursIncl:5,extraHour:1000,
  mode:"renta",rent:{price:7000,per:"evento",upTo:40,perExtraGuest:100},adj:{day:{sab:10},daytime:-15},negotiable:true,
  policy:Object.fromEntries(POLICY_CATS.map(([c])=>[c,P(c==="Mobiliario"?"inc":"no","si")])),
  deposit:"50%",advance:7,guarantee:1500,corkage:"",cancel:"Reembolso total con 15 días de aviso",docs:["INE"]}
];
return{VENUE_TYPES,VENUE_FEATS,NEED_KEYS,POLICY_CATS,DAYS,DAY_NAMES,STD,num,t2h,fmtH,dayKey,capFor,eventHours,venueQuote,reasonText,standardPrice,SAMPLE_VENUES};
})();
