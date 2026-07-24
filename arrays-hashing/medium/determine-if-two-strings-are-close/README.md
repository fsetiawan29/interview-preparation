# Problem: Determine if Two Strings Are Close

## 1. Problem Understanding

### Problem Summary

Two strings are considered **close** if you can transform one into the other using any number of the following operations, in any order:

- **Operation 1**: Swap any two existing characters (e.g. `abcde -> aecdb`).
- **Operation 2**: Transform every occurrence of one existing character into another existing character, and do the same for the other character in return (e.g. `aacabb -> bbcbaa`, swapping all `a`'s and `b`'s).

Determine whether `word1` and `word2` are close.

### Input

- A string `word1`
- A string `word2`

### Output

- `true` if `word1` and `word2` are close, `false` otherwise.

### Constraints

- `1 <= word1.length, word2.length <= 10^5`
- `word1` and `word2` contain only lowercase English letters.

### Example

Input:

```text
word1 = "cabbba", word2 = "abbccc"
```

Output:

```text
true
```

Manual walkthrough:

```text
word1 = "cabbba" -> counts: c=1, a=2, b=3
word2 = "abbccc" -> counts: a=1, b=2, c=3

You can attain word2 from word1 in 3 operations:
"cabbba" -> "caabbb"   (Operation 1: reorder characters)
"caabbb" -> "baaccc"   (Operation 2: swap all b's and c's)
"baaccc" -> "abbccc"   (Operation 2: swap all a's and b's)

Both strings use the same set of characters {a, b, c}.
Both strings' frequency counts, once sorted, are [1, 2, 3].

Since the character sets match and the sorted frequency lists match,
word1 and word2 are close -> true
```

---

## 2. Brute Force Approach

### Idea

Build each string's frequency map the slow way — for each position not yet counted, scan the rest of that string to tally every remaining occurrence of that character — then compare the two maps' key sets and sorted value lists.

### Pseudocode

```text
function bruteForceFreq(word)
    n = length(word)
    used = array of n false values
    freq = empty map

    for i = 0 to n - 1
        if used[i]
            continue
        count = 0
        for j = i to n - 1
            if word[j] == word[i] and not used[j]
                count += 1
                used[j] = true
        freq[word[i]] = count

    return freq

if length(word1) != length(word2)
    return false

freq1 = bruteForceFreq(word1)
freq2 = bruteForceFreq(word2)

if keys(freq1) != keys(freq2)
    return false

return sorted(values(freq1)) == sorted(values(freq2))
```

### Complexity Analysis

#### Time Complexity

```text
O(n^2)
```

Why?

- `n = len(word1) == len(word2)`; in the worst case (many distinct characters), building each frequency map re-scans the remaining string from every position.

#### Space Complexity

```text
O(n)
```

Why?

- Each `used` array tracks one boolean per character of its string.

### Why this isn't good enough

Each frequency map is built by repeatedly re-scanning the remaining characters of the string. Counting each string in a single pass with a hash map (incrementing a running count per character) computes the exact same frequency map in `O(n)`, instead of `O(n^2)`.

---

## 3. Key Insight

### What makes this problem difficult?

There are two very different operations in play, and it's tempting to try to simulate them directly. Simulating swaps and relabels on strings of length up to `10^5` would be slow and error-prone — the real question is what invariant the operations preserve, not how to execute them.

### Key Observation

- Operation 1 (swap any two characters) means **positions never matter** — only which characters appear and how often.
- Operation 2 (swap all occurrences of one character with another) means **character labels don't matter either** — only the *multiset* of frequencies. Two strings are close exactly when they use the same set of characters, and that set's frequency values match up after sorting (each frequency can be "relabeled" onto a matching frequency in the other string via repeated Operation 2).

Example:

```text
word1 = "cabbba"  -> freq1 = {c:1, a:2, b:3}
word2 = "abbccc"  -> freq2 = {a:1, b:2, c:3}

freq1.keys() == freq2.keys()              -> {a,b,c} == {a,b,c}  True
sorted(freq1.values()) == sorted(freq2.values())
                                           -> [1,2,3] == [1,2,3]  True
```

### Why does this observation help?

