const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots14/';const BASE='http://localhost:8765/';require('fs').mkdirSync(O,{recursive:true});
const D=n=>new Date(Date.now()+n*864e5).toISOString().slice(0,10);
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:860},deviceScaleFactor:1,reducedMotion:'reduce',acceptDownloads:true});
 const errs=[];
 const shot=async(pg,n,full=true)=>{try{await pg.waitForTimeout(400);await pg.addStyleTag({content:'#toast{display:none!important}'}).catch(()=>{});
   await pg.evaluate(()=>{document.querySelectorAll('details').forEach(d=>d.open=true);scrollTo(0,0);}).catch(()=>{});
   for(const f of pg.frames())await f.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true)).catch(()=>{});
   await pg.waitForTimeout(150);await pg.screenshot({path:O+n+'.jpg',fullPage:full,type:'jpeg',quality:80});console.log('ok',n);}catch(e){errs.push('shot '+n+': '+e.message.split('\n')[0]);}};
 const st=async(l,f)=>{try{await f();}catch(e){errs.push(l+': '+e.message.split('\n')[0]);}};
 const page=async(w=1280,h=860)=>{const p=await ctx.newPage();await p.setViewportSize({width:w,height:h});p.on('pageerror',e=>errs.push(e.message));return p;};

 const FILL=async(F)=>{await F.evaluate(()=>{S.name="Mariana";S.nameOk=true;S.wantPlanner=false;S.plannerPick=null;S.kind="social";S.occ="Boda";S.guests=120;S.date=new Date(Date.now()+75*864e5).toISOString().slice(0,10);S.start="17:00";S.end="23:00";S.suggestedFor="";if(typeof applySuggestions==="function")applySuggestions();
   S.hasPlace=false;S.need={state:"Ciudad de México",all:false,munis:["Álvaro Obregón","Coyoacán","Benito Juárez"],types:["Jardín","Terraza","Salón"],feats:["techado","estac","accesible"],featsOther:["Que acepte mascotas"],req:{techado:"req",estac:"opt",accesible:"req"},format:"sentados"};
   S.sel["Personal"]=["Meseros","Bartenders"];Object.keys(S.sel).forEach(c=>{S.meta[c]={inv:c==="Alimentos",who:hasPolicy(c)?(c==="Alimentos"||c==="Bebidas y barra"?"venue":"yo"):undefined};});
   rows().forEach((r,i)=>S.factor[r.k]=[1,1.2,0.9,1.1,1,1.3,0.8,1,1.15][i%9]);
   S.fact={docs:["Constancia de situación fiscal","Contrato firmado"],docsOther:["Carta de no adeudo"],days:"",reqDate:new Date(Date.now()+40*864e5).toISOString().slice(0,10),terms:"Anticipo y liquidación el día del evento",method:["Transferencia"],methodOther:["Vales de despensa"],biz:"Mariana López Díaz"};});};
 const EXT=()=>{S=exampleState();ensureState();const v=S.venue,p=S.planner,b=S.biz;
  b.links=[{t:"Sitio web",u:"lupitadulces.mx"},{t:"YouTube",u:"youtube.com/@lupitadulces"},{t:"Otro",u:"linktr.ee/lupita"}];
  v.mode="ambos";v.packages=[{name:"Paquete Plata",price:"650",per:"persona",min:"40",inc:["Comida","Sin alcohol","Mobiliario","Staff"]},{name:"Paquete Oro",price:"48000",per:"total",min:"",inc:["Comida","Con alcohol","Música","Mobiliario","Decoración","Staff"]}];
  v.extAll="";const P=v.policy;const set=(k,o)=>Object.assign(P[k],o);
  set("Comida",{incl:"inc",subs:["Taquizas","Banquetes"],subst:"si",substMode:"libre"});
  set("Con alcohol",{incl:"costo",price:"250",per:"persona",subst:"si",substMode:"cuota",fee:"150",feeUnit:"botella",feeNote:"Descorche"});
  set("Sin alcohol",{incl:"noinc"});
  set("Postres",{incl:"parte",detail:"Pastel de 3 pisos",subst:"parcial",substOther:"Mesa de dulces sí; pastel no",substMode:"otro",modeOther:"Solo proveedores de nuestra lista"});
  set("Música",{incl:"costo",price:"3500",per:"evento",subst:"no"});
  set("Luz y show",{incl:"inc",subst:"otro",substOther:"Solo si traen su propia planta de luz"});
  set("Mobiliario",{incl:"parte",detail:"60 sillas Tiffany y 6 mesas redondas",subst:"si",substMode:"cuota",fee:"20",feeUnit:"persona",feeNote:"Por limpieza"});
  set("Decoración",{incl:"inc",subst:"si",substMode:"otro",modeOther:"Montaje solo después de las 10:00"});
  set("Staff",{incl:"noinc"});
  v.typeOther="";v.featsOther=["Planta de luz","Cocina industrial"];
  p.fees=[{amount:"6000",unit:"evento",other:"",note:"Hasta 50 invitados"},{amount:"10",unit:"porcentaje",other:"",note:"Fiestas de más de 100 invitados"},{amount:"1500",unit:"otro",other:"Por día de montaje",note:""}];p.depositN="30";p.depositU="%";p.negotiable=true;
  p.socialFromBiz=false;p.instagram="@lupi.planner";p.links=[{t:"Pinterest",u:"pinterest.com/lupiplanner"}];};

 // ===== Cotizador: pago y resultado
 const c=await page();await c.goto(BASE+'fiestas.html');await c.waitForTimeout(800);await FILL(c);
 await c.evaluate(()=>{S.pay={mode:"mine",ant:[{n:"50",u:"%",t:"2",tu:"meses"},{n:"20000",u:"$",t:"3",tu:"semanas"}],liq:[{n:"25",u:"%",t:"2",tu:"días"}],how:["Transferencia SPEI"],howOther:""};go("detalles");});await shot(c,'A07_detalles_factura_y_pago');
 const pt=await c.evaluate(()=>payText());console.log(JSON.stringify(pt));
 await c.evaluate(()=>go("result"));await c.waitForTimeout(1000);await shot(c,'A08_resultado');
 const cm=await page(390,844);await cm.goto(BASE+'fiestas.html');await cm.waitForTimeout(700);await FILL(cm);await cm.evaluate(()=>{S.pay={mode:"mine",ant:[{n:"50",u:"%",t:"2",tu:"meses"}],liq:[{n:"50",u:"%",t:"1",tu:"días"}],how:["Efectivo"],howOther:""};go("detalles");});await shot(cm,'A07m_pago_celular');
 // ===== Registro
 const r=await page();await r.goto(BASE+'negocio.html');await r.waitForTimeout(800);
 await r.evaluate(()=>{S=exampleState();drawTypes();});await st('goProv',()=>r.click('#goProv'));await r.waitForTimeout(400);
 await r.evaluate(EXT);
 await r.evaluate(()=>{const i=stepList().findIndex(s=>s.id==="svc");S.svcZones=[{state:"__nac",all:false,munis:[]}];step=i;render();});await shot(r,'R03_paso_svc_entregas');
 // abrir la de envío con condiciones
 await st('open0',async()=>{await r.click('.dlc[data-j="0"] .dl-open');await r.waitForTimeout(300);});await shot(r,'R03b_entrega_envio_abierta');
 // agregar entrega con instalación por zona
 await st('addInst',async()=>{await r.click('.dlm[data-m="Entrega con instalación"]');await r.waitForTimeout(200);await r.click('[id^="dly-s0-2"] button[data-v="1"]');await r.waitForTimeout(200);await r.selectOption('.dlc.open .dl-u','Por zona geográfica');await r.waitForTimeout(200);
   const z=await r.$$('.dlc.open .dl-z');await z[0].fill('300');await z[1].fill('650');await z[2].fill('1200');await r.click('.dlc.open .dc-add');await r.waitForTimeout(200);});
 await shot(r,'R03c_entrega_instalacion_por_zona');
 const miss=await r.evaluate(()=>missing("svc"));console.log('miss svc',JSON.stringify(miss));
 const site=await r.evaluate(()=>[...document.querySelectorAll('.feat span')].map(x=>x.textContent).slice(0,8));console.log('site',JSON.stringify(site));
 await r.evaluate(()=>{const i=stepList().findIndex(s=>s.id==="venue");step=i;render();});await st('vio',async()=>{await r.click('.vio[data-v="1"]');await r.waitForTimeout(200);await r.fill('#v-ioc','500');});await shot(r,'R04_paso_venue');
 const rm=await page(390,844);await rm.goto(BASE+'negocio.html');await rm.waitForTimeout(700);await rm.evaluate(()=>{S=exampleState();drawTypes();});await st('gp',()=>rm.click('#goProv'));await rm.waitForTimeout(300);
 await rm.evaluate(()=>{const i=stepList().findIndex(s=>s.id==="svc");step=i;S.services[0].dlOpen=0;render();});await shot(rm,'R_m_svc_celular');
 // ===== Cuenta en celular: tracker + planner + pop-up de match
 const p=await ctx.newPage();await p.setViewportSize({width:390,height:844});p.on('pageerror',e=>errs.push(e.message));await p.emulateMedia({reducedMotion:'no-preference'});await p.goto(BASE+'index.html');await p.waitForTimeout(800);await p.evaluate(()=>{betaShown=true;goSide('hs',true)});await p.waitForTimeout(500);
 await st('open',async()=>{await p.click('#m-hs [data-open="fiestas"], #d-hs [data-open="fiestas"]');await p.waitForTimeout(1500);
  const F=p.frames().find(f=>f.url().includes('fiestas.html'));await FILL(F);await F.evaluate(()=>go("result"));await p.waitForTimeout(900);await F.fill('#pname','La boda de Mariana y Leo');await F.click('#send');await p.waitForTimeout(700);});
 await st('acc',async()=>{await p.fill('#acN','Mariana');await p.fill('#acL','López Díaz');await p.fill('#acW','5511223344');await p.fill('#acE','mariana@correo.com');await p.click('#acF button[type=submit]');await p.waitForTimeout(1200);});
 const vshot=async(n)=>{try{await p.waitForTimeout(200);await p.addStyleTag({content:'#toast{display:none!important}'});await p.screenshot({path:O+n+'.jpg',type:'jpeg',quality:80});console.log('ok',n);}catch(e){errs.push('vshot '+n);}};
 await st('ob',async()=>{await p.click('#obOk');await p.waitForTimeout(2600);});await vshot('M10_tracker_iluminando_celular');
 await p.waitForTimeout(5500);await vshot('M11_popup_event_planner_celular');
 await st('poNo',async()=>{await p.click('#poNo');await p.waitForTimeout(1500);});await vshot('M12_popup_match_contando_celular');
 await p.waitForTimeout(3500);await vshot('M13_popup_match_listo_celular');
 await st('mtNo',async()=>{await p.click('#mtNo');await p.waitForTimeout(500);});await shot(p,'M14_sin_planner_contactar_cada_uno_celular');
 // escritorio con planner elegido → lo decido después → match
 const q=await ctx.newPage();await q.setViewportSize({width:1280,height:860});q.on('pageerror',e=>errs.push(e.message));await q.emulateMedia({reducedMotion:'no-preference'});await q.goto(BASE+'index.html');await q.waitForTimeout(800);await q.evaluate(()=>{betaShown=true;goSide('hs',true)});await q.waitForTimeout(500);
 await st('qopen',async()=>{await q.click('#d-hs [data-open="fiestas"]');await q.waitForTimeout(1500);const F=q.frames().find(f=>f.url().includes('fiestas.html'));await FILL(F);await F.evaluate(()=>go("result"));await q.waitForTimeout(900);await F.fill('#pname','La boda de Mariana y Leo');await F.click('#send');await q.waitForTimeout(700);
  await q.fill('#acN','Mariana');await q.fill('#acL','López Díaz');await q.fill('#acW','5511223344');await q.fill('#acE','mariana@correo.com');await q.click('#acF button[type=submit]');await q.waitForTimeout(1200);await q.click('#obOk');await q.waitForTimeout(8200);
  await q.click('#poYes');await q.waitForTimeout(300);await q.click('#poPick');await q.waitForTimeout(300);await q.click('#poLater');await q.waitForTimeout(5000);});
 await q.screenshot({path:O+'C03h_popup_match_con_planner.jpg',type:'jpeg',quality:80});
 await st('mtGo',async()=>{await q.click('#mtGo');await q.waitForTimeout(600);});await q.screenshot({path:O+'C03i_match_a_pago.jpg',type:'jpeg',quality:80});
 console.log('ERRS',JSON.stringify(errs));await b.close();})();
