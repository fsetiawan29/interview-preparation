# Interview Preparation

Coding interview practice, organized by algorithmic pattern rather than by
source or difficulty. Each pattern folder is self-contained: a `README.md`
explaining the pattern with a general shape/template, a `PROGRESS.md`
tracking what's done vs. queued, and per-problem subfolders under
`easy/medium/hard`. Each problem subfolder has its own `README.md` (problem
understanding, key insight, mental model, and solution) and solution file.

## Roadmap

The order below is the intended learning path — each pattern builds on
intuition from the ones above it.

```
Arrays & Hashing
        │
        ▼
Two Pointers
        │
        ▼
Sliding Window
        │
        ▼
Stack
        │
        ▼
Binary Search
        │
        ▼
Linked List
        │
        ▼
Trees
        │
        ▼
Heap / Priority Queue
        │
        ▼
Backtracking
        │
        ▼
Graphs
        │
        ▼
Intervals
        │
        ▼
Greedy
        │
        ▼
Dynamic Programming
```

- [x] Arrays & Hashing — [arrays-hashing](./arrays-hashing)
- [x] Two Pointers — [two-pointers](./two-pointers)
- [x] Sliding Window — [sliding-window](./sliding-window)
- [x] Stack — [stack](./stack)
- [ ] Binary Search
- [ ] Linked List
- [ ] Trees — early traversal problems started in [dfs](./dfs)
- [ ] Heap / Priority Queue
- [ ] Backtracking — early problems started in [dfs](./dfs)
- [ ] Graphs — early problems started in [dfs](./dfs)
- [ ] Intervals
- [ ] Greedy
- [ ] Dynamic Programming

## Patterns

- [arrays-hashing](./arrays-hashing) — hash sets/maps for `O(1)` membership,
  complement lookups, frequency counting, and grouping.
- [two-pointers](./two-pointers) — opposite-ends or same-direction index
  pairs to avoid nested loops or extra space.
- [sliding-window](./sliding-window) — fixed- or variable-size window over a
  contiguous subarray/substring, updated incrementally instead of
  recomputed from scratch.
- [dfs](./dfs) — depth-first traversal and backtracking on trees, grids, and
  graphs.
- [stack](./stack) — LIFO push/pop/peek for matching/nesting structure,
  expression parsing, and monotonic next-greater/smaller lookups.

Each problem subfolder contains the solution and its `README.md` — see the
pattern's own `README.md` for a per-problem index and `PROGRESS.md` for
what's solved vs. still queued.

## Progress Summary

Problems solved so far, by topic and difficulty:

| Topic | Easy | Medium | Hard | Total |
|---|---|---|---|---|
| [arrays-hashing](./arrays-hashing) | 15 | 8 | 0 | 23 |
| [two-pointers](./two-pointers) | 13 | 6 | 1 | 20 |
| [sliding-window](./sliding-window) | 2 | 5 | 0 | 7 |
| [stack](./stack) | 4 | 0 | 0 | 4 |
| [dfs](./dfs) | 2 | 1 | 0 | 3 |
| **Total** | **36** | **20** | **1** | **57** |

## Structure

```
interview-preparation/
├── arrays-hashing/
│   ├── README.md       # pattern explanation + problem index
│   ├── PROGRESS.md      # tracker
│   └── easy|medium|hard/<problem-name>/
│       ├── README.md    # problem understanding + recognition notes: idea, steps, mistakes, complexity
│       └── <problem-name>.py
├── two-pointers/
│   ├── README.md
│   ├── PROGRESS.md
│   └── easy|medium|hard/<problem-name>/
├── sliding-window/
│   ├── README.md
│   ├── PROGRESS.md
│   └── easy|medium|hard/<problem-name>/
├── stack/
│   ├── README.md
│   ├── PROGRESS.md
│   └── easy|medium|hard/<problem-name>/
└── dfs/
    ├── README.md
    └── <problem-name>/
```

## Conventions

- Solutions are Python, following the LeetCode `class Solution` method
  signature convention.
- New patterns get their own top-level folder with the same
  `README.md` + `PROGRESS.md` + `easy/medium/hard` layout.
- Every problem subfolder has a single `README.md` covering the problem
  statement (understanding, examples, constraints) and the
  recognition/solution notes together.
