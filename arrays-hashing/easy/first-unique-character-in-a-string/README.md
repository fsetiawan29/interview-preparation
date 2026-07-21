# Problem

Name: First Unique Character in a String

Difficulty: Easy

----------------------------------------

# Pattern
Hash Map + Frequency Count


----------------------------------------

# Recognition

Idea

- Count the frequency of each character using a hash map.
- Iterate through the string from left to right.
  - If the current character has a frequency of `1`, return its index.
- If no unique character exists, return `-1`.


Steps

- INIT: `freq` hash map to track character counts
- BUILD: for each `char` in `s`, increment `freq[char]`
- SCAN: for each `i, char` in `enumerate(s)`, if `freq[char] == 1`, return `i`
- RETURN: `-1` if no unique character was found

----------------------------------------

# Complexity

- Time: `O(n)` — n = len(s), one pass to build `freq` and one pass to scan `s`
- Space: `O(k)` — k = number of distinct characters, bounded by the lowercase alphabet
