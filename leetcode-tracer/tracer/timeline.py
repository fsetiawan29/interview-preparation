"""Chronological event-flow rendering."""

from __future__ import annotations

from .models import EventRecord, HistoryEntry


def render_timeline(history: list[HistoryEntry]) -> str:
    """Render the recorded events as a top-to-bottom arrow chain.

    Example::

        Start

        ↓

        Create hash set

        ↓

        Visit 100
    """
    messages = [entry.record.message for entry in history if isinstance(entry.record, EventRecord)]
    if not messages:
        return "(no events recorded)"
    return "\n\n↓\n\n".join(messages)
