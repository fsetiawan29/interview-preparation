# Problem: Is Subsequence

## 1. Problem Understanding

### Problem Summary

Given two strings `s` and `t`, determine whether `s` is a subsequence of `t` — meaning every character of `s` appears in `t`, in the same relative order, but not necessarily consecutively.

### Input

- A string `s` (the candidate subsequence)
- A string `t` (the string to search within)

### Output

- `true` if `s` is a subsequence of `t`, `false` otherwise.

### Constraints

- `0 <= s.length <= 100`
- `0 <= t.length <= 10^4`
- `s` and `t` consist only of lowercase English letters.

### Example

Input:

```text
s = "abc", t = "ahbgdc"
```

Output:

```text
true
```

Manual walkthrough:

```text
s: a  b  c
t: a  h  b  g  d  c

Find 'a' in t -> position 0, matched
Find 'b' in t, searching after position 0 -> position 2, matched
Find 'c' in t, searching after position 2 -> position 5, matched

All characters of s found in order -> true
```

---

# 2. Key Insight

## What makes this problem difficult?

`s`'s characters don't need to be consecutive in `t`, so it's tempting to search for each character independently — but that risks re-matching an earlier position in `t`, which would break the "in order" requirement.

## Key Observation

Both strings only need to be scanned **once, left to right, together**. `t`'s pointer always advances every step; `s`'s pointer only advances when its current character is actually found at `t`'s current position.

Example:

```text
s = "abc"     t = "ahbgdc"
     ↑              ↑
     j              i

t[i]='a' == s[j]='a' -> match, j advances too
```

## Why does this observation help?

Because `t`'s pointer never goes backward, once a character of `s` is matched it's "consumed" and never revisited — a single synchronized pass is enough to verify the whole subsequence, with no need to search from scratch for each character of `s`.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture `i` walking through `t` one character at a time, always moving forward. `j` walks through `s`, but only takes a step whenever `i`'s current character happens to match what `j` is looking for.

```text
s: a  b  c          t: a  h  b  g  d  c
   ↑                     ↑
   j                     i

t[i]='a' matches s[j]='a' -> j advances, i advances

s: a  b  c          t: a  h  b  g  d  c
      ↑                     ↑
      j                     i

t[i]='h' doesn't match s[j]='b' -> only i advances

... continue until j reaches the end of s, or t runs out
```

If `j` ever reaches `len(s)`, every character was found in order — `s` is a subsequence of `t`.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize i = 0, j = 0
   │
   ▼
Is i < len(t) AND j < len(s) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is t[i] == s[j] ?     Return j == len(s)
 │
┌─┴────────┐
│          │
Yes        No
│          │
▼          │
j += 1     │
│          │
└────┬─────┘
     ▼
   i += 1
     │
     └──▶ (back to "Is i < len(t) AND j < len(s) ?")
```

Explanation of each decision:

- `i` always advances every iteration, matched or not — it's simply scanning forward through `t`.
- `j` only advances on a match — it represents how much of `s` has been confirmed so far.
- The loop stops early once `j` reaches `len(s)` isn't strictly necessary to check inside the loop; the `while` condition naturally exits when either string is exhausted, and the final check `j == len(s)` tells us which case happened.

---

# 5. Plain English Algorithm

1. Point `i` at the start of `t` and `j` at the start of `s`.
2. While both pointers are still within their strings:
   - If `t[i]` matches `s[j]`, advance `j` — that character of `s` is confirmed.
   - Always advance `i` — move forward through `t` regardless of a match.
3. Once the loop ends, `s` is a subsequence of `t` if and only if `j` reached `len(s)`.

---

# 6. Pseudocode

```text
i = 0
j = 0

while i < length(t) and j < length(s)
    if t[i] == s[j]
        j++

    i++

return j == length(s)
```

---

# 7. Python Solution

```python
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i = 0
        j = 0
        while i < len(t) and j < len(s):
            if t[i] == s[j]:
                j += 1

            i += 1

        return j == len(s)
```

---

# 8. Dry Run

Example:

```text
s = "axc", t = "ahbgdc"
```

| Step | Pointer(s) | Current Values | Action | Why? |
|------|------------|-----------------|--------|------|
| 1 | i=0, j=0 | t[0]='a', s[0]='a' | Match, j=1, i=1 | Characters equal |
| 2 | i=1, j=1 | t[1]='h', s[1]='x' | No match, i=2 | Characters differ |
| 3 | i=2, j=1 | t[2]='b', s[1]='x' | No match, i=3 | Characters differ |
| 4 | i=3, j=1 | t[3]='g', s[1]='x' | No match, i=4 | Characters differ |
| 5 | i=4, j=1 | t[4]='d', s[1]='x' | No match, i=5 | Characters differ |
| 6 | i=5, j=1 | t[5]='c', s[1]='x' | No match, i=6 | Characters differ |
| 7 | i=6, j=1 | — | Stop | `i < len(t)` is false |

Result: `j=1 != len(s)=3` → `false`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(t)`; `i` scans every character of `t` at most once.
- `j` never exceeds `len(s)`, and never moves backward.

### Space Complexity

```text
O(1)
```

Why?

- Only two pointers, `i` and `j`, are used — no extra structures.
