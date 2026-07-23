class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        if len(word1) != len(word2):
            return False
            
        freq1 = {}
        for w in word1:
            freq1[w] = freq1.get(w, 0) + 1

        freq2 = {}
        for w in word2:
            freq2[w] = freq2.get(w, 0) + 1

        return freq1.keys() == freq2.keys() and sorted(freq1.values()) == sorted(freq2.values())


def run_test(name, word1, word2, expected):
    result = Solution().closeStrings(word1, word2)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    word1={word1!r}, word2={word2!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "abc",
        "bca",
        True,
    )

    run_test(
        "Example 2",
        "a",
        "aa",
        False,
    )

    run_test(
        "Example 3",
        "cabbba",
        "abbccc",
        True,
    )
