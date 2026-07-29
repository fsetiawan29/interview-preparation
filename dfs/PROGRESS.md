# DFS — Progress Tracker

## Overview

| Problem | Difficulty | Main Concept | Status |
|---|---|---|---|
| #94 Binary Tree Inorder Traversal | Easy | Recursive tree traversal | Done |
| #257 Binary Tree Paths | Easy | Root-to-leaf path enumeration (choose/explore/un-choose) | Done |
| #79 Word Search | Medium | Grid DFS + backtracking | Done |
| #78 Subsets | Easy | Basic DFS template (take/skip) | |
| #90 Subsets II | Medium | Handle duplicates | |
| #77 Combinations | Medium | Choose k items | |
| #216 Combination Sum III | Medium | Fixed size + target | |
| #39 Combination Sum | Medium | Reuse items | |
| #40 Combination Sum II | Medium | No reuse | |
| #46 Permutations | Medium | Backtracking over unused items | |
| #47 Permutations II | Medium | Duplicates | |
| #31 Next Permutation | Medium | Interview favorite | |
| #17 Letter Combinations of a Phone Number | Medium | String DFS | |
| #93 Restore IP Addresses | Medium | String DFS + constraints | |
| #131 Palindrome Partitioning | Medium | String DFS + validity check | |
| #200 Number of Islands | Medium | Grid DFS | |
| #695 Max Area of Island | Medium | Grid DFS | |
| #733 Flood Fill | Easy | Grid DFS | |
| #130 Surrounded Regions | Medium | Grid DFS from the border | |
| #104 Maximum Depth of Binary Tree | Easy | Tree DFS | |
| #100 Same Tree | Easy | Tree DFS | |
| #112 Path Sum | Easy | Tree DFS | |
| #543 Diameter of Binary Tree | Easy | Tree DFS | |
| #124 Binary Tree Maximum Path Sum | Hard | Tree DFS | |
| #22 Generate Parentheses | Medium | Classic backtracking | |
| #51 N-Queens | Hard | Classic backtracking | |
| #37 Sudoku Solver | Hard | Classic backtracking | |
| #212 Word Search II | Hard | Backtracking + Trie | |
| #416 Partition Equal Subset Sum | Medium | DFS → DP transition | |
| #494 Target Sum | Medium | DFS → DP transition | |
| #322 Coin Change | Medium | DFS → DP transition | |
| 0/1 Knapsack (classic) | Medium | DFS → DP transition | |

## Level 1 — Decision Tree Basics ⭐⭐⭐⭐⭐ (Most Important)

These problems teach "take or skip".

| # | Problem | Difficulty | Learn | Status |
|---|---|---|---|---|
| 1 | #78 Subsets | Easy | Basic DFS template | |
| 2 | #90 Subsets II | Medium | Handle duplicates | |
| 3 | #77 Combinations | Medium | Choose k items | |
| 4 | #216 Combination Sum III | Medium | Fixed size + target | |
| 5 | #39 Combination Sum | Medium | Reuse items | |
| 6 | #40 Combination Sum II | Medium | No reuse (close to interview questions) | |

- [ ] #78 Subsets
- [ ] #90 Subsets II
- [ ] #77 Combinations
- [ ] #216 Combination Sum III
- [ ] #39 Combination Sum
- [ ] #40 Combination Sum II

**Goal:** "I can generate every possible subset."

## Level 2 — Permutation Pattern

Instead of "take/skip", every step asks: which unused number should I place next?

| # | Problem | Difficulty | Learn | Status |
|---|---|---|---|---|
| 7 | #46 Permutations | Medium | Backtracking | |
| 8 | #47 Permutations II | Medium | Duplicates | |
| 9 | #31 Next Permutation | Medium | Interview favorite | |

- [ ] #46 Permutations
- [ ] #47 Permutations II
- [ ] #31 Next Permutation

**Patterns learned:** choosing from a pool of unused items, marking used/unused.

## Level 3 — String DFS

Now the choices involve characters.

| # | Problem | Difficulty | Status |
|---|---|---|---|
| 10 | #17 Letter Combinations of a Phone Number | Medium | |
| 11 | #93 Restore IP Addresses | Medium | |
| 12 | #131 Palindrome Partitioning | Medium | |

- [ ] #17 Letter Combinations of a Phone Number
- [ ] #93 Restore IP Addresses
- [ ] #131 Palindrome Partitioning

