"""v7 · Home nuevo (comentarios de Diego en Miro, 8 oct 2026, 19:37):
pantalla de entrada con logo grande, «¡Organizar una fiesta ya es la fiesta!», switch con bola disco animada
(se arrastra a un lado o al otro) y, al elegir, aparece la puerta de ese lado. Sin destellos junto al logo.
Correr DESPUÉS de patch_shell7.py (y de patch_shell8.py si ya se aplicó). Edita shell.html en su lugar."""
from pathlib import Path
import re
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:100]
    s = s.replace(a, b, count)


# ---------- marcado: héroe nuevo en lugar del título y del panel neutral
rep('<div class="hh"><h1>¿De qué lado de la fiesta estás?</h1><p>Un mismo universo, dos caminos. Elige el tuyo.</p></div>',
    '<div class="hhero"><img class="big" src="img/logo.webp" alt="¡Hay que vernos!" width="900" height="358">'
    '<h1>¡Organizar una fiesta ya es la fiesta!</h1></div>')
rep('<span class="knob"><img src="img/ball.webp" alt=""></span></div></div>',
    '<span class="knob"><i class="ar l">‹</i><img src="img/ball.webp" alt="" draggable="false"><i class="ar r">›</i></span></div>'
    '<div class="swh"><b>Desliza hacia tu lado</b>'
    '<span>← A la izquierda, si ofreces servicios para fiestas</span>'
    '<span>A la derecha, si estás organizando una fiesta →</span></div></div>')
s, n = re.subn(r'\s*<div class="seam neutral-seam".*?</div>\s*<section class="neutral" id="d-neu".*?</section>', '', s, flags=re.S)
assert n == 1, 'panel neutral'
rep('<main id="home" class="wrap home">', '<main id="home" class="wrap home" data-s="neutral">')

# ---------- estilos
CSS = '''
/* ===== Home v7: héroe + switch en todas las pantallas ===== */
.home .hhero{display:grid;justify-items:center;text-align:center;gap:10px;padding-block:10px 18px;transition:all .3s}
.home .hhero img.big{width:min(420px,72vw);height:auto;filter:drop-shadow(0 10px 22px rgba(65,20,95,.18))}
.home .hhero h1{font-size:clamp(26px,4.4vw,46px);font-weight:900;margin:0;line-height:1.1}
.home .sw{display:block!important;position:sticky;top:calc(env(safe-area-inset-top,0px) + 60px);z-index:15;padding-block:4px 14px}
.home .swt{max-width:520px;padding:8px;touch-action:pan-y;user-select:none;-webkit-user-select:none}
.home .swt button{font-size:16px;padding:12px 6px}
.home .swt .knob{width:58px;height:58px;margin:-29px 0 0 -29px;pointer-events:auto;cursor:grab}
.home .swt.drag .knob{transition:none;cursor:grabbing}
.home .swt .knob .ar{position:absolute;top:50%;margin-top:-12px;font-style:normal;font-weight:900;font-size:22px;line-height:24px;color:var(--grape,#7B2FF7);opacity:0}
.home .swt .knob .ar.l{left:-16px}.home .swt .knob .ar.r{right:-16px}
.home .swt[data-s="neutral"] .knob img{animation:hqvNudge 2.6s ease-in-out infinite}
.home .swt[data-s="neutral"] .knob .ar.l{animation:hqvArL 2.6s ease-in-out infinite}
.home .swt[data-s="neutral"] .knob .ar.r{animation:hqvArR 2.6s ease-in-out infinite}
@keyframes hqvNudge{0%,100%{transform:none}18%{transform:translateX(-12px) rotate(-14deg)}36%{transform:none}54%{transform:translateX(12px) rotate(14deg)}72%{transform:none}}
@keyframes hqvArL{0%,100%{opacity:0;transform:none}18%{opacity:1;transform:translateX(-6px)}30%{opacity:0}}
@keyframes hqvArR{0%,50%,100%{opacity:0;transform:none}54%{opacity:1;transform:translateX(6px)}66%{opacity:0}}
@media (prefers-reduced-motion:reduce){.home .swt .knob img,.home .swt .knob .ar{animation:none!important}}
.home .swh{display:grid;justify-items:center;text-align:center;gap:2px;margin-top:14px;font-size:13px;color:var(--muted)}
.home .swh b{font-size:15px;color:var(--ink,#1a1033)}
.home:not([data-s="neutral"]) .swh{display:none}
.home:not([data-s="neutral"]) .hhero{padding-block:0 6px}
.home:not([data-s="neutral"]) .hhero img.big{width:min(220px,50vw)}
.home:not([data-s="neutral"]) .hhero h1{font-size:clamp(20px,2.6vw,26px)}
.home .doors{display:block!important;overflow:visible!important;margin-inline:0!important;max-width:640px;margin:0 auto}
.home .doors>*{display:none!important;padding-inline:0!important}
.home[data-s="pv"] #d-pv,.home[data-s="hs"] #d-hs{display:grid!important;animation:hqvIn .35s ease-out}
@keyframes hqvIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
body:has(#home:not([hidden])) .top .logo{visibility:hidden}
@media (max-width:860px){.home .hhero{padding-block:4px 12px}.home:not([data-s="neutral"]) .hhero h1{display:none}.home .swt button{font-size:14px}}
'''
rep('.hqv-ideas{display:none!important}', '.hqv-ideas{display:none!important}' + CSS)

