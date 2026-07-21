# Problem

Name: Two Sum II - Input Array Is Sorted

Difficulty: Medium

----------------------------------------

# Pattern

Two Pointer

----------------------------------------

# Recognition

Idea
- This problem is similar to the Two Sum hash map (complement lookup) approach. However, since the array is already sorted and the problem requires O(1) extra space, the optimal solution is to use the two-pointer technique.
- Initialize two pointers, one at each end of the array:
    - If the sum of the two values equals the target, return their indices.
    - If the sum is greater than the target, move the right pointer one step to the left
    - Otherwise, move the left pointer one step to the right.

Steps

- INIT: `left = 0`, `right = len(numbers) - 1`
- SCAN: while `left < right`, compute `candidate = numbers[left] + numbers[right]`
- MATCH: if `candidate == target`, return `[left + 1, right + 1]` (1-indexed)
- NARROW: if `candidate > target`, decrement `right`; otherwise increment `left`

----------------------------------------

# Complexity

- Time: `O(n)` — each pointer moves at most `n` times total, single pass
- Space: `O(1)` — only `left` and `right` are tracked, no extra structures
