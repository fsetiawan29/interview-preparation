# Problem: Buddy Strings

## 1. Problem Understanding

### Problem Summary

Given two strings `s` and `goal`, determine if swapping exactly two characters within `s` can make it equal to `goal`.

### Input

- A string `s`
- A string `goal`

### Output

- `true` if exactly one swap of two characters in `s` can produce `goal`, `false` otherwise.

### Constraints

- `1 <= s.length, goal.length <= 2 * 10^4`
- `s` and `goal` consist of lowercase letters.

### Example

Input:

```text
s = "ab", goal = "ba"
```

Output:

```text
true
```

Manual walkthrough:

```text
s    = a b
goal = b a

Swap indices 0 and 1 in s:

a b -> b a

Result matches goal -> true
```

---

## 2. Brute Force Approach

### Idea

Try every pair of positions in `s`, swap them, and check whether the result equals `goal`.

### Pseudocode

```text
n = length(s)
if n != length(goal)
    return false

for i = 0 to n - 1
    for j = i + 1 to n - 1
        candidate = copy of s with characters at i and j swapped
        if candidate == goal
            return true

return false
```

### Complexity Analysis

#### Time Complexity

```text
O(n^3)
```

Why?

- There are `O(n^2)` pairs `(i, j)` to try swapping.
- Building the swapped copy and comparing it to `goal` costs `O(n)` per pair.

#### Space Complexity

```text
O(n)
```

Why?

- Each candidate swapped string is a fresh `O(n)`-sized copy of `s`.

### Why this isn't good enough

Every pair is tested by materializing and comparing a whole new string, even though a swap only ever changes two positions. Scanning once to record the mismatched positions (at most two, and their mirror relationship) replaces all those `O(n)` rebuild-and-compare operations with a single `O(n)` pass.

---

## 3. Key Insight

### What makes this problem difficult?

It's tempting to think a single swap can fix any two mismatched positions, but that's only true if the mismatches are each other's mirror image. If `s == goal` already, a swap is still required (or forbidden) depending on whether a repeated letter exists to "swap with itself."

### Key Observation

There are really only two shapes this problem can take:

- If `s` and `goal` are already equal, a valid no-op swap exists only if some character repeats (swap two identical letters, string stays the same).
- If they differ, there must be **exactly two** mismatched positions, and those two positions must be mirror images of each other.

Example:

```text
s    = "ab"
goal = "ba"

Mismatches: index 0 ('a' vs 'b'), index 1 ('b' vs 'a')
s[0]==goal[1] ('a'=='a') and s[1]==goal[0] ('b'=='b') -> mirror match -> true
```

### Why does this observation help?

Instead of trying every possible swap (`O(n^2)`), a single left-to-right pass can count mismatches and remember their positions. If there are anything other than exactly two mismatches, or they aren't mirrors of each other, the answer is immediately `false`.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture scanning both strings side by side, tallying every position where they disagree. Stop as soon as you find a third disagreement — three or more mismatches can never be fixed by a single swap. If exactly two show up, check whether swapping those two specific letters in `s` would fix both spots at once.

```text
s:    a  b
goal: b  a
      ↑  ↑
   mismatch #1, mismatch #2

Swapping s[0] and s[1] turns "ab" into "ba" -> matches goal
```

If instead three or more disagreements appear, no single swap can fix them all — the picture immediately resolves to `false`.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Is len(s) != len(goal) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return false      Is s == goal ?
                       │
                     ┌─┴─────────────┐
                     │                │
                    Yes               No
                     │                │
                     ▼                ▼
              Any repeated       Scan for mismatches,
              character in s?    tracking first, second, count
                     │                │
                   ┌─┴───┐            ▼
                   │      │      Is count == 2 ?
                  Yes     No          │
                   │      │        ┌─┴───────┐
                   ▼      ▼        │          │
              Return   Return    No          Yes
              true     false      │            │
                                  ▼            ▼
                            Return false   Is s[first]==goal[second]
                                            and s[second]==goal[first]?
                                                  │
                                                ┌─┴───────┐
                                                │          │
                                               Yes         No
                                                │          │
                                                ▼          ▼
                                          Return true  Return false
```

Explanation of each decision:

- Different lengths make a swap impossible regardless of content — checked first.
- If the strings are already equal, a swap is only "valid" if it can be a no-op — which requires a repeated character to swap with itself.
- If the strings differ, exactly two mismatched positions are required; any other count (0, 1, or 3+) fails.
- The two mismatches must be mirror images: `s[first]` must equal `goal[second]` and vice versa.

---

## 6. Plain English Algorithm

1. If `s` and `goal` have different lengths, return `false`.
2. If `s` equals `goal`, scan `s` for any repeated character (using a hash set) — if one exists, return `true` (swap it with itself), otherwise return `false`.
3. Otherwise, scan both strings together, recording the index of every mismatch and counting them.
4. If the mismatch count isn't exactly 2, return `false`.
5. Check whether the two mismatched positions are mirror images: `s[first] == goal[second]` and `s[second] == goal[first]`. Return the result.

---

## 7. Pseudocode

```text
if length(s) != length(goal)
    return false

if s == goal
    seen = empty set
    for char in s
        if char in seen
            return true
        seen.add(char)
    return false

count = 0
first = -1
second = -1

for i in range(length(s))
    if s[i] != goal[i]
        count++
        if count == 1
            first = i
        else
            second = i

if count != 2
    return false

return s[first] == goal[second] and s[second] == goal[first]
```

---

## 8. Python Solution

```python
class Solution:
    def buddyStrings_hashset(self, s: str, goal: str) -> bool:
        if len(s) != len(goal):
            return False

        if s == goal:
            # check for duplicate letters
            seen = set()
            for char in s:
                if char in seen:
                    return True

                seen.add(char)

            return False

        count = 0
        first = -1
        second = -1
        for i in range(len(s)):
            if s[i] != goal[i]:
                count += 1

                if count == 1:
                    first = i
                else:
                    second = i

        if count != 2:
            return False

        return s[first] == goal[second] and s[second] == goal[first]
```

---

## 9. Dry Run

Example:

```text
s = "ab", goal = "ba"
```

| Step | Index | s[i] | goal[i] | Action | Why? |
|------|-------|------|---------|--------|------|
| 1 | — | — | — | len(s)==len(goal), not equal to each other | Guard passes, skip the equal-string branch |
| 2 | i=0 | 'a' | 'b' | Mismatch, count=1, first=0 | First disagreement recorded |
| 3 | i=1 | 'b' | 'a' | Mismatch, count=2, second=1 | Second disagreement recorded |
| 4 | — | — | — | count==2, check mirror | Exactly two mismatches found |
| 5 | — | — | — | s[first]='a'==goal[second]='a' and s[second]='b'==goal[first]='b' | Both mirror checks pass |

Result: `true`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- One pass to compare `s` and `goal` for mismatches (or one pass to check for a repeated character in the equal case), where `n = len(s)`.

### Space Complexity

```text
O(1)
```

Why?

- The mismatch-tracking path only stores a few indices (`first`, `second`, `count`).
- The equal-string path uses a `seen` set bounded by the lowercase alphabet, which is a constant size regardless of `n`.
