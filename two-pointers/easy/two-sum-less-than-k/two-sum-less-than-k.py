from typing import List


class Solution:
    def twoSumLessThanK(self, nums: List[int], k: int) -> int:
        nums.sort()
        left = 0
        right = len(nums) - 1

        max_sum = -1

        while left < right:
            current_sum = nums[left] + nums[right]
            if current_sum < k:
                max_sum = max(max_sum, current_sum)
                left += 1
            else:
                right -= 1

        return max_sum


def run_test(name, nums, k, expected):
    result = Solution().twoSumLessThanK(nums, k)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    nums={nums}, k={k}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [34, 23, 1, 24, 75, 33, 54, 8],
        60,
        58,
    )

    run_test(
        "Example 2",
        [10, 20, 30],
        15,
        -1,
    )
