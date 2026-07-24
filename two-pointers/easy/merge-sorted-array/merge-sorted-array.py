from typing import List


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        i = m - 1
        j = n - 1
        w = m + n - 1

        # if one of them is exhausted, process outside
        while i >= 0 and j >= 0:
            if nums1[i] >= nums2[j]:
                nums1[w] = nums1[i]
                i -= 1
            else:
                nums1[w] = nums2[j]
                j -= 1

            w -= 1

        while j >= 0:
            nums1[w] = nums2[j]
            j -= 1
            w -= 1


def run_test(name, nums1, m, nums2, n, expected):
    Solution().merge(nums1, m, nums2, n)
    passed = nums1 == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  expected: {expected}")
    print(f"  got:      {nums1}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 2, 3, 0, 0, 0],
        3,
        [2, 5, 6],
        3,
        [1, 2, 2, 3, 5, 6],
    )

    run_test(
        "Example 2",
        [1],
        1,
        [],
        0,
        [1],
    )

    run_test(
        "Example 3",
        [0],
        0,
        [1],
        1,
        [1],
    )
