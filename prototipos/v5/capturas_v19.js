const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots19/';
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag] of [[1280,900,'d'],[390,844,'m']]){const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>errs.push(tag+' '+e.message));
const ex=async(o)=>{await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(500);await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(200);await p.evaluate((o)=>{step=stepList().findIndex(s=>s.id==="svc");S.services[0].open=o;render();},o);await p.waitForTimeout(200);};
const J=f=>p.evaluate(f);
// 1. orden y ficha abierta
await ex("");await J(()=>{const s=S.services[0];s.offers=[];s.open="";drawServices();});
for(const n of ["Cóctel","Banquete","Buffet"]){await p.click(`.fmt[data-k="food"][data-n="${n}"]`);await p.waitForTimeout(120);}
await p.click(`.fmt[data-k="drink"][data-n="Estación"]`);await p.waitForTimeout(120);await p.click(`.fmt[data-k="drink"][data-n="Barra"]`);await p.waitForTimeout(120);
console.log(tag,'orden',await J(()=>[...document.querySelectorAll('.box[data-i="0"] .ofc[data-j]')].map(x=>(x.classList.contains('open')?'*':'')+S.services[0].offers[+x.dataset.j].n).join(" > ")));
// 2. paquete: bebidas dentro del banquete
await ex("f1");await p.click('.ofc.open .rel-c[data-c="Bebidas"]');await p.waitForTimeout(150);
await p.click('.ofc.open .relbox[data-l="sv:Bebidas"] .pk-c[data-n="Café"]');await p.waitForTimeout(150);
console.log(tag,'bebidas',await J(()=>JSON.stringify(S.services[0].offers[1].svcs.find(v=>v.cat==="Bebidas").rows)),await J(()=>document.querySelector('.ofc.open .dlh b').textContent));
await p.click('.ofc.open .relbox[data-l="sv:Bebidas"] .pk-new');await p.fill('.ofc.open .relbox[data-l="sv:Bebidas"] .pk-in','Pulque curado');await p.click('.ofc.open .relbox[data-l="sv:Bebidas"] .pk-addb');await p.waitForTimeout(150);
console.log(tag,'otro',await J(()=>S.services[0].offers[1].svcs.find(v=>v.cat==="Bebidas").rows.map(r=>r.c+":"+r.u).join(",")));
const el=await p.$('.ofc.open');await el.screenshot({path:O+tag+'_banquete_paquete.jpg',type:'jpeg',quality:72});
// 3. tarifas seleccionables en barra
await ex("f2");console.log(tag,'tw antes',await J(()=>S.services[0].offers[2].tw.join(",")),'campos',await J(()=>document.querySelectorAll('.ofc.open .tgrp').length));
await p.click('.ofc.open .tsb[data-w="rent"]');await p.waitForTimeout(150);console.log(tag,'tw después',await J(()=>S.services[0].offers[2].tw.join(",")),'campos',await J(()=>document.querySelectorAll('.ofc.open .tgrp').length));
await p.click('.ofc.open .pkbox[data-l="ex"] .pk-c[data-n="Hora extra"]');await p.waitForTimeout(150);console.log(tag,'extra',await J(()=>JSON.stringify(S.services[0].offers[2].ext.map(e=>e.c+"|"+e.u))));
const t2=await p.$('.ofc.open');await t2.screenshot({path:O+tag+'_barra_tarifas.jpg',type:'jpeg',quality:72});
// 4. todas las X
const cnt=()=>J(()=>{const s=S.services[0];if(s.offers.length<3)return "offers "+s.offers.length;return [s.offers.length,s.offers[1].tiempos.length,s.offers[1].inc.length,s.offers[1].svcs[0].rows.length,s.offers[0].ext.length,s.offers[0].tar.length,s.rent.length,S.svcPkgs.length].join(",")});
for(const [o,pre,sel] of [["f1","",".ofc.open .m-x"],["f1","",".ofc.open .rws[data-l='in'] .r-x"],["f1","",".ofc.open .relbox .pr-x"],["f0","",".ofc.open .pkbox[data-l='ex'] .pr-x"],["f0",".ofc.open .ta-add",".ofc.open .ta-x"],["f1","",".ofc.open .of-x"],["","",".ofc.closed .ofx"],["rt","",".sr-rm"],["","",".pk-x"]]){
 await ex(o);if(pre){await p.click(pre);await p.waitForTimeout(150);}const a=await cnt();const e=await p.$(sel);if(!e){console.log(tag,'NO',sel);continue;}await e.click();await p.waitForTimeout(150);const z=await cnt();console.log(tag,a!==z?'OK ':'FALLA',sel,a,'→',z);}
// 5. pop-up al terminar
await ex("f1");await p.click('.ofc.open .of-ok');await p.waitForTimeout(700);console.log(tag,'popup',await J(()=>{const m=document.querySelector('.rmodal');return m?m.innerText.replace(/\n+/g," | ").slice(0,200):"none";}));
await p.screenshot({path:O+tag+'_popup.jpg',type:'jpeg',quality:72});
await p.click('.rmodal .reco-y');await p.waitForTimeout(400);console.log(tag,'tras sí',await J(()=>S.services.map(s=>s.cat+":"+s.offers.length).join(" | ")),await J(()=>!!document.querySelector('.rmodal')));
console.log(tag,'sw',await J(()=>document.documentElement.scrollWidth));
await p.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
