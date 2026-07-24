# Problem: Valid Parentheses

## 1. Problem Understanding

### Problem Summary

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid. A string is valid if every open bracket is closed by the same type of bracket, and open brackets are closed in the correct order.

### Input

- A string `s` consisting of parentheses characters only.

### Output

- `true` if `s` is valid, `false` otherwise.

### Constraints

- `1 <= s.length <= 10^4`
- `s` consists of parentheses only `'()[]{}'`.

### Example

Input:

```text
s = "([)]"
```

Output:

```text
false
```

Manual walkthrough:

```text
Scan left to right, remembering unresolved open brackets:

( -> open, remember it: (
[ -> open, remember it: ( [
) -> close bracket arrives.

It must resolve the MOST RECENT open bracket, which is '['.
But ')' only matches '(', not '['.

Mismatch -> false
```

---

## 2. Brute Force Approach

### Idea

Repeatedly find and remove any adjacent matched pair (`"()"`, `"[]"`, or `"{}"`) from the string. If nothing but an empty string remains once no more pairs can be removed, the string was valid.

### Pseudocode

```text
str = s
changed = true

while changed
    changed = false
    for pair in ["()", "[]", "{}"]
        if pair in str
            str = replace first occurrence of pair in str with ""
            changed = true

return str == ""
```

### Complexity Analysis

#### Time Complexity

```text
O(n^2)
```

Why?

- `n = len(s)`; up to `n / 2` pairs can be removed, and each removal requires an `O(n)` scan to find the pair and rebuild the string.

#### Space Complexity

```text
O(n)
```

Why?

- A new string is built on every replacement.

### Why this isn't good enough

Every removal re-scans the entire string from scratch looking for the next collapsible pair, even though a close bracket only ever needs to check against the single most recently opened bracket. A stack exposes exactly that "most recent open bracket" at its top, so each character can be pushed or matched-and-popped in `O(1)`, with the whole string scanned only once.

---

## 3. Key Insight

### What makes this problem difficult?

It's tempting to just count brackets of each type, but counts alone ignore both **order** and **nesting**. `"([)]"` has one of each bracket type, yet it's invalid — the close brackets arrive in the wrong order relative to the opens.

### Key Observation

A close bracket must always resolve the **most recently seen, still-unresolved** open bracket — never an older one. That "most recent first" behavior is exactly what a stack's top gives you for free.

Example:

```text
( [   <- stack, top is on the right
    ↑
    the next close bracket MUST match this '['
```

### Why does this observation help?

By pushing every open bracket and popping on every close bracket, the top of the stack always tells us exactly which open bracket the current close bracket must match. A mismatch (or an empty stack when a close arrives) means the string is invalid immediately.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a stack of plates, one per unresolved open bracket, added on top as they appear. Every close bracket must remove the plate currently on top — and it must be the plate that matches its shape. If the shapes don't match, or there's no plate left to remove, something is wrong.

```text
( [
    ↑ top plate is '['

closing bracket ')' arrives -> tries to remove the top plate '['
'(' != what ')' expects -> mismatch
```

Once the whole string is scanned, if any plates are still stacked, some open brackets were never closed.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Initialize mapping (open -> close), stack = []
   │
   ▼
For each ch in s
   │
   ▼
Is ch an open bracket (in mapping)?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Push ch onto stack    Is stack empty?
 │                     │
 │                   ┌─┴────────┐
 │                   │          │
 │                  Yes        No
 │                   │          │
 │                   ▼          ▼
 │              Return false  Pop top, compare mapping[top] to ch
 │                              │
 │                            ┌─┴─────────┐
 │                            │           │
 │                          Match      Mismatch
 │                            │           │
 │                            ▼           ▼
 │                       Continue    Return false
 │                            │
 └────────────────────────────┴──▶ (back to "For each ch in s")

After loop:
   │
   ▼
Return not stack (empty stack ⇒ true)
```

Explanation of each decision:

- An open bracket is always pushed — we don't know yet what will close it.
- A close bracket arriving with an empty stack has nothing to match, so it's immediately invalid.
- A close bracket pops the top of the stack; if that popped bracket's expected close doesn't equal the current character, the nesting order was violated.
- Even if every close bracket matched something, leftover items in the stack after the loop mean some open brackets were never closed.

---

## 6. Plain English Algorithm

1. Build a mapping from each open bracket to its matching close bracket.
2. Initialize an empty stack.
3. For each character in `s`:
   - If it's an open bracket, push it onto the stack.
   - Otherwise (it's a close bracket):
     - If the stack is empty, return `false` immediately — there's nothing for it to close.
     - Pop the top of the stack. If the popped bracket's matching close isn't the current character, return `false`.
4. After scanning the whole string, return `true` only if the stack is empty — every open bracket was matched.

---

## 7. Pseudocode

```text
mapping = { '(': ')', '{': '}', '[': ']' }
stack = []

for ch in s
    if ch in mapping
        push ch onto stack
    else
        if stack is empty
            return false

        top = pop stack
        if mapping[top] != ch
            return false

return stack is empty
```

---

## 8. Python Solution

```python
class Solution:
    def isValid(self, s: str) -> bool:
        mapping = {
            '(': ')',
            "{": "}",
            "[": "]"
        }

        stack = []
        for ch in s:
            if ch in mapping:
                stack.append(ch)
            else:
                if not stack:
                    return False

                if mapping[stack.pop()] != ch:
                    return False

        return not stack
```

---

## 9. Dry Run

Example:

```text
s = "([)]"
```

| Step | Character | Stack Before | Action | Stack After | Why? |
|------|-----------|--------------|--------|-------------|------|
| 1 | `(` | `[]` | Push `(` | `['(']` | Open bracket, remember it |
| 2 | `[` | `['(']` | Push `[` | `['(', '[']` | Open bracket, remember it |
| 3 | `)` | `['(', '[']` | Pop `[`; `mapping['[']` is `]`, not `)` | `['(']` | Close bracket doesn't match top of stack |
| — | — | — | Return `false` | — | Mismatched bracket type |

Result: `false`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(s)`, one pass over the string.
- Each character is pushed or popped at most once.

### Space Complexity

```text
O(n)
```

Why?

- In the worst case (e.g. all open brackets, like `"((((("`), every character is pushed onto the stack.
