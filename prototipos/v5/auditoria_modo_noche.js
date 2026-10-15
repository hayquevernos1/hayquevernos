const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const BASE='http://localhost:8765/';const WIDTH=+(process.argv[2]||1280);
const AUDIT=()=>{const P=s=>{const m=s.match(/rgba?\(([^)]+)\)/);if(!m)return null;const a=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);return[a[0],a[1],a[2],a.length>3?a[3]:1];};
 const L=c=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4);};return .2126*f(c[0])+.7152*f(c[1])+.0722*f(c[2]);};
 const bgOf=el=>{const layers=[];let e=el;while(e&&e.nodeType===1){const cs=getComputedStyle(e);if(cs.backgroundImage&&cs.backgroundImage!=="none"&&!/url\(/.test(cs.backgroundImage))return null;const c=P(cs.backgroundColor);if(c&&c[3]>0){layers.push(c);if(c[3]>=1)break;}e=e.parentElement;}
  let base=[255,255,255];if(!layers.length||layers[layers.length-1][3]<1){const cs=getComputedStyle(document.body);const c=P(cs.backgroundColor);base=c&&c[3]?c.slice(0,3):[255,255,255];}
  for(let i=layers.length-1;i>=0;i--){const c=layers[i];base=[0,1,2].map(k=>c[k]*c[3]+base[k]*(1-c[3]));}return base;};
 const out=[];const seen=new Set();
 document.querySelectorAll("body *").forEach(el=>{if(["SCRIPT","STYLE","svg","path","IMG","OPTION"].includes(el.tagName))return;
  const isIn=["INPUT","TEXTAREA","SELECT"].includes(el.tagName);let txt="";
  if(isIn){if(["checkbox","radio","file","hidden","range","color"].includes(el.type))return;txt=el.value||"";}else{for(const n of el.childNodes)if(n.nodeType===3&&n.textContent.trim())txt+=n.textContent.trim()+" ";}
  if(!txt.trim())return;const r=el.getBoundingClientRect();if(r.width<2||r.height<2)return;const cs=getComputedStyle(el);if(cs.visibility==="hidden"||+cs.opacity===0)return;
  if(el.closest("[hidden]"))return;const fg=P(cs.color);if(!fg)return;const bg=bgOf(el);if(!bg)return;
  const f=fg[3]<1?[0,1,2].map(k=>fg[k]*fg[3]+bg[k]*(1-fg[3])):fg;const a=L(f),b=L(bg),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
  if(ratio<3){const sig=el.tagName+"."+[...el.classList].join(".")+"|"+(el.parentElement?[...el.parentElement.classList].join("."):"")+"|"+cs.color+"|"+bg.map(Math.round);if(seen.has(sig))return;seen.add(sig);out.push(ratio.toFixed(2)+" "+sig+" «"+txt.trim().slice(0,40)+"»");}});
 return out;};
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:WIDTH,height:900},colorScheme:'dark'});const res={};const errs=[];
 const add=(k,L)=>{L.forEach(x=>{(res[x]=res[x]||new Set()).add(k);});};
 const run=async(pg,k)=>{await pg.waitForTimeout(250);await pg.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true)).catch(()=>{});add(k,await pg.evaluate(AUDIT));};
 // negocio
 const r=await ctx.newPage();r.on('pageerror',e=>errs.push(e.message));await r.goto(BASE+'negocio.html');await r.waitForTimeout(800);await run(r,'neg:inicio');
 await r.evaluate(()=>{S=exampleState();drawTypes();});await run(r,'neg:tipos');await r.click('#goProv');await r.waitForTimeout(300);
 const n=await r.evaluate(()=>stepList().length);
 for(let i=0;i<n;i++){await r.evaluate(i=>{step=i;showMiss=true;render();},i);await run(r,'neg:paso'+i);}
 const svc=await r.evaluate(()=>stepList().findIndex(s=>s.id==="svc"));
 for(const o of ["f0","f1","f2","rt"]){await r.evaluate(([i,o])=>{step=i;S.services[0].open=o;render();},[svc,o]);await run(r,'neg:svc-'+o);}
 for(const t of ["svc","venue","planner"]){await r.evaluate(t=>{const b=document.querySelector('#site [data-vt="'+t+'"]');b&&b.click();},t);await run(r,'neg:sitio-'+t);}
 // fiestas
 const c=await ctx.newPage();c.on('pageerror',e=>errs.push(e.message));await c.goto(BASE+'fiestas.html');await c.waitForTimeout(800);
 await c.evaluate(()=>{S.name="Mariana";S.nameOk=true;S.kind="social";S.occ="Boda";S.guests=120;S.date=new Date(Date.now()+75*864e5).toISOString().slice(0,10);S.start="17:00";S.end="23:00";if(typeof applySuggestions==="function")applySuggestions();}).catch(e=>errs.push(String(e)));
 for(const s of ["intro","fiesta","lugar","servicios","extra","presupuesto","detalles","result","signup","sent"]){await c.evaluate(s=>{try{go(s);}catch(e){}},s);await run(c,'cot:'+s);}
 // shell
 const h=await ctx.newPage();h.on('pageerror',e=>errs.push(e.message));await h.goto(BASE+'index.html');await h.waitForTimeout(900);await h.evaluate(()=>{try{betaShown=true;}catch(e){}});await run(h,'home:hs');
 await h.evaluate(()=>goSide('pv',true));await run(h,'home:pv');
 for(const [fn,tabs] of [["demoUser",["fiestas","bandeja","perfil"]],["demoProv",["negocio","bandeja","perfil"]]]){await h.evaluate(fn=>{try{window[fn]();}catch(e){console.log(e)}},fn);await h.waitForTimeout(400);
  for(const t of tabs){await h.evaluate(t=>{try{U.tab=t;drawAcct();}catch(e){}},t);await run(h,'cuenta:'+fn+':'+t);}}
 const L=Object.entries(res).map(([k,v])=>k+"   @ "+[...v].slice(0,4).join(",")+(v.size>4?` +${v.size-4}`:""));console.log(L.length+" problemas\n"+L.join("\n"));console.log('ERRS',JSON.stringify(errs.slice(0,5)));await b.close();})();
