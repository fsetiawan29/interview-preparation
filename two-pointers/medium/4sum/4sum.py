from typing import List


class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        # sorting the array
        nums.sort()

        res = []
        for i in range(len(nums)-3):
            if i > 0 and nums[i] == nums[i-1]:
                continue

            for j in range(i+1,len(nums)-2):
                if j > i+1 and nums[j] == nums[j-1]:
                    continue

                left = j+1
                right = len(nums)-1
                while left < right:
                    total = nums[i] + nums[j] + nums[left] + nums[right]

                    if total < target:
                        left += 1
                    elif total > target:
                        right -= 1
                    else:
                        res.append([nums[i], nums[j], nums[left], nums[right]])

                        left +=1 
                        right -= 1

                        while left < right and nums[left] == nums[left-1]:
                            left +=1
                        
                        while left < right and nums[right] == nums[right+1]:
                            right -=1
        return res


def normalize(quadruplets):
    return sorted(sorted(quad) for quad in quadruplets)


def run_test(name, nums, target, expected):
    result = Solution().fourSum(nums, target)
    passed = normalize(result) == normalize(expected)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    nums={nums}, target={target}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 0, -1, 0, -2, 2],
        0,
        [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]],
    )

    run_test(
        "Example 2",
        [2, 2, 2, 2, 2],
        8,
        [[2, 2, 2, 2]],
    )
