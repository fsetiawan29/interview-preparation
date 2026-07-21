# Problem

Name: Container With Most Water

Difficulty: Medium

----------------------------------------

# Pattern

Two Pointer + Greedy

----------------------------------------

# Recognition

Idea
- To get the result, we need to calculate area = width * min(height_left, height_right).
- This problem use two pointers because we need to pick left and right ends and move pointer to find maximum height.
- This problem is greedy because we discard the shorter wall. We don't look ahead, trackback, or try both possibilities. A local optimal choice that is guaranteed to preserve the possibility of finding the global optimum.

Steps

- INIT: `left = 0`, `right = len(height) - 1`, `max_area = 0`
- SCAN: while `left < right`, compute `width = right - left` and `area = width * min(height[left], height[right])`
- TRACK: update `max_area = max(max_area, area)`
- NARROW: move whichever pointer points at the shorter wall (`left += 1` if `height[left] < height[right]`, else `right -= 1`) — moving the taller wall can only shrink the width without ever increasing the limiting height

----------------------------------------

# Complexity

- Time: `O(n)` — each pointer moves at most `n` times total, single pass
- Space: `O(1)` — only `left`, `right`, and `max_area` are tracked, no extra structures
