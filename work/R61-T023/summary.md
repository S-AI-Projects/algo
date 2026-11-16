# Issue #23: R61-T023 — Compare Two Methods: PHP 12

## 1. Overview
This task completes GitHub Issue #23 (`R61-T023`) in the `S-AI-Projects/algo` repository and resolves all feedback from PR #61 review. The assignment focuses on **A Simple HTML Form** and **Processing Form Data** in `docs/languages/php/php-12.md`. It provides a complete, executable, and directly comparable examination of HTTP form submission methods in PHP—specifically **POST vs. GET**—using the exact same fixture: a form collecting a user's **Name** and **Email**.

## 2. Implementation Details

### Target Documentation
- **File**: `docs/languages/php/php-12.md`
- **Anchors**: `## A Simple HTML Form` and `## Processing Form Data`

### Core Concepts & Comparison on the Shared Fixture
1. **Method 1: POST Submission (`post_form.html` & `welcome_post.php`)**:
   - **Wire Transmission**: Form fields are serialized into an `application/x-www-form-urlencoded` payload located in the HTTP request body (`POST /welcome_post.php HTTP/1.1`).
   - **Payload Length**: `name=Alice&email=alice%40example.com` has an exact length of **36 bytes**, accurately reflected as `Content-Length: 36`.
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
     - POST: Body is `name=Alice&email=alice%40example.com` (36 bytes) -> `$_POST` populated
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

The improved automated verification suite:
1. Dynamically extracts the executable PHP scripts (`welcome_post.php` and `welcome_get.php`) directly from their markdown code blocks in `docs/languages/php/php-12.md`.
2. Performs syntax linting via `php -l` on both extracted code snippets.
3. Executes both methods across normal inputs, missing parameter boundaries, and empty string boundaries using authentic CGI semantics (`php-cgi`) with fallback to CLI `php`.
4. Asserts that actual execution outputs strictly match expected outputs for all 6 positive test cases.
5. Executes **genuine negative tests**:
   - Temporarily mutates `welcome_post.php` in `docs/languages/php/php-12.md` to produce corrupted output.
   - Runs a worker instance of `check.py` against the mutated document and confirms it detects the mismatch and exits with a non-zero exit code (`1`).
   - Restores the original document automatically via a `try...finally` block.
   - Temporarily mutates `welcome_get.php` in `docs/languages/php/php-12.md` to produce corrupted output.
   - Confirms non-zero exit (`1`) and restores the original document via `try...finally`.
   - Confirms that normal checks still pass after restoration and verifies document integrity.
6. Records all diagnostic logs and evidence in `work/R61-T023/`:
   - `check.py`: Complete test harness with positive and genuine negative tests
   - `environment.txt`: Toolchain and runtime version specifications
   - `test_inputs.json` / `test_inputs.txt`: Test cases and preconditions
   - `expected_output.txt` / `actual_output.txt`: Raw execution output streams
   - `expected_vs_actual.txt`: Detailed side-by-side comparison
   - `wrong_test_detected.txt`: Negative test assertion record showing non-zero exits on mutated code
   - `build_test_results.txt`: Terminal execution log of `python3 work/R61-T023/check.py && npm run build`

## 4. Docusaurus Build Warning Investigation

During `npm run build`, the following pre-existing warnings were investigated:
1. **Broken `#explore` anchor on `/algo/stories/` and `/algo/hi/stories/`**:
   - **Root Cause**: In `src/pages/stories/index.tsx`, line 44 uses `<Link to="#explore">Read Catalog</Link>`, and line 54 renders `<section id="explore">`. Docusaurus's anchor validation on localized page routes (such as `/algo/hi/stories/`) flags in-page hash links on custom React pages where SSR DOM IDs are evaluated prior to client hydration.
   - **Disposition**: Modifying `src/pages/stories/index.tsx` is completely outside the scope of this PHP documentation task. Repository rules strictly forbid editing unrelated files. Docusaurus handles this warning via its `onBrokenAnchors: 'warn'` setting, allowing the build to complete with exit code 0.
2. **Missing optional `bufferutil` and `utf-8-validate` modules**:
   - **Root Cause**: The WebSocket client dependency (`ws`) in `node_modules` includes optional native C++ bindings for acceleration. When they are not installed, `ws` falls back to its built-in pure JavaScript implementation. Webpack emits an informational module-not-found warning on server bundling.
   - **Disposition**: Purely an upstream optional dependency warning; requires no changes to task files and does not affect the site build.

## 5. Test Results
- `python3 work/R61-T023/check.py`: **PASS** (6/6 positive assertions passed, 2 genuine negative tests passed with non-zero exit detection and automatic restoration, exit code 0)
- PHP Syntax Lint (`php -l`): **PASS** (0 syntax errors)
- `npm run build`: **PASS** (Docusaurus production build completed successfully, exit code 0)
