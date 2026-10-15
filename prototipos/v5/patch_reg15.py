"""v20 · Registro (Diego, 15 oct 2026). reg14.html → reg15.html — «Mis servicios» con la ruleta (svc7.js) integrada al prototipo."""
from pathlib import Path
V = Path('/home/claude/hqv/v5')
s = (V / 'reg14.html').read_text()


def rep(a, b, count=1):
    global s
    assert a in s, 'NO ENCONTRADO: ' + a[:140]
    s = s.replace(a, b, count)


js = (V / 'svc7.js').read_text()
rep('\n/* Venue: los servicios se eligen', '\n' + js + '\n/* Venue: los servicios se eligen')
rep('<script src="catalogo_v2.js"></script>', '<script src="catalogo_v2.js"></script>\n<script src="ruleta_data.js"></script>')
a = s.index('  S.services.forEach((s,i)=>{svcDefaults(s);const n=catOf(s.cat)?s.cat:`Ficha ${i+1}`;')
b = s.index('  if(!filled(S.svcVar))', a)
s = s[:a] + '  ruMissStep(m);\n' + s[b:]
rep('function preview(){ensureState();', 'function preview(){ensureState();if(S.types&&S.types.services)ruSyncServices();')
rep(' x.svcPkgs=[{name:"Paquete Fiesta Mexicana"', ' {const D=ruDemo();x.rprods=D.prods;x.rpkgs=D.pkgs;x.remb=3;x.rsel=["Catering","Bebidas","Barra de café","Espresso"];}\n x.svcPkgs=[{name:"Paquete Fiesta Mexicana"')
rep('variabilidad:S.svcVar,', 'variabilidad:S.svcVar,productos:(S.rprods||[]).map(p=>({id:p.id,categoria:p.dims[0],servicio:p.dims[1],formato:p.dims[2],detalle:p.dims[3],detalleOtro:p.otro||null,nombre:p.name,platillos:p.dishes,insumos:p.ins,staff:p.crew,personas:+p.pax,cobro:p.tw.map(w=>({modo:w,precio:+p.tar[w].p,unidad:p.tar[w].u,cantidad:+p.tar[w].q||null})),extras:p.ext,entregaSinPersonal:p.tw.includes("rent")?p.dlx.dl:null,personal:p.tw.includes("labor")?{perfiles:p.labor,politicas:p.lpol}:null,minimo:p.min,promo:p.promo,fotos:p.photos.length})),paquetesRuleta:(S.rpkgs||[]).map(p=>({id:p.id,nombre:p.name,productos:p.items,insumos:p.ins,staff:p.crew,personas:+p.pax,cobro:p.tw.map(w=>({modo:w,precio:+p.tar[w].p,unidad:p.tar[w].u})),extras:p.ext,entregaSinPersonal:p.tw.includes("rent")?p.dlx.dl:null,personal:p.tw.includes("labor")?{perfiles:p.labor,politicas:p.lpol}:null,minimo:p.min,promo:p.promo})),')

