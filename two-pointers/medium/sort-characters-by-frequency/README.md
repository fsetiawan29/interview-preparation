# Problem: Sort Characters By Frequency

## 1. Problem Understanding

### Problem Summary

Given a string `s`, sort it in decreasing order based on the frequency of the characters. The frequency of a character is the number of times it appears in the string. Return any string that satisfies this property.

### Input

- A string `s`

### Output

- A string with the same characters as `s`, rearranged so higher-frequency characters appear before lower-frequency ones.

### Constraints

- `1 <= s.length <= 5 * 10^5`
- `s` consists of uppercase and lowercase English letters and digits.

### Example

Input:

```text
s = "tree"
```

Output:

```text
"eert"
```

Manual walkthrough:

```text
Original

"tree"

Count frequencies:

t:1, r:1, e:2

Group characters into buckets indexed by frequency:

bucket[1] = [t, r]
bucket[2] = [e]

Walk buckets from highest frequency to lowest,
emitting each character repeated by its frequency:

bucket[2]: "ee"
bucket[1]: "t", "r"

↓

"eetr"  (also valid — "eert" is one of several correct answers)
```

---

## 2. Brute Force Approach

### Idea

Count each character's frequency, then sort every character in the string using a comparator based on that frequency.

### Pseudocode

```text
freq = {}
for char in s
    freq[char] = freq.get(char, 0) + 1

chars = list(s)
sort chars using key = -freq[char]   // comparison sort over all n characters

return join(chars)
```

### Complexity Analysis

#### Time Complexity

```text
O(n log n)
```

Why?

- `n = len(s)`; counting frequencies is `O(n)`, but sorting all `n` characters by a comparator dominates at `O(n log n)`.

#### Space Complexity

```text
O(n)
```

Why?

- `freq` holds at most one entry per distinct character; `chars` is a full copy of `s`.

### Why this isn't good enough

A comparison sort spends `O(n log n)` deciding an ordering, but frequencies are bounded by `len(s)`, so they can be used directly as bucket indices instead of compared pairwise. Counting sort — dropping each character into `bucket[frequency]` and reading the buckets from highest to lowest — produces the same decreasing-frequency order in `O(n)`, with no comparisons at all.

---

## 3. Key Insight

### What makes this problem difficult?

A direct approach would sort characters by frequency using a comparison sort, which costs `O(n log n)` and requires first counting frequencies anyway. Since frequencies are bounded by the length of the string, a comparison sort is more work than necessary.

### Key Observation

A character's frequency can never exceed `len(s)`, so frequencies live in a small, known range: `0` to `len(s)`. That means frequencies can be used directly as **bucket indices** — a form of counting sort — instead of comparing frequencies against each other.

Example:

```text
s = "tree", len(s) = 4

freq = {t:1, r:1, e:2}

buckets (index 0..4):
index 0: []
index 1: [t, r]
index 2: [e]
index 3: []
index 4: []
```

### Why does this observation help?

Placing each character straight into `bucket[count]` avoids any comparison between frequencies. Reading the buckets from the highest index down to the lowest naturally yields characters in decreasing frequency order, all in linear time.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a row of empty bins labeled `0, 1, 2, ..., len(s)`. Drop each distinct character into the bin matching its frequency. Then walk the bins from the highest label to the lowest, and for every character found in a bin, write it out that many times.

```text
bins:  0    1      2    3    4
      [ ]  [t,r]  [e]  [ ]  [ ]

walk from bin 4 down to bin 0:
bin 2 -> 'e' repeated 2 times -> "ee"
bin 1 -> 't' repeated 1 time -> "t"
bin 1 -> 'r' repeated 1 time -> "r"

result: "ee" + "t" + "r" = "eetr"
```

No comparisons between characters are ever made — only bucket placement and a single ordered walk.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Count frequency of each character into freq
Create res = list of (len(s)+1) empty buckets
   │
   ▼
For each (char, count) in freq:
   append char to res[count]
   │
   ▼
Initialize i = len(res) - 1
   │
   ▼
Is i >= 0 ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
For each char in res[i]:      Return "".join(result)
   append char * i to result
   │
   ▼
i -= 1
   │
   └──▶ (back to "Is i >= 0 ?")
```

Explanation of each decision:

- The frequency count is built first because bucket placement depends on it.
- Buckets are indexed by frequency (`0` to `len(s)`), so a character with frequency `k` always lands in `res[k]`.
- Walking `i` from the highest bucket down to `0` guarantees decreasing frequency order in the output.
- `char * i` reproduces the character exactly as many times as it originally appeared.

---

## 6. Plain English Algorithm

1. Count how many times each character appears in `s`, storing the result in `freq`.
2. Create `len(s) + 1` empty buckets, indexed `0` through `len(s)`.
3. For each character and its count in `freq`, append the character to `res[count]`.
4. Walk the bucket index `i` from `len(res) - 1` down to `0`.
5. For each character found in `res[i]`, append that character repeated `i` times to the result.
6. Join and return the result as a string.

---

## 7. Pseudocode

```text
freq = {}
for char in s
    freq[char] = freq.get(char, 0) + 1

res = array of (length(s) + 1) empty lists

for char, count in freq
    res[count].append(char)

result = []
for i from length(res) - 1 down to 0
    for char in res[i]
        result.append(char repeated i times)

return join(result)
```

---

## 8. Python Solution

```python
class Solution:
    def frequencySort(self, s: str) -> str:
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1

        res = [[] for _ in range(len(s) + 1)]
        for char, count in freq.items():
            res[count].append(char)

        result = []
        for i in range(len(res) - 1, -1, -1):
            for char in res[i]:
                result.append(char * i)

        return "".join(result)
```

---

## 9. Dry Run

Example:

```text
s = "tree"
```

| Step | Action | State | Why? |
|------|--------|-------|------|
| 1 | Scan `s` character by character | `freq = {t:1, r:1, e:2}` | One pass builds the frequency map |
| 2 | Create buckets | `res = [[], [], [], [], []]` (indices 0..4) | `len(s) + 1 = 5` buckets |
| 3 | Place `t` (count 1) | `res[1] = [t]` | `freq['t'] == 1` |
| 4 | Place `r` (count 1) | `res[1] = [t, r]` | `freq['r'] == 1` |
| 5 | Place `e` (count 2) | `res[2] = [e]` | `freq['e'] == 2` |
| 6 | `i=4`: `res[4]` empty | `result = []` | Nothing to emit |
| 7 | `i=3`: `res[3]` empty | `result = []` | Nothing to emit |
| 8 | `i=2`: `res[2] = [e]` | `result = ["ee"]` | `'e' * 2 = "ee"` |
| 9 | `i=1`: `res[1] = [t, r]` | `result = ["ee", "t", "r"]` | `'t' * 1 = "t"`, `'r' * 1 = "r"` |
| 10 | `i=0`: `res[0]` empty | `result = ["ee", "t", "r"]` | Nothing to emit |

Result: `"".join(result) = "eetr"` — a valid answer (frequencies appear in decreasing order: `e` before `t` and `r`).

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(s)`. One pass builds the frequency map.
- Placing each distinct character into its bucket is bounded by the number of distinct characters (at most `n`).
- Walking all buckets and emitting characters touches at most `n` total character-repeats across every bucket.

### Space Complexity

```text
O(n)
```

Why?

- `freq` holds at most one entry per distinct character.
- `res` allocates `n + 1` buckets, and together they hold at most `n` characters total.
