# Problem

Name: Longest Palindrome

Difficulty: Easy

----------------------------------------

# Pattern
Hash Map + Frequency Count



----------------------------------------

# Recognition

Idea

- The general rule is
    - If count character is even, use all of it
    - If count is odd, use the largest even part, which means `(count // 2) * 2`
    - If any character has an odd count, add exactly `+1` as the center


Steps

- INIT: `freq` hash map to track character counts
- BUILD: for each `char` in `s`, increment `freq[char]`
- SCAN: for each `char, count` in `freq.items()`
  - if `count` is even, add the full `count` to `result`
  - if `count` is odd, add `count - 1` to `result` and mark `has_odd = True`
- CENTER: if `has_odd`, add `+1` to `result` for a single odd-count char as the center
- RETURN: `result`

----------------------------------------

# Complexity

- Time: `O(n)` — n = len(s), one pass to build `freq` and one pass over the distinct characters
- Space: `O(k)` — k = number of distinct characters, bounded by the lowercase + uppercase alphabet
