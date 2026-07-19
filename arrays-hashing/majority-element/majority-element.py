from typing import List


class Solution:
    def majorityElementHashMap(self, nums: List[int]) -> int:
        threshold = len(nums) // 2
        freq = {}

        for n in nums:
            count = freq.get(n, 0) + 1
            freq[n] = count

            if count > threshold:
                return n

    def majorityElementBoyerMoore(self, nums: List[int]) -> int:
        candidate = None
        count = 0 # represent: summarize all pairwise cancellations

        for n in nums:
            if count == 0:
                candidate = n
            
            if n == candidate:
                count+=1
            else:
                count-=1
        
        return candidate


def run_test(name, nums, expected):
    for method in ("majorityElementHashMap", "majorityElementBoyerMoore"):
        result = getattr(Solution(), method)(nums)
        passed = result == expected
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name} ({method})")
        print(f"  input:    nums={nums!r}")
        print(f"  expected: {expected!r}")
        print(f"  got:      {result!r}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [3, 2, 3],
        3,
    )

    run_test(
        "Example 2",
        [2, 2, 1, 1, 1, 2, 2],
        2,
    )
