class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if len(s) == 0:
            return 0
            
        left = 0
        best = 0
        seen = set()

        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1

            seen.add(s[right])
            best = max(best, right - left + 1)
        return best


def run_test(name, s, expected):
    result = Solution().lengthOfLongestSubstring(s)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "abcabcbb",
        3,
    )

    run_test(
        "Example 2",
        "bbbbb",
        1,
    )

    run_test(
        "Example 3",
        "pwwkew",
        3,
    )
