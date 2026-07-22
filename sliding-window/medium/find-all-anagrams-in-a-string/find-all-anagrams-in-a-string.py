from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        if len(p) > len(s):
            return []

        # index
        left, right = 0, len(p) - 1
        freq_p = {}
        window_freq = {}
        for i in range(len(p)):
            freq_p[p[i]] = freq_p.get(p[i], 0) + 1
            window_freq[s[i]] = window_freq.get(s[i], 0) + 1

        res = []
        while right < len(s):
            # check two frequency count
            if window_freq == freq_p:
                res.append(left)

            if right == len(s) - 1:
                break

            # remove left value
            window_freq[s[left]] -= 1
            if window_freq[s[left]] == 0:
                del window_freq[s[left]]

            # add right value
            window_freq[s[right+1]] = window_freq.get(s[right+1], 0) + 1

            left += 1
            right += 1
        
        return res


def run_test(name, s, p, expected):
    result = Solution().findAnagrams(s, p)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}, p={p!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "cbaebabacd",
        "abc",
        [0, 6],
    )

    run_test(
        "Example 2",
        "abab",
        "ab",
        [0, 1, 2],
    )
