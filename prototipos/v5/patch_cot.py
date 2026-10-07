"""v6 · Cotizador conectado al catálogo maestro: 64 tipos de evento, 469 subcategorías filtradas por evento,
buscador, sugerencias y precios con el motor de conversión (conversiones.js). Lee cot5.html → escribe cot6.html."""
from pathlib import Path
D = Path('/home/claude/hqv/v5')


def rep(s, a, b, count=1):
    assert a in s, 'NO ENCONTRADO: ' + a[:100]
    return s.replace(a, b, count)


c = (D / 'cot5.html').read_text()
c = rep(c, '<script src="catalogo.js"></script>', '<script src="catalogo.js"></script>\n<script src="catalogo_servicios.js"></script>\n<script src="conversiones.js"></script>')

CSS = '''
/* v6 · servicios del catálogo maestro */
.qwrap{position:relative}
.qres{display:grid;gap:2px;margin-top:6px;background:var(--card);border-radius:16px;padding:6px;box-shadow:var(--hqv-clay-sm,0 6px 18px rgba(0,0,0,.08))}
.qres button{border:0;background:none;text-align:left;padding:8px 10px;border-radius:12px;font-size:13.5px;display:flex;gap:8px;align-items:center}
.qres button:hover,.qres button:focus{background:var(--grape-soft)}
.qres small{color:var(--muted)}
.cgrid{display:grid;gap:8px}
.cbox{background:var(--card);border-radius:16px;box-shadow:var(--hqv-clay-sm,0 4px 12px rgba(0,0,0,.06))}
.cbox summary{list-style:none;cursor:pointer;display:flex;gap:10px;align-items:center;padding:10px 14px;font-size:14.5px}
.cbox summary::-webkit-details-marker{display:none}
.cbox summary .emo{font-size:20px}
.cbox summary small{margin-left:auto;color:var(--muted);font-weight:600}
.cbox summary small.on{color:var(--grape)}
.cbox[open] summary{border-bottom:1px solid var(--line)}
.cbox .inner{padding:10px 14px 14px;display:grid;gap:8px}
.cbox .chip.hide{display:none}
.sline{display:flex;justify-content:space-between;gap:8px;font-size:13.5px;padding:4px 0;border-bottom:1px dashed var(--line)}
.sline:last-child{border-bottom:0}
.sline span:last-child{white-space:nowrap;font-weight:700;color:var(--grape)}
.sline .pc{color:var(--muted);font-weight:600}
.evq{max-width:340px}
.tile.hide{display:none}
.bud.pend{opacity:.9}
'''
i = c.index('</style>')
c = c[:i] + CSS + c[i:]

# ---------- catálogo, tipos de evento y sugerencias desde la lista maestra
a = c.index('const CATS=[')
b = c.index('const catOf=n=>CATS.find(c=>c.n===n);')
c = c[:a] + '''/* Catálogo maestro de Diego (catalogo_servicios.js) + motor de conversión (conversiones.js) */
const SVC=window.HQV_SVC,CONV=window.HQV_CONV,REF=CONV.ref;
const CATS=SVC.cats.map(c=>({n:c.n,e:c.e,s:c.s.map(([n,t,u])=>[n,t,u])}));
const FLAT={};CATS.forEach(c=>c.s.forEach(x=>{FLAT[c.n+"|"+x[0]]=Object.keys(FLAT).length;}));
''' + c[b:]
c = rep(c, '''const subOf=(c,s)=>catOf(c).s.find(x=>x[0]===s);''', '''const subOf=(c,s)=>{const k=catOf(c);return k&&k.s.find(x=>x[0]===s);};
const KEY=()=>S.kind==="empresa"?"E":"S";
function excluded(){const l=(SVC.ev[KEY()]||[]).find(x=>x[0]===S.occ);return new Set(l?l[2]:[]);}
const subVisible=(c,s,ex=excluded())=>{const x=subOf(c,s);return !!x&&x[1].includes(KEY())&&!ex.has(FLAT[c+"|"+s]);};
const visibleSubs=(c,ex=excluded())=>catOf(c).s.filter(x=>subVisible(c,x[0],ex)).map(x=>x[0]);
/* Qué «servicio de venue» es cada subcategoría (para saber si el venue lo incluye o deja meterlo) */
const POSTRES=new Set(["Cupcakes y repostería individual","Fuentes de chocolate","Galletas decoradas","Helados y paletas","Macarons y chocolates personalizados","Mesas de dulces","Mesas de postres","Pasteles de celebración","Pasteles escenográficos","Panadería para eventos"]);
const SIN_ALC=new Set(["Agua embotellada","Aguas frescas y bebidas preparadas","Barra de café y baristas","Barra de jugos y smoothies","Barra de té e infusiones","Coctelería sin alcohol","Refrescos y mezcladores","Hielo de consumo","Hielo seco para conservación","Dispensadores de bebidas en renta"]);
function policyOf(c,s){if(c==="Alimentos")return POSTRES.has(s)?"Postres":"Comida";if(c==="Bebidas y barra")return SIN_ALC.has(s)?"Sin alcohol":"Con alcohol";
 return{"Música y espectáculos":"Música","Audio, video e iluminación":"Luz y show","Mobiliario y equipo de banquete":"Mobiliario","Decoración y flores":"Decoración","Personal":"Staff"}[c]||null;}
const catPolicies=c=>[...new Set((S.sel[c]||[]).map(s=>policyOf(c,s)).filter(Boolean))];
const hasPolicy=c=>catPolicies(c).length>0;''')

