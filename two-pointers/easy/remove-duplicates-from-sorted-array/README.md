# Problem: Remove Duplicates from Sorted Array

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums` sorted in non-decreasing order, remove the duplicates in-place so each unique value appears only once. Return `k`, the number of unique elements, with those `k` values placed at the front of `nums` in their original sorted order.

The modification must be done **in-place**, without allocating another array.

### Input

- An integer array `nums`, sorted in non-decreasing order

### Output

- An integer `k` — the count of unique elements.
- `nums` modified in-place so `nums[0..k-1]` holds the unique values in order.

### Constraints

- `1 <= nums.length <= 3 * 10^4`
- `-100 <= nums[i] <= 100`
- `nums` is sorted in non-decreasing order.

### Example

Input:

```text
nums = [0,0,1,1,1,2,2,3,3,4]
```

Output:

```text
5, nums = [0,1,2,3,4,_,_,_,_,_]
```

Manual walkthrough:

```text
Original

[0,0,1,1,1,2,2,3,3,4]

Every time a new value is seen (different from the last unique one), keep it.

Unique values, in order: 0, 1, 2, 3, 4

Write them starting from index 0

↓

[0,1,2,3,4, _,_,_,_,_]

k = 5 (the rest of the array's contents no longer matter)
```

---

# 2. Key Insight

## What makes this problem difficult?

Removing an element from the middle of an array normally means shifting everything after it — done naively that's an `O(n)` shift per duplicate, and it's easy to lose track of which values have already been kept when duplicates repeat many times in a row.

## Key Observation

Because `nums` is **already sorted**, duplicates of the same value are always **adjacent**. That means uniqueness can be checked with a single comparison: is the current value different from the *last value we kept*?

Example:

```text
[0, 0, 1, 1, 1, 2]
       ↑
   last kept value is at j-1;
   compare nums[i] to nums[j-1], not to every prior value
```

## Why does this observation help?

No `set` is needed to track "seen" values — a single write pointer `j` remembers the last unique value's position. Whenever the read pointer `i` finds a value that differs from `nums[j-1]`, it's guaranteed to be a brand-new unique value (since sorted order rules out it matching anything further back).

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture `j` as a "unique values so far" counter that also marks the next free slot. `i` scans ahead looking for the next value that's different from whatever `j` last wrote — the moment it finds one, it hands it to `j`, and `j` advances.

```text
[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    i
 j

nums[i]=0 == nums[j-1]=0 -> duplicate, skip

[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
       i
    j

nums[i]=1 != nums[j-1]=0 -> new unique value, write it at j, j advances

[0, 1, 1, 1, 1, 2, 2, 3, 3, 4]
          i
       j
```

`nums[0]` is always trusted as the first unique value for free — there's nothing before it to duplicate.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize j = 1
(nums[0] is always kept as the first unique value)
   │
   ▼
For each i from 1 to len(nums) - 1
   │
   ▼
Is nums[i] != nums[j - 1] ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Write nums[j] = nums[i]   Skip — duplicate of the last kept value
j += 1                    (j stays put)
 │                    │
 └────────┬───────────┘
          ▼
    (next i)
   │
   ▼
Return j
```

Explanation of each decision:

- `nums[i] != nums[j-1]` means `nums[i]` is a value never kept before (sorted order guarantees no earlier duplicate could sneak past).
- `nums[i] == nums[j-1]` means it's a repeat of the value most recently kept — do nothing, and `j` continues to mark the correct next write position.

---

# 5. Plain English Algorithm

1. Set the write pointer `j` to `1` — `nums[0]` is always the first unique value.
2. Scan the array from index `1` onward with a read pointer `i`.
3. If `nums[i]` is different from `nums[j-1]` (the last value kept), write it to `nums[j]` and advance `j`.
4. If `nums[i]` equals `nums[j-1]`, it's a duplicate — skip it.
5. After the scan, `nums[0..j-1]` holds the unique values in order; return `j`.

---

# 6. Pseudocode

```text
j = 1

for i in 1 .. length(nums) - 1
    if nums[i] != nums[j - 1]
        nums[j] = nums[i]
        j++

return j
```

---

# 7. Python Solution

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        j = 1

        for i in range(1, len(nums)):
            if nums[i] != nums[j-1]:
                nums[j] = nums[i]
                j += 1

        return j
```

---

# 8. Dry Run

Example:

```text
nums = [1,1,2]
```

| Step | Pointer(s) | Current Values | Action | Array State | Why? |
|------|------------|-----------------|--------|-------------|------|
| 1 | i=1, j=1 | nums[1]=1, nums[j-1]=1 | Skip | [1,1,2] | Duplicate of last kept value |
| 2 | i=2, j=1 | nums[2]=2, nums[j-1]=1 | Write nums[1]=2, j=2 | [1,2,2] | New unique value |

Result: `k = 2`, `nums[:2] = [1, 2]`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- Single pass, `i` scans every element exactly once.
- No sorting is needed since `nums` is already sorted.

### Space Complexity

```text
O(1)
```

Why?

- Overwritten in place.
- Only the two pointers `i` and `j` are used as extra state — no `set` or auxiliary array.
