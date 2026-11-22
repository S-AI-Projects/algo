from pathlib import Path
import re
import sys

text = Path('docs/extra/advance-data-structure/heavy-light-decomposition.md').read_text()
section = text.split('### Python', 1)[1].split('### Pseudo Code', 1)[0]
fences = re.findall(r'```python\s*\n(.*?)\n```', section, re.S)
assert len(fences) == 2
old_limit = sys.getrecursionlimit()
ns = {'sys': sys}
exec(fences[0], ns)
assert sys.getrecursionlimit() == old_limit
exec(fences[1], ns)
assert sys.getrecursionlimit() == old_limit
assert ns['hld'].path_query(3, 2) == 9
assert ns['single'].path_query(0, 0) == -3
print({'path_3_to_2_max': 9, 'single_node': -3, 'recursion_limit_restored': old_limit})