a = c.index('const OCC={')
b = c.index('const PLACE_TYPES=')
c = c[:a] + '''const OCC={social:SVC.ev.S.map(x=>[x[0],x[1]]),empresa:SVC.ev.E.map(x=>[x[0],x[1]])};
''' + c[b:]

c = rep(c, '''const fromVenueCats=()=>S.hasPlace===false?Object.keys(S.sel).filter(c=>S.sel[c].length&&VENUE_CATS.includes(c)&&(S.meta[c]||{}).who==="venue"):[];
const ownVenueCats=()=>Object.keys(S.sel).filter(c=>S.sel[c].length&&VENUE_CATS.includes(c)&&(S.meta[c]||{}).who==="yo");''',
            '''const venueCats=()=>S.hasPlace===false?Object.keys(S.sel).filter(c=>S.sel[c].length&&hasPolicy(c)&&(S.meta[c]||{}).who==="venue"):[];
const fromVenueCats=()=>[...new Set(venueCats().flatMap(catPolicies))];
const ownVenueCats=()=>[...new Set(Object.keys(S.sel).filter(c=>S.sel[c].length&&hasPolicy(c)&&(S.meta[c]||{}).who==="yo").flatMap(catPolicies))];''')
c = rep(c, '''const fallback=venueBase(g)+req.fromVenue.reduce((a,c)=>a+catAvg(c,g),0);''', '''const fallback=venueBase(g)+venueCats().reduce((a,c)=>a+catAvg(c,g),0);''')

# nombres de ejemplo por categoría nueva
a = c.index('const NAMES={')
b = c.index('\n', a)
c = c[:a] + '''const NAMES={"Venue":["Terraza San Ángel","Jardín Las Flores"],"Alimentos":["Sabores de Coyoacán","Taquizas Don Beto"],"Bebidas y barra":["Barra La Catrina","Aguas La Güera"],"Música y espectáculos":["DJ Rafa Beats","Mariachi Los Reyes"],"Audio, video e iluminación":["Luz y Pista MX","Sonido Pro CDMX"],"Decoración y flores":["Globos Mágicos MX","Flores de Abril"],"Mobiliario y equipo de banquete":["Mobiliario Fiesta Total","Renta Lounge"],"Personal":["Meseros Pro","Staff Elegante"],"Experiencias y actividades":["Show Payasín","Inflables Brinco"],"Fotografía y contenido":["Foto Momentos","Video Vibras"],"Imagen personal y ceremonias":["Glam Studio","Peinados Luna"],"Diseño, impresión y regalos":["Recuerdos Bonitos","Invitaciones Pop"],"Estructuras e infraestructura":["Carpas del Valle","Estructuras MX"],"Tecnología y registro":["Registro Ágil","Stream Pro"]};''' + c[b:]

