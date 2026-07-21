"""Course Schedule, instrumented with solution-tracer.

Kahn's algorithm (BFS topological sort) over a prerequisite graph — gives
the visualizer real `graph` snapshots with a highlighted current node and
a growing visited set.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Tuple

from tracer import TraceRecorder
from tracer.cli import main


class Solution:
    def canFinish(
        self, numCourses: int, prerequisites: List[Tuple[int, int]], trace: TraceRecorder | None = None
    ) -> bool:
        adjacency: Dict[int, List[int]] = {c: [] for c in range(numCourses)}
        in_degree = [0] * numCourses
        for course, prereq in prerequisites:
            adjacency[prereq].append(course)
            in_degree[course] += 1

        queue = deque(c for c in range(numCourses) if in_degree[c] == 0)
        visited: List[int] = []
        i = 0

        while queue:
            course = queue.popleft()
            visited.append(course)

            if trace:
                trace.event(f"Visit course {course}", iteration=i)
                trace.step(iteration=i, variables={"course": course, "visited": list(visited)})
                trace.snapshot_graph(adjacency, current=course, visited=visited, iteration=i)

            for nxt in adjacency[course]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    queue.append(nxt)

            if trace:
                trace.decision(
                    condition=f"in-degree of neighbors of {course} reached 0",
                    result=any(in_degree[n] == 0 for n in adjacency[course]),
                    action="Enqueue newly-unblocked courses",
                    iteration=i,
                )
            i += 1

        result = len(visited) == numCourses
        if trace:
            trace.event("All courses visited" if result else "Cycle detected — courses remain blocked")
        return result


def run(numCourses: int, prerequisites: List[Tuple[int, int]]) -> tuple[bool, TraceRecorder]:
    trace = TraceRecorder(
        "Course Schedule",
        input_data={"numCourses": numCourses, "prerequisites": prerequisites},
        difficulty="Medium",
        algorithm="Topological Sort (Kahn's / BFS)",
        time_complexity="O(V + E)",
        space_complexity="O(V + E)",
    )
    result = Solution().canFinish(numCourses, prerequisites, trace=trace)
    trace.finish(answer=result)
    return result, trace


if __name__ == "__main__":
    main(run, 4, [(1, 0), (2, 0), (3, 1), (3, 2)])
