"""ASCII visualization for binary heaps stored as flat arrays."""

from __future__ import annotations

from typing import Any


class _ArrayNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val: Any, left: "_ArrayNode | None", right: "_ArrayNode | None") -> None:
        self.val = val
        self.left = left
        self.right = right


def _build_tree(values: list[Any], i: int = 0) -> _ArrayNode | None:
    if i >= len(values):
        return None
    return _ArrayNode(
        values[i],
        _build_tree(values, 2 * i + 1),
        _build_tree(values, 2 * i + 2),
    )


def render_heap(values: list[Any]) -> str:
    """Render a heap (array form) as a binary tree.

    Example::

              2
             / \\
            5   8
           /
          10
    """
    from .tree import render_tree

    if not values:
        return "(empty)"
    return render_tree(_build_tree(values))
