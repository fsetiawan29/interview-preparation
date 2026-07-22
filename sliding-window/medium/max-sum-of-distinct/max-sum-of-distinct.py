from typing import List


class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        left = 0
        freq = {}
        window_sum = 0
        best_sum = 0
        
        for right in range(len(nums)):
            nums_right = nums[right]
            # update freq
            freq[nums_right] = freq.get(nums_right, 0 ) + 1
            # update sum
            window_sum += nums_right

            if right - left + 1 == k:
                if len(freq) == k:
                    best_sum = max(best_sum, window_sum)
                
                nums_left = nums[left]
                # remove left number
                window_sum -= nums_left
                # update freq
                freq[nums_left] -= 1
                if freq[nums_left] == 0:
                    del freq[nums_left]

                left += 1
        
        return best_sum


def run_test(name, nums, k, expected):
    result = Solution().maximumSubarraySum(nums, k)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    nums={nums}, k={k}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 5, 4, 2, 9, 9, 9],
        3,
        15,
    )

    run_test(
        "Example 2",
        [4, 4, 4],
        3,
        0,
    )
