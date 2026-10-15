"""v22 · etiqueta de versión. Correr DESPUÉS de patch_shell21.py."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()
assert 'PROTOTIPO v21' in s
s = s.replace('PROTOTIPO v21', 'PROTOTIPO v22')
P.write_text(s)
print('shell22 ok')
