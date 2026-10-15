const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots21/';
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag,cs,mob] of [[390,844,'m','light',true],[1280,900,'d','dark',false]]){const ctx=await b.newContext({viewport:{width:w,height:h},colorScheme:cs,isMobile:mob,hasTouch:mob});const p=await ctx.newPage();p.on('pageerror',e=>errs.push(tag+' '+e.message));
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(700);
await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(300);
await p.evaluate(()=>{step=stepList().findIndex(s=>s.id==="svc");render();});await p.waitForTimeout(900);
const J=f=>p.evaluate(f);
console.log(tag,'missing demo',await J(()=>JSON.stringify(missing("svc"))));
await p.click('#ruSave');await p.waitForTimeout(500);
await p.click('.ru-tsb[data-w="rent"]');await p.waitForTimeout(150);
console.log(tag,'sin personal: campo cuántas',!!(await p.$('[data-tq="rent"]')),'entrega',await J(()=>[...document.querySelectorAll('#ruIdent .dlsec .dlm')].map(x=>x.textContent.trim()).join(', ')));
await p.fill('[data-tp="rent"]','60');
await p.click('#ruIdent .dlm[data-m="Recolección en establecimiento"]');await p.waitForTimeout(200);
console.log(tag,'dirección',await J(()=>document.querySelector('#ruIdent .dl-pa')?.value));
await p.click('#ruIdent [id^="dly-"] button[data-v="0"]');await p.waitForTimeout(150);await p.click('#ruIdent .dl-ok');await p.waitForTimeout(150);
await p.click('.ru-tsb[data-w="labor"]');await p.waitForTimeout(150);
console.log(tag,'perfiles',await J(()=>[...document.querySelectorAll('.ru-lr .ru-ln')].map(x=>x.textContent).join(', ')),'políticas',await J(()=>document.querySelectorAll('.ru-pol label').length));
const lp=await p.$$('.ru-lp');for(const [i,el] of lp.entries()){await el.fill(String(250+i*50));}
await p.fill('#ruPax','80');await p.waitForTimeout(150);
console.log(tag,'anfitrión',await J(()=>document.getElementById('ruHost').innerText.replace(/\n/g,' | ')));
await (await p.$('#ruIdent')).screenshot({path:O+tag+'_identidad.jpg',type:'jpeg',quality:72});
await p.click('#ruOk');await p.waitForTimeout(500);console.log(tag,'guardado',await J(()=>document.getElementById('ruProdH').textContent),await J(()=>document.getElementById('ruErr')?.textContent||'ok'));
console.log(tag,'sitio',await J(()=>[...document.querySelectorAll('#site .po .inc')].map(x=>x.textContent).filter(t=>/Sin personal|Solo personal|completo/.test(t)).slice(0,4).join(' || ')));
console.log(tag,'sw',await J(()=>document.documentElement.scrollWidth));
await ctx.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
