import re,shutil,subprocess,sys
from pathlib import Path
H=Path('/home/claude/hqv');V=H/'v5';O=V/'out';O.mkdir(exist_ok=True)
addr=(H/'addr.js').read_text()
addr=addr.replace('const bin=Uint8Array.from(atob(CPB64),c=>c.charCodeAt(0));','const bin=Uint8Array.from(atob((await (await fetch("cp.txt")).text()).trim()),c=>c.charCodeAt(0));').replace('const CPB64="__CPB64__";\n','')
mx=(H/'mx.json').read_text().strip()
HEAD='<!doctype html>\n<html lang="es-MX">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
def check(name,s):
    js='\n'.join(re.findall(r'<script>(.*?)</script>',s,re.S))
    Path('/tmp/claude-0/chk.js').write_text(js)
    r=subprocess.run(['node','--check','/tmp/claude-0/chk.js'],capture_output=True,text=True)
    print(name,'OK' if r.returncode==0 else r.stderr[:1200])
def build(src,out,doctype=True):
    s=(V/src).read_text()
    for k,v in {'__ADDR__':addr,'__MX__':mx,'__LOGO__':'img/logo.webp','__BALL__':'img/ball.webp'}.items(): s=s.replace(k,v)
    s=s.replace('"logo.webp"','"img/logo.webp"').replace('"ball.webp"','"img/ball.webp"').replace('src="logo.webp"','src="img/logo.webp"').replace('src="ball.webp"','src="img/ball.webp"')
    if doctype and not s.lstrip().startswith('<!doctype'): s=HEAD+s
    (O/out).write_text(s); check(out,s)
for f in ['catalogo.js','catalogo_servicios.js','venue_draw.js','config.js','marca.css','cp.txt']: shutil.copy(V/f,O/f)
if (O/'img').exists(): shutil.rmtree(O/'img')
shutil.copytree(V/'img',O/'img')
build('reg6.html' if (V/'reg6.html').exists() else 'reg5.html','negocio.html'); build('cot5.html','fiestas.html')
if (V/'shell.html').exists(): build('shell.html','index.html',doctype=False)
if (V/'pagos5.html').exists(): build('pagos5.html','pagos.html')
