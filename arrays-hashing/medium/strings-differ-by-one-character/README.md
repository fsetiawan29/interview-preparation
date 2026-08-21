# Problem: Strings Differ by One Character

## 1. Problem Understanding

### Problem Summary

Given a list of strings `dict` where every string has the same length,
determine whether there exist two strings in `dict` that differ by
**exactly one character at the same index** — i.e. every other position
matches, and exactly one position doesn't.

### Input

- A list of strings, `dict`, all of equal length.

### Output

- `true` if some pair of strings in `dict` differs by exactly one
  character at the same index, `false` otherwise.

### Constraints

- The total number of characters across `dict` is at most `10^5`.
- `dict[i].length == dict[j].length` for all `i, j`.
- `dict[i]` contains only lowercase English letters.
- All strings in `dict` are unique.
- Follow-up: solve it in `O(n * m)`, where `n = len(dict)` and `m` is the
  length of each string.

### Example

Input:

```text
dict = ["abcd","acbd","aacd"]
```

Output:

```text
true
```

Manual walkthrough:

```text
"abcd" vs "aacd":
 index: 0 1 2 3
 abcd:  a b c d
 aacd:  a a c d
              ^ only index 1 differs (b vs a) -> matches
```

Another example:

```text
dict = ["ab","cd","yz"]
```

```text
"ab" vs "cd": differ at index 0 AND index 1 -> doesn't count
"ab" vs "yz": differ at index 0 AND index 1 -> doesn't count
"cd" vs "yz": differ at index 0 AND index 1 -> doesn't count
Output: false
```

---

## 2. Brute Force Approach

### Idea

Compare every pair of strings directly. For each pair, walk both strings
position by position and count how many positions differ. If exactly one
position differs, a matching pair has been found.

### Pseudocode

```text
function solve(dict)
    n = len(dict)
    m = len(dict[0])
    for i = 0 to n - 1
        for j = i + 1 to n - 1
            diff = 0
            for k = 0 to m - 1
                if dict[i][k] != dict[j][k]
                    diff += 1
                    if diff > 1
                        break
            if diff == 1
                return true
    return false
```

### Complexity Analysis

#### Time Complexity

```text
O(n^2 * m)
```

Why?

- There are `O(n^2)` pairs of strings, and comparing each pair costs
  `O(m)` in the worst case.

#### Space Complexity

```text
O(1)
```

Why?

- Only a running difference counter is used beyond the input itself.

### Why this isn't good enough

With up to `10^5` characters total across `dict`, `n^2 * m` blows up fast
— e.g. `n = 1000` strings of length `100` already means `10^8` character
comparisons. The problem's own follow-up (`O(n * m)`) is a signal that
pairs shouldn't be compared directly at all.

---

## 3. Key Insight

### What makes this problem difficult?

Checking "differs by exactly one character" naturally suggests comparing
every pair, but that's quadratic in `n`. The trick is to avoid comparing
strings to each other and instead compare each string to a *summary* that
can be looked up in `O(1)`.

### Key Observation

Two strings differ by exactly one character at index `i` if and only if
they become **identical** once index `i` is masked out (replaced with a
wildcard) in both. So instead of comparing strings pairwise, generate
every "masked at index `i`" version of every string and check whether any
masked version has already been seen before:

- For each word, and for each index `i` in that word, build a key —
  the word with position `i` replaced by a placeholder character (e.g.
  `*`).
- If that exact key has already been produced by an *earlier* word, those
  two words are identical everywhere except index `i` — a match.
- Otherwise, record the key as seen and move on.

Example:

```text
"abcd" masked at index 1 -> "a*cd"
"aacd" masked at index 1 -> "a*cd"   <- same key, seen before -> match!
```

### Why does this observation help?

