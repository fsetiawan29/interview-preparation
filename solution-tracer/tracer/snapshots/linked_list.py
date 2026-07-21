"""ASCII visualization for singly linked lists."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class _Node(Protocol):
    val: Any
    next: Any


def render_linked_list(head: _Node | list[Any] | None) -> str:
    """Render a linked list (or plain Python list standing in for one).

    Example::

        1 -> 2 -> 3 -> None
    """
    values: list[Any] = []

    if isinstance(head, list):
        values = [str(v) for v in head]
    else:
        node = head
        seen: set[int] = set()
        while node is not None and id(node) not in seen:
            seen.add(id(node))
            values.append(str(node.val))
            node = node.next

    return " -> ".join(values + ["None"])
