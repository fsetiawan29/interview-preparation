# Problem

Name: Isomorphic Strings

Difficulty: Easy

----------------------------------------

# Pattern

Hash Map

----------------------------------------

# Recognition

Idea
- Use two hash map to check consistency character only map to one character

Steps

- INIT: two maps, `s_to_t` and `t_to_s`, to track the mapping in both directions
- SCAN: for each index `i`, if `s[i]` is already mapped to something other than `t[i]`, or `t[i]` is already mapped to something other than `s[i]`, return `False` — this catches both "one char maps to two different chars" and "two chars map to the same char"
- RECORD: otherwise set `s_to_t[s[i]] = t[i]` and `t_to_s[t[i]] = s[i]`
- RETURN: `True` if no conflict was found across the whole string

----------------------------------------

# Complexity

- Time: `O(n)` — n = len(s), single pass over both strings
- Space: `O(k)` — k = number of distinct characters, bounded by the ASCII alphabet
