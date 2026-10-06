s=open('v4/reg_src.html').read()
def R(a,b,n=1):
    global s
    c=s.count(a);assert c==n,(a[:70],c);s=s.replace(a,b)
R('<script>\n','<script>\nconst QS=new URLSearchParams(location.search),ACCT=QS.get("cuenta")==="1",ACCT_WA=QS.get("wa")||"",ACCT_NAME=QS.get("nombre")||"";\n',1)
R('<p class="sub">Crea tu cuenta para guardar tu sitio y recibir tu link.</p>','<p class="sub">${ACCT?"Revisa y publica. Tu sitio queda guardado en tu cuenta, en la pestaña Mi negocio.":"Crea tu cuenta para guardar tu sitio y recibir tu link."}</p>')
R('''   <div class="row"><div class="field"><label class="lbl" for="a-email">Correo</label><input type="email" id="a-email" value="${esc(S.account.email)}" placeholder="tunegocio@gmail.com"></div>
   <div class="field"><label class="lbl" for="a-pass">Contraseña</label><input type="password" id="a-pass" placeholder="Mínimo 8 caracteres"></div></div>''',
  '''   ${ACCT?'':`<div class="row"><div class="field"><label class="lbl" for="a-email">Correo</label><input type="email" id="a-email" value="${esc(S.account.email)}" placeholder="tunegocio@gmail.com"></div>
   <div class="field"><label class="lbl" for="a-pass">Contraseña</label><input type="password" id="a-pass" placeholder="Mínimo 8 caracteres"></div></div>`}''')
R('<button class="btn" type="submit" id="pubBtn" disabled>Crear cuenta y publicar 🎉</button>','<button class="btn" type="submit" id="pubBtn" disabled>${ACCT?"Publicar mi sitio 🎉":"Crear cuenta y publicar 🎉"}</button>')
R('''$("acct").onsubmit=e=>{e.preventDefault();const em=''','''$("acct").onsubmit=e=>{e.preventDefault();if(ACCT){publish();return;}const em=''')
R('function publish(){','function publish(){try{parent.postMessage({hqv:"negocio-publicado",nombre:S.biz.name},"*");}catch(_){}')
R('drawTypes();preview();loadCP();','if(ACCT&&ACCT_WA)S.biz.whatsapp=ACCT_WA;\nif(ACCT){const h=document.querySelector("#home h1");h.textContent=`${ACCT_NAME?ACCT_NAME+", c":"C"}onfiguremos tu negocio 💼`;document.querySelector("#home .lead").textContent="Elige qué ofreces y arma tu sitio web gratis. Todo queda guardado en tu cuenta, en esta pestaña.";document.querySelector("#home .perks").hidden=true;}\ndrawTypes();preview();loadCP();')
open('v4/reg_src.html','w').write(s);print("ok")
