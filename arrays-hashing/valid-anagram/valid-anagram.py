class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        freq = {}
        for char in s:
            freq[char] = freq.get(char,0) + 1
        
        for char in t:
            freq[char] = freq.get(char,0) - 1

        for count in freq.values():
            if count != 0:
                return False
        return True


def run_test(name, s, t, expected):
    result = Solution().isAnagram(s, t)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}, t={t!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "anagram",
        "nagaram",
        True,
    )

    run_test(
        "Example 2",
        "rat",
        "car",
        False,
    )
