#!/usr/bin/env python3
"""Execute the SQL example embedded in sql-19.md and record SQLite's query plans."""
import json
import platform
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/languages/SQL/sql-19.md"
OUT = Path(__file__).with_name("results.json")

EXPECTED = [
    [("Chai",), ("Chang",), ("Chef Anton's Cajun Seasoning",)],
    [("Aniseed Syrup",), ("Chang",), ("Chef Anton's Cajun Seasoning",)],
    [("Aniseed Syrup",)],
    [("1001",), ("1002",), ("1003",), ("1004",)],
    [],
]


def main():
    source = DOC.read_text()
    fences = re.findall(r"```sql\s*\n(.*?)\n```", source, re.S)
    if not fences:
        raise AssertionError("No SQL example found in the article")
    sql = fences[-1]
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA case_sensitive_like=OFF")
    pending = ""
    actual = []
    for line in sql.splitlines():
        pending += line + "\n"
        if sqlite3.complete_statement(pending):
            statement, pending = pending.strip(), ""
            if statement:
                cursor = db.execute(statement)
                if statement.upper().startswith("SELECT"):
                    actual.append(cursor.fetchall())
    if pending.strip():
        raise AssertionError(f"Incomplete SQL statement: {pending}")
    if actual != EXPECTED:
        raise AssertionError(f"Example results differ: expected {EXPECTED!r}, got {actual!r}")

    db.execute("CREATE INDEX products_name_nocase ON Products(ProductName COLLATE NOCASE)")
    db.executemany(
        "INSERT INTO Products VALUES (?, ?)",
        [(f"x{i:04}", f"Ch item {i}" if i % 2 == 0 else f"Other item {i}") for i in range(1000)],
    )
    plans = {}
    for label, pattern in (("prefix", "Ch%"), ("leading_wildcard", "%an%")):
        query = f"SELECT ProductName FROM Products WHERE ProductName LIKE '{pattern}'"
        plan = [row[3] for row in db.execute("EXPLAIN QUERY PLAN " + query)]
        count = db.execute("SELECT count(*) FROM Products WHERE ProductName LIKE ?", (pattern,)).fetchone()[0]
        expected_count = 503 if label == "prefix" else 3
        plan_text = " ".join(plan)
        if count != expected_count:
            raise AssertionError(f"{label} expected {expected_count} matches, got {count}")
        if label == "prefix" and "SEARCH" not in plan_text:
            raise AssertionError(f"Expected prefix index range search, got {plan!r}")
        if label == "leading_wildcard" and "SCAN" not in plan_text:
            raise AssertionError(f"Expected leading-wildcard scan, got {plan!r}")
        plans[label] = {"pattern": pattern, "query_plan": plan, "match_count": count}

    result = {
        "article_example": {"expected": EXPECTED, "actual": actual},
        "sqlite_version": sqlite3.sqlite_version,
        "python_version": platform.python_version(),
        "experiment": {"rows_added": 1000, "index": "ProductName COLLATE NOCASE", "plans": plans},
        "observations": "Prefix pattern uses an index range; leading wildcard scans the index (SQLite 3.50.4).",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
