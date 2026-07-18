# Problem

Name: Valid Sudoku

Difficulty: Medium

----------------------------------------

# Pattern

Hash Set + Matrix

----------------------------------------

# Recognition

Idea

- Create rows contains hash set for each row
- Create cols contains hash set for each col
- Create dictionary with key is (r // 3, c // 3)
- Scan every cell once; before adding a digit to its row/col/box set, check it isn't already there — a duplicate in any of the three means the board is invalid

Steps

- INIT: `rows`/`cols` as a list of 9 empty sets (one per row/col); `boxes` as a dict keyed by `(r // 3, c // 3)` holding a set per 3x3 sub-box
- SCAN: walk every cell `(r, c)`; skip `.`
- CHECK: for the cell's `value`, if it's already in `cols[c]`, `rows[r]`, or `boxes[(r//3, c//3)]`, return `False`
- RECORD: otherwise add `value` to all three sets and continue
- RETURN: `True` if no duplicate was found after scanning the whole board

----------------------------------------

# Complexity

- Time: `O(1)` — the board is a fixed 9x9 = 81 cells, so the scan is bounded regardless of input (equivalently `O(n^2)` if generalized to an n x n board)
- Space: `O(1)` — at most 9 rows + 9 cols + 9 boxes of sets, each holding at most 9 digits

