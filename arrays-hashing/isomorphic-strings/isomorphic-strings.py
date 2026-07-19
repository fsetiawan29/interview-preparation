class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        s_to_t = {}
        t_to_s = {}

        for i in range(len(s)):
            if s[i] in s_to_t and s_to_t[s[i]] != t[i]:
                return False
            
            if t[i] in t_to_s and t_to_s[t[i]] != s[i]:
                return False
            
            s_to_t[s[i]] = t[i]
            t_to_s[t[i]] = s[i]
        
        return True


def run_test(name, s, t, expected):
    result = Solution().isIsomorphic(s, t)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}, t={t!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "egg",
        "add",
        True,
    )

    run_test(
        "Example 2",
        "f11",
        "b23",
        False,
    )

    run_test(
        "Example 3",
        "paper",
        "title",
        True,
    )
