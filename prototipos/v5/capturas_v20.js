const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots20/';
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag,cs,mob] of [[390,844,'m','light',true],[1280,900,'d','dark',false]]){const ctx=await b.newContext({viewport:{width:w,height:h},colorScheme:cs,isMobile:mob,hasTouch:mob});const p=await ctx.newPage();p.on('pageerror',e=>errs.push(tag+' '+e.message));
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(700);
await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(300);
await p.evaluate(()=>{step=stepList().findIndex(s=>s.id==="svc");render();});await p.waitForTimeout(900);
const J=f=>p.evaluate(f);
console.log(tag,'rodillos',await J(()=>[...document.querySelectorAll('.ru-it.on')].map(x=>x.dataset.v).join(' | ')),'prods',await J(()=>document.getElementById('ruProdH').textContent),await J(()=>document.getElementById('ruPkgH').textContent));
console.log(tag,'missing',await J(()=>JSON.stringify(missing("svc"))));
await p.screenshot({path:O+tag+'_paso.jpg',type:'jpeg',quality:70,fullPage:true});
// buscar y guardar
await p.fill('#ruQ','dj boda');await p.waitForTimeout(150);console.log(tag,'busca',await J(()=>[...document.querySelectorAll('#ruQr button')].slice(0,2).map(b=>b.innerText.replace(/\n/g,' / ')).join(' || ')));
await p.keyboard.press('Enter');await p.waitForTimeout(1600);console.log(tag,'alineado',await J(()=>S.rsel.join(' › ')));
await p.click('#ruSave');await p.waitForTimeout(500);
console.log(tag,'orden secciones',await J(()=>[...document.querySelectorAll('#ruIdent .lbl, #ruIdent summary')].map(x=>x.textContent.trim().slice(0,28)).join(' → ')));
await p.click('.ru-tsb[data-w="full"]');await p.waitForTimeout(150);await p.fill('[data-tp="full"]','2500');await p.waitForTimeout(100);
const u=await J(()=>S&&document.querySelector('[data-tu="full"]').value);console.log(tag,'unidad sugerida',u);
if(await p.$('[data-tq="full"]')){await p.fill('[data-tq="full"]','5');}
await p.fill('#ruPax','150');await p.waitForTimeout(150);console.log(tag,'anfitrión',await J(()=>document.getElementById('ruHost').innerText.replace(/\n/g,' | ')));
// más opciones: extra con precio, entrega a domicilio
await p.click('#ruIdent details.ru-more summary');await p.waitForTimeout(150);
await p.fill('.ru-tags[data-t="ext"] input','hora');await p.waitForTimeout(150);await p.keyboard.press('Enter');await p.waitForTimeout(200);
console.log(tag,'extra',await J(()=>[...document.querySelectorAll('.ru-ex')].map(r=>r.querySelector('.ru-exc').value+' | '+r.querySelector('.ru-exu').value).join(',')),'foco en precio',await J(()=>document.activeElement.classList.contains('ru-exp')));
await p.keyboard.type('1200');
await p.click('#ruIdent .dlm[data-m="Recolección en establecimiento"]');await p.waitForTimeout(200);console.log(tag,'dirección local',await J(()=>document.querySelector('#ruIdent .dl-pa')?.value));
await (await p.$('#ruIdent')).screenshot({path:O+tag+'_identidad.jpg',type:'jpeg',quality:72});
await p.click('#ruOk');await p.waitForTimeout(300);console.log(tag,'error esperado',await J(()=>document.getElementById('ruErr')?.textContent));
await p.click('#ruIdent [id^="dly-"] button[data-v="0"]');await p.waitForTimeout(200);
await p.click('#ruIdent .dl-ok').catch(()=>{});await p.waitForTimeout(150);
await p.click('#ruOk');await p.waitForTimeout(500);console.log(tag,'guardado',await J(()=>document.getElementById('ruProdH').textContent),await J(()=>document.getElementById('ruErr')?.textContent||'ok'));
// sitio
const site=await J(()=>{const s=document.getElementById('site');return [...s.querySelectorAll('.po b')].map(x=>x.childNodes[0].textContent.trim()).join(' | ');});console.log(tag,'sitio',site);
console.log(tag,'sw',await J(()=>document.documentElement.scrollWidth));
await ctx.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
