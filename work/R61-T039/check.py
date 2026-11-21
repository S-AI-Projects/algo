import re, subprocess
from pathlib import Path

t = Path("docs/languages/swift/merge-sort.md").read_text(encoding="utf-8")
sw = re.search(r"```swift\n(.*?)\n```", t, re.DOTALL).group(1)
out = re.search(r"### Example Output\s+```plaintext\n(.*?)\n```", t, re.DOTALL).group(1).strip()

act = subprocess.run(["swift", "-"], input=sw, capture_output=True, text=True, check=True).stdout.strip()
assert act == out, f"Mismatch:\n{act}\n!=\n{out}"
assert act != out.replace("[5, 6, 7, 11, 12, 13]", "[12, 11, 13, 5, 6, 7]", 1)
print("PASS: Published Swift Merge Sort example executed and matched expected output.")
print(act)
