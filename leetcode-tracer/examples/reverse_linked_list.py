"""Reverse Linked List, instrumented with leetcode-tracer.

Iterative pointer-reversal — gives the visualizer real `linked-list`
snapshots with a highlighted current node as the list is rebuilt.
"""

from __future__ import annotations

from typing import List, Optional

from tracer import TraceRecorder
from tracer.cli import main


class ListNode:
    def __init__(self, val: int, next: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next


def build_list(values: List[int]) -> ListNode | None:
    head: ListNode | None = None
    tail: ListNode | None = None
    for v in values:
        node = ListNode(v)
        if head is None:
            head = tail = node
        else:
            assert tail is not None
            tail.next = node
            tail = node
    return head


def to_list(head: ListNode | None) -> List[int]:
    values = []
    node = head
    while node is not None:
        values.append(node.val)
        node = node.next
    return values


class Solution:
    def reverseList(self, head: ListNode | None, trace: TraceRecorder | None = None) -> ListNode | None:
        prev: ListNode | None = None
        curr = head
        i = 0

        while curr is not None:
            nxt = curr.next
            curr.next = prev

            if trace:
                trace.event(f"Reverse pointer at node {curr.val}", iteration=i)
                trace.step(iteration=i, variables={"current": curr.val, "prev": prev.val if prev else None})
                # `curr` is now the head of the (partially) reversed list so far,
                # since `curr.next` was just repointed to the old `prev`.
                trace.snapshot_linked_list(curr, current=curr, iteration=i)
                trace.decision(
                    condition="next node is None",
                    result=nxt is None,
                    action="Finish reversal" if nxt is None else "Advance to next node",
                    iteration=i,
                )

            prev = curr
            curr = nxt
            i += 1

        if trace:
            trace.event("List fully reversed")
        return prev


def run(values: List[int]) -> tuple[List[int], TraceRecorder]:
    trace = TraceRecorder(
        "Reverse Linked List",
        input_data={"head": values},
        difficulty="Easy",
        algorithm="Iterative Pointer Reversal",
        time_complexity="O(n)",
        space_complexity="O(1)",
    )
    head = build_list(values)
    reversed_head = Solution().reverseList(head, trace=trace)
    result = to_list(reversed_head)
    trace.finish(answer=result)
    return result, trace


if __name__ == "__main__":
    main(run, [1, 2, 3, 4, 5])
