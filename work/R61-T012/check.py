#!/usr/bin/env python3
"""Compile the Java example published in the UCS article and check its output."""

import json
import pathlib
import re
import subprocess
import tempfile
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
ARTICLE = ROOT / "docs/extra/algorithms/Searching Algorithms/Uniform-Cost-Search.md"
REPORT = pathlib.Path(__file__).resolve().parent / "results.json"
EXPECTED = "Worked example cost: 5\nStart equals goal cost: 0\n"


def run(command, **kwargs):
    result = subprocess.run(command, text=True, capture_output=True, **kwargs)
    return result, {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main():
    report = {
        "task_id": "R61-T012",
        "source_article": str(ARTICLE.relative_to(ROOT)),
        "inputs": {
            "worked_graph": "1 -> 3 (8), 1 -> 2 (2), 2 -> 3 (3)",
            "boundary_case": "start and goal are the same node (1)",
            "precondition": "all edge costs are non-negative",
        },
        "expected_stdout": EXPECTED,
    }
    try:
        source = ARTICLE.read_text(encoding="utf-8")
        match = re.search(r"```java\s*\n(.*?)\n```", source, re.DOTALL)
        if not match:
            raise AssertionError("Could not find the Java code fence in the article")

        java_version, java_version_record = run(["java", "-version"])
        javac_version, javac_version_record = run(["javac", "-version"])
        report["tools"] = {
            "python": sys.version,
            "java": java_version.stderr.strip(),
            "javac": (javac_version.stdout or javac_version.stderr).strip(),
        }
        report["version_commands"] = {
            "java": java_version_record,
            "javac": javac_version_record,
        }
        if java_version.returncode or javac_version.returncode:
            raise RuntimeError("Java runtime and compiler are required")

        with tempfile.TemporaryDirectory(prefix="r61-t012-") as temp_dir:
            source_path = pathlib.Path(temp_dir) / "UniformCostSearchDemo.java"
            source_path.write_text(match.group(1), encoding="utf-8")
            compiled, compile_record = run(["javac", str(source_path)])
            report["compile"] = compile_record
            if compiled.returncode:
                raise RuntimeError("The article's Java example did not compile")

            executed, execution_record = run(
                ["java", "-cp", temp_dir, "UniformCostSearchDemo"]
            )
            report["execution"] = execution_record
            report["actual_stdout"] = executed.stdout
            if executed.returncode:
                raise RuntimeError("The article's Java example exited unsuccessfully")
            if executed.stdout != EXPECTED:
                raise AssertionError(
                    f"Output mismatch: expected {EXPECTED!r}, got {executed.stdout!r}"
                )
        report["result"] = "passed"
        print("PASS: article Java example compiled and produced expected output")
    except Exception as error:
        report["result"] = "failed"
        report["failure"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
