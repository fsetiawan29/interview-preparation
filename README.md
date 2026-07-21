# Interview Preparation

Coding interview practice, organized by algorithmic pattern rather than by
source or difficulty. Each pattern folder is self-contained: a `README.md`
explaining the pattern with a general shape/template, a `PROGRESS.md`
tracking what's done vs. queued, and per-problem subfolders under
`easy/medium/hard`.

## Patterns

- [arrays-hashing](./arrays-hashing) — hash sets/maps for `O(1)` membership,
  complement lookups, frequency counting, and grouping.
- [two-pointers](./two-pointers) — opposite-ends or same-direction index
  pairs to avoid nested loops or extra space.
- [dfs](./dfs) — depth-first traversal and backtracking on trees, grids, and
  graphs.

Each problem subfolder typically contains the solution and any notes/tests
for that problem — see the pattern's own `README.md` for a per-problem index
and `PROGRESS.md` for what's solved vs. still queued.

## Structure

```
interview-preparation/
├── arrays-hashing/
│   ├── README.md       # pattern explanation + problem index
│   ├── PROGRESS.md      # tracker
│   └── easy|medium|hard/<problem-name>/
├── two-pointers/
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
