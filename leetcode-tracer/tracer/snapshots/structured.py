"""Structured (JSON-ready) snapshot payloads, matching docs/trace-schema.md.

These sit alongside the ASCII renderers in this package: the ASCII renderers
stay focused on console/markdown output, while these functions build the
`values`/`nodes`/`edges`/... payloads the React visualizer consumes.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Iterable


def array_data(
    values: list[Any], pointers: dict[str, int] | None, highlights: list[int] | None
) -> dict[str, Any]:
    return {
        "type": "array",
        "values": list(values),
        "highlights": list(highlights) if highlights else [],
        "pointers": dict(pointers) if pointers else {},
    }


def stack_data(values: list[Any], highlights: list[int] | None) -> dict[str, Any]:
    return {"type": "stack", "values": list(values), "highlights": list(highlights) if highlights else []}


def queue_data(values: list[Any], highlights: list[int] | None) -> dict[str, Any]:
    return {"type": "queue", "values": list(values), "highlights": list(highlights) if highlights else []}


def heap_data(values: list[Any], highlights: list[int] | None) -> dict[str, Any]:
    return {"type": "heap", "values": list(values), "highlights": list(highlights) if highlights else []}


def _walk_tree(root: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[int, int]]:
    """BFS walk of a `.left`/`.right` binary tree into flat nodes/edges."""
    node_id_of: dict[int, int] = {}
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    if root is None:
        return nodes, edges, node_id_of

    node_id_of[id(root)] = 0
    queue: deque[Any] = deque([root])
    visited: set[int] = set()

    while queue:
        node = queue.popleft()
        if id(node) in visited:
            continue
        visited.add(id(node))
        nid = node_id_of[id(node)]

        left = getattr(node, "left", None)
        right = getattr(node, "right", None)
        left_id = right_id = None

        if left is not None:
            left_id = node_id_of.setdefault(id(left), len(node_id_of))
            edges.append({"from": nid, "to": left_id})
            queue.append(left)
        if right is not None:
            right_id = node_id_of.setdefault(id(right), len(node_id_of))
            edges.append({"from": nid, "to": right_id})
            queue.append(right)

        nodes.append({"id": nid, "val": node.val, "left": left_id, "right": right_id})

    nodes.sort(key=lambda n: n["id"])
    return nodes, edges, node_id_of


def tree_data(root: Any, current: Any, visited: Iterable[Any] | None) -> dict[str, Any]:
    nodes, edges, node_id_of = _walk_tree(root)
    current_id = node_id_of.get(id(current)) if current is not None else None
    visited_ids = [node_id_of[id(v)] for v in (visited or []) if id(v) in node_id_of]
    return {
        "type": "tree",
        "nodes": nodes,
        "edges": edges,
        "current": current_id,
        "visited": visited_ids,
    }


def graph_data(
    adjacency: dict[Any, Iterable[Any]], current: Any, visited: Iterable[Any] | None
) -> dict[str, Any]:
    nodes = [{"id": str(k), "label": str(k)} for k in adjacency]
    edges = [
        {"from": str(k), "to": str(n)} for k, neighbors in adjacency.items() for n in neighbors
    ]
    return {
        "type": "graph",
        "nodes": nodes,
        "edges": edges,
        "current": str(current) if current is not None else None,
        "visited": [str(v) for v in (visited or [])],
    }


def _walk_linked_list(head: Any) -> tuple[list[dict[str, Any]], dict[int, int]]:
    if isinstance(head, list):
        n = len(head)
        nodes = [{"id": i, "val": v, "next": i + 1 if i + 1 < n else None} for i, v in enumerate(head)]
        return nodes, {i: i for i in range(n)}

    node_id_of: dict[int, int] = {}
    chain: list[Any] = []
    node = head
    seen: set[int] = set()
    while node is not None and id(node) not in seen:
        seen.add(id(node))
        chain.append(node)
        node_id_of[id(node)] = len(chain) - 1
        node = getattr(node, "next", None)

    nodes = []
    for i, chain_node in enumerate(chain):
        nxt = getattr(chain_node, "next", None)
        next_id = node_id_of.get(id(nxt)) if nxt is not None else None
        nodes.append({"id": i, "val": chain_node.val, "next": next_id})

    return nodes, node_id_of


def linked_list_data(head: Any, current: Any) -> dict[str, Any]:
    nodes, node_id_of = _walk_linked_list(head)
    if isinstance(head, list):
        current_id = current if isinstance(current, int) else None
    else:
        current_id = node_id_of.get(id(current)) if current is not None else None
    return {"type": "linked-list", "nodes": nodes, "current": current_id}
