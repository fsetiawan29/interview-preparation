"""CLI: generate a visualizer-ready JSON trace from a plain solution file.

Unlike `tracer.checker`, this targets *unmodified* LeetCode-style solutions
(no `trace.*` calls needed) — it runs the chosen method under `autotrace`
(see `tracer/autotrace.py`) and writes the resulting trace as JSON.

Two ways to supply input, same convention as `tracer.checker`:

1. Explicit args after `method`, parsed with `ast.literal_eval`::

       python -m tracer.generate two-sum.py twoSum '[2, 7, 11, 15]' 9

2. No args: the file's own `run_test("Example 1", ..., expected)` calls
   are discovered automatically. Use `--case N` (1-indexed) to pick one,
   `--list` to see what was found, or omit both to use the first example.

Because `autotrace` only observes local variables line-by-line, the
resulting trace has no `decision`/`events`/structured `snapshot` data (those
require explicit `trace.decision()` / `trace.event()` / `trace.snapshot_*()`
calls) — the visualizer will show the Variables panel stepping through the
run, but the Visualization panel stays empty. For a fully-instrumented trace
with array/stack/tree/graph snapshots, write a small script like the ones in
`examples/` instead.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ._cli_utils import load_module, parse_arg
from .autotrace import autotrace
from .discovery import DiscoveredCase, discover_test_cases


def _describe(case: DiscoveredCase) -> str:
    args_str = ", ".join(repr(a) for a in case.args)
    return f"{case.label}: args=({args_str})"


def _problem_name(solution_path: Path) -> str:
    return solution_path.stem.replace("-", " ").replace("_", " ").title()


def _generate(
    method,
    args: list,
    *,
    problem: str,
    out_path: Path,
) -> None:
    result, trace = autotrace(method, *args, problem=problem)
    print("Result:", result)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    trace.export_json(str(out_path))
    print(f"Wrote {out_path}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", type=Path, help="Path to the solution .py file")
    parser.add_argument("method", help="Method name to call, e.g. twoSum")
    parser.add_argument("args", nargs="*", help="Positional arguments, as Python literals")
    parser.add_argument("--cls", default="Solution", help="Class name inside the file (default: Solution)")
    parser.add_argument("--case", type=int, default=None, help="Use discovered example N (1-indexed)")
    parser.add_argument("--list", action="store_true", help="List discovered examples and exit, without running")
    parser.add_argument("--harness", default="run_test", help="Name of the test-runner function to read examples from")
    parser.add_argument(
        "-o", "--out", type=Path, default=None,
        help="Output JSON path (default: leetcode-tracer/generated_traces/<slug>_trace.json)",
    )
    parsed = parser.parse_args(argv)

    solution_path = parsed.path.resolve()
    module = load_module(solution_path)
    try:
        cls = getattr(module, parsed.cls)
    except AttributeError:
        parser.error(f"No class `{parsed.cls}` found in {solution_path.name} (pass --cls to override)")
    method = getattr(cls(), parsed.method)
    problem = _problem_name(solution_path)
    default_out = Path(__file__).resolve().parent.parent / "generated_traces" / f"{solution_path.stem.replace('-', '_')}_trace.json"

    if parsed.args:
        if parsed.case is not None or parsed.list:
            parser.error("--case/--list select among discovered examples; don't combine with explicit args")
        call_args = [parse_arg(a) for a in parsed.args]
        _generate(method, call_args, problem=problem, out_path=parsed.out or default_out)
        return

    cases = discover_test_cases(solution_path.read_text(), parsed.method, harness_name=parsed.harness)
    if not cases:
        parser.error(
            f"Couldn't auto-discover examples from `{parsed.harness}(...)` calls for `{parsed.method}`. "
            f"Pass arguments explicitly instead, e.g.:\n"
            f"  python -m tracer.generate {parsed.path} {parsed.method} <arg1> <arg2> ..."
        )

    if parsed.list:
        print(f"Discovered {len(cases)} example(s) from `{parsed.harness}(...)` in {solution_path.name}:\n")
        for i, case in enumerate(cases, start=1):
            print(f"  {i}. {_describe(case)}")
        return

    if parsed.case is not None:
        if not (1 <= parsed.case <= len(cases)):
            parser.error(f"--case must be between 1 and {len(cases)} (found {len(cases)} examples)")
        chosen = cases[parsed.case - 1]
    else:
        chosen = cases[0]

    _generate(method, chosen.args, problem=problem, out_path=parsed.out or default_out)


if __name__ == "__main__":
    main()
