# Problem: Custom Sort String

## 1. Problem Understanding

### Problem Summary

Given a string `order` (a permutation of some subset of the lowercase alphabet) and a string `s`, rearrange the characters of `s` so that characters appearing in `order` come out in the same relative order as they appear in `order`. Characters of `s` that don't appear in `order` can be placed anywhere in the output.

### Input

- A string `order` (all characters unique)
- A string `s`

### Output

- A permutation of `s` whose characters, when they also appear in `order`, follow `order`'s relative sequence.

### Constraints

- `1 <= order.length <= 26`
- `1 <= s.length <= 200`
- `order` and `s` consist of lowercase English letters.
- All the characters of `order` are unique.

### Example

Input:

```text
order = "cba", s = "abcd"
```

Output:

```text
"cbad"
```

Manual walkthrough:

```text
s = "abcd" -> count each character:
a:1, b:1, c:1, d:1

Walk order = "cba":
  'c' appears in s -> emit "c", stop tracking it
  'b' appears in s -> emit "b", stop tracking it
  'a' appears in s -> emit "a", stop tracking it

Anything left over (not in order) gets appended at the end:
  'd' was never in order -> emit "d"

Result: "c" + "b" + "a" + "d" = "cbad"
```

---

# 2. Key Insight

## What makes this problem difficult?

`order` only constrains *some* of the alphabet, and `s` can repeat characters — a naive custom comparator sort would need to handle "not in order" as a special case and would also need to preserve repeat counts, which is easy to get wrong (e.g. emitting a repeated character only once).

## Key Observation

We don't need to sort character-by-character at all. Since every occurrence of the same character must land together in the output (they're indistinguishable), we can first **count how many times each character occurs in `s`**, then simply **walk `order` once** and dump the entire count for each character in one shot.

Example:

```text
s = "abcd" -> freq = {a:1, b:1, c:1, d:1}

order = "cba":
  'c' in freq -> append 'c' * freq['c']  ("c")
  'b' in freq -> append 'b' * freq['b']  ("b")
  'a' in freq -> append 'a' * freq['a']  ("a")
```

## Why does this observation help?

Because `order` is walked exactly once (length ≤ 26) and every character of `s` is consumed exactly once via the frequency map, the whole problem collapses into two linear passes and one shorter pass over `order` — no sorting or per-character comparator needed. Deleting a character from `freq` once it's emitted also guarantees it isn't accidentally emitted twice, and cleanly identifies what's "leftover" (never in `order`) once the walk finishes.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture a tally sheet (`freq`) built from `s`, one tally mark per character seen. Then imagine walking down the `order` string like a checklist: for each letter on the checklist, if the tally sheet has any marks for it, cross off that whole line and write all of its marks into the answer at once.

```text
freq:  a=1  b=1  c=1  d=1

order walk:  c -> b -> a
             │    │    │
             ▼    ▼    ▼
           "c"  "cb" "cba"   (each line fully consumed & crossed off)

freq left over: d=1  -> appended at the end -> "cbad"
```

Whatever tally marks remain after the checklist is exhausted belongs to characters `order` never mentioned — their exact position doesn't matter, so they're simply tacked onto the end.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Count every character of s into freq
   │
   ▼
For each ch in order:
   │
   ▼
Is ch in freq ?
   │
 ┌─┴───────────────┐
 │                  │
Yes                 No
 │                  │
 ▼                  ▼
Append ch * freq[ch]   Skip (nothing to emit)
Delete ch from freq        │
 │                          │
 └────────────┬─────────────┘
              ▼
     (loop to next ch in order)
              │
              ▼
order exhausted — freq now holds only
characters never mentioned in order
              │
              ▼
For each remaining ch, count in freq:
Append ch * count
              │
              ▼
           Done — join and return
```

Explanation of each decision:

- If `ch` from `order` is in `freq`, every occurrence of that character is emitted at once (`ch * freq[ch]`), then it's deleted so it can't be emitted again in the leftover pass.
- If `ch` from `order` isn't in `freq`, `s` simply has none of that character — nothing to do.
- After the `order` walk finishes, whatever remains in `freq` are characters `order` never constrained; each is appended (with its full count) in whatever order the map yields them.

---

# 5. Plain English Algorithm

1. Build a frequency map `freq` counting each character in `s`.
2. Walk `order` from left to right:
   - If the current character exists in `freq`, append it repeated `freq[ch]` times to the result, then remove it from `freq`.
3. After the walk, any characters still left in `freq` never appeared in `order` — append each one repeated by its count, in any order.
4. Join the result list into a string and return it.

---

# 6. Pseudocode

```text
freq = empty map

for ch in s
    freq[ch] = freq.get(ch, 0) + 1

res = []

for ch in order
    if ch in freq
        append (ch repeated freq[ch] times) to res
        remove ch from freq

for ch, count in freq
    append (ch repeated count times) to res

return join(res)
```

---

# 7. Python Solution

```python
class Solution:
    def customSortString(self, order: str, s: str) -> str:
        freq = {}
        for ch in s:
            freq[ch] = freq.get(ch, 0) + 1

        res = []
        for ch in order:
            if ch in freq:
                res.append(ch * freq[ch])
                del freq[ch]

        for ch, count in freq.items():
            res.append(ch * count)

        return "".join(res)
```

---

# 8. Dry Run

Example:

```text
order = "cba", s = "abcd"

Initial freq (from s): {a:1, b:1, c:1, d:1}
```

| Step | Source | Char | In freq? | Action | freq after | res after |
|------|--------|------|----------|--------|------------|-----------|
| 1 | order | 'c' | Yes | Append "c", delete 'c' | {a:1, b:1, d:1} | ["c"] |
| 2 | order | 'b' | Yes | Append "b", delete 'b' | {a:1, d:1} | ["c","b"] |
| 3 | order | 'a' | Yes | Append "a", delete 'a' | {d:1} | ["c","b","a"] |
| 4 | leftover | 'd' | — | Append "d" | {} | ["c","b","a","d"] |

Result: `"".join(["c","b","a","d"])` = `"cbad"`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n + m)
```

Why?

- `n = len(s)`, `m = len(order)`.
- One pass over `s` to build `freq`.
- One pass over `order`, and one pass over the leftover entries of `freq` — together these touch at most `m` plus the remaining distinct characters of `s`.

### Space Complexity

```text
O(n)
```

Why?

- `freq` holds at most the distinct characters of `s` (bounded by the 26-letter alphabet).
- `res` accumulates all `n` output characters before joining.
