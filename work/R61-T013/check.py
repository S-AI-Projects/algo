from pathlib import Path
import re

source = Path('docs/extra/dynamic-programming/minimum-path-sum.md').read_text()
fences = re.findall(r'```python\s*\n(.*?)\n```', source, re.S)
assert len(fences) >= 2, 'Expected the tabulation and space-optimized Python examples'
namespace = {}
exec(fences[0], namespace)
exec(fences[1], namespace)
grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
assert namespace['min_path_sum'](grid) == 7
assert namespace['min_path_sum_optimized'](grid) == 7
assert namespace['min_path_sum']([]) == 0
assert namespace['min_path_sum_optimized']([]) == 0
print({'fixture': grid, 'tabulation': 7, 'rolling_row': 7, 'empty_grid': 0})
