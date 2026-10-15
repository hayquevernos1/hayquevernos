"""v28 · svc7_v27.js → svc7.js
- Paquetes: se desbloquean con 2 productos distintos; animación también en la tarjeta «2 · Tus paquetes».
- «Opciones de platillos por tiempos»; transporte sin monto; vista del anfitrión por persona arriba.
- Venue: «¿Cuáles no pueden traer?» predictivo con las categorías del anfitrión.
- Planner invitado: termina su perfil y tarifas ya dentro de su cuenta; opción de usar la bio y redes del negocio.
- Tu planner: bio y fecha de fundación ligadas a Mi negocio.
- Conexión con el anfitrión: categorías unidas (RU_HOSTCAT), datos de publicación actualizados (ruPayload) y oferta cotizable."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'svc7_v27.js').read_text()


def rep(a, b, c=1):
    global s
    assert s.count(a) == c, ('NO/MULTI', a[:110], s.count(a))
    s = s.replace(a, b)


# ---------- paquetes: desbloqueo y animación ----------
rep(' const lock=nRef<2;', ' const lock=P.length<2;')
rep('🔒 Se desbloquea cuando tengas 2 productos. ${nRef?"Te falta 1.":"Te faltan 2."}', '🔒 Se desbloquea cuando tengas 2 productos. ${P.length?"Te falta 1.":"Te faltan 2."}')
rep('document.querySelectorAll(".ru-step2").forEach(x=>x.classList.toggle("on",!lock));',
    'document.querySelectorAll(".ru-step2").forEach(x=>{x.classList.toggle("on",!lock);x.classList.toggle("locked",lock);x.onclick=()=>{if(x.classList.contains("locked"))ruLockPop(x);else{const k=$("ruPkSec");k&&k.scrollIntoView({behavior:RU_RM?"auto":"smooth",block:"start"});}};});')
# ---------- textos ----------
rep('🍴 Platillos por tiempo <span class="opt">escribe y te sugerimos</span>', '🍴 Opciones de platillos por tiempos <span class="opt">escribe y te sugerimos</span>')
rep('${pill("ride",L.ride,"🚕 Transporte de regreso lo cubre el anfitrión",`<label class="ru-pin">$<input type="number" min="0" class="ru-p-fee" value="${esc(L.rideFee)}" placeholder="0" aria-label="Transporte por persona">c/u</label>`)}',
    '${pill("ride",L.ride,"🚕 Transporte de regreso lo cubre el anfitrión")}')
rep('pol.ride&&e<=s?`🚕 El transporte de regreso lo cubre el anfitrión${+pol.rideFee>0?` (${money(pol.rideFee)} por persona)`:""}`', 'pol.ride&&e<=s?"🚕 El transporte de regreso del staff lo cubre el anfitrión"')
# vista del anfitrión: por persona arriba, total abajo
rep('<span class="ru-tot">${ruMoney(r.tot)}</span><small class="ru-ppx">total del evento · <b>${ruMoney(r.pp)}</b> por persona</small></div>`:"";}).filter(Boolean);',
    '<span class="ru-tot">${ruMoney(r.pp)} <small>por persona</small></span><small class="ru-ppx"><b>${ruMoney(r.tot)}</b> total del evento</small></div>`:"";}).filter(Boolean);')
# ---------- venue: proveedores que no pueden entrar ----------
rep('''${v.extAll==="algunos"?`<input type="text" id="v-extn" value="${esc(v.extAllNote)}" placeholder="¿Cuáles sí y cuáles no?" aria-label="Cuáles servicios externos">`:""}</div>''',
    '''${v.extAll==="algunos"?`<span class="ru-sl">🚫 ¿Cuáles no pueden traer?</span>${ruTags("extNo",v.extNo||(v.extNo=[]),"Ej. alimentos, bebidas y barra")}<span class="hint ru-comma">Sepáralos con coma o Enter.</span>`:""}</div>''')
rep('function vnBind(v){vnBindRows(v);vnBindPk(v);',
    'const HOST_CATS=()=>(window.HQV_SVC?HQV_SVC.cats.map(c=>c.n):[]).filter(n=>n!=="Espacios y hospedaje");\nfunction vnBind(v){vnBindRows(v);vnBindPk(v);const sv=$("vnSvc");if(sv)ruBindTags(sv,"extNo",v.extNo||(v.extNo=[]),HOST_CATS,x=>{const m=HOST_CATS().find(c=>nrm(c)===nrm(x))||x;if(!v.extNo.some(y=>nrm(y)===nrm(m)))v.extNo.push(m);},()=>{changed();const y=scrollY;drawVenue();scrollTo({top:y,behavior:"instant"});const i=document.querySelector(\'#vnSvc .ru-tags[data-t="extNo"] input\');i&&i.focus({preventScroll:true});});')
# ---------- planner invitado: su perfil en su cuenta ----------
rep('i.name=$("iaN").value.trim()||i.name;md.remove();ruInviteeFees(i);};}', 'i.name=$("iaN").value.trim()||i.name;md.remove();ruInviteeProfile(i);};}')
s += r'''
/* ===== v28 · la persona invitada termina su perfil ya dentro de su cuenta ===== */
function ruInviteeProfile(i){const b=S.biz,F=i.fees&&i.fees.length?i.fees:[];const fx=F.find(f=>f.unit==="evento")||{},pc=F.find(f=>f.unit==="porcentaje")||{};i.prof=i.prof||{bio:"",instagram:"",tiktok:"",facebook:"",useBiz:false};const P=i.prof;
 const md=ruModal(`<span class="ru-embk">✅ CUENTA CREADA · ${esc(i.name.toUpperCase())}</span><h2>Tu perfil de event planner</h2><span>Ya estás dentro de tu cuenta. Pusimos tus datos; revisa y agrega tus tarifas. Tu perfil queda ligado a «${esc(b.name||"su negocio")}».</span>
  <div class="ru-invf"><div class="ru-invp"><span class="ru-invav">🙂</span><span><b>${esc(i.name)}</b><small>${esc([i.wa?waShow(i.waCC,i.wa):"",i.email].filter(Boolean).join(" · "))}</small><small>🧭 Event planner de ${esc(b.name||"su negocio")}</small></span></div>
  <button type="button" class="btn ghost sm" id="ipBiz">${P.useBiz?"✓ Usando la bio y redes del negocio":"Usar la bio y redes de «"+esc(b.name||"el negocio")+"»"}</button>
  <textarea id="ipBio" rows="3" placeholder="Tu bio: cuéntales quién eres y cómo trabajas">${esc(P.bio)}</textarea><input type="text" id="ipIg" value="${esc(P.instagram)}" placeholder="📸 Tu Instagram (opcional)">
  <b>💲 ¿Cómo cobras por coordinar?</b><span class="hint" style="color:rgba(255,255,255,.85)!important">Llena una o las dos. El anfitrión ve la que más le conviene.</span>
  <label class="ru-invr"><span>Precio fijo por evento</span><span class="ru-fi"><i>$</i><input type="number" min="0" id="ifA" value="${esc(fx.amount||"")}" placeholder="0"></span></label>
  <label class="ru-invr"><span>Porcentaje del total del evento</span><span class="ru-fi"><input type="number" min="0" max="100" id="ifP" value="${esc(pc.amount||"")}" placeholder="10"><i>%</i></span></label>
  <label class="ru-invr"><span>Mínimo si cobras por porcentaje <small>(opcional)</small></span><span class="ru-fi"><i>$</i><input type="number" min="0" id="ifM" value="${esc(pc.min||"")}" placeholder="0"></span></label>
  <span class="err" id="ifErr" hidden></span><button type="button" class="btn cta" id="ifGo">Guardar mi perfil</button></div>`,"ru-inv");
 $("ipBiz").onclick=()=>{P.useBiz=!P.useBiz;if(P.useBiz){P.bio=b.about||"";P.instagram=b.instagram||"";P.tiktok=b.tiktok||"";P.facebook=b.facebook||"";}$("ipBio").value=P.bio;$("ipIg").value=P.instagram;$("ipBiz").textContent=P.useBiz?"✓ Usando la bio y redes del negocio":"Usar la bio y redes de «"+(b.name||"el negocio")+"»";};
 $("ipBio").oninput=e=>{P.bio=e.target.value;};$("ipIg").oninput=e=>{P.instagram=e.target.value;};
 $("ifGo").onclick=()=>{const a=$("ifA").value,p=$("ifP").value,m=$("ifM").value;if(!(+a>0)&&!(+p>0)){const e=$("ifErr");e.hidden=false;e.textContent="Pon al menos una forma de cobrar.";$("ifA").focus();return;}
  i.fees=[+a>0?{amount:a,unit:"evento",min:""}:null,+p>0?{amount:p,unit:"porcentaje",min:m}:null].filter(Boolean);i.status="aceptada";md.remove();ruDrawLists();changed();ruConfetti(90);ruToast(`🧭 ${i.name} aceptó: ya puedes sumarle a tus paquetes.`);};}
/* ===== v28 · tu planner: bio y fecha de fundación ligadas a «Mi negocio» ===== */
function plSync(){const p=S.planner,b=S.biz;if(!p)return;if(p.bioLink!==false){p.bio=b.about||p.bio||"";if(!b.about&&p.bio)b.about=p.bio;}if(b.founded){p.founded=b.founded;p.since=b.founded.slice(0,4);}}
/* ===== v28 · conexión con el anfitrión ===== */
/* las categorías del proveedor (22) se unen con las del cotizador del anfitrión (19) */
const RU_HOSTCAT={"Catering":"Alimentos","Música":"Música y espectáculos","Entretenimiento y shows":"Música y espectáculos","Infraestructura":"Estructuras e infraestructura","Mobiliario y montaje":"Mobiliario y equipo de banquete","Cristalería y cubertería":"Mobiliario y equipo de banquete","Audio, iluminación, foto y video":"Audio, video e iluminación","Tecnología":"Tecnología y registro","Registro y protocolo":"Tecnología y registro","Decoración y ambientación":"Decoración y flores","Marketing y comunicación":"Servicios profesionales y efectos","Exposición y negocios":"Servicios profesionales y efectos","Permisos y trámites":"Servicios profesionales y efectos","Transporte":"Transporte y logística","Hospedaje":"Espacios y hospedaje","Maquillaje y estilismo":"Imagen personal y ceremonias","Vestuario y accesorios":"Imagen personal y ceremonias","Souvenirs y regalos":"Diseño, impresión y regalos","Impresión y producción gráfica":"Diseño, impresión y regalos","Seguridad, salud y protección civil":"Seguridad, salud y accesibilidad","Actividades y experiencias":"Experiencias y actividades","Sustentabilidad y limpieza":"Limpieza y sostenibilidad"};
function ruHostCat(p){if(p.kind==="staff"||p.dims[1]==="Personal independiente")return"Personal";const [a,b]=p.dims;
 if(a==="Catering"){if(b==="Bebidas")return"Bebidas y barra";if(b==="Renta de equipo de cocina")return"Mobiliario y equipo de banquete";return"Alimentos";}
 if(a==="Audio, iluminación, foto y video"&&/Fotograf|Video|Cabinas|Postprod|Producción audiovisual|Streaming/.test(b))return"Fotografía y contenido";return RU_HOSTCAT[a]||a;}
/* lo que se envía al publicar (contrato con producción) */
function ruPayload(){ruDefaults();const v=S.venue||{},tar=t=>({precio:+t.p||0,unidad:t.u||null,cantidad:+t.q||null}),st=r=>({perfil:r.n,cantidad:+r.q||1,tarifas:(r.tars||[]).map(t=>({precio:+t.p||0,unidad:t.u})),extra:{precio:+r.xh||0,unidad:r.xu||null}});
 const prods=(S.rprods||[]).filter(p=>p.kind==="prod"),staff=(S.rprods||[]).filter(p=>p.kind==="staff");
 return{productos:prods.map(p=>({id:p.id,categoria:p.dims[0],servicio:p.dims[1],formato:p.dims[2],detalle:p.dims[3],detalleOtro:p.otro||null,categoriaAnfitrion:ruHostCat(p),nombre:p.name,personas:+p.pax,
   tiempos:ruTimed(p)?p.courses.map(c=>({tiempo:c.n,platillos:c.d})):null,platillos:ruDishes(p),incluye:p.ins,precioServicio:tar(p.tar.i),
   formas:p.tw.map(w=>({forma:w==="full"?"con_staff":"sin_staff",staff:w==="full"?p.labor.map(st):null,politicasStaff:w==="full"?p.lpol:null,entregas:w==="rent"?p.dlx.dl:null,totalEjemplo:(ruTotal(p,w)||{}).tot||null})),
   cobertura:p.cov.same?"zona_general":p.cov.zones,extras:p.ext,minimo:p.min,promo:p.promo,fotos:p.photos.length,emblema:p.emb||null})),
  staff:staff.map(p=>({id:p.id,categoria:p.dims[0],categoriaAnfitrion:"Personal",...st(p.labor[0]),politicas:p.lpol,cobertura:p.cov.same?"zona_general":p.cov.zones})),
  paquetesRuleta:(S.rpkgs||[]).map(p=>({id:p.id,nombre:p.name,piezas:p.items.map(r=>({ref:r,nombre:ruItemName(r,p),cantidad:+(p.qty&&p.qty[r])||1})),incluye:p.ins,personas:+p.pax,precio:tar(p.tar.full),sumaDePiezas:Math.round(ruSug(p)),minimo:p.min,promo:p.promo})),
  venueServicios:S.types.venue?{ofrece:Object.entries(v.svcIn||{}).map(([ref,e])=>({ref,ofrece:e.on!==false,precioEnVenue:+e.p||null})),proveedoresExternos:v.extAll||null,noPermitidos:v.extAll==="algunos"?(v.extNo||[]):[]}:null,
  plannersInvitados:(S.invites||[]).map(i=>({nombre:i.name,whatsapp:i.wa?waIntl(i.waCC,i.wa):null,correo:i.email||null,estado:i.status,tarifas:i.status==="aceptada"?i.fees:null})),
  oferta:ruOferta()};}
/* versión cotizable para el lado del anfitrión: el cotizador calcula con los invitados y el horario de cada fiesta */
function ruOferta(){const out=[],v=S.venue||{};
 (S.rprods||[]).filter(p=>ruOk(p)).forEach(p=>{if(p.kind==="staff"){const r=p.labor[0];out.push({tipo:"staff",cat:"Personal",nombre:p.name,tars:r.tars,xh:+r.xh||0,xu:r.xu,pol:p.lpol});return;}
  out.push({tipo:"servicio",cat:ruHostCat(p),nombre:p.name,pax:+p.pax,ins:{p:+p.tar.i.p,u:p.tar.i.u,q:+p.tar.i.q||0},fixed:RU_FIXED.includes(p.tar.i.u),formas:p.tw,staff:p.tw.includes("full")?p.labor.map(r=>({n:r.n,q:+r.q||1,tars:r.tars,xh:+r.xh||0,xu:r.xu})):[],pol:p.lpol});});
 const vi=ruVenueItem();if(vi&&v.rent&&+v.rent.price>0)out.push({tipo:"venue",cat:"Venue",nombre:v.name,rent:{precio:+v.rent.price,per:v.rent.per,upTo:+v.rent.upTo||0,extra:+v.rent.perExtraGuest||0,horas:+v.hoursIncl||5},cap:+v.seated||0});
 ruPlanners().forEach(x=>out.push({tipo:"planner",cat:"Planner",nombre:x.who,fees:x.fees,yo:!!x.me,bio:x.me?(S.planner.bio||""):""}));return out;}
'''
# tu planner arrastra bio y fecha
rep('if(!p.since&&b.founded)p.since=b.founded.slice(0,4);', 'plSync();')
(V / 'svc7.js').write_text(s)
print('ok v28 svc')
