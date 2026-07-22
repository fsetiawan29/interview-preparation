from typing import List


class Solution:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        left = 0
        right = k - 1
        window_sum = sum(arr[:k])
        limit = k * threshold

        count = 0
        while right < len(arr):
            if window_sum >= limit:
                count += 1
            
            if right == len(arr) - 1:
                break
            
            window_sum -= arr[left]
            window_sum += arr[right + 1]

            left += 1
            right += 1
        
        return count


def run_test(name, arr, k, threshold, expected):
    result = Solution().numOfSubarrays(arr, k, threshold)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    arr={arr}, k={k}, threshold={threshold}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [2, 2, 2, 2, 5, 5, 5, 8],
        3,
        4,
        3,
    )

    run_test(
        "Example 2",
        [11, 13, 17, 23, 29, 31, 7, 5, 2, 3],
        3,
        5,
        6,
    )
