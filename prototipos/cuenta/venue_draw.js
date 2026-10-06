function drawVenue(){const v=S.venue,k="v";const isR=v.mode==="renta"||v.mode==="ambos",isP=v.mode==="paquetes"||v.mode==="ambos";
 const pol=HQV.POLICY_CATS.map(([s,e])=>{const p=v.policy[s];return`<div class="pol2${MISS(polOk(p))}" data-s="${esc(s)}"><b>${e} ${esc(s)}</b>
  <span class="mini-l">¿Lo ofreces?</span><div class="chips">${[["inc","✅ Incluido"],["costo","💲 Con costo"],["no","No"]].map(([val,t])=>`<button type="button" class="chip pof" data-v="${val}" aria-pressed="${p.offer===val}">${TICK}${t}</button>`).join("")}</div>
  ${p.offer==="costo"?`<div class="row"><input type="number" min="0" class="ppr" value="${esc(p.price)}" placeholder="$ precio" aria-label="Precio de ${esc(s)}"><select class="pper" aria-label="Cómo lo cobras">${[["evento","por evento"],["persona","por persona"]].map(([val,t])=>`<option value="${val}" ${p.per===val?'selected':''}>${t}</option>`).join("")}</select></div>`:''}
  <span class="mini-l">¿El cliente puede traer el suyo?</span><div class="chips">${[["si","🆓 Libre"],["cuota","🎟️ Con cuota"],["no","🔒 No"]].map(([val,t])=>`<button type="button" class="chip pow" data-v="${val}" aria-pressed="${p.own===val}">${TICK}${t}</button>`).join("")}</div>
  ${p.own==="cuota"?`<input type="number" min="0" class="pfee" value="${esc(p.fee)}" placeholder="$ cuota por evento (descorche, derecho de piso…)" aria-label="Cuota por traer ${esc(s)}">`:''}</div>`;}).join("");
 const pk=v.packages.map((x,i)=>`<div class="pkg${MISS(pkgOk(x))}" data-i="${i}"><div class="row"><input type="text" class="pk-n" value="${esc(x.name)}" placeholder="Nombre: Paquete 1, Plata, Básico…" aria-label="Nombre del paquete"><input type="number" min="0" class="pk-p" value="${esc(x.price)}" placeholder="$ precio" aria-label="Precio del paquete"></div>
  <div class="row"><select class="pk-per" aria-label="Cómo se cobra">${[["persona","por persona"],["total","precio total"]].map(([val,t])=>`<option value="${val}" ${x.per===val?'selected':''}>${t}</option>`).join("")}</select><input type="number" min="0" class="pk-m" value="${esc(x.min)}" placeholder="Mínimo de invitados (opcional)" aria-label="Mínimo de invitados"></div>
  <span class="mini-l">Este paquete incluye</span><div class="chips">${HQV.POLICY_CATS.map(([s,e])=>`<button type="button" class="chip pk-i" data-s="${esc(s)}" aria-pressed="${x.inc.includes(s)}">${TICK}${e} ${esc(s)}</button>`).join("")}</div>
  <button type="button" class="link bad pk-rm">Quitar paquete</button></div>`).join("");
 const std=venueStdRows(v);
 $("stepBody").innerHTML=`<div class="panel"><span class="crumb">Mi negocio › Venue</span><h2>Mi venue 🏡</h2>
 <div class="alert info">💡 <span><b>¿Qué es un venue?</b> Es cualquier lugar donde se puede hacer una fiesta: una terraza, un jardín, un salón, un roof, una casa o un restaurante que rentas para eventos.</span></div>
 <div class="field"><label class="lbl" for="v-name">Nombre del lugar</label><input type="text" id="v-name" class="${MISS(filled(v.name))}" value="${esc(v.name)}" placeholder="Terraza Las Flores"></div>
 ${avatarHtml(v,"vav","avatar","🖼️ Foto de logo o perfil del lugar")}
 ${socialHtml(v,"v")}
 ${addrHtml(v.addr,"v","Dirección del lugar")}
 <div class="field"><span class="lbl">Tipo de espacio</span><div class="cats${MISS(!!v.type)}">${HQV.VENUE_TYPES.map(([t,e])=>`<button type="button" class="cat vt" data-t="${esc(t)}" aria-pressed="${v.type===t}"><span class="emo">${e}</span><span>${esc(t)}</span></button>`).join("")}</div></div>
 <div class="field"><span class="lbl">👥 ¿Cuántas personas caben?</span><div class="row"><div class="field"><label class="hint" for="v-seat">🪑 Sentadas</label><input type="number" id="v-seat" min="1" class="${MISS(+v.seated>0)}" value="${esc(v.seated)}"></div><div class="field"><label class="hint" for="v-stand">🕺 De pie</label><input type="number" id="v-stand" min="1" class="${MISS(+v.standing>0)}" value="${esc(v.standing)}"></div></div><span class="hint">Calculamos uno con el otro (de pie ≈ 1.5 × sentadas). Ajústalo si en tu lugar es distinto.</span></div>
 <div class="field"><label class="lbl" for="v-area">📐 Tamaño</label><select id="v-area" class="${MISS(!!v.area)}"><option value="">Elige</option>${["6 a 12 m²","13 a 20 m²","21 a 30 m²","31 a 40 m²","41 a 50 m²","51 a 60 m²","61 a 100 m²","101 a 300 m²","Más de 300 m²"].map(t=>`<option ${t===v.area?'selected':''}>${t}</option>`).join("")}</select></div>
 <div class="field"><span class="lbl">🏠 ¿Con qué cuenta tu espacio?</span><span class="hint">Los anfitriones buscan con esta misma lista. Lo que no marques, no aparecerá en sus búsquedas.</span><div class="chips${MISS(v.features.length>0)}" style="border-radius:14px">${HQV.VENUE_FEATS.map(([id,e,t])=>`<button type="button" class="chip ft" data-f="${id}" aria-pressed="${v.features.includes(id)}">${TICK}${e} ${esc(t)}</button>`).join("")}</div></div>
 <div class="field"><span class="lbl">🚻 Baños</span><div class="row${MISS(+v.baths.m+ +v.baths.w+ +v.baths.g>0)}" style="border-radius:12px">${[["m","🚹 Hombres"],["w","🚺 Mujeres"],["g","🚻 Generales"]].map(([f,t])=>`<div class="field"><label class="hint" for="vb-${f}">${t}</label><input type="number" min="0" id="vb-${f}" value="${esc(v.baths[f])}" placeholder="0"></div>`).join("")}</div></div>

 <div class="field"><span class="lbl">🕒 Horario</span><div class="sub-box">
  <span class="hint">¿Qué días rentas?</span><div class="chips${MISS(v.days.length>0)}" style="border-radius:14px">${HQV.DAYS.map(([d,t])=>`<button type="button" class="chip vd" data-d="${d}" aria-pressed="${v.days.includes(d)}">${TICK}${t}</button>`).join("")}</div>
  <div class="row"><div class="field"><label class="hint" for="v-open">Pueden empezar desde</label><input type="time" id="v-open" class="${MISS(filled(v.open))}" value="${esc(v.open)}"></div>
   <div class="field"><label class="hint" for="v-limit">Hora límite (todos fuera)</label><input type="time" id="v-limit" class="${MISS(filled(v.limit))}" value="${esc(v.limit)}"></div></div>
  <div class="row"><div class="field"><label class="hint" for="v-hincl">Horas de fiesta incluidas</label><input type="number" id="v-hincl" min="1" max="24" class="${MISS(+v.hoursIncl>0)}" value="${esc(v.hoursIncl)}"></div>
   <div class="field"><label class="hint" for="v-xh">Cada hora extra $</label><input type="number" id="v-xh" min="0" class="${MISS(filled(v.extraHour))}" value="${esc(v.extraHour)}"></div></div>
  <span class="hint">📏 Estándar ¡HQV!: además de las horas de fiesta, se dan ½ hora para montar y ½ hora para desmontar sin costo.</span></div></div>

 <div class="field"><span class="lbl">💲 ¿Cómo cobras?</span><div class="chips${MISS(!!v.mode)}" style="border-radius:14px">${[["renta","🏠 Renta del espacio"],["paquetes","📦 Paquetes"],["ambos","Las dos"]].map(([val,t])=>`<button type="button" class="chip vm" data-v="${val}" aria-pressed="${v.mode===val}">${TICK}${t}</button>`).join("")}</div>
  ${isR?`<div class="sub-box"><b style="font-size:14px">🏠 Renta del espacio</b><div class="row"><input type="number" min="0" id="r-price" class="${MISS(filled(v.rent.price))}" value="${esc(v.rent.price)}" placeholder="$ precio" aria-label="Precio de renta"><select id="r-per" aria-label="Cómo cobras la renta">${[["evento",`por evento (${v.hoursIncl||5} h incluidas)`],["hora","por hora"],["persona","por persona"]].map(([val,t])=>`<option value="${val}" ${v.rent.per===val?'selected':''}>${t}</option>`).join("")}</select></div>
   <div class="row"><div class="field"><label class="hint" for="r-upto">Incluye hasta (invitados) <span class="opt">opcional</span></label><input type="number" min="0" id="r-upto" value="${esc(v.rent.upTo)}" placeholder="Ej. 60"></div><div class="field"><label class="hint" for="r-pxg">Cada invitado extra $</label><input type="number" min="0" id="r-pxg" value="${esc(v.rent.perExtraGuest)}" placeholder="Ej. 150" ${filled(v.rent.upTo)?'':'disabled'}></div></div></div>`:''}
  ${isP?`<div class="sub-box"><b style="font-size:14px">📦 Mis paquetes</b><span class="hint">Por ejemplo: Paquete 1 básico, Paquete 2 con más cosas, Paquete 3 premium.</span>${pk||''}${v.packages.length<4?`<button type="button" class="btn ghost sm" id="pk-add">+ Agregar paquete</button>`:''}</div>`:''}</div>

 <div class="field"><span class="lbl">📈 Ajustes de precio <span class="opt">(opcional)</span></span><div class="sub-box">
  <span class="hint">¿Cobras distinto según el día? Pon el porcentaje de más (+) o de menos (−).</span>
  <div class="dayadj">${HQV.DAYS.filter(([d])=>v.days.includes(d)).map(([d,t])=>`<label><span>${t}</span><input type="number" step="5" class="adj-d" data-d="${d}" value="${esc(v.adj.day[d]||"")}" placeholder="0 %" aria-label="Ajuste ${HQV.DAY_NAMES[d]}"></label>`).join("")||'<span class="hint">Primero elige los días que rentas.</span>'}</div>
  <div class="field"><label class="hint" for="adj-dt">Si la fiesta es de día (termina antes de las 7 pm), % de ajuste</label><input type="number" step="5" id="adj-dt" value="${esc(v.adj.daytime)}" placeholder="Ej. −10"></div>
  <span class="hint">¿Rentas espacios extra? (salón VIP, terraza, alberca…)</span>
  ${v.spaces.map((x,i)=>`<div class="row sp-row" data-i="${i}"><input type="text" class="sp-n" value="${esc(x.name)}" placeholder="Nombre del espacio" aria-label="Espacio extra"><input type="number" min="0" class="sp-p" value="${esc(x.price)}" placeholder="$ por evento" aria-label="Precio del espacio extra"><button type="button" class="link bad sp-rm">Quitar</button></div>`).join("")}
  <button type="button" class="btn ghost sm" id="sp-add" style="width:fit-content">+ Espacio extra</button>
  <span class="hint">¿Tu precio es negociable?</span><div class="chips${MISS(v.negotiable!==null)}" style="width:fit-content;border-radius:99px">${[[true,"🤝 Sí, se puede platicar"],[false,"Precio fijo"]].map(([val,t])=>`<button type="button" class="chip neg" data-v="${val}" aria-pressed="${v.negotiable===val}">${TICK}${t}</button>`).join("")}</div></div></div>

 <div class="field"><span class="lbl">🔄 Servicios en tu venue</span><span class="hint">Para cada servicio dinos si tú lo ofreces y si el cliente puede traer el suyo (🔒 No = solo con tu gente o tu equipo). Así solo te llegan fiestas que sí puedes atender.</span><div class="pol">${pol}</div></div>
 <div class="field"><span class="lbl">📝 Condiciones para rentarlo</span><div class="sub-box">
  <div class="field"><span class="hint">Anticipo para apartar</span><div class="chips${MISS(!!v.deposit)}" style="width:fit-content;border-radius:99px">${["30%","50%","100%"].map(t=>`<button type="button" class="chip dep" data-v="${t}" aria-pressed="${v.deposit===t}">${TICK}${t}</button>`).join("")}</div></div>
  <div class="row"><div class="field"><label class="hint" for="v-adv">Reservar con (días de anticipación)</label><input type="number" id="v-adv" min="0" class="${MISS(filled(v.advance))}" value="${esc(v.advance)}"></div>
   <div class="field"><label class="hint" for="v-guar">Depósito en garantía $ <span class="opt">(opcional)</span></label><input type="number" id="v-guar" min="0" value="${esc(v.guarantee)}"></div>
   <div class="field"><label class="hint" for="v-cork">Descorche <span class="opt">(opcional)</span></label><input type="text" id="v-cork" value="${esc(v.corkage)}" placeholder="$150 por botella"></div></div>
  <div class="field"><label class="hint" for="v-cancel">Cancelación <span class="opt">(opcional)</span></label><input type="text" id="v-cancel" value="${esc(v.cancel)}" placeholder="Reembolso del anticipo con 30 días de aviso"></div>
  <div class="field"><span class="hint">📄 Documentos que pides al cliente</span><div class="chips${MISS(v.docsNone||v.docs.length>0||filled(v.docsOther))}" style="border-radius:14px">${DOCS.map(d=>`<button type="button" class="chip doc" data-d="${esc(d)}" aria-pressed="${v.docs.includes(d)}" ${v.docsNone?'disabled':''}>${TICK}${esc(d)}</button>`).join("")}<button type="button" class="chip" id="docNone" aria-pressed="${v.docsNone}">${TICK}No pido documentos</button></div>
   ${v.docsNone?'':`<input type="text" id="v-docs" value="${esc(v.docsOther)}" placeholder="Otro documento (opcional)">`}</div>
  <div class="field"><label class="hint" for="v-rules">📌 Reglas del lugar: escríbelas o sube tu reglamento</label><textarea id="v-rules" class="${MISS(filled(v.rulesText)||!!v.rulesFile)}" placeholder="Sin confeti, volumen moderado después de las 22:00…">${esc(v.rulesText)}</textarea>
   <div class="up-top"><label class="pick">📎 Subir reglamento<input type="file" id="v-rfile" accept="application/pdf,image/jpeg,image/png"></label><span class="specs"><span><b>PDF, JPG o PNG</b></span><span>hasta <b>10 MB</b></span></span></div>
   ${v.rulesFile?`<span class="file-chip">📄 ${esc(v.rulesFile.name)} · ${kb(v.rulesFile.size)} <button type="button" class="link bad" id="v-rrm">Quitar</button></span>`:''}<div id="rmsg"></div></div></div></div>
 <div class="stdbox" id="stdbox">${std}</div>
 ${promoHtml(v.promo,k,"venue")}
 <div class="field"><span class="lbl">📷 Fotos del lugar</span><span class="hint">Una desde cada esquina, de día y de noche, y montado como para un evento.</span>${uploaderHtml(k,"photo",v.photos,v.photos.length>0)}</div>
 ${navHtml()}</div>`;
 const redraw=()=>{const y=scrollY;drawVenue();scrollTo({top:y});};
 const ch=()=>{changed();const b=$("stdbox");if(b)b.innerHTML=venueStdRows(v);};
 [["v-name","name"],["v-area","area"],["v-open","open"],["v-limit","limit"],["v-hincl","hoursIncl"],["v-xh","extraHour"],["v-adv","advance"],["v-guar","guarantee"],["v-cork","corkage"],["v-cancel","cancel"],["v-rules","rulesText"]].forEach(([i,f])=>{$(i).oninput=$(i).onchange=e=>{v[f]=e.target.value;ch();};});
 $("v-seat").oninput=e=>{v.seated=e.target.value;v.standing=+v.seated>0?String(Math.round(+v.seated*1.5)):"";$("v-stand").value=v.standing;ch();};
 $("v-stand").oninput=e=>{v.standing=e.target.value;v.seated=+v.standing>0?String(Math.round(+v.standing/1.5)):"";$("v-seat").value=v.seated;ch();};
 ["m","w","g"].forEach(f=>$("vb-"+f).oninput=e=>{v.baths[f]=e.target.value;ch();});
 document.querySelectorAll(".vt").forEach(t=>t.onclick=()=>{v.type=t.dataset.t;document.querySelectorAll(".vt").forEach(x=>x.setAttribute("aria-pressed",x===t));ch();});
 document.querySelectorAll(".ft").forEach(c=>c.onclick=()=>{const f=c.dataset.f;v.features=v.features.includes(f)?v.features.filter(x=>x!==f):[...v.features,f];c.setAttribute("aria-pressed",v.features.includes(f));ch();});
 document.querySelectorAll(".vd").forEach(c=>c.onclick=()=>{const d=c.dataset.d;v.days=v.days.includes(d)?v.days.filter(x=>x!==d):HQV.DAYS.map(x=>x[0]).filter(x=>x===d||v.days.includes(x));redraw();changed();});
 document.querySelectorAll(".vm").forEach(c=>c.onclick=()=>{v.mode=c.dataset.v;if((v.mode==="paquetes"||v.mode==="ambos")&&!v.packages.length)v.packages.push(blankPkg());redraw();changed();});
 const rp=$("r-price");if(rp){rp.oninput=e=>{v.rent.price=e.target.value;ch();};$("r-per").onchange=e=>{v.rent.per=e.target.value;ch();};$("r-upto").oninput=e=>{v.rent.upTo=e.target.value;$("r-pxg").disabled=!filled(v.rent.upTo);ch();};$("r-pxg").oninput=e=>{v.rent.perExtraGuest=e.target.value;ch();};}
 document.querySelectorAll(".pkg").forEach(box=>{const x=v.packages[+box.dataset.i];const q=s=>box.querySelector(s);
  q(".pk-n").oninput=e=>{x.name=e.target.value;ch();};q(".pk-p").oninput=e=>{x.price=e.target.value;ch();};q(".pk-per").onchange=e=>{x.per=e.target.value;ch();};q(".pk-m").oninput=e=>{x.min=e.target.value;ch();};
  box.querySelectorAll(".pk-i").forEach(c=>c.onclick=()=>{const s=c.dataset.s;x.inc=x.inc.includes(s)?x.inc.filter(y=>y!==s):[...x.inc,s];c.setAttribute("aria-pressed",x.inc.includes(s));ch();});
  q(".pk-rm").onclick=()=>{v.packages.splice(+box.dataset.i,1);redraw();changed();};});
 const pa=$("pk-add");if(pa)pa.onclick=()=>{v.packages.push(blankPkg());redraw();changed();};
 document.querySelectorAll(".adj-d").forEach(i=>i.oninput=()=>{v.adj.day[i.dataset.d]=i.value;ch();});
 $("adj-dt").oninput=e=>{v.adj.daytime=e.target.value;ch();};
 document.querySelectorAll(".sp-row").forEach(r=>{const x=v.spaces[+r.dataset.i];r.querySelector(".sp-n").oninput=e=>{x.name=e.target.value;ch();};r.querySelector(".sp-p").oninput=e=>{x.price=e.target.value;ch();};r.querySelector(".sp-rm").onclick=()=>{v.spaces.splice(+r.dataset.i,1);redraw();changed();};});
 $("sp-add").onclick=()=>{v.spaces.push({name:"",price:""});redraw();changed();};
 document.querySelectorAll(".neg").forEach(c=>c.onclick=()=>{v.negotiable=c.dataset.v==="true";document.querySelectorAll(".neg").forEach(x=>x.setAttribute("aria-pressed",x===c));ch();});
 document.querySelectorAll(".pol2").forEach(box=>{const p=v.policy[box.dataset.s];
  box.querySelectorAll(".pof").forEach(c=>c.onclick=()=>{p.offer=c.dataset.v;redraw();changed();});
  box.querySelectorAll(".pow").forEach(c=>c.onclick=()=>{p.own=c.dataset.v;redraw();changed();});
  const pr=box.querySelector(".ppr");if(pr){pr.oninput=e=>{p.price=e.target.value;box.classList.toggle("miss",showMiss&&!polOk(p));ch();};box.querySelector(".pper").onchange=e=>{p.per=e.target.value;ch();};}
  const fe=box.querySelector(".pfee");if(fe)fe.oninput=e=>{p.fee=e.target.value;box.classList.toggle("miss",showMiss&&!polOk(p));ch();};});
 document.querySelectorAll(".dep").forEach(c=>c.onclick=()=>{v.deposit=c.dataset.v;document.querySelectorAll(".dep").forEach(x=>x.setAttribute("aria-pressed",x===c));ch();});
 document.querySelectorAll(".doc").forEach(c=>c.onclick=()=>{const d=c.dataset.d;v.docs=v.docs.includes(d)?v.docs.filter(x=>x!==d):[...v.docs,d];c.setAttribute("aria-pressed",v.docs.includes(d));ch();});
 $("docNone").onclick=()=>{v.docsNone=!v.docsNone;if(v.docsNone){v.docs=[];v.docsOther="";}redraw();changed();};
 const dO=$("v-docs");if(dO)dO.oninput=e=>{v.docsOther=e.target.value;ch();};
 $("v-rfile").onchange=e=>{const f=e.target.files[0];e.target.value="";if(!f)return;const okT=["application/pdf","image/jpeg","image/png"];
  if(!okT.includes(f.type)){$("rmsg").innerHTML=`<div class="alert bad">❌ <span>"${esc(f.name)}" no es PDF, JPG ni PNG. Si es un Word, guárdalo como PDF y vuelve a subirlo.</span></div>`;return;}
  if(f.size>10*1048576){$("rmsg").innerHTML=`<div class="alert bad">❌ <span>"${esc(f.name)}" pesa ${kb(f.size)}; el máximo es 10 MB.</span></div>`;return;}
  v.rulesFile={name:f.name,size:f.size};redraw();changed();};
 const rr=$("v-rrm");if(rr)rr.onclick=()=>{v.rulesFile=null;redraw();changed();};
 bindAvatar(v,"vav","avatar");bindSocial(v,"v");bindAddr(v.addr,"v",redraw);bindPromo(v.promo,k,redraw);bindUploader(k,"photo",v.photos,redraw);bindNav();}

