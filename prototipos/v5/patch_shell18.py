"""v18 · etiqueta de versión. Correr DESPUÉS de patch_shell17.py."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()
assert 'PROTOTIPO v17' in s
s = s.replace('PROTOTIPO v17', 'PROTOTIPO v18')
P.write_text(s)
print('shell18 ok')
