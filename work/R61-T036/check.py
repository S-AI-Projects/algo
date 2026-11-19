import re, subprocess, tempfile
from pathlib import Path

t = Path("docs/extra/graphs/graph-reversal.md").read_text(encoding="utf-8")
cpp = re.search(r"```cpp\n(.*?)\n```", t, re.DOTALL).group(1)
out = re.search(r"### Example Output\s+```plaintext\n(.*?)\n```", t, re.DOTALL).group(1).strip()
with tempfile.TemporaryDirectory() as d:
    src, exe = Path(d) / "main.cpp", Path(d) / "main"
    src.write_text(cpp, encoding="utf-8")
    subprocess.run(["g++", "-std=c++17", str(src), "-o", str(exe)], check=True)
    act = subprocess.run([str(exe)], capture_output=True, text=True, check=True).stdout.strip()
assert act == out, f"Mismatch:\n{act}\n!=\n{out}"
assert act != out.replace("[ 0 3 ]", "[ 3 0 ]", 1)
print("PASS: Published Graph Reversal C++ example compiled and matched expected output.")
print(act)
