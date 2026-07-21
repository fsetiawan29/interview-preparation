"""Automatic summary statistics derived from a recording session."""

from __future__ import annotations

from typing import Any

from .models import DecisionRecord, EventRecord, HistoryEntry, StepRecord, Summary


def compute_summary(
    history: list[HistoryEntry],
    *,
    execution_time: float,
    max_recursion_depth: int,
    answer: Any,
) -> Summary:
    steps = [entry.record for entry in history if isinstance(entry.record, StepRecord)]
    events = [entry.record for entry in history if isinstance(entry.record, EventRecord)]
    decisions = [entry.record for entry in history if isinstance(entry.record, DecisionRecord)]

    iterations = len(steps)
    skipped_iterations = sum(1 for e in events if e.message.lower().startswith("skip"))
    while_loops = sum(
        1 for d in decisions if d.result and "while" in d.action.lower()
    )

    max_stack_size = _max_snapshot_size(history, "stack")
    max_queue_size = _max_snapshot_size(history, "queue")
    max_heap_size = _max_snapshot_size(history, "heap")

    return Summary(
        iterations=iterations,
        skipped_iterations=skipped_iterations,
        while_loops=while_loops,
        max_recursion_depth=max_recursion_depth,
        max_stack_size=max_stack_size,
        max_queue_size=max_queue_size,
        max_heap_size=max_heap_size,
        execution_time=execution_time,
        answer=answer,
    )


def _max_snapshot_size(history: list[HistoryEntry], kind: str) -> int:
    sizes = [
        entry.record.size
        for entry in history
        if entry.kind == "snapshot" and getattr(entry.record, "kind", None) == kind
    ]
    return max(sizes, default=0)
