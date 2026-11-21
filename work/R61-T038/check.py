import re, subprocess, sys
from pathlib import Path

t = Path("docs/extra/string-algorithms/manachers-algorithm.md").read_text(encoding="utf-8")
py = re.search(r"## Runnable Python Example\s+```python\n(.*?)\n```", t, re.DOTALL).group(1)
out = re.search(r"### Example Output\s+```plaintext\n(.*?)\n```", t, re.DOTALL).group(1).strip()

act = subprocess.run([sys.executable, "-c", py], capture_output=True, text=True, check=True).stdout.strip()
assert act == out, f"Mismatch:\n{act}\n!=\n{out}"
assert act != out.replace("longest='bab'", "longest='aba'", 1)
print("PASS: Published Manacher's Algorithm Python example executed and matched expected output.")
print(act)
