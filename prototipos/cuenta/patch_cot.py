s=open('cot2_src.html').read()
def R(a,b,n=1):
    global s
    c=s.count(a);assert c==n,(a[:80],c);s=s.replace(a,b)
R('<script>\n','<script src="catalogo.js"></script>\n<script>\nconst QS=new URLSearchParams(location.search),ACCT=QS.get("cuenta")==="1",ACCT_NAME=QS.get("nombre")||"",ACCT_WA=QS.get("wa")||"";\n',1)
import re
# catálogos compartidos
a=s.index('const VENUE_TYPES=[');b=s.index('const FACT_DOCS=[')
s=s[:a]+'''const VENUE_TYPES=HQV.VENUE_TYPES.concat([["Me da igual","🤷"]]);
const FEATURES=HQV.VENUE_FEATS;
const NEED_FEATS=HQV.VENUE_FEATS.filter(f=>HQV.NEED_KEYS.includes(f[0])).concat([["nada","👌","Nada en especial"]]);
const VENUE_CATS=HQV.POLICY_CATS.map(c=>c[0]); // servicios que un venue puede poner
'''+s[b:]
R('need:{state:"Ciudad de México",all:false,munis:[],types:[],feats:[]},','need:{state:"Ciudad de México",all:false,munis:[],types:[],feats:[],format:""},')
# validación
R('if(!n.types.length)m.push("Tipo de venue");','if(!n.types.length)m.push("Tipo de venue");if(!n.format)m.push("¿Sentados o de pie?");')
R('if(S.hasPlace===false&&!md.who)m.push(`${c}: ¿lo incluye el venue o lo llevas tú?`);','if(S.hasPlace===false&&VENUE_CATS.includes(c)&&!md.who)m.push(`${c}: ¿lo pone el venue o lo llevas tú?`);')
# motor: fila del venue con venues reales de la red
R(' if(S.hasPlace===false)out.push({k:"Venue",e:"🏛️",label:"Venue (renta del espacio)",avg:venueBase(g)});',
''' if(S.hasPlace===false){const vm=venueMatch(g),inc=fromVenueCats();out.push({k:"Venue",e:"🏛️",label:"Venue"+(inc.length?" con "+inc.join(", ").toLowerCase():" (renta del espacio)"),subs:vm.ok.length?[`Promedio de ${vm.ok.length} ${vm.ok.length===1?"venue que cumple":"venues que cumplen"} lo que pides`]:["Promedio general (aún no hay venues que cumplan todo)"],avg:vm.avg});}''')
R("Object.keys(S.sel).forEach(c=>{if(!S.sel[c].length)return;const inVenue=S.hasPlace===false&&(S.meta[c]||{}).who===\"venue\";",
  "Object.keys(S.sel).forEach(c=>{if(!S.sel[c].length)return;const inVenue=S.hasPlace===false&&(S.meta[c]||{}).who===\"venue\"&&VENUE_CATS.includes(c);if(inVenue)return;")
R('function planCost(g){','''const fromVenueCats=()=>S.hasPlace===false?Object.keys(S.sel).filter(c=>S.sel[c].length&&VENUE_CATS.includes(c)&&(S.meta[c]||{}).who==="venue"):[];
const ownVenueCats=()=>Object.keys(S.sel).filter(c=>S.sel[c].length&&VENUE_CATS.includes(c)&&(S.meta[c]||{}).who==="yo");
/* Empareja la solicitud con los venues de la red (mismo catálogo que llenan los proveedores) */
function venueMatch(g=S.guests){const n=S.need;const req={guests:g,date:S.date,start:S.start,end:S.end,format:n.format||"sentados",types:n.types,feats:n.feats,munis:n.munis,allZone:n.all,fromVenue:fromVenueCats(),own:ownVenueCats()};
 if(n.state!=="Ciudad de México"){req.munis=["__fuera__"];req.allZone=false;} // por ahora la red de ejemplo solo tiene venues en CDMX
 const list=HQV.SAMPLE_VENUES.map(v=>({v,q:HQV.venueQuote(v,req)}));const ok=list.filter(x=>x.q.ok);
 const fallback=venueBase(g)+req.fromVenue.reduce((a,c)=>a+catAvg(c,g),0);
 return{list,ok,avg:ok.length?ok.reduce((a,x)=>a+x.q.total,0)/ok.length:fallback};}
function planCost(g){''')
# UI lugar: formato y contador en vivo
R('''   <div class="field"><span class="lbl">✅ ¿Qué debe tener?</span>''','''   <div class="field"><span class="lbl">👥 ¿Cómo estarán tus invitados?</span><div class="seg${MISS(!!n.format)}" id="nfmt">${[["sentados","🪑 Sentados"],["pie","🕺 De pie"],["mixto","🔀 Mixto"]].map(([v,t])=>`<button type="button" data-v="${v}" aria-pressed="${n.format===v}">${t}</button>`).join("")}</div><span class="hint">Así sabemos qué venues tienen cupo para ${S.guests.toLocaleString("es-MX")} invitados.</span></div>
   <div class="field"><span class="lbl">✅ ¿Qué debe tener?</span>''')
