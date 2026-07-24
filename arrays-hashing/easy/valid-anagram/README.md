# Problem: Valid Anagram

## 1. Problem Understanding

### Problem Summary

Given two strings `s` and `t`, determine if `t` is an anagram of `s` — meaning `t` uses exactly the same letters as `s`, with the same frequencies, just possibly in a different order.

### Input

- A string `s`
- A string `t`

### Output

- `true` if `t` is an anagram of `s`, `false` otherwise.

### Constraints

- `1 <= s.length, t.length <= 5 * 10^4`
- `s` and `t` consist of lowercase English letters.

### Example

Input:

```text
s = "anagram", t = "nagaram"
```

Output:

```text
true
```

Manual walkthrough:

```text
s = "anagram" -> counts: a:3, n:1, g:1, r:1, m:1
t = "nagaram" -> counts: n:1, a:3, g:1, r:1, m:1

Every letter count matches exactly between s and t -> true
```

---

# 2. Key Insight

## What makes this problem difficult?

Sorting both strings and comparing them works, but costs `O(n log n)`. Since only lowercase letters are involved, there's a faster way that avoids sorting entirely.

## Key Observation

If we count every character's frequency in `s`, then walk through `t` and *decrement* those same counts, an exact anagram will bring every count back down to precisely `0` — no more, no less.

Example:

```text
s = "rat" -> freq = {r:1, a:1, t:1}
t = "car" -> decrement:
c -> freq[c] = 0 - 1 = -1
a -> freq[a] = 1 - 1 = 0
r -> freq[r] = 1 - 1 = 0

freq = {r:0, a:0, t:1, c:-1}
Not every count is 0 (t:1, c:-1 remain) -> false
```

## Why does this observation help?

A single hash map, incremented for `s` and decremented for `t`, captures both "letter present in `s` but missing from `t`" (count stays positive) and "letter present in `t` but not in `s`" (count goes negative) — checking that every final count is `0` verifies both directions at once, in linear time.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture a set of scales, one per letter of the alphabet. Walking through `s` adds a weight to each letter's scale; walking through `t` removes a weight from that same letter's scale. If `t` is a true anagram of `s`, every scale ends up perfectly balanced at zero.

```text
s = "anagram" adds weights: a+3  n+1  g+1  r+1  m+1

t = "nagaram" removes weights: n-1  a-3  g-1  r-1  m-1

Final balance: a:0  n:0  g:0  r:0  m:0  -> every scale at zero -> true
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Is len(s) != len(t) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return false     Build freq by incrementing for each char in s
                       │
                       ▼
                 Decrement freq for each char in t
                       │
                       ▼
                 For each count in freq.values():
                       │
                       ▼
                 Is count != 0 ?
                       │
                     ┌─┴─────────┐
                     │            │
                    Yes           No
                     │            │
                     ▼            ▼
               Return false   Next count (or Done)
                                   │
                                   ▼
                             Return true
```

Explanation of each decision:

- Different lengths make an anagram impossible outright — checked first, avoiding wasted work.
- `freq` is incremented once per character of `s`, then decremented once per character of `t`, using the same map.
- If every final count is exactly `0`, both strings had identical letter multisets.

---

# 5. Plain English Algorithm

1. If `s` and `t` have different lengths, return `false`.
2. Build a frequency map `freq`, incrementing it once for each character in `s`.
3. Walk through `t`, decrementing `freq` once for each character.
4. Check every value in `freq` — if any is not `0`, return `false`.
5. If every value is `0`, return `true`.

---

# 6. Pseudocode

```text
if length(s) != length(t)
    return false

freq = empty map

for char in s
    freq[char] = freq.get(char, 0) + 1

for char in t
    freq[char] = freq.get(char, 0) - 1

for count in freq.values()
    if count != 0
        return false

return true
```

---

# 7. Python Solution

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1

        for char in t:
            freq[char] = freq.get(char, 0) - 1

        for count in freq.values():
            if count != 0:
                return False
        return True
```

---

# 8. Dry Run

Example:

```text
s = "anagram", t = "nagaram"

len(s) == len(t) == 7, guard passes
```

| Step | Phase | char | freq after update | Why? |
|------|-------|------|---------------------|------|
| 1 | count up (s) | 'a','n','a','g','r','a','m' | {a:3, n:1, g:1, r:1, m:1} | Every char of s increments its count |
| 2 | count down (t) | 'n','a','g','a','r','a','m' | {a:0, n:0, g:0, r:0, m:0} | Every char of t decrements the same map |
| 3 | final check | — | All values are 0 | No leftover counts in either direction |

Result: `true`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- Two linear passes to build/consume `freq` over strings of length `n`, plus a linear pass over the frequency map's values (bounded by 26 distinct keys).

### Space Complexity

```text
O(k)
```

Why?

- `k` is the number of distinct characters, bounded by the lowercase alphabet (at most 26), regardless of how long `s` and `t` are.