const blankPkg=()=>({name:"",price:"",per:"persona",min:"",inc:[]});
const polOk=p=>!!p.offer&&!!p.own&&(p.offer!=="costo"||filled(p.price))&&(p.own!=="cuota"||filled(p.fee));
const pkgOk=x=>filled(x.name)&&filled(x.price);
// Cómo ve el cotizador a este venue: precio estándar ¡HQV! (5 h, sábado en la noche, sin servicios extra)
function venueStdRows(v){const cap=+v.seated||0;if(!v.mode||!cap)return`<b>📊 Así te ve el cotizador</b><span class="hint">Cuando llenes capacidad y forma de cobro, aquí verás cuánto le aparece por persona a un anfitrión.</span>`;
 const gs=[...new Set([Math.min(30,cap),Math.round(cap/2),cap].filter(x=>x>0))].sort((a,b)=>a-b);
 const rows=gs.map(g=>{const t=HQV.standardPrice(venueForQuote(v),g);return t?`<div><span>${g} invitados</span><span><b>${money(Math.round(t/g))}</b> por persona <small>(${money(t)})</small></span></div>`:"";}).join("");
 return`<b>📊 Así te ve el cotizador · precio estándar ¡HQV!</b><span class="hint">Para comparar a todos los venues con la misma regla: fiesta de ${HQV.STD.hours} h en sábado por la noche, sin servicios extra.</span><div class="stdrows">${rows||'<span class="hint">Completa tu precio para verlo.</span>'}</div>`;}
// Convierte el formulario (texto) al formato del motor
function venueForQuote(v){const n=x=>HQV.num(x);return{...v,addr:{muni:v.addr.muni},seated:n(v.seated),standing:n(v.standing),hoursIncl:n(v.hoursIncl)||HQV.STD.hours,extraHour:n(v.extraHour),
 rent:{price:n(v.rent.price),per:v.rent.per,upTo:n(v.rent.upTo),perExtraGuest:n(v.rent.perExtraGuest)},packages:v.packages.filter(pkgOk).map(x=>({...x,price:n(x.price),min:n(x.min)})),
 adj:{day:Object.fromEntries(Object.entries(v.adj.day).map(([d,x])=>[d,n(x)])),daytime:n(v.adj.daytime)},days:v.days.length?v.days:HQV.DAYS.map(d=>d[0])};}