Instead of simulating any operations at all, the problem reduces to two `O(1)`-ish checks on frequency maps: same character set, same sorted frequency multiset. Both are cheap to compute with a single pass over each string plus a sort bounded by the alphabet size (26).

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture each string reduced down to a bar chart: one bar per distinct character, whose height is that character's count. Operation 1 doesn't change any bar (positions are irrelevant to a count). Operation 2 lets you swap the *labels* on two bars.

```text
word1 bars:  c=1   a=2   b=3
word2 bars:  a=1   b=2   c=3

Same labels present:  {a,b,c} == {a,b,c}  ✓
Same bar heights (ignoring which label sits where), sorted:
  [1,2,3]  ==  [1,2,3]  ✓

-> close
```

If either the set of labels differs, or the sorted heights differ, no amount of swapping or relabeling can make the bar charts match.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Is len(word1) == len(word2) ?
   │
 ┌─┴─────────────────┐
 │                    │
No                   Yes
 │                    │
 ▼                    ▼
Return false     Build freq1 from word1
                       │
                       ▼
                 Build freq2 from word2
                       │
                       ▼
              Is freq1.keys() == freq2.keys() ?
                       │
                     ┌─┴─────────────────┐
                     │                    │
                    No                   Yes
                     │                    │
                     ▼                    ▼
               Return false     Is sorted(freq1.values())
                                 == sorted(freq2.values()) ?
                                       │
                                     ┌─┴───────┐
                                     │          │
                                    No         Yes
                                     │          │
                                     ▼          ▼
                               Return false  Return true
```

Explanation of each decision:

- Different lengths can never produce matching frequency multisets, so it's checked first as a cheap short-circuit.
- Matching key sets confirms both strings use exactly the same characters (a prerequisite — Operation 2 can only relabel characters that exist in both).
- Matching sorted value lists confirms the counts themselves line up once freely relabeled.
- Only when both checks pass are the strings close.

---

## 6. Plain English Algorithm

1. If `word1` and `word2` have different lengths, return `false` immediately.
2. Build a frequency map `freq1` counting each character in `word1`.
3. Build a frequency map `freq2` counting each character in `word2`.
4. Compare the two maps' key sets — if they differ, return `false`.
5. Compare the two maps' sorted value lists — if they differ, return `false`.
6. If both checks pass, return `true`.

---

## 7. Pseudocode

```text
if length(word1) != length(word2)
    return false

freq1 = empty map
for ch in word1
    freq1[ch] = freq1.get(ch, 0) + 1

freq2 = empty map
for ch in word2
    freq2[ch] = freq2.get(ch, 0) + 1

if keys(freq1) != keys(freq2)
    return false

return sorted(values(freq1)) == sorted(values(freq2))
```

---

## 8. Python Solution

```python
class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        if len(word1) != len(word2):
            return False

        freq1 = {}
        for w in word1:
            freq1[w] = freq1.get(w, 0) + 1

        freq2 = {}
        for w in word2:
            freq2[w] = freq2.get(w, 0) + 1

        return freq1.keys() == freq2.keys() and sorted(freq1.values()) == sorted(freq2.values())
```

---

## 9. Dry Run

Example:

```text
word1 = "cabbba", word2 = "abbccc"
```

| Step | Operation | State | Why? |
|------|-----------|-------|------|
| 1 | Check lengths | `len(word1)=6`, `len(word2)=6` → equal | Continue instead of early return |
| 2 | Build `freq1` over `word1` | `{c:1, a:2, b:3}` | One pass counting characters |
| 3 | Build `freq2` over `word2` | `{a:1, b:2, c:3}` | One pass counting characters |
| 4 | Compare key sets | `{c,a,b} == {a,b,c}` → `True` | Same characters used in both strings |
| 5 | Compare sorted values | `sorted([1,2,3]) == sorted([1,2,3])` → `True` | Frequency multisets match |
| 6 | Return | `True` | Both checks passed |

Result: `true`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(word1) == len(word2)`.
- Building each frequency map is one linear pass over its string.
- Sorting the value lists is bounded by the 26-letter alphabet, i.e. `O(1)`.

### Space Complexity

```text
O(1)
```

Why?

- Both frequency maps are bounded by the lowercase English alphabet (at most 26 entries each), independent of string length.
