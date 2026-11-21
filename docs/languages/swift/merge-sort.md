---
id: swift-merge-sort
title: Merge Sort in Swift
sidebar_label: Merge Sort
sidebar_position: 5
description: Learn how to implement Merge Sort in Swift, with complete code examples, explanation, and complexity analysis.
tags: [swift, sorting, algorithms, merge-sort]
---

# Merge Sort in Swift

Merge Sort is an efficient, stable, comparison-based, divide-and-conquer sorting algorithm. Most implementations produce a stable sort, meaning that the order of equal elements is the same in the input and output.

## Implementation in Swift

Here is the implementation of Merge Sort in Swift using recursion.

```swift
func mergeSort<T: Comparable>(_ array: [T]) -> [T] {
    guard array.count > 1 else { return array }
    
    let middleIndex = array.count / 2
    
    let leftArray = mergeSort(Array(array[0..<middleIndex]))
    let rightArray = mergeSort(Array(array[middleIndex..<array.count]))
    
    return merge(leftArray, rightArray)
}

func merge<T: Comparable>(_ left: [T], _ right: [T]) -> [T] {
    var leftIndex = 0
    var rightIndex = 0
    var orderedArray = [T]()
    
    while leftIndex < left.count && rightIndex < right.count {
        if left[leftIndex] < right[rightIndex] {
            orderedArray.append(left[leftIndex])
            leftIndex += 1
        } else if left[leftIndex] > right[rightIndex] {
            orderedArray.append(right[rightIndex])
            rightIndex += 1
        } else {
            orderedArray.append(left[leftIndex])
            leftIndex += 1
            orderedArray.append(right[rightIndex])
            rightIndex += 1
        }
    }
    
    while leftIndex < left.count {
        orderedArray.append(left[leftIndex])
        leftIndex += 1
    }
    
    while rightIndex < right.count {
        orderedArray.append(right[rightIndex])
        rightIndex += 1
    }
    
    return orderedArray
}

// 1. Worked example (literal fixture)
let numbers = [12, 11, 13, 5, 6, 7]
let sortedNumbers = mergeSort(numbers)
print("Sorted array: \(sortedNumbers)")

// 2. Boundary examples (base-case contract: array.count <= 1)
let emptyNumbers: [Int] = []
print("Empty array: \(mergeSort(emptyNumbers))")
print("Single-element array: \(mergeSort([42]))")

// 3. Resource & copy-behavior observation experiment
struct ResourceMetrics {
    var splits = 0
    var sliceCopies = 0
    var mergeAppends = 0
}

func observedMergeSort<T: Comparable>(_ array: [T], _ metrics: inout ResourceMetrics) -> [T] {
    guard array.count > 1 else { return array }
    metrics.splits += 1
    let middleIndex = array.count / 2
    // Array(array[...]) materializes zero-copy ArraySlice views into new Array buffers
    metrics.sliceCopies += 2
    let leftArray = observedMergeSort(Array(array[0..<middleIndex]), &metrics)
    let rightArray = observedMergeSort(Array(array[middleIndex..<array.count]), &metrics)
    let merged = merge(leftArray, rightArray)
    metrics.mergeAppends += merged.count
    return merged
}

for sample in [emptyNumbers, [42], numbers] {
    var metrics = ResourceMetrics()
    let _ = observedMergeSort(sample, &metrics)
    print("n=\(sample.count): splits=\(metrics.splits), sliceCopies=\(metrics.sliceCopies), mergeAppends=\(metrics.mergeAppends)")
}
```

## Complexity Analysis

- **Time Complexity**:
  - **Best Case**: $O(n \log n)$
  - **Average Case**: $O(n \log n)$
  - **Worst Case**: $O(n \log n)$
- **Space Complexity**: $O(n)$ auxiliary space to store the merged sub-arrays.

### Resource, Copy/View & Scaling Behavior

- **Copy vs. View Semantics (`ArraySlice` Materialization):** In Swift, subscripting `array[0..<middleIndex]` and `array[middleIndex..<array.count]` creates `O(1)` `ArraySlice` views sharing the parent buffer, whereas wrapping them in `Array(...)` eagerly allocates and copies elements into new `Array` storage at every split. Across `n - 1` internal splits, the implementation performs `2(n - 1)` `Array` materializations (`10` slice copies for `n = 6`).
- **Auxiliary Buffer Allocation (`merge`):** Each `merge` call allocates a fresh `orderedArray = [T]()` and appends `left.count + right.count` elements (`16` appends across `3` recursion levels for `n = 6`), matching $O(n \log n)$ work and $O(n)$ active auxiliary space.
- **Base-Case Boundary (`array.count <= 1`):** Both `[]` (`n = 0`) and `[42]` (`n = 1`) satisfy `guard array.count > 1` immediately, resulting in `0` splits, `0` slice copies, and `0` merge appends.

### Example Output

```plaintext
Sorted array: [5, 6, 7, 11, 12, 13]
Empty array: []
Single-element array: [42]
n=0: splits=0, sliceCopies=0, mergeAppends=0
n=1: splits=0, sliceCopies=0, mergeAppends=0
n=6: splits=5, sliceCopies=10, mergeAppends=16
```
