# Problem

Name: Trapping Rain Water

Difficulty: Hard

----------------------------------------

# Pattern
Two Pointer (also: Brute Force, DP / Prefix-Suffix Max)

----------------------------------------

# Recognition

Idea
- Brute Force
    - Count including current `index` to find the max height
- Prefix & Suffix Maximum Arrays
    - formula: `water[i] = min(leftMax[i], rightMax[i]) - height[i]`
    - build array `leftMax`
    - build array `rightMax`
    - total it
- Two pointer
    - Water depends on `min(leftMax, rightMax)`
    - So 
        - `leftMax < rightMax`
            - process left
        - `rightMax <= leftMax`
            - process right


Steps

- Brute Force (`trap_bruteforce`)
  - SCAN: for each `i`, find `left_max` by scanning `height[0..i]` and
    `right_max` by scanning `height[i..n-1]`
  - ADD: `total_water += min(left_max, right_max) - height[i]`
- DP / Prefix-Suffix Max (`trap_dp`)
  - BUILD LEFT: `leftMax[i]` = tallest wall in `height[0..i]`, filled
    left to right (`leftMax[i] = max(leftMax[i-1], height[i])`)
  - BUILD RIGHT: `rightMax[i]` = tallest wall in `height[i..n-1]`, filled
    right to left (`rightMax[i] = max(rightMax[i+1], height[i])`)
  - SUM: for each `i`, `total += min(leftMax[i], rightMax[i]) - height[i]`
- Two Pointer (`trap_twopointer`)
  - INIT: `left = 0`, `right = n - 1`, `leftMax = height[left]`,
    `rightMax = height[right]`
  - COMPARE: while `left < right`, look at which side has the smaller
    running max — that side's water level is already decided, since the
    taller opposite wall can only help, never hurt, it
  - `leftMax < rightMax`: advance `left`, update
    `leftMax = max(leftMax, height[left])`, add `leftMax - height[left]`
  - `rightMax <= leftMax`: advance `right`, update
    `rightMax = max(rightMax, height[right])`, add
    `rightMax - height[right]`

Mistakes


----------------------------------------

# Complexity

- Brute Force: Time `O(n^2)` — for every index, rescan both directions
  to find `left_max`/`right_max`; Space `O(1)`
- DP / Prefix-Suffix Max: Time `O(n)` — one pass to build `leftMax`, one
  to build `rightMax`, one to sum; Space `O(n)` for the two arrays
- Two Pointer: Time `O(n)` — `left` and `right` each advance at most `n`
  times total; Space `O(1)` — only the two pointers and their running
  maxes are tracked, no extra arrays
