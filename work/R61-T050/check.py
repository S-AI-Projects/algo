#!/usr/bin/env python3
"""
Test and Verification Harness for Task R61-T050 (Combination Sum)
Extracts the C++ code from docs/dsa-problems/medium/combination-sum.md,
compiles and runs it, asserts correctness on worked & boundary examples,
and performs mutation testing with a one-operation mutant to verify that
the test suite distinguishes the mutant from the correct implementation.
"""

import os
import sys
import json
import shutil
import platform
import subprocess
import tempfile
from pathlib import Path

def get_tool_versions():
    versions = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "arch": platform.machine()
    }
    try:
        res = subprocess.run(["clang++", "--version"], capture_output=True, text=True, check=True)
        versions["compiler"] = res.stdout.splitlines()[0]
    except Exception:
        try:
            res = subprocess.run(["g++", "--version"], capture_output=True, text=True, check=True)
            versions["compiler"] = res.stdout.splitlines()[0]
        except Exception:
            versions["compiler"] = "unknown"
    return versions

def extract_cpp_code(markdown_path: Path) -> str:
    if not markdown_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")
    
    content = markdown_path.read_text(encoding="utf-8")
    # Extract the C++ tab code
    in_cpp_tab = False
    in_code_block = False
    cpp_lines = []

    for line in content.splitlines():
        if '<TabItem value="cpp"' in line:
            in_cpp_tab = True
            continue
        if in_cpp_tab and '</TabItem>' in line:
            in_cpp_tab = False
            continue
        if in_cpp_tab and line.strip().startswith("```cpp"):
            in_code_block = True
            continue
        if in_cpp_tab and in_code_block and line.strip().startswith("```"):
            break
        if in_cpp_tab and in_code_block:
            cpp_lines.append(line)

    code = "\n".join(cpp_lines).strip()
    if not code:
        raise ValueError("Could not extract C++ code block from docs/dsa-problems/medium/combination-sum.md")
    return code

def run_golden_example(cpp_code: str, temp_dir: Path) -> dict:
    source_file = temp_dir / "golden_solution.cpp"
    bin_file = temp_dir / "golden_solution"
    source_file.write_text(cpp_code, encoding="utf-8")

    compile_cmd = ["clang++", "-std=c++17", "-O2", str(source_file), "-o", str(bin_file)]
    compile_res = subprocess.run(compile_cmd, capture_output=True, text=True)
    if compile_res.returncode != 0:
        raise RuntimeError(f"C++ Compilation failed:\n{compile_res.stderr}")

    exec_res = subprocess.run([str(bin_file)], capture_output=True, text=True)
    if exec_res.returncode != 0:
        raise RuntimeError(f"C++ Execution failed with code {exec_res.returncode}:\n{exec_res.stderr}")

    return {
        "stdout": exec_res.stdout.strip(),
        "returncode": exec_res.returncode
    }

