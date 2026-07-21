from typing import List


class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        seen = set(nums1)

        res = set()
        for n in nums2:
            if n in seen:
                res.add(n)

        return list(res)


def run_test(name, nums1, nums2, expected):
    result = Solution().intersection(nums1, nums2)
    passed = set(result) == set(expected)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    nums1={nums1}, nums2={nums2}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 2, 2, 1],
        [2, 2],
        [2],
    )

    run_test(
        "Example 2",
        [4, 9, 5],
        [9, 4, 9, 8, 4],
        [9, 4],
    )
