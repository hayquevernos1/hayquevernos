"""v28 · Cuenta (index): conecta los dos lados del marketplace.
- Etiqueta v28.
- Las tarjetas de proveedores del anfitrión muestran primero el precio por persona y abajo el total.
- Cuando publicas tu negocio, aparece en las fiestas que le corresponden con tu precio real
  (invitados, horario de la fiesta con turno/horas extra/recargo del staff, tu venue y tu planner)."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()


def rep(a, b, c=1):
    global s
    assert s.count(a) == c, ('NO/MULTI', a[:100], s.count(a))
    s = s.replace(a, b)


rep('PROTOTIPO v27', 'PROTOTIPO v28')
rep('<b>${x.price==null?"Por cotizar":money(x.price)}</b></div>',
    '${x.price==null?"<b>Por cotizar</b>":x.unit?`<span class="pp2"><b>${money(x.price)}</b><small>${esc(x.unit)}</small></span>`:`<span class="pp2"><b>${money(Math.round(x.price/((e&&e.f&&e.f.guests)||1)))}</b><small>por persona · ${money(x.price)} total</small></span>`}</div>${x.mine?`<div class="why mine"><span>⭐ Tu negocio</span>${x.sub?`<span>🧾 ${esc(x.sub)}</span>`:""}</div>`:""}')
rep('rows.forEach(r=>{provs[r.k]=providersFor(r);provs[r.k].forEach((x,i)=>x.neg=(x.nm.length+i)%3===0);});',
    'rows.forEach(r=>{provs[r.k]=providersFor(r);provs[r.k].forEach((x,i)=>x.neg=(x.nm.length+i)%3===0);});rows.forEach(r=>{provs[r.k]=mineFor(r,f).concat(provs[r.k]);});')
rep('function plPool(e){const t=e.planner.tried.map(x=>x.n);return PLANNERS.map(normPl).filter(',
    'function plPool(e){const t=e.planner.tried.map(x=>x.n);return myPlanners(e).concat(PLANNERS.map(normPl)).filter(', 2)
rep('if(d.hqv==="negocio-publicado"){const x=d.datos||{};', 'if(d.hqv==="negocio-publicado"){const x=d.datos||{};setTimeout(()=>U.events.forEach(injectMine),0);')
rep('function drawEvent(p){const e=getEv(),f=e.f;', 'function drawEvent(p){const e=getEv(),f=e.f;injectMine(e);')
JS = r'''
/* ===== v28 · tu negocio publicado aparece en las fiestas que le corresponden, con tu precio real ===== */
const hHr=t=>{const [a,b]=String(t||"0:0").split(":").map(Number);return(a||0)+(b||0)/60;};
/* staff: turno de 5 h u hora, horas extra y recargo después de las 12, con el horario de la fiesta; usa la tarifa más conveniente */
function hProf(r,pol,s,e){if(e<=s)e+=24;const H=e-s,pct=pol&&pol.night?(+pol.nightPct||0)/100:0,nt=h=>h>=24;let best=null;
 (r.tars||[]).filter(t=>+t.p>0&&t.u).forEach(t=>{const p=+t.p;let tot=0;
  if(t.u==="Por hora"){for(let h=s;h<e-1e-9;h++)tot+=nt(h)?p*(1+pct):p;}
  else{const base=t.u==="Por turno (5 h)"?5:H;tot=p;const xh=Math.max(0,H-base);if(xh>0&&+r.xh>0){const xu=r.xu||"por hora";if(xu==="por hora"){for(let h=s+base;h<e-1e-9;h++)tot+=nt(h)?r.xh*(1+pct):+r.xh;}else tot+=(xu==="por turno de 5 h"?Math.ceil(xh/5):1)*r.xh;}}
  if(best===null||tot<best)best=tot;});return Math.round(best||0);}
function hOffer(o,f){const g=+f.guests||0,s=hHr(f.start||"18:00"),e=hHr(f.end||"23:00");
 if(o.tipo==="staff")return{price:hProf(o,o.pol,s,e),unit:`por ${o.nombre.toLowerCase()} · ${f.start||"18:00"} a ${f.end||"23:00"}`,sub:o.nombre};
 if(o.tipo==="venue"){const r=o.rent;let t=r.per==="hora"?r.precio*Math.max(r.horas,+f.hours||5):r.per==="persona"?r.precio*g:r.precio;if(r.per!=="persona"&&r.upTo&&g>r.upTo)t+=(g-r.upTo)*r.extra;return{price:Math.round(t),sub:o.nombre};}
 if(o.tipo==="servicio"){const i=o.ins,mult=o.pax?Math.max(1,Math.ceil(g/o.pax)):1,base=i.u==="Por persona"?i.p*g:o.fixed?i.p*mult:i.p*(i.q||o.pax||g)*mult;
  const staff=o.staff.reduce((a,r)=>a+(r.q*mult)*hProf(r,o.pol,s,e),0),F={};if(o.formas.includes("rent"))F.rent=Math.round(base);if(o.formas.includes("full"))F.full=Math.round(base+staff);
  const price=F.rent!==undefined?F.rent:F.full;return{price,sub:o.nombre+": "+[F.rent!==undefined?`sin staff ${money(F.rent)}`:"",F.full!==undefined?`con staff ${money(F.full)} (con tu horario)`:""].filter(Boolean).join(" · ")};}
 return null;}
function mineFor(row,f){const S2=U.site;if(!S2||!S2.oferta)return[];return S2.oferta.filter(o=>o.cat===row.k).map(o=>{const q=hOffer(o,f);if(!q||!q.price)return null;
 return{nm:S2.negocio||"Tu negocio",km:2.4,rate:5.0,rev:0,resp:5,price:q.price,unit:q.unit||null,sub:q.sub,badges:["fundador","responde_ya"],nuevo:true,fit:1,score:9,emo:row.e||"⭐",mine:true};}).filter(Boolean);}
function injectMine(e){if(!e||!e.provs||!e.f)return;Object.keys(e.provs).forEach(k=>{const l=e.provs[k].filter(x=>!x.mine),em=(l[0]||{}).emo;e.provs[k]=mineFor({k,e:em},e.f).concat(l);});}
/* tu event planner (o el que aceptó tu invitación) entra a la lista de planners de las fiestas */
function myPlanners(e){const S2=U.site;if(!S2||!S2.oferta)return[];const tot=(e&&e.f&&e.f.total)||0;
 return S2.oferta.filter(o=>o.tipo==="planner").map(o=>{let fee=null;(o.fees||[]).forEach(x=>{const a=+x.amount||0,t=x.unit==="porcentaje"?Math.max(a/100*tot,+x.min||0):x.unit==="invitado"?a*((e&&e.f&&e.f.guests)||0):x.unit==="hora"?a*5:a;if(t>0&&(fee===null||t<fee))fee=t;});
  return{n:o.nombre,img:null,emo:"🧭",z:"",y:0,r:5.0,neg:false,fee:Math.round(fee||0),sp:(o.yo?"Tu perfil · ":"Planner de ")+(S2.negocio||"tu negocio"),b:o.bio||"",mine:true};});}
'''
i = s.rindex('</script>')
s = s[:i] + JS + s[i:]
CSS = '.pp2{display:grid;justify-items:end;text-align:right;line-height:1.15}.pp2 small{font-size:11.5px;color:var(--muted);font-weight:700}.why.mine span{background:rgba(190,255,0,.35)}\n'
i = s.index('</style>')
s = s[:i] + CSS + s[i:]
P.write_text(s)
print('shell28 ok')
