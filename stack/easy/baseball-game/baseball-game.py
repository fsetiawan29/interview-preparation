from typing import List


class Solution:
    def calPoints(self, operations: List[str]) -> int:
        stack = []
        for ch in operations:
            if ch == "C":
                stack.pop()
            elif ch == "D":
                stack.append(2 * stack[-1])
            elif ch == "+":
                stack.append(stack[-2] + stack[-1])
            else:
                stack.append(int(ch))

        return sum(stack)


def run_test(name, operations, expected):
    result = Solution().calPoints(operations)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    operations={operations}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        ["5", "2", "C", "D", "+"],
        30,
    )

    run_test(
        "Example 2",
        ["5", "-2", "4", "C", "D", "9", "+", "+"],
        27,
    )

    run_test(
        "Example 3",
        ["1", "C"],
        0,
    )
