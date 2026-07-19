# Problem

Name: Intersection of Two Arrays

Difficulty: Easy

----------------------------------------

# Pattern

Hash Set

----------------------------------------

# Recognition

Idea
- Because only want to get intersection number and unique, use set from nums1 and check in nums2

Steps

- CONVERT: `nums1` to a set (`seen`) — dedupes and gives O(1) membership checks
- SCAN: iterate `nums2`, and whenever `n in seen`, add `n` to the result set `res` — using a set here dedupes matches from `nums2`'s side too
- RETURN: `list(res)`

----------------------------------------

# Complexity

- Time: `O(n + m)` — n = len(nums1) to build the set, m = len(nums2) to scan
- Space: `O(n + m)` worst case — `seen` holds up to n elements, `res` holds up to min(n, m) elements