# ---------- motor de cálculo: precio de referencia + conversión validada
c = rep(c, '''function lineCost(cat,sub,g){const x=subOf(cat,sub);if(!x)return 0;const [,p,u,ratio]=x;const h=Math.max(2,hours());
 if(u==="persona")return p*g;if(u==="hora")return p*h;if(u==="evento")return p;if(u==="mesa")return p*Math.ceil(g/10);if(u==="grupo20")return p*Math.ceil(g/20);
 if(u==="staff"){let r=ratio;if(sub==="Meseros"&&(S.sel["Comida"]||[]).includes("Menú a tiempos"))r=10;return p*Math.max(1,Math.ceil(g/r));}return 0;}''',
            '''function lineCalc(cat,sub,g){const r=REF[cat+"|"+sub];if(!r)return{total:0,pend:true};return hqvCost({cat,sub,u:r[0],price:r[1],pkgP:r[2],guests:g,hours:hours()});}
const lineCost=(cat,sub,g)=>lineCalc(cat,sub,g).total||0;
const linePend=(cat,sub)=>!!lineCalc(cat,sub,S.guests).pend;''')
c = rep(c, '''Object.keys(S.sel).forEach(c=>{if(!S.sel[c].length)return;const inVenue=S.hasPlace===false&&(S.meta[c]||{}).who==="venue"&&VENUE_CATS.includes(c);if(inVenue)return;out.push({k:c,e:catOf(c).e,label:c+(inVenue?" (en el venue)":""),subs:S.sel[c],avg:catAvg(c,g)});});''',
            '''Object.keys(S.sel).forEach(c=>{if(!S.sel[c].length)return;const inVenue=S.hasPlace===false&&(S.meta[c]||{}).who==="venue"&&hasPolicy(c);if(inVenue)return;const pend=S.sel[c].filter(s=>linePend(c,s));out.push({k:c,e:catOf(c).e,label:c,subs:S.sel[c],pend,avg:catAvg(c,g),pendOnly:pend.length===S.sel[c].length});});''')
c = rep(c, '''out.forEach(r=>{r.mkt=r.avg;r.avg=r.avg*ef;r.set=S.factor[r.k]!==undefined;''', '''out.forEach(r=>{r.mkt=r.avg;r.avg=r.avg*ef;r.set=S.factor[r.k]!==undefined||!!r.pendOnly;''')
c = rep(c, 'r.f=r.set?S.factor[r.k]:1', 'r.f=r.set?(S.factor[r.k]??1):1')

# ---------- validación
c = rep(c, '''cs.forEach(c=>{const md=S.meta[c]||{};if(!S.sel[c].length)m.push(`${c}: qué necesitas`);if(S.hasPlace===false&&VENUE_CATS.includes(c)&&!md.who)m.push(`${c}: ¿lo pone el venue o lo llevas tú?`);''',
            '''cs.forEach(c=>{const md=S.meta[c]||{};if(!S.sel[c].length)m.push(`${c}: qué necesitas`);if(S.hasPlace===false&&hasPolicy(c)&&!md.who)m.push(`${c}: ¿lo pone el venue o lo llevas tú?`);''')

# ---------- paso «fiesta»: tipos de evento del catálogo maestro (con buscador)
c = rep(c, '''${S.kind?`<div class="field"><span class="lbl">¿Qué celebras?</span><div class="tiles${MISS(!!S.occ)}">''',
        '''${S.kind?`<div class="field"><span class="lbl">${S.kind==="empresa"?"¿Qué tipo de evento es?":"¿Qué celebras?"}</span><input type="search" class="evq" id="evq" placeholder="🔎 Busca: boda, congreso, posada…" aria-label="Buscar tipo de evento"><div class="tiles${MISS(!!S.occ)}" id="evTiles">''')
c = rep(c, '''el.querySelectorAll(".occ").forEach(b=>b.onclick=()=>{S.occ=b.dataset.o;''', '''const evq=$("evq");if(evq)evq.oninput=()=>{const v=evq.value.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").trim();el.querySelectorAll(".occ").forEach(b=>b.classList.toggle("hide",!!v&&!b.dataset.o.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").includes(v)&&b.dataset.o!=="Otro"));};
  el.querySelectorAll(".occ").forEach(b=>b.onclick=()=>{S.occ=b.dataset.o;''')

