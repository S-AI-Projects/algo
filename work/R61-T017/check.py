from pathlib import Path
import re
import subprocess

text = Path('docs/languages/javascript/js-6.md').read_text()
section = text.split('### 1. Implicit Type Casting', 1)[1].split('### 2. Explicit Type Casting', 1)[0]
fences = re.findall(r'```javascript\s*\n(.*?)\n```', section, re.S)
assert len(fences) == 2
script = '\n'.join(fences) + r'''
const actual = {result, difference, truthy, resultType: typeof result, differenceType: typeof difference, joinedZero, numericZero};
console.log(JSON.stringify(actual));
'''
run = subprocess.run(['node', '-e', script], text=True, capture_output=True, check=True)
expected = {'result':'53','difference':8,'truthy':True,'resultType':'string','differenceType':'number','joinedZero':'00','numericZero':0}
assert expected == __import__('json').loads(run.stdout)
print(run.stdout.strip())
