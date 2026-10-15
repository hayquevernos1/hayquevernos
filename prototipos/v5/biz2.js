/* ===== v24 · Mi negocio en 4 bloques (Diego, 15 oct 2026) =====
   1. Tu negocio (público): nombre, logo, redes, WhatsApp y correo del negocio, año en que empezó, dirección,
      ¿atiendes clientes en tu negocio? → consumo en el lugar / punto de retiro / citas y degustaciones + horario, qué mostrar.
   2. Bio. 3. Tu perfil personal (privado salvo nombre y foto): nombre, foto, redes, WhatsApp, correo, género, cumpleaños.
   4. ¿Facturas? */
const BZ_MODES=[["consumo","🍽️ Consumo en el lugar"],["retiro","🛍️ Punto de retiro"],["cita","🤝 Citas y degustaciones"]];
const BZ_GEN=[["Mujer","Mujer"],["Hombre","Hombre"],["Otro","Otro"],["Prefiero no decir","Prefiero no decir"]];
function bzDefaults(){const b=S.biz;if(b.attends===undefined)b.attends=b.visits===true?true:b.visits===false?false:null;if(!b.modes)b.modes=b.visits?["cita"]:[];if(!b.hDays)b.hDays=[];if(b.hOpen===undefined)b.hOpen="";if(b.hClose===undefined)b.hClose="";
 if(!S.me)S.me={photo:"",instagram:"",tiktok:"",facebook:"",links:[],whatsapp:"",email:"",gender:"",genderOther:"",birthday:"",pub:{social:false}};}
