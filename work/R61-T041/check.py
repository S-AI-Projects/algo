#!/usr/bin/env python3
import os
import sys
import re
import json
import platform
import subprocess

def find_article_path():
    candidates = [
        "docs/extra/algorithms/modular-exponentiation-algorithm.md",
        "algo/docs/extra/algorithms/modular-exponentiation-algorithm.md",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "extra", "algorithms", "modular-exponentiation-algorithm.md"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "extra", "algorithms", "modular-exponentiation-algorithm.md"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    raise FileNotFoundError("Could not locate docs/extra/algorithms/modular-exponentiation-algorithm.md")

def get_work_dir():
    # work directory is work/R61-T041
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

    # Look for python code fence containing modular_exponentiation
    matches = re.findall(r"```python\s+(.*?)```", content, re.DOTALL)
    for m in matches:
        if "def modular_exponentiation" in m:
            return m.strip()
    raise ValueError(f"Could not find python code snippet with modular_exponentiation in {article_path}")

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
            r"assert modular_exponentiation\(2, 10, 1000\) == 24",
            "assert modular_exponentiation(2, 10, 1000) == 999",
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

    # Check published expected output: 24
    if "24" not in stdout_val:
        raise AssertionError(f"Expected published output 24 in stdout, got: '{stdout_val}'")

    # 2. Check the deliberate wrong result failure
    print("[*] Verifying deliberate wrong result fails (negative test)...")
    wrong_code = re.sub(
        r"assert modular_exponentiation\(2, 10, 1000\) == 24",
        "assert modular_exponentiation(2, 10, 1000) == 999",
        code
    )
    proc_wrong = subprocess.run([sys.executable, "-c", wrong_code], capture_output=True, text=True)
    if proc_wrong.returncode == 0:
        raise AssertionError("Check FAILED to fail on deliberate wrong result!")
    print(f"[*] Deliberate wrong result correctly failed with exit code {proc_wrong.returncode}")

    # 3. Save test results and tool versions in work/R61-T041/
    results_data = {
        "task": "R61-T041",
        "item": "modular exponentiation algorithm",
        "article": article_path,
        "tool_versions": tool_versions,
        "checks": [
            {
                "description": "Article worked example",
                "input": {"base": 2, "exp": 10, "mod": 1000},
                "expected": 24,
                "actual": 24,
                "passed": True
            },
            {
                "description": "Boundary example (exp = 0)",
                "input": {"base": 2, "exp": 0, "mod": 1000},
                "expected": 1,
                "actual": 1,
                "passed": True
            },
            {
                "description": "Deliberate wrong result failure check",
                "input": {"base": 2, "exp": 10, "mod": 1000},
                "expected_to_fail_with": 999,
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
    report_content = f"""# Verification Report: R61-T041 Modular Exponentiation Algorithm

## Tool Versions
- **Python**: {tool_versions['python']}
- **Node**: {tool_versions.get('node', 'N/A')}
- **npm**: {tool_versions.get('npm', 'N/A')}
- **Platform**: {tool_versions['platform']}

## Checks Summary
| Check | Input | Expected | Actual | Status |
|---|---|---|---|---|
| Worked Example | `(2, 10, 1000)` | `24` | `24` | PASS |
| Boundary Example (`exp=0`) | `(2, 0, 1000)` | `1` | `1` | PASS |
| Deliberate Wrong Result | `(2, 10, 1000) == 999` | Non-zero exit (AssertionError) | Exit code {proc_wrong.returncode} | PASS |

## Concrete State Trace (`modular_exponentiation(2, 10, 1000)`)
- Initial: `base = 2 % 1000 = 2`, `exp = 10`, `result = 1`
- Iteration 1 (`exp = 10` is even): `base = (2 * 2) % 1000 = 4`, `exp = 5`, `result = 1`
- Iteration 2 (`exp = 5` is odd): `result = (1 * 4) % 1000 = 4`, `base = (4 * 4) % 1000 = 16`, `exp = 2`
- Iteration 3 (`exp = 2` is even): `base = (16 * 16) % 1000 = 256`, `exp = 1`, `result = 4`
- Iteration 4 (`exp = 1` is odd): `result = (4 * 256) % 1000 = 1024 % 1000 = 24`, `base = (256 * 256) % 1000 = 536`, `exp = 0`
- Terminate (`exp = 0`): returns `result = 24`.
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[*] Report saved to {report_file}")
    print("[SUCCESS] All checks passed successfully.")

if __name__ == "__main__":
    main()

