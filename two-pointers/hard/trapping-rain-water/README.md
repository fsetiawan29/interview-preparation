# Problem: Trapping Rain Water

## 1. Problem Understanding

### Problem Summary

Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it is able to trap after raining.

### Input

- An integer array `height`

### Output

- The total units of water trapped.

### Constraints

- `n == height.length`
- `1 <= n <= 2 * 10^4`
- `0 <= height[i] <= 10^5`

### Example

Input:

```text
height = [0,1,0,2,1,0,1,3,2,1,2,1]
```

Output:

```text
6
```

Manual walkthrough:

```text
Original elevation map

[0,1,0,2,1,0,1,3,2,1,2,1]

Water above each bar is capped by the shorter of the tallest wall to its
left and the tallest wall to its right:

water[i] = min(leftMax[i], rightMax[i]) - height[i]

Summing water[i] across every position:

↓

6
```

---

# 2. Key Insight

## What makes this problem difficult?

The water trapped above any single position depends on the tallest wall to its left **and** the tallest wall to its right — a genuinely two-sided dependency. Computing both directly for every index is `O(n^2)` (brute force). Precomputing `leftMax` and `rightMax` arrays fixes that at `O(n)` time, but costs `O(n)` extra space for the two arrays.

## Key Observation

At any moment while scanning inward from both ends with running maxes `leftMax` and `rightMax`, **whichever side currently has the smaller running max has its water level already fully decided** — the opposite wall, wherever it ends up, is guaranteed to be at least as tall as the current running max on that side, so it can only help, never hurt. This means the water at that position doesn't need to wait for the true global right-max (or left-max) to be known.

Example:

```text
[0,1,0,2,1,0,1,3,2,1,2,1]
 ↑                       ↑
left                   right
leftMax=0              rightMax=1

leftMax(0) < rightMax(1) -> left's water level is decided:
whatever is further right, some wall >= rightMax(1) will always bound it
from that side, so min(leftMax, someFutureRightMax) = leftMax here.
```

## Why does this observation help?

Since the smaller-running-max side is already resolved, its pointer can be advanced immediately, water added on the fly, using the running max instead of a precomputed max array. Both `leftMax` and `rightMax` only ever need to track the tallest wall seen *so far* from each side, so the two precomputed arrays collapse into two scalars — turning `O(n)` space into `O(1)`.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture two hikers starting at opposite ends of the elevation map, each keeping a running tally of the tallest wall they've passed on their own side. At each step, whichever hiker has seen the *shorter* running-max wall is the one who moves — their side's water level is already locked in, since the other hiker's side is guaranteed at least as tall.

```text
[0,1,0,2,1,0,1,3,2,1,2,1]
 left                right
 leftMax=0           rightMax=1

leftMax < rightMax -> left hiker moves, water added using leftMax

[0,1,0,2,1,0,1,3,2,1,2,1]
   left              right
   leftMax=1         rightMax=1

leftMax not< rightMax -> right hiker moves instead

... continue until the hikers meet
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize left = 0, right = n - 1
leftMax = height[left], rightMax = height[right]
water = 0
   │
   ▼
Is left < right ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is leftMax < rightMax ?   Return water
   │
 ┌─┴────────┐
 │          │
Yes         No
 │          │
 ▼          ▼
left += 1              right -= 1
leftMax = max(leftMax, height[left])   rightMax = max(rightMax, height[right])
water += leftMax - height[left]        water += rightMax - height[right]
 │          │
 └────┬─────┘
      ▼
(back to "Is left < right ?")
```

Explanation of each decision:

- `leftMax` and `rightMax` are initialized from the two ends and only ever grow as their respective pointer advances.
- `leftMax < rightMax` means the left side's water level is safe to finalize now — some wall at least as tall as `rightMax` will always bound it from the right, so `min(leftMax, rightMax-or-taller) == leftMax`.
- Symmetrically, `rightMax <= leftMax` finalizes the right side's water using `rightMax`.
- Water added at each step is `runningMax - height[pointer]`, which is `0` (or positive) since `runningMax` already accounts for the current position.

