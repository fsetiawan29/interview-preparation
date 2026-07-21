"""ASCII visualization for stacks (last element rendered on top)."""

from __future__ import annotations

from typing import Any


def render_stack(values: list[Any]) -> str:
    """Render a stack with the top of the stack shown first.

    Example::

        Top
        +------+
        |  10  |
        +------+
        |   5  |
        +------+
    """
    if not values:
        return "Top\n(empty)"

    width = max(4, max(len(str(v)) for v in values) + 2)
    border = "+" + "-" * width + "+"

    lines = ["Top"]
    for value in reversed(values):
        lines.append(border)
        lines.append("|" + str(value).center(width) + "|")
    lines.append(border)
    return "\n".join(lines)
