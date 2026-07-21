class Solution:
    def firstUniqChar(self, s: str) -> int:
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1
        
        for i, char in enumerate(s):
            if freq[char] == 1:
                return i
        
        return -1


def run_test(name, s, expected):
    result = Solution().firstUniqChar(s)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}")
    print(f"  expected: {expected!r}")
    print(f"  got:      {result!r}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "leetcode",
        0,
    )

    run_test(
        "Example 2",
        "loveleetcode",
        2,
    )

    run_test(
        "Example 3",
        "aabb",
        -1,
    )
