# Problem: Isomorphic Strings

## 1. Problem Understanding

### Problem Summary

Given two strings `s` and `t`, determine if they are isomorphic — every character in `s` can be replaced to get `t`, with no two characters mapping to the same character, but a character may map to itself.

### Input

- A string `s`
- A string `t`

### Output

- `true` if `s` and `t` are isomorphic, `false` otherwise.

### Constraints

- `1 <= s.length <= 5 * 10^4`
- `t.length == s.length`
- `s` and `t` consist of any valid ASCII character.

### Example

Input:

```text
s = "egg", t = "add"
```

Output:

```text
true
```

Manual walkthrough:

```text
s: e g g
t: a d d

Map e -> a
Map g -> d
g -> d again, consistent with the earlier mapping

Every occurrence of a character in s maps to the same character in t,
and no two distinct characters in s map to the same character in t -> true
```

---

## 2. Brute Force Approach

### Idea

Without building any maps, directly verify the bijection property between every pair of positions: `s[i] == s[j]` must hold exactly when `t[i] == t[j]` holds, for every pair `(i, j)`.

### Pseudocode

```text
n = length(s)

for i = 0 to n - 1
    for j = 0 to i - 1
        if (s[j] == s[i]) != (t[j] == t[i])
            return false

return true
```

### Complexity Analysis

#### Time Complexity

```text
O(n^2)
```

Why?

- For each index `i`, comparing it against every earlier index `j` costs `O(n)`, across `n` indices.

#### Space Complexity

```text
O(1)
```

Why?

- No extra data structure is used beyond the loop indices.

### Why this isn't good enough

Every new index is checked against *every* earlier index individually. Two hash maps (`s -> t` and `t -> s`) let each index be checked against its single recorded mapping in `O(1)`, replacing the `O(n)` per-index comparison with a constant-time lookup.

---

## 3. Key Insight

### What makes this problem difficult?

A valid isomorphism must hold in **both directions** — `s[i]` must always map to the same `t[i]`, but also no two different characters of `s` may map to the same character of `t`. Checking only one direction misses cases like `s="ab"`, `t="aa"`, where `a` and `b` would both map to `a`.

### Key Observation

Two hash maps, one for each direction (`s -> t` and `t -> s`), can each catch a different kind of violation as we scan once, left to right.

Example:

```text
s = "ab", t = "aa"

i=0: s[0]='a' -> t[0]='a'   record a->a, a->a
i=1: s[1]='b' -> t[1]='a'   b is unmapped so far, but t[1]='a' is ALREADY mapped to 'a' in t_to_s
     t_to_s['a'] == 'a', but s[1] == 'b' != 'a' -> conflict! -> false
```

### Why does this observation help?

Checking both `s_to_t` and `t_to_s` at every index catches a mismatch in either direction the moment it happens, without needing a second pass or extra bookkeeping — a single left-to-right scan is enough.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture two logbooks, one recording "this letter from `s` always becomes this letter in `t`," and another recording the reverse. At every position, check both logbooks: does `s[i]` already have an entry that disagrees with `t[i]`? Does `t[i]` already have an entry that disagrees with `s[i]`? Only if both logbooks stay consistent do you write the new entry and move on.

```text
s: e  g  g
t: a  d  d

s_to_t: {}         -> e:a written        -> g:d written        -> g already maps to d, matches
t_to_s: {}         -> a:e written        -> d:g written        -> d already maps to g, matches

No conflicts found -> true
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Initialize s_to_t = {}, t_to_s = {}
   │
   ▼
For each i in range(len(s)):
   │
   ▼
Is s[i] in s_to_t AND s_to_t[s[i]] != t[i] ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return false     Is t[i] in t_to_s AND t_to_s[t[i]] != s[i] ?
                       │
                     ┌─┴─────────┐
                     │            │
                    Yes           No
                     │            │
                     ▼            ▼
               Return false   Record s_to_t[s[i]]=t[i]
                               and t_to_s[t[i]]=s[i]
                                   │
                                   ▼
                             Next i (or Done)
                                   │
                                   ▼
                             Return true
```

Explanation of each decision:

- The first check catches "one character of `s` maps to two different characters of `t`."
- The second check catches "two different characters of `s` map to the same character of `t`."
- Only when both checks pass does the pair get recorded (or re-confirmed, if it's a repeat mapping already stored).

---

## 6. Plain English Algorithm

1. Create two empty maps: `s_to_t` and `t_to_s`.
2. Scan both strings together by index `i`, from `0` to `len(s) - 1`:
   - If `s[i]` is already mapped in `s_to_t` to something other than `t[i]`, return `false`.
   - If `t[i]` is already mapped in `t_to_s` to something other than `s[i]`, return `false`.
   - Otherwise, record `s_to_t[s[i]] = t[i]` and `t_to_s[t[i]] = s[i]`.
3. If the scan completes without conflict, return `true`.

---

## 7. Pseudocode

```text
s_to_t = empty map
t_to_s = empty map

for i in range(length(s))
    if s[i] in s_to_t and s_to_t[s[i]] != t[i]
        return false

    if t[i] in t_to_s and t_to_s[t[i]] != s[i]
        return false

    s_to_t[s[i]] = t[i]
    t_to_s[t[i]] = s[i]

return true
```

---

## 8. Python Solution

```python
class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        s_to_t = {}
        t_to_s = {}

        for i in range(len(s)):
            if s[i] in s_to_t and s_to_t[s[i]] != t[i]:
                return False

            if t[i] in t_to_s and t_to_s[t[i]] != s[i]:
                return False

            s_to_t[s[i]] = t[i]
            t_to_s[t[i]] = s[i]

        return True
```

---

## 9. Dry Run

Example:

```text
s = "egg", t = "add"
```

| Step | i | s[i] | t[i] | Action | Why? |
|------|---|------|------|--------|------|
| 1 | 0 | 'e' | 'a' | Record e->a, a->e | Neither mapped yet |
| 2 | 1 | 'g' | 'd' | Record g->d, d->g | Neither mapped yet |
| 3 | 2 | 'g' | 'd' | No conflict, re-confirm mapping | s_to_t['g']=='d' and t_to_s['d']=='g', both consistent |

Result: `true`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(s)`; a single pass over both strings, with `O(1)` average map lookups per index.

### Space Complexity

```text
O(k)
```

Why?

- `k` is the number of distinct characters across `s` and `t`, bounded by the ASCII alphabet.
