const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots17/';
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag] of [[390,844,'m'],[1280,900,'d']]){const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>errs.push(tag+' '+e.message));
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(700);
await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(300);
await p.evaluate(()=>{step=stepList().findIndex(s=>s.id==="svc");S.services[0].open="st";render();});await p.waitForTimeout(300);
const el=await p.$('.inv .dlc.open');await el.scrollIntoViewIfNeeded();await p.screenshot({path:O+tag+'_R03f_staff_abierto.jpg',fullPage:true,type:'jpeg',quality:72});
await p.evaluate(()=>{S.services[0].open="rt";drawServices();});await p.waitForTimeout(300);
await p.evaluate(()=>{S.services[0].rtx.dlOpen=0;drawServices();});await p.screenshot({path:O+tag+'_R03g_renta_recoger_en_local.jpg',fullPage:true,type:'jpeg',quality:72});
// ideas
await p.evaluate(()=>{S.services[0].open="f1";drawServices();});await p.waitForTimeout(200);const d=(await p.$$('.ofc.open .m-d'))[1];await d.focus();await p.waitForTimeout(300);
console.log(tag,'ideas',await p.evaluate(()=>{const r=document.querySelector('.mr.act .ideas');return r?r.innerText.replace(/\n/g,' '):'none';}));
await p.screenshot({path:O+tag+'_R03h_ideas_cremas.jpg',type:'jpeg',quality:72});
console.log(tag,'sw',await p.evaluate(()=>document.documentElement.scrollWidth));
await p.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
