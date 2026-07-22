# Problem

Name: Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold

Difficulty: Medium

----------------------------------------

# Pattern
Fixed-Size Sliding Window


----------------------------------------

# Recognition

Idea

- Avoid floating-point division: instead of checking `window_sum / k >= threshold`, compare `window_sum >= k * threshold` (`limit`) — same comparison, no division per window
- Slide a fixed-size window of size `k` and count how many windows meet `limit`

Steps

- INIT: `left = 0`, `right = k - 1`, `window_sum = sum(arr[:k])`, `limit = k * threshold`, `count = 0`
- SCAN: while `right < len(arr)`
- CHECK: if `window_sum >= limit`, increment `count`
- STOP: if `right` is the last index, break
- SLIDE: subtract `arr[left]`, add `arr[right + 1]` to `window_sum`, advance both `left` and `right`
- RETURN: `count`

----------------------------------------

# Complexity

- Time: `O(n)` — n = len(arr), one pass sliding the window across the array
- Space: `O(1)` — only a running `window_sum` and two pointers, no extra data structures
