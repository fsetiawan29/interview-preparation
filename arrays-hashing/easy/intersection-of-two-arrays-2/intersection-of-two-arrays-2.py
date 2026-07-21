from typing import List


class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        freq = {}
        for n in nums1:
            freq[n] = freq.get(n, 0) + 1
        
        res = []
        for n in nums2:
            if n in freq:
                if freq[n] > 0:
                    res.append(n)
                    freq[n] -= 1
        
        return res


def run_test(name, nums1, nums2, expected):
    result = Solution().intersect(nums1, nums2)
    passed = sorted(result) == sorted(expected)
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
        [2, 2],
    )

    run_test(
        "Example 2",
        [4, 9, 5],
        [9, 4, 9, 8, 4],
        [4, 9],
    )
