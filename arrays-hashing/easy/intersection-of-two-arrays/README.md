# Problem: Intersection of Two Arrays

## 1. Problem Understanding

### Problem Summary

Given two integer arrays `nums1` and `nums2`, return an array of their intersection. Each element in the result must be **unique**, and the result may be returned in any order.

### Input

- An integer array `nums1`
- An integer array `nums2`

### Output

- An array of the unique values present in both arrays (order doesn't matter).

### Constraints

- `1 <= nums1.length, nums2.length <= 1000`
- `0 <= nums1[i], nums2[i] <= 1000`

### Example

Input:

```text
nums1 = [1,2,2,1], nums2 = [2,2]
```

Output:

```text
[2]
```

Manual walkthrough:

```text
nums1 = [1,2,2,1] -> unique values: {1, 2}
nums2 = [2,2]

Scan nums2, checking against {1, 2}:
2 is in {1,2} -> add to result set
2 is in {1,2} -> already in result set, no change

Result: [2]
```

---

# 2. Key Insight

## What makes this problem difficult?

Duplicates exist in both input arrays, but the result must contain each shared value only once. Comparing every element of `nums1` against every element of `nums2` with nested loops (`O(n*m)`) would also need extra logic to avoid adding the same value to the result twice.

## Key Observation

Converting `nums1` into a set immediately removes its duplicates and gives `O(1)` average membership checks. Scanning `nums2` and adding matches into a second set (instead of a list) automatically dedupes the result too — from either side.

Example:

```text
nums1 = [4,9,5] -> seen = {4,9,5}
nums2 = [9,4,9,8,4]

Scan nums2:
9 -> in seen -> res.add(9)
4 -> in seen -> res.add(4)
9 -> in seen -> res.add(9) again (no effect, already in res)
8 -> not in seen -> skip
4 -> in seen -> res.add(4) again (no effect, already in res)

Result: {9,4} -> [9,4]
```

## Why does this observation help?

Using a set for `nums1` turns membership checks into `O(1)` average operations, and using a set for the result eliminates the need for any manual duplicate tracking — the set data structure handles it for free.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture pouring all of `nums1`'s values into a bag, letting duplicates naturally merge into single copies. Then walk through `nums2`, and for every value that's found in the bag, drop it into a second (also duplicate-merging) result bag.

```text
Bag from nums1=[4,9,5]:  {4, 9, 5}

Walk nums2 = 9  4  9  8  4
             ↓  ↓  ↓  ↓  ↓
            in  in  in  not  in
           bag bag bag  bag  bag
result bag: {9} {9,4} {9,4} {9,4} {9,4}
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Build seen = set(nums1)
   │
   ▼
Initialize res = empty set
   │
   ▼
For each n in nums2:
   │
   ▼
Is n in seen ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Add n to res      Next n (or Done)
   │
   ▼
Next n (or Done)
   │
   ▼
Return list(res)
```

Explanation of each decision:

- `seen` is built once from `nums1`, deduping it from the start.
- Every value of `nums2` is checked against `seen`; only matches get added to `res`.
- Since `res` is also a set, adding an already-present value has no effect, so the final result naturally has no duplicates.

---

# 5. Plain English Algorithm

1. Convert `nums1` into a set `seen`.
2. Create an empty result set `res`.
3. Scan `nums2` left to right. For each value `n`:
   - If `n` is in `seen`, add `n` to `res`.
4. Return `res` converted to a list.

---

# 6. Pseudocode

```text
seen = set(nums1)
res = empty set

for n in nums2
    if n in seen
        res.add(n)

return list(res)
```

---

# 7. Python Solution

```python
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        seen = set(nums1)

        res = set()
        for n in nums2:
            if n in seen:
                res.add(n)

        return list(res)
```

---

# 8. Dry Run

Example:

```text
nums1 = [4,9,5], nums2 = [9,4,9,8,4]

seen built from nums1: {4,9,5}
```

| Step | n (from nums2) | In seen? | Action | res | Why? |
|------|-----------------|----------|--------|-----|------|
| 1 | 9 | Yes | Add 9 | {9} | 9 present in nums1 |
| 2 | 4 | Yes | Add 4 | {9,4} | 4 present in nums1 |
| 3 | 9 | Yes | Add 9 (no effect) | {9,4} | Already in res |
| 4 | 8 | No | Skip | {9,4} | 8 not present in nums1 |
| 5 | 4 | Yes | Add 4 (no effect) | {9,4} | Already in res |

Result: `[9,4]` (order may vary)

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n + m)
```

Why?

- `n = len(nums1)` to build `seen`, `m = len(nums2)` to scan — each with average `O(1)` set operations.

### Space Complexity

```text
O(n + m)
```

Why?

- Worst case, `seen` holds up to `n` distinct elements and `res` holds up to `min(n, m)` distinct elements.
