class Solution:
    def reverseVowels(self, s: str) -> str:
        vowels = {'a', 'e', 'i', 'o', 'u'}
        l = 0
        r = len(s) - 1
        s_array = list(s)
        while l < r:
            if s_array[l].lower() not in vowels:
                l += 1
                continue

            if s_array[r].lower() not in vowels:
                r -= 1
                continue

            s_array[l], s_array[r] = s_array[r], s_array[l]
            l += 1
            r -= 1

        return "".join(s_array)


def run_test(name, s, expected):
    result = Solution().reverseVowels(s)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "IceCreAm",
        "AceCreIm",
    )

    run_test(
        "Example 2",
        "leetcode",
        "leotcede",
    )
