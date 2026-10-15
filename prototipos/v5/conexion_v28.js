const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();const errs=[];const ctx=await b.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});const p=await ctx.newPage();p.on('pageerror',e=>errs.push('shell '+e.message));
await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(900);
await p.evaluate(()=>{demoUser();show("acct");});await p.waitForTimeout(400);
await p.evaluate(()=>openJourney("negocio"));await p.waitForTimeout(1500);
const fr=p.frame({url:/negocio\.html/});fr.on&&0;
await fr.evaluate(()=>{S=exampleState();S.biz.name="Lupita Dulces y Antojos";publish();});await p.waitForTimeout(800);
console.log('site oferta',await p.evaluate(()=>JSON.stringify((U.site.oferta||[]).map(o=>o.tipo+':'+o.cat+':'+o.nombre))));
console.log('payload keys',await p.evaluate(()=>Object.keys(U.site).join(',')));
console.log('producto0',await p.evaluate(()=>JSON.stringify(U.site.productos[0]).slice(0,500)));
await p.evaluate(()=>{$("modal").hidden=true;$("modal").innerHTML="";U.tab="fiestas";U.events[0].paid="prov";U.eventId=U.events[0].id;show("acct");drawAcct();});await p.waitForTimeout(600);
const ev=await p.evaluate(()=>{const e=U.events[0];return Object.keys(e.provs).map(k=>k+': '+e.provs[k].filter(x=>x.mine).map(x=>`${x.nm} $${x.price} ${x.unit||''} [${x.sub}]`).join(' | ')).join('\n');});console.log(ev);
console.log('cards mine en DOM',await p.evaluate(()=>document.querySelectorAll('.why.mine').length),'pp2',await p.evaluate(()=>(document.querySelector('.pp2')||{}).innerText));
const m=await p.$('.why.mine');if(m){const c=await m.evaluateHandle(x=>x.closest('.prov'));await c.asElement().screenshot({path:'shots28/m_cuenta_tu_negocio.jpg',type:'jpeg',quality:70});}
console.log('planners',await p.evaluate(()=>{const e=U.events[0];return JSON.stringify(myPlanners(e));}));
console.log('ERRS',JSON.stringify(errs));await b.close();})();
