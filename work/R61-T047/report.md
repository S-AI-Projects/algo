# Verification Report: R61-T047 SQL CASE Expression Step-by-Step Derivation

## Tool Versions
- **SQLite**: 3.50.4
- **Python**: 3.14.7 (v3.14.7:823f0323ee6, Aug  5 2026, 07:07:01) [Clang 21.0.0 (clang-2100.1.1.101)]
- **Node**: v24.18.0
- **npm**: 11.16.0
- **Platform**: macOS-27.0.1-arm64-arm-64bit-Mach-O

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
