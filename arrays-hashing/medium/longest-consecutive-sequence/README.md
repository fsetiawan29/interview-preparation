# Problem: Longest Consecutive Sequence

## 1. Problem Understanding

### Problem Summary

Given an unsorted array of integers `nums`, find the length of the longest run of consecutive integers (e.g. `[1,2,3,4]`) that can be formed from the numbers present in `nums`. The algorithm must run in `O(n)` time.

### Input

- An array of integers `nums`

### Output

- The length of the longest consecutive elements sequence, as an integer.

### Constraints

- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

### Example

Input:

```text
nums = [100,4,200,1,3,2]
```

Output:

```text
4
```

Manual walkthrough:

```text
nums = [100,4,200,1,3,2]

The numbers present are: {1,2,3,4,100,200}

Consecutive runs hiding in this set:
  1,2,3,4       (length 4)
  100           (length 1)
  200           (length 1)

Longest run: [1,2,3,4] -> length 4
```

---

# 2. Key Insight

## What makes this problem difficult?

Sorting first gives an `O(n log n)` solution — but the problem explicitly wants `O(n)`. Without sorting, checking "is `n+1` present?" naively for every element could restart the same run over and over (e.g. starting the walk from `2`, then again from `3`, then again from `4`, all part of the same run), wasting work.

## Key Observation

Put every number into a **hash set** for O(1) membership checks. Then, only start walking a sequence from a number `n` if `n - 1` is **not** in the set — that guarantees `n` is the *start* of its run, not somewhere in the middle. Every run then gets walked forward exactly once, from its true starting point.

Example:

```text
num_set = {1,2,3,4,100,200}

n = 3: is 2 in the set? yes -> 3 is NOT a start, skip it here
n = 1: is 0 in the set? no  -> 1 IS a start, walk forward: 2,3,4 all present -> length 4
```

## Why does this observation help?

Because each number is only ever walked forward as part of *one* run (the run it truly starts), the total work across all the inner "walk forward" loops adds up to at most `n` steps overall — even though the outer loop iterates over every number in the set, only true starts trigger the (potentially long) inner walk.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture the numbers laid out on a number line, with only the present values lit up. To find a run's length without retracing steps, only click "start walking" on a lit number that has no lit neighbor immediately to its left.

```text
Number line:  ... 1  2  3  4  ...  100  ...  200 ...
Present:          ✓  ✓  ✓  ✓        ✓         ✓

n=1: left neighbor 0 is unlit -> START here, walk right: 2✓ 3✓ 4✓ 5✗ -> length 4
n=2: left neighbor 1 is lit   -> not a start, skip (already covered by the walk from 1)
n=3: left neighbor 2 is lit   -> not a start, skip
n=4: left neighbor 3 is lit   -> not a start, skip
n=100: left neighbor 99 unlit -> START here, walk right: 101✗ -> length 1
n=200: left neighbor 199 unlit -> START here, walk right: 201✗ -> length 1
```

The longest walk found across all true starts is the answer.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Build num_set from nums (drops duplicates, O(1) lookups)
   │
   ▼
Initialize longest = 0
   │
   ▼
For each n in num_set:
   │
   ▼
Is (n - 1) in num_set ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Skip n (not a         n IS a sequence start
sequence start)              │
 │                            ▼
 │                     Walk forward: next_num = n+1,
 │                     length = 1; while next_num in
 │                     num_set: length++, next_num++
 │                            │
 │                            ▼
 │                     longest = max(longest, length)
 │                            │
 └──────────────┬─────────────┘
                ▼
     (loop to next n in num_set)
                │
                ▼
   All numbers processed — return longest
```

Explanation of each decision:

- Checking `n - 1 not in num_set` is what identifies a true sequence start — skipping non-starts is what keeps the total work linear.
- The inner `while` loop only runs from true starts, walking forward exactly as far as the consecutive run extends.
- `longest` is updated after every completed walk, tracking the best run seen so far.

---

# 5. Plain English Algorithm

1. Put every number from `nums` into a hash set `num_set` (this also removes duplicates).
2. Initialize `longest = 0`.
3. For each number `n` in `num_set`:
   - If `n - 1` is in `num_set`, skip it — `n` is not the start of a run.
   - Otherwise, `n` is a sequence start: walk forward (`n+1`, `n+2`, ...) counting the length of the run while each next number is present in `num_set`.
   - Update `longest` with the length of this run if it's larger.
4. Return `longest`.

---

# 6. Pseudocode

```text
num_set = set(nums)
longest = 0

for n in num_set
    if (n - 1) not in num_set
        next_num = n + 1
        length = 1

        while next_num in num_set
            next_num += 1
            length += 1

        longest = max(longest, length)

return longest
```

---

# 7. Python Solution

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)

        longest = 0
        for n in num_set:
            if n - 1 not in num_set:
                next_num = n + 1
                length = 1
                while next_num in num_set:
                    next_num += 1
                    length += 1
                longest = max(longest, length)
        return longest
```

---

# 8. Dry Run

Example:

```text
nums = [100,4,200,1,3,2]

num_set = {100,4,200,1,3,2}
```

| Step | n | (n-1) in set? | Action | Walk result | longest after |
|------|---|----------------|--------|--------------|----------------|
| 1 | 100 | 99 not in set | Start walk | 101 not in set → length=1 | 1 |
| 2 | 4 | 3 in set | Not a start, skip | — | 1 |
| 3 | 200 | 199 not in set | Start walk | 201 not in set → length=1 | 1 |
| 4 | 1 | 0 not in set | Start walk | 2✓,3✓,4✓,5✗ → length=4 | 4 |
| 5 | 3 | 2 in set | Not a start, skip | — | 4 |
| 6 | 2 | 1 in set | Not a start, skip | — | 4 |

(Iteration order over a Python `set` isn't guaranteed, but every element is visited exactly once regardless of order, and the result is the same.)

Result: `longest = 4`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- Building `num_set` from `nums` is `O(n)`.
- The outer `for` loop visits every element once, but the inner `while` loop only executes for true sequence starts.
- Across the entire run of the algorithm, every number is visited by an inner-loop walk at most once (since each number belongs to exactly one consecutive run and is only ever walked from that run's true start) — so total work stays `O(n)`.

### Space Complexity

```text
O(n)
```

Why?

- `num_set` holds up to `n` elements (fewer if there are duplicates).
