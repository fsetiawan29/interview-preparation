"""leetcode-tracer: educational execution tracing for LeetCode solutions."""

from .autotrace import autotrace
from .config import TracerConfig
from .models import DecisionRecord, EventRecord, HistoryEntry, SnapshotRecord, StepRecord, Summary
from .recorder import TraceRecorder, trace_algorithm

__all__ = [
    "TraceRecorder",
    "trace_algorithm",
    "autotrace",
    "TracerConfig",
    "StepRecord",
    "EventRecord",
    "DecisionRecord",
    "SnapshotRecord",
    "HistoryEntry",
    "Summary",
]

__version__ = "0.1.0"
