# Issue #23: R61-T023 — Compare Two Methods: PHP 12

## 1. Overview
This task completes GitHub Issue #23 (`R61-T023`) in the `S-AI-Projects/algo` repository. The assignment focuses on **A Simple HTML Form** and **Processing Form Data** in `docs/languages/php/php-12.md`. It provides a complete, executable, and directly comparable examination of HTTP form submission methods in PHP—specifically **POST vs. GET**—using the exact same fixture: a form collecting a user's **Name** and **Email**.

## 2. Implementation Details

### Target Documentation
- **File**: `docs/languages/php/php-12.md`
- **Anchors**: `## A Simple HTML Form` and `## Processing Form Data`

### Core Concepts & Comparison on the Shared Fixture
1. **Method 1: POST Submission (`post_form.html` & `welcome_post.php`)**:
   - **Wire Transmission**: Form fields are serialized into an `application/x-www-form-urlencoded` payload located in the HTTP request body (`POST /welcome_post.php HTTP/1.1`).
   - **Privacy & History**: Values are omitted from the browser URL address bar and access logs, making POST suitable for sensitive information and state changes.
   - **PHP Superglobal**: PHP automatically parses the request body into `$_POST` (e.g. `$_POST['name'] = 'Alice'`, `$_POST['email'] = 'alice@example.com'`). Raw unparsed bytes remain accessible via `php://input`.
   - **Sanitization & Output**: `htmlspecialchars($_POST['name'] ?? '')` neutralizes HTML special characters to prevent Cross-Site Scripting (XSS).

2. **Method 2: GET Submission (`get_form.html` & `welcome_get.php`)**:
   - **Wire Transmission**: Form fields are serialized into the URL query string appended to the destination path (`GET /welcome_get.php?name=Alice&email=alice%40example.com HTTP/1.1`). The HTTP request body is empty.
   - **Visibility & Bookmarking**: Data is visible in the address bar, browser history, and server logs. GET requests are idempotent and bookmarkable, but constrained by browser/server URL length limits (~2048 chars).
   - **PHP Superglobal**: The server sets `QUERY_STRING`, which PHP parses into `$_GET` (e.g. `$_GET['name'] = 'Alice'`, `$_GET['email'] = 'alice@example.com'`).
   - **Sanitization & Output**: `htmlspecialchars($_GET['name'] ?? '')` safely renders user data.

3. **Worked Example (Normal Input)**:
   - **Inputs**: Name = `Alice`, Email = `alice@example.com`
   - **Intermediate State**:
     - POST: Body is `name=Alice&email=alice%40example.com` -> `$_POST` populated
     - GET: Query is `?name=Alice&email=alice%40example.com` -> `$_GET` populated
   - **Execution Output (Identical for Both)**:
     ```text
     Welcome, Alice!
     Your email is: alice@example.com
     ```

4. **Boundary Example (Missing or Empty Input)**:
   - **Precondition & Contract**: In PHP 8+, accessing an undefined array key (e.g., direct navigation to the handler without submitting form data) triggers an `Undefined array key` warning. The null coalescing operator (`?? ''`) guarantees safe fallback to empty strings without generating runtime notices.
   - **Cases Tested**:
     - Omitted keys / direct page hit (`POST` with empty body, `GET` with empty query string).
     - Submitting blank form inputs (`name=&email=`).
   - **Execution Output for Boundary Cases (Both Methods)**:
     ```text
     Welcome, !
     Your email is: 
     ```

## 3. Verification Suite (`work/R61-T023/check.py`)

The automated verification suite:
1. Reads `docs/languages/php/php-12.md` and dynamically extracts the executable PHP scripts (`welcome_post.php` and `welcome_get.php`) directly from their markdown code blocks.
2. Performs syntax linting via `php -l` on both extracted code snippets.
3. Executes both methods across normal inputs, missing parameter boundaries, and empty string boundaries using authentic CGI semantics (`php-cgi`) with fallback to CLI `php`.
4. Asserts that actual execution outputs strictly match expected outputs for all 6 test cases.
5. Performs a negative test with intentionally mismatched output to confirm that assertion failures are accurately detected.
6. Records all diagnostic logs and evidence in `work/R61-T023/`:
   - `check.py`: Complete test harness
   - `environment.txt`: Toolchain and runtime version specifications
   - `test_inputs.json` / `test_inputs.txt`: Test cases and preconditions
   - `expected_output.txt` / `actual_output.txt`: Raw execution output streams
   - `expected_vs_actual.txt`: Detailed side-by-side comparison
   - `wrong_test_detected.txt`: Negative test assertion record
   - `build_test_results.txt`: Terminal execution log of `python3 work/R61-T023/check.py && npm run build`

## 4. Test Results
- `python3 work/R61-T023/check.py`: **PASS** (6/6 positive assertions passed, negative assertion detected, exit code 0)
- `npm run build`: **PASS** (Docusaurus production build completed successfully, exit code 0)
