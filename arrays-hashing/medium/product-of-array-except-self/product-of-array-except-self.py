from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        answer = [1] * len(nums)

        running = 1
        for i in range(len(nums)):
            answer[i] = running
            running = running * nums[i]
        
        running = 1
        for i in range(len(nums)-1,-1,-1):
            answer[i] = answer[i] * running
            running = running * nums[i]
        
        return answer


def run_test(name, nums, expected):
    result = Solution().productExceptSelf(nums)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    nums={nums}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 2, 3, 4],
        [24, 12, 8, 6],
    )

    run_test(
        "Example 2",
        [-1, 1, 0, -3, 3],
        [0, 0, 9, 0, 0],
    )
