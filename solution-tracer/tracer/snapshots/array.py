"""ASCII visualization for arrays/lists, with optional named pointers."""

from __future__ import annotations

from typing import Any


def render_array(values: list[Any], pointers: dict[str, int] | None = None) -> str:
    """Render an index/value grid with optional pointer markers underneath.

    Example::

        Index
        0 1 2 3 4
        Value
        2 7 11 15 18
         ^
         L
    """
    cells = [str(v) for v in values]
    widths = [max(len(str(i)), len(cells[i])) for i in range(len(values))]

    index_line = " ".join(str(i).rjust(widths[i]) for i in range(len(values)))
    value_line = " ".join(cells[i].rjust(widths[i]) for i in range(len(values)))

    lines = ["Index", index_line, "", "Value", value_line]

    if pointers:
        by_index: dict[int, list[str]] = {}
        for label, idx in pointers.items():
            by_index.setdefault(idx, []).append(label)

        offsets = [sum(widths[j] + 1 for j in range(i)) for i in range(len(values))]

        for idx in sorted(by_index):
            if idx < 0 or idx >= len(values):
                continue
            offset = offsets[idx]
            marker = " " * offset + "^"
            label = " " * offset + "/".join(by_index[idx])
            lines.append(marker)
            lines.append(label)

    return "\n".join(lines)
