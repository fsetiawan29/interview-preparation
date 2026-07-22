# Problem

Name: Maximum Average Subarray I

Difficulty: Easy

----------------------------------------

# Pattern
Fixed-Size Sliding Window

----------------------------------------

# Recognition

Idea 

- Initialize the sliding window with:
  - `left = 0`
  - `right = k - 1` because `right` represents the last index of a window with size `k`.
- Compute the initial window sum using `sum(nums[:k])`, where `k` is exclusive in Python slicing.
- Initialize `best = window_sum`, tracking the best **sum** rather than the best average.
- Slide the window until `right` reaches the end of the array:
  - Update `best` if the current `window_sum` is larger.
  - If `right` is already at the last index, stop.
  - Otherwise:
    - Remove `nums[left]` from `window_sum`.
    - Add `nums[right + 1]` to `window_sum`.
    - Advance both `left` and `right`.
- Return `best / k`, dividing by `k` only once at the end instead of on every iteration.

Steps

1. Compute the sum of the first window.
2. Initialize the best window sum.
3. Slide the window one position at a time.
4. Update the window sum and best sum seen so far.
5. Return the best sum divided by `k`.

Mistakes

- I found it difficult to decide whether the loop condition should be `right < len(nums)`.
- A good rule of thumb is:
  - When working with array indices, use `index < len(nums)` instead of `<=`.
  - This ensures the index always stays within the valid range.



----------------------------------------

# Complexity

- Time: `O(n)` — n = len(nums), one pass sliding the window across the array
- Space: `O(1)` — only a running `window_sum` and two pointers, no extra data structures
