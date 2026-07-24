# Problem: Two Sum Less Than K

## 1. Problem Understanding

### Problem Summary

Given an array of integers `nums` and an integer `k`, find two different indices `i < j` such that `nums[i] + nums[j] < k`, and return the **maximum possible sum** among all such pairs. If no such pair exists, return `-1`.

### Input

- An integer array `nums`
- An integer `k`

### Output

- The maximum sum of a pair strictly less than `k`, or `-1` if no valid pair exists.

### Constraints

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 1000`
- `1 <= k <= 2000`

### Example

Input:

```text
nums = [34,23,1,24,75,33,54,8], k = 60
```

Output:

```text
58
```

Manual walkthrough:

```text
Original

[34,23,1,24,75,33,54,8], k = 60

Sort first

↓

[1,8,23,24,33,34,54,75]

Try pairs from opposite ends, keeping only sums < 60,
tracking the largest one seen:

34 + 24 = 58 < 60 -> candidate, best so far

↓

58
```

---

## 2. Brute Force Approach

### Idea

Check every pair of indices directly, keeping the largest sum found that's still under `k`.

### Pseudocode

```text
n = length(nums)
max_sum = -1

for i = 0 to n - 1
    for j = i + 1 to n - 1
        if nums[i] + nums[j] < k
            max_sum = max(max_sum, nums[i] + nums[j])

return max_sum
```

### Complexity Analysis

#### Time Complexity

```text
O(n^2)
```

Why?

- There are `O(n^2)` pairs `(i, j)` with `i < j`, each checked in `O(1)`.

#### Space Complexity

```text
O(1)
```

Why?

- Only `max_sum` and the two loop indices are used.

### Why this isn't good enough

Every pair is checked individually, with no way to steer the search toward bigger valid sums. Sorting first makes pointer movement predictable — advancing `left` can only grow the sum, retreating `right` can only shrink it — so a single opposite-ends scan can chase the maximum valid sum directly instead of trying every pair.

---

## 3. Key Insight

### What makes this problem difficult?

Checking every pair directly is `O(n^2)`, and simply looking for *any* valid pair isn't enough — we specifically need the **largest** sum under `k`, so the search has to be steered toward bigger sums without missing the true maximum.

### Key Observation

Once `nums` is **sorted**, a pair's sum only moves in one predictable direction when a pointer moves: shifting the left pointer right increases the sum, shifting the right pointer left decreases it. That means a classic opposite-ends two-pointer scan can be steered directly by whether the current sum is valid or not.

Example:

```text
[1, 8, 23, 24, 33, 34, 54, 75], k = 60
 ↑                            ↑
left                        right

nums[left] + nums[right] = 1 + 75 = 76 >= 60 -> too big, need a smaller sum
```

### Why does this observation help?

If the current pair's sum is `< k`, it's a valid candidate — record it, then push `left` forward to *try for an even bigger* valid sum (moving `right` instead could only make the sum smaller, never bigger, so it would waste the opportunity). If the sum is `>= k`, the only way to shrink it is to pull `right` left.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture two readers on a sorted line, starting at opposite ends. Whenever their combined value is a legal (under-`k`) sum, the left reader steps inward to chase an even bigger legal sum. Whenever it's too big, the right reader steps inward to bring the sum down.

```text
[1, 8, 23, 24, 33, 34, 54, 75], k = 60
 left                        right

1 + 75 = 76, too big -> right moves left

[1, 8, 23, 24, 33, 34, 54, 75]
 left                     right

1 + 54 = 55, valid! record 55, chase bigger -> left moves right

[1, 8, 23, 24, 33, 34, 54, 75]
    left                  right

8 + 54 = 62, too big -> right moves left

... continue until left meets right
```

Every valid sum encountered along the way is compared against the running best.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Sort nums
Initialize left = 0, right = len(nums) - 1, max_sum = -1
   │
   ▼
Is left < right ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
current_sum = nums[left] + nums[right]   Return max_sum
   │
   ▼
Is current_sum < k ?
   │
 ┌─┴────────┐
 │          │
Yes         No
 │          │
 ▼          ▼
max_sum = max(max_sum, current_sum)   right -= 1
left += 1                             (sum too big, shrink it)
 │          │
 └────┬─────┘
      ▼
(back to "Is left < right ?")
```

Explanation of each decision:

- Sorting first is what makes the pointer movement predictable — without it, moving a pointer wouldn't reliably increase or decrease the sum.
- A valid sum (`< k`) advances `left`, since that's the only direction that can produce a *bigger* valid sum next.
- An invalid sum (`>= k`) retreats `right`, since that's the only direction that can shrink the sum.

---

## 6. Plain English Algorithm

1. Sort `nums`.
2. Point `left` at the first index and `right` at the last index. Set `max_sum = -1`.
3. While `left` is left of `right`:
   - Compute `current_sum = nums[left] + nums[right]`.
   - If `current_sum < k`, it's a valid candidate — update `max_sum` if it's bigger, then advance `left` to look for a larger valid sum.
   - Otherwise, the sum is too big — retreat `right` to shrink it.
4. Return `max_sum`.

---

## 7. Pseudocode

```text
sort(nums)

left = 0
right = length(nums) - 1
max_sum = -1

while left < right
    current_sum = nums[left] + nums[right]

    if current_sum < k
        max_sum = max(max_sum, current_sum)
        left++
    else
        right--

return max_sum
```

---

## 8. Python Solution

```python
class Solution:
    def twoSumLessThanK(self, nums: List[int], k: int) -> int:
        nums.sort()
        left = 0
        right = len(nums) - 1

        max_sum = -1

        while left < right:
            current_sum = nums[left] + nums[right]
            if current_sum < k:
                max_sum = max(max_sum, current_sum)
                left += 1
            else:
                right -= 1

        return max_sum
```

---

## 9. Dry Run

Example:

```text
nums = [10,20,30], k = 15
```

Sorted: `[10,20,30]`

| Step | Pointer(s) | Current Values | current_sum | Action | Why? |
|------|------------|-----------------|--------------|--------|------|
| 1 | left=0, right=2 | 10, 30 | 40 | 40 >= 15, right=1 | Sum too big |
| 2 | left=0, right=1 | 10, 20 | 30 | 30 >= 15, right=0 | Sum too big |
| 3 | left=0, right=0 | — | — | Stop | `left < right` is false |

Result: `max_sum = -1` (no valid pair found)

---

## 10. Complexity Analysis

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

- Excluding whatever space the sort implementation uses internally, only `left`, `right`, and `max_sum` are tracked.
