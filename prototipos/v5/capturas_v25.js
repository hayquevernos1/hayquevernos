const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots25/';
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag,cs,mob] of [[390,844,'m','light',true],[1280,900,'d','dark',false]]){const ctx=await b.newContext({viewport:{width:w,height:h},colorScheme:cs,isMobile:mob,hasTouch:mob});const p=await ctx.newPage();p.on('pageerror',e=>errs.push(tag+' '+e.message));p.on('console',m=>{if(m.type()==='error')errs.push(tag+' console '+m.text());});
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(700);
await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(300);
const J=f=>p.evaluate(f);const go=id=>p.evaluate(id=>{step=stepList().findIndex(s=>s.id===id);render();},id);
await J(()=>{step=stepList().findIndex(s=>s.id==="biz");render();});await p.waitForTimeout(300);
console.log(tag,'biz missing',await J(()=>JSON.stringify(missing("biz"))),'me.same',await J(()=>JSON.stringify(S.me.same)));
// cambiar el correo personal a mismo que negocio (reuse)
const ru=await p.$('.bz-reuse[data-k="email"]');if(ru){await ru.click();await p.waitForTimeout(150);}
console.log(tag,'correo personal',await J(()=>[S.me.email,S.account.email,$("me-em").value].join(" | ")));
await p.selectOption('#f-wa-cc','US');await p.waitForTimeout(150);
console.log(tag,'lada US missing',await J(()=>JSON.stringify(missing("biz"))),'wa link',await J(()=>(document.querySelector('#site a.wa')||{}).href));
await p.selectOption('#f-wa-cc','MX');await p.waitForTimeout(150);
await (await p.$('.bz-sec:nth-of-type(3)')||await p.$('.bz-sec')).screenshot({path:O+tag+'_perfil.jpg',type:'jpeg',quality:70}).catch(()=>{});
await go("svc");await p.waitForTimeout(900);
console.log(tag,'grupos',await J(()=>[...document.querySelectorAll('.ru-grp')].map(g=>g.querySelector('h4').textContent+' ['+[...g.querySelectorAll('.ru-fc')].map(c=>c.querySelector('.ru-fl').textContent+' '+c.querySelector('.ru-tot')?.textContent).join(' / ')+']').join(' || ')));
console.log(tag,'personal',await J(()=>[...document.querySelectorAll('.ru-sc h4')].map(x=>x.textContent).join(', ')),'paquetes',await J(()=>[...document.querySelectorAll('.ru-kc h4')].map(x=>x.textContent).join(', ')),'svc missing',await J(()=>JSON.stringify(missing("svc"))));
await (await p.$('#ruProds')).screenshot({path:O+tag+'_productos.jpg',type:'jpeg',quality:70});
await (await p.$('#ruStaffSec')).screenshot({path:O+tag+'_personal_lista.jpg',type:'jpeg',quality:70});
// quitar una forma y deshacer
await p.click('.ru-grp[data-id="pdemo1"] .ru-fc[data-w="rent"] [data-rm]');await p.waitForTimeout(150);
console.log(tag,'tras quitar forma',await J(()=>S.rprods.find(x=>x.id==="pdemo1").tw.join(",")));await p.click('.ru-toast .link');await p.waitForTimeout(150);
console.log(tag,'deshacer',await J(()=>S.rprods.find(x=>x.id==="pdemo1").tw.join(",")));
// editar forma labor abre ficha
await p.click('.ru-grp[data-id="pdemo1"] .ru-fc[data-w="labor"] [data-ed]');await p.waitForTimeout(500);
await (await p.$('#ruIdent .ru-labr')).screenshot({path:O+tag+'_personal_ficha.jpg',type:'jpeg',quality:75});
console.log(tag,'desborde ficha',await J(()=>{const W=innerWidth;return [...document.querySelectorAll('#ruIdent *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>W+1&&!e.closest('.ru-addc')&&!e.closest('.ru-reel');}).map(e=>e.className).slice(0,5).join(',')||'ninguno';}),'sw',await J(()=>document.documentElement.scrollWidth));
// min y promo
await J(()=>{document.querySelector('#ruIdent details.ru-more').open=true;});await p.waitForTimeout(100);
const yes=await p.$('#ruIdent [id^="mn-"] button, #ruIdent .yn button');console.log(tag,'yn botones',await J(()=>[...document.querySelectorAll('#ruIdent details.ru-more .yn button, #ruIdent details.ru-more [data-yn]')].length));
await J(()=>{const b=[...document.querySelectorAll('#ruIdent details.ru-more button')].find(x=>/^Sí/.test(x.textContent.trim()));b&&b.click();});await p.waitForTimeout(200);
console.log(tag,'minimo has',await J(()=>RU_EDIT.min.has));
await p.click('#ruCancel');await p.waitForTimeout(200);
// producto nuevo: personal prellenado
await p.click('#ruSave');await p.waitForTimeout(600);await p.click('.ru-tsb[data-w="labor"]');await p.waitForTimeout(200);
await J(()=>{const b=[...document.querySelectorAll('.ru-lab-c')].find(x=>x.dataset.n==="Mesero");b&&b.click();});await p.waitForTimeout(200);
console.log(tag,'mesero prellenado',await J(()=>JSON.stringify(RU_EDIT.labor.find(r=>r.n==="Mesero")||RU_EDIT.labor)));
await (await p.$('#ruIdent .ru-labr')).screenshot({path:O+tag+'_personal_nuevo.jpg',type:'jpeg',quality:75});
// sin personal + recoger en mi negocio con costo
await p.click('.ru-tsb[data-w="rent"]');await p.waitForTimeout(200);
await J(()=>{const b=[...document.querySelectorAll('#ruIdent .dlm')].find(x=>/Recoger/.test(x.textContent));b&&b.click();});await p.waitForTimeout(200);
console.log(tag,'chip recoger',await J(()=>[...document.querySelectorAll('#ruIdent .dlm')].map(x=>x.textContent.trim()).join(' | ')));
await J(()=>{const c=document.querySelector('#ruIdent .dlc.open .dlq');const b=c&&[...c.querySelectorAll('button')].find(x=>/^Sí/.test(x.textContent.trim()));b&&b.click();});await p.waitForTimeout(200);
console.log(tag,'recoger con costo',await J(()=>{const c=document.querySelector('#ruIdent .dlc.open');return c?c.innerText.replace(/\s+/g,' ').slice(0,200):'-';}));
await p.click('#ruCancel');await p.waitForTimeout(200);
// combinador con venue
await p.click('#ruMk');await p.waitForTimeout(300);
console.log(tag,'venue en combinador',await J(()=>!!document.querySelector('.ru-vc')));
await p.click('.ru-vc .ru-pick');await p.waitForTimeout(100);await p.click('.ru-fc[data-id="pdemo1"][data-w="full"] .ru-pick');await p.waitForTimeout(100);await p.click('.ru-sc[data-id="st-mesero"] .ru-pick');await p.waitForTimeout(100);
await (await p.$('#ruProds')).screenshot({path:O+tag+'_combinar.jpg',type:'jpeg',quality:65}).catch(()=>{});
await p.click('#ruGo');await p.waitForTimeout(400);
console.log(tag,'paquete items',await J(()=>JSON.stringify(RU_EDIT.items)),'crumbs',await J(()=>document.querySelector('#ruIdent .ru-kits').innerText.replace(/\s+/g,' ')),'sug',await J(()=>(document.querySelector('.ru-sug')||{}).innerText));
await p.fill('[data-kq="st-mesero"]','3');await p.waitForTimeout(100);console.log(tag,'qty',await J(()=>RU_EDIT.qty["st-mesero"]));
await p.click('#ruCancel');
// venue
await go("venue");await p.waitForTimeout(500);
console.log(tag,'venue filas',await J(()=>[...document.querySelectorAll('.vn-r')].map(r=>r.querySelector('b').textContent+(r.classList.contains('off')?' (no)':'')).join(', ')),'pk',await J(()=>[...document.querySelectorAll('.vn-kc b')].map(x=>x.textContent).join(', ')),'venue missing',await J(()=>JSON.stringify(missing("venue"))));
const sv=await p.$('#vnSvc');await sv.screenshot({path:O+tag+'_venue_servicios.jpg',type:'jpeg',quality:70});
const vp=await p.$('.vn-pk');if(vp)await vp.screenshot({path:O+tag+'_venue_paquetes.jpg',type:'jpeg',quality:70});
await p.click('.vn-r[data-ref="st-bartender"] .vn-on');await p.waitForTimeout(100);console.log(tag,'toggle bartender',await J(()=>S.venue.svcIn["st-bartender"].on));
// sitio
await J(()=>{renderSite&&renderSite();}).catch(()=>{});
console.log(tag,'sitio venue',await J(()=>{const x=document.querySelector('#site .vn-site');return x?x.innerText.replace(/\s+/g,' ').slice(0,260):'-';}));
console.log(tag,'sitio personal',await J(()=>{const x=document.querySelector('#site .pstaff');return x?x.innerText.replace(/\s+/g,' ').slice(0,200):'-';}),'formas',await J(()=>document.querySelectorAll('#site .pform').length));
// venue-only
await J(()=>{S.types.services=false;step=stepList().findIndex(s=>s.id==="venue");render();});await p.waitForTimeout(500);
console.log(tag,'solo venue builder',await J(()=>!!document.querySelector('.vn-build #ruReel0')),'open',await J(()=>document.querySelector('.vn-build').open));
await p.click('#vnMkPk');await p.waitForTimeout(400);console.log(tag,'solo venue pick',await J(()=>RU_PICK+' '+JSON.stringify(RU_PICKED)));
await p.screenshot({path:O+tag+'_solo_venue.jpg',type:'jpeg',quality:60});
await ctx.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
