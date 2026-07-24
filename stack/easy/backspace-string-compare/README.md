# Problem: Backspace String Compare

## 1. Problem Understanding

### Problem Summary

Given two strings `s` and `t`, each containing lowercase letters and the character `'#'` (representing a backspace that deletes the character typed immediately before it), determine whether the two strings are equal once every backspace has been applied.

### Input

- Two strings `s` and `t`, containing only lowercase letters and `'#'`.

### Output

- `true` if `s` and `t` are equal after processing backspaces, `false` otherwise.

### Constraints

- `1 <= s.length, t.length <= 200`
- `s` and `t` only contain lowercase letters and `'#'` characters.

### Example

Input:

```text
s = "ab#c", t = "ad#c"
```

Output:

```text
true
```

Manual walkthrough:

```text
s = "ab#c"
a -> keep:              a
b -> keep:               ab
# -> delete previous:    a
c -> keep:               ac
s becomes "ac"

t = "ad#c"
a -> keep:              a
d -> keep:               ad
# -> delete previous:    a
c -> keep:               ac
t becomes "ac"

"ac" == "ac" -> true
```

---

# 2. Key Insight

## What makes this problem difficult?

A `'#'` deletes whatever character was typed immediately before it — but that character might itself have already been deleted by an earlier `'#'`. You can't simply pair up each `'#'` with the literal character in front of it in the original string; you need to track what's still "alive" as you scan.

## Key Observation

Processing left to right, a `'#'` should simply pop whatever is currently on top of a stack of surviving characters. This naturally cascades: an earlier deletion changes what the next `'#'` ends up removing.

Example:

```text
s = "ab#c"
'a' -> push -> [a]
'b' -> push -> [a, b]
'#' -> pop  -> [a]
'c' -> push -> [a, c]

final stack: [a, c] -> "ac"
```

## Why does this observation help?

Building each string's surviving characters with a stack turns "apply the backspaces" into plain push/pop operations. Once both strings have been reduced to their surviving stacks, the answer is just a direct equality check between the two stacks.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture typing each string into a text box, one character at a time. Every regular letter appears and stacks on top of what's already there; every `'#'` is a backspace keypress that erases whichever letter is currently on top.

```text
type: a  b  #  c

a  -> [a]
b  -> [a, b]
#  -> [a]        (erases 'b')
c  -> [a, c]
```

Whatever remains in the stack once typing finishes is exactly the text visible in the box.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize stack = []
   │
   ▼
For each ch in the string
   │
   ▼
Is ch == "#" ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is stack empty?     Push ch onto stack
 │
┌─┴─────────┐
│           │
Yes         No
│           │
▼           ▼
Do nothing  Pop stack
│           │
└─────┬─────┘
      ▼
(back to "For each ch in the string")

After loop:
   │
   ▼
Return the stack (the surviving characters)

Finally: compare build(s) == build(t)
```

Explanation of each decision:

- A `'#'` on an empty stack has nothing to delete, so it's simply ignored.
- A `'#'` on a non-empty stack pops the most recently kept character — the cascading-delete effect.
- Any other character is a regular letter and gets pushed as a surviving character.
- Two strings produce equal results if and only if their surviving-character stacks are identical, element for element.

---

# 5. Plain English Algorithm

1. Define a helper that reduces a string to its "surviving characters" using a stack: for each character, if it's `'#'`, pop the stack (only if it isn't empty); otherwise, push the character.
2. Build the surviving-character stack for `s`.
3. Build the surviving-character stack for `t`.
4. Return whether the two stacks are equal.

---

# 6. Pseudocode

```text
function build(str)
    stack = []
    for ch in str
        if ch == "#"
            if stack is not empty
                pop stack
        else
            push ch onto stack
    return stack

return build(s) == build(t)
```

---

# 7. Python Solution

```python
class Solution:
    def backspaceCompare_stack(self, s: str, t: str) -> bool:
        return self.build(s) == self.build(t)

    def build(self, s: str) -> list[str]:
        stack = []
        for ch in s:
            if ch == "#":
                if stack:
                    stack.pop()
            else:
                stack.append(ch)

        return stack
```

---

# 8. Dry Run

Example:

```text
s = "ab#c", t = "ad#c"
```

Build(s):

| Step | Character | Stack Before | Action | Stack After | Why? |
|------|-----------|---------------|--------|-------------|------|
| 1 | `a` | `[]` | Push | `[a]` | Regular character |
| 2 | `b` | `[a]` | Push | `[a, b]` | Regular character |
| 3 | `#` | `[a, b]` | Pop | `[a]` | Backspace deletes the most recent character |
| 4 | `c` | `[a]` | Push | `[a, c]` | Regular character |

`build(s) = [a, c]`

Build(t):

| Step | Character | Stack Before | Action | Stack After | Why? |
|------|-----------|---------------|--------|-------------|------|
| 1 | `a` | `[]` | Push | `[a]` | Regular character |
| 2 | `d` | `[a]` | Push | `[a, d]` | Regular character |
| 3 | `#` | `[a, d]` | Pop | `[a]` | Backspace deletes the most recent character |
| 4 | `c` | `[a]` | Push | `[a, c]` | Regular character |

`build(t) = [a, c]`

Final comparison: `[a, c] == [a, c]` → `true`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n + m)
```

Why?

- `n = len(s)`, `m = len(t)`; each string is scanned once to build its stack.
- Every character causes at most one push or one pop.

### Space Complexity

```text
O(n + m)
```

Why?

- Both built stacks are kept in memory (up to the full length of each string) in order to compare them.
