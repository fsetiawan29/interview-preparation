"""Automatic tracing for unmodified solutions, via `sys.settrace`.

No `trace.*` calls are needed in the algorithm itself. `autotrace` runs the
function under a line tracer, records a variable-trace step whenever local
state changes, and tracks recursion depth from call/return events — so you
can write a plain, unmodified solution and still get a full report.
"""

from __future__ import annotations

import sys
from types import FrameType
from typing import Any, Callable

from .recorder import TraceRecorder
from .utils import is_primitive

_CONTAINER_TYPES = (list, dict, set, frozenset, tuple)


def _is_capturable(name: str, value: Any) -> bool:
    return not name.startswith("__") and (is_primitive(value) or isinstance(value, _CONTAINER_TYPES))


def _snapshot_locals(frame: FrameType) -> dict[str, Any]:
    snapshot: dict[str, Any] = {}
    for name, value in frame.f_locals.items():
        if not _is_capturable(name, value):
            continue
        snapshot[name] = value.copy() if isinstance(value, (list, dict, set)) else value
    return snapshot


def autotrace(
    func: Callable[..., Any],
    *args: Any,
    problem: str | None = None,
    max_steps: int = 5000,
    **kwargs: Any,
) -> tuple[Any, TraceRecorder]:
    """Run ``func(*args, **kwargs)`` and build a `TraceRecorder` automatically.

    Example::

        from tracer import autotrace

        class Solution:
            def twoSum(self, nums, target):
                seen = {}
                for i, num in enumerate(nums):
                    complement = target - num
                    if complement in seen:
                        return [seen[complement], i]
                    seen[num] = i

        result, trace = autotrace(Solution().twoSum, [2, 7, 11, 15], 9)
        trace.display()

    Every time a traced line executes and local variables (primitives,
    lists, dicts, sets, tuples — anything JSON-shaped) differ from the
    previous snapshot, a new variable-trace row is recorded. Tracing
    follows any call into a function defined in the same source file as
    `func` — not just `func` itself — so nested recursive helpers (e.g. a
    `dfs` closure inside a DFS solution's outer method) are captured too,
    and their nesting is reported as "Maximum recursion depth" (0 for a
    non-recursive function).
    """
    name = problem or getattr(func, "__qualname__", getattr(func, "__name__", "Untitled"))
    input_data = {"args": args, "kwargs": kwargs} if (args or kwargs) else None
    trace = TraceRecorder(name, input_data=input_data)

    target_filename = func.__code__.co_filename
    step_count = 0
    depth = 0
    last_snapshot: dict[str, Any] | None = None

    def tracer(frame: FrameType, event: str, arg: Any) -> Any:
        nonlocal step_count, depth, last_snapshot

        if event == "call":
            if frame.f_code.co_filename != target_filename:
                return None
            depth += 1
            trace._note_recursion_depth(depth - 1)
            if depth > 1:
                trace.event(f"Call {frame.f_code.co_name} (depth {depth - 1})")
            return tracer

        if event == "line":
            if step_count < max_steps:
                snapshot = _snapshot_locals(frame)
                if snapshot != last_snapshot:
                    step_count += 1
                    trace.step(iteration=step_count, variables=snapshot)
                    last_snapshot = snapshot
            return tracer

        if event == "return":
            depth -= 1
            return tracer

        return tracer

    old_tracer = sys.gettrace()
    sys.settrace(tracer)
    try:
        result = func(*args, **kwargs)
    finally:
        sys.settrace(old_tracer)

    trace.finish(answer=result)
    return result, trace
