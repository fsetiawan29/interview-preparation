# Problem

Name: Reverse String

Difficulty: Easy

----------------------------------------

# Pattern

Two pointer: Initialize two pointers at both ends of the array.

----------------------------------------

# Recognition

Idea
- Place pointer both start and end of array
- Iterate and change position

Steps

- INIT: `l = 0`, `r = len(s) - 1`
- SCAN: while `l < r`, swap `s[l]` and `s[r]` in place
- MOVE: `l += 1`, `r -= 1` each iteration
- RETURN: nothing — `s` is mutated in place

----------------------------------------

# Complexity

- Time: `O(n)` — each pointer moves at most `n / 2` times, single pass
- Space: `O(1)` — swapped in place, no extra structures
