# Problem: Roman to Integer

## 1. Problem Understanding

### Problem Summary

Roman numerals are represented by seven symbols (`I`, `V`, `X`, `L`, `C`,
`D`, `M`), each with a fixed value. Normally symbols are written largest to
smallest and their values summed, but six subtractive pairs exist where a
smaller symbol placed before a larger one means "subtract" instead of "add":
`IV` (4), `IX` (9), `XL` (40), `XC` (90), `CD` (400), `CM` (900). Given a
valid roman numeral string, convert it to its integer value.

### Input

- A string `s` representing a valid roman numeral.

### Output

- An integer: the value of `s`.

### Constraints

- `1 <= s.length <= 15`
- `s` contains only the characters `('I', 'V', 'X', 'L', 'C', 'D', 'M')`.
- `s` is guaranteed to be a valid roman numeral in the range `[1, 3999]`.

### Example

Input:

```text
s = "MCMXCIV"
```

Output:

```text
1994
```

Manual walkthrough:

```text
M    -> 1000
CM   -> 900   (C before M: subtract)
XC   -> 90    (X before C: subtract)
IV   -> 4     (I before V: subtract)

1000 + 900 + 90 + 4 = 1994
```

---

## 2. Brute Force Approach

### Idea

Hardcode the six subtractive two-character substrings (`CM`, `CD`, `XC`, `XL`, `IX`, `IV`) as their own lookup entries alongside the single-symbol values. Scan `s` from left to right: at each position, first check whether the next two characters form one of the six known subtractive pairs — if so, add that pair's value and advance by two characters; otherwise add the single symbol's value and advance by one.

### Pseudocode

```text
values = {"I":1, "V":5, "X":10, "L":50, "C":100, "D":500, "M":1000}
pairs  = {"CM":900, "CD":400, "XC":90, "XL":40, "IX":9, "IV":4}

res = 0
i = 0
while i < length(s)
    two_char = s[i:i+2]
    if two_char in pairs
        res += pairs[two_char]
        i += 2
    else
        res += values[s[i]]
        i += 1

return res
```

### Complexity Analysis

#### Time Complexity

```text
O(n)
```

Why?

- `n = len(s)`; each iteration advances `i` by 1 or 2, and the two-character lookup against `pairs` is a fixed-size (6-entry) `O(1)` check.

#### Space Complexity

```text
O(1)
```

Why?

- `values` (7 entries) and `pairs` (6 entries) are fixed-size lookup tables, independent of `len(s)`.

### Why this isn't good enough

This is already `O(n)`, same as the optimized version — there's no asymptotic win available here. The real problem is duplication: the six subtractive pairs are hand-enumerated in their own table, so the "is this subtractive?" logic is special-cased per pair instead of expressed as one general rule. A single comparison between adjacent symbol values captures all six cases uniformly, with no separate pair table needed.

---

## 3. Key Insight

### What makes this problem difficult?

Roman numerals mix additive symbols (read left to right, sum the values) with subtractive pairs (`IV`, `IX`, `XL`, `XC`, `CD`, `CM`) where a smaller-value symbol placed before a larger one flips it from addition to subtraction. Treating those six pairs as arbitrary special cases means enumerating and hardcoding all of them by hand.

### Key Observation

"Subtractive" isn't really about which six specific pairs exist — it's about **relative value**: whenever a symbol's value is *less than* the value of the symbol immediately following it, that symbol should be subtracted instead of added. This single comparison naturally reproduces all six subtractive pairs (and no others) without ever naming them.

Example:

```text
s = "MCMXCIV"

M: value(M)=1000, next=C, value(C)=100  -> 1000 < 100? no  -> add 1000
C: value(C)=100,  next=M, value(M)=1000 -> 100 < 1000? yes -> subtract 100
M: value(M)=1000, next=X, value(X)=10   -> 1000 < 10? no   -> add 1000
X: value(X)=10,   next=C, value(C)=100  -> 10 < 100? yes   -> subtract 10
C: value(C)=100,  next=I, value(I)=1    -> 100 < 1? no     -> add 100
I: value(I)=1,    next=V, value(V)=5    -> 1 < 5? yes      -> subtract 1
V: value(V)=5,    no next                -> add 5

1000 - 100 + 1000 - 10 + 100 - 1 + 5 = 1994
```

