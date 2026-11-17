#!/usr/bin/env python3
"""Compile and run the C# example extracted from the Functions in C# article."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import os

ROOT = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / "docs/languages/csharp/csharp-3.md"
EXPECTED = (
    "Subtract(10, 5) = 5\n"
    "int after method = 5\n"
    "array element after method = 99\n"
    "Subtract(5, 5) = 0\n"
)


def main() -> None:
    dotnet = shutil.which("dotnet")
    if not dotnet:
        raise SystemExit(".NET SDK is required (dotnet was not found on PATH).")
    text = ARTICLE.read_text(encoding="utf-8")
    section = text.split("### Copy and Resource Behavior of Value Parameters", 1)[1]
    start = section.index("```csharp") + len("```csharp")
    code = section[start:section.index("```", start)].strip() + "\n"
    with tempfile.TemporaryDirectory(prefix="r61-t009-") as temp:
        directory = Path(temp)
        (directory / "Program.cs").write_text(code, encoding="utf-8")
        (directory / "Example.csproj").write_text(
            '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><OutputType>Exe</OutputType>'
            '<TargetFramework>net11.0</TargetFramework><ImplicitUsings>enable</ImplicitUsings>'
            '<Nullable>enable</Nullable></PropertyGroup></Project>', encoding="utf-8"
        )
        env = os.environ.copy()
        env.update({
            "DOTNET_ROOT": "/opt/homebrew/opt/dotnet/libexec",
            "DOTNET_CLI_HOME": str(directory / "dotnet-home"),
            "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
            "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
            "NUGET_PACKAGES": str(directory / "nuget-packages"),
        })
        actual = subprocess.check_output(
            [dotnet, "run", "--project", str(directory / "Example.csproj"), "--configuration", "Release"],
            text=True, stderr=subprocess.STDOUT, env=env,
        )
    # SDK restore may emit informational lines; compare the four program lines exactly.
    lines = [line for line in actual.splitlines() if line.startswith(("Subtract(", "int after", "array element"))]
    actual_output = "\n".join(lines) + "\n"
    if actual_output != EXPECTED:
        raise AssertionError(f"output mismatch\nexpected: {EXPECTED!r}\nactual:   {actual_output!r}\nfull output:\n{actual}")
    out = Path(__file__).parent
    (out / "inputs.txt").write_text("Subtract(10, 5); Increment(5); ReplaceFirst(new[] {5}); Subtract(5, 5)\n", encoding="utf-8")
    (out / "expected.txt").write_text(EXPECTED, encoding="utf-8")
    (out / "actual.txt").write_text(actual_output, encoding="utf-8")
    env = os.environ.copy()
    env.update({"DOTNET_ROOT": "/opt/homebrew/opt/dotnet/libexec", "DOTNET_CLI_HOME": str(Path(__file__).parent / ".dotnet-home"), "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1", "DOTNET_CLI_TELEMETRY_OPTOUT": "1"})
    version = subprocess.check_output([dotnet, "--version"], text=True, env=env).strip()
    (out / "tool-versions.txt").write_text(f".NET SDK {version}\nPython {sys.version.split()[0]}\n", encoding="utf-8")
    print("PASS: C# value and array-reference behavior matched the published output.")


if __name__ == "__main__":
    main()
