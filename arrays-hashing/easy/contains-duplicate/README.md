# Problem: Contains Duplicate

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums`, determine if any value appears at least twice in the array.

### Input

- An integer array `nums`

### Output

- `true` if any value appears more than once, `false` if every element is distinct.

### Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

### Example

Input:

```text
nums = [1,2,3,1]
```

Output:

```text
true
```

Manual walkthrough:

```text
nums = [1, 2, 3, 1]

Seen so far: {}      -> see 1, not seen, remember it
Seen so far: {1}     -> see 2, not seen, remember it
Seen so far: {1,2}   -> see 3, not seen, remember it
Seen so far: {1,2,3} -> see 1, already seen -> duplicate found
```

---

# 2. Key Insight

## What makes this problem difficult?

Comparing every pair of elements to check for a duplicate costs `O(n^2)`. Sorting first would work in `O(n log n)`, but a faster approach exists if we're willing to spend a little extra memory.

## Key Observation

Membership in a hash set can be checked in average `O(1)` time. Instead of comparing each element against every other element, we can just ask "have I seen this value before?" as we scan once, left to right.

Example:

```text
nums = [1,2,3,1]

At the 4th element (value=1):
seen = {1,2,3}
1 is already in seen -> duplicate exists
```

## Why does this observation help?

A single pass with a hash set turns the pairwise comparison problem into a sequence of `O(1)` average-case lookups, reducing overall time to `O(n)` at the cost of `O(n)` extra space.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture walking through the array left to right while holding a growing bag of "numbers I've already seen." Before dropping a new number into the bag, check if it's already inside. If it is, stop immediately — a duplicate was found.

```text
nums:  1   2   3   1
       ↑
   bag={} -> 1 not in bag -> drop 1 in

nums:  1   2   3   1
           ↑
   bag={1} -> 2 not in bag -> drop 2 in

nums:  1   2   3   1
                   ↑
   bag={1,2,3} -> 1 IS in bag -> duplicate!
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize seen = empty set
   │
   ▼
For each n in nums:
   │
   ▼
Is n in seen ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return true       Add n to seen
                       │
                       ▼
                  Next n (or Done)
                       │
                       ▼
                 Return false
```

Explanation of each decision:

- Every element is checked against `seen` before being added — this ordering matters, since checking-then-adding is what makes a true duplicate detectable.
- The moment a repeated value is found, the scan stops early and returns `true`.
- If the loop finishes without any hit, every element was distinct.

---

# 5. Plain English Algorithm

1. Create an empty hash set `seen`.
2. Scan `nums` left to right. For each value `n`:
   - If `n` is already in `seen`, return `true` immediately.
   - Otherwise, add `n` to `seen`.
3. If the scan completes without finding a repeat, return `false`.

---

# 6. Pseudocode

```text
seen = empty set

for n in nums
    if n in seen
        return true
    seen.add(n)

return false
```

---

# 7. Python Solution

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for n in nums:
            if n in seen:
                return True
            seen.add(n)
        return False
```

---

# 8. Dry Run

Example:

```text
nums = [1,2,3,1]
```

| Step | n | seen (before) | Action | Why? |
|------|---|---------------|--------|------|
| 1 | 1 | {} | Not found, add 1 | seen = {1} |
| 2 | 2 | {1} | Not found, add 2 | seen = {1,2} |
| 3 | 3 | {1,2} | Not found, add 3 | seen = {1,2,3} |
| 4 | 1 | {1,2,3} | Found! Return true | 1 already in seen |

Result: `true`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- A single pass over `nums`, with average `O(1)` hash set lookup and insert per element.

### Space Complexity

```text
O(n)
```

Why?

- Worst case (no duplicates), `seen` grows to hold every element in `nums`.
