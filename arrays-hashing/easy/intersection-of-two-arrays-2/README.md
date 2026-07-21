# Problem

Name: Intersection of Two Arrays II

Difficulty: Easy

----------------------------------------

# Pattern

Hash Dictionary


----------------------------------------

# Recognition

Idea
- Create hash dictionary and value its frequency count.
- Create in another list and append to res if count if available, if count down the frequency and iterate next

Steps

- COUNT: build `freq`, a dict mapping each value in `nums1` to how many times it appears
- SCAN: iterate `nums2`; whenever `n` is in `freq` with a remaining count > 0, append `n` to `res` and decrement `freq[n]`
- RETURN: `res`

----------------------------------------

# Complexity

- Time: `O(n + m)` — n = len(nums1) to build `freq`, m = len(nums2) to scan
- Space: `O(n)` — `freq` holds up to n distinct keys (output `res` not counted as extra space)
