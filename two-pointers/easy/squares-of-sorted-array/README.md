# Problem

Name: Squares of a Sorted Array

Difficulty: Easy

----------------------------------------

# Pattern
Two Pointer as reader and Writer Pointer



----------------------------------------

# Recognition

Idea
- Compare `nums[left]` and `nums[right]` and write to another array

Mistakes
- There's no need to square the values for comparison; comparing their absolute values is sufficient
- Use left <= right instead of write > -1

Steps

- INIT: `left = 0`, `right = len(nums) - 1` — the read pointers; `write = len(nums) - 1` — the write pointer, filled from the back since the largest square is always at one of the two ends
- INIT: `result = [0] * len(nums)`
- LOOP: while `left <= right`
- CHECK: if `abs(nums[left]) >= abs(nums[right])` — the left end has the bigger magnitude
- WRITE: `result[write] = nums[left] * nums[left]`, then `left += 1`
- ELSE: the right end has the bigger magnitude — `result[write] = nums[right] * nums[right]`, then `right -= 1`
- ADVANCE: `write -= 1`
- RETURN: `result`

----------------------------------------

# Complexity

- Time: `O(n)` — single pass, `left` and `right` together cross the array once
- Space: `O(n)` — the `result` array (excluding the output itself, extra space is `O(1)`)
