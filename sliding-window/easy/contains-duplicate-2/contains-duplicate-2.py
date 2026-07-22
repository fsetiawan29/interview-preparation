from typing import List


class Solution:
    def containsNearbyDuplicate_hashset(self, nums: List[int], k: int) -> bool:
        # create set window
        window = set()
        left = 0

        for right in range(len(nums)):
            if nums[right] in window:
                return True

            window.add(nums[right])

            if right - left == k:
                window.remove(nums[left])
                left += 1

        return False

    def containsNearbyDuplicate_hashmap(self, nums: List[int], k: int) -> bool:
        if k == 0:
            return False

        left = 0
        right = min(k, len(nums) - 1)

        freq = {}

        # Initialize first window
        for i in range(right + 1):
            freq[nums[i]] = freq.get(nums[i], 0) + 1
            if freq[nums[i]] == 2:
                return True

        while right < len(nums) - 1:
            # Remove left element
            left_num = nums[left]
            freq[left_num] -= 1
            if freq[left_num] == 0:
                del freq[left_num]

            # Add new right element
            right_num = nums[right + 1]
            freq[right_num] = freq.get(right_num, 0) + 1
            if freq[right_num] == 2:
                return True

            left += 1
            right += 1

        return False


def run_test(name, nums, k, expected):
    for method in ("containsNearbyDuplicate_hashset", "containsNearbyDuplicate_hashmap"):
        result = getattr(Solution(), method)(nums, k)
        passed = result == expected
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name} ({method})")
        print(f"  input:    nums={nums}, k={k}")
        print(f"  expected: {expected}")
        print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 2, 3, 1],
        3,
        True,
    )

    run_test(
        "Example 2",
        [1, 0, 1, 1],
        1,
        True,
    )

    run_test(
        "Example 3",
        [1, 2, 3, 1, 2, 3],
        2,
        False,
    )
