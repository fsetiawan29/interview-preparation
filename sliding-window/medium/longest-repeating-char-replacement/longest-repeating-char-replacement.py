class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        left = 0
        freq = {}
        answer = 0
        max_freq = 0

        for right in range(len(s)):
            freq[s[right]] = freq.get(s[right], 0) + 1

            max_freq = max(max_freq, freq[s[right]])

            # replacement
            while (right - left + 1) - max_freq > k:
                freq[s[left]] -= 1
                left += 1
            
            answer = max(answer, right - left + 1)

        return answer


def run_test(name, s, k, expected):
    result = Solution().characterReplacement(s, k)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}, k={k!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "ABAB",
        2,
        4,
    )

    run_test(
        "Example 2",
        "AABABBA",
        1,
        4,
    )