# ---------- paso «servicios» (nuevo)
a = c.index(''' if(screen==="servicios"){''')
b = c.index(''' if(screen==="presupuesto"){''')
NEW = r''' if(screen==="servicios"){const venue=S.hasPlace===false,ex=excluded(),nSel=Object.values(S.sel).reduce((a,l)=>a+l.length,0);
  const norm=x=>String(x).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"");
  const chip=(c,s)=>`<button type="button" class="chip sb" data-c="${esc(c)}" data-s="${esc(s)}" aria-pressed="${(S.sel[c]||[]).includes(s)}">${esc(s)}</button>`;
  const priceTxt=(c,s)=>{const x=lineCalc(c,s,S.guests);return x.pend?'<span class="pc">Por cotizar</span>':`~${money(x.total/S.guests)} c/u · ${money(x.total)}`;};
  el.innerHTML=`<div class="card">${say(`Te dejé marcado lo más común para <b>${esc(S.occ.toLowerCase())}</b> ✨ Busca lo que necesites o explóralo por categoría.`)}
  <div class="field qwrap"><label class="lbl" for="sq">🔎 ¿Qué necesitas?</label><input type="search" id="sq" autocomplete="off" placeholder="Ej. taquiza, DJ, meseros, carpa, fotógrafo…"><div id="sqr" class="qres" hidden></div></div>
  ${nSel?`<div class="field"><span class="lbl">✅ Tu selección <span class="opt">${nSel} ${nSel===1?"servicio":"servicios"} · toca para quitar</span></span><div class="chips">${Object.keys(S.sel).flatMap(c=>S.sel[c].map(s=>chip(c,s))).join("")}</div></div>`:''}
  <div class="field"><span class="lbl">📂 Explora por categoría <span class="opt">Solo lo que aplica a ${esc(S.occ.toLowerCase())}</span></span>
   <div class="cgrid">${CATS.map(c=>{const vs=visibleSubs(c.n,ex);if(!vs.length)return"";const sel=(S.sel[c.n]||[]).length,open=OPENC.has(c.n);
    const extra=(S.sel[c.n]||[]).filter(s=>!vs.includes(s));const list=[...vs,...extra];
    return`<details class="cbox" data-c="${esc(c.n)}"${open?" open":""}><summary><span class="emo">${c.e}</span><b>${esc(c.n)}</b><small class="${sel?"on":""}">${sel?sel+" elegidos":list.length+" opciones"}</small></summary><div class="inner">
     ${c.n==="Espacios y hospedaje"?`<div class="note">🏛️ <span>El lugar de tu fiesta se elige en el paso <b>Lugar</b>. Aquí está hospedaje y espacios extra.</span></div>`:''}
     ${list.length>12?`<input type="search" class="subq" placeholder="🔎 Filtrar ${list.length} opciones…" aria-label="Filtrar ${esc(c.n)}">`:''}
     <div class="chips">${list.map((s,i)=>chip(c.n,s).replace('class="chip sb"',`class="chip sb${i>=12&&!(S.sel[c.n]||[]).includes(s)&&!ALLC.has(c.n)?" hide more":""}"`)).join("")}${list.length>12&&!ALLC.has(c.n)?`<button type="button" class="chip all" data-c="${esc(c.n)}">Ver las ${list.length}</button>`:''}</div></div></details>`;}).join("")}</div></div>
  <div style="display:grid;gap:10px">${CATS.filter(c=>(S.sel[c.n]||[]).length).map(c=>{const md=S.meta[c.n]||(S.meta[c.n]={});return`<div class="svc"><div class="svc-head"><b>${c.e} ${esc(c.n)}</b><button type="button" class="btn ghost sm rmc" data-c="${esc(c.n)}">Quitar</button></div>
   <div>${S.sel[c.n].map(s=>`<div class="sline"><span>${esc(s)}</span><span>${priceTxt(c.n,s)}</span></div>`).join("")}</div>
   ${venue&&hasPolicy(c.n)?`<span class="mini-l">¿Quién lo pone?</span><div class="seg${MISS(!!md.who)}" data-c="${esc(c.n)}" data-f="who"><button type="button" data-v="venue" aria-pressed="${md.who==="venue"}">🏛️ Que lo ponga el venue</button><button type="button" data-v="yo" aria-pressed="${md.who==="yo"}">🙋 Lo llevo yo</button></div><span class="hint">${md.who==="yo"?"Solo te mostraremos venues que dejen entrar a tu proveedor.":md.who==="venue"?"Buscaremos venues que lo incluyan o lo vendan.":"¿No sabes? Elige \"que lo ponga el venue\": muchos ya lo incluyen."}</span>`:''}
   <span class="mini-l">¿Necesitas factura de este proveedor?</span><div class="seg${MISS(md.inv!==undefined)}" data-c="${esc(c.n)}" data-f="inv"><button type="button" data-v="1" aria-pressed="${md.inv===true}">🧾 Sí</button><button type="button" data-v="0" aria-pressed="${md.inv===false}">No</button></div>
   <input type="text" class="cm" data-c="${esc(c.n)}" value="${esc(md.note||"")}" placeholder="💬 Cuéntale algo al proveedor (opcional): sin gluten, tema vaquero, música de los 80…" aria-label="Comentario para ${esc(c.n)}">
   </div>`;}).join("")}</div>
  <span class="hint">«Por cotizar» = aún no tenemos precio promedio de ese servicio; los proveedores te lo cotizan directo.</span>
  <div class="field"><label class="lbl" for="more">✏️ ¿Algo más que no veas aquí? <span class="opt">(opcional)</span></label><input type="text" id="more" value="${esc(S.more)}" placeholder="Un violinista, tatuajes de henna, pirotecnia…"><span class="hint">Lo enviamos como pedido especial. No se suma al cálculo.</span></div>
  ${navHtml("servicios")}</div>`;
  const keep=fn=>{const y=scrollY;fn();render();scrollTo({top:y});};
  const toggle=(c,s)=>{const l=S.sel[c]||[];if(l.includes(s)){S.sel[c]=l.filter(x=>x!==s);if(!S.sel[c].length){delete S.sel[c];delete S.meta[c];}}else{S.sel[c]=[...l,s];S.meta[c]=S.meta[c]||{};OPENC.add(c);}};
  el.querySelectorAll(".sb").forEach(b=>b.onclick=()=>keep(()=>toggle(b.dataset.c,b.dataset.s)));
  el.querySelectorAll(".cbox").forEach(d=>d.ontoggle=()=>{if(d.open)OPENC.add(d.dataset.c);else OPENC.delete(d.dataset.c);});
  el.querySelectorAll(".chip.all").forEach(b=>b.onclick=()=>keep(()=>ALLC.add(b.dataset.c)));
  el.querySelectorAll(".subq").forEach(q=>q.oninput=()=>{const v=norm(q.value).trim();q.parentNode.querySelectorAll(".chip.sb").forEach(x=>x.classList.toggle("hide",v?!norm(x.dataset.s).includes(v)&&x.getAttribute("aria-pressed")!=="true":x.classList.contains("more")));const al=q.parentNode.querySelector(".chip.all");if(al)al.hidden=!!v;});
  el.querySelectorAll(".rmc").forEach(b=>b.onclick=()=>keep(()=>{delete S.sel[b.dataset.c];delete S.meta[b.dataset.c];}));
  el.querySelectorAll(".seg[data-c]").forEach(g=>g.querySelectorAll("button").forEach(b=>b.onclick=()=>{const md=S.meta[g.dataset.c];const f=g.dataset.f;md[f]=f==="inv"?b.dataset.v==="1":b.dataset.v;if(f==="who"){keep(()=>{});return;}g.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",x===b));g.classList.remove("miss");refresh("servicios");}));
  el.querySelectorAll(".cm").forEach(i=>i.oninput=()=>{S.meta[i.dataset.c].note=i.value;});
  $("more").oninput=e=>{S.more=e.target.value;};
  const q=$("sq"),qr=$("sqr");
  q.oninput=()=>{const v=norm(q.value).trim();if(v.length<2){qr.hidden=true;return;}const toks=v.split(/\s+/),res=[];
   CATS.forEach(c=>c.s.forEach(([s])=>{if(!subVisible(c.n,s,ex))return;const h=norm(s+" "+c.n);if(toks.every(t=>h.includes(t)))res.push([c,s,norm(s).startsWith(v)?0:norm(s).includes(v)?1:2]);}));
   res.sort((x,y)=>x[2]-y[2]);
   qr.innerHTML=res.slice(0,8).map(([c,s])=>{const on=(S.sel[c.n]||[]).includes(s);return`<button type="button" data-c="${esc(c.n)}" data-s="${esc(s)}"><span>${c.e}</span><span><b>${esc(s)}</b> <small>· ${esc(c.n)}${on?" · ya lo tienes ✓":""}</small></span></button>`;}).join("")||`<span class="hint" style="padding:8px">No lo encontramos. Escríbelo abajo en «¿Algo más?» y lo enviamos como pedido especial.</span>`;
   qr.hidden=false;qr.querySelectorAll("button").forEach(x=>x.onclick=()=>{const c=x.dataset.c,s=x.dataset.s;if(!(S.sel[c]||[]).includes(s))toggle(c,s);hqvTrack("servicio_buscado",{sub:s,lado:"anfitrion"});render();setTimeout(()=>{const n=document.querySelector(`.cbox[data-c="${CSS.escape(c)}"]`);n&&n.scrollIntoView({behavior:"smooth",block:"center"});},0);});};
  q.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();const f=qr.querySelector("button");f&&f.click();}if(e.key==="Escape")qr.hidden=true;};
  bindNav("servicios","lugar","presupuesto");return;}

'''
c = c[:a] + NEW + c[b:]
c = rep(c, '''let screen="intro",showMiss=false,''', '''const OPENC=new Set(),ALLC=new Set();
let screen="intro",showMiss=false,''')

