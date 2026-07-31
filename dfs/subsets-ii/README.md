# Problem: Subsets II

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums` that may contain duplicates, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.

### Input

- An integer array `nums` that may contain duplicate values

### Output

- A list of lists, where each inner list is one subset of `nums`, and together they form the full power set — with no duplicate subsets.

### Constraints

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`

### Example

Input:

```text
nums = [1,2,2]
```

Output:

```text
[[],[1],[1,2],[1,2,2],[2],[2,2]]
```

---

## 2. Brute Force Approach

### Idea

Reuse the [Subsets](../subsets) take/skip recursion unchanged, generate every subset (including duplicates), then dedupe the result afterward — e.g. by converting each subset to a sorted tuple and inserting everything into a set.

### Pseudocode

```text
result = []

function dfs(index, subset):
    if index == length(nums):
        result.append(copy of subset)
        return
    subset.append(nums[index])
    dfs(index + 1, subset)
    subset.pop()
    dfs(index + 1, subset)

dfs(0, [])

deduped = set of tuple(sorted(subset)) for subset in result
return deduped, converted back to lists
```

### Complexity Analysis

#### Time Complexity

```text
O(n * 2^n)
```

Why?

- Same `2^n` leaves as Subsets I, each costing `O(n)` to copy — plus another `O(n log n)` per subset to sort it for the dedup key, which doesn't change the dominant term.

#### Space Complexity

```text
O(n * 2^n)
```

Why?

- Every one of the `2^n` generated subsets (including duplicates before dedup) is held in memory at once inside the intermediate set, before the final result is produced.

### Why this isn't good enough

It does `2^n` work to generate raw subsets and then throws a large fraction of them away as duplicates — for `nums = [2,2,2,2,2,2,2,2,2,2]` almost every one of the 1024 generated subsets is a duplicate of just 11 distinct ones. The wasted generation and the extra sort-per-subset dedup step are avoidable if duplicates are skipped *during* generation instead of *after*.

---

## 3. Key Insight

### What makes this problem difficult?

Duplicate values in `nums` (e.g. the two `2`s in `[1,2,2]`) can produce the exact same subset through different index choices — picking index 1's `2` vs. index 2's `2` both yield the subset `[2]`. Naively they look like different decisions, but they must collapse into one entry in the output.

### Key Observation

If `nums` is sorted first, every duplicate value ends up adjacent. At any given recursion depth, iterating over sibling choices left-to-right, a duplicate equal to the *previous* sibling *at that same depth* would only ever regenerate a subset that the previous sibling's subtree already fully covered. So skip a candidate whenever it equals the sibling right before it in the same loop (`nums[i] == nums[i-1]` and `i > start`) — that's not a global "seen it before" check, just a local one against the immediately preceding sibling.

### Why does this observation help?

Sorting turns "duplicate values scattered anywhere in the array" into "duplicate values sitting next to each other," which makes the skip condition a cheap, local comparison (`nums[i] == nums[i-1]`) instead of needing a hash set to track every subset seen so far. Only the *first* occurrence of a value at each recursion level is explored; every later occurrence is skipped because its entire subtree of subsets is identical to what the first occurrence already generated.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture `nums` sorted and laid out left to right. Every recursive call records the current `subset` immediately (it's already valid the moment it's reached), then tries extending it with each remaining element to its right, one at a time — skipping any element that is identical to the sibling immediately before it, since that sibling's subtree already generated every subset reachable from this position.

```text
sorted nums = [1, 2, 2]

dfs(start=0, [])              -> record []
 ├─ i=0 (1): dfs(1, [1])       -> record [1]
 │   ├─ i=1 (2): dfs(2, [1,2]) -> record [1,2]
 │   │   └─ i=2 (2): dfs(3, [1,2,2]) -> record [1,2,2]
 │   └─ i=2 (2): SKIP (nums[2]==nums[1], i>start)
 └─ i=1 (2): dfs(2, [2])       -> record [2]
     └─ i=2 (2): dfs(3, [2,2]) -> record [2,2]
     (i=2 never separately tried here — it's the branch just taken)
     back at top level, i=2 (2): SKIP (nums[2]==nums[1], i>start)
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
dfs(start, subset)
   │
   ▼
Record a copy of subset into result
(every call's subset is a valid answer)
   │
   ▼
for i in start .. len(nums)-1:
   │
   ▼
Is i > start AND nums[i] == nums[i-1] ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Skip this i      TAKE: subset.append(nums[i])
(continue loop)         │
                         ▼
                  dfs(i + 1, subset)
                         │
                         ▼
                  BACKTRACK: subset.pop()
                         │
                         ▼
                  continue loop with next i
```

Explanation of each decision:

- Recording happens unconditionally at the top of every call — unlike Word Search, there's no invalid state here; the current `subset` (empty or not) is always a complete, legitimate answer the moment this frame is entered.
- The loop (not a binary take/skip) is what lets `start` control "which elements are still eligible" — each recursive call only considers elements at or after `start`, so earlier elements are never revisited, guaranteeing every subset is generated in strictly increasing index order and thus exactly once *before* dedup logic is even needed.
- The skip condition `i > start and nums[i] == nums[i-1]` only fires against the *immediately preceding sibling in this same loop* — it does not compare against elements from earlier recursion levels, so it's safe even though `nums[i-1]` might have been used deeper in the branch that was just explored.
- `subset.pop()` after each recursive call restores `subset` to the state it had before `nums[i]` was appended, so the next iteration of the loop starts clean.

