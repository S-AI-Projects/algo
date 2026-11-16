#!/usr/bin/env python3
"""
Validation and verification suite for Issue #23 (R61-T023).
Target: docs/languages/php/php-12.md
Anchor: ## A Simple HTML Form / ## Processing Form Data

Extracts the runnable PHP examples for POST and GET from the markdown documentation,
executes them using the PHP runtime, asserts expected normal and boundary outputs,
and executes genuine negative tests by temporarily mutating extracted PHP examples
to confirm non-zero exit detection and automatic restoration.
"""

import os
import sys
import json
import shutil
import platform
import subprocess
import tempfile
from pathlib import Path

WORKDIR = Path(__file__).resolve().parent
REPO_ROOT = WORKDIR.parents[1]
DOC_PATH = REPO_ROOT / "docs" / "languages" / "php" / "php-12.md"


def log(msg: str):
    print(f"[CHECK] {msg}")


def extract_code_block(content: str, title: str, fallback_needle: str) -> str:
    """Extract code block by title marker or content needle fallback."""
    marker = f'```php title="{title}"'
    start_idx = content.find(marker)
    if start_idx != -1:
        code_start = content.find("\n", start_idx) + 1
        code_end = content.find("```", code_start)
        if code_end != -1:
            return content[code_start:code_end].strip()

    # Fallback search by needle
    start_idx = 0
    while True:
        pos = content.find("```php", start_idx)
        if pos == -1:
            break
        code_start = content.find("\n", pos) + 1
        code_end = content.find("```", code_start)
        if code_end == -1:
            break
        snippet = content[code_start:code_end].strip()
        if fallback_needle in snippet:
            return snippet
        start_idx = code_end + 3

    raise ValueError(f"Could not extract PHP code block for {title} (needle: {fallback_needle})")


def record_environment():
    php_ver = subprocess.check_output(["php", "-v"], text=True).splitlines()[0]
    php_cgi_path = shutil.which("php-cgi")
    php_cgi_ver = (
        subprocess.check_output([php_cgi_path, "-v"], text=True).splitlines()[0]
        if php_cgi_path
        else "N/A"
    )

    try:
        node_ver = subprocess.check_output(["node", "--version"], text=True).strip()
    except Exception:
        node_ver = "unknown"

    try:
        npm_ver = subprocess.check_output(["npm", "--version"], text=True).strip()
    except Exception:
        npm_ver = "unknown"

    env_data = (
        f"Runtime and Interpreter Environment for Issue #23 (R61-T023)\n"
        f"Target: docs/languages/php/php-12.md\n"
        f"--------------------------------------------------------------------------------\n"
        f"PHP Environment:\n"
        f"  php (CLI):     {php_ver}\n"
        f"  php-cgi (CGI): {php_cgi_ver} ({php_cgi_path})\n"
        f"\n"
        f"Python Runtime:\n"
        f"  python: {platform.python_version()} ({sys.executable})\n"
        f"\n"
        f"Node & NPM Environment:\n"
        f"  node: {node_ver}\n"
        f"  npm:  {npm_ver}\n"
        f"\n"
        f"OS & Architecture:\n"
        f"  system:   {platform.system()}\n"
        f"  release:  {platform.release()}\n"
        f"  machine:  {platform.machine()}\n"
        f"  platform: {platform.platform()}\n"
    )
    (WORKDIR / "environment.txt").write_text(env_data, encoding="utf-8")
    log("Recorded environment to environment.txt")


