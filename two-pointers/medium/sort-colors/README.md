# Problem

Name: Sort Colors

Difficulty: Medium

----------------------------------------

# Pattern
Use Three Pointer



----------------------------------------

# Recognition

Idea
- Use three pointer. `low`, `mid`, `high` pointer
- Use `mid` to check its, position, does it swap with low, swap with high, or just advance the mid


Steps

- INIT: `low = 0`, `mid = 0`, `high = len(nums) - 1`
- SCAN: while `mid <= high`
- ZERO: if `nums[mid] == 0`, swap `nums[mid]` with `nums[low]`, advance both `low` and `mid`
- ONE: elif `nums[mid] == 1`, it's already in place — advance `mid` only
- TWO: else (`nums[mid] == 2`), swap `nums[mid]` with `nums[high]`, decrement `high` only — don't advance `mid`, since the swapped-in value still needs to be checked

----------------------------------------

# Complexity

- Time: `O(n)` — single pass, each index is visited at most once by `mid` (swaps with `high` don't re-visit already-processed indices)
- Space: `O(1)` — sorted in-place with three pointers, no extra data structures
