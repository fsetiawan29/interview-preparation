"""Data records produced by :class:`tracer.recorder.TraceRecorder`."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class StepRecord:
    iteration: int
    variables: dict[str, Any]
    timestamp: float = field(default_factory=time.perf_counter)


@dataclass
class EventRecord:
    message: str
    iteration: int | None = None
    timestamp: float = field(default_factory=time.perf_counter)


@dataclass
class DecisionRecord:
    condition: str
    result: bool
    action: str
    iteration: int | None = None
    timestamp: float = field(default_factory=time.perf_counter)


@dataclass
class SnapshotRecord:
    kind: str
    rendered: str
    data: dict[str, Any] = field(default_factory=dict)
    label: str | None = None
    iteration: int | None = None
    size: int = 0
    timestamp: float = field(default_factory=time.perf_counter)


@dataclass
class HistoryEntry:
    """A single chronological entry tying together every record type."""

    seq: int
    kind: str  # "step" | "event" | "decision" | "snapshot"
    record: StepRecord | EventRecord | DecisionRecord | SnapshotRecord


@dataclass
class Summary:
    iterations: int
    skipped_iterations: int
    while_loops: int
    max_recursion_depth: int
    max_stack_size: int
    max_queue_size: int
    max_heap_size: int
    execution_time: float
    answer: Any = None
