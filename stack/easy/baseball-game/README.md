# Problem

Name: Baseball Game

Difficulty: Easy

----------------------------------------

# Pattern
Stack — Auxiliary State

----------------------------------------

# Recognition

Idea
- Every operation only ever cares about the *most recent* score(s) still
  on the record — "previous score", "previous two scores" — which is
  exactly what a stack's top (and the one below it) gives you.
- `"C"` undoes the last record by popping it; `"D"` and `"+"` derive a
  new score from what's currently on top and push it; an integer just
  gets pushed directly.
- The record itself doubles as the stack — no separate structure is
  needed to track "current scores," since invalidated scores are
  actually removed, not just skipped.

Steps

- INIT: `stack = []`
- SCAN: for each `ch` in `operations`
- UNDO: if `ch == "C"`, pop the top of `stack` — discards the last score
- DOUBLE: if `ch == "D"`, push `2 * stack[-1]`
- SUM: if `ch == "+"`, push `stack[-2] + stack[-1]`
- RECORD: otherwise, push `int(ch)`
- RETURN: `sum(stack)`

Mistakes


----------------------------------------

# Complexity

- Time: `O(n)` — n = len(operations); each operation does `O(1)` work
  (push/pop/peek), plus a final `O(n)` sum over the stack
- Space: `O(n)` — worst case every operation pushes, so the stack holds
  up to `n` scores
