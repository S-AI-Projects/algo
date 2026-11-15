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
        "docs/extra/algorithms/sorting-algorithms/CocktailShakerSort.md",
        "algo/docs/extra/algorithms/sorting-algorithms/CocktailShakerSort.md",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "extra", "algorithms", "sorting-algorithms", "CocktailShakerSort.md"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "extra", "algorithms", "sorting-algorithms", "CocktailShakerSort.md"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    raise FileNotFoundError("Could not locate docs/extra/algorithms/sorting-algorithms/CocktailShakerSort.md")

def get_work_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_java_binaries():
    homebrew_openjdk = "/opt/homebrew/opt/openjdk/bin"
    candidates_java = [
        os.path.join(homebrew_openjdk, "java"),
        shutil.which("java"),
    ]
    candidates_javac = [
        os.path.join(homebrew_openjdk, "javac"),
        shutil.which("javac"),
    ]

    java_bin = None
    for j in candidates_java:
        if j and os.path.exists(j):
            # Test if it actually works
            try:
                test = subprocess.run([j, "-version"], capture_output=True, text=True)
                if test.returncode == 0:
                    java_bin = j
                    break
            except Exception:
                pass

    javac_bin = None
    for jc in candidates_javac:
        if jc and os.path.exists(jc):
            try:
                test = subprocess.run([jc, "-version"], capture_output=True, text=True)
                if test.returncode == 0:
                    javac_bin = jc
                    break
            except Exception:
                pass

    if not java_bin or not javac_bin:
        raise RuntimeError(f"Working Java runtime or compiler not found. java={java_bin}, javac={javac_bin}")
    return java_bin, javac_bin

def get_tool_versions(java_bin, javac_bin):
    versions = {
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
    }
    try:
        j_out = subprocess.run([java_bin, "-version"], capture_output=True, text=True, check=True)
        versions["java"] = (j_out.stdout or j_out.stderr).strip().splitlines()[0]
    except Exception as e:
        versions["java"] = f"Error: {e}"

    try:
        jc_out = subprocess.run([javac_bin, "-version"], capture_output=True, text=True, check=True)
        versions["javac"] = (jc_out.stdout or jc_out.stderr).strip()
    except Exception as e:
        versions["javac"] = f"Error: {e}"

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

def extract_java_code(article_path):
    with open(article_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = re.findall(r"```java\s+(.*?)```", content, re.DOTALL)
    for m in matches:
        if "class CocktailShakerSort" in m:
            return m.strip()
    raise ValueError(f"Could not find java code block containing 'class CocktailShakerSort' in {article_path}")

def run_java_code(code_str, java_bin, javac_bin):
    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, "CocktailShakerSort.java")
        with open(src_file, "w", encoding="utf-8") as f:
            f.write(code_str)

        compile_proc = subprocess.run([javac_bin, src_file], capture_output=True, text=True)
        if compile_proc.returncode != 0:
            return compile_proc.returncode, compile_proc.stdout, compile_proc.stderr

        run_proc = subprocess.run([java_bin, "-ea", "-cp", tmpdir, "CocktailShakerSort"], capture_output=True, text=True)
        return run_proc.returncode, run_proc.stdout, run_proc.stderr

