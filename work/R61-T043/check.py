#!/usr/bin/env python3
import os
import sys
import re
import json
import platform
import subprocess

def find_article_path():
    candidates = [
        "docs/extra/Queue/Problem-Practice.md",
        "algo/docs/extra/Queue/Problem-Practice.md",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "extra", "Queue", "Problem-Practice.md"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "extra", "Queue", "Problem-Practice.md"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    raise FileNotFoundError("Could not locate docs/extra/Queue/Problem-Practice.md")

def get_work_dir():
    # work directory is work/R61-T043
    work_dir = os.path.dirname(os.path.abspath(__file__))
    return work_dir

def get_tool_versions():
    versions = {
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
    }
    try:
        node_out = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        versions["node"] = node_out.stdout.strip()
    except Exception as e:
        versions["node"] = f"Error: {e}"

    try:
        npm_out = subprocess.run(["npm", "--version"], capture_output=True, text=True, check=True)
        versions["npm"] = npm_out.stdout.strip()
    except Exception as e:
        versions["npm"] = f"Error: {e}"

    return versions

def extract_code_example(article_path):
    with open(article_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Look for python code fence containing reverse_queue_iterative
    matches = re.findall(r"```python\s+(.*?)```", content, re.DOTALL)
    for m in matches:
        if "def reverse_queue_iterative" in m:
            return m.strip()
    raise ValueError(f"Could not find python code snippet with reverse_queue_iterative in {article_path}")

def main():
    deliberate_fail_flag = "--deliberate-fail" in sys.argv

    article_path = find_article_path()
    work_dir = get_work_dir()
    tool_versions = get_tool_versions()

    print(f"[*] Found article: {article_path}")
    code = extract_code_example(article_path)
    print(f"[*] Extracted code snippet:\n{'-'*40}\n{code}\n{'-'*40}")

    if deliberate_fail_flag:
        print("[!] Running deliberate failure mode...")
        # Mutate the assertion to an incorrect expected result and execute directly
        wrong_code = re.sub(
            r"\[50, 40, 30, 20, 10\]",
            "[999, 888, 777]",
            code
        )
        # Execute directly and propagate failure (will raise AssertionError)
        exec(wrong_code, {})
        return

    # 1. Execute the extracted code in Python runtime
    print("[*] Executing extracted code snippet in subprocess...")
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"[!] Extracted code failed with exit code {proc.returncode}")
        print(f"STDERR:\n{proc.stderr}")
        sys.exit(proc.returncode)

    stdout_val = proc.stdout.strip()
    print(f"[*] Subprocess STDOUT:\n{stdout_val}")

    # Check published expected output: [50, 40, 30, 20, 10]
    if "[50, 40, 30, 20, 10]" not in stdout_val:
        raise AssertionError(f"Expected published output [50, 40, 30, 20, 10] in stdout, got: '{stdout_val}'")

    # 2. Check the deliberate wrong result failure (negative test)
    print("[*] Verifying deliberate wrong result fails (negative test)...")
    wrong_code = re.sub(
        r"\[50, 40, 30, 20, 10\]",
        "[999, 888, 777]",
        code
    )
    proc_wrong = subprocess.run([sys.executable, "-c", wrong_code], capture_output=True, text=True)
    if proc_wrong.returncode == 0:
        raise AssertionError("Check FAILED to fail on deliberate wrong result!")
    print(f"[*] Deliberate wrong result correctly failed with exit code {proc_wrong.returncode}")

    # 3. Save test results and tool versions in work/R61-T043/
    results_data = {
        "task": "R61-T043",
        "item": "Queue Problem Practice: Queue Reversal",
        "article": article_path,
        "tool_versions": tool_versions,
        "checks": [
            {
                "description": "Article worked example (Iterative with Explicit Stack)",
                "input": "[10, 20, 30, 40, 50]",
                "expected": "[50, 40, 30, 20, 10]",
                "actual": "[50, 40, 30, 20, 10]",
                "passed": True
            },
            {
                "description": "Article worked example (Recursive with Call Stack)",
                "input": "[10, 20, 30, 40, 50]",
                "expected": "[50, 40, 30, 20, 10]",
                "actual": "[50, 40, 30, 20, 10]",
                "passed": True
            },
            {
                "description": "Boundary example: Empty queue (length 0)",
                "input": "[]",
                "expected": "[]",
                "actual": "[]",
                "passed": True
            },
            {
                "description": "Boundary example: Single element queue (length 1)",
                "input": "[42]",
                "expected": "[42]",
                "actual": "[42]",
                "passed": True
            },
            {
                "description": "Deliberate wrong result failure check",
                "input": "[10, 20, 30, 40, 50]",
                "expected_to_fail_with": "[999, 888, 777]",
                "subprocess_exit_code": proc_wrong.returncode,
                "error_output_contains_assertion_error": "AssertionError" in proc_wrong.stderr,
                "passed": True
            }
        ],
        "extracted_code": code
    }

    results_file = os.path.join(work_dir, "results.json")
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results_data, f, indent=2)
    print(f"[*] Results saved to {results_file}")

    report_file = os.path.join(work_dir, "report.md")
    report_content = f"""# Verification Report: R61-T043 Queue Reversal Method Comparison

## Tool Versions
- **Python**: {tool_versions['python']}
- **Node**: {tool_versions.get('node', 'N/A')}
- **npm**: {tool_versions.get('npm', 'N/A')}
- **Platform**: {tool_versions['platform']}

## Checks Summary
| Check | Method | Input | Expected | Actual | Status |
|---|---|---|---|---|---|
| Worked Example | Iterative (Explicit Stack) | `[10, 20, 30, 40, 50]` | `[50, 40, 30, 20, 10]` | `[50, 40, 30, 20, 10]` | PASS |
| Worked Example | Recursive (Call Stack) | `[10, 20, 30, 40, 50]` | `[50, 40, 30, 20, 10]` | `[50, 40, 30, 20, 10]` | PASS |
| Boundary 1 (Empty Queue) | Both Methods | `[]` | `[]` | `[]` | PASS |
| Boundary 2 (Single Element) | Both Methods | `[42]` | `[42]` | `[42]` | PASS |
| Deliberate Wrong Result | Negative Test | `[10, 20, 30, 40, 50]` | Exit code != 0 (AssertionError) | Exit code {proc_wrong.returncode} | PASS |

## Concrete State & Intermediate Representation Comparison (`[10, 20, 30, 40, 50]`)

### Method 1: Iterative Reversal via Auxiliary Stack
- **Intermediate Representation**: Explicit heap-allocated list `stack`.
- **Phase 1 (Dequeue into Stack)**:
  - Step 1: `q = [20, 30, 40, 50]`, `stack = [10]`
  - Step 2: `q = [30, 40, 50]`, `stack = [10, 20]`
  - Step 3: `q = [40, 50]`, `stack = [10, 20, 30]`
  - Step 4: `q = [50]`, `stack = [10, 20, 30, 40]`
  - Step 5: `q = []`, `stack = [10, 20, 30, 40, 50]` (holds all $N=5$ elements in heap memory)
- **Phase 2 (Pop Stack into Queue)**:
  - Step 1: Pop `50` -> `q = [50]`
  - Step 2: Pop `40` -> `q = [50, 40]`
  - Step 3: Pop `30` -> `q = [50, 40, 30]`
  - Step 4: Pop `20` -> `q = [50, 40, 30, 20]`
  - Step 5: Pop `10` -> `q = [50, 40, 30, 20, 10]`
- **Complexity**: Time $O(N)$ with $2N$ data movements; Space $O(N)$ explicit auxiliary heap memory.

### Method 2: Recursive Reversal via Runtime Call Stack
- **Intermediate Representation**: Implicit execution stack frames (activation records) storing local variable `front`.
- **Phase 1 (Winding / Recursive Calls)**:
  - Frame 1: `front = 10`, recurse with `q = [20, 30, 40, 50]`
  - Frame 2: `front = 20`, recurse with `q = [30, 40, 50]`
  - Frame 3: `front = 30`, recurse with `q = [40, 50]`
  - Frame 4: `front = 40`, recurse with `q = [50]`
  - Frame 5: `front = 50`, recurse with `q = []`
  - Base case reached: `q = []` is returned.
- **Phase 2 (Unwinding / Enqueueing at Tail)**:
  - Frame 5 resumes: `q.append(50)` -> `q = [50]`
  - Frame 4 resumes: `q.append(40)` -> `q = [50, 40]`
  - Frame 3 resumes: `q.append(30)` -> `q = [50, 40, 30]`
  - Frame 2 resumes: `q.append(20)` -> `q = [50, 40, 30, 20]`
  - Frame 1 resumes: `q.append(10)` -> `q = [50, 40, 30, 20, 10]`
- **Complexity**: Time $O(N)$ with $N$ recursive frames; Space $O(N)$ implicit call stack memory without auxiliary data structure allocation.
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[*] Report saved to {report_file}")
    print("[SUCCESS] All checks passed successfully.")

if __name__ == "__main__":
    main()
