"""v27 · etiqueta de versión. Correr DESPUÉS de patch_shell26.py."""
from pathlib import Path
P = Path('/home/claude/hqv/v5/shell.html')
s = P.read_text()
assert 'PROTOTIPO v26' in s
s = s.replace('PROTOTIPO v26', 'PROTOTIPO v27')
P.write_text(s)
print('shell27 ok')
