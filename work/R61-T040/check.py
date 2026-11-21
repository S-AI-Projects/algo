import re, subprocess, sys
from pathlib import Path

t = Path("docs/extra/algorithms/Scheduling Algorithms/EarliestDeadlineFirst.md").read_text(encoding="utf-8")
py = re.search(r"```python\n(.*?)\n```", t, re.DOTALL).group(1)
out = re.search(r"## Example Output.*?```plaintext\n(.*?)\n```", t, re.DOTALL).group(1).strip()

act = subprocess.run([sys.executable, "-c", py], capture_output=True, text=True, check=True).stdout.strip()
assert act == out, f"Mismatch:\n{act!r}\n!=\n{out!r}"

# Temporary one-operation mutant: drop cumulative wait_times[i - 1]
mutant_py = py.replace(" + wait_times[i - 1]", "", 1)
assert mutant_py != py, "Mutant substitution failed"
mutant_out = subprocess.run([sys.executable, "-c", mutant_py], capture_output=True, text=True, check=True).stdout.strip()
assert act != mutant_out, "Check failed to distinguish one-operation mutant"
assert mutant_out != out, "Mutant unexpectedly matched expected output"

print("PASS: Published EDF example matched expected output and killed one-operation mutant.")
print(act)