R('''   <div class="tip info"><span class="emo">💡</span><span>En el siguiente paso eliges qué servicios quieres que incluya el venue y cuáles llevas tú.</span></div>`:''}''',
  '''   <div id="vlive"></div>
   <div class="tip info"><span class="emo">💡</span><span>En el siguiente paso eliges qué servicios quieres que ponga el venue y cuáles llevas tú.</span></div>`:''}''')
R('''   el.querySelectorAll(".nf").forEach(b=>b.onclick=''','''   el.querySelectorAll("#nfmt button").forEach(b=>b.onclick=()=>{n.format=b.dataset.v;el.querySelectorAll("#nfmt button").forEach(x=>x.setAttribute("aria-pressed",x===b));refresh("lugar");});
   el.querySelectorAll(".nf").forEach(b=>b.onclick=''')
# servicios: quién lo pone
R('''   ${venue?`<span class="mini-l">¿Quién lo pone?</span><div class="seg${MISS(!!md.who)}" data-c="${esc(c.n)}" data-f="who"><button type="button" data-v="venue" aria-pressed="${md.who==="venue"}">🏛️ Que lo incluya el venue</button><button type="button" data-v="yo" aria-pressed="${md.who==="yo"}">🙋 Lo llevo yo</button></div>`:''}''',
  '''   ${venue&&VENUE_CATS.includes(c.n)?`<span class="mini-l">¿Quién lo pone?</span><div class="seg${MISS(!!md.who)}" data-c="${esc(c.n)}" data-f="who"><button type="button" data-v="venue" aria-pressed="${md.who==="venue"}">🏛️ Que lo ponga el venue</button><button type="button" data-v="yo" aria-pressed="${md.who==="yo"}">🙋 Lo llevo yo</button></div><span class="hint">${md.who==="yo"?"Solo te mostraremos venues que dejen entrar a tu proveedor.":md.who==="venue"?"Buscaremos venues que lo incluyan o lo vendan.":"¿No sabes? Elige \\"que lo ponga el venue\\": muchos ya lo incluyen."}</span>`:''}''')
R('''md[f]=f==="inv"?b.dataset.v==="1":b.dataset.v;g.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",x===b));g.classList.remove("miss");refresh("servicios");}));''',
  '''md[f]=f==="inv"?b.dataset.v==="1":b.dataset.v;if(f==="who"){const y=scrollY;render();scrollTo({top:y});return;}g.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",x===b));g.classList.remove("miss");refresh("servicios");}));''')
