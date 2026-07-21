from typing import List


class Solution:
    def removeElement_read_write(self, nums: List[int], val: int) -> int:
        j = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[j] = nums[i]
                j += 1
        return j

    def removeElement_opposite_ends(self, nums: List[int], val: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            if nums[left] == val:
                nums[left] = nums[right]
                right -= 1
            else:
                left += 1
        
        return left


def run_test(name, fn, nums, val, expected_k, expected_nums):
    k = fn(nums, val)
    passed = k == expected_k and sorted(nums[:k]) == sorted(expected_nums[:expected_k])
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  expected: k={expected_k}, nums={expected_nums}")
    print(f"  got:      k={k}, nums={nums}")


if __name__ == "__main__":
    for label, fn in [
        ("read/write pointer", Solution().removeElement_read_write),
        ("opposite ends pointer", Solution().removeElement_opposite_ends),
    ]:
        print(f"--- {label} ---")

        run_test(
            "Example 1",
            fn,
            [3, 2, 2, 3],
            3,
            2,
            [2, 2],
        )

        run_test(
            "Example 2",
            fn,
            [0, 1, 2, 2, 3, 0, 4, 2],
            2,
            5,
            [0, 1, 4, 0, 3],
        )