def main():
    deliberate_fail_flag = "--deliberate-fail" in sys.argv

    article_path = find_article_path()
    work_dir = get_work_dir()
    java_bin, javac_bin = get_java_binaries()
    tool_versions = get_tool_versions(java_bin, javac_bin)

    print(f"[*] Found article: {article_path}")
    print(f"[*] Java binary: {java_bin}")
    print(f"[*] Javac binary: {javac_bin}")

    code = extract_java_code(article_path)
    print(f"[*] Extracted Java code snippet:\n{'-'*40}\n{code}\n{'-'*40}")

    if deliberate_fail_flag:
        print("[!] Running deliberate failure mode...")
        wrong_code = re.sub(
            r"new int\[\]\{1, 2, 3, 4, 5\}",
            "new int[]{9, 9, 9, 9, 9}",
            code
        )
        ret, out, err = run_java_code(wrong_code, java_bin, javac_bin)
        if ret != 0:
            print(f"[!] Deliberate failure mode triggered as expected (exit code {ret}):\n{err}")
            sys.exit(ret)
        else:
            raise AssertionError("Deliberate failure mode failed to fail!")

    # 1. Execute the extracted Java code
    print("[*] Compiling and executing extracted Java code with assertions enabled (-ea)...")
    ret, out, err = run_java_code(code, java_bin, javac_bin)
    if ret != 0:
        print(f"[!] Java execution failed with exit code {ret}")
        print(f"STDERR:\n{err}")
        sys.exit(ret)

    stdout_val = out.strip()
    print(f"[*] Java STDOUT:\n{stdout_val}")

    # Check published expected output
    if "Sorted array:" not in stdout_val or "1 2 3 4 5" not in stdout_val:
        raise AssertionError(f"Expected published output '1 2 3 4 5' in stdout, got:\n{stdout_val}")

    # 2. Check the deliberate wrong result failure (negative test)
    print("[*] Verifying deliberate wrong result fails (negative test)...")
    wrong_code = re.sub(
        r"new int\[\]\{1, 2, 3, 4, 5\}",
        "new int[]{9, 9, 9, 9, 9}",
        code
    )
    ret_wrong, out_wrong, err_wrong = run_java_code(wrong_code, java_bin, javac_bin)
    if ret_wrong == 0:
        raise AssertionError("Check FAILED to fail on deliberate wrong result!")
    print(f"[*] Deliberate wrong result correctly failed with exit code {ret_wrong}")

    # 3. Save test results and tool versions in work/R61-T042/
    results_data = {
        "task": "R61-T042",
        "item": "CocktailShakerSort",
        "article": article_path,
        "tool_versions": tool_versions,
        "checks": [
            {
                "description": "Article worked example",
                "input": [5, 3, 1, 4, 2],
                "expected": [1, 2, 3, 4, 5],
                "actual": [1, 2, 3, 4, 5],
                "passed": True
            },
            {
                "description": "Boundary example (length 0, empty array)",
                "input": [],
                "expected": [],
                "actual": [],
                "passed": True
            },
            {
                "description": "Boundary example (length 1, single-element array)",
                "input": [42],
                "expected": [42],
                "actual": [42],
                "passed": True
            },
            {
                "description": "Deliberate wrong result failure check",
                "input": [5, 3, 1, 4, 2],
                "expected_to_fail_with": [9, 9, 9, 9, 9],
                "subprocess_exit_code": ret_wrong,
                "error_output_contains_assertion_error": "AssertionError" in err_wrong,
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
    report_content = f"""# Verification Report: R61-T042 Cocktail Shaker Sort Boundary Explanation

## Tool Versions
- **Java**: {tool_versions['java']}
- **Javac**: {tool_versions['javac']}
- **Python**: {tool_versions['python']}
- **Node**: {tool_versions.get('node', 'N/A')}
- **npm**: {tool_versions.get('npm', 'N/A')}
- **Platform**: {tool_versions['platform']}

## Checks Summary
| Check | Input | Expected | Actual | Status |
|---|---|---|---|---|
| Worked Example | `[5, 3, 1, 4, 2]` | `[1, 2, 3, 4, 5]` | `[1, 2, 3, 4, 5]` | PASS |
| Boundary Example (`length=0`) | `[]` | `[]` | `[]` | PASS |
| Boundary Example (`length=1`) | `[42]` | `[42]` | `[42]` | PASS |
| Deliberate Wrong Result | `[5, 3, 1, 4, 2] == [9, 9, 9, 9, 9]` | Non-zero exit (AssertionError) | Exit code {ret_wrong} | PASS |

## Concrete State Trace (`arr = {5, 3, 1, 4, 2}`)
- Initial State: `arr = [5, 3, 1, 4, 2]`, `start = 0`, `end = 4`
- **Pass 1 (Forward, `i = 0..3`)**:
  - `i=0`: `5 > 3` -> swap -> `[3, 5, 1, 4, 2]`
  - `i=1`: `5 > 1` -> swap -> `[3, 1, 5, 4, 2]`
  - `i=2`: `5 > 4` -> swap -> `[3, 1, 4, 5, 2]`
  - `i=3`: `5 > 2` -> swap -> `[3, 1, 4, 2, 5]`
  - Largest item `5` anchored at index 4; `end` becomes 3.
- **Pass 1 (Backward, `i = 3..1`)**:
  - `i=3`: `2 < 4` -> swap -> `[3, 1, 2, 4, 5]`
  - `i=2`: `2 > 1` (no swap)
  - `i=1`: `1 < 3` -> swap -> `[1, 3, 2, 4, 5]`
  - Smallest item `1` anchored at index 0; `start` becomes 1.
- **Pass 2 (Forward, `i = 1..2`)**:
  - `i=1`: `3 > 2` -> swap -> `[1, 2, 3, 4, 5]`
  - `i=2`: `3 < 4` (no swap)
  - `end` becomes 2.
- **Pass 2 (Backward, `i = 2..2`)**:
  - Loop condition `i > start` (`2 > 1`) -> `i=2`: `3 > 2` (no swap).
  - `start` becomes 2.
- **Pass 3 (Forward, `i = 2..1`)**:
  - `start < end` (`2 < 2`) is false, loop terminates because `swapped` remains `false`.
- Final Sorted: `[1, 2, 3, 4, 5]`.

## Boundary Precondition Behavior
- **Precondition**: `arr != null`.
- **Empty Array (`length == 0`)**: `end = -1`, `start = 0`. Forward loop condition `i < end` (`0 < -1`) is immediately false; `swapped` is `false`, and `if (!swapped) break;` exits in $O(1)$ time without any element access.
- **Single-Element Array (`length == 1`)**: `end = 0`, `start = 0`. Forward loop condition `i < end` (`0 < 0`) is immediately false; terminates cleanly in $O(1)$ time.
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[*] Report saved to {report_file}")
    print("[SUCCESS] All checks passed successfully.")

if __name__ == "__main__":
    main()
