import re, subprocess
from pathlib import Path

t = Path("docs/extra/basic-dsa/array/arrays-insertionsort.md").read_text(encoding="utf-8")
js = re.search(r"```javascript[^\n]*\n(.*?)\n```", t, re.DOTALL).group(1)
out = re.search(r"## Example Output.*?```plaintext\n(.*?)\n```", t, re.DOTALL).group(1).strip()
act = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout.strip()
assert act == out, f"Mismatch:\n{act}\n!=\n{out}"
assert act != out.replace("[ 5, 6, 11, 12, 13 ]", "[ 5, 6, 11, 13, 12 ]", 1)
print("PASS: Published Insertion Sort example executed and matched expected output.")
print(act)
