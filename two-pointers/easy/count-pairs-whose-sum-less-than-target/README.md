# Problem: Count Pairs Whose Sum is Less than Target

## 1. Problem Understanding

### Problem Summary

Given a 0-indexed integer array `nums` and an integer `target`, count the number of pairs `(i, j)` where `0 <= i < j < len(nums)` and `nums[i] + nums[j] < target`.

### Input

- An integer array `nums`
- An integer `target`

### Output

- An integer — the total count of valid pairs.

### Constraints

- `1 <= nums.length <= 50`
- `-50 <= nums[i], target <= 50`

### Example

Input:

```text
nums = [-1,1,2,3,1], target = 2
```

Output:

```text
3
```

Manual walkthrough:

```text
Original

[-1,1,2,3,1], target = 2

Sort first

↓

[-1,1,1,2,3]

Check pairs, opposite ends, counting every valid pair
that a match unlocks in one shot:

-1 + 3 = 2, not < 2 -> shrink from the right
-1 + 2 = 1, < 2 -> valid! every index between left and right
                   also pairs with -1, so count 3 pairs at once
                   ((-1,1), (-1,1), (-1,2))

↓

3
```

---

# 2. Key Insight

## What makes this problem difficult?

Counting every pair with a nested loop is `O(n^2)`, and since we need a **count**, not just existence, it's tempting to think every valid pair must be found and tallied individually — which seems to require checking each one.

## Key Observation

Once `nums` is **sorted**, if `nums[left] + nums[right] < target`, then `nums[left]` paired with **any** index strictly between `left` and `right` is also `< target` — because every value in that range is `<= nums[right]`. That's `right - left` valid pairs discovered in a single comparison, not just one.

Example:

```text
[-1, 1, 1, 2, 3], target = 2
  ↑           ↑
left        right

nums[left] + nums[right] = -1 + 3 = 2, not valid

[-1, 1, 1, 2, 3]
  ↑        ↑
left     right

nums[left] + nums[right] = -1 + 2 = 1 < 2 -> valid, and every m with
left < m <= right also satisfies nums[left] + nums[m] < target,
since nums[m] <= nums[right]
```

## Why does this observation help?

Instead of counting one pair at a time, a valid comparison at the two ends lets us add `right - left` to the count in one step and advance `left` — collapsing what would be an inner loop into pure arithmetic.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture two readers on a sorted line. Whenever their sum is under `target`, every position between them (paired with the left reader's value) is *also* guaranteed to be under target — so instead of visiting each one, we just count how many there are and move the left reader inward to look for more.

```text
[-1, 1, 1, 2, 3], target = 2
 left                right

-1 + 3 = 2, not < target -> shrink right

[-1, 1, 1, 2, 3]
 left             right

-1 + 2 = 1 < target -> valid!
positions between left and right (exclusive of left): 3 of them
count += 3, left advances to chase new pairs
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Sort nums
Initialize left = 0, right = len(nums) - 1, count = 0
   │
   ▼
Is left < right ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
current_sum = nums[left] + nums[right]   Return count
   │
   ▼
Is current_sum < target ?
   │
 ┌─┴────────┐
 │          │
Yes         No
 │          │
 ▼          ▼
count += (right - left)   right -= 1
left += 1                 (sum too big, shrink it)
 │          │
 └────┬─────┘
      ▼
(back to "Is left < right ?")
```

Explanation of each decision:

- Sorting first is what guarantees "every value between `left` and `right` is `<= nums[right]`" — without it the shortcut wouldn't be valid.
- A valid sum adds `right - left` (the count of indices strictly between `left` and `right`, inclusive of `right`) to `count`, then advances `left` to search for further valid pairs.
- An invalid sum retreats `right`, since only a smaller value can bring the sum under `target`.

---

# 5. Plain English Algorithm

1. Sort `nums`.
2. Point `left` at the first index, `right` at the last index. Set `count = 0`.
3. While `left` is left of `right`:
   - Compute `current_sum = nums[left] + nums[right]`.
   - If `current_sum < target`, every index from `left + 1` to `right` also forms a valid pair with `left` — add `right - left` to `count`, then advance `left`.
   - Otherwise, retreat `right`.
4. Return `count`.

---

# 6. Pseudocode

```text
sort(nums)

left = 0
right = length(nums) - 1
count = 0

while left < right
    current_sum = nums[left] + nums[right]

    if current_sum < target
        count += (right - left)
        left++
    else
        right--

return count
```

---

# 7. Python Solution

```python
class Solution:
    def countPairs(self, nums: List[int], target: int) -> int:
        nums.sort()

        left = 0
        right = len(nums) - 1

        count = 0
        while left < right:
            current_sum = nums[left] + nums[right]

            if current_sum < target:
                count += right - left
                left += 1
            else:
                right -= 1

        return count
```

---

# 8. Dry Run

Example:

```text
nums = [-6,2,5,-2,-7,-1,3], target = -2
```

Sorted: `[-7,-6,-2,-1,2,3,5]`

| Step | Pointer(s) | Current Values | current_sum | Action | Why? |
|------|------------|-----------------|--------------|--------|------|
| 1 | left=0, right=6 | -7, 5 | -2 | Not < -2, right=5 | Sum equals target, not strictly less |
| 2 | left=0, right=5 | -7, 3 | -4 | Valid, count += 5, left=1 | -7 pairs with everything from index 1 to 5 |
| 3 | left=1, right=5 | -6, 3 | -3 | Valid, count += 4, left=2 | -6 pairs with everything from index 2 to 5 |
| 4 | left=2, right=5 | -2, 3 | 1 | Not < -2, right=4 | Sum too big |
| 5 | left=2, right=4 | -2, 2 | 0 | Not < -2, right=3 | Sum too big |
| 6 | left=2, right=3 | -2, -1 | -3 | Valid, count += 1, left=3 | Single pair |
| 7 | left=3, right=3 | — | — | Stop | `left < right` is false |

Result: `count = 5 + 4 + 1 = 10`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n log n)
```

Why?

- `n = len(nums)`; dominated by the sort.
- The two-pointer scan itself is `O(n)`, since `left` and `right` together cross the array once.

### Space Complexity

```text
O(1)
```

Why?

- Excluding whatever space the sort implementation uses internally, only `left`, `right`, and `count` are tracked.
