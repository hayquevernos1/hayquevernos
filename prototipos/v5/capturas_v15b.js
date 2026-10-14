const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots15/';
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag] of [[390,844,'m'],[1280,860,'d']]){
const q=await b.newPage({viewport:{width:w,height:h}});q.on('pageerror',e=>errs.push(tag+': '+e.message));
await q.goto('http://localhost:8765/index.html');await q.waitForTimeout(700);
await q.evaluate(()=>{demoProv();U.tab="negocio";U.neg.vt="svc";drawAcct();});await q.waitForTimeout(400);
await q.screenshot({path:O+tag+'_P0_negocio.jpg',fullPage:true,type:'jpeg',quality:75});
await q.click('#sReq');await q.waitForTimeout(900);await q.screenshot({path:O+tag+'_P1_lead_popup.jpg',type:'jpeg',quality:80});
await q.click('#lpGo');await q.waitForTimeout(500);
await q.evaluate(()=>{U.neg.post.unshift({id:11,vt:"svc",ev:"Boda de Mariana López · 120 invitados",svc:"Mesas de dulces",date:new Date(Date.now()+40*864e5).toISOString().slice(0,10),stage:0,fin:null});drawAcct();});
for(let i=0;i<8;i++){if(await q.evaluate(()=>!document.getElementById('modal').hidden))break;const bt=await q.$('[data-ps]');if(!bt)break;await bt.click();await q.waitForTimeout(250);}
await q.waitForTimeout(700);await q.screenshot({path:O+tag+'_P2_seleccionado_svc.jpg',type:'jpeg',quality:80});
await q.evaluate(()=>{document.getElementById('modal').hidden=true;U.neg.vt="planner";U.neg.sel=null;drawAcct();});await q.waitForTimeout(300);
try{await q.click('[data-pd$="|si"]');await q.waitForTimeout(300);await q.click('[data-pw$="|Es mi especialidad"]');await q.fill('[id^="pc-"]','14000');await q.click('[data-pq$="|bien"]');await q.waitForTimeout(300);await q.click('[data-pok]');await q.waitForTimeout(800);
await q.click('#jConf');await q.waitForTimeout(1200);}catch(e){errs.push(tag+' planner: '+e.message.split('\n')[0]);}
await q.screenshot({path:O+tag+'_P3_planner_seleccionado.jpg',type:'jpeg',quality:80});
await q.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
