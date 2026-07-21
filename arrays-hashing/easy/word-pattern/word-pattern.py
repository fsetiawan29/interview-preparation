class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split()

        if len(pattern) != len(words):
            return False

        mapping = {}
        seen = set()

        for char, word in zip(pattern, words):
            if char in mapping:
                if mapping[char] != word:
                    return False
            else:
                if word in seen:
                    return False
                
                mapping[char] = word
                seen.add(word)
        
        return True


def run_test(name, pattern, s, expected):
    result = Solution().wordPattern(pattern, s)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    pattern={pattern!r}, s={s!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "abba",
        "dog cat cat dog",
        True,
    )

    run_test(
        "Example 2",
        "abba",
        "dog cat cat fish",
        False,
    )

    run_test(
        "Example 3",
        "aaaa",
        "dog cat cat dog",
        False,
    )
