---
id: odd-even-sort-algo  
sidebar_position: 19  
title: Odd-Even Sort  
sidebar_label: Odd-Even Sort
description: "Complete guide to Odd-Even Sort, a parallel sorting algorithm that alternates between odd and even phases to gradually sort the array."
tags: [sorting algorithms, odd even sort, parallel sorting, dsa]

---

### Definition:

Odd-Even Sort (also known as Odd-Even Transposition Sort) is a simple parallel sorting algorithm that works by repeatedly performing two phases: an odd phase and an even phase. It compares and swaps adjacent elements in two passes, which gradually sorts the array. It is mainly used in parallel computing environments due to its ability to be implemented efficiently across multiple processors.

### Loop Invariant & State Verification:

The correctness of Odd-Even Sort is governed by the following state invariants:

1. **Phase Invariant**:
   - **Odd Phase**: For every odd index $i \in \{1, 3, 5, \dots\}$ such that $i < n - 1$, after the odd-phase pass completes, $arr[i] \le arr[i + 1]$. Because all odd-indexed pairs $(i, i+1)$ are disjoint, each comparison-swap operation is mutually independent.
   - **Even Phase**: For every even index $i \in \{0, 2, 4, \dots\}$ such that $i < n - 1$, after the even-phase pass completes, $arr[i] \le arr[i + 1]$. All even-indexed pairs $(i, i+1)$ are likewise disjoint and independent.

2. **Monotonic Inversion Reduction**:
   Let $\text{inv}(arr) = \sum_{j < k} \mathbf{1}[arr[j] > arr[k]]$ denote the number of inversions. Whenever $\text{inv}(arr) > 0$, at least one pair is out of order and will be swapped during the alternating phases, strictly reducing $\text{inv}(arr)$ on every iteration where swaps occur until $\text{inv}(arr) = 0$.

3. **Termination & Postcondition Invariant**:
   The algorithm terminates when both the odd and even phases complete consecutively with zero swaps (`isSorted == true`). At termination:
   $$\forall i \in \{0, 1, \dots, n-2\}, \quad arr[i] \le arr[i + 1]$$
   The multiset of elements is invariant ($\text{multiset}(arr_{\text{final}}) = \text{multiset}(arr_{\text{initial}})$), guaranteeing a complete, stable non-decreasing permutation.

4. **Preconditions & Boundary Behavior**:
   - **Precondition**: The input array must be non-null (`arr != null`).
   - **Empty array ($n = 0$) and Single-element array ($n = 1$)**: The loop conditions $i < n - 1$ evaluate to $i < -1$ and $i < 0$ respectively. No iterations occur, zero swaps are performed, and the algorithm terminates safely in $O(1)$ time with the invariant trivially satisfied.

### Video Explanation

<LiteYouTubeEmbed
  id="Sazh4Y-WlDk"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Odd Even Transposition Parallel Formulation || Bubble Sort and it's Variants || Explained in Hindi"
  poster="maxresdefault"
  lazyLoad={true}
  webp
/>

### Characteristics:

- **Two Phases**:  
  The algorithm alternates between an odd phase (comparing elements at odd indexes with their next even index) and an even phase (comparing elements at even indexes with their next odd index).

- **In-Place**:  
  The algorithm sorts the array without requiring any additional storage, modifying the input array directly.

- **Not Stable**:  
  Odd-Even Sort is not stable, meaning that the relative order of equal elements may not be preserved.

### Time Complexity:

- **Best Case: O(n)**  
  When the array is already sorted, the algorithm only requires one pass.

- **Average Case: O(n²)**  
The average time complexity is quadratic, similar to other simple sorting algorithms.

- **Worst Case: O(n²)**  
The worst-case scenario occurs when the array is in reverse order.

### Space Complexity:

- **Space Complexity: O(1)**  
The algorithm operates in constant space, only using a few variables for swapping.

### Java Implementation:

