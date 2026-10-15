const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const O=process.argv[2]+'/shotsR/';
(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,h,tag,cs,touch] of [[390,844,'m','light',true],[1280,900,'d','dark',false]]){const ctx=await b.newContext({viewport:{width:w,height:h},colorScheme:cs,hasTouch:touch,isMobile:touch});const p=await ctx.newPage();p.on('pageerror',e=>errs.push(tag+' '+e.message));p.on('console',m=>{if(m.type()==='error')errs.push(tag+' console '+m.text());});
await p.goto('http://localhost:8766/index.html');await p.waitForTimeout(900);
await p.screenshot({path:O+tag+'_inicio.jpg',type:'jpeg',quality:75});
const S=()=>p.evaluate(()=>[...document.querySelectorAll('.it.on')].map(x=>x.dataset.v).join(' | '));
console.log(tag,'inicial',await S());
// mover rodillo 2 (servicio) a otro: desplazar
await p.evaluate(()=>{const el=document.getElementById('reel1');el.scrollBy({left:260});});await p.waitForTimeout(1400);
console.log(tag,'tras mover servicio',await S(), await p.evaluate(()=>document.getElementById('path').innerText.replace(/\n/g,' ')));
// buscador
await p.fill('#q','sillas tiffany');await p.waitForTimeout(200);console.log(tag,'resultados',await p.evaluate(()=>[...document.querySelectorAll('#qr button')].slice(0,3).map(b=>b.innerText.replace(/\n/g,' / ')).join(' || ')));
await p.keyboard.press('Enter');await p.waitForTimeout(1800);console.log(tag,'tras buscar',await S());
await p.screenshot({path:O+tag+'_buscado.jpg',type:'jpeg',quality:75});
// guardar
await p.click('#save');await p.waitForTimeout(600);
console.log(tag,'nombre sugerido',await p.inputValue('#iName'));
await p.fill('#iPax','120');await p.dispatchEvent('#iPax','change');await p.waitForTimeout(150);
await p.fill('[data-tp="full"]','45');await p.waitForTimeout(100);
console.log(tag,'host',await p.evaluate(()=>document.querySelector('[data-th="full"]').innerText));
await p.fill('.tags[data-t="ins"] input','mant');await p.waitForTimeout(150);await p.keyboard.press('Enter');await p.waitForTimeout(150);
console.log(tag,'insumos',await p.evaluate(()=>[...document.querySelectorAll('.tags[data-t="ins"] .tag')].map(x=>x.firstChild.textContent).join(',')));
const id=await p.$('#ident');await id.screenshot({path:O+tag+'_identidad.jpg',type:'jpeg',quality:75});
// cambiar unidad a por pieza y cantidad
await p.selectOption('[data-tu="full"]','Por pieza');await p.waitForTimeout(150);await p.fill('[data-tq="full"]','120');await p.waitForTimeout(100);
console.log(tag,'host pieza',await p.evaluate(()=>document.querySelector('[data-th="full"]').innerText));
await p.click('#iSave');await p.waitForTimeout(700);console.log(tag,'productos',await p.evaluate(()=>document.getElementById('prodH').textContent));
// paquete
await p.click('#mkPkg');await p.waitForTimeout(300);const picks=await p.$$('.pc .pick');await picks[0].click();await p.waitForTimeout(100);await (await p.$$('.pc .pick'))[1].click();await p.waitForTimeout(100);
await p.screenshot({path:O+tag+'_elegir.jpg',type:'jpeg',quality:75});
await p.click('#pkGo');await p.waitForTimeout(600);
console.log(tag,'paquete en blanco',await p.inputValue('#iName')==='', await p.evaluate(()=>document.querySelector('.sug')?.innerText));
await p.fill('#iName','Paquete Boda Oro');await p.fill('#iPax','100');await p.dispatchEvent('#iPax','change');await p.waitForTimeout(150);await p.click('#useSug');await p.waitForTimeout(150);
console.log(tag,'precio sugerido',await p.inputValue('[data-tp="full"]'));
await (await p.$('#ident')).screenshot({path:O+tag+'_paquete.jpg',type:'jpeg',quality:75});
await p.click('#iSave');await p.waitForTimeout(600);console.log(tag,'paquetes',await p.evaluate(()=>document.getElementById('pkgH').textContent));
await p.screenshot({path:O+tag+'_final.jpg',type:'jpeg',quality:70,fullPage:true});
console.log(tag,'sw',await p.evaluate(()=>document.documentElement.scrollWidth));
await ctx.close();}
console.log('ERRS',JSON.stringify(errs));await b.close();})();