const bzHours=b=>b.attends&&b.hDays.length&&b.hOpen&&b.hClose?`${b.hDays.map(d=>HQV.DAYS.find(x=>x[0]===d)[1]).join(" ")} · ${b.hOpen} a ${b.hClose}`:"";
function drawBiz(){bzDefaults();const b=S.biz,me=S.me,yrs=[];for(let y=yearNow;y>=1960;y--)yrs.push(y);
 $("stepBody").innerHTML=`<div class="panel"><h2>Mi negocio 🏷️</h2><p class="sub">Primero tu negocio, que es lo que ven tus clientes. Después, tú.</p>
 <section class="bz-sec"><div class="bz-h"><b>1</b><span><strong>Tu negocio</strong><small>Todo esto se publica en tu sitio.</small></span></div>
 <div class="field"><label class="lbl" for="f-name">Nombre de tu negocio</label><input type="text" id="f-name" class="${MISS(filled(b.name))}" value="${esc(b.name)}" placeholder="Así te conocen tus clientes"></div>
 ${avatarHtml(b,"biz","avatar","🖼️ Logo o foto del negocio")}
 ${socialHtml(b,"biz")}
 <div class="row"><div class="field"><label class="lbl" for="f-wa">📱 WhatsApp del negocio</label><input type="tel" id="f-wa" class="${MISS(b.whatsapp.replace(/\D/g,"").length===10)}" value="${esc(b.whatsapp)}" placeholder="55 1234 5678"></div>
  <div class="field"><label class="lbl" for="f-email">✉️ Correo del negocio</label><input type="email" id="f-email" autocomplete="email" class="${MISS(EMAIL_OK(S.account.email))}" value="${esc(S.account.email)}" placeholder="hola@tunegocio.com"><span class="hint">Con él creamos tu cuenta.</span></div></div>
 <div class="field"><label class="lbl" for="f-since">🎉 ¿Desde qué año haces fiestas?</label><select id="f-since" class="${MISS(!!b.since)}" style="width:fit-content"><option value="">Elige el año</option>${yrs.map(y=>`<option ${String(y)===String(b.since)?"selected":""}>${y}</option>`).join("")}</select></div>
 ${addrHtml(b.addr,"biz","📍 Dirección de tu negocio")}
 <div class="field"><span class="lbl">🏪 ¿Atiendes clientes en tu negocio?</span><div class="${MISS(b.attends!==null)}" style="width:fit-content;border-radius:99px">${ynHtml("bat",b.attends)}</div>
  ${b.attends?`<div class="sub-box bz-att"><span class="lbl" style="font-size:14px">¿Para qué van? <span class="opt">elige uno o varios</span></span>
   <div class="chips${MISS(b.modes.length>0)}">${BZ_MODES.map(([v,t])=>`<button type="button" class="chip bz-m" data-v="${v}" aria-pressed="${b.modes.includes(v)}">${TICK}${t}</button>`).join("")}</div>
   <span class="lbl" style="font-size:14px">🕒 Horario de atención</span>
   <div class="chips cmini${MISS(b.hDays.length>0)}">${HQV.DAYS.map(([d,t])=>`<button type="button" class="chip bz-d" data-d="${d}" aria-pressed="${b.hDays.includes(d)}">${TICK}${t}</button>`).join("")}</div>
   <div class="row bz-hr"><label class="field"><span class="hint">Abre</span><input type="time" id="bzO" class="${MISS(filled(b.hOpen))}" value="${esc(b.hOpen)}"></label><label class="field"><span class="hint">Cierra</span><input type="time" id="bzC" class="${MISS(filled(b.hClose))}" value="${esc(b.hClose)}"></label></div></div>`:""}</div>
 <div class="field"><span class="lbl">👀 ¿Qué mostrar de tu dirección en tu sitio?</span><div class="chips${MISS(!!b.showAddr)}" style="width:fit-content;border-radius:99px">${[["colonia","Solo colonia y municipio"],["full","Dirección completa"]].map(([v,t])=>`<button type="button" class="chip sa" data-v="${v}" aria-pressed="${b.showAddr===v}">${TICK}${t}</button>`).join("")}</div></div></section>
 <section class="bz-sec"><div class="bz-h"><b>2</b><span><strong>Tu bio</strong><small>Lo primero que leen en tu sitio.</small></span></div>
 <div class="field"><label class="lbl" for="f-about">💬 Cuéntanos en una frase qué haces</label><textarea id="f-about" class="${MISS(filled(b.about))}" placeholder="Mesas de dulces que se roban la fiesta 🍭">${esc(b.about)}</textarea></div></section>
 <section class="bz-sec"><div class="bz-h"><b>3</b><span><strong>Tu perfil personal</strong><small>🔒 Privado. Solo publicamos tu nombre y tu foto como responsable del negocio.</small></span></div>
 <div class="field"><label class="lbl" for="f-owner">Tu nombre</label><input type="text" id="f-owner" autocomplete="name" class="${MISS(filled(b.owner||""))}" value="${esc(b.owner||"")}" placeholder="Quien atiende a los clientes"></div>
 ${avatarHtml(me,"me","face","🙂 Tu foto <span class=\"opt\">(opcional)</span>")}
 ${socialHtml(me,"me","Tus redes personales; no se publican.")}
 <div class="row"><div class="field"><label class="lbl" for="me-wa">📱 Tu WhatsApp <span class="opt">(opcional)</span></label><input type="tel" id="me-wa" value="${esc(me.whatsapp)}" placeholder="Si es distinto al del negocio"></div>
  <div class="field"><label class="lbl" for="me-em">✉️ Tu correo <span class="opt">(opcional)</span></label><input type="email" id="me-em" value="${esc(me.email)}" placeholder="Si es distinto al del negocio"></div></div>
 <div class="field"><span class="lbl">Género <span class="opt">(opcional)</span></span><div class="chips">${BZ_GEN.map(([v,t])=>`<button type="button" class="chip bz-g" data-v="${v}" aria-pressed="${me.gender===v}">${TICK}${t}</button>`).join("")}</div>
  ${me.gender==="Otro"?`<input type="text" id="me-go" value="${esc(me.genderOther)}" placeholder="¿Cómo te identificas? (opcional)" style="max-width:360px">`:""}</div>
 <div class="field"><label class="lbl" for="me-bd">🎂 Tu cumpleaños <span class="opt">(opcional)</span></label><input type="date" id="me-bd" value="${esc(me.birthday)}" style="width:fit-content"></div>
 <p class="bz-priv">🔒 Tus datos personales no se publican. Los usamos para conocer mejor a la comunidad de proveedores (por ejemplo, cuántas mujeres y hombres emprenden en fiestas) y para felicitarte en tu cumpleaños. Consulta el <b>Aviso de privacidad</b> <span class="opt">(próximamente)</span>.</p></section>
 <section class="bz-sec"><div class="bz-h"><b>4</b><span><strong>Facturas</strong></span></div>
 <div class="field"><span class="lbl">🧾 ¿Facturas?</span><div class="chips${MISS(!!b.invoice)}" style="width:fit-content;border-radius:99px">${[["si","Sí facturo"],["no","No facturo"]].map(([v,t])=>`<button type="button" class="chip inv" data-v="${v}" aria-pressed="${b.invoice===v}">${TICK}${t}</button>`).join("")}</div></div></section>
 ${navHtml()}</div>`;
 [["f-name","name"],["f-wa","whatsapp"],["f-about","about"],["f-since","since"],["f-owner","owner"]].forEach(([i,k])=>{$(i).oninput=$(i).onchange=e=>{b[k]=e.target.value;changed();};});
 $("f-email").oninput=e=>{S.account.email=e.target.value.trim();changed();};
 [["me-wa","whatsapp"],["me-em","email"],["me-bd","birthday"]].forEach(([i,k])=>{$(i).oninput=$(i).onchange=e=>{me[k]=e.target.value;changed();};});
 const go=$("me-go");if(go)go.oninput=e=>{me.genderOther=e.target.value;changed();};
 document.querySelectorAll(".bz-g").forEach(c=>c.onclick=()=>{me.gender=me.gender===c.dataset.v?"":c.dataset.v;keep(drawBiz);changed();});
 document.querySelectorAll(".inv").forEach(c=>c.onclick=()=>{b.invoice=c.dataset.v;document.querySelectorAll(".inv").forEach(x=>x.setAttribute("aria-pressed",x===c));changed();});
 document.querySelectorAll(".sa").forEach(c=>c.onclick=()=>{b.showAddr=c.dataset.v;document.querySelectorAll(".sa").forEach(x=>x.setAttribute("aria-pressed",x===c));changed();});
 document.querySelectorAll(".bz-m").forEach(c=>c.onclick=()=>{const v=c.dataset.v;b.modes=b.modes.includes(v)?b.modes.filter(x=>x!==v):[...b.modes,v];c.setAttribute("aria-pressed",b.modes.includes(v));changed();});
 document.querySelectorAll(".bz-d").forEach(c=>c.onclick=()=>{const d=c.dataset.d;b.hDays=b.hDays.includes(d)?b.hDays.filter(x=>x!==d):HQV.DAYS.map(x=>x[0]).filter(x=>x===d||b.hDays.includes(x));c.setAttribute("aria-pressed",b.hDays.includes(d));changed();});
 const o=$("bzO"),c2=$("bzC");if(o)o.oninput=e=>{b.hOpen=e.target.value;changed();};if(c2)c2.oninput=e=>{b.hClose=e.target.value;changed();};
 bindAvatar(b,"biz","avatar");bindAvatar(me,"me","face");bindSocial(b,"biz",()=>keep(drawBiz));bindSocial(me,"me",()=>keep(drawBiz));bindYN("bat",x=>{b.attends=x;b.visits=x;keep(drawBiz);changed();});bindAddr(b.addr,"biz",()=>keep(drawBiz));bindNav();}
function keep(f){const y=scrollY;f();scrollTo({top:y,behavior:"instant"});}
