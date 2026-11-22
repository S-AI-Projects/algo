from pathlib import Path
import re
import subprocess
import tempfile

text = Path('docs/extra/algorithms/Searching Algorithms/InterpolationSearch.md').read_text()
section = text.split('**Iterative Approach**:', 1)[1].split('**Recursive Approach**:', 1)[0]
code = re.search(r'```cpp\s*\n(.*?)\n```', section, re.S).group(1)
with tempfile.TemporaryDirectory() as directory:
    source = Path(directory) / 'example.cpp'
    executable = Path(directory) / 'example'
    source.write_text(code)
    subprocess.run(['g++', '-std=c++17', str(source), '-o', str(executable)], check=True)
    run = subprocess.run([str(executable)], text=True, capture_output=True, check=True)
expected = '''Element found at index 4
Repeated value index: 0
Repeated value absent: -1
Empty input: -1
'''
assert run.stdout == expected, (run.stdout, expected)
print(run.stdout, end='')
