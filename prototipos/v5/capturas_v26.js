const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shots26/';
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag,cs,mob] of [[390,844,'m','light',true],[1280,900,'d','dark',false]]){const ctx=await b.newContext({viewport:{width:w,height:h},colorScheme:cs,isMobile:mob,hasTouch:mob});const p=await ctx.newPage();p.on('pageerror',e=>errs.push(tag+' '+e.stack.split('\n').slice(0,2).join(' ')));
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(700);
await p.evaluate(()=>{S=exampleState();drawTypes();});await p.click('#goProv');await p.waitForTimeout(300);
const J=f=>p.evaluate(f);const go=id=>p.evaluate(id=>{step=stepList().findIndex(s=>s.id===id);render();},id);
await go("biz");await p.waitForTimeout(300);
console.log(tag,'biz missing',await J(()=>JSON.stringify(missing("biz"))),'pins',await J(()=>[...document.querySelectorAll('.lbl')].filter(x=>/Dirección de tu negocio/.test(x.textContent)).map(x=>x.textContent).join('|')));
console.log(tag,'alineación tel/correo',await J(()=>{const a=$("f-wa").getBoundingClientRect().top,b=$("f-email").getBoundingClientRect().top;return Math.round(a-b);}));
await p.click('.bz-sh[data-v="0"]');await p.waitForTimeout(200);
console.log(tag,'por día filas',await J(()=>document.querySelectorAll('.bz-hd').length),'missing',await J(()=>JSON.stringify(missing("biz"))),'texto',await J(()=>bzHours(S.biz)));
await J(()=>{const r=document.querySelector('.bz-hd[data-d="sab"]');if(r){const i=r.querySelector('.bz-hc');i.value="14:00";i.dispatchEvent(new Event('input'));}});
console.log(tag,'horario',await J(()=>bzHours(S.biz)));
const att=await p.$('.bz-att');if(att)await att.screenshot({path:O+tag+'_horario.jpg',type:'jpeg',quality:70});
const r1=await p.$('.bz-row');if(r1)await r1.screenshot({path:O+tag+'_telcorreo.jpg',type:'jpeg',quality:70});
await go("svc");await p.waitForTimeout(900);
console.log(tag,'grupos',await J(()=>[...document.querySelectorAll('.ru-grp')].map(g=>g.querySelector('h4').textContent+' ['+[...g.querySelectorAll('.ru-fc')].map(c=>c.querySelector('.ru-fl').textContent+' '+c.querySelector('.ru-tot')?.textContent).join(' / ')+']').join(' || ')));
console.log(tag,'personal',await J(()=>[...document.querySelectorAll('.ru-sc')].map(x=>x.innerText.replace(/\s+/g,' ')).join(' | ')),'svc missing',await J(()=>JSON.stringify(missing("svc"))));
await (await p.$('#ruProds')).screenshot({path:O+tag+'_productos.jpg',type:'jpeg',quality:65});
await p.click('.ru-grp[data-id="pdemo1"] .ru-fc[data-w="full"] [data-ed]');await p.waitForTimeout(500);
await (await p.$('#ruIdent .ru-inc')).screenshot({path:O+tag+'_tiempos.jpg',type:'jpeg',quality:70});
const fu=await p.$('#ruIdent .ru-tg[data-w="full"]');await fu.screenshot({path:O+tag+'_con_personal.jpg',type:'jpeg',quality:72});
console.log(tag,'simulación',await J(()=>document.querySelector('#ruExBox').innerText.replace(/\s+/g,' ').slice(0,420)));
console.log(tag,'desborde',await J(()=>{const W=innerWidth;return [...document.querySelectorAll('#ruIdent *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>W+1&&!e.closest('.ru-addc')&&!e.closest('.ru-reel');}).map(e=>e.className).slice(0,5).join(',')||'ninguno';}),'sw',await J(()=>document.documentElement.scrollWidth));
// agregar forma de cobro y tiempo
await p.click('#ruIdent .ru-lr[data-ix="1"] .ru-addt');await p.waitForTimeout(200);console.log(tag,'tarifas cocinero',await J(()=>JSON.stringify(RU_EDIT.labor[1].tars)));
await p.click('#ruIdent .ru-cadd');await p.waitForTimeout(200);console.log(tag,'tiempos',await J(()=>RU_EDIT.courses.map(c=>c.n).join(', ')));
const inp=await p.$('#ruIdent .ru-tags[data-t="course3"] input');await inp.fill('Pastel de tres leches, café');await inp.press('Enter');await p.waitForTimeout(200);console.log(tag,'coma',await J(()=>JSON.stringify(RU_EDIT.courses[3].d)));
await p.click('#ruCancel');await p.waitForTimeout(200);
// producto nuevo: sin personal + recoger
await p.click('#ruSave');await p.waitForTimeout(600);await p.click('.ru-tsb[data-w="rent"]');await p.waitForTimeout(200);
await J(()=>{const b=[...document.querySelectorAll('#ruIdent .dlm')].find(x=>/Recoger/.test(x.textContent));b&&b.click();});await p.waitForTimeout(200);
console.log(tag,'recoger',await J(()=>{const c=document.querySelector('#ruIdent .dlc.open');return c?c.innerText.replace(/\s+/g,' ').slice(0,220):'-';}),'cobra',await J(()=>RU_EDIT.dlx.dl.map(d=>d.m+':'+d.cobra+':'+d.ph).join(' | ')));
const rt=await p.$('#ruIdent .ru-tsel');await p.click('.ru-tsb[data-w="full"]');await p.waitForTimeout(200);
await (await p.$('#ruIdent .ru-tsel')).screenshot({path:O+tag+'_entrega_cobro.jpg',type:'jpeg',quality:70});
const nf=await p.$('#ruIdent .ru-tg[data-w="full"]');if(nf)await nf.screenshot({path:O+tag+'_con_personal_nuevo.jpg',type:'jpeg',quality:72});
console.log(tag,'nuevo labor',await J(()=>JSON.stringify(RU_EDIT.labor.map(r=>[r.n,r.tars.map(t=>t.p+' '+t.u).join('/')]))));
await p.click('#ruCancel');await p.waitForTimeout(200);
// ficha de un perfil
await p.click('.ru-sc[data-id="st-mesero"] [data-ed]');await p.waitForTimeout(400);
await (await p.$('#ruIdent')).screenshot({path:O+tag+'_perfil_mesero.jpg',type:'jpeg',quality:65});
console.log(tag,'mesero host',await J(()=>$("ruHost").innerText.replace(/\s+/g,' ').slice(0,300)));
await p.click('#ruCancel');
// combinador
await p.click('#ruMk');await p.waitForTimeout(300);await p.click('.ru-vc .ru-pick');await p.click('.ru-fc[data-id="pdemo1"][data-w="full"] .ru-pick');await p.click('.ru-sc[data-id="st-bartender"] .ru-pick');await p.click('#ruGo');await p.waitForTimeout(300);
console.log(tag,'paquete',await J(()=>document.querySelector('#ruIdent .ru-kits').innerText.replace(/\s+/g,' ')),'sug',await J(()=>(document.querySelector('.ru-sug')||{}).innerText));
await p.click('#ruCancel');
await go("venue");await p.waitForTimeout(500);
console.log(tag,'venue filas',await J(()=>[...document.querySelectorAll('.vn-r')].map(r=>r.innerText.replace(/\s+/g,' ').slice(0,70)).join(' | ')),'venue missing',await J(()=>JSON.stringify(missing("venue"))));
await (await p.$('#vnSvc')).screenshot({path:O+tag+'_venue.jpg',type:'jpeg',quality:60});
await go("svc");await p.waitForTimeout(400);
if(mob){await p.click('text=Ver mi sitio');await p.waitForTimeout(400);}
const pl=(await p.$$('#site .plist'))[1];if(pl)await pl.screenshot({path:O+tag+'_sitio.jpg',type:'jpeg',quality:60});
await ctx.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