```java
public class OddEvenSort {

    // Method to perform Odd-Even Sort
    public static void oddEvenSort(int[] arr) {
        boolean isSorted = false;
        int n = arr.length;

        while (!isSorted) {
            isSorted = true;

            // Odd phase
            for (int i = 1; i < n - 1; i += 2) {
                if (arr[i] > arr[i + 1]) {
                    swap(arr, i, i + 1);
                    isSorted = false;
                }
            }

            // Even phase
            for (int i = 0; i < n - 1; i += 2) {
                if (arr[i] > arr[i + 1]) {
                    swap(arr, i, i + 1);
                    isSorted = false;
                }
            }
        }
    }

    // Helper method to swap two elements
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    // Invariant verifier: checks that elements are sorted in non-decreasing order
    public static boolean isSortedInvariant(int[] arr) {
        if (arr == null) return true;
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i] > arr[i + 1]) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        // Worked example from article
        int[] arr = {5, 3, 1, 4, 2};
        oddEvenSort(arr);
        System.out.println("Sorted array:");
        for (int num : arr) {
            System.out.print(num + " ");
        }
        System.out.println();

        // 1. Assert worked example output and invariant
        assert java.util.Arrays.equals(arr, new int[]{1, 2, 3, 4, 5}) : "Worked example assertion failed";
        assert isSortedInvariant(arr) : "Worked example invariant failed";

        // 2. Boundary variation 1: Empty array (n = 0)
        int[] emptyArr = {};
        oddEvenSort(emptyArr);
        assert java.util.Arrays.equals(emptyArr, new int[]{}) : "Empty array assertion failed";
        assert isSortedInvariant(emptyArr) : "Empty array invariant failed";

        // 3. Boundary variation 2: Single-element array (n = 1)
        int[] singleArr = {42};
        oddEvenSort(singleArr);
        assert java.util.Arrays.equals(singleArr, new int[]{42}) : "Single element assertion failed";
        assert isSortedInvariant(singleArr) : "Single element invariant failed";

        // 4. Variation 3: Already sorted array (0 inversions)
        int[] sortedArr = {1, 2, 3, 4, 5};
        oddEvenSort(sortedArr);
        assert java.util.Arrays.equals(sortedArr, new int[]{1, 2, 3, 4, 5}) : "Already sorted assertion failed";
        assert isSortedInvariant(sortedArr) : "Already sorted invariant failed";

        // 5. Variation 4: Reverse sorted array (maximum inversions)
        int[] reverseArr = {5, 4, 3, 2, 1};
        oddEvenSort(reverseArr);
        assert java.util.Arrays.equals(reverseArr, new int[]{1, 2, 3, 4, 5}) : "Reverse sorted assertion failed";
        assert isSortedInvariant(reverseArr) : "Reverse sorted invariant failed";

        // 6. Variation 5: Duplicate elements (non-distinct keys)
        int[] dupArr = {4, 2, 2, 4, 1, 3};
        oddEvenSort(dupArr);
        assert java.util.Arrays.equals(dupArr, new int[]{1, 2, 2, 3, 4, 4}) : "Duplicates assertion failed";
        assert isSortedInvariant(dupArr) : "Duplicates invariant failed";

        // 7. Variation 6: Array with negative numbers and zero
        int[] negArr = {-3, 0, -1, 5, -2};
        oddEvenSort(negArr);
        assert java.util.Arrays.equals(negArr, new int[]{-3, -2, -1, 0, 5}) : "Negative numbers assertion failed";
        assert isSortedInvariant(negArr) : "Negative numbers invariant failed";

        // 8. Variation 7: Two-element inverted array (single inversion)
        int[] twoArr = {2, 1};
        oddEvenSort(twoArr);
        assert java.util.Arrays.equals(twoArr, new int[]{1, 2}) : "Two elements assertion failed";
        assert isSortedInvariant(twoArr) : "Two elements invariant failed";
    }
}
```

### Summary:
Odd-Even Sort is a straightforward sorting algorithm that alternates between odd and even phases to sort an array. While it can be implemented efficiently in parallel computing environments, its average and worst-case time complexities of O(n2) make it less efficient compared to more advanced algorithms like Quick Sort or Merge Sort.
