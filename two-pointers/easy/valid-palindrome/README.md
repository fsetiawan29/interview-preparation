# Problem

Name: Valid Palindrome

Difficulty: Easy

----------------------------------------

# Pattern

Two pointer from opposite both ends

----------------------------------------

# Recognition

Idea
- Use two pointer from left and right
- Use while logic condition, stop when left overlaps right position
- There are two approach to calculate the string
    - reformat with `isalnum()` and `lower()` function and with `"".join(word)` function
    - no need reformat, if not valid string, move the pointer

Steps

- Reformat approach
    - CLEAN: build `s_reformat` by keeping only `char.lower()` for chars where `char.isalnum()`
    - INIT: `left = 0`, `right = len(s_reformat) - 1`
    - SCAN: while `left < right`, compare `s_reformat[left]` vs `s_reformat[right]`; mismatch returns `False`
    - MOVE: `left += 1`, `right -= 1` each iteration
- No-reformat approach
    - INIT: `l = 0`, `r = len(s) - 1` on the original string
    - SKIP: while `l < r`, if `s[l]` isn't alnum, `l += 1` and `continue`; same for `s[r]` with `r -= 1`
    - COMPARE: once both sides land on alnum chars, compare `s[l].lower()` vs `s[r].lower()`; mismatch returns `False`
    - MOVE: `l += 1`, `r -= 1` after a successful compare

----------------------------------------

# Complexity

- Reformat approach
    - Time: `O(n)` — one pass to clean the string, one pass to compare pointers
    - Space: `O(n)` — `s_reformat` holds a copy of the cleaned string
- No-reformat approach
    - Time: `O(n)` — each pointer moves at most `n` times total across skips and compares
    - Space: `O(1)` — only `l` and `r` are tracked, no extra string built
