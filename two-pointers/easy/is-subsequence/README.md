# Problem

Name: Is Subsequence

Difficulty: Easy

----------------------------------------

# Pattern
Two Pointer


----------------------------------------

# Recognition

Idea
- Set `j` pointer as pointer of subsequence `s` string
- Set `i` pointer as pointer of `t` string
- If match then increase `j` pointer
- If `j` value is same as length `s` string, then it is a is subsequence

Mistakes
- Forget to add constraint for `j` pointer. if `j` value is greater and equal than len(s), then stop the process

Steps

- INIT: `i = 0` — pointer over `t`; `j = 0` — pointer over `s`
- LOOP: while `i < len(t) and j < len(s)` — stop once either string is exhausted
- CHECK: if `t[i] == s[j]` — `s[j]` found its match, so advance `j += 1`
- ADVANCE: `i += 1` — always move `t`'s pointer forward, matched or not
- RETURN: `j == len(s)` — every character of `s` was matched in order

----------------------------------------

# Complexity

- Time: `O(n)` — single pass over `t` (length `n`), `i` scans every element once
- Space: `O(1)` — only two pointers, no extra structures
