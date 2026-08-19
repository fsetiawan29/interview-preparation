# Problem: Binary Tree Preorder Traversal

## 1. Problem Understanding

### Problem Summary

Given the root of a binary tree, return the values of its nodes using a
**preorder traversal** — visit the current node first, then the left
subtree, then the right subtree.

### Input

- The root of a binary tree, `root`

### Output

- A list of integers representing the node values in preorder sequence.

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
[1,2,3]
```

Manual walkthrough:

```text
Tree:

1
 \
  2
 /
3

Preorder = node, left, right

Start at 1 -> visit 1
           -> go left (None, nothing to visit)
           -> go right to 2
              -> visit 2
              -> go left to 3
                 -> visit 3
                 -> go left (None, nothing to visit)
                 -> go right (None, nothing to visit)
              -> go right (None, nothing to visit)

Visited order: 1, 2, 3

↓

[1,2,3]
```

---

## 2. Brute Force Approach

### Idea

Instead of appending into one shared result list, have every recursive
call build and return its own brand-new list by concatenating its own
value, its left subtree's values, and its right subtree's values.

### Pseudocode

```text
function dfs(node)
    if node is None
        return []

    left_values = dfs(node.left)
    right_values = dfs(node.right)

    return [node.val] + left_values + right_values   // creates a new list every call

return dfs(root)
```

### Complexity Analysis

#### Time Complexity

```text
O(n^2)
```

Why?

- `n` = number of nodes. In the worst case (a skewed tree), each level's
  concatenation copies the entire list accumulated so far, and this
  happens at every one of the `n` levels — `1 + 2 + ... + n = O(n^2)`.

#### Space Complexity

```text
O(n^2)
```

Why?

- Every level of recursion allocates a fresh, fully-copied list, so the
  total memory churned across all the intermediate concatenations is
  `O(n^2)` in the worst case (beyond the final `O(n)`-sized output).

### Why this isn't good enough

Building a new list at every recursive call means the same values get
copied over and over as they bubble up toward the root. Appending directly
into one shared `result` list — passed by reference into every call
instead of returned and concatenated — means each value is written exactly
once, dropping the total work to `O(n)`.

---

## 3. Key Insight

### What makes this problem difficult?

It's tempting to think of "traversal" as scanning the tree left-to-right
the way you'd scan an array, but a tree has no single linear layout — the
only way to visit nodes in a well-defined order is to let recursion do the
walking. The order in which the "visit" step is placed relative to the two
recursive calls (before, between, or after) is exactly what defines
pre/in/post-order.

### Key Observation

Visiting the current node *before* recursing into either child, then
recursing left before right, guarantees every node's value lands in the
result list exactly once, in root-first, left-to-right structural order.

Example:

```text
    2
   / \
  1   3

dfs(2):
  append 2
  dfs(1) -> append 1
  dfs(3) -> append 3

result = [2, 1, 3]
```

### Why does this observation help?

Recursion naturally handles "record me, then go all the way down, then
come back up" for us — we don't need to manage an explicit stack
ourselves. Placing a single `result.append(node.val)` line before the two
recursive calls is enough to produce a correctly ordered traversal for a
tree of any shape.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture standing at a node with one instruction: "announce yourself the
moment you arrive, then finish everything to your left before you look
right." Every node repeats this same rule for its own children, so the
whole tree unfolds into one path that announces a node the instant it's
first reached, then dips left before circling back for the right side.

```text
        1
         \
          2
         /
        3

Call stack grows downward (leftmost first):

dfs(1)
  visit 1       <- record 1, the instant we arrive
  dfs(None)     <- nothing to do, unwind immediately
  dfs(2)
    visit 2     <- record 2, the instant we arrive
    dfs(3)
      visit 3   <- record 3, the instant we arrive
      dfs(None) <- nothing to do, unwind immediately
      dfs(None) <- nothing to do, unwind immediately
    dfs(None)   <- nothing to do, unwind immediately
```

The recursion stack itself *is* the traversal order — reading the "visit"
lines top to bottom gives `[1, 2, 3]`.

---

## 5. Decision Tree

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
Return              Append node.val to result
(nothing to visit)     │
                        ▼
                    dfs(node.left)
                        │
                        ▼
                    dfs(node.right)
                        │
                        ▼
                      Return
```

Explanation of each decision:

- A `None`/`nil` node is the base case — there's nothing to visit, so
  recursion simply unwinds.
- The current node is appended to `result` immediately, before either
  child is explored.
- The left subtree is always fully explored before the right subtree is
  even started.

---

## 6. Plain English Algorithm

1. If the current node is `nil`, return immediately — there's nothing to
   visit.
2. Otherwise, append the current node's value to the result list.
3. Recurse into the left child.
4. Recurse into the right child.
5. Start this process at `root`, and return the accumulated result list
   once the initial call returns.

---

## 7. Pseudocode

```text
result = []

function dfs(node):
    if node is None:
        return

    result.append(node.val)
    dfs(node.left)
    dfs(node.right)

dfs(root)
return result
```

---

## 8. Go Solution

```go
package solution

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func preorderTraversal(root *TreeNode) []int {
	var res []int

	var dfs func(node *TreeNode)
	dfs = func(node *TreeNode) {
		if node == nil {
			return
		}

		res = append(res, node.Val)

		dfs(node.Left)

		dfs(node.Right)
	}

	dfs(root)

	return res
}
```

---

## 9. Dry Run

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

| Step | Call | Node | Action | `res` so far | Why? |
|------|------|------|--------|---------------|------|
| 1 | `dfs(1)` | 1 | Append `1.Val` | `[1]` | Visit the node before recursing anywhere |
| 2 | `dfs(1)` (cont.) | 1 | Recurse left: `dfs(nil)` | `[1]` | Left subtree explored first |
| 3 | `dfs(nil)` | — | Return immediately | `[1]` | Base case: node is `nil` |
| 4 | `dfs(1)` (resume) | 1 | Recurse right: `dfs(2)` | `[1]` | Right subtree explored last |
| 5 | `dfs(2)` | 2 | Append `2.Val` | `[1,2]` | Visit 2 before recursing into its children |
| 6 | `dfs(2)` (cont.) | 2 | Recurse left: `dfs(3)` | `[1,2]` | Left subtree explored first |
| 7 | `dfs(3)` | 3 | Append `3.Val` | `[1,2,3]` | Visit 3 before recursing into its children |
| 8 | `dfs(3)` (cont.) | 3 | Recurse left: `dfs(nil)`, return immediately | `[1,2,3]` | 3 has no left child |
| 9 | `dfs(3)` (resume) | 3 | Recurse right: `dfs(nil)`, return immediately | `[1,2,3]` | 3 has no right child |
| 10 | `dfs(2)` (resume) | 2 | Recurse right: `dfs(nil)`, return immediately | `[1,2,3]` | 2 has no right child |

Result: `[1,2,3]`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- Every node is visited exactly once.
- Each visit does O(1) work (a single append).

### Space Complexity

```text
O(n)
```

Why?

- The result slice holds all `n` values.
- The recursion stack holds at most `O(h)` frames at once, where `h` is
  the tree height — worst case `O(n)` for a skewed tree.
