from typing import List


class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        l = 0
        r = len(s) - 1
        while l < r:
            s[l], s[r] = s[r], s[l]
            l += 1
            r -= 1


def run_test(name, s, expected):
    Solution().reverseString(s)
    passed = s == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  expected: {expected}")
    print(f"  got:      {s}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        ["h", "e", "l", "l", "o"],
        ["o", "l", "l", "e", "h"],
    )

    run_test(
        "Example 2",
        ["H", "a", "n", "n", "a", "h"],
        ["h", "a", "n", "n", "a", "H"],
    )
