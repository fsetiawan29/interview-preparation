# Problem: Permutation in String

## 1. Problem Understanding

### Problem Summary

Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1` — in other words, if some contiguous substring of `s2` is a rearrangement of `s1`'s characters.

### Input

- A string `s1`.
- A string `s2`.

### Output

- A boolean: `true` if any substring of `s2` is a permutation of `s1`, `false` otherwise.

### Constraints

- `1 <= s1.length, s2.length <= 10^4`
- `s1` and `s2` consist of lowercase English letters.

### Example

Input:

```text
s1 = "ab", s2 = "eidbaooo"
```

Output:

```text
true
```

Manual walkthrough:

```text
s2 contains the substring "ba" (at index 3), which is a permutation of s1 = "ab".
```

---

## 2. Brute Force Approach

### Idea

For every possible start index in `s2`, cut out a window of length `len(s1)` and check — from scratch — whether that window's letters are a permutation of `s1` by comparing frequency maps. No information is carried over between windows.

### Pseudocode

```text
if length(s1) > length(s2)
    return False

n = length(s2)
m = length(s1)
freq_s1 = frequency map of s1

for i = 0 to n - m
    freq_window = {}
    for j = i to i + m - 1
        freq_window[s2[j]] = freq_window.get(s2[j], 0) + 1

    if freq_window == freq_s1
        return True

return False
```

### Complexity Analysis

#### Time Complexity

```text
O(n * m)
```

Why?

- There are roughly `n = len(s2)` starting positions to try.
- For each one, building `freq_window` from scratch by scanning the window costs `O(m)` (`m = len(s1)`).
- Total: `O(n * m)`, which hits `~10^8` operations at the given constraint (`n, m` up to `10^4`) — too slow.

#### Space Complexity

```text
O(1)
```

Why?

- `freq_s1` and `freq_window` each hold at most 26 lowercase-letter keys, independent of `n` or `m`.

### Why this isn't good enough

Each window is treated as brand new, so sliding by one re-scans and re-counts all `m` characters even though the window only changed by one character on each end. That repeated work is exactly what the optimized approach below eliminates.

---

## 3. Key Insight

### What makes this problem difficult?

"Permutation" means same letters with the same counts, in any order, so a direct substring comparison doesn't work. Checking every window by sorting or rebuilding a frequency count from scratch is `O(n * m)` (`m = len(s1)`) — too slow when both lengths can reach `10^4`.

### Key Observation

A window of `s2` is a permutation of `s1` exactly when its letter-frequency map equals `s1`'s letter-frequency map. Since the window has fixed size `len(s1)`, sliding it by one only removes one letter's count (`left`) and adds another's (`right + 1`) — the frequency map can be updated incrementally instead of rebuilt.

Example:

```text
s1 = "ab"          freq_s1 = {a:1, b:1}
window "ba"         window_freq = {b:1, a:1}  -> equal to freq_s1 -> permutation found
```

### Why does this observation help?

Dictionary equality (`window_freq == freq_s1`) does the "is this a permutation" check in `O(26)` (bounded alphabet) instead of `O(m log m)` for sorting each window. Combined with `O(1)` incremental updates per slide, the whole scan stays `O(n)`.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a window of fixed width `len(s1)` sliding across `s2`, carrying a tally of the letters currently inside it. At every position, that tally is compared against `s1`'s own tally — a match means the window is a rearrangement of `s1`.

```text
s2: e  i  d  b  a  o  o  o
       [-----]
   window_freq = {i:1, d:1}  != freq_s1 = {a:1, b:1}  -> no match

slide ->

s2: e  i  d  b  a  o  o  o
             [-----]
   window_freq = {b:1, a:1}  == freq_s1                -> match, return True
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Is len(s1) > len(s2) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return False    Build freq_s1 from s1
                Build window_freq from s2[0..len(s1)-1]
                left = 0, right = len(s1) - 1
                      │
                      ▼
                (loop) window_freq == freq_s1 ?
                      │
                   ┌─┴───────┐
                   │         │
                  Yes        No
                   │         │
                   ▼         ▼
             Return True   Is right == len(s2) - 1 ?
                                 │
                              ┌─┴───────┐
                             Yes        No
                              │         │
                              ▼         ▼
                          break    Slide: right += 1, add s2[right]
                                   remove s2[left], left += 1
                                        │
                                        └──▶ (back to "window_freq == freq_s1 ?")

