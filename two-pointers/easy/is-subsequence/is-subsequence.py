class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i = 0
        j = 0
        while i < len(t) and j < len(s):
            if t[i] == s[j]:
                j += 1
            
            i += 1
        
        return j == len(s)


def run_test(name, s, t, expected):
    result = Solution().isSubsequence(s, t)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}, t={t!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "abc",
        "ahbgdc",
        True,
    )

    run_test(
        "Example 2",
        "axc",
        "ahbgdc",
        False,
    )
