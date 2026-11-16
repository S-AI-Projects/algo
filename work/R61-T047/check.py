#!/usr/bin/env python3
import os
import sys
import re
import json
import sqlite3
import platform
import subprocess

def find_article_path():
    candidates = [
        "docs/languages/SQL/sql-26.md",
        "algo/docs/languages/SQL/sql-26.md",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "languages", "SQL", "sql-26.md"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "languages", "SQL", "sql-26.md"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    raise FileNotFoundError("Could not locate docs/languages/SQL/sql-26.md")

def get_work_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_tool_versions():
    versions = {
        "sqlite3_version": sqlite3.sqlite_version,
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

def extract_sql_blocks(article_path):
    with open(article_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = re.findall(r"```sql\s+(.*?)```", content, re.DOTALL)
    for m in matches:
        if "CREATE TABLE Products" in m and "CASE CategoryID" in m:
            return m.strip()
    raise ValueError(f"Could not find SQL block with 'CREATE TABLE Products' and 'CASE CategoryID' in {article_path}")

def run_sql_harness(sql_code, deliberate_wrong=False):
    # Split SQL into individual statements
    statements = [stmt.strip() for stmt in sql_code.split(";") if stmt.strip()]

    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    worked_result = None
    boundary_result = None

    for stmt in statements:
        # Strip comments
        lines = [line for line in stmt.splitlines() if not line.strip().startswith("--")]
        clean_stmt = "\n".join(lines).strip()
        if not clean_stmt:
            continue

        if clean_stmt.upper().startswith("SELECT"):
            if "WHERE ProductID = 4" in clean_stmt:
                boundary_result = cur.execute(clean_stmt).fetchone()
            else:
                worked_result = cur.execute(clean_stmt).fetchall()
        else:
            cur.execute(clean_stmt)

    con.commit()

    expected_worked = [
        ("Laptop", "Electronics"),
        ("Desk Chair", "Furniture"),
        ("Apples", "Groceries"),
        ("Desk Lamp", "Other"),
        ("Uncategorized Item", "Other")
    ]

    expected_boundary = ("Desk Lamp", None)

    if deliberate_wrong:
        expected_worked = [
            ("Laptop", "WrongCategory"),
            ("Desk Chair", "Furniture"),
            ("Apples", "Groceries"),
            ("Desk Lamp", "Other"),
            ("Uncategorized Item", "Other")
        ]

    # Boundary test on empty table
    cur.execute("DELETE FROM Products;")
    con.commit()
    empty_result = cur.execute("""
    SELECT ProductName,
        CASE CategoryID
            WHEN 1 THEN 'Electronics'
            ELSE 'Other'
        END AS CategoryLabel
    FROM Products;
    """).fetchall()

    con.close()

    if worked_result != expected_worked:
        raise AssertionError(f"Worked example mismatch:\nActual:   {worked_result}\nExpected: {expected_worked}")

    if boundary_result != expected_boundary:
        raise AssertionError(f"Boundary result mismatch:\nActual:   {boundary_result}\nExpected: {expected_boundary}")

    if empty_result != []:
        raise AssertionError(f"Empty table result mismatch: expected [], got {empty_result}")

    return worked_result, boundary_result, empty_result

def main():
    deliberate_fail_flag = "--deliberate-fail" in sys.argv

    article_path = find_article_path()
    work_dir = get_work_dir()
    tool_versions = get_tool_versions()

    print(f"[*] Found article: {article_path}")
    print(f"[*] SQLite version: {tool_versions['sqlite3_version']}")

    sql_code = extract_sql_blocks(article_path)
    print(f"[*] Extracted SQL block:\n{'-'*40}\n{sql_code}\n{'-'*40}")

    if deliberate_fail_flag:
        print("[!] Running deliberate failure mode...")
        # Force deliberate mismatch
        try:
            run_sql_harness(sql_code, deliberate_wrong=True)
        except AssertionError as e:
            print(f"Deliberate failure caught successfully: {e}")
            sys.exit(1)
        sys.exit(0)

    # 1. Execute SQL harness
    print("[*] Executing extracted SQL statements against in-memory SQLite runtime...")
    worked_res, boundary_res, empty_res = run_sql_harness(sql_code, deliberate_wrong=False)

    print("[*] Worked Example Results:")
    for row in worked_res:
        print(f"    {row[0]:<20} -> {row[1]}")

    print(f"[*] Boundary Result (Omitted ELSE): {boundary_res}")
    print(f"[*] Boundary Result (Empty Table):  {empty_res}")

    # 2. Check the deliberate wrong result failure (negative test)
    print("[*] Verifying deliberate wrong result fails (negative test)...")
    failed_as_expected = False
    try:
        run_sql_harness(sql_code, deliberate_wrong=True)
    except AssertionError:
        failed_as_expected = True

    if not failed_as_expected:
        raise AssertionError("Check FAILED to fail on deliberate wrong result!")
    print("[*] Deliberate wrong result correctly failed with AssertionError.")

    # 3. Save test results and tool versions in work/R61-T047/
    results_data = {
        "task": "R61-T047",
        "item": "SQL CASE Expression Derivation",
        "article": article_path,
        "tool_versions": tool_versions,
        "derivation": {
            "row_1": {"input": ("Laptop", 1), "branch": "WHEN 1", "output": "Electronics"},
            "row_2": {"input": ("Desk Chair", 2), "branch": "WHEN 2", "output": "Furniture"},
            "row_3": {"input": ("Apples", 3), "branch": "WHEN 3", "output": "Groceries"},
            "row_4": {"input": ("Desk Lamp", 99), "branch": "ELSE", "output": "Other"},
            "row_5": {"input": ("Uncategorized Item", None), "branch": "ELSE", "output": "Other"}
        },
        "checks": [
            {
                "description": "Article worked example (Simple CASE with 5 fixture rows)",
                "expected": [
                    ["Laptop", "Electronics"],
                    ["Desk Chair", "Furniture"],
                    ["Apples", "Groceries"],
                    ["Desk Lamp", "Other"],
                    ["Uncategorized Item", "Other"]
                ],
                "actual": [list(r) for r in worked_res],
                "passed": True
            },
            {
                "description": "Boundary case 1: Omitted ELSE clause produces NULL",
                "input": ["Desk Lamp", 99],
                "expected": ["Desk Lamp", None],
                "actual": list(boundary_res),
                "passed": True
            },
            {
                "description": "Boundary case 2: Empty table returns 0 rows",
                "input": "0 rows",
                "expected": [],
                "actual": empty_res,
                "passed": True
            },
            {
                "description": "Deliberate wrong result failure check",
                "input": "WrongCategory assertion",
                "expected_to_fail": True,
                "passed": True
            }
        ],
        "extracted_sql": sql_code
    }

    results_file = os.path.join(work_dir, "results.json")
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results_data, f, indent=2)
    print(f"[*] Results saved to {results_file}")

    report_file = os.path.join(work_dir, "report.md")
    report_content = f"""# Verification Report: R61-T047 SQL CASE Expression Step-by-Step Derivation

## Tool Versions
- **SQLite**: {tool_versions['sqlite3_version']}
- **Python**: {tool_versions['python']}
- **Node**: {tool_versions.get('node', 'N/A')}
- **npm**: {tool_versions.get('npm', 'N/A')}
- **Platform**: {tool_versions['platform']}

## Step-by-Step Fixture Derivation
| ProductID | Input ProductName | Input CategoryID | Evaluated Branch | Output CategoryLabel | Derivation Notes |
|---|---|---|---|---|---|
| 1 | Laptop | 1 | `WHEN 1` | Electronics | `CategoryID = 1` matches branch 1 -> `'Electronics'` |
| 2 | Desk Chair | 2 | `WHEN 2` | Furniture | `CategoryID = 2` matches branch 2 -> `'Furniture'` |
| 3 | Apples | 3 | `WHEN 3` | Groceries | `CategoryID = 3` matches branch 3 -> `'Groceries'` |
| 4 | Desk Lamp | 99 | `ELSE` | Other | No `WHEN` branch matches; falls through to `ELSE 'Other'` |
| 5 | Uncategorized Item | NULL | `ELSE` | Other | Under 3VL, `NULL = 1..3` evaluates to `UNKNOWN`; falls through to `ELSE 'Other'` |

## Checks Summary
| Check | Query / Operation | Expected Output | Actual Output | Status |
|---|---|---|---|---|
| Worked Example | Simple CASE on 5 rows | 5 categorized rows | 5 categorized rows | PASS |
| Boundary 1 | Omitted ELSE (ProductID 4) | `('Desk Lamp', None)` | `('Desk Lamp', None)` | PASS |
| Boundary 2 | Empty table query | `[]` (0 rows) | `[]` (0 rows) | PASS |
| Deliberate Wrong Result | Negative Test | Non-zero exit (AssertionError) | AssertionError caught | PASS |
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[*] Report saved to {report_file}")
    print("[SUCCESS] All checks passed successfully.")

if __name__ == "__main__":
    main()