# ---------- presupuesto: los «por cotizar» no llevan barra
c = rep(c, '''<div style="display:grid;gap:10px" id="buds">${rows().map(r=>`<div class="bud">''',
        '''<div style="display:grid;gap:10px" id="buds">${rows().map(r=>r.pendOnly?`<div class="bud pend"><div class="bud-top"><b>${r.e} ${esc(r.label)}</b><span class="amt">Por cotizar</span></div><span class="hint">${r.subs.map(esc).join(" · ")} · aún no tenemos precio promedio; los proveedores te lo cotizan directo.</span></div>`:`<div class="bud">''')
c = rep(c, '''${r.subs?`<span class="hint">${r.subs.map(esc).join(" · ")}</span>`:''}
   <div class="avg"''', '''${r.subs?`<span class="hint">${r.subs.map(esc).join(" · ")}${r.pend&&r.pend.length?` · <b>por cotizar:</b> ${r.pend.map(esc).join(", ")}`:""}</span>`:''}
   <div class="avg"''')

# ---------- resultado y envío a la cuenta
c = rep(c, '''<span>${money(r.amt/S.guests)} c/u<br><span class="sub">${money(r.amt)}</span></span></div>`).join("")}''',
        '''<span>${r.pendOnly?"Por cotizar":`${money(r.amt/S.guests)} c/u<br><span class="sub">${money(r.amt)}${r.pend&&r.pend.length?" + por cotizar":""}</span>`}</span></div>`).join("")}''')
