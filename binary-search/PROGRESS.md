# Binary Search — Progress Tracker

## Blind 75 Binary Search Problems

| Problem | Difficulty | Status |
|---|---|---|
| #704 Binary Search | Easy | |
| #33 Search in Rotated Sorted Array | Medium | |
| #153 Find Minimum in Rotated Sorted Array | Medium | |
| #34 Find First and Last Position of Element in Sorted Array | Medium | |
| #74 Search a 2D Matrix | Medium | |
| #981 Time Based Key-Value Store | Medium | |
| #4 Median of Two Sorted Arrays | Hard | |

## NeetCode 150 Additions

Problems NeetCode 150 adds on top of Blind 75 (`Min Eating Speed` is the
same problem as `Koko Eating Bananas`, #875).

| Problem | Difficulty | Status |
|---|---|---|
| #875 Koko Eating Bananas | Medium | |
| #1011 Capacity To Ship Packages Within D Days | Medium | |
| #81 Search in Rotated Sorted Array II | Medium | |
| #162 Find Peak Element | Medium | |
| #35 Search Insert Position | Easy | |

## Level 1 — Master the Fundamentals

Goal: learn the invariant, interval representation, and pointer movement.

| # | Problem | Difficulty | Blind 75 | Status |
|---|---|---|---|---|
| 1 | #704 Binary Search | Easy | ✅ | |
| 2 | #35 Search Insert Position | Easy | | |
| 3 | #374 Guess Number Higher or Lower | Easy | | |
| 4 | #367 Valid Perfect Square | Easy | | |
| 5 | #69 Sqrt(x) | Easy | | |
| 6 | #441 Arranging Coins | Easy | | |

- [ ] #704 Binary Search (Blind 75)
- [ ] #35 Search Insert Position
- [ ] #374 Guess Number Higher or Lower
- [ ] #367 Valid Perfect Square
- [ ] #69 Sqrt(x)
- [ ] #441 Arranging Coins

**Patterns learned:** basic binary search, lower bound, binary search on
values.

## Level 2 — Boundaries

Goal: understand first occurrence, last occurrence, lower_bound, upper_bound.

| # | Problem | Difficulty | Blind 75 | Status |
|---|---|---|---|---|
| 7 | #34 Find First and Last Position of Element in Sorted Array | Medium | ✅ | |
| 8 | #744 Find Smallest Letter Greater Than Target | Easy | | |
| 9 | #162 Find Peak Element | Medium | | |
| 10 | #852 Peak Index in a Mountain Array | Medium | | |
| 11 | #540 Single Element in a Sorted Array | Medium | | |

- [ ] #34 Find First and Last Position of Element in Sorted Array (Blind 75)
- [ ] #744 Find Smallest Letter Greater Than Target
- [ ] #162 Find Peak Element
- [ ] #852 Peak Index in a Mountain Array
- [ ] #540 Single Element in a Sorted Array

**Patterns learned:** lower/upper bound, decision-based binary search on a
non-target condition.

## Level 3 — Rotated Arrays

Goal: binary search when order changes.

| # | Problem | Difficulty | Blind 75 | Status |
|---|---|---|---|---|
| 12 | #33 Search in Rotated Sorted Array | Medium | ✅ | |
| 13 | #81 Search in Rotated Sorted Array II | Medium | | |
| 14 | #153 Find Minimum in Rotated Sorted Array | Medium | ✅ | |
| 15 | #154 Find Minimum in Rotated Sorted Array II | Hard | | |
| 16 | #74 Search a 2D Matrix | Medium | ✅ | |

- [ ] #33 Search in Rotated Sorted Array (Blind 75)
- [ ] #81 Search in Rotated Sorted Array II
- [ ] #153 Find Minimum in Rotated Sorted Array (Blind 75)
- [ ] #154 Find Minimum in Rotated Sorted Array II
- [ ] #74 Search a 2D Matrix (Blind 75)

**Patterns learned:** deciding which half is sorted, duplicate fallback.

## Level 4 — Binary Search on Answer

The most important category for senior interviews: instead of searching for
a number, search for the minimum/maximum feasible answer.

| # | Problem | Difficulty | NeetCode | Status |
|---|---|---|---|---|
| 17 | #875 Koko Eating Bananas | Medium | ✅ | |
| 18 | #1011 Capacity To Ship Packages Within D Days | Medium | ✅ | |
| 19 | #1482 Minimum Days to Make m Bouquets | Medium | | |
| 20 | #410 Split Array Largest Sum | Hard | | |
| 21 | #1552 Magnetic Force Between Two Balls | Medium | | |
| 22 | #2439 Minimize Maximum of Array | Medium | | |
| 23 | #1870 Minimum Speed to Arrive on Time | Medium | | |
| 24 | #2560 House Robber IV | Medium | | |

- [ ] #875 Koko Eating Bananas (NeetCode)
- [ ] #1011 Capacity To Ship Packages Within D Days (NeetCode)
- [ ] #1482 Minimum Days to Make m Bouquets
- [ ] #410 Split Array Largest Sum
- [ ] #1552 Magnetic Force Between Two Balls
- [ ] #2439 Minimize Maximum of Array
- [ ] #1870 Minimum Speed to Arrive on Time
- [ ] #2560 House Robber IV

**Patterns learned:** feasibility functions, monotonic answer space, greedy
+ binary search.

## Level 5 — Advanced Binary Search

These appear frequently in senior interviews.

| # | Problem | Difficulty | Blind 75 | Status |
|---|---|---|---|---|
| 25 | #981 Time Based Key-Value Store | Medium | ✅ | |
| 26 | #528 Random Pick with Weight | Medium | | |
| 27 | #4 Median of Two Sorted Arrays | Hard | ✅ | |
| 28 | #378 Kth Smallest Element in a Sorted Matrix | Medium | | |
| 29 | #658 Find K Closest Elements | Medium | | |
| 30 | #275 H-Index II | Medium | | |

- [ ] #981 Time Based Key-Value Store (Blind 75)
- [ ] #528 Random Pick with Weight
- [ ] #4 Median of Two Sorted Arrays (Blind 75)
- [ ] #378 Kth Smallest Element in a Sorted Matrix
- [ ] #658 Find K Closest Elements
- [ ] #275 H-Index II

**Patterns learned:** binary search combined with hash maps, prefix sums,
and value-space search over a matrix.

## Must-Know Problems

If short on time before interviews, prioritize these:

**Beginner**
- [ ] #704 Binary Search (Blind 75)
- [ ] #35 Search Insert Position

**Core**
- [ ] #34 Find First and Last Position of Element in Sorted Array (Blind 75)
- [ ] #33 Search in Rotated Sorted Array (Blind 75)
- [ ] #153 Find Minimum in Rotated Sorted Array (Blind 75)
- [ ] #74 Search a 2D Matrix (Blind 75)

**Advanced**
- [ ] #875 Koko Eating Bananas
- [ ] #981 Time Based Key-Value Store (Blind 75)
- [ ] #4 Median of Two Sorted Arrays (Blind 75)

## Recommended Order

1. **Stage 1 – Learn the invariant:** #704, #35
2. **Stage 2 – Learn boundaries:** #34, #162
3. **Stage 3 – Rotated arrays:** #33, #153, #74
4. **Stage 4 – Binary search on answer:** #875, #1011, #410
5. **Stage 5 – Interview-level mastery:** #981, #4, #528
