# Trace JSON Schema

## Goal

Define the JSON contract between

Python Trace SDK

and

React Visualizer.

The frontend must rely only on this document.

---

# Root

```json
{
  "problem": "",
  "metadata": {},
  "steps": [],
  "summary": {}
}
```

---

# Metadata

```json
{
  "problem": "Two Sum",
  "difficulty": "Easy",
  "language": "Python",
  "algorithm": "Hash Map",
  "time_complexity": "O(n)",
  "space_complexity": "O(n)"
}
```

---

# Step

Every execution frame becomes one step.

```json
{
  "id": 14,
  "title": "Visit index 3",
  "timestamp": 14,
  "variables": {},
  "decision": {},
  "events": [],
  "snapshot": {},
  "statistics": {}
}
```

---

# Variables

```json
{
  "left": 2,
  "right": 7,
  "sum": 11,
  "answer": 3
}
```

---

# Decision

```json
{
  "condition": "sum < target",
  "result": true,
  "action": "Move left pointer"
}
```

---

# Events

```json
[
    "Expand Window",
    "Push Stack"
]
```

---

# Snapshot

Every snapshot has

```json
{
    "type": ""
}
```

Supported types

```
array
matrix
stack
queue
heap
tree
graph
linked-list
trie
union-find
```

---

# Array Snapshot

```json
{
    "type":"array",

    "values":[2,7,11,15],

    "highlights":[1],

    "pointers":{
        "left":0,
        "right":3
    }
}
```

---

# Stack Snapshot

```json
{
    "type":"stack",

    "values":[2,5,9]
}
```

---

# Queue Snapshot

```json
{
    "type":"queue",

    "values":[4,8,9]
}
```

---

# Heap Snapshot

```json
{
    "type":"heap",

    "values":[2,5,8,10]
}
```

---

# Tree Snapshot

```json
{
    "type":"tree",

    "nodes":[...],

    "edges":[...],

    "current":7
}
```

---

# Graph Snapshot

```json
{
    "type":"graph",

    "nodes":[...],

    "edges":[...],

    "visited":[1,4]
}
```

---

# Summary

```json
{
    "iterations":14,

    "execution_time":0.002,

    "answer":4
}
```

---

# Future Compatibility

The frontend must ignore unknown fields.

Example

```json
{
    "future_data":{}
}
```

This allows future SDK versions without breaking the UI.

---

# Versioning

Every trace must include

```json
{
    "schema_version":"1.0.0"
}
```

Future

```
1.1.0

2.0.0
```

---

# Validation

Provide JSON Schema validation.

Every trace must be valid before export.