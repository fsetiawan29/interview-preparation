class Solution:
    def intToRoman(self, num: int) -> str:
        values = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I")
        ]

        res = []
        for (value, symbol) in values:
            while num >= value:
                res.append(symbol)
                num -= value
        
        return "".join(res)


def run_test(name, num, expected):
    result = Solution().intToRoman(num)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    num={num}")
    print(f"  expected: {expected!r}")
    print(f"  got:      {result!r}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        3749,
        "MMMDCCXLIX",
    )

    run_test(
        "Example 2",
        58,
        "LVIII",
    )

    run_test(
        "Example 3",
        1994,
        "MCMXCIV",
    )
