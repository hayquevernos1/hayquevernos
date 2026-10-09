"""v11 · Mis fiestas = solo las fiestas propias del anfitrión (Diego, 8 oct 2026 noche). Correr DESPUÉS de patch_shell13.py.
- Sin sub-pestañas «Mis fiestas personales / Las fiestas de mis clientes».
- Las fiestas de los clientes del planner viven en Mi negocio › Event planner › En proceso › «Mis clientes»
  (esperando confirmación → proveedores liberados). Aceptar a un cliente ya no manda a Mis fiestas."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:110]
    s = s.replace(a, b, count)


# ---------- sacar jobEvent / jobDetailHtml / bindJob de drawFiestas (quedan globales)
a = s.index('\nfunction jobEvent(j)')
b = s.index('\n', s.index('\nfunction bindJob(j)') + 5)
block = s[a:b]
s = s[:a] + s[b:]
i = s.index('\nfunction drawFiestas(p)')
s = s[:i] + block + s[i:]

# ---------- Mis fiestas: una sola vista
rep('''U.sub=U.sub||"mias";''', '''U.sub="mias";''')
rep('''const tabs=true?`<div class="subtabs" role="tablist">''', '''const tabs=false?`<div class="subtabs" role="tablist">''')
rep('''Mis fiestas personales</h2>''', '''Mis fiestas</h2>''')

# ---------- Mi negocio › Event planner: «Mis clientes»
rep('''`:`<span class="hint">Los clientes que aceptes pasan a <b>Mis fiestas › Las fiestas de mis clientes</b>.</span>`}</section>''',
    '''`:`<b style="margin-top:8px">${em("handshake")} Mis clientes</b><span class="hint">Las fiestas que organizas como event planner. Cuando tu cliente confirma el trato, aquí ves a sus proveedores.</span>
   ${(U.plannerJobs||[]).length?`<div class="flist">${U.plannerJobs.map(j=>`<div class="fch ${j.nombre===U.jobSel?"on":""}"><div class="fh" data-job="${esc(j.nombre)}" role="button" tabindex="0" style="background:var(--prov)"><small>${esc(j.nombre)} · ${j.guests} invitados · ${fdate(j.date)}</small><span class="n"><b>${money(j.total/j.guests)}</b><span>por persona</span></span><small>Total pre-cotizado ${money(j.total)} · tu cobro ${money(j.cobro||0)}</small>${j.nuevo&&!j.conf?`<span class="st wait">Esperando a tu cliente</span>`:`<span class="st go">En progreso</span>`}</div>
   <div class="fv"><div class="vr"><span class="grow"><b>Tu cliente: ${esc(j.cliente)}</b><small>Le das seguimiento por WhatsApp junto con sus proveedores.</small></span><span class="ico"><button type="button" data-job="${esc(j.nombre)}">Ver</button></span></div></div></div>`).join("")}</div><div id="jobBox"></div>`:'<div class="empty"><span class="hint">Cuando aceptes a un cliente, su fiesta aparece aquí.</span></div>'}`}</section>''')
# render + binding del cliente seleccionado dentro de drawNegocio
rep(''' p.querySelectorAll("[data-nv]").forEach(b=>b.onclick=()=>{N.vt=b.dataset.nv;N.sel=null;drawAcct();});
 p.querySelectorAll("[data-so]")''',
    ''' p.querySelectorAll("[data-nv]").forEach(b=>b.onclick=()=>{N.vt=b.dataset.nv;N.sel=null;drawAcct();});
 if(vt==="planner"&&(U.plannerJobs||[]).length){const jj=U.plannerJobs.find(j=>j.nombre===U.jobSel)||U.plannerJobs[0];U.jobSel=jj.nombre;$("jobBox").innerHTML=jobDetailHtml(jj);bindJob(jj);
  p.querySelectorAll("[data-job]").forEach(b=>b.onclick=()=>{U.jobSel=b.dataset.job;drawAcct();setTimeout(()=>{const d=$("jobBox");d&&d.scrollIntoView({behavior:"smooth",block:"start"});},50);});}
 p.querySelectorAll("[data-so]")''')
# aceptar: se queda en Mi negocio › Event planner
rep('''"Guardar y pasar a mis fiestas":"Guardar"''', '''"Guardar y pasar a mis clientes":"Guardar"''')
rep('''inbox("fiestas",`📋 «${r.occ} de ${r.cli.n}» ya está en Mis fiestas › Las fiestas de mis clientes. Esperamos la confirmación de tu cliente.`);''',
    '''inbox("negocio",`📋 «${r.occ} de ${r.cli.n}» ya está en Mi negocio › Event planner › Mis clientes. Esperamos la confirmación de tu cliente.`);''')
rep('''toast("🤝 ¡Aceptado! Lo encuentras en Mis fiestas › Las fiestas de mis clientes.");U.tab="fiestas";U.sub="otros";U.jobSel=U.plannerJobs[0].nombre;drawAcct();''',
    '''toast("🤝 ¡Aceptado! Lo encuentras abajo, en Mis clientes.");U.tab="negocio";U.jobSel=U.plannerJobs[0].nombre;drawAcct();setTimeout(()=>{const d=$("jobBox");d&&d.scrollIntoView({behavior:"smooth",block:"start"});},80);''')
s = s.replace('inbox("fiestas",`🔓 ${j.cliente} confirmó. Ya ves a sus proveedores.`)', 'inbox("negocio",`🔓 ${j.cliente} confirmó. Ya ves a sus proveedores.`)', 1)
# Mis fiestas sin fiestas propias: invitación azul siempre (aunque sea planner)
rep('''if(U.tab==="fiestas")return drawFiestas(p);''', '''if(U.tab==="fiestas")return U.sides.fiestas?drawFiestas(p):drawInvite(p,"fiestas");''')

s = s.replace('PROTOTIPO v10', 'PROTOTIPO v11')
P.write_text(s)
print('shell14 ok', len(s))
