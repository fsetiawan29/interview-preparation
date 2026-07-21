"""JSON export formatter — the contract consumed by the React visualizer.

Shape follows docs/trace-schema.md: a `steps[]` array where each step embeds
its own variables/decision/events/snapshot, grouped by the `iteration` value
attached to each record. Records recorded without an explicit `iteration`
(e.g. a stray `trace.event(...)` call that omits it) are not attached to any
step — every `trace.*` call in this codebase's examples passes `iteration=`
explicitly so nothing is silently dropped in practice.
"""

from __future__ import annotations

import json as _json
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from ..utils import stringify

if TYPE_CHECKING:
    from ..models import DecisionRecord, SnapshotRecord, StepRecord
    from ..recorder import TraceRecorder

SCHEMA_VERSION = "1.0.0"


def _safe(value: Any) -> Any:
    try:
        _json.dumps(value)
        return value
    except TypeError:
        return stringify(value)


def _decision_dict(decision: "DecisionRecord | None") -> dict[str, Any] | None:
    if decision is None:
        return None
    return {"condition": decision.condition, "result": decision.result, "action": decision.action}


def _snapshot_dict(snapshot: "SnapshotRecord | None") -> dict[str, Any] | None:
    if snapshot is None or not snapshot.data:
        return None
    return {k: _safe(v) for k, v in snapshot.data.items()}


def _title_for(
    step: "StepRecord", events: list[str], decision: "DecisionRecord | None", snapshot: "SnapshotRecord | None"
) -> str:
    if snapshot is not None and snapshot.label:
        return snapshot.label
    if events:
        return events[0]
    if decision is not None:
        return decision.action
    return f"Iteration {step.iteration}"


def _build_steps(trace: "TraceRecorder") -> list[dict[str, Any]]:
    buckets: dict[int, dict[str, Any]] = {}
    for entry in trace.history:
        iteration = getattr(entry.record, "iteration", None)
        if iteration is None:
            continue
        bucket = buckets.setdefault(iteration, {"events": [], "decision": None, "snapshot": None})
        if entry.kind == "event":
            bucket["events"].append(entry.record.message)
        elif entry.kind == "decision":
            bucket["decision"] = entry.record
        elif entry.kind == "snapshot":
            bucket["snapshot"] = entry.record

    steps: list[dict[str, Any]] = []
    for i, step in enumerate(trace.steps, start=1):
        bucket = buckets.get(step.iteration, {"events": [], "decision": None, "snapshot": None})
        events: list[str] = bucket["events"]
        decision: "DecisionRecord | None" = bucket["decision"]
        snapshot: "SnapshotRecord | None" = bucket["snapshot"]

        steps.append(
            {
                "id": i,
                "title": _title_for(step, events, decision, snapshot),
                "timestamp": step.timestamp - trace.start_time,
                "variables": {k: _safe(v) for k, v in step.variables.items()},
                "decision": _decision_dict(decision),
                "events": events,
                "snapshot": _snapshot_dict(snapshot),
                "statistics": {"iterations_so_far": i},
            }
        )
    return steps


def to_dict(trace: "TraceRecorder") -> dict[str, Any]:
    summary = trace.summary()
    return {
        "schema_version": SCHEMA_VERSION,
        "problem": trace.problem,
        "metadata": {
            "problem": trace.problem,
            "difficulty": trace.difficulty,
            "language": trace.language,
            "algorithm": trace.algorithm,
            "time_complexity": trace.time_complexity,
            "space_complexity": trace.space_complexity,
        },
        "input": _safe(trace.input_data),
        "steps": _build_steps(trace),
        "summary": asdict(summary) | {"answer": _safe(summary.answer)},
    }


def render_json(trace: "TraceRecorder", *, indent: int = 2) -> str:
    return _json.dumps(to_dict(trace), indent=indent)
