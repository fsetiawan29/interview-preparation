from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        def dfs(index, subset):
            if index == len(nums):
                result.append(subset.copy())
                return
            
            # Take
            subset.append(nums[index])
            dfs(index+1, subset)

            # Backtrack
            subset.pop()

            # Skip
            dfs(index+1, subset)
        
        dfs(0, [])
        return result


def run_test(name, nums, expected):
    result = Solution().subsets(nums)
    normalize = lambda subsets: sorted(sorted(s) for s in subsets)
    passed = normalize(result) == normalize(expected)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  nums:     {nums}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test("Example 1", [1, 2, 3], [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]])
    run_test("Example 2", [0], [[], [0]])
