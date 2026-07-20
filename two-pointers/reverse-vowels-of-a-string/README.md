# Problem

Name: Reverse Vowels of a String

Difficulty: Easy

----------------------------------------

# Pattern
Two Pointer - Check if vowel or not 



----------------------------------------

# Recognition

Idea
- Two pointer from most left and right
- Check `char.lower()` is vowel or not by creating set of vowel
- If we are in the `left` pointer and `char[left]`, then move the left pointer by increase it
- If we are in the `right` pointer and `char[right]`, then move the right pointer by decrease it


Steps

- INIT: `vowels = {'a', 'e', 'i', 'o', 'u'}`, `l = 0`, `r = len(s) - 1`, `s_array = list(s)`
- SCAN: while `l < r`
- SKIP LEFT: if `s_array[l].lower()` not in `vowels`, `l += 1` and `continue`
- SKIP RIGHT: if `s_array[r].lower()` not in `vowels`, `r -= 1` and `continue`
- SWAP: both `l` and `r` point at vowels — swap `s_array[l]` and `s_array[r]`, then `l += 1`, `r -= 1`
- RETURN: `"".join(s_array)`

----------------------------------------

# Complexity

- Time: `O(n)` — each pointer moves at most `n` positions total, single pass
- Space: `O(n)` — `s` is immutable, so it's copied into `s_array` to allow in-place swaps (excluding the output string, extra space for the two pointers is `O(1)`)
