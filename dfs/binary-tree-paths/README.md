# Problem: Binary Tree Paths

## 1. Problem Understanding

### Problem Summary

Given the root of a binary tree, return all root-to-leaf paths, in any order, formatted as strings that join each node's value with `"->"`.

### Input

- The root of a binary tree, `root`

### Output

- A list of strings, one per root-to-leaf path, e.g. `"1->2->5"`.

### Constraints

- The number of nodes in the tree is in the range `[1, 100]`.
- `-100 <= Node.val <= 100`

### Example

Input:

```text
root = [1,2,3,null,5]
```

Output:

```text
["1->2->5","1->3"]
```

Manual walkthrough:

```text
Tree:

     1
    / \
   2   3
    \
     5

From 1, go left to 2 -> not a leaf (has a right child) -> keep going
From 2, go right to 5 -> no children -> leaf! path so far: "1->2->5"

From 1, go right to 3 -> no children -> leaf! path so far: "1->3"

↓

["1->2->5", "1->3"]
```

---

## 2. Brute Force Approach

### Idea

First find every leaf with one traversal. Then, for each leaf separately, run a brand-new search starting back at the root to rediscover the path down to that specific leaf.

### Pseudocode

```text
function find_leaves(node)
    if node is None
        return []
    if node.left is None and node.right is None
        return [node]
    return find_leaves(node.left) + find_leaves(node.right)

function path_to(node, target, path)
    if node is None
        return None

    new_path = (path + "->" + str(node.val)) if path else str(node.val)

    if node == target
        return new_path

    left_result = path_to(node.left, target, new_path)
    if left_result is not None
        return left_result

    return path_to(node.right, target, new_path)

leaves = find_leaves(root)
result = []
for leaf in leaves
    result.append(path_to(root, leaf, ""))

return result
```

### Complexity Analysis

#### Time Complexity

```text
O(n^3)
```

Why?

- `n` = number of nodes; there can be up to `O(n)` leaves.
- For each leaf, `path_to` re-searches from the root — up to `O(n)` nodes — and at each of those nodes it pays another `O(n)` to extend the path string by concatenation, giving `O(n^2)` per leaf and `O(n^3)` total.

#### Space Complexity

```text
O(n^2)
```

Why?

- `leaves` holds up to `O(n)` nodes, and the accumulated path strings across all leaves sum to `O(n^2)` in the worst case (a skewed tree).

### Why this isn't good enough

Every leaf triggers its own completely separate walk from the root, redoing work that a single traversal already covers. Carrying the path down *while* the one traversal is already visiting every node — extending it once per level instead of re-deriving it from scratch per leaf — removes that redundant re-searching entirely.

---

## 3. Key Insight

### What makes this problem difficult?

Each path needs to remember every node visited since the root, but a single shared list (like the one used for inorder traversal) would keep growing forever and would need explicit undoing whenever recursion backtracks up from a leaf to try a different branch.

### Key Observation

Because `path` is a Python string (immutable), passing `path + "->" + str(node.val)` down into a recursive call automatically gives that call — and only that call — its own private copy. No two branches can see or corrupt each other's path.

Example:

```text
dfs(2, "1"):
    path = "1->2"
    dfs(5, "1->2")   # gets "1->2", unaffected by dfs(3, "1")'s path

dfs(3, "1"):
    path = "1->3"    # completely separate string
```

### Why does this observation help?

There's no need for an explicit backtracking step (no "undo" after the recursive calls return) — each call builds its own extended path and simply lets it go out of scope when it returns. Contrast this with Word Search, where the shared, mutable `board` *does* require an explicit undo.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture handing a growing note card down to each child before branching. Every child receives a *photocopy* of the note with its own name appended — never the original. When a child hits a dead end (no children of its own), it seals the photocopy into the results envelope. When a child has more children, it photocopies its own copy again for each of them.

```text
        1
       / \
      2   3
       \
        5

"1" is created at the root.
  -> copy "1", append "2" -> "1->2" travels to node 2
       -> node 2 has only a right child
       -> copy "1->2", append "5" -> "1->2->5" travels to node 5
            -> node 5 is a leaf -> seal "1->2->5" into results
  -> copy "1", append "3" -> "1->3" travels to node 3
       -> node 3 is a leaf -> seal "1->3" into results
```

