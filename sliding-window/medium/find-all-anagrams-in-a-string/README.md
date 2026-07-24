# Problem: Find All Anagrams in a String

## 1. Problem Understanding

### Problem Summary

Given two strings `s` and `p`, find all the start indices of `p`'s anagrams in `s`. The order of the output does not matter.

### Input

- A string `s`
- A string `p`

### Output

- A list of integers: every start index in `s` where a substring of length `len(p)` is an anagram of `p`.

### Constraints

- `1 <= s.length, p.length <= 3 * 10^4`
- `s` and `p` consist of lowercase English letters.

### Example

Input:

```text
s = "cbaebabacd", p = "abc"
```

Output:

```text
[0,6]
```

Explanation: The substring with start index = 0 is "cba", which is an anagram of "abc". The substring with start index = 6 is "bac", which is an anagram of "abc".

Manual walkthrough:

```text
s: c  b  a  e  b  a  b  a  c  d
p: a  b  c

window at 0: "cba" -> letters {c,b,a} match p's {a,b,c} -> anagram, record 0
window at 6: "bac" -> letters {b,a,c} match p's {a,b,c} -> anagram, record 6

-> [0, 6]
```

---

# 2. Key Insight

## What makes this problem difficult?

Checking every window of length `len(p)` by sorting or rebuilding a frequency count from scratch is `O(n * m)` (`m = len(p)`) — too slow when both lengths can reach `3 * 10^4`. Also, "anagram" means same letters with the same counts, not same order, so a direct substring comparison doesn't work.

## Key Observation

A window is an anagram of `p` exactly when its letter-frequency map equals `p`'s letter-frequency map. Since the window has fixed size `len(p)`, sliding it by one only removes one letter's count and adds another's — the frequency map can be updated incrementally instead of rebuilt.

Example:

```text
p = "abc"          freq_p = {a:1, b:1, c:1}
window "cba"        window_freq = {c:1, b:1, a:1}  -> equal to freq_p -> anagram
```

## Why does this observation help?

Dictionary equality (`window_freq == freq_p`) does the "is this an anagram" check in `O(26)` (bounded alphabet) instead of `O(m log m)` for sorting each window. Combined with `O(1)` incremental updates per slide, the whole scan stays `O(n)`.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture a window of fixed width `len(p)` sliding across `s`, carrying a tally of the letters currently inside it. At every position, that tally is compared against `p`'s own tally — a match means the window is a rearrangement of `p`.

```text
s:  c  b  a  e  b  a  b  a  c  d
   [-------]
   window_freq = {c:1, b:1, a:1}  == freq_p = {a:1, b:1, c:1}  -> match, record index 0

slide ->

s:  c  b  a  e  b  a  b  a  c  d
       [-------]
   window_freq = {b:1, a:1, e:1}  != freq_p                    -> no match
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Is len(p) > len(s) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return []        Build freq_p from p
                 Build window_freq from s[0..len(p)-1]
                 left = 0, right = len(p) - 1, res = []
                       │
                       ▼
                 Is right < len(s) ?
                       │
                    ┌─┴─────────┐
                    │           │
                   Yes          No
                    │           │
                    ▼           ▼
             window_freq == freq_p ?    Return res
                    │
                 ┌─┴───────┐
                 │         │
                Yes        No
                 │         │
                 ▼         ▼
          res.append(left) (continue)
                 │         │
                 └────┬────┘
                      ▼
              Is right == len(s) - 1 ?
                      │
                   ┌─┴───────┐
                  Yes        No
                   │         │
                   ▼         ▼
                 break   Slide: remove s[left], add s[right+1]
                         left += 1, right += 1
                         │
                         └──▶ (back to "Is right < len(s) ?")
```

Explanation of each decision:

- `len(p) > len(s)` is checked up front because no window of that size could even exist.
- The first window is built once; every later window is derived from it by a single remove and a single add.
- `window_freq == freq_p` is checked *before* sliding, so every valid window position gets tested exactly once.
- Deleting a key once its count hits `0` is essential — otherwise a stale `key: 0` entry makes the dictionaries compare unequal even when the letter sets truly match.

---

# 5. Plain English Algorithm

1. If `p` is longer than `s`, no anagram can fit — return `[]`.
2. Build `freq_p`, the letter-frequency map of `p`.
3. Build `window_freq`, the letter-frequency map of `s`'s first `len(p)` characters. Set `left = 0`, `right = len(p) - 1`.
4. While `right` is within `s`:
   - If `window_freq` equals `freq_p`, record `left` as a valid start index.
   - If `right` is the last index of `s`, stop.
   - Otherwise, remove `s[left]` from `window_freq` (deleting the key if its count hits `0`), add `s[right + 1]` to `window_freq`, and advance both `left` and `right`.
5. Return the recorded indices.

---

# 6. Pseudocode

```text
if length(p) > length(s)
    return []

left = 0
right = length(p) - 1
freq_p = frequency map of p
window_freq = frequency map of s[0 .. length(p)-1]
res = []

while right < length(s)
    if window_freq == freq_p
        res.append(left)

    if right == length(s) - 1
        break

    decrement window_freq[s[left]]
    if window_freq[s[left]] == 0
        delete window_freq[s[left]]

    increment window_freq[s[right + 1]]

    left++
    right++

return res
```

---

# 7. Python Solution

```python
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        if len(p) > len(s):
            return []

        left, right = 0, len(p) - 1
        freq_p = {}
        window_freq = {}
        for i in range(len(p)):
            freq_p[p[i]] = freq_p.get(p[i], 0) + 1
            window_freq[s[i]] = window_freq.get(s[i], 0) + 1

        res = []
        while right < len(s):
            if window_freq == freq_p:
                res.append(left)

            if right == len(s) - 1:
                break

            window_freq[s[left]] -= 1
            if window_freq[s[left]] == 0:
                del window_freq[s[left]]

            window_freq[s[right + 1]] = window_freq.get(s[right + 1], 0) + 1

            left += 1
            right += 1

        return res
```

---

# 8. Dry Run

Example:

```text
s = "abab", p = "ab"

freq_p = {a:1, b:1}
```

| Step | left, right | window_freq (before check) | Match? | Action | Why? |
|------|-------------|------------------------------|--------|--------|------|
| 1 | 0, 1 | {a:1, b:1} | Yes | res=[0]; remove s[0]='a' (-> del), add s[2]='a' | {a:1,b:1} == freq_p |
| 2 | 1, 2 | {b:1, a:1} | Yes | res=[0,1]; remove s[1]='b' (-> del), add s[3]='b' | {b:1,a:1} == freq_p |
| 3 | 2, 3 | {a:1, b:1} | Yes | res=[0,1,2]; right == last index -> break | {a:1,b:1} == freq_p |

Result: `[0, 1, 2]`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(s)`; each position is visited once as the window slides.
- Each dictionary equality check is `O(26)` (bounded lowercase alphabet), a constant factor, not a function of `n`.

### Space Complexity

```text
O(1)
```

Why?

- `freq_p` and `window_freq` each hold at most 26 lowercase-letter keys, independent of the length of `s` or `p`.