### Why does this observation help?

One `if mapping[s[i]] < mapping[s[i + 1]]` check per character replaces the entire hardcoded six-pair lookup table — every subtractive case is handled by the exact same comparison, and there's nothing left to enumerate by hand.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture reading the numeral left to right while always peeking one symbol ahead, like reading a sentence and glancing at the next word before deciding how to punctuate the current one. If the next symbol outranks the current one, the current symbol is a "minus sign in disguise" — subtract it. Otherwise it's business as usual — add it.

```text
s = "IV"

Look at 'I' (1), peek at 'V' (5): 5 outranks 1 -> 'I' acts as a minus sign -> -1
Look at 'V' (5), nothing to peek at -> add normally -> +5

-1 + 5 = 4
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Build mapping = {I:1, V:5, X:10, L:50, C:100, D:500, M:1000}
   │
   ▼
For each index i in s:
   │
   ▼
Is there a next character (i + 1 < len(s))?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is mapping[s[i]] < mapping[s[i+1]] ?   res += mapping[s[i]]
 │                                          │
┌┴──────────┐                               │
│            │                              │
Yes          No                             │
│            │                              │
▼            ▼                              │
res -= mapping[s[i]]   res += mapping[s[i]]  │
│            │                              │
└─────┬──────┘                              │
      ▼                                     │
Next i (or Done) ◀───────────────────────────┘
      │
      ▼
Return res
```

Explanation of each decision:

- `mapping` is built once and gives `O(1)` lookup of any symbol's value.
- For every symbol except the last, its value is compared against the *next* symbol's value: if smaller, the current symbol is being used subtractively, so it's subtracted; otherwise it's added normally.
- The last symbol has no successor to compare against, so it's always added.
- No pair is ever named explicitly — the comparison alone reproduces every subtractive case.

---

## 6. Plain English Algorithm

1. Build a map from each roman symbol to its integer value.
2. Initialize `res = 0`.
3. Scan `s` left to right by index `i`:
   - If a next character exists and the current symbol's value is less than the next symbol's value, subtract the current symbol's value from `res` (it's part of a subtractive pair).
   - Otherwise, add the current symbol's value to `res`.
4. After the scan finishes, `res` holds the final integer value — return it.

---

## 7. Pseudocode

```text
mapping = {I:1, V:5, X:10, L:50, C:100, D:500, M:1000}

res = 0
for i in range(length(s))
    if i + 1 < length(s) and mapping[s[i]] < mapping[s[i + 1]]
        res -= mapping[s[i]]
    else
        res += mapping[s[i]]

return res
```

---

## 8. Python Solution

```python
class Solution:
    def romanToInt(self, s: str) -> int:
        mapping = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }

        res = 0
        for i in range(len(s)):
            if i + 1 < len(s) and mapping[s[i]] < mapping[s[i + 1]]:
                res -= mapping[s[i]]
            else:
                res += mapping[s[i]]

        return res
```

---

## 9. Dry Run

Example:

```text
s = "MCMXCIV"
```

| Step | i | s[i] | next char | mapping[s[i]] < mapping[next]? | Action | res after |
|------|---|------|-----------|----------------------------------|--------|-----------|
| 1 | 0 | 'M' | 'C' | 1000 < 100 → no | res += 1000 | 1000 |
| 2 | 1 | 'C' | 'M' | 100 < 1000 → yes | res -= 100 | 900 |
| 3 | 2 | 'M' | 'X' | 1000 < 10 → no | res += 1000 | 1900 |
| 4 | 3 | 'X' | 'C' | 10 < 100 → yes | res -= 10 | 1890 |
| 5 | 4 | 'C' | 'I' | 100 < 1 → no | res += 100 | 1990 |
| 6 | 5 | 'I' | 'V' | 1 < 5 → yes | res -= 1 | 1989 |
| 7 | 6 | 'V' | — (no next) | — | res += 5 | 1994 |

Result: `1994`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(s)`; the loop makes one `O(1)` mapping lookup (and at most one comparison) per character.

### Space Complexity

```text
O(1)
```

Why?

- `mapping` is a fixed-size table with exactly 7 entries, independent of `len(s)`.
