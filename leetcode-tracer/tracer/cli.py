"""Shared runner for example scripts, so each one only needs a `run()`.

Usage in an example file::

    if __name__ == "__main__":
        main(run, [2, 7, 11, 15], 9)
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable

from .recorder import TraceRecorder


def main(
    run_fn: Callable[..., tuple[Any, "TraceRecorder"]],
    *args: Any,
    export: bool = True,
    **kwargs: Any,
) -> tuple[Any, "TraceRecorder"]:
    """Call `run_fn(*args, **kwargs)`, print the result, and display the trace.

    `run_fn` must return `(result, trace)`. By default also writes a
    `<problem>_trace.md` report next to the calling script.
    """
    result, trace = run_fn(*args, **kwargs)

    print("Result:", result)
    print()
    trace.display()

    if export:
        caller_dir = Path(sys.argv[0]).resolve().parent
        slug = trace.problem.lower().replace(" ", "_")
        output_path = caller_dir / f"{slug}_trace.md"
        trace.export_markdown(str(output_path))
        print(f"\nMarkdown report written to {output_path}")

    return result, trace
