const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots15/';
(async()=>{const b=await chromium.launch();const errs=[];const p=await b.newPage({viewport:{width:1280,height:900}});p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(700);
await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(400);
await p.evaluate(()=>{const i=stepList().findIndex(s=>s.id==="svc");step=i;render();});await p.waitForTimeout(300);
await p.screenshot({path:O+'a_svc_demo.jpg',fullPage:true,type:'jpeg',quality:75});
console.log('miss',JSON.stringify(await p.evaluate(()=>missing("svc"))));
await p.click('.ofc[data-j="0"] .of-open');await p.waitForTimeout(300);
await p.screenshot({path:O+'b_offer_open.jpg',fullPage:true,type:'jpeg',quality:75});
// flujo nuevo desde cero
await p.evaluate(()=>{S.services.push(blankSvc());drawServices();});await p.waitForTimeout(200);
await p.click('.box[data-i="1"] .cat[data-c="Música"]');await p.waitForTimeout(200);
await p.click('.box[data-i="1"] .way[data-w="full"]');await p.waitForTimeout(200);
await p.click('.box[data-i="1"] .of-c[data-n="DJ"]');await p.waitForTimeout(200);
await p.fill('.box[data-i="1"] .ofc.open .ta-p','650');await p.waitForTimeout(200);
await p.click('.box[data-i="0"] .of-c[data-n="Barra de bebidas"]');await p.waitForTimeout(200);
await p.screenshot({path:O+'c_new_box.jpg',fullPage:true,type:'jpeg',quality:75});
// buscar
await p.fill('#svcQ','pastor');await p.waitForTimeout(300);console.log('q',await p.$eval('#svcQr',e=>e.innerText.slice(0,300)));
await p.fill('#svcQ','meseros');await p.waitForTimeout(300);console.log('q2',await p.$eval('#svcQr',e=>e.innerText.slice(0,200)));
await p.evaluate(()=>{const i=stepList().findIndex(s=>s.id==="venue");step=i;render();});await p.waitForTimeout(300);
await p.screenshot({path:O+'d_venue.jpg',fullPage:true,type:'jpeg',quality:75});
console.log('missV',JSON.stringify(await p.evaluate(()=>missing("venue"))));
await p.evaluate(()=>{const i=stepList().findIndex(s=>s.id==="planner");step=i;render();});await p.waitForTimeout(300);
await p.screenshot({path:O+'e_planner.jpg',fullPage:true,type:'jpeg',quality:75});
console.log('missP',JSON.stringify(await p.evaluate(()=>missing("planner"))));
console.log('ERRS',JSON.stringify(errs));await b.close();})();
