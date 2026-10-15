"""v25 · etiqueta de versión. Correr DESPUÉS de patch_shell24.py."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()
assert 'PROTOTIPO v24' in s
s = s.replace('PROTOTIPO v24', 'PROTOTIPO v25')
P.write_text(s)
print('shell25 ok')
