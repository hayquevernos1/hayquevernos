"""v19 · etiqueta de versión. Correr DESPUÉS de patch_shell18.py."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()
assert 'PROTOTIPO v18' in s
s = s.replace('PROTOTIPO v18', 'PROTOTIPO v19')
P.write_text(s)
print('shell19 ok')
