# Problem

Name: Count Pairs Whose Sum is Less than Target

Difficulty: Easy

----------------------------------------

# Pattern
Two Pointer (sort + opposite ends)

----------------------------------------

# Recognition

Idea
- Sort `nums` first so the two-pointer trick applies
- If `nums[left] + nums[right] < target`, then every index between `left` and `right` also pairs with `left` to stay under `target` (since the array is sorted, any `nums[m]` with `left < m <= right` is `<= nums[right]`) — that's `right - left` valid pairs in one shot, so advance `left`
- Otherwise the sum is too big — decrease `right` to try a smaller value

Steps

- SORT: sort `nums` in place
- INIT: `left = 0`, `right = len(nums) - 1`, `count = 0`
- SCAN: while `left < right`
- CHECK: compute `current_sum = nums[left] + nums[right]`
- VALID: if `current_sum < target`, every pair `(left, m)` for `m` in `left+1..right` is valid — add `right - left` to `count`, advance `left`
- INVALID: else, decrement `right`
- RETURN: `count`

Mistakes:
- I forgot how to count other pair values other than your pair which means `count = right - (left+1) + 1`
- If less than target, advance `i`
- Else decrease `j`


----------------------------------------

# Complexity

- Time: `O(n log n)` — n = len(nums), dominated by the sort; the two-pointer scan itself is `O(n)`
- Space: `O(1)` extra — excluding the space used by the sort itself, only two pointers and a running `count` are needed
