# Problem

Name: Merge Strings Alternately

Difficulty: Easy

----------------------------------------

# Pattern

Same-direction pointers

----------------------------------------

# Recognition

Idea
- First approach: use two pointer
    - Initialize both pointers at the beginning of their respective strings
    - Init `res` as array
    - While both pointers are within their valid ranges:
        - If the left pointer within its threshold
            - Append the current character(s) to the `res` result
            - increment the pointer
        - If the right pointer within its threshold,
            - Append the current character(s) to the `res` result
            - increment the pointer
    - Return the joined array as a string
- Second approach: use a single shared index
    - Init `res` as array
    - Find the max length as range for the loop
        - If `i` is within `word1`'s length, append `word1[i]` to `res`
        - If `i` is within `word2`'s length, append `word2[i]` to `res`
    - Return the joined array as a string

Steps

- Two-pointer approach
    - INIT: `res = []`, `i = 0`, `j = 0`
    - SCAN: while `i < len(word1) or j < len(word2)`
    - APPEND LEFT: if `i < len(word1)`, append `word1[i]` and `i += 1`
    - APPEND RIGHT: if `j < len(word2)`, append `word2[j]` and `j += 1`
    - RETURN: `"".join(res)`
- Single-shared-index approach
    - INIT: `res = []`
    - SCAN: `for i in range(max(len(word1), len(word2)))`
    - APPEND LEFT: if `i < len(word1)`, append `word1[i]`
    - APPEND RIGHT: if `i < len(word2)`, append `word2[i]`
    - RETURN: `"".join(res)`

----------------------------------------

# Complexity

- Two-pointer approach
    - Time: `O(n + m)` — n = len(word1), m = len(word2); each pointer advances once per matched char
    - Space: `O(n + m)` — `res` holds every character from both strings (excluding the output string itself, extra space is `O(1)`)
- Single-shared-index approach
    - Time: `O(max(n, m))` — n = len(word1), m = len(word2); one shared index bounded by the longer string
    - Space: `O(n + m)` — `res` holds every character from both strings (excluding the output string itself, extra space is `O(1)`)