CSS = '''
/* ===== v20 · Mis servicios con la ruleta ===== */
.ru-steps{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.ru-st{display:flex;gap:10px;align-items:flex-start;border:2px solid var(--line);background:var(--card);border-radius:18px;padding:10px 12px;opacity:.7}
.ru-st.on{opacity:1;border-color:#9146FF;box-shadow:0 0 0 3px rgba(145,70,255,.15)}
.ru-st>b{flex:none;width:28px;height:28px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(135deg,#9146FF,#FA1ED2);color:#fff;font-weight:900}
.ru-st span{display:grid;gap:1px;min-width:0}.ru-st strong{font-size:14.5px}.ru-st small{font-size:12px;color:var(--help,#9A92AE);line-height:1.3}
.ru-search{position:relative}
.ru-search input{width:100%;border:2px solid var(--line);background:var(--card);border-radius:99px;padding:12px 18px 12px 44px;font-weight:700}
.ru-search::before{content:"🔎";position:absolute;left:16px;top:50%;transform:translateY(-50%);font-size:16px;z-index:1}
.ru-qr{position:absolute;z-index:30;left:0;right:0;top:calc(100% + 6px);background:var(--card);border-radius:18px;box-shadow:0 12px 30px rgba(65,20,95,.2);padding:6px;display:grid;max-height:340px;overflow:auto}
.ru-qr button{border:0;background:none;text-align:left;padding:9px 12px;border-radius:12px;display:grid;gap:1px;color:var(--ink)}
.ru-qr button:hover,.ru-qr button.on{background:var(--paper)}.ru-qr small{color:var(--muted);font-size:12px}
.ru-m{position:relative;background:linear-gradient(160deg,#41145F 0%,#7B2FF7 55%,#FA1ED2 120%);border-radius:28px;padding:16px 0 14px;color:#fff;box-shadow:0 16px 36px rgba(91,31,184,.32);overflow:hidden;display:grid;gap:10px;min-width:0}
.ru-m::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 12% 18%,rgba(250,250,25,.35) 0 3px,transparent 4px),radial-gradient(circle at 86% 12%,rgba(190,255,0,.45) 0 4px,transparent 5px),radial-gradient(circle at 70% 88%,rgba(255,255,255,.3) 0 3px,transparent 4px),radial-gradient(circle at 30% 92%,rgba(250,30,210,.5) 0 4px,transparent 5px);pointer-events:none}
.ru-m>*{min-width:0}
.ru-mh{display:flex;align-items:center;gap:12px;padding-inline:16px;min-height:52px}
.ru-mt{display:grid;gap:2px;flex:1;min-width:0}.ru-mt b{font-size:16.5px;font-weight:900}.ru-mt span{font-size:12.5px;opacity:.85}
.ru-masc{width:58px;height:58px;object-fit:contain;filter:drop-shadow(0 6px 10px rgba(0,0,0,.3));flex:none}
.ru-masc.pop{animation:ruPop .5s cubic-bezier(.3,1.6,.5,1)}@keyframes ruPop{0%{transform:scale(.4) rotate(-20deg)}100%{transform:none}}
.ru-reels{position:relative;display:grid;gap:7px;min-width:0}
.ru-reels::after{content:"";position:absolute;top:-6px;bottom:-6px;left:50%;width:3px;margin-left:-1.5px;border-radius:3px;background:#BEFF00;box-shadow:0 0 12px #BEFF00;pointer-events:none;z-index:0}
.ru-reels.aligned::after{animation:ruGlow 1s ease-out}@keyframes ruGlow{40%{box-shadow:0 0 28px 6px #BEFF00}}
.ru-row,.ru-wrap{display:grid;gap:4px;min-width:0;position:relative}
.ru-lab{display:flex;justify-content:space-between;align-items:baseline;padding-inline:16px;font-size:11px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;opacity:.9}
.ru-lab span{font-weight:700;letter-spacing:0;text-transform:none;opacity:.8}
.ru-reel{position:relative;z-index:1;display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding:6px calc(50% - 20px);background:rgba(255,255,255,.1);cursor:grab;-webkit-mask-image:linear-gradient(90deg,transparent,#000 14%,#000 86%,transparent);mask-image:linear-gradient(90deg,transparent,#000 14%,#000 86%,transparent)}
.ru-reel::-webkit-scrollbar{display:none}.ru-reel.drag{cursor:grabbing;scroll-snap-type:none}
.ru-it{position:relative;z-index:1;flex:none;scroll-snap-align:center;border:0;border-radius:16px;padding:9px 13px;background:#fff;color:#8E84A6;font:inherit;font-weight:800;font-size:14px;white-space:nowrap;transform:scale(calc(1 - var(--d,1)*.16));opacity:calc(1 - var(--d,1)*.45);user-select:none;-webkit-user-select:none;cursor:pointer}
.ru-it.on{background:#BEFF00;color:#1A2600;box-shadow:0 0 0 3px rgba(255,255,255,.35)}.ru-it .e{margin-right:6px}
.ru-ar{position:absolute;top:50%;transform:translateY(-50%);z-index:4;width:32px;height:32px;border-radius:50%;border:0;background:rgba(255,255,255,.92);color:#41145F;font-size:19px;font-weight:900;line-height:1;box-shadow:0 4px 10px rgba(0,0,0,.25);cursor:pointer}
.ru-ar.l{left:10px}.ru-ar.r{right:10px}
@media (hover:none),(max-width:560px){.ru-ar{display:none}}
.ru-combo{display:grid;gap:10px;padding-inline:16px}
.ru-unit{display:inline-block;background:rgba(0,0,0,.22);border-radius:14px;padding:5px 12px;font-size:12.5px;font-weight:800;width:fit-content}
#ruOtro input{width:100%;border:0;border-radius:14px;padding:11px 14px;font-weight:700;background:#fff;color:#22163A}
.ru-save{width:100%}
.ru-ident{display:grid;gap:16px;background:var(--card);border:2px solid #9146FF;border-radius:24px;padding:18px;box-shadow:0 12px 30px rgba(65,20,95,.12)}
.ru-ident h3{font-size:20px;font-weight:900;margin:0}
.ru-crumbs{display:flex;flex-wrap:wrap;gap:4px;font-size:12px;font-weight:800;color:var(--muted)}
.ru-crumbs span:not(:last-child)::after{content:"›";margin-left:4px;opacity:.6}
.ru-inc{gap:8px}.ru-sl{font-weight:900;font-size:13.5px}
.ru-tags{display:flex;flex-wrap:wrap;gap:6px;align-items:center;border:1.5px solid var(--line);background:var(--paper);border-radius:14px;padding:5px;position:relative}
.ru-tag{display:inline-flex;align-items:center;gap:4px;background:var(--card);border-radius:99px;padding:4px 6px 4px 11px;font-weight:800;font-size:13px;box-shadow:0 2px 6px rgba(65,20,95,.08)}
.ru-tag button{border:0;background:none;color:var(--bad);font-weight:900;padding:0 4px;cursor:pointer}
.ru-tags input{flex:1;min-width:150px;border:0!important;background:none!important;padding:6px!important;font-weight:700;outline:none;box-shadow:none!important}
.ru-sg{position:absolute;z-index:20;left:0;right:0;top:calc(100% + 4px);background:var(--card);border-radius:14px;box-shadow:0 10px 30px rgba(65,20,95,.2);padding:4px;display:grid}
.ru-sg button{border:0;background:none;text-align:left;padding:8px 10px;border-radius:10px;font-weight:700;color:var(--ink);cursor:pointer}.ru-sg button:hover,.ru-sg button.on{background:var(--paper)}
.ru-crewq{display:flex;flex-wrap:wrap;gap:8px}
.ru-crewq label{display:flex;align-items:center;gap:6px;background:var(--paper);border-radius:14px;padding:5px 6px 5px 12px;font-weight:800;font-size:13px}
.ru-crewq input{width:58px;padding:5px 7px}
.ru-tsel{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;border-radius:16px}
.ru-tsb{display:grid;gap:2px;align-content:start;text-align:left;border:2px solid var(--line);background:var(--paper);border-radius:16px;padding:10px 12px;font:inherit;color:var(--ink);cursor:pointer}
.ru-tsb b{font-size:14px}.ru-tsb small{font-size:12px;color:var(--help,#9A92AE);line-height:1.3}
.ru-tsb[aria-pressed="true"]{border-color:#9146FF;box-shadow:0 0 0 3px rgba(145,70,255,.22)}.ru-tsb[aria-pressed="true"] b::before{content:"✓ ";color:#9146FF}
.ru-tg{display:grid;gap:8px;background:var(--paper);border-radius:16px;padding:12px}.ru-tg b{font-size:14px}
.ru-money{display:flex;align-items:center;gap:4px;font-weight:900;color:#8205B4}.ru-money input{width:120px}
.ru-tg select{width:auto}.ru-q{display:flex;align-items:center;gap:6px;font-weight:800;font-size:13.5px}.ru-q input{width:80px}
.ru-host{display:grid;gap:4px;background:linear-gradient(135deg,rgba(190,255,0,.22),rgba(250,250,25,.16));border-radius:16px;padding:12px 14px;font-size:14px;font-variant-numeric:tabular-nums;margin-top:6px}
.ru-sug{display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:rgba(190,255,0,.2);border-radius:14px;padding:9px 12px;font-size:13.5px;font-weight:700}
.ru-mo{display:grid;gap:16px;margin-top:12px}
.ru-exl{display:grid;gap:6px}.ru-ex{display:grid;grid-template-columns:minmax(0,1.2fr) 130px minmax(0,1fr) 24px;gap:6px;align-items:center;background:var(--paper);border-radius:14px;padding:6px 8px}
.ru-ex input{padding:7px 9px;min-width:0}.ru-ex .ru-money input{width:100%}
.ru-share{display:grid;gap:6px;background:var(--paper);border-radius:16px;padding:12px 14px;font-weight:800;font-size:13.5px}
.ru-share code{font-size:12.5px;background:var(--card);border-radius:10px;padding:6px 10px;overflow-wrap:anywhere;font-weight:700}
.ru-err{color:var(--bad);font-weight:800;font-size:13.5px}
.ru-lh{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}.ru-lh h3{font-size:19px;font-weight:900;margin:0}
.ru-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
.ru-pc{position:relative;background:var(--card);border:2px solid var(--line);border-radius:20px;padding:13px;display:grid;gap:5px;align-content:start}
.ru-pc.sel{border-color:#9146FF;box-shadow:0 0 0 3px rgba(145,70,255,.2)}.ru-pc.warn{border-color:#FFB3C7}
.ru-pc h4{font-size:15.5px;font-weight:900;margin:0;padding-right:54px}.ru-pc .ru-crumbs{padding-right:54px}
.ru-pr{font-variant-numeric:tabular-nums;font-size:13.5px}.ru-pr b{font-size:15.5px}
.ru-meta{font-size:12.5px;color:var(--muted)}
.ru-tools{position:absolute;top:8px;right:8px;display:flex;gap:2px}.ru-tools button{border:0;background:none;font-size:15px;padding:4px;border-radius:8px;cursor:pointer;color:var(--ink)}
.ru-pick{position:absolute;inset:0;border:0;background:transparent;border-radius:20px;cursor:pointer}
.ru-ck{position:absolute;top:10px;right:10px;width:26px;height:26px;border-radius:50%;border:2px solid var(--line);background:var(--card);display:grid;place-items:center;font-weight:900;color:#fff;pointer-events:none}
.ru-pc.sel .ru-ck{background:#9146FF;border-color:#9146FF}
.ru-pkb{background:linear-gradient(135deg,#FA1ED2,#FF6905);color:#fff;border-radius:99px;padding:2px 9px;font-size:11px;font-weight:900;width:fit-content}
.ru-empty{color:var(--muted);font-size:14px;border:2px dashed var(--line);border-radius:18px;padding:14px;margin:0}
.ru-bar{position:sticky;bottom:calc(10px + env(safe-area-inset-bottom,0px));z-index:15;display:flex;gap:10px;align-items:center;justify-content:space-between;background:var(--ink);color:var(--paper);border-radius:20px;padding:10px 12px 10px 16px;font-weight:800;box-shadow:0 10px 24px rgba(0,0,0,.25)}
.ru-bar .link{color:inherit}
.ru-toast{position:fixed;left:50%;bottom:calc(18px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:var(--ink);color:var(--paper);border-radius:16px;padding:10px 16px;font-weight:800;z-index:90;display:flex;gap:10px;align-items:center;max-width:calc(100% - 32px)}
.ru-toast .link{color:#BEFF00}
.ctag{display:block;font-weight:600;font-size:11.5px;color:var(--muted)}
.ru-ident .dlh{flex-wrap:wrap;min-width:0}.ru-ident .dlc{min-width:0}
.ru-note{display:block;background:rgba(0,195,137,.12);border-radius:12px;padding:7px 10px;font-size:13px;font-weight:700}
.ru-tg .dlsec{margin-top:4px}.ru-tg .dlc{background:var(--card)}
.ru-lt{display:grid;gap:6px}
.ru-lhd,.ru-lr{display:grid;grid-template-columns:minmax(110px,1.3fr) 104px 118px 118px 70px 104px 24px;gap:8px;align-items:center}
.ru-lhd{font-size:11px;font-weight:900;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:0 10px}
.ru-lr{background:var(--card);border-radius:14px;padding:6px 10px}
.ru-lr input,.ru-lr select{padding:6px 8px!important;min-width:0;font-size:14px}.ru-lr select{width:100%}
.ru-ln{font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ru-stp{display:flex;align-items:center;border:1.5px solid var(--line);border-radius:99px;overflow:hidden;background:var(--paper)}
.ru-stp button{border:0;background:none;width:30px;height:32px;font-weight:900;font-size:17px;color:#8205B4;cursor:pointer}
.ru-stp input{width:40px!important;border:0!important;background:none!important;text-align:center;padding:4px 0!important;box-shadow:none!important}
.ru-lr .ru-money input{width:100%}.ru-mn,.ru-xh{display:flex;align-items:center;gap:3px;font-weight:800;font-size:13px}.ru-mn input{width:46px}.ru-xh input{width:100%}.ru-na{color:var(--help,#9A92AE);justify-content:center}
.ru-add,.ru-pols{display:grid;gap:6px}
.ru-addc{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}.ru-addc::-webkit-scrollbar{display:none}.ru-addc .chip{flex:none;white-space:nowrap}
.ru-pils{display:flex;flex-wrap:wrap;gap:6px}
.ru-pill{display:inline-flex;align-items:center;gap:6px;border:1.5px solid var(--line);background:var(--card);border-radius:99px;padding:2px 4px 2px 2px}
.ru-pill[aria-pressed="true"]{border-color:#9146FF;background:rgba(145,70,255,.12)}
.ru-pt{border:0;background:none;font:inherit;font-weight:800;font-size:13px;padding:6px 10px;color:var(--ink);cursor:pointer}
.ru-pin{display:flex;align-items:center;gap:3px;font-weight:900;font-size:13px;padding-right:6px}.ru-pin input{width:58px;padding:4px 6px!important}
.ru-embs{gap:12px}.ru-embk{font-size:11px;font-weight:900;letter-spacing:.14em;color:#BEFF00}
.ru-emb{position:relative;width:150px;height:166px;display:grid;place-items:center;clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%);background:linear-gradient(160deg,#BEFF00,#FAFA19 45%,#FF6905);animation:ruEmbIn .6s cubic-bezier(.3,1.6,.5,1)}
.ru-emb::before{content:"";position:absolute;inset:8px;clip-path:inherit;background:linear-gradient(160deg,#9146FF,#FA1ED2)}
.ru-emb img{position:relative;width:86px;height:86px;object-fit:contain;margin-top:-14px;filter:drop-shadow(0 6px 10px rgba(0,0,0,.3))}
.ru-emb span{position:absolute;bottom:30px;background:#1A2600;color:#BEFF00;font-size:11px;font-weight:900;letter-spacing:.14em;border-radius:99px;padding:3px 10px}
@keyframes ruEmbIn{0%{transform:scale(.3) rotate(-30deg)}100%{transform:none}}
.ru-embmini{margin-right:4px}.ms-sv{background:rgba(190,255,0,.9);color:#1A2600;border-radius:99px;padding:2px 9px;font-size:12px;font-weight:900}
.ru-tg,.ru-labr,.ru-lt,.ru-add,.ru-pols,.ru-addc,.ru-pils,.ru-cov{min-width:0;max-width:100%}
.ru-labr{container-type:inline-size}
@container (max-width:720px){.ru-labr .ru-lhd{display:none}.ru-labr .ru-lr{grid-template-columns:minmax(0,1fr) minmax(0,1fr) 24px;grid-template-areas:"n n x" "q p p" "u u u" "m h h";row-gap:8px;column-gap:6px;padding:8px 10px}.ru-labr .ru-ln{display:block;min-width:0;font-size:15px}.ru-labr .ru-stp{width:100%;min-width:0}.ru-labr .ru-mn,.ru-labr .ru-xh{min-width:0;justify-content:flex-start}.ru-labr .ru-mn input,.ru-labr .ru-xh input{flex:1;min-width:0;width:auto}.ru-labr .ru-ln{grid-area:n}.ru-labr .ru-stp{grid-area:q}.ru-labr .ru-lr .ru-lrm{grid-area:x}.ru-labr .ru-lr .ru-money{grid-area:p}.ru-labr .ru-lr .ru-lu{grid-area:u}.ru-labr .ru-mn{grid-area:m}.ru-labr .ru-xh{grid-area:h}.ru-mn::before{content:"mín. ";font-weight:800;font-size:12px}.ru-xh::before{content:"extra ";white-space:nowrap;font-weight:800;font-size:12px;margin-right:2px}.ru-pill{max-width:100%;flex-wrap:wrap}.ru-pt{white-space:normal;text-align:left}}
.ru-stb{background:linear-gradient(135deg,#00C389,#BEFF00);color:#0B2A1F;border-radius:99px;padding:2px 9px;font-size:11px;font-weight:900;width:fit-content}
.ru-confl{gap:10px}.ru-cf{display:grid;gap:6px;justify-items:center;background:rgba(255,255,255,.12);border-radius:14px;padding:10px;width:100%}
.ru-pksec{display:grid;gap:12px}.ru-pksec.locked .ru-lh h3{color:var(--muted)}
.ru-lock{margin:0;border:2px dashed var(--line);border-radius:18px;padding:14px;color:var(--muted);font-weight:700;background:repeating-linear-gradient(-45deg,transparent 0 10px,rgba(145,70,255,.05) 10px 20px)}
.ru-pol{display:grid;gap:8px;background:var(--card);border-radius:14px;padding:10px 12px;font-size:13.5px}
.ru-pol label{display:block;line-height:1.7;font-weight:700}.ru-pol input[type=checkbox]{vertical-align:middle;margin:0 6px 0 0;width:18px;height:18px}.ru-pol input[type=number]{width:72px;padding:4px 8px}
.ru-paxc{position:relative;display:grid;grid-template-columns:auto minmax(0,1fr);gap:6px 14px;align-items:center;background:linear-gradient(135deg,#BEFF00,#FAFA19);color:#1A2600;border-radius:24px;padding:18px;box-shadow:0 12px 26px rgba(120,140,0,.28)}
.ru-paxm{width:70px;height:70px;object-fit:contain;filter:drop-shadow(0 6px 10px rgba(0,0,0,.2))}
.ru-paxq{display:grid;gap:4px;min-width:0}
.ru-paxl{font-size:clamp(19px,3.4vw,24px);font-weight:900;line-height:1.15}
.ru-paxh{font-size:13px;font-weight:700;opacity:.8}
.ru-paxi{display:flex;align-items:center;gap:10px;margin-top:4px}.ru-paxi input{width:130px;font-size:26px;font-weight:900;text-align:center;padding:8px 10px;border-radius:16px;border:3px solid #1A2600!important;background:#fff!important;color:#1A2600!important}
.ru-paxi b{font-size:18px;font-weight:900}
.ru-paxc #ruHost{grid-column:1/-1}.ru-paxc .ru-host{background:rgba(255,255,255,.75);color:#1A2600;margin:0}.ru-paxc .ru-host .hint{color:#4A5200!important}
@media(max-width:560px){.ru-paxc{grid-template-columns:minmax(0,1fr)}.ru-paxm{position:absolute;top:-18px;right:10px;width:54px;height:54px}.ru-paxl{padding-right:48px}.ru-ident{padding:14px}.ru-steps,.ru-tsel{grid-template-columns:minmax(0,1fr)}.ru-masc{width:48px;height:48px}.ru-ex{grid-template-columns:minmax(0,1fr) 110px 24px;grid-template-areas:"c p x" "u u u"}.ru-ex .ru-exc{grid-area:c}.ru-ex .ru-money{grid-area:p}.ru-ex .ru-exu{grid-area:u}.ru-ex .ru-exx{grid-area:x}}
@media (prefers-reduced-motion:reduce){.ru-masc.pop,.ru-reels.aligned::after{animation:none}}
'''
i = s.index('</style>')
s = s[:i] + CSS + s[i:]
rep('<div class="ms-emb"><img src="img/b_fundador.webp" alt="">Fundador #38', '<div class="ms-emb">${(S.rprods||[]).length?`<span class="ms-sv">🏅 ${(S.rprods||[]).length} ${(S.rprods||[]).length===1?"servicio":"servicios"}</span>`:""}<img src="img/b_fundador.webp" alt="">Fundador #38')
(V / 'reg15.html').write_text(s)
print('ok reg15', len(s))
