from typing import List


class Solution:
    def trap_bruteforce(self, height: List[int]) -> int:
        total_water = 0

        for i in range(len(height)):
            # Find tallest wall on the left (including current)
            left_max = 0
            for j in range(i + 1):
                left_max = max(left_max, height[j])

            # Find tallest wall on the right (including current)
            right_max = 0
            for j in range(i, len(height)):
                right_max = max(right_max, height[j])

            # Water trapped at position i
            total_water += min(left_max, right_max) - height[i]

        return total_water

    def trap_dp(self, height: List[int]) -> int:
        n = len(height)

        leftMax = [0] * n
        rightMax = [0] * n

        leftMax[0] = height[0]
        for i in range(1, n):
            leftMax[i] = max(leftMax[i-1], height[i])

        rightMax[n-1] = height[n-1]
        for i in range(n-2, -1, -1):
            rightMax[i] = max(rightMax[i+1], height[i])

        total = 0
        for i in range(n):
            total += min(leftMax[i], rightMax[i]) - height[i]

        return total

    def trap_twopointer(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1

        leftMax = height[left]
        rightMax = height[right]

        water = 0

        while left < right:
            if leftMax < rightMax:
                # leftMax is the smaller boundary.
                # Therefore min(leftMax, rightMax) = leftMax,
                # so the water at the current left index is finalized.
                left += 1
                leftMax = max(leftMax, height[left])
                water += leftMax - height[left]
            else:
                # its because min(min(leftMax, rightMax)) so we confident moving right
                right -= 1
                rightMax = max(rightMax, height[right])
                water += rightMax - height[right]

        return water


def run_test(name, height, expected):
    for method in ("trap_bruteforce", "trap_dp", "trap_twopointer"):
        result = getattr(Solution(), method)(height)
        passed = result == expected
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name} ({method})")
        print(f"  input:    height={height}")
        print(f"  expected: {expected}")
        print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],
        6,
    )

    run_test(
        "Example 2",
        [4, 2, 0, 3, 2, 5],
        9,
    )
