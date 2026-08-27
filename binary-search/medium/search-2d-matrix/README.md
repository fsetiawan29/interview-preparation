# Problem: Search a 2D Matrix

## 1. Problem Understanding

### Problem Summary

Given an `m x n` integer matrix `matrix` where each row is sorted in
non-decreasing order, and the first integer of each row is greater than the
last integer of the previous row, return `true` if `target` exists in the
matrix, `false` otherwise. The solution must run in `O(log(m * n))` time.

### Input

- A 2D integer matrix, `matrix`, with rows sorted ascending and rows
  themselves in ascending order relative to each other.
- An integer, `target`.

### Output

- `true` if `target` is found in `matrix`, `false` otherwise.

### Constraints

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 100`
- `-10^4 <= matrix[i][j], target <= 10^4`

### Example

Input:

```text
matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
```

Output:

```text
true
```

Manual walkthrough:

```text
rows=3, cols=4, left=0, right=11
mid=5 -> row=1, col=1 -> matrix[1][1]=11, 11 > 3 -> right=4
mid=2 -> row=0, col=2 -> matrix[0][2]=5, 5 > 3 -> right=1
mid=0 -> row=0, col=0 -> matrix[0][0]=1, 1 < 3 -> left=1
mid=1 -> row=0, col=1 -> matrix[0][1]=3 == target -> return true
```

---

## 2. Brute Force Approach

### Idea

Scan every cell of the matrix, row by row and column by column, comparing
it against `target`. The special ordering between rows isn't used at all.

### Pseudocode

```text
function solve(matrix, target)
    for row in matrix
        for val in row
            if val == target
                return true
    return false
```

### Complexity Analysis

#### Time Complexity

```text
O(m * n)
```

Why?

- Every cell can be visited once, and in the worst case (target missing, or
  in the very last cell) all `m * n` cells are checked.

#### Space Complexity

```text
O(1)
```

Why?

- No extra structure is used beyond the loop indices.

### Why this isn't good enough

The matrix isn't just "sorted rows" — the two given properties (each row
ascending, and each row's first value greater than the previous row's last
value) mean the whole matrix reads as **one single ascending sequence** when
scanned left-to-right, top-to-bottom. A cell-by-cell scan throws that global
order away and never discards more than one candidate per comparison.

---

## 3. Key Insight

### What makes this problem difficult?

There are two sorted dimensions (rows and columns), so it isn't immediately
obvious how to apply a single binary search — searching each row
individually would cost `O(m log n)`, not `O(log(m*n))`.

### Key Observation

Because every row is ascending *and* strictly continues from where the
previous row left off, laying the rows end to end produces one fully sorted
array of length `m * n`. Reading the matrix row-major (`matrix[0][0],
matrix[0][1], ..., matrix[0][n-1], matrix[1][0], ...`) never violates
ascending order anywhere, including at the row boundaries.

That means any "virtual" 1D index `idx` in `[0, m*n)` maps to a real cell via:

```text
row = idx / cols
col = idx % cols
```

Example:

```text
matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]

Flattened: [1, 3, 5, 7, 10, 11, 16, 20, 23, 30, 34, 60]
idx=5 -> row=5/4=1, col=5%4=1 -> matrix[1][1]=11 (matches flattened[5]=11)
```

### Why does this observation help?

Once the matrix is treated as a single sorted array reachable through index
arithmetic, an ordinary binary search over `[0, m*n)` works directly — no
actual flattening or extra memory is needed, and each comparison still
eliminates half of the remaining search space.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture the matrix's rows cut apart and glued end to end into one long
ascending ribbon. Binary search walks that ribbon exactly like a 1D sorted
array; the only extra step is translating a ribbon position back into
`(row, col)` using division and remainder.

```text
[1, 3, 5, 7 | 10, 11, 16, 20 | 23, 30, 34, 60]   target = 3
              row 0                row 1            row 2
idx=5 (row 1, col 1) -> 11 > 3 -> search left half
idx=2 (row 0, col 2) -> 5 > 3  -> search left half
idx=0 (row 0, col 0) -> 1 < 3  -> search right half
idx=1 (row 0, col 1) -> 3 == 3 -> found
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
matrix empty or first row empty?
   │
 ┌─┴──────────────────┐
 │                     │
