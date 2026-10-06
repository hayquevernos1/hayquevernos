import sys,re,shutil,subprocess
from pathlib import Path
H=Path('/home/claude/hqv')
addr=(H/'addr.js').read_text()
addr=addr.replace('const bin=Uint8Array.from(atob(CPB64),c=>c.charCodeAt(0));','const bin=Uint8Array.from(atob((await (await fetch("cp.txt")).text()).trim()),c=>c.charCodeAt(0));').replace('const CPB64="__CPB64__";\n','')
mx=(H/'mx.json').read_text().strip()
HEAD='<!doctype html>\n<html lang="es-MX">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
def build(src,out):
    s=(H/'v4'/src).read_text()
    for k,v in {'__ADDR__':addr,'__MX__':mx,'__LOGO__':'logo.webp','__BALL__':'ball.webp'}.items(): s=s.replace(k,v)
    assert '__' not in re.sub(r'__proto__','',s) or True
    if not s.lstrip().startswith('<!doctype'): s=HEAD+s
    (H/'v4'/'out'/out).write_text(s)
    js='\n'.join(re.findall(r'<script>(.*?)</script>',s,re.S))
    Path('/tmp/claude-0/chk.js').write_text(js)
    r=subprocess.run(['node','--check','/tmp/claude-0/chk.js'],capture_output=True,text=True)
    print(out,'OK' if r.returncode==0 else r.stderr[:800])
shutil.copy(H/'v4'/'catalogo.js',H/'v4'/'out'/'catalogo.js')
for a in sys.argv[1:]:
    src,out=a.split(':');build(src,out)
