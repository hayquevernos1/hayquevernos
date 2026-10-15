"""v26 · reescribe partes de svc7.js (motor de «Arma tu servicio»). Se corre UNA vez sobre svc7_v25.js → svc7.js."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
L = (V / 'svc7_v25.js').read_text().split('\n')


def decl(prefix, new):
    """Reemplaza la declaración de primer nivel que empieza con `prefix` (hasta la siguiente línea en columna 0)."""
    i = [k for k, l in enumerate(L) if l.startswith(prefix)]
    assert len(i) == 1, ('decl', prefix, i)
    i = i[0]
    j = i + 1
    while j < len(L) and (L[j].startswith(' ') or L[j] == ''):
        j += 1
    L[i:j] = new.strip('\n').split('\n')


decl('const RU_TL=', r'''const RU_TL={rent:["📦 Insumos sin personal","Lo llevas o lo recogen"],full:["🙋 Insumos con personal","Tu equipo va al evento"],labor:["🙋 Personal","Por perfil"]};''')
decl('const RU_XU=', r'''const RU_XU=["por hora","por turno de 5 h","por evento","por día"];''')
decl('const ruShortU=', r'''const ruShortU=t=>t.replace(/^por /,"").replace("turno de 5 h","turno 5 h");''')
decl('const RU_LU=', r'''const RU_LU=[["Por turno (5 h)","por turno de 5 h"],["Por hora","por hora"],["Por evento","por evento"],["Por día","por día"]];''')
decl('const ruXU=', r'''const ruXU=u=>(RU_LU.find(x=>x[0]===u)||["","por hora"])[1];
/* v26 · cada perfil puede cobrarse de varias formas (turno de 5 h, por hora…) y tiene un solo extra */
const ruTarsOk=r=>(r.tars||[]).length>0&&r.tars.every(t=>+t.p>0&&!!t.u);
const ruTarsText=r=>(r.tars||[]).filter(t=>+t.p>0&&t.u).map(t=>`${money(t.p)} ${ruXU(t.u)}`).join(" · ");
const ruHM=h=>{h=((h%24)+24)%24;const H=Math.floor(h),M=Math.round((h-H)*60),ap=H<12?"a.m.":"p.m.",h12=H%12||12;return`${h12}:${String(M).padStart(2,"0")} ${ap}`;};
const ruHr=t=>{const [a,b]=String(t||"0:0").split(":").map(Number);return(a||0)+(b||0)/60;};
/* cómo se cotiza un perfil en una fiesta (s, e en horas; e puede pasar de 24) */
function ruProfQuote(r,pol,s,e){if(e<=s)e+=24;const H=e-s,pct=pol&&pol.night?(+pol.nightPct||0)/100:0,night=h=>h>=24;let best=null;
 (r.tars||[]).filter(t=>+t.p>0&&t.u).forEach(t=>{const p=+t.p,lines=[];let tot=0;
  if(t.u==="Por hora"){let n=0,nn=0;for(let h=s;h<e-1e-9;h++)night(h)?nn++:n++;tot=p*n+p*(1+pct)*nn;lines.push(`${n} h × ${money(p)}`+(nn?` + ${nn} h × ${money(Math.round(p*(1+pct)))} después de las 12 (+${Math.round(pct*100)}%)`:""));}
  else{const base=t.u==="Por turno (5 h)"?5:H;tot=p;lines.push(t.u==="Por turno (5 h)"?`Turno de 5 h (${ruHM(s)} a ${ruHM(s+5)}): ${money(p)}`:`${ruXU(t.u).replace(/^por /,"").replace(/^./,c=>c.toUpperCase())}: ${money(p)}`);
   const xh=Math.max(0,H-base);if(xh>0&&+r.xh>0){const xu=r.xu||"por hora";
    if(xu==="por hora"){let n=0,nn=0;for(let h=s+base;h<e-1e-9;h++)night(h)?nn++:n++;const x=+r.xh;tot+=x*n+x*(1+pct)*nn;lines.push(`${xh} h extra: `+[n?`${n} × ${money(x)}`:"",nn?`${nn} × ${money(Math.round(x*(1+pct)))} después de las 12 (+${Math.round(pct*100)}%)`:""].filter(Boolean).join(" + "));}
    else{const k=xu==="por turno de 5 h"?Math.ceil(xh/5):1;tot+=k*(+r.xh);lines.push(`${xh} h extra: ${k} × ${money(r.xh)} ${xu}`);}}
   else if(xh>0)lines.push(`${xh} h extra: sin precio de extra`);}
  if(!best||tot<best.tot)best={tot:Math.round(tot),lines,t};});return best;}
const ruProfCost=(r,pol)=>{const q=ruProfQuote(r,pol,18,23);return q?q.tot:0;};''')
decl('function ruLabRow(', r'''function ruLabRow(n,q){const s=ruStaffBy(n),r=s&&s.labor[0];return r?{n,q:q||"1",tars:JSON.parse(JSON.stringify(r.tars||[{p:r.p,u:r.u}])),xh:r.xh,xu:r.xu}:{n,q:q||"1",tars:[{p:"",u:""}],xh:"",xu:""};}
const ruSyncPU=r=>{const t=(r.tars||[])[0]||{};r.p=t.p||"";r.u=t.u||"";};''')
decl('function ruNewStaff(', r'''function ruNewStaff(r,cat){const n=r.n,x={n,q:"1",tars:JSON.parse(JSON.stringify(r.tars||[{p:r.p,u:r.u}])),xh:r.xh,xu:r.xu};ruSyncPU(x);return Object.assign(ruBlankMore(),{id:"st-"+slug(n),kind:"staff",n,name:n,dims:[cat,"Personal independiente","Solo talento",n],otro:"",dishes:[],ins:[],crew:[],pax:"",tw:["labor"],tar:ruBlankT("Por hora"),emb:0,labor:[x]});}''')
decl('function ruPropStaff(', r'''function ruPropStaff(sp){const e=sp.labor[0];(S.rprods||[]).forEach(x=>{if(x.kind!=="prod")return;x.labor.forEach(r=>{if(nrm(r.n)===nrm(sp.n)){r.tars=JSON.parse(JSON.stringify(e.tars));r.xh=e.xh;r.xu=e.xu;ruSyncPU(r);}});});}''')
decl('function ruSyncStaff(', r'''function ruSyncStaff(p,done){const cat=p.dims[0],added=[],conf=[],key=r=>JSON.stringify((r.tars||[]).map(t=>[+t.p,t.u]));
 p.labor.forEach(r=>{let sp=ruStaffBy(r.n);if(!sp){sp=ruNewStaff(r,cat);S.rprods.push(sp);added.push(r.n);return;}const e=sp.labor[0];
  if(ruTarsOk(e)&&ruTarsOk(r)&&key(e)!==key(r))conf.push({n:r.n,sp,r});else{if(ruTarsOk(r))e.tars=JSON.parse(JSON.stringify(r.tars));e.xh=r.xh;e.xu=r.xu;ruSyncPU(e);}});
 const fin=()=>{(S.rprods||[]).filter(x=>x.kind==="staff").forEach(ruPropStaff);ruDrawLists();changed();if(added.length)ruToast(`🙋 Sumamos a «Tu personal»: ${added.join(", ")}. También se cotizan solos.`);done&&done();};
 if(!conf.length){fin();return;}
 const md=document.createElement("div");md.className="rmodal";md.innerHTML=`<div class="rsheet ru-confl"><span class="ru-embk">🙋 TU PERSONAL</span><h2>Un perfil, un precio</h2><span>Estos perfiles ya tenían otras tarifas. ¿Con cuáles te quedas para todos tus productos?</span>
  ${conf.map((c,i)=>`<div class="ru-cf" data-i="${i}"><b>${esc(c.n)}</b><span class="row"><button type="button" class="btn sm ru-cfa">${esc(ruTarsText(c.sp.labor[0]))}</button><button type="button" class="btn sm ghost ru-cfb">${esc(ruTarsText(c.r))}</button></span></div>`).join("")}</div>`;
 document.body.appendChild(md);let left=conf.length;
 md.querySelectorAll(".ru-cf").forEach(R=>{const c=conf[+R.dataset.i],pick=a=>{const e=c.sp.labor[0];if(!a){e.tars=JSON.parse(JSON.stringify(c.r.tars));e.xh=c.r.xh;e.xu=c.r.xu;ruSyncPU(e);}R.remove();if(--left===0){md.remove();fin();}};R.querySelector(".ru-cfa").onclick=()=>pick(true);R.querySelector(".ru-cfb").onclick=()=>pick(false);});}''')
decl('function ruDefaults(', r'''function ruDefaults(){if(!S.rprods)S.rprods=[];if(!S.rpkgs)S.rpkgs=[];
 /* v24 → v25: «Tu personal de X» (grupo) se separa en un producto por perfil */
 if(S.rprods.some(x=>x.kind==="staff"&&!x.n)){const old=S.rprods.filter(x=>x.kind==="staff"&&!x.n);S.rprods=S.rprods.filter(x=>!old.includes(x));old.forEach(o=>o.labor.forEach(r=>{if(!ruStaffBy(r.n))S.rprods.push(ruNewStaff(r,o.dims[0]));}));}
 /* v25 → v26: tarifas por perfil, sin mínimo; «Solo personal» deja de ser forma de contratar; un solo precio de insumos */
 S.rprods.forEach(x=>{(x.labor||[]).forEach(r=>{if(!r.tars)r.tars=[{p:r.p||"",u:r.u||""}];if(r.xu==="por turno (5 h)")r.xu="por turno de 5 h";if(!r.xu)r.xu="por hora";ruSyncPU(r);});
  if(x.kind==="prod"){if(!x.tar.i){const s=+x.tar.rent.p?x.tar.rent:+x.tar.full.p?x.tar.full:x.tar.rent;x.tar.i={p:s.p,u:s.u,q:s.q||""};}
   if(x.tw.includes("labor")){x.tw=x.tw.filter(w=>w!=="labor");if(!x.tw.includes("full"))x.tw.push("full");}x.tw=["rent","full"].filter(w=>x.tw.includes(w));
   if(!x.courses)x.courses=ruTimed(x)&&x.dishes.length?x.dishes.map((d,i)=>({n:ruCourseN(i),d:[d]})):[{n:ruCourseN(0),d:ruTimed(x)?[]:[...x.dishes]}];}});
 (S.rpkgs||[]).forEach(k=>{k.items=k.items.filter(r=>ruRefW(r)!=="labor");k.tw=["full"];});
 if(!S.rsel||!RU_T.has(S.rsel[0]))S.rsel=["Catering","Bebidas","Barra","Sin alcohol"];}''')
decl('const ruLabTot=', r'''const ruLabTot=p=>(p.labor||[]).reduce((a,r)=>a+ruProfCost(r,p.lpol)*(+r.q||1),0);
/* tiempos: banquete o formato «por tiempos» */
const ruTimed=p=>p.dims&&p.dims[1]==="Alimentos"&&(p.dims[2]==="Banquete"||/tiempo/i.test(p.dims[3]||""));
const RU_ORD=["Primer","Segundo","Tercer","Cuarto","Quinto","Sexto","Séptimo"];
const ruCourseN=i=>(RU_ORD[i]||`${i+1}.º`)+" tiempo";
const ruDishes=p=>p.courses?p.courses.flatMap(c=>c.d):p.dishes||[];''')
decl('const ruFN=', r'''const ruFN={rent:"📦 Insumos sin personal",full:"🙋 Insumos con personal",labor:"🙋 Personal"};''')
decl('function ruWithPrice(', r'''function ruWithPrice(x,w,pr){const y=JSON.parse(JSON.stringify(x));if(x.kind==="staff"){y.labor.forEach(r=>{r.tars[0].p=pr;ruSyncPU(r);});}else if(x.kind==="pkg")y.tar.full.p=pr;else y.tar.i.p=pr;return y;}''')
decl('function ruTotal(', r'''function ruInsTot(p){const t=p.tar.i||{},pr=+t.p||0,pax=+p.pax||0;if(!pr)return 0;return t.u==="Por persona"?pr*pax:RU_FIXED.includes(t.u)?pr:pr*(+t.q||pax);}
function ruTotal(p,w){const pax=+p.pax||0;
 if(p.kind==="pkg"){const t=p.tar.full,pr=+t.p||0;if(!pr)return null;const tot=t.u==="Por persona"?pr*pax:RU_FIXED.includes(t.u)?pr:pr*(+t.q||1);return{tot,pp:pax?tot/pax:null};}
 if(p.kind==="staff"){const tot=ruProfCost(p.labor[0],p.lpol);return tot?{tot,pp:null}:null;}
 const b=ruInsTot(p);if(!b)return null;const tot=w==="full"?b+ruLabTot(p):b;return{tot,pp:pax?tot/pax:null};}''')
decl('const ruTarOk=', r'''const ruInsOk=p=>{const t=p.tar.i||{};return +t.p>0&&!!t.u;};
const ruTarOk=(p,w)=>ruInsOk(p)&&(w!=="full"||(p.labor.length>0&&p.labor.every(ruTarsOk)))&&(w!=="rent"||(p.dlx.dl.length>0&&p.dlx.dl.every(dlOk)));''')
decl('function ruOk(', r'''function ruOk(p){if(!p.cov)p.cov={same:true,zones:[{state:"",all:false,munis:[]}]};const tail=p.ext.every(e=>!filled(e.c)||+e.p>0)&&(p.min.has!==true||minOk(p.min))&&(p.promo.has!==true||promoOk(p.promo))&&(p.cov.same||zonesOk(p.cov.zones));
 if(p.kind==="staff")return ruTarsOk(p.labor[0])&&tail;
 if(p.kind==="pkg")return filled(p.name)&&+p.pax>0&&+p.tar.full.p>0&&tail;
 return filled(p.name)&&+p.pax>0&&p.tw.length>0&&p.tw.every(w=>ruTarOk(p,w))&&tail;}''')
decl('function ruMiss(', r'''function ruMiss(p){const m=[];
 if(p.kind==="staff"){if(!ruTarsOk(p.labor[0]))m.push("precio y forma de cobro");}
 else{if(!filled(p.name))m.push("nombre");
  if(p.kind==="pkg"){if(!(+p.tar.full.p>0))m.push("precio del paquete");}
  else{if(!p.tw.length)m.push("cómo lo entregas y cobras");else{if(!ruInsOk(p))m.push("precio de los insumos");if(p.tw.includes("full")&&!(p.labor.length&&p.labor.every(ruTarsOk)))m.push("precio y forma de cobro de tu personal");if(p.tw.includes("rent")&&!p.dlx.dl.length)m.push("cómo entregas sin personal");else if(p.tw.includes("rent")&&!p.dlx.dl.every(dlOk))m.push("entrega por completar");}}
  if(!(+p.pax>0))m.push("para cuántas personas alcanza");}
 if(p.cov&&!p.cov.same&&!zonesOk(p.cov.zones))m.push("zona");
 if(!p.ext.every(e=>!filled(e.c)||+e.p>0))m.push("precio de cada extra");if(p.min.has===true&&!minOk(p.min))m.push("mínimo de compra");if(p.promo.has===true&&!promoOk(p.promo))m.push("promoción");return m;}''')
decl('function ruHost(', r'''let RU_EX={s:"18:00",e:"02:00"};
function ruExHtml(p){const s=ruHr(RU_EX.s),e=ruHr(RU_EX.e),H=(e<=s?e+24:e)-s,pol=p.lpol,rows=p.labor.filter(ruTarsOk);if(!rows.length)return"";let sum=0;
 const L=rows.map(r=>{const q=ruProfQuote(r,pol,s,e),n=p.kind==="staff"?1:(+r.q||1);sum+=q.tot*n;return`<div class="ru-exr"><b>${n>1?n+" × ":""}${esc(r.n)}</b>${q.lines.map(l=>`<span>${esc(l)}</span>`).join("")}<span class="ru-ext">${money(q.tot)}${n>1?` c/u · ${money(q.tot*n)}`:""}</span></div>`;}).join("");
 const notes=[pol.ride&&e<=s?`🚕 El transporte de regreso lo cubre el anfitrión${+pol.rideFee>0?` (${money(pol.rideFee)} por persona)`:""}`:"",pol.meal&&H>5?"🍽️ Alimentos para tu personal (fiesta de más de 5 h)":"",pol.uniform?"👔 Uniforme incluido":""].filter(Boolean);
 return`<div class="ru-host ru-exh"><b>👀 Así lo verá el anfitrión</b><div class="ru-exq"><span>Si su fiesta es de</span><input type="time" id="ruExS" value="${RU_EX.s}" aria-label="Empieza"><span>a</span><input type="time" id="ruExE" value="${RU_EX.e}" aria-label="Termina"><span>(${H} h)</span></div>${L}${p.kind==="staff"?"":`<div class="ru-exr ru-exsum"><b>Tu equipo en esa fiesta</b><span class="ru-ext">${money(sum)}</span></div>`}${notes.map(n=>`<span class="ru-exn">${esc(n)}</span>`).join("")}<span class="hint">Usamos la tarifa que más le conviene al anfitrión.</span></div>`;}
function ruHost(p){if(p.kind==="staff")return ruExHtml(p);const pax=+p.pax;if(!pax||!p.tw.length)return"";const L=p.tw.map(w=>{const r=ruTotal(p,w);return r?`<span>${RU_TL[w][0]}: <b>${ruMoney(r.pp)}</b> por persona · <b>${ruMoney(r.tot)}</b> en total</span>`:"";}).filter(Boolean);
 return L.length?`<div class="ru-host"><b>👀 Así lo verá el anfitrión</b><span class="hint">En una fiesta de ${pax} personas${p.tw.includes("full")?" (con personal: fiesta de 5 h)":""}:</span>${L.join("")}</div>`:"";}''')
decl('function ruTarHtml(', r'''/* precio de los insumos: uno solo para «con» y «sin» personal */
function ruInsHtml(p){const t=p.tar.i,cnt=t.u&&!RU_FIXED.includes(t.u);
 return`<div class="ru-tg" data-w="ins"><b>🧺 Precio de los insumos</b><span class="hint">Es el mismo con o sin personal; tu equipo se suma aparte.</span><div class="ru-line ru-l3"><label class="ru-f"><span class="ru-fi"><i>$</i><input type="number" min="0" inputmode="decimal" id="ruIp" class="${MISS(+t.p>0)}" value="${esc(t.p)}" placeholder="0" aria-label="Precio de los insumos"></span></label>
  <label class="ru-f ru-fsel"><span class="ru-fi"><select id="ruIu" class="${t.u?"":"ph"}${MISS(!!t.u)}" aria-label="Unidad de medida"><option value="" disabled ${t.u?"":"selected"} hidden>por persona</option>${RU_UNITS.map(u=>`<option ${t.u===u?"selected":""}>${u}</option>`).join("")}</select></span></label>
  ${cnt?`<label class="ru-f"><span class="ru-fi"><input type="number" min="1" inputmode="numeric" id="ruIq" value="${esc(t.q)}" placeholder="${esc(p.pax||"#")}" aria-label="¿Cuántas ${esc(ruNoun(t.u))}?"><i>${esc(ruNoun(t.u))}</i></span></label>`:"<span></span>"}</div></div>`;}
function ruPkgPriceHtml(p){const t=p.tar.full,cnt=!RU_FIXED.includes(t.u);
 return`<div class="ru-tg" data-w="full"><b>💲 Precio del paquete</b><div class="row"><label class="ru-money">$<input type="number" min="0" inputmode="decimal" data-tp="full" class="${MISS(+t.p>0)}" value="${esc(t.p)}" placeholder="precio" aria-label="Precio del paquete"></label>
  <select data-tu="full" aria-label="Unidad">${RU_UNITS.map(u=>`<option ${t.u===u?"selected":""}>${u}</option>`).join("")}</select>
  ${cnt?`<label class="ru-q">¿Cuántas ${esc(ruNoun(t.u))}? <input type="number" min="1" data-tq="full" class="${MISS(+t.q>0)}" value="${esc(t.q)}" placeholder="#"></label>`:""}</div></div>`;}''')
decl('function ruLaborHtml(', r'''function ruLaborHtml(p,staff){const sk=p.kind==="staff",rest=sk?[]:[...new Set(staff)].filter(n=>!p.labor.some(r=>r.n===n)),L=p.lpol;
 const pill=(k,on,txt,extra)=>`<span class="ru-pill" aria-pressed="${on}"><button type="button" class="ru-pt" data-k="${k}" aria-pressed="${on}">${on?"✓ ":""}${txt}</button>${on&&extra?extra:""}</span>`;
 const sel=(cls,val,opts,ph,lab)=>`<label class="ru-f ru-fsel"><span class="ru-fi"><select class="${cls}${val?"":" ph"}" aria-label="${esc(lab)}"><option value="" disabled ${val?"":"selected"} hidden>${ph}</option>${opts.map(([v,t])=>`<option value="${v}" ${val===v?"selected":""}>${t}</option>`).join("")}</select></span></label>`;
 const LU=RU_LU.map(([u,t])=>[u,ruShortU(t)]),XU=RU_XU.map(t=>[t,ruShortU(t)]);
 return`<div class="ru-tg ru-labr" data-w="labor"><b>${sk?"🙋 Precio de este perfil":"🙋 Tu personal"}</b><span class="hint">${sk?"Lo que cobra una persona. Puedes darle varias formas de cobro; si lo cambias, se actualiza en todos tus productos.":"Cuántos mandas y cuánto cobra cada uno. Si ya lo usaste antes, lo llenamos por ti. Cada perfil se vuelve un producto que el anfitrión puede contratar solo."}</span>
  <div class="ru-lt">${p.labor.map((r,ix)=>{const known=!sk&&ruStaffBy(r.n)&&ruTarsOk(ruStaffBy(r.n).labor[0]);return`<div class="ru-lr${sk?" one":""}" data-ix="${ix}"><div class="ru-lnr"><b class="ru-ln">${esc(r.n)}</b>${known?`<span class="ru-known" title="Precio guardado en Tu personal">🔁<span> guardado</span></span>`:""}${sk?"":`<button type="button" class="link bad ru-lrm" aria-label="Quitar ${esc(r.n)}">✕</button>`}</div>
   <div class="ru-lbody">${r.tars.map((t,j)=>`<div class="ru-line${sk?" ru-l2":""}" data-j="${j}">${sk?"":j===0?`<label class="ru-f ru-fq"><span class="ru-fi"><input type="number" min="1" inputmode="numeric" class="ru-lq" value="${esc(r.q)}" placeholder="1" aria-label="¿Cuántos ${esc(r.n)}?"></span></label>`:`<span class="ru-or">o</span>`}
     <label class="ru-f"><span class="ru-fi"><i>$</i><input type="number" min="0" inputmode="decimal" class="ru-tp${MISS(+t.p>0)}" value="${esc(t.p)}" placeholder="0" aria-label="Precio de ${esc(r.n)}"></span></label>
     ${sel("ru-tu"+MISS(!!t.u),t.u,LU,"turno 5 h","Unidad de medida de "+r.n)}${j>0?`<button type="button" class="link bad ru-trm" aria-label="Quitar esta forma de cobro">✕</button>`:""}</div>`).join("")}
    <button type="button" class="link ru-addt">＋ Otra forma de cobrarlo</button>
    <div class="ru-line ru-lx${sk?" ru-l2":""}">${sk?"":`<span class="ru-xt">Extra</span>`}<label class="ru-f"><span class="ru-fi"><i>$</i><input type="number" min="0" inputmode="decimal" class="ru-lx" value="${esc(r.xh)}" placeholder="0" aria-label="Precio extra de ${esc(r.n)}"></span></label>${sel("ru-lxu",r.xu,XU,"hora","Unidad del extra de "+r.n)}${sk?`<span class="ru-xt">Extra</span>`:""}</div></div></div>`;}).join("")||`<span class="hint">Agrega al menos un perfil.</span>`}</div>
  ${sk?"":`<div class="ru-add"><span class="ru-sl">＋ Sumar perfil</span><div class="ru-addc">${rest.map(n=>`<button type="button" class="chip ru-lab-c" data-n="${esc(n)}">＋ ${esc(n)}${ruStaffBy(n)&&ruTarsOk(ruStaffBy(n).labor[0])?` <small>${money(ruStaffBy(n).labor[0].tars[0].p)}</small>`:""}</button>`).join("")}<button type="button" class="chip new ru-lab-o">✏️ Otro</button></div><div class="ru-labnew" hidden>${ruTags("labNew",[],"Otro perfil: escribe y Enter")}</div></div>`}
  <div class="ru-pols"><span class="ru-sl">📋 Tus políticas</span><div class="ru-pils">
   ${pill("night",L.night,"🌙 Recargo después de las 12 a.m.",`<label class="ru-pin">+<input type="number" min="0" class="ru-p-pct" value="${esc(L.nightPct)}" aria-label="Recargo nocturno">%</label>`)}
   ${pill("ride",L.ride,"🚕 Transporte de regreso lo cubre el anfitrión",`<label class="ru-pin">$<input type="number" min="0" class="ru-p-fee" value="${esc(L.rideFee)}" placeholder="0" aria-label="Transporte por persona">c/u</label>`)}
   ${pill("meal",L.meal,"🍽️ Alimentos al personal (+5 h)")}
   ${pill("uniform",L.uniform,"👔 Uniforme incluido")}</div>
   <span class="hint">El tiempo cuenta desde que tu personal llega. Viáticos fuera de zona se acuerdan.</span></div>
  ${sk?"":`<div id="ruExBox">${ruExHtml(p)}</div>`}</div>`;}''')
decl('function ruFormDesc(', r'''function ruFormDesc(p,w){if(w==="rent")return p.dlx.dl.length?p.dlx.dl.map(d=>(DL_LABEL[d.m]||d.m)+(d.cobra?" (con costo)":"")).join(" · "):"Solo insumos";return"Insumos + "+(p.labor.map(r=>`${r.q} ${ruPl(r.n,r.q)}`).join(" + ")||"tu personal")+" · entrega y montaje incluidos";}''')
decl('function ruStaffCard(', r'''function ruStaffCard(p){const r=p.labor[0],ok=ruOk(p),sel=RU_PICK&&RU_PICKED.includes(p.id);
 return`<article class="ru-pc ru-sc${sel?" sel":""}${ok?"":" warn"}" data-id="${p.id}"><span class="ru-stb">🙋 Personal</span><h4>${esc(p.name)}</h4>${ruTarsOk(r)?r.tars.map((t,j)=>`<span class="ru-pr">${j?"o ":""}<b>${money(t.p)}</b> ${esc(ruXU(t.u))}</span>`).join("")+`<span class="ru-meta">${+r.xh>0?`Extra ${money(r.xh)} ${esc(r.xu||"por hora")}`:"Sin precio de extra"}</span>`:`<span class="ru-pr hint">Falta el precio</span>`}
  ${RU_PICK?ruPickB(p.id,p.name):ruTools(p.name)}</article>`;}''')
decl('function ruSiteForm(', r'''function ruSiteForm(p,w){const r=ruTotal(p,w);if(!r||r.pp===null)return"";const v=+S.svcVar||0;
 const d=w==="rent"?(p.dlx.dl.length?p.dlx.dl.map(dlText).join(" · "):"Solo insumos"):"Insumos + "+p.labor.map(x=>`${x.q} ${ruPl(x.n,x.q)}`).join(" + ")+" · entrega y montaje incluidos · fiesta de 5 h"+(p.lpol.night?` · después de las 12:00 a.m. +${p.lpol.nightPct}%`:"");
 return`<span class="pform"><span class="pfh"><b>${ruFN[w]}</b><span class="price"><span class="pl">${ruMoney(r.pp)} <small>por persona</small></span><span class="pl"><small>${ruMoney(r.tot)} en total</small></span>${v?`<span class="pl"><small class="pmv">± ${v}%</small></span>`:""}</span></span><small class="inc">${esc(d)}</small></span>`;}''')
decl('function ruSiteStaff(', r'''function ruSiteStaff(L){return L.length?`<span class="po pstaff"><span class="pob"><span class="poh"><b>🙋 Personal por persona<small class="ctag">Contrátalo solo o súmalo a tu fiesta</small></b></span>
 ${L.map(x=>{const r=x.labor[0];return`<span class="pst-r"><span>${esc(x.name)}</span><span>${esc(ruTarsText(r))}${+r.xh>0?` · extra ${money(r.xh)} ${esc(r.xu||"por hora")}`:""}</span></span>`;}).join("")}</span></span>`:"";}''')
decl('function vnItems(', r'''function vnItems(){const out=[];(S.rprods||[]).filter(p=>p.kind==="prod"&&ruOk(p)).forEach(p=>p.tw.forEach(w=>{const t=p.tar.i;out.push({g:"prod",ref:p.id+"|"+w,name:p.name,sub:ruFN[w]+(w==="full"?" · insumos aquí; tu personal con sus tarifas":""),price:t.p,unit:(t.u||"").toLowerCase()});}));
 (S.rprods||[]).filter(p=>p.kind==="staff"&&ruOk(p)).forEach(p=>{const r=p.labor[0],t=r.tars[0];out.push({g:"staff",ref:p.id,name:p.name,sub:"🙋 Tu personal",price:t.p,unit:ruXU(t.u)});});
 (S.rpkgs||[]).filter(k=>!k.items.includes("venue")&&ruOk(k)).forEach(k=>{const t=k.tar.full;out.push({g:"pkg",ref:"pkg:"+k.id,name:k.name,sub:"🎁 Paquete",price:t&&t.p,unit:t&&t.u.toLowerCase()});});return out;}''')
(V / 'svc7.js').write_text('\n'.join(L))
print('ok decls')

# ---------- reemplazos puntuales ----------
s = (V / 'svc7.js').read_text()


def rep(a, b, c=1):
    global s
    assert s.count(a) == c, ('NO/MULTI', a[:100], s.count(a))
    s = s.replace(a, b)


rep('const ruBlankT=u=>({full:{p:"",u,q:""},rent:{p:"",u,q:""},labor:{p:"",u:"Por hora",q:""}});',
    'const ruBlankT=u=>({i:{p:"",u,q:""},full:{p:"",u,q:""},rent:{p:"",u,q:""},labor:{p:"",u:"Por hora",q:""}});')
rep('pax:"",tw:[],tar:ruBlankT(u)},ruBlankMore());}', 'pax:"",tw:[],tar:ruBlankT(u),courses:[{n:ruCourseN(0),d:[]}]},ruBlankMore());}')
# demo v26
rep('dishes:["Crema de elote","Mole poblano con pollo","Flan napolitano"]', 'dishes:["Crema de elote","Mole poblano con pollo","Flan napolitano"],courses:[{n:"Primer tiempo",d:["Crema de elote"]},{n:"Segundo tiempo",d:["Mole poblano con pollo","Arroz rojo"]},{n:"Postre",d:["Flan napolitano"]}]')
rep('tw:["full","rent","labor"],labor:[{n:"Mesero",q:"7",p:"90",u:"Por hora",min:"5",xh:"110",xu:"por hora"},{n:"Cocinero",q:"2",p:"700",u:"Por turno (5 h)",min:"5",xh:"150",xu:"por hora"},{n:"Capitán de meseros",q:"1",p:"130",u:"Por hora",min:"5",xh:"160",xu:"por hora"}]',
    'tw:["rent","full"],labor:[{n:"Mesero",q:"7",tars:[{p:"1000",u:"Por turno (5 h)"},{p:"250",u:"Por hora"}],xh:"200",xu:"por hora"},{n:"Cocinero",q:"2",tars:[{p:"1200",u:"Por turno (5 h)"}],xh:"250",xu:"por hora"},{n:"Capitán de meseros",q:"1",tars:[{p:"1400",u:"Por turno (5 h)"}],xh:"280",xu:"por hora"}]')
rep('a.tar.full.p="650";a.tar.rent.p="480";', 'a.tar.i={p:"480",u:"Por persona",q:""};a.lpol.ride=true;a.lpol.rideFee="150";')
rep('tw:["full","labor"],labor:[{n:"Bartender",q:"2",p:"280",u:"Por hora",min:"5",xh:"320",xu:"por hora"}]});b.tar.full.p="95";',
    'tw:["full"],labor:[{n:"Bartender",q:"2",tars:[{p:"1500",u:"Por turno (5 h)"},{p:"350",u:"Por hora"}],xh:"320",xu:"por hora"}]});b.tar.i={p:"60",u:"Por persona",q:""};')
rep('c.tar.rent.p="3500";c.tar.rent.u="Por evento";', 'c.tar.i={p:"3500",u:"Por evento",q:""};')
rep('const st=[...a.labor,...b.labor].map(r=>ruNewStaff(r,"Catering"));', '[a,b].forEach(x=>x.labor.forEach(ruSyncPU));const st=[...a.labor,...b.labor].map(r=>ruNewStaff(r,"Catering"));')
rep('"pdemo1|rent":{on:true,p:""},"pdemo2|full":{on:true,p:""}', '"pdemo1|rent":{on:true,p:"440"},"pdemo2|full":{on:true,p:""}')
rep('vin:{"pdemo1|full":{on:true,p:"590"},', 'vin:{"pdemo1|full":{on:true,p:"440"},')
# package total for staff refs
rep('if(x.kind==="staff"){const y=vin?ruWithPrice(x,"labor",vin.p):x,r=y.labor[0];return(+r.p||0)*(r.u==="Por hora"?(+r.min||5):1)*(+(P.qty&&P.qty[ref])||1);}',
    'if(x.kind==="staff"){const y=vin?ruWithPrice(x,"labor",vin.p):x;return ruProfCost(y.labor[0],y.lpol)*(+(P.qty&&P.qty[ref])||1);}')
rep('return!x?[]:x.kind==="staff"?[x.n]:x.crew.map(c=>c.n);', 'return!x?[]:x.kind==="staff"?[x.n]:ruRefW(r)==="full"?(x.labor||[]).map(c=>c.n):[];')
# etiquetas para tags separadas por coma (pegar «a, b» agrega dos)
rep('const add=v=>{v=(v||"").trim().replace(/,$/,"");if(!v)return;if(onAdd)onAdd(v);else{if(L.some(x=>nrm(x)===nrm(v)))return;L.push(v);}redraw(id);};',
    'const add=v=>{const P=String(v||"").split(",").map(x=>x.trim()).filter(Boolean);if(!P.length)return;P.forEach(v=>{if(onAdd)onAdd(v);else if(!L.some(x=>nrm(x)===nrm(v)))L.push(v);});redraw(id);};')
# ---------- ficha: tiempos, insumos y «¿Cómo lo entregas y cobras?» ----------
a = s.index('''${sk?ruLaborHtml(p,staff):`<div class="field ru-inc"><span class="lbl">¿Qué incluye?</span>''')
b = s.index('''${sk?`<div id="ruHost">${ruHost(p)}</div>`''')
s = s[:a] + r'''${sk?ruLaborHtml(p,staff):pk?`<div class="field ru-inc"><span class="lbl">¿Qué incluye?</span><span class="ru-sl">🧺 Además incluye <span class="opt">opcional</span></span>${ruTags("ins",p.ins,"Ej. centros de mesa, mantelería")}</div>
 <div class="field">${sug?`<div class="ru-sug">💡 Tus productos suman <b>${ruMoney(sug)}</b>${+p.pax?` · ${ruMoney(sug/ +p.pax)} por persona`:""}<button type="button" class="link" id="ruUseSug">Usar como precio</button></div>`:""}${ruPkgPriceHtml(p)}</div>`
 :`<div class="field ru-inc"><span class="lbl">¿Qué incluye?</span>
  ${ruFood(p)?(ruTimed(p)?`<span class="ru-sl">🍴 Platillos por tiempo <span class="opt">escribe y te sugerimos</span></span>
   ${p.courses.map((c,i)=>`<div class="ru-course" data-i="${i}"><div class="ru-ch"><input type="text" class="ru-cn" value="${esc(c.n)}" aria-label="Nombre del tiempo">${p.courses.length>1?`<button type="button" class="link bad ru-crm" aria-label="Quitar ${esc(c.n)}">✕</button>`:""}</div>${ruTags("course"+i,c.d,i===0?"Ej. crema de elote, sopa de fideo":"Escribe y te sugerimos")}</div>`).join("")}
   <span class="hint ru-comma">Separa los platillos con coma o Enter.</span><button type="button" class="link ru-cadd" style="justify-self:start">＋ Agregar tiempo</button>`
   :`<span class="ru-sl">🍴 Platillos <span class="opt">escribe y te sugerimos</span></span>${ruTags("course0",p.courses[0].d,"Ej. tacos al pastor, quesadillas")}<span class="hint ru-comma">Separa los platillos con coma o Enter.</span>`):""}
  <span class="ru-sl">🧺 Insumos <span class="opt">solo el nombre; alcanzan para tus personas</span></span>${ruTags("ins",p.ins,"Ej. platos, hielo, mantelería")}<span class="hint ru-comma">Sepáralos con coma o Enter.</span></div>
 <div class="field"><span class="lbl">🚚 ¿Cómo lo entregas y cobras? <span class="opt">elige una o las dos</span></span>
  <div class="ru-tsel ru-tsel2${MISS(p.tw.length>0)}">${["rent","full"].map(w=>`<button type="button" class="ru-tsb" data-w="${w}" aria-pressed="${p.tw.includes(w)}"><b>${RU_TL[w][0]}</b><small>${RU_TL[w][1]}</small></button>`).join("")}</div>
  ${p.tw.length?ruInsHtml(p):""}
  ${p.tw.includes("rent")?`<div class="ru-tg" data-w="rent"><b>${RU_TL.rent[0]}</b>${dlSecHtml(p.dlx,k+"dlx","rt","¿Cómo lo entregas?")}</div>`:""}
  ${p.tw.includes("full")?`<div class="ru-tg" data-w="full"><b>${RU_TL.full[0]}</b><span class="ru-note">🚚 La entrega y el montaje van incluidos: tu equipo va al evento.</span>${ruLaborHtml(p,staff)}</div>`:""}</div>`}
 ''' + s[b:]
# ---------- enlaces de la ficha ----------
rep('ruBindTags(box,"dishes",p.dishes,()=>RU_DISHES,null,rd);',
    '''(p.courses||[]).forEach((c,i)=>ruBindTags(box,"course"+i,c.d,()=>RU_DISHES,null,rd));
 box.querySelectorAll(".ru-course").forEach(C=>{const c=p.courses[+C.dataset.i];C.querySelector(".ru-cn").oninput=e=>{c.n=e.target.value;};const x=C.querySelector(".ru-crm");if(x)x.onclick=()=>{p.courses.splice(+C.dataset.i,1);ruDrawIdent();};});
 const ca=box.querySelector(".ru-cadd");if(ca)ca.onclick=()=>{p.courses.push({n:ruCourseN(p.courses.length),d:[]});ruDrawIdent(false,"course"+(p.courses.length-1));};
 const ip=$("ruIp"),iu=$("ruIu"),iq=$("ruIq");if(ip)ip.oninput=e=>{p.tar.i.p=e.target.value;live();};if(iu)iu.onchange=e=>{p.tar.i.u=e.target.value;ruDrawIdent();};if(iq)iq.oninput=e=>{p.tar.i.q=e.target.value;live();};''')
rep('''box.querySelectorAll(".ru-tsb").forEach(b=>b.onclick=()=>{const w=b.dataset.w;p.tw=p.tw.includes(w)?p.tw.filter(x=>x!==w):["full","rent","labor"].filter(x=>x===w||p.tw.includes(x));
  if(w==="labor"&&p.tw.includes("labor")&&!p.labor.length)p.labor=p.crew.map(r=>ruLabRow(r.n,r.q));ruDrawIdent();});''',
    '''box.querySelectorAll(".ru-tsb").forEach(b=>b.onclick=()=>{const w=b.dataset.w;p.tw=p.tw.includes(w)?p.tw.filter(x=>x!==w):["rent","full"].filter(x=>x===w||p.tw.includes(x));
  if(w==="full"&&p.tw.includes("full")&&!p.labor.length)p.labor=p.crew.map(r=>ruLabRow(r.n,r.q));if(!p.tar.i.u)p.tar.i.u=(RU_U[p.dims.join("|")]||["Por persona"])[0];ruDrawIdent();});''')
rep('const live=()=>{$("ruHost").innerHTML=ruHost(p);};',
    '''const bindEx=()=>{const s=$("ruExS"),e=$("ruExE");if(s)s.onchange=x=>{RU_EX.s=x.target.value||"18:00";live();};if(e)e.onchange=x=>{RU_EX.e=x.target.value||"02:00";live();};};
 const live=()=>{const h=$("ruHost");if(h)h.innerHTML=ruHost(p);const x=$("ruExBox");if(x)x.innerHTML=ruExHtml(p);bindEx();};bindEx();''')
a = s.index('box.querySelectorAll(".ru-lr").forEach(R=>{const r=p.labor[+R.dataset.ix];')
b = s.index('box.querySelectorAll(".ru-pt").forEach(')
s = s[:a] + r'''box.querySelectorAll(".ru-lr").forEach(R=>{const r=p.labor[+R.dataset.ix],up=()=>{ruSyncPU(r);live();};
  const q=R.querySelector(".ru-lq");if(q)q.oninput=e=>{r.q=e.target.value;live();};
  R.querySelectorAll(".ru-line[data-j]").forEach(T=>{const t=r.tars[+T.dataset.j];T.querySelector(".ru-tp").oninput=e=>{t.p=e.target.value;up();};T.querySelector(".ru-tu").onchange=e=>{t.u=e.target.value;e.target.classList.remove("ph");if(!r.xu)r.xu=t.u==="Por hora"?"por hora":"por hora";up();};const x=T.querySelector(".ru-trm");if(x)x.onclick=()=>{r.tars.splice(+T.dataset.j,1);ruSyncPU(r);ruDrawIdent();};});
  R.querySelector(".ru-addt").onclick=()=>{const used=r.tars.map(t=>t.u);r.tars.push({p:"",u:(RU_LU.find(([u])=>!used.includes(u))||[""])[0]});ruDrawIdent();setTimeout(()=>{const l=[...document.querySelectorAll(`#ruIdent .ru-lr[data-ix="${R.dataset.ix}"] .ru-tp`)].pop();l&&l.focus({preventScroll:true});},0);};
  R.querySelector(".ru-lx").oninput=e=>{r.xh=e.target.value;live();};R.querySelector(".ru-lxu").onchange=e=>{r.xu=e.target.value;e.target.classList.remove("ph");live();};
  const rm=R.querySelector(".ru-lrm");if(rm)rm.onclick=()=>{p.labor.splice(+R.dataset.ix,1);ruDrawIdent();};});
 ''' + s[b:]
rep('''box.querySelectorAll(".ru-crew").forEach(b=>b.onclick=()=>{const n=b.dataset.n,ix=p.crew.findIndex(r=>r.n===n);if(ix>=0)p.crew.splice(ix,1);else p.crew.push({n,q:"1"});ruDrawIdent();});''', '')
rep('const us=$("ruUseSug");if(us)us.onclick=()=>{const s=ruSug(p);if(!p.tw.includes("full"))p.tw.unshift("full");', 'const us=$("ruUseSug");if(us)us.onclick=()=>{const s=ruSug(p);p.tw=["full"];')
# imagen para redes y emblema: platillos por tiempos
rep('[...p.dishes,...p.ins].slice(0,4).join(", ")', '[...ruDishes(p),...p.ins].slice(0,4).join(", ")')
# sitio: platillos por tiempos
rep('${p.dishes.length?`<small class="inc">🍴 ${esc(p.dishes.join(", "))}</small>`:""}',
    '${ruDishes(p).length?(ruTimed(p)?p.courses.filter(c=>c.d.length).map(c=>`<small class="inc">🍴 <b>${esc(c.n)}:</b> ${esc(c.d.join(", "))}</small>`).join(""):`<small class="inc">🍴 ${esc(ruDishes(p).join(", "))}</small>`):""}')
(V / 'svc7.js').write_text(s)
print('ok v26')
s = (V / 'svc7.js').read_text()
assert s.count("p.tw.includes('labor')") == 1
s = s.replace("p.tw.includes('labor')", "p.tw.includes('full')")
(V / 'svc7.js').write_text(s)
print('ok sync personal al guardar')
