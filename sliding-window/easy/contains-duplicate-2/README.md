# Problem

Name: Contains Duplicate II

Difficulty: Easy

----------------------------------------

# Pattern
Fixed-Size Sliding Window (two approaches: Hash Set and Hash Map)

----------------------------------------

# Recognition

Idea
- There are two approaches to solve this problem, both keeping a window of size at most `k` and checking for a repeated value inside it.
    - Hash Set (`containsNearbyDuplicate_hashset`)
        - Initialize `window` as `set()`, `left = 0`.
        - Iterate `right` from `0` to `len(nums)` exclusive.
        - If `nums[right]` is already in `window`, `return True` — it's a duplicate within distance `k`.
        - Add `nums[right]` into `window`.
        - If `right - left == k`, the window has grown past size `k`, so remove `nums[left]` and advance `left`.
    - Hash Map (`containsNearbyDuplicate_hashmap`)
        - Handle `k == 0` up front by returning `False` (a window of size 0 can never contain a duplicate).
        - Set `right = min(k, len(nums) - 1)` so the initial window never runs past the end of `nums` when `k > len(nums)`.
        - Build `freq` (value -> count) for the initial window `nums[0..right]`; if any count reaches `2`, `return True`.
        - Slide the window one step at a time while `right < len(nums) - 1`:
            - Decrement `freq[nums[left]]`, deleting the key once it hits `0` so `freq` only ever holds values currently in the window.
            - Increment `freq[nums[right + 1]]`; if it reaches `2`, `return True`.
            - Advance `left` and `right`.
        - Return `False` if the loop finishes without finding a duplicate.

Steps

1. Pick a window representation (`set` for membership, `dict` for counts).
2. Grow/initialize the window up to size `k`.
3. Check for a duplicate as each element enters the window.
4. Shrink the window from the left once it exceeds size `k`.
5. Slide until the window reaches the end of `nums`.

Mistakes
- Forgot to handle the edge case `k == 0` in the hash map approach — must return `False` immediately.
- Forgot that `k` can exceed `len(nums)`; clamping with `right = min(k, len(nums) - 1)` avoids an out-of-range initial window.
- Forgot to delete a key from `freq` once its count drops to `0` — otherwise stale zero-count entries stick around.

----------------------------------------

# Complexity

- Time: `O(n)` — n = len(nums), each index enters and leaves the window at most once
- Space: `O(min(n, k))` — the set/map holds at most `k` elements at a time
