from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []

        def dfs(start, subset):
            result.append(subset.copy())

            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i-1]:
                    continue

                subset.append(nums[i])
                dfs(i+1, subset)
                subset.pop()

        dfs(0, [])
        return result


def run_test(name, nums, expected):
    result = Solution().subsetsWithDup(nums)
    normalize = lambda subsets: sorted(sorted(s) for s in subsets)
    passed = normalize(result) == normalize(expected)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  nums:     {nums}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test("Example 1", [1, 2, 2], [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]])
    run_test("Example 2", [0], [[], [0]])
