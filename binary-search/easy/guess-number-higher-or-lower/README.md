# Problem: Guess Number Higher or Lower

## 1. Problem Understanding

### Problem Summary

A number guessing game: a number `pick` between `1` and `n` (inclusive) has
already been chosen. There's no direct access to `pick` — instead, a
pre-built API `guess(num)` can be called with a guess and it reports how
that guess compares to `pick`:

- `-1` if `num` is higher than `pick`
- `1` if `num` is lower than `pick`
- `0` if `num` equals `pick`

Find `pick` using as few calls to `guess` as possible.

### Input

- An integer `n` — the upper bound of the range `[1, n]`.
- Implicitly, access to a black-box function `guess(num int) int`.

### Output

- The integer `pick` that `guess` was built around.

### Constraints

- `1 <= n <= 2^31 - 1`
- `1 <= pick <= n`

### Example

Input:

```text
n = 10, pick = 6
```

Output:

```text
6
```

Manual walkthrough:

```text
guess(5)  -> 1   (5 is lower than pick, pick is higher)
guess(8)  -> -1  (8 is higher than pick, pick is lower)
guess(6)  -> 0   (found it)
```

---

## 2. Brute Force Approach

### Idea

Ask about every number from `1` to `n` in order until `guess` reports `0`.

### Pseudocode

```text
function solve(n)
    for num = 1 to n
        if guess(num) == 0
            return num
```

### Complexity Analysis

#### Time Complexity

```text
O(n)
```

Why?

- In the worst case (`pick == n`), every value from `1` to `n` is guessed
  before finding a match — that's `n` calls to `guess`.

#### Space Complexity

```text
O(1)
```

Why?

- Only a loop counter is kept; no extra structure is used.

### Why this isn't good enough

With `n` up to `2^31 - 1`, a linear scan could take over two billion calls
to `guess`. The problem's whole premise — a hidden number being compared
against guesses — is a signal that the search space can be pruned much
faster than one-at-a-time.

---

## 3. Key Insight

### What makes this problem difficult?

`pick` can't be inspected directly, only compared against via `guess`.
That comparison, though, is exactly a three-way comparison (`<`, `>`,
`==`) against a fixed value inside a fixed range `[1, n]`.

### Key Observation

`guess(num)` behaves like comparing `num` to `pick` in a sorted sequence
`1, 2, 3, ..., n`. Every number below `pick` returns `1` ("go higher") and
every number above `pick` returns `-1` ("go lower"), so the range is
monotonic around `pick` the same way a sorted array is monotonic around a
search target.

Example:

```text
n = 10, pick = 6

num:        1  2  3  4  5  6  7  8  9  10
guess(num): 1  1  1  1  1  0 -1 -1 -1 -1
                          ^ pick, the only 0
```

### Why does this observation help?

Since the range `[1, n]` is effectively "sorted" with respect to `guess`,
binary search applies directly: pick the midpoint, let `guess` say which
half `pick` is in, and discard the other half.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a number line from `1` to `n` with a hidden marker somewhere on
it. Each guess is a probe that returns "warmer, go right", "warmer, go
left", or "found it" — like the classic "higher/lower" guessing game,
solved by always probing the middle of what's left.

```text
[1 ......... 10]  pick = 6
     mid=5  guess(5)=1 (go higher) -> search [6, 10]
        mid=8  guess(8)=-1 (go lower) -> search [6, 7]
           mid=6  guess(6)=0 -> found
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
low = 1, high = n
   │
   ▼
low <= high ?
   │
 ┌─┴──────────────────┐
 │                     │
No                    Yes
 │                     │
 ▼                     ▼
(unreachable       mid = low + (high-low)//2
 per constraints)       │
                        ▼
                  guess(mid) == 0 ?
                        │
              ┌─────────┼─────────┐
              │         │         │
             Yes    guess(mid)   otherwise
              │      == 1        (guess(mid) == -1)
              ▼      (pick higher)  (pick lower)
          Return mid    │             │
                        ▼             ▼
                  low = mid+1    high = mid-1
                        │             │
                        └──────┬──────┘
                               ▼
                     (loop back to low <= high ?)
```

Explanation of each decision:

- `guess(mid) == 0` means `mid` is `pick` — return it immediately.
- `guess(mid) == 1` means `mid` is lower than `pick` — narrow to
  `[mid+1, high]`.
- `guess(mid) == -1` means `mid` is higher than `pick` — narrow to
  `[low, mid-1]`.
- The loop is guaranteed to terminate with a match before `low > high`
  because the problem guarantees `pick` exists in `[1, n]`.

---

## 6. Plain English Algorithm

1. Set `low = 1` and `high = n`.
2. While `low <= high`:
   - Compute `mid = low + (high - low) / 2`.
   - Call `result = guess(mid)`.
   - If `result == 0`, return `mid` — it's `pick`.
   - If `result == 1`, `pick` is higher than `mid` — move `low` to
     `mid + 1`.
   - If `result == -1`, `pick` is lower than `mid` — move `high` to
     `mid - 1`.
3. The loop always finds `pick` before the range empties, since `pick` is
   guaranteed to be within `[1, n]`.

---

## 7. Pseudocode

```text
function solve(n)
    low, high = 1, n
    while low <= high
        mid = low + (high - low) // 2
        result = guess(mid)
        if result == 0
            return mid
        elif result == 1
            low = mid + 1
        else
            high = mid - 1
```

---

## 8. Go Solution

```go
package solution

/**
 * Forward declaration of guess API.
 * @param   num   your guess
 * @return        -1 if num is higher than the picked number
 *                  1 if num is lower than the picked number
 *                  0 if num is equal to the picked number
 * func guess(num int) int;
 */

func guessNumber(n int) int {
	low, high := 1, n

	for low <= high {
		mid := low + (high-low)/2
		result := guess(mid)

		if result == 0 {
			return mid
		} else if result == 1 {
			low = mid + 1
		} else {
			high = mid - 1
		}
	}

	return -1
}

func guessNumberBruteForce(n int) int {
	for num := 1; num <= n; num++ {
		if guess(num) == 0 {
			return num
		}
	}

	return -1
}
```

---

## 9. Dry Run

Example:

```text
n = 10, pick = 6
```

| Step | `low` | `high` | `mid` | `guess(mid)` | Action | Why? |
|------|-------|--------|-------|--------------|--------|------|
| 1 | 1 | 10 | 5 | 1 | `low = 6` | `pick` is higher than 5 |
| 2 | 6 | 10 | 8 | -1 | `high = 7` | `pick` is lower than 8 |
| 3 | 6 | 7 | 6 | 0 | Return `6` | `mid` equals `pick` |

Result: `6`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(log n)
```

Why?

- Each call to `guess` halves the remaining range `[low, high]`, so the
  number of calls before finding `pick` is `O(log n)`.

### Space Complexity

```text
O(1)
```

Why?

- Only a fixed number of variables (`low`, `high`, `mid`) are used,
  regardless of `n`.
