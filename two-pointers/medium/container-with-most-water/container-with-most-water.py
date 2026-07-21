from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        max_area = 0

        while left < right:
            width = right - left
            area = width * min(height[left], height[right])
            max_area = max(max_area, area)

            # Greedy:
            # Move the shorter line because moving the taller line
            # can never increase the area.
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area


def run_test(name, height, expected):
    result = Solution().maxArea(height)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    height={height}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 8, 6, 2, 5, 4, 8, 3, 7],
        49,
    )

    run_test(
        "Example 2",
        [1, 1],
        1,
    )
