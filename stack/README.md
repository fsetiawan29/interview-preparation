# Stack

## What is this pattern?

A stack is a LIFO (last-in, first-out) structure: push onto the top, pop off
the top, peek at the top without removing it. Problems reach for a stack
whenever the answer depends on **the most recent unresolved item**, not the
whole history — matching the last open bracket, undoing the last operation,
or comparing each element only against what's still "active" above it.

Use this pattern when the problem is about:
- **Matching/nesting structure** — parentheses, tags, nested expressions
  where the most recently opened thing must be the next one closed
- **Simulating a process with undo** — backspaces, "go back" navigation,
  removing adjacent duplicates
- **Parsing expressions** — numbers, operators, and nested groups that need
  to be evaluated inside-out
- Finding, for every element, the **next/previous greater or smaller**
  element (monotonic stack) — the classic "how far until it gets warmer"
  shape
- **Greedy character/digit removal** to build the smallest/largest possible
  result, popping from a stack while the current element makes a previously
  pushed one obsolete

## The general shape

Almost every stack problem is a variation of this skeleton:

```python
def solve(items):
    stack = []

    for item in items:
        # 1. CHECK — does the current item resolve/conflict with the top
        #    of the stack? (closing bracket, a bigger value, a pop signal)
        while stack and should_pop(stack[-1], item):
            stack.pop()

        # 2. PUSH — the current item becomes the new "most recent unresolved"
        stack.append(item)

    return stack
```

Two steps, always in this order:

1. **CHECK/RESOLVE first** — before pushing, see whether the current item
   closes out (or invalidates) whatever's on top. This is what makes
   `stack[-1]` meaningful — it's always "the nearest unresolved thing."
2. **PUSH second** — once nothing more can be resolved against the top,
   the current item goes on the stack as the new most-recent item.

## Common sub-patterns

**Matching pairs** (parentheses/brackets)
*(problems: [valid-parentheses](./easy/valid-parentheses), [remove-outermost-parentheses](./easy/remove-outermost-parentheses))*
```python
pairs = {')': '(', ']': '[', '}': '{'}
stack = []
for ch in s:
    if ch in pairs:
        if not stack or stack.pop() != pairs[ch]:
            return False
    else:
        stack.append(ch)
return not stack
```

**Auxiliary stack** (track extra state alongside the main one)
*(problems: Min Stack)*
```python
stack, mins = [], []
def push(x):
    stack.append(x)
    mins.append(x if not mins else min(x, mins[-1]))
def pop():
    mins.pop()
    return stack.pop()
```

**Expression parsing** (calculator / decode string)
*(problems: Evaluate Reverse Polish Notation, Basic Calculator, Decode String)*
```python
stack = []
num, sign = 0, 1
for ch in s:
    if ch.isdigit():
        num = num * 10 + int(ch)
    elif ch in "+-":
        stack.append(sign * num)
        num, sign = 0, 1 if ch == "+" else -1
    elif ch == "(":
        # push current total/sign, reset, recurse into the group
        ...
    elif ch == ")":
        # pop the saved state, fold the group's result back in
        ...
```

**Monotonic stack** (next greater/smaller element)
*(problems: Daily Temperatures, Next Greater Element I/II, Online Stock Span)*
```python
stack = []  # indices, values kept decreasing top-to-bottom
result = [0] * len(nums)
for i, n in enumerate(nums):
    while stack and nums[stack[-1]] < n:
        j = stack.pop()
        result[j] = i - j  # distance, or `n` itself, depending on the ask
    stack.append(i)
```

**Previous/next smaller element** (histogram / rectangle)
*(problems: Largest Rectangle in Histogram, Maximal Rectangle, Trapping Rain Water)*
```python
stack = []  # indices, heights kept increasing top-to-bottom
best = 0
for i, h in enumerate(heights + [0]):  # sentinel forces a final flush
    while stack and heights[stack[-1]] > h:
        height = heights[stack.pop()]
        width = i if not stack else i - stack[-1] - 1
        best = max(best, height * width)
    stack.append(i)
```

**Stack + greedy** (remove k digits / remove duplicate letters)
*(problems: Remove K Digits, Remove Duplicate Letters, Smallest Subsequence of Distinct Characters)*
```python
stack = []
for i, ch in enumerate(s):
    while stack and stack[-1] > ch and pop_is_still_beneficial(stack, ch, i):
        stack.pop()
    stack.append(ch)
```

## Complexity

- **Time:** `O(n)` amortized for monotonic-stack problems — each element is
  pushed and popped at most once, so the total work across the whole loop
  is `O(n)` even though there's a `while` inside a `for`.
- **Space:** `O(n)` worst case for the stack itself (e.g. a strictly
  increasing/decreasing input never pops until the end).

## Common pitfalls

- **Popping from an empty stack** — always guard with `if stack` /
  `while stack and ...` before `stack[-1]` or `stack.pop()`.
- **Forgetting to check leftover stack contents at the end** — e.g. valid
  parentheses isn't done just because the loop finished; an unclosed `(`
  leaves something on the stack, so the real check is `not stack`.
- **Monotonic stack in the wrong direction** — an increasing stack finds
  the next *smaller* element; a decreasing stack finds the next *greater*
  element. Mixing these up silently gives the wrong answer instead of
  crashing.
- **Off-by-one converting stack gaps into distances/widths** — `i - j` vs
  `i - j - 1` depending on whether the popped index itself is included.
- **Missing the sentinel value** — histogram-style problems often need a
  trailing `0` (or `-1`) appended so the last run of unpopped bars gets
  flushed out of the stack.
- **Popping greedily without a remaining-count check** — in remove-k-digits
  / remove-duplicate-letters, you can only pop the top if there's still
  enough of that character left later in the string to push back on.

## Problems in this folder

### Easy

- [valid-parentheses](./easy/valid-parentheses) — push open brackets, and
  on a close bracket check it matches whatever's on top of the stack;
  valid only if the stack is empty once the string is fully scanned.
- [baseball-game](./easy/baseball-game) — the general check/push skeleton
  itself: `"C"` pops, `"D"`/`"+"` derive a new score from the top (and
  second-from-top) and push it, an integer just gets pushed directly;
  the record's running sum is just `sum(stack)` at the end.
- [backspace-string-compare](./easy/backspace-string-compare) — build
  each string with a stack (`'#'` pops, otherwise push) and compare the
  results; the `O(1)`-space follow-up swaps the stack for two pointers
  walking both strings from the right, skipping a run of pending
  backspaces before each character comparison.
- [remove-outermost-parentheses](./easy/remove-outermost-parentheses) —
  a stack's *size* (a running `depth` counter) is enough to spot each
  primitive block's outermost pair, without pushing actual characters:
  skip a `'('` that takes depth `0 → 1` and a `')'` that takes depth
  `1 → 0`, keep every other character.

### Medium

- [build-array-with-stack-operations](./medium/build-array-with-stack-operations) —
  since both the stream and `target` are strictly increasing, a real
  stack is never needed: a single pointer into `target` tracks what's
  still wanted, every stream value gets `"Push"`ed, and anything that
  doesn't match the pointer is immediately `"Pop"`ped back off.

See [PROGRESS.md](./PROGRESS.md) for the full curriculum (7 levels, 30
problems) and the recommended learning order.
