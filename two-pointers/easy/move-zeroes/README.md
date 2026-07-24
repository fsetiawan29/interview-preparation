# Problem: Move Zeroes

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums`, move all `0`s to the end while keeping the relative order of the non-zero elements the same.

The modification must be done **in-place**, without making a copy of the array.

### Input

- An integer array `nums`

### Output

- Modify `nums` in-place so all zeroes are pushed to the end, non-zero order preserved.

### Constraints

- `1 <= nums.length <= 10^4`
- `-2^31 <= nums[i] <= 2^31 - 1`

### Example

Input:

```text
nums = [0,1,0,3,12]
```

Output:

```text
[1,3,12,0,0]
```

Manual walkthrough:

```text
Original

[0,1,0,3,12]

Every non-zero value, in order: 1, 3, 12

Place them starting from index 0

↓

[1,3,12, ?, ?]

Fill the remaining slots with 0

↓

[1,3,12,0,0]
```

---

# 2. Key Insight

## What makes this problem difficult?

We can't simply delete zeroes and append them at the end using a second array — that violates the in-place constraint. And shifting elements one at a time whenever a zero is found is easy to get wrong (it's easy to accidentally reorder non-zero values).

## Key Observation

Every non-zero value needs to land at the **next available "non-zero slot"**, in the same order it was read. That slot pointer only moves forward when a non-zero value is actually placed.

Example:

```text
[0, 1, 0, 3, 12]
    ↑
  next non-zero slot starts at index 0,
  only advances once something is written there
```

## Why does this observation help?

A single forward pass with two pointers — one reading every element, one marking where the next non-zero value belongs — places every non-zero value correctly without ever touching a second array. Whatever's left behind the write pointer is automatically all zeroes.

---

# 3. Mental Model

> What picture should I imagine in my head?

Imagine `j` as a "collector" walking just behind `i`. Every time `i` finds a non-zero value, it hands it to `j`'s slot and `j` steps forward. Zeroes are simply not handed over — `j` stays put and waits.

```text
[0, 1, 0, 3, 12]
 i
 j

i finds 0 -> skip, j stays

[0, 1, 0, 3, 12]
    i
 j

i finds 1 -> swap with j's slot, j advances

[1, 0, 0, 3, 12]
       i
    j

... continue until i passes the end
```

By the time `i` finishes scanning, every non-zero value sits before `j`, in original order, and every zero has been swapped past it.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize j = 0
   │
   ▼
For each i from 0 to len(nums) - 1
   │
   ▼
Is nums[i] == 0 ?
   │
 ┌─┴─────────────┐
 │               │
Yes              No
 │               │
 ▼               ▼
Skip (leave j)   Is i != j ?
 │                  │
 │                ┌─┴──────┐
 │                │         │
 │               Yes        No
 │                │         │
 │                ▼         ▼
 │            Swap       (already in place)
 │            nums[i], nums[j]
 │                │         │
 │                └────┬────┘
 │                     ▼
 │                  j += 1
 │                     │
 └─────────────────────┴──▶ (next i)
```

Explanation of each decision:

- A zero at `i` is simply skipped — `j` doesn't move, reserving its slot for the next non-zero value.
- A non-zero at `i` gets swapped into `j`'s slot (only if `i != j`, to avoid a wasted no-op swap), and `j` advances to reserve the next slot.

---

# 5. Plain English Algorithm

1. Set a write pointer `j` to `0`.
2. Scan the array left to right with a read pointer `i`.
3. If `nums[i]` is `0`, skip it — leave `j` where it is.
4. If `nums[i]` is non-zero, swap it into position `j` (if it isn't already there), then advance `j`.
5. After the scan, every non-zero value sits in its original relative order before index `j`, and everything from `j` onward is `0`.

---

# 6. Pseudocode

```text
j = 0

for i in 0 .. length(nums) - 1
    if nums[i] == 0
        continue

    if i != j
        swap nums[i], nums[j]

    j++
```

---

# 7. Python Solution

```python
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        j = 0
        for i in range(len(nums)):
            if nums[i] == 0:
                continue

            if i != j:
                nums[i], nums[j] = nums[j], nums[i]
            j += 1
```

---

# 8. Dry Run

Example:

```text
nums = [0,1,0,3,12]
```

| Step | Pointer(s) | Current Values | Action | Array State | Why? |
|------|------------|-----------------|--------|-------------|------|
| 1 | i=0, j=0 | 0 | Skip | [0,1,0,3,12] | Zero, leave j |
| 2 | i=1, j=0 | 1 | Swap, j=1 | [1,0,0,3,12] | Non-zero placed at slot 0 |
| 3 | i=2, j=1 | 0 | Skip | [1,0,0,3,12] | Zero, leave j |
| 4 | i=3, j=1 | 3 | Swap, j=2 | [1,3,0,0,12] | Non-zero placed at slot 1 |
| 5 | i=4, j=2 | 12 | Swap, j=3 | [1,3,12,0,0] | Non-zero placed at slot 2 |

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- Single pass with `i` scanning every element once.
- `j` moves at most `n` times, always in step with `i`.

### Space Complexity

```text
O(1)
```

Why?

- Values are swapped in place.
- Only the two pointers `i` and `j` are used as extra state.
