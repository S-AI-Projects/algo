# Verification Report: R61-T041 Modular Exponentiation Algorithm

## Tool Versions
- **Python**: 3.14.7 (v3.14.7:823f0323ee6, Aug  5 2026, 07:07:01) [Clang 21.0.0 (clang-2100.1.1.101)]
- **Node**: v24.18.0
- **npm**: 11.16.0
- **Platform**: macOS-27.0.1-arm64-arm-64bit-Mach-O

## Checks Summary
| Check | Input | Expected | Actual | Status |
|---|---|---|---|---|
| Worked Example | `(2, 10, 1000)` | `24` | `24` | PASS |
| Boundary Example (`exp=0`) | `(2, 0, 1000)` | `1` | `1` | PASS |
| Deliberate Wrong Result | `(2, 10, 1000) == 999` | Non-zero exit (AssertionError) | Exit code 1 | PASS |

## Concrete State Trace (`modular_exponentiation(2, 10, 1000)`)
- Initial: `base = 2 % 1000 = 2`, `exp = 10`, `result = 1`
- Iteration 1 (`exp = 10` is even): `base = (2 * 2) % 1000 = 4`, `exp = 5`, `result = 1`
- Iteration 2 (`exp = 5` is odd): `result = (1 * 4) % 1000 = 4`, `base = (4 * 4) % 1000 = 16`, `exp = 2`
- Iteration 3 (`exp = 2` is even): `base = (16 * 16) % 1000 = 256`, `exp = 1`, `result = 4`
- Iteration 4 (`exp = 1` is odd): `result = (4 * 256) % 1000 = 1024 % 1000 = 24`, `base = (256 * 256) % 1000 = 536`, `exp = 0`
- Terminate (`exp = 0`): returns `result = 24`.
