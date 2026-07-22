# Problem

Name: Ransom Note

Difficulty: Easy

----------------------------------------

# Pattern
Hash Map + Frequency Count

----------------------------------------

# Recognition

Idea
- Count the frequency of `magazine`
- Decrease the frequency of `ransomNote`
- If there's frequency of `ransomNote == -1`, `return False`
- Else `return True`


Steps

- GUARD: if `len(ransomNote) > len(magazine)`, return `False` — can't construct a longer note from a shorter magazine
- INIT: `freq` hash map to track character counts
- BUILD: for each `char` in `magazine`, increment `freq[char]`
- CONSUME: for each `char` in `ransomNote`, decrement `freq[char]`
- CHECK: if `freq[char] < 0`, return `False` — `ransomNote` needs more of `char` than `magazine` has
- RETURN: `True` if the loop finishes without running out of any character

Mistakes
- Forget to check longer first, because if `ransomNote` is longer, then it's impossible to construct it.
- Better to use `ransomNote < 0` because it's more robust and communicates the intent better.


----------------------------------------

# Complexity

- Time: `O(m + n)` — m = len(magazine), n = len(ransomNote), one pass to build `freq` and one pass to consume it
- Space: `O(k)` — k = number of distinct characters, bounded by the lowercase alphabet
