class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # if len(s) != len(t):
        #     return False
        
        result = {}
        for i in range(len(s)):
            if s[i] in result:
                result[s[i]] = result[s[i]] + 1
            else:
                result[s[i]] = 1

        for i in range(len(t)):
            if t[i] in result:
                result[t[i]] = result[t[i]] - 1
            else:
                return False

        for i in result:
            if result[i] != 0:
                return False
        return True


# ---- Local test harness ----
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        # (s, t, expected, description)
        # ("anagram", "nagaram", True, "Example 1: basic anagram"),
        # ("rat", "car", False, "Example 2: not an anagram"),
        # ("a", "a", True, "single matching char"),
        ("a", "aa", False, "t longer than s, same chars"),
        # ("aa", "a", False, "s longer than t, same chars"),
        # ("ab", "ba", True, "simple 2-char swap"),
        # ("abc", "def", False, "completely different letters"),
        # ("", "", True, "both empty (edge case, constraints say len>=1 but good to check)"),
        # ("aacc", "ccac", False, "same length, different counts"),
        # ("aabbcc", "abcabc", True, "repeated letters, valid anagram"),
    ]

    passed = 0
    failed = 0

    for s, t, expected, desc in test_cases:
        try:
            actual = sol.isAnagram(s, t)
        except Exception as e:
            actual = f"ERROR: {e}"

        status = "PASS" if actual == expected else "FAIL"
        if status == "PASS":
            passed += 1
        else:
            failed += 1

        print(f"[{status}] isAnagram(s={s!r}, t={t!r}) -> {actual} (expected {expected}) | {desc}")

    print(f"\n{passed} passed, {failed} failed out of {len(test_cases)} tests")