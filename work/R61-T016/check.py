from pathlib import Path
import re
import subprocess

text = Path('docs/extra/basic-dsa/array/quick-sort.md').read_text()
section = text.split('### JavaScript Code Implementation', 1)[1].split('### Explanation of the Code', 1)[0]
code = re.search(r'```javascript\s*\n(.*?)\n```', section, re.S).group(1)
checks = r'''
const partitionFixture = [3, 6, 8, 10, 1, 2, 1];
const pivotIndex = QuickSort.partition(partitionFixture, 0, partitionFixture.length - 1);
if (pivotIndex !== 3 || JSON.stringify(partitionFixture) !== JSON.stringify([1, 1, 2, 3, 6, 8, 10])) process.exit(1);
const empty = [];
QuickSort.quickSort(empty, 0, empty.length - 1);
if (empty.length !== 0) process.exit(1);
console.log(JSON.stringify({pivotIndex, partitionFixture, empty}));
'''
run = subprocess.run(['node', '-e', code + '\n' + checks], text=True, capture_output=True, check=True)
assert '"pivotIndex":3' in run.stdout
assert '"partitionFixture":[1,1,2,3,6,8,10]' in run.stdout
assert '"empty":[]' in run.stdout
print(run.stdout.strip())
