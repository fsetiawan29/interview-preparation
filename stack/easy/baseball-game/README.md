# Problem: Baseball Game

## 1. Problem Understanding

### Problem Summary

You are keeping score for a baseball game with unusual rules. Given a list of strings `operations` representing the record of past scores, apply each operation and return the sum of all the scores on the record after applying every operation.

### Input

- A list of strings `operations`, where each element is `"C"`, `"D"`, `"+"`, or a string representing an integer.

### Output

- An integer: the sum of all scores on the record after applying every operation.

### Constraints

- `1 <= operations.length <= 1000`
- `operations[i]` is `"C"`, `"D"`, `"+"`, or a string representing an integer in the range `[-3 * 10^4, 3 * 10^4]`.
- For operation `"+"`, there will always be at least two previous scores on the record.
- For operations `"C"` and `"D"`, there will always be at least one previous score on the record.

### Example

Input:

```text
ops = ["5","2","C","D","+"]
```

Output:

```text
30
```

Manual walkthrough:

```text
Record starts empty: []

"5" -> record a new score:                       [5]
"2" -> record a new score:                        [5, 2]
"C" -> invalidate and remove the previous score:  [5]
"D" -> double the previous score (2*5=10), record: [5, 10]
"+" -> sum the previous two scores (5+10=15):     [5, 10, 15]

Total = 5 + 10 + 15 = 30
```

---

## 2. Brute Force Approach

### Idea

Never actually remove an entry from the record — mark it "cancelled" instead. Whenever an operation needs "the previous score(s)," scan backward from the end each time, skipping over cancelled entries, to find the most recent one(s) still in play.

### Pseudocode

```text
record = []   // stores (value, cancelled) pairs

for op in operations
    if op == "C"
        for i = length(record) - 1 down to 0
            if not record[i].cancelled
                record[i].cancelled = true
                break
    elif op == "D"
        for i = length(record) - 1 down to 0
            if not record[i].cancelled
                record.append((2 * record[i].value, false))
                break
    elif op == "+"
        found = []
        for i = length(record) - 1 down to 0
            if not record[i].cancelled
                found.append(record[i].value)
                if length(found) == 2
                    break
        record.append((found[1] + found[0], false))
    else
        record.append((int(op), false))

return sum(v for (v, cancelled) in record if not cancelled)
```

### Complexity Analysis

#### Time Complexity

```text
O(n^2)
```

Why?

- `n = len(operations)`; each `"C"`, `"D"`, or `"+"` may scan backward through the entire record to find the most recent uncancelled entry (or entries), and this can happen up to `n` times.

#### Space Complexity

```text
O(n)
```

Why?

- `record` holds one entry (cancelled or not) per operation processed.

### Why this isn't good enough

Keeping cancelled entries around means every lookup has to re-scan past them to find what's still valid. A real stack makes `"C"` an actual pop — permanently removing the invalidated entry — so the top of the stack is always exactly "the previous score," retrievable in `O(1)` with no scanning at all.

---

## 3. Key Insight

### What makes this problem difficult?

`"D"` and `"+"` refer to "the previous score(s)" — but that phrase means something different every time `"C"` removes an entry. It's tempting to track scores in a plain list indexed by position, but "previous" is a moving target once records are actually deleted, not just skipped.

### Key Observation

Every operation only ever needs the **top one or two entries of the record, as it currently stands** — exactly what a stack's top (and second-from-top) expose. The record itself can BE the stack: `"C"` pops, everything else pushes.

Example:

```text
stack (record): [5, 2]

"C" -> pop the top          -> [5]
"D" -> push 2 * top (2*5)   -> [5, 10]
"+" -> push top + second-from-top (5+10) -> [5, 10, 15]
```

### Why does this observation help?

Push, pop, and peek are all `O(1)` operations on a stack. Each operation can be resolved using only what's currently on top, with no need to search or rebuild history — and invalidated scores are genuinely removed rather than merely ignored.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture the scoreboard as a single stack of cards, one score per card, newest card on top. Every operation only ever looks at — or removes — the top card, or the top two cards.

