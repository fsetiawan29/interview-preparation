# Problem: Container With Most Water

## 1. Problem Understanding

### Problem Summary

Given an integer array `height` of length `n`, where the `i`-th element represents a vertical line at position `i` with height `height[i]`, find two lines that, together with the x-axis, form a container that holds the most water. Return the maximum amount of water the container can store.

### Input

- An integer array `height`

### Output

- The maximum area of water that can be contained between any two lines.

### Constraints

- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`

### Example

Input:

```text
height = [1,8,6,2,5,4,8,3,7]
```

Output:

```text
49
```

Manual walkthrough:

```text
Original

[1,8,6,2,5,4,8,3,7]

Try the widest container first (index 0 and index 8):

width = 8, height = min(1,7) = 1 -> area = 8

Move the shorter wall (index 0, height 1) inward:

width = 7, height = min(8,7) = 7 -> area = 49  (best so far)

Keep narrowing, always discarding the shorter wall,
tracking the largest area seen:

↓

49
```

---

# 2. Key Insight

## What makes this problem difficult?

Checking every pair of lines directly is `O(n^2)`. The area formula `width * min(height[left], height[right])` means both the width *and* the limiting (shorter) height shrink as the pointers move inward, so it isn't obvious which pointer to move without risking missing the true maximum.

## Key Observation

For any pair `(left, right)`, the water level is capped by the **shorter** of the two walls — the taller wall contributes nothing beyond that cap. Moving the *taller* wall inward can only shrink the width while the limiting height stays the same or gets worse, so it can never produce a bigger area. Moving the *shorter* wall inward is the only move that has a chance of increasing the limiting height, even though it shrinks the width.

Example:

```text
[1, 8, 6, 2, 5, 4, 8, 3, 7]
 ↑                       ↑
left                   right

height[left]=1 < height[right]=7 -> left is the shorter wall
moving left inward is the only move that could raise the limiting height
```

## Why does this observation help?

This turns the search into a greedy, single-pass, opposite-ends two-pointer scan: always discard the shorter wall. Every pair that could possibly beat the current best is still reachable this way, so no candidate is skipped, and the whole search finishes in `O(n)`.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture two vertical lines standing at opposite ends of the array, holding water between them like a container. The water level is always set by whichever line is shorter. Step the shorter line inward, one position at a time, recording the area at each stop, until the two lines meet.

```text
[1, 8, 6, 2, 5, 4, 8, 3, 7]
 left                  right

min(1,7)=1, width=8, area=8 -> shorter wall is left -> left moves in

[1, 8, 6, 2, 5, 4, 8, 3, 7]
    left               right

min(8,7)=7, width=7, area=49 -> shorter wall is right -> right moves in

... continue until left meets right, tracking the best area seen
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize left = 0, right = len(height) - 1, max_area = 0
   │
   ▼
Is left < right ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
width = right - left      Return max_area
area = width * min(height[left], height[right])
max_area = max(max_area, area)
   │
   ▼
Is height[left] < height[right] ?
   │
 ┌─┴────────┐
 │          │
Yes         No
 │          │
 ▼          ▼
left += 1   right -= 1
(left is shorter,   (right is shorter or equal,
 chase a taller      chase a taller left)
 right)
 │          │
 └────┬─────┘
      ▼
(back to "Is left < right ?")
```

Explanation of each decision:

- Every iteration computes and records the area for the current pair before deciding which pointer to move — no candidate is skipped.
- `height[left] < height[right]` means `left` is the shorter wall — it's advanced because that's the only move that could raise the limiting height.
- Otherwise `right` is the shorter wall (or the two are equal, in which case moving either is equivalent) — `right` is retreated.

---

# 5. Plain English Algorithm

1. Point `left` at index `0` and `right` at the last index. Set `max_area = 0`.
2. While `left` is left of `right`:
   - Compute `width = right - left` and `area = width * min(height[left], height[right])`.
   - Update `max_area` if `area` is bigger.
   - If `height[left] < height[right]`, advance `left`; otherwise retreat `right`.
3. Return `max_area`.

---

# 6. Pseudocode

```text
left = 0
right = length(height) - 1
max_area = 0

while left < right
    width = right - left
    area = width * min(height[left], height[right])
    max_area = max(max_area, area)

    if height[left] < height[right]
        left++
    else
        right--

return max_area
```

---

# 7. Python Solution

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        max_area = 0

        while left < right:
            width = right - left
            area = width * min(height[left], height[right])
            max_area = max(max_area, area)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_area
```

---

# 8. Dry Run

Example:

```text
height = [1,8,6,2,5,4,8,3,7]
Indices:  0 1 2 3 4 5 6 7 8
```

| Step | left,right (vals) | width | area | max_area | Action | Why? |
|------|--------------------|-------|------|----------|--------|------|
| 1 | left=0(1), right=8(7) | 8 | 8 | 8 | left=1 | height[left]=1 < height[right]=7 |
| 2 | left=1(8), right=8(7) | 7 | 49 | 49 | right=7 | height[left]=8 not < height[right]=7 |
| 3 | left=1(8), right=7(3) | 6 | 18 | 49 | right=6 | 8 not < 3 |
| 4 | left=1(8), right=6(8) | 5 | 40 | 49 | right=5 | 8 not < 8 |
| 5 | left=1(8), right=5(4) | 4 | 16 | 49 | right=4 | 8 not < 4 |
| 6 | left=1(8), right=4(5) | 3 | 15 | 49 | right=3 | 8 not < 5 |
| 7 | left=1(8), right=3(2) | 2 | 4 | 49 | right=2 | 8 not < 2 |
| 8 | left=1(8), right=2(6) | 1 | 6 | 49 | right=1, stop | 8 not < 6; `left<right` now false |

Result: `max_area = 49` — matches the expected output.

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `left` and `right` move toward each other and together cross the array at most once.
- Each iteration does constant work (one comparison, one area computation).

### Space Complexity

```text
O(1)
```

Why?

- Only `left`, `right`, and `max_area` are tracked as extra state.
- No auxiliary arrays or data structures are used.
