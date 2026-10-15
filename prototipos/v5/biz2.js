/* ===== v24 · Mi negocio en 4 bloques (Diego, 15 oct 2026) =====
   1. Tu negocio (público): nombre, logo, redes, WhatsApp y correo del negocio, año en que empezó, dirección,
      ¿atiendes clientes en tu negocio? → consumo en el lugar / punto de retiro / citas y degustaciones + horario, qué mostrar.
   2. Bio. 3. Tu perfil personal (privado salvo nombre y foto): nombre, foto, redes, WhatsApp, correo, género, cumpleaños.
   4. ¿Facturas? */
const BZ_MODES=[["consumo","🍽️ Consumo en el lugar"],["retiro","🛍️ Punto de retiro"],["cita","🤝 Citas y degustaciones"]];
/* v25 · clave de país en todo WhatsApp (proveedores con número de otro país) */
const CC=[["MX","🇲🇽","+52"],["US","🇺🇸","+1"],["CA","🇨🇦","+1"],["CO","🇨🇴","+57"],["AR","🇦🇷","+54"],["VE","🇻🇪","+58"],["CU","🇨🇺","+53"],["ES","🇪🇸","+34"],["PE","🇵🇪","+51"],["CL","🇨🇱","+56"],["GT","🇬🇹","+502"],["SV","🇸🇻","+503"],["HN","🇭🇳","+504"],["DO","🇩🇴","+1"],["EC","🇪🇨","+593"],["BR","🇧🇷","+55"],["UY","🇺🇾","+598"],["GB","🇬🇧","+44"],["FR","🇫🇷","+33"],["IT","🇮🇹","+39"],["DE","🇩🇪","+49"]];
const ccDial=c=>(CC.find(x=>x[0]===c)||CC[0])[2];
const waOk=(c,n)=>{const d=String(n||"").replace(/\D/g,"");return(c||"MX")==="MX"?d.length===10:d.length>=6&&d.length<=14;};
const waIntl=(c,n)=>ccDial(c).replace("+","")+String(n||"").replace(/\D/g,"");
const waShow=(c,n)=>n?ccDial(c)+" "+n:"";
function telHtml(id,cc,val,cls,ph){return`<div class="tel${cls||""}"><select id="${id}-cc" aria-label="Clave de país">${CC.map(([c,f,d])=>`<option value="${c}" ${c===(cc||"MX")?"selected":""}>${f} ${d}</option>`).join("")}</select><input type="tel" id="${id}" autocomplete="tel-national" value="${esc(val)}" placeholder="${ph||((cc||"MX")==="MX"?"55 1234 5678":"Número")}"></div>`;}
const BZ_GEN=[["Mujer","Mujer"],["Hombre","Hombre"],["Otro","Otro"],["Prefiero no decir","Prefiero no decir"]];
function bzDefaults(){const b=S.biz;if(b.attends===undefined)b.attends=b.visits===true?true:b.visits===false?false:null;if(!b.modes)b.modes=b.visits?["cita"]:[];if(!b.hDays)b.hDays=[];if(b.hSame===undefined)b.hSame=true;if(!b.hBy)b.hBy={};if(b.hOpen===undefined)b.hOpen="";if(b.hClose===undefined)b.hClose="";
 if(!S.me)S.me={photo:"",instagram:"",tiktok:"",facebook:"",links:[],whatsapp:"",email:"",gender:"",genderOther:"",birthday:"",pub:{social:false}};
 if(!b.waCC)b.waCC="MX";const me=S.me;if(!me.waCC)me.waCC="MX";if(!me.links)me.links=[];
 /* v25 · tu perfil personal se llena con los datos del negocio; solo cambias lo que sea distinto */
 if(!me.same)me.same={wa:!me.whatsapp||me.whatsapp===b.whatsapp,email:!me.email||me.email===S.account.email,social:!(me.instagram||me.tiktok||me.facebook||me.links.length)};bzMirror();}
function bzMirror(){const b=S.biz,me=S.me;if(!me||!me.same)return;if(me.same.wa){me.whatsapp=b.whatsapp;me.waCC=b.waCC;}if(me.same.email)me.email=S.account.email;
 if(me.same.social){me.instagram=b.instagram;me.tiktok=b.tiktok;me.facebook=b.facebook;me.links=JSON.parse(JSON.stringify(b.links||[]));}}
