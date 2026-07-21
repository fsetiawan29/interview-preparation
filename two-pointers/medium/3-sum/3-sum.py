from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # Sort the array
        nums.sort()

        res = []
        for i in range(len(nums)):
            # Skip duplicate first numbers to avoid duplicate triplets
            if i > 0 and nums[i] == nums[i-1]:
                continue

            left = i + 1
            right = len(nums) - 1
            while left < right:
                count = nums[i] + nums[left] + nums[right]

                if count < 0:
                    left +=1
                elif count > 0:
                    right -= 1
                else:
                    res.append([nums[i], nums[left], nums[right]])
                    # Found a valid triplet.
                    # Move both pointers to search for another pair.
                    left +=1
                    right -= 1

                    # Skip duplicate values on the left.
                    # We already used the previous left value in a triplet.
                    while left < right and nums[left] == nums[left-1]:
                        left += 1


                    # Skip duplicate values on the right.
                    # We already used the previous right value.
                    while left < right and nums[right] == nums[right+1]:
                        right -= 1
        return res


def normalize(triplets):
    return sorted(sorted(triplet) for triplet in triplets)


def run_test(name, nums, expected):
    result = Solution().threeSum(nums)
    passed = normalize(result) == normalize(expected)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    nums={nums}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [-1, 0, 1, 2, -1, -4],
        [[-1, -1, 2], [-1, 0, 1]],
    )

    run_test(
        "Example 2",
        [0, 1, 1],
        [],
    )

    run_test(
        "Example 3",
        [0, 0, 0],
        [[0, 0, 0]],
    )
