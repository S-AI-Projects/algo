---

id: bitap-algo  
sidebar_position: 3  
title: Bitap Algorithm  
sidebar_label: Bitap Algorithm  

---

### Definition:

The Bitap algorithm, also known as the **Shift-Or**, **Shift-And**, or **Bitap for Approximate String Matching**, is a string matching algorithm that efficiently finds patterns in a text with possible mismatches or errors. The algorithm leverages bitwise operations to perform both exact and approximate string matching, making it ideal for fuzzy searching.

### Reproducible Execution & Environment Contract:

To guarantee deterministic, portable execution across operating systems and compilers:
1. **Locale Management**: Character bitmask construction depends on byte values. We pin the process-global locale to `"C"` via `std::setlocale(LC_ALL, "C")` to ensure uniform ASCII behavior regardless of ambient system configurations, and restore the original locale prior to termination.
2. **Character Domain Mapping**: Characters are cast via `static_cast<unsigned char>` to guarantee non-negative indices in the range `[0, 255]`, preventing undefined behavior or memory corruption on platforms where `char` defaults to signed.
3. **Boundary Guarantees**:
   - When pattern length $m$ exceeds text length $n$ ($m > n$), the algorithm early-exits safely in $O(1)$ time.
   - Exact matching ($k = 0$ allowed errors) functions as a strict substring locator.
   - Single-character patterns are matched correctly at string boundaries (indices $0$ and $n-1$).

### Video Explanation

<LiteYouTubeEmbed
  id="jXNj27TMQRU"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Bitap algorithm for fuzzy matching explained with example"
  poster="maxresdefault"
  lazyLoad={true}
  webp
/>

### Characteristics:

- **Bitwise Matching**:
  - The Bitap algorithm uses bitwise operations to compare the pattern against the text. Each bit represents whether a character in the text matches a position in the pattern.

- **Approximate Matching**:
  - It supports approximate matching, where the pattern may have a certain number of mismatches, insertions, or deletions. This is especially useful in fields like text retrieval or DNA sequence matching.

- **Pattern Masking**:
  - The pattern is preprocessed into bitmasks, which are then used during the text scan to track how much of the pattern has been matched, including the handling of allowed errors.

- **Linear Search with Errors**:
  - The algorithm scans the text linearly, and the number of allowed errors (insertions, deletions, substitutions) is parameterized, allowing for flexible search criteria.

### Time Complexity:

- **Best Case: $O\left(\frac{n}{w}\right)$**  
  The best-case complexity is linear, as the algorithm processes `w` characters in parallel per word size `w` of the machine.

- **Average Case: $O(n)$**  
  On average, the algorithm performs in linear time with respect to the text size `n`, especially for small patterns or when only a few errors are allowed.

- **Worst Case: $O(n \times m)$**  
  In the worst case, if the pattern is large or if there are many errors allowed, the time complexity can degrade to quadratic, where `m` is the pattern length.

### Space Complexity:

- **Space Complexity: $O(m)$**  
  The algorithm requires space proportional to the pattern length `m` for storing bitmasks, making it efficient in terms of memory usage.

### C++ Implementation:

**Approximate Matching with `k` Allowed Errors**
```cpp
#include <iostream>
#include <vector>
#include <string>
#include <cassert>
#include <clocale>
using namespace std;

#define CHAR_SIZE 256 // Extended ASCII

void preprocessPattern(const string& pattern, vector<int>& patternMask) {
    int m = pattern.size();
    for (int i = 0; i < CHAR_SIZE; ++i) {
        patternMask[i] = ~0;
    }
    for (int i = 0; i < m; ++i) {
        patternMask[static_cast<unsigned char>(pattern[i])] &= ~(1 << i);
    }
}

vector<int> bitapSearch(const string& text, const string& pattern, int maxErrors, bool verbose = true) {
    vector<int> matches;
    int n = text.size();
    int m = pattern.size();

    if (m > n || m == 0) return matches;

    vector<int> patternMask(CHAR_SIZE);
    preprocessPattern(pattern, patternMask);

    vector<int> R(maxErrors + 1, ~0);
    for (int i = 0; i <= maxErrors; ++i) {
        R[i] = ~1; // All bits set except the least significant bit
    }

    for (int i = 0; i < n; ++i) {
        int oldR_jMinus1 = ~0;
        for (int j = 0; j <= maxErrors; ++j) {
            int temp = R[j];
            R[j] = ((R[j] << 1) | patternMask[static_cast<unsigned char>(text[i])]);
            if (j > 0) {
                R[j] &= (oldR_jMinus1 << 1) | (R[j - 1] << 1) | oldR_jMinus1;
            }
            oldR_jMinus1 = temp;
        }
        if ((R[maxErrors] & (1 << (m - 1))) == 0) {
            int matchIdx = i - m + 1;
            matches.push_back(matchIdx);
            if (verbose) {
                cout << "Pattern found at index " << matchIdx << " with " << maxErrors << " allowed errors." << endl;
            }
        }
    }
    return matches;
}

int main() {
    // 1. Fix process-global locale to "C" for reproducible ASCII character handling
    const char* prevLocale = setlocale(LC_ALL, nullptr);
    string savedLocale = prevLocale ? prevLocale : "C";
    setlocale(LC_ALL, "C");

    // Worked example from article
    string text = "this is a simple example";
    string pattern = "example";
    int maxErrors = 1; // Allow 1 error (insertion, deletion, or substitution)

    vector<int> matches = bitapSearch(text, pattern, maxErrors);

    // Worked example assertion
    assert(matches.size() == 1 && matches[0] == 17);

    // Boundary case 1: Exact match with 0 errors
    assert(bitapSearch("this is a simple example", "example", 0, false) == vector<int>{17});

    // Boundary case 2: Pattern longer than text (m > n)
    assert(bitapSearch("short", "longer pattern", 1, false).empty());

    // Boundary case 3: Single-character pattern at boundaries
    assert(bitapSearch("abcdef", "a", 0, false) == vector<int>{0});
    assert(bitapSearch("abcdef", "f", 0, false) == vector<int>{5});

    // Boundary case 4: Pattern not present in text
    assert(bitapSearch("hello world", "xyz", 1, false).empty());

    // 2. Restore process-global locale setting
    setlocale(LC_ALL, savedLocale.c_str());

    return 0;
}
```

### Summary:

The Bitap algorithm is a highly efficient string matching technique that supports approximate matching, making it ideal for applications requiring fuzzy search capabilities. Its use of bitwise operations allows for fast text scanning, while its flexibility in handling errors sets it apart from other exact matching algorithms. Despite its quadratic worst-case complexity, it performs well for small patterns and a limited number of errors.