"""Binary Tree Level Order Traversal, instrumented with solution-tracer.

A BFS over a binary tree — gives the visualizer real `tree` snapshots (with
a highlighted current node) plus `queue` snapshots for the BFS frontier.
"""

from __future__ import annotations

from collections import deque
from typing import Any, List, Optional

from tracer import TraceRecorder
from tracer.cli import main


class TreeNode:
    def __init__(self, val: int, left: "TreeNode | None" = None, right: "TreeNode | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def build_tree(values: List[Optional[int]]) -> TreeNode | None:
    """Build a binary tree from a level-order list (None = missing child)."""
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


class Solution:
    def levelOrder(self, root: TreeNode | None, trace: TraceRecorder | None = None) -> List[List[int]]:
        result: List[List[int]] = []
        if root is None:
            return result

        queue: deque[TreeNode] = deque([root])
        i = 0

        while queue:
            level_size = len(queue)
            level: List[int] = []

            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)

                if trace:
                    trace.event(f"Visit {node.val}", iteration=i)
                    trace.step(iteration=i, variables={"current": node.val, "level": list(level)})
                    trace.snapshot_tree(root, current=node, iteration=i)
                i += 1

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

                if trace:
                    trace.event(f"Enqueue children of {node.val}", iteration=i)
                    trace.step(iteration=i, variables={"current": node.val, "queue": [n.val for n in queue]})
                    trace.snapshot_queue([n.val for n in queue], iteration=i)
                i += 1

            result.append(level)
            if trace:
                trace.decision(
                    condition="queue empty",
                    result=not queue,
                    action="Finish traversal" if not queue else "Process next level",
                    iteration=i - 1,
                )

        return result


def run(values: List[Optional[int]]) -> tuple[List[List[int]], TraceRecorder]:
    trace = TraceRecorder(
        "Binary Tree Level Order Traversal",
        input_data={"root": values},
        difficulty="Medium",
        algorithm="BFS",
        time_complexity="O(n)",
        space_complexity="O(n)",
    )
    root = build_tree(values)
    result = Solution().levelOrder(root, trace=trace)
    trace.finish(answer=result)
    return result, trace


if __name__ == "__main__":
    main(run, [3, 9, 20, None, None, 15, 7])
