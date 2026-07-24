# Problem: Build an Array With Stack Operations

## 1. Problem Understanding

### Problem Summary

You are given an integer array `target` and an integer `n`. Starting from an empty stack and a stream of integers `1` to `n` (in order), use only `"Push"` (push the next stream integer onto the stack) and `"Pop"` (remove the top of the stack) so that the stack, read bottom to top, ends up equal to `target`. Return the sequence of operations used. Stop as soon as the stack equals `target` — don't read further integers or do more operations.

### Input

- `target`: a strictly increasing integer array.
- `n`: an integer; the stream provides integers `1` through `n` in order.

### Output

- A list of strings, each either `"Push"` or `"Pop"`, describing the operations applied to build `target`.

### Constraints

- `1 <= target.length <= 100`
- `1 <= n <= 100`
- `1 <= target[i] <= n`
- `target` is strictly increasing.

### Example

Input:

```text
target = [1,3], n = 3
```

Output:

```text
["Push","Push","Pop","Push"]
```

Manual walkthrough:

```text
Read 1, Push -> s = [1]
Read 2, Push -> s = [1,2]
Pop         -> s = [1]
Read 3, Push -> s = [1,3]
```

---

## 2. Brute Force Approach

### Idea

Actually maintain a real stack. Walk the stream from `1` to `n`; for each value, always `"Push"` it onto the stack. If the value just pushed doesn't match the next element still needed from `target`, immediately `"Pop"` it back off. Once the stack (tracked separately) equals `target`, stop.

### Pseudocode

```text
stack = []
ops = []
p = 0  // index into target

for val = 1 to n
    if p == length(target)
        break

    stack.append(val)
    ops.append("Push")

    if val == target[p]
        p += 1
    else
        stack.pop()
        ops.append("Pop")

return ops
```

### Complexity Analysis

#### Time Complexity

```text
O(n)
```

Why?

- `n` = the upper bound of the stream; each value from `1` to `n` is visited once and does `O(1)` work.

#### Space Complexity

```text
O(n)
```

Why?

- The real `stack` list mirrors the stream values that are still "on the stack" at any point, up to `O(n)` in the worst case, on top of the `O(n)`-sized `ops` result.

### Why this isn't good enough

This already runs in `O(n)` time, so it isn't "bad" — but keeping an actual `stack` list around is unnecessary. The stack's contents are never inspected or used for anything other than deciding whether to pop the value that was just pushed, and that decision only depends on comparing `val` to `target[p]`. The stack can be dropped entirely in favor of a single pointer into `target`.

---

## 3. Key Insight

### What makes this problem difficult?

The problem is phrased entirely in terms of physically pushing and popping a stack, which nudges you toward simulating one. But `target` is strictly increasing and the stream is also strictly increasing (`1, 2, 3, ...`), so every value that isn't needed gets pushed and immediately popped again — it never stays on the stack and never affects anything downstream.

### Key Observation

Since both the stream and `target` are strictly increasing, "is `val` needed?" is always answered by a single comparison: `val == target[p]`, where `p` tracks how much of `target` has been matched so far. A value that doesn't match is pushed then popped in the very next step, so the real stack contents are irrelevant — only `p` (how far through `target` we are) needs to be tracked.

### Why does this observation help?

It replaces an `O(n)`-space simulated stack with a single integer pointer `p`, and removes any need to actually store or compare list contents. The result list (`res`, the sequence of operation strings) is the only thing that needs to grow, so space drops from `O(n)` (stack) + `O(n)` (ops) to just `O(n)` for the ops themselves.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture `target` as a checklist with a finger (`p`) resting on the next number you're waiting for. Walk the stream `1, 2, 3, ...` one value at a time: if the value matches what your finger is pointing at, `"Push"` it and slide your finger forward one spot. If it doesn't match, `"Push"` it anyway and immediately `"Pop"` it right back off — a wasted round trip that leaves the checklist untouched. Stop the moment the finger walks off the end of the checklist.

```text
target = [1, 3]   p -> 1

val=1: matches target[p]=1 -> Push, p -> 3
val=2: doesn't match target[p]=3 -> Push, Pop
val=3: matches target[p]=3 -> Push, p -> off the end, stop
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Initialize p = 0, res = []
   │
   ▼
For val = 1 to n
   │
   ▼
Is p == length(target) ?
   │
 ┌─┴──────────────┐
 │                 │
Yes                No
 │                 │
 ▼                 ▼
Break loop     Append "Push" to res
                    │
                    ▼
              Does val == target[p] ?
                    │
                  ┌─┴──────────────┐
                  │                 │
                 Yes                No
                  │                 │
                  ▼                 ▼
            p += 1            Append "Pop" to res
                  │                 │
                  └────────┬────────┘
                            ▼
              (back to "For val = 1 to n")

After loop:
   │
   ▼
Return res
```

Explanation of each decision:

- Stop as soon as `p` has matched every element of `target` — no further stream values are read or operations performed.
- Every stream value is unconditionally pushed first, matching the problem's own rule that a push always happens before a possible pop.
- If the pushed value is the one `target` needs next (`val == target[p]`), keep it and advance `p`.
- Otherwise it was never needed — pop it right back off in the very next operation.

---

## 6. Plain English Algorithm

1. Initialize `p = 0` (how much of `target` has been matched) and an empty result list `res`.
2. For each stream value `val` from `1` to `n`:
   - If `p` already equals `len(target)`, every needed number has been placed — stop reading the stream.
   - Otherwise, append `"Push"` to `res`.
   - If `val` equals `target[p]`, this value is needed: keep it on the (implicit) stack and advance `p` by 1.
   - Otherwise, this value isn't needed: append `"Pop"` to `res` to remove it again.
3. Return `res`.

---

## 7. Pseudocode

```text
p = 0
res = []

for val = 1 to n
    if p == length(target)
        break

    res.append("Push")

    if val == target[p]
        p += 1
    else
        res.append("Pop")

return res
```

---

## 8. Python Solution

```python
class Solution:
    def buildArray(self, target: List[int], n: int) -> List[str]:
        p = 0  # index of the next target element to match
        res = []
        for val in range(1, n + 1):
            if p == len(target):
                break

            if val == target[p]:
                res.append("Push")
                p += 1
            else:
                res.append("Push")
                res.append("Pop")

        return res
```

---

## 9. Dry Run

Example:

```text
target = [1, 3], n = 3
```

| Step | Stream Value (`val`) | `p` Before | Action | `p` After | Why? |
|------|----------------------|------------|--------|-----------|------|
| 1 | `1` | `0` (`target[0]=1`) | Push | `1` | `val == target[p]` — needed, keep it |
| 2 | `2` | `1` (`target[1]=3`) | Push, Pop | `1` | `val != target[p]` — not needed, pop it back off |
| 3 | `3` | `1` (`target[1]=3`) | Push | `2` | `val == target[p]` — needed, keep it |
| — | `4` | `2 == len(target)` | — | — | Loop breaks before reading `val=4` |

Result: `["Push", "Push", "Pop", "Push"]`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- The loop runs at most `n` times (the stream is bounded by `n`), and each iteration does `O(1)` work — one or two appends and a comparison.

### Space Complexity

```text
O(n)
```

Why?

- No auxiliary stack is kept — only the pointer `p` (`O(1)`) — but the returned `res` list holds up to two operations per stream value, so it's `O(n)` in the size of the output itself (unavoidable, since the result must be returned).
