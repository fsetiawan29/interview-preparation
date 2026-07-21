"""Plain-text console formatter. Works with or without `rich` installed."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import DecisionRecord
from ..timeline import render_timeline
from ..utils import render_table, step_variable_keys, stringify

if TYPE_CHECKING:
    from ..recorder import TraceRecorder


def render_console(trace: "TraceRecorder") -> str:
    sections: list[str] = []

    sections.append(f"# {trace.problem}")
    if trace.input_data is not None:
        sections.append(f"\nInput: {stringify(trace.input_data)}")

    steps = trace.steps
    if steps:
        var_keys = step_variable_keys(steps)
        headers = ["Iter", *var_keys]
        rows = [
            [str(s.iteration), *(stringify(s.variables[k]) if k in s.variables else "-" for k in var_keys)]
            for s in steps
        ]
        sections.append("\n## Variable Trace\n\n" + render_table(headers, rows))

    decisions = trace.decisions
    if decisions:
        sections.append("\n## Decision Log\n\n" + _render_decisions(decisions))

    events = trace.events
    if events:
        sections.append("\n## Timeline\n\n" + render_timeline(trace.history))

    snapshots = trace.snapshots
    if snapshots:
        blocks = []
        for snap in snapshots:
            title = snap.label or snap.kind.title()
            blocks.append(f"[{title}]\n{snap.rendered}")
        sections.append("\n## Snapshots\n\n" + "\n\n".join(blocks))

    summary = trace.summary()
    sections.append(
        "\n## Summary\n\n"
        + render_table(
            ["Metric", "Value"],
            [
                ["Iterations", str(summary.iterations)],
                ["Skipped iterations", str(summary.skipped_iterations)],
                ["While loops", str(summary.while_loops)],
                ["Maximum recursion depth", str(summary.max_recursion_depth)],
                ["Maximum stack size", str(summary.max_stack_size)],
                ["Maximum queue size", str(summary.max_queue_size)],
                ["Maximum heap size", str(summary.max_heap_size)],
                ["Execution time", f"{summary.execution_time:.6f} seconds"],
                ["Answer", stringify(summary.answer)],
            ],
        )
    )

    return "\n".join(sections)


def _render_decisions(decisions: list[DecisionRecord]) -> str:
    blocks = []
    for i, d in enumerate(decisions, start=1):
        blocks.append(
            f"Iteration {d.iteration if d.iteration is not None else i}\n\n"
            f"Condition\n\n{d.condition}\n\n"
            f"Result\n\n{'TRUE' if d.result else 'FALSE'}\n\n"
            f"Action\n\n{d.action}"
        )
    return "\n\n---\n\n".join(blocks)
