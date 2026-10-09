"""v14 · Cuenta (Diego, 9 oct 2026 tarde). Correr DESPUÉS de patch_shell15.py.
- Tracker con más brillo (lima neón que «se enciende») y, en celular, la pantalla baja sola hasta el tracker.
- 2.º intento de conversión: al cerrarse el pop-up del event planner (con o sin planner), sale otro pop-up enfocado en el
  tracker: «Estamos encontrando proveedores que hacen match con tu evento», contador rápido 1, 2, 3… y botón para
  contactarlos. Si dice «Ahora no», se queda la pantalla con «Contactar» en cada proveedor."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:120]
    s = s.replace(a, b, count)


CSS = '''
/* ===== v14 · tracker con brillo + pop-up de match ===== */
.int .st.vis{background:linear-gradient(135deg,#BEFF00,#FAFA19);color:#1a1033;border-radius:99px;padding:3px 11px;font-weight:900;box-shadow:0 0 0 3px rgba(190,255,0,.3),0 0 18px rgba(190,255,0,.75);animation:lit .55s ease-out}
.int .st.wait{color:#9146FF;font-weight:900}
@keyframes lit{0%{transform:scale(.5);opacity:0}60%{transform:scale(1.18)}100%{transform:scale(1)}}
.trkm i{box-shadow:0 0 14px rgba(250,30,210,.8)}
.sheet.mtc{max-width:460px;width:100%;text-align:center;justify-items:center;color:#fff;background:linear-gradient(165deg,#41145F 0%,#8205B4 55%,#FA1ED2 120%)!important;box-shadow:0 0 0 3px rgba(190,255,0,.35),0 24px 60px rgba(0,0,0,.45)}
.sheet.mtc h2{color:#fff;font-size:22px;line-height:1.15}
.sheet.mtc .mk{font-size:11px;font-weight:900;letter-spacing:.14em;color:#BEFF00;display:flex;gap:6px;align-items:center}
.sheet.mtc .mk i{width:9px;height:9px;border-radius:50%;background:#BEFF00;box-shadow:0 0 10px #BEFF00;animation:pulse 1s infinite}
.mnum{display:grid;justify-items:center;line-height:1}
.mnum b{font-size:92px;font-weight:900;letter-spacing:-.04em;background:linear-gradient(135deg,#BEFF00,#FAFA19);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 18px rgba(190,255,0,.55));font-variant-numeric:tabular-nums}
.mnum span{font-weight:900;font-size:15px;opacity:.9}
.mnum b.bump{animation:bump .12s}@keyframes bump{50%{transform:scale(1.08)}}
.mlines{display:grid;gap:6px;width:100%}
.ml{display:flex;justify-content:space-between;align-items:center;gap:8px;background:rgba(255,255,255,.1);border-radius:14px;padding:8px 12px;font-weight:800;font-size:14px;transition:background .3s}
.ml span{text-align:left}.ml b{font-size:13px;opacity:.7;white-space:nowrap}
.ml.on{background:rgba(190,255,0,.16)}
.ml.on b{opacity:1;color:#1a1033;background:linear-gradient(135deg,#BEFF00,#FAFA19);border-radius:99px;padding:3px 10px;box-shadow:0 0 14px rgba(190,255,0,.8);animation:lit .5s ease-out}
.trkm.big{height:10px;width:100%;background:rgba(255,255,255,.15)}
.trkm.big i{background:linear-gradient(90deg,#BEFF00,#FAFA19);box-shadow:0 0 16px rgba(190,255,0,.9);transition:width .15s}
.mcta{display:grid;gap:8px;width:100%;animation:lit .5s ease-out}
.mcta .hint{color:rgba(255,255,255,.85)!important}
.mcta button.link{color:#fff}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# al cerrar el pop-up del planner (con o sin planner) → pop-up de match
rep('''function plOffer(e,step){const m=$("modal");e.plAsked=true;step=step||"ask";const pool=PLANNERS.map(normPl);e.plI=(e.plI||0)%pool.length;const c=pool[e.plI],cur=e.planner.cur;
 const close=()=>{m.hidden=true;drawAcct();};''',
    '''function plOffer(e,step){const m=$("modal");e.plAsked=true;step=step||"ask";const pool=PLANNERS.map(normPl);e.plI=(e.plI||0)%pool.length;const c=pool[e.plI],cur=e.planner.cur;
 const close=()=>{m.hidden=true;drawAcct();matchPop(e);};''')

# en celular, bajar hasta el tracker mientras se ilumina
rep(' if(!e.trk)startTracker(e);}', ''' if(!e.trk){startTracker(e);const h=$("tkH");if(h&&innerWidth<820)setTimeout(()=>h.scrollIntoView({behavior:"smooth",block:"start"}),250);}}
/* Pop-up de match: 2.º intento de conversión, después del pop-up del event planner */
function matchPop(e){if(e.mAsked||e.paid)return;e.mAsked=true;const m=$("modal"),ks=Object.keys(e.provs),fast=matchMedia("(prefers-reduced-motion: reduce)").matches;
 setTimeout(()=>{if(U.eventId!==e.id||U.tab!=="fiestas"||!m.hidden)return;const pl=e.opts.planner&&e.planner.cur,N=ks.reduce((a,k)=>a+e.provs[k].length,0);
  const cum=[];ks.reduce((a,k,i)=>(cum[i]=a+e.provs[k].length),0);
  m.innerHTML=`<div class="sheet mtc"><span class="mk"><i></i>BUSCANDO EN VIVO</span><h2 id="mtH">Estamos encontrando proveedores que hacen match con tu evento</h2>
   <div class="mnum"><b id="mtN">0</b><span id="mtS">proveedores disponibles</span></div>
   <div class="mlines">${ks.map((k,i)=>`<div class="ml" id="ml-${i}"><span>${e.provs[k][0].emo} ${esc(k)}</span><b>⏳ buscando…</b></div>`).join("")}</div>
   <div class="trkm big"><i id="mtM" style="width:0"></i></div>
   <div class="mcta" id="mtCta" hidden><button class="btn cta" type="button" id="mtGo" style="width:100%">${pl?`Contactar a ${esc(first(pl.n))} + ${N} proveedores →`:`Contactar a los ${N} proveedores →`}</button>
    <span class="hint">Pago único: ${money(pl?PR.proveedoresMasPlanner:PR.desbloquearProveedores)} · ves sus datos y les escribes por WhatsApp.</span>
    <button class="link" type="button" id="mtNo">Ahora no</button></div></div>`;
  m.hidden=false;let n=0;const NE=$("mtN"),done=()=>{ks.forEach((k,i)=>{const r=$("ml-"+i);if(r&&!r.classList.contains("on")){r.classList.add("on");r.querySelector("b").textContent=`✅ ${e.provs[k].length}`;}});
   NE.textContent=N;$("mtM").style.width="100%";const mk=m.querySelector(".mk");if(mk)mk.innerHTML="✅ MATCH LISTO";$("mtH").textContent=`¡${N} proveedores hacen match con tu evento! 🎉`;$("mtS").textContent="cumplen con lo que pides, cerca de ti y libres en tu fecha";$("mtCta").hidden=false;
   $("mtGo").onclick=()=>{track("match_pop",{contactar:true});m.hidden=true;drawAcct();startPay(e);};
   $("mtNo").onclick=()=>{track("match_pop",{contactar:false});m.hidden=true;drawAcct();};};
  if(fast){done();return;}
  const dt=Math.max(45,Math.min(120,2600/N)),tick=()=>{if(m.hidden)return;n++;NE.textContent=n;NE.classList.remove("bump");void NE.offsetWidth;NE.classList.add("bump");$("mtM").style.width=Math.round(n/N*100)+"%";
   cum.forEach((c,i)=>{const r=$("ml-"+i);if(n>=c&&r&&!r.classList.contains("on")){r.classList.add("on");r.querySelector("b").textContent=`✅ ${e.provs[ks[i]].length}`;}});
   if(n>=N)setTimeout(done,350);else setTimeout(tick,dt);};
  setTimeout(tick,500);},fast?0:450);}''')

s = s.replace('PROTOTIPO v13', 'PROTOTIPO v14')
P.write_text(s)
print('shell16 ok')
