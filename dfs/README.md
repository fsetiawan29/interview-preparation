# DFS (Depth-First Search)

## What is DFS?

DFS is a traversal strategy for trees and graphs: from the current node, go as
deep as possible along one branch before backtracking and trying the next
branch. It's implemented either with **recursion** (the call stack acts as
the "stack") or with an **explicit stack** in an iterative version.

Contrast with BFS, which explores level-by-level (all neighbors first, using
a queue). DFS explores path-by-path (as deep as possible first, using a
stack).

Use DFS when the problem is about:
- Exploring **all paths** from root to leaf (or start to end)
- **Backtracking** — trying a choice, recursing, then undoing the choice
- Tree traversals (preorder / inorder / postorder)
- Connected components / flood fill on a grid or graph
- Checking reachability, cycles, or counting islands/regions

## The general shape

Almost every DFS problem is a variation of this skeleton:

```python
def dfs(state):
    # 1. BASE CASE — when do you stop recursing?
    if base_case_condition:
        do_something_with(state)  # save it, return a value, etc.
        return

    # 2. (Optional) PRUNE — is this state already invalid? Bail early.
    if invalid_condition:
        return

    # 3. PROCESS current state (mark visited, build up path, etc.)
    update_state_or_mark_visited(state)

    # 4. RECURSE into all valid next options
    for next_state in options(state):
        dfs(next_state)

    # 5. (Optional) BACKTRACK — undo step 3, if state is shared/mutated
    undo_the_mark_or_restore_state(state)
```

Five steps:

1. **Base case** — the condition that stops recursion (null node, out of
   bounds, reached a leaf/target). This is also where you usually record
   the answer, since it's the point where a state is "complete."
2. **Prune (optional)** — a state that's already invalid (visited, blocked,
   out of budget) — bail before doing any work on it.
3. **Process** — mark the current state visited, or add it to the path
   being built.
4. **Recurse** — call `dfs` on every valid next state (neighbor, child,
   choice).
5. **Backtrack (optional)** — undo step 3 so sibling branches don't see
   this state.

Step 5 is the one people forget. It's required whenever `visited`/`path` is
a single mutable object shared across the whole recursion — skip it and
branches contaminate each other. It's *not* needed if each recursive call
gets its own copy of the state instead of sharing one (or if you're
permanently marking nodes, e.g. counting connected components).

## Recursive template (tree)

```python
class Solution:
    def dfs(self, node):
        if node is None:
            return

        # pre-order: process node here, before children

        self.dfs(node.left)
        # in-order: process node here, between children
        self.dfs(node.right)

        # post-order: process node here, after children
```

## Recursive template (grid / graph, with backtracking)

```python
class Solution:
    def dfs(self, grid, r, c, visited):
        rows, cols = len(grid), len(grid[0])

        # 1. base case: out of bounds, blocked, or already visited
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if (r, c) in visited or grid[r][c] == "blocked":
            return

        # 2. mark
        visited.add((r, c))

        # 4. explore neighbors (up, down, left, right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            self.dfs(grid, r + dr, c + dc, visited)

        # 5. unmark — only needed if `visited` must be reused for other
        # starting points/paths; for "count connected components" style
        # problems you usually keep it marked permanently instead.
```

## Iterative template (explicit stack)

```python
class Solution:
    def dfs(self, root):
        if root is None:
            return []

        stack = [root]
        visited_order = []

        while stack:
            node = stack.pop()
            visited_order.append(node.val)

            # push right before left so left is processed first (LIFO)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return visited_order
```

## Complexity

- **Time:** O(V + E) for graphs, O(N) for trees — every node/edge is
  visited once.
- **Space:** O(H) for the recursion stack, where H is the tree height (or
  O(V) worst case for a skewed tree / graph DFS).

## Common pitfalls

- **Forgetting to copy the path** before appending it to the result
  (`result.append(path)` stores a reference that later mutates — use
  `list(path)` or `path[:]`).
- **Forgetting to mark visited** on a graph with cycles → infinite
  recursion / stack overflow.
- **Forgetting to backtrack** (undo the mark/pop) when the same mutable
  state is reused across sibling branches.
- Recursion depth limits in Python (`sys.setrecursionlimit`) for very deep
  trees/graphs — consider the iterative stack version if input size is
  large.

## Problems in this folder

- [binary-tree-paths](./binary-tree-paths) — classic root-to-leaf path
  enumeration; the canonical "choose / explore / un-choose" DFS.