class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        left = 0
        right = len(s1) - 1

        window_freq = {}
        for i in range(right+1):
            window_freq[s2[i]] = window_freq.get(s2[i], 0) + 1

        freq_s1 = {}
        for ch in s1:
            freq_s1[ch] = freq_s1.get(ch, 0) + 1
        
        while True:
            if freq_s1 == window_freq:
                return True

            if right == len(s2) - 1:
                break

            right += 1
            window_freq[s2[right]] = window_freq.get(s2[right], 0) + 1

            window_freq[s2[left]] -= 1
            if window_freq[s2[left]] == 0:
                del window_freq[s2[left]]

            left += 1
        
        return False


def run_test(name, s1, s2, expected):
    result = Solution().checkInclusion(s1, s2)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s1={s1!r}, s2={s2!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "ab",
        "eidbaooo",
        True,
    )

    run_test(
        "Example 2",
        "ab",
        "eidboaoo",
        False,
    )
