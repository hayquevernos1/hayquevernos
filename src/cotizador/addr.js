/* ---------- Dirección asegurada: CP → estado, municipio y colonias (catálogo SEPOMEX) + confirmación en mapa ---------- */
const CPB64="__CPB64__";
let CPDB=null,CPLOAD=null;
function loadCP(){if(CPLOAD)return CPLOAD;CPLOAD=(async()=>{try{if(typeof DecompressionStream==="undefined")throw 0;const bin=Uint8Array.from(atob(CPB64),c=>c.charCodeAt(0));const txt=await new Response(new Blob([bin]).stream().pipeThrough(new DecompressionStream("gzip"))).text();CPDB=JSON.parse(txt);}catch(e){CPDB=false;}return CPDB;})();return CPLOAD;}
const blankAddr=()=>({cp:"",state:"",muni:"",col:"",colOther:"",street:"",num:"",int:"",ref:"",ok:false,manual:false,found:false});
function cpLookup(cp){if(!CPDB||!/^\d{5}$/.test(cp))return null;const e=CPDB.c[cp];return e?{state:CPDB.s[e[0]],muni:e[1],cols:e[2]}:null;}
const addrOk=a=>/^\d{5}$/.test(a.cp)&&!!a.state&&!!a.muni&&(!!a.col&&a.col!=="__otra"||String(a.colOther).trim()!=="")&&String(a.street).trim()!==""&&String(a.num).trim()!==""&&a.ok;
const addrText=a=>[`${a.street} ${a.num}${a.int?" int. "+a.int:""}`.trim(),a.col==="__otra"?a.colOther:a.col,a.cp?"CP "+a.cp:"",a.muni,a.state].filter(x=>String(x).trim()).join(", ");
const addrShort=a=>[a.col==="__otra"?a.colOther:a.col,a.muni].filter(Boolean).join(", ");
const addrMap=a=>"https://www.google.com/maps/search/?api=1&query="+encodeURIComponent(addrText(a));
const okHtml=(a,k)=>a.street&&a.num&&(a.col&&a.col!=="__otra"||a.colOther)?`<div class="addr-ok"><a href="${addrMap(a)}" target="_blank" rel="noopener">📍 Revisar en el mapa</a><label class="chk-in"><input type="checkbox" id="aok-${k}" ${a.ok?'checked':''}> Confirmo que la dirección es correcta</label></div>`:`<span class="hint">Al terminar, revisa tu dirección en el mapa y confírmala.</span>`;
function addrBlock(a,k,title,missFn,showRef){const M=missFn||(()=>"");const look=cpLookup(a.cp);
 const status=!/^\d{5}$/.test(a.cp)?`<span class="hint">🔎 Escribe tu código postal y llenamos estado, municipio y colonia por ti.</span>`
  :CPDB===null?`<span class="hint">⏳ Buscando tu código postal…</span>`
  :look?`<span class="hint" style="color:var(--mint);font-weight:600">✅ ${esc(look.muni)}, ${esc(look.state)}</span>`
  :a.manual?`<span class="hint">✍️ Llenando a mano</span>`:`<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap"><span class="hint" style="color:var(--bad);font-weight:600">No encontramos ese código postal. Revísalo, o</span><button type="button" class="link-btn" id="am-${k}">llénala a mano</button></div>`;
 const cols=look?look.cols:[];
 return`<div class="field"><span class="lbl">📍 ${title}</span><div class="addr-box${M(addrOk(a))}">
  <div class="addr-cp"><input type="text" inputmode="numeric" maxlength="5" id="acp-${k}" value="${esc(a.cp)}" placeholder="Código postal" aria-label="Código postal">${status}</div>
  ${look||a.manual?`
   ${a.manual&&!look?`<div class="row"><select id="ast-${k}" aria-label="Estado"><option value="">Estado</option>${Object.keys(MX).map(s=>`<option ${s===a.state?'selected':''}>${esc(s)}</option>`).join("")}</select><select id="amu-${k}" aria-label="Municipio" ${a.state?'':'disabled'}><option value="">Municipio o alcaldía</option>${(MX[a.state]||[]).map(m=>`<option ${m===a.muni?'selected':''}>${esc(m)}</option>`).join("")}</select></div>
    <input type="text" id="aco-${k}" value="${esc(a.colOther)}" placeholder="Colonia" aria-label="Colonia">`
   :`<select id="acl-${k}" aria-label="Colonia"><option value="">Elige tu colonia</option>${cols.map(c=>`<option ${c===a.col?'selected':''}>${esc(c)}</option>`).join("")}<option value="__otra" ${a.col==="__otra"?'selected':''}>Mi colonia no aparece</option></select>
    ${a.col==="__otra"?`<input type="text" id="aco-${k}" value="${esc(a.colOther)}" placeholder="Escribe tu colonia" aria-label="Colonia">`:''}`}
   <div class="addr-street"><input type="text" id="asr-${k}" value="${esc(a.street)}" placeholder="Calle" aria-label="Calle"><input type="text" id="anu-${k}" value="${esc(a.num)}" placeholder="Núm. ext." aria-label="Número exterior"><input type="text" id="ain-${k}" value="${esc(a.int)}" placeholder="Int. (opc.)" aria-label="Número interior"></div>
   ${showRef?`<input type="text" id="arf-${k}" value="${esc(a.ref)}" placeholder="Referencias para llegar (opcional)" aria-label="Referencias">`:''}
   <div id="aokw-${k}">${okHtml(a,k)}</div>`:''}
 </div></div>`;}
function bindAddrBlock(a,k,changed,redraw){const g=id=>document.getElementById(id+"-"+k);
 const bindOk=()=>{const ok=g("aok");if(ok)ok.onchange=e=>{a.ok=e.target.checked;changed();};};
 const reset=()=>{a.ok=false;const w=g("aokw");if(w){w.innerHTML=okHtml(a,k);bindOk();}};
 g("acp").oninput=e=>{const v=e.target.value.replace(/\D/g,"").slice(0,5);e.target.value=v;if(v===a.cp)return;a.cp=v;a.ok=false;a.col="";a.colOther="";
  if(v.length===5){const go=()=>{const l=cpLookup(v);if(l){a.state=l.state;a.muni=l.muni;a.manual=false;if(l.cols.length===1)a.col=l.cols[0];}redraw();changed();setTimeout(()=>{const n=g("acl")||g("asr");n&&n.focus();},0);};if(CPDB===null){redraw();loadCP().then(go);}else go();}
  else{if(!a.manual){a.state="";a.muni="";}changed();}};
 const am=g("am");if(am)am.onclick=()=>{a.manual=true;redraw();};
 const st=g("ast");if(st)st.onchange=e=>{a.state=e.target.value;a.muni="";reset();redraw();changed();};
 const mu=g("amu");if(mu)mu.onchange=e=>{a.muni=e.target.value;reset();changed();};
 const cl=g("acl");if(cl)cl.onchange=e=>{a.col=e.target.value;reset();redraw();changed();};
 [["aco","colOther"],["asr","street"],["anu","num"],["ain","int"],["arf","ref"]].forEach(([id,f])=>{const el=g(id);if(el)el.oninput=e=>{a[f]=e.target.value;if(f!=="ref")reset();changed();};});
 bindOk();}