const bzSame=(k,on)=>on?`<span class="bz-same">🔗 Igual que tu negocio · cámbialo solo si es distinto</span>`:`<button type="button" class="link bz-reuse" data-k="${k}">↺ Usar el de tu negocio</button>`;
/* v26 · horario de atención: mismo todos los días o por día (igual que en el venue) */
const bzDayT=d=>HQV.DAYS.find(x=>x[0]===d)[1];
const bzHoursOk=b=>b.hDays.length>0&&(b.hSame!==false?filled(b.hOpen)&&filled(b.hClose):b.hDays.every(d=>b.hBy[d]&&filled(b.hBy[d].o)&&filled(b.hBy[d].c)));
const bzHours=b=>{if(!b.attends||!bzHoursOk(b))return"";if(b.hSame!==false)return`${b.hDays.map(bzDayT).join(" ")} · ${b.hOpen} a ${b.hClose}`;return b.hDays.map(d=>`${bzDayT(d)} ${b.hBy[d].o} a ${b.hBy[d].c}`).join(" · ");};
function drawBiz(){bzDefaults();const b=S.biz,me=S.me,yrs=[];for(let y=yearNow;y>=1960;y--)yrs.push(y);
 $("stepBody").innerHTML=`<div class="panel"><h2>Mi negocio 🏷️</h2><p class="sub">Primero tu negocio, que es lo que ven tus clientes. Después, tú.</p>
 <section class="bz-sec"><div class="bz-h"><b>1</b><span><strong>Tu negocio</strong><small>Todo esto se publica en tu sitio.</small></span></div>
 <div class="field"><label class="lbl" for="f-name">Nombre de tu negocio</label><input type="text" id="f-name" class="${MISS(filled(b.name))}" value="${esc(b.name)}" placeholder="Así te conocen tus clientes"></div>
 ${avatarHtml(b,"biz","avatar","🖼️ Logo o foto del negocio")}
 ${socialHtml(b,"biz")}
 <div class="row bz-row"><div class="field"><label class="lbl" for="f-wa">📱 WhatsApp del negocio</label>${telHtml("f-wa",b.waCC,b.whatsapp,MISS(waOk(b.waCC,b.whatsapp)))}${b.waCC!=="MX"?`<span class="hint">Tus clientes te escribirán al ${esc(ccDial(b.waCC))}.</span>`:""}</div>
  <div class="field"><label class="lbl" for="f-email">✉️ Correo del negocio</label><input type="email" id="f-email" autocomplete="email" class="${MISS(EMAIL_OK(S.account.email))}" value="${esc(S.account.email)}" placeholder="hola@tunegocio.com"></div></div>
 <div class="field"><label class="lbl" for="f-found">🎉 Fecha de fundación de tu negocio</label><input type="date" id="f-found" class="${MISS(!!b.founded)}" value="${esc(b.founded||"")}" max="${new Date().toISOString().slice(0,10)}" style="width:fit-content"><span class="hint">Con ella celebramos tu aniversario con promociones.</span></div>
 ${addrHtml(b.addr,"biz","Dirección de tu negocio")}
 <div class="field"><span class="lbl">🏪 ¿Atiendes clientes en tu negocio?</span><div class="${MISS(b.attends!==null)}" style="width:fit-content;border-radius:99px">${ynHtml("bat",b.attends)}</div>
  ${b.attends?`<div class="sub-box bz-att"><span class="lbl" style="font-size:14px">¿Para qué van? <span class="opt">elige uno o varios</span></span>
   <div class="chips${MISS(b.modes.length>0)}">${BZ_MODES.map(([v,t])=>`<button type="button" class="chip bz-m" data-v="${v}" aria-pressed="${b.modes.includes(v)}">${TICK}${t}</button>`).join("")}</div>
   <span class="lbl" style="font-size:14px">🕒 Horario de atención</span>
   <div class="chips cmini${MISS(b.hDays.length>0)}">${HQV.DAYS.map(([d,t])=>`<button type="button" class="chip bz-d" data-d="${d}" aria-pressed="${b.hDays.includes(d)}">${TICK}${t}</button>`).join("")}</div>
   <div class="chips" style="width:fit-content;border-radius:99px"><button type="button" class="chip bz-sh" data-v="1" aria-pressed="${b.hSame!==false}">${TICK}Mismo horario todos los días</button><button type="button" class="chip bz-sh" data-v="0" aria-pressed="${b.hSame===false}">${TICK}Horario por día</button></div>
   ${b.hSame!==false?`<div class="row bz-hr"><label class="field"><span class="hint">Abre</span><input type="time" id="bzO" class="${MISS(filled(b.hOpen))}" value="${esc(b.hOpen)}"></label><label class="field"><span class="hint">Cierra</span><input type="time" id="bzC" class="${MISS(filled(b.hClose))}" value="${esc(b.hClose)}"></label></div>`
    :`<div class="hrs">${b.hDays.map(d=>{const h=b.hBy[d]||(b.hBy[d]={o:b.hOpen,c:b.hClose});return`<div class="hr bz-hd" data-d="${d}"><b>${bzDayT(d)}</b><input type="time" class="bz-ho${MISS(filled(h.o))}" value="${esc(h.o||"")}" aria-label="Abre, ${bzDayT(d)}"><input type="time" class="bz-hc${MISS(filled(h.c))}" value="${esc(h.c||"")}" aria-label="Cierra, ${bzDayT(d)}"></div>`;}).join("")||'<span class="hint">Primero elige los días.</span>'}</div>`}</div>`:""}</div>
 <div class="field"><span class="lbl">👀 ¿Qué mostrar de tu dirección en tu sitio?</span><div class="chips${MISS(!!b.showAddr)}" style="width:fit-content;border-radius:99px">${[["colonia","Solo colonia y municipio"],["full","Dirección completa"]].map(([v,t])=>`<button type="button" class="chip sa" data-v="${v}" aria-pressed="${b.showAddr===v}">${TICK}${t}</button>`).join("")}</div></div></section>
 <section class="bz-sec"><div class="bz-h"><b>2</b><span><strong>Tu bio</strong><small>Lo primero que leen en tu sitio.</small></span></div>
 <div class="field"><label class="lbl" for="f-about">💬 Cuéntales quién eres y qué haces</label><textarea id="f-about" class="${MISS(filled(b.about))}" placeholder="Mesas de dulces que se roban la fiesta 🍭">${esc(b.about)}</textarea></div></section>
 <section class="bz-sec"><div class="bz-h"><b>3</b><span><strong>Tu perfil personal</strong><small>🔒 Privado. Solo publicamos tu nombre y tu foto como responsable del negocio.</small></span></div>
 <div class="field"><label class="lbl" for="f-owner">Tu nombre</label><input type="text" id="f-owner" autocomplete="name" class="${MISS(filled(b.owner||""))}" value="${esc(b.owner||"")}" placeholder="Quien atiende a los clientes"></div>
 ${avatarHtml(me,"me","face","🙂 Tu foto <span class=\"opt\">(opcional)</span>")}
 ${socialHtml(me,"me","Tus redes personales; no se publican.")}<div style="margin-top:-12px">${bzSame("social",me.same.social)}</div>
 <div class="row bz-row"><div class="field"><label class="lbl" for="me-wa">📱 Tu WhatsApp</label>${telHtml("me-wa",me.waCC,me.whatsapp,"","Tu número")}${bzSame("wa",me.same.wa)}</div>
  <div class="field"><label class="lbl" for="me-em">✉️ Tu correo</label><input type="email" id="me-em" value="${esc(me.email)}" placeholder="tucorreo@gmail.com">${bzSame("email",me.same.email)}</div></div>
 <div class="field"><span class="lbl">Género <span class="opt">(opcional)</span></span><div class="chips">${BZ_GEN.map(([v,t])=>`<button type="button" class="chip bz-g" data-v="${v}" aria-pressed="${me.gender===v}">${TICK}${t}</button>`).join("")}</div>
  ${me.gender==="Otro"?`<input type="text" id="me-go" value="${esc(me.genderOther)}" placeholder="¿Cómo te identificas? (opcional)" style="max-width:360px">`:""}</div>
 <div class="field"><label class="lbl" for="me-bd">🎂 Tu cumpleaños <span class="opt">(opcional)</span></label><input type="date" id="me-bd" value="${esc(me.birthday)}" style="width:fit-content"></div>
 <p class="bz-priv">🔒 Tus datos personales no se publican. Los usamos para conocer mejor a la comunidad de proveedores (por ejemplo, cuántas mujeres y hombres emprenden en fiestas) y para felicitarte en tu cumpleaños. Consulta el <b>Aviso de privacidad</b> <span class="opt">(próximamente)</span>.</p></section>
 <section class="bz-sec"><div class="bz-h"><b>4</b><span><strong>Facturas</strong></span></div>
 <div class="field"><span class="lbl">🧾 ¿Facturas?</span><div class="chips${MISS(!!b.invoice)}" style="width:fit-content;border-radius:99px">${[["si","Sí facturo"],["no","No facturo"]].map(([v,t])=>`<button type="button" class="chip inv" data-v="${v}" aria-pressed="${b.invoice===v}">${TICK}${t}</button>`).join("")}</div></div></section>
 ${navHtml()}</div>`;
 const mir=()=>{bzMirror();if(me.same.wa){$("me-wa").value=me.whatsapp;$("me-wa-cc").value=me.waCC;}if(me.same.email)$("me-em").value=me.email;if(me.same.social)[["ig-me","instagram"],["tt-me","tiktok"],["fb-me","facebook"]].forEach(([i,k])=>{const x=$(i);if(x)x.value=me[k]||"";});};
 [["f-name","name"],["f-wa","whatsapp"],["f-about","about"],["f-owner","owner"]].forEach(([i,k])=>{$(i).oninput=$(i).onchange=e=>{b[k]=e.target.value;mir();if(typeof plSync==="function")plSync();changed();};});
 $("f-found").oninput=$("f-found").onchange=e=>{b.founded=e.target.value;b.since=b.founded?b.founded.slice(0,4):"";if(typeof plSync==="function")plSync();changed();};
 $("f-wa-cc").onchange=e=>{b.waCC=e.target.value;bzMirror();keep(drawBiz);changed();};
 $("f-email").oninput=e=>{S.account.email=e.target.value.trim();mir();changed();};
 [["me-wa","whatsapp","wa"],["me-em","email","email"],["me-bd","birthday"]].forEach(([i,k,f])=>{$(i).oninput=$(i).onchange=e=>{me[k]=e.target.value;if(f&&me.same[f]){me.same[f]=false;keep(drawBiz);const x=$(i);x.focus();x.setSelectionRange&&x.type!=="email"&&x.setSelectionRange(x.value.length,x.value.length);}changed();};});
 $("me-wa-cc").onchange=e=>{me.waCC=e.target.value;me.same.wa=false;keep(drawBiz);changed();};
 document.querySelectorAll(".bz-reuse").forEach(x=>x.onclick=()=>{me.same[x.dataset.k]=true;bzMirror();keep(drawBiz);changed();});
 const go=$("me-go");if(go)go.oninput=e=>{me.genderOther=e.target.value;changed();};
 document.querySelectorAll(".bz-g").forEach(c=>c.onclick=()=>{me.gender=me.gender===c.dataset.v?"":c.dataset.v;keep(drawBiz);changed();});
 document.querySelectorAll(".inv").forEach(c=>c.onclick=()=>{b.invoice=c.dataset.v;document.querySelectorAll(".inv").forEach(x=>x.setAttribute("aria-pressed",x===c));changed();});
 document.querySelectorAll(".sa").forEach(c=>c.onclick=()=>{b.showAddr=c.dataset.v;document.querySelectorAll(".sa").forEach(x=>x.setAttribute("aria-pressed",x===c));changed();});
 document.querySelectorAll(".bz-m").forEach(c=>c.onclick=()=>{const v=c.dataset.v;b.modes=b.modes.includes(v)?b.modes.filter(x=>x!==v):[...b.modes,v];c.setAttribute("aria-pressed",b.modes.includes(v));changed();});
 document.querySelectorAll(".bz-d").forEach(c=>c.onclick=()=>{const d=c.dataset.d;b.hDays=b.hDays.includes(d)?b.hDays.filter(x=>x!==d):HQV.DAYS.map(x=>x[0]).filter(x=>x===d||b.hDays.includes(x));if(b.hSame===false)keep(drawBiz);else c.setAttribute("aria-pressed",b.hDays.includes(d));changed();});
 const o=$("bzO"),c2=$("bzC");if(o)o.oninput=e=>{b.hOpen=e.target.value;changed();};if(c2)c2.oninput=e=>{b.hClose=e.target.value;changed();};
 document.querySelectorAll(".bz-sh").forEach(c=>c.onclick=()=>{b.hSame=c.dataset.v==="1";keep(drawBiz);changed();});
 document.querySelectorAll(".bz-hd").forEach(r=>{const h=b.hBy[r.dataset.d];r.querySelector(".bz-ho").oninput=e=>{h.o=e.target.value;changed();};r.querySelector(".bz-hc").oninput=e=>{h.c=e.target.value;changed();};});
 bindAvatar(b,"biz","avatar");bindAvatar(me,"me","face");bindSocial(b,"biz",()=>{bzMirror();keep(drawBiz);},()=>mir());bindSocial(me,"me",()=>keep(drawBiz),()=>{if(me.same.social){me.same.social=false;}});bindYN("bat",x=>{b.attends=x;b.visits=x;keep(drawBiz);changed();});bindAddr(b.addr,"biz",()=>keep(drawBiz));bindNav();}
function keep(f){const y=scrollY;f();scrollTo({top:y,behavior:"instant"});}
