from typing import List


class Solution:
    def buildArray(self, target: List[int], n: int) -> List[str]:
        p = 0  # index of the next target element to match
        res = []
        for val in range(1, n + 1):
            if p == len(target):
                break

            if val == target[p]:
                res.append("Push")
                p += 1
            else:
                res.append("Push")
                res.append("Pop")

        return res


def run_test(name, target, n, expected):
    result = Solution().buildArray(target, n)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    target={target}, n={n}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 3],
        3,
        ["Push", "Push", "Pop", "Push"],
    )

    run_test(
        "Example 2",
        [1, 2, 3],
        3,
        ["Push", "Push", "Push"],
    )

    run_test(
        "Example 3",
        [1, 2],
        4,
        ["Push", "Push"],
    )
