const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots18/';
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag] of [[390,844,'m'],[1280,900,'d']]){const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>errs.push(tag+' '+e.message));
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(700);
await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(300);
await p.evaluate(()=>{step=stepList().findIndex(s=>s.id==="svc");S.services[0].open="f1";render();});await p.waitForTimeout(300);
const el=await p.$('.ofc.open');await el.scrollIntoViewIfNeeded();await el.screenshot({path:O+tag+'_banquete.jpg',type:'jpeg',quality:75});
// insumo nuevo: escribir platos en una nueva fila
await p.click('.ofc.open .rws[data-l="in"] .r-add');await p.waitForTimeout(150);
const ins=(await p.$$('.ofc.open .rws[data-l="in"] .r-c')).pop();await ins.fill('Hielo');await ins.dispatchEvent('change');await p.waitForTimeout(200);
console.log(tag,'unidad hielo',await p.evaluate(()=>{const L=S.services[0].offers[1].inc;return L[L.length-1].u;}));
// pax recalcula staff
await p.fill('.ofc.open .of-pax','150');await p.dispatchEvent('.ofc.open .of-pax','change');await p.waitForTimeout(200);
console.log(tag,'crew 150',await p.evaluate(()=>JSON.stringify(S.services[0].offers[1].crew.map(r=>r.n+":"+r.q))));
// servicio incluido nuevo
await p.click('.ofc.open .rel-c[data-c="Música"]');await p.waitForTimeout(200);
console.log(tag,'svcs',await p.evaluate(()=>S.services[0].offers[1].svcs.map(v=>v.cat).join(",")));
console.log(tag,'sw',await p.evaluate(()=>document.documentElement.scrollWidth));
// cerrar y ver recomendación
await p.evaluate(()=>{S.services[0].open="";drawServices();});await p.waitForTimeout(200);
const rc=await p.$('.reco');console.log(tag,'reco',rc?await rc.innerText():'none');
if(rc){await rc.scrollIntoViewIfNeeded();await rc.screenshot({path:O+tag+'_reco.jpg',type:'jpeg',quality:75});
 await p.click('.recor[data-c="Mobiliario y montaje"] .reco-y');await p.waitForTimeout(400);
 console.log(tag,'after yes',await p.evaluate(()=>S.services.map(s=>s.cat+":"+s.offers.map(o=>o.n).join("/")).join(" | ")));
 await p.screenshot({path:O+tag+'_reco_after.jpg',type:'jpeg',quality:70});}
console.log(tag,'missing',await p.evaluate(()=>JSON.stringify(missing("svc"))));
await p.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
