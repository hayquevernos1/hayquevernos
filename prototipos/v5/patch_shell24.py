"""v24 · etiqueta de versión. Correr DESPUÉS de patch_shell21.py."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()
assert 'PROTOTIPO v23' in s
s = s.replace('PROTOTIPO v23', 'PROTOTIPO v24')
P.write_text(s)
print('shell24 ok')