# contador en vivo: se actualiza con refresh
R('function refresh(st){','function refresh(st){drawVenueLive();')
R('function go(s){','''function drawVenueLive(){const box=$("vlive");if(!box||S.hasPlace!==false)return;const vm=venueMatch();const tot=vm.list.length,k=vm.ok.length;
 const why={};vm.list.filter(x=>!x.q.ok).forEach(x=>x.q.reasons.forEach(r=>{const t=HQV.reasonText(r);why[t]=(why[t]||0)+1;}));
 box.innerHTML=`<div class="vlive ${k?'':'none'}"><b>🏛️ ${k} de ${tot} venues de la red cumplen lo que pides <span class="ex">Ejemplo</span></b>${Object.keys(why).length?`<span class="hint">Descartados: ${Object.entries(why).sort((a,b)=>b[1]-a[1]).map(([t,c])=>`${esc(t)} (${c})`).join(" · ")}</span>`:''}</div>`;}
function go(s){''')
R('bindNav("lugar","fiesta","servicios");return;}','drawVenueLive();bindNav("lugar","fiesta","servicios");return;}')
# resultado: tarjeta de venues + condiciones
R('''  <div class="card"><h3 style="font-size:19px">Así se reparte 👇</h3>''','''  ${S.hasPlace===false?venueResultHtml():''}
  <div class="card"><h3 style="font-size:19px">Así se reparte 👇</h3>''')
R('function drawBudgetAmounts(){','''const rng=(a,f)=>{const lo=Math.min(...a),hi=Math.max(...a);return lo===hi?f(lo):`${f(lo)} a ${f(hi)}`;};
function venueResultHtml(){const vm=venueMatch(),ef=earlyFactor(),f=S.factor.Venue??1;const ok=vm.ok.sort((a,b)=>a.q.total-b.q.total);
 const conds=ok.map(x=>x.q.cond);const deps=[...new Set(conds.map(c=>c.deposit).filter(Boolean))].sort();const advs=conds.map(c=>+c.advance).filter(x=>x>0);const guar=conds.map(c=>+c.guarantee).filter(x=>x>0);const docs=[...new Set(conds.flatMap(c=>c.docs))];
 return`<div class="card"><h3 style="font-size:19px">🏛️ Venues para tu fiesta <span class="ex">Ejemplo</span></h3>
  ${ok.length?`<span class="hint">${ok.length} de ${vm.list.length} venues de la red cumplen lo que pides. Así queda cada uno con tus horas, tu día y tus servicios:</span>
  <div class="vres">${ok.map(x=>`<div><span><b>${esc(x.v.type)} en ${esc(x.v.addr.muni)}</b><br><span class="sub">${esc(x.q.option)}${x.q.extraH?` · ${x.q.extraH} h extra`:''}${x.q.negotiable?' · 🤝 negociable':''}</span></span><span>${money(x.q.total*ef*f/S.guests)} c/u<br><span class="sub">${money(x.q.total*ef*f)}</span></span></div>`).join("")}</div>
  <div class="tip info"><span class="emo">📋</span><span><b>Lo que te pedirán:</b> anticipo de ${deps.join(" a ")||"—"}${advs.length?` · reservar con ${rng(advs,x=>x)} días de anticipación`:''}${guar.length?` · depósito en garantía de ${rng(guar,money)}`:''}${docs.length?` · documentos: ${esc(docs.join(", "))}`:''}.</span></div>`
  :`<div class="tip warn"><span class="emo">🔎</span><span>Todavía no hay venues en la red que cumplan todo lo que pides. Usamos el promedio general; prueba con más zonas, otro tipo de lugar o que algún servicio lo ponga el venue.</span></div>`}
  </div>`;}
function drawBudgetAmounts(){''')
# cuenta: sin registro extra
R('$("send").onclick=()=>go("signup");','$("send").onclick=()=>{if(ACCT){S.name=S.name||ACCT_NAME||"tú";S.wa=ACCT_WA;go("sent");try{parent.postMessage({hqv:"fiesta-enviada",occ:S.occ},"*");}catch(_){}}else go("signup");};')
# CSS
R('</style>','''html,body{overflow-x:clip}
.vlive{border:2px dashed var(--grape);border-radius:14px;padding:10px 12px;display:grid;gap:4px;background:var(--grape-soft);font-size:14px}
.vlive.none{border-color:var(--orange);background:var(--sun-soft)}
.vres{display:grid;gap:6px}.vres>div{display:flex;justify-content:space-between;gap:10px;border:1.5px solid var(--line);border-radius:12px;padding:8px 10px;font-size:13.5px}
.vres>div>span:last-child{text-align:right;white-space:nowrap;font-weight:700}.vres .sub{font-weight:500;color:var(--muted);font-size:12px}
</style>''',1)
open('v4/cot_src.html','w').write(s);print('ok')
