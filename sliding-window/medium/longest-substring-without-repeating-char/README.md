# Problem

Name: Longest Substring Without Repeating Characters

Difficulty: Medium

----------------------------------------

# Pattern
Sliding Window (variable-size) — Hash Set

----------------------------------------

# Recognition

Idea
- The window `[left, right]` always holds a substring with no repeated
  characters, tracked by a hash set of what's currently inside it.
- Expand `right` by one each step. If `s[right]` is already in the
  window, that's a duplicate — shrink from `left` (removing characters
  from the set) until the duplicate is gone, *then* add `s[right]`.
- The window is valid after every step, so the answer is just the max
  window size seen along the way.

Steps

- GUARD: if `s` is empty, return `0`
- INIT: `left = 0`, `best = 0`, `seen = set()`
- EXPAND: for `right` in `range(len(s))`
- SHRINK: while `s[right]` is in `seen`, remove `s[left]` from `seen` and
  advance `left` — keep shrinking until the incoming character no longer
  conflicts
- ADD: add `s[right]` to `seen` — the window `[left, right]` is now valid
- RECORD: `best = max(best, right - left + 1)`
- RETURN: `best`

Mistakes

- There's no need to initialize `right` to `1`.
  - Start both `left` and `right` at `0`.

- I incorrectly compared `left` and `right` to determine whether to remove elements.
  - Instead, while the current character is already in the `seen` set:
    - Remove `s[left]` from the set.
    - Advance `left`.
  - Once the duplicate is removed, add the current character to the set.

- I forgot to calculate the window length correctly.
  - The current window size is `right - left + 1`.
  - Update the longest length using:
    ```python
    longest = max(longest, right - left + 1)
    ```


----------------------------------------

# Complexity

- Time: `O(n)` — n = len(s); `left` and `right` each advance at most `n`
  times total across the whole loop, so the inner `while` doesn't add a
  nested-loop factor
- Space: `O(min(n, k))` — `seen` holds at most one of each character
  currently in the window, bounded by the string length or the alphabet
  size, whichever is smaller
