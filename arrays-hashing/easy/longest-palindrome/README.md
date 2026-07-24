# Problem: Longest Palindrome

## 1. Problem Understanding

### Problem Summary

Given a string `s` of lowercase and/or uppercase letters, determine the length of the longest palindrome that can be built using the letters of `s` (case-sensitively). Letters can be rearranged freely, but only as many of each letter may be used as appear in `s`.

### Input

- A string `s`

### Output

- An integer: the length of the longest buildable palindrome.

### Constraints

- `1 <= s.length <= 2000`
- `s` consists of lowercase and/or uppercase English letters only.

### Example

Input:

```text
s = "abccccdd"
```

Output:

```text
7
```

Manual walkthrough:

```text
Counts: a:1  b:1  c:4  d:2

Pairs usable: c (2 pairs = 4 letters), d (1 pair = 2 letters) -> 6 letters so far
Leftover odd counts: a:1, b:1 -> pick just one of them as the center

Example palindrome: "dccaccd" -> length 7
```

---

## 2. Brute Force Approach

### Idea

For each character position not yet accounted for, scan the rest of the string to count every remaining occurrence of that character, marking each one as counted so it isn't counted again from a later position.

### Pseudocode

```text
n = length(s)
used = array of n false values
result = 0
has_odd = false

for i = 0 to n - 1
    if used[i]
        continue

    count = 0
    for j = i to n - 1
        if s[j] == s[i] and not used[j]
            count += 1
            used[j] = true

    if count % 2 == 0
        result += count
    else
        has_odd = true
        result += count - 1

if has_odd
    result += 1

return result
```

### Complexity Analysis

#### Time Complexity

```text
O(n^2)
```

Why?

- In the worst case (many distinct characters), every index triggers an `O(n)` scan of the rest of the string before being marked `used`.

#### Space Complexity

```text
O(n)
```

Why?

- The `used` array tracks one boolean per character in `s`.

### Why this isn't good enough

Every character's total count is rediscovered by re-scanning the remaining string, position by position. A single frequency map built in one pass counts every character exactly once, replacing all those repeated scans with `O(1)` lookups.

---

## 3. Key Insight

### What makes this problem difficult?

The palindrome doesn't need to use every letter of `s` — leftover letters with odd counts can't all be paired up, so it's tempting to either overcount them or forget the "one odd letter allowed in the center" rule.

### Key Observation

A palindrome is built from pairs of matching letters mirrored around a center, plus optionally **one single leftover letter** sitting exactly in the middle. So for each character:

- If its count is even, every copy can be used in a mirrored pair.
- If its count is odd, only `count - 1` copies can be paired up (the largest even part); the leftover single copy is a *candidate* for the center.

Example:

```text
freq = {a:1, b:1, c:4, d:2}

c:4 (even) -> use all 4
d:2 (even) -> use all 2
a:1 (odd)  -> use 0 (1-1), one leftover 'a' available for center
b:1 (odd)  -> use 0 (1-1), one leftover 'b' available for center

Paired total = 4 + 2 = 6
Only ONE center slot exists -> add +1 (using either leftover 'a' or 'b')

Total = 7
```

### Why does this observation help?

Counting frequencies once lets us decide, character by character, exactly how many letters contribute to mirrored pairs — and a single flag (`has_odd`) is enough to know whether at least one leftover letter is available to occupy the one allowed center slot.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture building the palindrome from the outside in. For each letter, use as many *matching pairs* as its count allows — one goes on the left, one on the mirrored position on the right. Whatever count is left over (0 or 1 per letter) can't be paired anymore. If **any** letter has a leftover single copy, exactly one of them can be dropped into the very center of the palindrome.

```text
c:4 -> c _ _ _ _ _ _ c
          c _ _ _ c
d:2 ->    c d _ _ d c
a:1, b:1 -> only one can go in the single center slot:
          c d a d c   (or c d b d c)   <- one letter left over, unused
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Build freq (count each character in s)
   │
   ▼
Initialize result = 0, has_odd = False
   │
   ▼
For each (char, count) in freq:
   │
   ▼
Is count even ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
result += count    result += count - 1
                   has_odd = True
   │                    │
   └────────┬───────────┘
            ▼
   Next (char, count) (or Done)
            │
            ▼
   Is has_odd ?
            │
          ┌─┴─────────┐
          │            │
         Yes           No
          │            │
          ▼            ▼
   result += 1     result unchanged
          │            │
          └────┬────────┘
               ▼
        Return result
```

Explanation of each decision:

- Every even-count character contributes its full count — all copies pair up cleanly.
- Every odd-count character contributes `count - 1` (its largest even part), and marks that at least one leftover single letter exists.
- After scanning every character, at most one leftover single letter is allowed to occupy the center, adding `+1` only if `has_odd` was ever set.

---

## 6. Plain English Algorithm

1. Build a frequency map `freq` counting every character in `s`.
2. Initialize `result = 0` and `has_odd = False`.
3. For each `(char, count)` in `freq`:
   - If `count` is even, add the full `count` to `result`.
   - If `count` is odd, add `count - 1` to `result` and set `has_odd = True`.
4. If `has_odd` is `True`, add `1` to `result` (one leftover letter becomes the center).
5. Return `result`.

---

## 7. Pseudocode

```text
freq = empty map

for char in s
    freq[char] = freq.get(char, 0) + 1

result = 0
has_odd = false

for char, count in freq.items()
    if count % 2 == 0
        result += count
    else
        has_odd = true
        result += count - 1

if has_odd
    result += 1

return result
```

---

## 8. Python Solution

```python
class Solution:
    def longestPalindrome(self, s: str) -> int:
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1

        result = 0
        has_odd = False
        for char, count in freq.items():
            if count % 2 == 0:
                result += count
            else:
                has_odd = True
                result += count - 1

        if has_odd:
            result += 1

        return result
```

---

## 9. Dry Run

Example:

```text
s = "abccccdd"

freq built (in scan order): {a:1, b:1, c:4, d:2}
```

| Step | char | count | Even? | Action | result | has_odd |
|------|------|-------|-------|--------|--------|---------|
| 1 | a | 1 | No | result += 0 (1-1) | 0 | True |
| 2 | b | 1 | No | result += 0 (1-1) | 0 | True |
| 3 | c | 4 | Yes | result += 4 | 4 | True |
| 4 | d | 2 | Yes | result += 2 | 6 | True |
| 5 | — | — | — | has_odd is True, result += 1 | 7 | — |

Result: `7`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(s)`; one pass to build `freq` and one pass over the distinct characters in `freq` (at most 52, bounded by the alphabet).

### Space Complexity

```text
O(k)
```

Why?

- `k` is the number of distinct characters, bounded by the lowercase + uppercase alphabet (at most 52).
