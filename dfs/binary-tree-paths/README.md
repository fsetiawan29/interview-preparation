# Problem

Name: Binary Tree Paths

Difficulty: Easy

----------------------------------------

# Pattern

DFS

----------------------------------------

# Recognition

Steps

- STATE: `(node, path so far)`
- PROCESS: Append current `node`'s value onto path (`str(node.val)` if path is empty, else `path + "->" + str(node.val)`)
- BASE CASE: `node` is a leaf (no left, no right) -> path is complete -> save to result, then stop
- PRUNE: Not needed. we only recurse into children that actually exist, so there's nothing invalid to catch early
- RECURSE: Into `node.left` and/or `node.right`, whichever are `not None`
- BACKTRACK: Not needed. since path is string (immutable), passing it to `dfs(node.left, path)` and `dfs(node.right, path)` gives each call its own copy; no shared state to undo

----------------------------------------

# Complexity

- Time: `O(n^2)` — each of the `n` nodes can appear in up to `n` paths, and each path is rebuilt via string concatenation
- Space: `O(n^2)` for the output (sum of all path lengths), plus `O(h)` recursion stack where `h` is tree height