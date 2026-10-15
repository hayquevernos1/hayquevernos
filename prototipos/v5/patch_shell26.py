"""v26 · etiqueta de versión. Correr DESPUÉS de patch_shell25.py."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()
assert 'PROTOTIPO v25' in s
s = s.replace('PROTOTIPO v25', 'PROTOTIPO v26')
P.write_text(s)
print('shell26 ok')
