# Problem

Name: Binary Tree Inorder Traversal

Difficulty: Easy

----------------------------------------

# Pattern

DFS

----------------------------------------

# Recognition

Steps

- STATE: `node`
- BASE CASE: `node` is `None` -> return (nothing to append)
- PROCESS: Append current `node`'s value onto result, positioned between the left and right recursive calls (in-order)
- PRUNE: Not needed. we always recurse into both children regardless of value, so there's nothing invalid to catch early
- RECURSE: Into `node.left` first, then PROCESS, then into `node.right`
- BACKTRACK: Not needed. `result` is a single shared list built via `append`, so there's no state to undo between calls


----------------------------------------

Mistakes
- Don't know the concept it will go deep first for the recursive process