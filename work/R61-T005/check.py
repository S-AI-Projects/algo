#!/usr/bin/env python3
"""Execute the exact Python code block published in the Round Robin article."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / "docs/extra/cpu-scheduling-algorithms/round-robin.md"
EXPECTED = """
Gantt Chart:

    idle        p1        p2        p3        p1        p3        p4        p3
0         2         5         8         11         13         16         18         19

Turn Around Time:
p1: 11
p2: 5
p3: 14
p4: 6
Average turn around time =  9.0

Waiting Time:
p1: 6
p2: 2
p3: 7
p4: 4
Average waiting time =  4.75

Response Time:
p1: 0
p2: 2
p3: 3
p4: 4
Average response time =  2.25

Boundary: solo completes at 1 (turnaround=1, waiting=0, response=0)
""".lstrip("\n")


def main() -> None:
    text = ARTICLE.read_text(encoding="utf-8")
    heading = text.index("## 7. Python Implementation")
    start = text.index("```python", heading) + len("```python")
    code = text[start:text.index("```", start)].strip() + "\n"
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as source:
        source.write(code)
        source.flush()
        actual = subprocess.check_output([sys.executable, source.name], text=True, stderr=subprocess.STDOUT)
    if actual != EXPECTED:
        raise AssertionError(f"output mismatch\nexpected:\n{EXPECTED}\nactual:\n{actual}")
    out = Path(__file__).parent
    (out / "inputs.txt").write_text("p1 2 5; p2 3 3; p3 5 7; p4 12 2; quantum=3\nBoundary: solo arrives at 0, burst=1, quantum=1\n", encoding="utf-8")
    (out / "expected.txt").write_text(EXPECTED, encoding="utf-8")
    (out / "actual.txt").write_text(actual, encoding="utf-8")
    (out / "tool-versions.txt").write_text(f"{sys.version.splitlines()[0]}\n", encoding="utf-8")
    print("PASS: published worked schedule and isolated one-process boundary match exactly.")


if __name__ == "__main__":
    main()