After loop:
   │
   ▼
Return False
```

Explanation of each decision:

- `len(s1) > len(s2)` is checked up front because no window of that size could even exist.
- The first window is built once; every later window is derived from it by a single add and a single remove.
- `window_freq == freq_s1` is checked *before* sliding, so every valid window position gets tested exactly once, and the very first match short-circuits with `True`.
- Deleting a key once its count hits `0` is essential — otherwise a stale `key: 0` entry makes the dictionaries compare unequal even when the letter sets truly match.

---

## 6. Plain English Algorithm

1. If `s1` is longer than `s2`, no permutation can fit — return `False`.
2. Build `freq_s1`, the letter-frequency map of `s1`.
3. Build `window_freq`, the letter-frequency map of `s2`'s first `len(s1)` characters. Set `left = 0`, `right = len(s1) - 1`.
4. Loop:
   - If `window_freq` equals `freq_s1`, a permutation was found — return `True`.
   - If `right` is the last index of `s2`, stop.
   - Otherwise, advance `right` by 1 and add `s2[right]` to `window_freq`; remove `s2[left]` from `window_freq` (deleting the key if its count hits `0`), then advance `left` by 1.
5. Return `False`.

---

## 7. Pseudocode

```text
if length(s1) > length(s2)
    return False

left = 0
right = length(s1) - 1
freq_s1 = frequency map of s1
window_freq = frequency map of s2[0 .. length(s1)-1]

while True
    if window_freq == freq_s1
        return True

    if right == length(s2) - 1
        break

    right += 1
    increment window_freq[s2[right]]

    decrement window_freq[s2[left]]
    if window_freq[s2[left]] == 0
        delete window_freq[s2[left]]

    left += 1

return False
```

---

## 8. Python Solution

```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        left = 0
        right = len(s1) - 1

        window_freq = {}
        for i in range(right + 1):
            window_freq[s2[i]] = window_freq.get(s2[i], 0) + 1

        freq_s1 = {}
        for ch in s1:
            freq_s1[ch] = freq_s1.get(ch, 0) + 1

        while True:
            if freq_s1 == window_freq:
                return True

            if right == len(s2) - 1:
                break

            right += 1
            window_freq[s2[right]] = window_freq.get(s2[right], 0) + 1

            window_freq[s2[left]] -= 1
            if window_freq[s2[left]] == 0:
                del window_freq[s2[left]]

            left += 1

        return False
```

---

## 9. Dry Run

Example:

```text
s1 = "ab", s2 = "eidbaooo"

freq_s1 = {a:1, b:1}
```

| Step | left, right | Window State (before check) | Match? | Action | Why? |
|------|-------------|------------------------------|--------|--------|------|
| 1 | 0, 1 | `{e:1, i:1}` | No | right=2, add `s2[2]='d'`; remove `s2[0]='e'` (-> del); left=1 | Window is `"ei"`, not a permutation of `"ab"` |
| 2 | 1, 2 | `{i:1, d:1}` | No | right=3, add `s2[3]='b'`; remove `s2[1]='i'` (-> del); left=2 | Window is `"id"`, not a permutation of `"ab"` |
| 3 | 2, 3 | `{d:1, b:1}` | No | right=4, add `s2[4]='a'`; remove `s2[2]='d'` (-> del); left=3 | Window is `"db"`, not a permutation of `"ab"` |
| 4 | 3, 4 | `{b:1, a:1}` | Yes | Return `True` | Window is `"ba"`, `{b:1,a:1} == freq_s1` |

Result: `True`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(s2)`; each position is visited once as the window slides.
- Each dictionary equality check is `O(26)` (bounded lowercase alphabet), a constant factor, not a function of `n`.

### Space Complexity

```text
O(1)
```

Why?

- `freq_s1` and `window_freq` each hold at most 26 lowercase-letter keys, independent of the length of `s1` or `s2`.

---

## 11. Mistakes

- Forgot to check if `len(s1) > len(s2)` before processing.
- Forgot to iterate over the characters in the string; instead, I accidentally iterated over integer indices.