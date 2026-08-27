# Problem: Arranging Coins

## 1. Problem Understanding

### Problem Summary

You have `n` coins and want to build a staircase where row `i` (1-indexed)
uses exactly `i` coins. Rows must be filled in order, and the last row is
allowed to be incomplete. Return how many **complete** rows can be built.

### Input

- A single integer, `n` — the total number of coins.

### Output

- An integer — the number of complete rows.

### Constraints

- `1 <= n <= 2^31 - 1`

### Example

Input:

```text
n = 5
```

Output:

```text
2
```

Manual walkthrough:

```text
Row 1 needs 1 coin  -> 4 coins left -> complete
Row 2 needs 2 coins -> 2 coins left -> complete
Row 3 needs 3 coins -> only 2 left  -> incomplete
2 complete rows.
```

Input:

```text
n = 8
```

Output:

```text
3
```

Manual walkthrough:

```text
Row 1 needs 1 coin  -> 7 coins left -> complete
Row 2 needs 2 coins -> 5 coins left -> complete
Row 3 needs 3 coins -> 2 coins left -> complete
Row 4 needs 4 coins -> only 2 left  -> incomplete
3 complete rows.
```

---

## 2. Brute Force Approach

### Idea

Simulate building the staircase one row at a time: keep subtracting `i`
coins for row `i` as long as there are enough coins left, and stop as soon
as a row can't be completed.

### Pseudocode

```text
function solve(n)
    row = 0
    remaining = n
    while remaining >= row + 1
        row = row + 1
        remaining = remaining - row
    return row
```

### Complexity Analysis

#### Time Complexity

```text
O(sqrt(n))
```

Why?

- Row `k` consumes `k(k+1)/2` coins in total, so the loop stops once `row`
  reaches roughly `sqrt(2n)` — the number of iterations grows with the
  square root of `n`, not `n` itself.

#### Space Complexity

```text
O(1)
```

Why?

- Only the running counters `row` and `remaining` are kept.

### Why this isn't good enough

`n` can be as large as `2^31 - 1`, so `sqrt(n)` is still only around
`65536` iterations — small enough to pass, but the total coins used through
row `k` is a closed-form, monotonically increasing function of `k`. That
monotonic shape means the answer can be found directly with binary search
instead of walking row by row.

---

## 3. Key Insight

### What makes this problem difficult?

There's no array to search — the candidates are row counts `k = 0, 1, 2,
...`, and "feasible" means "the coins needed for `k` complete rows fit
within `n`". Recognizing that this feasibility condition is monotonic is
what turns a simulation into a search.

### Key Observation

The total coins needed for `k` complete rows is `f(k) = k(k+1)/2`, which is
strictly increasing in `k`. So `f(k) <= n` is a condition that is `true`
for every small enough `k` and `false` for every `k` beyond some point —
exactly the `True...True False...False` shape binary search on the answer
needs.

Example:

```text
n = 8

k=4 -> f(4) = 10 > 8  -> too many rows -> search smaller k
k=3 -> f(3) = 6  <= 8 -> 3 rows fit    -> try a larger k
k=3 is the largest feasible k
```

### Why does this observation help?

Instead of accumulating coins row by row (`O(sqrt(n))`), binary search over
the candidate row count `k` in `[0, n]` and test `f(mid) <= n` directly,
cutting the search down to `O(log n)`.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a number line of candidate row counts from `0` to `n`, each mapped
to the total coins it would consume (`k(k+1)/2`). That mapping only grows
as `k` grows, so probing the middle candidate and comparing its coin cost
to `n` tells which half of the line can still contain the true answer —
same as probing the middle of a sorted array.

```text
[0 ..................... n]  candidate row counts
      mid -> f(mid) vs n -> keep the half that can still be feasible
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
left = 0, right = n
   │
   ▼
left <= right ?
   │
 ┌─┴──────────────────┐
 │                     │
No                    Yes
 │                     │
 ▼                     ▼
Return left        mid = left + (right-left)//2
                        │
                        ▼
                  mid*(mid+1)/2 vs n ?
                        │
              ┌─────────┴─────────┐
              │                   │
          <= n                  > n
              │                   │
              ▼                   ▼
        left = mid+1         right = mid-1
        (mid rows fit,       (mid rows overshoot,
         try more)            need fewer)
              │                   │
              └─────────┬─────────┘
                         ▼
              (loop back to left <= right ?)
```

Explanation of each decision:

- `left > right` is the base case — the search space is exhausted, and
  `left` has settled one past the largest feasible row count, which equals
  the answer.
- `mid*(mid+1)/2 <= n` means `mid` complete rows fit within `n` coins —
  the answer might be `mid` or larger, so narrow to `[mid+1, right]`.
- `mid*(mid+1)/2 > n` means `mid` rows overshoot `n` — the answer must be
  smaller, so narrow to `[left, mid-1]`.

---

## 6. Plain English Algorithm

1. Set `left = 0` and `right = n`.
2. While `left <= right`:
   - Compute `mid = left + (right - left) / 2` and `coins = mid * (mid + 1)
     / 2`.
   - If `coins <= n`, `mid` rows are feasible — move `left` to `mid + 1` to
     try for more complete rows.
   - If `coins > n`, `mid` rows overshoot — move `right` to `mid - 1`.
3. When the loop ends, `left` is the largest row count whose coin cost
   doesn't exceed `n` — return `left`.

---

## 7. Pseudocode

```text
function solve(n)
    left, right = 0, n
    while left <= right
        mid = left + (right - left) // 2
        coins = mid * (mid + 1) // 2
        if coins <= n
            left = mid + 1
        else
            right = mid - 1
    return left
```

---

## 8. Go Solution

```go
package solution

func arrangeCoins(n int) int {
	// TODO: implement
	return 0
}
```

---

## 9. Dry Run

Example:

```text
n = 8
```

| Step | `left` | `right` | `mid` | `mid*(mid+1)/2` | Action | Why? |
|------|--------|---------|-------|-----------------|--------|------|
| 1 | 0 | 8 | 4 | 10 | `10 > 8` -> `right = 3` | 4 rows overshoot |
| 2 | 0 | 3 | 1 | 1 | `1 <= 8` -> `left = 2` | 1 row fits, look for more |
| 3 | 2 | 3 | 2 | 3 | `3 <= 8` -> `left = 3` | 2 rows fit, look for more |
| 4 | 3 | 3 | 3 | 6 | `6 <= 8` -> `left = 4` | 3 rows fit, look for more |
| 5 | 4 | 3 | — | — | `left > right` -> return `left` | Search space exhausted |

Result: `3`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(log n)
```

Why?

- Each iteration halves the candidate range `[left, right]`, so the loop
  runs `O(log n)` times regardless of how large `n` is.

### Space Complexity

```text
O(1)
```

Why?

- Only a fixed number of variables (`left`, `right`, `mid`, `coins`) are
  used, regardless of input size.
