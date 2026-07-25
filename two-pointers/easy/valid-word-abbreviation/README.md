# Problem: Valid Word Abbreviation

## 1. Problem Understanding

### Problem Summary

A string can be abbreviated by replacing any number of non-adjacent,
non-empty substrings with their lengths (no leading zeros in any numeral).
Given a string `word` and an abbreviation `abbr`, determine whether `abbr`
is a valid abbreviation of `word`.

### Input

- A string `word`
- A string `abbr`

### Output

- `true` if `abbr` is a valid abbreviation of `word`, `false` otherwise.

### Constraints

- `1 <= word.length <= 20`
- `word` consists of only lowercase English letters.
- `1 <= abbr.length <= 10`
- `abbr` consists of lowercase English letters and digits.
- All the integers in `abbr` will fit in a 32-bit integer.
- No leading zeros in any numeral run in `abbr`.

### Example

Input:

```text
word = "internationalization", abbr = "i12iz4n"
```

Output:

```text
true
```

Manual walkthrough:

```text
"internationalization" -> "i5n6i5n" -> "i12iz4n"

i                (1 char, matches 'i')
nternationa      (12 chars, replaced by "12")
i                (1 char, matches 'i')
z                (1 char, matches 'z')
atio             (4 chars, replaced by "4")
n                (1 char, matches 'n')
```

---

## 2. Brute Force Approach

### Idea

First split `abbr` into a list of tokens — each token is either a single letter or a full multi-digit number — using a separate parsing pass (e.g. a regex or a manual scan that groups consecutive digits together). Then walk `word` with an index, consuming one token at a time: a letter token must match the current character exactly (advance by 1); a number token skips that many characters. This works, but tokenizing `abbr` into its own list is a separate step done before comparing against `word`, instead of parsing numbers inline while scanning.

### Pseudocode

```text
tokens = []
i = 0
while i < length(abbr)
    if abbr[i] is a letter
        tokens.append(abbr[i])
        i += 1
    else
        num = ""
        while i < length(abbr) and abbr[i] is a digit
            num += abbr[i]
            i += 1
        tokens.append(int(num))

j = 0
for token in tokens
    if token is a letter
        if j >= length(word) or word[j] != token
            return false
        j += 1
    else
        j += token
        if j > length(word)
            return false

return j == length(word)
```

### Complexity Analysis

#### Time Complexity

```text
O(n + m)
```

Why?

- `n = len(word)`, `m = len(abbr)`; tokenizing is one pass over `abbr` (`O(m)`), then consuming tokens against `word` is another pass bounded by `O(n + m)` total work.

#### Space Complexity

```text
O(m)
```

Why?

- `tokens` stores every letter and parsed number from `abbr` as a separate list entry before any comparison against `word` happens.

### Why this isn't good enough

Building the `tokens` list is an unnecessary extra pass and extra `O(m)` storage — digits can be parsed into a number *inline* while a single pointer walks `abbr`, without ever materializing a separate token list. A fused two-pointer walk (one pointer in `word`, one in `abbr`) does the parsing and the matching in the same pass, dropping the auxiliary space to `O(1)`.

---

## 3. Key Insight

### What makes this problem difficult?

`abbr` mixes two different "instructions" — a letter demands an exact character match against `word`, while a digit run demands *skipping* a computed number of characters in `word` — and a numeral with a leading `'0'` (like `"01"`) is explicitly invalid. Handling both instruction types, plus the leading-zero edge case, in a single scan is easy to get subtly wrong (e.g. only reading one digit instead of the full run).

### Key Observation

Two pointers — `i` into `abbr`, `j` into `word` — can be advanced in lockstep without ever building an intermediate structure: whenever `abbr[i]` is a letter, compare it directly against `word[j]` and advance both by 1; whenever `abbr[i]` is a digit, parse the *entire* consecutive digit run right there (rejecting a leading `'0'`) into a number `skip`, and jump `j` forward by `skip` while advancing `i` past the whole run. At the very end, both pointers must have reached the exact end of their strings — this single check catches leftover unmatched characters in either `word` or `abbr`.

Example:

```text
word = "internationalization", abbr = "i12iz4n"

i=0,j=0:  abbr[0]='i' letter, word[0]='i' match  -> i=1, j=1
i=1,j=1:  abbr[1]='1' digit, parse "12" -> skip=12 -> i=3, j=13
i=3,j=13: abbr[3]='i' letter, word[13]='i' match -> i=4, j=14
i=4,j=14: abbr[4]='z' letter, word[14]='z' match -> i=5, j=15
i=5,j=15: abbr[5]='4' digit, parse "4" -> skip=4  -> i=6, j=19
i=6,j=19: abbr[6]='n' letter, word[19]='n' match -> i=7, j=20

i == len(abbr) == 7 and j == len(word) == 20 -> true
```

### Why does this observation help?

Parsing the full digit run inline (instead of one digit at a time, and instead of pre-tokenizing) means the number is read and consumed in the same pass that matches letters — no auxiliary list, and no risk of stopping after only the first digit of a multi-digit run.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture reading `abbr` left to right with a finger on `word` that moves along with it. Every letter in `abbr` means "check this exact spot in `word`, then move my finger one step." Every number in `abbr` means "lift my finger and set it down that many spots further ahead, without looking at what's underneath." If either reading runs out before the other, or the finger ever overshoots the end of `word`, the abbreviation doesn't fit.

