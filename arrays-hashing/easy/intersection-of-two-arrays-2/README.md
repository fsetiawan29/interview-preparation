# Problem: Intersection of Two Arrays II

## 1. Problem Understanding

### Problem Summary

Given two integer arrays `nums1` and `nums2`, return an array of their intersection, where each element in the result appears as many times as it shows up in both arrays.

### Input

- An integer array `nums1`
- An integer array `nums2`

### Output

- An array containing every value present in both arrays, with the correct multiplicity (order doesn't matter).

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
[2,2]
```

Manual walkthrough:

```text
nums1 = [1,2,2,1]  -> counts: 1:2, 2:2
nums2 = [2,2]

Scan nums2:
first 2 -> available in nums1's count (2 left) -> take it, count becomes 1
second 2 -> available (1 left) -> take it, count becomes 0

Result: [2,2]
```

---

# 2. Key Insight

## What makes this problem difficult?

Unlike a plain set intersection, duplicates matter here — an element should appear in the result exactly `min(count in nums1, count in nums2)` times, not just once. A naive nested loop comparing every pair would work but costs `O(n*m)` and needs careful bookkeeping to avoid reusing the same element twice.

## Key Observation

If we count how many times each value appears in `nums1`, we can then scan `nums2` once and, for each value, "spend" one unit of its remaining count from the map — as long as some count remains, that value belongs in the intersection.

Example:

```text
nums1 = [4,9,5]         -> freq = {4:1, 9:1, 5:1}
nums2 = [9,4,9,8,4]

Scan nums2:
9 -> freq[9]=1 > 0 -> take it, freq[9]=0
4 -> freq[4]=1 > 0 -> take it, freq[4]=0
9 -> freq[9]=0, not > 0 -> skip (already used up)
8 -> not in freq -> skip
4 -> freq[4]=0, not > 0 -> skip (already used up)

Result: [9,4]
```

## Why does this observation help?

Decrementing the count as each match is consumed naturally caps how many times a value can appear in the result — exactly matching the number of times it was available in `nums1`. This turns an `O(n*m)` nested search into a single `O(n + m)` pass.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture `nums1`'s values sorted into labeled buckets, each holding a stack of tokens (one token per occurrence). Walk through `nums2`, and for each value, try to take one token off the matching bucket. If the bucket has a token, take it and add the value to the result. If the bucket is empty (or doesn't exist), move on without taking anything.

```text
Buckets from nums1=[4,9,5]:  4:[●]   9:[●]   5:[●]

Walk nums2 = 9  4  9  8  4
             ↓  ↓  ↓  ↓  ↓
take 9   take 4  bucket 9    no       bucket 4
token    token   empty    bucket    empty
result:  [9]    [9,4]    (skip)    (skip)   (skip)
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Build freq (count each value in nums1)
   │
   ▼
Initialize res = empty list
   │
   ▼
For each n in nums2:
   │
   ▼
Is n in freq ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is freq[n] > 0 ?   Next n (or Done)
   │
 ┌─┴─────────┐
 │            │
Yes           No
 │            │
 ▼            ▼
Append n to res,   Next n (or Done)
freq[n] -= 1
   │
   ▼
Next n (or Done)
   │
   ▼
Return res
```

Explanation of each decision:

- `freq` is built once from `nums1` before scanning `nums2` — it holds the full available supply of each value.
- A value is only added to `res` if it's present in `freq` *and* still has a remaining count above `0`.
- Every successful match decrements the count, so a value can never be matched more times than it originally appeared in `nums1`.

---

# 5. Plain English Algorithm

1. Build a frequency map `freq` counting every value in `nums1`.
2. Create an empty result list `res`.
3. Scan `nums2` left to right. For each value `n`:
   - If `n` is in `freq` and `freq[n] > 0`, append `n` to `res` and decrement `freq[n]`.
4. Return `res`.

---

# 6. Pseudocode

```text
freq = empty map

for n in nums1
    freq[n] = freq.get(n, 0) + 1

res = empty list

for n in nums2
    if n in freq and freq[n] > 0
        res.append(n)
        freq[n] -= 1

return res
```

---

# 7. Python Solution

```python
class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        freq = {}
        for n in nums1:
            freq[n] = freq.get(n, 0) + 1

        res = []
        for n in nums2:
            if n in freq:
                if freq[n] > 0:
                    res.append(n)
                    freq[n] -= 1

        return res
```

---

# 8. Dry Run

Example:

```text
nums1 = [4,9,5], nums2 = [9,4,9,8,4]

freq built from nums1: {4:1, 9:1, 5:1}
```

| Step | n (from nums2) | freq[n] before | Action | res | Why? |
|------|-----------------|------------------|--------|-----|------|
| 1 | 9 | 1 | Append, freq[9]=0 | [9] | 9 available in freq |
| 2 | 4 | 1 | Append, freq[4]=0 | [9,4] | 4 available in freq |
| 3 | 9 | 0 | Skip | [9,4] | 9's supply already used up |
| 4 | 8 | — | Skip | [9,4] | 8 not in freq at all |
| 5 | 4 | 0 | Skip | [9,4] | 4's supply already used up |

Result: `[9,4]`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n + m)
```

Why?

- `n = len(nums1)` to build `freq`, `m = len(nums2)` to scan and consume it — each element does constant work.

### Space Complexity

```text
O(n)
```

Why?

- `freq` holds up to `n` distinct keys from `nums1` (the output `res` isn't counted as extra space).
