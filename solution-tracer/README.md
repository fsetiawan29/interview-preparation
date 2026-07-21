# solution-tracer

A reusable Python library that instruments coding solutions and generates
educational execution traces — variable tables, decision logs, timelines,
data-structure snapshots, and a final summary — without changing the
algorithm's logic.

## Install

Homebrew/system Python refuses plain `pip install` (PEP 668), so use a
project-local virtualenv:

```bash
cd solution-tracer
python3 -m venv .venv
.venv/bin/pip install -e .                  # editable install of the tracer package
.venv/bin/pip install -r requirements.txt   # optional: only needed for colored `rich` output
```

The core library has **zero required dependencies**. `rich` is optional and
only used by `trace.display()` if it's installed. The editable install is
what lets example scripts do `from tracer import TraceRecorder` without any
`sys.path` hacking — run them with `.venv/bin/python examples/<file>.py`.

## Checking a solution's logic (zero instrumentation)

To sanity-check any plain, unmodified solution file — no
`trace.*` calls, no copying — use the `checker` CLI. It imports the file,
runs the given method under a line tracer, and prints/exports the same
report:

```bash
.venv/bin/python -m tracer.checker \
    ../arrays-hashing/easy/two-sum/two-sum.py twoSum \
    '[2, 7, 11, 15]' 9
```

The class defaults to `Solution` (every file in this repo uses that name —
pass `--cls Other` if not). Arguments after the method name are parsed as
Python literals (lists, dicts, ints, strings all work directly). This is
the fastest way to check a solution you just wrote — point it at the file
and go. It writes `<solution>_trace.md` next to the file (`--no-export` to
skip that).

**Or skip typing arguments entirely.** Every solution in this repo already
has its own examples baked in as `run_test("Example 1", ..., expected)`
calls under `if __name__ == "__main__":`. Drop the trailing args and the
checker reads those directly:

```bash
# list what it found, without running anything
.venv/bin/python -m tracer.checker ../arrays-hashing/easy/two-sum/two-sum.py twoSum --list
#   1. Example 1: args=([2, 7, 11, 15], 9)  expected=[0, 1]
#   2. Example 2: args=([3, 2, 4], 6)  expected=[1, 2]
#   3. Example 3: args=([3, 3], 6)  expected=[0, 1]

# no --case: PASS/FAIL for every example, then a full trace for the first
# failure (or example 1, if everything passes)
.venv/bin/python -m tracer.checker ../arrays-hashing/easy/two-sum/two-sum.py twoSum

# trace one specific example (1-indexed)
.venv/bin/python -m tracer.checker ../arrays-hashing/easy/two-sum/two-sum.py twoSum --case 2
```

Discovery is static (via `ast`, no code execution) and conservative: it
only auto-runs when it can unambiguously match `run_test`'s parameters to
a single `<obj>.<method>(...)` call using literal arguments. Files that
dispatch dynamically (e.g. looping over method *names*) or pass non-literal
args (e.g. a function reference) won't match — the checker tells you so
and asks for explicit arguments instead of guessing.

Limitations: it captures locals from the target method *and* any nested
helper function defined in the same file (so recursive `dfs`/backtracking
closures are traced too), but rows show whatever variables happen to be
primitives/lists/dicts/sets/tuples at that point — not a curated
decision/event narrative. It also can't build rich objects like
`TreeNode`/`ListNode` from CLI args, so problems whose signature takes a
tree or linked list need the manual approach below instead.

## Generating a JSON trace for the visualizer

`tracer.generate` is `checker`'s sibling: same file-path/method/`--case`/
`--list` interface and the same `run_test`-discovery, but instead of
printing a report it writes a `frontend/`-ready JSON trace (see
`docs/trace-schema.md`) built from `autotrace` — so **any unmodified
solution in this repo works, zero instrumentation required**:

```bash
# list discovered examples, same as checker
.venv/bin/python -m tracer.generate ../arrays-hashing/easy/contains-duplicate/contains-duplicate.py containsDuplicate --list

# generate from a specific example
.venv/bin/python -m tracer.generate ../arrays-hashing/easy/contains-duplicate/contains-duplicate.py containsDuplicate --case 1
#   Wrote generated_traces/contains_duplicate_trace.json

# or from explicit arguments
.venv/bin/python -m tracer.generate ../arrays-hashing/easy/two-sum/two-sum.py twoSum '[3, 2, 4]' 6 -o my_trace.json
```

Drop the resulting file onto the visualizer (`frontend/`) via drag-and-drop
or the file picker. `generated_traces/` is gitignored, so ad-hoc traces
don't pollute the repo.

**The catch:** `autotrace` only observes local variables line-by-line, so a
generated trace has `decision: null`, `events: []`, and `snapshot: null` on
every step — the Variables panel steps through the run, but the
Visualization panel stays empty (no array/stack/tree/graph rendering). For
that, the solution needs real `trace.decision()` / `trace.event()` /
`trace.snapshot_*()` calls — see the curated examples in `examples/`, which
mirror plain solutions from this repo with exactly those calls added.

