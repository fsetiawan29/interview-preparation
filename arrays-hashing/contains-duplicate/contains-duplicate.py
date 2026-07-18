from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for n in nums:
            if n in seen:
                return True
            seen.add(n)
        return False


def run_test(name, nums, expected):
    result = Solution().containsDuplicate(nums)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    nums={nums}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 2, 3, 1],
        True,
    )

    run_test(
        "Example 2",
        [1, 2, 3, 4],
        False,
    )

    run_test(
        "Example 3",
        [1, 1, 1, 3, 3, 4, 3, 2, 4, 2],
        True,
    )