---

## 6. Plain English Algorithm

1. Sort `nums` first, so equal values become adjacent.
2. Start `dfs` at `start = 0` with an empty `subset`.
3. Immediately record a copy of `subset` into `result` — it's already a valid subset the moment this call is entered.
4. Loop over every index `i` from `start` to the end of `nums`:
   - If `i` is past `start` and `nums[i]` equals the previous element `nums[i-1]`, skip this `i` — it's a duplicate sibling choice that would only regenerate subsets already produced.
   - Otherwise, take `nums[i]`: append it to `subset`, recurse with `dfs(i + 1, subset)`, then pop it back off (backtrack) before moving to the next `i`.
5. Once the initial `dfs(0, [])` call returns, `result` holds every distinct subset — return it.

---

## 7. Pseudocode

```text
nums.sort()
result = []

function dfs(start, subset):
    result.append(copy of subset)

    for i in start .. length(nums) - 1:
        if i > start and nums[i] == nums[i - 1]:
            continue                      # skip duplicate sibling

        subset.append(nums[i])
        dfs(i + 1, subset)
        subset.pop()                      # backtrack

dfs(0, [])
return result
```

---

## 8. Python Solution

```python
class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []

        def dfs(start, subset):
            result.append(subset.copy())

            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i-1]:
                    continue

                subset.append(nums[i])
                dfs(i+1, subset)
                subset.pop()

        dfs(0, [])
        return result
```

---

## 9. Dry Run

Example (`nums` already sorted: `[1,2,2]`):

```text
nums = [1,2,2]
```

| Step | Call | `subset` | Action | Why? |
|------|------|----------|--------|------|
| 1 | `dfs(0, [])` | `[]` | record `[]` | every call records first |
| 2 | loop `i=0` (`1`) | `[]` → `[1]` | `i==start`, take, recurse `dfs(1,[1])` | first choice at this level |
| 3 | `dfs(1, [1])` | `[1]` | record `[1]` | |
| 4 | loop `i=1` (`2`) | `[1]` → `[1,2]` | `i==start`, take, recurse `dfs(2,[1,2])` | first choice at this level |
| 5 | `dfs(2, [1,2])` | `[1,2]` | record `[1,2]` | |
| 6 | loop `i=2` (`2`) | `[1,2]` → `[1,2,2]` | `i==start`, take, recurse `dfs(3,[1,2,2])` | first choice at this level |
| 7 | `dfs(3, [1,2,2])` | `[1,2,2]` | record `[1,2,2]`; loop range is empty | base of this branch |
| 8 | back in step 6's call | `[1,2,2]` → `[1,2]` | `pop()` | backtrack |
| 9 | back in step 4's call | `[1,2]` → `[1]` | `pop()`; loop ends (`i=2` was the last index) | backtrack |
| 10 | back in step 2's call | `[1]` → `[]` | `pop()` | backtrack from `dfs(1,...)` |
| 11 | loop `i=1` (`2`) | `[]` → `[2]` | `i>start` but `nums[1] != nums[0]` (`2 != 1`), take, recurse `dfs(2,[2])` | second top-level choice, not a duplicate sibling |
| 12 | `dfs(2, [2])` | `[2]` | record `[2]` | |
| 13 | loop `i=2` (`2`) | `[2]` → `[2,2]` | `i==start`, take, recurse `dfs(3,[2,2])` | first choice at this level |
| 14 | `dfs(3, [2,2])` | `[2,2]` | record `[2,2]`; loop empty | base of this branch |
| 15 | back in step 13's call | `[2,2]` → `[2]` | `pop()` | backtrack |
| 16 | back in step 11's call | `[2]` → `[]` | `pop()`; loop ends | backtrack |
| 17 | loop `i=2` (`2`) | `[]` | `i>start` (`2>0`) and `nums[2]==nums[1]` (`2==2`) → **skip** | duplicate sibling of `i=1`, would only regenerate `[2]`/`[2,2]` |

Result: `[[], [1], [1,2], [1,2,2], [2], [2,2]]` — matches the expected output exactly, including order.

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n * 2^n)
```

Why?

- Sorting costs `O(n log n)`, dwarfed by the rest. In the worst case (no duplicates), the recursion still explores the same shape of decision tree as Subsets I — up to `2^n` distinct subsets, each recorded via an `O(n)` copy. Skipping duplicate siblings only ever *prunes* branches, so it never exceeds the duplicate-free bound of `O(n * 2^n)`.

### Space Complexity

```text
O(n)
```

Why?

- Excluding the output, the recursion stack holds at most `n` frames (one per index consumed, from `start` growing toward `len(nums)`), and `subset` holds at most `n` elements at a time. Sorting is done in place (or costs `O(n)` auxiliary depending on the sort implementation), which doesn't change the asymptotic bound. The `O(n * 2^n)` needed for the output itself is required by the problem, not extra auxiliary space.
