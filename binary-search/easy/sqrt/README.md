# Problem: Sqrt(x)

## 1. Problem Understanding

### Problem Summary

Given a non-negative integer `x`, return its square root rounded **down**
to the nearest integer. Built-in exponent functions/operators (e.g.
`pow(x, 0.5)`, `x ** 0.5`) may not be used.

### Input

- A non-negative integer, `x`.

### Output

- A non-negative integer: `floor(sqrt(x))`.

### Constraints

- `0 <= x <= 2^31 - 1`

### Example

Input:

```text
x = 4
```

Output:

```text
2
```

Manual walkthrough:

```text
sqrt(4) = 2 exactly, so the floor is 2.
```

Input:

```text
x = 8
```

Output:

```text
2
```

Manual walkthrough:

```text
sqrt(8) = 2.82842..., and rounding down gives 2.
```

---

## 2. Brute Force Approach

### Idea

Try every integer `i` starting from `0`, and stop as soon as `(i+1) *
(i+1)` overshoots `x`. The last `i` whose square didn't overshoot is the
floor of the square root.

### Pseudocode

```text
function solve(x)
    i = 0
    while (i + 1) * (i + 1) <= x
        i = i + 1
    return i
```

### Complexity Analysis

#### Time Complexity

```text
O(sqrt(x))
```

Why?

- The loop advances `i` one step at a time until `i` reaches
  `floor(sqrt(x))`, so it runs `O(sqrt(x))` times.

#### Space Complexity

```text
O(1)
```

Why?

- Only the counter `i` is kept.

### Why this isn't good enough

With `x` up to `2^31 - 1`, `sqrt(x)` can be around `46340` — the sequence
of squares `0, 1, 4, 9, 16, ...` is strictly increasing, and checking it
one candidate at a time throws away that ordering instead of exploiting it
with a halving search.

---

## 3. Key Insight

### What makes this problem difficult?

There's no array to search — the "sequence" is implicit: the squares of
`0, 1, 2, 3, ...`. The task also isn't a plain exact-match search, since
`x` usually isn't a perfect square; the answer is the *last* candidate
whose square doesn't exceed `x`.

### Key Observation

`f(i) = i * i` is monotonically increasing, so the condition `i * i <= x`
is `True` for small `i` and flips to `False` once `i` passes
`floor(sqrt(x))` — a `True...True False...False` pattern. That's exactly
the shape a boundary binary search looks for: find the last index where
the condition still holds.

Example:

```text
x = 8

i:         0  1  2  3  4
i*i <= x:  T  T  T  F  F
                 ^ last True, floor(sqrt(8)) = 2
```

### Why does this observation help?

Binary search can narrow directly to that boundary in `O(log x)` steps
instead of walking through every candidate: at each `mid`, checking `mid *
mid <= x` says whether the answer is `mid` or something larger, or
strictly smaller than `mid`.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a number line of candidate roots from `0` to `x`, each mapped to
whether its square still fits under `x`. The candidates split into a
"fits" block followed by a "doesn't fit" block; binary search walks
straight to the seam between them, remembering the last candidate that
still fit.

```text
[0 ................. 8]  x = 8
      mid=4  4*4=16 > 8 -> doesn't fit -> search [0, 3]
         mid=1  1*1=1 <= 8 -> fits, remember 1 -> search [2, 3]
            mid=2  2*2=4 <= 8 -> fits, remember 2 -> search [3, 3]
               mid=3  3*3=9 > 8 -> doesn't fit -> search empty
      answer: last remembered fit = 2
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
left = 0, right = x, ans = 0
   │
   ▼
left <= right ?
   │
 ┌─┴──────────────────┐
 │                     │
No                    Yes
 │                     │
 ▼                     ▼
Return ans         mid = left + (right-left)//2
                        │
                        ▼
                  mid * mid <= x ?
                        │
              ┌─────────┴─────────┐
              │                   │
             Yes                 No
     (mid fits, might      (mid overshoots,
      still improve)        answer is smaller)
              │                   │
              ▼                   ▼
        ans = mid            right = mid - 1
        left = mid + 1
        (keep looking
         for a larger fit)
              │                   │
              └─────────┬─────────┘
                        ▼
              (loop back to left <= right ?)
```

Explanation of each decision:

- `left > right` is the base case — the search space is exhausted; `ans`
  holds the largest `mid` whose square didn't exceed `x` (or `0` if none
  did beyond the trivial `0 * 0 <= x`, which always holds).
- `mid * mid <= x` means `mid` is a valid candidate — record it as the
  best answer so far, then keep searching further right in case a larger
  candidate also fits.
- `mid * mid > x` means `mid` overshoots — the answer must be smaller,
  narrow to `[left, mid-1]`.

---

## 6. Plain English Algorithm

1. Set `left = 0`, `right = x`, and `ans = 0`.
2. While `left <= right`:
   - Compute `mid = left + (right - left) / 2`.
   - If `mid * mid <= x`, `mid` is a valid candidate — set `ans = mid` and
     move `left` to `mid + 1` to check for an even larger fit.
   - Otherwise `mid * mid > x` — move `right` to `mid - 1`.
3. Return `ans`, the largest integer whose square didn't exceed `x`.

---

## 7. Pseudocode

```text
function solve(x)
    left, right, ans = 0, x, 0
    while left <= right
        mid = left + (right - left) // 2
        if mid * mid <= x
            ans = mid
            left = mid + 1
        else
            right = mid - 1
    return ans
```

---

## 8. Go Solution

```go
package solution

func mySqrt(x int) int {
	// TODO: implement
	return 0
}
```

---

## 9. Dry Run

Example:

```text
x = 8
```

| Step | `left` | `right` | `mid` | `mid*mid` | Action | Why? |
|------|--------|---------|-------|-----------|--------|------|
| 1 | 0 | 8 | 4 | 16 | `16 > 8` -> `right = 3` | `mid` overshoots |
| 2 | 0 | 3 | 1 | 1 | `1 <= 8` -> `ans = 1`, `left = 2` | `mid` fits, look for a larger one |
| 3 | 2 | 3 | 2 | 4 | `4 <= 8` -> `ans = 2`, `left = 3` | `mid` fits, look for a larger one |
| 4 | 3 | 3 | 3 | 9 | `9 > 8` -> `right = 2` | `mid` overshoots |
| 5 | 3 | 2 | — | — | `left > right` -> return `ans` | Search space exhausted |

Result: `2`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(log x)
```

Why?

- Each iteration halves the candidate range `[left, right]`, so the loop
  runs `O(log x)` times regardless of how large `x` is.

### Space Complexity

```text
O(1)
```

Why?

- Only a fixed number of variables (`left`, `right`, `mid`, `ans`) are
  used, regardless of input size.
