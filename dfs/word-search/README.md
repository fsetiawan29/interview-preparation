# Problem: Word Search

## 1. Problem Understanding

### Problem Summary

Given an `m x n` grid of characters `board` and a string `word`, determine whether `word` can be constructed by tracing a path through adjacent cells (horizontally or vertically), using each cell at most once per path.

### Input

- A 2D grid of characters `board`
- A string `word`

### Output

- `true` if `word` exists in `board` following the adjacency rule, `false` otherwise.

### Constraints

- `m == board.length`
- `n == board[i].length`
- `1 <= m, n <= 6`
- `1 <= word.length <= 15`
- `board` and `word` consist of only lowercase and uppercase English letters.

### Example

Input:

```text
board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
word = "ABCCED"
```

Output:

```text
true
```

Manual walkthrough:

```text
Board:
A B C E
S F C S
A D E E

Start at (0,0)='A' matches word[0]='A'
  -> move right to (0,1)='B' matches word[1]='B'
     -> move right to (0,2)='C' matches word[2]='C'
        -> move down to (1,2)='C' matches word[3]='C'
           -> move down to (2,2)='E' matches word[4]='E'
              -> move left to (2,1)='D' matches word[5]='D'
                 -> all 6 letters matched

↓

true
```

---

## 2. Brute Force Approach

### Idea

Instead of marking a cell directly on the board and restoring it afterward, pass a freshly copied `visited` set into every recursive call, adding the current cell to the copy each time.

### Pseudocode

```text
function dfs(r, c, index, visited)
    if index == length(word)
        return true

    if r < 0 or r >= rows or c < 0 or c >= cols
        return false
    if (r, c) in visited
        return false
    if board[r][c] != word[index]
        return false

    new_visited = copy of visited, plus (r, c)   // O(L) copy

    return dfs(r+1, c, index+1, new_visited)
        or dfs(r-1, c, index+1, new_visited)
        or dfs(r, c+1, index+1, new_visited)
        or dfs(r, c-1, index+1, new_visited)

for r in 0 .. rows-1
    for c in 0 .. cols-1
        if dfs(r, c, 0, empty set)
            return true

return false
```

### Complexity Analysis

#### Time Complexity

```text
O(rows * cols * 4^L * L)
```

Why?

- Same `rows * cols` starting points and `4^L` branching as the optimized version (`L = len(word)`), but every recursive call now also pays `O(L)` to copy the `visited` set before recursing.

#### Space Complexity

```text
O(L^2)
```

Why?

- Up to `L` recursive calls can be active at once, and each one carries its own `O(L)`-sized copy of `visited`.

### Why this isn't good enough

Copying the visited set at every step multiplies the entire search by an extra factor of `L`, in both time and space. Marking a cell directly on the board (and un-marking it when backtracking) needs no copying at all — it reuses storage that already exists, at `O(1)` extra work per step instead of `O(L)`.

---

## 3. Key Insight

### What makes this problem difficult?

A cell can lead down multiple possible directions, and a wrong guess several steps in requires undoing exactly the cells that were tentatively claimed — without an explicit "undo," a used cell would stay marked as visited forever and block every other path that also needs to pass through it.

### Key Observation

The board itself can double as the "visited" tracker: temporarily overwrite a matched cell with a sentinel (like `"#"`) while exploring deeper, then restore its original letter once that exploration path is exhausted — this is backtracking.

Example:

```text
board[r][c] = 'C'  -> matches word[index], so:
board[r][c] = '#'           # mark visited
... recurse deeper ...
board[r][c] = 'C'  # restore ('#' -> original letter) before trying a sibling direction
```

### Why does this observation help?

No second `visited` grid is needed — mutating and then restoring `board` in place gives O(1) extra bookkeeping per cell, and guarantees that once a path backtracks past a cell, that cell is available again for a completely different path starting elsewhere.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a hiker leaving footprints in snow while chasing the letters of `word` one step at a time, in four possible directions. Each footprint is temporary: if the trail dead-ends, the hiker erases their last footprint and backs up to try a different direction, exactly like exploring a maze.

```text
A  B  C  E              #  #  C  E
S  F  C  S      ->       S  F  C  S      (after matching A, B — footprints left behind)
A  D  E  E               A  D  E  E

If this path dead-ends, backtrack:

#  #  C  E               A  B  C  E
S  F  C  S      ->       S  F  C  S      (footprints erased, cells restored)
A  D  E  E               A  D  E  E
```

