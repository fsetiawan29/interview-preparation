# Problem: Maximum Number of Vowels in a Substring of Given Length

## 1. Problem Understanding

### Problem Summary

Given a string `s` and an integer `k`, find the maximum number of vowel letters (`a`, `e`, `i`, `o`, `u`) in any substring of `s` with length `k`.

### Input

- A string `s`
- An integer `k`

### Output

- An integer: the maximum vowel count across all substrings of length `k`.

### Constraints

- `1 <= s.length <= 10^5`
- `s` consists of lowercase English letters.
- `1 <= k <= s.length`

### Example

Input:

```text
s = "abciiidef", k = 3
```

Output:

```text
3
```

Explanation: The substring "iii" contains 3 vowel letters.

Manual walkthrough:

```text
s: a b c i i i d e f

Windows of size 3:
"abc" -> 1 vowel (a)
"bci" -> 1 vowel (i)
"cii" -> 2 vowels (i,i)
"iii" -> 3 vowels (i,i,i)  <- best
"iid" -> 2 vowels
"ide" -> 2 vowels
"def" -> 1 vowel

-> 3
```

---

# 2. Key Insight

## What makes this problem difficult?

Recounting vowels in every length-`k` window from scratch is `O(n * k)` — wasteful, since consecutive windows overlap in all but two characters.

## Key Observation

Sliding the window by one position only changes two characters: the one leaving on the left and the one entering on the right. The vowel count only needs to be adjusted for those two characters, not recomputed for the whole window.

Example:

```text
window "abc" vowel count = 1 (just 'a')
slide right by one -> drop 'a' (was a vowel, count -1), add 'i' (is a vowel, count +1)
new count = 1 - 1 + 1 = 1  (window is now "bci")
```

## Why does this observation help?

Each slide becomes `O(1)` work (two membership checks against a fixed vowel set) instead of an `O(k)` recount, bringing the total scan down to `O(n)`.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture a window of fixed width `k` sliding across the string, carrying a running vowel tally. Each slide only asks two yes/no questions — "was the outgoing character a vowel?" and "is the incoming character a vowel?" — and adjusts the tally accordingly.

```text
s:  a  b  c  i  i  i  d  e  f
   [-----]
   window_vowels = 1 ('a')

slide ->

s:  a  b  c  i  i  i  d  e  f
      [-----]
   window_vowels = 1 - 1 (drop 'a', a vowel) + 1 (add 'i', a vowel) = 1
```

The best count seen across all slides is the answer.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize left = 0, right = k - 1
window_vowels = count of vowels in s[0..k-1]
best = window_vowels
   │
   ▼
Is right < len(s) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
best = max(best, window_vowels)   Return best
 │
 ▼
Is right == len(s) - 1 ?
 │
┌─┴───────┐
│         │
Yes       No
│         │
▼         ▼
break     Is s[left] a vowel? -> window_vowels -= 1
          Is s[right + 1] a vowel? -> window_vowels += 1
          left += 1, right += 1
          │
          └──▶ (back to "Is right < len(s) ?")
```

Explanation of each decision:

- The window starts already covering indices `0..k-1`, so its vowel count is computed once up front with a helper.
- `best` is updated with the *current* window's count before checking whether to slide further.
- Stopping when `right` reaches the last index avoids sliding past the end of the string.
- Each slide independently checks the outgoing and incoming characters — both may or may not be vowels.

---

# 5. Plain English Algorithm

1. Set `left = 0` and `right = k - 1` — the first window covers indices `0` through `k - 1`.
2. Count the vowels in that first window as `window_vowels`; initialize `best` to it.
3. While `right` is within the string:
   - Update `best` with the larger of `best` and `window_vowels`.
   - If `right` is already the last index, stop sliding.
   - Otherwise, if `s[left]` (leaving the window) is a vowel, decrement `window_vowels`; if `s[right + 1]` (entering the window) is a vowel, increment `window_vowels`. Advance both `left` and `right`.
4. Return `best`.

---

# 6. Pseudocode

```text
VOWELS = {a, e, i, o, u}

left = 0
right = k - 1
window_vowels = count of vowels in s[0 .. k-1]
best = window_vowels

while right < length(s)
    best = max(best, window_vowels)

    if right == length(s) - 1
        break

    if s[left] in VOWELS
        window_vowels--

    if s[right + 1] in VOWELS
        window_vowels++

    left++
    right++

return best
```

---

# 7. Python Solution

```python
class Solution:
    VOWELS = {'a', 'e', 'i', 'o', 'u'}

    def maxVowels(self, s: str, k: int) -> int:
        left = 0
        right = k - 1
        window_vowels = self.countVowel(s, k)
        best = window_vowels

        while right < len(s):
            best = max(best, window_vowels)

            if right == len(s) - 1:
                break

            if self.isVowel(s[left]):
                window_vowels -= 1

            if self.isVowel(s[right + 1]):
                window_vowels += 1

            left += 1
            right += 1

        return best

    def isVowel(self, char: str) -> bool:
        return char in self.VOWELS

    def countVowel(self, s: str, k: int) -> int:
        res = 0
        for char in s[:k]:
            if self.isVowel(char):
                res += 1
        return res
```

---

# 8. Dry Run

Example:

```text
s = "abciiidef", k = 3
```

| Step | left, right | window_vowels | best | Action | Why? |
|------|-------------|-----------------|------|--------|------|
| 1 | 0, 2 | 1 | 1 | s[0]='a' vowel -> -1=0; s[3]='i' vowel -> +1=1 | slide to "bci" |
| 2 | 1, 3 | 1 | 1 | s[1]='b' not vowel; s[4]='i' vowel -> +1=2 | slide to "cii" |
| 3 | 2, 4 | 2 | 2 | s[2]='c' not vowel; s[5]='i' vowel -> +1=3 | slide to "iii" |
| 4 | 3, 5 | 3 | 3 | s[3]='i' vowel -> -1=2; s[6]='d' not vowel | slide to "iid" |
| 5 | 4, 6 | 2 | 3 | s[4]='i' vowel -> -1=1; s[7]='e' vowel -> +1=2 | slide to "ide" |
| 6 | 5, 7 | 2 | 3 | s[5]='i' vowel -> -1=1; s[8]='f' not vowel | slide to "def" |
| 7 | 6, 8 | 1 | 3 | right == last index (8) -> break | no more windows |

Result: `best = 3`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(s)`; the initial window's vowel count is computed once in `O(k)`.
- Each subsequent slide does `O(1)` work (two membership checks), and there are `O(n)` slides total.

### Space Complexity

```text
O(1)
```

Why?

- `VOWELS` is a fixed-size set of 5 characters.
- Only `window_vowels`, `best`, and two pointers are used as extra state.