def save_test_inputs():
    inputs_json = {
        "issue": "GitHub Issue #23: R61-T023 — Compare two methods: php 12",
        "document": "docs/languages/php/php-12.md",
        "section": "A Simple HTML Form / Processing Form Data",
        "comparison": {
            "method_1": "POST (application/x-www-form-urlencoded in HTTP request body; superglobal $_POST)",
            "method_2": "GET (URL query string ?key=val; superglobal $_GET)"
        },
        "test_cases": [
            {
                "case_id": "TC-01",
                "name": "POST Normal Worked Example",
                "method": "POST",
                "inputs": {"name": "Alice", "email": "alice@example.com"},
                "wire_payload": "name=Alice&email=alice%40example.com",
                "content_length": 36,
                "expected_output": "Welcome, Alice!\nYour email is: alice@example.com\n"
            },
            {
                "case_id": "TC-02",
                "name": "GET Normal Worked Example",
                "method": "GET",
                "inputs": {"name": "Alice", "email": "alice@example.com"},
                "wire_payload": "name=Alice&email=alice%40example.com",
                "expected_output": "Welcome, Alice!\nYour email is: alice@example.com\n"
            },
            {
                "case_id": "TC-03",
                "name": "POST Boundary Case (Missing Parameters)",
                "method": "POST",
                "inputs": {},
                "wire_payload": "",
                "precondition": "Null coalescing fallback handles absent array keys without undefined key notices",
                "expected_output": "Welcome, !\nYour email is: \n"
            },
            {
                "case_id": "TC-04",
                "name": "GET Boundary Case (Missing Parameters)",
                "method": "GET",
                "inputs": {},
                "wire_payload": "",
                "precondition": "Null coalescing fallback handles absent array keys without undefined key notices",
                "expected_output": "Welcome, !\nYour email is: \n"
            },
            {
                "case_id": "TC-05",
                "name": "POST Boundary Case (Empty String Inputs)",
                "method": "POST",
                "inputs": {"name": "", "email": ""},
                "wire_payload": "name=&email=",
                "precondition": "Empty strings sanitized and rendered safely",
                "expected_output": "Welcome, !\nYour email is: \n"
            },
            {
                "case_id": "TC-06",
                "name": "GET Boundary Case (Empty String Inputs)",
                "method": "GET",
                "inputs": {"name": "", "email": ""},
                "wire_payload": "name=&email=",
                "precondition": "Empty strings sanitized and rendered safely",
                "expected_output": "Welcome, !\nYour email is: \n"
            }
        ]
    }
    (WORKDIR / "test_inputs.json").write_text(json.dumps(inputs_json, indent=2), encoding="utf-8")

    inputs_txt = (
        "Test Inputs for Issue #23 (R61-T023)\n"
        "Document: docs/languages/php/php-12.md\n"
        "Section: A Simple HTML Form / Processing Form Data\n"
        "\n"
        "Comparison: POST vs GET on Name and Email Form Fixture\n"
        "--------------------------------------------------------------------------------\n"
        "Case TC-01: POST Normal Input (Worked Example)\n"
        "  Method: POST\n"
        "  Wire Payload: name=Alice&email=alice%40example.com (Content-Length: 36)\n"
        "  Parsed: $_POST['name']='Alice', $_POST['email']='alice@example.com'\n"
        "  Expected Output: Welcome, Alice!\\nYour email is: alice@example.com\\n\n"
        "\n"
        "Case TC-02: GET Normal Input (Worked Example)\n"
        "  Method: GET\n"
        "  Wire Query String: name=Alice&email=alice%40example.com\n"
        "  Parsed: $_GET['name']='Alice', $_GET['email']='alice@example.com'\n"
        "  Expected Output: Welcome, Alice!\\nYour email is: alice@example.com\\n\n"
        "\n"
        "Case TC-03: POST Boundary Case (Missing Parameters)\n"
        "  Method: POST\n"
        "  Wire Payload: '' (empty body)\n"
        "  Precondition: $_POST['name'] ?? '' evaluates to empty string without warnings\n"
        "  Expected Output: Welcome, !\\nYour email is: \\n\n"
        "\n"
        "Case TC-04: GET Boundary Case (Missing Parameters)\n"
        "  Method: GET\n"
        "  Wire Query String: '' (empty query string)\n"
        "  Precondition: $_GET['name'] ?? '' evaluates to empty string without warnings\n"
        "  Expected Output: Welcome, !\\nYour email is: \\n\n"
        "\n"
        "Case TC-05: POST Boundary Case (Empty Strings)\n"
        "  Method: POST\n"
        "  Wire Payload: name=&email=\n"
        "  Parsed: $_POST['name']='', $_POST['email']=''\n"
        "  Expected Output: Welcome, !\\nYour email is: \\n\n"
        "\n"
        "Case TC-06: GET Boundary Case (Empty Strings)\n"
        "  Method: GET\n"
        "  Wire Query String: name=&email=\n"
        "  Parsed: $_GET['name']='', $_GET['email']=''\n"
        "  Expected Output: Welcome, !\\nYour email is: \\n\n"
    )
    (WORKDIR / "test_inputs.txt").write_text(inputs_txt, encoding="utf-8")
    log("Saved test inputs to test_inputs.json and test_inputs.txt")


