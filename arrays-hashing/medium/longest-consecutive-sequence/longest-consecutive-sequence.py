from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)

        longest = 0
        for n in num_set:
            if n - 1 not in num_set:
                next_num = n + 1
                length = 1
                while next_num in num_set:
                    next_num += 1
                    length += 1
                longest = max(longest, length)
        return longest


def run_test(name, nums, expected):
    result = Solution().longestConsecutive(nums)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    nums={nums}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [100, 4, 200, 1, 3, 2],
        4,
    )

    run_test(
        "Example 2",
        [0, 3, 7, 2, 5, 8, 4, 6, 0, 1],
        9,
    )

    run_test(
        "Example 3",
        [1, 0, 1, 2],
        3,
    )
