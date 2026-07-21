from typing import List


class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        left = 0
        right = len(nums) - 1
        write = len(nums) - 1

        result = [0] * len(nums)
        while left <= right:
            if abs(nums[left]) >= abs(nums[right]):
                result[write] = nums[left] * nums[left]
                left += 1
            else:
                result[write] = nums[right] * nums[right]
                right -= 1
            
            write -= 1

        return result


def run_test(name, nums, expected):
    result = Solution().sortedSquares(nums)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [-4, -1, 0, 3, 10],
        [0, 1, 9, 16, 100],
    )

    run_test(
        "Example 2",
        [-7, -3, 2, 3, 11],
        [4, 9, 9, 49, 121],
    )
