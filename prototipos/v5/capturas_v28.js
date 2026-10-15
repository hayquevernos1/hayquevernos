const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots28/';
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag,cs,mob] of [[390,844,'m','light',true],[1280,900,'d','dark',false]]){const ctx=await b.newContext({viewport:{width:w,height:h},colorScheme:cs,isMobile:mob,hasTouch:mob});const p=await ctx.newPage();p.on('pageerror',e=>errs.push(tag+' '+e.stack.split('\n').slice(0,2).join(' ')));
ctx.on('page',pg=>pg.close().catch(()=>{}));
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(700);
await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(300);
const J=f=>p.evaluate(f);const go=id=>p.evaluate(id=>{step=stepList().findIndex(s=>s.id===id);render();},id);
await go("biz");await p.waitForTimeout(300);
console.log(tag,'biz missing',await J(()=>JSON.stringify(missing("biz"))),'fundación',await J(()=>$("f-found").value),'hint cuenta',await J(()=>/creamos tu cuenta/.test(document.body.innerText)));
await go("svc");await p.waitForTimeout(900);
console.log(tag,'copys',await J(()=>[document.querySelector('.ru-mt span').textContent,$("ruSave").textContent,$("ruUnit").hidden,!!document.querySelector('.panel>.sub'),[...document.querySelectorAll('.ru-st small')].map(x=>x.textContent).join(' / ')].join(' | ')));
console.log(tag,'formas',await J(()=>[...document.querySelectorAll('.ru-fc')].slice(0,2).map(c=>c.querySelector('.ru-fl').textContent+' ['+[...c.querySelectorAll('li')].map(l=>l.textContent).join('; ')+']').join(' || ')));
console.log(tag,'aviso paquete',await J(()=>(document.querySelector('.ru-chg')||{}).innerText));
await (await p.$('#ruPkSec')).screenshot({path:O+tag+'_paquetes.jpg',type:'jpeg',quality:65});
await p.click('.ru-upd');await p.waitForTimeout(200);console.log(tag,'tras actualizar',await J(()=>S.rpkgs[0].tar.full.p+' '+!!document.querySelector('.ru-chg')));
console.log(tag,'planners',await J(()=>$("ruPl").innerText.replace(/\s+/g,' ')));
// ficha
await p.click('.ru-grp[data-id="pdemo1"] .ru-gh [data-ed]');await p.waitForTimeout(500);
console.log(tag,'orden',await J(()=>[...document.querySelectorAll('#ruIdent .ru-tg[data-w="ins"], #ruIdent .ru-stw, #ruIdent .ru-dlw')].map(x=>x.dataset.w).join(' > ')),'título',await J(()=>$("ruName").placeholder+' | '+$("ruName").value));
await (await p.$('#ruIdent')).screenshot({path:O+tag+'_ficha.jpg',type:'jpeg',quality:55});
const hb=await p.$('.ru-paxc');await hb.screenshot({path:O+tag+'_host.jpg',type:'jpeg',quality:70});
await p.click('#ruCancel');await p.waitForTimeout(200);
// guardar con faltantes salta al error
await p.click('#ruSave');await p.waitForTimeout(600);await J(()=>{$("ruName").value="";RU_EDIT.name="";});await p.click('#ruOk');await p.waitForTimeout(600);
console.log(tag,'salto a error',await J(()=>[document.activeElement.id||document.activeElement.className,$("ruErr").textContent].join(' | ')));
await p.click('#ruCancel');await p.waitForTimeout(200);
// por hora más barato
await J(()=>{const m=S.rprods.find(x=>x.id==="st-mesero");m.labor[0].tars[1].p="150";});await p.click('.ru-sc[data-id="st-mesero"] [data-ed]');await p.waitForTimeout(400);console.log(tag,'aviso hora',await J(()=>(document.querySelector('.ru-warn')||{}).innerText));await p.click('#ruCancel');await J(()=>{S.rprods.find(x=>x.id==="st-mesero").labor[0].tars[1].p="250";});
// invitar planner
await p.click('#ruInv');await p.waitForTimeout(300);await p.fill('#ivN','Andrea López');await p.fill('#ivW','5512345678');await p.waitForTimeout(100);
console.log(tag,'mensaje',await J(()=>$("ivM").textContent.slice(0,140)),'href',await J(()=>$("ivWa").href.slice(0,40)));
await (await p.$('.ru-inv')).screenshot({path:O+tag+'_invitar.jpg',type:'jpeg',quality:65});
await p.click('#ivWa');await p.waitForTimeout(400);
console.log(tag,'invitaciones',await J(()=>JSON.stringify(S.invites.map(i=>i.name+':'+i.status))));
await p.click('.ru-sim');await p.waitForTimeout(300);await (await p.$('.ru-inv')).screenshot({path:O+tag+'_invitado.jpg',type:'jpeg',quality:65});
await p.click('#iaGo');await p.waitForTimeout(200);console.log(tag,'sin casilla',await J(()=>$("iaErr").textContent));
await p.check('#iaOk');await p.click('#iaGo');await p.waitForTimeout(300);await (await p.$('.ru-inv')).screenshot({path:O+tag+'_perfil_invitado.jpg',type:'jpeg',quality:65});await p.click('#ipBiz');console.log(tag,'bio negocio',await J(()=>$('ipBio').value.slice(0,40)));await p.fill('#ifP','12');await p.fill('#ifM','9000');await p.click('#ifGo');await p.waitForTimeout(400);
console.log(tag,'aceptó',await J(()=>$("ruPl").innerText.replace(/\s+/g,' ').slice(0,300)));
// combinador con planner
await p.click('#ruMk');await p.waitForTimeout(300);
console.log(tag,'gate?',await J(()=>!!document.querySelector('.ru-gates')),'pick',await J(()=>RU_PICK));
await p.click('.ru-fc[data-id="pdemo1"][data-w="full"] .ru-pick');const inv=await J(()=>"pl:"+S.invites[0].id);await p.click(`.ru-plc [data-ref="${inv}"]`);await p.click('#ruGo');await p.waitForTimeout(300);
console.log(tag,'paquete planner',await J(()=>document.querySelector('#ruIdent .ru-kits').innerText.replace(/\s+/g,' ')),'sug',await J(()=>(document.querySelector('.ru-sug')||{}).innerText.replace(/\s+/g,' ')));
await p.click('#ruCancel');
// pop-up: sin venue ni planner
await J(()=>{S.types.venue=false;S.types.planner=false;S.invites=[];S.askNo={};ruDrawLists();});
await p.click('#ruMk');await p.waitForTimeout(300);
console.log(tag,'gate',await J(()=>(document.querySelector('.ru-gates')||{}).innerText.replace(/\s+/g,' ')));
await (await p.$('.ru-gates')).screenshot({path:O+tag+'_gate.jpg',type:'jpeg',quality:65});
await p.click('.ru-gb[data-k="v"] [data-v="si"]');await p.click('.ru-gb[data-k="p"] [data-v="yo"]');console.log(tag,'botón',await J(()=>$("gtGo").textContent));await p.click('#gtGo');await p.waitForTimeout(500);
console.log(tag,'paso',await J(()=>stepList()[step].id),'banner',await J(()=>(document.querySelector('.ru-qb')||{}).innerText));
await p.click('.ru-qb button');await p.waitForTimeout(500);
console.log(tag,'paso2',await J(()=>stepList()[step].id),'planner prellenado',await J(()=>[S.planner.person,!!S.planner.photo,S.planner.instagram].join(' | ')),'banner',await J(()=>(document.querySelector('.ru-qb')||{}).innerText));
await p.click('.ru-qb button');await p.waitForTimeout(700);
console.log(tag,'regresa',await J(()=>stepList()[step].id+' pick '+RU_PICK+' '+JSON.stringify(RU_PICKED)));
// paquetes bloqueados
await J(()=>{RU_PICK=false;S.rprods=S.rprods.filter(x=>x.id==="pdemo3");S.types.venue=false;S.types.planner=false;ruDrawLists();});
await p.click('#ruPkSec');await p.waitForTimeout(500);console.log(tag,'burbuja',await J(()=>(document.querySelector('.ru-lockb')||{}).innerText));
await (await p.$('#ruPkSec')).screenshot({path:O+tag+'_bloqueado.jpg',type:'jpeg',quality:70});
await ctx.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
// v28 extra
(async()=>{const { chromium } = require('/opt/npm-tools/node_modules/playwright');const b=await chromium.launch();const errs=[];const p=await (await b.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true})).newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(700);await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(300);
const J=f=>p.evaluate(f),go=id=>p.evaluate(id=>{step=stepList().findIndex(s=>s.id===id);render();},id);
await go("svc");await p.waitForTimeout(700);
await J(()=>{S.rprods=S.rprods.filter(x=>x.id==="pdemo1"||x.kind==="staff");ruDrawLists();});
console.log('X lock con 1 producto + staff',await J(()=>$("ruPkSec").classList.contains("locked")));
await p.click('.ru-st.ru-step2');await p.waitForTimeout(500);console.log('X burbuja tarjeta',await J(()=>(document.querySelector('.ru-st .ru-lockb')||{}).innerText));
await p.screenshot({path:'shots28/m_tarjeta_bloqueada.jpg',type:'jpeg',quality:60,clip:{x:0,y:0,width:390,height:844}});
await p.click('.ru-grp[data-id="pdemo1"] .ru-gh [data-ed]');await p.waitForTimeout(400);
console.log('X transporte',await J(()=>[...document.querySelectorAll('.ru-pill')].map(x=>x.innerText.replace(/\s+/g,' ')).join(' | ')),'tiempos',await J(()=>document.querySelector('.ru-inc .ru-sl').textContent));
console.log('X host',await J(()=>document.querySelector('.ru-hr').innerText.replace(/\s+/g,' ')));
await (await p.$('.ru-paxc')).screenshot({path:'shots28/m_host.jpg',type:'jpeg',quality:70});
await p.click('#ruCancel');
await go("venue");await p.waitForTimeout(400);await p.click('.p-ext[data-v="algunos"]');await p.waitForTimeout(300);
const ti=await p.$('#vnSvc .ru-tags[data-t="extNo"] input');await ti.fill('alim');await p.waitForTimeout(200);console.log('X sugerencias',await J(()=>document.querySelector('#vnSvc .ru-sg').innerText.replace(/\s+/g,' | ')));await ti.press('Enter');await p.waitForTimeout(300);
const ti2=await p.$('#vnSvc .ru-tags[data-t="extNo"] input');await ti2.fill('Bebidas y barra, Música y espectáculos');await ti2.press('Enter');await p.waitForTimeout(300);
console.log('X no permitidos',await J(()=>JSON.stringify(S.venue.extNo)),'sitio',await J(()=>siteHtml().match(/Proveedores externos:[^<]*/)[0]));
await (await p.$('#vnSvc .polc')).screenshot({path:'shots28/m_no_permitidos.jpg',type:'jpeg',quality:70});
await go("planner");await p.waitForTimeout(400);
console.log('X planner fecha',await J(()=>$("pl-since").value),'bio=negocio',await J(()=>$("pl-bio").value===S.biz.about));
await p.fill('#pl-bio','Bio nueva desde planner');console.log('X bio sincronizada',await J(()=>S.biz.about));
await go("biz");await p.waitForTimeout(300);await p.fill('#f-about','Bio desde mi negocio');await p.fill('#f-found','2018-05-20');console.log('X sync inverso',await J(()=>S.planner.bio+' | '+S.planner.since));
console.log('X ERRS',JSON.stringify(errs));await b.close();})();
