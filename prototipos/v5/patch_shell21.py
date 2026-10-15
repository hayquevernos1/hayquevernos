"""v21 · etiqueta de versión. Correr DESPUÉS de patch_shell20.py."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()
assert 'PROTOTIPO v20' in s
s = s.replace('PROTOTIPO v20', 'PROTOTIPO v21')
P.write_text(s)
print('shell21 ok')
