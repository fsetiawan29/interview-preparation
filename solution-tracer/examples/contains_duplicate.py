"""Contains Duplicate, instrumented with the solution-tracer framework.

Mirrors the solution in
arrays-hashing/easy/contains-duplicate/contains-duplicate.py — the
algorithm logic is untouched, only a handful of `trace.*` calls were added.
"""

from __future__ import annotations

from typing import List

from tracer import TraceRecorder
from tracer.cli import main


class Solution:
    def containsDuplicate(self, nums: List[int], trace: TraceRecorder | None = None) -> bool:
        seen: set[int] = set()

        for i, n in enumerate(nums):
            found = n in seen

            if trace:
                trace.decision(
                    condition=f"{n} in seen",
                    result=found,
                    action="Return True" if found else "Add to seen",
                    iteration=i,
                )

            if found:
                if trace:
                    trace.event(f"Duplicate found: {n} (index {i})", iteration=i)
                    trace.step(iteration=i, variables={"n": n, "seen": set(seen)})
                    trace.snapshot_array(nums, pointers={"i": i}, iteration=i)
                return True

            seen.add(n)
            if trace:
                trace.event(f"Add nums[{i}]={n} to seen", iteration=i)
                trace.step(iteration=i, variables={"n": n, "seen": set(seen)})
                trace.snapshot_array(nums, pointers={"i": i}, iteration=i)

        if trace:
            trace.event("No duplicates found")
        return False


def run(nums: List[int]) -> tuple[bool, TraceRecorder]:
    trace = TraceRecorder(
        "Contains Duplicate",
        input_data={"nums": nums},
        difficulty="Easy",
        algorithm="Hash Set",
        time_complexity="O(n)",
        space_complexity="O(n)",
    )
    result = Solution().containsDuplicate(nums, trace=trace)
    trace.finish(answer=result)
    return result, trace


if __name__ == "__main__":
    main(run, [1, 1, 1, 3, 3, 4, 3, 2, 4, 2])
