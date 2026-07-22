class Solution:
    VOWELS = {'a', 'e', 'i', 'o', 'u'}
    
    def maxVowels(self, s: str, k: int) -> int:
        left = 0
        right = k - 1
        window_vowels = self.countVowel(s,k)
        best = window_vowels

        while right < len(s):
            best = max(best, window_vowels)

            if right == len(s) - 1:
                break

            if self.isVowel(s[left]):
                window_vowels -= 1
            
            if self.isVowel(s[right+1]):
                window_vowels += 1

            left += 1
            right += 1

        return best
    
    def isVowel(self, char: str) -> bool:
        return char in self.VOWELS
    
    def countVowel(self, s: str, k: int) -> int:
        res = 0
        for char in s[:k]:
            if self.isVowel(char):
                res += 1
        return res


def run_test(name, s, k, expected):
    result = Solution().maxVowels(s, k)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}, k={k}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "abciiidef",
        3,
        3,
    )

    run_test(
        "Example 2",
        "aeiou",
        2,
        2,
    )

    run_test(
        "Example 3",
        "leetcode",
        3,
        2,
    )
