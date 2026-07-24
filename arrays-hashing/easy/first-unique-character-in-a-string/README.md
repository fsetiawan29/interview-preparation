# Problem: First Unique Character in a String

## 1. Problem Understanding

### Problem Summary

Given a string `s`, find the index of the first character that appears exactly once. If no such character exists, return `-1`.

### Input

- A string `s`

### Output

- An integer index of the first non-repeating character, or `-1` if none exists.

### Constraints

- `1 <= s.length <= 10^5`
- `s` consists of only lowercase English letters.

### Example

Input:

```text
s = "leetcode"
```

Output:

```text
0
```

Manual walkthrough:

```text
s = l e e t c o d e

Counts: l:1  e:3  t:1  c:1  o:1  d:1

Scan left to right, looking for the first count of 1:
index 0 -> 'l' has count 1 -> found it!
```

---

# 2. Key Insight

## What makes this problem difficult?

Determining whether a character is "unique" requires knowing how many times it appears *anywhere* in the string — information that isn't available just by looking at the character in isolation as we scan.

## Key Observation

If we first count every character's total frequency across the whole string, then a second left-to-right scan can simply check each character's precomputed count. The first one with a count of exactly `1` is the answer.

Example:

```text
s = "loveleetcode"

freq = {l:2, o:2, v:1, e:4, t:1, c:1, d:1}

Scan left to right:
index 0 'l' -> freq=2, skip
index 1 'o' -> freq=2, skip
index 2 'v' -> freq=1 -> found it!
```

## Why does this observation help?

Separating the problem into "count everything" then "scan for the first count of 1" avoids re-scanning the rest of the string for every character — each phase is a single linear pass, giving `O(n)` total instead of `O(n^2)`.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture tallying every letter on a scoreboard first, one full pass over the string. Then take a second walk through the string from the start, and the first letter whose scoreboard tally reads exactly `1` is your answer.

```text
Scoreboard for "loveleetcode":
l:2  o:2  v:1  e:4  t:1  c:1  d:1

Walk again: l o v e l e e t c o d e
            2 2 1 ...
                ↑
          first tally of 1 -> index 2
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Build freq (count each character in s)
   │
   ▼
For each i, char in enumerate(s):
   │
   ▼
Is freq[char] == 1 ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return i          Next char (or Done)
                       │
                       ▼
                 Return -1
```

Explanation of each decision:

- The frequency map is fully built *before* the second scan begins, so every count checked is final and correct.
- The second scan stops at the first index whose character has a total count of `1`.
- If no such index is found by the end of the string, `-1` signals no unique character exists.

---

# 5. Plain English Algorithm

1. Build a frequency map `freq` counting every character in `s`.
2. Scan `s` left to right with its index `i`. For each `char`:
   - If `freq[char] == 1`, return `i` immediately.
3. If the scan completes without a match, return `-1`.

---

# 6. Pseudocode

```text
freq = empty map

for char in s
    freq[char] = freq.get(char, 0) + 1

for i, char in enumerate(s)
    if freq[char] == 1
        return i

return -1
```

---

# 7. Python Solution

```python
class Solution:
    def firstUniqChar(self, s: str) -> int:
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1

        for i, char in enumerate(s):
            if freq[char] == 1:
                return i

        return -1
```

---

# 8. Dry Run

Example:

```text
s = "loveleetcode"

freq built: {l:2, o:2, v:1, e:4, t:1, c:1, d:1}
```

| Step | i | char | freq[char] | Action | Why? |
|------|---|------|------------|--------|------|
| 1 | 0 | 'l' | 2 | Skip | Count is not 1 |
| 2 | 1 | 'o' | 2 | Skip | Count is not 1 |
| 3 | 2 | 'v' | 1 | Return 2 | First character with count exactly 1 |

Result: `2`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(s)`; one pass to build `freq` and one pass to scan `s`, each doing constant work per character.

### Space Complexity

```text
O(k)
```

Why?

- `k` is the number of distinct characters, bounded by the lowercase alphabet (at most 26).
