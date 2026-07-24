# Problem: Remove Outermost Parentheses

## 1. Problem Understanding

### Problem Summary

A valid parentheses string can be uniquely decomposed into a concatenation of one or more "primitive" valid parentheses strings, where a primitive string is one that cannot be split into two non-empty valid parentheses strings. Given a valid parentheses string `s`, return `s` after removing the outermost pair of parentheses from every primitive string in its decomposition.

### Input

- A string `s` consisting only of `'('` and `')'`, guaranteed to be a valid parentheses string.

### Output

- The string `s` after the outermost parentheses of each primitive substring have been removed.

### Constraints

- `1 <= s.length <= 10^5`
- `s[i]` is either `'('` or `')'`.
- `s` is a valid parentheses string.

### Example

Input:

```text
s = "(()())(())"
```

Output:

```text
"()()()"
```

Manual walkthrough:

```text
s = "(()())(())"

Primitive decomposition (each piece starts fresh, back at ground level):
"(()())" + "(())"

Remove the outermost pair from each primitive piece:
"(()())" -> "()()"
"(())"   -> "()"

Concatenate the results:
"()()" + "()" = "()()()"
```

---

# 2. Key Insight

## What makes this problem difficult?

It's tempting to think you must first split `s` into its primitive pieces (by tracking matching-bracket boundaries), then strip the first and last character off each piece. That's extra bookkeeping — but it turns out you never need to identify the piece boundaries explicitly.

## Key Observation

The characters to **drop** are exactly the `'('` that takes the nesting depth from `0` to `1`, and the `')'` that takes it back from `1` to `0` — one such pair per primitive piece. Every other character is nested one level deeper (or more) and belongs in the output. A single running `depth` counter is enough to spot these two special characters, with no need to ever locate the piece boundaries themselves.

Example:

```text
s = "(()())"
depth:  0->1  1->2  2->1  1->2  2->1  1->0
chars:   (     (     )     (     )     )
         ^ outermost open (0->1): DROP              ^ outermost close (1->0): DROP
               ^^^^^^^^^^^^^^^^^^^^ everything else stays >= depth 1: KEEP
```

## Why does this observation help?

A single left-to-right pass with one integer counter is all that's needed — no stack of characters, and no explicit search for where one primitive piece ends and the next begins.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture nested doors, like floors of a building. `depth` tracks which floor you're currently on. Every time you walk through a door that takes you from the ground floor up to floor 1, that's the *outer shell* of a new primitive block being entered — don't record that door. Every time you walk back down from floor 1 to the ground floor, that's the outer shell closing — don't record that door either. Every other door you pass through, on the way up or down, is an inner door and belongs in the answer.

```text
(   (   )   (   )   )   (   (   )   )
0->1 1->2 2->1 1->2 2->1 1->0 0->1 1->2 2->1 1->0
 ^                              ^                ^
 skip: entering ground floor    skip: entering    skip: leaving
                                 ground floor      ground floor
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize res = [], depth = 0
   │
   ▼
For each ch in s
   │
   ▼
Is ch == "(" ?
   │
 ┌─┴──────────────────┐
 │                     │
Yes                    No (ch == ")")
 │                     │
 ▼                     ▼
Is depth > 0 ?       depth -= 1
 │                     │
┌─┴─────────┐          ▼
│           │        Is depth > 0 ?
Yes         No          │
│           │         ┌─┴─────────┐
▼           │         │           │
Append ch   │        Yes          No
│           │         │           │
└─────┬─────┘         ▼           │
      ▼           Append ch       │
   depth += 1        │            │
      │              └─────┬──────┘
      │                    ▼
      └──────────────▶ (back to "For each ch in s")

After loop:
   │
   ▼
Return "".join(res)
```

Explanation of each decision:

- For an open bracket, only append it if we're already nested (`depth > 0`) — an open bracket seen at `depth == 0` is an outermost open, which gets dropped.
- `depth` is incremented right after that check, since the open bracket is what causes the nesting to deepen.
- For a close bracket, `depth` is decremented **first**, reflecting that the bracket closes the current nesting level.
- The close bracket is only appended if the decremented `depth` is still `> 0` — if it just dropped to `0`, this was the outermost close, which gets dropped.

---

# 5. Plain English Algorithm

1. Initialize an empty result list and `depth = 0`.
2. For each character in `s`:
   - If it's `'('`: append it to the result only if `depth > 0` (i.e., it isn't an outermost open), then increment `depth`.
   - If it's `')'`: decrement `depth` first, then append it to the result only if `depth` is still `> 0` after decrementing (i.e., it wasn't an outermost close).
3. Join the result list into a string and return it.

---

# 6. Pseudocode

```text
res = []
depth = 0

for ch in s
    if ch == "("
        if depth > 0
            append ch to res
        depth += 1
    else
        depth -= 1
        if depth > 0
            append ch to res

return join(res)
```

---

# 7. Python Solution

```python
class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        res = []
        depth = 0
        i = 0

        while i < len(s):
            if s[i] == "(":
                if depth > 0:
                    res.append(s[i])

                depth += 1
            else:
                depth -= 1

                if depth > 0:
                    res.append(s[i])

            i += 1

        return "".join(res)
```

---

# 8. Dry Run

Example:

```text
s = "(()())(())"
```

| Step (i) | Character | Depth Before | Action | Depth After | Result So Far |
|----------|-----------|--------------|--------|-------------|----------------|
| 0 | `(` | 0 | `depth == 0` → skip append; `depth += 1` | 1 | `""` |
| 1 | `(` | 1 | `depth > 0` → append `(`; `depth += 1` | 2 | `"("` |
| 2 | `)` | 2 | `depth -= 1` → 1; `depth > 0` → append `)` | 1 | `"()"` |
| 3 | `(` | 1 | `depth > 0` → append `(`; `depth += 1` | 2 | `"()("` |
| 4 | `)` | 2 | `depth -= 1` → 1; `depth > 0` → append `)` | 1 | `"()()"` |
| 5 | `)` | 1 | `depth -= 1` → 0; `depth == 0` → skip append | 0 | `"()()"` |
| 6 | `(` | 0 | `depth == 0` → skip append; `depth += 1` | 1 | `"()()"` |
| 7 | `(` | 1 | `depth > 0` → append `(`; `depth += 1` | 2 | `"()()("` |
| 8 | `)` | 2 | `depth -= 1` → 1; `depth > 0` → append `)` | 1 | `"()()()"` |
| 9 | `)` | 1 | `depth -= 1` → 0; `depth == 0` → skip append | 0 | `"()()()"` |

Result: `"()()()"`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(s)`, one pass over the string.
- Each character is examined exactly once, doing `O(1)` work.

### Space Complexity

```text
O(n)
```

Why?

- The output list grows up to `O(n)` to hold the result.
- Excluding the output, only the `depth` counter is tracked, which is `O(1)` extra space.
