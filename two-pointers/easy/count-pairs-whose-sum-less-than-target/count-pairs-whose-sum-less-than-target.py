from typing import List


class Solution:
    def countPairs(self, nums: List[int], target: int) -> int:
        nums.sort()

        left = 0
        right = len(nums) - 1

        count = 0
        while left < right:
            current_sum = nums[left] + nums[right]

            if current_sum < target:
                count += right - (left+1) + 1
                left += 1
            else:
                right -= 1
        return count


def run_test(name, nums, target, expected):
    result = Solution().countPairs(nums, target)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    nums={nums}, target={target}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [-1, 1, 2, 3, 1],
        2,
        3,
    )

    run_test(
        "Example 2",
        [-6, 2, 5, -2, -7, -1, 3],
        -2,
        10,
    )