Every cell on the current trail is "frozen" (can't be reused) only while the hiker is actively standing on it or beyond it — the moment the hiker backs off that cell, it thaws and becomes walkable again.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
dfs(r, c, index)
   │
   ▼
Is index == len(word) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return True     Is (r,c) out of bounds
                OR board[r][c] != word[index] ?
                    │
                  ┌─┴─────────────────┐
                  │                    │
                 Yes                  No
                  │                    │
                  ▼                    ▼
             Return False       Mark board[r][c] = "#"
                                       │
                                       ▼
                                Recurse into all 4 directions
                                (index + 1), stop at first True
                                       │
                                       ▼
                                Restore board[r][c] to its
                                original letter (backtrack)
                                       │
                                       ▼
                                Return whether any direction found the word
```

Explanation of each decision:

- Checking `index == len(word)` first means the full word has already been matched by the time this cell is reached — no need to even look at the current cell.
- The prune step catches three invalid cases in one place: stepping off the grid, landing on a mismatched letter, and landing on a cell already used earlier in *this same path* (marked `"#"`).
- Marking the cell before recursing prevents the same path from doubling back onto itself.
- Restoring the cell after recursing is the backtracking step — it undoes the mark so a *different* starting path, or a sibling direction, can still use that cell.

---

## 6. Plain English Algorithm

1. Try every cell `(r, c)` in the grid as a possible starting point for `word[0]`.
2. From a given cell, if `index` has already reached `len(word)`, the whole word matched — return `true`.
3. If `(r, c)` is out of bounds, or its letter doesn't match `word[index]`, or the cell was already used earlier in this path (marked `"#"`), fail this branch — return `false`.
4. Otherwise, temporarily mark `board[r][c] = "#"` to claim it for this path.
5. Recurse into all four neighboring directions with `index + 1`, stopping as soon as one succeeds.
6. Restore `board[r][c]` to its original letter — whether or not the recursion succeeded — so other paths can reuse this cell.
7. If any starting cell leads to a full match, return `true`; if none do, return `false`.

---

## 7. Pseudocode

```text
rows = number of rows in board
cols = number of cols in board

function dfs(r, c, index):
    if index == length(word):
        return true

    if r < 0 or r >= rows or c < 0 or c >= cols:
        return false
    if board[r][c] != word[index]:
        return false

    original = board[r][c]
    board[r][c] = "#"

    found = dfs(r+1, c, index+1)
         or dfs(r-1, c, index+1)
         or dfs(r, c+1, index+1)
         or dfs(r, c-1, index+1)

    board[r][c] = original

    return found

for r in 0 .. rows-1:
    for c in 0 .. cols-1:
        if dfs(r, c, 0):
            return true

return false
```

---

## 8. Python Solution

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        def dfs(r, c, index):
            # 1. BASE CASE (matched full word)
            if index == len(word):
                return True

            # 2. PRUNE (out of bounds / mismatch / already visited)
            if r < 0 or r >= len(board) or c < 0 or c >= len(board[0]):
                return False
            # 2.b if letter doesn't match
            if board[r][c] != word[index]:
                return False
            if board[r][c] == "#":
                return False

            # 3. PROCESS (mark cell as visited)
            board[r][c] = "#"

            # 4. RECURSE (explore 4 directions)
            found = dfs(r+1,c,index+1) or dfs(r-1,c,index+1) or dfs(r,c+1,index+1) or dfs(r,c-1,index+1)

            # 5. BACKTRACK (restore cell)
            board[r][c] = word[index]

            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False
```

---

## 9. Dry Run

Example:

```text
board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
word = "ABCCED"
```

| Step | Call | Cell (r,c) | Board value | Action | Why? |
|------|------|------------|--------------|--------|------|
| 1 | `dfs(0,0,0)` | (0,0) | `'A'` | Matches `word[0]='A'`; mark `#`; recurse | Start of a candidate path |
| 2 | `dfs(1,0,1)` | (1,0) | `'S'` | `'S' != word[1]='B'` -> return `False` | Mismatch, prune this direction |
| 3 | `dfs(-1,0,1)` | (-1,0) | — | Out of bounds -> return `False` | Off the top edge |
| 4 | `dfs(0,1,1)` | (0,1) | `'B'` | Matches `word[1]='B'`; mark `#`; recurse | Right neighbor continues the path |
| 5 | `dfs(0,2,2)` | (0,2) | `'C'` | Matches `word[2]='C'`; mark `#`; recurse | Continue right |
| 6 | `dfs(1,2,3)` | (1,2) | `'C'` | Matches `word[3]='C'`; mark `#`; recurse | Move down |
| 7 | `dfs(2,2,4)` | (2,2) | `'E'` | Matches `word[4]='E'`; mark `#`; recurse | Move down |
| 8 | `dfs(2,1,5)` | (2,1) | `'D'` | Matches `word[5]='D'`; mark `#`; recurse | Move left |
| 9 | `dfs(3,1,6)` (first of 4 branches tried) | — | — | `index==6==len(word)` -> return `True` | Full word matched |
| 10 | Unwind through steps 8 -> 4 | (2,1) -> (0,1) | each restored | Every frame restores its cell (e.g. `board[2][1]` back to `'D'`) and propagates `True` upward | Backtracking cleans up while success bubbles to the top |
| 11 | `dfs(0,0,0)` (resume) | (0,0) | restored to `'A'` | `found=True`, restore, return `True` | Path complete |

Result: `true`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(rows * cols * 4^L)
```

Why?

- Every cell in the grid is tried as a potential starting point: `rows * cols` starts.
- From each start, the DFS can branch in up to 4 directions per character of `word`, giving `4^L` in the worst case, where `L = len(word)`.

### Space Complexity

```text
O(L)
```

Why?

- The recursion stack holds at most `L` frames at once, one per matched character.
- No extra visited grid is allocated — `board` is mutated in place and restored via backtracking.
