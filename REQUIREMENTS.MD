# LeetCode Tracer Framework Requirements

**Version:** 1.0  
**Language:** Python 3.12+  
**Purpose:** Educational algorithm tracing and visualization for LeetCode interview preparation.

---

# 1. Project Goal

Build a reusable Python library that instruments LeetCode algorithms and automatically generates detailed execution traces.

The framework should help developers understand **how** an algorithm works rather than simply seeing the final answer.

It should be designed as a reusable library that can be imported into any LeetCode solution.

Example:

```python
from tracer import TraceRecorder

trace = TraceRecorder("Longest Consecutive Sequence")
```

The framework should generate educational outputs such as:

- Variable traces
- Iteration tables
- Decision logs
- Timeline of execution
- Data structure visualizations
- Final execution summary
- Markdown reports
- Console output

---

# 2. Project Structure

The project should be organized as a reusable library.

```
leetcode-tracer/
│
├── tracer/
│   │
│   ├── __init__.py
│   ├── recorder.py
│   ├── models.py
│   ├── config.py
│   │
│   ├── formatters/
│   │   ├── stdout.py
│   │   ├── markdown.py
│   │   ├── json.py
│   │   └── csv.py
│   │
│   ├── snapshots/
│   │   ├── array.py
│   │   ├── stack.py
│   │   ├── queue.py
│   │   ├── heap.py
│   │   ├── tree.py
│   │   ├── graph.py
│   │   └── linked_list.py
│   │
│   ├── timeline.py
│   ├── statistics.py
│   └── utils.py
│
├── examples/
│   ├── two_sum.py
│   ├── longest_consecutive.py
│   ├── sliding_window.py
│   ├── binary_search.py
│   ├── dfs.py
│   ├── bfs.py
│   └── dp.py
│
├── README.md
├── pyproject.toml
└── requirements.txt
```

---

# 3. Design Principles

The framework must be

- reusable
- modular
- lightweight
- educational
- interview-friendly
- extensible

The framework should NOT require changing algorithm logic.

Instrumentation should require only a few additional lines.

---

# 4. Core Component

Implement a central class

```python
TraceRecorder
```

Responsibilities:

- collect trace events
- store snapshots
- store variable states
- generate reports
- export results

---

# 5. Core API

Example usage

```python
trace = TraceRecorder(
    problem="Longest Consecutive Sequence"
)

trace.step(
    iteration=1,
    variables={
        "num": num,
        "current": current,
        "length": length,
        "longest": longest,
    }
)

trace.event("Start new sequence")

trace.decision(
    condition="num - 1 not in set",
    result=True,
    action="Start while loop"
)

trace.snapshot_array(nums)

trace.finish()

trace.export_markdown("trace.md")
```

---

# 6. Variable Trace

The framework shall support recording variables every iteration.

Example

```python
trace.step(
    iteration=i,
    variables={
        "left": left,
        "right": right,
        "sum": current_sum,
        "answer": answer,
    }
)
```

Expected output

| Iter | left | right | sum | answer |
|------|------|-------|-----|--------|
| 1 | 0 | 5 | 12 | 0 |
| 2 | 1 | 5 | 14 | 1 |

---

# 7. Variable Evolution

Generate a timeline showing how variables evolve.

Example

| Step | current | length | longest |
|------|---------|---------|----------|
| Start | - | - | 0 |
| Visit 100 | 100 | 1 | 1 |
| Visit 1 | 1 | 1 | 1 |
| While | 2 | 2 | 2 |
| While | 3 | 3 | 3 |
| While | 4 | 4 | 4 |

---

# 8. Iteration Table

Support customizable iteration tables.

Example

```python
trace.iteration(
    values={
        "num": num,
        "current": current,
        "length": length,
        "answer": answer,
    }
)
```

Output

| Iter | num | current | length | answer |
|------|-----|----------|---------|---------|

---

# 9. Decision Log

Support logging algorithm decisions.

Example

```python
trace.decision(
    condition="sum > target",
    result=True,
    action="Move right pointer"
)
```

