# Problem

Name: Two Sum Less Than K

Difficulty: Easy

----------------------------------------

# Statement

Given an array `nums` of integers and an integer `k`, return the maximum sum such that there exists `i < j` with `nums[i] + nums[j] == sum` and `sum < k`. If no `i, j` exist satisfying this equation, return `-1`.

## Examples

**Example 1:**

```
Input: nums = [34,23,1,24,75,33,54,8], k = 60
Output: 58
Explanation: We can use 34 and 24 to sum 58 which is less than 60.
```

**Example 2:**

```
Input: nums = [10,20,30], k = 15
Output: -1
Explanation: In this case it is not possible to get a pair sum less than 15.
```

## Constraints

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 1000`
- `1 <= k <= 2000`

----------------------------------------

# Pattern
Two Pointer (sort + opposite ends)

----------------------------------------

# Recognition

Idea
- Sort `nums` first — the array isn't sorted going in, but once sorted, the classic two-pointer trick applies
- Use `left`/`right` pointers from opposite ends: if the pair sum is `< k`, it's a valid candidate — record it and move `left` right to try a larger sum; otherwise move `right` left to shrink the sum

Steps

- SORT: sort `nums` in place
- INIT: `left = 0`, `right = len(nums) - 1`, `max_sum = -1`
- SCAN: while `left < right`
- CHECK: compute `current_sum = nums[left] + nums[right]`
- VALID: if `current_sum < k`, update `max_sum = max(max_sum, current_sum)` and advance `left` — try to find a bigger valid sum
- INVALID: else, decrement `right` — the sum is too big, need a smaller value
- RETURN: `max_sum` (`-1` if no valid pair was found)

Mistakes
- Forget to solve this need to sort first
- Because it's already sorted, then can add from opposite both end pointer



----------------------------------------

# Complexity

- Time: `O(n log n)` — n = len(nums), dominated by the sort; the two-pointer scan itself is `O(n)`
- Space: `O(1)` extra — excluding the space used by the sort itself, only two pointers and a running `max_sum` are needed
