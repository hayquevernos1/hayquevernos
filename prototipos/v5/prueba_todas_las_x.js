const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/negocio.html');await p.waitForTimeout(500);
const n=await p.evaluate(()=>{S=exampleState();drawTypes();return 0;});await p.click('#goProv');await p.waitForTimeout(200);
const steps=await p.evaluate(()=>stepList().map(s=>s.id));
for(const st of steps){for(const op of ["","f0","f1","f2","rt"]){
 const cls=await p.evaluate(([st,op])=>{S=exampleState();ensureState();step=stepList().findIndex(s=>s.id===st);if(op&&S.services[0])S.services[0].open=op;if(S.services[0])S.services[0].dlOpen=0;render();document.querySelectorAll('details').forEach(d=>d.open=true);return [...new Set([...document.querySelectorAll('#stepBody .bad, #stepBody .ofx')].filter(x=>x.offsetParent).map(x=>[...x.classList].filter(c=>!["link","bad"].includes(c)).join(".")))];},[st,op]);
 for(const c of cls){const r=await p.evaluate(([st,op,c])=>{S=exampleState();ensureState();step=stepList().findIndex(s=>s.id===st);if(op&&S.services[0])S.services[0].open=op;if(S.services[0])S.services[0].dlOpen=0;render();document.querySelectorAll('details').forEach(d=>d.open=true);
   const sel="#stepBody ."+(c||"bad").split(".").join(".");const x=[...document.querySelectorAll(sel)].find(e=>e.offsetParent);if(!x)return "noel";const a=JSON.stringify(S);x.click();return JSON.stringify(S)!==a?"OK":"FALLA";},[st,op,c]);
  global.N=(global.N||0)+1;if(r!=="OK")console.log(st,op,c,r);}}}console.log("probadas",global.N);
console.log('done ERRS',JSON.stringify(errs.slice(0,3)));await b.close();})();
