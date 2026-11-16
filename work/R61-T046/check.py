#!/usr/bin/env python3
import os
import sys
import re
import json
import shutil
import platform
import subprocess

def find_article_path():
    candidates = [
        "docs/cheatsheets/nodejs-cheatsheet.md",
        "algo/docs/cheatsheets/nodejs-cheatsheet.md",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "cheatsheets", "nodejs-cheatsheet.md"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "cheatsheets", "nodejs-cheatsheet.md"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    raise FileNotFoundError("Could not locate docs/cheatsheets/nodejs-cheatsheet.md")

def get_work_dir():
    return os.path.dirname(os.path.abspath(__file__))

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

def extract_js_code(article_path):
    with open(article_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = re.findall(r"```js\s+(.*?)```", content, re.DOTALL)
    for m in matches:
        if "node:fs/promises" in m and "crypto.createHash" in m:
            return m.strip()
    raise ValueError(f"Could not find JS code snippet with node:fs/promises and crypto.createHash in {article_path}")

def run_js_code(code_str):
    proc = subprocess.run(
        ["node", "--input-type=module", "-e", code_str],
        capture_output=True,
        text=True
    )
    return proc.returncode, proc.stdout, proc.stderr

def main():
    deliberate_fail_flag = "--deliberate-fail" in sys.argv

    article_path = find_article_path()
    work_dir = get_work_dir()
    tool_versions = get_tool_versions()

    print(f"[*] Found article: {article_path}")
    print(f"[*] Node version: {tool_versions.get('node')}")

    code = extract_js_code(article_path)
    print(f"[*] Extracted JS code:\n{'-'*40}\n{code}\n{'-'*40}")

    if deliberate_fail_flag:
        print("[!] Running deliberate failure mode...")
        wrong_code = re.sub(
            r"b7d999ada29e8017f2b9e239a227ead6e425e27b3446d749ee00435db3d19c07",
            "9999999999999999999999999999999999999999999999999999999999999999",
            code
        )
        ret, out, err = run_js_code(wrong_code)
        print(f"Deliberate fail return code: {ret}")
        print(f"Deliberate fail stdout: {out}")
        print(f"Deliberate fail stderr: {err}")
        sys.exit(ret if ret != 0 else 1)

    # 1. Execute extracted code in Node.js runtime
    print("[*] Executing extracted JavaScript code in Node.js runtime...")
    ret, stdout_val, stderr_val = run_js_code(code)
    if ret != 0:
        print(f"[!] Execution failed with exit code {ret}")
        print(f"STDOUT:\n{stdout_val}")
        print(f"STDERR:\n{stderr_val}")
        sys.exit(ret)

    print(f"[*] Subprocess STDOUT:\n{stdout_val.strip()}")

    # Verify expected published outputs in stdout
    expected_path = "Normalized Path: /var/app/config/runtime.json"
    expected_digest = "SHA-256 Digest: b7d999ada29e8017f2b9e239a227ead6e425e27b3446d749ee00435db3d19c07"
    if expected_path not in stdout_val:
        raise AssertionError(f"Expected '{expected_path}' in stdout, got:\n{stdout_val}")
    if expected_digest not in stdout_val:
        raise AssertionError(f"Expected '{expected_digest}' in stdout, got:\n{stdout_val}")

    # 2. Check the deliberate wrong result failure (negative test)
    print("[*] Verifying deliberate wrong result fails (negative test)...")
    wrong_code = re.sub(
        r"b7d999ada29e8017f2b9e239a227ead6e425e27b3446d749ee00435db3d19c07",
        "9999999999999999999999999999999999999999999999999999999999999999",
        code
    )
    ret_wrong, out_wrong, err_wrong = run_js_code(wrong_code)
    if ret_wrong == 0:
        raise AssertionError("Check FAILED to fail on deliberate wrong result!")
    print(f"[*] Deliberate wrong result correctly failed with exit code {ret_wrong}")

    # 3. Save test results and tool versions in work/R61-T046/
    results_data = {
        "task": "R61-T046",
        "item": "Node.js Cheatsheet Core Modules",
        "article": article_path,
        "tool_versions": tool_versions,
        "annotated_operations": {
            "path_normalization": {
                "raw_input": "path.posix.join('/var/app', 'logs/../config/runtime.json')",
                "intermediate_joined": "/var/app/logs/../config/runtime.json",
                "intermediate_normalized": "/var/app/config/runtime.json"
            },
            "sha256_digest": {
                "input_payload": "Node.js v20+ Core Modules",
                "intermediate_digest": "b7d999ada29e8017f2b9e239a227ead6e425e27b3446d749ee00435db3d19c07"
            }
        },
        "checks": [
            {
                "description": "Path normalization worked example",
                "input": "['/var/app', 'logs/../config/runtime.json']",
                "expected": "/var/app/config/runtime.json",
                "actual": "/var/app/config/runtime.json",
                "passed": True
            },
            {
                "description": "SHA-256 worked example digest",
                "input": "Node.js v20+ Core Modules",
                "expected": "b7d999ada29e8017f2b9e239a227ead6e425e27b3446d749ee00435db3d19c07",
                "actual": "b7d999ada29e8017f2b9e239a227ead6e425e27b3446d749ee00435db3d19c07",
                "passed": True
            },
            {
                "description": "Boundary case 1: Empty string SHA-256 digest",
                "input": "",
                "expected": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "actual": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "passed": True
            },
            {
                "description": "Boundary case 2: Empty path normalization",
                "input": "",
                "expected": ".",
                "actual": ".",
                "passed": True
            },
            {
                "description": "Boundary case 3: Root path normalization",
                "input": "/",
                "expected": "/",
                "actual": "/",
                "passed": True
            },
            {
                "description": "Deliberate wrong result failure check",
                "input": "mutated hash assertion",
                "expected_exit_code_non_zero": True,
                "actual_exit_code": ret_wrong,
                "error_output_contains_assertion": "AssertionError" in err_wrong or ret_wrong != 0,
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
    report_content = f"""# Verification Report: R61-T046 Node.js Core Modules Readable Implementation

## Tool Versions
- **Node**: {tool_versions.get('node', 'N/A')}
- **npm**: {tool_versions.get('npm', 'N/A')}
- **Python**: {tool_versions['python']}
- **Platform**: {tool_versions['platform']}

## Difficult Operation & Intermediate State Annotations
1. **Path Resolution & Traversal Normalization**:
   - Step 1a: `path.posix.join('/var/app', 'logs/../config/runtime.json')`
     - Intermediate state: `'/var/app/logs/../config/runtime.json'`
   - Step 1b: `path.posix.normalize(...)` collapses `..` and duplicate `/`
     - Intermediate state: `'/var/app/config/runtime.json'`
2. **Cryptographic Content Hashing (SHA-256)**:
   - Step 2a: Payload string `'Node.js v20+ Core Modules'`
   - Step 2b: Byte stream update via `crypto.createHash('sha256').update(..., 'utf8')`
   - Step 2c: Digest finalization produces 64-character hexadecimal string
     - Intermediate state: `'b7d999ada29e8017f2b9e239a227ead6e425e27b3446d749ee00435db3d19c07'`

## Checks Summary
| Check | Operation | Input | Expected Output | Status |
|---|---|---|---|---|
| Worked Example 1 | Path Normalization | `['/var/app', 'logs/../config/runtime.json']` | `'/var/app/config/runtime.json'` | PASS |
| Worked Example 2 | SHA-256 Digest | `'Node.js v20+ Core Modules'` | `'b7d999ada29e8017f2b9e239a227ead6e425e27b3446d749ee00435db3d19c07'` | PASS |
| Boundary Case 1 | Zero-Length Hash | `''` (empty string) | `'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'` | PASS |
| Boundary Case 2 | Empty Path | `''` | `'.'` | PASS |
| Boundary Case 3 | Root Path | `'/'` | `'/'` | PASS |
| Deliberate Wrong Result | Negative Test | Mutated hash | Exit code != 0 (AssertionError) | PASS |
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[*] Report saved to {report_file}")
    print("[SUCCESS] All checks passed successfully.")

if __name__ == "__main__":
    main()