def execute_php(code: str, method: str, params: str) -> str:
    """
    Executes extracted PHP code. Uses php-cgi if present for full HTTP CGI semantics,
    otherwise falls back to invoking php CLI with simulated superglobals.
    """
    php_cgi_path = shutil.which("php-cgi")
    if php_cgi_path:
        with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False) as tf:
            tf.write(code)
            fpath = tf.name

        try:
            env = os.environ.copy()
            env["REDIRECT_STATUS"] = "200"
            env["REQUEST_METHOD"] = method
            env["SCRIPT_FILENAME"] = fpath

            if method == "POST":
                env["CONTENT_TYPE"] = "application/x-www-form-urlencoded"
                env["CONTENT_LENGTH"] = str(len(params.encode("utf-8")))
                proc = subprocess.run(
                    [php_cgi_path, "-q", fpath],
                    input=params,
                    env=env,
                    capture_output=True,
                    text=True,
                    check=True
                )
            else:
                env["QUERY_STRING"] = params
                proc = subprocess.run(
                    [php_cgi_path, "-q", fpath],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=True
                )

            stdout = proc.stdout
            if "\r\n\r\n" in stdout:
                return stdout.split("\r\n\r\n", 1)[1]
            elif "\n\n" in stdout:
                return stdout.split("\n\n", 1)[1]
            return stdout
        finally:
            if os.path.exists(fpath):
                os.unlink(fpath)
    else:
        # Fallback using php CLI
        clean_code = code.strip()
        if clean_code.startswith("<?php"):
            inner_code = clean_code[5:].strip()
        else:
            inner_code = clean_code
        if inner_code.endswith("?>"):
            inner_code = inner_code[:-2].strip()

        if method == "POST":
            shim = f"parse_str('{params}', $_POST);\n"
        else:
            shim = f"parse_str('{params}', $_GET);\n"

        full_script = f"<?php\n{shim}{inner_code}\n?>"
        proc = subprocess.run(
            ["php", "-r", full_script],
            capture_output=True,
            text=True,
            check=True
        )
        return proc.stdout