Yes                   No
 │                     │
 ▼                     ▼
Return false     rows = matrix.length
                 cols = matrix[0].length
                 left = 0, right = rows*cols - 1
                        │
                        ▼
                 left <= right ?
                        │
              ┌─────────┴─────────┐
              │                   │
             No                  Yes
              │                   │
              ▼                   ▼
        Return false        mid = left + (right-left)//2
                             row = mid / cols, col = mid % cols
                             val = matrix[row][col]
                                    │
                                    ▼
                             val == target ?
                                    │
                        ┌───────────┴───────────┐
                        │                        │
                       Yes                       No
                        │                        │
                        ▼                        ▼
                 Return true              val < target ?
                                                  │
                                        ┌─────────┴─────────┐
                                        │                    │
                                       Yes                   No
                                        │                    │
                                        ▼                    ▼
                                  left = mid+1         right = mid-1
                                        │                    │
                                        └──────────┬─────────┘
                                                   ▼
                                        (loop back to left <= right ?)
```

Explanation of each decision:

- An empty matrix (or a matrix whose rows have zero columns) can't contain
  `target` — handle it up front so `cols` is never zero.
- `left > right` is the base case — the virtual search space is empty, so
  `target` isn't in the matrix.
- `mid` is a position in the flattened array; `row = mid / cols` and
  `col = mid % cols` recover the real cell without building the flattened
  array.
- Comparing `val` to `target` follows ordinary binary search: match returns
  immediately, `val < target` discards the left half, `val > target`
  discards the right half.

---

## 6. Plain English Algorithm

1. If `matrix` is empty or its first row is empty, return `false`.
2. Set `rows = matrix.length`, `cols = matrix[0].length`.
3. Set `left = 0` and `right = rows * cols - 1`.
4. While `left <= right`:
   - Compute `mid = left + (right - left) / 2`.
   - Convert `mid` into a cell: `row = mid / cols`, `col = mid % cols`.
   - Read `val = matrix[row][col]`.
   - If `val == target`, return `true`.
   - If `val < target`, move `left` to `mid + 1`.
   - Otherwise, move `right` to `mid - 1`.
5. If the loop ends without returning, `target` isn't in the matrix — return
   `false`.

---

## 7. Pseudocode

```text
function solve(matrix, target)
    if matrix is empty or matrix[0] is empty
        return false

    rows = matrix.length
    cols = matrix[0].length
    left, right = 0, rows * cols - 1

    while left <= right
        mid = left + (right - left) // 2
        row = mid / cols
        col = mid % cols
        val = matrix[row][col]

        if val == target: return true
        elif val < target: left = mid + 1
        else: right = mid - 1

    return false
```

---

## 8. Go Solution

```go
package solution

func searchMatrix(matrix [][]int, target int) bool {
	if len(matrix) == 0 || len(matrix[0]) == 0 {
		return false
	}

	rows := len(matrix)
	cols := len(matrix[0])
	left := 0
	right := rows*cols - 1

	for left <= right {
		mid := left + (right-left)/2
		row := mid / cols
		col := mid % cols
		val := matrix[row][col]

		if val == target {
			return true
		}

		if val < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return false
}
```

---

## 9. Dry Run

Example:

```text
matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
```

| Step | `left` | `right` | `mid` | `row` | `col` | `val` | Action | Why? |
|------|--------|---------|-------|-------|-------|-------|--------|------|
| 1 | 0 | 11 | 5 | 1 | 1 | 11 | `right = 4` | `11 > 3`, discard right half |
| 2 | 0 | 4 | 2 | 0 | 2 | 5 | `right = 1` | `5 > 3`, discard right half |
| 3 | 0 | 1 | 0 | 0 | 0 | 1 | `left = 1` | `1 < 3`, discard left half |
| 4 | 1 | 1 | 1 | 0 | 1 | 3 | Return `true` | `val == target` |

Result: `true`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(log(m * n))
```

Why?

- The search treats the matrix as one virtual sorted array of `m * n`
  elements and halves the remaining range on every iteration, exactly like
  a 1D binary search.

### Space Complexity

```text
O(1)
```

Why?

- Only a fixed number of index variables (`left`, `right`, `mid`, `row`,
  `col`) are used, regardless of the matrix's size.
