# Problem: Valid Sudoku

## 1. Problem Understanding

### Problem Summary

Given a 9x9 Sudoku board (partially filled, with `'.'` for empty cells), determine whether the board is valid according to Sudoku rules: each row, each column, and each of the nine 3x3 sub-boxes must contain the digits `1-9` with no repetition. Note only the *filled* cells need to satisfy these rules — the board doesn't need to be solvable or fully filled.

### Input

- A 9x9 board `board`, where each cell is a digit `'1'`-`'9'` or `'.'`.

### Output

- `true` if the board is a valid Sudoku board (no row/column/box duplicates), `false` otherwise.

### Constraints

- `board.length == 9`
- `board[i].length == 9`
- `board[i][j]` is a digit `1-9` or `'.'`.

### Example

Input:

```text
board =
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
```

Output:

```text
true
```

Manual walkthrough:

```text
Same board, but with the top-left cell changed from "5" to "8":

Output: false
Explanation: the top-left 3x3 sub-box already contains an "8" at row 2,
column 2. Changing row 0, column 0 to "8" puts a second "8" in that same
sub-box, so the board is now invalid — even though no row or column has
a duplicate.
```

---

# 2. Key Insight

## What makes this problem difficult?

Three different kinds of "no duplicates" rules (row, column, 3x3 box) all apply simultaneously, and a single cell participates in exactly one row, one column, and one box at the same time. Checking each rule with a separate full scan of the board would be wasteful, and mapping a cell to "its" box requires a bit of index arithmetic that's easy to get wrong.

## Key Observation

Every cell `(r, c)` belongs to exactly one row `r`, one column `c`, and one box identified by `(r // 3, c // 3)`. If we keep **one hash set per row, per column, and per box**, a single pass over the board can check *and* record membership in all three simultaneously — a duplicate in any one of the three sets means the board is invalid.

Example:

```text
cell (r=2, c=2), value "8"
row index:    2        -> rows[2]
column index: 2        -> cols[2]
box key:      (2//3, 2//3) = (0, 0)  -> boxes[(0,0)]

If "8" is already in rows[2], cols[2], or boxes[(0,0)] -> invalid, return False
Otherwise, add "8" to all three and continue
```

## Why does this observation help?

One single pass over all 81 cells is enough — no separate row-pass, column-pass, or box-pass is needed. Each cell's membership check and insertion into its row/column/box set happens together, so a duplicate anywhere is caught the moment it's seen.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture 27 clipboards laid out: 9 for rows, 9 for columns, 9 for the 3x3 boxes. As you scan the board cell by cell, left to right, top to bottom, every non-empty digit gets checked against its row's clipboard, its column's clipboard, and its box's clipboard — if that digit is already written on any of the three, stop immediately, the board is invalid. Otherwise, jot the digit down on all three clipboards and move to the next cell.

```text
board scan order:  (0,0) (0,1) (0,2) ... (0,8) (1,0) (1,1) ...

At each non-'.' cell (r, c) with value v:
  check rows[r]           -> has v already? invalid
  check cols[c]           -> has v already? invalid
  check boxes[(r//3,c//3)]-> has v already? invalid
  otherwise: write v on all three clipboards, keep going
```

If the scan reaches the last cell without ever finding `v` already on a clipboard, the board is valid.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize rows = 9 empty sets, cols = 9 empty sets, boxes = empty map
   │
   ▼
For each cell (r, c) in row-major order:
   │
   ▼
