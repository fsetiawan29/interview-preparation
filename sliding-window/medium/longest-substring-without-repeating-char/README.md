# Problem: Longest Substring Without Repeating Characters

## 1. Problem Understanding

### Problem Summary

Given a string `s`, find the length of the longest substring (contiguous) that contains no repeated characters.

### Input

- A string `s`

### Output

- An integer: the length of the longest substring without repeating characters.

### Constraints

- `0 <= s.length <= 5 * 10^4`
- `s` consists of English letters, digits, symbols and spaces.

### Example

Input:

```text
s = "abcabcbb"
```

Output:

```text
3
```

Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.

Manual walkthrough:

```text
s: a b c a b c b b

"a"    -> length 1
"ab"   -> length 2
"abc"  -> length 3 (best so far)
"abca" -> 'a' repeats, shrink from left until 'a' is gone -> "bca" length 3
...continues, but never beats length 3

-> 3
```

---

# 2. Key Insight

## What makes this problem difficult?

The window's size isn't fixed like a typical sliding-window problem — it needs to grow and shrink dynamically depending on where duplicates appear, so the naive approach of checking every substring is `O(n^2)` or worse.

## Key Observation

A window `[left, right]` is valid (no repeats) as long as we track what's currently inside it with a set. Expanding `right` by one is always safe to *attempt* — if the incoming character is already in the set, shrinking from `left` (removing characters from the set as they leave) is guaranteed to eventually remove the conflicting duplicate, because it's somewhere inside the current window.

Example:

```text
s = "abcabcbb"
window "abc", seen = {a,b,c}
right moves to next 'a' -> duplicate! shrink: remove s[left]='a' from seen, left advances
now seen = {b,c}, no more conflict -> add 'a' -> window "bca"
```

## Why does this observation help?

Both `left` and `right` only ever move forward, never backward. Each character is added to `seen` once and removed at most once across the entire scan, so the total work is `O(n)` even though there's a `while` loop nested inside the `for` loop.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture `right` scanning forward one character at a time, always trying to grow the window. Whenever the new character is already inside the window, `left` catches up — sliding forward and evicting characters — until the duplicate is expelled, and only then does the new character join.

```text
s: a  b  c  a  b  c  b  b
   ↑     ↑
   left  right     seen = {a, b, c}

right advances to the second 'a' -> conflict!
left slides forward, evicting 'a' from seen, until the duplicate is gone:

s: a  b  c  a  b  c  b  b
      ↑  ↑
      left right    seen = {b, c} -> now add 'a' -> seen = {b, c, a}
```

The best answer is simply the largest `right - left + 1` seen at any point.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Is len(s) == 0 ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return 0        left = 0, best = 0, seen = {}
                For right = 0 .. len(s)-1
                       │
                       ▼
                 Is s[right] in seen ?
                       │
                    ┌─┴─────────┐
                   Yes          No
                    │           │
                    ▼           │
             Remove s[left] from seen│
             left += 1              │
             (repeat this check)    │
                    │               │
                    └───────┬───────┘
                            ▼
                    Add s[right] to seen
                    best = max(best, right - left + 1)
                            │
                            └──▶ next right
                                      │
                                      ▼
                              Loop finished -> Return best
```

Explanation of each decision:

- The empty-string guard avoids indexing into an empty `s`.
- The inner "while `s[right]` in `seen`" loop may run zero or more times per `right` — it only runs as many times as needed to clear the specific duplicate.
- `s[right]` is only added to `seen` *after* any needed shrinking, guaranteeing the window is always valid the moment its length is measured.
- `best` is updated every iteration, since the window is always valid right after the add.

---

# 5. Plain English Algorithm

1. If `s` is empty, return `0`.
2. Initialize `left = 0`, `best = 0`, and an empty set `seen`.
3. For each `right` from `0` to `len(s) - 1`:
   - While `s[right]` is already in `seen`, remove `s[left]` from `seen` and advance `left` — repeat until the duplicate is gone.
   - Add `s[right]` to `seen` — the window `[left, right]` is now guaranteed duplicate-free.
   - Update `best` with the larger of `best` and `right - left + 1`.
4. Return `best`.

---

# 6. Pseudocode

```text
if length(s) == 0
    return 0

left = 0
best = 0
seen = {}

for right = 0 to length(s) - 1
    while s[right] in seen
        remove s[left] from seen
        left++

    add s[right] to seen
    best = max(best, right - left + 1)

return best
```

---

# 7. Python Solution

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if len(s) == 0:
            return 0

        left = 0
        best = 0
        seen = set()

        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1

            seen.add(s[right])
            best = max(best, right - left + 1)
        return best
```

---

# 8. Dry Run

Example:

```text
s = "abcabcbb"
```

| Step | right | s[right] | left before | Shrink? | left after | seen after add | best |
|------|-------|----------|-------------|---------|------------|------------------|------|
| 1 | 0 | 'a' | 0 | No | 0 | {a} | 1 |
| 2 | 1 | 'b' | 0 | No | 0 | {a,b} | 2 |
| 3 | 2 | 'c' | 0 | No | 0 | {a,b,c} | 3 |
| 4 | 3 | 'a' | 0 | Yes, remove 'a' | 1 | {b,c,a} | 3 |
| 5 | 4 | 'b' | 1 | Yes, remove 'b' | 2 | {c,a,b} | 3 |
| 6 | 5 | 'c' | 2 | Yes, remove 'c' | 3 | {a,b,c} | 3 |
| 7 | 6 | 'b' | 3 | Yes, remove 'a', then 'b' | 5 | {c,b} | 3 |
| 8 | 7 | 'b' | 5 | Yes, remove 'c', then 'b' | 7 | {b} | 3 |

Result: `best = 3`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(s)`; `left` and `right` each advance forward at most `n` times in total across the whole run.
- The inner `while` loop's total iterations across all steps of `right` are bounded by `n`, so there's no nested-loop blowup.

### Space Complexity

```text
O(min(n, k))
```

Why?

- `seen` holds at most one entry per character currently in the window.
- Bounded by either the string length `n` or the size of the character set `k`, whichever is smaller.