Output

```
Iteration 5

Condition

sum > target

Result

TRUE

Action

Move right pointer
```

---

# 10. Event Log

Support generic events.

Example

```python
trace.event("Expand window")

trace.event("Found duplicate")

trace.event("Pop stack")
```

---

# 11. Timeline

Generate chronological execution.

Example

```
Start

↓

Create hash set

↓

Visit 100

↓

Skip 4

↓

Visit 200

↓

Visit 1

↓

Expand

↓

Expand

↓

Finish
```

---

# 12. Array Visualization

Support pointer visualization.

Example

```
Index

0 1 2 3 4

Value

2 7 11 15 18

 ^
 L

         ^
         R
```

---

# 13. Stack Visualization

```
Top

+------+
|  10  |
+------+
|   5  |
+------+
|   2  |
+------+
```

---

# 14. Queue Visualization

```
Front

[3][7][9][12]
```

---

# 15. Heap Visualization

```
      2
     / \
    5   8
   /
  10
```

---

# 16. Binary Tree Visualization

```
        5
      /   \
     3     8
    / \
   1   4
```

---

# 17. Graph Visualization

```
A ----- B
|       |
|       |
C ----- D
```

---

# 18. Final Summary

Automatically compute

```
Iterations

18

Skipped iterations

9

While loops

4

Maximum recursion depth

5

Maximum stack size

4

Maximum queue size

7

Execution time

0.002 seconds

Answer

4
```

---

# 19. Export Formats

Support

## Markdown

Generate

```
trace.md
```

## Console

Pretty stdout output.

## JSON

Useful for tooling.

## CSV

Useful for spreadsheets.

---

# 20. Markdown Report

Generate a report containing

- Problem name
- Input
- Variable trace
- Timeline
- Decision log
- Snapshots
- Summary

Example

```
# Longest Consecutive Sequence

## Input

[100,4,200,1,3,2]

## Variable Trace

| Iter | current | longest |

...

## Timeline

...

## Summary

...
```

---

# 21. Supported Data Structures

The framework should support visualization for

- Array
- Matrix
- Stack
- Queue
- Heap
- Linked List
- Binary Tree
- Trie
- Graph
- Hash Map
- Hash Set

---

# 22. Supported Algorithm Categories

The framework should be generic enough for

- Arrays
- Hash Maps
- Hash Sets
- Two Pointers
- Sliding Window
- Binary Search
- DFS
- BFS
- Dynamic Programming
- Greedy
- Backtracking
- Monotonic Stack
- Heap
- Trie
- Union Find
- Graph
- Topological Sort
- Segment Tree

No algorithm-specific logic should exist in the framework.

---

# 23. Nice-to-Have Features

## Automatic Variable Capture

Support

```python
trace.auto(locals())
```

Automatically capture primitive variables.

---

## Decorator

Support

```python
@trace_algorithm
def solve():
    ...
```

---

## Context Manager

Support

```python
with TraceRecorder() as trace:
    ...
```

---

## Rich Terminal Output

Optionally use the `rich` library for

- colored tables
- panels
- trees
- syntax highlighting

The framework should still work without `rich`.

---

## Performance Metrics

Automatically compute

- execution time
- iteration count
- recursion depth
- maximum stack size
- maximum queue size
- maximum heap size

---

# 24. Non-Functional Requirements

- Python 3.12+
- Fully typed using type hints
- Modular architecture
- Unit-testable design
- Minimal external dependencies
- Clean API
- Comprehensive documentation
- Extensible formatter architecture
- Easy to integrate into any LeetCode solution

---

# 25. Success Criteria

The framework should enable a developer to instrument a LeetCode solution with minimal code changes and produce a comprehensive, educational execution report that includes:

- Variable traces
- Iteration tables
- Decision logs
- Timeline
- Data structure snapshots
- Final statistics
- Markdown export
- Console visualization

The resulting reports should make it easy to understand how an algorithm executes step by step and should be suitable for interview preparation, debugging, and learning algorithmic patterns.