import re, subprocess, sys
from pathlib import Path

t = Path("docs/extra/Queue/priority-queue.md").read_text(encoding="utf-8")
sec = t.split("#### Python Implementation", 1)[1].split("#### C++ Implementation", 1)[0]
py = re.search(r"```python\n(.*?)\n```", sec, re.DOTALL).group(1)
out = re.search(r"##### Example Output\s+```plaintext\n(.*?)\n```", sec, re.DOTALL).group(1).strip()

act = subprocess.run([sys.executable, "-c", py], capture_output=True, text=True, check=True).stdout.strip()
assert act == out, f"Mismatch:\n{act}\n!=\n{out}"
assert act != out.replace("('Task 2', 1)", "('Task 1', 2)", 1)
print("PASS: Published Priority Queue Python example executed and matched expected output.")
print(act)