c = rep(c, '''rows:rs.map(r=>({k:r.k,e:r.e,label:r.label,subs:r.subs||[],amt:Math.round(r.amt)})),early:earlyPct()};''',
        '''rows:rs.map(r=>({k:r.k,e:r.e,label:r.label,subs:r.subs||[],amt:Math.round(r.amt),pend:!!r.pendOnly})),early:earlyPct(),
    servicios:Object.keys(S.sel).map(c=>({cat:c,subs:S.sel[c].map(s=>{const x=lineCalc(c,s,S.guests),r=REF[c+"|"+s];return{n:s,unidad:r?r[0]:null,estimado:Math.round(x.total||0),cantidad:x.qty||null};})}))};''')

# ---------- sugerencias por tipo de evento
c = rep(c, '''function applySuggestions(){if(S.suggestedFor===S.occ)return;const sg=SUGG[S.occ]||{};S.sel={};S.meta={};Object.entries(sg).forEach(([c,a])=>{S.sel[c]=[...a];S.meta[c]={};});S.suggestedFor=S.occ;}''',
        '''function applySuggestions(){const id=S.kind+"|"+S.occ;if(S.suggestedFor===id)return;const K=KEY(),sg=(CONV.sug[K]||{})[S.occ]||CONV.sug["def"+K]||[];const ex=excluded();
 S.sel={};S.meta={};OPENC.clear();sg.forEach(k=>{const [c,s]=k.split("|");if(!subVisible(c,s,ex))return;(S.sel[c]=S.sel[c]||[]).push(s);S.meta[c]=S.meta[c]||{};});S.suggestedFor=id;}''')

assert 'VENUE_CATS.includes' not in c, 'queda VENUE_CATS.includes'
(D / 'cot6.html').write_text(c)
print('cot6.html', len(c))

c = (D / 'cot6.html').read_text()
c = rep(c, '<span class="tt">Total aproximado de tu fiesta: <b>${money(t)}</b></span>',
        '<span class="tt">Total aproximado de tu fiesta: <b>${money(t)}</b></span>${rs.some(r=>r.pend&&r.pend.length)?`<small>+ ${rs.reduce((a,r)=>a+(r.pend?r.pend.length:0),0)} por cotizar con los proveedores</small>`:""}')
(D / 'cot6.html').write_text(c)
print('nota por cotizar ok')
