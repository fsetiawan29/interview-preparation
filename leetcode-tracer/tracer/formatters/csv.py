"""CSV export formatter — useful for spreadsheets."""

from __future__ import annotations

import csv
import io
from typing import TYPE_CHECKING, Literal

from ..utils import step_variable_keys, stringify

if TYPE_CHECKING:
    from ..recorder import TraceRecorder

Section = Literal["steps", "events", "decisions"]


def render_csv(trace: "TraceRecorder", *, section: Section = "steps") -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    if section == "steps":
        steps = trace.steps
        var_keys = step_variable_keys(steps)
        writer.writerow(["iteration", *var_keys])
        for s in steps:
            writer.writerow(
                [s.iteration, *(stringify(s.variables[k]) if k in s.variables else "" for k in var_keys)]
            )
    elif section == "events":
        writer.writerow(["iteration", "message"])
        for e in trace.events:
            writer.writerow([e.iteration, e.message])
    elif section == "decisions":
        writer.writerow(["iteration", "condition", "result", "action"])
        for d in trace.decisions:
            writer.writerow([d.iteration, d.condition, d.result, d.action])
    else:
        raise ValueError(f"Unknown CSV section: {section!r}")

    return buffer.getvalue()
