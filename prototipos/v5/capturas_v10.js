const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots11/';const BASE='http://localhost:8765/';require('fs').mkdirSync(O,{recursive:true});
const D=n=>new Date(Date.now()+n*864e5).toISOString().slice(0,10);
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:860},deviceScaleFactor:1,reducedMotion:'reduce',acceptDownloads:true});
 const errs=[];
 const shot=async(pg,n,full=true)=>{try{await pg.waitForTimeout(400);await pg.addStyleTag({content:'#toast{display:none!important}'}).catch(()=>{});
   await pg.evaluate(()=>{document.querySelectorAll('details').forEach(d=>d.open=true);scrollTo(0,0);}).catch(()=>{});
   for(const f of pg.frames())await f.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true)).catch(()=>{});
   await pg.waitForTimeout(150);await pg.screenshot({path:O+n+'.jpg',fullPage:full,type:'jpeg',quality:80});console.log('ok',n);}catch(e){errs.push('shot '+n+': '+e.message.split('\n')[0]);}};
 const st=async(l,f)=>{try{await f();}catch(e){errs.push(l+': '+e.message.split('\n')[0]);}};
 const page=async(w=1280,h=860)=>{const p=await ctx.newPage();await p.setViewportSize({width:w,height:h});p.on('pageerror',e=>errs.push(e.message));return p;};

 // ================= HOME
 const h=await page();await h.goto(BASE+'index.html');await h.waitForTimeout(900);await shot(h,'H01_home_escritorio',false);
 await h.evaluate(()=>goSide('pv',true));await h.waitForTimeout(700);await shot(h,'H02_puerta_proveedor_escritorio');
 await h.evaluate(()=>{betaShown=true;goSide('hs',true)});await h.waitForTimeout(700);await shot(h,'H03_puerta_anfitrion_escritorio');
 const hm=await page(390,844);await hm.goto(BASE+'index.html');await hm.waitForTimeout(800);await shot(hm,'H04_home_celular',false);
 await hm.evaluate(()=>goSide('pv',true));await hm.waitForTimeout(700);await shot(hm,'H05_puerta_proveedor_celular');
 await hm.evaluate(()=>{goSide('hs',true);document.getElementById('beta').hidden=false;});await hm.waitForTimeout(600);await shot(hm,'H06_aviso_beta_celular',false);
 await st('beta',()=>hm.click('#betaOk'));await shot(hm,'H07_puerta_anfitrion_celular');await hm.close();

 // ================= COTIZADOR con todo desplegado
 const FILL=async(F)=>{await F.evaluate(()=>{S.name="Mariana";S.nameOk=true;S.wantPlanner=true;S.plannerPick=1;S.kind="social";S.occ="Boda";S.guests=120;S.date=new Date(Date.now()+75*864e5).toISOString().slice(0,10);S.start="17:00";S.end="23:00";S.suggestedFor="";if(typeof applySuggestions==="function")applySuggestions();
   S.hasPlace=false;S.need={state:"Ciudad de México",all:false,munis:["Álvaro Obregón","Coyoacán","Benito Juárez"],types:["Jardín","Terraza","Salón"],feats:["techado","estac","accesible"],featsOther:["Que acepte mascotas"],req:{techado:"req",estac:"opt",accesible:"req"},format:"sentados"};
   S.sel["Personal"]=["Meseros","Bartenders"];Object.keys(S.sel).forEach(c=>{S.meta[c]={inv:c==="Alimentos",who:hasPolicy(c)?(c==="Alimentos"||c==="Bebidas y barra"?"venue":"yo"):undefined};});
   rows().forEach((r,i)=>S.factor[r.k]=[1,1.2,0.9,1.1,1,1.3,0.8,1,1.15][i%9]);
   S.fact={docs:["Constancia de situación fiscal","Contrato firmado"],docsOther:["Carta de no adeudo"],days:"",reqDate:new Date(Date.now()+40*864e5).toISOString().slice(0,10),terms:"Anticipo y liquidación el día del evento",method:["Transferencia"],methodOther:["Vales de despensa"],biz:"Mariana López Díaz"};});};
 const c=await page();await c.goto(BASE+'fiestas.html');await c.waitForTimeout(800);
 await st('nm',async()=>{await c.fill('#nm0','Mariana');});await shot(c,'A01_hola_soy_vernie');
 await st('nmok',async()=>{await c.click('#nmOk');await c.waitForTimeout(300);await c.click('#wpl button[data-v="1"]');await c.waitForTimeout(400);});await shot(c,'A02_quieres_planner');
 await st('pl',async()=>{await c.click('#plNo');await c.click('#plYes');await c.waitForTimeout(300);await c.click('#kind button[data-v="social"]');await c.click('.occ[data-o="Boda"]');});
 await c.evaluate(()=>{S.guests=120;S.date=new Date(Date.now()+75*864e5).toISOString().slice(0,10);S.start="17:00";S.end="23:00";S.suggestedFor="";if(typeof applySuggestions==="function")applySuggestions();render();});await shot(c,'A03_tu_fiesta');
 await st('lugar',async()=>{await c.click('#next');await c.waitForTimeout(300);await c.click('#hp button[data-v="1"]');await c.click('#own button[data-v="rentado"]');await c.waitForTimeout(200);
  await c.evaluate(()=>{const p=S.place;p.type="Jardín";p.addr={cp:"01000",state:"Ciudad de México",muni:"Álvaro Obregón",col:"San Ángel",colOther:"",street:"Av. Revolución",num:"1500",int:"",ref:"Portón negro",ok:true,manual:false};p.floor="otro";p.floorOther="Mezzanine";p.up="elevador";p.cover="mixto";p.parking="otro";p.parkingOther="Estacionamiento público a 1 cuadra";p.feats=["luz","agua","sonido"];p.featsOther=["Planta de luz","Cocina industrial"];p.baths={m:"1",w:"2",g:"0"};render();});});
 await shot(c,'A04a_lugar_ya_tengo');
 await c.evaluate(()=>{S.hasPlace=false;S.need={state:"Ciudad de México",all:false,munis:["Álvaro Obregón","Coyoacán","Benito Juárez"],types:["Jardín","Terraza","Salón"],feats:["techado","estac","accesible"],featsOther:["Que acepte mascotas"],req:{techado:"req",estac:"opt",accesible:"req"},format:"sentados"};render();});await shot(c,'A04b_lugar_busco_venue');
 await c.evaluate(()=>{S.sel["Personal"]=["Meseros","Bartenders"];Object.keys(S.sel).forEach(k=>{S.meta[k]={inv:k==="Alimentos",who:hasPolicy(k)?(k==="Alimentos"||k==="Bebidas y barra"?"venue":"yo"):undefined};});S.more="Un violinista para la entrada de la novia";CATS.forEach(k=>{OPENC.add(k.n);ALLC.add(k.n);});go("servicios");});await shot(c,'A05_servicios_todas_las_categorias_abiertas');
 await c.evaluate(()=>{rows().forEach((r,i)=>S.factor[r.k]=[1,1.2,0.9,1.1,1,1.3,0.8,1,1.15][i%9]);go("presupuesto");});await shot(c,'A06_presupuesto');
 await c.evaluate(()=>{S.fact={docs:["Constancia de situación fiscal","Contrato firmado"],docsOther:["Carta de no adeudo"],days:"",reqDate:new Date(Date.now()+40*864e5).toISOString().slice(0,10),terms:"Anticipo y liquidación el día del evento",method:["Transferencia"],methodOther:["Vales de despensa"],biz:"Mariana López Díaz"};go("detalles");});await shot(c,'A07_detalles_factura');
 await c.evaluate(()=>go("result"));await c.waitForTimeout(1200);await st('pn',()=>c.fill('#pname','La boda de Mariana y Leo'));await shot(c,'A08_resultado');
 const cm=await page(390,844);await cm.goto(BASE+'fiestas.html');await cm.waitForTimeout(600);await FILL(cm);await cm.evaluate(()=>{CATS.forEach(k=>{OPENC.add(k.n);});go("servicios");});await shot(cm,'A05m_servicios_celular');
 await cm.evaluate(()=>go("result"));await cm.waitForTimeout(1000);await st('pnm',()=>cm.fill('#pname','La boda de Mariana y Leo'));await shot(cm,'A08m_resultado_celular');await cm.close();await c.close();

 // ================= REGISTRO DE NEGOCIO con todas las ramas
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
 const r=await page();await r.goto(BASE+'negocio.html');await r.waitForTimeout(800);
 await r.evaluate(()=>{S=exampleState();drawTypes();});await shot(r,'R01_que_ofreces');
 await st('goProv',()=>r.click('#goProv'));await r.waitForTimeout(400);
 await r.evaluate(EXT);
 const steps=await r.evaluate(()=>stepList().map(s=>s.id));
 for(let i=0;i<steps.length;i++){await r.evaluate(i=>{step=i;render();},i);await shot(r,'R0'+(i+2)+'_paso_'+steps[i]+'_todo_desplegado');}
 // venue: mismo horario todos los días + solo renta
 await r.evaluate(()=>{const i=stepList().findIndex(s=>s.id==="venue");S.venue.sameHours=true;S.venue.mode="renta";S.venue.type="__otro";S.venue.typeOther="Hacienda";step=i;render();});await shot(r,'R04b_venue_variante_mismo_horario_solo_renta_otro_tipo');
 await r.evaluate(()=>{const i=stepList().findIndex(s=>s.id==="venue");S.venue.mode="paquetes";S.venue.extAll="si";step=i;render();});await shot(r,'R04c_venue_variante_solo_paquetes_externos_si');
 await r.evaluate(EXT);
 const data=await r.evaluate(async()=>await hqvShareImage({logo:"img/logo.webp",kicker:"¡Ya estamos en ¡Hay que vernos!",title:"Lupita Dulces y Antojos",sub:"Mesas de dulces y carritos para que tu fiesta sea inolvidable",url:"hayquevernos.com/lupita-dulces-y-antojos"}));
 require('fs').writeFileSync(O+'R07b_imagen_para_redes.png',Buffer.from(data.split(',')[1],'base64'));
 await r.evaluate(()=>{demo=true;publish();});await r.waitForTimeout(400);await shot(r,'R07_sitio_publicado');
 await st('pub',()=>r.click('#toPublic'));await r.waitForTimeout(400);await shot(r,'R08_sitio_publico_servicios');
 await st('tv',()=>r.click('#publicSite [data-vt="venue"]'));await r.waitForTimeout(300);await shot(r,'R08b_sitio_publico_venue');
 await st('tp',()=>r.click('#publicSite [data-vt="planner"]'));await r.waitForTimeout(300);await shot(r,'R08c_sitio_publico_planner');await r.close();
 const rm=await page(390,844);await rm.goto(BASE+'negocio.html');await rm.waitForTimeout(700);await rm.evaluate(()=>{S=exampleState();drawTypes();});await st('gp',()=>rm.click('#goProv'));await rm.waitForTimeout(300);await rm.evaluate(EXT);
 for(const id of ['svc','venue','planner']){await rm.evaluate(id=>{step=stepList().findIndex(s=>s.id===id);render();},id);await shot(rm,'R_m_'+id+'_celular');}
 await rm.close();

 // ================= CUENTA ÚNICA · llega por la puerta de fiestas (Mariana)
 const p=await page();await p.goto(BASE+'index.html');await p.waitForTimeout(800);await p.evaluate(()=>{betaShown=true;goSide('hs',true)});await p.waitForTimeout(500);
 await st('open',async()=>{await p.click('#d-hs [data-open="fiestas"]');await p.waitForTimeout(1500);
  const F=p.frames().find(f=>f.url().includes('fiestas.html'));await FILL(F);await F.evaluate(()=>go("result"));await p.waitForTimeout(900);await F.fill('#pname','La boda de Mariana y Leo');await F.click('#send');await p.waitForTimeout(700);});
 await st('acc',async()=>{await p.fill('#acN','Mariana');await p.fill('#acL','López Díaz');await p.fill('#acW','5511223344');await p.fill('#acE','mariana@correo.com');});await shot(p,'C01_crea_tu_cuenta',false);
 await st('accs',async()=>{await p.click('#acF button[type=submit]');await p.waitForTimeout(1200);});await shot(p,'C02_bienvenida',false);
 await st('ob',async()=>{await p.click('#obOk');await p.waitForTimeout(400);await p.fill('#agW','Cumpleaños de mi mamá');await p.fill('#agD','2027-03-14');await p.click('#agAdd');await p.waitForTimeout(300);});
 await shot(p,'C03_mis_fiestas_personales_descripcion');
 await st('ver',async()=>{await p.click('[data-vw] >> nth=0');await p.waitForTimeout(400);});await shot(p,'C04_ver_precotizacion_pdf',false);await st('verX',()=>p.click('#dX'));
 await st('pago',async()=>{await p.click('#contact');await p.waitForTimeout(500);});await shot(p,'C05_pago_planner_mas_proveedores',false);
 await st('pay',async()=>{await p.click('#doPay');await p.waitForTimeout(2600);});await shot(p,'C06_siguientes_pasos');
 await st('dec',async()=>{await p.click('#sOk');await p.waitForTimeout(400);});await shot(p,'C07_haras_equipo_con_planner');
 await st('perfil',async()=>{await p.click('.plcard .av');await p.waitForTimeout(400);});await shot(p,'C08_perfil_del_planner',false);await st('ppb',()=>p.click('#ppBack'));
 await st('elige',async()=>{await p.click('#pNo');await p.waitForTimeout(400);});await shot(p,'C09_elige_otra_opcion');
 await st('pick',async()=>{await p.click('#plPick');await p.waitForTimeout(300);await p.click('#sOk');await p.waitForTimeout(300);await p.click('#pYes');await p.waitForTimeout(400);});await shot(p,'C10_confirmando_trato');
 await st('lib',async()=>{await p.click('#sConf');await p.waitForTimeout(2600);});await shot(p,'C11_proveedores_liberados');
 await st('rate',async()=>{const s1=await p.$$('[data-sel$="|1"]');await s1[0].click();await p.waitForTimeout(400);const s0=await p.$$('[data-sel$="|0"]');await s0[1].click();await p.waitForTimeout(400);
  await p.click('[data-rw$="|Precio fuera de mi presupuesto"]');await p.click('[data-rw$="|Tardó en responder"]');await p.fill('[data-rpub] >> nth=0','Me encantó tu propuesta, pero se salió de mi presupuesto.');});
 await shot(p,'C12_seleccionado_y_no_seleccionado_con_motivos');
 await st('rok',async()=>{await p.click('[data-rok]');await p.waitForTimeout(400);});
 await st('past',async()=>{await p.evaluate(()=>document.getElementById('evPast').click());await p.waitForTimeout(600);await p.evaluate(()=>{document.querySelectorAll('[data-ps$="|5"]').forEach(x=>x.click());const s=document.querySelector('[data-st="5"]');s&&s.click();});await p.fill('#svNote','La barra se acabó antes de las 12, todo lo demás perfecto');});
 await shot(p,'C13_encuesta_un_dia_despues');
 await st('send',async()=>{await p.evaluate(()=>document.getElementById('svSend').click());await p.waitForTimeout(900);});await shot(p,'C14_mis_fiestas_celebrada');
  for(const [vt,n] of [['svc','C16'],['venue','C17'],['planner','C18']]){await p.evaluate(vt=>{U.tab="negocio";negState();U.neg.vt=vt;drawAcct();},vt);await shot(p,n+'_mi_negocio_'+vt+'_invitacion');}
 await p.evaluate(()=>{U.tab="bandeja";drawAcct();});await shot(p,'C19_bandeja');
 await p.evaluate(()=>{U.tab="perfil";drawAcct();});await shot(p,'C20_perfil');
 await p.evaluate(()=>{U.tab="negocio";U.neg.vt="svc";drawAcct();});
 await st('inv',async()=>{await p.click('#act');await p.waitForTimeout(800);});await shot(p,'C21_invitacion_lleva_a_la_puerta_proveedor',false);
 await p.close();

 // ================= CUENTA ÚNICA · llega por la puerta de negocio (Lupita)
 const q=await page();await q.goto(BASE+'index.html');await q.waitForTimeout(700);
 await q.evaluate(()=>window.postMessage({hqv:'negocio-publicado',datos:{nombre:'Lupita Ramírez',negocio:'Lupita Dulces y Antojos',wa:'5512345678',email:'lupita@ejemplo.com',tipos:['services','venue','planner'],servicios:[{cat:'Alimentos'}],url:'hayquevernos.com/lupita-dulces-y-antojos',completo:100}},'*'));
 await q.waitForTimeout(2000);await shot(q,'D01_sitio_publicado_en_tu_cuenta',false);
 const lup=async()=>{await q.evaluate(()=>{document.getElementById('modal').hidden=true;demoProv();const N=U.neg,sv=N.sol.filter(r=>r.vt==="svc");
   N.post.unshift({id:11,vt:"svc",ev:"Boda de Mariana López · 120 invitados",svc:"Mesas de dulces",date:new Date(Date.now()+40*864e5).toISOString().slice(0,10),stage:0,fin:null},{id:12,vt:"svc",ev:"15 años de Laura M. · 150 invitados",svc:"Galletas decoradas",date:new Date(Date.now()+55*864e5).toISOString().slice(0,10),stage:1,fin:null});
   });await q.waitForTimeout(400);};
 await lup();await shot(q,'D02_mi_negocio_servicios_solicitud_nueva');
 await q.evaluate(()=>{const sv=U.neg.sol.filter(r=>r.vt==="svc");sv[0].rej=true;sv[0].why=["El presupuesto no me alcanza","Muy poca anticipación"];U.neg.sel=sv[0].id;drawAcct();});await shot(q,'D03_rechazar_con_motivos');
 await st('spo',async()=>{await q.evaluate(()=>{const sv=U.neg.sol.filter(r=>r.vt==="svc");sv[0].rej=false;U.neg.sel=sv[1].id;drawAcct();});await q.click('[data-spo="'+await q.evaluate(()=>U.neg.sel)+'"]');await q.waitForTimeout(500);});await shot(q,'D04_postular_pide_plan_pro',false);
 await st('mens',async()=>{await q.click('[data-b="mensual"]').catch(()=>{});await q.waitForTimeout(300);});await shot(q,'D04b_plan_pro_mensual',false);
 await st('gopro',async()=>{await q.click('#goPro');await q.waitForTimeout(2600);});await shot(q,'D05_postulado_proyecto_completo_y_tracker_6_estados');
 await st('d5b',()=>q.evaluate(()=>{U.plan="gratis";const sv=U.neg.sol.filter(r=>r.vt==="svc");U.neg.sel=(sv.find(r=>r.st==="postulada")||sv[0]).id;drawAcct();}));await shot(q,'D05b_postulado_sin_pro');
 await q.evaluate(()=>{U.plan="pro";U.neg.vt="venue";U.neg.sel=null;drawAcct();});await shot(q,'D06_mi_negocio_venue');
 await q.evaluate(()=>{U.neg.vt="planner";U.neg.sel=null;drawAcct();});await shot(q,'D07_mi_negocio_planner_solicitud');
 await st('pdno',async()=>{await q.click('[data-pd$="|no"]');await q.waitForTimeout(300);await q.click('[data-pw$="|Presupuesto muy bajo"]');});await shot(q,'D08_planner_rechaza_con_motivo');
 await st('pdsi',async()=>{await q.click('[data-pd$="|si"]');await q.waitForTimeout(300);await q.click('[data-pw$="|Es mi especialidad"]');await q.fill('[id^="pc-"]','14000');await q.click('[data-pq$="|bien"]');await q.waitForTimeout(300);});await shot(q,'D09_planner_acepta_cobro_y_calidad');
 await st('pok',async()=>{await q.click('[data-pok]');await q.waitForTimeout(800);});await shot(q,'D10_mis_clientes_esperando_confirmacion');
 await st('jconf',async()=>{await q.click('#jConf');await q.waitForTimeout(1500);});await shot(q,'D11_mis_clientes_proveedores_liberados');
 await st('mias',async()=>{await q.evaluate(()=>{U.tab="fiestas";drawAcct();});});await shot(q,'D12_mis_fiestas_invitacion_azul');
 await q.evaluate(()=>{U.tab="bandeja";drawAcct();});await shot(q,'D13_bandeja');
 await q.evaluate(()=>{U.tab="perfil";drawAcct();});await shot(q,'D14_perfil');
 // cuenta con un solo tipo activado: las otras pestañas invitan
 await q.evaluate(()=>{U.site.tipos=["services"];U.tab="negocio";U.neg.vt="venue";drawAcct();});await shot(q,'D15_venue_sin_activar_invitacion');
 await q.evaluate(()=>{U.neg.vt="planner";drawAcct();});await shot(q,'D16_planner_sin_activar_invitacion');
 await q.close();

 // ================= CELULAR
 const m=await page(390,844);await m.goto(BASE+'index.html');await m.waitForTimeout(600);
 await m.evaluate(()=>demoUser());await m.waitForTimeout(500);await m.evaluate(()=>{U.tab="fiestas";U.sub="mias";U.eventId=null;drawAcct();});await shot(m,'M01_mis_fiestas_celular');
 await m.evaluate(()=>{U.tab="negocio";negState();U.neg.vt="planner";drawAcct();});await shot(m,'M02_mi_negocio_planner_mis_clientes_celular');
 await m.evaluate(()=>{U.tab="negocio";U.neg=null;negState();U.neg.vt="venue";drawAcct();});await shot(m,'M03_mi_negocio_venue_activar_celular');
 await m.evaluate(()=>demoProv());await m.waitForTimeout(400);await m.evaluate(()=>{drawAcct();});await shot(m,'M04_mi_negocio_servicios_celular');
 await m.evaluate(()=>{U.tab="fiestas";U.sub="mias";drawAcct();});await shot(m,'M05_mis_fiestas_invitacion_celular');
 await m.evaluate(()=>{U.tab="perfil";drawAcct();});await shot(m,'M06_perfil_celular');
 console.log('ERR',JSON.stringify(errs,null,1));await b.close();})();
