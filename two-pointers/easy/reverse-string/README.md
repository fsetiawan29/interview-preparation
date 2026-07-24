# Problem: Reverse String

## 1. Problem Understanding

### Problem Summary

Given a character array `s`, reverse it **in-place**.

The reversal must be done with `O(1)` extra memory, meaning we cannot allocate another array to hold the result.

### Input

- A character array `s`

### Output

- Modify `s` in-place so its elements are reversed.

### Constraints

- `1 <= s.length <= 10^5`
- `s[i]` is a printable ASCII character.

### Example

Input:

```text
s = ["h","e","l","l","o"]
```

Output:

```text
["o","l","l","e","h"]
```

Manual walkthrough:

```text
Original

["h","e","l","l","o"]

Swap outermost pair (index 0 and 4)

↓

["o","e","l","l","h"]

Swap next pair (index 1 and 3)

↓

["o","l","l","e","h"]

Middle index (2) has no partner left — stop
```

---

# 2. Key Insight

## What makes this problem difficult?

A naive reversal might build a brand-new array by reading `s` back to front, but that costs `O(n)` extra space — the problem explicitly forbids it.

## Key Observation

Reversing an array is just **swapping mirrored positions**: index `0` with index `n-1`, index `1` with index `n-2`, and so on, until the two positions meet or cross.

Example:

```text
Original

[h, e, l, l, o]
 ↑           ↑
 l           r

Swap l and r

[o, e, l, l, h]
```

## Why does this observation help?

Because every swap only touches two positions at a time, we never need a second array — the array reverses itself from the outside in, using two pointers that walk toward each other.

---

# 3. Mental Model

> What picture should I imagine in my head?

Imagine two hands reaching in from opposite ends of the array, swapping whatever they're holding, then both stepping one position closer to the middle.

```text
[h, e, l, l, o]
 ↑           ↑
 l           r

Step 1: swap

[o, e, l, l, h]
 ↑           ↑
 l           r

Step 2: move inward

[o, e, l, l, h]
    ↑     ↑
    l     r

Step 3: swap

[o, l, l, e, h]
    ↑     ↑
    l     r

Step 4: move inward — l meets/crosses r, stop
```

The two pointers never look outside the segment between them — once `l` is no longer strictly less than `r`, every position has already been placed.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize
l = 0
r = len(s) - 1
   │
   ▼
Is l < r ?
   │
 ┌─┴─────────────┐
 │               │
Yes              No
 │               │
 ▼               ▼
Swap s[l], s[r]  Done — s is fully reversed
 │
 ▼
l += 1, r -= 1
 │
 └──▶ (back to "Is l < r ?")
```

Explanation of each decision:

- `l < r` means there are still two distinct positions to swap.
- Once `l == r` (odd length) or `l > r` (even length), every pair has already been swapped — the middle element, if any, is already in its correct place.

---

# 5. Plain English Algorithm

1. Point `l` at the first index and `r` at the last index.
2. While `l` is still to the left of `r`:
   - Swap the characters at `l` and `r`.
   - Move `l` one step right, move `r` one step left.
3. Stop once `l` and `r` meet or cross — the array is fully reversed.

---

# 6. Pseudocode

```text
l = 0
r = length(s) - 1

while l < r
    swap s[l], s[r]
    l++
    r--
```

---

# 7. Python Solution

```python
class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        l = 0
        r = len(s) - 1
        while l < r:
            s[l], s[r] = s[r], s[l]
            l += 1
            r -= 1
```

---

# 8. Dry Run

Example:

```text
s = ["h","e","l","l","o"]
```

| Step | Pointer(s) | Current Values | Action | Array State | Why? |
|------|------------|-----------------|--------|-------------|------|
| 1 | l=0, r=4 | 'h', 'o' | Swap | [o,e,l,l,h] | Outermost pair not yet matched |
| 2 | l=1, r=3 | 'e', 'l' | Swap | [o,l,l,e,h] | Next pair inward not yet matched |
| 3 | l=2, r=2 | 'l' | Stop | [o,l,l,e,h] | `l < r` is false, loop ends |

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- Each pointer moves at most `n / 2` times.
- Every element is touched exactly once, by exactly one swap.

### Space Complexity

```text
O(1)
```

Why?

- Swapping happens in place on the given array.
- Only the two pointers `l` and `r` are used as extra state.
