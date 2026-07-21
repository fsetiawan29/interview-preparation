"""CLI: autotrace an unmodified LeetCode solution file directly.

Usage::

    python -m tracer.checker <path/to/solution.py> <method> [args...]
    python -m tracer.checker <path/to/solution.py> <method> --case N
    python -m tracer.checker <path/to/solution.py> <method> --list

No changes to the solution file are required. The class defaults to
`Solution` (every file in this repo uses that name) — pass `--cls Other`
if a file's class is named differently.

Two ways to supply input:

1. Explicit args after `method`, parsed with `ast.literal_eval` — lists,
   dicts, ints, strings all work as plain shell arguments::

       python -m tracer.checker two-sum.py twoSum '[2, 7, 11, 15]' 9

2. No args: the file's own `run_test("Example 1", ..., expected)` calls
   (under `if __name__ == "__main__":`) are discovered automatically and
   listed/run, so you don't need to retype example inputs. Use `--case N`
   (1-indexed) to pick which discovered example to trace, or `--list` to
   just see what was found.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from ._cli_utils import load_module as _load_module, parse_arg as _parse_arg
from .autotrace import autotrace
from .discovery import DiscoveredCase, discover_test_cases


def _describe(case: DiscoveredCase) -> str:
    args_str = ", ".join(repr(a) for a in case.args)
    expected_str = repr(case.expected) + (" (partial)" if case.expected_is_partial else "")
    return f"{case.label}: args=({args_str})  expected={expected_str}"


def _run_case(
    method: Any, cls_name: str, method_name: str, case: DiscoveredCase, *, export: bool, solution_path: Path, index: int
) -> None:
    result, trace = autotrace(method, *case.args, problem=f"{cls_name}.{method_name} — {case.label}")

    print("Result:", result)
    print()
    trace.display()

    if not case.expected_is_partial:
        status = "PASS" if result == case.expected else "FAIL"
        print(f"\n[{status}] expected {case.expected!r}, got {result!r}")

    if export:
        output_path = solution_path.parent / f"{solution_path.stem}_case{index}_trace.md"
        trace.export_markdown(str(output_path))
        print(f"\nMarkdown report written to {output_path}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", type=Path, help="Path to the solution .py file")
    parser.add_argument("method", help="Method name to call, e.g. twoSum")
    parser.add_argument("args", nargs="*", help="Positional arguments, as Python literals")
    parser.add_argument("--cls", default="Solution", help="Class name inside the file (default: Solution)")
    parser.add_argument("--case", type=int, default=None, help="Run only discovered example N (1-indexed)")
    parser.add_argument("--list", action="store_true", help="List discovered examples and exit, without running")
    parser.add_argument("--harness", default="run_test", help="Name of the test-runner function to read examples from")
    parser.add_argument("--no-export", action="store_true", help="Skip writing a markdown report")
    parsed = parser.parse_args(argv)

    solution_path = parsed.path.resolve()
    module = _load_module(solution_path)
    try:
        cls = getattr(module, parsed.cls)
    except AttributeError:
        parser.error(f"No class `{parsed.cls}` found in {solution_path.name} (pass --cls to override)")
    method = getattr(cls(), parsed.method)

    if parsed.args:
        if parsed.case is not None or parsed.list:
            parser.error("--case/--list select among discovered examples; don't combine with explicit args")
        call_args = [_parse_arg(a) for a in parsed.args]
        result, trace = autotrace(method, *call_args, problem=f"{parsed.cls}.{parsed.method}")
        print("Result:", result)
        print()
        trace.display()
        if not parsed.no_export:
            output_path = solution_path.parent / f"{solution_path.stem}_trace.md"
            trace.export_markdown(str(output_path))
            print(f"\nMarkdown report written to {output_path}")
        return

    cases = discover_test_cases(solution_path.read_text(), parsed.method, harness_name=parsed.harness)
    if not cases:
        parser.error(
            f"Couldn't auto-discover examples from `{parsed.harness}(...)` calls for `{parsed.method}`. "
            f"Pass arguments explicitly instead, e.g.:\n"
            f"  python -m tracer.checker {parsed.path} {parsed.method} <arg1> <arg2> ..."
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
        _run_case(
            method, parsed.cls, parsed.method, chosen,
            export=not parsed.no_export, solution_path=solution_path, index=parsed.case,
        )
        return

    # No explicit case: quick PASS/FAIL over every discovered example, then a
    # full trace for the first failure (or example 1 if everything passes).
    print(f"Discovered {len(cases)} example(s) from `{parsed.harness}(...)`:\n")
    first_failure: int | None = None
    for i, case in enumerate(cases, start=1):
        result = method(*case.args)
        if case.expected_is_partial:
            status = "?"
        else:
            status = "PASS" if result == case.expected else "FAIL"
            if status == "FAIL" and first_failure is None:
                first_failure = i
        print(f"  [{status}] {i}. {_describe(case)}  got={result!r}")

    primary = first_failure if first_failure is not None else 1
    reason = "first failure" if first_failure is not None else "example 1"
    print(f"\nFull trace for {reason} (pass --case N to pick another, --list to see all):\n")

    method = getattr(cls(), parsed.method)  # fresh instance, in case the solution keeps state
    _run_case(
        method, parsed.cls, parsed.method, cases[primary - 1],
        export=not parsed.no_export, solution_path=solution_path, index=primary,
    )


if __name__ == "__main__":
    main()
