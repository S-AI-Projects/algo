#!/usr/bin/env python3
"""Execute the PHP example published under Creating Strings."""
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / "docs/languages/php/php-8.md"
EXPECTED = "Hello, Alice!\nHello, !\n"


def published_example() -> str:
    text = ARTICLE.read_text(encoding="utf-8")
    section = text.split("## Creating Strings", 1)[1].split("\n* * *", 1)[0]
    start = section.index("```php") + len("```php")
    return section[start:section.index("```", start)].strip() + "\n"


def run(source: str) -> str:
    with tempfile.TemporaryDirectory(prefix="r61-t001-") as temp:
        path = Path(temp) / "example.php"
        path.write_text(source, encoding="utf-8")
        return subprocess.check_output(["php", str(path)], text=True, stderr=subprocess.STDOUT)


def main() -> None:
    php = shutil.which("php")
    if not php:
        raise SystemExit("PHP CLI is required (php was not found on PATH).")
    source = published_example()
    actual = run(source)
    if actual != EXPECTED:
        raise AssertionError(f"published example output mismatch\nexpected: {EXPECTED!r}\nactual:   {actual!r}")
    # Prove the assertion catches a deliberately incorrect expected result.
    try:
        wrong_expected = EXPECTED.replace("Hello, Alice!", "Hello, Bob!")
        if actual != wrong_expected:
            raise AssertionError("deliberate mismatch")
    except AssertionError:
        pass
    else:
        raise AssertionError("negative check did not reject a wrong result")

    out = Path(__file__).parent
    (out / "inputs.txt").write_text("Alice\n(empty name)\n", encoding="utf-8")
    (out / "expected.txt").write_text(EXPECTED, encoding="utf-8")
    (out / "actual.txt").write_text(actual, encoding="utf-8")
    version = subprocess.check_output([php, "-v"], text=True).splitlines()[0]
    (out / "tool-versions.txt").write_text(f"{version}\nPython {__import__('sys').version.split()[0]}\n", encoding="utf-8")
    print("PASS: extracted PHP example output matches; deliberate mismatch rejected.")


if __name__ == "__main__":
    main()
