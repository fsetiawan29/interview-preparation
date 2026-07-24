# Problem: Ransom Note

## 1. Problem Understanding

### Problem Summary

Given two strings `ransomNote` and `magazine`, determine if `ransomNote` can be constructed by using the letters from `magazine`, where each letter in `magazine` can only be used once.

### Input

- A string `ransomNote`
- A string `magazine`

### Output

- `true` if `ransomNote` can be constructed from `magazine`'s letters, `false` otherwise.

### Constraints

- `1 <= ransomNote.length, magazine.length <= 10^5`
- `ransomNote` and `magazine` consist of lowercase English letters.

### Example

Input:

```text
ransomNote = "aa", magazine = "aab"
```

Output:

```text
true
```

Manual walkthrough:

```text
magazine = "aab" -> available letters: a:2, b:1

ransomNote = "aa" needs: a, a

Take first 'a' -> magazine has 2 a's, 1 left
Take second 'a' -> magazine has 1 a's, 0 left

Both letters found -> true
```

---

# 2. Key Insight

## What makes this problem difficult?

Each letter in `magazine` can only be used once, so it's not enough to check that a letter *exists* somewhere in `magazine` — we must track how many copies remain as `ransomNote` consumes them.

## Key Observation

Counting every letter's availability in `magazine` up front, then decrementing that count as `ransomNote` "spends" each letter, immediately reveals a shortage: the moment any count goes negative, `magazine` has run out of that letter.

Example:

```text
magazine = "aab" -> freq = {a:2, b:1}

ransomNote = "aab" consumes:
'a' -> freq[a] 2->1
'a' -> freq[a] 1->0
'b' -> freq[b] 1->0

All consumed without going negative -> true
```

## Why does this observation help?

A single frequency map, built once and then decremented as `ransomNote` is scanned, lets us detect a shortage in one linear pass — no need to re-scan `magazine` for every letter of `ransomNote`.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture `magazine`'s letters laid out as a pile of clippings, one pile per letter, each pile's height equal to how many times that letter appears. As `ransomNote` is built letter by letter, take one clipping off the matching pile. If a pile is ever empty when a clipping is needed, the note simply can't be built.

```text
Piles from magazine="aab":  a:[■■]  b:[■]

Building ransomNote = "aa":
take 'a' -> a:[■]
take 'a' -> a:[]

Note fully built without running out -> true
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Is len(ransomNote) > len(magazine) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return false     Build freq (count each char in magazine)
                       │
                       ▼
                 For each char in ransomNote:
                       │
                       ▼
                 freq[char] -= 1
                       │
                       ▼
                 Is freq[char] < 0 ?
                       │
                     ┌─┴─────────┐
                     │            │
                    Yes           No
                     │            │
                     ▼            ▼
               Return false   Next char (or Done)
                                   │
                                   ▼
                             Return true
```

Explanation of each decision:

- A quick length check upfront rules out the impossible case where `ransomNote` is longer than `magazine`.
- `freq` is built once from `magazine`, then decremented for every letter `ransomNote` consumes.
- The moment any count drops below `0`, `magazine` doesn't have enough of that letter — return `false` immediately.

---

# 5. Plain English Algorithm

1. If `ransomNote` is longer than `magazine`, return `false` immediately.
2. Build a frequency map `freq` counting every character in `magazine`.
3. Scan `ransomNote` left to right. For each `char`:
   - Decrement `freq[char]`.
   - If `freq[char]` is now negative, return `false` — `magazine` ran out of that letter.
4. If the scan completes without going negative, return `true`.

---

# 6. Pseudocode

```text
if length(ransomNote) > length(magazine)
    return false

freq = empty map

for char in magazine
    freq[char] = freq.get(char, 0) + 1

for char in ransomNote
    freq[char] = freq.get(char, 0) - 1

    if freq[char] < 0
        return false

return true
```

---

# 7. Python Solution

```python
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False

        freq = {}
        for char in magazine:
            freq[char] = freq.get(char, 0) + 1

        for char in ransomNote:
            freq[char] = freq.get(char, 0) - 1

            if freq[char] < 0:
                return False

        return True
```

---

# 8. Dry Run

Example:

```text
ransomNote = "aa", magazine = "aab"

freq built from magazine: {a:2, b:1}
```

| Step | char (from ransomNote) | freq[char] after decrement | Negative? | Action |
|------|--------------------------|-------------------------------|-----------|--------|
| 1 | 'a' | 1 | No | Continue |
| 2 | 'a' | 0 | No | Continue |
| 3 | — | — | — | Loop finished, return true |

Result: `true`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(m + n)
```

Why?

- `m = len(magazine)` to build `freq`, `n = len(ransomNote)` to consume it — each doing constant work per character.

### Space Complexity

```text
O(k)
```

Why?

- `k` is the number of distinct characters, bounded by the lowercase alphabet (at most 26).
