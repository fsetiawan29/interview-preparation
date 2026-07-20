from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        j = 1

        for i in range(1, len(nums)):
            if nums[i] != nums[j-1]:
                nums[j] = nums[i]
                j += 1
        
        return j


def run_test(name, nums, expected_k, expected_nums):
    k = Solution().removeDuplicates(nums)
    passed = k == expected_k and nums[:k] == expected_nums[:expected_k]
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  expected: k={expected_k}, nums={expected_nums}")
    print(f"  got:      k={k}, nums={nums}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 1, 2],
        2,
        [1, 2],
    )

    run_test(
        "Example 2",
        [0, 0, 1, 1, 1, 2, 2, 3, 3, 4],
        5,
        [0, 1, 2, 3, 4],
    )
