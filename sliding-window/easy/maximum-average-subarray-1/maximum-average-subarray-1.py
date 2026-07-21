from typing import List


class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        left = 0
        right = k - 1
        window_sum = sum(nums[:k])
        max_average = window_sum / k

        while right < len(nums):
            average = window_sum / k
            max_average = max(max_average, average)

            if right == len(nums) - 1:
                break

            window_sum = window_sum - nums[left] + nums[right+1]
            left += 1
            right += 1

        return max_average


def run_test(name, nums, k, expected):
    result = Solution().findMaxAverage(nums, k)
    passed = abs(result - expected) < 1e-5
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    nums={nums}, k={k}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 12, -5, -6, 50, 3],
        4,
        12.75000,
    )

    run_test(
        "Example 2",
        [5],
        1,
        5.00000,
    )
