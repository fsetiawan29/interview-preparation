from typing import List


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        j = 0
        for i in range(len(nums)):
            if nums[i] == 0:
                continue

            if i != j:
                nums[i], nums[j] = nums[j], nums[i]
            j += 1


def run_test(name, nums, expected):
    Solution().moveZeroes(nums)
    passed = nums == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  expected: {expected}")
    print(f"  got:      {nums}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [0, 1, 0, 3, 12],
        [1, 3, 12, 0, 0],
    )

    run_test(
        "Example 2",
        [0],
        [0],
    )
