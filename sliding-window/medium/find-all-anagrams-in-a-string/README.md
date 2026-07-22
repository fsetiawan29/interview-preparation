# Problem

Name: Find All Anagrams in a String

Difficulty: Medium

----------------------------------------

# Pattern
Fixed-Size Sliding Window + Frequency Count

----------------------------------------

# Recognition

Idea
- Slide a fixed-size window of size `len(p)`, maintaining a `window_freq` hash map of the counts of characters currently in the window
- The window is an anagram of `p` exactly when `window_freq == freq_p` — both maps have the same characters with the same counts
- If `len(p) > len(s)`, no anagram can fit, so return `[]` immediately

Steps

- EDGE CASE: if `len(p) > len(s)`, return `[]`
- INIT: `left = 0`, `right = len(p) - 1`, build `freq_p` from all of `p`, and `window_freq` from `s`'s first window `s[:len(p)]`
- SCAN: while `right < len(s)`
- CHECK: if `window_freq == freq_p`, append `left` to `res`
- STOP: if `right` is the last index, break
- SLIDE: decrement `window_freq[s[left]]` (deleting the key if it hits `0`), increment `window_freq[s[right + 1]]`, advance both `left` and `right`
- RETURN: `res`

Mistakes
- No need to check `len(s) == 0` because constraint problem guarantee it
- We can use `==` comparison to compare both hash map in python but if it has `key: 0`, should be removed because the comparison should broken


----------------------------------------

# Complexity

- Time: `O(n)` — n = len(s), one pass sliding the window across the string; each `==` comparison between maps is `O(26)` (bounded alphabet), not `O(n)`
- Space: `O(1)` — `freq_p` and `window_freq` hold at most 26 lowercase-letter keys each, independent of input size
