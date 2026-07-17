from typing import Optional, List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


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


def build_tree(values):
    """Build a binary tree from a LeetCode-style level-order list (with None gaps)."""
    if not values or values[0] is None:
        return None

    nodes = [None if v is None else TreeNode(v) for v in values]
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node:
            if kids:
                child = kids.pop()
                node.left = child
            if kids:
                child = kids.pop()
                node.right = child
    return root


def run_test(name, values, expected):
    root = build_tree(values)
    result = Solution().binaryTreePaths(root)
    passed = sorted(result) == sorted(expected)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    {values}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 2, 3, None, 5],
        ["1->2->5", "1->3"],
    )

    run_test(
        "Example 2",
        [1],
        ["1"],
    )

    run_test(
        "Left skewed",
        [1, 2, None, 3],
        ["1->2->3"],
    )

    run_test(
        "Negative values",
        [-1, -2, -3],
        ["-1->-2", "-1->-3"],
    )

    run_test(
        "Full small tree",
        [1, 2, 3, 4, 5, 6, 7],
        ["1->2->4", "1->2->5", "1->3->6", "1->3->7"],
    )
