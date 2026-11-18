import os, re, subprocess, sys
from pathlib import Path

t = Path("docs/extra/machine-learning/Long_Short_Term_Memory.md").read_text(encoding="utf-8")
py = re.search(r"```python\n(.*?)\n```", t, re.DOTALL).group(1)
out = re.search(r"### Example Output\s+```plaintext\n(.*?)\n```", t, re.DOTALL).group(1).strip()
runs = []
for seed in ("1", "999"):
    env = os.environ.copy()
    env["PYTHONHASHSEED"] = seed
    runs.append(subprocess.run([sys.executable, "-c", py], capture_output=True, text=True, check=True, env=env).stdout.strip())
assert runs[0] == runs[1] == out, f"Mismatch:\n{runs[0]}\n!=\n{out}"
assert runs[0] != out.replace("Positive", "Negative", 1)
print("PASS: Published LSTM example is deterministic across PYTHONHASHSEEDs and matched expected output.")
print(runs[0])
