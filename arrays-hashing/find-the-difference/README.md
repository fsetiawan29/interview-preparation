# Problem

Name: Find the Difference

Difficulty: Easy

----------------------------------------

# Pattern
Hash Dictionary + Frequency Count


----------------------------------------

# Recognition

Idea
- Create `freq` hash dictionary with the value is count frequency
- Return `char` if not found in dictionary
- Decrease the count if found in dictionary
- Check `if count == 0`, then return the `char`

Steps

- INIT: `freq` hash map to track character counts
- BUILD: for each `char` in `s`, increment `freq[char]`
- SCAN: for each `char` in `t`, if `char not in freq` or `freq[char] == 0`, return `char` — this is the added letter
- DECREMENT: otherwise decrease `freq[char]` by 1 and continue

----------------------------------------

# Complexity

- Time: `O(n)` — n = len(t), one pass to build `freq` from `s` and one pass to scan `t`
- Space: `O(k)` — k = number of distinct characters, bounded by the lowercase alphabet