```text
abbr = "a2e", word = "apple"

'a' -> check word[0]='a', match -> finger at 1
'2' -> lift finger, jump 2 spots -> finger at 3
'e' -> check word[3]='l', NOT 'e' -> mismatch -> false
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
i = 0, j = 0
   │
   ▼
Loop while i < len(abbr) and j < len(word):
   │
   ▼
Is abbr[i] a letter?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No (digit)
 │                    │
 ▼                    ▼
abbr[i] == word[j]?   Is abbr[i] == '0' ?
 │                    │
┌┴────┐              ┌┴────┐
Yes    No            Yes    No
│      │              │      │
▼      ▼              ▼      ▼
i+=1  return       return  Parse full digit run into `skip`,
j+=1  False        False   advance i past the run
│                            │
│                            ▼
│                     j += skip; is j > len(word)?
│                            │
│                          ┌─┴────┐
│                         Yes      No
│                          │        │
│                          ▼        │
│                     return False  │
└──────────────┬───────────────────┘
               ▼
     Loop again (or exit when i or j runs out)
               │
               ▼
     Return i == len(abbr) and j == len(word)
```

Explanation of each decision:

- Each iteration looks at `abbr[i]` to decide whether it's a literal character or the start of a numeral.
- A letter must match `word[j]` exactly, or the abbreviation is invalid immediately.
- A digit run starting with `'0'` is rejected outright — leading zeros are never valid.
- Otherwise, the entire consecutive digit run is parsed into `skip` in one inner loop, and `j` jumps forward by `skip`; if that jump pushes `j` past `len(word)`, the abbreviation overshoots and is invalid.
- The final check (`i == len(abbr) and j == len(word)`) ensures both strings were fully consumed — not just that the loop exited without an early `False`.

---

## 6. Plain English Algorithm

1. Initialize two pointers, `i = 0` into `abbr` and `j = 0` into `word`.
2. While both pointers are within bounds:
   - If `abbr[i]` is a letter: it must equal `word[j]` exactly, or return `False`. Advance both `i` and `j` by 1.
   - Otherwise (`abbr[i]` is a digit): if it's `'0'`, return `False` (no leading zeros). Otherwise, parse the entire consecutive run of digits starting at `i` into a number `skip`, advance `i` to just past that run, and advance `j` by `skip`. If `j` now exceeds `len(word)`, return `False`.
3. After the loop, `abbr` and `word` are both valid only if every character of each was consumed — return `i == len(abbr) and j == len(word)`.

---

## 7. Pseudocode

```text
i, j = 0, 0
while i < length(abbr) and j < length(word)
    if abbr[i] is a letter
        if abbr[i] != word[j]
            return false
        i += 1
        j += 1
    else
        if abbr[i] == '0'
            return false

        skip = 0
        k = i
        while k < length(abbr) and abbr[k] is a digit
            skip = skip * 10 + int(abbr[k])
            k += 1

        i = k
        j = j + skip
        if j > length(word)
            return false

return i == length(abbr) and j == length(word)
```

---

## 8. Python Solution

```python
class Solution:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        i, j = 0, 0
        while i < len(abbr) and j < len(word):
            if abbr[i].isalpha():
                if abbr[i] != word[j]:
                    return False
                i += 1
                j += 1
            else:
                if abbr[i] == '0':
                    return False

                skip = 0
                k = i
                while k < len(abbr) and abbr[k].isdigit():
                    skip = skip * 10 + int(abbr[k])
                    k += 1

                i = k
                j = j + skip
                if j > len(word):
                    return False
        return i == len(abbr) and j == len(word)
```

---

## 9. Dry Run

Example:

```text
word = "internationalization", abbr = "i12iz4n"
```

| Step | i before | j before | abbr[i] (or run) | Action | i after | j after |
|------|----------|----------|-------------------|--------|---------|---------|
| 1 | 0 | 0 | `'i'` | letter matches `word[0]='i'` | 1 | 1 |
| 2 | 1 | 1 | `"12"` | digit run, `skip=12` | 3 | 13 |
| 3 | 3 | 13 | `'i'` | letter matches `word[13]='i'` | 4 | 14 |
| 4 | 4 | 14 | `'z'` | letter matches `word[14]='z'` | 5 | 15 |
| 5 | 5 | 15 | `"4"` | digit run, `skip=4` | 6 | 19 |
| 6 | 6 | 19 | `'n'` | letter matches `word[19]='n'` | 7 | 20 |

Loop ends: `i == 7 == len(abbr)` and `j == 20 == len(word)` → both fully consumed.

Result: `True`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n + m)
```

Why?

- `n = len(word)`, `m = len(abbr)`; each character of `abbr` is visited exactly once (either as a matched letter or as part of a digit run), and `j` never revisits a position in `word`.

### Space Complexity

```text
O(1)
```

Why?

- Only the two pointers `i`, `j` and the running `skip` value are used — no auxiliary list or string is built, unlike the brute-force tokenization approach.