## Quick start (manual instrumentation)

For a curated trace — meaningful decision points, named events, data
structure snapshots — add a few `trace.*` calls by hand:

```python
from tracer import TraceRecorder

trace = TraceRecorder("Two Sum", input_data={"nums": [2, 7, 11, 15], "target": 9})

for i, num in enumerate(nums):
    complement = target - num
    found = complement in seen

    trace.decision(condition=f"{complement} in seen", result=found, action="Return pair")
    trace.step(iteration=i, variables={"num": num, "complement": complement, "seen": dict(seen)})

    if found:
        trace.event(f"Found pair ({seen[complement]}, {i})")
        trace.snapshot_array(nums, pointers={"j": seen[complement], "i": i})
        break

    seen[num] = i

trace.finish(answer=result)
trace.display()                       # pretty console output
trace.export_markdown("trace.md")     # full report
trace.export_json("trace.json")
trace.export_csv("trace.csv")
```

See [examples/two_sum.py](examples/two_sum.py) for a complete, runnable
example mirroring
[arrays-hashing/easy/two-sum](../arrays-hashing/easy/two-sum/two-sum.py):

```bash
.venv/bin/python examples/two_sum.py
```

## Adding a new curated example

Every example follows the same three-part shape. Copy `two_sum.py` and edit:

```python
from tracer import TraceRecorder
from tracer.cli import main


class Solution:
    def solve(self, ..., trace: TraceRecorder | None = None):
        ...                      # algorithm logic, unchanged
        if trace:
            trace.step(...)      # sprinkle trace.* calls where useful
            trace.event(...)
            trace.decision(...)
        return answer


def run(...) -> tuple[Any, TraceRecorder]:
    trace = TraceRecorder("Problem Name", input_data={...})
    result = Solution().solve(..., trace=trace)
    trace.finish(answer=result)
    return result, trace


if __name__ == "__main__":
    main(run, ...)   # pass whatever args your run() takes
```

`tracer.cli.main` handles printing the result, calling `trace.display()`,
and exporting `<problem>_trace.md` next to the script — so each new problem
file only needs the algorithm and the `run()`/`main()` wiring above.

## API surface

| Method | Purpose |
|---|---|
| `trace.step(iteration, variables)` | Add a row to the variable trace table |
| `trace.iteration(values)` | Same, but auto-numbered |
| `trace.event(message)` | Log a generic event (feeds the timeline) |
| `trace.decision(condition, result, action)` | Log a branch taken by the algorithm |
| `trace.auto(locals())` | Auto-capture primitive locals |
| `trace.snapshot_array/stack/queue/heap/tree/graph/linked_list(...)` | Render a data structure snapshot |
| `trace.frame()` | Context manager that tracks recursion depth |
| `trace.finish(answer=...)` | Stop the timer and compute the summary |
| `trace.display()` | Pretty console output (rich if available, plain text otherwise) |
| `trace.export_markdown/json/csv(path)` | Write a report to disk |

`TraceRecorder` also works as a context manager and via the `@trace_algorithm`
decorator (see `tracer/recorder.py`). `autotrace(func, *args, **kwargs)`
(`tracer/autotrace.py`) builds a trace automatically without any `trace.*`
calls — it's what `python -m tracer.checker` uses under the hood.

## Project layout

```
tracer/
├── recorder.py     # TraceRecorder — the central API
├── autotrace.py    # zero-instrumentation tracing via sys.settrace
├── checker.py      # CLI: autotrace an unmodified solution file, print/export a report
├── generate.py     # CLI: autotrace an unmodified solution file, export JSON for frontend/
├── discovery.py    # static ast parsing of a file's own run_test(...) examples
├── _cli_utils.py   # shared module-loading/arg-parsing helpers for checker.py/generate.py
├── cli.py          # shared example runner (used by examples/*.py)
├── models.py       # dataclasses for steps/events/decisions/snapshots
├── config.py       # TracerConfig
├── timeline.py     # chronological event-flow rendering
├── statistics.py   # automatic summary computation
├── utils.py        # table rendering, stringification helpers
├── formatters/     # stdout, markdown, json, csv
└── snapshots/      # array, stack, queue, heap, tree, graph, linked_list — ASCII + structured (JSON) payloads
```

No algorithm-specific logic lives in the framework — every snapshot/format
module is generic over the data structure it renders, per the design goals
in [REQUIREMENTS.MD](../REQUIREMENTS.MD).

## Notes on fidelity

- `while_loops` and `skipped_iterations` in the summary are derived
  heuristically from event/decision text (`event("Skip ...")`,
  `decision(..., action="... while loop")`) since the spec doesn't define a
  dedicated API for them — call `trace.event`/`trace.decision` with those
  words in the message to have them counted.
- Tree/heap rendering uses a centered level-order layout without slash
  connector lines, to keep the renderer generic over arbitrary trees.
- Graph rendering prints a deduplicated edge list rather than a 2D layout,
  since arbitrary graphs have no canonical ASCII grid representation.
