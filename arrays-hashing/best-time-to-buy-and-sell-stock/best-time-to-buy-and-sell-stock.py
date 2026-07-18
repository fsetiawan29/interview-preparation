from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        min_price = prices[0]
        for price in prices:
            min_price = min(min_price, price)
            max_profit = max(max_profit, price - min_price)
        return max_profit


def run_test(name, prices, expected):
    result = Solution().maxProfit(prices)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    prices={prices}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        [7, 1, 5, 3, 6, 4],
        5,
    )

    run_test(
        "Example 2",
        [7, 6, 4, 3, 1],
        0,
    )
