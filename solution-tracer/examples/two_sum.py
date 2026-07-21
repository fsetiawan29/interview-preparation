"""Two Sum, instrumented with the solution-tracer framework.

Mirrors the solution in arrays-hashing/easy/two-sum/two-sum.py — the
algorithm logic is untouched, only a handful of `trace.*` calls were added.
"""

from __future__ import annotations

from typing import List

from tracer import TraceRecorder
from tracer.cli import main


class Solution:
    def twoSum(self, nums: List[int], target: int, trace: TraceRecorder | None = None) -> List[int]:
        seen: dict[int, int] = {}

        for i, num in enumerate(nums):
            complement = target - num
            found = complement in seen

            if trace:
                trace.decision(
                    condition=f"{complement} in seen",
                    result=found,
                    action="Return pair" if found else "Store num",
                    iteration=i,
                )

            if found:
                if trace:
                    trace.event(f"Found pair (seen[{complement}]={seen[complement]}, i={i})", iteration=i)
                    trace.step(
                        iteration=i,
                        variables={"num": num, "complement": complement, "seen": dict(seen)},
                    )
                    trace.snapshot_array(nums, pointers={"j": seen[complement], "i": i}, iteration=i)
                return [seen[complement], i]

            seen[num] = i
            if trace:
                trace.event(f"Store nums[{i}]={num}", iteration=i)
                trace.step(
                    iteration=i,
                    variables={"num": num, "complement": complement, "seen": dict(seen)},
                )
                trace.snapshot_array(nums, pointers={"i": i}, iteration=i)

        if trace:
            trace.event("No pair found")
        return []


def run(nums: List[int], target: int) -> tuple[List[int], TraceRecorder]:
    trace = TraceRecorder(
        "Two Sum",
        input_data={"nums": nums, "target": target},
        difficulty="Easy",
        algorithm="Hash Map",
        time_complexity="O(n)",
        space_complexity="O(n)",
    )
    result = Solution().twoSum(nums, target, trace=trace)
    trace.finish(answer=result)
    return result, trace


if __name__ == "__main__":
    main(run, [2, 7, 11, 15], 9)
