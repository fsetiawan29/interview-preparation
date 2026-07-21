"""Textual visualization for graphs given as an adjacency mapping."""

from __future__ import annotations

from typing import Any, Iterable


def render_graph(adjacency: dict[Any, Iterable[Any]]) -> str:
    """Render a graph as a deduplicated edge list.

    Arbitrary graphs don't have a canonical 2D ASCII layout, so the tracer
    renders a stable, readable edge list instead::

        A -- B
        A -- C
        B -- D
    """
    if not adjacency:
        return "(empty)"

    seen: set[tuple[str, str]] = set()
    lines: list[str] = []
    for node, neighbors in adjacency.items():
        for neighbor in neighbors:
            key = tuple(sorted((str(node), str(neighbor))))
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"{node} -- {neighbor}")

    return "\n".join(lines) if lines else "\n".join(f"{node}" for node in adjacency)
