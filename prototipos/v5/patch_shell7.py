"""v7 · Bloque 1 (inicio): correr DESPUÉS de patch_shell6.py. Edita shell.html en su lugar.
Comentarios de Diego en Miro (8 oct 2026): puertas limpias, botón protagonista, beneficios, zona enfática,
tracker de fundadores, color azul para anfitriones, aviso de beta como popup, sin «Háganmelo ustedes» ni botón de ideas."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:100]
    s = s.replace(a, b, count)


# ---------- color anfitrión: azul eléctrico con letra blanca
rep('--host:var(--hqv-magenta)', '--host:var(--hqv-azul)')
s = s.replace('background:var(--host);color:#14000F', 'background:var(--host);color:#fff')
rep('.door.pv .go{color:#4A13A8}.door.hs .go{color:#7A0063}', '.door.pv .go{background:var(--prov);color:#fff}.door.hs .go{background:var(--host);color:#fff}')
rep('.swt[data-s="hs"] .r{color:#B0008F}', '.swt[data-s="hs"] .r{color:var(--host)}')
s = s.replace('.pill.host{background:var(--host);color:#fff}', '.pill.host{background:var(--host);color:#fff}')
s = s.replace('${fs?"var(--host)":"var(--prov)"};color:${fs?"#14000F":"#fff"}', '${fs?"var(--host)":"var(--prov)"};color:#fff')

# ---------- CSS de las puertas nuevas
CSS = '''
/* v7 · puertas limpias */
.door .top{padding:24px 22px 6px;display:grid;gap:14px}
.door .top h2{max-width:none;font-size:clamp(26px,3vw,34px)}
.door .go{justify-self:stretch;text-align:center;font-size:19px;padding:18px 20px;box-shadow:0 10px 24px rgba(30,20,90,.28),var(--hqv-clay-sm)}
.ben-t{font-size:12px;font-weight:900;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.ben-lead{font-size:15px;line-height:1.4}
.ben-lead b{background:var(--hqv-vainilla);border-radius:6px;padding:0 4px}
.bens{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.bens li{display:flex;gap:10px;font-size:14px;line-height:1.35}
.bens li .em{width:24px;height:24px;flex:none;margin-top:1px}
.bens li b{display:block;font-size:14.5px}
.emph{border-radius:22px;padding:16px 18px;display:grid;gap:4px;color:#fff;box-shadow:var(--hqv-clay)}
.door.pv .emph{background:var(--prov)}.door.hs .emph{background:var(--host)}
.emph strong{font-size:16.5px;line-height:1.3;font-weight:900}
.emph small{font-size:12px;font-weight:800;opacity:.9;letter-spacing:.02em}
.fnd{display:grid;grid-template-columns:56px 1fr;gap:12px;align-items:center;background:var(--paper);border-radius:22px;padding:12px 14px}
.fnd img{width:56px}
.fnd b{font-size:15px}
.fnd .hint{font-size:12px}
.home .hh p{display:none}
@media(max-width:860px){.home:has(#swt[data-s="pv"]) .hh,.home:has(#swt[data-s="hs"]) .hh{display:none}}
.swt{grid-template-columns:1fr 64px 1fr}
.swt .knob{width:46px;height:46px;margin:-23px 0 0 -23px}
.swt[data-s="pv"] .knob{left:calc(50% - 1px)}
.swt[data-s="hs"] .knob{left:calc(50% + 1px)}
.swt[data-s="pv"] .knob img{transform:translateX(-6px) rotate(-14deg)}
.swt[data-s="hs"] .knob img{transform:translateX(6px) rotate(14deg)}
.beta{position:fixed;inset:0;z-index:60;background:rgba(20,10,40,.45);display:grid;place-items:center;padding:16px}
.beta[hidden]{display:none}
.beta .bx{background:var(--card);border-radius:28px;max-width:420px;width:100%;overflow:hidden;box-shadow:var(--hqv-clay)}
.beta .bx .in{padding:18px;display:grid;gap:12px;font-size:14.5px}
.beta .bx .tape{height:12px;background:repeating-linear-gradient(-45deg,#FAFA19 0 12px,#000 12px 24px)}
.hqv-ideas{display:none!important}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# ---------- puertas
a = s.index('<section class="door pv" id="d-pv"')
b = s.index('<div class="seam neutral-seam"')
PV = '''<section class="door pv" id="d-pv" aria-labelledby="hpv">
      <div class="top"><h2 id="hpv">Soy proveedor de fiestas</h2>
        <button class="go" type="button" data-open="negocio">Crear mi sitio web gratis →</button></div>
      <div class="body">
        <span class="ben-t">Beneficios</span>
        <p class="ben-lead" style="margin:0">Crea tu sitio web antes del <b>1º de noviembre de 2026</b>, conviértete en <b>miembro fundador</b> y obtén <b>totalmente gratis</b>:</p>
        <ul class="bens">
          <li><img class="em" src="img/e_globe_showing_americas.webp" alt=""><span><b>Mayor visibilidad</b>Haz que más clientes te encuentren en internet.</span></li>
          <li><img class="em" src="img/e_money_bag.webp" alt=""><span><b>Más oportunidades de venta</b>Muestra tus datos de contacto fácilmente y convierte visitantes en clientes potenciales.</span></li>
          <li><img class="em" src="img/e_sparkles.webp" alt=""><span><b>Imagen profesional</b>Genera confianza, destaca frente a tu competencia y fortalece tu marca.</span></li>
          <li><img class="em" src="img/e_camera_with_flash.webp" alt=""><span><b>Escaparate digital 24/7</b>Exhibe tus servicios, paquetes, fotografías y trabajos anteriores en cualquier momento.</span></li>
          <li><img class="em" src="img/e_rocket.webp" alt=""><span><b>Crecimiento de tu negocio</b>Promociona tus servicios, facilita el contacto y conecta con clientes que están organizando eventos.</span></li>
        </ul>
        <div class="emph"><strong>Y recibe pre-cotizaciones perfectamente calculadas de clientes 100% reales, listos para contratarte, directo en tu WhatsApp.</strong><small>Beneficio exclusivo · Tarifa preferencial</small></div>
        <div class="fnd"><img src="img/b_fundador.webp" alt="Insignia de miembro fundador"><div style="display:grid;gap:6px"><b>Serías el proveedor 38 de 100 de nuestros miembros fundadores</b><div class="bar"><i style="width:37%"></i></div><span class="hint">Lugares de ejemplo</span></div></div>
        <div class="kinds"><span class="lab">Diseñado para</span><div class="ks"><span class="k"><img class="em" src="img/e_balloon.webp" alt="">Proveedores de servicios</span><span class="k"><img class="em" src="img/e_house.webp" alt="">Venues</span><span class="k"><img class="em" src="img/e_magic_wand.webp" alt="">Event planners</span></div>
          <div class="ks"><span class="k"><img class="em" src="img/e_birthday_cake.webp" alt="">Eventos sociales</span><span class="k"><img class="em" src="img/e_briefcase.webp" alt="">Eventos corporativos</span></div></div>
      </div>
    </section>
    '''
s = s[:a] + PV + s[b:]
a = s.index('<section class="door hs" id="d-hs"')
b = s.index('</section>', a) + len('</section>')
HS = '''<section class="door hs" id="d-hs" aria-labelledby="hhs">
      <div class="top"><h2 id="hhs">Soy anfitrión de una fiesta</h2>
        <button class="go" type="button" data-open="fiestas">Pre-cotizar mi evento gratis →</button></div>
      <div class="body">
        <span class="ben-t">Beneficios</span>
        <p class="ben-lead" style="margin:0">Calcula el costo de tu evento a partir del <b>1º de noviembre de 2026</b>, conviértete en <b>miembro fundador</b> y obtén <b>totalmente gratis</b>:</p>
        <ul class="bens">
          <li><img class="em" src="img/e_money_bag.webp" alt=""><span><b>Presupuesto en minutos</b>Descubre cuánto podría costar tu evento de forma rápida, sencilla y gratuita.</span></li>
          <li><img class="em" src="img/e_bar_chart.webp" alt=""><span><b>Precios reales, estimaciones confiables</b>Obtén un cálculo basado en el promedio de precios publicados por proveedores reales.</span></li>
          <li><img class="em" src="img/e_stopwatch.webp" alt=""><span><b>Ahorra tiempo</b>Evita saturarte con múltiples cotizaciones para conocer los precios del mercado.</span></li>
          <li><img class="em" src="img/e_bullseye.webp" alt=""><span><b>Planea a tu medida</b>Personaliza servicios, cantidades e invitados para ajustar tu evento a tu presupuesto.</span></li>
          <li><img class="em" src="img/e_handshake.webp" alt=""><span><b>Decide con confianza</b>Compara escenarios, toma decisiones informadas y encuentra proveedores que se ajusten a tus necesidades.</span></li>
        </ul>
        <div class="emph"><strong>Y conecta con proveedores 100% listos para atender tu evento, directo en tu WhatsApp.</strong><small>Beneficio exclusivo · Tarifa preferencial</small></div>
        <div class="fnd"><img src="img/b_fundador.webp" alt="Insignia de miembro fundador"><div style="display:grid;gap:6px"><b>Serías el anfitrión 128 de 500 de nuestros miembros fundadores</b><div class="bar"><i style="width:26%"></i></div><span class="hint">Lugares de ejemplo</span></div></div>
        <div class="kinds"><span class="lab">Te ayudamos con</span><div class="ks"><span class="k"><img class="em" src="img/e_birthday_cake.webp" alt="">Todo tipo de eventos sociales</span><span class="k"><img class="em" src="img/e_briefcase.webp" alt="">Todo tipo de eventos corporativos</span></div></div>
      </div>
    </section>
    <div class="beta" id="beta" hidden role="dialog" aria-modal="true" aria-labelledby="betaT"><div class="bx"><div class="tape"></div><div class="in">
      <b id="betaT" style="font-size:19px">🚧 Estamos en versión beta</b>
      <span>Por ahora el cotizador funciona con precios de ejemplo. Los precios reales llegan con nuestros proveedores fundadores el 1º de noviembre.</span>
      <div class="cd" id="cd"></div>
      <button class="btn host" type="button" id="betaOk" style="justify-self:stretch">Entendido. Probar versión beta</button></div></div></div>'''
s = s[:a] + HS + s[b:]

# popup de beta: aparece un momento después de entrar al lado del anfitrión (una vez por visita)
rep('''document.querySelectorAll("[data-go]").forEach(b=>b.onclick=()=>goSide(b.dataset.go));''',
    '''document.querySelectorAll("[data-go]").forEach(b=>b.onclick=()=>goSide(b.dataset.go));
let betaShown=false;function betaSoon(){if(betaShown)return;betaShown=true;setTimeout(()=>{if(U.view!=="home"||!$("journey").hidden)return;$("beta").hidden=false;$("betaOk").focus();track("beta_popup");},1200);}
$("betaOk").onclick=()=>{$("beta").hidden=true;};
(()=>{const hs=$("d-hs");if(!hs)return;hs.addEventListener("pointerenter",e=>{if(e.pointerType==="mouse")betaSoon();});hs.addEventListener("focusin",betaSoon);
 const sw=$("swt");new MutationObserver(()=>{if(sw.dataset.s==="hs")betaSoon();}).observe(sw,{attributes:true,attributeFilter:["data-s"]});})();''')

# sin botón de ideas por ahora
s = s.replace('drawTop();hqvIdeas();track("home_vista");', 'drawTop();track("home_vista");')
P.write_text(s)
print('shell7 ok')

# ---------- «Crea tu cuenta» al guardar la pre-cotización + onboarding corto
s = P.read_text()
def rep2(a, b):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:100]
    s = s.replace(a, b, 1)
rep2('''function accountModal(next,why){const m=$("modal");
 m.innerHTML=`<form class="sheet" id="acF" novalidate><img src="img/ball.webp" alt="" style="width:70px"><h2>Guarda tu cuenta</h2><span class="hint">${esc(why)}</span>''',
     '''function accountModal(next,why,onClose){const m=$("modal");
 m.innerHTML=`<form class="sheet" id="acF" novalidate><img src="img/ball.webp" alt="" style="width:70px"><h2>Crea tu cuenta</h2><span class="hint">${esc(why||"Para recibir en tu WhatsApp / correo tu pre-cotización, sumarte a nuestra comunidad de anfitriones y acceder a beneficios exclusivos.")}</span>''')
rep2('''<span>Quiero recibir recordatorios de mis fechas, novedades y promociones. <span class="hint">(opcional)</span></span>''',
     '''<span>Quiero recibir pre-cotizaciones, opciones de proveedores y beneficios exclusivos.</span>''')
rep2('''<p class="legal">Al continuar, tu cuenta invitada se vuelve cuenta de ¡Hay que vernos! con estos datos y aceptas los Términos y el Aviso de privacidad. Para entrar después te mandamos un código, sin contraseñas.</p>''',
     '''<p class="legal">Al continuar se crea tu cuenta de ¡Hay que vernos! con estos datos y aceptas los Términos y el Aviso de privacidad. Para entrar después te mandamos un código, sin contraseñas.</p>''')
rep2('''m.hidden=false;$("acX").onclick=()=>m.hidden=true;''', '''m.hidden=false;$("acX").onclick=()=>{m.hidden=true;onClose&&onClose();};''')
rep2('''Object.assign(U,{name:n,wa:w,email:em_,account:"cuenta",marketing:$("acM").checked});track("cuenta_creada",{desde:"pago"});''',
     '''Object.assign(U,{name:n,wa:w,email:em_,account:"cuenta",marketing:$("acM").checked});track("cuenta_creada",{desde:why?"pago":"pre-cotizacion"});''')
rep2('''if(d.hqv==="fiesta-lista"){if(!U.account)U.account="invitado";if(d.nombre&&!U.name)U.name=d.nombre;U.sides.fiestas=true;
  let ev;''', '''if(d.hqv==="fiesta-lista"){if(d.nombre&&!U.name)U.name=d.nombre;track("cta_pre_cotizacion",{cta:d.cta||"guardar"});
  if(U.account!=="cuenta"){accountModal(()=>saveFiesta(d),"",null);return;}saveFiesta(d);return;}
 if(d.hqv==="__nunca__"){
  let ev;''')
rep2('''function accountModal(''', '''/* Guarda la pre-cotización en la cuenta (ya creada) y abre un onboarding corto antes de cualquier pago */
function saveFiesta(d){U.sides.fiestas=true;let ev;const old=U.editing&&U.events.find(x=>x.id===U.editing);
 if(old){const nv=newEvent(d.fiesta);old.versions=old.versions||[{f:old.f,t:old.t||now()}];old.versions.unshift({f:nv.f,t:now()});Object.assign(old,{f:nv.f,provs:nv.provs,interes:nv.interes});ev=old;}
 else{ev=newEvent(d.fiesta);ev.versions=[{f:ev.f,t:now()}];ev.cta=d.cta||"guardar";U.events.unshift(ev);}
 U.editing=null;U.tab="fiestas";U.eventId=ev.id;closeJourney();show("acct");confetti();
 inbox("fiestas",`📄 Te enviamos la pre-cotización de «${ev.f.nombre||ev.f.occ}» a tu correo, con un botón para mandártela a tu WhatsApp.`);
 onboarding(ev);}
function onboarding(ev){const m=$("modal"),f=ev.f,txt=encodeURIComponent(`Mi pre-cotización de ¡Hay que vernos!: ${f.nombre||f.occ} · ${f.guests} invitados · ${money(f.pp)} por persona · total aprox. ${money(f.total)}`);
 m.innerHTML=`<div class="sheet"><img src="img/ball.webp" alt="" style="width:76px"><h2>¡Listo, ${esc(first(U.name))}! 🎉</h2><span class="hint">Ya tienes tu cuenta de ¡Hay que vernos!. Así funciona:</span>
  <div class="soft" style="text-align:left;gap:10px">
   <span>📄 <b>Tu pre-cotización ya va en camino a tu correo</b> en PDF.</span>
   <span>🗂️ <b>Aquí se guardan tus pre-cotizaciones</b>: si recalculas, guardamos cada versión.</span>
   <span>🔔 <b>Te avisamos aquí y por correo</b> cuando tu planner o tus proveedores respondan.</span></div>
  <a class="btn ghost" href="https://wa.me/?text=${txt}" target="_blank" rel="noopener">💬 Enviármela a mi WhatsApp</a>
  <button class="btn host" type="button" id="obOk">Ver mi fiesta →</button></div>`;
 m.hidden=false;$("obOk").onclick=()=>{m.hidden=true;};track("onboarding_visto");}
function accountModal(''')
P.write_text(s)
print('shell7 cuenta ok')
