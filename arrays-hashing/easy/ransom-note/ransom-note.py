class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False

        freq = {}
        for char in magazine:
            freq[char] = freq.get(char, 0) + 1

        for char in ransomNote:
            freq[char] = freq.get(char, 0) - 1

            if freq[char] < 0:
                return False
        
        return True


def run_test(name, ransomNote, magazine, expected):
    result = Solution().canConstruct(ransomNote, magazine)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    ransomNote={ransomNote!r}, magazine={magazine!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "a",
        "b",
        False,
    )

    run_test(
        "Example 2",
        "aa",
        "ab",
        False,
    )

    run_test(
        "Example 3",
        "aa",
        "aab",
        True,
    )