**Patterns learned:** building a string one choice at a time, validity checks mid-recursion.

## Level 4 — Grid DFS

Now recursion explores neighbors (up/down/left/right) instead of take/skip.

| # | Problem | Difficulty | Status |
|---|---|---|---|
| 13 | #200 Number of Islands | Medium | |
| 14 | #695 Max Area of Island | Medium | |
| 15 | #733 Flood Fill | Easy | |
| 16 | #130 Surrounded Regions | Medium | |

- [ ] #200 Number of Islands
- [ ] #695 Max Area of Island
- [ ] #733 Flood Fill
- [ ] #130 Surrounded Regions

**Patterns learned:** 4-directional exploration, marking visited cells, connected components.

## Level 5 — Tree DFS

Same recursion, different structure.

| # | Problem | Difficulty | Status |
|---|---|---|---|
| — | #94 Binary Tree Inorder Traversal | Easy | Done |
| — | #257 Binary Tree Paths | Easy | Done |
| 17 | #104 Maximum Depth of Binary Tree | Easy | |
| 18 | #100 Same Tree | Easy | |
| 19 | #112 Path Sum | Easy | |
| 20 | #543 Diameter of Binary Tree | Easy | |
| 21 | #124 Binary Tree Maximum Path Sum | Hard | |

- [x] #94 Binary Tree Inorder Traversal — [binary-tree-inorder-traversal](./binary-tree-inorder-traversal)
- [x] #257 Binary Tree Paths — [binary-tree-paths](./binary-tree-paths)
- [ ] #104 Maximum Depth of Binary Tree
- [ ] #100 Same Tree
- [ ] #112 Path Sum
- [ ] #543 Diameter of Binary Tree
- [ ] #124 Binary Tree Maximum Path Sum

**Patterns learned:** preorder/inorder/postorder recursion, root-to-leaf path building
(choose/explore/un-choose), passing accumulated state down the call stack.

## Level 6 — Classic Backtracking

These are common in interviews.

| # | Problem | Difficulty | Status |
|---|---|---|---|
| 22 | #22 Generate Parentheses | Medium | |
| 23 | #51 N-Queens | Hard | |
| 24 | #37 Sudoku Solver | Hard | |
| 25 | #79 Word Search | Medium | Done |
| 26 | #212 Word Search II | Hard | |

- [ ] #22 Generate Parentheses
- [ ] #51 N-Queens
- [ ] #37 Sudoku Solver
- [x] #79 Word Search — [word-search](./word-search)
- [ ] #212 Word Search II

**Patterns learned:** grid + string DFS combined, pruning invalid branches early, undoing a
mark on the shared grid so sibling paths don't see it.

## Level 7 — DFS → DP Transition

These start as brute-force DFS, then get optimized.

| # | Problem | Difficulty | Status |
|---|---|---|---|
| 27 | #416 Partition Equal Subset Sum | Medium | |
| 28 | #494 Target Sum | Medium | |
| 29 | #322 Coin Change | Medium | |
| 30 | 0/1 Knapsack (classic) | Medium | |

- [ ] #416 Partition Equal Subset Sum
- [ ] #494 Target Sum
- [ ] #322 Coin Change
- [ ] 0/1 Knapsack (classic)

**Patterns learned:** recognizing overlapping subproblems in a DFS tree, then adding
memoization — "first I'll solve it using DFS, then optimize it with memoization."

## Recommended Learning Order

Week 1
- #78 Subsets
- #77 Combinations
- #90 Subsets II
- #39 Combination Sum
- #40 Combination Sum II

Week 2
- #46 Permutations
- #47 Permutations II
- #17 Letter Combinations of a Phone Number
- #131 Palindrome Partitioning

Week 3
- #200 Number of Islands
- #695 Max Area of Island
- #130 Surrounded Regions

Week 4
- #22 Generate Parentheses
- #79 Word Search
- #416 Partition Equal Subset Sum
- #494 Target Sum
- #322 Coin Change

**Starting point:** since tree DFS was already learned interactively
([binary-tree-inorder-traversal](./binary-tree-inorder-traversal),
[binary-tree-paths](./binary-tree-paths)) and [word-search](./word-search) is done, the next
four problems to build deep DFS/backtracking intuition before moving on to DP are:

1. #78 Subsets — learn the DFS template.
2. #77 Combinations — practice choosing items.
3. #39 Combination Sum — learn when items can be reused.
4. #40 Combination Sum II — no reuse, close to a typical interview question.
