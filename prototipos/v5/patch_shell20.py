"""v20 · etiqueta de versión. Correr DESPUÉS de patch_shell19.py."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()
assert 'PROTOTIPO v19' in s
s = s.replace('PROTOTIPO v19', 'PROTOTIPO v20')
P.write_text(s)
print('shell20 ok')