```text
Record (stack), newest on top:
[5, 2]
     ↑ top

"C" -> discard the top card:            [5]
"D" -> peek top (5), push 2*5:          [5, 10]
"+" -> peek top two (5,10), push 5+10:  [5, 10, 15]
```

Whatever remains on the stack once every operation card has been played is exactly what gets summed.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Initialize stack = []
   │
   ▼
For each ch in operations
   │
   ▼
Is ch == "C" ?
   │
 ┌─┴──────────────────┐
 │                     │
Yes                    No
 │                     │
 ▼                     ▼
Pop stack            Is ch == "D" ?
 │                     │
 │                   ┌─┴──────────┐
 │                   │            │
 │                  Yes           No
 │                   │            │
 │                   ▼            ▼
 │         Push 2 * stack[-1]   Is ch == "+" ?
 │                   │            │
 │                   │          ┌─┴──────────┐
 │                   │          │            │
 │                   │         Yes           No
 │                   │          │            │
 │                   │          ▼            ▼
 │                   │   Push stack[-2]   Push int(ch)
 │                   │   + stack[-1]
 │                   │          │            │
 └───────────────────┴──────────┴────────────┘
                      │
                      ▼
        (back to "For each ch in operations")

After loop:
   │
   ▼
Return sum(stack)
```

Explanation of each decision:

- `"C"` pops — it discards the most recent record entirely.
- `"D"` pushes double the current top — it depends only on the single most recent score.
- `"+"` pushes the sum of the top two entries — it depends on the two most recent scores.
- Anything else is a plain integer score and gets pushed as-is.
- After every operation is applied, the answer is simply the sum of whatever remains on the stack.

---

## 6. Plain English Algorithm

1. Initialize an empty stack to represent the record.
2. For each operation string in `operations`:
   - If it's `"C"`, pop the stack — this discards the previous score.
   - If it's `"D"`, push twice the value currently on top of the stack.
   - If it's `"+"`, push the sum of the top two values currently on the stack.
   - Otherwise, it's an integer string — push its integer value.
3. After processing every operation, return the sum of all values left on the stack.

---

## 7. Pseudocode

```text
stack = []

for ch in operations
    if ch == "C"
        pop stack
    else if ch == "D"
        push 2 * stack[top]
    else if ch == "+"
        push stack[top - 1] + stack[top]
    else
        push toInt(ch)

return sum(stack)
```

---

## 8. Python Solution

```python
class Solution:
    def calPoints(self, operations: List[str]) -> int:
        stack = []
        for ch in operations:
            if ch == "C":
                stack.pop()
            elif ch == "D":
                stack.append(2 * stack[-1])
            elif ch == "+":
                stack.append(stack[-2] + stack[-1])
            else:
                stack.append(int(ch))

        return sum(stack)
```

---

## 9. Dry Run

Example:

```text
ops = ["5","2","C","D","+"]
```

| Step | Operation | Stack Before | Action | Stack After | Why? |
|------|-----------|---------------|--------|-------------|------|
| 1 | `"5"` | `[]` | Push `int("5")=5` | `[5]` | Plain integer score |
| 2 | `"2"` | `[5]` | Push `int("2")=2` | `[5, 2]` | Plain integer score |
| 3 | `"C"` | `[5, 2]` | Pop | `[5]` | Invalidate previous score |
| 4 | `"D"` | `[5]` | Push `2 * 5 = 10` | `[5, 10]` | Double the previous score |
| 5 | `"+"` | `[5, 10]` | Push `5 + 10 = 15` | `[5, 10, 15]` | Sum of previous two scores |

Result: `sum([5, 10, 15]) = 30`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(operations)`; each operation does `O(1)` work (push, pop, or peek).
- A final `O(n)` pass sums whatever remains on the stack.

### Space Complexity

```text
O(n)
```

Why?

- In the worst case (every operation pushes and none pop), the stack holds up to `n` scores.
