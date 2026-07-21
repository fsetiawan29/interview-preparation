"""The central instrumentation API: :class:`TraceRecorder`."""

from __future__ import annotations

import time
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Iterator

from .config import TracerConfig
from .formatters.csv import Section, render_csv
from .formatters.json import render_json
from .formatters.markdown import render_markdown
from .formatters.stdout import render_console
from .models import DecisionRecord, EventRecord, HistoryEntry, StepRecord, SnapshotRecord, Summary
from .snapshots import (
    array_data,
    graph_data,
    heap_data,
    linked_list_data,
    queue_data,
    render_array,
    render_graph,
    render_heap,
    render_linked_list,
    render_queue,
    render_stack,
    render_tree,
    stack_data,
    tree_data,
)
from .statistics import compute_summary
from .utils import is_primitive


class TraceRecorder:
    """Collects trace events for a single algorithm run and reports on them.

    Instrumenting a solution requires only a few extra lines and never
    changes the algorithm's logic::

        trace = TraceRecorder("Two Sum")
        trace.step(iteration=i, variables={"num": num})
        trace.event("Found pair")
        trace.finish(answer=result)
        trace.export_markdown("trace.md")
    """

    def __init__(
        self,
        problem: str,
        input_data: Any = None,
        config: TracerConfig | None = None,
        *,
        difficulty: str | None = None,
        algorithm: str | None = None,
        time_complexity: str | None = None,
        space_complexity: str | None = None,
        language: str = "Python",
    ) -> None:
        self.problem = problem
        self.input_data = input_data
        self.config = config or TracerConfig()

        self.difficulty = difficulty
        self.algorithm = algorithm
        self.time_complexity = time_complexity
        self.space_complexity = space_complexity
        self.language = language

        self.history: list[HistoryEntry] = []
        self._seq = 0
        self._auto_iteration = 0
        self._current_iteration: int | None = None

        self._start_time = time.perf_counter()
        self._end_time: float | None = None
        self._answer: Any = None

        self._recursion_depth = 0
        self._max_recursion_depth = 0

    # -- recording -----------------------------------------------------

    def step(self, iteration: int, variables: dict[str, Any]) -> None:
        """Record a variable snapshot for a given iteration (variable trace)."""
        self._current_iteration = iteration
        self._append("step", StepRecord(iteration=iteration, variables=dict(variables)))

    def iteration(self, values: dict[str, Any]) -> None:
        """Record a row in the iteration table, auto-numbering iterations."""
        self._auto_iteration += 1
        self._current_iteration = self._auto_iteration
        self._append(
            "step", StepRecord(iteration=self._auto_iteration, variables=dict(values))
        )

    def event(self, message: str, iteration: int | None = None) -> None:
        """Record a generic, human-readable event."""
        self._append("event", EventRecord(message=message, iteration=iteration))

    def decision(self, condition: str, result: bool, action: str, iteration: int | None = None) -> None:
        """Record a branch/decision point taken by the algorithm."""
        self._append(
            "decision",
            DecisionRecord(condition=condition, result=result, action=action, iteration=iteration),
        )

    def auto(self, local_vars: dict[str, Any], iteration: int | None = None) -> None:
        """Capture primitive locals automatically, e.g. ``trace.auto(locals())``."""
        captured = {k: v for k, v in local_vars.items() if is_primitive(v) and not k.startswith("_")}
        if iteration is None:
            self.iteration(captured)
        else:
            self.step(iteration, captured)

    # -- snapshots -------------------------------------------------------

    def snapshot_array(
        self,
        values: list[Any],
        pointers: dict[str, int] | None = None,
        highlights: list[int] | None = None,
        label: str | None = None,
        iteration: int | None = None,
    ) -> None:
        self._snapshot(
            "array", render_array(values, pointers), len(values), label,
            array_data(values, pointers, highlights), iteration,
        )

    def snapshot_stack(
        self, values: list[Any], highlights: list[int] | None = None,
        label: str | None = None, iteration: int | None = None,
    ) -> None:
        self._snapshot(
            "stack", render_stack(values), len(values), label,
            stack_data(values, highlights), iteration,
        )

    def snapshot_queue(
        self, values: list[Any], highlights: list[int] | None = None,
        label: str | None = None, iteration: int | None = None,
    ) -> None:
        self._snapshot(
            "queue", render_queue(values), len(values), label,
            queue_data(values, highlights), iteration,
        )

    def snapshot_heap(
        self, values: list[Any], highlights: list[int] | None = None,
        label: str | None = None, iteration: int | None = None,
    ) -> None:
        self._snapshot(
            "heap", render_heap(values), len(values), label,
            heap_data(values, highlights), iteration,
        )

    def snapshot_tree(
        self, root: Any, current: Any = None, visited: list[Any] | None = None,
        label: str | None = None, iteration: int | None = None,
    ) -> None:
        self._snapshot(
            "tree", render_tree(root), 0, label,
            tree_data(root, current, visited), iteration,
        )

    def snapshot_graph(
        self, adjacency: dict[Any, Any], current: Any = None, visited: list[Any] | None = None,
        label: str | None = None, iteration: int | None = None,
    ) -> None:
        self._snapshot(
            "graph", render_graph(adjacency), len(adjacency), label,
            graph_data(adjacency, current, visited), iteration,
        )

    def snapshot_linked_list(
        self, head: Any, current: Any = None,
        label: str | None = None, iteration: int | None = None,
    ) -> None:
        self._snapshot(
            "linked_list", render_linked_list(head), 0, label,
            linked_list_data(head, current), iteration,
        )

    # -- recursion depth tracking -----------------------------------------

    @contextmanager
    def frame(self) -> Iterator[None]:
        """Track recursion depth: ``with trace.frame(): recurse(...)``."""
        self._recursion_depth += 1
        self._note_recursion_depth(self._recursion_depth)
        try:
            yield
        finally:
            self._recursion_depth -= 1

    def _note_recursion_depth(self, depth: int) -> None:
        self._max_recursion_depth = max(self._max_recursion_depth, depth)

    # -- lifecycle ---------------------------------------------------------

    def finish(self, answer: Any = None) -> Summary:
        """Stop the timer, record the answer, and return the final summary."""
        self._end_time = time.perf_counter()
        self._answer = answer
        return self.summary()

    def summary(self) -> Summary:
        end_time = self._end_time if self._end_time is not None else time.perf_counter()
        return compute_summary(
            self.history,
            execution_time=end_time - self._start_time,
            max_recursion_depth=self._max_recursion_depth,
            answer=self._answer,
        )

    # -- read accessors used by formatters ----------------------------------

    @property
    def start_time(self) -> float:
        return self._start_time

    @property
    def steps(self) -> list[StepRecord]:
        return [e.record for e in self.history if isinstance(e.record, StepRecord)]

    @property
    def events(self) -> list[EventRecord]:
        return [e.record for e in self.history if isinstance(e.record, EventRecord)]

    @property
    def decisions(self) -> list[DecisionRecord]:
        return [e.record for e in self.history if isinstance(e.record, DecisionRecord)]

    @property
    def snapshots(self) -> list[SnapshotRecord]:
        return [e.record for e in self.history if isinstance(e.record, SnapshotRecord)]

    # -- rendering / export --------------------------------------------------

    def render_console(self) -> str:
        return render_console(self)

    def render_markdown(self) -> str:
        return render_markdown(self)

    def render_json(self) -> str:
        return render_json(self)

    def render_csv(self, section: Section = "steps") -> str:
        return render_csv(self, section=section)

    def display(self) -> None:
        """Print the trace to the console, using `rich` when available."""
        if self.config.use_rich:
            try:
                from ._rich_display import display_with_rich

                display_with_rich(self)
                return
            except ImportError:
                pass
        print(self.render_console())

    def export_markdown(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.render_markdown())

    def export_json(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.render_json())

    def export_csv(self, path: str, section: Section = "steps") -> None:
        with open(path, "w", newline="") as f:
            f.write(self.render_csv(section=section))

    # -- internals -----------------------------------------------------------

    def _append(self, kind: str, record: Any) -> None:
        self._seq += 1
        self.history.append(HistoryEntry(seq=self._seq, kind=kind, record=record))

    def _snapshot(
        self, kind: str, rendered: str, size: int, label: str | None,
        data: dict[str, Any], iteration: int | None,
    ) -> None:
        if iteration is None:
            iteration = self._current_iteration
        self._append(
            "snapshot",
            SnapshotRecord(kind=kind, rendered=rendered, data=data, label=label, iteration=iteration, size=size),
        )

    # -- context manager -------------------------------------------------------

    def __enter__(self) -> "TraceRecorder":
        return self

    def __exit__(self, *exc_info: object) -> None:
        if self._end_time is None:
            self.finish()


def trace_algorithm(problem: str | None = None) -> Callable:
    """Decorator that instruments a function with a fresh `TraceRecorder`.

    The wrapped function must accept a ``trace`` keyword argument::

        @trace_algorithm("Two Sum")
        def solve(nums, target, trace=None):
            ...

        solve([2, 7, 11, 15], 9)
        solve.last_trace.display()
    """

    def decorator(func: Callable) -> Callable:
        name = problem or func.__name__

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            trace = TraceRecorder(name)
            try:
                result = func(*args, trace=trace, **kwargs)
            finally:
                if trace._end_time is None:
                    trace.finish()
            wrapper.last_trace = trace
            return result

        wrapper.last_trace = None
        return wrapper

    if callable(problem):
        func, problem = problem, None
        return decorator(func)

    return decorator