Each branch only ever sees its own copy — nothing needs to be cleaned up afterward.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
dfs(node, path)
   │
   ▼
path = path + "->" + node.val   (or just node.val if path was empty)
   │
   ▼
Is node a leaf (no left AND no right) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Append path to     Is node.left not None ?
result, return       │
                    ┌─┴────────┐
                    │          │
                   Yes        No
                    │          │
                    ▼          │
              dfs(node.left,   │
                  path)        │
                    │          │
                    └────┬─────┘
                         ▼
                   Is node.right not None ?
                         │
                       ┌─┴────────┐
                       │          │
                      Yes        No
                       │          │
                       ▼          │
                 dfs(node.right,  │
                     path)        │
                       │          │
                       └────┬─────┘
                            ▼
                          Return
```

Explanation of each decision:

- `path` is extended with the current node's value *before* the leaf check — every node, including leaves, must appear in its own path string.
- A leaf (no children) is the base case: the completed path is saved to `result` and this branch stops.
- A non-leaf only recurses into children that actually exist — there's nothing to prune, since `dfs` is simply never called on a `None` child.
- Both children (when present) receive the *same* `path` value — but because strings are immutable, each call's local extension doesn't leak into the sibling's call.

---

## 6. Plain English Algorithm

1. Start `dfs(root, "")`.
2. Extend `path` with the current node's value — `str(node.val)` if `path` was empty, otherwise `path + "->" + str(node.val)`.
3. If the current node is a leaf (no left and no right child), save `path` to `result` and stop this branch.
4. Otherwise, recurse into `node.left` if it exists, passing the extended `path`.
5. Recurse into `node.right` if it exists, passing the extended `path`.
6. After the initial call returns, `result` holds every root-to-leaf path.

---

## 7. Pseudocode

```text
result = []

function dfs(node, path):
    if path == "":
        path = str(node.val)
    else:
        path = path + "->" + str(node.val)

    if node.left is None and node.right is None:
        result.append(path)
        return

    if node.left is not None:
        dfs(node.left, path)
    if node.right is not None:
        dfs(node.right, path)

dfs(root, "")
return result
```

---

## 8. Python Solution

```python
class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        result = []

        def dfs(node, path):
            # 1. PROCESS
            if path == "":
                path = str(node.val)
            else:
                path = path + "->" + str(node.val)

            # 2. BASE CASE
            if node.left is None and node.right is None:
                result.append(path)
                return

            # 3. (No prune step needed here)

            # 4. RECURSE
            if node.left is not None:
                dfs(node.left, path)
            if node.right is not None:
                dfs(node.right, path)

        dfs(root, "")
        return result
```

---

## 9. Dry Run

Example:

```text
root = [1,2,3,null,5]

Tree:
     1
    / \
   2   3
    \
     5
```

| Step | Call | Node | `path` before | Action | `result` so far | Why? |
|------|------|------|----------------|--------|------------------|------|
| 1 | `dfs(1, "")` | 1 | `""` | `path` becomes `"1"`; not a leaf (has children) | `[]` | Root has both children, keep going |
| 2 | `dfs(2, "1")` | 2 | `"1"` | `path` becomes `"1->2"`; not a leaf (has right child) | `[]` | Node 2 has a right child only |
| 3 | `dfs(5, "1->2")` | 5 | `"1->2"` | `path` becomes `"1->2->5"`; leaf -> append | `["1->2->5"]` | Node 5 has no children |
| 4 | `dfs(2, "1")` (resume) | 2 | — | `node.right` (5) already recursed; no left child to visit | `["1->2->5"]` | Node 2's only child was `right` |
| 5 | `dfs(3, "1")` | 3 | `"1"` | `path` becomes `"1->3"`; leaf -> append | `["1->2->5", "1->3"]` | Node 3 has no children |

Result: `["1->2->5", "1->3"]`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n^2)
```

Why?

- Each of the `n` nodes can appear in up to `O(n)` different root-to-leaf paths in a skewed tree.
- Extending `path` via string concatenation copies the whole string each time, so total work across all calls is `O(n^2)` in the worst case.

### Space Complexity

```text
O(n^2)
```

Why?

- `result` stores every root-to-leaf path; the sum of all path lengths is `O(n^2)` in the worst case.
- On top of that, the recursion stack holds at most `O(h)` frames at once, where `h` is the tree height.
