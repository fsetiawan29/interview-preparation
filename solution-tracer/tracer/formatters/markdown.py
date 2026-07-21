"""Markdown report formatter (see REQUIREMENTS.MD section 20)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..timeline import render_timeline
from ..utils import render_table, step_variable_keys, stringify

if TYPE_CHECKING:
    from ..recorder import TraceRecorder


def render_markdown(trace: "TraceRecorder") -> str:
    lines: list[str] = [f"# {trace.problem}", ""]

    if trace.input_data is not None:
        lines += ["## Input", "", f"```\n{stringify(trace.input_data)}\n```", ""]

    steps = trace.steps
    if steps:
        var_keys = step_variable_keys(steps)
        headers = ["Iter", *var_keys]
        rows = [
            [str(s.iteration), *(stringify(s.variables[k]) if k in s.variables else "-" for k in var_keys)]
            for s in steps
        ]
        lines += [
            "## Variable Trace",
            "",
            render_table(headers, rows, markdown=True),
            "",
        ]

    decisions = trace.decisions
    if decisions:
        lines += ["## Decision Log", ""]
        for i, d in enumerate(decisions, start=1):
            iteration = d.iteration if d.iteration is not None else i
            lines += [
                f"**Iteration {iteration}**",
                "",
                f"- Condition: `{d.condition}`",
                f"- Result: {'TRUE' if d.result else 'FALSE'}",
                f"- Action: {d.action}",
                "",
            ]

    if trace.events:
        lines += ["## Timeline", "", "```", render_timeline(trace.history), "```", ""]

    snapshots = trace.snapshots
    if snapshots:
        lines += ["## Snapshots", ""]
        for snap in snapshots:
            title = snap.label or snap.kind.title()
            lines += [f"### {title}", "", "```", snap.rendered, "```", ""]

    summary = trace.summary()
    lines += [
        "## Summary",
        "",
        render_table(
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
            markdown=True,
        ),
        "",
    ]

    return "\n".join(lines)
