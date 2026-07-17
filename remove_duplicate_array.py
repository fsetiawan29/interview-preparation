from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0

        k = 1  # first element is always unique, keep it
        for i in range(1, len(nums)):
            if nums[i] != nums[k - 1]:
                nums[k] = nums[i]
                k += 1

        return k


def run_test(nums, expected):
    """Mimics the LeetCode custom judge."""
    original = nums[:]  # keep a copy for printing
    sol = Solution()
    k = sol.removeDuplicates(nums)

    passed = (k == len(expected)) and (nums[:k] == expected)

    status = "PASS" if passed else "FAIL"
    print(f"[{status}] input={original}")
    print(f"       expected k={len(expected)}, got k={k}")
    print(f"       expected nums[:k]={expected}, got nums[:k]={nums[:k]}")
    print()

    return passed


if __name__ == "__main__":
    test_cases = [
        ([1, 1, 2], [1, 2]),
        ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], [0, 1, 2, 3, 4]),
        ([1], [1]),
        ([1, 1, 1, 1], [1]),
        ([1, 2, 3], [1, 2, 3]),
    ]

    results = [run_test(nums[:], expected) for nums, expected in test_cases]

    total = len(results)
    passed = sum(results)
    print(f"Summary: {passed}/{total} test cases passed")