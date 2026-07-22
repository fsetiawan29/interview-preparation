# Problem

Name: Maximum Sum of Distinct Subarrays With Length K

Difficulty: Medium

----------------------------------------

# Pattern
Fixed-Size Sliding Window + Frequency Count

----------------------------------------

# Recognition

Idea
- Slide a fixed-size window of size `k`, maintaining a running `window_sum` and a `freq` hash map of the counts of elements currently in the window
- The window has all-distinct elements exactly when `len(freq) == k` — every key in `freq` appears once, and there are `k` of them

Steps

- INIT: `left = 0`, `freq = {}`, `window_sum = 0`, `best_sum = 0`
- SCAN: for `right` in `range(len(nums))`
- EXPAND: increment `freq[nums[right]]`, add `nums[right]` to `window_sum`
- CHECK: once the window reaches size `k` (`right - left + 1 == k`)
  - if `len(freq) == k`, the window is all-distinct — update `best_sum = max(best_sum, window_sum)`
  - SLIDE: subtract `nums[left]` from `window_sum`, decrement `freq[nums[left]]` (deleting the key if it hits `0`), advance `left`
- RETURN: `best_sum`

Mistakes
- I initially used an array to store the sliding window and updated it with `append()` and `pop()`, which adds unnecessary overhead.
  - A more efficient approach is to maintain a running sum:
    - Add the incoming value: `window_sum += nums[right]`
    - Remove the outgoing value: `window_sum -= nums[left]`

- I used a `set` to check whether all elements in the window were distinct.
  - This does not work because a `set` cannot track duplicate counts.
  - Instead, use a frequency hash map to count the occurrences of each element.

- I forgot to remove elements from the frequency map when their count became `0`.
  - Always delete the key when its frequency reaches `0`.
  - This keeps the frequency map consistent, allowing `len(freq) == k` to correctly indicate that all `k` elements in the window are distinct.

----------------------------------------

# Complexity

- Time: `O(n)` — n = len(nums), one pass sliding the window across the array
- Space: `O(k)` — `freq` holds at most `k` entries, one per element currently in the window