---

# 5. Plain English Algorithm

1. Point `left` at index `0` and `right` at the last index. Set `leftMax = height[left]`, `rightMax = height[right]`, and `water = 0`.
2. While `left < right`:
   - If `leftMax < rightMax`: advance `left`, update `leftMax = max(leftMax, height[left])`, and add `leftMax - height[left]` to `water`.
   - Otherwise: retreat `right`, update `rightMax = max(rightMax, height[right])`, and add `rightMax - height[right]` to `water`.
3. Return `water`.

---

# 6. Pseudocode

```text
left = 0
right = length(height) - 1
leftMax = height[left]
rightMax = height[right]
water = 0

while left < right
    if leftMax < rightMax
        left++
        leftMax = max(leftMax, height[left])
        water += leftMax - height[left]
    else
        right--
        rightMax = max(rightMax, height[right])
        water += rightMax - height[right]

return water
```

---

# 7. Python Solution

```python
class Solution:
    def trap_twopointer(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1

        leftMax = height[left]
        rightMax = height[right]

        water = 0

        while left < right:
            if leftMax < rightMax:
                # leftMax is the smaller boundary.
                # min(leftMax, rightMax) = leftMax,
                # so the water at the current left index is finalized.
                left += 1
                leftMax = max(leftMax, height[left])
                water += leftMax - height[left]
            else:
                # rightMax <= leftMax, so it's safe to finalize the right side.
                right -= 1
                rightMax = max(rightMax, height[right])
                water += rightMax - height[right]

        return water
```

---

# 8. Dry Run

Example:

```text
height = [0,1,0,2,1,0,1,3,2,1,2,1]
Indices:  0 1 2 3 4 5 6 7 8 9 10 11
```

| Step | left,right | leftMax,rightMax | Compare | Action | water += | water |
|------|------------|-------------------|---------|--------|----------|-------|
| 1 | 0,11 | 0,1 | 0 < 1 | left=1, leftMax=max(0,1)=1 | 1-1=0 | 0 |
| 2 | 1,11 | 1,1 | 1 not< 1 | right=10, rightMax=max(1,2)=2 | 2-2=0 | 0 |
| 3 | 1,10 | 1,2 | 1 < 2 | left=2, leftMax=max(1,0)=1 | 1-0=1 | 1 |
| 4 | 2,10 | 1,2 | 1 < 2 | left=3, leftMax=max(1,2)=2 | 2-2=0 | 1 |
| 5 | 3,10 | 2,2 | 2 not< 2 | right=9, rightMax=max(2,1)=2 | 2-1=1 | 2 |
| 6 | 3,9 | 2,2 | 2 not< 2 | right=8, rightMax=max(2,2)=2 | 2-2=0 | 2 |
| 7 | 3,8 | 2,2 | 2 not< 2 | right=7, rightMax=max(2,3)=3 | 3-3=0 | 2 |
| 8 | 3,7 | 2,3 | 2 < 3 | left=4, leftMax=max(2,1)=2 | 2-1=1 | 3 |
| 9 | 4,7 | 2,3 | 2 < 3 | left=5, leftMax=max(2,0)=2 | 2-0=2 | 5 |
| 10 | 5,7 | 2,3 | 2 < 3 | left=6, leftMax=max(2,1)=2 | 2-1=1 | 6 |
| 11 | 6,7 | 2,3 | 2 < 3 | left=7, stop | — | 6 |

Result: `water = 6` — matches the expected output.

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `left` and `right` move toward each other and together cross the array at most once.
- Each iteration does constant work (one comparison, one max update, one addition).

### Space Complexity

```text
O(1)
```

Why?

- Only `left`, `right`, `leftMax`, `rightMax`, and `water` are tracked as extra state.
- No `leftMax`/`rightMax` arrays are allocated, unlike the prefix/suffix DP approach.
