class Solution:
    def longestPalindrome(self, s: str) -> int:
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1
        
        result = 0
        has_odd = False
        for char, count in freq.items():
            if count % 2 == 0:
                result += count
            else:
                has_odd = True
                result += count - 1
        
        if has_odd:
            result += 1
        
        return result


def run_test(name, s, expected):
    result = Solution().longestPalindrome(s)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}")
    print(f"  expected: {expected!r}")
    print(f"  got:      {result!r}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "abccccdd",
        7,
    )

    run_test(
        "Example 2",
        "a",
        1,
    )
