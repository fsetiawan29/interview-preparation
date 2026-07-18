# Problem

Name: Valid Anagram

Difficulty: Easy

----------------------------------------

# Pattern

Hash Table — Frequency counting

----------------------------------------

# Recognition

Idea
- Dictionary vs Counter
- Frequency counting

Steps

- SHAPE: Count frequency
- EARLY EXIT: if `len(s) != len(t)`, they can't be anagrams — return `False` immediately
- COUNT UP: iterate `s`, incrementing `freq[char]`
- COUNT DOWN: iterate `t`, decrementing `freq[char]` — same dict, opposite direction
- CHECK: if every count in `freq` is `0`, `s` and `t` have identical letter counts

----------------------------------------

# Complexity

- Time: `O(n)` — two linear passes over strings of length `n`, plus a linear pass over the frequency map
- Space: `O(n)` — frequency map holds up to `n` distinct characters

