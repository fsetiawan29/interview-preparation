# Tracer SDK Requirements

## Goal

Build a reusable Python SDK that instruments LeetCode algorithms and records execution.

The SDK must never know anything about React.

Its responsibility ends after producing JSON.

---

## Responsibilities

- Record execution steps
- Record variables
- Record events
- Record decisions
- Record snapshots
- Produce a timeline
- Compute statistics
- Export JSON
- Export Markdown
- Export stdout

---

## Core Class

TraceRecorder

Responsibilities

- create trace
- append steps
- append events
- export

---

## Public API

```python
trace = TraceRecorder(problem="Two Sum")

trace.step(...)

trace.event(...)

trace.snapshot(...)

trace.finish()
```

---

## Step API

```python
trace.step(
    title="Visit 5",
    variables={
        "left": left,
        "right": right,
        "sum": s
    }
)
```

---

## Decision API

```python
trace.decision(
    condition="sum > target",
    result=True,
    action="Move Right"
)
```

---

## Snapshot API

Support

- Array
- Matrix
- Stack
- Queue
- Heap
- Tree
- Trie
- Graph
- Linked List

---

## Statistics

Automatically compute

- iterations
- skipped
- recursion depth
- execution time
- answer

---

## Output

stdout

markdown

json

csv

---

## Design Principles

- modular
- typed
- testable
- no UI code
- no React dependency
- reusable