# ---------- comportamiento: el switch decide qué puerta se ve (también arrastrando la bola)
s, n = re.subn(r'function goSide\(s\)\{.*?\n', '''function goSide(s,quiet){$("home").dataset.s=s;$("swt").dataset.s=s;if(!quiet)track("home_switch",{lado:s});
 if(s!=="neutral"){const sw=document.querySelector(".home .sw");setTimeout(()=>{const y=sw.getBoundingClientRect().top+scrollY-70;if(scrollY>y)scrollTo({top:y,behavior:"smooth"});},40);}}
''', s, count=1, flags=re.S)
assert n == 1, 'goSide'
s, n = re.subn(r'function syncSwitch\(\)\{.*?\naddEventListener\("load",centerNeutral\);setTimeout\(centerNeutral,60\);\n', '''function centerNeutral(){}
(()=>{const sw=$("swt");let x0=null,dx=0,moved=false;
 sw.addEventListener("pointerdown",e=>{x0=e.clientX;dx=0;moved=false;});
 addEventListener("pointermove",e=>{if(x0===null)return;dx=e.clientX-x0;if(Math.abs(dx)>8){moved=true;sw.classList.add("drag");
  const r=sw.getBoundingClientRect(),k=sw.querySelector(".knob"),half=r.width/2-36;k.style.left=`calc(50% + ${Math.max(-half,Math.min(half,dx))}px)`;}});
 addEventListener("pointerup",()=>{if(x0===null)return;const k=sw.querySelector(".knob");sw.classList.remove("drag");k.style.left="";
  if(moved&&Math.abs(dx)>24)goSide(dx<0?"pv":"hs");x0=null;});
 sw.addEventListener("click",e=>{if(moved){e.stopPropagation();e.preventDefault();moved=false;}},true);
 /* deslizar sobre la puerta también cambia de lado (celular) */
 let tx=null,ty=null;doors.addEventListener("touchstart",e=>{tx=e.touches[0].clientX;ty=e.touches[0].clientY;},{passive:true});
 doors.addEventListener("touchend",e=>{if(tx===null)return;const ddx=e.changedTouches[0].clientX-tx,ddy=e.changedTouches[0].clientY-ty;tx=null;
  if(Math.abs(ddx)>70&&Math.abs(ddx)>Math.abs(ddy)*1.6){const cur=$("home").dataset.s;goSide(ddx<0?(cur==="pv"?"hs":cur==="neutral"?"hs":"hs"):(cur==="hs"?"pv":"pv"));}},{passive:true});
})();
''', s, count=1, flags=re.S)
assert n == 1, 'syncSwitch'
P.write_text(s)
print('shell9 home ok')
