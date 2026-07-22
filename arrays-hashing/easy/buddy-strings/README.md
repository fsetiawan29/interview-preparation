# Problem

Name: Buddy Strings

Difficulty: Easy

----------------------------------------

# Pattern
Hash Set + Index Tracking (two approaches: index pair and diff-tuple list)

----------------------------------------

# Recognition

Idea
- If length is not same, `return False`
- If `s == goal`
    - If there is at least duplicate letter, then it's `return True`
    - Else `return False`
- Else
    - Exactly two mismatches and they must cross match
    - Else `return False`

- There are 2 approaches to check the cross match values
    - Provide `count`, `first`, and `second`. If count != 2, `return False`
    - Using list and each element of the list is tuple `diff: List[Tuple[str, str]]`


Steps

- GUARD: if `len(s) != len(goal)`, return `False`
- EQUAL CASE: if `s == goal`, scan `s` with a `seen` hash set — return `True` as soon as a repeated character is found (a swap of two equal letters leaves `s` unchanged), else return `False`
- MISMATCH CASE (`buddyStrings_hashset`): scan both strings tracking `count`, `first`, `second` — the indices of the first two mismatches
  - if `count != 2`, return `False`
  - return `s[first] == goal[second] and s[second] == goal[first]` — the two mismatches must be each other's mirror
- MISMATCH CASE (`buddyStrings_diffcount`): scan both strings collecting mismatches as `(s[i], goal[i])` tuples into `diff`, short-circuiting `False` once `len(diff) > 2`
  - if `len(diff) != 2`, return `False`
  - return `diff[0][0] == diff[1][1] and diff[0][1] == diff[1][0]`

Mistakes
- Forget to check the length of both strings


----------------------------------------

# Complexity

- Time: `O(n)` — n = len(s), one pass to compare characters (plus one pass over `s` in the equal case to check for a duplicate)
- Space: `O(1)` — bounded by the lowercase alphabet for `seen`; `O(1)` for the two tracked indices or the diff list, which never holds more than 2-3 entries