A hash set lookup is `O(1)` on average, so instead of `O(n)` comparisons
per string (against every other string), each string only needs `O(m)`
masked keys generated and checked — one per character position.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture every string as a strip with `m` slots. For each slot, cover that
one slot with your thumb and read off the rest of the strip as a
"fingerprint". Two strips that ever produce the *same* fingerprint (same
slot covered, same letters everywhere else) are strips that differ by
exactly one letter — the one under the thumb.

```text
"abcd", cover index 1: a?cd
"acbd", cover index 1: a?bd
"aacd", cover index 1: a?cd   <- matches "abcd"'s fingerprint -> found it
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
seen = empty set
   │
   ▼
For each word in dict:
   │
   ▼
For each index i in word:
   │
   ▼
key = word with index i replaced by '*'
   │
   ▼
key in seen ?
   │
 ┌─┴──────────────────┐
 │                     │
Yes                   No
 │                     │
 ▼                     ▼
Return true       Add key to seen,
                   continue to next i / word
   │                     │
   └──────────┬──────────┘
              ▼
   (all words, all indices exhausted)
              │
              ▼
        Return false
```

Explanation of each decision:

- `key in seen` means some earlier word produced the exact same masked
  fingerprint — the current word and that earlier word are identical
  everywhere except index `i`, which is exactly a one-character
  difference.
- If every word's every masked key is new, no two words in `dict` differ
  by exactly one character, so the answer is `false`.

---

## 6. Plain English Algorithm

1. Create an empty hash set `seen` to hold masked-string keys.
2. For each `word` in `dict`:
   - For each index `i` from `0` to `len(word) - 1`:
     - Build `key` by replacing the character at index `i` in `word` with
       a placeholder (e.g. `*`).
     - If `key` is already in `seen`, return `true` — a matching pair has
       been found.
     - Otherwise, add `key` to `seen`.
3. If every word's masked keys are exhausted with no match, return
   `false`.

---

## 7. Pseudocode

```text
function solve(dict)
    seen = empty set
    for word in dict
        for i = 0 to len(word) - 1
            key = word[0:i] + '*' + word[i+1:]
            if key in seen
                return true
            seen.add(key)
    return false
```

---

## 8. Go Solution

```go
package solution

func differByOne(dict []string) bool {
	seen := make(map[string]struct{})

	for _, word := range dict {
		key := []byte(word)

		for i := range key {
			original := key[i]
			key[i] = '*'

			if _, ok := seen[string(key)]; ok {
				return true
			}
			seen[string(key)] = struct{}{}

			key[i] = original
		}
	}

	return false
}
```

---

## 9. Dry Run

Example:

```text
dict = ["abcd", "acbd", "aacd"]
```

| Step | Word | Masked keys generated | Match found? | Why? |
|------|------|------------------------|---------------|------|
| 1 | `"abcd"` | `*bcd`, `a*cd`, `ab*d`, `abc*` | No | None of these keys were seen before; all added to `seen` |
| 2 | `"acbd"` | `*cbd`, `a*bd`, `ac*d`, `acb*` | No | None of these keys were seen before; all added to `seen` |
| 3 | `"aacd"` | `*acd` (new), `a*cd` | Yes | `a*cd` was already added by `"abcd"` at step 1 |

Result: `true`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n * m^2)
```

Why?

- There are `n` words, each producing `m` masked keys (one per index).
- Building each masked key and hashing it costs `O(m)` (string
  construction/copy), giving `O(n * m * m) = O(n * m^2)` overall.
- The problem's `O(n * m)` follow-up is reachable by avoiding the
  per-key string rebuild — e.g. precomputing rolling hashes of each
  word's prefix and suffix so a "mask index `i`" hash can be combined in
  `O(1)`, turning the inner loop's cost from `O(m)` down to `O(1)` per
  index.

### Space Complexity

```text
O(n * m^2)
```

Why?

- Every masked key (length `m`) for every word (`n` words, `m` keys each)
  can end up stored in `seen` in the worst case, before a match is found.
