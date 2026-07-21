"""Valid Parentheses, instrumented with the solution-tracer framework.

A classic stack problem — gives the visualizer real `stack` snapshots.
"""

from __future__ import annotations

from typing import List

from tracer import TraceRecorder
from tracer.cli import main

PAIRS = {")": "(", "]": "[", "}": "{"}


class Solution:
    def isValid(self, s: str, trace: TraceRecorder | None = None) -> bool:
        stack: List[str] = []

        for i, ch in enumerate(s):
            if ch in PAIRS:
                top = stack[-1] if stack else None
                matched = top == PAIRS[ch]

                if trace:
                    trace.decision(
                        condition=f"top of stack == match for '{ch}'",
                        result=matched,
                        action="Pop matching bracket" if matched else "Return False",
                        iteration=i,
                    )

                if not matched:
                    if trace:
                        trace.event(f"Mismatch at '{ch}' (index {i})", iteration=i)
                        trace.step(iteration=i, variables={"char": ch, "stack": list(stack)})
                        trace.snapshot_stack(stack, iteration=i)
                    return False

                stack.pop()
                if trace:
                    trace.event(f"Popped '{top}' for '{ch}'", iteration=i)
                    trace.step(iteration=i, variables={"char": ch, "stack": list(stack)})
                    trace.snapshot_stack(stack, iteration=i)
            else:
                stack.append(ch)
                if trace:
                    trace.event(f"Pushed '{ch}'", iteration=i)
                    trace.step(iteration=i, variables={"char": ch, "stack": list(stack)})
                    trace.snapshot_stack(stack, highlights=[len(stack) - 1], iteration=i)

        result = not stack
        if trace:
            trace.event("Stack empty" if result else "Unmatched brackets remain")
        return result


def run(s: str) -> tuple[bool, TraceRecorder]:
    trace = TraceRecorder(
        "Valid Parentheses",
        input_data={"s": s},
        difficulty="Easy",
        algorithm="Stack",
        time_complexity="O(n)",
        space_complexity="O(n)",
    )
    result = Solution().isValid(s, trace=trace)
    trace.finish(answer=result)
    return result, trace


if __name__ == "__main__":
    main(run, "{[()]}")
