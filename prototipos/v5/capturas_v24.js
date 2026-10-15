const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots24/';
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag,cs,mob] of [[390,844,'m','light',true],[1280,900,'d','dark',false]]){const ctx=await b.newContext({viewport:{width:w,height:h},colorScheme:cs,isMobile:mob,hasTouch:mob});const p=await ctx.newPage();p.on('pageerror',e=>errs.push(tag+' '+e.message));
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(700);
await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(300);
const J=f=>p.evaluate(f);
await p.evaluate(()=>{step=stepList().findIndex(s=>s.id==="biz");render();});await p.waitForTimeout(400);
console.log(tag,'biz missing',await J(()=>JSON.stringify(missing("biz"))),'secciones',await J(()=>[...document.querySelectorAll('.bz-h strong')].map(x=>x.textContent).join(' > ')));
await p.screenshot({path:O+tag+'_negocio.jpg',type:'jpeg',quality:65,fullPage:true});
console.log(tag,'hero',await J(()=>[document.querySelector('#site .ms-own')?.innerText,[...document.querySelectorAll('#site .ms-tags span')].map(x=>x.textContent).join(' | ')].join(' || ')));
await p.evaluate(()=>{step=stepList().findIndex(s=>s.id==="svc");render();});await p.waitForTimeout(900);
console.log(tag,'svc missing',await J(()=>JSON.stringify(missing("svc"))),'productos',await J(()=>[...document.querySelectorAll('#ruProds .ru-pc h4')].map(x=>x.textContent).join(' | ')));
// nuevo producto con personal: revisar desborde
await p.click('#ruSave');await p.waitForTimeout(600);await p.click('.ru-tsb[data-w="labor"]');await p.waitForTimeout(200);
console.log(tag,'desborde en ficha',await J(()=>{const W=innerWidth;return [...document.querySelectorAll('#ruIdent *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>W+1&&!e.closest('.ru-addc')&&!e.closest('.ru-reel');}).map(e=>e.className).slice(0,5).join(',')||'ninguno';}),'sw',await J(()=>document.documentElement.scrollWidth));
await (await p.$('.ru-labr')).screenshot({path:O+tag+'_personal.jpg',type:'jpeg',quality:75});
// cobertura
await p.click('.ru-covb[data-v="0"]');await p.waitForTimeout(200);console.log(tag,'otra zona',await J(()=>!!document.querySelector('#ruIdent [id^="zs-rupcv"]')));
await p.click('#ruCancel');await p.waitForTimeout(200);
// conflicto de precio: editar Barra sin alcohol y cambiar precio del bartender
await p.evaluate(()=>{const c=[...document.querySelectorAll('#ruProds .ru-pc')].find(x=>x.querySelector('h4').textContent.includes('Barra sin alcohol'));c.querySelector('[data-ed]').click();});await p.waitForTimeout(400);
await p.fill('.ru-lr .ru-lp','300');await p.click('#ruOk');await p.waitForTimeout(500);
console.log(tag,'conflicto',await J(()=>document.querySelector('.ru-confl')?.innerText.replace(/\n+/g,' | ')||'none'));
await p.screenshot({path:O+tag+'_conflicto.jpg',type:'jpeg',quality:70});
await p.click('.ru-cfb');await p.waitForTimeout(400);
console.log(tag,'staff tras elegir',await J(()=>JSON.stringify(S.rprods.find(x=>x.kind==="staff").labor.map(r=>r.n+":"+r.p))));
await ctx.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
