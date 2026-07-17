# Problem

Name: Word Search

Difficulty: Medium

----------------------------------------

# Pattern

DFS

----------------------------------------

# Recognition

Steps

- STATE: your position in the grid `(r,c)` and how far into the word you've matched `word[index]`
- BASE CASE: `if index == len(word)`, every letter has been matched, `return True`
- PRUNE:
    1. `(r,c)` is out of bounds
    2. `board[r][c] != word[index]` (covers a mismatched letter and an already-visited cell, since visited cells are marked `"#"`)
- PROCESS: Mark the cell as visited (e.g. swap it to `"#"`)
- RECURSE: Four directions, up/down/left/right, each with `index+1`
- BACKTRACK: Restore the cell to its original letter after recursing, so other paths can reuse it

----------------------------------------

# Complexity

- Time: `O(rows * cols * 4^L)` where `L` is `len(word)` — try every starting cell, and each DFS branches 4 ways per character
- Space: `O(L)` for the recursion stack (board is mutated in place, no extra grid needed)

----------------------------------------

Mistakes
- Don't know the concept it will go deep first for the recursive process