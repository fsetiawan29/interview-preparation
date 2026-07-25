class Solution:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        i,j = 0,0
        while i < len(abbr) and j < len(word):
            if abbr[i].isalpha():
                if abbr[i] != word[j]:
                   return False
                i += 1
                j += 1
            else:
                if abbr[i] == '0':
                    return False

                skip = 0
                k = i
                while k < len(abbr) and abbr[k].isdigit():
                    skip = skip * 10 + int(abbr[k])
                    k += 1

                i = k
                j = j + skip
                if j > len(word):
                    return False
        return i == len(abbr) and j == len(word)


def run_test(name, word, abbr, expected):
    result = Solution().validWordAbbreviation(word, abbr)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    word={word!r}, abbr={abbr!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "internationalization",
        "i12iz4n",
        True,
    )

    run_test(
        "Example 2",
        "apple",
        "a2e",
        False,
    )