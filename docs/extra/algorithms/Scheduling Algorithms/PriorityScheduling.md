---

id: priority-scheduling
title: Priority Scheduling Algorithm
sidebar_label: "Priority Scheduling"
sidebar_position: 7
description: Priority Scheduling is a scheduling algorithm that selects processes based on priority. Higher priority processes are executed before lower priority ones.
tags: [Scheduling, Priority]

---

# Priority Scheduling Algorithm

## Introduction

The **Priority Scheduling** algorithm is a process scheduling technique where processes are assigned priorities. The CPU is allocated to the process with the highest priority. If two processes have the same priority, they are scheduled in the order they arrive (FCFS).

### Example

Consider four processes with the following burst times and priorities:
- Process 1: `10 units` (Priority 2)
- Process 2: `1 unit` (Priority 1)
- Process 3: `2 units` (Priority 3)
- Process 4: `1 unit` (Priority 4)

Using the Priority Scheduling algorithm, the processes will be executed in the order of their priority: Process 2, Process 1, Process 3, and then Process 4.

## Video Explanation 

<LiteYouTubeEmbed
  id="rsDGfFxSgiY"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="L-2.8: Pre-emptive Priority Scheduling Algorithm with Example | Operating System"
  lazyLoad={true}
  webp
/>

## Problem Definition

Given a list of processes along with their burst times and priorities, calculate the waiting times, turnaround times, average waiting time, and average turnaround time for the processes.

### Key Concepts

- **Waiting Time**: The amount of time a process spends waiting before it starts executing.
- **Turnaround Time**: The total time taken for a process from arrival to completion, which includes both the waiting time and the duration time.

## Priority Scheduling Approach

In the Priority Scheduling algorithm:
- The process with the highest priority is selected for execution next.
- If multiple processes have the same priority, the one that arrives first is executed first.

## Code Implementation in Python

Below is the Python implementation for the Priority Scheduling algorithm:

```python
from typing import List, Tuple

def calculate_wait_times(processes: List[Tuple[int, int, int]]) -> List[int]:
    """
    Calculate the waiting times for a list of processes given their burst times and priorities.
    """
    # Sort processes by priority (lower number indicates higher priority)
    processes.sort(key=lambda x: (x[2], x[0]))  # Sort by priority, then by arrival time
    n = len(processes)
    wait_times = [0] * n
    
    for i in range(1, n):
        wait_times[i] = processes[i - 1][1] + wait_times[i - 1]
    
    return wait_times

def calculate_turnaround_times(processes: List[Tuple[int, int, int]], wait_times: List[int]) -> List[int]:
    """
    Calculate the turnaround times for a list of processes.
    Turnaround time is the sum of waiting time and burst time for each process.
    """
    return [processes[i][1] + wait_times[i] for i in range(len(processes))]

def calculate_avg_turnaround_time(turnaround_times: List[int]) -> float:
    """
    Calculate the average turnaround time for a list of processes.
    """
    return sum(turnaround_times) / len(turnaround_times)

def calculate_avg_wait_time(wait_times: List[int]) -> float:
    """
    Calculate the average waiting time for a list of processes.
    """
    return sum(wait_times) / len(wait_times)

if __name__ == "__main__":
    processes = [(1, 10, 2), (2, 1, 1), (3, 2, 3), (4, 1, 4)]  # List of (process_id, burst_time, priority)

    # Calculate waiting times and turnaround times
    wait_times = calculate_wait_times(processes)
    turnaround_times = calculate_turnaround_times(processes, wait_times)

    # Calculate average waiting time and average turnaround time
    avg_wait_time = calculate_avg_wait_time(wait_times)
    avg_turnaround_time = calculate_avg_turnaround_time(turnaround_times)

    # Display process details and calculated times
    print("Process ID\tBurst Time\tPriority\tWaiting Time\tTurnaround Time")
    for i, (process_id, burst_time, priority) in enumerate(processes):
        print(f"{process_id}\t\t{burst_time}\t\t{priority}\t\t{wait_times[i]}\t\t{turnaround_times[i]}")
    
    # Display averages
    print(f"Average waiting time = {avg_wait_time}")
    print(f"Average turnaround time = {avg_turnaround_time}")

    # Smallest valid boundary case: single process (len(processes) == 1)
    boundary_processes = [(1, 5, 1)]
    boundary_wait = calculate_wait_times(boundary_processes)
    boundary_tat = calculate_turnaround_times(boundary_processes, boundary_wait)
    print(f"\nBoundary Case (1 Process): {boundary_processes}")
    print(f"Waiting Times: {boundary_wait}, Turnaround Times: {boundary_tat}")
    print(f"Average waiting time = {calculate_avg_wait_time(boundary_wait)}")
    print(f"Average turnaround time = {calculate_avg_turnaround_time(boundary_tat)}")

```

## Explanation of the Code
    - Waiting Time Calculation:
        - Processes are first sorted by their priority and then by arrival time.
        - The waiting time for the first process is 0, and for subsequent processes, it is the sum of the durations of all previous processes.
    - Turnaround Time Calculation:
        - Turnaround time is calculated as the sum of the waiting time and the burst time of each process.
    - Average Times:
        - The average waiting time and average turnaround time are calculated by taking the sum of the respective times and dividing by the total number of processes.

### Boundary Case & Precondition
- **Precondition:** The input list `processes` must contain at least one process (`len(processes) >= 1`) with non-negative burst times, because `calculate_avg_wait_time` and `calculate_avg_turnaround_time` divide by `len(wait_times)` and `len(turnaround_times)` directly (passing `[]` raises `ZeroDivisionError`).
- **Concrete Input & Intermediate State:** For `[(1, 10, 2), (2, 1, 1), (3, 2, 3), (4, 1, 4)]`, sorting by `(priority, process_id)` produces `[(2, 1, 1), (1, 10, 2), (3, 2, 3), (4, 1, 4)]`, yielding intermediate arrays `wait_times = [0, 1, 11, 13]` and `turnaround_times = [1, 11, 13, 14]`.
- **Smallest Valid Boundary (`len(processes) == 1`):** For `[(1, 5, 1)]`, the waiting-time loop `range(1, 1)` does not execute (`wait_times = [0]`) and `turnaround_times = [5]`, so average waiting time is `0.0` and average turnaround time equals the single process's burst time (`5.0`).

## Example Output
For the worked example input `[(1, 10, 2), (2, 1, 1), (3, 2, 3), (4, 1, 4)]` followed by the 1-process boundary case `[(1, 5, 1)]`, the exact output is:
```plaintext
Process ID	Burst Time	Priority	Waiting Time	Turnaround Time
2		1		1		0		1
1		10		2		1		11
3		2		3		11		13
4		1		4		13		14
Average waiting time = 6.25
Average turnaround time = 9.75

Boundary Case (1 Process): [(1, 5, 1)]
Waiting Times: [0], Turnaround Times: [5]
Average waiting time = 0.0
Average turnaround time = 5.0
```

## Time and Space Complexity
- **Time Complexity**: The time complexity is O(n log n) due to the sorting of processes, where n is the number of processes.
- **Space Complexity**: The space complexity is O(n) due to the storage of waiting times and turnaround times.

## Conclusion
The Priority Scheduling algorithm is effective for ensuring that high-priority processes are executed first. However, it can lead to the "starvation" of lower-priority processes if higher-priority processes continue to arrive.
