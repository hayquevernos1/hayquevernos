"""v13 · Registro (Diego, 9 oct 2026). reg7.html → reg8.html
- En el sitio público solo se menciona la negociación cuando es un plus («🤝 Precios negociables»); si es precio fijo no se dice nada."""
from pathlib import Path
s = Path('/home/claude/hqv/v5/reg7.html').read_text()
a = '''${p.negotiable?'<span>🤝 Costos negociables</span>':p.negotiable===false?'<span>Precio fijo</span>':""}'''
assert a in s
s = s.replace(a, '''${p.negotiable?'<span>🤝 Precios negociables</span>':""}''')
s = s.replace("'<span>Precio fijo</span>'", '""')
Path('/home/claude/hqv/v5/reg8.html').write_text(s)
print('reg8 ok')
