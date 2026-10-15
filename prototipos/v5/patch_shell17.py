"""v15 · Cuenta del proveedor (Diego, 14 oct 2026). Correr DESPUÉS de patch_shell16.py.
- Agenda: «bloquear» en lugar de «cerrar» (Bloquear una fecha · Fecha bloqueada · Bloqueada con disponibilidad).
- Pop-up con confeti cuando llega una solicitud (primer empuje de conversión del lado proveedor).
- Pop-up con confeti cuando el proveedor queda seleccionado:
  · Event planner: el anfitrión ya lo eligió y espera que el planner lo contacte primero; los contactos de los proveedores
    están liberados solo para el planner; desde ahora él es el contacto principal y el proyecto depende 100% de él.
  · Servicios y venue: más flexible; CTA para escribir primero (los que contactan en menos de 1 hora se quedan con más proyectos)."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:120]
    s = s.replace(a, b, count)


for a, b in [('Las fechas cerradas les avisan', 'Las fechas bloqueadas les avisan'), ('>Fecha cerrada</button>', '>Fecha bloqueada</button>'),
             ('>Cerrada con disponibilidad</button>', '>Bloqueada con disponibilidad</button>'), ('>Cerrar una fecha</button>', '>Bloquear una fecha</button>'),
             ('«Fecha cerrada con disponibilidad»', '«Bloqueada con disponibilidad»'), ('Saldrás con «Fecha cerrada» en esa fecha.', 'Saldrás con «Fecha bloqueada» en esa fecha.'),
             ('toast("📅 Fecha cerrada")', 'toast("📅 Fecha bloqueada")')]:
    rep(a, b)

CSS = '''
/* ===== v15 · pop-ups del proveedor ===== */
.sheet.celeb{max-width:460px;text-align:center;justify-items:center;background:linear-gradient(165deg,#41145F 0%,#8205B4 50%,#FA1ED2 115%)!important;color:#fff;box-shadow:0 0 0 3px rgba(190,255,0,.35),0 24px 60px rgba(0,0,0,.45)}
.sheet.celeb h2{color:#fff;font-size:23px;line-height:1.15;margin:0}
.sheet.celeb .mk{font-size:11px;font-weight:900;letter-spacing:.14em;color:#BEFF00}
.sheet.celeb .big{font-size:56px;line-height:1;filter:drop-shadow(0 6px 14px rgba(0,0,0,.3));animation:lit .6s ease-out}
.sheet.celeb .lead{display:grid;gap:6px;width:100%;background:rgba(255,255,255,.12);border-radius:18px;padding:12px 14px;text-align:left}
.sheet.celeb .lead b{font-size:16px}.sheet.celeb .lead span{font-size:13.5px;opacity:.92}
.sheet.celeb .lead .kv{display:flex;flex-wrap:wrap;gap:6px}.sheet.celeb .lead .kv i{font-style:normal;background:rgba(255,255,255,.16);border-radius:99px;padding:3px 10px;font-size:12.5px;font-weight:800}
.sheet.celeb .clock{background:#BEFF00;color:#1a1033;border-radius:99px;padding:4px 12px;font-weight:900;font-size:13px}
.sheet.celeb .todo{display:grid;gap:8px;width:100%;text-align:left}
.sheet.celeb .todo div{display:flex;gap:10px;align-items:flex-start;background:rgba(255,255,255,.12);border-radius:16px;padding:10px 12px;font-size:13.5px;line-height:1.35}
.sheet.celeb .todo div b{display:block;font-size:14.5px}
.sheet.celeb .todo .n{flex:0 0 26px;height:26px;border-radius:50%;background:#BEFF00;color:#1a1033;display:grid;place-items:center;font-weight:900}
.sheet.celeb .hint{color:rgba(255,255,255,.85)!important}
.sheet.celeb button.link{color:#fff}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

JS = r'''
/* Pop-ups con confeti para el proveedor */
function celebPop(html,bind){const m=$("modal");m.innerHTML=`<div class="sheet celeb">${html}</div>`;m.hidden=false;try{confetti();}catch(_){}bind(m);}
function leadPop(r,vt){if(!r)return;const pl=vt==="planner";
 celebPop(`<span class="mk">${pl?"📋 TE ELIGIERON":"🔔 NUEVA OPORTUNIDAD"}</span><div class="big">${pl?"🥳":"🎉"}</div>
  <h2>${pl?`¡${esc(r.cli.n)} te eligió como su event planner!`:`¡Te llegó una oportunidad de trabajo!`}</h2>
  <div class="lead"><b>${esc(r.occ)} · ${r.guests} invitados</b><span>${fdate(r.date)} · ${esc(r.zona)} · a ${r.km} km de ti</span>
   <div class="kv">${pl?`<i>💰 Presupuesto ${money(r.total)}</i>`:`<i>${esc(r.svc)}</i><i>💰 ${money(r.est)} estimado</i>`}<i>⭐ ${r.cli.stars} anfitrión ${r.cli.ver?"verificado":""}</i></div></div>
  <span class="clock">⏳ Tienes 24 h para ${pl?"aceptar":"postularte"}</span>
  <button class="btn cta" type="button" id="lpGo" style="width:100%">${pl?"Ver la solicitud y aceptar →":"Ver la solicitud y postularme →"}</button>
  <button class="link" type="button" id="lpLater">Más tarde</button>`,m=>{
  $("lpGo").onclick=()=>{track("lead_popup",{abrir:true,vt});m.hidden=true;U.neg.sel=r.id;drawAcct();setTimeout(()=>{const f=document.querySelector(".ficha.on,.ficha[aria-pressed='true']");f&&f.scrollIntoView({behavior:"smooth",block:"center"});},80);};
  $("lpLater").onclick=()=>{track("lead_popup",{abrir:false,vt});m.hidden=true;};});}
function plannerSelPop(j){const n=esc(j.cliente),np=(j.e&&j.e.interes)||"tus";
 celebPop(`<span class="mk">✅ TRATO CONFIRMADO</span><div class="big">🏆</div><h2>¡${n} confirmó y pagó! Ahora te toca a ti 💪</h2>
  <div class="todo">
   <div><span class="n">1</span><span><b>Da el primer paso hoy</b>${n} ya te eligió y no hará nada más: está esperando tu mensaje.</span></div>
   <div><span class="n">2</span><span><b>Los contactos son solo tuyos</b>Liberamos a ${np} proveedores únicamente para ti. Tu cliente no tiene sus datos.</span></div>
   <div><span class="n">3</span><span><b>Tú eres el contacto principal</b>Desde ahora coordinas con los proveedores. El rumbo y el éxito del proyecto dependen 100% de ti.</span></div></div>
  <button class="btn wa" type="button" id="spWa" style="width:100%">💬 Escribirle a ${n} por WhatsApp</button>
  <button class="link" type="button" id="spProv">Primero quiero ver a los proveedores</button>`,m=>{
  $("spWa").onclick=()=>{track("planner_primer_contacto");m.hidden=true;toast("📲 Abriríamos WhatsApp con tu cliente (simulado)");};
  $("spProv").onclick=()=>{m.hidden=true;};});}
function svcSelPop(x){celebPop(`<span class="mk">🏆 ¡GANASTE!</span><div class="big">🎉</div><h2>¡Te seleccionaron para ${esc(x.ev)}!</h2>
  <span>Tu cliente ya tiene tu WhatsApp y puede escribirte. ¿Quieres adelantarte?</span>
  <div class="lead"><b>⚡ Los proveedores que escriben en menos de 1 hora se quedan con más proyectos.</b><span>Preséntate, confirma la fecha y pregunta cómo quiere que te lleguen los detalles.</span></div>
  <button class="btn wa" type="button" id="ssWa" style="width:100%">💬 Escribirle ahora</button>
  <button class="link" type="button" id="ssLater">Prefiero esperar su mensaje</button>`,m=>{
  $("ssWa").onclick=()=>{track("proveedor_primer_contacto");m.hidden=true;toast("📲 Abriríamos WhatsApp con tu cliente (simulado)");};
  $("ssLater").onclick=()=>{m.hidden=true;};});}
'''
rep('function seedSol(vt,n){', JS + '\nfunction seedSol(vt,n){')
rep('$("sReq").onclick=()=>{seedSol(vt,1);inbox("negocio",vt==="planner"?"📋 Un anfitrión te eligió como su event planner. Tienes 24 h.":"🔔 Un evento encaja contigo. Tienes 24 h para postularte.");drawAcct();};',
    '$("sReq").onclick=()=>{seedSol(vt,1);inbox("negocio",vt==="planner"?"📋 Un anfitrión te eligió como su event planner. Tienes 24 h.":"🔔 Un evento encaja contigo. Tienes 24 h para postularte.");drawAcct();leadPop(U.neg.sol[0],vt);};')
rep('x.fin==="sel"){N.agenda.push({d:x.date,ev:x.ev,st:"cerrada",vt:x.vt});toast("🎉 ¡Te seleccionaron!");}',
    'x.fin==="sel"){N.agenda.push({d:x.date,ev:x.ev,st:"cerrada",vt:x.vt});setTimeout(()=>svcSelPop(x),60);}')
rep('c.onclick=()=>{j.conf=true;confetti();inbox("negocio",`🔓 ${j.cliente} confirmó. Ya ves a sus proveedores.`);drawAcct();};',
    'c.onclick=()=>{j.conf=true;inbox("negocio",`🔓 ${j.cliente} confirmó. Ya ves a sus proveedores. Te toca dar el primer paso.`);drawAcct();plannerSelPop(j);};')
s = s.replace('PROTOTIPO v14', 'PROTOTIPO v16')
P.write_text(s)
print('shell17 ok')
