from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
            


def run_test(name, nums, target, expected):
    result = Solution().twoSum(nums, target)
    passed = sorted(result) == sorted(expected) if result else False
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    nums={nums}, target={target}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [2, 7, 11, 15],
        9,
        [0, 1],
    )

    run_test(
        "Example 2",
        [3, 2, 4],
        6,
        [1, 2],
    )

    run_test(
        "Example 3",
        [3, 3],
        6,
        [0, 1],
    )
