from typing import List


class Solution:
    def duplicateZeros(self, arr: List[int]) -> None:
        """
        Do not return anything, modify arr in-place instead.
        """
        zeros = 0
        for a in arr:
            if a == 0:
                zeros += 1

        i = len(arr) - 1
        j = len(arr) + zeros - 1

        while i >= 0:
            if arr[i] == 0:
                if j < len(arr):
                    arr[j] = 0

                j -= 1

                if j < len(arr):
                    arr[j] = 0
                
                j -= 1
                i -= 1
            else:
                if j < len(arr):
                    arr[j] = arr[i]

                j -= 1
                i -= 1


def run_test(name, arr, expected):
    Solution().duplicateZeros(arr)
    passed = arr == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  expected: {expected}")
    print(f"  got:      {arr}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [1, 0, 2, 3, 0, 4, 5, 0],
        [1, 0, 0, 2, 3, 0, 0, 4],
    )

    run_test(
        "Example 2",
        [1, 2, 3],
        [1, 2, 3],
    )
