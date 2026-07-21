# Problem

Name: Word Pattern

Difficulty: Easy

----------------------------------------

# Pattern

Hash Map

----------------------------------------

# Recognition

Idea
- Check the length is same between pattern and s because there's no constraint about that
- If char in mapping then should check the value of mapping is same as word
- Else should check if word in seen then return False
    - If not in seen then create new dictionary and add seen

Steps

- SPLIT: `s.split()` into `words`; if `len(pattern) != len(words)`, return `False` immediately (no bijection possible)
- INIT: `mapping` (char -> word) and `seen` (set of words already mapped to some char)
- SCAN: zip `pattern` and `words` together; for each `(char, word)`:
  - if `char` already in `mapping`, it must map to this same `word`, else return `False`
  - otherwise, `word` must not already be in `seen` (would mean another char claimed it), else return `False` — then record `mapping[char] = word` and add `word` to `seen`
- RETURN: `True` if no conflict was found across the whole pattern

----------------------------------------

# Complexity

- Time: `O(n + m)` — n = len(pattern)/len(words) for the scan, m = total length of `s` for the split
- Space: `O(k)` — k = number of distinct characters/words, for `mapping` and `seen`