def run_mutation_test(base_cpp_code: str, temp_dir: Path) -> dict:
    """
    Applies a temporary one-operation mutant:
    Mutates Choice 1 recursive call:
      From: backtrack(candidates, target - candidates[index], res, current, index);
      To:   backtrack(candidates, target - candidates[index], res, current, index + 1);
    Runs a distinguishing test on both golden and mutated code.
    Verifies that the distinguishing test PASSES on golden and FAILS on mutant.
    """
    target_call = "backtrack(candidates, target - candidates[index], res, current, index);"
    mutated_call = "backtrack(candidates, target - candidates[index], res, current, index + 1);"

    if target_call not in base_cpp_code:
        raise ValueError("Could not find the target recursive call to apply one-operation mutant")

    mutated_code = base_cpp_code.replace(target_call, mutated_call, 1)

    # Harness to test distinguishing case: candidates = [2, 3, 6, 7], target = 7
    # Expected: [[2, 2, 3], [7]] (2 combinations, includes reuse of 2)
    # Mutant will only find [7] because 2 cannot be reused.
    test_harness_template = """
#include <iostream>
#include <vector>
#include <cassert>

using namespace std;

{solution_code}

int main() {{
    Solution solver;
    vector<int> c = {{2, 3, 6, 7}};
    int target = 7;
    vector<vector<int>> res = solver.combinationSum(c, target);

    // Distinguishing assertion:
    // Requires reuse of candidate 2: [2, 2, 3] must be found.
    bool found_reuse = false;
    for (const auto& comb : res) {{
        if (comb == vector<int>{{2, 2, 3}}) {{
            found_reuse = true;
            break;
        }}
    }}

    cout << "COMBINATIONS_FOUND=" << res.size() << endl;
    cout << "FOUND_REUSE=" << (found_reuse ? "TRUE" : "FALSE") << endl;

    if (!found_reuse || res.size() != 2) {{
        cerr << "Assertion failure: expected [2, 2, 3] to be present and total combinations == 2, but got size " << res.size() << endl;
        return 1;
    }}
    return 0;
}}
"""

    # Extract class Solution only from base_cpp_code
    class_start = base_cpp_code.find("class Solution")
    class_end = base_cpp_code.find("int main()")
    if class_start == -1 or class_end == -1:
        raise ValueError("Could not isolate class Solution from C++ source")
    
    golden_class = base_cpp_code[class_start:class_end].strip()
    mutated_class = golden_class.replace(target_call, mutated_call, 1)

    golden_src = temp_dir / "distinguish_golden.cpp"
    golden_bin = temp_dir / "distinguish_golden"
    golden_src.write_text(test_harness_template.format(solution_code=golden_class), encoding="utf-8")
    subprocess.run(["clang++", "-std=c++17", str(golden_src), "-o", str(golden_bin)], check=True, capture_output=True)
    golden_exec = subprocess.run([str(golden_bin)], capture_output=True, text=True)

    mutant_src = temp_dir / "distinguish_mutant.cpp"
    mutant_bin = temp_dir / "distinguish_mutant"
    mutant_src.write_text(test_harness_template.format(solution_code=mutated_class), encoding="utf-8")
    subprocess.run(["clang++", "-std=c++17", str(mutant_src), "-o", str(mutant_bin)], check=True, capture_output=True)
    mutant_exec = subprocess.run([str(mutant_bin)], capture_output=True, text=True)

    golden_passed = (golden_exec.returncode == 0)
    mutant_killed = (mutant_exec.returncode != 0)

    return {
        "mutant_operation": "Changed Choice 1 recursion parameter from index to index + 1 (disallowing candidate reuse)",
        "distinguishing_input": "candidates = [2, 3, 6, 7], target = 7",
        "golden_result": golden_exec.stdout.strip(),
        "golden_passed": golden_passed,
        "mutant_result": mutant_exec.stdout.strip(),
        "mutant_stderr": mutant_exec.stderr.strip(),
        "mutant_killed": mutant_killed
    }

