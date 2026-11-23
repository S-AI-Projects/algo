#!/usr/bin/env python3
"""
Validation check for Issue #21 (R61-T021) - C# 9 Interface Example Executability

This script:
1. Extracts the actual C# interface example directly from docs/languages/csharp/csharp-9.md.
2. Compiles and executes the extracted C# code using the installed dotnet runtime.
3. Asserts the exact expected output for the worked example ("Bark") and boundary case ("Silence").
4. Verifies that a deliberately incorrect output comparison causes assertion failure.
5. Propagates subprocess errors and returns non-zero on failure.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile


def get_doc_path():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    doc_path = os.path.join(repo_root, "docs", "languages", "csharp", "csharp-9.md")
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"Markdown document not found at: {doc_path}")
    return doc_path


def extract_csharp_example(doc_path):
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match all ```csharp ... ``` blocks in the markdown file
    pattern = r"```csharp\s*\n(.*?)```"
    code_blocks = re.findall(pattern, content, re.DOTALL)

    # Find the executable example block containing IAnimal and Program Main
    target_block = None
    for block in code_blocks:
        if "interface IAnimal" in block and "class Program" in block and "static void Main" in block:
            target_block = block
            break

    if not target_block:
        raise ValueError(
            "Could not find the executable C# interface example block containing IAnimal and Program.Main in docs/languages/csharp/csharp-9.md"
        )

    return target_block.strip()


def get_dotnet_target_framework():
    # Detect installed dotnet major version to target matching TFM (e.g. net11.0, net9.0, net8.0)
    try:
        proc = subprocess.run(["dotnet", "--version"], capture_output=True, text=True, check=True)
        version_str = proc.stdout.strip()
        major = version_str.split(".")[0]
        return f"net{major}.0", version_str
    except Exception as e:
        raise RuntimeError(f"Failed to query dotnet version: {e}")


def execute_csharp_code(code_str, tfm):
    dotnet_bin = shutil.which("dotnet")
    if not dotnet_bin:
        raise RuntimeError("dotnet binary not found in PATH")

    with tempfile.TemporaryDirectory(dir="/tmp") as tmpdir:
        cs_file = os.path.join(tmpdir, "Program.cs")
        with open(cs_file, "w", encoding="utf-8") as f:
            f.write(code_str)

        csproj_file = os.path.join(tmpdir, "InterfaceExample.csproj")
        csproj_content = f"""<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>{tfm}</TargetFramework>
    <ImplicitUsings>disable</ImplicitUsings>
    <Nullable>disable</Nullable>
  </PropertyGroup>
</Project>
"""
        with open(csproj_file, "w", encoding="utf-8") as f:
            f.write(csproj_content)

        env = os.environ.copy()
        env["DOTNET_CLI_HOME"] = os.path.join(tmpdir, ".dotnet_home")
        env["DOTNET_NOLOGO"] = "1"
        env["DOTNET_CLI_TELEMETRY_OPTOUT"] = "1"
        env["DOTNET_CLI_DO_NOT_USE_MSBUILD_SERVER"] = "1"

        run_proc = subprocess.run(
            [dotnet_bin, "run", "--project", tmpdir],
            capture_output=True,
            text=True,
            env=env
        )

        return run_proc


def parse_clean_output(stdout_text):
    # Filter out any informational telemetry / msbuild warning lines from stdout
    clean_lines = []
    for line in stdout_text.splitlines():
        trimmed = line.strip()
        if not trimmed:
            continue
        if trimmed.startswith("MSBuild") or trimmed.startswith("CSSM"):
            continue
        clean_lines.append(trimmed)
    return clean_lines


def test_deliberate_failure(actual_lines):
    """
    Verify that deliberately incorrect expected output causes assertion failure.
    """
    incorrect_expected = ["Bark", "Meow"]
    try:
        assert actual_lines == incorrect_expected, "Deliberate mismatch assertion"
        # If no assertion error, the negative test failed
        return False
    except AssertionError:
        return True


def main():
    print("=== Step 1: Locating and reading markdown article ===")
    doc_path = get_doc_path()
    print(f"Document path: {doc_path}")

    print("\n=== Step 2: Extracting C# interface example from markdown ===")
    csharp_code = extract_csharp_example(doc_path)
    print(f"Successfully extracted {len(csharp_code.splitlines())} lines of C# code from markdown.")
    print("--- Extracted Code Snippet (first 10 lines) ---")
    for line in csharp_code.splitlines()[:10]:
        print(f"  {line}")
    print("  ...")

    print("\n=== Step 3: Detecting .NET runtime and SDK ===")
    tfm, dotnet_version = get_dotnet_target_framework()
    print(f"Installed dotnet version: {dotnet_version}")
    print(f"Target framework moniker (TFM): {tfm}")

    print("\n=== Step 4: Compiling and executing extracted C# code ===")
    proc = execute_csharp_code(csharp_code, tfm)

    if proc.returncode != 0:
        print("ERROR: Subprocess execution failed with non-zero return code!", file=sys.stderr)
        print(f"Return code: {proc.returncode}", file=sys.stderr)
        print(f"Stdout:\n{proc.stdout}", file=sys.stderr)
        print(f"Stderr:\n{proc.stderr}", file=sys.stderr)
        sys.exit(proc.returncode)

    actual_lines = parse_clean_output(proc.stdout)
    print("Actual stdout lines received:")
    for line in actual_lines:
        print(f"  > {line}")

    print("\n=== Step 5: Asserting expected outputs ===")
    expected_lines = ["Bark", "Silence"]
    print(f"Expected output lines: {expected_lines}")

    # Assert exact match
    if actual_lines != expected_lines:
        print(f"ASSERTION FAILURE: Expected {expected_lines}, but got {actual_lines}", file=sys.stderr)
        sys.exit(1)
    print("PASS: Exact output assertion matches expected [worked example: 'Bark', boundary: 'Silence'].")

    print("\n=== Step 6: Verifying deliberately incorrect output causes check failure ===")
    negative_test_passed = test_deliberate_failure(actual_lines)
    if not negative_test_passed:
        print("ERROR: Negative test failed! Incorrect output did not raise AssertionError.", file=sys.stderr)
        sys.exit(1)
    print("PASS: Deliberately incorrect output correctly triggered AssertionError.")

    print("\n==========================================")
    print(" ALL CHECKS PASSED: C# example is runnable and valid!")
    print("==========================================")
    sys.exit(0)


if __name__ == "__main__":
    main()

