# Problem: Valid Perfect Square

## 1. Problem Understanding

### Problem Summary

Given a positive integer `num`, determine whether it is a perfect square —
the product of some integer with itself (e.g. `16 = 4 * 4`). Built-in
library functions such as `sqrt` may not be used.

### Input

- A positive integer, `num`.

### Output

- A boolean: `true` if `num` is a perfect square, `false` otherwise.

### Constraints

- `1 <= num <= 2^31 - 1`

### Example

Input:

```text
num = 16
```

Output:

```text
true
```

Manual walkthrough:

```text
4 * 4 = 16, and 4 is an integer, so 16 is a perfect square.
```

Input:

```text
num = 14
```

Output:

```text
false
```

Manual walkthrough:

```text
3 * 3 = 9 and 4 * 4 = 16 -> no integer squared equals 14, so it isn't a
perfect square.
```

---

## 2. Brute Force Approach

### Idea

Try every integer `i` starting from `1`, squaring it, until the square
reaches or passes `num`. If some `i * i` lands exactly on `num`, it's a
perfect square; if the square overshoots first, it isn't.

### Pseudocode

```text
function solve(num)
    i = 1
    while i * i <= num
        if i * i == num
            return true
        i = i + 1
    return false
```

### Complexity Analysis

#### Time Complexity

```text
O(sqrt(num))
```

Why?

- The loop stops as soon as `i` reaches `sqrt(num)`, so at most
  `sqrt(num)` iterations run.

#### Space Complexity

```text
O(1)
```

Why?

- Only the loop counter `i` is kept.

### Why this isn't good enough

With `num` up to `2^31 - 1`, `sqrt(num)` can be around `46340` — small
enough to pass, but it's still checking every candidate one at a time when
the candidates form a monotonic sequence (`i * i` only grows as `i`
grows), which is exactly the shape binary search is built for.

---

## 3. Key Insight

### What makes this problem difficult?

There's no array to search — the "sequence" being searched is implicit:
the squares `1, 4, 9, 16, 25, ...`. Recognizing that this implicit
sequence is strictly increasing is what turns a scan into a search.

### Key Observation

`f(i) = i * i` is strictly increasing for `i >= 1`, so comparing `mid *
mid` to `num` behaves exactly like comparing `nums[mid]` to `target` in an
ordinary sorted-array binary search — except the "array" is generated on
the fly instead of stored.

Example:

```text
num = 16

mid=8 -> 8*8=64 > 16 -> the root is smaller -> search [1, 7]
mid=4 -> 4*4=16 == 16 -> found
```

### Why does this observation help?

Binary search applies directly over the candidate range `[1, num]`:
each comparison discards half of the remaining candidates, cutting the
search from `O(sqrt(num))` down to `O(log num)`.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a number line of candidate roots from `1` to `num`, each one
mapped to its square. Squaring is monotonic, so probing the middle
candidate and comparing its square to `num` tells which half of the line
still could contain the true root — same as probing the middle of a
sorted array.

```text
[1 ................. 16]  num = 16
      mid=8  8*8=64 > 16 -> root is smaller -> search [1, 7]
         mid=4  4*4=16 == 16 -> found
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
left = 1, right = num
   │
   ▼
left <= right ?
   │
 ┌─┴──────────────────┐
 │                     │
No                    Yes
 │                     │
 ▼                     ▼
Return false       mid = left + (right-left)//2
                        │
                        ▼
                  mid * mid vs num ?
                        │
              ┌─────────┼─────────────┐
              │         │             │
          square      square        square
           == num      < num         > num
              │         │             │
              ▼         ▼             ▼
        Return true  left = mid+1  right = mid-1
                     (root is        (root is
                      larger)         smaller)
                        │             │
                        └──────┬──────┘
                               ▼
                     (loop back to left <= right ?)
```

Explanation of each decision:

- `left > right` is the base case — the search space is empty, so no
  integer squared equals `num`.
- `mid * mid == num` means `mid` is the exact integer square root —
  `num` is a perfect square.
- `mid * mid < num` means the true root is larger than `mid` — narrow to
  `[mid+1, right]`.
- `mid * mid > num` means the true root is smaller than `mid` — narrow to
  `[left, mid-1]`.

---

## 6. Plain English Algorithm

1. Set `left = 1` and `right = num`.
2. While `left <= right`:
   - Compute `mid = left + (right - left) / 2` and `square = mid * mid`.
   - If `square == num`, return `true` — `mid` is the integer square root.
   - If `square < num`, the root is larger — move `left` to `mid + 1`.
   - If `square > num`, the root is smaller — move `right` to `mid - 1`.
3. If the loop ends without a match, no integer's square equals `num` —
   return `false`.

---

## 7. Pseudocode

```text
function solve(num)
    left, right = 1, num
    while left <= right
        mid = left + (right - left) // 2
        square = mid * mid
        if square == num
            return true
        elif square < num
            left = mid + 1
        else
            right = mid - 1
    return false
```

---

## 8. Go Solution

```go
package solution

func isPerfectSquare(num int) bool {
	left := 1
	right := num

	for left <= right {
		mid := left + (right-left)/2
		square := mid * mid

		if square == num {
			return true
		} else if square < num {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return false
}

func isPerfectSquareBruteForce(num int) bool {
	for i := 1; i*i <= num; i++ {
		if i*i == num {
			return true
		}
	}

	return false
}
```

---

## 9. Dry Run

Example:

```text
num = 16
```

| Step | `left` | `right` | `mid` | `mid*mid` | Action | Why? |
|------|--------|---------|-------|-----------|--------|------|
| 1 | 1 | 16 | 8 | 64 | `64 > 16` -> `right = 7` | Root is smaller than 8 |
| 2 | 1 | 7 | 4 | 16 | `16 == 16` -> Return `true` | `mid` is the exact root |

Result: `true`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(log num)
```

Why?

- Each iteration halves the candidate range `[left, right]`, so the loop
  runs `O(log num)` times regardless of how large `num` is.

### Space Complexity

```text
O(1)
```

Why?

- Only a fixed number of variables (`left`, `right`, `mid`, `square`) are
  used, regardless of input size.
