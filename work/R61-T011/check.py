#!/usr/bin/env python3
"""Compile and run the C++ example directly from the linked-list article."""

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / "docs/extra/linked-list/intersection-linked-lists.md"
REPORT = Path(__file__).resolve().parent / "results.json"
EXPECTED_STDOUT = (
    "The intersection point is 15\n"
    "The intersection point for lists without a shared node is -1\n"
)
INPUTS = [
    {
        "name": "shared_tail",
        "list1": [10, 15, 30],
        "list2": [3, 6, 9, 15, 30],
        "shared_node_value": 15,
        "expected_result": 15,
        "alignment": "Advance list2 by 2 nodes (3 and 6); after 9 is compared with 10, both pointers reach the shared node 15.",
    },
    {
        "name": "equal_values_without_shared_node",
        "list1": [15, 30],
        "list2": [15],
        "nodes_are_shared": False,
        "expected_result": -1,
    },
]


def run(command):
    """Run a command and retain its output for the evidence report."""
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    record = {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    return result, record


def main():
    report = {
        "task_id": "R61-T011",
        "source_article": str(ARTICLE.relative_to(ROOT)),
        "inputs": INPUTS,
        "expected_stdout": EXPECTED_STDOUT,
        "tools": {"python": sys.version},
        "result": "failed",
    }

    try:
        article = ARTICLE.read_text(encoding="utf-8")
        match = re.search(r"(?ms)^```cpp\s*\n(.*?)^```\s*$", article)
        if match is None:
            raise AssertionError("Could not find the article's C++ code fence")
        cpp_source = match.group(1)

        compiler = shlex.split(os.environ.get("CXX", "g++"))
        compiler_path = shutil.which(compiler[0])
        if compiler_path is None:
            raise FileNotFoundError(f"C++ compiler not found: {compiler[0]}")
        compiler[0] = compiler_path
        version, version_record = run(compiler + ["--version"])
        report["tools"]["compiler"] = version.stdout.splitlines()[0] if version.stdout else version.stderr.splitlines()[0]
        report["compiler_version_command"] = version_record
        if version.returncode != 0:
            raise RuntimeError("Could not read the C++ compiler version")

        for tool_name, command in (("node", ["node", "--version"]), ("npm", ["npm", "--version"])):
            tool_path = shutil.which(command[0])
            if tool_path:
                tool_result, tool_record = run([tool_path, *command[1:]])
                report["tools"][tool_name] = tool_result.stdout.strip()
                report[f"{tool_name}_version_command"] = tool_record

        with tempfile.TemporaryDirectory(prefix="r61-t011-") as temp_dir:
            source_path = Path(temp_dir) / "article_example.cpp"
            binary_path = Path(temp_dir) / "article_example"
            source_path.write_text(cpp_source, encoding="utf-8")

            compile_command = compiler + [
                "-std=c++17",
                "-Wall",
                "-Wextra",
                "-pedantic",
                str(source_path),
                "-o",
                str(binary_path),
            ]
            compiled, compile_record = run(compile_command)
            compile_record["command"] = [
                compiler[0],
                "-std=c++17",
                "-Wall",
                "-Wextra",
                "-pedantic",
                "<article_example.cpp>",
                "-o",
                "<article_example>",
            ]
            report["compile"] = compile_record
            if compiled.returncode != 0:
                raise RuntimeError("The C++ example did not compile")

            execution, execution_record = run([str(binary_path)])
            execution_record["command"] = ["<article_example>"]
            report["execution"] = execution_record
            report["actual_stdout"] = execution.stdout
            if execution.returncode != 0:
                raise RuntimeError("The C++ example exited with a failure")
            if execution.stdout != EXPECTED_STDOUT:
                raise AssertionError(
                    "Output mismatch:\n"
                    f"expected: {EXPECTED_STDOUT!r}\n"
                    f"actual:   {execution.stdout!r}"
                )

        report["result"] = "passed"
        print("PASS: article C++ example compiled and produced the expected output")
    except Exception as error:
        report["failure"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
