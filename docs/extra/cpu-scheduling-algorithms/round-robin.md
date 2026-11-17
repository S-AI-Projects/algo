---
id: round-robin-cpu-scheduling
title: Round Robin CPU Scheduling Algorithm
sidebar_label: "Round Robin CPU Scheduling Algorithm"
sidebar_position: 6
description: Round Robin is a scheduling algorithm where each process can use the CPU only for a given time slice or time quantum.
tags: [CPU Scheduling, Round robin, Preemptive, Algorithm]
---

# Round Robin Scheduling

## 1. Introduction

Round Robin (RR) is a preemptive CPU scheduling algorithm designed for time-sharing systems. Each process is assigned a fixed amount of CPU time called a time quantum or time slice. If a process does not complete within its time quantum, it is preempted and moved to the end of the ready queue.

This ensures fair CPU allocation among all processes.

## Video Explanation

<LiteYouTubeEmbed
  id="TxjIlNYRZ5M"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="L-2.7: Round Robin(RR) CPU Scheduling Algorithm with Example"
  poster="maxresdefault"
  lazyLoad={true}
  webp
/>

## 2. How It Works

- Processes are placed in a ready queue.
- The first process is given the CPU for one time quantum.
- If the process completes, it leaves the system.
- If it does not complete, it is moved to the back of the queue.
- The next process receives the CPU.
- The cycle repeats until all processes are completed.

## 3. Advantages

- Fair CPU allocation to all processes.
- Good response time for interactive systems.
- Prevents process starvation.

## 4. Disadvantages

- Performance depends heavily on the chosen time quantum.
- Excessively small time quantum increases context-switching overhead.
- Large time quantum makes RR behave similarly to FCFS.

## 5. Applications

Round Robin is commonly used in time-sharing and multitasking operating systems where multiple users or applications require responsive CPU access.

## 6. Evaluation Metrics

### 6.1 Waiting Time

Waiting time is the total amount of time a process spends in the ready queue waiting for CPU allocation.
It does not include the time the process is actually executing.

Formula:
Waiting Time = Turnaround Time − Burst Time

It tells how long a process has to wait before getting executed.

### 6.2 Turnaround Time

Turnaround time is the total time taken by a process from its arrival to its completion.

Formula:
Turnaround Time = Completion Time − Arrival Time

It includes both waiting time and execution time.

### 6.3 Response Time

Response time is the time from when a process arrives in the ready queue to when it gets the CPU for the first time.

Formula:
Response Time = Time of first CPU allocation − Arrival Time

It measures how quickly a system responds to a process (important in interactive systems).

## 7. Python Implementation

The function receives the process fixture and time quantum as explicit inputs. Each call creates new process records and keeps its queue, clock, and results local, so a repeated run cannot inherit mutated scheduling state from an earlier run.

```python
from collections import deque


def round_robin(process_specs, quantum):
    """Return a schedule and metrics without mutating caller-owned input."""
    if quantum <= 0:
        raise ValueError("time quantum must be positive")

    processes = [
        {**spec, "order": order, "rbt": spec["bt"], "st": None}
        for order, spec in enumerate(process_specs, start=1)
    ]
    pending = deque(sorted(processes, key=lambda p: (p["at"], p["order"])))
    ready = deque()
    segments = []
    time = 0

    while pending or ready:
        while pending and pending[0]["at"] <= time:
            ready.append(pending.popleft())

        if not ready:
            next_arrival = pending[0]["at"]
            segments.append(("idle", time, next_arrival))
            time = next_arrival
            continue

        process = ready.popleft()
        if process["st"] is None:
            process["st"] = time
        run = min(quantum, process["rbt"])
        start = time
        time += run
        process["rbt"] -= run
        segments.append((process["name"], start, time))

        while pending and pending[0]["at"] <= time:
            ready.append(pending.popleft())
        if process["rbt"] == 0:
            process["ct"] = time
        else:
            ready.append(process)

    metrics = {}
    for process in processes:
        turnaround = process["ct"] - process["at"]
        metrics[process["name"]] = {
            "turnaround": turnaround,
            "waiting": turnaround - process["bt"],
            "response": process["st"] - process["at"],
        }
    return segments, metrics


def show_schedule(process_specs, quantum):
    segments, metrics = round_robin(process_specs, quantum)
    print("Gantt Chart:\n")
    print("    " + "        ".join(name for name, _, _ in segments))
    print("         ".join([str(segments[0][1])] + [str(end) for _, _, end in segments]))

    for label, key in (("Turn Around Time", "turnaround"), ("Waiting Time", "waiting"), ("Response Time", "response")):
        print(f"\n{label}:")
        total = 0
        for process in process_specs:
            value = metrics[process["name"]][key]
            total += value
            print(f"{process['name']}: {value}")
        print(f"Average {label.lower()} = ", total / len(process_specs))


# Literal fixture from the worked example; all scheduling state is local to the call.
worked_processes = [
    {"name": "p1", "at": 2, "bt": 5},
    {"name": "p2", "at": 3, "bt": 3},
    {"name": "p3", "at": 5, "bt": 7},
    {"name": "p4", "at": 12, "bt": 2},
]
original_fixture = [process.copy() for process in worked_processes]
worked_result = round_robin(worked_processes, 3)
assert worked_result == round_robin(worked_processes, 3)
assert worked_processes == original_fixture  # repeated calls do not leak mutated state
show_schedule(worked_processes, 3)

# Small boundary: one process, one quantum, and no queue rotation.
boundary = [{"name": "solo", "at": 0, "bt": 1}]
_, boundary_metrics = round_robin(boundary, 1)
assert boundary_metrics["solo"] == {"turnaround": 1, "waiting": 0, "response": 0}
print("\nBoundary: solo completes at 1 (turnaround=1, waiting=0, response=0)")
```

**Example:**

Input:
```text
Enter no of processes: 4
Enter name of process, arrival time, and burst time:
p1 2 5
p2 3 3
p3 5 7
p4 12 2
Enter time quantum: 3
```

Output:
```text
Gantt Chart:

    idle        p1        p2        p3        p1        p3        p4        p3
0         2         5         8         11         13         16         18         19

Turn Around Time:
p1: 11
p2: 5
p3: 14
p4: 6
Average turn around time =  9.0

Waiting Time:
p1: 6
p2: 2
p3: 7
p4: 4
Average waiting time =  4.75

Response Time:
p1: 0
p2: 2
p3: 3
p4: 4
Average response time =  2.25

Boundary: solo completes at 1 (turnaround=1, waiting=0, response=0)
```