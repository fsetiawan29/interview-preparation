class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1

        for char in t:
            if char not in freq:
                return char

            if freq[char] == 0:
                return char

            freq[char] -= 1


def run_test(name, s, t, expected):
    result = Solution().findTheDifference(s, t)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}, t={t!r}")
    print(f"  expected: {expected!r}")
    print(f"  got:      {result!r}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "abcd",
        "abcde",
        "e",
    )

    run_test(
        "Example 2",
        "",
        "y",
        "y",
    )
