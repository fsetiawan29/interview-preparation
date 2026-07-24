# Problem: Valid Palindrome

## 1. Problem Understanding

### Problem Summary

Given a string `s`, determine if it is a palindrome after converting all uppercase letters to lowercase and removing all non-alphanumeric characters.

### Input

- A string `s`

### Output

- `true` if `s` is a palindrome under those rules, `false` otherwise.

### Constraints

- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters.

### Example

Input:

```text
s = "A man, a plan, a canal: Panama"
```

Output:

```text
true
```

Manual walkthrough:

```text
Original

"A man, a plan, a canal: Panama"

Keep only letters/digits, lowercase them (conceptually):

"amanaplanacanalpanama"

Compare front and back:

a...a, m...m, a...a, n...n, ... meets in the middle, all match

↓

true
```

---

# 2. Key Insight

## What makes this problem difficult?

Punctuation, spaces, and casing get in the way of a direct comparison. Building a fully cleaned copy of the string works, but costs `O(n)` extra space — an `O(1)`-space solution needs to skip irrelevant characters *while* comparing, without ever materializing the cleaned string.

## Key Observation

Two pointers starting from both ends can each independently **skip past non-alphanumeric characters** before comparing — the cleaning and the comparing happen in the same pass, character by character.

Example:

```text
"A man, a plan, a canal: Panama"
 ↑                             ↑
 l                             r

s[l]='A' is alnum -> stop here
s[r]='a' is alnum -> stop here
compare 'a' == 'a' (case-insensitive) -> match, move both inward
```

## Why does this observation help?

Instead of building a cleaned string up front, each pointer scans forward/backward *only as needed*, skipping punctuation and whitespace on the fly. The comparison happens directly on the original string, so no extra copy is ever created.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture two readers starting at opposite ends of the sentence, each ignoring punctuation and spaces as if they were invisible. They only "stop" on a letter or digit, then compare (case-insensitively) with the other reader before both step one more position inward.

```text
A  ␣m  a  n  ,  ␣a  ...  ␣P  a  n  a  m  a
↑                                        ↑
l                                        r

l is on 'A' (alnum) -> stop
r is on 'a' (alnum) -> stop
compare (case-insensitive): match -> both move inward
```

Whenever a pointer lands on punctuation or whitespace, it simply steps past it without comparing anything.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize l = 0, r = len(s) - 1
   │
   ▼
Is l < r ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is s[l] alnum ?       Done — return true
 │
┌─┴────────┐
│          │
No         Yes
│          │
▼          ▼
l += 1     Is s[r] alnum ?
continue    │
           ┌─┴────────┐
           │          │
          No         Yes
           │          │
           ▼          ▼
        r -= 1    Is s[l].lower() == s[r].lower() ?
        continue   │
                   ┌─┴────────┐
                   │          │
                  No         Yes
                   │          │
                   ▼          ▼
              Return false   l += 1, r -= 1
                              │
                              └──▶ (back to "Is l < r ?")
```

Explanation of each decision:

- A non-alphanumeric character at `l` only advances `l` — `r`'s status hasn't been checked yet.
- A non-alphanumeric character at `r` only retreats `r`.
- Only once both `l` and `r` sit on alphanumeric characters does the actual comparison happen.
- Any mismatch immediately returns `false`; reaching `l >= r` without a mismatch means every pair matched.

---

# 5. Plain English Algorithm

1. Point `l` at the first index and `r` at the last index of `s`.
2. While `l` is left of `r`:
   - If `s[l]` isn't alphanumeric, advance `l` and check again.
   - If `s[r]` isn't alphanumeric, retreat `r` and check again.
   - Once both land on alphanumeric characters, compare them case-insensitively — a mismatch means `s` isn't a palindrome.
   - On a match, advance `l` and retreat `r`.
3. If the loop finishes without a mismatch, `s` is a palindrome.

---

# 6. Pseudocode

```text
l = 0
r = length(s) - 1

while l < r
    if not isalnum(s[l])
        l++
        continue

    if not isalnum(s[r])
        r--
        continue

    if lower(s[l]) != lower(s[r])
        return false

    l++
    r--

return true
```

---

# 7. Python Solution

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1

        while left < right:
            cl = s[left]
            cr = s[right]
            if not cl.isalnum():
                left += 1
                continue

            if not cr.isalnum():
                right -= 1
                continue

            if cl.lower() != cr.lower():
                return False

            left += 1
            right -= 1

        return True
```

---

# 8. Dry Run

Example:

```text
s = "race a car"
```

| Step | Pointer(s) | Current Values | Action | Why? |
|------|------------|-----------------|--------|------|
| 1 | l=0, r=9 | 'r', 'r' | Match, l=1, r=8 | Both alnum, equal |
| 2 | l=1, r=8 | 'a', 'a' | Match, l=2, r=7 | Both alnum, equal |
| 3 | l=2, r=7 | 'c', 'c' | Match, l=3, r=6 | Both alnum, equal |
| 4 | l=3, r=6 | 'e', ' ' | r not alnum, r=5 | Skip space |
| 5 | l=3, r=5 | 'e', 'a' | Mismatch | Return false |

Result: `false`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- Each pointer moves at most `n` positions total, across both skips and compares.
- Every character is visited at most once by each pointer.

### Space Complexity

```text
O(1)
```

Why?

- No cleaned copy of the string is built.
- Only the two pointers `left` and `right` are used as extra state.
