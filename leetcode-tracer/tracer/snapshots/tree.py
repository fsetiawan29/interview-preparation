"""ASCII visualization for binary trees."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class _TreeNode(Protocol):
    val: Any
    left: Any
    right: Any


def render_tree(root: _TreeNode | None) -> str:
    """Render a binary tree top-down, centered, using level-order layout.

    Example::

                5
              /   \\
             3     8
            / \\
           1   4
    """
    if root is None:
        return "(empty)"

    def val_str(node: _TreeNode | None) -> str:
        return str(node.val) if node is not None else ""

    levels: list[list[_TreeNode | None]] = [[root]]
    while any(n is not None for n in levels[-1]):
        next_level: list[_TreeNode | None] = []
        for node in levels[-1]:
            if node is None:
                next_level.extend([None, None])
            else:
                next_level.append(getattr(node, "left", None))
                next_level.append(getattr(node, "right", None))
        levels.append(next_level)
    levels.pop()  # drop the all-None level

    node_width = max((len(val_str(n)) for level in levels for n in level), default=1)
    node_width = max(node_width, 1)

    depth = len(levels)
    lines: list[str] = []
    for level_index, level in enumerate(levels):
        gap = 2 ** (depth - level_index) - 1
        lead = 2 ** (depth - level_index - 1) - 1

        cells = [val_str(node).center(node_width) for node in level]
        row = " " * (lead * node_width) + (" " * gap * node_width).join(cells)
        lines.append(row.rstrip())

    return "\n".join(lines)
