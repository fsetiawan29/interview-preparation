# Problem: Binary Tree Inorder Traversal

## 1. Problem Understanding

### Problem Summary

Given the root of a binary tree, return the values of its nodes using an **inorder traversal** — visit the left subtree, then the current node, then the right subtree.

### Input

- The root of a binary tree, `root`

### Output

- A list of integers representing the node values in inorder sequence.

### Constraints

- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`

### Example

Input:

```text
root = [1,null,2,3]
```

Output:

```text
[1,3,2]
```

Manual walkthrough:

```text
Tree:

1
 \
  2
 /
3

Inorder = left, node, right

Start at 1 -> go left (None, nothing to visit)
           -> visit 1
           -> go right to 2
              -> go left to 3
                 -> go left (None, nothing to visit)
                 -> visit 3
                 -> go right (None, nothing to visit)
              -> visit 2
              -> go right (None, nothing to visit)

Visited order: 1, 3, 2

↓

[1,3,2]
```

---

# 2. Key Insight

## What makes this problem difficult?

It's tempting to think of "traversal" as scanning the tree left-to-right the way you'd scan an array, but a tree has no single linear layout — the only way to visit nodes in a well-defined order is to let recursion do the walking. The order in which the "visit" step is placed relative to the two recursive calls (before, between, or after) is exactly what defines pre/in/post-order.

## Key Observation

Recursing into the left subtree fully before touching the current node, and only visiting the right subtree after the current node, guarantees every node's value lands in the result list exactly once, in left-to-right structural order.

Example:

```text
    2
   / \
  1   3

dfs(2):
  dfs(1) -> append 1
  append 2
  dfs(3) -> append 3

result = [1, 2, 3]
```

## Why does this observation help?

Recursion naturally handles "go all the way down, then come back up" for us — we don't need to manage an explicit stack ourselves. Placing a single `result.append(node.val)` line between the two recursive calls is enough to produce a correctly ordered traversal for a tree of any shape.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture standing at a node holding two instructions: "finish everything to my left before you look at me, and don't look right until you've looked at me." Every node repeats this same rule for its own children, so the whole tree unfolds into one path that dips all the way to the leftmost leaf before recording anything.

```text
        1
         \
          2
         /
        3

Call stack grows downward (leftmost first):

dfs(1)
  dfs(None)     <- nothing to do, unwind immediately
  visit 1       <- record 1
  dfs(2)
    dfs(3)
      dfs(None) <- nothing to do, unwind immediately
      visit 3   <- record 3
      dfs(None) <- nothing to do, unwind immediately
    visit 2     <- record 2
    dfs(None)   <- nothing to do, unwind immediately
```

The recursion stack itself *is* the traversal order — reading the "visit" lines top to bottom gives `[1, 3, 2]`.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
dfs(node)
   │
   ▼
Is node None ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return              dfs(node.left)
(nothing to visit)     │
                        ▼
                    Append node.val to result
                        │
                        ▼
                    dfs(node.right)
                        │
                        ▼
                      Return
```

Explanation of each decision:

- A `None` node is the base case — there's nothing to visit, so recursion simply unwinds.
- The left subtree is always fully explored before the current node is recorded.
- The current node is appended to `result` only after its entire left subtree has been visited.
- The right subtree is explored last, after the current node has already been recorded.

---

# 5. Plain English Algorithm

1. If the current node is `None`, return immediately — there's nothing to visit.
2. Otherwise, recurse into the left child first.
3. Append the current node's value to the result list.
4. Recurse into the right child.
5. Start this process at `root`, and return the accumulated result list once the initial call returns.

---

# 6. Pseudocode

```text
result = []

function dfs(node):
    if node is None:
        return

    dfs(node.left)
    result.append(node.val)
    dfs(node.right)

dfs(root)
return result
```

---

# 7. Python Solution

```python
class Solution:
    def inorderTraversal(self, root: TreeNode | None) -> list[int]:
        result = []

        def dfs(node):
            if node is None:
                return node

            # Traverse left subtree
            dfs(node.left)

            # Visit the current node
            result.append(node.val)

            # Traverse right subtree
            dfs(node.right)

        dfs(root)
        return result
```

---

# 8. Dry Run

Example:

```text
root = [1,null,2,3]

Tree:
1
 \
  2
 /
3
```

| Step | Call | Node | Action | `result` so far | Why? |
|------|------|------|--------|------------------|------|
| 1 | `dfs(1)` | 1 | Recurse left: `dfs(1.left)` = `dfs(None)` | `[]` | Must fully explore left before visiting 1 |
| 2 | `dfs(None)` | — | Return immediately | `[]` | Base case: node is `None` |
| 3 | `dfs(1)` (resume) | 1 | Append `1.val` | `[1]` | Left subtree done, now visit current node |
| 4 | `dfs(1)` (resume) | 1 | Recurse right: `dfs(2)` | `[1]` | Visit right subtree last |
| 5 | `dfs(2)` | 2 | Recurse left: `dfs(3)` | `[1]` | Must fully explore left before visiting 2 |
| 6 | `dfs(3)` | 3 | Recurse left: `dfs(None)` | `[1]` | Must fully explore left before visiting 3 |
| 7 | `dfs(None)` | — | Return immediately | `[1]` | Base case: node is `None` |
| 8 | `dfs(3)` (resume) | 3 | Append `3.val` | `[1,3]` | Left subtree done, now visit current node |
| 9 | `dfs(3)` (resume) | 3 | Recurse right: `dfs(None)`, return immediately | `[1,3]` | 3 has no right child |
| 10 | `dfs(2)` (resume) | 2 | Append `2.val` | `[1,3,2]` | Left subtree (3) done, now visit current node |
| 11 | `dfs(2)` (resume) | 2 | Recurse right: `dfs(None)`, return immediately | `[1,3,2]` | 2 has no right child |

Result: `[1,3,2]`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- Every node is visited exactly once.
- Each visit does O(1) work (a single `append`).

### Space Complexity

```text
O(n)
```

Why?

- The result list holds all `n` values.
- The recursion stack holds at most `O(h)` frames at once, where `h` is the tree height — worst case `O(n)` for a skewed tree.
