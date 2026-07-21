"""Small, dependency-free helpers shared across the tracer package."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .models import StepRecord

_PRIMITIVE_TYPES = (int, float, str, bool, type(None))


def is_primitive(value: Any) -> bool:
    """Return True for values that are safe to auto-capture (no containers)."""
    return isinstance(value, _PRIMITIVE_TYPES)


def stringify(value: Any) -> str:
    """Render a value for table/text display, truncating long collections."""
    if isinstance(value, dict):
        items = list(value.items())
        shown = ", ".join(f"{k}: {v}" for k, v in items[:6])
        suffix = ", ..." if len(items) > 6 else ""
        return "{" + shown + suffix + "}"
    if isinstance(value, (list, tuple, set)):
        values = list(value)
        shown = ", ".join(str(v) for v in values[:8])
        suffix = ", ..." if len(values) > 8 else ""
        opener, closer = ("[", "]") if not isinstance(value, (tuple, set)) else (
            ("(", ")") if isinstance(value, tuple) else ("{", "}")
        )
        return f"{opener}{shown}{suffix}{closer}"
    return str(value)


def step_variable_keys(steps: list["StepRecord"]) -> list[str]:
    """Union of variable names across all steps, in first-seen order.

    Steps don't always share the same keys — `trace.auto`/`autotrace`
    capture whatever locals exist at each point, which grows as the
    function runs. Using only the first step's keys would misalign later
    rows, so the header set is the union across every step.
    """
    keys: dict[str, None] = {}
    for step in steps:
        for key in step.variables:
            keys.setdefault(key, None)
    return list(keys)


def render_table(headers: list[str], rows: list[list[str]], *, markdown: bool = False) -> str:
    """Render a plain-text or markdown table for a list of stringified rows."""
    if not rows:
        return "(no data)" if not markdown else f"| {' | '.join(headers)} |\n| {' | '.join('---' for _ in headers)} |"

    if markdown:
        lines = [f"| {' | '.join(headers)} |", f"| {' | '.join('---' for _ in headers)} |"]
        for row in rows:
            lines.append(f"| {' | '.join(row)} |")
        return "\n".join(lines)

    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt_row(cells: list[str]) -> str:
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells))

    lines = [fmt_row(headers), "  ".join("-" * w for w in widths)]
    for row in rows:
        lines.append(fmt_row(row))
    return "\n".join(lines)
