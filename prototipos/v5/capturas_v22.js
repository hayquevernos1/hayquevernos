const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots22/';
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag,cs,mob] of [[390,844,'m','light',true],[1280,900,'d','dark',false]]){const ctx=await b.newContext({viewport:{width:w,height:h},colorScheme:cs,isMobile:mob,hasTouch:mob});const p=await ctx.newPage();p.on('pageerror',e=>errs.push(tag+' '+e.message));
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(700);
await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(300);
await p.evaluate(()=>{step=stepList().findIndex(s=>s.id==="svc");render();});await p.waitForTimeout(900);
const J=f=>p.evaluate(f);
await p.click('#ruSave');await p.waitForTimeout(700);
for(const wv of ["labor","full","rent"]){await p.evaluate(wv=>document.querySelector(`.ru-tsb[data-w="${wv}"]`).scrollIntoView({block:"center"}),wv);await p.waitForTimeout(150);
 const y0=await J(()=>Math.round(document.querySelector('.ru-tsel').getBoundingClientRect().top));await p.click(`.ru-tsb[data-w="${wv}"]`);await p.waitForTimeout(250);
 const y1=await J(()=>Math.round(document.querySelector('.ru-tsel').getBoundingClientRect().top));console.log(tag,'clic',wv,'la fila se movió',y1-y0,'px');}
console.log(tag,'orden abierto',await J(()=>[...document.querySelectorAll('#ruIdent .ru-tg > b')].map(x=>x.textContent.trim()).join(' > ')));
// stepper y pills
await p.click('.ru-lr .ru-sp');await p.waitForTimeout(80);console.log(tag,'cantidad tras +',await J(()=>document.querySelector('.ru-lr .ru-lq').value));
await p.click('.ru-pt[data-k="ride"]');await p.waitForTimeout(150);console.log(tag,'transporte',await J(()=>!!document.querySelector('.ru-p-fee')));
await p.click('.ru-addc .ru-lab-c');await p.waitForTimeout(150);console.log(tag,'perfiles',await J(()=>document.querySelectorAll('.ru-lr').length));
const L=await p.$('.ru-labr');await L.screenshot({path:O+tag+'_personal.jpg',type:'jpeg',quality:75});
console.log(tag,'alto sección personal',await J(()=>Math.round(document.querySelector('.ru-labr').getBoundingClientRect().height)));
// bloqueo de paquetes
await p.click('#ruCancel');await p.evaluate(()=>{S.rprods=S.rprods.slice(0,1);ruDrawLists();});await p.waitForTimeout(150);
console.log(tag,'paquetes bloqueados',await J(()=>[document.getElementById('ruPkSec').classList.contains('locked'),document.getElementById('ruMk').disabled,document.getElementById('ruPkgs').innerText].join(' | ')));
await (await p.$('#ruPkSec')).screenshot({path:O+tag+'_bloqueo.jpg',type:'jpeg',quality:75});
console.log(tag,'sw',await J(()=>document.documentElement.scrollWidth));
await ctx.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
