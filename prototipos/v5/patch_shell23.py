"""v23 · etiqueta de versión. Correr DESPUÉS de patch_shell21.py."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()
assert 'PROTOTIPO v22' in s
s = s.replace('PROTOTIPO v22', 'PROTOTIPO v23')
P.write_text(s)
print('shell23 ok')
