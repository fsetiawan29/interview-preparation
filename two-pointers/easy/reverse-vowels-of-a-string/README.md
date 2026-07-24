# Problem: Reverse Vowels of a String

## 1. Problem Understanding

### Problem Summary

Given a string `s`, reverse only the vowels in it. Every consonant, digit, and symbol stays exactly where it is — only the vowel characters swap positions with each other.

### Input

- A string `s`

### Output

- A new string with the same characters, but vowels reversed in place.

### Constraints

- `1 <= s.length <= 3 * 10^5`
- `s` consists of printable ASCII characters.

### Example

Input:

```text
s = "IceCreAm"
```

Output:

```text
"AceCreIm"
```

Manual walkthrough:

```text
Original

I c e C r e A m

Vowels found, left to right: I, e, e, A

Reverse that list of vowels: A, e, e, I

Write them back into the vowel positions, left to right

↓

A c e C r e I m
```

---

## 2. Brute Force Approach

### Idea

Collect every vowel into a separate list first, reverse that list, then walk the string a second time and drop the reversed vowels back into their original vowel positions.

### Pseudocode

```text
VOWELS = {a, e, i, o, u} (case-insensitive)
n = length(s)
s_array = list(s)

vowel_list = []
for i = 0 to n - 1
    if s_array[i].lower() in VOWELS
        vowel_list.append(s_array[i])

reverse(vowel_list)

v = 0
for i = 0 to n - 1
    if s_array[i].lower() in VOWELS
        s_array[i] = vowel_list[v]
        v += 1

return join(s_array)
```

### Complexity Analysis

#### Time Complexity

```text
O(n)
```

Why?

- Three linear passes: one to extract vowels, one (bounded by the vowel count) to reverse them, one to reinsert.

#### Space Complexity

```text
O(n)
```

Why?

- `s_array` is needed regardless (strings are immutable), plus a separate `vowel_list` holding up to `n` extra characters.

### Why this isn't good enough

This is still `O(n)` time, same as the optimized version, but it makes three separate passes and allocates a whole second list just for the vowels. Two pointers walking in from both ends, each skipping non-vowels and swapping the vowels they land on directly, does the extraction and reinsertion in a single combined pass with no separate vowel list.

---

## 3. Key Insight

### What makes this problem difficult?

Consonants must not move, so we can't just filter out vowels, reverse them, and splice them back in with a simple linear scan — we need to know, for every vowel position from the left, which vowel from the right should land there.

### Key Observation

If we walk in from **both ends at once**, the first vowel found from the left and the first vowel found from the right are exactly the pair that needs to swap — they are mirror images of each other in the final vowel ordering.

Example:

```text
I c e C r e A m
↑             ↑
l             r

l skips nothing (I is a vowel)
r skips nothing (m is not a vowel, keep moving r left)
```

### Why does this observation help?

Instead of extracting vowels into a separate list, reversing it, and reinserting, two pointers can swap vowels directly in place as they're discovered — each pointer independently skips non-vowels until it lands on one, and only then does a swap happen.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture two scanners starting at opposite ends of the string, each hunting for the next vowel in their direction. Whenever both have found one, they trade places and both keep hunting inward.

```text
I  c  e  C  r  e  A  m
↑                    ↑
l                    r

l is on 'I' (vowel) — stop
r is on 'm' (not a vowel) — keep moving left

I  c  e  C  r  e  A  m
↑                 ↑
l                 r

r is on 'A' (vowel) — stop, both found

Swap I <-> A

A  c  e  C  r  e  I  m
```

Both pointers only ever care about vowels — consonants are invisible to them except as something to skip over.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Initialize
l = 0
r = len(s) - 1
s_array = list(s)
   │
   ▼
Is l < r ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is s_array[l] a vowel?   Done — join s_array into a string
 │
 ┌─┴──────────┐
 │            │
No            Yes
 │            │
 ▼            ▼
l += 1     Is s_array[r] a vowel?
 │            │
 │          ┌─┴──────────┐
 │          │             │
 │         No            Yes
 │          │             │
 │          ▼             ▼
 │       r -= 1        Swap s_array[l], s_array[r]
 │          │             │
 │          │             ▼
 │          │          l += 1, r -= 1
 │          │             │
 └──────────┴─────────────┘
             │
             ▼
      (back to "Is l < r ?")
```

Explanation of each decision:

- If `s_array[l]` isn't a vowel, only `l` advances — `r` must wait since its vowel status hasn't been checked yet.
- If `s_array[r]` isn't a vowel, only `r` retreats.
- Only once **both** land on vowels do they swap and both move — this guarantees no vowel is skipped or double-counted.

---

## 6. Plain English Algorithm

1. Convert the string to a list so characters can be swapped in place.
2. Point `l` at the first index and `r` at the last index.
3. While `l` is left of `r`:
   - If `s[l]` isn't a vowel, move `l` right and check again.
   - If `s[r]` isn't a vowel, move `r` left and check again.
   - Once both `l` and `r` sit on vowels, swap them, then move `l` right and `r` left.
4. Join the list back into a string and return it.

---

## 7. Pseudocode

```text
vowels = {a, e, i, o, u} (case-insensitive)

l = 0
r = length(s) - 1
s_array = list(s)

while l < r
    if s_array[l].lower() not in vowels
        l++
        continue

    if s_array[r].lower() not in vowels
        r--
        continue

    swap s_array[l], s_array[r]
    l++
    r--

return join(s_array)
```

---

## 8. Python Solution

```python
class Solution:
    def reverseVowels(self, s: str) -> str:
        vowels = {'a', 'e', 'i', 'o', 'u'}
        l = 0
        r = len(s) - 1
        s_array = list(s)
        while l < r:
            if s_array[l].lower() not in vowels:
                l += 1
                continue

            if s_array[r].lower() not in vowels:
                r -= 1
                continue

            s_array[l], s_array[r] = s_array[r], s_array[l]
            l += 1
            r -= 1

        return "".join(s_array)
```

---

## 9. Dry Run

Example:

```text
s = "leetcode"
```

| Step | Pointer(s) | Current Values | Action | Array State | Why? |
|------|------------|-----------------|--------|-------------|------|
| 1 | l=0, r=7 | 'l', 'e' | l is not vowel, l += 1 | l,e,e,t,c,o,d,e | 'l' skipped |
| 2 | l=1, r=7 | 'e', 'e' | Swap | l,e,e,t,c,o,d,e | Both vowels (no visible change, same char) |
| 3 | l=2, r=6 | 'e', 'd' | r is not vowel, r -= 1 | l,e,e,t,c,o,d,e | 'd' skipped |
| 4 | l=2, r=5 | 'e', 'o' | Swap | l,e,o,t,c,e,d,e | Both vowels |
| 5 | l=3, r=4 | 't', 'c' | l not vowel, then r not vowel | l,e,o,t,c,e,d,e | Both skipped, pointers cross |
| 6 | l=4, r=3 | — | Stop | l,e,o,t,c,e,d,e | `l < r` is false |

Result: `"leotcede"`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- Each pointer moves at most `n` positions total across skips and swaps.
- Every character is visited at most once by each pointer.

### Space Complexity

```text
O(n)
```

Why?

- `s` is immutable in Python, so it must be copied into `s_array` before swaps can happen.
- Excluding the output string, the extra state (`l`, `r`, `vowels`) is `O(1)`.
