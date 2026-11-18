import re, subprocess, tempfile
from pathlib import Path

t = Path("docs/languages/Rust/rust-5.md").read_text(encoding="utf-8")
sec = t.split("## Function Invariant and Bounded Variations", 1)[1]
rs = re.search(r"```rust\n(.*?)\n```", sec, re.DOTALL).group(1)
out = re.search(r"### Output\s+```text\n(.*?)\n```", sec, re.DOTALL).group(1).strip()
with tempfile.TemporaryDirectory() as d:
    src, exe = Path(d) / "main.rs", Path(d) / "main"
    src.write_text(rs, encoding="utf-8")
    subprocess.run(["rustc", str(src), "-o", str(exe)], check=True)
    act = subprocess.run([str(exe)], capture_output=True, text=True, check=True).stdout.strip()
assert act == out, f"Mismatch:\n{act}\n!=\n{out}"
assert act != out.replace("sum(3, 7)): 10", "sum(3, 7)): 99", 1)
print("PASS: Published Rust Functions invariant example compiled and matched expected output.")
print(act)
