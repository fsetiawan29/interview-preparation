from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # count the frequency
        freq = {}
        for n in nums:
            freq[n] = freq.get(n,0) + 1

        # store in the bucket with index is the count
        buckets = [[] for _ in range(len(nums)+1)]
        for n, c in freq.items():
            buckets[c].append(n)
        
        # harvest from the buckets
        res = []
        for i in range(len(buckets) - 1, 0, -1):
            for n in buckets[i]:
                res.append(n)
                if len(res) == k:
                    return res


def run_test(name, nums, k, expected):
    result = Solution().topKFrequent(nums, k)
    passed = sorted(result) == sorted(expected) if result else False
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    nums={nums}, k={k}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 1, 1, 2, 2, 3],
        2,
        [1, 2],
    )

    run_test(
        "Example 2",
        [1],
        1,
        [1],
    )

    run_test(
        "Example 3",
        [1, 2, 1, 2, 1, 2, 3, 1, 3, 2],
        2,
        [1, 2],
    )