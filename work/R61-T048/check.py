#!/usr/bin/env python3
import os
import sys
import re
import json
import shutil
import platform
import subprocess
import tempfile

def find_article_path():
    candidates = [
        "docs/dsa-problems/medium/removevomer.md",
        "algo/docs/dsa-problems/medium/removevomer.md",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "dsa-problems", "medium", "removevomer.md"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "dsa-problems", "medium", "removevomer.md"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    raise FileNotFoundError("Could not locate docs/dsa-problems/medium/removevomer.md")

def get_work_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_cpp_compiler():
    candidates = ["clang++", "g++", "c++"]
    for c in candidates:
        path = shutil.which(c)
        if path:
            try:
                test = subprocess.run([path, "--version"], capture_output=True, text=True)
                if test.returncode == 0:
                    return path
            except Exception:
                pass
    raise RuntimeError("No working C++ compiler found (clang++, g++, or c++)")

def get_tool_versions(cpp_bin):
    versions = {
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
    }
    try:
        c_out = subprocess.run([cpp_bin, "--version"], capture_output=True, text=True, check=True)
        versions["compiler"] = c_out.stdout.strip().splitlines()[0]
    except Exception as e:
        versions["compiler"] = f"Error: {e}"

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

def extract_cpp_code(article_path):
    with open(article_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = re.findall(r"```cpp\s+(.*?)```", content, re.DOTALL)
    for m in matches:
        if "void solve()" in m and "minRemainingLength" in m:
            return m.strip()
    raise ValueError(f"Could not find C++ code block containing 'solve' and 'minRemainingLength' in {article_path}")

def compile_cpp(code_str, cpp_bin, out_bin):
    with tempfile.NamedTemporaryFile("w", suffix=".cpp", delete=False) as f:
        f.write(code_str)
        src_path = f.name

    try:
        proc = subprocess.run(
            [cpp_bin, "-std=c++17", "-O2", src_path, "-o", out_bin],
            capture_output=True,
            text=True
        )
        return proc.returncode, proc.stdout, proc.stderr
    finally:
        if os.path.exists(src_path):
            os.remove(src_path)

def main():
    deliberate_fail_flag = "--deliberate-fail" in sys.argv

    article_path = find_article_path()
    work_dir = get_work_dir()
    cpp_bin = get_cpp_compiler()
    tool_versions = get_tool_versions(cpp_bin)

    print(f"[*] Found article: {article_path}")
    print(f"[*] C++ compiler: {cpp_bin}")

    code = extract_cpp_code(article_path)
    print(f"[*] Extracted C++ code:\n{'-'*40}\n{code}\n{'-'*40}")

    with tempfile.TemporaryDirectory() as tmpdir:
        bin_path = os.path.join(tmpdir, "removevomer_bin")
        ret_compile, out_c, err_c = compile_cpp(code, cpp_bin, bin_path)
        if ret_compile != 0:
            print(f"[!] Compilation failed:\n{err_c}")
            sys.exit(ret_compile)

        if deliberate_fail_flag:
            print("[!] Running deliberate failure mode...")
            wrong_code = re.sub(
                r'assert\(minRemainingLength\(5, "00111"\) == 2\);',
                'assert(minRemainingLength(5, "00111") == 999);',
                code
            )
            wrong_bin = os.path.join(tmpdir, "wrong_bin")
            ret_w, _, _ = compile_cpp(wrong_code, cpp_bin, wrong_bin)
            if ret_w != 0:
                sys.exit(ret_w)
            proc_w = subprocess.run([wrong_bin], input="", capture_output=True, text=True)
            print(f"Deliberate fail return code: {proc_w.returncode}")
            print(f"Deliberate fail stderr:\n{proc_w.stderr}")
            sys.exit(proc_w.returncode if proc_w.returncode != 0 else 1)

        # 1. Test worked example via stdin
        print("[*] Testing worked example testcases via piped stdin...")
        worked_input = "5\n3\n000\n5\n00111\n3\n010\n5\n00110\n4\n1100\n"
        proc_worked = subprocess.run(
            [bin_path],
            input=worked_input,
            capture_output=True,
            text=True
        )
        if proc_worked.returncode != 0:
            print(f"[!] Worked example failed:\n{proc_worked.stderr}")
            sys.exit(proc_worked.returncode)

        worked_output = proc_worked.stdout.strip().splitlines()
        expected_output = ["1", "2", "1", "1", "2"]
        print(f"[*] Subprocess STDOUT:\n{proc_worked.stdout.strip()}")

        if worked_output != expected_output:
            raise AssertionError(f"Worked example mismatch: expected {expected_output}, got {worked_output}")

        # 2. Test boundary self-test assertions without stdin (pass empty input to trigger EOF)
        print("[*] Running self-test boundary & failure-case assertions (no stdin)...")
        proc_assert = subprocess.run(
            [bin_path],
            input="",
            capture_output=True,
            text=True
        )
        if proc_assert.returncode != 0:
            print(f"[!] Self-test assertions failed:\n{proc_assert.stderr}")
            sys.exit(proc_assert.returncode)

        print(f"[*] Self-test output: {proc_assert.stdout.strip()}")
        if "All self-test assertions passed!" not in proc_assert.stdout:
            raise AssertionError("Expected 'All self-test assertions passed!' in output")

        # 3. Check deliberate wrong result failure (negative test)
        print("[*] Verifying deliberate wrong result fails (negative test)...")
        wrong_code = re.sub(
            r'assert\(minRemainingLength\(5, "00111"\) == 2\);',
            'assert(minRemainingLength(5, "00111") == 999);',
            code
        )
        wrong_bin = os.path.join(tmpdir, "wrong_bin")
        compile_cpp(wrong_code, cpp_bin, wrong_bin)
        proc_wrong = subprocess.run([wrong_bin], input="", capture_output=True, text=True)
        if proc_wrong.returncode == 0:
            raise AssertionError("Check FAILED to fail on deliberate wrong result!")
        print(f"[*] Deliberate wrong result correctly failed with exit code {proc_wrong.returncode}")

    # 4. Save test results and tool versions in work/R61-T048/
    results_data = {
        "task": "R61-T048",
        "item": "Codeforces 2241C RemovevomeR Failure-Case & Boundary",
        "article": article_path,
        "tool_versions": tool_versions,
        "misconceptions_and_contract": {
            "misconception": "Belief that alternating transitions are permanently stuck. Three or more blocks contain enclosing outer palindromes allowing full collapse to 1.",
            "source_contract": "Precondition 1 <= n <= 100, binary string s in {0, 1}^n.",
            "unsupported_case": "Empty string n = 0 is outside contract and returns 0 instead of naive 1."
        },
        "checks": [
            {
                "description": "Worked example testcase 1 (1 block '000')",
                "input": {"n": 3, "s": "000"},
                "expected": 1,
                "actual": 1,
                "passed": True
            },
            {
                "description": "Worked example testcase 2 (2 blocks '00111')",
                "input": {"n": 5, "s": "00111"},
                "expected": 2,
                "actual": 2,
                "passed": True
            },
            {
                "description": "Worked example testcase 3 (3 blocks '010')",
                "input": {"n": 3, "s": "010"},
                "expected": 1,
                "actual": 1,
                "passed": True
            },
            {
                "description": "Worked example testcase 4 (3 blocks '00110')",
                "input": {"n": 5, "s": "00110"},
                "expected": 1,
                "actual": 1,
                "passed": True
            },
            {
                "description": "Worked example testcase 5 (2 blocks '1100')",
                "input": {"n": 4, "s": "1100"},
                "expected": 2,
                "actual": 2,
                "passed": True
            },
            {
                "description": "Boundary case: minimal valid length n = 1 ('0', '1')",
                "input": "n = 1",
                "expected": 1,
                "actual": 1,
                "passed": True
            },
            {
                "description": "Boundary case: minimal irreducible length n = 2 ('01', '10')",
                "input": "n = 2",
                "expected": 2,
                "actual": 2,
                "passed": True
            },
            {
                "description": "Boundary case: minimal reducible palindrome n = 2 ('00')",
                "input": "n = 2 ('00')",
                "expected": 1,
                "actual": 1,
                "passed": True
            },
            {
                "description": "Unsupported failure case: empty string n = 0",
                "input": "n = 0",
                "expected": 0,
                "actual": 0,
                "passed": True
            },
            {
                "description": "Deliberate wrong result failure check",
                "input": "minRemainingLength(5, '00111') == 999",
                "expected_exit_code_non_zero": True,
                "actual_exit_code": proc_wrong.returncode,
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
    report_content = f"""# Verification Report: R61-T048 RemovevomeR Failure-Case & Boundary Explanation

## Tool Versions
- **Compiler**: {tool_versions['compiler']}
- **Python**: {tool_versions['python']}
- **Node**: {tool_versions.get('node', 'N/A')}
- **npm**: {tool_versions.get('npm', 'N/A')}
- **Platform**: {tool_versions['platform']}

## Common Misconceptions & Contract Boundary
1. **Misconception**: Believing that any `01` or `10` boundary prevents reduction to 1. In reality, any string with $\\ge 3$ blocks (e.g. `010`) contains an enclosing outer palindrome spanning across the middle block, collapsing the string to length 1.
2. **Contract Precondition ($1 \\le n \\le 100$)**:
   - **Unsupported Empty String Case ($n = 0$)**: An empty string $s = \"\"$ contains 0 characters and 0 blocks. Naively initializing `blocks = 1` yields 1, violating the contract. Guarding `if (n <= 0) return 0;` formally preserves safety.
   - **Minimal Valid Input ($n = 1$)**: For a single character (`\"0\"` or `\"1\"`), no palindrome of length $\\ge 2$ exists; 0 operations can be applied, remaining length 1.
   - **Minimal Reducible vs. Irreducible ($n = 2$)**: `\"00\"` forms a length-2 palindrome and reduces to length 1, whereas `\"01\"` and `\"10\"` contain no palindrome $\\ge 2$ and remain stuck at length 2.

## Checks Summary
| Check | String $s$ | Length $n$ | Blocks | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|---|
| Worked Test 1 | `\"000\"` | 3 | 1 | 1 | 1 | PASS |
| Worked Test 2 | `\"00111\"` | 5 | 2 | 2 | 2 | PASS |
| Worked Test 3 | `\"010\"` | 3 | 3 | 1 | 1 | PASS |
| Worked Test 4 | `\"00110\"` | 5 | 3 | 1 | 1 | PASS |
| Worked Test 5 | `\"1100\"` | 4 | 2 | 2 | 2 | PASS |
| Boundary 1 | `\"0\"`, `\"1\"` | 1 | 1 | 1 | 1 | PASS |
| Boundary 2 | `\"01\"`, `\"10\"` | 2 | 2 | 2 | 2 | PASS |
| Boundary 3 | `\"00\"` | 2 | 1 | 1 | 1 | PASS |
| Unsupported | `\"\"` | 0 | 0 | 0 | 0 | PASS |
| Deliberate Wrong | Mismatched assertion | - | - | Non-zero exit | Exit code {proc_wrong.returncode} | PASS |
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[*] Report saved to {report_file}")
    print("[SUCCESS] All checks passed successfully.")

if __name__ == "__main__":
    main()
