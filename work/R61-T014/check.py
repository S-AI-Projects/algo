from pathlib import Path
import re

text = Path('docs/languages/python/py-1.md').read_text()
section = text.split('### a. Integers (`int`)', 1)[1].split('### b. Floating-Point', 1)[0]
fences = re.findall(r'```python\s*\n(.*?)\n```', section, re.S)
assert len(fences) == 2
ns = {}
exec(fences[0], ns)
exec(fences[1], ns)
assert ns['x'] == 4 and ns['y'] == -21
for a, b in [(0, 0), (1, 2), (-1, 2), (2, -1), (-8, -13), (1000, -997)]:
    result = a + b
    assert type(a) is int and type(b) is int and type(result) is int
print('fixture and six bounded variations preserve int under addition')
