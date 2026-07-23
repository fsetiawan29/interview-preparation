# Problem

Name: Valid Parentheses

Difficulty: Easy

----------------------------------------

# Pattern
Stack — Matching Pairs

----------------------------------------

# Recognition

Idea
- An open bracket is only resolved by the *most recent* unclosed open
  bracket, which is exactly what a stack's top gives you.
- Push every open bracket. On a close bracket, it must match whatever's
  currently on top of the stack — if it doesn't (or the stack is empty),
  the string is invalid.
- The string is only fully valid if every open bracket got matched, i.e.
  the stack is empty once the loop finishes.

Steps

- INIT: `mapping` — open bracket → its matching close bracket
- INIT: `stack = []`
- SCAN: for each `ch` in `s`
- PUSH: if `ch in mapping` (`ch` is an open bracket), push it onto `stack`
- CHECK: otherwise (`ch` is a close bracket) — if `stack` is empty,
  return `False` (nothing to match); pop the stack and if
  `mapping[popped] != ch`, return `False` (mismatched type)
- RETURN: `not stack` — `True` only if every pushed bracket got matched

Mistakes


----------------------------------------

# Complexity

- Time: `O(n)` — n = len(s), one pass over the string, each character
  pushed/popped at most once
- Space: `O(n)` worst case — an all-open-brackets string pushes every
  character onto the stack
