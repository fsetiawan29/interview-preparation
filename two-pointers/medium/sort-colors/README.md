# Problem: Sort Colors

## 1. Problem Understanding

### Problem Summary

Given an array `nums` containing only the values `0`, `1`, and `2` (representing red, white, and blue), sort the array in-place so that objects of the same color are adjacent, in the order red, white, blue — without using a library sort function.

### Input

- An integer array `nums` containing only `0`, `1`, or `2`

### Output

- `nums` sorted in-place (no return value).

### Constraints

- `n == nums.length`
- `1 <= n <= 300`
- `nums[i]` is `0`, `1`, or `2`.

### Example

Input:

```text
nums = [2,0,2,1,1,0]
```

Output:

```text
[0,0,1,1,2,2]
```

Manual walkthrough:

```text
Original

[2,0,2,1,1,0]

Use three pointers: low (next spot for 0), mid (current), high (next spot for 2)

mid sees 2 -> swap with high, shrink high
mid sees 0 -> swap with low, advance both low and mid
mid sees 1 -> already in place, advance mid only

Keep going until mid passes high

↓

[0,0,1,1,2,2]
```

---

# 2. Key Insight

## What makes this problem difficult?

Values can only take on `0`, `1`, or `2`, and the array must be sorted **in-place** in a single pass, without calling a general-purpose sort. A naive counting pass followed by a rewrite works, but a true one-pass, constant-space partition needs a way to place values correctly as it scans, even when a swapped-in value hasn't been checked yet.

## Key Observation

Because there are only three possible values, the array can be thought of as three growing regions: `0`s on the left, `1`s in the middle, and `2`s on the right. Three pointers — `low` (boundary of the `0` region), `mid` (current element being classified), and `high` (boundary of the `2` region) — can partition the array in a single pass, similar in spirit to opposite-ends two-pointer narrowing but with a third pointer added for the middle region.

Example:

```text
[2, 0, 2, 1, 1, 0]
 low                high
 mid

nums[mid] = 2 -> swap with nums[high], shrink high (don't advance mid yet —
the swapped-in value at mid hasn't been checked)
```

## Why does this observation help?

Swapping `nums[mid]` with `nums[low]` when it's a `0` extends the `0`-region and is always safe to advance past (the value swapped in from `low` was already known to be `1`, having been passed over by `mid` earlier). Swapping with `nums[high]` when it's a `2` extends the `2`-region, but the newly swapped-in value at `mid` is unclassified, so `mid` must stay put and be re-examined. This lets the whole array be partitioned in one linear pass with no extra memory.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture the array being carved into three zones as `mid` scans left to right: a `0`-zone growing from the left (bounded by `low`), a `2`-zone growing from the right (bounded by `high`), and an unexamined zone in between where `mid` currently stands.

```text
[ 0s ]        [ unknown ]        [ 2s ]
        ↑                  ↑
       low                high
        mid walks through "unknown", left to right

nums[mid]==0 -> swap into the 0-zone, low and mid both advance
nums[mid]==1 -> already in the middle zone, mid advances alone
nums[mid]==2 -> swap into the 2-zone, high shrinks, mid stays
                (must re-check the value just swapped in)
```

The scan ends once `mid` crosses `high` — everything left of `low` is `0`, everything from `low` to `high` is `1`, and everything past `high` is `2`.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize low = 0, mid = 0, high = len(nums) - 1
   │
   ▼
Is mid <= high ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
What is nums[mid] ?      Done — nums is sorted in-place
   │
 ┌─┴──────────────────┬──────────────────┐
 │                     │                  │
0                     1                  2
 │                     │                  │
 ▼                     ▼                  ▼
swap nums[mid],       mid += 1        swap nums[mid],
nums[low]             (already in         nums[high]
low += 1, mid += 1     place)         high -= 1
 │                     │              (mid stays — recheck
 │                     │               the swapped-in value)
 └─────────┬───────────┴──────────────────┘
           ▼
(back to "Is mid <= high ?")
```

Explanation of each decision:

- `nums[mid] == 0`: it belongs in the `0`-zone. Swapping it to `nums[low]` is always safe because the value that was at `low` (now moved to `mid`) was already confirmed to be a `1` by an earlier pass of `mid`.
- `nums[mid] == 1`: it's already exactly where it belongs (the middle zone) — only `mid` advances.
- `nums[mid] == 2`: it belongs in the `2`-zone. Swapping it to `nums[high]` is necessary, but the value now at `mid` came from an unexamined position and must be classified next, so `mid` does **not** advance.

---

# 5. Plain English Algorithm

1. Point `low = 0`, `mid = 0`, and `high = len(nums) - 1`.
2. While `mid <= high`:
   - If `nums[mid] == 0`, swap `nums[mid]` with `nums[low]`, then advance both `low` and `mid`.
   - Else if `nums[mid] == 1`, advance `mid` only.
   - Else (`nums[mid] == 2`), swap `nums[mid]` with `nums[high]`, then retreat `high` only (don't advance `mid` — recheck the swapped-in value).
3. `nums` is now sorted in-place.

---

# 6. Pseudocode

```text
low = 0
mid = 0
high = length(nums) - 1

while mid <= high
    if nums[mid] == 0
        swap(nums[mid], nums[low])
        low++
        mid++
    else if nums[mid] == 1
        mid++
    else
        swap(nums[mid], nums[high])
        high--
```

---

# 7. Python Solution

```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        low = 0
        mid = 0
        high = len(nums) - 1

        while mid <= high:
            if nums[mid] == 0:
                nums[mid], nums[low] = nums[low], nums[mid]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
```

---

# 8. Dry Run

Example:

```text
nums = [2,0,2,1,1,0]
Indices: 0 1 2 3 4 5
```

| Step | low,mid,high | nums[mid] | Action | Array State | Why? |
|------|--------------|-----------|--------|-------------|------|
| 1 | low=0, mid=0, high=5 | 2 | Swap nums[0],nums[5]; high=4 | [0,0,2,1,1,2] | mid sees 2, extend 2-zone, mid stays |
| 2 | low=0, mid=0, high=4 | 0 | Swap nums[0],nums[0] (no-op); low=1, mid=1 | [0,0,2,1,1,2] | mid sees 0, extend 0-zone |
| 3 | low=1, mid=1, high=4 | 0 | Swap nums[1],nums[1] (no-op); low=2, mid=2 | [0,0,2,1,1,2] | mid sees 0, extend 0-zone |
| 4 | low=2, mid=2, high=4 | 2 | Swap nums[2],nums[4]; high=3 | [0,0,1,1,2,2] | mid sees 2, extend 2-zone, mid stays |
| 5 | low=2, mid=2, high=3 | 1 | mid=3 | [0,0,1,1,2,2] | mid sees 1, already in place |
| 6 | low=2, mid=3, high=3 | 1 | mid=4 | [0,0,1,1,2,2] | mid sees 1, already in place |
| 7 | low=2, mid=4, high=3 | — | Stop | [0,0,1,1,2,2] | `mid <= high` is false |

Result: `[0,0,1,1,2,2]` — matches the expected output.

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `mid` scans the array exactly once, from `0` to `high`, and `high` only ever shrinks.
- Each index is classified at most a constant number of times (a `2`-swap re-examines the same `mid` position once more, but never revisits an already-finalized index).

### Space Complexity

```text
O(1)
```

Why?

- The array is sorted in-place using only the three pointers `low`, `mid`, and `high`.
- No additional arrays or data structures are allocated.