def lint_php(code: str, label: str):
    log(f"Linting PHP syntax for {label} ...")
    proc = subprocess.run(["php", "-l"], input=code, capture_output=True, text=True, check=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Syntax error in {label}:\n{proc.stderr}")
    log(f"PHP syntax lint clean for {label}")


def run_positive_checks(target_doc: Path, verbose: bool = True) -> tuple:
    """Extracts PHP examples from target_doc and executes all 6 test cases."""
    if not target_doc.is_file():
        raise FileNotFoundError(f"Target documentation not found at {target_doc}")

    content = target_doc.read_text(encoding="utf-8")

    # Extract POST and GET handlers
    post_code = extract_code_block(content, "welcome_post.php", "$_POST['name']")
    get_code = extract_code_block(content, "welcome_get.php", "$_GET['name']")

    if verbose:
        log(f"Extracted welcome_post.php ({len(post_code.splitlines())} lines)")
        log(f"Extracted welcome_get.php ({len(get_code.splitlines())} lines)")

    # Lint both code snippets
    lint_php(post_code, "welcome_post.php")
    lint_php(get_code, "welcome_get.php")

    # Execute test cases
    normal_payload = "name=Alice&email=alice%40example.com"
    empty_payload = "name=&email="
    missing_payload = ""

    expected_normal = "Welcome, Alice!\nYour email is: alice@example.com\n"
    expected_boundary = "Welcome, !\nYour email is: \n"

    # TC-01: POST Normal
    actual_post_normal = execute_php(post_code, "POST", normal_payload)
    # TC-02: GET Normal
    actual_get_normal = execute_php(get_code, "GET", normal_payload)

    # TC-03: POST Missing
    actual_post_missing = execute_php(post_code, "POST", missing_payload)
    # TC-04: GET Missing
    actual_get_missing = execute_php(get_code, "GET", missing_payload)

    # TC-05: POST Empty String
    actual_post_empty = execute_php(post_code, "POST", empty_payload)
    # TC-06: GET Empty String
    actual_get_empty = execute_php(get_code, "GET", empty_payload)

    # Assertions
    assert actual_post_normal == expected_normal, f"POST normal failed: {repr(actual_post_normal)} != {repr(expected_normal)}"
    assert actual_get_normal == expected_normal, f"GET normal failed: {repr(actual_get_normal)} != {repr(expected_normal)}"
    assert actual_post_missing == expected_boundary, f"POST missing failed: {repr(actual_post_missing)} != {repr(expected_boundary)}"
    assert actual_get_missing == expected_boundary, f"GET missing failed: {repr(actual_get_missing)} != {repr(expected_boundary)}"
    assert actual_post_empty == expected_boundary, f"POST empty failed: {repr(actual_post_empty)} != {repr(expected_boundary)}"
    assert actual_get_empty == expected_boundary, f"GET empty failed: {repr(actual_get_empty)} != {repr(expected_boundary)}"

    if verbose:
        log("All 6 test assertions PASSED!")

    return (
        actual_post_normal, actual_get_normal,
        actual_post_missing, actual_get_missing,
        actual_post_empty, actual_get_empty,
        expected_normal, expected_boundary
    )


def run_genuine_negative_tests():
    """
    Genuine Negative Test:
    Temporarily modifies an extracted PHP example in docs/languages/php/php-12.md
    to produce incorrect output, executes the checker subprocess against that modified
    example, asserts that the checker fails with a non-zero exit status, and restores
    the original file in all circumstances via try...finally.
    """
    log("Executing genuine negative tests ...")
    original_doc_content = DOC_PATH.read_text(encoding="utf-8")
    script_path = str(Path(__file__).resolve())
    negative_log_entries = []

    # Case 1: Mutate welcome_post.php to emit incorrect output
    log("Negative Case 1: Temporarily mutating welcome_post.php to produce incorrect output ...")
    mutated_post_marker = 'echo "Welcome, $name!\\n";'
    corrupted_post_replacement = 'echo "Welcome, CORRUPTED_TEST_NAME!\\n";'
    assert mutated_post_marker in original_doc_content, "Target marker not found in php-12.md"

    try:
        mutated_content = original_doc_content.replace(mutated_post_marker, corrupted_post_replacement, 1)
        DOC_PATH.write_text(mutated_content, encoding="utf-8")

        # Run checker in subprocess
        proc = subprocess.run(
            [sys.executable, script_path, "--worker-check"],
            capture_output=True,
            text=True
        )

        assert proc.returncode != 0, (
            f"Expected checker to fail with non-zero exit code on corrupted POST example, but got exit code 0!\nOutput:\n{proc.stdout}"
        )
        log(f"Subprocess checker correctly failed with non-zero exit code ({proc.returncode}) on mutated POST example.")
        negative_log_entries.append(
            f"--- Negative Case 1: Mutated welcome_post.php ---\n"
            f"Exit Code: {proc.returncode} (Expected Non-Zero)\n"
            f"Captured Failure Output:\n{proc.stderr or proc.stdout}\n"
        )
    finally:
        DOC_PATH.write_text(original_doc_content, encoding="utf-8")
        log("Restored original docs/languages/php/php-12.md from Negative Case 1.")

    # Case 2: Mutate welcome_get.php to emit incorrect output
    log("Negative Case 2: Temporarily mutating welcome_get.php to produce incorrect output ...")
    mutated_get_marker = 'echo "Your email is: $email\\n";'
    corrupted_get_replacement = 'echo "Your email is: CORRUPTED_EMAIL\\n";'
    assert mutated_get_marker in original_doc_content, "Target marker not found in php-12.md"

    try:
        # Replace the second occurrence (which is in welcome_get.php)
        parts = original_doc_content.split(mutated_get_marker)
        if len(parts) >= 3:
            mutated_content = parts[0] + mutated_get_marker + parts[1] + corrupted_get_replacement + mutated_get_marker.join(parts[2:])
        else:
            mutated_content = original_doc_content.replace(mutated_get_marker, corrupted_get_replacement, 1)

        DOC_PATH.write_text(mutated_content, encoding="utf-8")

        proc = subprocess.run(
            [sys.executable, script_path, "--worker-check"],
            capture_output=True,
            text=True
        )

        assert proc.returncode != 0, (
            f"Expected checker to fail with non-zero exit code on corrupted GET example, but got exit code 0!\nOutput:\n{proc.stdout}"
        )
        log(f"Subprocess checker correctly failed with non-zero exit code ({proc.returncode}) on mutated GET example.")
        negative_log_entries.append(
            f"--- Negative Case 2: Mutated welcome_get.php ---\n"
            f"Exit Code: {proc.returncode} (Expected Non-Zero)\n"
            f"Captured Failure Output:\n{proc.stderr or proc.stdout}\n"
        )
    finally:
        DOC_PATH.write_text(original_doc_content, encoding="utf-8")
        log("Restored original docs/languages/php/php-12.md from Negative Case 2.")

    # Ensure document is pristine
    restored_content = DOC_PATH.read_text(encoding="utf-8")
    assert restored_content == original_doc_content, "Integrity check failed: restored file does not match original!"
    log("Integrity verified: docs/languages/php/php-12.md is completely intact.")

    # Save log to wrong_test_detected.txt
    (WORKDIR / "wrong_test_detected.txt").write_text("\n".join(negative_log_entries), encoding="utf-8")
    log("Saved genuine negative test evidence to wrong_test_detected.txt")


def main():
    # If run in worker-check mode, execute positive checks only and exit with appropriate status
    if len(sys.argv) > 1 and sys.argv[1] == "--worker-check":
        try:
            run_positive_checks(DOC_PATH, verbose=False)
            sys.exit(0)
        except Exception as exc:
            print(f"[WORKER-FAIL] {exc}", file=sys.stderr)
            sys.exit(1)

    log("Starting verification suite for Issue #23 (R61-T023) ...")
    record_environment()
    save_test_inputs()

    # Step 1: Run all 6 positive checks
    log("Running 6 positive test cases on target article ...")
    (
        actual_post_normal, actual_get_normal,
        actual_post_missing, actual_get_missing,
        actual_post_empty, actual_get_empty,
        expected_normal, expected_boundary
    ) = run_positive_checks(DOC_PATH, verbose=True)

    # Save expected and actual outputs
    combined_expected = (
        f"--- TC-01 POST Normal ---\n{expected_normal}"
        f"--- TC-02 GET Normal ---\n{expected_normal}"
        f"--- TC-03 POST Missing ---\n{expected_boundary}"
        f"--- TC-04 GET Missing ---\n{expected_boundary}"
        f"--- TC-05 POST Empty ---\n{expected_boundary}"
        f"--- TC-06 GET Empty ---\n{expected_boundary}"
    )
    combined_actual = (
        f"--- TC-01 POST Normal ---\n{actual_post_normal}"
        f"--- TC-02 GET Normal ---\n{actual_get_normal}"
        f"--- TC-03 POST Missing ---\n{actual_post_missing}"
        f"--- TC-04 GET Missing ---\n{actual_get_missing}"
        f"--- TC-05 POST Empty ---\n{actual_post_empty}"
        f"--- TC-06 GET Empty ---\n{actual_get_empty}"
    )

    (WORKDIR / "expected_output.txt").write_text(combined_expected, encoding="utf-8")
    (WORKDIR / "actual_output.txt").write_text(combined_actual, encoding="utf-8")

    # Write expected_vs_actual.txt comparison
    comparison_text = (
        "Expected vs. Actual Outputs for Issue #23 (R61-T023)\n"
        "Execution Target: Extracted PHP examples from docs/languages/php/php-12.md\n"
        "Validator: python3 work/R61-T023/check.py\n"
        "================================================================================\n"
        "Case TC-01: POST Normal Input (Alice, alice@example.com)\n"
        f"Expected:\n{expected_normal}"
        f"Actual:\n{actual_post_normal}"
        "Status: MATCH (PASS)\n"
        "--------------------------------------------------------------------------------\n"
        "Case TC-02: GET Normal Input (Alice, alice@example.com)\n"
        f"Expected:\n{expected_normal}"
        f"Actual:\n{actual_get_normal}"
        "Status: MATCH (PASS)\n"
        "--------------------------------------------------------------------------------\n"
        "Case TC-03: POST Boundary Case (Missing Parameters)\n"
        f"Expected:\n{expected_boundary}"
        f"Actual:\n{actual_post_missing}"
        "Status: MATCH (PASS)\n"
        "--------------------------------------------------------------------------------\n"
        "Case TC-04: GET Boundary Case (Missing Parameters)\n"
        f"Expected:\n{expected_boundary}"
        f"Actual:\n{actual_get_missing}"
        "Status: MATCH (PASS)\n"
        "--------------------------------------------------------------------------------\n"
        "Case TC-05: POST Boundary Case (Empty String Values)\n"
        f"Expected:\n{expected_boundary}"
        f"Actual:\n{actual_post_empty}"
        "Status: MATCH (PASS)\n"
        "--------------------------------------------------------------------------------\n"
        "Case TC-06: GET Boundary Case (Empty String Values)\n"
        f"Expected:\n{expected_boundary}"
        f"Actual:\n{actual_get_empty}"
        "Status: MATCH (PASS)\n"
        "================================================================================\n"
        "Overall Status: ALL CASES PERFECT MATCH\n"
    )
    (WORKDIR / "expected_vs_actual.txt").write_text(comparison_text, encoding="utf-8")
    log("Saved comparison to expected_vs_actual.txt")

    # Step 2: Genuine negative tests
    run_genuine_negative_tests()

    # Step 3: Final check to ensure normal checker passes cleanly after restoration
    log("Re-verifying normal positive checks on restored file ...")
    run_positive_checks(DOC_PATH, verbose=False)
    log("Normal checks confirmed passing after negative tests!")

    print("\n[SUCCESS] All checks passed successfully for Issue #23 (R61-T023).")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        sys.exit(1)
