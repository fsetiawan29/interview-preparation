from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            candidate = numbers[left] + numbers[right]
            if candidate == target:
                return [left+1, right+1]
            
            if candidate > target:
                right -= 1
            else:
                left += 1


def run_test(name, numbers, target, expected):
    result = Solution().twoSum(numbers, target)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    numbers={numbers}, target={target}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [2, 7, 11, 15],
        9,
        [1, 2],
    )

    run_test(
        "Example 2",
        [2, 3, 4],
        6,
        [1, 3],
    )

    run_test(
        "Example 3",
        [-1, 0],
        -1,
        [1, 2],
    )
