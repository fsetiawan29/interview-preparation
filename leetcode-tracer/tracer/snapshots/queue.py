"""ASCII visualization for FIFO queues."""

from __future__ import annotations

from typing import Any


def render_queue(values: list[Any]) -> str:
    """Render a queue with the front element shown first.

    Example::

        Front
        [3][7][9][12]
    """
    if not values:
        return "Front\n[]"
    body = "".join(f"[{v}]" for v in values)
    return f"Front\n{body}"
