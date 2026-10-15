const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots16/';require('fs').mkdirSync(O,{recursive:true});
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag] of [[1280,900,'d'],[390,844,'m']]){
const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>errs.push(tag+' '+e.message));
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(700);
await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(300);
await p.evaluate(()=>{step=stepList().findIndex(s=>s.id==="svc");S.services[0].open="f0";render();});await p.waitForTimeout(400);
await p.screenshot({path:O+tag+'_R03_buffet_abierto.jpg',fullPage:true,type:'jpeg',quality:72});
await p.evaluate(()=>{S.services[0].open="f1";drawServices();});await p.waitForTimeout(300);await p.screenshot({path:O+tag+'_R03b_banquete_tiempos.jpg',fullPage:true,type:'jpeg',quality:72});
await p.evaluate(()=>{S.services[0].open="f2";drawServices();});await p.waitForTimeout(300);await p.screenshot({path:O+tag+'_R03c_bebidas_barra.jpg',fullPage:true,type:'jpeg',quality:72});
// predictivo
await p.evaluate(()=>{S.services[0].open="f0";drawServices();});await p.waitForTimeout(200);
const inp=(await p.$$('.ofc.open .m-d'))[0];await inp.fill('');await inp.type('pozo');await p.waitForTimeout(300);
await p.screenshot({path:O+tag+'_R03d_predictivo.jpg',type:'jpeg',quality:72});
console.log(tag,'sugg',await p.evaluate(()=>{const b=document.querySelector('.sgf');return b&&!b.hidden?b.innerText.replace(/\n/g,' | '):'none';}));
// nueva categoría general
await p.evaluate(()=>{S.services.push(blankSvc());drawServices();});await p.click('.box[data-i="1"] .cat[data-c="Música"]');await p.click('.box[data-i="1"] .way[data-w="full"]');await p.click('.box[data-i="1"] .fmt[data-n="DJ"]');await p.fill('.box[data-i="1"] .ofc.open .ta-p','6500');await p.waitForTimeout(200);
await p.screenshot({path:O+tag+'_R03e_musica_dj.jpg',fullPage:true,type:'jpeg',quality:72});
console.log(tag,'sw',await p.evaluate(()=>document.documentElement.scrollWidth),'miss',JSON.stringify(await p.evaluate(()=>missing("svc"))));
await p.evaluate(()=>{S=exampleState();demo=true;showPublic("home");});await p.waitForTimeout(400);await p.screenshot({path:O+tag+'_R08_sitio_publico.jpg',fullPage:true,type:'jpeg',quality:72});
await p.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