Is board[r][c] == '.' ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Skip cell        value = board[r][c]
                       │
                       ▼
              Is value in cols[c] OR rows[r]
              OR boxes[(r//3, c//3)] ?
                       │
                     ┌─┴─────────────────┐
                     │                    │
                    Yes                  No
                     │                    │
                     ▼                    ▼
              Return false       Add value to cols[c],
                                  rows[r], boxes[(r//3,c//3)]
                                        │
                                        └──▶ (loop to next cell)
                                                    │
                                                    ▼
                              All 81 cells scanned without
                              duplicates found — return true
```

Explanation of each decision:

- A `'.'` cell contributes nothing to any rule, so it's simply skipped.
- Checking all three sets (`cols[c]`, `rows[r]`, `boxes[(r//3, c//3)]`) before adding anything is what catches a duplicate the instant it appears, in whichever rule it violates.
- Only after passing all three checks is the value recorded into all three sets — this way, a rejected value never pollutes the sets.
- If every cell passes its check, no rule was ever violated, so the board is valid.

---

# 5. Plain English Algorithm

1. Create 9 empty sets for rows, 9 empty sets for columns, and an empty map of sets for 3x3 boxes (keyed by `(r // 3, c // 3)`).
2. Scan the board cell by cell, row by row:
   - Skip cells containing `'.'`.
   - For a filled cell's `value`, check whether it already exists in that column's set, that row's set, or that box's set. If so, return `false` immediately.
   - Otherwise, add `value` to all three sets and continue.
3. If the scan completes without finding any duplicate, return `true`.

---

# 6. Pseudocode

```text
rows = 9 empty sets
cols = 9 empty sets
boxes = empty map

for r from 0 to 8
    for c from 0 to 8
        value = board[r][c]

        if value == '.'
            continue

        boxKey = (r // 3, c // 3)
        if boxKey not in boxes
            boxes[boxKey] = empty set

        if value in cols[c] or value in rows[r] or value in boxes[boxKey]
            return false

        add value to cols[c]
        add value to rows[r]
        add value to boxes[boxKey]

return true
```

---

# 7. Python Solution

```python
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        cols = [set() for _ in range(9)]
        rows = [set() for _ in range(9)]
        boxes = {}
        for r in range(9):
            for c in range(9):
                value = board[r][c]

                if value == ".":
                    continue

                col_set = cols[c]
                if value in col_set:
                    return False

                row_set = rows[r]
                if value in row_set:
                    return False

                boxKey = (r // 3, c // 3)
                if boxKey not in boxes:
                    boxes[boxKey] = set()

                box_set = boxes[boxKey]
                if value in box_set:
                    return False

                cols[c].add(value)
                rows[r].add(value)
                boxes[boxKey].add(value)

        return True
```

---

# 8. Dry Run

Example (the invalid board — same as the "true" board but with `board[0][0]` changed from `"5"` to `"8"`):

```text
Relevant cells (row-major order, non-'.' only, up to the failure):
(0,0)="8" (0,1)="3" (0,4)="7"
(1,0)="6" (1,3)="1" (1,4)="9" (1,5)="5"
(2,1)="9" (2,2)="8"  <- duplicate found here
```

| Step | Cell (r,c) | value | boxKey | Check | Action | Sets after |
|------|------------|-------|--------|-------|--------|------------|
| 1 | (0,0) | "8" | (0,0) | not in cols[0], rows[0], boxes[(0,0)] | Add to all three | cols[0]={8}, rows[0]={8}, boxes[(0,0)]={8} |
| 2 | (0,1) | "3" | (0,0) | not in cols[1], rows[0], boxes[(0,0)] | Add to all three | rows[0]={8,3}, boxes[(0,0)]={8,3}, cols[1]={3} |
| 3 | (0,4) | "7" | (0,1) | not in cols[4], rows[0], boxes[(0,1)] | Add to all three | rows[0]={8,3,7}, cols[4]={7}, boxes[(0,1)]={7} |
| 4 | (1,0) | "6" | (0,0) | not in cols[0]={8}, rows[1]={}, boxes[(0,0)]={8,3} | Add to all three | cols[0]={8,6}, rows[1]={6}, boxes[(0,0)]={8,3,6} |
| 5 | (1,3) | "1" | (0,1) | not in cols[3], rows[1]={6}, boxes[(0,1)]={7} | Add to all three | cols[3]={1}, rows[1]={6,1}, boxes[(0,1)]={7,1} |
| 6 | (1,4) | "9" | (0,1) | not in cols[4]={7}, rows[1]={6,1}, boxes[(0,1)]={7,1} | Add to all three | cols[4]={7,9}, rows[1]={6,1,9}, boxes[(0,1)]={7,1,9} |
| 7 | (1,5) | "5" | (0,1) | not in cols[5], rows[1]={6,1,9}, boxes[(0,1)]={7,1,9} | Add to all three | cols[5]={5}, rows[1]={6,1,9,5}, boxes[(0,1)]={7,1,9,5} |
| 8 | (2,1) | "9" | (0,0) | not in cols[1]={3}, rows[2]={}, boxes[(0,0)]={8,3,6} | Add to all three | cols[1]={3,9}, rows[2]={9}, boxes[(0,0)]={8,3,6,9} |
| 9 | (2,2) | "8" | (0,0) | cols[2]={} ok, rows[2]={9} ok, **boxes[(0,0)]={8,3,6,9} already has "8"** | Return False | — |

Result: `false` — the duplicate "8" is caught in the top-left 3x3 box (cells `(0,0)` and `(2,2)` share box key `(0,0)`), matching the example's explanation.

---

# 9. Complexity Analysis

### Time Complexity

```text
O(1)
```

Why?

- The board is a fixed 9x9 = 81 cells, so the scan always does a bounded amount of work regardless of what digits are on the board.
- Equivalently, this is `O(n^2)` if generalized to an `n x n` board with `n x n` sub-boxes.

### Space Complexity

```text
O(1)
```

Why?

- At most 9 row sets, 9 column sets, and 9 box sets exist, each holding at most 9 digits — all bounded by the fixed board size, independent of input.
