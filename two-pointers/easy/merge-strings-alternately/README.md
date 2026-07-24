# Problem: Merge Strings Alternately

## 1. Problem Understanding

### Problem Summary

Given two strings `word1` and `word2`, merge them by adding letters in alternating order, starting with `word1`. If one string is longer than the other, append its remaining letters to the end of the merged result.

### Input

- Two strings `word1` and `word2`

### Output

- A single merged string, alternating characters from `word1` and `word2`.

### Constraints

- `1 <= word1.length, word2.length <= 100`
- `word1` and `word2` consist of lowercase English letters.

### Example

Input:

```text
word1 = "ab", word2 = "pqrs"
```

Output:

```text
"apbqrs"
```

Manual walkthrough:

```text
word1: a  b
word2: p  q  r  s

Take one char from word1, then one from word2, alternating:

a, p, b, q, (word1 exhausted), r, s

↓

"apbqrs"

Notice "rs" is simply appended once word1 runs out.
```

---

## 2. Brute Force Approach

### Idea

Build the result with repeated string concatenation (`result = result + char`) instead of collecting characters in a list and joining once at the end.

### Pseudocode

```text
result = ""
i = 0
j = 0

while i < length(word1) or j < length(word2)
    if i < length(word1)
        result = result + word1[i]
        i++
    if j < length(word2)
        result = result + word2[j]
        j++

return result
```

### Complexity Analysis

#### Time Complexity

```text
O((n + m)^2)
```

Why?

- `n = len(word1)`, `m = len(word2)`; strings are immutable, so each `result + char` copies the entire string built so far, and this happens `O(n + m)` times.

#### Space Complexity

```text
O(n + m)
```

Why?

- The final `result` string holds all characters (the discarded intermediate copies aren't counted).

### Why this isn't good enough

Every concatenation silently re-copies everything appended so far, turning what should be linear work into quadratic work. Appending characters to a list and joining once at the very end does the same job with each character written exactly once.

---

## 3. Key Insight

### What makes this problem difficult?

The two strings can have different lengths, so a naive `zip()`-style pairing would silently drop the longer string's extra characters once the shorter one runs out.

### Key Observation

Each string just needs **its own independent pointer** that advances only while it still has characters left. Once one pointer runs out, the other keeps going on its own — the "alternating" behavior falls out naturally as long as both pointers get a chance to contribute on every round, when available.

Example:

```text
word1 = "ab"     word2 = "pqrs"
         ↑                ↑
         i                j

i < len(word1) -> take word1[i], i++
j < len(word2) -> take word2[j], j++

once i >= len(word1), only j keeps contributing
```

### Why does this observation help?

By checking each pointer's bound independently on every round (instead of stopping the whole loop when either one is exhausted), the leftover tail of the longer string gets appended automatically — no special-case "append the rest" step is needed after the loop.

---

## 4. Mental Model

> What picture should I imagine in my head?

Imagine two hands taking turns placing a letter down, left hand first. If a hand runs out of letters, it simply stops reaching in — the other hand keeps placing letters until it also runs dry.

```text
word1: a  b            word2: p  q  r  s
       ↑                       ↑
       i                       j

Round 1: place word1[i]='a', i++; place word2[j]='p', j++  -> "ap"
Round 2: place word1[i]='b', i++; place word2[j]='q', j++  -> "apbq"
Round 3: i is out of bounds, skip word1;  place word2[j]='r', j++ -> "apbqr"
Round 4: i out of bounds, skip; place word2[j]='s', j++ -> "apbqrs"
Round 5: both out of bounds -> stop
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Initialize
res = []
i = 0, j = 0
   │
   ▼
Is i < len(word1) OR j < len(word2) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is i < len(word1) ?   Done — join res into a string
 │
┌─┴────────┐
│          │
Yes        No
│          │
▼          ▼
Append     (skip word1's turn)
word1[i]
i += 1
│          │
└────┬─────┘
     ▼
Is j < len(word2) ?
 │
┌─┴────────┐
│          │
Yes        No
│          │
▼          ▼
Append     (skip word2's turn)
word2[j]
j += 1
│          │
└────┬─────┘
     ▼
(back to top of loop)
```

Explanation of each decision:

- The outer loop condition uses `or` — it keeps going as long as *either* string still has characters left.
- Each string's append is gated by its own bound check, so an exhausted string simply contributes nothing that round instead of halting the whole process.

---

## 6. Plain English Algorithm

1. Start two pointers, `i` for `word1` and `j` for `word2`, both at `0`.
2. While either `i` is within `word1` or `j` is within `word2`:
   - If `i` is still in range, append `word1[i]` and advance `i`.
   - If `j` is still in range, append `word2[j]` and advance `j`.
3. Join every appended character into the final string and return it.

---

## 7. Pseudocode

```text
res = []
i = 0
j = 0

while i < length(word1) or j < length(word2)
    if i < length(word1)
        append word1[i] to res
        i++

    if j < length(word2)
        append word2[j] to res
        j++

return join(res)
```

---

## 8. Python Solution

```python
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        res = []
        i = 0
        j = 0
        while i < len(word1) or j < len(word2):
            if i < len(word1):
                res.append(word1[i])
                i += 1

            if j < len(word2):
                res.append(word2[j])
                j += 1

        return "".join(res)
```

---

## 9. Dry Run

Example:

```text
word1 = "abcd", word2 = "pq"
```

| Step | Pointer(s) | Current Values | Action | Result So Far | Why? |
|------|------------|-----------------|--------|----------------|------|
| 1 | i=0, j=0 | 'a', 'p' | Append both, i=1, j=1 | "ap" | Both strings have characters |
| 2 | i=1, j=1 | 'b', 'q' | Append both, i=2, j=2 | "apbq" | Both strings have characters |
| 3 | i=2, j=2 | 'c', — | Append word1 only, i=3 | "apbqc" | word2 exhausted, skip its turn |
| 4 | i=3, j=2 | 'd', — | Append word1 only, i=4 | "apbqcd" | word2 exhausted, skip its turn |
| 5 | i=4, j=2 | —, — | Stop | "apbqcd" | Both exhausted |

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n + m)
```

Why?

- `n = len(word1)`, `m = len(word2)`.
- Each pointer advances exactly once per character in its own string, regardless of the other's length.

### Space Complexity

```text
O(n + m)
```

Why?

- `res` collects every character from both strings.
- Excluding the output string itself, the extra state (`i`, `j`) is `O(1)`.
