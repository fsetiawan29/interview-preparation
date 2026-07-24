# Problem: Word Pattern

## 1. Problem Understanding

### Problem Summary

Given a `pattern` string and a string `s` containing words separated by single spaces, determine if `s` follows the same pattern — a bijection must exist where each character in `pattern` maps to exactly one word in `s`, and no two characters map to the same word.

### Input

- A string `pattern`
- A string `s` (words separated by single spaces)

### Output

- `true` if `s` follows the pattern as a bijection, `false` otherwise.

### Constraints

- `1 <= pattern.length <= 300`
- `pattern` contains only lowercase English letters.
- `1 <= s.length <= 3000`
- `s` contains only lowercase English letters and spaces `' '`.
- `s` does not contain any leading or trailing spaces.
- All the words in `s` are separated by a single space.

### Example

Input:

```text
pattern = "abba", s = "dog cat cat dog"
```

Output:

```text
true
```

Manual walkthrough:

```text
pattern: a    b    b    a
words:   dog  cat  cat  dog

Map a -> dog
Map b -> cat
b -> cat again, consistent
a -> dog again, consistent

Every character maps to the same word every time,
and no two characters share a word -> true
```

---

# 2. Key Insight

## What makes this problem difficult?

This is isomorphism, but between a string of characters and a sequence of words, and it must hold in both directions: the same character must always produce the same word, and no two different characters may produce the same word (e.g., `pattern="aa"`, `s="dog dog"` is fine, but `pattern="ab"`, `s="dog dog"` is not, since `a` and `b` would both map to "dog").

## Key Observation

First, splitting `s` on spaces gives a list of words the same length as `pattern` (otherwise a bijection is impossible immediately). Then a single map (`char -> word`) plus a `seen` set of already-used words can catch both kinds of violation in one pass: a character remapping to a different word, or two characters claiming the same word.

Example:

```text
pattern = "ab", s = "dog dog"
words = ["dog", "dog"]

i=0: char='a', word='dog' -> 'a' unmapped, 'dog' not in seen -> map a->dog, seen={dog}
i=1: char='b', word='dog' -> 'b' unmapped, but 'dog' IS already in seen (claimed by 'a')
     -> conflict! -> false
```

## Why does this observation help?

Checking `mapping` for an existing (and different) value, and checking `seen` for an already-claimed word, together guarantee a true bijection — a single left-to-right pass through `pattern` and `words` together is enough, no need for a second reverse-direction map.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture assigning each letter of `pattern` a "nametag" the first time it appears, written as the corresponding word from `s`. Keep a guest list of nametags already handed out. Every time a letter reappears, its nametag must match what was already written; every time a new nametag would be written, the word on it must not already belong to someone else.

```text
pattern: a     b     b     a
words:   dog   cat   cat   dog

a gets nametag "dog"   (guest list: dog)
b gets nametag "cat"   (guest list: dog, cat)
b's nametag already says "cat" -> matches -> ok
a's nametag already says "dog" -> matches -> ok

No conflicts -> true
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
words = s.split()
   │
   ▼
Is len(pattern) != len(words) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return false     Initialize mapping = {}, seen = {}
                       │
                       ▼
                 For each char, word in zip(pattern, words):
                       │
                       ▼
                 Is char in mapping ?
                       │
                     ┌─┴─────────────────┐
                     │                    │
                    Yes                   No
                     │                    │
                     ▼                    ▼
              Is mapping[char] != word ?   Is word in seen ?
                     │                        │
                   ┌─┴───────┐              ┌─┴───────┐
                   │          │              │          │
                  Yes         No            Yes         No
                   │          │              │          │
                   ▼          ▼              ▼          ▼
             Return false  continue      Return false  mapping[char]=word
                                                          seen.add(word)
                                                              │
                                                              ▼
                                                        Next pair (or Done)
                                                              │
                                                              ▼
                                                        Return true
```

Explanation of each decision:

- The length check happens first — if `pattern` and `words` don't have matching lengths, no bijection is possible.
- If `char` is already mapped, it must map to the *same* `word` every time — any different word is a conflict.
- If `char` is new, the `word` it wants must not already belong to some other character — checked via `seen`.
- Only after both checks pass does a new `(char, word)` pair get recorded.

---

# 5. Plain English Algorithm

1. Split `s` into a list of `words` on spaces.
2. If `len(pattern) != len(words)`, return `false` immediately.
3. Create an empty map `mapping` (char -> word) and an empty set `seen` (words already claimed).
4. Walk `pattern` and `words` together, pair by pair:
   - If the character is already in `mapping`, it must map to this exact `word` — otherwise return `false`.
   - Otherwise, the `word` must not already be in `seen` — otherwise return `false`. Then record `mapping[char] = word` and add `word` to `seen`.
5. If every pair passes without conflict, return `true`.

---

# 6. Pseudocode

```text
words = split(s, " ")

if length(pattern) != length(words)
    return false

mapping = empty map
seen = empty set

for char, word in zip(pattern, words)
    if char in mapping
        if mapping[char] != word
            return false
    else
        if word in seen
            return false

        mapping[char] = word
        seen.add(word)

return true
```

---

# 7. Python Solution

```python
class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split()

        if len(pattern) != len(words):
            return False

        mapping = {}
        seen = set()

        for char, word in zip(pattern, words):
            if char in mapping:
                if mapping[char] != word:
                    return False
            else:
                if word in seen:
                    return False

                mapping[char] = word
                seen.add(word)

        return True
```

---

# 8. Dry Run

Example:

```text
pattern = "abba", s = "dog cat cat dog"

words = ["dog", "cat", "cat", "dog"]
len(pattern)=4 == len(words)=4, guard passes
```

| Step | char | word | Action | Why? |
|------|------|------|--------|------|
| 1 | 'a' | "dog" | Record a->dog, seen={dog} | 'a' unmapped, "dog" unclaimed |
| 2 | 'b' | "cat" | Record b->cat, seen={dog,cat} | 'b' unmapped, "cat" unclaimed |
| 3 | 'b' | "cat" | No conflict | mapping[b]=="cat", matches |
| 4 | 'a' | "dog" | No conflict | mapping[a]=="dog", matches |

Result: `true`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n + m)
```

Why?

- `n = len(pattern)` (equal to the number of words after splitting) for the scan, `m = len(s)` for the initial split.

### Space Complexity

```text
O(k)
```

Why?

- `k` is the number of distinct characters/words, used by `mapping` and `seen`.
