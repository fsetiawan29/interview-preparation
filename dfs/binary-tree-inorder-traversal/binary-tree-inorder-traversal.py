from __future__ import annotations


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


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


def build_tree(values: list) -> TreeNode | None:
    """Build a binary tree from a LeetCode-style level-order list (with None gaps)."""
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values):
            if values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
    return root


if __name__ == "__main__":
    test_cases = [
        ([1, None, 2, 3], [1, 3, 2]),
        ([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9], [4, 2, 6, 5, 7, 1, 3, 9, 8]),
        ([], []),
        ([1], [1]),
    ]

    solution = Solution()
    for i, (values, expected) in enumerate(test_cases, start=1):
        root = build_tree(values)
        result = solution.inorderTraversal(root)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i}: {status} | input={values} expected={expected} got={result}")
