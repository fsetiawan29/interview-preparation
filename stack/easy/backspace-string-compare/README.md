# Problem

Name: Backspace String Compare

Difficulty: Easy

----------------------------------------

# Pattern
Stack — Matching Pairs (also: Two Pointer, `O(1)` space)

----------------------------------------

# Recognition

Idea
- `'#'` deletes the character typed right before it — the most recent
  unresolved character — which is exactly a stack's `pop`. Building each
  string's final text with a stack and comparing the two results gives
  a straightforward `O(n + m)` time, `O(n + m)` space solution.
- The `O(1)`-space follow-up avoids building either string: walk both
  strings **from the right**, since a `'#'` only ever affects characters
  *before* it. Skip a run of "pending backspaces" before comparing each
  next surviving character, and only stop once both pointers exhaust —
  a length mismatch after backspaces is itself a `False`.

Steps

- Stack (`backspaceCompare_stack`)
  - BUILD: `build(s)` — for each `ch` in `s`, if `ch == "#"` pop the
    stack (when non-empty), otherwise push `ch`
  - COMPARE: `return build(s) == build(t)` — equal final stacks means
    equal typed text
- Two Pointer (`backspaceCompare_twopointer`)
  - INIT: `i = len(s) - 1`, `j = len(t) - 1`, `skip_s = skip_t = 0`
  - LOOP: while `i >= 0 or j >= 0` — keep going until *both* pointers
    are exhausted, not just one
  - ADVANCE `i`: while `i >= 0`, if `s[i] == "#"` increment `skip_s` and
    decrement `i`; elif `skip_s > 0`, consume a pending skip
    (`skip_s -= 1`, `i -= 1`); else `break` — `i` now points at the next
    surviving character (or `-1`)
  - ADVANCE `j`: same logic, mirrored for `t`/`skip_t`
  - COMPARE: if both pointers are still in range and `s[i] != t[j]`,
    return `False`; if only one is in range, the strings have different
    surviving lengths — return `False`
  - STEP: `i -= 1`, `j -= 1`
  - RETURN: `True` if the loop finishes without a mismatch

Mistakes
- Using the two-pointer approach:
  - I mistakenly initialized the `skip` variables inside the outer loop, causing them to reset on every iteration.
    - The `skip_s` and `skip_t` counters should be initialized **before** the outer loop so they persist while processing each string.

  - I used the wrong condition for the outer loop.
    - **Incorrect**
      ```python
      while i >= 0 and j >= 0:
      ```
    - **Correct**
      ```python
      while i >= 0 or j >= 0:
      ```
    - The loop should continue until **both** pointers are exhausted. Using `and` stops the loop as soon as one pointer reaches the beginning, leaving the other string unprocessed.


----------------------------------------

# Complexity

- Stack: Time `O(n + m)` — n = len(s), m = len(t), one pass to build
  each stack; Space `O(n + m)` — both built stacks are kept to compare
- Two Pointer: Time `O(n + m)` — each pointer walks its string at most
  once, backspaces skip characters instead of rescanning; Space `O(1)`
  — only the two pointers and two skip counters are tracked, satisfying
  the follow-up
