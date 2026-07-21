"""Optional `rich`-powered console rendering. Only imported when rich is installed."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .timeline import render_timeline
from .utils import step_variable_keys, stringify

if TYPE_CHECKING:
    from .recorder import TraceRecorder


def display_with_rich(trace: "TraceRecorder") -> None:
    console = Console()
    console.rule(f"[bold]{trace.problem}[/bold]")

    if trace.input_data is not None:
        console.print(f"[bold]Input:[/bold] {stringify(trace.input_data)}")

    steps = trace.steps
    if steps:
        var_keys = step_variable_keys(steps)
        table = Table(title="Variable Trace")
        table.add_column("Iter")
        for key in var_keys:
            table.add_column(key)
        for s in steps:
            table.add_row(
                str(s.iteration),
                *(stringify(s.variables[k]) if k in s.variables else "-" for k in var_keys),
            )
        console.print(table)

    for d in trace.decisions:
        console.print(
            Panel(
                f"Condition: {d.condition}\nResult: {'TRUE' if d.result else 'FALSE'}\nAction: {d.action}",
                title=f"Decision (iter {d.iteration})" if d.iteration is not None else "Decision",
            )
        )

    if trace.events:
        console.print(Panel(render_timeline(trace.history), title="Timeline"))

    for snap in trace.snapshots:
        console.print(Panel(snap.rendered, title=snap.label or snap.kind.title()))

    summary = trace.summary()
    summary_table = Table(title="Summary")
    summary_table.add_column("Metric")
    summary_table.add_column("Value")
    summary_table.add_row("Iterations", str(summary.iterations))
    summary_table.add_row("Skipped iterations", str(summary.skipped_iterations))
    summary_table.add_row("While loops", str(summary.while_loops))
    summary_table.add_row("Maximum recursion depth", str(summary.max_recursion_depth))
    summary_table.add_row("Maximum stack size", str(summary.max_stack_size))
    summary_table.add_row("Maximum queue size", str(summary.max_queue_size))
    summary_table.add_row("Maximum heap size", str(summary.max_heap_size))
    summary_table.add_row("Execution time", f"{summary.execution_time:.6f} seconds")
    summary_table.add_row("Answer", stringify(summary.answer))
    console.print(summary_table)