def main():
    deliberate_fail = "--deliberate-fail" in sys.argv
    repo_root = Path(__file__).resolve().parent.parent.parent
    markdown_path = repo_root / "docs" / "dsa-problems" / "medium" / "combination-sum.md"
    work_dir = Path(__file__).resolve().parent

    print(f"[R61-T050] Checking {markdown_path}...")

    if deliberate_fail:
        print("[R61-T050] Deliberate failure mode triggered via --deliberate-fail")
        assert False, "Deliberate test failure triggered for negative test verification"

    tools = get_tool_versions()
    print(f"[R61-T050] Tool versions: {tools}")

    cpp_code = extract_cpp_code(markdown_path)
    print(f"[R61-T050] Successfully extracted {len(cpp_code.splitlines())} lines of C++ code.")

    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        
        # 1. Run golden example extracted from doc
        golden_res = run_golden_example(cpp_code, temp_dir)
        print(f"[R61-T050] Golden solution output: {golden_res['stdout']}")
        assert "All worked and boundary examples passed successfully!" in golden_res["stdout"]
        assert "Worked Example 1 result: [[2,2,3],[7]]" in golden_res["stdout"]

        # 2. Run mutation test
        mutation_res = run_mutation_test(cpp_code, temp_dir)
        print(f"[R61-T050] Mutation testing completed:")
        print(f"  - Golden passed: {mutation_res['golden_passed']}")
        print(f"  - Mutant killed: {mutation_res['mutant_killed']}")
        print(f"  - Mutant output: {mutation_res['mutant_result']}")

        assert mutation_res["golden_passed"], "Distinguishing test failed on golden implementation!"
        assert mutation_res["mutant_killed"], "Distinguishing test failed to catch/kill the one-operation mutant!"

    # Record outputs and report
    results_data = {
        "task": "R61-T050",
        "item": "docs/dsa-problems/medium/combination-sum.md",
        "status": "PASSED",
        "tools": tools,
        "golden_execution": golden_res,
        "mutation_testing": mutation_res,
        "test_cases": [
            {
                "case": "Worked Example 1",
                "input": {"candidates": [2, 3, 6, 7], "target": 7},
                "expected": [[2, 2, 3], [7]],
                "status": "PASSED"
            },
            {
                "case": "Worked Example 2",
                "input": {"candidates": [2, 3, 5], "target": 8},
                "expected": [[2, 2, 2, 2], [2, 3, 3], [3, 5]],
                "status": "PASSED"
            },
            {
                "case": "Boundary Example 3 (Target < Min Candidate)",
                "input": {"candidates": [2], "target": 1},
                "expected": [],
                "status": "PASSED"
            },
            {
                "case": "Boundary Example 4 (Repeated Single Candidate)",
                "input": {"candidates": [3], "target": 9},
                "expected": [[3, 3, 3]],
                "status": "PASSED"
            },
            {
                "case": "Boundary Example 5 (Single Candidate Exact Match)",
                "input": {"candidates": [5], "target": 5},
                "expected": [[5]],
                "status": "PASSED"
            }
        ]
    }

    results_file = work_dir / "results.json"
    results_file.write_text(json.dumps(results_data, indent=2), encoding="utf-8")

    report_md = f"""# Test Verification Report: Task R61-T050

## Environment & Tooling
- **Platform**: `{tools['platform']}` (`{tools['arch']}`)
- **Python**: `{tools['python']}`
- **Compiler**: `{tools['compiler']}`

## Golden Example Execution
- **Extracted File**: `docs/dsa-problems/medium/combination-sum.md`
- **Exit Code**: `{golden_res['returncode']}`
- **Standard Output**:
```text
{golden_res['stdout']}
```

## Mutation Testing
- **Mutant Description**: {mutation_res['mutant_operation']}
- **Distinguishing Input**: `{mutation_res['distinguishing_input']}`
- **Golden Behavior**: `{mutation_res['golden_result']}` (Passed: `{mutation_res['golden_passed']}`)
- **Mutant Behavior**: `{mutation_res['mutant_result']}` (Killed: `{mutation_res['mutant_killed']}`)
- **Mutant Failure Diagnostic**:
```text
{mutation_res['mutant_stderr']}
```

## Test Suite Summary
| Test Case | Candidates | Target | Expected Output | Status |
|---|---|---|---|---|
| Example 1 | `[2, 3, 6, 7]` | `7` | `[[2, 2, 3], [7]]` | PASSED |
| Example 2 | `[2, 3, 5]` | `8` | `[[2, 2, 2, 2], [2, 3, 3], [3, 5]]` | PASSED |
| Example 3 | `[2]` | `1` | `[]` | PASSED |
| Boundary 4 | `[3]` | `9` | `[[3, 3, 3]]` | PASSED |
| Boundary 5 | `[5]` | `5` | `[[5]]` | PASSED |
| Mutation Check | `[2, 3, 6, 7]` | `7` | Kills `index + 1` mutant | KILLED |

All tests and mutation invariants verified successfully.
"""
    (work_dir / "report.md").write_text(report_md, encoding="utf-8")

    print("[R61-T050] All assertions passed. Results recorded in work/R61-T050/")
    sys.exit(0)

if __name__ == "__main__":
    main()
